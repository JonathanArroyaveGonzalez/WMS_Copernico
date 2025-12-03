// chatbot.js - Script mejorado para el chatbot con IA

document.addEventListener('DOMContentLoaded', function() {
    const messageInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    const typingIndicator = document.getElementById('typing-indicator');
    const clearHistoryBtn = document.getElementById('clear-history-btn');
    const refreshInsightsBtn = document.getElementById('refresh-insights-btn');
    
    // Auto-resize del textarea
    messageInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 150) + 'px';
    });
    
    // Enviar mensaje con Enter (Shift+Enter para nueva línea)
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Botón de enviar
    sendBtn.addEventListener('click', sendMessage);
    
    // Limpiar historial
    clearHistoryBtn.addEventListener('click', clearHistory);
    
    // Actualizar insights
    if (refreshInsightsBtn) {
        refreshInsightsBtn.addEventListener('click', refreshInsights);
    }
    
    // Botones de sugerencias
    document.querySelectorAll('.suggestion-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const question = this.getAttribute('data-question');
            messageInput.value = question;
            messageInput.focus();
            // Auto enviar
            setTimeout(() => sendMessage(), 100);
        });
    });
    
    // Scroll automático al final
    scrollToBottom();
    
    function sendMessage() {
        const message = messageInput.value.trim();
        
        if (!message) {
            return;
        }
        
        // Deshabilitar input mientras se procesa
        messageInput.disabled = true;
        sendBtn.disabled = true;
        
        // Agregar mensaje del usuario a la UI
        addUserMessage(message);
        
        // Limpiar input
        messageInput.value = '';
        messageInput.style.height = 'auto';
        
        // Mostrar indicador de escritura
        typingIndicator.style.display = 'flex';
        scrollToBottom();
        
        // Enviar mensaje al servidor
        fetch('/chatbot/send-message/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            // Ocultar indicador de escritura
            typingIndicator.style.display = 'none';
            
            if (data.success) {
                // Agregar respuesta del bot
                addBotMessage(data.response, data.timestamp);
            } else {
                // Mostrar error
                addBotMessage('Lo siento, hubo un error: ' + data.error, new Date().toISOString());
            }
        })
        .catch(error => {
            typingIndicator.style.display = 'none';
            addBotMessage('Error de conexión. Por favor, intenta de nuevo.', new Date().toISOString());
            console.error('Error:', error);
        })
        .finally(() => {
            // Rehabilitar input
            messageInput.disabled = false;
            sendBtn.disabled = false;
            messageInput.focus();
        });
    }
    
    function addUserMessage(message) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message fade-in';
        messageDiv.innerHTML = `
            <div class='message-content'>
                <div class='message-icon-wrapper'>
                    <i class='fas fa-user message-icon'></i>
                </div>
                <div class='message-bubble'>
                    <div class='message-text'>${escapeHtml(message)}</div>
                    <div class='message-time'>${formatTime(new Date())}</div>
                </div>
            </div>
        `;
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }
    
    function addBotMessage(response, timestamp) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message fade-in';
        
        // Formatear el mensaje con markdown básico
        const formattedResponse = formatMarkdown(response);
        
        messageDiv.innerHTML = `
            <div class='message-content'>
                <div class='message-icon-wrapper bot-icon'>
                    <i class='fas fa-robot message-icon'></i>
                </div>
                <div class='message-bubble'>
                    <div class='message-text markdown-content'>${formattedResponse}</div>
                    <div class='message-time'>${formatTime(new Date(timestamp))}</div>
                </div>
            </div>
        `;
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }
    
    function formatMarkdown(text) {
        // Escapar HTML primero
        text = escapeHtml(text);
        
        // Negritas **texto**
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Itálicas *texto*
        text = text.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        // Convertir saltos de línea a <br>
        text = text.replace(/\n/g, '<br>');
        
        // Emojis y viñetas
        text = text.replace(/•/g, '•');
        
        return text;
    }
    
    function clearHistory() {
        if (!confirm('¿Estás seguro de que quieres limpiar todo el historial?')) {
            return;
        }
        
        fetch('/chatbot/clear-history/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Recargar la página para mostrar mensaje de bienvenida
                location.reload();
            } else {
                alert('Error al limpiar historial: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error de conexión');
        });
    }
    
    function refreshInsights() {
        const btn = refreshInsightsBtn;
        btn.disabled = true;
        btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Actualizando...';
        
        fetch('/chatbot/get-insights/', {
            method: 'GET',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Agregar insights como mensaje del bot
                addBotMessage('📊 **Insights Actualizados**\n\n' + data.insights, new Date().toISOString());
                
                // Obtener nuevas sugerencias
                return fetch('/chatbot/get-suggestions/', {
                    method: 'GET',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken')
                    }
                });
            } else {
                throw new Error(data.error);
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                addBotMessage('💡 **Preguntas Sugeridas**\n\n' + data.suggestions, new Date().toISOString());
            }
        })
        .catch(error => {
            console.error('Error:', error);
            addBotMessage('Error al actualizar insights: ' + error.message, new Date().toISOString());
        })
        .finally(() => {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-sync-alt"></i> Actualizar';
        });
    }
    
    function scrollToBottom() {
        setTimeout(() => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }, 100);
    }
    
    function formatTime(date) {
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        return `${hours}:${minutes}`;
    }
    
    function escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});