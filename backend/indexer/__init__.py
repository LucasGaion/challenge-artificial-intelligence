import os
from chromadb.utils import embedding_functions
from chromadb import PersistentClient

CHROMA_PATH = "./chroma_db"
client = PersistentClient(path=CHROMA_PATH)
hf_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

from .index_texts import index_texts
from .index_pdfs import index_pdfs
from .index_videos import index_videos
from .index_images import index_images
from .save_response import save_response_to_chromadb 