# LLM
gpt_model = "gpt-4"

# Embedding models
openai_embedding_model = ['OpenAIEmbeddings',"text-embedding-ada-002"]
sentence_transformers_model = ["SentenceTransformerEmbeddings","all-MiniLM-L6-v2"]
embedding_choose = openai_embedding_model

# CHUNKS
chunk_size = 1200
chunk_overlap_size = 150