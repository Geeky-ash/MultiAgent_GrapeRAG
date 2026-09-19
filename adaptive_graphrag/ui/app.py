"""Adaptive Agentic GraphRAG - Two-Column Enterprise Defense Console."""

import asyncio
import time
from typing import Dict, Any
import streamlit as st

try:
    import graphviz
    HAS_GRAPHVIZ = True
except ImportError:
    graphviz = None
    HAS_GRAPHVIZ = False

from src.config import settings
from src.routing import calculate_query_complexity, determine_routing_strategy
from src.workflow.state_machine import execute_graphrag_pipeline
from ui.styles import CUSTOM_CSS

st.set_page_config(page_title="Adaptive Agentic GraphRAG", page_icon="🕸️", layout="wide", initial_sidebar_state="collapsed")
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# Top Telemetry Header
st.markdown("""
<div class="telemetry-header">
    <div style="font-size: 20px; font-weight: 700; color: #F0F6FC;">
        🕸️ Adaptive Agentic GraphRAG <span style="font-size: 14px; color: #8B949E; font-weight: 400;">| Defense Console</span>
    </div>
    <div class="telemetry-badge"><span class="pulse-dot"></span>SYSTEM ONLINE | LANGGRAPH READY</div>
</div>
""", unsafe_allow_html=True)

# State initialization
if "last_state" not in st.session_state:
    st.session_state["last_state"] = None
if "current_query" not in st.session_state:
    st.session_state["current_query"] = "Trace all supply chain dependencies connecting ASML to TSMC and Apple."
if "exec_latency" not in st.session_state:
    st.session_state["exec_latency"] = 0.0

last_state: Dict[str, Any] = st.session_state["last_state"] or {}
v_score = last_state.get("verification_score", 0.0)
last_modality = str(last_state.get("routing_strategy", "HYBRID")).upper() if last_state else "STANDBY"
lat_display = f"{st.session_state['exec_latency']:.1f}ms" if st.session_state["exec_latency"] > 0 else "< 40ms"

# Two-Column Dashboard Grid
col1, col2 = st.columns([2, 3], gap="medium")

