import streamlit as st
import time
import re

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

:root {
    --bg:        #060812;
    --surface:   rgba(255,255,255,0.035);
    --surface2:  rgba(255,255,255,0.055);
    --border:    rgba(255,255,255,0.08);
    --border-hi: rgba(255,255,255,0.18);
    --accent:    #38BDF8;
    --accent2:   #A78BFA;
    --accent3:   #34D399;
    --gold:      #FBBF24;
    --text:      #F1F5F9;
    --text2:     #CBD5E1;
    --muted:     #7C8DB5;
}

html, body, [class*="css"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif;
}
.stApp { background: transparent !important; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 2rem 4rem !important; max-width: 1100px; margin: auto; position: relative; z-index: 1; }

/* ── Animated aurora background ── */
.aurora-bg { position: fixed; inset: 0; z-index: -2; overflow: hidden; background: var(--bg); }
.aurora-blob { position: absolute; border-radius: 50%; filter: blur(110px); }
.aurora-blob.b1 { width: 620px; height: 620px; background: var(--accent); opacity: 0.22; top: -15%; left: -12%; animation: driftA 28s ease-in-out infinite alternate; }
.aurora-blob.b2 { width: 720px; height: 720px; background: var(--accent2); opacity: 0.20; bottom: -18%; right: -12%; animation: driftB 34s ease-in-out infinite alternate; }
.aurora-blob.b3 { width: 520px; height: 520px; background: var(--accent3); opacity: 0.16; top: 38%; left: 48%; animation: driftC 30s ease-in-out infinite alternate; }

@keyframes driftA { from { transform: translate(0,0) scale(1); }    to { transform: translate(130px, 90px) scale(1.18); } }
@keyframes driftB { from { transform: translate(0,0) scale(1); }    to { transform: translate(-110px,-70px) scale(1.12); } }
@keyframes driftC { from { transform: translate(-50%,-50%) scale(0.9); } to { transform: translate(-50%,-50%) translate(70px,-50px) scale(1.25); } }

@keyframes fadeInUp { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: translateY(0); } }
@keyframes gradientShift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
@keyframes blink { 50% { opacity: 0; } }
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes pulseRing {
    0%   { box-shadow: 0 0 0 0 color-mix(in srgb, var(--c) 55%, transparent); }
    70%  { box-shadow: 0 0 0 16px transparent; }
    100% { box-shadow: 0 0 0 0 transparent; }
}
@keyframes flowMove { from { transform: translateX(-120%); } to { transform: translateX(280%); } }
@keyframes popIn { from { opacity: 0; transform: scale(0.9) translateY(8px); } to { opacity: 1; transform: scale(1) translateY(0); } }

/* ── Hero ── */
.nexus-hero { text-align: center; padding: 3.5rem 1rem 1.2rem; animation: fadeInUp 0.8s ease; }
.nexus-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem; letter-spacing: 0.28em; color: var(--accent3);
    text-transform: uppercase; margin-bottom: 1rem; opacity: 0.9;
}
.nexus-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(3.2rem, 8vw, 5.6rem);
    font-weight: 800; line-height: 1.0; letter-spacing: -0.02em;
    background: linear-gradient(120deg, #38BDF8 0%, #A78BFA 35%, #34D399 65%, #38BDF8 100%);
    background-size: 300% 300%;
    -webkit-background-clip: text; background-clip: text;
    -webkit-text-fill-color: transparent; color: transparent;
    animation: gradientShift 9s ease infinite;
    margin-bottom: 0.6rem;
}
.nexus-subtitle { font-size: 1.02rem; color: var(--muted); font-weight: 400; letter-spacing: 0.02em; margin-bottom: 0; }
.nexus-divider {
    width: 64px; height: 3px; border-radius: 3px; margin: 1.8rem auto 2.4rem;
    background: linear-gradient(90deg, var(--accent), var(--accent2), var(--accent3));
    background-size: 200% 100%; animation: gradientShift 4s linear infinite;
}

