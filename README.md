# WMS - Sistema de Gestión de Inventario (Python + Django)

**WMS Management System** es una aplicación completa desarrollada con **Django** bajo el patrón **MVC**, diseñada para administrar inventarios, ventas, compras, productos, clientes, proveedores y almacenes.

## Funcionalidades Principales

- **Dashboard**: Panel principal con estadísticas generales y visualización resumida de todos los módulos del sistema.
- **Productos**: Gestión completa de productos con código, nombre, descripción, categoría, precios de compra/venta y control de stock.
- **Categorías**: Organización de productos por categorías personalizables para mejor clasificación.
- **Clientes**: Administración de clientes con datos de contacto, historial de compras y seguimiento de transacciones.
- **Proveedores**: Gestión de proveedores con información de contacto y registro de compras realizadas.
- **Almacenes**: Control de múltiples almacenes con capacidad, ubicación y productos asignados.
- **Movimientos Inventario**: Registro detallado de entradas y salidas de productos con trazabilidad completa.
- **Roles**: Sistema de permisos y roles personalizables para control de acceso granular.
- **Ventas**: Registro de ventas con cliente, productos vendidos, cantidades, precios y métodos de pago.
- **Detalle Ventas**: Desglose completo de cada venta con productos, cantidades, subtotales e IVA.
- **Compras**: Gestión de compras a proveedores con productos, cantidades y costos.
- **Detalle Compras**: Desglose detallado de cada compra realizada con precios y totales.
- **Reportes**: Generación de reportes de ventas, compras, inventario y análisis financiero.
- **Configuración**: Gestión de usuarios del sistema, perfiles, contraseñas y parámetros generales.
- **Documentación**: Página completa con guía de funcionalidades, tecnologías usadas, arquitectura y usuarios de prueba.

### Chatbot con IA - Sistema de Inventario

Asistente virtual con Inteligencia Artificial integrado al Sistema de Inventario. Utiliza Google Gemini AI para responder preguntas y ayudar con la gestión del inventario mediante lenguaje natural.

- **"ayuda"** - Muestra qué puede hacer el chatbot
- **"buscar producto [nombre]"** - Busca productos específicos
- **"resumen de ventas"** - Muestra estadísticas de ventas
- **"resumen de compras"** - Muestra estadísticas de compras
- **"productos con stock bajo"** - Lista productos con poco inventario

## Roles de Usuario Iniciales

El sistema está diseñado con **roles personalizables**:

1. **Administrador**: Acceso completo a todos los módulos del sistema
2. **Vendedor**: Acceso a ventas, clientes y consulta de productos
3. **Almacenero**: Gestión de inventario, movimientos y almacenes
4. **Supervisor**: Visualización de reportes y estadísticas

## Tecnologías Usadas

| **Tecnología**             | **Descripción**                                                                                                                                                   |
|----------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Django 5.0**             | Framework web de alto nivel para Python que fomenta el desarrollo rápido y el diseño limpio.                                                                     |
| **Python 3.11**            | Lenguaje de programación potente y versátil para desarrollo backend.                                                                                              |
| **MySQL 8.0**              | Sistema de gestión de bases de datos relacional robusto y escalable.                                                                                              |
| **Docker & Docker Compose**| Plataforma de contenerización para desarrollo, envío y ejecución de aplicaciones de forma aislada.                                                                |
| **Make**                   | Herramienta de automatización de tareas que simplifica comandos complejos.                                                                                        |
| **phpMyAdmin**             | Interfaz web para administración de bases de datos MySQL.                                                                                                         |

---

## Usuarios de Prueba

| **Nombre**                     | **Usuario**                       | **Contraseña** | **Rol**         |
|---------------------------------|-----------------------------------|----------------|-----------------|
| JonathanA Admin                 | admin                            | admin123       | Administrador   |
| JonathanA SuperAdmin            | superadmin                       | password       | Administrador   |
| JonathanA Vendedor              | jperez                           | vendedor123    | Gerente         |
| JonathanA Gerente               | mgonzalez                        | almacen123     | Vendedor        |

---

## Configuración del Entorno (.env)

```env
PROJECT_NAME=WMS_Management_System
DB_DATABASE=wms_management_system
MYSQL_USER=jonathanA
MYSQL_PASSWORD=password
MY_USER=jonathanA
MY_GROUP=jonathanA
APP_PORT=8081
PHPMYADMIN_PORT=8082
```

---

## Instalación

### Requisitos Previos

- Tener **Docker** y **Docker Compose** instalados.
- **Make**: Utilizado para automatizar procesos y gestionar contenedores de manera más eficiente.

### Pasos de Instalación

1. Clona el repositorio desde GitHub.
2. Dentro del repositorio, encontrarás un archivo **Makefile** que contiene los comandos necesarios para iniciar y gestionar tu aplicación.
3. Usa los siguientes comandos de **ps1** para interactuar con la aplicación:

   - **`.\make.ps1 init-app`**: Inicializa los contenedores y configura la aplicación.
   - **`.\make.ps1 up`**: Levanta la aplicación y sus contenedores asociados.
   - **`.\make.ps1 down`**: Detiene los contenedores y apaga la aplicación.
   - **`.\make.ps1 shell`**: Ingresa al contenedor para interactuar directamente con el sistema en su entorno de ejecución.
   - **`.\make.ps1 init-chatbot`**: Instala y configura el chatbot en el sistema.

4. Además de estos comandos, dentro del archivo **Make** puedes encontrar otros comandos que te permitirán interactuar de manera más específica con los contenedores y los diferentes servicios que conforman la aplicación.

5. Accede a los siguientes URL:
   - **Aplicación Web**: [http://localhost:8081/](http://localhost:8081/)
   - **PhpMyAdmin**: [http://localhost:8082/](http://localhost:8082/)

---

## Instalación en Windows (Sin Make)

configuracion manual:

```powershell
# 1. Copiar archivo de configuración
Copy-Item .env.example .env

# 2. Copiar .env a la carpeta Docker
Copy-Item .env .docker\.env

# 3. Levantar los contenedores
docker compose -f .docker/docker-compose.yml up -d

# 4. Ver estado de los contenedores
docker compose -f .docker/docker-compose.yml ps

# 5. Inicializar el chatbot (opcional)
docker compose -f .docker/docker-compose.yml exec server_docker python init_chatbot.py

# 6. Detener los contenedores
docker compose -f .docker/docker-compose.yml down
```

---

