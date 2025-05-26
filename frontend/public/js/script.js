const input = document.getElementById('input');
    const send = document.getElementById('send');
    const messages = document.getElementById('messages');
    const suggestionsBox = document.getElementById('suggestions');
    const avatarSelect = document.getElementById('avatar-select');

    // Função para obter o avatar selecionado
    function getUserAvatar() {
      return localStorage.getItem('user_avatar') || '🧑';
    }
    // Evento de seleção de avatar
    if (avatarSelect) {
      avatarSelect.addEventListener('click', (e) => {
        if (e.target.classList.contains('avatar-option')) {
          const emoji = e.target.getAttribute('data-emoji');
          localStorage.setItem('user_avatar', emoji);
          document.querySelectorAll('.avatar-option').forEach(opt => opt.classList.remove('selected'));
          e.target.classList.add('selected');
        }
      });
      // Destacar avatar salvo ao carregar
      window.addEventListener('DOMContentLoaded', () => {
        const saved = getUserAvatar();
        document.querySelectorAll('.avatar-option').forEach(opt => {
          if (opt.getAttribute('data-emoji') === saved) {
            opt.classList.add('selected');
          }
        });
      });
    }

    // Adiciona mensagem ao chat com avatar
    function addMessage(text, sender) {
      const div = document.createElement('div');
      div.className = `msg ${sender}`;
      let name = '';
      if (sender === 'user') {
        const studentName = document.getElementById('studentName').value.trim();
        name = studentName ? `<span style='font-weight:600; margin-left:6px; color:#007bff;'>${studentName}</span>` : '';
      }
      const avatar = sender === 'user'
        ? `<div class="avatar" title="Você">${getUserAvatar()}</div>${name}`
        : `<div class="avatar" title="IA">🤖</div>`;
      let bubbleContent = text;
      if (sender === 'bot') {
        // Renderiza Markdown para respostas do bot
        bubbleContent = marked.parse(text);
      }
      div.innerHTML = sender === 'user'
        ? `${avatar}<div class="bubble">${bubbleContent}</div>`
        : `${avatar}<div class="bubble bot-bubble">${bubbleContent}</div>`;
      messages.appendChild(div);
      messages.scrollTop = messages.scrollHeight;
    }

    function showTyping() {
      const typing = document.createElement('div');
      typing.className = 'typing';
      typing.id = 'typing';
      typing.innerText = 'IA está digitando...';
      messages.appendChild(typing);
      messages.scrollTop = messages.scrollHeight;
    }
    function removeTyping() {
      const typing = document.getElementById('typing');
      if (typing) typing.remove();
    }

    async function fetchResponse(question) {
      try {
        // Gera ou recupera session_id único do usuário
        let sessionId = localStorage.getItem('session_id');
        if (!sessionId) {
          sessionId = crypto.randomUUID();
          localStorage.setItem('session_id', sessionId);
        }
        const res = await fetch('http://127.0.0.1:8000/prompt', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ user_input: question, preferences: { format: 'text' }, session_id: sessionId })
        });
        const data = await res.json();
        return data.response;
      } catch (error) {
        console.error('Erro ao buscar resposta:', error);
        return 'Erro ao conectar com o servidor. Tente novamente.';
      }
    }

    async function handleUserInput() {
      const question = input.value.trim();
      if (!question) return;
      addMessage(question, 'user');
      input.value = '';
      suggestionsBox.style.display = 'none';
      showTyping();
      const response = await fetchResponse(question);
      removeTyping();
      addMessage(response, 'bot');
      if (/nível de conhecimento/i.test(response)) {
        addNivelButtons();
      }
      if (/formato de aprendizado|prefere\? \(texto, vídeo, áudio ou imagem\)/i.test(response)) {
        addFormatoButtons();
      }
      if (/desafiador|dificuldade|gostaria de focar/i.test(response)) {
        addDificuldadeButtons();
      }
    }

    function fillCommand(text) {
      input.value = text;
      input.focus();
      suggestionsBox.style.display = 'none';
    }

    function addNivelButtons() {
      const div = document.createElement('div');
      div.className = 'nivel-buttons';
      div.style.display = 'flex';
      div.style.gap = '10px';
      ['Iniciante', 'Intermediário', 'Avançado'].forEach(nivel => {
        const btn = document.createElement('button');
        btn.textContent = nivel;
        btn.className = 'nivel-btn';
        btn.onclick = () => {
          input.value = nivel.toLowerCase();
          handleUserInput();
          div.remove();
        };
        div.appendChild(btn);
      });
      messages.appendChild(div);
      messages.scrollTop = messages.scrollHeight;
    }

    function addFormatoButtons() {
      const div = document.createElement('div');
      div.className = 'formato-buttons';
      div.style.display = 'flex';
      div.style.gap = '10px';
      ['Texto', 'Vídeo', 'Áudio', 'Imagem'].forEach(formato => {
        const btn = document.createElement('button');
        btn.textContent = formato;
        btn.className = 'nivel-btn'; // reutiliza o mesmo estilo dos botões de nível
        btn.onclick = () => {
          input.value = formato.toLowerCase();
          handleUserInput();
          div.remove();
        };
        div.appendChild(btn);
      });
      messages.appendChild(div);
      messages.scrollTop = messages.scrollHeight;
    }

    function addDificuldadeButtons() {
      const div = document.createElement('div');
      div.className = 'dificuldade-buttons';
      div.style.display = 'flex';
      div.style.gap = '10px';
      ['Nenhuma', 'HTML', 'CSS', 'JavaScript', 'Outro'].forEach(dif => {
        const btn = document.createElement('button');
        btn.textContent = dif;
        btn.className = 'nivel-btn';
        btn.onclick = () => {
          input.value = dif.toLowerCase();
          handleUserInput();
          div.remove();
        };
        div.appendChild(btn);
      });
      messages.appendChild(div);
      messages.scrollTop = messages.scrollHeight;
    }

    send.onclick = handleUserInput;

    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') handleUserInput();
    });

    input.addEventListener('input', () => {
      const value = input.value.trim();
      suggestionsBox.style.display = value.startsWith('/') ? 'flex' : 'none';
    });

    window.onload = () => {
      // Saudação dinâmica conforme o horário
      const now = new Date();
      const hour = now.getHours();
      let saudacao = 'Olá';
      if (hour >= 5 && hour < 12) {
        saudacao = 'Bom dia';
      } else if (hour >= 12 && hour < 18) {
        saudacao = 'Boa tarde';
      } else {
        saudacao = 'Boa noite';
      }
      addMessage(`${saudacao}! Sobre qual tema você gostaria de conversar ou aprender mais hoje?`, 'bot');
    };