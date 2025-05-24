import streamlit as st
import shutil
from rag_chat_qwen.file_handler import handle_pdf_upload
from rag_chat_qwen.rag_engine import run_rag_completion
from rag_chat_qwen.utils import display_assistant_message, init_session_state


def start_ui():
    st.set_page_config(page_title="RAG Chat", layout="wide")
    init_session_state()

    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("RAG Chat Interface")

    with col2:
        if st.button("Clear Chat"):
            st.session_state.clear()
            st.rerun()
# we have 2 choicess to choose good models from -qwen3/d-seek

    with st.sidebar:
        generative_model = st.selectbox("Generative Model", ["Qwen/Qwen3-235B-A22B", "deepseek-ai/DeepSeek-V3"])
        st.subheader("Upload PDF")
        uploaded_file = st.file_uploader("Choose PDF", type="pdf")

        if uploaded_file:
            handle_pdf_upload(uploaded_file)

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                display_assistant_message(msg["content"])
            else:
                st.markdown(msg["content"])

    if prompt := st.chat_input("Ask a question..."):
        if not st.session_state.docs_loaded:
            st.error("Please upload a PDF first")
            return
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    res = run_rag_completion(st.session_state.documents, prompt, generative_model=generative_model)
                    st.session_state.messages.append({"role": "assistant", "content": res})
                    display_assistant_message(res)
                except Exception as e:
                    st.error(f"Error: {e}")