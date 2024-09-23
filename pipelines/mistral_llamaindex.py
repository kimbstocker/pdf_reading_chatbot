import os
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.mistralai import MistralAIEmbedding

def mistralai_llamaindex_pipeline(query: str, uploaded_file_name=""):

    MISTRALAI_API_KEY = os.environ["MISTRALAI_API_KEY"]
    DOC_PATH = os.environ["DATASET_PATH"]

    # ----- Indexing Data -----

    # Loading pdf docs, for asking question about a specific file 
    if uploaded_file_name:
        input_files = [os.path.join(DOC_PATH, uploaded_file_name)]
        reader = SimpleDirectoryReader(input_files=input_files)
    else:    
        reader = SimpleDirectoryReader(input_dir=DOC_PATH)
    
    loaded_documents = reader.load_data()
    
    # Mistral setup, define LLM and embedding model
    llm = MistralAI(api_key=MISTRALAI_API_KEY, model="mistral-medium")
    embed_model = MistralAIEmbedding(model_name="mistral-embed", api_key=MISTRALAI_API_KEY)
    Settings.llm = llm
    Settings.embed_model = embed_model

    # Create in-memory vector store index
    index = VectorStoreIndex.from_documents(loaded_documents)
    
    # ----- create context_text for performance evalutation purposes only -----
    
    retriever = index.as_retriever()
    nodes_with_score = retriever.retrieve(query)
    context_text = "\n\n".join([n.text for n in nodes_with_score])

    # ----- Retrieval and Generation -----

    # Create query engine from the vector store index
    query_engine = index.as_query_engine(similarity_top_k=5)
    
    try:
        response = query_engine.query(query)
    except Exception as e:
        print(f"Error: {e}")
        response = "There is a problem with generating answers, please reload and retry"

    return {"answer": response, "contexts": context_text}

# NOTE: https://docs.llamaindex.ai/en/stable/examples/prompts/prompt_optimization/
