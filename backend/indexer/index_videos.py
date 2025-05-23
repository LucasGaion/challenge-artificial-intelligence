import os
import whisper

def index_videos(client, hf_ef):
    """
    Endpoint para indexar videos.
    Mede o tempo necessário para indexar o video e registra o resultado.
    """
    indexed = {}
    video_path = os.path.join("resources", "Dica do professor.mp4")
    if os.path.exists(video_path):
        try:
            model = whisper.load_model("base")
            result = model.transcribe(video_path, language="pt")
            transcription = result["text"]
            if transcription.strip():
                collection = client.get_or_create_collection("videos", embedding_function=hf_ef)
                collection.add(
                    documents=[transcription],
                    metadatas=[{"source": "Dica do professor.mp4", "description": "Transcrição do vídeo sobre dicas de programação."}],
                    ids=["dica-professor-video"]
                )
                indexed["Dica do professor.mp4"] = transcription
                print(f"[INFO] Indexado: Dica do professor.mp4")
            else:
                print(f"[WARN] Transcrição de Dica do professor.mp4 está vazia")
        except Exception as e:
            print(f"[ERROR] Erro ao indexar Dica do professor.mp4: {e}")
    else:
        print(f"[WARN] Arquivo Dica do professor.mp4 não encontrado em {video_path}")
    
    if not indexed:
        print("[INFO] Nenhum vídeo indexado")
    return indexed