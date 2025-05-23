import os
from PIL import Image, ImageOps
import pytesseract
from pytesseract import TesseractError

def index_images(client, hf_ef):
    """
    Endpoint para indexar imagens.
    Mede o tempo necessário para indexar as imagens e registra o resultado.
    """
    indexed = {}
    image_path = os.path.join("resources", "Infografico-1.jpg")
    if not os.path.exists(image_path):
        print(f"[WARN] Arquivo Infografico-1.jpg não encontrado em {image_path}")
        return indexed
    try:
        with Image.open(image_path) as img:
            gray = ImageOps.grayscale(img)
            gray = ImageOps.autocontrast(gray)
        ocr_text = pytesseract.image_to_string(gray, lang="por").strip()
        if not ocr_text:
            ocr_text = pytesseract.image_to_string(gray, lang="eng").strip()
        if not ocr_text:
            ocr_text = "[Imagem sem texto reconhecível – talvez seja puramente ilustrativa.]"
        collection = client.get_or_create_collection("images", embedding_function=hf_ef)
        collection.add(
            documents=[ocr_text],
            metadatas=[{
                "source": os.path.basename(image_path),
                "tags": "infografico, programação, imagem",
                "ocr": True,
            }],
            ids=[os.path.basename(image_path)]
        )
        indexed[os.path.basename(image_path)] = ocr_text
        print(f"[INFO] Indexado: Infografico-1.jpg")
    except Exception as e:
        print(f"[ERROR] Erro ao indexar Infografico-1.jpg: {e}")
    
    if not indexed:
        print("[INFO] Nenhuma imagem indexada")
    return indexed