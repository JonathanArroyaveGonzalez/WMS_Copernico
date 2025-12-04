from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app.models.user import User
from app.models.chatbot_message import ChatbotMessage
from app.services.ai_service import AIService
from app.views.chatbot_view import ChatbotView
import json


class ChatbotController:
    """Controlador del Chatbot con IA mejorado"""

    @staticmethod
    def index(request):
        """Muestra la interfaz del chatbot"""
        user_id = request.session.get("user_id")

        if not user_id:
            return HttpResponseRedirect("/login/")

        user = User.get_by_id(user_id)

        if not user:
            request.session.flush()
            return HttpResponseRedirect("/login/")

        # Obtener historial de conversación
        history = ChatbotMessage.get_history(user_id, limit=20)

        # Inicializar servicio de IA
        try:
            ai_service = AIService()

            # Generar insights y sugerencias para la vista inicial
            quick_insights = ai_service.get_quick_insights()
            suggested_questions = ai_service.suggest_questions()

        except Exception as e:
            quick_insights = None
            suggested_questions = None
            print(f"Error inicializando AI: {e}")

        # Renderizar vista con información adicional
        return HttpResponse(
            ChatbotView.render(
                user,
                history,
                quick_insights=quick_insights,
                suggested_questions=suggested_questions,
            )
        )

    @staticmethod
    def send_message(request):
        """Procesa un mensaje del usuario y retorna la respuesta de la IA"""
        user_id = request.session.get("user_id")

        if not user_id:
            return JsonResponse(
                {"success": False, "error": "No autenticado"}, status=401
            )

        if request.method != "POST":
            return JsonResponse(
                {"success": False, "error": "Método no permitido"}, status=405
            )

        try:
            body = json.loads(request.body.decode("utf-8"))
            user_message = body.get("message", "").strip()

            if not user_message:
                return JsonResponse(
                    {"success": False, "error": "Mensaje vacío"}, status=400
                )

            # Inicializar servicio de IA
            try:
                ai_service = AIService()
            except Exception as e:
                return JsonResponse(
                    {
                        "success": False,
                        "error": f"Error de configuración de IA: {str(e)}",
                    },
                    status=500,
                )

            # Obtener historial para contexto conversacional
            history = ChatbotMessage.get_history(user_id, limit=10)

            # Convertir historial al formato esperado por el AI Service
            conversation_history = []
            for msg in history:
                conversation_history.append(
                    {"is_user": True, "content": msg.get("message", "")}
                )
                conversation_history.append(
                    {"is_user": False, "content": msg.get("response", "")}
                )

            # Procesar el mensaje con contexto completo
            response = ai_service.process_query(
                user_message, user_id, conversation_history=conversation_history
            )

            # Guardar mensaje y respuesta en la base de datos
            ChatbotMessage.save(user_id, user_message, response)

            # Renderizar el Markdown a HTML usando la misma función que el historial
            response_html = ChatbotView.format_markdown(response)

            return JsonResponse(
                {
                    "success": True,
                    "message": user_message,
                    "response": response,
                    "response_html": response_html,  # HTML ya renderizado
                    "timestamp": ChatbotMessage.get_current_timestamp(),
                }
            )

        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "error": "JSON inválido"}, status=400
            )
        except Exception as e:
            return JsonResponse(
                {"success": False, "error": f"Error al procesar mensaje: {str(e)}"},
                status=500,
            )

    @staticmethod
    def get_insights(request):
        """Obtiene insights rápidos del inventario"""
        user_id = request.session.get("user_id")

        if not user_id:
            return JsonResponse(
                {"success": False, "error": "No autenticado"}, status=401
            )

        try:
            ai_service = AIService()
            insights = ai_service.get_quick_insights()

            return JsonResponse({"success": True, "insights": insights})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    @staticmethod
    def get_suggestions(request):
        """Obtiene sugerencias de preguntas inteligentes"""
        user_id = request.session.get("user_id")

        if not user_id:
            return JsonResponse(
                {"success": False, "error": "No autenticado"}, status=401
            )

        try:
            ai_service = AIService()
            suggestions = ai_service.suggest_questions()

            return JsonResponse({"success": True, "suggestions": suggestions})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    @staticmethod
    def clear_history(request):
        """Limpia el historial de conversación del usuario"""
        user_id = request.session.get("user_id")

        if not user_id:
            return JsonResponse(
                {"success": False, "error": "No autenticado"}, status=401
            )

        if request.method != "POST":
            return JsonResponse(
                {"success": False, "error": "Método no permitido"}, status=405
            )

        try:
            ChatbotMessage.delete_history(user_id)

            return JsonResponse(
                {"success": True, "message": "Historial eliminado correctamente"}
            )
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    @staticmethod
    def get_history(request):
        """Obtiene el historial de conversación"""
        user_id = request.session.get("user_id")

        if not user_id:
            return JsonResponse(
                {"success": False, "error": "No autenticado"}, status=401
            )

        try:
            history = ChatbotMessage.get_history(user_id, limit=50)

            return JsonResponse({"success": True, "history": history})
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)
