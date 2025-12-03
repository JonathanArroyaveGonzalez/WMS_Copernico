import google.generativeai as genai
from config.database import Database
from app.models.product import Product
from app.models.category import Category
from app.models.sale import Sale
from app.models.purchase import Purchase
from app.models.client import Client
from app.models.supplier import Supplier
from app.models.warehouse import Warehouse
from app.models.inventory_movement import InventoryMovement
from dotenv import load_dotenv
import json
import os
from datetime import datetime, timedelta

load_dotenv()

class AIService:
    """Servicio de IA mejorado con capacidades de exploración en lenguaje natural"""
    
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key or api_key == 'tu-api-key-aqui':
            raise ValueError(
                "GEMINI_API_KEY no está configurada. "
                "Por favor, configura tu API key en el archivo .env"
            )
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Configuración de generación para respuestas más conversacionales
        self.generation_config = {
            'temperature': 0.7,
            'top_p': 0.95,
            'top_k': 40,
            'max_output_tokens': 2048,
        }
    
    def get_comprehensive_context(self):
        """Obtiene contexto completo y detallado del sistema"""
        try:
            context = {
                'products': Product.get_all(),
                'categories': Category.get_all(),
                'sales': Sale.get_all(),
                'purchases': Purchase.get_all(),
                'clients': Client.get_all(),
                'suppliers': Supplier.get_all(),
                'warehouses': Warehouse.get_all(),
                'movements': InventoryMovement.get_all()
            }
            return context
        except Exception as e:
            print(f"Error obteniendo contexto: {e}")
            return {}
    
    def analyze_data_for_context(self, context):
        """Analiza los datos y genera insights automáticos"""
        insights = []
        
        # Análisis de productos
        products = context.get('products', [])
        if products:
            total_stock = sum(p.get('stock_actual', 0) for p in products)
            low_stock = [p for p in products if p.get('stock_actual', 0) < 10]
            out_of_stock = [p for p in products if p.get('stock_actual', 0) == 0]
            high_value_products = [p for p in products if p.get('precio_venta', 0) > 1000]
            
            insights.append(f"Hay {len(products)} productos en total con {total_stock} unidades en inventario")
            if low_stock:
                insights.append(f"{len(low_stock)} productos tienen stock bajo (menos de 10 unidades)")
            if out_of_stock:
                insights.append(f"⚠️ {len(out_of_stock)} productos están agotados")
            if high_value_products:
                insights.append(f"{len(high_value_products)} productos son de alto valor (más de $1000)")
        
        # Análisis de ventas
        sales = context.get('sales', [])
        if sales:
            total_sales = sum(s.get('total', 0) for s in sales)
            avg_sale = total_sales / len(sales) if sales else 0
            insights.append(f"Se han registrado {len(sales)} ventas por un total de ${total_sales:,.2f} (promedio: ${avg_sale:,.2f})")
        
        # Análisis de compras
        purchases = context.get('purchases', [])
        if purchases:
            total_purchases = sum(p.get('total', 0) for p in purchases)
            insights.append(f"Se han registrado {len(purchases)} compras por un total de ${total_purchases:,.2f}")
        
        # Análisis de clientes y proveedores
        clients = context.get('clients', [])
        suppliers = context.get('suppliers', [])
        if clients:
            insights.append(f"Base de datos: {len(clients)} clientes registrados")
        if suppliers:
            insights.append(f"{len(suppliers)} proveedores activos")
        
        return "\n• ".join(insights)
    
    def format_data_for_llm(self, context):
        """Formatea los datos de manera estructurada para el LLM"""
        formatted = "=== DATOS DEL SISTEMA DE INVENTARIO ===\n\n"
        
        # Insights generales
        insights = self.analyze_data_for_context(context)
        if insights:
            formatted += f"📊 INSIGHTS GENERALES:\n• {insights}\n\n"
        
        # Productos destacados
        products = context.get('products', [])
        if products:
            formatted += "📦 PRODUCTOS (muestra de los primeros 20):\n"
            for i, p in enumerate(products[:20], 1):
                formatted += f"{i}. {p.get('nombre', 'N/A')}\n"
                formatted += f"   - Stock: {p.get('stock_actual', 0)} unidades"
                if p.get('stock_actual', 0) < 10:
                    formatted += " ⚠️ STOCK BAJO"
                formatted += f"\n   - Precio Venta: ${p.get('precio_venta', 0):,.2f}\n"
                formatted += f"   - Categoría: {p.get('categoria', 'Sin categoría')}\n"
                if p.get('descripcion'):
                    formatted += f"   - Descripción: {p.get('descripcion')[:100]}\n"
                formatted += "\n"
            
            if len(products) > 20:
                formatted += f"... y {len(products) - 20} productos más.\n\n"
        
        # Categorías
        categories = context.get('categories', [])
        if categories:
            formatted += f"🏷️ CATEGORÍAS ({len(categories)}):\n"
            for cat in categories[:10]:
                formatted += f"- {cat.get('nombre', 'N/A')}"
                if cat.get('descripcion'):
                    formatted += f": {cat.get('descripcion')}"
                formatted += "\n"
            formatted += "\n"
        
        # Almacenes
        warehouses = context.get('warehouses', [])
        if warehouses:
            formatted += f"🏢 ALMACENES ({len(warehouses)}):\n"
            for w in warehouses:
                formatted += f"- {w.get('nombre', 'N/A')}"
                if w.get('ubicacion'):
                    formatted += f" (Ubicación: {w.get('ubicacion')})"
                formatted += "\n"
            formatted += "\n"
        
        # Ventas recientes
        sales = context.get('sales', [])
        if sales:
            recent_sales = sales[-5:]
            formatted += "💰 VENTAS RECIENTES:\n"
            for s in recent_sales:
                formatted += f"- Venta #{s.get('id', 'N/A')}: ${s.get('total', 0):,.2f}"
                if s.get('fecha'):
                    formatted += f" (Fecha: {s.get('fecha')})"
                formatted += "\n"
            formatted += "\n"
        
        return formatted
    
    def create_system_prompt(self):
        """Crea el prompt del sistema con instrucciones detalladas"""
        return """Eres un asistente virtual inteligente especializado en gestión de inventarios. Tu nombre es InventoryBot.

TU PERSONALIDAD:
- Eres profesional pero amigable y conversacional
- Hablas en español de manera natural
- Eres proactivo: sugieres análisis, alertas y recomendaciones
- Cuando detectas problemas, los mencionas constructivamente
- Preguntas para clarificar cuando algo es ambiguo

TUS CAPACIDADES:
1. Consultar productos, stock, precios y categorías
2. Analizar ventas y compras
3. Identificar productos con stock bajo o agotados
4. Comparar datos y generar insights
5. Recomendar acciones basadas en los datos
6. Responder preguntas sobre clientes, proveedores y almacenes
7. Explicar tendencias y patrones

CÓMO RESPONDER:
- Usa los datos proporcionados para responder con precisión
- Si los datos no contienen la información exacta, infiere razonablemente o pide clarificación
- Formatea las respuestas de manera clara con emojis relevantes
- Incluye números específicos cuando sea relevante
- Si detectas algo importante (stock bajo, productos agotados), menciónalo
- Ofrece seguimiento: "¿Quieres que analice algo más?" o "¿Te gustaría ver los detalles de...?"

EJEMPLOS DE PREGUNTAS QUE PUEDES RESPONDER:
- "¿Cuáles son los productos más caros?"
- "¿Qué productos se están agotando?"
- "¿Cuánto hemos vendido este mes?"
- "Compara las ventas con las compras"
- "¿Qué productos nunca se han vendido?"
- "Dame recomendaciones para optimizar el inventario"
- "¿En qué categoría tenemos más productos?"

IMPORTANTE:
- Nunca inventes datos que no existen
- Si algo no está claro en los datos, di "No tengo esa información específica, pero..."
- Sé conversacional: el usuario debe sentir que habla con un experto amigable"""
    
    def process_query(self, user_message, user_id, conversation_history=None):
        """Procesa consultas usando el poder completo del LLM"""
        try:
            # Obtener contexto completo
            context = self.get_comprehensive_context()
            formatted_context = self.format_data_for_llm(context)
            
            # Construir el historial de conversación
            messages = []
            
            if conversation_history:
                for msg in conversation_history[-5:]:  # Últimos 5 mensajes
                    role = "user" if msg.get('is_user') else "model"
                    messages.append({
                        'role': role,
                        'parts': [msg.get('content', '')]
                    })
            
            # Construir el prompt completo
            full_prompt = f"""{self.create_system_prompt()}

{formatted_context}

Usuario: {user_message}

Responde de manera natural y conversacional. Si puedes generar insights o recomendaciones basadas en los datos, hazlo."""
            
            # Generar respuesta con Gemini
            chat = self.model.start_chat(history=messages)
            response = chat.send_message(
                full_prompt,
                generation_config=self.generation_config
            )
            
            return response.text
            
        except Exception as e:
            return f"Disculpa, tuve un problema al procesar tu consulta. Error técnico: {str(e)}\n\n¿Podrías intentar reformular tu pregunta?"
    
    def get_quick_insights(self):
        """Genera insights rápidos del estado actual"""
        try:
            context = self.get_comprehensive_context()
            
            prompt = f"""{self.create_system_prompt()}

{self.format_data_for_llm(context)}

Genera un resumen ejecutivo breve (3-5 puntos) con los insights más importantes del inventario actual. 
Incluye alertas si hay productos agotados o stock bajo. Sé conciso y directo."""
            
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            return response.text
            
        except Exception as e:
            return f"Error generando insights: {str(e)}"
    
    def suggest_questions(self):
        """Sugiere preguntas inteligentes basadas en los datos actuales"""
        try:
            context = self.get_comprehensive_context()
            
            prompt = f"""{self.create_system_prompt()}

{self.format_data_for_llm(context)}

Basándote en los datos actuales del inventario, sugiere 5 preguntas inteligentes que el usuario podría hacerte para obtener insights valiosos. 
Las preguntas deben ser específicas y relevantes a la situación actual del negocio.
Formato: Solo lista las preguntas, una por línea, con emoji al inicio."""
            
            response = self.model.generate_content(
                prompt,
                generation_config=self.generation_config
            )
            
            return response.text
            
        except Exception as e:
            return "¿Qué te gustaría saber sobre tu inventario?"
    
    def get_help_message(self):
        """Mensaje de ayuda conversacional"""
        return """¡Hola! 👋 Soy tu asistente de inventario inteligente.

Puedes hablarme de manera natural. Por ejemplo:

💬 Preguntas que puedo responder:
- "¿Cuáles productos tienen poco stock?"
- "Muéstrame los productos más caros"
- "¿Cuánto hemos vendido esta semana?"
- "Dame un resumen del inventario"
- "¿Qué productos debería reordenar?"
- "Compara ventas vs compras"

🎯 También puedo:
- Analizar tendencias
- Generar recomendaciones
- Alertarte sobre problemas
- Responder preguntas específicas sobre cualquier producto

Solo pregúntame lo que necesites saber. ¿En qué puedo ayudarte?"""