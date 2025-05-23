<<<<<<< HEAD
import os
import logging
from typing import List
from chromadb.errors import NotFoundError
from backend.db_config import client, hf_ef
import unicodedata

# Configuração de logging profissional
logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Estado simples do usuário (em memória, por session_id fictício)
user_states = {}

def normalize(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower().strip()

def summarize(text: str, max_chars: int = 400) -> str:
    """Retorna um resumo simples (até max_chars ou até o ponto final mais próximo)."""
    if len(text) <= max_chars:
        return text
    end = text.find(".", max_chars)
    if end == -1:
        end = max_chars
    return text[:end + 1] + "..."

def get_user_state(session_id: str):
    if session_id not in user_states:
        user_states[session_id] = {
            "nivel": None,
            "preferencia": None,
            "dificuldade": None
        }
    return user_states[session_id]

def update_user_state(session_id: str, nivel=None, preferencia=None, dificuldade=None):
    state = get_user_state(session_id)
    if nivel:
        state["nivel"] = nivel
    if preferencia:
        state["preferencia"] = preferencia
    if dificuldade:
        state["dificuldade"] = dificuldade

def generate_adaptive_prompt(user_input: str, user_preferences: dict = None, session_id: str = "default") -> str:
    """
    Pesquisa semanticamente em todas as coleções definidas
    e devolve trechos explicativos para o usuário, adaptando-se às preferências de formato.
    Também faz perguntas para identificar nível, preferência e dificuldade.
    """
    logging.info(f"Entrada do usuário: {user_input}")
    state = get_user_state(session_id)

    # Detecta respostas do usuário para atualizar o estado
    nivel_keywords = ["iniciante", "intermediario", "intermediário", "avancado", "avançado"]
    preferencia_keywords = ["texto", "video", "vídeo", "audio", "áudio", "imagem"]
    dificuldade_opcoes = ["nenhuma", "html", "css", "javascript", "outro"]

    user_input_norm = normalize(user_input)

    # Validação do nível
    if not state["nivel"]:
        if user_input_norm and user_input_norm not in [normalize(x) for x in nivel_keywords]:
            return (
                "Está quase lá! Por favor, escolha uma das opções abaixo:\n"
                "- Iniciante\n- Intermediário\n- Avançado\n"
                "Qual seu nível de conhecimento sobre o tema?"
            )
        for word in nivel_keywords:
            if user_input_norm == normalize(word):
                update_user_state(session_id, nivel=word)
                return (
                    f"Ótimo, você selecionou: {word.capitalize()}!\n"
                    "Agora, escolha o formato de aprendizado que prefere:\n"
                    "- Texto\n- Vídeo\n- Áudio\n- Imagem"
                )

    # Validação da preferência
    elif not state["preferencia"]:
        if user_input_norm and user_input_norm not in [normalize(x) for x in preferencia_keywords]:
            return (
                "Quase certo! Por favor, escolha um formato entre:\n"
                "- Texto\n- Vídeo\n- Áudio\n- Imagem\n"
                "Qual formato de aprendizado você prefere?"
            )
        for word in preferencia_keywords:
            if user_input_norm == normalize(word):
                update_user_state(session_id, preferencia=word)
                return (
                    f"Formato de aprendizado escolhido: {word.capitalize()}!\n"
                    "Existe algum tópico específico que você considera mais desafiador ou gostaria de focar?\n"
                    "- Nenhuma\n- HTML\n- CSS\n- JavaScript\n- Outro"
                )

    # Validação da dificuldade
    elif not state["dificuldade"]:
        if user_input_norm and user_input_norm not in [normalize(x) for x in dificuldade_opcoes]:
            return (
                "Ótimo! Agora, selecione uma dificuldade entre:\n"
                "- Nenhuma\n- HTML\n- CSS\n- JavaScript\n- Outro\n"
                "Qual dessas opções melhor representa sua dificuldade?"
            )
        for word in dificuldade_opcoes:
            if user_input_norm == normalize(word):
                update_user_state(session_id, dificuldade=word)
                return (
                    f"Dificuldade definida: {word.capitalize()}! Obrigado, agora vamos buscar conteúdos personalizados para você."
                )

    if not state["nivel"]:
        return (
            "Antes de prosseguirmos, poderia informar seu nível de conhecimento sobre o tema? "
            "(iniciante, intermediário ou avançado)\n\n"
            "Sugestões de temas para começar:\n"
            "- HTML5\n- CSS\n- JavaScript\n- Acessibilidade Web\n- Estrutura de uma página\n"
            "Ou digite sua dúvida!"
        )
    if not state["preferencia"]:
        return ("Para personalizar sua experiência, qual formato de aprendizado você prefere? "
                "(texto, vídeo, áudio ou imagem)")
    if not state["dificuldade"]:
        return ("Existe algum tópico específico que você considera mais desafiador ou gostaria de focar?")

    collections = ["texts", "exercises", "pdfs", "videos", "images"]
    results: List[dict] = []
    for name in collections:
        try:
            collection = client.get_collection(name, embedding_function=hf_ef)
            logging.info(f"Acessando coleção '{name}'")
        except NotFoundError:
            logging.info(f"Coleção '{name}' não encontrada. Criando nova...")
            collection = client.create_collection(name, embedding_function=hf_ef)
        except Exception as e:
            logging.warning(f"Falha ao acessar a coleção '{name}': {e}")
            continue
        try:
            res = collection.query(query_texts=[user_input], n_results=2)
            logging.info(f"Resultados da coleção '{name}': {len(res.get('documents', [[]])[0])} documentos encontrados")
        except Exception as e:
            logging.warning(f"Falha na consulta da coleção '{name}': {e}")
            continue
        docs = res.get("documents", [[]])[0]
        metas = res.get("metadatas", [[]])[0]
        for doc, meta in zip(docs, metas):
            if doc:
                results.append({
                    "collection": name,
                    "document": doc,
                    "metadata": meta or {},
                })

    preferred_type = state['preferencia'] or 'texto'
    type_map = {
        'texto': ['texts', 'pdfs'],
        'vídeo': ['videos'],
        'video': ['videos'],
        'áudio': ['videos'], 
        'audio': ['videos'],
        'imagem': ['images']
    }
    priority = type_map.get(preferred_type, ['texts'])

    results.sort(key=lambda r: 0 if r['collection'] in priority else 1)
    results = results[:3]

    if not results:
        logging.info(f"Nenhuma correspondência encontrada para '{user_input}'")
        return ("Desculpe, não encontrei conteúdos relevantes para sua busca no momento. "
                "Tente reformular sua pergunta ou escolha outro tema.")

    main = results[0]
    main_trecho = summarize(main["document"])
    main_file = main["metadata"].get("source", "desconhecido")
    main_type = main["collection"]

    resposta = (
        f"Aqui está um conteúdo selecionado especialmente para você, conforme sua preferência por **{preferred_type}**:\n\n"
        f"**Resumo:** {main_trecho}\n\n"
        f"_Fonte: {main_file} (tipo: {main_type})_\n"
    )

    if len(results) > 1:
        resposta += "\nOutras fontes que podem complementar seu aprendizado:\n"
        for r in results[1:]:
            file_name = r["metadata"].get("source", "desconhecido")
            doc_type = r["collection"]
            trecho = summarize(r["document"])
            resposta += f"- **{file_name}** ({doc_type}): {trecho}\n"

    if state["dificuldade"] == "nenhuma":
        resposta += ("\nCaso queira se aprofundar em algum tópico específico, fique à vontade para perguntar!\n")

    resposta += (f"\n\n**Seu perfil:** Nível: {state['nivel'].capitalize()}, "
                 f"Preferência: {state['preferencia'].capitalize()}, "
                 f"Dificuldade: {state['dificuldade'].capitalize() if state['dificuldade'] else 'Não informada'}")

    logging.info(f"Resposta gerada (início): {resposta[:100]}...")
    return resposta

if __name__ == "__main__":
    pergunta = input("Digite sua pergunta: ")
    resposta = generate_adaptive_prompt(pergunta)
    print("\n=== Resposta Adaptativa ===\n")
    print(resposta)
=======
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

CHROMA_PATH = "chroma_db"

def summarize(text: str, max_chars: int = 400) -> str:
    """Retorna um resumo simples do texto (primeiras frases ou até max_chars)."""
    if len(text) <= max_chars:
        return text
    # Tenta cortar no final de frase
    end = text.find('.', max_chars)
    if end == -1:
        end = max_chars
    return text[:end+1] + '...'

def generate_adaptive_prompt(user_input: str):
    # Busca semântica em todas as coleções, incluindo imagens
    results: List[dict] = []
    for collection_name in ["texts", "exercises", "pdfs", "videos", "images"]:
        try:
            collection = client.get_collection(collection_name, embedding_function=hf_ef)
            res = collection.query(query_texts=[user_input], n_results=2)
            for doc, meta in zip(res["documents"][0], res["metadatas"][0]):
                results.append({
                    "collection": collection_name,
                    "document": doc,
                    "metadata": meta
                })
        except Exception:
            continue
    if not results:
        return "Nenhum conteúdo relevante encontrado."
    # Monta uma resposta explicativa para cada fonte
    explanations = []
    for r in results:
        file_name = r["metadata"].get("source", "desconhecido")
        tipo = r["collection"]
        trecho = summarize(r["document"])
        explanations.append(f"Fonte: {file_name} (tipo: {tipo})\nTrecho relevante: {trecho}")
    resposta = "\n\n".join(explanations)
    return resposta 
>>>>>>> 1a2aef2be476b4f276ce1d6a88a7ceea75d47cfc
