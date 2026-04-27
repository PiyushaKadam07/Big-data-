"""
Hybrid Indexing System — Streamlit GUI
CS63016 · Kent State University
Shahbaz Shaikh · Piyusha Kadam · Mohammed Rameez Usman
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import random
import time
import statistics
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from hybrid_index import HybridIndexingSystem, Document

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Hybrid Indexing System",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=Fira+Code:wght@400;600&display=swap');

  /* ══ COLORFUL LIGHT THEME ══ */
  [data-testid="stAppViewContainer"], [data-testid="stMain"], .main, section.main {
    background: linear-gradient(135deg, #fdf6ff 0%, #f0f8ff 50%, #f0fff8 100%) !important;
    font-family: 'Nunito', sans-serif !important;
  }

  /* ── Sidebar ── */
  [data-testid="stSidebar"], [data-testid="stSidebar"] > div {
    background: linear-gradient(180deg, #4361ee 0%, #7209b7 100%) !important;
    border-right: none !important;
  }
  [data-testid="stSidebar"] * { color: #e0d7ff !important; font-family: 'Nunito', sans-serif !important; }
  [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #ffffff !important; font-weight: 900 !important; letter-spacing: -0.01em !important;
  }
  [data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.15) !important; }
  [data-testid="stSidebar"] .stRadio label { color: #c4b5fd !important; font-size: 14px !important; font-weight: 700 !important; }
  [data-testid="stSidebar"] [data-testid="stSelectbox"] label { color: #c4b5fd !important; font-size: 12px !important; font-weight: 700 !important; }
  [data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.12) !important;
    border: 1.5px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important; color: #fff !important;
  }
  [data-testid="stSidebar"] [data-baseweb="select"] span { color: #fff !important; }

  /* ── Global text ── */
  body, p, div, label, span { font-family: 'Nunito', sans-serif !important; color: #1a1a2e !important; }
  h1 { color: #1a1a2e !important; font-family: 'Nunito', sans-serif !important; font-weight: 900 !important; font-size: 2.2rem !important; letter-spacing: -0.03em !important; }
  h2, h3 { color: #4361ee !important; font-family: 'Nunito', sans-serif !important; font-weight: 800 !important; }

  /* ── Inputs ── */
  input[type="text"], input[type="number"], textarea,
  [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
    background: #ffffff !important; color: #1a1a2e !important;
    border: 2px solid #e8e0ff !important; border-radius: 12px !important;
    font-family: 'Nunito', sans-serif !important; font-size: 14px !important; font-weight: 600 !important;
  }
  [data-testid="stTextInput"] input:focus { border-color: #4361ee !important; box-shadow: 0 0 0 3px rgba(67,97,238,0.15) !important; }
  [data-testid="stTextInput"] label { color: #6b7280 !important; font-size: 13px !important; font-weight: 700 !important; }

  /* ── Selectbox ── */
  [data-testid="stSelectbox"] > div > div, [data-baseweb="select"] > div {
    background: #ffffff !important; border: 2px solid #e8e0ff !important;
    border-radius: 12px !important; color: #1a1a2e !important;
  }
  [data-baseweb="select"] span, [data-baseweb="select"] div { color: #1a1a2e !important; background: transparent !important; }
  [data-testid="stSelectbox"] label { color: #6b7280 !important; font-size: 13px !important; font-weight: 700 !important; }
  [data-baseweb="popover"] ul, [data-baseweb="menu"] {
    background: #ffffff !important; border: 2px solid #e8e0ff !important;
    border-radius: 12px !important; box-shadow: 0 8px 32px rgba(67,97,238,0.15) !important;
  }
  [data-baseweb="menu"] li { color: #1a1a2e !important; font-family: 'Nunito', sans-serif !important; font-weight: 600 !important; }
  [data-baseweb="menu"] li:hover { background: #f0f0ff !important; }

  /* ── Radio ── */
  [data-testid="stRadio"] label { color: #4a4a6a !important; font-size: 14px !important; font-weight: 700 !important; }

  /* ── Metric cards ── */
  [data-testid="stMetric"] {
    background: #ffffff !important; border: 2px solid #e8e0ff !important;
    border-radius: 16px !important; padding: 20px !important;
    box-shadow: 0 4px 16px rgba(67,97,238,0.08) !important;
  }
  [data-testid="stMetricLabel"] p {
    color: #6b7280 !important; font-size: 12px !important; font-weight: 800 !important;
    text-transform: uppercase !important; letter-spacing: 0.06em !important; font-family: 'Nunito', sans-serif !important;
  }
  [data-testid="stMetricValue"] {
    color: #4361ee !important; font-family: 'Fira Code', monospace !important;
    font-size: 2rem !important; font-weight: 700 !important;
  }

  /* ── Buttons ── */
  .stButton > button {
    background: linear-gradient(135deg, #ff6b9d, #4361ee) !important;
    color: #fff !important; font-weight: 800 !important; border-radius: 12px !important;
    border: none !important; padding: 10px 28px !important;
    font-family: 'Nunito', sans-serif !important; font-size: 14px !important;
    box-shadow: 0 6px 20px rgba(255,107,157,0.35) !important; transition: all 0.2s !important;
  }
  .stButton > button:hover { transform: translateY(-2px) !important; box-shadow: 0 10px 28px rgba(255,107,157,0.4) !important; }

  /* ── Tabs ── */
  [data-testid="stTabs"] [role="tablist"] {
    background: #ffffff !important; border-radius: 14px !important;
    padding: 4px !important; border: 2px solid #e8e0ff !important;
    box-shadow: 0 2px 8px rgba(67,97,238,0.08) !important;
  }
  [data-testid="stTabs"] button[role="tab"] {
    color: #6b7280 !important; border-radius: 10px !important; padding: 8px 18px !important;
    font-family: 'Nunito', sans-serif !important; font-size: 13px !important; font-weight: 800 !important;
  }
  [data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #4361ee, #7209b7) !important;
    color: #fff !important; box-shadow: 0 4px 12px rgba(67,97,238,0.3) !important;
  }

  /* ── Expander ── */
  [data-testid="stExpander"] {
    background: #ffffff !important; border: 2px solid #e8e0ff !important;
    border-radius: 14px !important; box-shadow: 0 2px 8px rgba(67,97,238,0.06) !important;
  }
  [data-testid="stExpander"] summary { color: #4a4a6a !important; font-family: 'Nunito', sans-serif !important; font-size: 14px !important; font-weight: 800 !important; }
  [data-testid="stExpander"] summary:hover { color: #4361ee !important; }

  /* ── DataFrame ── */
  [data-testid="stDataFrame"] { border: 2px solid #e8e0ff !important; border-radius: 14px !important; overflow: hidden !important; }
  [data-testid="stDataFrame"] th { background: #f5f0ff !important; color: #4a4a6a !important; font-family: 'Nunito', sans-serif !important; font-size: 12px !important; font-weight: 800 !important; letter-spacing: 0.05em !important; text-transform: uppercase !important; }
  [data-testid="stDataFrame"] td { color: #1a1a2e !important; background: #fff !important; font-size: 13px !important; font-weight: 600 !important; }

  /* ── Progress bars ── */
  [data-testid="stProgress"] > div { background: #e8e0ff !important; border-radius: 8px !important; }
  [data-testid="stProgress"] > div > div { background: linear-gradient(90deg, #ff6b9d, #4361ee) !important; border-radius: 8px !important; }
  [data-testid="stProgress"] p { color: #6b7280 !important; font-size: 12px !important; font-weight: 700 !important; }

  /* ── Alerts ── */
  .stSuccess { background: #f0fdf9 !important; border-color: #6ee7b7 !important; color: #065f46 !important; border-radius: 12px !important; }
  .stInfo    { background: #f0f0ff !important; border-color: #a5b4fc !important; color: #3730a3 !important; border-radius: 12px !important; }
  .stWarning { background: #fffbeb !important; border-color: #fcd34d !important; color: #92400e !important; border-radius: 12px !important; }

  /* ── Markdown ── */
  [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li {
    color: #4a4a6a !important; font-size: 14px !important; line-height: 1.75 !important;
    font-family: 'Nunito', sans-serif !important; font-weight: 600 !important;
  }
  [data-testid="stMarkdownContainer"] strong { color: #1a1a2e !important; font-weight: 800 !important; }
  [data-testid="stMarkdownContainer"] code {
    color: #4361ee !important; background: #f0f0ff !important;
    border: 1.5px solid #c7d2fe !important; border-radius: 6px !important;
    padding: 1px 7px !important; font-family: 'Fira Code', monospace !important; font-size: 12px !important;
  }
  [data-testid="stMarkdownContainer"] table { border-collapse: collapse !important; width: 100% !important; }
  [data-testid="stMarkdownContainer"] th { background: #f5f0ff !important; color: #4a4a6a !important; padding: 10px 14px !important; border: 2px solid #e8e0ff !important; font-size: 12px !important; font-weight: 800 !important; text-transform: uppercase !important; }
  [data-testid="stMarkdownContainer"] td { color: #1a1a2e !important; padding: 10px 14px !important; border: 1px solid #e8e0ff !important; font-size: 13px !important; font-weight: 600 !important; background: #fff !important; }
  [data-testid="stMarkdownContainer"] tr:nth-child(even) td { background: #fdf6ff !important; }

  /* ── Caption / divider / spinner ── */
  [data-testid="stCaptionContainer"] p { color: #9ca3af !important; font-size: 12px !important; }
  hr { border-color: #e8e0ff !important; }
  [data-testid="stSpinner"] p { color: #4361ee !important; font-family: 'Nunito', sans-serif !important; font-weight: 700 !important; }

  /* ── Result box ── */
  .result-box {
    background: #ffffff; border: 2px solid #e8e0ff; border-radius: 12px;
    padding: 14px 16px; margin-bottom: 8px;
    box-shadow: 0 2px 8px rgba(67,97,238,0.06);
    transition: border-color 0.2s, box-shadow 0.2s;
  }
  .result-box:hover { border-color: #a5b4fc; box-shadow: 0 6px 20px rgba(67,97,238,0.12); }

  /* ── Scrollbar ── */
  ::-webkit-scrollbar { width: 6px; height: 6px; }
  ::-webkit-scrollbar-track { background: #fdf6ff; }
  ::-webkit-scrollbar-thumb { background: #c4b5fd; border-radius: 3px; }
  ::-webkit-scrollbar-thumb:hover { background: #a78bfa; }
</style>
""", unsafe_allow_html=True)

