import os
from PIL import Image, ImageOps
import pytesseract
from pytesseract import TesseractError

def index_images(client, hf_ef):
    indexed = {}
    image_path = os.path.join("resources", "Infografico-1.jpg")
    if not os.path.exists(image_path):
        return indexed
    with Image.open(image_path) as img:
        gray = ImageOps.grayscale(img)
        gray = ImageOps.autocontrast(gray)
    try:
        ocr_text = pytesseract.image_to_string(gray, lang="por").strip()
    except TesseractError:
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
    return indexed 