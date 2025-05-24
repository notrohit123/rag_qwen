import streamlit as st
import re

def init_session_state():
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("docs_loaded", False)
    st.session_state.setdefault("temp_dir", None)
    st.session_state.setdefault("current_pdf", None)

def display_assistant_message(content):
    match = re.search(r"<think>(.*?)</think>", content, re.DOTALL)
    if match:
        think_block = match.group(0)
        plain_resp = content.replace(think_block, "")
        reasoning = think_block.replace("<think>", "").replace("</think>", "").strip()
        with st.expander("AI Reasoning"):
            st.markdown(reasoning)
        st.markdown(plain_resp)
    else:
        st.markdown(content)
