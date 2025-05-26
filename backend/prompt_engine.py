import os
import logging
from typing import List
from chromadb.errors import NotFoundError
from backend.db_config import client, hf_ef
import unicodedata

logging.basicConfig(
    level=logging.INFO,
    format='[%(levelname)s] %(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

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
    nivel_keywords = ["iniciante", "intermediario", "intermediário", "avancado", "avançado"]
    preferencia_keywords = ["texto", "video", "vídeo", "audio", "áudio", "imagem"]
    dificuldade_opcoes = ["nenhuma", "html", "css", "javascript", "outro"]

    user_input_norm = normalize(user_input)

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

    saudacoes = [
        "ola", "olá", "oi", "bom dia", "boa tarde", "boa noite", "eae", "opa", "salve"
    ]
    if any(user_input_norm.startswith(normalize(s)) for s in saudacoes):
        return (
            "Oi! Que bom te ver por aqui! 😊\n"
            "Pra começar, me conta: qual seu nível de conhecimento sobre o tema?\n"
            "[OPCOES] Iniciante | Intermediário | Avançado"
        )

    if not state["nivel"]:
        if user_input_norm and user_input_norm not in [normalize(x) for x in nivel_keywords]:
            return (
                "Quase lá! Só preciso que você escolha uma dessas opções para eu te conhecer melhor:\n"
                "- Iniciante\n- Intermediário\n- Avançado\n"
                "Com qual dessas você se identifica mais?"
            )
        for word in nivel_keywords:
            if user_input_norm == normalize(word):
                update_user_state(session_id, nivel=word)
                return (
                    f"Legal, você escolheu: {word.capitalize()}! 😊\n"
                    "Agora me conta, como você prefere aprender?\n"
                    "- Texto\n- Vídeo\n- Áudio\n- Imagem"
                )

    elif not state["preferencia"]:
        if user_input_norm and user_input_norm not in [normalize(x) for x in preferencia_keywords]:
            return (
                "Quase lá! Só preciso que você escolha um formato entre:\n"
                "- Texto\n- Vídeo\n- Áudio\n- Imagem\n"
                "Qual deles você prefere para aprender?"
            )
        for word in preferencia_keywords:
            if user_input_norm == normalize(word):
                update_user_state(session_id, preferencia=word)
                return (
                    f"Show! Você prefere aprender por: {word.capitalize()}! 🎉\n"
                    "Agora, tem algum assunto que você acha mais difícil ou gostaria de focar?\n"
                    "- Nenhuma\n- HTML\n- CSS\n- JavaScript\n- Outro"
                )

    elif not state["dificuldade"]:
        if user_input_norm and user_input_norm not in [normalize(x) for x in dificuldade_opcoes]:
            return (
                "Ótimo! Agora, só mais uma coisinha: escolha uma dificuldade entre:\n"
                "- Nenhuma\n- HTML\n- CSS\n- JavaScript\n- Outro\n"
                "Qual dessas opções tem mais a ver com o que você quer aprender ou sente dificuldade?"
            )
        for word in dificuldade_opcoes:
            if user_input_norm == normalize(word):
                update_user_state(session_id, dificuldade=word)
                return (
                    f"Beleza! Dificuldade escolhida: {word.capitalize()}! Obrigado por compartilhar, vou buscar conteúdos feitos pra você. 😉"
                )

    if not state["nivel"]:
        return (
            "Antes de continuarmos, me conta: qual seu nível de conhecimento sobre o tema? "
            "(iniciante, intermediário ou avançado)\n\n"
            "Se quiser, pode começar por um desses temas:\n"
            "- HTML5\n- CSS\n- JavaScript\n- Acessibilidade Web\n- Estrutura de uma página\n"
            "Ou, se preferir, digite sua dúvida! Estou aqui pra ajudar."
        )
    if not state["preferencia"]:
        return ("Pra deixar tudo do seu jeito, como você prefere aprender? "
                "(texto, vídeo, áudio ou imagem)")
    if not state["dificuldade"]:
        return ("Tem algum assunto que você acha mais difícil ou gostaria de focar? Me conta! 😊")

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

    # Detectar preferências explícitas do usuário na resposta
    preferencias_explicitas = {
        'exemplo': 'exemplo',
        'exemplos': 'exemplo',
        'video': 'vídeo',
        'vídeo': 'vídeo',
        'imagem': 'imagem',
        'imagens': 'imagem',
        'desafio': 'desafio',
        'explicacao': 'explicação',
        'explicação': 'explicação',
        'resumo': 'resumo',
        'texto': 'texto',
        'fácil': 'fácil',
        'facil': 'fácil',
        'avançado': 'avançado',
        'avancado': 'avançado',
        'dica': 'dica',
        'dicas': 'dica',
    }
    for palavra, tipo in preferencias_explicitas.items():
        if palavra in user_input_norm:
            state['preferencia_explicita'] = tipo
            break

    # Se houver preferência explícita, priorizar esse tipo de conteúdo
    preferencia_explicita = state.get('preferencia_explicita')
    if preferencia_explicita:
        if preferencia_explicita in ['vídeo', 'video']:
            preferred_type = 'vídeo'
        elif preferencia_explicita == 'imagem':
            preferred_type = 'imagem'
        elif preferencia_explicita == 'exemplo':
            priority = ['exercises'] + priority
        elif preferencia_explicita == 'desafio':
            priority = ['exercises'] + priority
        elif preferencia_explicita == 'texto' or preferencia_explicita == 'resumo':
            preferred_type = 'texto'

        del state['preferencia_explicita']
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

    if 'historico_temas' not in state:
        state['historico_temas'] = []

    # Detecta se o usuário está mudando de tema após já ter passado pela avaliação
    temas_validos = ["html", "css", "javascript", "acessibilidade", "outro"]
    if state.get("avaliado") and user_input_norm in [normalize(t) for t in temas_validos]:
        # Reinicia apenas a dificuldade e avaliação, mantém nível e preferência
        update_user_state(session_id, dificuldade=user_input_norm)
        state["avaliado"] = False
        if user_input_norm not in state['historico_temas']:
            state['historico_temas'].append(user_input_norm)
        return (
            f"Legal! Agora vamos focar em {user_input.strip().capitalize()}! Se quiser, me conta se tem alguma dúvida específica ou quer um conteúdo geral sobre {user_input.strip().capitalize()}."
        )

    if state["dificuldade"] and not state.get("avaliado"):
        if user_input_norm == normalize(state["dificuldade"]):
            state["avaliado"] = True
        else:
            state["avaliado"] = True
            return f"Pra eu te ajudar ainda melhor em {state['dificuldade']}, me conta com suas palavras o que você já sabe sobre esse tema? Pode ser bem à vontade!\n(Se quiser pular, é só digitar o nome do tema de novo ou outro tema que queira aprender!)"

    # Ao buscar resultados, evitar repetir o mesmo conteúdo para o mesmo tema
    resultados_mostrados = state.get('resultados_mostrados', {})
    tema_atual = normalize(state.get('dificuldade', ''))
    if tema_atual and tema_atual in resultados_mostrados:
        ids_mostrados = set(resultados_mostrados[tema_atual])
    else:
        ids_mostrados = set()

    novos_results = []
    for r in results:
        doc_id = r['metadata'].get('source', '') + r['document'][:30]
        if doc_id not in ids_mostrados:
            novos_results.append(r)
    if novos_results:
        if tema_atual:
            if tema_atual not in resultados_mostrados:
                resultados_mostrados[tema_atual] = []
            for r in novos_results:
                doc_id = r['metadata'].get('source', '') + r['document'][:30]
                resultados_mostrados[tema_atual].append(doc_id)
            state['resultados_mostrados'] = resultados_mostrados
        results = novos_results
    else:
        sugestao = ""
        if preferred_type in ['texto', 'pdfs']:
            sugestao = "Quer tentar ver um vídeo ou imagem sobre esse tema? Ou me pergunte algo mais específico!"
        elif preferred_type in ['videos']:
            sugestao = "Que tal ver um texto ou exercício sobre esse tema? Ou me pergunte algo mais específico!"
        else:
            sugestao = "Se quiser, posso buscar outros formatos ou você pode escolher outro tema!"
        return (
            f"Acho que já te mostrei o principal sobre {tema_atual.capitalize()} nesse formato. {sugestao}"
        )

    main = results[0]
    main_trecho = summarize(main["document"])
    main_file = main["metadata"].get("source", "desconhecido")
    main_type = main["collection"]

    if main_type == 'images':
        descricao = main["metadata"].get("description")
        if not descricao:
            descricao = main["document"].split(". ")[0][:200]
        resposta = (
            f"Olha só o que encontrei pra você, do jeitinho que você gosta (imagem):\n\n"
            f"Descrição da imagem: {descricao}\n\n"
            f"_Fonte: {main_file} (tipo: {main_type})_\n"
        )
    else:
        resposta = (
            f"Olha só o que encontrei pra você, do jeitinho que você gosta (**{preferred_type}**):\n\n"
            f"**Resumo:** {main_trecho}\n\n"
            f"_Fonte: {main_file} (tipo: {main_type})_\n"
        )

    if len(results) > 1:
        resposta += "\nOutras dicas que podem te ajudar também:\n"
        for r in results[1:]:
            file_name = r["metadata"].get("source", "desconhecido")
            doc_type = r["collection"]
            trecho = summarize(r["document"])
            resposta += f"- **{file_name}** ({doc_type}): {trecho}\n"

    if state["dificuldade"] == "nenhuma":
        resposta += ("\nSe quiser se aprofundar em algum tema, é só falar! Estou aqui pra te ajudar a ir mais longe.\n")

    resposta += (f"\n\n**Seu perfil:** Nível: {state['nivel'].capitalize()}, "
                 f"Preferência: {state['preferencia'].capitalize()}, "
                 f"Dificuldade: {state['dificuldade'].capitalize() if state['dificuldade'] else 'Não informada'}")

    logging.info(f"Resposta gerada (início): {resposta[:100]}...")

    return resposta

def avaliar_conhecimento(user_input, tema):
    respostas_esperadas = {
        "html": ["tag", "<html>", "estrutura", "elemento"],
        "css": ["estilo", "cor", "font", "seletores"],
        "javascript": ["função", "variável", "evento", "console.log"]
    }
    palavras = respostas_esperadas.get(tema.lower(), [])
    acertos = sum(1 for p in palavras if p in user_input.lower())
    if acertos >= 2:
        return "Ótimo! Você já tem uma boa noção desse tema. Quer se aprofundar ou tentar um desafio?"
    else:
        return "Percebi que você ainda tem dúvidas. Posso te explicar de outra forma ou sugerir um vídeo/texto?"

if __name__ == "__main__":
    pergunta = input("Digite sua pergunta: ")
    resposta = generate_adaptive_prompt(pergunta)
    print("\n=== Resposta Adaptativa ===\n")
    print(resposta)