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
        model = whisper.load_model("base")
        result = model.transcribe(video_path, language="pt")
        transcription = result["text"]
        collection = client.get_or_create_collection("videos", embedding_function=hf_ef)
        collection.add(
            documents=[transcription],
            metadatas=[{"source": "Dica do professor.mp4", "description": "Transcrição do vídeo sobre dicas de programação."}],
            ids=["dica-professor-video"]
        )
        indexed["Dica do professor.mp4"] = transcription
    return indexed 