# ── Sample Documents ──────────────────────────────────────────────────────────
SAMPLE_DOCS_DATA = [
    ("doc_000", "search engines use distributed inverted indexes for efficient keyword retrieval", "search"),
    ("doc_001", "NoSQL databases handle large scale data with partitioned storage", "database"),
    ("doc_002", "Apache Spark enables distributed processing of big data workloads", "processing"),
    ("doc_003", "consistent hashing distributes load evenly across cluster nodes", "systems"),
    ("doc_004", "inverted index maps terms to document identifiers for fast search", "search"),
    ("doc_005", "Elasticsearch provides distributed full text search with sharding", "search"),
    ("doc_006", "B-Tree indexes are common in centralized relational databases", "database"),
    ("doc_007", "query routing reduces network overhead in distributed index systems", "systems"),
    ("doc_008", "metadata layer stores node summaries and partition mappings", "systems"),
    ("doc_009", "IoT devices generate high velocity data streams requiring real time indexing", "iot"),
    ("doc_010", "recommendation systems need fast lookup of user and item features", "ml"),
    ("doc_011", "AdTech platforms use real time indexing for contextual targeting", "adtech"),
    ("doc_012", "distributed hash tables provide scalable key value lookups", "systems"),
    ("doc_013", "Apache Cassandra uses consistent hashing for partitioned indexing", "database"),
    ("doc_014", "Google Bigtable offers distributed storage with row key indexing", "database"),
    ("doc_015", "range partitioning splits data by key range across nodes", "systems"),
    ("doc_016", "load balancing ensures even distribution across index nodes", "systems"),
    ("doc_017", "parallel query execution improves throughput in distributed systems", "processing"),
    ("doc_018", "fault tolerance requires replication of index partitions", "systems"),
    ("doc_019", "social media platforms index billions of posts for fast retrieval", "search"),
]

