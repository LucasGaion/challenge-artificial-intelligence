# Comentários do Projeto

## Decisão da Arquitetura Utilizada

- **Backend:** Python (FastAPI)
- **Indexação e Busca Semântica:** ChromaDB (embeddings), HuggingFace (all-MiniLM-L6-v2) para embeddings
- **Processamento de PDFs:** pdfplumber
- **Transcrição de Vídeos:** Whisper (OpenAI)
- **Banco de Dados:** ChromaDB + arquivos locais para metadados
- **Prompt Adaptativo:** Busca semântica + sumarização dos trechos mais relevantes de cada fonte
- **Modularização:** Funções de indexação separadas por tipo de arquivo em módulos distintos

---

## Bibliotecas de Terceiros Utilizadas

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

---

## Funcionalidades Implementadas

- Indexação de textos, exercícios (JSON), PDFs, vídeos (transcrição) e imagens (OCR)
- Endpoints REST para indexação de cada tipo de arquivo
- Cada endpoint retorna o conteúdo indexado de cada arquivo
- Busca adaptativa que retorna trechos relevantes de todas as fontes
- Modularização do backend para facilitar manutenção e expansão

---

## Melhorias se Tivesse Mais Tempo

- Indexação de imagens com visão computacional além de OCR
- Suporte a múltiplos usuários e autenticação
- Deploy em nuvem
- Testes automatizados

---

## Requisitos Obrigatórios Não Entregues

> **Todos os requisitos obrigatórios foram entregues conforme especificação do desafio.**