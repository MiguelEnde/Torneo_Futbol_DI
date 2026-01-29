"""
Configuración general de la aplicación.
Parámetros y constantes de la aplicación.
"""

# Información de la aplicación
APP_NAME = "App Torneo de Fútbol"
APP_VERSION = "1.0"
APP_AUTHOR = "Miguel Ángel Iñigo Montero"
APP_ORGANIZATION = "Instituto Educativo"
APP_DESCRIPTION = "Aplicación para gestionar torneos de fútbol por eliminatorias"

# Base de datos
DB_NAME = "torneo_futbol_sqlite.db"
DB_TYPE = "QSQLITE"

# Configuración de la interfaz
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
WINDOW_MIN_WIDTH = 1000
WINDOW_MIN_HEIGHT = 700

# Colores
COLOR_PRIMARY = "#DC143C"      # Rojo crimson
COLOR_SECONDARY = "#2C2C2C"    # Gris oscuro
COLOR_BACKGROUND = "#FFFFFF"   # Blanco
COLOR_TEXT = "#000000"         # Negro
COLOR_SUCCESS = "#00A86B"      # Verde
COLOR_ERROR = "#FF0000"        # Rojo
COLOR_WARNING = "#FFB300"      # Naranja
COLOR_INFO = "#0066CC"         # Azul

# Eliminatorias disponibles
ELIMINATORIAS = ["Octavos", "Cuartos", "Semifinal", "Final"]

# Posiciones en fútbol
POSICIONES = ["Portero", "Defensa Central", "Lateral", "Centrocampista", "Delantero"]

# Puntos por resultado
PUNTOS_VICTORIA = 3
PUNTOS_EMPATE = 1
PUNTOS_DERROTA = 0

# Límites de visualización
LIMITE_GOLEADORES = 10
LIMITE_TARJETADOS = 10
LIMITE_PROXIMOS_PARTIDOS = 5

# Configuración de logging
LOG_FILE = "torneo_futbol.log"
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Validaciones
MIN_NOMBRE_LENGTH = 2
MIN_EDAD = 10
MAX_EDAD = 50

# Tipos de tarjeta
TIPOS_TARJETA = ["amarilla", "roja"]

# Estilos
STYLESHEET_PATH = "qss/estilo.qss"
ICON_SIZE = 32

# Configuración de tabla
ITEMS_PER_PAGE = 50

# Mensajes de confirmación
MSG_CONFIRM_DELETE = "¿Está seguro de que desea eliminar este elemento?\nEsta acción no se puede deshacer."
MSG_SUCCESS = "Operación realizada correctamente"
MSG_ERROR = "Error al realizar la operación"
MSG_WARNING = "Advertencia"

# Estados de partido
ESTADO_PENDIENTE = "Pendiente"
ESTADO_FINALIZADO = "Finalizado"
ESTADO_EN_JUEGO = "En juego"

# Formatos
FORMATO_FECHA = "dd/MM/yyyy"
FORMATO_FECHA_HORA = "dd/MM/yyyy HH:mm"
FORMATO_BD_FECHA = "yyyy-MM-dd"
FORMATO_BD_FECHA_HORA = "yyyy-MM-dd HH:mm"

# Expresiones regulares
REGEX_EMAIL = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
REGEX_TELEFONO = r'^\d{9,}$'

# Configuración de seguridad
ENABLE_SOFT_DELETE = True  # Usar soft delete en lugar de hard delete
REQUIRE_CONFIRMATION = True  # Requerir confirmación para operaciones destructivas

# Configuración de rendimiento
USAR_CACHE = False  # Usar caché de datos
TIMEOUT_DB = 5000  # ms
MAX_RESULTADOS_QUERY = 1000

# Rutas por defecto
RUTA_RECURSOS = "RESOURCES"
RUTA_IMAGENES = "RESOURCES/img"
RUTA_ICONOS = "RESOURCES/iconos"
RUTA_QSS = "RESOURCES/qss"