/* ── Orchestration rail (signature element) ── */
.rail-wrap { animation: fadeInUp 1s ease 0.15s both; }
.rail { display: flex; align-items: center; justify-content: center; gap: 0; max-width: 760px; margin: 0 auto 0.5rem; padding: 0 1rem; }
.rail-node { display: flex; flex-direction: column; align-items: center; gap: 0.65rem; flex-shrink: 0; }
.rail-orb {
    width: 66px; height: 66px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.55rem; background: var(--surface);
    border: 2px solid var(--border); position: relative;
    transition: border-color 0.4s, background 0.4s, box-shadow 0.4s;
}
.rail-node.pending .rail-orb { opacity: 0.35; }
.rail-node.active .rail-orb {
    border-color: var(--c);
    animation: pulseRing 1.7s ease-out infinite;
}
.rail-node.active .rail-orb::before {
    content: ''; position: absolute; inset: -7px; border-radius: 50%;
    background: conic-gradient(from 0deg, var(--c), transparent 55%, var(--c));
    animation: spin 1.5s linear infinite; z-index: -1;
}
.rail-node.done .rail-orb {
    border-color: var(--c);
    background: color-mix(in srgb, var(--c) 16%, var(--surface));
    box-shadow: 0 0 26px -4px var(--c);
}
.rail-label {
    font-family: 'JetBrains Mono', monospace; font-size: 0.66rem;
    letter-spacing: 0.16em; color: var(--muted); transition: color 0.4s;
}
.rail-node.active .rail-label, .rail-node.done .rail-label { color: var(--text); }
.rail-connector {
    flex: 1; height: 2px; min-width: 28px; background: var(--border);
    margin: 0 -2px 1.85rem; position: relative; overflow: hidden; border-radius: 2px;
    transition: background 0.5s;
}
.rail-connector.flow { background: linear-gradient(90deg, var(--accent3), var(--accent)); }
.rail-connector.flow::after {
    content: ''; position: absolute; inset: 0; width: 45%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.85), transparent);
    animation: flowMove 1.6s linear infinite;
}

/* ── Terminal log ── */
.terminal {
    background: rgba(6,8,18,0.65); border: 1px solid var(--border); border-radius: 12px;
    backdrop-filter: blur(14px); margin: 1.6rem 0; overflow: hidden;
    animation: fadeInUp 0.6s ease; box-shadow: 0 12px 40px -16px rgba(0,0,0,0.6);
}
.term-header { display: flex; align-items: center; gap: 0.4rem; padding: 0.65rem 1rem; border-bottom: 1px solid var(--border); }
.term-dot { width: 10px; height: 10px; border-radius: 50%; }
.term-dot.r { background: #F87171; } .term-dot.y { background: #FBBF24; } .term-dot.g { background: #34D399; }
.term-title { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: var(--muted); margin-left: 0.6rem; letter-spacing: 0.12em; }
.term-body { padding: 1rem 1.1rem; font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: var(--text2); max-height: 230px; overflow-y: auto; }
.term-line { padding: 0.18rem 0; animation: fadeInUp 0.4s ease; white-space: pre-wrap; }
.term-line .t-tag { color: var(--muted); }
.term-line .t-ok { color: var(--accent3); }
.term-line .t-go { color: var(--accent); }
.term-cursor { display: inline-block; color: var(--accent3); animation: blink 1s step-end infinite; }

/* ── Search card ── */
.search-card {
    background: var(--surface); border: 1px solid var(--border); border-radius: 16px;
    padding: 2rem 2rem 1.6rem; margin-bottom: 2rem; position: relative; overflow: hidden;
    backdrop-filter: blur(14px); animation: fadeInUp 0.9s ease 0.05s both;
}
.search-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--accent3), var(--accent), var(--accent2), var(--gold));
    background-size: 200% 100%; animation: gradientShift 6s linear infinite;
}
.search-label {
    font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: var(--accent);
    letter-spacing: 0.2em; text-transform: uppercase; margin-bottom: 0.9rem;
}

/* ── Input ── */
div[data-testid="stTextInputRootElement"] {
    background: var(--surface2) !important; border: 1px solid var(--border-hi) !important;
    border-radius: 10px !important; transition: box-shadow 0.25s, border-color 0.25s !important;
}
div[data-testid="stTextInputRootElement"]:focus-within {
    border-color: var(--accent) !important; box-shadow: 0 0 0 4px rgba(56,189,248,0.16) !important;
}
div[data-testid="stTextInputRootElement"] input {
    background: transparent !important; color: var(--text) !important;
    font-family: 'Inter', sans-serif !important; font-size: 1rem !important; padding: 0.85rem 1.05rem !important;
    -webkit-text-fill-color: var(--text) !important;
}
div[data-testid="stTextInputRootElement"] input::placeholder { color: var(--muted) !important; }
div[data-baseweb="base-input"] { background: transparent !important; }

