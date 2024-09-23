import os
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredPDFLoader


def get_split_documents(docs_path: str, uploaded_file_name) -> List[str]:
    split_docs = []
    file_names = [uploaded_file_name] if uploaded_file_name else os.listdir(docs_path)
    
    for file_name in file_names:
        loader = UnstructuredPDFLoader(os.path.join(docs_path, file_name))
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        split_docs.extend(text_splitter.split_documents(loader.load()))

    return split_docs