import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.prompts import ChatPromptTemplate
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from dotenv import load_dotenv
from model import prompt_template

load_dotenv()
# OPENAI_API_KEY = os.environ["GOOGLE_API_KEY"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
DOC_PATH = os.environ["DATASET_PATH"]
CHROMA_PATH = os.environ["DATASTORE_DIR"] 

# ----- Indexing Data -----

# loading pdf doc
loader = UnstructuredPDFLoader(DOC_PATH)
pages = loader.load()

# split the doc into smaller chunks i.e. chunk_size=500
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(pages)

# Embedding using OpenAI Embedding model
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# embed the chunks as vectors and load them into the database
db_chroma = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_PATH)

# ----- Retrieval and Generation -----

# this is an example of a user question (query)
query = 'Please summarise the document or context provided?'

# retrieve context - top 5 most relevant (closests) chunks to the query vector 
# (by default Langchain is using cosine distance metric)
docs_chroma = db_chroma.similarity_search_with_score(query, k=5)

# generate an answer based on given user query and retrieved context information
context_text = "\n\n".join([doc.page_content for doc, _score in docs_chroma])

# load retrieved context and user query in the prompt template
prompt_template = ChatPromptTemplate.from_template(prompt_template.PROMPT_TEMPLATE)
prompt = prompt_template.format(context=context_text, question=query)

# call LLM model to generate the answer based on the given context and prompt
model = ChatOpenAI(model="gpt-3.5-turbo")
response_text = model.invoke(prompt)

print(f"response: {response_text}")