/* ── Button ── */
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #38BDF8, #A78BFA, #34D399) !important;
    background-size: 200% 200% !important;
    color: #06080F !important; border: none !important; border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important; font-weight: 700 !important;
    font-size: 0.95rem !important; letter-spacing: 0.06em !important;
    padding: 0.78rem 1.5rem !important; width: 100%;
    transition: transform 0.18s, box-shadow 0.25s, background-position 0.6s !important;
}
div[data-testid="stButton"] button p { color: #06080F !important; }
div[data-testid="stButton"] button:hover {
    transform: translateY(-2px) !important; background-position: 100% 50% !important;
    box-shadow: 0 10px 28px -10px rgba(56,189,248,0.55) !important;
}
div[data-testid="stButton"] button:active { transform: translateY(0) !important; }

div[data-testid="stDownloadButton"] button {
    background: var(--surface2) !important; border: 1px solid var(--border-hi) !important;
    border-radius: 10px !important; color: var(--text) !important;
    font-family: 'Syne', sans-serif !important; font-weight: 700 !important;
    transition: border-color 0.25s, transform 0.18s !important;
}
div[data-testid="stDownloadButton"] button p { color: var(--text) !important; }
div[data-testid="stDownloadButton"] button:hover {
    border-color: var(--accent3) !important; transform: translateY(-2px) !important;
}

/* ── Markdown headings inside result panels ── */
.result-panel h1, .result-panel h2, .result-panel h3 {
    font-family: 'Syne', sans-serif !important; font-weight: 700 !important;
    background: linear-gradient(120deg, var(--text), var(--text2));
    -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent; color: transparent;
    margin-top: 1.4rem !important;
}
.result-panel h2:first-child, .result-panel h3:first-child { margin-top: 0 !important; }
.result-panel p, .result-panel li { color: var(--text2); line-height: 1.7; }
.result-panel strong { color: var(--text); }
.result-panel table { border-collapse: collapse; width: 100%; }
.result-panel th, .result-panel td { border: 1px solid var(--border); padding: 0.5rem 0.8rem; }
.result-panel th { background: var(--surface2); font-family: 'Syne', sans-serif; }

/* ── Activity feed cards ── */
.activity-card {
    background: var(--surface); border: 1px solid var(--border); border-left: 3px solid var(--c);
    border-radius: 12px; padding: 1.15rem 1.4rem; margin-bottom: 0.85rem;
    backdrop-filter: blur(10px); animation: fadeInUp 0.55s ease both;
    transition: border-color 0.3s, transform 0.2s; box-shadow: 0 8px 30px -18px rgba(0,0,0,0.55);
}
.activity-card:hover { transform: translateY(-2px); border-color: var(--border-hi); }
.activity-head { display: flex; align-items: center; gap: 0.7rem; margin-bottom: 0.5rem; }
.activity-icon {
    font-size: 1.2rem; width: 34px; height: 34px; border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    background: color-mix(in srgb, var(--c) 16%, transparent); border: 1px solid color-mix(in srgb, var(--c) 35%, transparent);
}
.activity-title { font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.95rem; color: var(--text); }
.activity-time { margin-left: auto; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: var(--muted); }
.activity-snippet {
    font-size: 0.85rem; color: var(--text2); line-height: 1.6;
    display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;
}

/* ── Metric row ── */
.metric-row { display: flex; gap: 1rem; margin-top: 1.8rem; flex-wrap: wrap; }
.metric-tile {
    flex: 1; min-width: 130px; background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 1.2rem; text-align: center; position: relative; overflow: hidden;
    backdrop-filter: blur(10px); animation: popIn 0.5s ease both;
}
.metric-tile::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: var(--mc); opacity: 0.7;
}
.metric-tile:nth-child(1) { animation-delay: 0.05s; }
.metric-tile:nth-child(2) { animation-delay: 0.15s; }
.metric-tile:nth-child(3) { animation-delay: 0.25s; }
.metric-tile:nth-child(4) { animation-delay: 0.35s; }
.metric-val { font-family: 'Syne', sans-serif; font-size: 1.9rem; font-weight: 800; }
.metric-val.v1 { color: var(--accent); } .metric-val.v2 { color: var(--accent2); }
.metric-val.v3 { color: var(--accent3); } .metric-val.v4 { color: var(--gold); }
.metric-label { font-size: 0.7rem; color: var(--muted); letter-spacing: 0.1em; text-transform: uppercase; margin-top: 0.3rem; }