# --- LEFT COLUMN: Input & Telemetry Controls ---
with col1:
    # 3 Compact KPI Cards
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi-card"><div class="kpi-label">Latency SLA</div><div class="kpi-value">{lat_display}</div></div>
        <div class="kpi-card"><div class="kpi-label">Active Modality</div><div class="kpi-value" style="color:#58A6FF;">{last_modality}</div></div>
        <div class="kpi-card"><div class="kpi-label">Verify S_total</div><div class="kpi-value" style="color:#3FB950;">{v_score:.3f}</div></div>
    </div>
    """, unsafe_allow_html=True)

    # Sample Query Pills
    st.caption("Quick Test Presets:")
    p_c1, p_c2 = st.columns(2)
    if p_c1.button("⚡ Apple Revenue", use_container_width=True):
        st.session_state["current_query"] = "What is the primary revenue stream of Apple?"
    if p_c2.button("🕸️ ASML-TSMC-Apple", use_container_width=True):
        st.session_state["current_query"] = "Trace all supply chain dependencies connecting ASML to TSMC and Apple."

    # Query Textarea
    query = st.text_area("Investigation Query Prompt", value=st.session_state["current_query"], height=95)
    st.session_state["current_query"] = query

    # Dynamic Glowing Modality Badge
    c_q = calculate_query_complexity(query)
    strategy = determine_routing_strategy(c_q)
    badge_html = f"<span class='badge-{strategy}'>{strategy.upper()} ROUTING</span>"
    st.markdown(f"<div style='margin: 8px 0 14px 0;'><b>Complexity C(Q):</b> <code>{c_q:.4f}</code> &nbsp;|&nbsp; {badge_html}</div>", unsafe_allow_html=True)

    # Execute Button
    run_btn = st.button("🚀 Execute Adaptive Pipeline", type="primary", use_container_width=True)

    # Hyperparameter Expander
    with st.expander("⚙️ Guardrail Configuration", expanded=False):
        settings.verification_threshold = st.slider("Threshold (T_verify)", 0.50, 0.95, settings.verification_threshold, 0.05)
        settings.max_retry_count = st.slider("Max Retries (N_retry)", 1, 5, settings.max_retry_count, 1)

# Pipeline Execution Trigger
if run_btn:
    with st.spinner("Executing LangGraph multi-agent traversal..."):
        t0 = time.perf_counter()
        final_state = asyncio.run(execute_graphrag_pipeline(query))
        st.session_state["exec_latency"] = (time.perf_counter() - t0) * 1000
        st.session_state["last_state"] = final_state
        st.rerun()

# --- RIGHT COLUMN: Synthesized Response & Visualizer Tabs ---
with col2:
    st.markdown("#### Synthesized Natural Language Intelligence")
    if last_state:
        response_text = last_state.get("generated_response", "No response generated.")
        st.markdown(f"<div class='response-card'>\n\n{response_text}\n\n</div>", unsafe_allow_html=True)
    else:
        st.info("Select a query and click 'Execute Adaptive Pipeline' to view synthesized intelligence.")

    # Workspace Tabs
    tab_graph, tab_trace, tab_metrics, tab_json = st.tabs([
        "🕸️ Knowledge Subgraph",
        "🔄 Agent Trace",
        "📊 Verification Metrics",
        "📋 Raw JSON"
    ])

    with tab_graph:
        triples = last_state.get("retrieved_graph_triples", [])
        if triples and HAS_GRAPHVIZ and graphviz is not None:
            dot = graphviz.Digraph()
            dot.attr(bgcolor="#0D1117", rankdir="LR")
            dot.attr("node", shape="box", style="filled,rounded", fillcolor="#161B22", fontcolor="#58A6FF", color="#388BFD", fontname="sans-serif")
            dot.attr("edge", color="#6E7681", fontcolor="#C9D1D9", fontsize="10", fontname="sans-serif")
            for t in triples:
                dot.edge(str(t.get("subject")), str(t.get("object")), label=f"{t.get('predicate')}\n[w={t.get('weight', 1.0):.2f}]")
            st.graphviz_chart(dot, use_container_width=True)
        elif triples:
            for t in triples:
                st.markdown(f"- **{t.get('subject')}** ──_{t.get('predicate')}_ (w={t.get('weight', 1.0):.2f})──> **{t.get('object')}**")
        else:
            st.caption("No knowledge graph triples retrieved for this query mode.")

    with tab_trace:
        trace = last_state.get("execution_trace", [])
        durations = {step.get("node"): f"{step.get('duration_ms', 0):.2f}ms" for step in trace}
        st.markdown(f"""
        <div class="step-tracker">
            <div class="step-item"><div class="step-title">1. Planner</div><div class="step-time">{durations.get('planner', '-')}</div></div>
            <div class="step-arrow">➔</div>
            <div class="step-item"><div class="step-title">2. Retriever</div><div class="step-time">{durations.get('retriever', '-')}</div></div>
            <div class="step-arrow">➔</div>
            <div class="step-item"><div class="step-title">3. Generator</div><div class="step-time">{durations.get('generator', '-')}</div></div>
            <div class="step-arrow">➔</div>
            <div class="step-item"><div class="step-title">4. Verifier</div><div class="step-time">{durations.get('verifier', '-')}</div></div>
        </div>
        """, unsafe_allow_html=True)
        if trace:
            st.dataframe(trace, use_container_width=True)

    with tab_metrics:
        mb = last_state.get("metric_breakdown", {})
        sf = mb.get("faithfulness", 1.0 if last_state else 0.0)
        sar = mb.get("answer_relevance", 0.8 if last_state else 0.0)
        st_val = mb.get("temporal_validity", 0.85 if last_state else 0.0)
        st.markdown(f"**Faithfulness $S_{{\\text{{faith}}}}$ (0.50):** `{sf:.3f}`")
        st.progress(min(1.0, max(0.0, sf)))
        st.markdown(f"**Answer Relevance $S_{{\\text{{ans\\_rel}}}}$ (0.30):** `{sar:.3f}`")
        st.progress(min(1.0, max(0.0, sar)))
        st.markdown(f"**Temporal Freshness $S_{{\\text{{temp}}}}$ (0.20):** `{st_val:.3f}`")
        st.progress(min(1.0, max(0.0, st_val)))
        st.markdown(f"**Composite $S_{{\\text{{total}}}}$:** `{v_score:.3f}` &nbsp;|&nbsp; Target: `{settings.verification_threshold:.2f}`")

    with tab_json:
        if last_state:
            st.json(last_state)
        else:
            st.caption("No active state dictionary.")
