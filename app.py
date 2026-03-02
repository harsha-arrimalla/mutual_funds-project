"""Streamlit app for a facts-only INDMoney mutual fund FAQ assistant."""

from html import escape

import streamlit as st

from rag import FundFactsRetriever


st.set_page_config(page_title="Mutual Fund Facts Assistant", page_icon="📘", layout="wide")

assistant = FundFactsRetriever()

EXAMPLE_QUESTIONS = [
    "Expense ratio of HDFC Large Cap Fund",
    "Lock-in period of SBI ELSS Fund",
    "Minimum SIP of HDFC Flexi Cap Fund",
]

SUPPORTED_SCHEMES = [
    "HDFC Large Cap Fund",
    "HDFC Flexi Cap Fund",
    "SBI Large Cap Fund",
    "ICICI Prudential Large Cap Fund",
    "SBI ELSS Tax Saver Fund",
    "Parag Parikh Flexi Cap Fund",
]

if "user_question" not in st.session_state:
    st.session_state["user_question"] = ""
if "last_result" not in st.session_state:
    st.session_state["last_result"] = None
if "last_question" not in st.session_state:
    st.session_state["last_question"] = ""


def run_query(question: str) -> None:
    clean_question = (question or "").strip()
    if not clean_question:
        return
    st.session_state["last_question"] = clean_question
    st.session_state["last_result"] = assistant.answer(clean_question)


