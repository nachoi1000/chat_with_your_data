from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores.chroma import Chroma
from PyPDF2 import PdfReader

def read_pdf(file):
    loader = PyPDFLoader(file)
    pages = loader.load_and_split()
    return pages


def generate_chunks(pdf_files):
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", "(?<=\. )", " ", ""])
    
    chunks = text_splitter.split_documents(pdf_files)
    return chunks

def initialize_embeddings():
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return embeddings

def generate_vectorstore(texts, embeddings):
    persist_directory = "db"
    
    vectordb = Chroma.from_texts(
        texts = texts,
        embedding = embeddings,
        persist_directory = persist_directory)
    
    vectordb.persist()
    return vectordb

# 08/12/2023

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def generate_chunks_2(txt_files):
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", "(?<=\. )", " ", ""])
    
    chunks = text_splitter.split_text(txt_files)
    return chunks