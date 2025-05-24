import os, shutil, tempfile
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader
import streamlit as st
load_dotenv()

def handle_pdf_upload(uploaded_file):
    if uploaded_file != st.session_state.current_pdf:
        st.session_state.current_pdf = uploaded_file
        try:
            if not os.getenv("NEBIUS_API_KEY"):
                st.error("Missing Nebius API key")
                st.stop()

            if st.session_state.temp_dir:
                shutil.rmtree(st.session_state.temp_dir)
            st.session_state.temp_dir = tempfile.mkdtemp()
            file_path = os.path.join(st.session_state.temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            with st.spinner("Loading PDF..."):
                documents = SimpleDirectoryReader(st.session_state.temp_dir).load_data()
                st.session_state.docs_loaded = True
                st.session_state.documents = documents
                st.success("PDF loaded successfully")
        except Exception as e:
            st.error(f"Error: {e}")
