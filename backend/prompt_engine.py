import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

CHROMA_PATH = "chroma_db"

def summarize(text: str, max_chars: int = 400) -> str:
    """Retorna um resumo simples do texto (primeiras frases ou até max_chars)."""
    if len(text) <= max_chars:
        return text
    # Tenta cortar no final de frase
    end = text.find('.', max_chars)
    if end == -1:
        end = max_chars
    return text[:end+1] + '...'

def generate_adaptive_prompt(user_input: str):
    # Busca semântica em todas as coleções, incluindo imagens
    results: List[dict] = []
    for collection_name in ["texts", "exercises", "pdfs", "videos", "images"]:
        try:
            collection = client.get_collection(collection_name, embedding_function=hf_ef)
            res = collection.query(query_texts=[user_input], n_results=2)
            for doc, meta in zip(res["documents"][0], res["metadatas"][0]):
                results.append({
                    "collection": collection_name,
                    "document": doc,
                    "metadata": meta
                })
        except Exception:
            continue
    if not results:
        return "Nenhum conteúdo relevante encontrado."
    # Monta uma resposta explicativa para cada fonte
    explanations = []
    for r in results:
        file_name = r["metadata"].get("source", "desconhecido")
        tipo = r["collection"]
        trecho = summarize(r["document"])
        explanations.append(f"Fonte: {file_name} (tipo: {tipo})\nTrecho relevante: {trecho}")
    resposta = "\n\n".join(explanations)
    return resposta 