from PySide6.QtWidgets import (QMainWindow, QMessageBox, QDialog, QVBoxLayout, 
                               QHBoxLayout, QLabel, QPushButton, QScrollArea)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from WIDGET.ui_main_window import Ui_MainWindow 
from VIEWS.equipos import EquiposView
from VIEWS.participantes import ParticipantesView
from VIEWS.partidos import PartidosView
from RESOURCES.utilidades import obtener_ruta_recurso

class MainWindow(QMainWindow):
    """Ventana principal de la aplicación."""
    
    def __init__(self):
        super().__init__()
        # Cargar diseño del .ui
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Cargar imágenes con rutas correctas
        self._cargar_imagenes()
        
        # Conectar botones del menú principal
        self.ui.btn_equipos.clicked.connect(self.abrir_equipos)
        self.ui.btn_participantes.clicked.connect(self.abrir_participantes)
        self.ui.btn_partidos.clicked.connect(self.abrir_partidos)
        self.ui.btn_eliminatorias.clicked.connect(self.abrir_partidos)  # Mismo que partidos
        self.ui.btn_creditos.clicked.connect(self.mostrar_creditos)
        self.ui.btn_ayuda.clicked.connect(self.mostrar_ayuda)
        
        # Vistas (se crean cuando se necesitan)
        self.vista_equipos = None
        self.vista_participantes = None
        self.vista_partidos = None
        
        # Mensaje de bienvenida
        self.ui.statusbar.showMessage("¡Bienvenido al Gestor de Torneo de Fútbol!")
    
    def _cargar_imagenes(self):
        """Carga todas las imágenes de los botones con rutas correctas."""
        imagenes = {
            'imagen_principal': 'img/futbol.png',
            'img_equipos': 'img/eq.jpg',
            'img_participantes': 'img/par.jpg',
            'img_calendario': 'img/cal.jpg',
            'img_eliminatorias': 'img/eliminatoria.jpg'
        }
        
        for widget_name, ruta in imagenes.items():
            try:
                widget = getattr(self.ui, widget_name, None)
                if widget is not None:
                    ruta_completa = obtener_ruta_recurso(ruta)
                    print(f"[DEBUG] Cargando {widget_name}: {ruta_completa}")
                    
                    pixmap = QPixmap(ruta_completa)
                    if not pixmap.isNull():
                        widget.setPixmap(pixmap)
                        print(f"[DEBUG] OK - Imagen cargada correctamente")
                    else:
                        print(f"[DEBUG] FAIL - QPixmap esta null - ruta invalida")
            except Exception as e:
                print(f"[DEBUG] Error cargando imagen {widget_name}: {e}")
        
    def abrir_equipos(self):
        """Abre la ventana de gestión de equipos."""
        if self.vista_equipos is None:
            self.vista_equipos = EquiposView()
        self.vista_equipos.show()
        self.vista_equipos.cargar_equipos()
        self.ui.statusbar.showMessage("Gestión de Equipos abierta")
        
    def abrir_participantes(self):
        """Abre la ventana de gestión de participantes."""
        if self.vista_participantes is None:
            self.vista_participantes = ParticipantesView()
        self.vista_participantes.show()
        self.vista_participantes.cargar_participantes()
        self.ui.statusbar.showMessage("Gestión de Participantes abierta")
        
    def abrir_partidos(self):
        """Abre la ventana de gestión de partidos."""
        if self.vista_partidos is None:
            self.vista_partidos = PartidosView()
        self.vista_partidos.show()
        self.vista_partidos.cargar_partidos()
        self.ui.statusbar.showMessage("Gestión de Partidos abierta")
        
    def mostrar_creditos(self):
        """Muestra los créditos de la aplicación con imagen del campo."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Créditos")
        dialog.setMinimumSize(900, 450)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: black;
                background-color: white;
            }
        """)
        
        layout = QHBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Logo a la izquierda 
        imagen_label = QLabel()
        imagen_cargada = False
        
        try:
            # Intentar cargar la imagen (me dio muchos errores)
            rutas_posibles = [
                obtener_ruta_recurso("img/logo.webp"),
                obtener_ruta_recurso("RESOURCES/img/logo.webp"),
            ]
            
            print("[DEBUG CREDITOS] Rutas a probar:")
            for ruta in rutas_posibles:
                print(f"  - {ruta}")
            
            pixmap = None
            for ruta in rutas_posibles:
                pixmap = QPixmap(ruta)
                if not pixmap.isNull():
                    print(f"[DEBUG CREDITOS] OK - Imagen cargada desde: {ruta}")
                    imagen_cargada = True
                    break
                else:
                    print(f"[DEBUG CREDITOS] FAIL - Fallo en: {ruta}")
            
            if imagen_cargada:
                pixmap = pixmap.scaledToWidth(300, Qt.SmoothTransformation)
                imagen_label.setPixmap(pixmap)
                imagen_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        except Exception as e:
            pass
        
        if not imagen_cargada:
            # Si no se carga la imagen, mostrar placeholder
            imagen_label.setText("Imagen del campo\nde fútbol")
            imagen_label.setAlignment(Qt.AlignCenter)
            imagen_label.setStyleSheet("color: #DC143C; font-weight: bold; border: 2px dashed #DC143C; padding: 20px;")
        
        layout.addWidget(imagen_label, 1)
        
        # Texto de créditos a la derecha
        creditos_text = """
        <h2 style='color: #DC143C;'>APP Torneo de Fútbol</h2>
        <b>Fecha:</b> 4 Febrero 2026<br>
        <b>Autor:</b> Miguel Ángel Iñigo Montero<br>
        <b>Instituto:</b> IES Brianda de Mendoza<br>
        <br>
        <p>Aplicación desarrollada como proyecto educativo para la gestión
        de torneos de fútbol por eliminatorias en el instituto.</p>
        
        <p style='color: #DC143C;'><b>¡Gracias por usar esta aplicación!</b></p>
        """
        
        texto_label = QLabel(creditos_text)
        texto_label.setTextFormat(Qt.RichText)
        texto_label.setWordWrap(True)
        texto_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        layout.addWidget(texto_label, 1)
        
        dialog.exec()
        
    def mostrar_ayuda(self):
        """Muestra la ayuda de la aplicación con logo en la parte superior."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Ayuda - Manual de Usuario")
        dialog.setMinimumSize(600, 700)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                color: black;
                background-color: white;
            }
            QPushButton {
                background-color: #DC143C;
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #B81030;
            }
        """)
        
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Imagen de futbol en la parte superior
        logo_label = QLabel()
        logo_cargado = False
        
        try:
            # Intentar cargar la imagen (me dio muchos errores)
            rutas_posibles = [
                obtener_ruta_recurso("img/futbol.png"),
                obtener_ruta_recurso("RESOURCES/img/futbol.png"),
            ]
            
            print("[DEBUG AYUDA] Rutas a probar:")
            for ruta in rutas_posibles:
                print(f"  - {ruta}")
            
            pixmap = None
            for ruta in rutas_posibles:
                pixmap = QPixmap(ruta)
                if not pixmap.isNull():
                    print(f"[DEBUG AYUDA] OK - Imagen cargada desde: {ruta}")
                    logo_cargado = True
                    break
                else:
                    print(f"[DEBUG AYUDA] FAIL - Fallo en: {ruta}")
            
            if logo_cargado:
                pixmap = pixmap.scaledToHeight(100, Qt.SmoothTransformation)
                logo_label.setPixmap(pixmap)
                logo_label.setAlignment(Qt.AlignCenter)
                layout.addWidget(logo_label)
        except Exception:
            pass
        
        if not logo_cargado:
            logo_label.setText("Logo de la Aplicación")
            logo_label.setAlignment(Qt.AlignCenter)
            logo_label.setStyleSheet("color: #DC143C; font-weight: bold; padding: 20px; border: 2px dashed #DC143C;")
            layout.addWidget(logo_label)
        
        # Área desplazable para el texto de ayuda
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { background-color: white; }")
        
        ayuda_text = """
        <h2 style='color: #DC143C;'>Manual de Usuario</h2>
        
        <h3 style='color: #DC143C;'>Equipos</h3>
        <p>
        • <b>Anadir:</b> Crear nuevos equipos con nombre, curso y color<br>
        • <b>Editar:</b> Modificar datos de equipos existentes<br>
        • <b>Ver:</b> Ver la lista de jugadores asignados al equipo<br>
        • <b>Eliminar:</b> Eliminar equipos (requiere confirmacion)
        </p>
        
        <h3 style='color: #DC143C;'>Participantes</h3>
        <p>
        • Registrar jugadores y arbitros<br>
        • Un participante puede ser jugador, arbitro o ambos<br>
        • Especificar posicion para jugadores<br>
        • Ver estadisticas de goles y tarjetas
        </p>
        
        <h3 style='color: #DC143C;'>Partidos</h3>
        <p>
        • <b>Programar partidos</b> por eliminatorias (Octavos, Cuartos, Semifinal, Final)<br>
        • Asignar arbitros a cada partido<br>
        • Registrar resultados y goles<br>
        • Ver cuadro completo de eliminatorias
        </p>
        
        <h3 style='color: #DC143C;'>Consejos</h3>
        <p>
        • Crea primero los equipos y participantes<br>
        • Asigna jugadores a los equipos<br>
        • Programa los partidos de octavos<br>
        • Registra los resultados para avanzar en el torneo
        </p>
        """
        
        texto_label = QLabel(ayuda_text)
        texto_label.setTextFormat(Qt.RichText)
        texto_label.setWordWrap(True)
        texto_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        scroll_area.setWidget(texto_label)
        layout.addWidget(scroll_area)
        
        # Botón cerrar
        btn_cerrar = QPushButton("Cerrar")
        btn_cerrar.clicked.connect(dialog.close)
        layout.addWidget(btn_cerrar)
        
        dialog.exec()