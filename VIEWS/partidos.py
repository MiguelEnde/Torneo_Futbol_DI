from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                               QTableWidget, QTableWidgetItem, QHeaderView,
                               QLabel, QComboBox, QMessageBox, QDialog,
                               QFormLayout, QDialogButtonBox, QDateTimeEdit,
                               QTabWidget, QTreeWidget, QTreeWidgetItem,
                               QSpinBox, QGroupBox, QListWidget, QFileDialog)
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtSql import QSqlQuery
from CONTROLLERS.partidos_controller import PartidosController
import csv
import os

class PartidosView(QWidget):
    """Vista principal para gestión de partidos."""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.cargar_partidos()
        
    def init_ui(self):
        """Inicializa la interfaz de usuario."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Título
        title_label = QLabel("Gestión de Partidos")
        title_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: #DC143C;")
        layout.addWidget(title_label)
        
        # Barra de herramientas
        toolbar_layout = QHBoxLayout()
        
        self.btn_nuevo = QPushButton("➕ Nuevo Partido")
        self.btn_nuevo.setToolTip("Programar nuevo partido")
        self.btn_nuevo.clicked.connect(self.nuevo_partido)
        
        self.btn_resultado = QPushButton("⚽ Registrar Resultado")
        self.btn_resultado.setToolTip("Registrar resultado del partido")
        self.btn_resultado.clicked.connect(self.registrar_resultado)
        self.btn_resultado.setEnabled(False)
        
        self.btn_eliminar = QPushButton("🗑️ Eliminar")
        self.btn_eliminar.setToolTip("Eliminar partido seleccionado")
        self.btn_eliminar.clicked.connect(self.eliminar_partido)
        self.btn_eliminar.setEnabled(False)
        
        self.btn_refrescar = QPushButton("🔄 Refrescar")
        self.btn_refrescar.setToolTip("Recargar lista de partidos")
        self.btn_refrescar.clicked.connect(self.cargar_partidos)
        
        self.btn_exportar = QPushButton("📥 Exportar a CSV")
        self.btn_exportar.setToolTip("Exportar resultados a CSV")
        self.btn_exportar.clicked.connect(self.exportar_resultados)
        
        toolbar_layout.addWidget(self.btn_nuevo)
        toolbar_layout.addWidget(self.btn_resultado)
        toolbar_layout.addWidget(self.btn_eliminar)
        toolbar_layout.addWidget(self.btn_refrescar)
        toolbar_layout.addWidget(self.btn_exportar)
        toolbar_layout.addStretch()
        
        layout.addLayout(toolbar_layout)
        
        # Pestañas
        self.tabs = QTabWidget()
        
        # Pestaña de calendario
        tab_calendario = self.crear_tab_calendario()
        self.tabs.addTab(tab_calendario, "📅 Calendario")
        
        # Pestaña de eliminatorias
        tab_eliminatorias = self.crear_tab_eliminatorias()
        self.tabs.addTab(tab_eliminatorias, "🏆 Cuadro Eliminatorio")
        
        # Pestaña de resultados
        tab_resultados = self.crear_tab_resultados()
        self.tabs.addTab(tab_resultados, "📊 Resultados")
        
        layout.addWidget(self.tabs)
        
    def crear_tab_calendario(self):
        """Crea la pestaña de calendario."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 10, 0, 0)
        
        # Filtro por eliminatoria
        filtro_layout = QHBoxLayout()
        filtro_layout.addWidget(QLabel("Filtrar por:"))
        
        self.combo_filtro_eliminatoria = QComboBox()
        self.combo_filtro_eliminatoria.addItems([
            "Todas", "Octavos", "Cuartos", "Semifinal", "Final"
        ])
        self.combo_filtro_eliminatoria.currentTextChanged.connect(self.cargar_partidos)
        filtro_layout.addWidget(self.combo_filtro_eliminatoria)
        filtro_layout.addStretch()
        layout.addLayout(filtro_layout)
        
        # Tabla de partidos
        self.tabla_partidos = QTableWidget()
        self.tabla_partidos.setColumnCount(7)
        self.tabla_partidos.setHorizontalHeaderLabels([
            "ID", "Fecha/Hora", "Equipo Local", "Equipo Visitante", 
            "Árbitro", "Eliminatoria", "Estado"
        ])
        self.tabla_partidos.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.tabla_partidos.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.tabla_partidos.setSelectionBehavior(QTableWidget.SelectRows)
        self.tabla_partidos.setSelectionMode(QTableWidget.SingleSelection)
        self.tabla_partidos.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tabla_partidos.hideColumn(0)
        self.tabla_partidos.itemSelectionChanged.connect(self.partido_seleccionado)
        layout.addWidget(self.tabla_partidos)
        
        return widget
        
    def crear_tab_eliminatorias(self):
        """Crea la pestaña del cuadro de eliminatorias."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 10, 0, 0)
        
        info_label = QLabel("🏆 Cuadro de Eliminatorias del Torneo")
        info_label.setStyleSheet("font-weight: bold; font-size: 12pt; margin-bottom: 10px; color: #DC143C;")
        layout.addWidget(info_label)
        
        # Árbol de eliminatorias
        self.tree_eliminatorias = QTreeWidget()
        self.tree_eliminatorias.setHeaderLabels(["Eliminatoria", "Enfrentamientos"])
        self.tree_eliminatorias.setColumnWidth(0, 200)
        layout.addWidget(self.tree_eliminatorias)
        
        return widget
        
    def crear_tab_resultados(self):
        """Crea la pestaña de resultados."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 10, 0, 0)
        
        info_label = QLabel("📊 Partidos Finalizados")
        info_label.setStyleSheet("font-weight: bold; font-size: 12pt; margin-bottom: 10px; color: #DC143C;")
        layout.addWidget(info_label)
        
        # Tabla de resultados
        self.tabla_resultados = QTableWidget()
        self.tabla_resultados.setColumnCount(6)
        self.tabla_resultados.setHorizontalHeaderLabels([
            "Fecha", "Equipo Local", "Resultado", "Equipo Visitante", 
            "Eliminatoria", "Árbitro"
        ])
        self.tabla_resultados.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tabla_resultados.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.tabla_resultados.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.tabla_resultados)
        
        return widget
        
    def cargar_partidos(self):
        """Carga los partidos desde la base de datos."""
        self.tabla_partidos.setRowCount(0)
        
        filtro = self.combo_filtro_eliminatoria.currentText()
        
        query = QSqlQuery()
        sql = """
            SELECT p.id, p.fecha_hora, 
                   el.nombre as local, ev.nombre as visitante,
                   COALESCE(a.nombre, 'Sin asignar') as arbitro,
                   p.eliminatoria, p.finalizado,
                   p.goles_local, p.goles_visitante
            FROM partidos p
            INNER JOIN equipos el ON p.equipo_local_id = el.id
            INNER JOIN equipos ev ON p.equipo_visitante_id = ev.id
            LEFT JOIN participantes a ON p.arbitro_id = a.id
            WHERE 1=1
        """
        
        if filtro != "Todas":
            sql += f" AND p.eliminatoria = '{filtro}'"
            
        sql += " ORDER BY p.fecha_hora ASC"
        
        query.exec(sql)
        
        row = 0
        while query.next():
            self.tabla_partidos.insertRow(row)
            
            # ID
            self.tabla_partidos.setItem(row, 0, QTableWidgetItem(str(query.value(0))))
            
            # Fecha/Hora
            fecha_hora = QDateTime.fromString(query.value(1), "yyyy-MM-dd HH:mm")
            fecha_texto = fecha_hora.toString("dd/MM/yyyy HH:mm")
            self.tabla_partidos.setItem(row, 1, QTableWidgetItem(fecha_texto))
            
            # Equipos
            self.tabla_partidos.setItem(row, 2, QTableWidgetItem(query.value(2)))
            self.tabla_partidos.setItem(row, 3, QTableWidgetItem(query.value(3)))
            
            # Árbitro
            self.tabla_partidos.setItem(row, 4, QTableWidgetItem(query.value(4)))
            
            # Eliminatoria
            self.tabla_partidos.setItem(row, 5, QTableWidgetItem(query.value(5)))
            
            # Estado
            finalizado = query.value(6)
            if finalizado:
                goles_local = query.value(7)
                goles_visitante = query.value(8)
                estado_texto = f"✅ Finalizado ({goles_local}-{goles_visitante})"
            else:
                estado_texto = "⏳ Pendiente"
            self.tabla_partidos.setItem(row, 6, QTableWidgetItem(estado_texto))
            
            row += 1
            
        self.cargar_eliminatorias()
        self.cargar_resultados()
        
    def cargar_eliminatorias(self):
        """Carga el árbol de eliminatorias."""
        self.tree_eliminatorias.clear()
        
        eliminatorias = ["Octavos", "Cuartos", "Semifinal", "Final"]
        
        for eliminatoria in eliminatorias:
            item_elim = QTreeWidgetItem(self.tree_eliminatorias, [eliminatoria])
            item_elim.setExpanded(True)
            
            # Icono según eliminatoria
            if eliminatoria == "Final":
                item_elim.setText(0, "🏆 " + eliminatoria)
            elif eliminatoria == "Semifinal":
                item_elim.setText(0, "🥈 " + eliminatoria)
            else:
                item_elim.setText(0, "⚽ " + eliminatoria)
            
            # Cargar partidos de esta eliminatoria
            query = QSqlQuery()
            query.prepare("""
                SELECT el.nombre, ev.nombre, p.goles_local, p.goles_visitante, p.finalizado
                FROM partidos p
                INNER JOIN equipos el ON p.equipo_local_id = el.id
                INNER JOIN equipos ev ON p.equipo_visitante_id = ev.id
                WHERE p.eliminatoria = ?
                ORDER BY p.fecha_hora
            """)
            query.addBindValue(eliminatoria)
            query.exec()
            
            contador = 0
            while query.next():
                contador += 1
                local = query.value(0)
                visitante = query.value(1)
                goles_l = query.value(2)
                goles_v = query.value(3)
                finalizado = query.value(4)
                
                if finalizado:
                    ganador = local if goles_l > goles_v else visitante
                    partido_texto = f"{local} {goles_l} - {goles_v} {visitante} (Gana: {ganador})"
                else:
                    partido_texto = f"{local} vs {visitante}"
                    
                QTreeWidgetItem(item_elim, [partido_texto])
            
            if contador == 0:
                QTreeWidgetItem(item_elim, ["No hay partidos programados"])
                
    def cargar_resultados(self):
        """Carga la tabla de resultados."""
        self.tabla_resultados.setRowCount(0)
        
        query = QSqlQuery()
        query.exec("""
            SELECT p.fecha_hora, el.nombre, p.goles_local, p.goles_visitante,
                   ev.nombre, p.eliminatoria, COALESCE(a.nombre, 'Sin asignar')
            FROM partidos p
            INNER JOIN equipos el ON p.equipo_local_id = el.id
            INNER JOIN equipos ev ON p.equipo_visitante_id = ev.id
            LEFT JOIN participantes a ON p.arbitro_id = a.id
            WHERE p.finalizado = 1
            ORDER BY p.fecha_hora DESC
        """)
        
        row = 0
        while query.next():
            self.tabla_resultados.insertRow(row)
            
            # Fecha
            fecha_hora = QDateTime.fromString(query.value(0), "yyyy-MM-dd HH:mm")
            fecha_texto = fecha_hora.toString("dd/MM/yyyy")
            self.tabla_resultados.setItem(row, 0, QTableWidgetItem(fecha_texto))
            
            # Local
            self.tabla_resultados.setItem(row, 1, QTableWidgetItem(query.value(1)))
            
            # Resultado
            resultado = f"{query.value(2)} - {query.value(3)}"
            self.tabla_resultados.setItem(row, 2, QTableWidgetItem(resultado))
            
            # Visitante
            self.tabla_resultados.setItem(row, 3, QTableWidgetItem(query.value(4)))
            
            # Eliminatoria
            self.tabla_resultados.setItem(row, 4, QTableWidgetItem(query.value(5)))
            
            # Árbitro
            self.tabla_resultados.setItem(row, 5, QTableWidgetItem(query.value(6)))
            
            row += 1
            
    def partido_seleccionado(self):
        """Maneja la selección de un partido."""
        has_selection = self.tabla_partidos.currentRow() >= 0
        self.btn_resultado.setEnabled(has_selection)
        self.btn_eliminar.setEnabled(has_selection)
        
    def nuevo_partido(self):
        """Abre el diálogo para crear un nuevo partido."""
        dialog = PartidoDialog(self)
        if dialog.exec() == QDialog.Accepted:
            self.cargar_partidos()
            QMessageBox.information(self, "Éxito", "Partido creado correctamente")
            
    def registrar_resultado(self):
        """Abre el diálogo para registrar el resultado del partido."""
        selected_row = self.tabla_partidos.currentRow()
        if selected_row < 0:
            return
            
        partido_id = int(self.tabla_partidos.item(selected_row, 0).text())
        
        dialog = ResultadoDialog(self, partido_id)
        if dialog.exec() == QDialog.Accepted:
            self.cargar_partidos()
            QMessageBox.information(self, "Éxito", "Resultado registrado correctamente")
            
    def eliminar_partido(self):
        """Elimina el partido seleccionado."""
        selected_row = self.tabla_partidos.currentRow()
        if selected_row < 0:
            return
            
        partido_id = self.tabla_partidos.item(selected_row, 0).text()
        local = self.tabla_partidos.item(selected_row, 2).text()
        visitante = self.tabla_partidos.item(selected_row, 3).text()
        
        reply = QMessageBox.question(
            self,
            "Confirmar eliminación",
            f"¿Está seguro de eliminar el partido '{local} vs {visitante}'?\n"
            "Esta acción no se puede deshacer.",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            query = QSqlQuery()
            query.prepare("DELETE FROM partidos WHERE id = ?")
            query.addBindValue(partido_id)
            
            if query.exec():
                self.cargar_partidos()
                QMessageBox.information(self, "Éxito", "Partido eliminado correctamente")
            else:
                QMessageBox.warning(self, "Error", f"No se pudo eliminar: {query.lastError().text()}")

    def exportar_resultados(self):
        """Exporta los resultados de los partidos a un archivo CSV."""
        # Diálogo para seleccionar ubicación
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar resultados como...",
            os.path.expanduser("~\\Desktop\\resultados.csv"),
            "CSV Files (*.csv);;All Files (*.*)"
        )
        
        if not file_path:
            return
        
        try:
            query = QSqlQuery()
            query.exec("""
                SELECT 
                    p.id,
                    e1.nombre as equipo_local,
                    e2.nombre as equipo_visitante,
                    p.goles_local,
                    p.goles_visitante,
                    p.eliminatoria,
                    p.fecha_hora,
                    CASE WHEN p.finalizado = 1 THEN 'Finalizado' ELSE 'Pendiente' END as estado
                FROM partidos p
                INNER JOIN equipos e1 ON p.equipo_local_id = e1.id
                INNER JOIN equipos e2 ON p.equipo_visitante_id = e2.id
                ORDER BY p.fecha_hora DESC
            """)
            
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    "ID", "Equipo Local", "Equipo Visitante", 
                    "Goles Local", "Goles Visitante", "Eliminatoria", 
                    "Fecha/Hora", "Estado"
                ])
                
                while query.next():
                    writer.writerow([
                        query.value(0),
                        query.value(1),
                        query.value(2),
                        query.value(3),
                        query.value(4),
                        query.value(5),
                        query.value(6),
                        query.value(7)
                    ])
            
            QMessageBox.information(
                self,
                "Éxito",
                f"Resultados exportados correctamente a:\n{file_path}"
            )
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"No se pudo exportar los resultados:\n{str(e)}"
            )


