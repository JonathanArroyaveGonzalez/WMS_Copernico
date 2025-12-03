# app/models/chatbot_message.py

from config.database import Database
from datetime import datetime


class ChatbotMessage:
    """Modelo para los mensajes del chatbot"""

    @staticmethod
    def create_table():
        """Crea la tabla chatbot_messages si no existe"""
        query = """
            CREATE TABLE IF NOT EXISTS chatbot_messages (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                message TEXT NOT NULL,
                response TEXT NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """
        Database.execute_query(query, fetch=False)

    @staticmethod
    def save(user_id, message, response):
        """Guarda un mensaje y su respuesta en la base de datos"""
        query = """
            INSERT INTO chatbot_messages (user_id, message, response, created_at)
            VALUES (%s, %s, %s, %s)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        Database.execute_query(
            query, (user_id, message, response, timestamp), fetch=False
        )

    @staticmethod
    def get_history(user_id, limit=20):
        """Obtiene el historial de conversación de un usuario"""
        query = """
            SELECT id, user_id, message, response, 
                   DATE_FORMAT(created_at, '%%Y-%%m-%%d %%H:%%i:%%s') as created_at
            FROM chatbot_messages
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT %s
        """
        results = Database.execute_query(query, (user_id, limit))

        # Invertir el orden para mostrar más antiguos primero
        if results:
            return list(reversed(results))
        return []

    @staticmethod
    def delete_history(user_id):
        """Elimina todo el historial de un usuario"""
        query = "DELETE FROM chatbot_messages WHERE user_id = %s"
        Database.execute_query(query, (user_id,), fetch=False)

    @staticmethod
    def get_current_timestamp():
        """Retorna el timestamp actual formateado"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_recent_context(user_id, limit=5):
        """Obtiene los mensajes recientes para contexto"""
        query = """
            SELECT message, response
            FROM chatbot_messages
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT %s
        """
        results = Database.execute_query(query, (user_id, limit))

        if results:
            return list(reversed(results))
        return []
