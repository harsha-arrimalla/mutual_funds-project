"""Streamlit app for a facts-only INDMoney mutual fund FAQ assistant."""

import streamlit as st

from rag import FundFactsRetriever


st.set_page_config(page_title="Mutual Fund Facts Assistant", page_icon="📘", layout="centered")

assistant = FundFactsRetriever()

st.title("Mutual Fund Facts Assistant")
st.subheader("Facts-only Mutual Fund FAQ (INDMoney sources)")

st.write(
    "Ask factual questions about mutual fund schemes such as expense ratio, exit load, "
    "SIP, lock-in, riskometer, or benchmark."
)

st.markdown("**Example questions**")
st.markdown("- Expense ratio of HDFC Large Cap Fund")
st.markdown("- Lock-in period of SBI ELSS Fund")
st.markdown("- Minimum SIP of HDFC Flexi Cap Fund")

st.info(
    "This assistant provides factual information from official mutual fund pages. "
    "It does not provide investment advice or recommendations."
)

user_question = st.text_input("Enter your question")

if user_question:
    result = assistant.answer(user_question)

    with st.container(border=True):
        st.markdown("**Answer**")
        st.write(result["answer_text"])
        st.markdown(f"Source: [{result['source_url']}]({result['source_url']})")
        st.write(f"Last updated from sources: {result['last_updated_from_sources']}")