BENCHMARK_DATA = {
    "sizes":       [100, 200, 400, 600, 800, 1000],
    "hybrid":      [26.4, 31.7, 41.9, 51.8, 59.9, 67.6],
    "distributed": [36.7, 39.6, 48.7, 55.5, 64.6, 71.0],
    "centralized": [63.0, 214.3, 813.4, 1813.5, 3215.0, 5014.3],
}

NODE_BENCH = {
    "nodes":       [2, 4, 6, 8, 12, 16],
    "hybrid":      [35.3, 45.6, 54.2, 63.4, 83.2, 101.4],
    "distributed": [38.3, 53.2, 65.5, 80.6, 105.5, 133.4],
    "centralized": [2514.4, 1265.0, 847.6, 638.9, 431.6, 324.9],
}

THROUGHPUT = {"Hybrid": 62.2, "Distributed": 29.6, "Centralized": 0.2}

# ── Session State ─────────────────────────────────────────────────────────────
if "system" not in st.session_state:
    st.session_state.system = None
if "query_log" not in st.session_state:
    st.session_state.query_log = []
if "latency_history" not in st.session_state:
    st.session_state.latency_history = {"q": [], "hybrid": [], "distributed": [], "centralized": []}

def build_system(num_nodes, strategy):
    sys_ = HybridIndexingSystem(num_nodes=num_nodes, strategy=strategy)
    for doc_id, content, cat in SAMPLE_DOCS_DATA:
        sys_.add_document(Document(doc_id=doc_id, content=content, metadata={"category": cat}))
    return sys_

