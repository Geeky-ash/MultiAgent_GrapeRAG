# Adaptive-Agentic-GraphRAG

Adaptive Agentic GraphRAG is a production-ready, enterprise-grade Retrieval-Augmented Generation (RAG) framework designed to eliminate hallucinations in regulated domains. It dynamically routes queries across vector and knowledge graph backends, prunes stale relations via temporal exponential decay, verifies answers programmatically via extrinsic metrics (RAGAS), and executes in a bounded LangGraph multi-agent state machine.

---

## Key Features

- ⚡ **Dynamic Policy Routing ($C(Q)$):** Evaluates query complexity continuously using a logistic model, routing dynamically to Vector (`ChromaDB`), Knowledge Graph (`Neo4j`), or Hybrid (`RRF`).
- ⏳ **Temporal Edge Decay:** Prunes outdated knowledge graph relations with $w(e, t) = w_0 \cdot \exp(-\lambda (t_0 - t_e))$ where $w(e, t) < 0.30$.
- 🛡️ **Extrinsic Verification Gating ($S_{\text{total}}$):** Programmatically scores answers using claim faithfulness, answer relevance, and temporal freshness ($S_{\text{total}} \ge 0.75$).
- 🔄 **LangGraph Reflection Loop:** Enforces self-correction loops bounded by a strict maximum retry limit ($N_{\text{retry}} = 3$) with deterministic fallback.
- 🖥️ **Streamlit Telemetry Console:** Interactive UI featuring live modality indicators, dynamic Cypher/Vector similarity inspectors, GraphViz subgraph visualizers, and state trace auditing.
- 📦 **Zero Hardcoded Prompts & Strict Typing:** All prompts centralized in `src/config.py`, 100% Pydantic/typing coverage, and $< 250$ LOC per file.

---

## Project Structure

```
adaptive_graphrag/
├── .env.example
├── docker-compose.yml
├── requirements.txt
├── README.md
├── PRD.md
├── AGENTS.md
├── DESIGN.md
├── ARCHITECTURE.md
├── RULES.md
├── MEMORY.md
├── DECISIONS.md
├── TESTING.md
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── schema.py
│   ├── routing.py
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── vector_store.py
│   │   └── graph_store.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── planner.py
│   │   ├── generator.py
│   │   └── verifier.py
│   ├── workflow/
│   │   ├── __init__.py
│   │   └── state_machine.py
│   └── utils/
│       ├── __init__.py
│       └── metrics.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_routing.py
│   ├── test_graph.py
│   └── test_workflow.py
└── ui/
    └── app.py
```

---

## Quickstart

### 1. Environment Setup
```bash
# Clone and enter the repository
cd adaptive_graphrag

# Create virtual environment
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
```

### 2. Launch Storage Backends via Docker Compose (Optional)
```bash
docker compose up -d neo4j chromadb
```
*Note: The system contains built-in in-memory fallbacks, allowing test suites and the UI to run seamlessly even without active Docker containers!*

### 3. Run Unit Tests
```bash
pytest tests/ -v
```

### 4. Launch Streamlit UI
```bash
streamlit run ui/app.py
```
Open your browser at `http://localhost:8501` to access the interactive console.
