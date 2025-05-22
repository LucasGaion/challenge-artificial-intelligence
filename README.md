# Sistema de Aprendizagem Adaptativa com IA

Este projeto é um backend em Python (FastAPI) para indexação, busca semântica e sumarização de conteúdos educacionais em diversos formatos: textos, exercícios (JSON), PDFs, vídeos (transcrição) e imagens (OCR). Utiliza ChromaDB para armazenamento e busca semântica, com embeddings do modelo HuggingFace all-MiniLM-L6-v2.

## Estrutura do Projeto

```
challenge-artificial-intelligence-main/
├── backend/
│   ├── main.py                # API FastAPI principal
│   ├── prompt_engine.py       # Engine de busca adaptativa
│   ├── indexer/               # Funções modulares de indexação
│   │   ├── __init__.py
│   │   ├── index_texts.py
│   │   ├── index_pdfs.py
│   │   ├── index_videos.py
│   │   ├── index_images.py
│   │   └── save_response.py
│   └── test_curls.py          # Script de testes dos endpoints via curl
├── resources/                 # Arquivos a serem indexados
│   ├── Apresentação.txt
│   ├── Exercícios.json
│   ├── Capítulo do Livro.pdf
│   ├── Dica do professor.mp4
│   └── Infografico-1.jpg
├── chroma_db/                 # Banco de dados ChromaDB
├── requirements.txt           # Dependências do projeto
├── README.md                  # Este arquivo
└── COMMENTS.md                # Comentários técnicos e decisões
```

## Como rodar o projeto

1. **Clone o repositório e entre na pasta:**
   ```bash
   git clone <url-do-repo>
   cd challenge-artificial-intelligence-main
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a API:**
   ```bash
   uvicorn backend.main:app --reload
   ```

5. **Acesse a documentação interativa:**
   - [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Endpoints principais

- `POST /index/texts`   — Indexa textos e exercícios
- `POST /index/pdfs`    — Indexa PDFs
- `POST /index/videos`  — Indexa vídeos (transcrição)
- `POST /index/images`  — Indexa imagens (OCR)
- `POST /prompt`        — Busca adaptativa (retorna trechos relevantes de todos os arquivos)

### Exemplo de uso do endpoint de busca

```bash
curl -X POST http://127.0.0.1:8000/prompt \
     -H "Content-Type: application/json" \
     -d '{"user_input": "O que é inteligência artificial?"}'
```

### Exemplo de resposta
```json
{
  "response": "Fonte: Apresentação.txt (tipo: texts)\nTrecho relevante: ...\n\nFonte: Exercícios.json (tipo: exercises)\nTrecho relevante: ...\n..."
}
```

## Testes rápidos dos endpoints

Execute todos os testes de indexação e busca com:
```bash
python backend/test_curls.py
```

## Observações
- O projeto está modularizado para facilitar manutenção e expansão.
- Todos os endpoints de indexação retornam o conteúdo indexado.
- O sistema pode ser facilmente expandido para outros tipos de arquivos ou fontes.

## Melhorias sugeridas
- Interface web para uploads e buscas
- Indexação visual de imagens (além de OCR)
- Suporte a múltiplos usuários
- Testes automatizados
- Deploy em nuvem

---

Dúvidas ou sugestões? Abra uma issue ou entre em contato!