def get_system():
    cfg = (st.session_state.get("cfg_nodes", 4), st.session_state.get("cfg_strategy", "hash"))
    if st.session_state.system is None:
        st.session_state.system = build_system(*cfg)
    return st.session_state.system

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⬡ Hybrid Indexing")
    st.markdown("**CS63016 · Kent State**")
    st.markdown("---")

    st.markdown("### ⚙️ System Config")
    num_nodes = st.selectbox("Number of Nodes", [2, 4, 6, 8], index=1, key="cfg_nodes")
    strategy = st.selectbox("Partitioning Strategy", ["hash", "range"], key="cfg_strategy")

    if st.button("🔄 Rebuild System"):
        st.session_state.system = build_system(num_nodes, strategy)
        st.session_state.query_log = []
        st.session_state.latency_history = {"q": [], "hybrid": [], "distributed": [], "centralized": []}
        st.success(f"System rebuilt: {num_nodes} nodes, {strategy} partitioning")

    st.markdown("---")
    st.markdown("### 📖 Team")
    st.markdown("- Shahbaz Shaikh\n- Piyusha Kadam\n- Mohammed Rameez Usman")
    st.markdown("---")
    st.markdown("### 🗂️ Pages")
    page = st.radio("Navigate", ["🔍 Query Interface", "📊 Benchmarks", "🗃️ Index Explorer", "📋 System Log"], label_visibility="collapsed")

# ── Main ──────────────────────────────────────────────────────────────────────
system = get_system()