/* ── Result panels ── */
.result-panel {
    background: var(--surface); border: 1px solid var(--border); border-radius: 14px;
    padding: 1.9rem; margin-top: 1.6rem; backdrop-filter: blur(12px);
    animation: fadeInUp 0.7s ease both; position: relative; overflow: hidden;
}
.result-panel::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; background: var(--rc);
    background-size: 200% 100%; animation: gradientShift 5s linear infinite;
}
.result-panel-title {
    font-family: 'Syne', sans-serif; font-size: 1.08rem; font-weight: 700;
    margin-bottom: 1.15rem; padding-bottom: 0.85rem; border-bottom: 1px solid var(--border);
}

/* ── Progress ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent3), var(--accent), var(--accent2), var(--gold), var(--accent3)) !important;
    background-size: 250% 100% !important; animation: gradientShift 2.4s linear infinite !important;
}

/* ── Expanders ── */
.streamlit-expanderHeader {
    background: var(--surface) !important; border: 1px solid var(--border) !important;
    border-radius: 10px !important; color: var(--text2) !important;
    font-family: 'Syne', sans-serif !important; font-weight: 600 !important;
}
.streamlit-expanderContent {
    background: var(--surface2) !important; border: 1px solid var(--border) !important;
    border-top: none !important; border-radius: 0 0 10px 10px !important;
}

/* ── Source items ── */
.source-item {
    display: flex; flex-direction: column; gap: 0.2rem; padding: 0.75rem 1.05rem;
    margin-bottom: 0.5rem; background: var(--surface2); border: 1px solid var(--border);
    border-left: 3px solid var(--accent); border-radius: 8px; transition: border-color 0.25s, transform 0.2s;
}
.source-item:hover { border-color: var(--accent); transform: translateX(2px); }
.source-label { font-family: 'Syne', sans-serif; font-weight: 600; font-size: 0.88rem; color: var(--text); }
.source-url { font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: var(--accent); text-decoration: none; word-break: break-all; }
.source-url:hover { text-decoration: underline; color: var(--accent2); }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border-hi); border-radius: 3px; }
</style>

<div class="aurora-bg">
  <div class="aurora-blob b1"></div>
  <div class="aurora-blob b2"></div>
  <div class="aurora-blob b3"></div>
</div>
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

# ── Pipeline config ──────────────────────────────────────────────────────────
STEPS = [
    dict(key="SEARCH", icon="🔍", title="Search Agent", color="var(--accent3)",
         desc="Scanning the web for recent, reliable sources"),
    dict(key="READER", icon="📄", title="Reader Agent", color="var(--accent)",
         desc="Scraping & extracting deep content from top URLs"),
    dict(key="WRITER", icon="✍️", title="Writer Agent", color="var(--accent2)",
         desc="Synthesising findings into a structured report"),
    dict(key="CRITIC", icon="🧐", title="Critic Agent", color="var(--gold)",
         desc="Peer-reviewing for accuracy, gaps & quality"),
]


def render_rail(states):
    """states: list of 4 strings -> 'pending' | 'active' | 'done'"""
    parts = []
    for i, step in enumerate(STEPS):
        parts.append(f"""
        <div class="rail-node {states[i]}" style="--c:{step['color']}">
          <div class="rail-orb">{step['icon']}</div>
          <div class="rail-label">{step['key']}</div>
        </div>""")
        if i < len(STEPS) - 1:
            flow = "flow" if states[i] == "done" else ""
            parts.append(f'<div class="rail-connector {flow}"></div>')
    return f'<div class="rail-wrap"><div class="rail">{"".join(parts)}</div></div>'


def render_terminal(lines):
    rows = "".join(f'<div class="term-line">{l}</div>' for l in lines)
    return f"""
    <div class="terminal">
      <div class="term-header">
        <span class="term-dot r"></span><span class="term-dot y"></span><span class="term-dot g"></span>
        <span class="term-title">repilot@agents — live run</span>
      </div>
      <div class="term-body">{rows}<span class="term-cursor">▌</span></div>
    </div>"""


