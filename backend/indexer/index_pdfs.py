import os
import pdfplumber

def index_pdfs(client, hf_ef):
<<<<<<< HEAD
    """
    Endpoint para indexar pdfs.
    Mede o tempo necessário para indexar o pdfs e registra o resultado.
    """
    indexed = {}
    pdf_path = os.path.join("resources", "Capítulo do Livro.pdf")
    if os.path.exists(pdf_path):
        try:
            with pdfplumber.open(pdf_path) as pdf:
                full_text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            if full_text.strip():
                collection = client.get_or_create_collection("pdfs", embedding_function=hf_ef)
                collection.add(
                    documents=[full_text],
                    metadatas=[{"source": "Capítulo do Livro.pdf"}],
                    ids=["capitulo-livro-pdf"]
                )
                indexed["Capítulo do Livro.pdf"] = full_text
                print(f"[INFO] Indexado: Capítulo do Livro.pdf")
            else:
                print(f"[WARN] Capítulo do Livro.pdf está vazio")
        except Exception as e:
            print(f"[ERROR] Erro ao indexar Capítulo do Livro.pdf: {e}")
    else:
        print(f"[WARN] Arquivo Capítulo do Livro.pdf não encontrado em {pdf_path}")
    
    if not indexed:
        print("[INFO] Nenhum PDF indexado")
    return indexed
=======
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
>>>>>>> 1a2aef2be476b4f276ce1d6a88a7ceea75d47cfc
