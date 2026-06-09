import streamlit as st
import time

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Repilot – AI Powered Multi-Agent Research System",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root palette — medium dark, vivid accents ── */
:root {
    --bg:        #12151C;
    --surface:   #1C2030;
    --surface2:  #232840;
    --border:    #2D3452;
    --border-hi: #3D4870;
    --accent:    #38BDF8;
    --accent2:   #A78BFA;
    --accent3:   #34D399;
    --gold:      #FBBF24;
    --pink:      #F472B6;
    --text:      #F1F5F9;
    --text2:     #CBD5E1;
    --muted:     #7C8DB5;
    --success:   #34D399;
}

html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif;
}
.stApp { background: var(--bg) !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 4rem !important; max-width: 1100px; margin: auto; }

/* ── Hero ── */
.nexus-hero {
    text-align: center;
    padding: 3.5rem 1rem 1.8rem;
}
.nexus-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 1rem;
    opacity: 0.9;
}
.nexus-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(3rem, 7vw, 5rem);
    font-weight: 800;
    line-height: 1.0;
    background: linear-gradient(120deg, #F1F5F9 10%, #38BDF8 45%, #A78BFA 80%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.6rem;
    letter-spacing: -0.02em;
}
.nexus-subtitle {
    font-size: 1rem;
    color: var(--muted);
    font-weight: 400;
    letter-spacing: 0.03em;
    margin-bottom: 1.8rem;
}
.nexus-divider {
    width: 60px;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    margin: 0 auto 2.5rem;
    border-radius: 3px;
}

/* ── Pipeline strip ── */
.pipeline-strip {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 0;
    margin-bottom: 2.5rem;
    flex-wrap: wrap;
}
.pipe-node {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    padding: 0.5rem 1.1rem;
    border: 1px solid var(--border);
    background: var(--surface);
    font-size: 0.75rem;
    font-family: 'JetBrains Mono', monospace;
    color: var(--text2);
    letter-spacing: 0.06em;
}
.pipe-node:first-child { border-radius: 8px 0 0 8px; }
.pipe-node:last-child  { border-radius: 0 8px 8px 0; }
.pipe-arrow {
    background: var(--surface);
    border-top: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    padding: 0.5rem 0.4rem;
    color: var(--accent);
    font-size: 1rem;
}
.pipe-dot { width: 7px; height: 7px; border-radius: 50%; background: var(--border-hi); }
.pipe-dot.s { background: var(--accent3);  box-shadow: 0 0 7px var(--accent3); }
.pipe-dot.r { background: var(--accent);   box-shadow: 0 0 7px var(--accent); }
.pipe-dot.w { background: var(--accent2);  box-shadow: 0 0 7px var(--accent2); }
.pipe-dot.c { background: var(--gold);     box-shadow: 0 0 7px var(--gold); }

/* ── Search card ── */
.search-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 2rem 2rem 1.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.search-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent3), var(--accent), var(--accent2), var(--pink));
}
.search-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.68rem;
    color: var(--accent);
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

/* ── Input ── */
.stTextInput > div > div > input {
    background: var(--surface2) !important;
    border: 1px solid var(--border-hi) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.8rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(56,189,248,0.18) !important;
}
.stTextInput > div > div > input::placeholder { color: var(--muted) !important; }

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #38BDF8, #A78BFA) !important;
    color: #0D1117 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.72rem 1.5rem !important;
    width: 100%;
    transition: opacity 0.2s, transform 0.15s !important;
}
.stButton > button:hover  { opacity: 0.88 !important; transform: translateY(-1px) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* ── Step cards ── */
.step-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 0.75rem;
    transition: border-color 0.25s, background 0.25s;
}
.step-card.active  { border-color: var(--accent);   background: rgba(56,189,248,0.05); }
.step-card.done    { border-color: var(--success);  background: rgba(52,211,153,0.05); }
.step-card.pending { opacity: 0.38; }

