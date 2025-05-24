import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, Settings
from llama_index.embeddings.nebius import NebiusEmbedding
from llama_index.llms.nebius import NebiusLLM
load_dotenv()

def run_rag_completion(documents, query_text: str, embedding_model="BAAI/bge-en-icl", generative_model="Qwen/Qwen3-235B-A22B"):
    llm = NebiusLLM(model=generative_model, api_key=os.getenv("NEBIUS_API_KEY"))
    embed_model = NebiusEmbedding(model_name=embedding_model, api_key=os.getenv("NEBIUS_API_KEY"))
    Settings.llm = llm
    Settings.embed_model = embed_model
    index = VectorStoreIndex.from_documents(documents)
    return str(index.as_query_engine(similarity_top_k=5).query(query_text))

