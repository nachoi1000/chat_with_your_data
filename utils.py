from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings
from langchain.vectorstores.chroma import Chroma
from PyPDF2 import PdfReader

def get_pdf_text(file):
    text = ""
    if file.endswith('.pdf'):
        pdf_reader = PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text()
    elif file.endswith('.txt'):
        with open(file, 'r', encoding='utf-8') as txt_file:
            text += txt_file.read()
    else:
        raise ValueError(f"Unsupported file type: {file}")
    return text

def generate_chunks(txt_files):
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", "(?<=\. )", " ", ""])
    
    chunks = text_splitter.split_text(txt_files)
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