st.markdown(
    """
    <style>
      @import url("https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap");

      :root {
        --bg: #eef2f5;
        --bg-soft: #f7fafc;
        --surface: #ffffff;
        --line: #d7e0e8;
        --ink: #10151b;
        --muted: #5a6674;
        --ind-green: #00b386;
        --ind-green-ink: #056a52;
        --ind-dark: #0d131a;
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

      .stApp {
        background:
          radial-gradient(1000px 420px at -10% -20%, rgba(0, 179, 134, 0.18) 0%, rgba(0, 179, 134, 0) 55%),
          radial-gradient(900px 360px at 115% -30%, rgba(57, 99, 255, 0.16) 0%, rgba(57, 99, 255, 0) 60%),
          var(--bg);
      }

      .main .block-container {
        max-width: 1080px;
        padding-top: 0 !important;
        margin-top: 0 !important;
        padding-bottom: 2.5rem;
      }

      [data-testid="stAppViewContainer"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
      }

      [data-testid="stAppViewContainer"] > .main {
        padding-top: 0 !important;
        margin-top: 0 !important;
      }

      [data-testid="stAppViewContainer"] .main .block-container {
        padding-top: 0 !important;
      }

      /* Streamlit runtime class seen in current build; force-remove top gap */
      .st-emotion-cache-zy6yx3 {
        padding-top: 0 !important;
      }

      /* Stable selector fallback across Streamlit versions */
      [data-testid="stMainBlockContainer"] {
        padding-top: 0 !important;
        margin-top: 0 !important;
      }

      .ind-topbar {
        margin-left: calc(50% - 50vw);
        margin-right: calc(50% - 50vw);
        background: linear-gradient(90deg, #050a14 0%, #0c1726 55%, #121927 100%);
        border-bottom: 1px solid #1f314e;
        box-shadow: 0 10px 30px rgba(8, 16, 28, 0.22);
      }

      /*
        Streamlit's vertical stack uses `gap: 1rem`; a hidden first node can
        leave an apparent empty strip above the first visible block. Remove only
        that initial visual gap without changing spacing elsewhere.
      */
      .element-container:has(.ind-topbar) {
        margin-top: -1rem !important;
      }

      .ind-topbar-inner {
        max-width: 1080px;
        margin: 0 auto;
        padding: 0.92rem 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
      }

      .brand {
        display: flex;
        align-items: center;
        gap: 0.65rem;
      }

      .brand img {
        width: 31px;
        height: 31px;
        border-radius: 999px;
        background: #ffffff;
        padding: 2px;
      }

      .brand-name {
        color: #f5f8ff;
        font-weight: 700;
        letter-spacing: 0.015em;
        font-size: 0.94rem;
      }

      .brand-pill {
        color: #b4f8e6;
        border: 1px solid rgba(0, 179, 134, 0.55);
        background: rgba(0, 179, 134, 0.18);
        border-radius: 999px;
        padding: 0.16rem 0.56rem;
        font-size: 0.72rem;
        font-weight: 700;
      }

      .hero {
        margin-top: 1.15rem;
        margin-bottom: 1rem;
        background:
          radial-gradient(420px 180px at 90% 20%, rgba(108, 127, 255, 0.22) 0%, rgba(108, 127, 255, 0) 60%),
          radial-gradient(420px 180px at 8% 80%, rgba(0, 179, 134, 0.23) 0%, rgba(0, 179, 134, 0) 63%),
          linear-gradient(135deg, #0f151d 0%, #1b2430 100%);
        border: 1px solid #2a3340;
        border-radius: 30px;
        padding: 1.45rem 1.5rem;
        box-shadow: 0 24px 50px rgba(12, 19, 30, 0.26);
      }

      .hero-grid {
        display: grid;
        grid-template-columns: 1.5fr 1fr;
        gap: 1rem;
        align-items: end;
      }

      .hero-title {
        color: #f9fbff;
        margin: 0;
        font-weight: 800;
        letter-spacing: -0.02em;
        line-height: 1.07;
        font-size: clamp(1.7rem, 3vw, 2.4rem);
      }

      .hero-sub {
        color: #d5dde8;
        margin: 0.55rem 0 0;
        max-width: 670px;
        line-height: 1.45;
      }

      .hero-metric-wrap {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.52rem;
      }

      .hero-metric {
        border: 1px solid rgba(215, 229, 255, 0.25);
        background: rgba(255, 255, 255, 0.07);
        border-radius: 14px;
        padding: 0.62rem 0.56rem;
        text-align: center;
      }

      .hero-metric strong {
        display: block;
        color: #f2f7ff;
        font-size: 0.84rem;
        line-height: 1.25;
      }

      .hero-metric span {
        display: block;
        color: #a8b7c9;
        margin-top: 0.15rem;
        font-size: 0.72rem;
      }

      .panel {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 22px;
        padding: 1rem 1.1rem;
        box-shadow: 0 12px 28px rgba(19, 25, 35, 0.08);
      }

      .panel-title {
        color: var(--ink);
        margin: 0;
        font-size: 1.03rem;
        font-weight: 800;
        letter-spacing: -0.01em;
      }

      .panel-copy {
        color: var(--muted);
        margin: 0.5rem 0 0;
        line-height: 1.45;
        font-size: 0.98rem;
      }

      .section-label {
        margin: 1rem 0 0.45rem;
        color: var(--ink);
        font-size: 0.92rem;
        font-weight: 800;
      }

      div[data-testid="stForm"] {
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 18px;
        padding: 0.95rem 0.95rem 0.75rem;
        box-shadow: 0 10px 24px rgba(19, 25, 35, 0.06);
      }

      div[data-testid="stForm"] .stTextInput label {
        font-size: 0.9rem;
        font-weight: 700;
        color: #222f3d;
      }

      div[data-testid="stForm"] .stTextInput {
        margin-bottom: 0.2rem;
      }

      div[data-testid="stForm"] div[data-baseweb="input"] {
        border: 1px solid #c8d4e0 !important;
        border-radius: 14px !important;
        background: #ffffff !important;
        box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.95), 0 1px 2px rgba(16, 24, 40, 0.06) !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
      }

      div[data-testid="stForm"] div[data-baseweb="input"] > div {
        background: transparent !important;
        border: 0 !important;
      }

      div[data-testid="stForm"] div[data-baseweb="input"]:focus-within {
        border-color: var(--ind-green) !important;
        box-shadow: 0 0 0 3px rgba(0, 179, 134, 0.18), 0 8px 18px rgba(11, 22, 35, 0.09) !important;
      }

      div[data-testid="stForm"] div[data-baseweb="input"] input {
        background: transparent !important;
        border: 0 !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        line-height: 1.35 !important;
        padding: 0.78rem 0.95rem !important;
        color: #14202b !important;
        caret-color: #111a22 !important;
      }

      div[data-testid="stForm"] div[data-baseweb="input"] input:focus {
        outline: none !important;
        box-shadow: none !important;
      }

      div[data-testid="stForm"] div[data-baseweb="input"] input::placeholder {
        color: #92a0af !important;
        -webkit-text-fill-color: #92a0af !important;
        font-weight: 500 !important;
        font-style: italic;
        letter-spacing: 0.01em;
        opacity: 1 !important;
      }

      div[data-testid="stForm"] div[data-baseweb="input"] input:-webkit-autofill,
      div[data-testid="stForm"] div[data-baseweb="input"] input:-webkit-autofill:hover,
      div[data-testid="stForm"] div[data-baseweb="input"] input:-webkit-autofill:focus {
        -webkit-box-shadow: 0 0 0 1000px #ffffff inset !important;
        -webkit-text-fill-color: #111a22 !important;
      }

      div[data-testid="stForm"] div[data-testid="stFormSubmitButton"] {
        margin-top: 0.58rem;
      }

      div[data-testid="stFormSubmitButton"] button,
      div[data-testid="stFormSubmitButton"] > button[kind="primary"] {
        border: 0;
        border-radius: 12px;
        background: linear-gradient(90deg, #00a27a 0%, #00be8f 100%);
        color: #ffffff;
        font-weight: 700;
        padding: 0.56rem 0.9rem;
      }

      div[data-testid="stFormSubmitButton"] button:hover,
      div[data-testid="stFormSubmitButton"] > button[kind="primary"]:hover {
        filter: brightness(1.06);
      }

      .stButton > button[kind="secondary"] {
        width: 100%;
        border-radius: 12px;
        border: 1px solid #cfd9e3;
        color: #1c2630;
        background: #ffffff;
        font-size: 0.84rem;
        font-weight: 650;
        line-height: 1.35;
        min-height: 3.1rem;
      }

      .stButton > button[kind="secondary"]:hover {
        color: #06755b;
        border-color: #89dfc9;
        background: #f2fcf9;
      }

      .disclaimer {
        margin-top: 0.85rem;
        border: 1px solid #b8ebdd;
        border-left: 6px solid var(--ind-green);
        border-radius: 14px;
        padding: 0.72rem 0.84rem;
        background: #ecfaf5;
        color: #124135;
        line-height: 1.4;
        font-size: 0.9rem;
      }

      .right-card {
        background: linear-gradient(180deg, #ffffff 0%, #f9fbfd 100%);
        border: 1px solid var(--line);
        border-radius: 20px;
        padding: 0.9rem 0.95rem;
        box-shadow: 0 10px 25px rgba(19, 25, 35, 0.06);
        margin-bottom: 0.75rem;
      }

      .right-card h4 {
        margin: 0;
        color: #15202b;
        font-size: 0.95rem;
        font-weight: 800;
      }

      .tag-wrap {
        margin-top: 0.62rem;
        display: flex;
        flex-wrap: wrap;
        gap: 0.38rem;
      }

      .tag {
        font-size: 0.76rem;
        font-weight: 700;
        color: #1f2d38;
        background: #eef3f8;
        border: 1px solid #d4dee8;
        border-radius: 999px;
        padding: 0.2rem 0.55rem;
      }

      .scheme-list {
        margin: 0.62rem 0 0;
        padding-left: 1rem;
        color: #334252;
      }

      .scheme-list li {
        margin: 0.24rem 0;
        font-size: 0.88rem;
        line-height: 1.3;
      }

      .answer-wrap {
        margin-top: 1rem;
        background: var(--surface);
        border: 1px solid var(--line);
        border-radius: 22px;
        padding: 1.05rem 1.15rem;
        box-shadow: 0 14px 30px rgba(18, 26, 36, 0.09);
      }

      .answer-head {
        margin: 0;
        color: #07795f;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.07em;
        text-transform: uppercase;
      }

      .answer-question {
        margin: 0.36rem 0 0.55rem;
        color: #5c6a79;
        font-size: 0.87rem;
        font-weight: 600;
      }

      .answer-text {
        margin: 0;
        color: #121a22;
        font-size: 1.05rem;
        line-height: 1.46;
        font-weight: 700;
      }

      .answer-meta {
        margin-top: 0.6rem;
        color: #4d5d6f;
        font-size: 0.9rem;
      }

      .answer-meta a {
        color: #136dcb;
        text-decoration: none;
      }

      .answer-meta a:hover {
        text-decoration: underline;
      }

      @media (max-width: 900px) {
        .hero-grid {
          grid-template-columns: 1fr;
        }

        .hero-metric-wrap {
          grid-template-columns: 1fr;
        }
      }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="ind-topbar">
      <div class="ind-topbar-inner">
        <div class="brand">
          <img src="https://indcdn.indmoney.com/cdn/images/fe/ind-money-logo.svg" alt="INDMoney logo">
          <span class="brand-name">INDMoney Styled Experience</span>
          <span class="brand-pill">Facts-only</span>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <div class="hero-grid">
        <div>
          <h1 class="hero-title">Mutual Fund Facts Assistant</h1>
          <p class="hero-sub">Facts-only Mutual Fund FAQ (INDMoney sources)</p>
        </div>
        <div class="hero-metric-wrap">
          <div class="hero-metric"><strong>One Source Link</strong><span>Per answer</span></div>
          <div class="hero-metric"><strong>No Advice</strong><span>Strict refusal rules</span></div>
          <div class="hero-metric"><strong>Scheme Facts</strong><span>JSON / CSV backed</span></div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

left_col, right_col = st.columns([1.65, 1], gap="large")

with left_col:
    st.markdown(
        """
        <div class="panel">
          <p class="panel-title">Ask factual scheme questions</p>
          <p class="panel-copy">Ask factual questions about mutual fund schemes such as expense ratio, exit load, SIP, lock-in, riskometer, or benchmark.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<p class="section-label">Example questions</p>', unsafe_allow_html=True)
    example_cols = st.columns(3)
    for idx, question in enumerate(EXAMPLE_QUESTIONS):
        if example_cols[idx].button(question, key=f"example_{idx}"):
            st.session_state["user_question"] = question
            run_query(question)

    with st.form("query_form", clear_on_submit=False, enter_to_submit=False):
        st.text_input(
            "Input box for user question",
            key="user_question",
            placeholder="Type your question (e.g., expense ratio of HDFC Large Cap Fund)",
        )
        submitted = st.form_submit_button("Get Fact", type="primary")

    if submitted:
        run_query(st.session_state.get("user_question", ""))

    last_result = st.session_state.get("last_result")
    if last_result:
        answer_text = escape(last_result["answer_text"])
        source_url = escape(last_result["source_url"])
        updated_note = escape(last_result["last_updated_from_sources"])
        question_text = escape(st.session_state.get("last_question", ""))

        st.markdown(
            f"""
            <div class="answer-wrap">
              <p class="answer-head">Answer</p>
              <p class="answer-question">Query: {question_text}</p>
              <p class="answer-text">{answer_text}</p>
              <p class="answer-meta">Source: <a href="{source_url}" target="_blank">{source_url}</a></p>
              <p class="answer-meta">Last updated from sources: {updated_note}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="disclaimer">
          This assistant provides factual information from official mutual fund pages. It does not provide investment advice or recommendations.
        </div>
        """,
        unsafe_allow_html=True,
    )

with right_col:
    st.markdown(
        """
        <div class="right-card">
          <h4>Covered factual fields</h4>
          <div class="tag-wrap">
            <span class="tag">Expense ratio</span>
            <span class="tag">Exit load</span>
            <span class="tag">Minimum SIP</span>
            <span class="tag">Minimum lump sum</span>
            <span class="tag">Lock-in period</span>
            <span class="tag">Riskometer</span>
            <span class="tag">Benchmark index</span>
            <span class="tag">AMC</span>
            <span class="tag">Category</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    schemes_html = "".join(f"<li>{escape(name)}</li>" for name in SUPPORTED_SCHEMES)
    st.markdown(
        f"""
        <div class="right-card">
          <h4>Included schemes (INDMoney)</h4>
          <ul class="scheme-list">{schemes_html}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
