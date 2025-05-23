import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv
import os

load_dotenv()

CHROMA_PATH = "chroma_db"
client = chromadb.PersistentClient(path=CHROMA_PATH)
hf_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
)