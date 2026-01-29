"""
Aplicación de Gestión de Torneo de Fútbol
Descripción: Aplicación para gestionar torneos de fútbol con sistema de eliminatorias,
registro de equipos, participantes, partidos y estadísticas.
"""

import sys
import os
import logging
from PySide6.QtWidgets import QApplication, QSplashScreen, QMessageBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer
from VIEWS.main_window import MainWindow
from MODELS.database import conectar
from RESOURCES.utilidades import obtener_ruta_recurso
import config

# Configurar logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT,
    handlers=[
        logging.FileHandler(config.LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_stylesheet(path):
    """
    Carga el archivo QSS y lo devuelve como string.
    
    Args:
        path (str): Ruta al archivo QSS
        
    Returns:
        str: Contenido del archivo QSS
    """
    try:
        with open(path, "r", encoding="utf-8") as file:
            content = file.read()
            logger.info(f"Hoja de estilos cargada: {path}")
            return content
    except FileNotFoundError:
        logger.warning(f"No se encontró el archivo de estilos: {path}")
        return ""
    except Exception as e:
        logger.error(f"Error al cargar estilos: {e}")
        return ""


def main():
    """
    Función principal que inicia la aplicación.
    """
    try:
        logger.info("=" * 60)
        logger.info("Iniciando aplicación...")
        logger.info(f"Versión: {config.APP_VERSION}")
        logger.info(f"Autor: {config.APP_AUTHOR}")
        logger.info("=" * 60)
        
        # Crear aplicación
        app = QApplication(sys.argv)
        app.setApplicationName(config.APP_NAME)
        app.setApplicationVersion(config.APP_VERSION)
        app.setOrganizationName(config.APP_ORGANIZATION)
        
        # Cargar estilo QSS
        qss_path = obtener_ruta_recurso(config.STYLESHEET_PATH)
        qss = load_stylesheet(qss_path)
        if qss:
            app.setStyleSheet(qss)
            logger.info("Estilos aplicados correctamente")
        
        # Inicializar base de datos si es necesario
        logger.info("Verificando base de datos...")
        import inicializar_db
        inicializar_db.inicializar_datos()
        
        # Conectar a la base de datos
        logger.info("Conectando a la base de datos...")
        db = conectar()
        logger.info("Base de datos conectada correctamente")
        
        # Crear y mostrar ventana principal
        logger.info("Creando ventana principal...")
        window = MainWindow()
        window.show()
        
        logger.info("Aplicación iniciada correctamente")
        logger.info("=" * 60)
        
        # Ejecutar aplicación
        sys.exit(app.exec())
        
    except Exception as e:
        logger.error(f"Error crítico al iniciar la aplicación: {e}", exc_info=True)
        error_msg = f"Error al iniciar la aplicación:\n\n{str(e)}\n\nVer archivo '{config.LOG_FILE}' para más detalles."
        
        # Intentar mostrar un cuadro de diálogo de error
        try:
            app = QApplication.instance() or QApplication(sys.argv)
            QMessageBox.critical(None, f"{config.APP_NAME} - Error", error_msg)
        except:
            print(error_msg)
        
        sys.exit(1)


if __name__ == "__main__":
    main()