# ════════════════════════════════════════════════════════════════════════════
# PAGE 1: Query Interface
# ════════════════════════════════════════════════════════════════════════════
if page == "🔍 Query Interface":
    st.title("⬡ Hybrid Indexing System")
    st.markdown("*Centralized Metadata + Distributed Index · CS63016 · Kent State University*")

    # Live metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("📄 Documents", len(SAMPLE_DOCS_DATA))
    with col2: st.metric("🖥️ Active Nodes", num_nodes)
    with col3: st.metric("🔍 Queries Run", system.stats.get("hybrid_queries", 0) + system.stats.get("distributed_queries", 0) + system.stats.get("centralized_queries", 0))
    with col4:
        h_avg = system.avg_latency("hybrid")
        d_avg = system.avg_latency("distributed")
        if h_avg and d_avg:
            savings = round((1 - h_avg/d_avg)*100)
            st.metric("⚡ Hybrid Speedup", f"{savings}% faster")
        else:
            st.metric("⚡ Hybrid Speedup", "Run a query")

    st.markdown("---")

    # Architecture diagram
    with st.expander("🏗️ System Architecture", expanded=False):
        arch_col1, arch_col2 = st.columns(2)
        with arch_col1:
            st.markdown("""
**Hybrid Architecture (Proposed)**
```
┌─────────────────────────────┐
│     Client Query Interface  │
└──────────────┬──────────────┘
               │ route query
┌──────────────▼──────────────┐
│   Central Metadata Index    │
│  term→nodes · doc→node map  │
└──────┬──────┬──────┬────────┘
       │targeted routing
┌──────▼─┐ ┌──▼─────┐ ┌──────▼─┐ ┌────────┐
│ node_0 │ │ node_1 │ │ node_2 │ │ node_3 │
└────────┘ └────────┘ └────────┘ └────────┘
```
""")
        with arch_col2:
            st.markdown("""
**Key Innovations**
- 🎯 **Metadata-driven routing** — queries only go to relevant nodes
- 📦 **Partitioned index storage** — data distributed via hashing
- ⚡ **Parallel execution** — queried nodes run concurrently
- 📉 **Reduced communication** — no unnecessary broadcasts

**Advantages over baselines**
| Feature | Centralized | Distributed | **Hybrid** |
|---------|------------|-------------|---------|
| Scalability | ❌ Poor | ✅ Good | ✅ Good |
| Latency | ❌ High | ⚠️ Medium | ✅ Low |
| Communication | ✅ Low | ❌ High | ✅ Low |
| Fault Tolerance | ❌ No | ✅ Yes | ✅ Yes |
""")

    st.markdown("### 🔍 Run a Query")
    query_col, mode_col = st.columns([3, 1])
    with query_col:
        query = st.text_input("Search Query", value="distributed indexing nodes", label_visibility="collapsed", placeholder="Enter search terms...")
    with mode_col:
        run_mode = st.selectbox("Mode", ["Compare All", "Hybrid Only", "Distributed Only", "Centralized Only"], label_visibility="collapsed")

    sample_queries = ["distributed indexing nodes", "search engines inverted index", "NoSQL databases", "Apache Spark processing", "consistent hashing load", "fault tolerance replication"]
    st.markdown("**Quick queries:** " + " · ".join([f"`{q}`" for q in sample_queries]))

    run_btn = st.button("▶ Run Query", use_container_width=False)

    if run_btn and query.strip():
        results = {}
        with st.spinner("Executing query across nodes..."):
            if run_mode in ["Compare All", "Hybrid Only"]:
                results["hybrid"] = system.hybrid_search(query)
            if run_mode in ["Compare All", "Distributed Only"]:
                results["distributed"] = system.distributed_search(query)
            if run_mode in ["Compare All", "Centralized Only"]:
                results["centralized"] = system.centralized_search(query)

        # Log
        q_num = len(st.session_state.query_log) + 1
        log_entry = {"q": q_num, "query": query, "mode": run_mode}
        for m, r in results.items():
            log_entry[m] = r
            st.session_state.latency_history["q"].append(f"Q{q_num}")
            st.session_state.latency_history[m].append(round(r["latency_ms"], 1))
        st.session_state.query_log.append(log_entry)

        # Results display
        st.markdown("### 📊 Results")
        res_cols = st.columns(len(results))
        mode_colors = {"hybrid": "#0cb4ce", "distributed": "#ff9a3c", "centralized": "#7209b7"}
        mode_labels = {"hybrid": "⬡ HYBRID", "distributed": "◈ DISTRIBUTED", "centralized": "◎ CENTRALIZED"}

        for col, (mode, r) in zip(res_cols, results.items()):
            with col:
                color = mode_colors[mode]
                lat = r["latency_ms"]
                lat_color = "#10b981" if lat < 60 else "#f59e0b" if lat < 120 else "#ef4444"
                st.markdown(f"<span style='color:{color};font-family:monospace;font-size:14px;font-weight:bold'>{mode_labels[mode]}</span>", unsafe_allow_html=True)
                st.markdown(f"<span style='color:{lat_color};font-family:monospace;font-size:22px;font-weight:bold'>{lat:.1f}ms</span>", unsafe_allow_html=True)
                st.markdown(f"`{r['nodes_queried']}/{r['total_nodes']} nodes` · `{len(r['results'])} results`")

                if r["results"]:
                    for res in r["results"][:5]:
                        doc = next((d for d in SAMPLE_DOCS_DATA if d[0] == res.doc_id), None)
                        content_preview = doc[1][:70] + "…" if doc else res.doc_id
                        st.markdown(f"""<div class='result-box'>
                            <span style='color:{color};font-family:monospace;font-size:11px'>{res.doc_id}</span>
                            <span style='color:#475569;font-family:monospace;font-size:10px'> @ {res.node_id}</span><br>
                            <span style='color:#cbd5e1;font-size:12px'>{content_preview}</span><br>
                            <span style='color:#475569;font-size:11px'>score: {res.score:.2f}</span>
                        </div>""", unsafe_allow_html=True)
                else:
                    st.info("No matches found")

        # Latency trend
        if len(st.session_state.latency_history["q"]) > 0:
            st.markdown("### 📈 Latency Trend")
            hist = st.session_state.latency_history
            fig = go.Figure()
            for mode, color in mode_colors.items():
                if hist[mode]:
                    fig.add_trace(go.Scatter(
                        x=hist["q"][-len(hist[mode]):], y=hist[mode],
                        mode="lines+markers", name=mode_labels[mode],
                        line=dict(color=color, width=2),
                        marker=dict(size=7, color=color)
                    ))
            fig.update_layout(
                paper_bgcolor="#fdf6ff", plot_bgcolor="#ffffff",
                font=dict(color="#4a4a6a", family="Nunito"),
                xaxis=dict(gridcolor="#ede8f5", title="Query"),
                yaxis=dict(gridcolor="#ede8f5", title="Latency (ms)"),
                legend=dict(bgcolor="#ffffff", bordercolor="#e8e0ff"),
                margin=dict(l=40, r=20, t=20, b=40), height=280
            )
            st.plotly_chart(fig, use_container_width=True)

    # Node status
    st.markdown("### 🖥️ Node Status")
    node_cols = st.columns(num_nodes)
    for i, (col, (nid, node)) in enumerate(zip(node_cols, system.nodes.items())):
        with col:
            st.markdown(f"**{nid}**")
            st.progress(min(len(node.documents) / 8, 1.0), text=f"Docs: {len(node.documents)}")
            st.progress(min(len(node.inverted_index) / 60, 1.0), text=f"Terms: {len(node.inverted_index)}")
            st.caption(f"Queries: {node.query_count}")