def render_feed(cards):
    return "".join(cards)


def activity_card(step, snippet, ts):
    snippet = (snippet or "").strip().replace("\n", " ")
    if len(snippet) > 240:
        snippet = snippet[:240].rsplit(" ", 1)[0] + " …"
    return f"""
    <div class="activity-card" style="--c:{step['color']}">
      <div class="activity-head">
        <div class="activity-icon" style="--c:{step['color']}">{step['icon']}</div>
        <div class="activity-title">{step['title']}</div>
        <div class="activity-time">{ts}</div>
      </div>
      <div class="activity-snippet">{snippet}</div>
    </div>"""


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
if "topic" not in st.session_state:
    st.session_state.topic = ""

# ── Run pipeline ──────────────────────────────────────────────────────────────
if run_clicked and topic.strip():
    st.session_state.results = None
    st.session_state.topic = topic

    from agents import build_reader_agent, build_search_agent, writer_Chain, critic_chain

    rail_ph = st.empty()
    terminal_ph = st.empty()
    progress_bar = st.progress(0)
    feed_ph = st.empty()

    states = ["pending"] * 4
    log_lines = []
    feed_cards = []
    state = {}
    start_time = time.time()

    def ts():
        return time.strftime("%H:%M:%S")

    def refresh():
        rail_ph.markdown(render_rail(states), unsafe_allow_html=True)
        terminal_ph.markdown(render_terminal(log_lines), unsafe_allow_html=True)
        feed_ph.markdown(render_feed(feed_cards), unsafe_allow_html=True)

    # initial render
    refresh()

    # ── Step 1: Search Agent ──
    states[0] = "active"
    log_lines.append(
        f'<span class="t-tag">[{ts()}]</span> <span class="t-go">▸</span> '
        f'SEARCH agent dispatched — scanning the web for &quot;{topic}&quot;'
    )
    refresh()
    progress_bar.progress(5)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_result"] = search_result['messages'][-1].content

    states[0] = "done"
    log_lines.append(
        f'<span class="t-tag">[{ts()}]</span> <span class="t-ok">✓</span> '
        f'SEARCH agent returned {len(state["search_result"]):,} chars of raw findings'
    )
    feed_cards.append(activity_card(STEPS[0], state["search_result"], ts()))
    refresh()
    progress_bar.progress(25)

    # ── Step 2: Reader Agent ──
    states[1] = "active"
    log_lines.append(
        f'<span class="t-tag">[{ts()}]</span> <span class="t-go">▸</span> '
        f'READER agent dispatched — scraping top-ranked sources for deep content'
    )
    refresh()

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URLs and scrape their content for deeper insights. "
            f"Search Results:\n{state['search_result'][:800]}"
        )]
    })
    state['Scraped_content'] = reader_result['messages'][-1].content

    states[1] = "done"
    log_lines.append(
        f'<span class="t-tag">[{ts()}]</span> <span class="t-ok">✓</span> '
        f'READER agent extracted {len(state["Scraped_content"]):,} chars of source material'
    )
    feed_cards.append(activity_card(STEPS[1], state["Scraped_content"], ts()))
    refresh()
    progress_bar.progress(50)

    # ── Step 3: Writer Chain ──
    states[2] = "active"
    log_lines.append(
        f'<span class="t-tag">[{ts()}]</span> <span class="t-go">▸</span> '
        f'WRITER chain drafting a structured research report ...'
    )
    refresh()

    research_combined = (
        f"SEARCH RESULTS:\n{state['search_result']}\n\n"
        f"DETAILED SCRAPED CONTENT:\n{state['Scraped_content']}\n\n"
    )
    state['Report'] = writer_Chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    states[2] = "done"
    log_lines.append(
        f'<span class="t-tag">[{ts()}]</span> <span class="t-ok">✓</span> '
        f'WRITER chain produced a {len(state["Report"].split()):,}-word report'
    )
    feed_cards.append(activity_card(STEPS[2], state["Report"], ts()))
    refresh()
    progress_bar.progress(75)

    # ── Step 4: Critic Chain ──
    states[3] = "active"
    log_lines.append(
        f'<span class="t-tag">[{ts()}]</span> <span class="t-go">▸</span> '
        f'CRITIC chain peer-reviewing the report for accuracy & quality ...'
    )
    refresh()

    state['Feedback'] = critic_chain.invoke({"report": state["Report"]})

    states[3] = "done"
    log_lines.append(
        f'<span class="t-tag">[{ts()}]</span> <span class="t-ok">✓</span> '
        f'CRITIC chain completed peer review — pipeline finished'
    )
    feed_cards.append(activity_card(STEPS[3], state["Feedback"], ts()))
    refresh()
    progress_bar.progress(100)

    st.session_state.results = state
    st.session_state.elapsed = round(time.time() - start_time, 1)

