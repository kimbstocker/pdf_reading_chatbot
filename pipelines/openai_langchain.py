import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from model import prompt_templates
from pipelines.utils.get_split_docs import get_split_documents


def openai_langchain_pipeline(query: str, uploaded_file_name=""):

    load_dotenv()
    OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
    DOC_PATH = os.environ["DATASET_PATH"]
    # CHROMA_PATH = os.environ["DATASTORE_DIR"]

    # ----- Indexing Data -----

    # loading pdf docs and split them into smaller chunks i.e. chunk_size=1000 chunk_overlap=50
    chunks = get_split_documents(DOC_PATH, uploaded_file_name)

    # Embedding using OpenAI Embedding model
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # embed the chunks as vectors and load them into the database. Using in-memory datastore
    # TODO: Disable the use of persistence data storage as it hallucinates btw contexts more than 1 pdf uploaded
    # Find a better way to manage data source. Maybe add meta data when upload pdf?
    # db_chroma = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_PATH)

    db_chroma = Chroma.from_documents(chunks, embeddings)

    # ----- Retrieval and Generation -----

    # retrieve context - top 5 most relevant (closests) chunks to the query vector
    top_chunks_context = db_chroma.similarity_search_with_score(query, k=5)

    # generate an answer based on given user query and retrieved context information
    context_text = "\n\n".join([doc.page_content for doc, _score in top_chunks_context])

    # load retrieved context and user query in the prompt template and format it
    prompt_template = ChatPromptTemplate.from_template(prompt_templates.PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query)

    # call LLM model to generate the answer based on the given formatted prompt
    model = ChatOpenAI(model="gpt-3.5-turbo")

    try:
        response = model.invoke(prompt).content
    except Exception as e:
        print(f"Error: {e}")
        response = "There is a problem with generating answers, please reload and retry"

    return {"answer": response, "contexts": context_text}
