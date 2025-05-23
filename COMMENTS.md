<<<<<<< HEAD
# Comentários do Projeto

## Decisão da Arquitetura Utilizada

- **Backend:** Python (FastAPI)
- **Indexação e Busca Semântica:** ChromaDB (embeddings), HuggingFace (all-MiniLM-L6-v2) para embeddings
=======
# COMMENTS.md

## Decisão da arquitetura utilizada
- **Backend:** Python (FastAPI)
- **Indexação e Busca Semântica:** ChromaDB (embeddings), HuggingFace (all-MiniLM-L6-v2) para embeddings.
>>>>>>> 1a2aef2be476b4f276ce1d6a88a7ceea75d47cfc
- **Processamento de PDFs:** pdfplumber
- **Transcrição de Vídeos:** Whisper (OpenAI)
- **Banco de Dados:** ChromaDB + arquivos locais para metadados
- **Prompt Adaptativo:** Busca semântica + sumarização dos trechos mais relevantes de cada fonte
- **Modularização:** Funções de indexação separadas por tipo de arquivo em módulos distintos

<<<<<<< HEAD
---

## Bibliotecas de Terceiros Utilizadas

=======
## Bibliotecas de terceiros utilizadas
>>>>>>> 1a2aef2be476b4f276ce1d6a88a7ceea75d47cfc
- fastapi
- uvicorn
- chromadb
- pdfplumber
- whisper
- ffmpeg-python
- python-dotenv
- tqdm
- pillow
- pytesseract
- rich

<<<<<<< HEAD
---

## Funcionalidades Implementadas

=======
## Funcionalidades implementadas
>>>>>>> 1a2aef2be476b4f276ce1d6a88a7ceea75d47cfc
- Indexação de textos, exercícios (JSON), PDFs, vídeos (transcrição) e imagens (OCR)
- Endpoints REST para indexação de cada tipo de arquivo
- Cada endpoint retorna o conteúdo indexado de cada arquivo
- Busca adaptativa que retorna trechos relevantes de todas as fontes
- Modularização do backend para facilitar manutenção e expansão

<<<<<<< HEAD
---

## Melhorias se Tivesse Mais Tempo

=======
## Melhorias se tivesse mais tempo
- Interface web (React)
>>>>>>> 1a2aef2be476b4f276ce1d6a88a7ceea75d47cfc
- Indexação de imagens com visão computacional além de OCR
- Suporte a múltiplos usuários e autenticação
- Deploy em nuvem
- Testes automatizados

<<<<<<< HEAD
---

## Requisitos Obrigatórios Não Entregues

> **Todos os requisitos obrigatórios foram entregues conforme especificação do desafio.**
=======
## Requisitos obrigatórios não entregues
- Todos os requisitos obrigatórios foram entregues conforme especificação do desafio. 
>>>>>>> 1a2aef2be476b4f276ce1d6a88a7ceea75d47cfc
