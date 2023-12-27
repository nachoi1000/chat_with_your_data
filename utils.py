from config import chunk_overlap_size, chunk_size, embedding_choose
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import SentenceTransformerEmbeddings, OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from PyPDF2 import PdfReader
from logging_chat import logger
import secret_keys

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

def generate_chunks(txt_files, chunk_size, chunk_overlap_size):
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap_size,
        separators = ["\n\n", "\n", "(?<=\. )", " ", ""])
    
    chunks = text_splitter.split_text(txt_files)
    chunks = [chunk.replace("\n","") for chunk in chunks]
    return chunks

def initialize_embeddings(embedding_choose):
    embeddings = OpenAIEmbeddings(model_name = embedding_choose[1], openai_api_key=secret_keys.CORPORATE_OPENAI_KEY)
    return embeddings

def generate_vectorstore(texts, embeddings):
    persist_directory = "db"
    
    vectordb = Chroma.from_texts(
        texts = texts,
        embedding = embeddings,
        persist_directory = persist_directory)
    
    vectordb.persist()
    return vectordb
