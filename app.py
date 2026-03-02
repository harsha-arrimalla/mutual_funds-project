"""Streamlit app for a facts-only INDMoney mutual fund FAQ assistant."""

from html import escape

import streamlit as st

from rag import FundFactsRetriever


st.set_page_config(page_title="Mutual Fund Facts Assistant", page_icon="📘", layout="wide")

assistant = FundFactsRetriever()

EXAMPLE_QUESTIONS = [
    "Expense ratio of HDFC Large Cap Fund",
    "Exit load of SBI Large Cap Fund",
    "Minimum SIP of HDFC Flexi Cap Fund",
    "Lock-in period of SBI ELSS Fund",
]

FACT_FIELDS = [
    "Expense ratio",
    "Exit load",
    "Minimum SIP",
    "Minimum lump sum",
    "Lock-in period",
    "Riskometer",
    "Benchmark index",
    "AMC",
    "Category",
]

METRIC_KEYS = [
    ("Expense ratio", "expense_ratio"),
    ("Exit load", "exit_load"),
    ("Minimum SIP", "minimum_sip"),
    ("Lock-in", "lock_in_period"),
    ("Riskometer", "riskometer"),
    ("Benchmark", "benchmark_index"),
]

if "user_query" not in st.session_state:
    st.session_state["user_query"] = ""
if "last_result" not in st.session_state:
    st.session_state["last_result"] = None
if "last_question" not in st.session_state:
    st.session_state["last_question"] = ""
if "last_fund" not in st.session_state:
    st.session_state["last_fund"] = None
if "pending_user_query" not in st.session_state:
    st.session_state["pending_user_query"] = None


def matched_fund(query: str):
    finder = getattr(assistant, "_find_fund", None)
    if not callable(finder):
        return None
    try:
        return finder(query)
    except Exception:
        return None


def run_query(question: str) -> None:
    clean_question = (question or "").strip()
    if not clean_question:
        return

    st.session_state["last_question"] = clean_question
    with st.spinner("Fetching facts..."):
        st.session_state["last_result"] = assistant.answer(clean_question)
        st.session_state["last_fund"] = matched_fund(clean_question)


