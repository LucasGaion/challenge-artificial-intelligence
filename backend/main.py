from fastapi import FastAPI
from pydantic import BaseModel
from rich.console import Console
import time
import os
import whisper
from PIL import Image

import chromadb
from chromadb.config import Settings

from .indexer import index_texts as idx_texts, index_pdfs as idx_pdfs, index_videos as idx_videos, index_images as idx_images, client, hf_ef
from .prompt_engine import generate_adaptive_prompt

console = Console()
app = FastAPI()


class PromptRequest(BaseModel):
    user_input: str


@app.get("/")
def root():
    return {"message": "API do sistema de aprendizagem adaptativa"}


@app.post("/index/texts")
def index_texts():
    start_time = time.time()
    indexed = idx_texts(client, hf_ef)
    elapsed_time = time.time() - start_time
    console.print("[bold green]Indexação de textos finalizada![/bold green]")
    console.print(f"[cyan]Tempo: {elapsed_time:.2f} segundos[/cyan]")
    return {
        "status": "Textos indexados",
        "conteudo_indexado": indexed
    }


@app.post("/index/pdfs")
def index_pdfs():
    start_time = time.time()
    indexed = idx_pdfs(client, hf_ef)
    elapsed_time = time.time() - start_time
    console.print("[bold green]Indexação de PDFs finalizada![/bold green]")
    console.print(f"[cyan]Tempo: {elapsed_time:.2f} segundos[/cyan]")
    return {
        "status": "PDFs indexados",
        "conteudo_indexado": indexed
    }


@app.post("/index/videos")
def index_videos():
    start_time = time.time()
    indexed = idx_videos(client, hf_ef)
    elapsed_time = time.time() - start_time
    console.print("[bold green]Indexação de vídeos finalizada![/bold green]")
    console.print(f"[cyan]Tempo: {elapsed_time:.2f} segundos[/cyan]")
    return {
        "status": "Vídeos indexados",
        "conteudo_indexado": indexed
    }


@app.post("/index/images")
def index_images():
    start_time = time.time()
    indexed = idx_images(client, hf_ef)
    elapsed_time = time.time() - start_time
    console.print("[bold green]Indexação de imagens finalizada![/bold green]")
    console.print(f"[cyan]Tempo: {elapsed_time:.2f} segundos[/cyan]")
    return {
        "status": "Imagens indexadas",
        "conteudo_indexado": indexed
    }


@app.post("/prompt")
def prompt(request: PromptRequest):
    response = generate_adaptive_prompt(request.user_input)
    return {"response": response}


def transcribe_video():
    video_path = os.path.join("resources", "Dica do professor.mp4")
    if os.path.exists(video_path):
        try:
            model = whisper.load_model("base")
            result = model.transcribe(video_path, language="pt")
            transcription = result["text"]
            print("Transcrição do vídeo:", transcription)
        except Exception as e:
            print(f"Erro ao transcrever o vídeo: {e}")
    else:
        print("Arquivo de vídeo não encontrado.")


def view_image():
    image_path = os.path.join("resources", "Infografico-1.jpg")
    if os.path.exists(image_path):
        try:
            with Image.open(image_path) as img:
                img.show()
                description = "Infográfico sobre fundamentos de programação. Imagem ilustrativa do conteúdo abordado."
                print("Descrição da imagem:", description)
        except Exception as e:
            print(f"Erro ao abrir a imagem: {e}")
    else:
        print("Imagem não encontrada.")


if __name__ == "__main__":
    print("Iniciando indexação manual...")
    idx_texts(client, hf_ef)
    idx_pdfs(client, hf_ef)
    idx_videos(client, hf_ef)
    idx_images(client, hf_ef)
    transcribe_video()
    view_image()
