
### Exemplo em Imagem
![Exemplo de uso do chat adaptativo](prototipo/IA.png)
> *A imagem acima mostra a interface do chat, com sugestões de temas, botões de escolha e uma resposta personalizada da I.A.*


## Como rodar o projeto

1. **Ative o ambiente virtual**
   ```bash
   source venv/bin/activate
   ```

2. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

3. **Garanta permissões de escrita/leitura na pasta do banco**
   ```bash
   chmod -R u+rw chroma_db/
   ```

4. **Reindexe os dados (opcional, mas recomendado após alterações nos arquivos de resources)**
   ```bash
   python -m backend.main
   ```

5. **Inicie o backend (FastAPI)**
   ```bash
   uvicorn backend.main:app --reload
   ```

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

## Como funciona a conversa adaptativa com a IA

O sistema utiliza uma lógica de chat adaptativo, onde a IA conduz o estudante por etapas para personalizar o aprendizado:

1. **Identificação do nível:**  
   A IA pergunta se o estudante é iniciante, intermediário ou avançado.

2. **Preferência de formato:**  
   Em seguida, pergunta qual formato de conteúdo o estudante prefere (texto, vídeo, áudio ou imagem).

3. **Dificuldades específicas:**  
   A IA questiona se há algum tema ou tópico que o estudante considera mais difícil (ex: HTML, CSS, JavaScript, etc).

4. **Entrega personalizada:**  
   Com base nessas respostas, a IA busca e retorna conteúdos relevantes, indicando a fonte e o tipo de material.

### Exemplo de diálogo adaptativo

```
IA: Qual seu nível de conhecimento sobre o tema? (Iniciante, Intermediário, Avançado)
Estudante: Iniciante

IA: Qual formato de aprendizado você prefere? (Texto, Vídeo, Áudio, Imagem)
Estudante: Vídeo

IA: Existe algum tópico específico que você considera mais desafiador? (Nenhuma, HTML, CSS, JavaScript, Outro)
Estudante: CSS

IA: Aqui está um vídeo selecionado especialmente para você sobre CSS. Fonte: Dica do professor.mp4 (tipo: vídeos)
```
