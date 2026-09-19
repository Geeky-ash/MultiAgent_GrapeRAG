"""Extrinsic programmatic evaluation metrics for Adaptive Agentic GraphRAG."""

import re
from typing import List, Dict, Any, Optional
from src.config import settings
from src.schema import MetricBreakdown, VerificationOutput


def calculate_faithfulness_score(response: str, context: str) -> float:
    """Calculates S_faith: ratio of sentence claims grounded in context."""
    if not response or not context:
        return 0.0
    
    # Check for refusal / insufficient context
    if "insufficient context" in response.lower():
        return 1.0

    sentences = [s.strip() for s in re.split(r"[.!?]", response) if len(s.strip()) > 10]
    if not sentences:
        return 0.8

    context_lower = context.lower()
    context_tokens = set(re.findall(r"\b[a-zA-Z0-9_-]{3,}\b", context_lower))
    supported_claims = 0

    for sentence in sentences:
        # Extract substantial keywords (ignoring stop words)
        words = re.findall(r"\b[a-zA-Z0-9_-]{3,}\b", sentence.lower())
        meaningful_words = [w for w in words if w not in {"the", "and", "this", "that", "with", "from", "for"}]
        if not meaningful_words:
            continue
        
        # Check token presence or root overlap in context
        matches = sum(
            1 for w in meaningful_words
            if w in context_lower or any(w in ct or ct in w for ct in context_tokens if len(ct) >= 4)
        )
        overlap_ratio = matches / len(meaningful_words)
        
        # If at least 50% of content tokens appear in context, claim is grounded
        if overlap_ratio >= 0.50:
            supported_claims += 1

    return round(float(supported_claims / max(1, len(sentences))), 4)


def calculate_answer_relevance_score(response: str, query: str) -> float:
    """Calculates S_ans_rel: semantic alignment between answer and query."""
    if not response or not query:
        return 0.0

    q_tokens = set(re.findall(r"\b[a-zA-Z0-9_-]{3,}\b", query.lower()))
    r_tokens = set(re.findall(r"\b[a-zA-Z0-9_-]{3,}\b", response.lower()))
    
    if not q_tokens:
        return 0.8
    
    shared = q_tokens.intersection(r_tokens)
    overlap = len(shared) / len(q_tokens)

    # Reward answering direct relational inquiries
    length_penalty = 0.0 if len(response) > 30 else -0.2
    score = min(1.0, max(0.1, (overlap * 0.7) + 0.35 + length_penalty))
    return round(float(score), 4)


def calculate_temporal_validity_score(retrieved_triples: List[Dict[str, Any]]) -> float:
    """Calculates S_temp: mean normalized edge weight of retrieved context triples."""
    if not retrieved_triples:
        return 0.85  # Default for purely vector retrieved chunks

    weights = [float(item.get("weight", 1.0)) for item in retrieved_triples]
    mean_weight = sum(weights) / len(weights)
    return round(float(min(1.0, max(0.0, mean_weight))), 4)


def evaluate_extrinsic_verification(
    response: str,
    context: str,
    query: str,
    retrieved_triples: Optional[List[Dict[str, Any]]] = None,
    threshold: Optional[float] = None,
) -> VerificationOutput:
    """Computes S_total = alpha*S_faith + beta*S_ans_rel + gamma*S_temp."""
    t_verify = threshold if threshold is not None else settings.verification_threshold
    alpha = settings.weight_faithfulness
    beta = settings.weight_answer_relevance
    gamma = settings.weight_temporal_validity

    s_faith = calculate_faithfulness_score(response, context)
    s_ans_rel = calculate_answer_relevance_score(response, query)
    s_temp = calculate_temporal_validity_score(retrieved_triples or [])

    s_total = round((alpha * s_faith) + (beta * s_ans_rel) + (gamma * s_temp), 4)
    is_verified = s_total >= t_verify

    critique = "Verification passed."
    if not is_verified:
        critique_parts = []
        if s_faith < 0.70:
            critique_parts.append(f"Low faithfulness ({s_faith:.2f}): claims not fully supported by context.")
        if s_ans_rel < 0.70:
            critique_parts.append(f"Low relevance ({s_ans_rel:.2f}): response drifts from query intent.")
        if s_temp < 0.70:
            critique_parts.append(f"Stale temporal graph edges ({s_temp:.2f}).")
        critique = " | ".join(critique_parts) if critique_parts else f"Score {s_total:.2f} below threshold {t_verify}."

    breakdown = MetricBreakdown(
        faithfulness=s_faith,
        answer_relevance=s_ans_rel,
        temporal_validity=s_temp,
        composite_score=s_total,
    )

    return VerificationOutput(
        score_total=s_total,
        is_verified=is_verified,
        metric_breakdown=breakdown,
        critique=critique,
    )
