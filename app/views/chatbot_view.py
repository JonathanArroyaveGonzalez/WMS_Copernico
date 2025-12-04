from django.http import HttpResponse
from app.views.layout import Layout
import markdown, re


class ChatbotView:
    """Vista del Chatbot con IA mejorada"""

    @staticmethod
    def render(user, history, quick_insights=None, suggested_questions=None):
        """Renderiza la interfaz del chatbot mejorada"""

        # Construir mensajes del historial
        history_html = ""
        if history:
            for msg in history:
                # Mensaje del usuario - escapar HTML para seguridad
                user_msg = msg["message"].replace("<", "&lt;").replace(">", "&gt;")
                # Mensaje del bot - procesar con format_markdown (ya maneja el escape internamente)
                bot_msg = msg["response"]

                history_html += f"""
                <div class='message user-message fade-in'>
                    <div class='message-content'>
                        <div class='message-icon-wrapper'>
                            <i class='fas fa-user message-icon'></i>
                        </div>
                        <div class='message-bubble'>
                            <div class='message-text'>{user_msg}</div>
                            <div class='message-time'>{msg.get("created_at", "")}</div>
                        </div>
                    </div>
                </div>
                <div class='message bot-message fade-in'>
                    <div class='message-content'>
                        <div class='message-icon-wrapper bot-icon'>
                            <i class='fas fa-robot message-icon'></i>
                        </div>
                        <div class='message-bubble'>
                            <div class='message-text markdown-content'>{ChatbotView.format_markdown(bot_msg)}</div>
                            <div class='message-time'>{msg.get("created_at", "")}</div>
                        </div>
                    </div>
                </div>
                """
        else:
            # Mensaje de bienvenida mejorado
            insights_section = ""
            if quick_insights:
                insights_section = f"""
                <div class='insights-section'>
                    <h4><i class='fas fa-chart-line'></i> Estado Actual del Inventario</h4>
                    <div class='insights-content'>
                        {ChatbotView.format_markdown(quick_insights)}
                    </div>
                </div>
                """

            suggestions_section = ""
            if suggested_questions:
                # Parsear las sugerencias y convertirlas en botones clickeables
                suggestions_lines = suggested_questions.strip().split("\n")
                suggestions_buttons = ""
                for line in suggestions_lines:
                    if line.strip():
                        # Remover emojis y limpiar
                        clean_question = line.strip()
                        # Remover guiones y emojis al inicio
                        import re

                        clean_question = re.sub(r"^[-•\d.)\s]*", "", clean_question)
                        clean_question = re.sub(
                            r"^[\U0001F300-\U0001F9FF\s]+", "", clean_question
                        )
                        if clean_question:
                            suggestions_buttons += f"""
                            <button class='suggestion-btn' data-question="{clean_question.replace('"', "&quot;")}">
                                <i class='fas fa-lightbulb'></i> {clean_question}
                            </button>
                            """

                suggestions_section = f"""
                <div class='suggestions-section'>
                    <h4><i class='fas fa-magic'></i> Preguntas Sugeridas</h4>
                    <div class='suggestions-buttons'>
                        {suggestions_buttons}
                    </div>
                </div>
                """

            history_html = f"""
            <div class='welcome-message'>
                <div class='welcome-header'>
                    <div class='welcome-icon-container'>
                        <i class='fas fa-robot welcome-icon'></i>
                    </div>
                    <h2>¡Hola, {user.get("username", "Usuario")}! 👋</h2>
                    <p class='welcome-subtitle'>Soy tu asistente inteligente de inventario</p>
                </div>
                
                <div class='welcome-content'>
                    {insights_section}
                    
                    <div class='capabilities-section'>
                        <h4><i class='fas fa-brain'></i> ¿Qué puedo hacer por ti?</h4>
                        <div class='capabilities-grid'>
                            <div class='capability-card'>
                                <i class='fas fa-search'></i>
                                <h5>Consultar Datos</h5>
                                <p>Pregúntame sobre productos, stock, precios y categorías</p>
                            </div>
                            <div class='capability-card'>
                                <i class='fas fa-chart-bar'></i>
                                <h5>Analizar Ventas</h5>
                                <p>Revisa estadísticas y tendencias de ventas y compras</p>
                            </div>
                            <div class='capability-card'>
                                <i class='fas fa-exclamation-triangle'></i>
                                <h5>Alertas Inteligentes</h5>
                                <p>Te aviso sobre stock bajo o productos agotados</p>
                            </div>
                            <div class='capability-card'>
                                <i class='fas fa-lightbulb'></i>
                                <h5>Recomendaciones</h5>
                                <p>Sugerencias para optimizar tu inventario</p>
                            </div>
                        </div>
                    </div>
                    
                    {suggestions_section}
                    
                    <div class='quick-tips'>
                        <p><strong>💡 Tip:</strong> Háblame de forma natural. Por ejemplo:</p>
                        <ul>
                            <li>"¿Qué productos necesito reordenar?"</li>
                            <li>"Muéstrame las ventas de esta semana"</li>
                            <li>"¿Cuáles son mis productos más caros?"</li>
                        </ul>
                    </div>
                </div>
            </div>
            """

        # CSS mejorado para el chatbot
        styles = """
        <style>
            .chatbot-container {
                display: flex;
                flex-direction: column;
                height: calc(100vh - 250px);
                min-height: 600px;
            }
            
            .chat-messages {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                border-radius: 8px;
                margin-bottom: 15px;
            }
            
            .message {
                margin-bottom: 20px;
                animation: fadeIn 0.3s ease-in;
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .message-content {
                display: flex;
                gap: 12px;
                align-items: flex-start;
            }
            
            .message-icon-wrapper {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                background: #007bff;
                color: white;
                flex-shrink: 0;
            }
            
            .bot-icon {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }
            
            .message-bubble {
                max-width: 70%;
                background: white;
                padding: 12px 16px;
                border-radius: 18px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            
            .user-message .message-content {
                flex-direction: row-reverse;
            }
            
            .user-message .message-bubble {
                background: #007bff;
                color: white;
            }
            
            .message-text {
                line-height: 1.6;
                word-wrap: break-word;
            }
            
            .message-time {
                font-size: 0.75rem;
                color: #6c757d;
                margin-top: 5px;
            }
            
            .user-message .message-time {
                color: rgba(255,255,255,0.8);
            }
            
            .markdown-content {
                white-space: pre-wrap;
            }
            
            .markdown-content strong {
                font-weight: 600;
                color: #2c3e50;
            }
            
            /* Welcome Message Styles */
            .welcome-message {
                background: white;
                border-radius: 12px;
                padding: 30px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            }
            
            .welcome-header {
                text-align: center;
                margin-bottom: 30px;
            }
            
            .welcome-icon-container {
                width: 80px;
                height: 80px;
                margin: 0 auto 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            
            .welcome-icon {
                font-size: 2.5rem;
                color: white;
            }
            
            .welcome-header h2 {
                color: #2c3e50;
                margin-bottom: 10px;
            }
            
            .welcome-subtitle {
                color: #7f8c8d;
                font-size: 1.1rem;
            }
            
            .insights-section, .suggestions-section, .capabilities-section {
                background: #f8f9fa;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 20px;
            }
            
            .insights-section h4, .suggestions-section h4, .capabilities-section h4 {
                color: #2c3e50;
                margin-bottom: 15px;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .insights-content {
                color: #34495e;
                line-height: 1.8;
            }
            
            .capabilities-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 15px;
                margin-top: 15px;
            }
            
            .capability-card {
                background: white;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                transition: transform 0.2s;
            }
            
            .capability-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            }
            
            .capability-card i {
                font-size: 2rem;
                color: #667eea;
                margin-bottom: 10px;
            }
            
            .capability-card h5 {
                color: #2c3e50;
                margin-bottom: 8px;
            }
            
            .capability-card p {
                color: #7f8c8d;
                font-size: 0.9rem;
            }
            
            .suggestions-buttons {
                display: flex;
                flex-direction: column;
                gap: 10px;
            }
            
            .suggestion-btn {
                background: white;
                border: 2px solid #e0e0e0;
                padding: 12px 20px;
                border-radius: 8px;
                text-align: left;
                cursor: pointer;
                transition: all 0.2s;
                color: #2c3e50;
                font-size: 0.95rem;
            }
            
            .suggestion-btn:hover {
                border-color: #667eea;
                background: #f0f2ff;
                transform: translateX(5px);
            }
            
            .suggestion-btn i {
                color: #667eea;
                margin-right: 8px;
            }
            
            .quick-tips {
                background: #fff3cd;
                border-left: 4px solid #ffc107;
                padding: 15px;
                border-radius: 4px;
            }
            
            .quick-tips p {
                margin-bottom: 10px;
                color: #856404;
            }
            
            .quick-tips ul {
                margin: 0;
                padding-left: 20px;
                color: #856404;
            }
            
            .quick-tips li {
                margin-bottom: 5px;
            }
            
            /* Chat Input */
            .chat-input-container {
                padding: 15px 0;
            }
            
            .chat-input-wrapper {
                display: flex;
                gap: 10px;
                align-items: flex-end;
            }
            
            .chat-input {
                flex: 1;
                border: 2px solid #e0e0e0;
                border-radius: 24px;
                padding: 12px 20px;
                resize: none;
                max-height: 150px;
                font-size: 1rem;
                transition: border-color 0.2s;
            }
            
            .chat-input:focus {
                outline: none;
                border-color: #667eea;
            }
            
            .send-btn {
                width: 48px;
                height: 48px;
                border-radius: 50%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
                color: white;
                font-size: 1.2rem;
                cursor: pointer;
                transition: transform 0.2s;
                flex-shrink: 0;
            }
            
            .send-btn:hover {
                transform: scale(1.1);
            }
            
            .send-btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            
            #typing-indicator {
                padding: 10px 20px;
                color: #667eea;
                font-style: italic;
            }
            
            /* Scrollbar */
            .chat-messages::-webkit-scrollbar {
                width: 8px;
            }
            
            .chat-messages::-webkit-scrollbar-track {
                background: #f1f1f1;
                border-radius: 4px;
            }
            
            .chat-messages::-webkit-scrollbar-thumb {
                background: #888;
                border-radius: 4px;
            }
            
            .chat-messages::-webkit-scrollbar-thumb:hover {
                background: #555;
            }
        </style>
        """

        content = f"""
        {styles}
        <div class='card'>
            <div class='card-header' style='display: flex; justify-content: space-between; align-items: center;'>
                <span><i class='fas fa-robot'></i> Asistente Virtual Inteligente</span>
                <div style='display: flex; gap: 10px;'>
                    <button class='btn btn-sm btn-info' id='refresh-insights-btn' title='Actualizar insights'>
                        <i class='fas fa-sync-alt'></i> Actualizar
                    </button>
                    <button class='btn btn-sm btn-secondary' id='clear-history-btn' title='Limpiar historial'>
                        <i class='fas fa-trash'></i> Limpiar
                    </button>
                </div>
            </div>
            <div class='card-body chatbot-container'>
                <div id='chat-messages' class='chat-messages'>
                    {history_html}
                </div>
                <div id='typing-indicator' style='display:none;'>
                    <span class='spinner-border spinner-border-sm'></span>
                    <span>Pensando...</span>
                </div>
                <div class='chat-input-container'>
                    <div class='chat-input-wrapper'>
                        <textarea id='message-input' class='chat-input' rows='1' placeholder='Escribe tu pregunta en lenguaje natural...'></textarea>
                        <button id='send-btn' class='send-btn'>
                            <i class='fas fa-paper-plane'></i>
                        </button>
                    </div>
                </div>
            </div>
        </div>
        """

        html = Layout.render(
            title="Asistente Virtual IA",
            user=user,
            active_page="chatbot",
            content=content,
        )

        return html

    @staticmethod
    def format_markdown(text):
        """
        Formatea texto Markdown a HTML, preservando bloques de código Mermaid.
        """
        # 1. Patrón para bloques de código Mermaid
        # Busca ```mermaid...``` y los reemplaza temporalmente con un marcador
        mermaid_blocks = re.findall(r"```mermaid\s*\n(.*?)\n```", text, re.DOTALL)

        # Marcador para reintroducir los bloques de código después del renderizado Markdown
        MERMAID_PLACEHOLDER = "@@MERMAID_BLOCK_PLACEHOLDER@@"

        # Reemplazar los bloques de mermaid en el texto original con el marcador
        text_with_placeholders = re.sub(
            r"```mermaid\s*\n(.*?)\n```", MERMAID_PLACEHOLDER, text, flags=re.DOTALL
        )

        # 2. Convertir el texto con la librería Python-Markdown
        # Usamos 'extra' y 'fenced_code' para un soporte de Markdown más rico, incluyendo tablas.
        html_output = markdown.markdown(
            text_with_placeholders, extensions=["extra", "codehilite", "fenced_code"]
        )

        # 3. Reinsertar los bloques de código Mermaid con la estructura <pre class="mermaid">...</pre>
        # Esto es lo que el frontend necesita para renderizar el diagrama.
        for block in mermaid_blocks:
            mermaid_html = f'<pre class="mermaid">\n{block.strip()}\n</pre>'
            # Solo reemplazamos UNA vez, para manejar múltiples bloques si existen
            html_output = html_output.replace(MERMAID_PLACEHOLDER, mermaid_html, 1)

        # Retornar el HTML final
        return html_output