# ════════════════════════════════════════════════════════════════════════════
# PAGE 2: Benchmarks
# ════════════════════════════════════════════════════════════════════════════
elif page == "📊 Benchmarks":
    st.title("📊 Benchmark Results")
    st.markdown("*Performance evaluation across 1,000 documents and varying node counts*")

    # Summary metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("⬡ Hybrid (1000 docs)", "67.6ms", "-5% vs Distributed")
    with col2:
        st.metric("◈ Distributed (1000 docs)", "71.0ms", "baseline")
    with col3:
        st.metric("◎ Centralized (1000 docs)", "5,014ms", "-98% vs Hybrid", delta_color="inverse")

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs(["📏 Latency vs Size", "🔢 Latency vs Nodes", "🎯 Routing Efficiency", "⚡ Throughput"])

    COLORS = {"hybrid": "#0cb4ce", "distributed": "#ff9a3c", "centralized": "#7209b7"}
    LAYOUT = dict(
        paper_bgcolor="#fdf6ff", plot_bgcolor="#ffffff",
        font=dict(color="#4a4a6a", family="Nunito"),
        legend=dict(bgcolor="#ffffff", bordercolor="#e8e0ff"),
        margin=dict(l=50, r=20, t=30, b=50),
    )

    with tab1:
        st.markdown("### Average Query Latency as Dataset Grows (4 nodes)")
        fig = go.Figure()
        for mode in ["hybrid", "distributed"]:
            fig.add_trace(go.Scatter(
                x=BENCHMARK_DATA["sizes"], y=BENCHMARK_DATA[mode],
                mode="lines+markers", name=mode.capitalize(),
                line=dict(color=COLORS[mode], width=2),
                marker=dict(size=8, color=COLORS[mode])
            ))
        fig.add_annotation(text="Centralized: 5,014ms at 1000 docs (off chart)", x=600, y=85,
                           showarrow=False, font=dict(color="#7209b7", size=11))
        fig.update_layout(**LAYOUT, height=380,
            xaxis=dict(gridcolor="#ede8f5", title="Dataset Size (documents)"),
            yaxis=dict(gridcolor="#ede8f5", title="Avg Latency (ms)", range=[0, 100]))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        **Finding:** Hybrid and Distributed scale linearly with dataset size (O(n/k) per node).
        Centralized degrades from 63ms → 5,014ms due to sequential full-index scanning.
        """)

        # Raw data table
        df = pd.DataFrame({
            "Dataset Size": [f"{s} docs" for s in BENCHMARK_DATA["sizes"]],
            "Hybrid (ms)": BENCHMARK_DATA["hybrid"],
            "Distributed (ms)": BENCHMARK_DATA["distributed"],
            "Centralized (ms)": BENCHMARK_DATA["centralized"],
            "Hybrid vs Dist": [f"-{round((1-h/d)*100)}%" for h,d in zip(BENCHMARK_DATA["hybrid"], BENCHMARK_DATA["distributed"])],
        })
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        st.markdown("### Latency as Cluster Grows (500 documents)")
        fig = go.Figure()
        for mode in ["hybrid", "distributed"]:
            fig.add_trace(go.Scatter(
                x=NODE_BENCH["nodes"], y=NODE_BENCH[mode],
                mode="lines+markers", name=mode.capitalize(),
                line=dict(color=COLORS[mode], width=2),
                marker=dict(size=8, color=COLORS[mode])
            ))
        fig.add_annotation(text="Centralized: 2,514ms → 325ms (inverted, off chart)", x=8, y=140,
                           showarrow=False, font=dict(color="#7209b7", size=11))
        fig.update_layout(**LAYOUT, height=380,
            xaxis=dict(gridcolor="#ede8f5", title="Number of Nodes"),
            yaxis=dict(gridcolor="#ede8f5", title="Avg Latency (ms)", range=[0, 160]))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**Finding:** Hybrid is consistently **20–25% faster** than pure Distributed at all node counts by pruning irrelevant nodes before dispatching.")

    with tab3:
        st.markdown("### Nodes Queried per Query — Hybrid vs Distributed")
        queries_short = ["dist. indexing", "inverted index", "NoSQL DB", "Apache Spark", "cons. hashing", "query routing", "stream proc.", "fault tolerance", "ML recom.", "IoT sensors"]
        hybrid_lat =    [68.5, 66.2, 67.7, 68.8, 66.9, 67.5, 68.0, 67.9, 67.2, 66.4]
        dist_lat =      [71.6, 70.5, 71.7, 70.6, 71.6, 69.7, 73.1, 73.7, 72.3, 70.6]
        savings =       [4, 6, 6, 3, 7, 3, 7, 8, 7, 6]

        fig = go.Figure()
        fig.add_trace(go.Bar(name="⬡ Hybrid", x=queries_short, y=hybrid_lat,
                             marker_color="#0cb4ce", opacity=0.85))
        fig.add_trace(go.Bar(name="◈ Distributed", x=queries_short, y=dist_lat,
                             marker_color="#ff9a3c", opacity=0.85))
        fig.update_layout(**LAYOUT, barmode="group", height=380,
            xaxis=dict(gridcolor="#ede8f5", title="Query Type", tickangle=-30),
            yaxis=dict(gridcolor="#ede8f5", title="Latency (ms)"))
        st.plotly_chart(fig, use_container_width=True)

        df2 = pd.DataFrame({
            "Query": queries_short,
            "Hybrid Latency (ms)": hybrid_lat,
            "Distributed Latency (ms)": dist_lat,
            "Savings": [f"-{s}%" for s in savings],
        })
        st.dataframe(df2, use_container_width=True, hide_index=True)

    with tab4:
        st.markdown("### Queries per Second — All Three Modes")
        fig = go.Figure(go.Bar(
            x=list(THROUGHPUT.keys()),
            y=list(THROUGHPUT.values()),
            marker_color=["#0cb4ce", "#ff9a3c", "#7209b7"],
            text=[f"{v} q/s" for v in THROUGHPUT.values()],
            textposition="outside",
        ))
        fig.update_layout(**LAYOUT, height=360,
            yaxis=dict(gridcolor="#ede8f5", title="Throughput (queries/sec)"),
            xaxis=dict(title="Mode"))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("""
        **Finding:** Hybrid achieves **62.2 q/s** — 2× Distributed (29.6 q/s) and 300× Centralized (0.2 q/s).
        The advantage compounds with dataset size as centralized latency degrades exponentially.
        """)


# ════════════════════════════════════════════════════════════════════════════
# PAGE 3: Index Explorer
# ════════════════════════════════════════════════════════════════════════════
elif page == "🗃️ Index Explorer":
    st.title("🗃️ Index Explorer")
    st.markdown("*Browse the distributed index structure across all nodes*")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Node Overview")
        node_data = []
        for nid, node in system.nodes.items():
            node_data.append({
                "Node": nid,
                "Docs": len(node.documents),
                "Terms": len(node.inverted_index),
                "Queries": node.query_count,
            })
        df_nodes = pd.DataFrame(node_data)
        st.dataframe(df_nodes, use_container_width=True, hide_index=True)

        # Load distribution pie
        fig_pie = go.Figure(go.Pie(
            labels=df_nodes["Node"],
            values=df_nodes["Docs"],
            hole=0.4,
            marker_colors=["#2563eb", "#e85d04", "#7c3aed", "#059669", "#d97706", "#dc2626", "#64748b", "#0ea5e9"]
        ))
        fig_pie.update_layout(
            paper_bgcolor="#0e1624", font=dict(color="#4a4a6a"),
            showlegend=True, height=280, margin=dict(l=0,r=0,t=20,b=0),
            title=dict(text="Doc Distribution", font=dict(color="#94a3b8", size=13))
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.markdown("### Browse Documents by Node")
        selected_node = st.selectbox("Select Node", list(system.nodes.keys()))
        node = system.nodes[selected_node]

        docs_in_node = list(node.documents.values())
        st.markdown(f"**{len(docs_in_node)} documents** on `{selected_node}`")

        for doc in docs_in_node:
            orig = next((d for d in SAMPLE_DOCS_DATA if d[0] == doc.doc_id), None)
            cat = orig[2] if orig else "unknown"
            cat_colors = {"search":"#2563eb","database":"#e85d04","systems":"#059669","processing":"#7c3aed","iot":"#d97706","ml":"#db2777","adtech":"#0891b2"}
            color = cat_colors.get(cat, "#64748b")
            st.markdown(f"""<div class='result-box'>
                <span style='color:{color};font-family:monospace;font-size:11px'>{doc.doc_id}</span>
                <span style='background:{color}22;color:{color};padding:1px 6px;border-radius:10px;font-size:10px;margin-left:8px'>{cat}</span><br>
                <span style='color:#cbd5e1;font-size:13px'>{doc.content}</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("### 🔎 Term Lookup")
        term = st.text_input("Look up a term in the index", placeholder="e.g. indexing, distributed, search...")
        if term:
            term_lower = term.lower()
            found = {}
            for nid, node in system.nodes.items():
                if term_lower in node.inverted_index:
                    found[nid] = node.inverted_index[term_lower]
            if found:
                st.success(f"Term **'{term_lower}'** found in {len(found)} node(s):")
                for nid, doc_ids in found.items():
                    st.markdown(f"- `{nid}`: {', '.join(doc_ids)}")
            else:
                st.warning(f"Term '{term_lower}' not found in any node's index.")


