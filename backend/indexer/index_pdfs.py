import os
import pdfplumber

def index_pdfs(client, hf_ef):
    indexed = {}
    pdf_path = os.path.join("resources", "Capítulo do Livro.pdf")
    if os.path.exists(pdf_path):
        with pdfplumber.open(pdf_path) as pdf:
            full_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
        collection = client.get_or_create_collection("pdfs", embedding_function=hf_ef)
        collection.add(
            documents=[full_text],
            metadatas=[{"source": "Capítulo do Livro.pdf"}],
            ids=["capitulo-livro-pdf"]
        )
        indexed["Capítulo do Livro.pdf"] = full_text
    return indexed 