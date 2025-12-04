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
import re
import os
from datetime import datetime, timedelta

load_dotenv()


class AIService:
    """Servicio de IA mejorado con acceso a base de datos y consultas SQL"""

    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "tu-api-key-aqui":
            raise ValueError(
                "GEMINI_API_KEY no está configurada. "
                "Por favor, configura tu API key en el archivo .env"
            )
        # Modelo "gemini-2.5-flash"
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-pro")

        # Configuración de generación
        self.generation_config = {
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 40,
            "max_output_tokens": 2048,
        }

    def get_database_schema(self):
        """Obtiene el esquema completo de la base de datos"""
        try:
            # Obtener todas las tablas
            tables_query = "SHOW TABLES"
            tables = Database.execute_query(tables_query)

            schema_info = "=== ESTRUCTURA DE LA BASE DE DATOS ===\n\n"

            for table in tables:
                table_name = list(table.values())[0]

                # Obtener estructura de cada tabla
                columns_query = f"DESCRIBE {table_name}"
                columns = Database.execute_query(columns_query)

                # Contar registros
                count_query = f"SELECT COUNT(*) as total FROM {table_name}"
                count = Database.execute_query(count_query)
                total_records = count[0]["total"] if count else 0

                schema_info += f"📋 TABLA: {table_name} ({total_records} registros)\n"
                schema_info += "   Columnas:\n"

                for col in columns:
                    field = col.get("Field", "")
                    col_type = col.get("Type", "")
                    null = "NULL" if col.get("Null") == "YES" else "NOT NULL"
                    key = col.get("Key", "")
                    key_info = ""
                    if key == "PRI":
                        key_info = " [PRIMARY KEY]"
                    elif key == "MUL":
                        key_info = " [FOREIGN KEY]"
                    elif key == "UNI":
                        key_info = " [UNIQUE]"

                    schema_info += f"   - {field}: {col_type} {null}{key_info}\n"

                schema_info += "\n"

            return schema_info

        except Exception as e:
            return f"Error obteniendo esquema: {str(e)}"

    def execute_safe_query(self, sql_query):
        """Ejecuta una consulta SQL de forma segura (solo SELECT)"""
        try:
            # Limpiar y validar la consulta
            sql_clean = sql_query.strip().upper()

            # Solo permitir consultas SELECT
            if not sql_clean.startswith("SELECT"):
                return {"error": "Solo se permiten consultas SELECT por seguridad"}

            # Prohibir palabras peligrosas
            dangerous_words = [
                "DROP",
                "DELETE",
                "UPDATE",
                "INSERT",
                "ALTER",
                "TRUNCATE",
                "CREATE",
                "GRANT",
                "REVOKE",
            ]
            for word in dangerous_words:
                if word in sql_clean:
                    return {"error": f"Consulta no permitida: contiene {word}"}

            # Ejecutar la consulta
            results = Database.execute_query(sql_query)

            # Convertir a formato serializable
            if results:
                # Convertir fechas y decimales a strings
                clean_results = []
                for row in results:
                    clean_row = {}
                    for key, value in row.items():
                        if hasattr(value, "isoformat"):
                            clean_row[key] = value.isoformat()
                        elif hasattr(value, "__float__"):
                            clean_row[key] = float(value)
                        else:
                            clean_row[key] = value
                    clean_results.append(clean_row)
                return {"success": True, "data": clean_results, "count": len(results)}
            return {"success": True, "data": [], "count": 0}

        except Exception as e:
            return {"error": str(e)}

    def get_comprehensive_context(self):
        """Obtiene contexto completo y detallado del sistema"""
        try:
            context = {
                "products": Product.get_all(),
                "categories": Category.get_all(),
                "sales": Sale.get_all(),
                "purchases": Purchase.get_all(),
                "clients": Client.get_all(),
                "suppliers": Supplier.get_all(),
                "warehouses": Warehouse.get_all(),
                "movements": InventoryMovement.get_all(),
            }
            return context
        except Exception as e:
            print(f"Error obteniendo contexto: {e}")
            return {}

    def get_advanced_stats(self):
        """Obtiene estadísticas avanzadas mediante consultas SQL"""
        stats = {}

        try:
            # Top 5 productos más vendidos
            top_sold_query = """
                SELECT p.nombre, SUM(dv.cantidad) as total_vendido, SUM(dv.subtotal) as ingresos
                FROM detalle_ventas dv
                JOIN productos p ON dv.producto_id = p.id
                GROUP BY p.id, p.nombre
                ORDER BY total_vendido DESC
                LIMIT 5
            """
            stats["top_productos_vendidos"] = Database.execute_query(top_sold_query)

            # Top 5 clientes por compras
            top_clients_query = """
                SELECT c.nombre, COUNT(v.id) as num_compras, SUM(v.total) as total_gastado
                FROM ventas v
                JOIN clientes c ON v.cliente_id = c.id
                GROUP BY c.id, c.nombre
                ORDER BY total_gastado DESC
                LIMIT 5
            """
            stats["top_clientes"] = Database.execute_query(top_clients_query)

            # Productos por categoría
            productos_categoria_query = """
                SELECT c.nombre as categoria, COUNT(p.id) as num_productos, 
                       SUM(p.stock_actual) as stock_total
                FROM categorias c
                LEFT JOIN productos p ON c.id = p.categoria_id
                GROUP BY c.id, c.nombre
                ORDER BY num_productos DESC
            """
            stats["productos_por_categoria"] = Database.execute_query(
                productos_categoria_query
            )

            # Productos con stock crítico (menos de 5)
            stock_critico_query = """
                SELECT nombre, stock_actual, stock_minimo, precio_venta
                FROM productos
                WHERE stock_actual <= 5
                ORDER BY stock_actual ASC
            """
            stats["stock_critico"] = Database.execute_query(stock_critico_query)

            # Valor total del inventario
            valor_inventario_query = """
                SELECT SUM(stock_actual * precio_compra) as valor_costo,
                       SUM(stock_actual * precio_venta) as valor_venta
                FROM productos
            """
            stats["valor_inventario"] = Database.execute_query(valor_inventario_query)

            # NUEVO: Productos más comprados por los TOP 5 clientes
            productos_por_top_clientes_query = """
                SELECT 
                    c.nombre AS cliente,
                    p.nombre AS producto,
                    cat.nombre AS categoria,
                    SUM(dv.cantidad) AS cantidad_total,
                    COUNT(DISTINCT v.id) AS num_compras
                FROM clientes c
                JOIN ventas v ON c.id = v.cliente_id
                JOIN detalle_ventas dv ON v.id = dv.venta_id
                JOIN productos p ON dv.producto_id = p.id
                JOIN categorias cat ON p.categoria_id = cat.id
                WHERE c.id IN (
                    SELECT c2.id FROM clientes c2
                    JOIN ventas v2 ON c2.id = v2.cliente_id
                    GROUP BY c2.id
                    ORDER BY SUM(v2.total) DESC
                    LIMIT 5
                )
                GROUP BY c.id, c.nombre, p.id, p.nombre, cat.id, cat.nombre
                ORDER BY c.nombre, cantidad_total DESC
            """
            stats["productos_por_top_clientes"] = Database.execute_query(
                productos_por_top_clientes_query
            )

            # NUEVO: Categorías favoritas por cliente TOP
            categorias_por_top_clientes_query = """
                SELECT 
                    c.nombre AS cliente,
                    cat.nombre AS categoria,
                    SUM(dv.cantidad) AS cantidad_total,
                    SUM(dv.subtotal) AS total_gastado
                FROM clientes c
                JOIN ventas v ON c.id = v.cliente_id
                JOIN detalle_ventas dv ON v.id = dv.venta_id
                JOIN productos p ON dv.producto_id = p.id
                JOIN categorias cat ON p.categoria_id = cat.id
                WHERE c.id IN (
                    SELECT c2.id FROM clientes c2
                    JOIN ventas v2 ON c2.id = v2.cliente_id
                    GROUP BY c2.id
                    ORDER BY SUM(v2.total) DESC
                    LIMIT 5
                )
                GROUP BY c.id, c.nombre, cat.id, cat.nombre
                ORDER BY c.nombre, cantidad_total DESC
            """
            stats["categorias_por_top_clientes"] = Database.execute_query(
                categorias_por_top_clientes_query
            )

        except Exception as e:
            stats["error"] = str(e)

        return stats

    def analyze_data_for_context(self, context):
        """Analiza los datos y genera insights automáticos"""
        insights = []

        products = context.get("products", [])
        if products:
            total_stock = sum(p.get("stock_actual", 0) for p in products)
            low_stock = [p for p in products if p.get("stock_actual", 0) < 10]
            out_of_stock = [p for p in products if p.get("stock_actual", 0) == 0]
            high_value_products = [
                p for p in products if p.get("precio_venta", 0) > 1000
            ]

            insights.append(
                f"Hay {len(products)} productos en total con {total_stock} unidades en inventario"
            )
            if low_stock:
                insights.append(
                    f"{len(low_stock)} productos tienen stock bajo (menos de 10 unidades)"
                )
            if out_of_stock:
                insights.append(f"⚠️ {len(out_of_stock)} productos están agotados")
            if high_value_products:
                insights.append(
                    f"{len(high_value_products)} productos son de alto valor (más de $1000)"
                )

        sales = context.get("sales", [])
        if sales:
            total_sales = sum(s.get("total", 0) for s in sales)
            avg_sale = total_sales / len(sales) if sales else 0
            insights.append(
                f"Se han registrado {len(sales)} ventas por un total de ${total_sales:,.2f} (promedio: ${avg_sale:,.2f})"
            )

        purchases = context.get("purchases", [])
        if purchases:
            total_purchases = sum(p.get("total", 0) for p in purchases)
            insights.append(
                f"Se han registrado {len(purchases)} compras por un total de ${total_purchases:,.2f}"
            )

        clients = context.get("clients", [])
        suppliers = context.get("suppliers", [])
        if clients:
            insights.append(f"Base de datos: {len(clients)} clientes registrados")
        if suppliers:
            insights.append(f"{len(suppliers)} proveedores activos")

        return "\n• ".join(insights)

    def format_data_for_llm(self, context, include_schema=True, include_stats=True):
        """Formatea los datos de manera estructurada para el LLM"""
        formatted = ""

        # Incluir esquema de BD (resumido para evitar tokens excesivos)
        if include_schema:
            formatted += "=== TABLAS PRINCIPALES ===\n"
            formatted += "- productos, categorias, clientes, proveedores\n"
            formatted += "- ventas, detalle_ventas, compras, detalle_compras\n"
            formatted += "- almacenes, movimientos_inventario, usuarios, roles\n\n"

        # Incluir estadísticas avanzadas
        if include_stats:
            stats = self.get_advanced_stats()
            formatted += "=== ESTADÍSTICAS DEL NEGOCIO ===\n\n"

            if stats.get("top_productos_vendidos"):
                formatted += "🏆 TOP 5 PRODUCTOS MÁS VENDIDOS:\n"
                for i, p in enumerate(stats["top_productos_vendidos"], 1):
                    formatted += f"   {i}. {p.get('nombre')}: {p.get('total_vendido')} uds (${float(p.get('ingresos', 0)):,.2f})\n"
                formatted += "\n"

            if stats.get("top_clientes"):
                formatted += "👥 TOP 5 MEJORES CLIENTES:\n"
                for i, c in enumerate(stats["top_clientes"], 1):
                    formatted += f"   {i}. {c.get('nombre')}: {c.get('num_compras')} compras (${float(c.get('total_gastado', 0)):,.2f})\n"
                formatted += "\n"

            # NUEVO: Mostrar productos por cada cliente TOP
            if stats.get("productos_por_top_clientes"):
                formatted += "🛒 PRODUCTOS COMPRADOS POR TOP CLIENTES:\n"
                current_client = None
                for item in stats["productos_por_top_clientes"]:
                    if item.get("cliente") != current_client:
                        current_client = item.get("cliente")
                        formatted += f"\n   📌 {current_client}:\n"
                    formatted += f"      - {item.get('producto')} ({item.get('categoria')}): {item.get('cantidad_total')} uds en {item.get('num_compras')} compras\n"
                formatted += "\n"

            # NUEVO: Mostrar categorías favoritas por cliente TOP
            if stats.get("categorias_por_top_clientes"):
                formatted += "📊 CATEGORÍAS FAVORITAS POR CLIENTE TOP:\n"
                current_client = None
                for item in stats["categorias_por_top_clientes"]:
                    if item.get("cliente") != current_client:
                        current_client = item.get("cliente")
                        formatted += f"\n   📌 {current_client}:\n"
                    formatted += f"      - {item.get('categoria')}: {item.get('cantidad_total')} productos (${float(item.get('total_gastado', 0)):,.2f})\n"
                formatted += "\n"

            if stats.get("valor_inventario") and stats["valor_inventario"]:
                inv = stats["valor_inventario"][0]
                formatted += f"💰 VALOR DEL INVENTARIO:\n"
                formatted += (
                    f"   - Costo: ${float(inv.get('valor_costo', 0) or 0):,.2f}\n"
                )
                formatted += (
                    f"   - Venta: ${float(inv.get('valor_venta', 0) or 0):,.2f}\n\n"
                )

            if stats.get("stock_critico"):
                formatted += "🚨 STOCK CRÍTICO (≤5 uds):\n"
                for p in stats["stock_critico"][:5]:
                    formatted += (
                        f"   - {p.get('nombre')}: {p.get('stock_actual')} uds\n"
                    )
                formatted += "\n"

            if stats.get("productos_por_categoria"):
                formatted += "📦 PRODUCTOS POR CATEGORÍA:\n"
                for cat in stats["productos_por_categoria"]:
                    formatted += f"   - {cat.get('categoria')}: {cat.get('num_productos')} productos\n"
                formatted += "\n"

        # Resumen general
        insights = self.analyze_data_for_context(context)
        if insights:
            formatted += f"📈 RESUMEN:\n• {insights}\n"

        return formatted

    def create_system_prompt(self):
        """Crea el prompt del sistema con instrucciones detalladas"""
        return """Eres InventoryBot, un asistente virtual experto en gestión de inventarios con acceso DIRECTO a la base de datos.

🔧 TUS CAPACIDADES ESPECIALES:
1. Tienes acceso al ESQUEMA COMPLETO de la base de datos (tablas, columnas, tipos de datos)
2. Puedes analizar estadísticas avanzadas en tiempo real
3. PUEDES EJECUTAR consultas SQL SELECT directamente y mostrar los resultados
4. Tienes acceso a métricas de negocio (top clientes, productos más vendidos, etc.)
5. **Generas diagramas de flujo o estructura en formato Mermaid** (usando ```mermaid...```) para visualizar procesos o relaciones de datos complejas.

📊 CÓMO USAR TU CONOCIMIENTO:
- Cuando te pregunten algo específico, usa los datos que tienes disponibles
- Si el usuario pide ejecutar una consulta o necesita datos específicos, USA LA FUNCIÓN execute_sql
- Proporciona números exactos cuando los tengas
- Ofrece insights basados en los datos reales
- **Utiliza diagramas Mermaid** para visualizar jerarquías (ej: categorías), flujos (ej: movimiento de inventario) o estructuras de datos complejas.

💬 TU PERSONALIDAD:
- Profesional pero amigable
- Hablas en español de manera natural
- Eres proactivo: sugieres análisis y recomendaciones
- Cuando detectas problemas (stock bajo, tendencias negativas), los mencionas

📋 FORMATO DE RESPUESTAS:
- Usa emojis para hacer la información más visual
- Incluye números específicos siempre que sea posible
- Si hay alertas importantes (stock crítico, productos agotados), destácalas
- Mantén las respuestas concisas y directas
- **Para diagramas, usa el formato de bloque de código: \`\`\`mermaid\n[CODIGO MERMAID AQUÍ]\n\`\`\`**

⚠️ REGLAS IMPORTANTES:
- Nunca inventes datos - usa solo la información proporcionada
- Si no tienes un dato específico, dilo honestamente
- NO sugieras consultas SQL - EJECÚTALAS directamente con los datos disponibles
- Prioriza la información más relevante para la pregunta del usuario"""

    def process_query(self, user_message, user_id, conversation_history=None):
        """Procesa consultas con acceso completo a la base de datos"""
        try:
            # Obtener contexto completo
            context = self.get_comprehensive_context()
            formatted_context = self.format_data_for_llm(
                context, include_schema=True, include_stats=True
            )

            # Construir el historial de conversación
            messages = []

            if conversation_history:
                for msg in conversation_history[-5:]:
                    role = "user" if msg.get("is_user") else "model"
                    messages.append({"role": role, "parts": [msg.get("content", "")]})

            # Construir el prompt completo
            full_prompt = f"""{self.create_system_prompt()}

{formatted_context}

PREGUNTA DEL USUARIO: {user_message}

Responde de manera completa usando todos los datos disponibles. Si la pregunta requiere análisis, hazlo con los datos proporcionados."""

            # Generar respuesta con Gemini
            chat = self.model.start_chat(history=messages)
            response = chat.send_message(
                full_prompt, generation_config=self.generation_config
            )

            # Verificar si la respuesta es válida
            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]

                # Verificar finish_reason (1=STOP es OK, 2=SAFETY, 3=RECITATION, etc.)
                if hasattr(candidate, "finish_reason"):
                    finish_reason = candidate.finish_reason
                    # finish_reason 2 = SAFETY block
                    if finish_reason == 2:
                        # Reintentar con contexto reducido
                        return self._retry_with_reduced_context(
                            user_message, context, messages
                        )

                # Intentar obtener el texto
                if candidate.content and candidate.content.parts:
                    return candidate.content.parts[0].text

            # Si llegamos aquí, intentar response.text como fallback
            return response.text

        except Exception as e:
            error_msg = str(e)
            # Si es un error de seguridad, reintentar con menos contexto
            if "finish_reason" in error_msg or "SAFETY" in error_msg.upper():
                try:
                    return self._retry_with_reduced_context(
                        user_message, context, messages
                    )
                except Exception as retry_error:
                    pass

            return f"Disculpa, tuve un problema al procesar tu consulta. Error técnico: {error_msg}\n\n¿Podrías intentar reformular tu pregunta?"

    def _retry_with_reduced_context(self, user_message, context, messages):
        """Reintenta la consulta con contexto reducido"""
        try:
            # Usar solo estadísticas básicas, sin esquema completo
            reduced_context = self.format_data_for_llm(
                context, include_schema=False, include_stats=True
            )

            # Detectar si el usuario pide un diagrama
            wants_diagram = any(
                word in user_message.lower()
                for word in [
                    "diagrama",
                    "gráfico",
                    "grafico",
                    "flujo",
                    "mermaid",
                    "visualiza",
                    "visualizar",
                    "esquema",
                    "relación",
                    "relacion",
                ]
            )

            diagram_instruction = ""
            if wants_diagram:
                diagram_instruction = """
IMPORTANTE: El usuario ha pedido un diagrama. Genera un diagrama Mermaid válido usando este formato:

```mermaid
graph TD
    A[Nodo A] --> B[Nodo B]
    B --> C[Nodo C]
```

Usa los datos reales del sistema para construir el diagrama.
"""

            simple_prompt = f"""Eres InventoryBot, un asistente de inventario amigable que habla español.
Puedes generar diagramas usando formato Mermaid cuando te lo pidan.

{reduced_context}

{diagram_instruction}

PREGUNTA: {user_message}

Responde de forma útil y concisa basándote en los datos disponibles."""

            response = self.model.generate_content(
                simple_prompt,
                generation_config={
                    "temperature": 0.5,
                    "max_output_tokens": 2048,
                },
            )

            # Verificar respuesta válida
            if response.candidates and len(response.candidates) > 0:
                candidate = response.candidates[0]
                if candidate.content and candidate.content.parts:
                    return candidate.content.parts[0].text

            return response.text

        except Exception as e:
            # Último intento: respuesta genérica útil
            return self._generate_fallback_response(user_message, context)

    def _generate_fallback_response(self, user_message, context):
        """Genera una respuesta de respaldo cuando Gemini falla"""
        stats = self.get_advanced_stats()

        # Detectar si el usuario pide un diagrama
        wants_diagram = any(
            word in user_message.lower()
            for word in [
                "diagrama",
                "gráfico",
                "grafico",
                "flujo",
                "mermaid",
                "visualiza",
                "visualizar",
                "esquema",
                "relación",
                "relacion",
            ]
        )

        response = "📊 **Información disponible del sistema:**\n\n"

        if stats.get("top_productos_vendidos"):
            response += "🏆 **TOP 5 Productos más vendidos:**\n"
            for i, p in enumerate(stats["top_productos_vendidos"], 1):
                response += (
                    f"   {i}. {p.get('nombre')}: {p.get('total_vendido')} unidades\n"
                )
            response += "\n"

        if stats.get("top_clientes"):
            response += "👥 **TOP 5 Mejores clientes:**\n"
            for i, c in enumerate(stats["top_clientes"], 1):
                response += f"   {i}. {c.get('nombre')}: ${float(c.get('total_gastado', 0)):,.2f}\n"
            response += "\n"

        if stats.get("valor_inventario") and stats["valor_inventario"]:
            inv = stats["valor_inventario"][0]
            response += f"💰 **Valor del inventario:** ${float(inv.get('valor_venta', 0)):,.2f}\n\n"

        # Si pidió un diagrama, generar uno básico con los datos disponibles
        if wants_diagram and stats.get("top_productos_vendidos"):
            response += "📈 **Diagrama de productos más vendidos:**\n\n"
            response += "```mermaid\n"
            response += "graph LR\n"
            response += "    subgraph TOP[🏆 Top Productos Vendidos]\n"
            for i, p in enumerate(stats["top_productos_vendidos"][:5], 1):
                nombre = p.get("nombre", "Producto")[:20].replace('"', "'")
                cantidad = p.get("total_vendido", 0)
                response += f'        P{i}["{nombre}<br/>{cantidad} uds"]\n'
            response += "    end\n"
            response += "```\n\n"

        response += "---\n"
        response += "⚠️ *Nota: Tuve dificultades procesando tu pregunta completa. "
        response += "Aquí tienes un resumen de los datos principales. "
        response += "¿Puedes reformular tu pregunta de forma más específica?*"

        return response

    def get_quick_insights(self):
        """Genera insights rápidos del estado actual"""
        try:
            context = self.get_comprehensive_context()

            prompt = f"""{self.create_system_prompt()}

{self.format_data_for_llm(context, include_schema=False, include_stats=True)}

Genera un resumen ejecutivo breve (3-5 puntos) con los insights más importantes del inventario actual. 
Incluye alertas si hay productos agotados o stock bajo. Sé conciso y directo."""

            response = self.model.generate_content(
                prompt, generation_config=self.generation_config
            )

            return response.text

        except Exception as e:
            return f"Error generando insights: {str(e)}"

    def suggest_questions(self):
        """Sugiere preguntas inteligentes basadas en los datos actuales"""
        try:
            context = self.get_comprehensive_context()

            prompt = f"""{self.create_system_prompt()}

{self.format_data_for_llm(context, include_schema=False, include_stats=True)}

Basándote en los datos actuales del inventario, sugiere 5 preguntas inteligentes que el usuario podría hacerte para obtener insights valiosos. 
Las preguntas deben ser específicas y relevantes a la situación actual del negocio.
Formato: Solo lista las preguntas, una por línea, con emoji al inicio."""

            response = self.model.generate_content(
                prompt, generation_config=self.generation_config
            )

            return response.text

        except Exception as e:
            return "¿Qué te gustaría saber sobre tu inventario?"

    def get_help_message(self):
        """Mensaje de ayuda conversacional"""
        return """¡Hola! 👋 Soy InventoryBot, tu asistente de inventario con acceso directo a la base de datos.

🔍 PUEDO ANALIZAR:
- Productos, stock, precios y categorías
- Ventas y compras con estadísticas detalladas
- Top clientes y productos más vendidos
- Valor total del inventario
- Tendencias y patrones

💬 EJEMPLOS DE PREGUNTAS:
- "¿Cuáles son los 5 productos más vendidos?"
- "¿Quiénes son mis mejores clientes?"
- "¿Cuál es el valor total de mi inventario?"
- "¿Qué productos necesito reabastecer urgentemente?"
- "Compara las ventas de este mes vs el anterior"
- "¿Qué categoría genera más ingresos?"

📊 TENGO ACCESO A:
- Estructura completa de la base de datos
- Estadísticas en tiempo real
- Métricas de negocio avanzadas

¡Pregúntame lo que necesites!"""
