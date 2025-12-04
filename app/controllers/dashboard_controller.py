from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from config.database import Database
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.sale import Sale
from app.models.purchase import Purchase
from app.models.client import Client
from app.models.supplier import Supplier
from app.models.warehouse import Warehouse
from app.models.inventory_movement import InventoryMovement
from app.views.dashboard_view import DashboardView
import json


class DashboardController:
    """Controlador del Dashboard"""

    @staticmethod
    def index(request):
        """Muestra el dashboard"""
        # Verificar autenticación
        user_id = request.session.get("user_id")

        if not user_id:
            return HttpResponseRedirect("/login/")

        # Obtener datos del usuario
        user = User.get_by_id(user_id)

        if not user:
            request.session.flush()
            return HttpResponseRedirect("/login/")

        # Obtener estadísticas principales
        stats = {
            "total_productos": Product.count(),
            "total_categorias": Category.count(),
            "total_clientes": Client.count(),
            "total_proveedores": Supplier.count(),
            "total_almacenes": Warehouse.count(),
            "ventas_mes": Sale.total_ventas_mes(),
            "compras_mes": Purchase.total_compras_mes(),
            "total_ventas": Sale.count(),
            "total_compras": Purchase.count(),
            "total_movimientos": InventoryMovement.count(),
        }

        # Obtener productos con stock bajo (menos de 10 unidades)
        productos_bajo_stock = Product.get_low_stock(limit=10)

        # Obtener últimas ventas
        ultimas_ventas = Sale.get_all(limit=5)

        # Obtener últimas compras
        ultimas_compras = Purchase.get_all(limit=5)

        # Obtener datos para gráficas
        chart_data = DashboardController.get_chart_data()

        # Renderizar dashboard
        return HttpResponse(
            DashboardView.index(
                user,
                request.path,
                stats,
                productos_bajo_stock,
                ultimas_ventas,
                ultimas_compras,
                chart_data,
            )
        )

    @staticmethod
    def get_chart_data():
        """Obtiene los datos para las gráficas del dashboard"""
        chart_data = {
            "ventas_por_mes": [],
            "compras_por_mes": [],
            "productos_por_categoria": [],
            "top_productos": [],
            "ventas_vs_compras": [],
            "stock_por_categoria": [],
        }

        try:
            # Ventas por mes (todas las ventas históricas)
            ventas_mes_query = """
                SELECT 
                    DATE_FORMAT(fecha, '%%Y-%%m') as mes,
                    DATE_FORMAT(fecha, '%%b %%Y') as mes_label,
                    COUNT(*) as num_ventas,
                    COALESCE(SUM(total), 0) as total
                FROM ventas
                GROUP BY DATE_FORMAT(fecha, '%%Y-%%m'), DATE_FORMAT(fecha, '%%b %%Y')
                ORDER BY mes DESC
                LIMIT 12
            """
            ventas_mes = Database.execute_query(ventas_mes_query)
            # Invertir para mostrar de más antiguo a más reciente
            chart_data["ventas_por_mes"] = (
                [
                    {
                        "mes": v["mes_label"],
                        "total": float(v["total"]),
                        "cantidad": v["num_ventas"],
                    }
                    for v in reversed(ventas_mes)
                ]
                if ventas_mes
                else []
            )

            # Compras por mes (todas las compras históricas)
            compras_mes_query = """
                SELECT 
                    DATE_FORMAT(fecha, '%%Y-%%m') as mes,
                    DATE_FORMAT(fecha, '%%b %%Y') as mes_label,
                    COUNT(*) as num_compras,
                    COALESCE(SUM(total), 0) as total
                FROM compras
                GROUP BY DATE_FORMAT(fecha, '%%Y-%%m'), DATE_FORMAT(fecha, '%%b %%Y')
                ORDER BY mes DESC
                LIMIT 12
            """
            compras_mes = Database.execute_query(compras_mes_query)
            # Invertir para mostrar de más antiguo a más reciente
            chart_data["compras_por_mes"] = (
                [
                    {
                        "mes": c["mes_label"],
                        "total": float(c["total"]),
                        "cantidad": c["num_compras"],
                    }
                    for c in reversed(compras_mes)
                ]
                if compras_mes
                else []
            )

            # Productos por categoría
            productos_categoria_query = """
                SELECT 
                    c.nombre as categoria,
                    COUNT(p.id) as cantidad
                FROM categorias c
                LEFT JOIN productos p ON c.id = p.categoria_id
                GROUP BY c.id, c.nombre
                ORDER BY cantidad DESC
                LIMIT 10
            """
            productos_cat = Database.execute_query(productos_categoria_query)
            chart_data["productos_por_categoria"] = (
                [
                    {"categoria": p["categoria"], "cantidad": p["cantidad"]}
                    for p in productos_cat
                ]
                if productos_cat
                else []
            )

            # Top 5 productos más vendidos (todas las ventas)
            top_productos_query = """
                SELECT 
                    p.nombre,
                    COALESCE(SUM(dv.cantidad), 0) as total_vendido,
                    COALESCE(SUM(dv.subtotal), 0) as ingresos
                FROM productos p
                LEFT JOIN detalle_ventas dv ON p.id = dv.producto_id
                LEFT JOIN ventas v ON dv.venta_id = v.id
                GROUP BY p.id, p.nombre
                HAVING total_vendido > 0
                ORDER BY total_vendido DESC
                LIMIT 5
            """
            top_prod = Database.execute_query(top_productos_query)
            chart_data["top_productos"] = (
                [
                    {
                        "nombre": t["nombre"],
                        "vendido": int(t["total_vendido"]),
                        "ingresos": float(t["ingresos"]),
                    }
                    for t in top_prod
                ]
                if top_prod
                else []
            )

            # Stock por categoría (mostrar todas las categorías)
            stock_categoria_query = """
                SELECT 
                    c.nombre as categoria,
                    COALESCE(SUM(p.stock_actual), 0) as stock_total,
                    COALESCE(SUM(p.stock_actual * p.precio_venta), 0) as valor_stock
                FROM categorias c
                LEFT JOIN productos p ON c.id = p.categoria_id
                GROUP BY c.id, c.nombre
                ORDER BY stock_total DESC
                LIMIT 8
            """
            stock_cat = Database.execute_query(stock_categoria_query)
            chart_data["stock_por_categoria"] = (
                [
                    {
                        "categoria": s["categoria"],
                        "stock": int(s["stock_total"]),
                        "valor": float(s["valor_stock"]),
                    }
                    for s in stock_cat
                ]
                if stock_cat
                else []
            )

        except Exception as e:
            print(f"Error obteniendo datos de gráficas: {e}")

        return chart_data

    @staticmethod
    def api_chart_data(request):
        """API endpoint para obtener datos de gráficas (para actualización dinámica)"""
        user_id = request.session.get("user_id")
        if not user_id:
            return JsonResponse({"error": "No autenticado"}, status=401)

        chart_data = DashboardController.get_chart_data()
        return JsonResponse(chart_data)
