import os
from dotenv import load_dotenv
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.mistralai import MistralAIEmbedding

def mistralai_llamaindex_pipeline(query: str):
    load_dotenv()
    MISTRALAI_API_KEY = os.environ["MISTRALAI_API_KEY"]
    DOC_PATH = os.environ["DATASET_PATH"]

    # ----- Indexing Data -----

    # Loading pdf docs
    reader = SimpleDirectoryReader(input_dir=DOC_PATH)
    loaded_documents = reader.load_data()

    # Mistral setup, define LLM and embedding model
    llm = MistralAI(api_key=MISTRALAI_API_KEY, model="mistral-medium")
    embed_model = MistralAIEmbedding(model_name="mistral-embed", api_key=MISTRALAI_API_KEY)
    Settings.llm = llm
    Settings.embed_model = embed_model

    # Create in-memory vector store index
    index = VectorStoreIndex.from_documents(loaded_documents)

    # ----- Retrieval and Generation -----

    # Create query engine from the vector store index
    query_engine = index.as_query_engine(similarity_top_k=5)
    response = query_engine.query(query)
    
    return response

# NOTE: https://docs.llamaindex.ai/en/stable/examples/prompts/prompt_optimization/