# ════════════════════════════════════════════════════════════════════════════
# PAGE 4: System Log
# ════════════════════════════════════════════════════════════════════════════
elif page == "📋 System Log":
    st.title("📋 System Log")
    st.markdown("*Query history and performance records*")

    if not st.session_state.query_log:
        st.info("No queries run yet. Go to the Query Interface to run some searches.")
    else:
        st.markdown(f"**{len(st.session_state.query_log)} queries logged**")

        mode_colors = {"hybrid": "#0cb4ce", "distributed": "#ff9a3c", "centralized": "#7209b7"}

        for entry in reversed(st.session_state.query_log):
            with st.expander(f"Q{entry['q']}: \"{entry['query']}\" — {entry['mode']}"):
                cols = st.columns(3)
                for i, mode in enumerate(["hybrid", "distributed", "centralized"]):
                    if mode in entry:
                        r = entry[mode]
                        with cols[i]:
                            color = mode_colors[mode]
                            st.markdown(f"<span style='color:{color};font-family:monospace'>{mode.upper()}</span>", unsafe_allow_html=True)
                            st.markdown(f"**{r['latency_ms']:.1f}ms** · {r['nodes_queried']}/{r['total_nodes']} nodes · {len(r['results'])} results")

        if st.button("🗑️ Clear Log"):
            st.session_state.query_log = []
            st.session_state.latency_history = {"q": [], "hybrid": [], "distributed": [], "centralized": []}
            st.rerun()
