import os
import json

def index_texts(client, hf_ef):
<<<<<<< HEAD
    """
    Função para indexar textos a partir de arquivos.
    Lê o conteúdo de arquivos de texto e os adiciona a uma coleção no banco de dados.
    """
    indexed = {}
    txt_path = os.path.join("resources", "Apresentação.txt")
    if os.path.exists(txt_path):
        try:
            with open(txt_path, "r", encoding="utf-8") as f:
                content = f.read()
            if content.strip():
                collection = client.get_or_create_collection("texts", embedding_function=hf_ef)
                collection.add(
                    documents=[content],
                    metadatas=[{"source": "Apresentação.txt"}],
                    ids=["apresentacao-txt"]
                )
                indexed["Apresentação.txt"] = content
                print(f"[INFO] Indexado: Apresentação.txt")
            else:
                print(f"[WARN] Apresentação.txt está vazio")
        except Exception as e:
            print(f"[ERROR] Erro ao indexar Apresentação.txt: {e}")
    else:
        print(f"[WARN] Arquivo Apresentação.txt não encontrado em {txt_path}")

    json_path = os.path.join("resources", "Exercícios.json")
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            if "content" in data:
                collection = client.get_or_create_collection("exercises", embedding_function=hf_ef)
                questions = []
                for i, q in enumerate(data["content"]):
                    q_text = q.get("title", "") + ": " + q["content"].get("html", "")
                    if q_text.strip():
                        collection.add(
                            documents=[q_text],
                            metadatas=[{"source": "Exercícios.json", "question": q.get("title", "")}],
                            ids=[f"exercise-{i}"]
                        )
                        questions.append(q_text)
                        print(f"[INFO] Indexado: Exercício {i} de Exercícios.json")
                    else:
                        print(f"[WARN] Exercício {i} está vazio")
                indexed["Exercícios.json"] = questions
            else:
                print(f"[WARN] Chave 'content' não encontrada em Exercícios.json")
        except Exception as e:
            print(f"[ERROR] Erro ao indexar Exercícios.json: {e}")
    else:
        print(f"[WARN] Arquivo Exercícios.json não encontrado em {json_path}")

    if not indexed:
        print("[INFO] Nenhum texto indexado")
    return indexed
=======
    indexed = {}
    txt_path = os.path.join("resources", "Apresentação.txt")
    if os.path.exists(txt_path):
        with open(txt_path, "r", encoding="utf-8") as f:
            content = f.read()
        collection = client.get_or_create_collection("texts", embedding_function=hf_ef)
        collection.add(
            documents=[content],
            metadatas=[{"source": "Apresentação.txt"}],
            ids=["apresentacao-txt"]
        )
        indexed["Apresentação.txt"] = content
    # Indexa questões do Exercícios.json
    json_path = os.path.join("resources", "Exercícios.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "content" in data:
            collection = client.get_or_create_collection("exercises", embedding_function=hf_ef)
            questions = []
            for i, q in enumerate(data["content"]):
                q_text = q.get("title", "") + ": " + q["content"].get("html", "")
                collection.add(
                    documents=[q_text],
                    metadatas=[{"source": "Exercícios.json", "question": q.get("title", "")}],
                    ids=[f"exercise-{i}"]
                )
                questions.append(q_text)
            indexed["Exercícios.json"] = questions
    return indexed 
>>>>>>> 1a2aef2be476b4f276ce1d6a88a7ceea75d47cfc
