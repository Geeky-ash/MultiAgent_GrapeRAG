"""Unit tests for multi-agent workflow, verification metrics, and fallback handling."""

import pytest
from src.utils.metrics import (
    calculate_faithfulness_score,
    calculate_answer_relevance_score,
    calculate_temporal_validity_score,
    evaluate_extrinsic_verification,
)
from src.workflow.state_machine import (
    execute_graphrag_pipeline,
    verifier_conditional_router,
)


def test_extrinsic_verification_math():
    """Validates composite formula: S_total = 0.5*S_faith + 0.3*S_ans_rel + 0.2*S_temp."""
    response = "TSMC manufactures advanced microchips for Apple."
    context = "[Doc2]: TSMC manufactures custom silicon including chips for Apple."
    query = "Who manufactures chips for Apple?"
    triples = [{"weight": 0.90}, {"weight": 0.85}]

    output = evaluate_extrinsic_verification(
        response=response,
        context=context,
        query=query,
        retrieved_triples=triples,
        threshold=0.75,
    )

    expected = round(
        (0.50 * output.metric_breakdown.faithfulness) +
        (0.30 * output.metric_breakdown.answer_relevance) +
        (0.20 * output.metric_breakdown.temporal_validity),
        4
    )
    assert abs(output.score_total - expected) < 1e-4
    assert output.is_verified is True


def test_verifier_conditional_router():
    """Tests branching decisions: 'end', 'reflect', or 'fallback'."""
    # Case 1: Pass
    state_pass = {"verification_score": 0.85, "retry_count": 0}
    assert verifier_conditional_router(state_pass) == "end"

    # Case 2: Fail with retries remaining
    state_reflect = {"verification_score": 0.50, "retry_count": 1}
    assert verifier_conditional_router(state_reflect) == "reflect"

    # Case 3: Retries exhausted
    state_fallback = {"verification_score": 0.50, "retry_count": 3}
    assert verifier_conditional_router(state_fallback) == "fallback"


@pytest.mark.asyncio
async def test_end_to_end_pipeline_execution():
    """Validates complete execution through LangGraph state machine."""
    query = "What is the role of an attention head in Transformer architectures?"
    final_state = await execute_graphrag_pipeline(query)

    assert final_state is not None
    assert "generated_response" in final_state
    assert len(final_state["generated_response"]) > 0
    assert "routing_strategy" in final_state
    assert final_state["verification_score"] >= 0.0
    assert len(final_state["execution_trace"]) >= 4

    # Verify execution visited planner, retriever, generator, verifier
    visited_nodes = [step["node"] for step in final_state["execution_trace"]]
    assert "planner" in visited_nodes
    assert "retriever" in visited_nodes
    assert "generator" in visited_nodes
    assert "verifier" in visited_nodes
