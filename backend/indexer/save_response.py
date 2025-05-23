import time

def save_response_to_chromadb(client, hf_ef, response: str, user_input: str):
    """
    Endpoint para indexar pdfs.
    Salve arquivos temporarios no chromadb
    """
    collection = client.get_or_create_collection("responses", embedding_function=hf_ef)
    collection.add(
        documents=[response],
        metadatas=[{"user_input": user_input}],
        ids=[f"response-{int(time.time())}"]
    ) 