from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QLabel, QLineEdit, QComboBox, QMessageBox,
                               QDialog, QFormLayout, QDialogButtonBox,
                               QCheckBox, QDateEdit, QTabWidget, QGroupBox)
from PySide6.QtCore import Qt, QDate
from PySide6.QtSql import QSqlQuery
from CONTROLLERS.participantes_controller import ParticipantesController

class ParticipantesView(QWidget):
    """Vista principal para gestión de participantes."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.cargar_participantes()
        
    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Título
        title_label = QLabel("Gestión de Participantes")
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: #DC143C;")
        layout.addWidget(title_label)
        
        # Barra de herramientas
        toolbar_layout = QHBoxLayout()
        
        self.btn_nuevo = QPushButton("➕ Nuevo Participante")
        self.btn_nuevo.setToolTip("Registrar nuevo jugador o árbitro")
        self.btn_nuevo.clicked.connect(self.nuevo_participante)
        
        self.btn_editar = QPushButton("✏️ Editar")
        self.btn_editar.setToolTip("Editar participante seleccionado")
        self.btn_editar.clicked.connect(self.editar_participante)
        self.btn_editar.setEnabled(False)
        
        self.btn_eliminar = QPushButton("🗑️ Eliminar")
        self.btn_eliminar.setToolTip("Eliminar participante seleccionado")
        self.btn_eliminar.clicked.connect(self.eliminar_participante)
        self.btn_eliminar.setEnabled(False)
        
        self.btn_refrescar = QPushButton("🔄 Refrescar")
        self.btn_refrescar.setToolTip("Recargar lista")
        self.btn_refrescar.clicked.connect(self.cargar_participantes)
        
        toolbar_layout.addWidget(self.btn_nuevo)
        toolbar_layout.addWidget(self.btn_editar)
        toolbar_layout.addWidget(self.btn_eliminar)
        toolbar_layout.addWidget(self.btn_refrescar)
        toolbar_layout.addStretch()
        
        # Filtros
        self.combo_filtro = QComboBox()
        self.combo_filtro.addItems(["Todos", "Solo Jugadores", "Solo Árbitros"])
        self.combo_filtro.currentTextChanged.connect(self.cargar_participantes)
        toolbar_layout.addWidget(QLabel("Filtrar:"))
        toolbar_layout.addWidget(self.combo_filtro)
        
        layout.addLayout(toolbar_layout)
        
        # Pestañas
        self.tabs = QTabWidget()
        
        # Pestaña de lista
        tab_lista = QWidget()
        tab_lista_layout = QVBoxLayout(tab_lista)
        tab_lista_layout.setContentsMargins(0, 10, 0, 0)
        
        self.tabla_participantes = QTableWidget()
        self.tabla_participantes.setColumnCount(6)
        self.tabla_participantes.setHorizontalHeaderLabels([
            "ID", "Nombre", "Curso", "Tipo", "Posición", "Estadísticas"
        ])
        self.tabla_participantes.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabla_participantes.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_participantes.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla_participantes.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_participantes.hideColumn(0)
        self.tabla_participantes.itemSelectionChanged.connect(self.participante_seleccionado)
        tab_lista_layout.addWidget(self.tabla_participantes)
        
        self.tabs.addTab(tab_lista, "📋 Lista General")
        
        # Pestaña de estadísticas
        tab_stats = self.crear_tab_estadisticas()
        self.tabs.addTab(tab_stats, "📊 Estadísticas")
        
        layout.addWidget(self.tabs)
        
    def crear_tab_estadisticas(self):
        """Crea la pestaña de estadísticas."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 10, 0, 0)
        
        # Goleadores
        group_goles = QGroupBox("🏆 Máximos Goleadores")
        group_goles_layout = QVBoxLayout(group_goles)
        
        self.tabla_goleadores = QTableWidget()
        self.tabla_goleadores.setColumnCount(3)
        self.tabla_goleadores.setHorizontalHeaderLabels(["Jugador", "Equipo", "Goles"])
        self.tabla_goleadores.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla_goleadores.setEditTriggers(QTableWidget.NoEditTriggers)
        group_goles_layout.addWidget(self.tabla_goleadores)
        
        layout.addWidget(group_goles)
        
        # Tarjetas
        group_tarjetas = QGroupBox("🟨 Tarjetas 🟥")
        group_tarjetas_layout = QVBoxLayout(group_tarjetas)
        
        self.tabla_tarjetas = QTableWidget()
        self.tabla_tarjetas.setColumnCount(4)
        self.tabla_tarjetas.setHorizontalHeaderLabels([
            "Jugador", "Equipo", "Amarillas", "Rojas"
        ])
        self.tabla_tarjetas.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.tabla_tarjetas.setEditTriggers(QTableWidget.NoEditTriggers)
        group_tarjetas_layout.addWidget(self.tabla_tarjetas)
        
        layout.addWidget(group_tarjetas)
        
        return widget
        
    def cargar_participantes(self):
        """Carga los participantes desde la base de datos."""
        self.tabla_participantes.setRowCount(0)
        
        filtro = self.combo_filtro.currentText()
        
        query = QSqlQuery()
        sql = """
            SELECT p.id, p.nombre, p.curso, p.posicion, p.es_jugador, p.es_arbitro,
                   COALESCE((SELECT COUNT(*) FROM goles WHERE participante_id = p.id), 0) as goles,
                   COALESCE((SELECT COUNT(*) FROM tarjetas WHERE participante_id = p.id AND tipo = 'amarilla'), 0) as amarillas,
                   COALESCE((SELECT COUNT(*) FROM tarjetas WHERE participante_id = p.id AND tipo = 'roja'), 0) as rojas
            FROM participantes p
            WHERE p.activo = 1
        """
        
        if filtro == "Solo Jugadores":
            sql += " AND p.es_jugador = 1"
        elif filtro == "Solo Árbitros":
            sql += " AND p.es_arbitro = 1"
            
        sql += " ORDER BY p.nombre"
        
        query.exec(sql)
        
        row = 0
        while query.next():
            self.tabla_participantes.insertRow(row)
            
            # ID
            self.tabla_participantes.setItem(row, 0, QTableWidgetItem(str(query.value(0))))
            
            # Nombre
            self.tabla_participantes.setItem(row, 1, QTableWidgetItem(query.value(1)))
            
            # Curso
            self.tabla_participantes.setItem(row, 2, QTableWidgetItem(query.value(2)))
            
            # Tipo
            es_jugador = query.value(4)
            es_arbitro = query.value(5)
            tipos = []
            if es_jugador:
                tipos.append("Jugador")
            if es_arbitro:
                tipos.append("Árbitro")
            tipo_texto = ", ".join(tipos) if tipos else "N/A"
            self.tabla_participantes.setItem(row, 3, QTableWidgetItem(tipo_texto))
            
            # Posición
            posicion = query.value(3) or "N/A"
            self.tabla_participantes.setItem(row, 4, QTableWidgetItem(posicion))
            
            # Estadísticas
            goles = query.value(6)
            amarillas = query.value(7)
            rojas = query.value(8)
            stats = f"⚽ {goles} | 🟨 {amarillas} | 🟥 {rojas}"
            self.tabla_participantes.setItem(row, 5, QTableWidgetItem(stats))
            
            row += 1
            
        self.cargar_estadisticas()
        
    def cargar_estadisticas(self):
        """Carga las estadísticas en las tablas correspondientes."""
        # Goleadores
        self.tabla_goleadores.setRowCount(0)
        query = QSqlQuery()
        query.exec("""
            SELECT p.nombre, 
                   COALESCE(e.nombre, 'Sin equipo') as equipo,
                   COUNT(g.id) as total_goles
            FROM participantes p
            LEFT JOIN goles g ON p.id = g.participante_id
            LEFT JOIN equipo_participante ep ON p.id = ep.participante_id
            LEFT JOIN equipos e ON ep.equipo_id = e.id
            WHERE p.activo = 1 AND p.es_jugador = 1
            GROUP BY p.id, p.nombre, e.nombre
            ORDER BY COUNT(g.id) DESC
            LIMIT 10
        """)
        
        row = 0
        while query.next():
            self.tabla_goleadores.insertRow(row)
            self.tabla_goleadores.setItem(row, 0, QTableWidgetItem(query.value(0)))
            self.tabla_goleadores.setItem(row, 1, QTableWidgetItem(query.value(1)))
            self.tabla_goleadores.setItem(row, 2, QTableWidgetItem(str(query.value(2))))
            row += 1
            
        # Tarjetas
        self.tabla_tarjetas.setRowCount(0)
        query.exec("""
            SELECT p.nombre,
                   COALESCE(e.nombre, 'Sin equipo') as equipo,
                   SUM(CASE WHEN t.tipo = 'amarilla' THEN 1 ELSE 0 END) as amarillas,
                   SUM(CASE WHEN t.tipo = 'roja' THEN 1 ELSE 0 END) as rojas
            FROM participantes p
            LEFT JOIN tarjetas t ON p.id = t.participante_id
            LEFT JOIN equipo_participante ep ON p.id = ep.participante_id
            LEFT JOIN equipos e ON ep.equipo_id = e.id
            WHERE p.activo = 1 AND p.es_jugador = 1
            GROUP BY p.id, p.nombre, e.nombre
            ORDER BY SUM(CASE WHEN t.tipo = 'roja' THEN 1 ELSE 0 END) DESC, 
                     SUM(CASE WHEN t.tipo = 'amarilla' THEN 1 ELSE 0 END) DESC
            LIMIT 10
        """)
        
        row = 0
        while query.next():
            self.tabla_tarjetas.insertRow(row)
            self.tabla_tarjetas.setItem(row, 0, QTableWidgetItem(query.value(0)))
            self.tabla_tarjetas.setItem(row, 1, QTableWidgetItem(query.value(1)))
            self.tabla_tarjetas.setItem(row, 2, QTableWidgetItem(str(query.value(2))))
            self.tabla_tarjetas.setItem(row, 3, QTableWidgetItem(str(query.value(3))))
            row += 1
            
    def participante_seleccionado(self):
        """Maneja la selección de un participante."""
        has_selection = self.tabla_participantes.currentRow() >= 0
        self.btn_editar.setEnabled(has_selection)
        self.btn_eliminar.setEnabled(has_selection)
        
    def nuevo_participante(self):
        """Abre el diálogo para crear un nuevo participante."""
        dialog = ParticipanteDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.cargar_participantes()
            QMessageBox.information(self, "Éxito", "Participante creado correctamente")
            
    def editar_participante(self):
        """Abre el diálogo para editar el participante seleccionado."""
        selected_row = self.tabla_participantes.currentRow()
        if selected_row < 0:
            return
            
        participante_id = int(self.tabla_participantes.item(selected_row, 0).text())
        
        dialog = ParticipanteDialog(self, participante_id)
        if dialog.exec() == QDialog.Accepted:
            self.cargar_participantes()
            QMessageBox.information(self, "Éxito", "Participante actualizado correctamente")
            
    def eliminar_participante(self):
        """Elimina el participante seleccionado."""
        selected_row = self.tabla_participantes.currentRow()
        if selected_row < 0:
            return
            
        participante_id = self.tabla_participantes.item(selected_row, 0).text()
        participante_nombre = self.tabla_participantes.item(selected_row, 1).text()
        
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Está seguro de eliminar a '{participante_nombre}'?\n"
            "Esta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            query = QSqlQuery()
            query.prepare("UPDATE participantes SET activo = 0 WHERE id = ?")
            query.addBindValue(participante_id)
            
            if query.exec():
                self.cargar_participantes()
                QMessageBox.information(self, "Éxito", "Participante eliminado correctamente")
            else:
                QMessageBox.warning(self, "Error", f"No se pudo eliminar: {query.lastError().text()}")