elif run_clicked and not topic.strip():
    st.warning("Please enter a research topic to begin.")


# ── Helpers for rendering results ───────────────────────────────────────────
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

    for m in re.finditer(r'\[([^\]]+)\]\s*[—–-]+\s*(https?://[^\s\)]+)', sources_raw):
        entries.append((m.group(1).strip(), m.group(2).strip().rstrip(')')))

    if not entries:
        for m in re.finditer(r'\[([^\]]+)\]\((https?://[^\s\)]+)\)', sources_raw):
            label = m.group(1).strip()
            url = m.group(2).strip()
            if label != url:
                entries.append((label, url))
            else:
                entries.append(("", url))

    if not entries:
        lines = [l.strip() for l in sources_raw.splitlines() if l.strip()]
        i = 0
        while i < len(lines):
            url_match = re.search(r'https?://\S+', lines[i])
            if url_match:
                url = url_match.group(0).rstrip(')')
                label = lines[i - 1] if i > 0 and not re.search(r'https?://', lines[i - 1]) else ""
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
            st.markdown(sources_raw)
    else:
        st.markdown(text)


def render_feedback(text: str):
    """Render critic feedback, stripping the internal REVIEWER SELF-CHECK block."""
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
    src_count = results.get("search_result", "").count("http")

    st.markdown(f"""
    <div class="metric-row">
      <div class="metric-tile" style="--mc:var(--accent)">
        <div class="metric-val v1">{st.session_state.elapsed}s</div>
        <div class="metric-label">Runtime</div>
      </div>
      <div class="metric-tile" style="--mc:var(--accent2)">
        <div class="metric-val v2">4</div>
        <div class="metric-label">Agents</div>
      </div>
      <div class="metric-tile" style="--mc:var(--accent3)">
        <div class="metric-val v3">{word_count:,}</div>
        <div class="metric-label">Report Words</div>
      </div>
      <div class="metric-tile" style="--mc:var(--gold)">
        <div class="metric-val v4">{src_count}</div>
        <div class="metric-label">Sources</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        '<div class="result-panel" style="--rc:linear-gradient(90deg,var(--accent3),var(--accent),var(--accent2))">',
        unsafe_allow_html=True
    )
    st.markdown('<div class="result-panel-title" style="color:var(--accent);">✍️ &nbsp;Research Report</div>',
                 unsafe_allow_html=True)
    render_report(results.get("Report", ""))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        '<div class="result-panel" style="--rc:linear-gradient(90deg,var(--gold),var(--accent2),var(--accent))">',
        unsafe_allow_html=True
    )
    st.markdown('<div class="result-panel-title" style="color:var(--gold);">🧐 &nbsp;Critic Review & Recommendations</div>',
                 unsafe_allow_html=True)
    render_feedback(results.get("Feedback", ""))
    st.markdown('</div>', unsafe_allow_html=True)

    with st.expander("🔍  Raw Search Results"):
        st.text(results.get("search_result", ""))
    with st.expander("📄  Scraped Content"):
        st.text(results.get("Scraped_content", ""))

    st.markdown("<br>", unsafe_allow_html=True)
    report_text = (
        f"RepilotAI – Research Report\nTopic: {st.session_state.topic}\n"
        f"{'='*60}\n\n{results.get('Report','')}\n\n"
        f"{'='*60}\nCRITIC FEEDBACK\n{'='*60}\n\n{results.get('Feedback','')}"
    )
    st.download_button(
        label="⬇️  Download Full Report (.txt)",
        data=report_text,
        file_name="repilotai_research_report.txt",
        mime="text/plain",
    )