class PartidoDialog(QDialog):
    """Diálogo para crear partidos."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Nuevo Partido")
        self.setMinimumWidth(500)
        self.init_ui()
        
    def init_ui(self):
        """Inicializa la interfaz del diálogo."""
        layout = QFormLayout(self)
        
        # Equipo local
        self.combo_local = QComboBox()
        self.cargar_equipos(self.combo_local)
        layout.addRow("Equipo Local:", self.combo_local)
        
        # Equipo visitante
        self.combo_visitante = QComboBox()
        self.cargar_equipos(self.combo_visitante)
        layout.addRow("Equipo Visitante:", self.combo_visitante)
        
        # Árbitro
        self.combo_arbitro = QComboBox()
        self.cargar_arbitros()
        layout.addRow("Árbitro:", self.combo_arbitro)
        
        # Fecha y hora
        self.datetime_partido = QDateTimeEdit()
        self.datetime_partido.setCalendarPopup(True)
        self.datetime_partido.setDateTime(QDateTime.currentDateTime())
        self.datetime_partido.setDisplayFormat("dd/MM/yyyy HH:mm")
        layout.addRow("Fecha y Hora:", self.datetime_partido)
        
        # Eliminatoria
        self.combo_eliminatoria = QComboBox()
        self.combo_eliminatoria.addItems(["Octavos", "Cuartos", "Semifinal", "Final"])
        layout.addRow("Eliminatoria:", self.combo_eliminatoria)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.aceptar)
        buttons.rejected.connect(self.reject)
        layout.addRow(buttons)
        
    def cargar_equipos(self, combo):
        """Carga los equipos en el combo box."""
        query = QSqlQuery()
        query.exec("SELECT id, nombre FROM equipos ORDER BY nombre")
        
        while query.next():
            combo.addItem(query.value(1), query.value(0))
            
    def cargar_arbitros(self):
        """Carga los árbitros en el combo box."""
        self.combo_arbitro.addItem("Sin asignar", None)
        
        query = QSqlQuery()
        query.exec("""
            SELECT id, nombre FROM participantes 
            WHERE es_arbitro = 1 AND activo = 1 
            ORDER BY nombre
        """)
        
        while query.next():
            self.combo_arbitro.addItem(query.value(1), query.value(0))
            
    def aceptar(self):
        """Valida y guarda los datos."""
        local_id = self.combo_local.currentData()
        visitante_id = self.combo_visitante.currentData()
        
        if local_id == visitante_id:
            QMessageBox.warning(self, "Error", "Debe seleccionar equipos diferentes")
            return
            
        arbitro_id = self.combo_arbitro.currentData()
        fecha_hora = self.datetime_partido.dateTime().toString("yyyy-MM-dd HH:mm")
        eliminatoria = self.combo_eliminatoria.currentText()
        
        query = QSqlQuery()
        query.prepare("""
            INSERT INTO partidos (equipo_local_id, equipo_visitante_id, arbitro_id, fecha_hora, eliminatoria)
            VALUES (?, ?, ?, ?, ?)
        """)
        query.addBindValue(local_id)
        query.addBindValue(visitante_id)
        query.addBindValue(arbitro_id)
        query.addBindValue(fecha_hora)
        query.addBindValue(eliminatoria)
        
        if query.exec():
            self.accept()
        else:
            QMessageBox.warning(self, "Error", f"No se pudo guardar: {query.lastError().text()}")


class ResultadoDialog(QDialog):
    """Diálogo para registrar resultados de partidos."""
    
    def __init__(self, parent=None, partido_id=None):
        super().__init__(parent)
        self.partido_id = partido_id
        self.setWindowTitle("Registrar Resultado")
        self.setMinimumWidth(400)
        self.init_ui()
        self.cargar_datos_partido()
        
    def init_ui(self):
        """Inicializa la interfaz del diálogo."""
        layout = QVBoxLayout(self)
        
        # Info del partido
        self.label_info = QLabel()
        self.label_info.setStyleSheet("font-weight: bold; font-size: 11pt; padding: 10px;")
        layout.addWidget(self.label_info)
        
        # Formulario de goles
        form_layout = QFormLayout()
        
        self.spin_goles_local = QSpinBox()
        self.spin_goles_local.setMinimum(0)
        self.spin_goles_local.setMaximum(20)
        form_layout.addRow("Goles Local:", self.spin_goles_local)
        
        self.spin_goles_visitante = QSpinBox()
        self.spin_goles_visitante.setMinimum(0)
        self.spin_goles_visitante.setMaximum(20)
        form_layout.addRow("Goles Visitante:", self.spin_goles_visitante)
        
        layout.addLayout(form_layout)
        
        # Botones
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.aceptar)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
    def cargar_datos_partido(self):
        """Carga los datos del partido."""
        query = QSqlQuery()
        query.prepare("""
            SELECT el.nombre, ev.nombre, p.goles_local, p.goles_visitante
            FROM partidos p
            INNER JOIN equipos el ON p.equipo_local_id = el.id
            INNER JOIN equipos ev ON p.equipo_visitante_id = ev.id
            WHERE p.id = ?
        """)
        query.addBindValue(self.partido_id)
        query.exec()
        
        if query.next():
            local = query.value(0)
            visitante = query.value(1)
            goles_l = query.value(2)
            goles_v = query.value(3)
            
            self.label_info.setText(f"⚽ {local} vs {visitante}")
            self.spin_goles_local.setValue(goles_l)
            self.spin_goles_visitante.setValue(goles_v)
            
    def aceptar(self):
        """Guarda el resultado."""
        goles_local = self.spin_goles_local.value()
        goles_visitante = self.spin_goles_visitante.value()
        
        query = QSqlQuery()
        query.prepare("""
            UPDATE partidos 
            SET goles_local = ?, goles_visitante = ?, finalizado = 1
            WHERE id = ?
        """)
        query.addBindValue(goles_local)
        query.addBindValue(goles_visitante)
        query.addBindValue(self.partido_id)
        
        if query.exec():
            self.accept()
        else:
            QMessageBox.warning(self, "Error", f"No se pudo guardar: {query.lastError().text()}")