st.markdown(
    """
    <style>
      @import url("https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap");

      :root {
        --bg: #dbe3e9;
        --bg-2: #e6edf2;
        --ink: #0f1722;
        --muted: #667586;
        --accent: #00b386;
        --accent-2: #00a97d;
        --radius-xl: 20px;
        --radius-lg: 18px;
        --radius-md: 16px;
        --line: rgba(255, 255, 255, 0.38);
        --line-strong: rgba(180, 193, 206, 0.55);
        --glass: rgba(255, 255, 255, 0.55);
        --glass-strong: rgba(255, 255, 255, 0.72);
        --shadow-soft: 0 10px 30px rgba(16, 24, 36, 0.10);
        --section-gap: 1.35rem;
      }

      html, body, [class*="css"] {
        font-family: "Manrope", sans-serif;
      }

      [data-testid="stHeader"],
      [data-testid="stToolbar"],
      #MainMenu,
      footer {
        display: none !important;
      }

      [data-testid="stMainBlockContainer"] {
        padding-top: 1rem !important;
      }

      .stApp {
        background:
          radial-gradient(920px 380px at -10% -15%, rgba(0, 179, 134, 0.16) 0%, rgba(0, 179, 134, 0) 56%),
          radial-gradient(880px 360px at 110% -10%, rgba(95, 116, 255, 0.17) 0%, rgba(95, 116, 255, 0) 60%),
          linear-gradient(180deg, var(--bg-2) 0%, var(--bg) 100%);
      }

      .main .block-container {
        max-width: 1180px;
        padding-bottom: 2rem;
      }

      /* Keep vertical rhythm consistent across both columns */
      [data-testid="column"] [data-testid="stVerticalBlock"] {
        gap: var(--section-gap) !important;
      }

      .space-16 {
        height: 16px;
      }

      .space-24 {
        height: 24px;
      }

      .hero {
        background:
          radial-gradient(420px 180px at 92% 22%, rgba(119, 139, 255, 0.30) 0%, rgba(119, 139, 255, 0) 60%),
          radial-gradient(480px 170px at 7% 84%, rgba(0, 179, 134, 0.26) 0%, rgba(0, 179, 134, 0) 65%),
          linear-gradient(120deg, #0a121d 0%, #0f1c2f 52%, #182238 100%);
        border: 1px solid rgba(71, 88, 112, 0.65);
        border-radius: var(--radius-xl);
        padding: 1.25rem 1.35rem;
        box-shadow: 0 20px 44px rgba(10, 17, 28, 0.32);
      }

      .hero-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin-bottom: 0.65rem;
      }

      .hero-title {
        color: #f6f8fc;
        margin: 0;
        font-size: clamp(1.6rem, 3vw, 2.2rem);
        letter-spacing: -0.02em;
        line-height: 1.08;
        font-weight: 800;
      }

      .hero-sub {
        margin: 0.35rem 0 0;
        color: #d2dceb;
        font-size: 1rem;
        font-weight: 500;
      }

      .hero-badge {
        color: #d4ffef;
        background: rgba(0, 179, 134, 0.2);
        border: 1px solid rgba(0, 179, 134, 0.6);
        border-radius: 999px;
        padding: 0.3rem 0.75rem;
        font-size: 0.78rem;
        font-weight: 700;
        white-space: nowrap;
      }

      .glass-card {
        background: var(--glass);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid var(--line);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-soft);
      }

      .section-card {
        padding: 1.15rem 1.15rem;
      }

      .section-title {
        margin: 0;
        color: #122131 !important;
        font-size: 1.02rem;
        letter-spacing: -0.01em;
        font-weight: 800;
        text-shadow: none;
      }

      .section-copy {
        margin: 0.45rem 0 0;
        color: #5f6f82 !important;
        line-height: 1.45;
      }

      .query-wrap {
        margin-top: 0;
      }

      div[data-testid="stForm"] {
        background: var(--glass-strong);
        border: 1px solid var(--line);
        border-radius: var(--radius-lg);
        padding: 1rem;
        box-shadow: var(--shadow-soft);
      }

      div[data-testid="stForm"] .stTextInput {
        margin-bottom: 0.45rem;
      }

      div[data-testid="stForm"] .stTextInput > label {
        font-size: 0.9rem;
        font-weight: 700;
        color: #223040;
      }

      div[data-testid="stForm"] div[data-baseweb="input"] {
        border: 1px solid var(--line-strong) !important;
        border-radius: 16px !important;
        background: #ffffff !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.9), 0 4px 14px rgba(17, 24, 39, 0.05) !important;
        transition: all 0.2s ease;
      }

      div[data-testid="stForm"] div[data-baseweb="input"] > div {
        border: 0 !important;
        background: transparent !important;
      }

      div[data-testid="stForm"] div[data-baseweb="input"]:focus-within {
        border-color: rgba(0, 179, 134, 0.65) !important;
        box-shadow: 0 0 0 3px rgba(0, 179, 134, 0.18), 0 8px 22px rgba(8, 20, 33, 0.09) !important;
      }

      div[data-testid="stForm"] div[data-baseweb="input"] input {
        background: transparent !important;
        color: #12202c !important;
        -webkit-text-fill-color: #12202c !important;
        caret-color: #12202c !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        padding: 0.85rem 0.95rem !important;
      }

      div[data-testid="stForm"] div[data-baseweb="input"] input::placeholder {
        color: #91a0b0 !important;
        -webkit-text-fill-color: #91a0b0 !important;
        font-weight: 500 !important;
      }

      div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] {
        margin-top: 0.55rem;
      }

      div[data-testid="stFormSubmitButton"] button {
        border: 0 !important;
        border-radius: 14px !important;
        padding: 0.6rem 1rem !important;
        font-weight: 700 !important;
        background: linear-gradient(90deg, var(--accent-2) 0%, var(--accent) 100%) !important;
        color: #ffffff !important;
        box-shadow: 0 8px 20px rgba(0, 163, 120, 0.25) !important;
      }

      div[data-testid="stFormSubmitButton"] button:hover {
        filter: brightness(1.05);
      }

      .chip-label {
        margin: 0.2rem 0 0.55rem;
        color: #243244 !important;
        font-size: 0.85rem;
        font-weight: 700;
      }

      .stButton > button[kind="secondary"] {
        width: 100%;
        min-height: 2.7rem;
        border-radius: 999px;
        border: 1px solid rgba(176, 192, 207, 0.7);
        background: rgba(255, 255, 255, 0.78);
        color: #263548;
        font-size: 0.82rem;
        font-weight: 650;
        line-height: 1.25;
      }

      .stButton > button[kind="secondary"]:hover {
        border-color: rgba(0, 179, 134, 0.55);
        color: #056c53;
        background: rgba(240, 254, 249, 0.95);
      }

      .side-card {
        padding: 1rem 1.05rem;
        margin-bottom: 0;
      }

      .side-title {
        margin: 0;
        color: #122131 !important;
        font-size: 0.98rem;
        font-weight: 800;
        text-shadow: none;
      }

      .tag-grid {
        display: flex;
        flex-wrap: wrap;
        gap: 0.38rem;
        margin-top: 0.68rem;
      }

      .tag {
        border-radius: 999px;
        border: 1px solid rgba(172, 188, 202, 0.65);
        background: rgba(236, 242, 248, 0.78);
        color: #2a3a4b;
        padding: 0.24rem 0.58rem;
        font-size: 0.76rem;
        font-weight: 700;
      }

      .scheme-list {
        margin: 0.65rem 0 0;
        padding-left: 1rem;
        color: #2f3f52;
      }

      .scheme-list li {
        margin: 0.26rem 0;
        line-height: 1.32;
        font-size: 0.88rem;
      }

      .result-card {
        margin-top: 0;
        padding: 1.1rem 1.15rem;
        animation: riseIn 0.35s ease-out;
      }

      .result-head {
        margin-bottom: 0.85rem;
      }

      .result-title {
        margin: 0;
        color: #102131;
        font-size: 1.1rem;
        font-weight: 800;
        letter-spacing: -0.01em;
      }

      .result-meta {
        margin: 0.32rem 0 0;
        color: #617083;
        font-size: 0.9rem;
        font-weight: 600;
      }

      .metrics-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.55rem;
        margin-bottom: 0.9rem;
      }

      .metric-tile {
        border: 1px solid rgba(176, 191, 206, 0.62);
        background: rgba(255, 255, 255, 0.78);
        border-radius: 14px;
        padding: 0.58rem 0.62rem;
      }

      .metric-label {
        margin: 0;
        color: #6c7b8c;
        font-size: 0.74rem;
        font-weight: 700;
      }

      .metric-value {
        margin: 0.22rem 0 0;
        color: #112233;
        font-size: 0.94rem;
        font-weight: 800;
        line-height: 1.2;
      }

      .answer-line {
        margin: 0;
        color: #142434;
        font-size: 0.98rem;
        line-height: 1.45;
        font-weight: 600;
      }

      .result-meta-line {
        margin: 0.58rem 0 0;
        color: #526476;
        font-size: 0.9rem;
      }

      .result-meta-line a {
        color: #1068c0;
        text-decoration: none;
      }

      .result-meta-line a:hover {
        text-decoration: underline;
      }

      .disclaimer {
        margin-top: 1rem;
        padding: 0.9rem 1rem;
        border-radius: 16px;
        border: 1px solid rgba(170, 191, 207, 0.58);
        background: rgba(255, 255, 255, 0.62);
        color: #2d4255;
        line-height: 1.45;
        font-size: 0.9rem;
      }

      @keyframes riseIn {
        from {
          opacity: 0;
          transform: translateY(10px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }

      @media (max-width: 980px) {
        .metrics-grid {
          grid-template-columns: repeat(2, minmax(0, 1fr));
        }
      }

      @media (max-width: 760px) {
        .metrics-grid {
          grid-template-columns: 1fr;
        }
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <section class="hero">
      <div class="hero-top">
        <div>
          <h1 class="hero-title">Mutual Fund Facts Assistant</h1>
          <p class="hero-sub">Facts-only Mutual Fund FAQ (INDMoney sources)</p>
        </div>
        <span class="hero-badge">Facts-only</span>
      </div>
    </section>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="space-24"></div>', unsafe_allow_html=True)

main_col, side_col = st.columns([1.8, 1], gap="large")

with main_col:
    pending_query = st.session_state.get("pending_user_query")
    if pending_query:
        # Prefill must happen before the text_input widget is instantiated.
        st.session_state["user_query"] = pending_query
        st.session_state["pending_user_query"] = None

    st.markdown(
        """
        <section class="glass-card section-card">
          <h3 class="section-title">Search Scheme Facts</h3>
          <p class="section-copy">Get factual values only from official INDMoney scheme pages.</p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="space-16"></div>', unsafe_allow_html=True)

    st.markdown('<div class="query-wrap">', unsafe_allow_html=True)
    with st.form("search_form", clear_on_submit=False, enter_to_submit=True):
        st.text_input(
            "Ask your factual question",
            key="user_query",
            placeholder="Ask expense ratio, exit load, SIP, lock-in, riskometer...",
        )
        submit = st.form_submit_button("Search Facts")
    st.markdown("</div>", unsafe_allow_html=True)

    if submit:
        run_query(st.session_state.get("user_query", ""))

    st.markdown('<div class="space-16"></div>', unsafe_allow_html=True)

    st.markdown('<p class="chip-label">Example questions</p>', unsafe_allow_html=True)
    chip_cols = st.columns(4)
    for idx, question in enumerate(EXAMPLE_QUESTIONS):
        if chip_cols[idx].button(question, key=f"chip_{idx}"):
            st.session_state["pending_user_query"] = question
            run_query(question)
            st.rerun()

    result = st.session_state.get("last_result")
    if result:
        st.markdown('<div class="space-24"></div>', unsafe_allow_html=True)
        fund = st.session_state.get("last_fund")
        answer_text = escape(result["answer_text"])
        source_url = escape(result["source_url"])
        updated_note = escape(result["last_updated_from_sources"])

        if fund:
            title = escape(fund.get("fund_name", "Mutual Fund Scheme"))
            category = escape(fund.get("category", "Category not available"))
            amc = escape(fund.get("amc", "AMC not available"))
            meta_line = f"{category} | {amc}"

            metrics_html = "".join(
                f'<div class="metric-tile"><p class="metric-label">{escape(label)}</p>'
                f'<p class="metric-value">{escape(str(fund.get(key, "Not available")))}</p></div>'
                for label, key in METRIC_KEYS
            )
        else:
            title = "Assistant Response"
            meta_line = "Facts-only output"
            metrics_html = ""

        result_html = (
            '<section class="glass-card result-card">'
            '<div class="result-head">'
            f'<p class="result-title">{title}</p>'
            f'<p class="result-meta">{meta_line}</p>'
            '</div>'
            f'<div class="metrics-grid">{metrics_html}</div>'
            f'<p class="answer-line">{answer_text}</p>'
            f'<p class="result-meta-line">Source: <a href="{source_url}" target="_blank">{source_url}</a></p>'
            f'<p class="result-meta-line">Last updated from sources: {updated_note}</p>'
            '</section>'
        )
        st.markdown(result_html, unsafe_allow_html=True)

with side_col:
    field_tags = "".join(f"<span class='tag'>{escape(item)}</span>" for item in FACT_FIELDS)
    st.markdown(
        f"""
        <aside class="glass-card side-card">
          <h4 class="side-title">Covered factual fields</h4>
          <div class="tag-grid">{field_tags}</div>
        </aside>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="space-24"></div>', unsafe_allow_html=True)

    scheme_items = "".join(
        f"<li>{escape(fund.get('fund_name', 'Unknown Scheme'))}</li>" for fund in assistant.funds
    )
    st.markdown(
        f"""
        <aside class="glass-card side-card">
          <h4 class="side-title">Included schemes</h4>
          <ul class="scheme-list">{scheme_items}</ul>
        </aside>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <section class="disclaimer">
      This assistant provides factual information from official mutual fund pages. It does not provide investment advice or recommendations.
    </section>
    """,
    unsafe_allow_html=True,
)