class ParticipanteDialog(QDialog):
    """Diálogo para crear o editar participantes."""
    
    def __init__(self, parent=None, participante_id=None):
        super().__init__(parent)
        self.participante_id = participante_id
        self.setWindowTitle("Editar Participante" if participante_id else "Nuevo Participante")
        self.setMinimumWidth(450)
        self.init_ui()
        
        if participante_id:
            self.cargar_datos()
            
    def init_ui(self):
        """Inicializa la interfaz del diálogo."""
        layout = QFormLayout(self)
        
        # Nombre
        self.txt_nombre = QLineEdit()
        self.txt_nombre.setPlaceholderText("Nombre completo")
        layout.addRow("Nombre:", self.txt_nombre)
        
        # Fecha de nacimiento
        self.date_nacimiento = QDateEdit()
        self.date_nacimiento.setCalendarPopup(True)
        self.date_nacimiento.setDate(QDate.currentDate().addYears(-15))
        self.date_nacimiento.setDisplayFormat("dd/MM/yyyy")
        layout.addRow("Fecha Nacimiento:", self.date_nacimiento)
        
        # Curso
        self.txt_curso = QLineEdit()
        self.txt_curso.setPlaceholderText("Ej: 3º ESO B")
        layout.addRow("Curso:", self.txt_curso)
        
        # Tipo
        tipo_layout = QHBoxLayout()
        self.check_jugador = QCheckBox("Es Jugador")
        self.check_arbitro = QCheckBox("Es Árbitro")
        self.check_jugador.stateChanged.connect(self.actualizar_posicion)
        tipo_layout.addWidget(self.check_jugador)
        tipo_layout.addWidget(self.check_arbitro)
        layout.addRow("Tipo:", tipo_layout)
        
        # Posición (solo para jugadores)
        self.combo_posicion = QComboBox()
        posiciones = ["Portero", "Defensa", "Centrocampista", "Delantero"]
        self.combo_posicion.addItems(posiciones)
        self.combo_posicion.setEnabled(False)
        layout.addRow("Posición:", self.combo_posicion)
        
        # Goles
        self.spin_goles = QLineEdit()
        self.spin_goles.setPlaceholderText("0")
        self.spin_goles.setText("0")
        layout.addRow("Goles:", self.spin_goles)
        
        # Tarjetas Amarillas
        self.spin_amarillas = QLineEdit()
        self.spin_amarillas.setPlaceholderText("0")
        self.spin_amarillas.setText("0")
        layout.addRow("Tarjetas Amarillas:", self.spin_amarillas)
        
        # Tarjetas Rojas
        self.spin_rojas = QLineEdit()
        self.spin_rojas.setPlaceholderText("0")
        self.spin_rojas.setText("0")
        layout.addRow("Tarjetas Rojas:", self.spin_rojas)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.aceptar)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
    def actualizar_posicion(self):
        """Habilita o deshabilita el campo de posición según sea jugador."""
        self.combo_posicion.setEnabled(self.check_jugador.isChecked())
        
    def cargar_datos(self):
        """Carga los datos del participante a editar."""
        query = QSqlQuery()
        query.prepare("""
            SELECT nombre, fecha_nacimiento, curso, es_jugador, es_arbitro, posicion
            FROM participantes WHERE id = ?
        """)
        query.addBindValue(self.participante_id)
        query.exec()
        
        if query.next():
            self.txt_nombre.setText(query.value(0))
            fecha_str = query.value(1)
            if fecha_str:
                fecha = QDate.fromString(fecha_str, "yyyy-MM-dd")
                self.date_nacimiento.setDate(fecha)
            self.txt_curso.setText(query.value(2))
            self.check_jugador.setChecked(bool(query.value(3)))
            self.check_arbitro.setChecked(bool(query.value(4)))
            
            posicion = query.value(5)
            if posicion:
                index = self.combo_posicion.findText(posicion)
                if index >= 0:
                    self.combo_posicion.setCurrentIndex(index)
        
        # Cargar estadísticas de goles y tarjetas
        query_stats = QSqlQuery()
        query_stats.prepare("""
            SELECT 
                COALESCE((SELECT COUNT(*) FROM goles WHERE participante_id = ?), 0) as total_goles,
                COALESCE((SELECT COUNT(*) FROM tarjetas WHERE participante_id = ? AND tipo = 'amarilla'), 0) as amarillas,
                COALESCE((SELECT COUNT(*) FROM tarjetas WHERE participante_id = ? AND tipo = 'roja'), 0) as rojas
        """)
        query_stats.addBindValue(self.participante_id)
        query_stats.addBindValue(self.participante_id)
        query_stats.addBindValue(self.participante_id)
        query_stats.exec()
        
        if query_stats.next():
            self.spin_goles.setText(str(query_stats.value(0)))
            self.spin_amarillas.setText(str(query_stats.value(1)))
            self.spin_rojas.setText(str(query_stats.value(2)))
                    
    def aceptar(self):
        """Valida y guarda los datos."""
        nombre = self.txt_nombre.text().strip()
        fecha_nacimiento = self.date_nacimiento.date().toString("yyyy-MM-dd")
        curso = self.txt_curso.text().strip()
        es_jugador = 1 if self.check_jugador.isChecked() else 0
        es_arbitro = 1 if self.check_arbitro.isChecked() else 0
        posicion = self.combo_posicion.currentText() if es_jugador else None
        
        if not nombre or not curso:
            QMessageBox.warning(self, "Error", "Nombre y curso son obligatorios")
            return
            
        if not es_jugador and not es_arbitro:
            QMessageBox.warning(self, "Error", "Debe ser al menos jugador o árbitro")
            return
        
        # Validar que goles y tarjetas sean números
        try:
            goles = int(self.spin_goles.text())
            amarillas = int(self.spin_amarillas.text())
            rojas = int(self.spin_rojas.text())
            
            if goles < 0 or amarillas < 0 or rojas < 0:
                raise ValueError("Los valores no pueden ser negativos")
        except ValueError as e:
            QMessageBox.warning(self, "Error", f"Goles y tarjetas deben ser números positivos: {e}")
            return
            
        query = QSqlQuery()
        
        if self.participante_id:
            query.prepare("""
                UPDATE participantes 
                SET nombre = ?, fecha_nacimiento = ?, curso = ?, 
                    es_jugador = ?, es_arbitro = ?, posicion = ?
                WHERE id = ?
            """)
            query.addBindValue(nombre)
            query.addBindValue(fecha_nacimiento)
            query.addBindValue(curso)
            query.addBindValue(es_jugador)
            query.addBindValue(es_arbitro)
            query.addBindValue(posicion)
            query.addBindValue(self.participante_id)
            
            if query.exec():
                # Actualizar goles y tarjetas si es jugador
                if es_jugador:
                    self.actualizar_estadisticas(self.participante_id, goles, amarillas, rojas)
                self.accept()
            else:
                QMessageBox.warning(self, "Error", f"No se pudo guardar: {query.lastError().text()}")
        else:
            query.prepare("""
                INSERT INTO participantes (nombre, fecha_nacimiento, curso, es_jugador, es_arbitro, posicion)
                VALUES (?, ?, ?, ?, ?, ?)
            """)
            query.addBindValue(nombre)
            query.addBindValue(fecha_nacimiento)
            query.addBindValue(curso)
            query.addBindValue(es_jugador)
            query.addBindValue(es_arbitro)
            query.addBindValue(posicion)
            
            if query.exec():
                self.accept()
            else:
                QMessageBox.warning(self, "Error", f"No se pudo guardar: {query.lastError().text()}")
    
    def actualizar_estadisticas(self, participante_id, goles_target, amarillas_target, rojas_target):
        """Actualiza goles y tarjetas para que coincidan con los valores ingresados."""
        
        # Obtener goles actuales
        query_goles = QSqlQuery()
        query_goles.prepare("SELECT COUNT(*) FROM goles WHERE participante_id = ?")
        query_goles.addBindValue(participante_id)
        query_goles.exec()
        goles_actuales = 0
        if query_goles.next():
            goles_actuales = query_goles.value(0)
        
        # Agregar o eliminar goles
        if goles_target > goles_actuales:
            # Agregar goles
            for _ in range(goles_target - goles_actuales):
                insert_query = QSqlQuery()
                insert_query.prepare("INSERT INTO goles (participante_id) VALUES (?)")
                insert_query.addBindValue(participante_id)
                insert_query.exec()
        elif goles_target < goles_actuales:
            # Eliminar goles (desde el final)
            cantidad_a_eliminar = goles_actuales - goles_target
            delete_query = QSqlQuery()
            delete_query.prepare(f"DELETE FROM goles WHERE participante_id = ? LIMIT ?")
            delete_query.addBindValue(participante_id)
            delete_query.addBindValue(cantidad_a_eliminar)
            delete_query.exec()
        
        # Obtener tarjetas amarillas actuales
        query_amarillas = QSqlQuery()
        query_amarillas.prepare("SELECT COUNT(*) FROM tarjetas WHERE participante_id = ? AND tipo = 'amarilla'")
        query_amarillas.addBindValue(participante_id)
        query_amarillas.exec()
        amarillas_actuales = 0
        if query_amarillas.next():
            amarillas_actuales = query_amarillas.value(0)
        
        # Actualizar tarjetas amarillas
        if amarillas_target > amarillas_actuales:
            for _ in range(amarillas_target - amarillas_actuales):
                insert_query = QSqlQuery()
                insert_query.prepare("INSERT INTO tarjetas (participante_id, tipo) VALUES (?, 'amarilla')")
                insert_query.addBindValue(participante_id)
                insert_query.exec()
        elif amarillas_target < amarillas_actuales:
            cantidad_a_eliminar = amarillas_actuales - amarillas_target
            delete_query = QSqlQuery()
            delete_query.prepare("DELETE FROM tarjetas WHERE participante_id = ? AND tipo = 'amarilla' LIMIT ?")
            delete_query.addBindValue(participante_id)
            delete_query.addBindValue(cantidad_a_eliminar)
            delete_query.exec()
        
        # Obtener tarjetas rojas actuales
        query_rojas = QSqlQuery()
        query_rojas.prepare("SELECT COUNT(*) FROM tarjetas WHERE participante_id = ? AND tipo = 'roja'")
        query_rojas.addBindValue(participante_id)
        query_rojas.exec()
        rojas_actuales = 0
        if query_rojas.next():
            rojas_actuales = query_rojas.value(0)
        
        # Actualizar tarjetas rojas
        if rojas_target > rojas_actuales:
            for _ in range(rojas_target - rojas_actuales):
                insert_query = QSqlQuery()
                insert_query.prepare("INSERT INTO tarjetas (participante_id, tipo) VALUES (?, 'roja')")
                insert_query.addBindValue(participante_id)
                insert_query.exec()
        elif rojas_target < rojas_actuales:
            cantidad_a_eliminar = rojas_actuales - rojas_target
            delete_query = QSqlQuery()
            delete_query.prepare("DELETE FROM tarjetas WHERE participante_id = ? AND tipo = 'roja' LIMIT ?")
            delete_query.addBindValue(participante_id)
            delete_query.addBindValue(cantidad_a_eliminar)
            delete_query.exec()