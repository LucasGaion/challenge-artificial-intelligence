import time
import chromadb

def save_response_to_chromadb(client, hf_ef, response: str, user_input: str):
    """
    Salva a resposta no ChromaDB na coleção 'responses'.
    """
    try:
        collection = client.get_or_create_collection("responses", embedding_function=hf_ef)
        collection.add(
            documents=[response],
            metadatas=[{"user_input": user_input}],
            ids=[f"response-{int(time.time())}"]
        )
        print(f"[INFO] Resposta salva no ChromaDB: {response[:50]}...")
    except Exception as e:
        print(f"[ERROR] Falha ao salvar resposta no ChromaDB: {e}")