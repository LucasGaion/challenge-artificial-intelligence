import os
from typing import List

import chromadb
from chromadb.utils import embedding_functions
from chromadb.errors import NotFoundError
from dotenv import load_dotenv

load_dotenv()

CHROMA_PATH = "chroma_db"

client = chromadb.PersistentClient(path=CHROMA_PATH)

hf_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
)

def summarize(text: str, max_chars: int = 400) -> str:
    """Retorna um resumo simples (até max_chars ou até o ponto final mais próximo)."""
    if len(text) <= max_chars:
        return text
    end = text.find(".", max_chars)
    if end == -1:
        end = max_chars
    return text[: end + 1] + "..."

def generate_adaptive_prompt(user_input: str) -> str:
    """
    Pesquisa semanticamente em todas as coleções definidas
    e devolve trechos explicativos para o usuário.
    """
    collections = ["texts", "exercises", "pdfs", "videos", "images"]
    results: List[dict] = []

    for name in collections:
        try:
            collection = client.get_collection(name, embedding_function=hf_ef)
        except NotFoundError:
            print(f"[INFO] Coleção '{name}' não encontrada. Criando nova...")
            collection = client.create_collection(name, embedding_function=hf_ef)
        except Exception as e:
            print(f"[WARN] Falha ao acessar a coleção '{name}': {e}")
            continue

        try:
            res = collection.query(query_texts=[user_input], n_results=2)
        except Exception as e:
            print(f"[WARN] Falha na consulta da coleção '{name}': {e}")
            continue

        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]
        for doc, meta in zip(docs, metas):
            if doc:  
                results.append(
                    {
                        "collection": name,
                        "document": doc,
                        "metadata": meta or {},
                    }
                )

    if not results:
        return "Nenhum conteúdo relevante encontrado."

    explanations = []
    for r in results:
        file_name = r["metadata"].get("source", "desconhecido")
        doc_type = r["collection"]
        trecho = summarize(r["document"])
        explanations.append(
            f"🔹 **Fonte:** {file_name} _(tipo: {doc_type})_\n"
            f"Trecho relevante: {trecho}"
        )

    return "\n\n".join(explanations)

if __name__ == "__main__":
    pergunta = input("Digite sua pergunta: ")
    resposta = generate_adaptive_prompt(pergunta)
    print("\n=== Resposta Adaptativa ===\n")
    print(resposta)