.step-header { display: flex; align-items: center; gap: 0.8rem; margin-bottom: 0.3rem; }
.step-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.63rem;
    letter-spacing: 0.1em;
    padding: 0.18rem 0.55rem;
    border-radius: 4px;
    border: 1px solid;
}
.badge-search { color: var(--accent3); border-color: var(--accent3); background: rgba(52,211,153,0.1); }
.badge-reader { color: var(--accent);  border-color: var(--accent);  background: rgba(56,189,248,0.1); }
.badge-writer { color: var(--accent2); border-color: var(--accent2); background: rgba(167,139,250,0.1); }
.badge-critic { color: var(--gold);    border-color: var(--gold);    background: rgba(251,191,36,0.1); }

.step-title  { font-family: 'Syne', sans-serif; font-weight: 600; font-size: 0.93rem; color: var(--text); }
.step-desc   { font-size: 0.8rem; color: var(--muted); }
.step-status { margin-left: auto; font-size: 0.78rem; font-family: 'JetBrains Mono', monospace; }
.status-running { color: var(--accent); }
.status-done    { color: var(--success); }
.status-wait    { color: var(--muted); }

/* ── Metric row ── */
.metric-row { display: flex; gap: 1rem; margin-top: 1.8rem; flex-wrap: wrap; }
.metric-tile {
    flex: 1; min-width: 120px;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 1.1rem;
    text-align: center;
}
.metric-val   { font-family: 'Syne', sans-serif; font-size: 1.8rem; font-weight: 800; }
.metric-val.v1 { color: var(--accent); }
.metric-val.v2 { color: var(--accent2); }
.metric-val.v3 { color: var(--accent3); }
.metric-val.v4 { color: var(--gold); }
.metric-label { font-size: 0.7rem; color: var(--muted); letter-spacing: 0.09em; text-transform: uppercase; margin-top: 0.25rem; }

/* ── Result panels ── */
.result-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.8rem;
    margin-top: 1.5rem;
}
.result-panel-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    margin-bottom: 1.1rem;
    padding-bottom: 0.8rem;
    border-bottom: 1px solid var(--border);
}

/* ── Progress ── */
.stProgress > div > div > div { background: linear-gradient(90deg, var(--accent), var(--accent2)) !important; }

/* ── Expanders ── */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text2) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
}
.streamlit-expanderContent {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 8px 8px !important;
}

/* ── Source items ── */
.source-item {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
    padding: 0.7rem 1rem;
    margin-bottom: 0.5rem;
    background: var(--surface2);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    border-radius: 6px;
}
.source-label {
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    font-size: 0.88rem;
    color: var(--text);
}
.source-url {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: var(--accent);
    text-decoration: none;
    word-break: break-all;
}
.source-url:hover { text-decoration: underline; color: var(--accent2); }
.source-raw {
    font-size: 0.85rem;
    color: var(--text2);
    word-break: break-all;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border-hi); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nexus-hero">
  <div class="nexus-eyebrow">AI-Powered Multi-Agent Research System</div>
  <div class="nexus-title">Repilot</div>
  <div class="nexus-subtitle">Search · Read · Write · Critique &nbsp;·&nbsp; 4 Specialized Agents Working in Unison</div>
  <div class="nexus-divider"></div>
</div>
""", unsafe_allow_html=True)

# ── Pipeline strip ────────────────────────────────────────────────────────────
st.markdown("""
<div class="pipeline-strip">
  <div class="pipe-node"><span class="pipe-dot s"></span>SEARCH</div>
  <div class="pipe-arrow">›</div>
  <div class="pipe-node"><span class="pipe-dot r"></span>READER</div>
  <div class="pipe-arrow">›</div>
  <div class="pipe-node"><span class="pipe-dot w"></span>WRITER</div>
  <div class="pipe-arrow">›</div>
  <div class="pipe-node"><span class="pipe-dot c"></span>CRITIC</div>
