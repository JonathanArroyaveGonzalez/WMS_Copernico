// chatbot.js - Script mejorado para el chatbot con IA

document.addEventListener('DOMContentLoaded', function() {
    const messageInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');
    const typingIndicator = document.getElementById('typing-indicator');
    const clearHistoryBtn = document.getElementById('clear-history-btn');
    const refreshInsightsBtn = document.getElementById('refresh-insights-btn');
    
    // Inicializar Mermaid
    if (typeof mermaid !== 'undefined') {
        mermaid.initialize({
            startOnLoad: false,
            theme: 'default',
            securityLevel: 'loose',
            flowchart: {
                useMaxWidth: true,
                htmlLabels: true,
                curve: 'basis'
            }
        });
        // Renderizar diagramas existentes en el historial después de que el DOM esté listo
        setTimeout(() => {
            renderMermaidDiagrams();
        }, 200);
    }
    
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
                // Agregar respuesta del bot (usar HTML pre-renderizado del servidor)
                addBotMessage(data.response_html || data.response, data.timestamp);
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
    
    function addBotMessage(responseHtml, timestamp) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message fade-in';
        
        // El servidor ya envía el HTML renderizado, lo usamos directamente
        messageDiv.innerHTML = `
            <div class='message-content'>
                <div class='message-icon-wrapper bot-icon'>
                    <i class='fas fa-robot message-icon'></i>
                </div>
                <div class='message-bubble'>
                    <div class='message-text markdown-content'>${responseHtml}</div>
                    <div class='message-time'>${formatTime(new Date(timestamp))}</div>
                </div>
            </div>
        `;
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
        
        // Renderizar diagramas Mermaid si existen
        renderMermaidDiagrams();
    }
    
    // formatMarkdown ya no es necesario para mensajes nuevos,
    // pero lo mantenemos por si se necesita para fallback o errores
    function formatMarkdown(text) {
        // Almacenar bloques de código Mermaid temporalmente
        const mermaidBlocks = [];
        const mermaidPlaceholder = '@@MERMAID_PLACEHOLDER@@';
        
        // Extraer bloques de código Mermaid
        text = text.replace(/```mermaid\s*\n([\s\S]*?)```/gi, function(match, code) {
            mermaidBlocks.push(code.trim());
            return mermaidPlaceholder;
        });
        
        // Almacenar otros bloques de código
        const codeBlocks = [];
        const codePlaceholder = '@@CODE_PLACEHOLDER@@';
        
        // Extraer bloques de código genéricos ```code```
        text = text.replace(/```(\w*)\s*\n([\s\S]*?)```/g, function(match, lang, code) {
            codeBlocks.push({ lang: lang, code: code.trim() });
            return codePlaceholder;
        });
        
        // Extraer código inline `code`
        const inlineCode = [];
        const inlinePlaceholder = '@@INLINE_CODE@@';
        text = text.replace(/`([^`]+)`/g, function(match, code) {
            inlineCode.push(code);
            return inlinePlaceholder;
        });
        
        // Extraer y procesar tablas Markdown ANTES de escapar HTML
        const tables = [];
        const tablePlaceholder = '@@TABLE_PLACEHOLDER@@';
        text = text.replace(/(?:^|\n)((?:\|[^\n]+\|\n)+)/g, function(match, tableContent) {
            const lines = tableContent.trim().split('\n');
            if (lines.length < 2) return match;
            
            // Verificar si la segunda línea es separador (|---|---|)
            const separatorLine = lines[1];
            if (!/^\|[\s:-]+\|$/.test(separatorLine.replace(/\|/g, '|').replace(/[^|:-\s]/g, ''))) {
                // No es una tabla válida, verificar de otra forma
                if (!separatorLine.includes('---') && !separatorLine.includes(':--') && !separatorLine.includes('--:')) {
                    return match;
                }
            }
            
            let tableHtml = '<table>';
            
            // Header row
            const headerCells = lines[0].split('|').filter(cell => cell.trim() !== '');
            tableHtml += '<thead><tr>';
            headerCells.forEach(cell => {
                tableHtml += `<th>${cell.trim()}</th>`;
            });
            tableHtml += '</tr></thead>';
            
            // Body rows (skip header and separator)
            tableHtml += '<tbody>';
            for (let i = 2; i < lines.length; i++) {
                const cells = lines[i].split('|').filter(cell => cell.trim() !== '');
                if (cells.length > 0) {
                    tableHtml += '<tr>';
                    cells.forEach(cell => {
                        tableHtml += `<td>${cell.trim()}</td>`;
                    });
                    tableHtml += '</tr>';
                }
            }
            tableHtml += '</tbody></table>';
            
            tables.push(tableHtml);
            return '\n' + tablePlaceholder + '\n';
        });
        
        // Escapar HTML en el texto restante
        text = escapeHtml(text);
        
        // Líneas horizontales ---
        text = text.replace(/^---+$/gm, '<hr>');
        
        // Encabezados ### Título
        text = text.replace(/^### (.+)$/gm, '<h4>$1</h4>');
        text = text.replace(/^## (.+)$/gm, '<h3>$1</h3>');
        text = text.replace(/^# (.+)$/gm, '<h2>$1</h2>');
        
        // Negritas **texto**
        text = text.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
        
        // Itálicas *texto*
        text = text.replace(/\*(.+?)\*/g, '<em>$1</em>');
        
        // Listas con viñetas - y •
        text = text.replace(/^[-•]\s+(.+)$/gm, '<li>$1</li>');
        text = text.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');
        
        // Listas numeradas
        text = text.replace(/^\d+\.\s+(.+)$/gm, '<li>$1</li>');
        
        // Links [texto](url)
        text = text.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank">$1</a>');
        
        // Convertir saltos de línea a <br> (pero no dentro de listas)
        text = text.replace(/\n/g, '<br>');
        
        // Limpiar <br> extras alrededor de elementos de bloque
        text = text.replace(/<br>(<h[234]>)/g, '$1');
        text = text.replace(/(<\/h[234]>)<br>/g, '$1');
        text = text.replace(/<br>(<ul>)/g, '$1');
        text = text.replace(/(<\/ul>)<br>/g, '$1');
        text = text.replace(/<br>(<li>)/g, '$1');
        text = text.replace(/(<\/li>)<br>/g, '$1');
        text = text.replace(/<br>(<hr>)/g, '$1');
        text = text.replace(/(<hr>)<br>/g, '$1');
        
        // Restaurar código inline
        inlineCode.forEach(code => {
            text = text.replace(inlinePlaceholder, `<code class="inline-code">${escapeHtml(code)}</code>`);
        });
        
        // Restaurar bloques de código
        codeBlocks.forEach(block => {
            const langClass = block.lang ? ` class="language-${block.lang}"` : '';
            text = text.replace(codePlaceholder, `<pre><code${langClass}>${escapeHtml(block.code)}</code></pre>`);
        });
        
        // Restaurar bloques Mermaid
        mermaidBlocks.forEach(code => {
            text = text.replace(mermaidPlaceholder, `<pre class="mermaid">${code}</pre>`);
        });
        
        // Restaurar tablas
        tables.forEach(tableHtml => {
            text = text.replace(tablePlaceholder, tableHtml);
        });
        
        // Limpiar <br> alrededor de tablas
        text = text.replace(/<br>(<table>)/g, '$1');
        text = text.replace(/(<\/table>)<br>/g, '$1');
        
        return text;
    }
    
    function renderMermaidDiagrams() {
        // Verificar si Mermaid está disponible
        if (typeof mermaid !== 'undefined') {
            try {
                // Buscar elementos mermaid no procesados (que no tengan SVG dentro)
                const mermaidElements = document.querySelectorAll('pre.mermaid');
                mermaidElements.forEach((element, index) => {
                    // Solo procesar si no tiene ya un SVG renderizado
                    if (!element.querySelector('svg') && !element.hasAttribute('data-processed')) {
                        element.setAttribute('data-processed', 'true');
                        const graphId = `mermaid-graph-${Date.now()}-${index}`;
                        const graphDefinition = element.textContent || element.innerText;
                        
                        // Usar mermaid.render para renderizar el diagrama
                        mermaid.render(graphId, graphDefinition.trim())
                            .then(({ svg }) => {
                                element.innerHTML = svg;
                            })
                            .catch(err => {
                                console.error('Error renderizando Mermaid:', err);
                                element.innerHTML = `<div class="mermaid-error">Error al renderizar diagrama: ${err.message}</div>`;
                            });
                    }
                });
            } catch (e) {
                console.error('Error en renderMermaidDiagrams:', e);
            }
        }
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