from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QLabel, QLineEdit, QComboBox, QMessageBox,
                               QDialog, QFormLayout, QDialogButtonBox, QGroupBox,
                               QListWidget, QSplitter)
from PySide6.QtCore import Qt
from PySide6.QtSql import QSqlQuery
from CONTROLLERS.equipos_controller import EquiposController

class EquiposView(QWidget):
    """Vista principal para gestión de equipos."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.cargar_equipos()
        
    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Título
        title_label = QLabel("Gestión de Equipos")
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: #DC143C;")
        layout.addWidget(title_label)
        
        # Barra de herramientas
        toolbar_layout = QHBoxLayout()
        
        self.btn_nuevo = QPushButton("➕ Nuevo Equipo")
        self.btn_nuevo.setToolTip("Crear un nuevo equipo")
        self.btn_nuevo.clicked.connect(self.nuevo_equipo)
        
        self.btn_editar = QPushButton("✏️ Editar")
        self.btn_editar.setToolTip("Editar equipo seleccionado")
        self.btn_editar.clicked.connect(self.editar_equipo)
        self.btn_editar.setEnabled(False)
        
        self.btn_eliminar = QPushButton("🗑️ Eliminar")
        self.btn_eliminar.setToolTip("Eliminar equipo seleccionado")
        self.btn_eliminar.clicked.connect(self.eliminar_equipo)
        self.btn_eliminar.setEnabled(False)
        
        self.btn_refrescar = QPushButton("🔄 Refrescar")
        self.btn_refrescar.setToolTip("Recargar lista de equipos")
        self.btn_refrescar.clicked.connect(self.cargar_equipos)
        
        toolbar_layout.addWidget(self.btn_nuevo)
        toolbar_layout.addWidget(self.btn_editar)
        toolbar_layout.addWidget(self.btn_eliminar)
        toolbar_layout.addWidget(self.btn_refrescar)
        toolbar_layout.addStretch()
        
        layout.addLayout(toolbar_layout)
        
        # Splitter para tabla de equipos y jugadores
        splitter = QSplitter(Qt.Horizontal)
        
        # Tabla de equipos
        equipos_widget = QWidget()
        equipos_layout = QVBoxLayout(equipos_widget)
        equipos_layout.setContentsMargins(0, 0, 0, 0)
        
        equipos_label = QLabel("Lista de Equipos")
        equipos_label.setStyleSheet("font-weight: bold; font-size: 11pt;")
        equipos_layout.addWidget(equipos_label)
        
        self.tabla_equipos = QTableWidget()
        self.tabla_equipos.setColumnCount(4)
        self.tabla_equipos.setHorizontalHeaderLabels(["ID", "Nombre", "Curso", "Color"])
        self.tabla_equipos.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabla_equipos.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_equipos.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla_equipos.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_equipos.hideColumn(0)  # Ocultar ID
        self.tabla_equipos.itemSelectionChanged.connect(self.equipo_seleccionado)
        equipos_layout.addWidget(self.tabla_equipos)
        
        splitter.addWidget(equipos_widget)
        
        # Panel de jugadores
        jugadores_widget = QWidget()
        jugadores_layout = QVBoxLayout(jugadores_widget)
        jugadores_layout.setContentsMargins(0, 0, 0, 0)
        
        jugadores_label = QLabel("Jugadores del Equipo")
        jugadores_label.setStyleSheet("font-weight: bold; font-size: 11pt;")
        jugadores_layout.addWidget(jugadores_label)
        
        self.lista_jugadores = QListWidget()
        self.lista_jugadores.setStyleSheet("""
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #E0E0E0;
            }
        """)
        jugadores_layout.addWidget(self.lista_jugadores)
        
        btn_asignar_jugador = QPushButton("➕ Asignar Jugador")
        btn_asignar_jugador.clicked.connect(self.asignar_jugador)
        jugadores_layout.addWidget(btn_asignar_jugador)
        
        splitter.addWidget(jugadores_widget)
        splitter.setSizes([500, 300])
        
        layout.addWidget(splitter)
        
    def cargar_equipos(self):
        """Carga los equipos desde la base de datos."""
        self.tabla_equipos.setRowCount(0)
        
        query = QSqlQuery()
        query.exec("""
            SELECT id, nombre, curso, color_camiseta 
            FROM equipos 
            ORDER BY nombre
        """)
        
        row = 0
        while query.next():
            self.tabla_equipos.insertRow(row)
            self.tabla_equipos.setItem(row, 0, QTableWidgetItem(str(query.value(0))))
            self.tabla_equipos.setItem(row, 1, QTableWidgetItem(query.value(1)))
            self.tabla_equipos.setItem(row, 2, QTableWidgetItem(query.value(2)))
            self.tabla_equipos.setItem(row, 3, QTableWidgetItem(query.value(3)))
            row += 1
            
        self.lista_jugadores.clear()
        
    def equipo_seleccionado(self):
        """Maneja la selección de un equipo."""
        has_selection = self.tabla_equipos.currentRow() >= 0
        self.btn_editar.setEnabled(has_selection)
        self.btn_eliminar.setEnabled(has_selection)
        
        if has_selection:
            self.cargar_jugadores_equipo()
            
    def cargar_jugadores_equipo(self):
        """Carga los jugadores del equipo seleccionado."""
        self.lista_jugadores.clear()
        
        selected_row = self.tabla_equipos.currentRow()
        if selected_row < 0:
            return
            
        equipo_id = self.tabla_equipos.item(selected_row, 0).text()
        
        query = QSqlQuery()
        query.prepare("""
            SELECT p.nombre, p.posicion, 
                   COALESCE((SELECT COUNT(*) FROM goles WHERE participante_id = p.id), 0) as goles
            FROM participantes p
            INNER JOIN equipo_participante ep ON p.id = ep.participante_id
            WHERE ep.equipo_id = ? AND p.es_jugador = 1 AND p.activo = 1
            ORDER BY p.nombre
        """)
        query.addBindValue(equipo_id)
        query.exec()
        
        if not query.next():
            self.lista_jugadores.addItem("No hay jugadores asignados")
            return
            
        query.previous()
        while query.next():
            nombre = query.value(0)
            posicion = query.value(1) or "Sin posición"
            goles = query.value(2)
            
            texto = f"{nombre} - {posicion} ({goles} goles)"
            self.lista_jugadores.addItem(texto)
            
    def nuevo_equipo(self):
        """Abre el diálogo para crear un nuevo equipo."""
        dialog = EquipoDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.cargar_equipos()
            QMessageBox.information(self, "Éxito", "Equipo creado correctamente")
            
    def editar_equipo(self):
        """Abre el diálogo para editar el equipo seleccionado."""
        selected_row = self.tabla_equipos.currentRow()
        if selected_row < 0:
            return
            
        equipo_id = int(self.tabla_equipos.item(selected_row, 0).text())
        
        dialog = EquipoDialog(self, equipo_id)
        if dialog.exec() == QDialog.Accepted:
            self.cargar_equipos()
            QMessageBox.information(self, "Éxito", "Equipo actualizado correctamente")
            
    def eliminar_equipo(self):
        """Elimina el equipo seleccionado."""
        selected_row = self.tabla_equipos.currentRow()
        if selected_row < 0:
            return
            
        equipo_id = self.tabla_equipos.item(selected_row, 0).text()
        equipo_nombre = self.tabla_equipos.item(selected_row, 1).text()
        
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Está seguro de eliminar el equipo '{equipo_nombre}'?\n"
            "Esta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            query = QSqlQuery()
            query.prepare("UPDATE equipos SET activo = 0 WHERE id = ?")
            query.addBindValue(equipo_id)
            
            if query.exec():
                self.cargar_equipos()
                QMessageBox.information(self, "Éxito", "Equipo eliminado correctamente")
            else:
                QMessageBox.warning(self, "Error", f"No se pudo eliminar el equipo: {query.lastError().text()}")
                
    def asignar_jugador(self):
        """Asigna un jugador al equipo seleccionado."""
        selected_row = self.tabla_equipos.currentRow()
        if selected_row < 0:
            QMessageBox.warning(self, "Advertencia", "Seleccione un equipo primero")
            return
            
        equipo_id = self.tabla_equipos.item(selected_row, 0).text()
        
        dialog = AsignarJugadorDialog(self, equipo_id)
        if dialog.exec() == QDialog.Accepted:
            self.cargar_jugadores_equipo()


class EquipoDialog(QDialog):
    """Diálogo para crear o editar equipos."""
    
    def __init__(self, parent=None, equipo_id=None):
        super().__init__(parent)
        self.equipo_id = equipo_id
        self.setWindowTitle("Editar Equipo" if equipo_id else "Nuevo Equipo")
        self.setMinimumWidth(600)
        self.init_ui()
        
        if equipo_id:
            self.cargar_datos()
            
    def init_ui(self):
        """Inicializa la interfaz del diálogo."""
        layout = QFormLayout(self)
        
        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Nombre del equipo")
        
        self.txt_curso = QLineEdit()
        self.txt_curso.setPlaceholderText("Ej: 1º ESO A")
        
        self.combo_color = QComboBox()
        colores = ["Rojo", "Azul", "Verde", "Amarillo", "Negro", "Blanco", 
                   "Naranja", "Morado", "Rosa", "Gris"]
        self.combo_color.addItems(colores)
        
        layout.addRow("Nombre:", self.txt_nombre)
        layout.addRow("Curso:", self.txt_curso)
        layout.addRow("Color:", self.combo_color)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.aceptar)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
    def cargar_datos(self):
        """Carga los datos del equipo a editar."""
        query = QSqlQuery()
        query.prepare("SELECT nombre, curso, color_camiseta FROM equipos WHERE id = ?")
        query.addBindValue(self.equipo_id)
        query.exec()
        
        if query.next():
            self.txt_nombre.setText(query.value(0))
            self.txt_curso.setText(query.value(1))
            index = self.combo_color.findText(query.value(2))
            if index >= 0:
                self.combo_color.setCurrentIndex(index)
                
    def aceptar(self):
        """Valida y guarda los datos."""
        nombre = self.txt_nombre.text().strip()
        curso = self.txt_curso.text().strip()
        color = self.combo_color.currentText()
        
        if not nombre or not curso:
            QMessageBox.warning(self, "Error", "Todos los campos son obligatorios")
            return
            
        query = QSqlQuery()
        
        if self.equipo_id:
            query.prepare("""
                UPDATE equipos 
                SET nombre = ?, curso = ?, color_camiseta = ?
                WHERE id = ?
            """)
            query.addBindValue(nombre)
            query.addBindValue(curso)
            query.addBindValue(color)
            query.addBindValue(self.equipo_id)
        else:
            query.prepare("""
                INSERT INTO equipos (nombre, curso, color_camiseta)
                VALUES (?, ?, ?)
            """)
            query.addBindValue(nombre)
            query.addBindValue(curso)
            query.addBindValue(color)
            
        if query.exec():
            self.accept()
        else:
            QMessageBox.warning(self, "Error", f"No se pudo guardar: {query.lastError().text()}")


class AsignarJugadorDialog(QDialog):
    """Diálogo para asignar jugadores a un equipo."""
    
    def __init__(self, parent=None, equipo_id=None):
        super().__init__(parent)
        self.equipo_id = equipo_id
        self.setWindowTitle("Asignar Jugador al Equipo")
        self.setMinimumSize(600, 300)
        self.init_ui()
        self.cargar_jugadores_disponibles()
        
    def init_ui(self):
        """Inicializa la interfaz del diálogo."""
        layout = QVBoxLayout(self)
        
        label = QLabel("Seleccione un jugador disponible:")
        layout.addWidget(label)
        
        self.lista_disponibles = QListWidget()
        layout.addWidget(self.lista_disponibles)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.aceptar)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
    def cargar_jugadores_disponibles(self):
        """Carga jugadores que no están en el equipo."""
        query = QSqlQuery()
        query.prepare("""
            SELECT id, nombre, posicion
            FROM participantes
            WHERE es_jugador = 1 AND activo = 1
            AND id NOT IN (
                SELECT participante_id 
                FROM equipo_participante 
                WHERE equipo_id = ?
            )
            ORDER BY nombre
        """)
        query.addBindValue(self.equipo_id)
        query.exec()
        
        while query.next():
            jugador_id = query.value(0)
            nombre = query.value(1)
            posicion = query.value(2) or "Sin posición"
            
            item_text = f"{nombre} - {posicion}"
            item = QTableWidgetItem(item_text)
            item.setData(Qt.UserRole, jugador_id)
            self.lista_disponibles.addItem(item_text)
            self.lista_disponibles.item(self.lista_disponibles.count() - 1).setData(Qt.UserRole, jugador_id)
            
    def aceptar(self):
        """Asigna el jugador seleccionado al equipo."""
        current_item = self.lista_disponibles.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Error", "Seleccione un jugador")
            return
            
        jugador_id = current_item.data(Qt.UserRole)
        
        query = QSqlQuery()
        query.prepare("""
            INSERT INTO equipo_participante (equipo_id, participante_id)
            VALUES (?, ?)
        """)
        query.addBindValue(self.equipo_id)
        query.addBindValue(jugador_id)
        
        if query.exec():
            self.accept()
        else:
            QMessageBox.warning(self, "Error", f"No se pudo asignar: {query.lastError().text()}")