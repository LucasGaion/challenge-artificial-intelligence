<<<<<<< HEAD


## Como rodar o projeto

1. **Ative o ambiente virtual**
   ```bash
   source venv/bin/activate
   ```

2. **Instale as dependências**
=======
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
>>>>>>> 1a2aef2be476b4f276ce1d6a88a7ceea75d47cfc
   ```bash
   pip install -r requirements.txt
   ```

<<<<<<< HEAD
3. **Garanta permissões de escrita/leitura na pasta do banco**
   ```bash
   chmod -R u+rw chroma_db/
   ```

4. **Reindexe os dados (opcional, mas recomendado após alterações nos arquivos de resources)**
   ```bash
   python -m backend.main
   ```

5. **Inicie o backend (FastAPI)**
=======
4. **Execute a API:**
>>>>>>> 1a2aef2be476b4f276ce1d6a88a7ceea75d47cfc
   ```bash
   uvicorn backend.main:app --reload
   ```

<<<<<<< HEAD
6. **Sirva o frontend (HTML) em outro terminal**
   ```bash
   cd <diretório onde está o index.html>
   python -m http.server 8000
   ```

7. **Acesse o sistema**
   - Abra o navegador em: [http://localhost:8000/index.html](http://localhost:8000/index.html)

---

## Resolvendo problemas comuns

- **CORS (Cross-Origin Resource Sharing):**
  - Certifique-se de que o backend FastAPI está com o middleware CORS habilitado:
    ```python
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    ```
  - Use sempre o mesmo host (localhost ou 127.0.0.1) no frontend e backend.

- **Permissão de escrita/leitura no banco:**
  - Se der erro de permissão, rode:
    ```bash
    chmod -R u+rw chroma_db/
    ```

- **Reindexação:**
  - Sempre que alterar arquivos em `resources/`, rode novamente:
    ```bash
    python -m backend.main
    ```

---

## Exemplos de uso do chat

- Pergunte sobre HTML5, listas, âncoras, tabelas, etc.
- O bot irá buscar respostas nos arquivos indexados e indicar a fonte.

## Exemplos Visuais de Uso

Abaixo você encontra exemplos práticos de como a I.A funciona na prática. **O vídeo (IA.mov) e a imagem (IA.png) estão incluídos dentro deste protótipo do projeto.**

### Demonstração em Vídeo

https://github.com/seu-usuario/seu-repo/raw/main/IA.mov

> *Assista ao vídeo acima para ver uma conversa real com a I.A, desde a personalização do chat até a sugestão de conteúdos adaptativos e interativos.*

### Exemplo em Imagem

![Exemplo de uso do chat adaptativo](IA.png)

> *A imagem acima mostra a interface do chat, com sugestões de temas, botões de escolha e uma resposta personalizada da I.A.*
=======
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
>>>>>>> 1a2aef2be476b4f276ce1d6a88a7ceea75d47cfc
