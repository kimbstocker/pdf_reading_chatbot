import os
from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredPDFLoader


def get_split_documents(docs_path: str) -> List[str]:
    split_docs = []

    for file_name in os.listdir(docs_path):
        loader = UnstructuredPDFLoader(os.path.join(docs_path, file_name))
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
        split_docs.extend(text_splitter.split_documents(loader.load()))

    return split_docs