</div>
""", unsafe_allow_html=True)

# ── Search card ───────────────────────────────────────────────────────────────
st.markdown('<div class="search-card"><div class="search-label">Research Query</div>', unsafe_allow_html=True)
col_input, col_btn = st.columns([5, 1])
with col_input:
    topic = st.text_input(
        label="",
        placeholder="e.g. AI's impact on drug discovery ...",
        key="topic_input",
        label_visibility="collapsed",
    )
with col_btn:
    st.markdown('<div style="margin-top:1.95rem;">', unsafe_allow_html=True)
    run_clicked = st.button("⚡  Run", key="run_btn")
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = None
if "elapsed" not in st.session_state:
    st.session_state.elapsed = 0

# ── Pipeline steps config ─────────────────────────────────────────────────────
STEPS = [
    ("SEARCH", "badge-search", "🔍", "Search Agent",  "Scanning the web for recent, reliable sources"),
    ("READER", "badge-reader", "📄", "Reader Agent",  "Scraping & extracting deep content from top URLs"),
    ("WRITER", "badge-writer", "✍️", "Writer Agent",  "Synthesising findings into a structured report"),
    ("CRITIC", "badge-critic", "🧐", "Critic Agent",  "Peer-reviewing for accuracy, gaps & quality"),
]

# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_clicked and topic.strip():
    st.session_state.results = None
    st.markdown("### ⚙️ Pipeline Status")

    step_placeholders = []
    for key, badge, icon, title, desc in STEPS:
        ph = st.empty()
        step_placeholders.append(ph)
        ph.markdown(f"""
        <div class="step-card pending">
          <div class="step-header">
            <span class="step-badge {badge}">{key}</span>
            <span class="step-title">{icon} {title}</span>
            <span class="step-status status-wait">waiting</span>
          </div>
          <div class="step-desc">{desc}</div>
        </div>""", unsafe_allow_html=True)

    progress_bar = st.progress(0)

    from agents import build_reader_agent, build_search_agent, writer_Chain, critic_chain

    state = {}
    start_time = time.time()

    def mark(idx, status_cls, status_text):
        key, badge, icon, title, desc = STEPS[idx]
        card_cls = "active" if status_cls == "status-running" else "done"
        step_placeholders[idx].markdown(f"""
        <div class="step-card {card_cls}">
          <div class="step-header">
            <span class="step-badge {badge}">{key}</span>
            <span class="step-title">{icon} {title}</span>
            <span class="step-status {status_cls}">{status_text}</span>
          </div>
          <div class="step-desc">{desc}</div>
        </div>""", unsafe_allow_html=True)

    # Step 1
    mark(0, "status-running", "● running")
    progress_bar.progress(5)
    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_result"] = search_result['messages'][-1].content
    mark(0, "status-done", "✓ complete")
    progress_bar.progress(25)

    # Step 2
    mark(1, "status-running", "● running")
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URLs and scrape their content for deeper insights. "
            f"Search Results:\n{state['search_result'][:800]}"
        )]
    })
    state['Scraped_content'] = reader_result['messages'][-1].content
    mark(1, "status-done", "✓ complete")
    progress_bar.progress(50)

    # Step 3
    mark(2, "status-running", "● running")
    research_combined = (
        f"SEARCH RESULTS:\n{state['search_result']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['Scraped_content']}\n\n"
    )
    state['Report'] = writer_Chain.invoke({
        "topic": topic,
        "research": research_combined
    })
    mark(2, "status-done", "✓ complete")
    progress_bar.progress(75)

    # Step 4
    mark(3, "status-running", "● running")
    state['Feedback'] = critic_chain.invoke({"report": state["Report"]})
    mark(3, "status-done", "✓ complete")
    progress_bar.progress(100)

    st.session_state.results = state
    st.session_state.elapsed = round(time.time() - start_time, 1)

elif run_clicked and not topic.strip():
    st.warning("Please enter a research topic to begin.")

# ── Helpers ───────────────────────────────────────────────────────────────────
import re

def parse_sources(sources_raw: str):
    """
    Extract (label, url) pairs from any format the LLM may output:
      1. [Title] — https://...          (em-dash format)
      2. [Title](https://...)           (markdown link)
      3. [Title](https://...) -         (markdown link with trailing dash)
      4. - [Title] — https://...        (bullet + em-dash)
      5. Bare https://... lines         (plain URL)
    Returns list of (label, url) tuples.
    """
    entries = []

    # Format 1 & 4: [Label] — URL  (em/en-dash or plain hyphen separator)
    for m in re.finditer(r'\[([^\]]+)\]\s*[—–-]+\s*(https?://[^\s\)]+)', sources_raw):
        entries.append((m.group(1).strip(), m.group(2).strip().rstrip(')')))

    # Format 2 & 3: [Label](URL)
    if not entries:
        for m in re.finditer(r'\[([^\]]+)\]\((https?://[^\s\)]+)\)', sources_raw):
            label = m.group(1).strip()
            url   = m.group(2).strip()
            # skip if label IS the url (duplicate)
            if label != url:
                entries.append((label, url))
            else:
                entries.append(("", url))

    # Format 5: bare URLs on their own lines, possibly preceded by a label line
    if not entries:
        lines = [l.strip() for l in sources_raw.splitlines() if l.strip()]
        i = 0
        while i < len(lines):
            url_match = re.search(r'https?://\S+', lines[i])
            if url_match:
                url = url_match.group(0).rstrip(')')
                # Check if previous line was a label
                label = lines[i - 1] if i > 0 and not re.search(r'https?://', lines[i - 1]) else ""
                # Clean label of bullets/brackets
                label = re.sub(r'^[-•*\[\]]+\s*', '', label).strip()
                entries.append((label, url))
            i += 1

    return entries


def render_report(text: str):
    """Render report, replacing the Sources section with clean styled cards."""
    source_pattern = re.compile(
        r'(#{1,3}\s*Sources\b[^\n]*|^\*{1,2}Sources\*{1,2}[^\n]*)',
        re.IGNORECASE | re.MULTILINE
    )
    parts = source_pattern.split(text, maxsplit=1)

    if len(parts) == 3:
        before, _heading, sources_raw = parts
        st.markdown(before)
        st.markdown("### 🔗 Sources")

        entries = parse_sources(sources_raw)

        if entries:
            for label, url in entries:
                url_clean = url.rstrip('.,)')
                display_label = label if label else url_clean
                st.markdown(f"""
<div class="source-item">
  <span class="source-label">{display_label}</span>
  <a class="source-url" href="{url_clean}" target="_blank">{url_clean}</a>
</div>""", unsafe_allow_html=True)
        else:
            # Last resort: just render raw text
            st.markdown(sources_raw)
    else:
        st.markdown(text)


def render_feedback(text: str):
    """Render critic feedback, stripping the internal REVIEWER SELF-CHECK block
    which is prompt scaffolding not meant to be shown to users."""
    cleaned = re.sub(
        r'-{3,}.*?REVIEWER SELF-CHECK.*?-{3,}',
        '',
        text,
        flags=re.DOTALL | re.IGNORECASE
    ).strip()
    st.markdown(cleaned)


# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.results:
    results = st.session_state.results
    word_count = len(results.get("Report", "").split())
    src_count  = results.get("search_result", "").count("http")

    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-tile">
        <div class="metric-val v1">{st.session_state.elapsed}s</div>
        <div class="metric-label">Runtime</div>
      </div>
      <div class="metric-tile">
        <div class="metric-val v2">4</div>
        <div class="metric-label">Agents</div>
      </div>
      <div class="metric-tile">
        <div class="metric-val v3">{word_count:,}</div>
        <div class="metric-label">Report Words</div>
      </div>
      <div class="metric-tile">
        <div class="metric-val v4">{src_count}</div>
        <div class="metric-label">Sources</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="result-panel">', unsafe_allow_html=True)
    st.markdown('<div class="result-panel-title" style="color:var(--accent);">✍️ &nbsp;Research Report</div>', unsafe_allow_html=True)
    render_report(results.get("Report", ""))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="result-panel">', unsafe_allow_html=True)
    st.markdown('<div class="result-panel-title" style="color:var(--gold);">🧐 &nbsp;Critic Review & Recommendations</div>', unsafe_allow_html=True)
    render_feedback(results.get("Feedback", ""))
    st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("🔍  Raw Search Results"):
        st.text(results.get("search_result", ""))
    with st.expander("📄  Scraped Content"):
        st.text(results.get("Scraped_content", ""))

    st.markdown("<br>", unsafe_allow_html=True)
    report_text = (
        f"RepilotAI – Research Report\nTopic: {topic}\n"
        f"{'='*60}\n\n{results.get('Report','')}\n\n"
        f"{'='*60}\nCRITIC FEEDBACK\n{'='*60}\n\n{results.get('Feedback','')}"
    )
    st.download_button(
        label="⬇️  Download Full Report (.txt)",
        data=report_text,
        file_name="repilotai_research_report.txt",
        mime="text/plain",
    )