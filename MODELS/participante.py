"""Clase que representa un participante (jugador o árbitro) y sus operaciones relacionadas con la base de datos."""

from dataclasses import dataclass
from typing import Optional
from datetime import date
from PySide6.QtSql import QSqlQuery


@dataclass
class Participante:
    """Clase que representa un participante (jugador o árbitro)."""
    
    id: Optional[int] = None
    nombre: str = ""
    fecha_nacimiento: str = ""  # Formato: yyyy-MM-dd
    curso: str = ""
    es_jugador: int = 0
    es_arbitro: int = 0
    posicion: Optional[str] = None
    activo: int = 1
    
    def __post_init__(self):
        """Validaciones después de la inicialización."""
        if not self.nombre or not self.fecha_nacimiento or not self.curso:
            raise ValueError("Nombre, fecha de nacimiento y curso son obligatorios")
        if not (self.es_jugador or self.es_arbitro):
            raise ValueError("Un participante debe ser jugador, árbitro o ambos")
    
    def guardar(self) -> bool:
        """
        Guarda el participante en la base de datos.
        
        Returns:
            bool: True si se guardó correctamente
        """
        query = QSqlQuery()
        
        try:
            if self.id:
                # Actualizar
                query.prepare("""
                    UPDATE participantes 
                    SET nombre = ?, fecha_nacimiento = ?, curso = ?, 
                        es_jugador = ?, es_arbitro = ?, posicion = ?
                    WHERE id = ?
                """)
                query.addBindValue(self.nombre)
                query.addBindValue(self.fecha_nacimiento)
                query.addBindValue(self.curso)
                query.addBindValue(self.es_jugador)
                query.addBindValue(self.es_arbitro)
                query.addBindValue(self.posicion)
                query.addBindValue(self.id)
            else:
                # Crear
                query.prepare("""
                    INSERT INTO participantes 
                    (nombre, fecha_nacimiento, curso, es_jugador, es_arbitro, posicion)
                    VALUES (?, ?, ?, ?, ?, ?)
                """)
                query.addBindValue(self.nombre)
                query.addBindValue(self.fecha_nacimiento)
                query.addBindValue(self.curso)
                query.addBindValue(self.es_jugador)
                query.addBindValue(self.es_arbitro)
                query.addBindValue(self.posicion)
            
            if query.exec():
                if not self.id:
                    self.id = query.lastInsertId()
                return True
            return False
        except Exception as e:
            print(f"Error al guardar participante: {e}")
            return False
    
    def eliminar(self) -> bool:
        """
        Elimina el participante (soft delete).
        
        Returns:
            bool: True si se eliminó correctamente
        """
        if not self.id:
            return False
        
        query = QSqlQuery()
        query.prepare("UPDATE participantes SET activo = 0 WHERE id = ?")
        query.addBindValue(self.id)
        return query.exec()
    
    def asignar_equipo(self, equipo_id: int) -> bool:
        """
        Asigna el participante a un equipo.
        
        Args:
            equipo_id: ID del equipo
            
        Returns:
            bool: True si se asignó correctamente
        """
        if not self.id or not self.es_jugador:
            return False
        
        query = QSqlQuery()
        query.prepare("""
            INSERT OR IGNORE INTO equipo_participante (equipo_id, participante_id)
            VALUES (?, ?)
        """)
        query.addBindValue(equipo_id)
        query.addBindValue(self.id)
        return query.exec()
    
    def desasignar_equipo(self, equipo_id: int) -> bool:
        """
        Desasigna el participante de un equipo.
        
        Args:
            equipo_id: ID del equipo
            
        Returns:
            bool: True si se desasignó correctamente
        """
        if not self.id:
            return False
        
        query = QSqlQuery()
        query.prepare("""
            DELETE FROM equipo_participante 
            WHERE equipo_id = ? AND participante_id = ?
        """)
        query.addBindValue(equipo_id)
        query.addBindValue(self.id)
        return query.exec()
    
    def obtener_goles(self) -> int:
        """
        Obtiene el total de goles marcados.
        
        Returns:
            int: Número de goles
        """
        query = QSqlQuery()
        query.prepare("SELECT COUNT(*) FROM goles WHERE participante_id = ?")
        query.addBindValue(self.id)
        
        if query.exec() and query.next():
            return query.value(0) or 0
        return 0
    
    def obtener_tarjetas(self) -> dict:
        """
        Obtiene el conteo de tarjetas (amarillas y rojas).
        
        Returns:
            dict: {'amarillas': count, 'rojas': count}
        """
        query = QSqlQuery()
        query.prepare("""
            SELECT tipo, COUNT(*) FROM tarjetas 
            WHERE participante_id = ?
            GROUP BY tipo
        """)
        query.addBindValue(self.id)
        
        resultado = {'amarillas': 0, 'rojas': 0}
        if query.exec():
            while query.next():
                tipo = query.value(0)
                count = query.value(1) or 0
                if tipo == 'amarilla':
                    resultado['amarillas'] = count
                elif tipo == 'roja':
                    resultado['rojas'] = count
        
        return resultado
    
    @staticmethod
    def obtener_por_id(participante_id: int) -> Optional['Participante']:
        """
        Obtiene un participante por su ID.
        
        Args:
            participante_id: ID del participante
            
        Returns:
            Participante o None
        """
        query = QSqlQuery()
        query.prepare("""
            SELECT id, nombre, fecha_nacimiento, curso, es_jugador, es_arbitro, posicion, activo
            FROM participantes WHERE id = ?
        """)
        query.addBindValue(participante_id)
        
        if query.exec() and query.next():
            return Participante(
                id=query.value(0),
                nombre=query.value(1),
                fecha_nacimiento=query.value(2),
                curso=query.value(3),
                es_jugador=query.value(4),
                es_arbitro=query.value(5),
                posicion=query.value(6),
                activo=query.value(7)
            )
        return None
    
    @staticmethod
    def obtener_todos(filtro: str = "todos", solo_activos: bool = True) -> list['Participante']:
        """
        Obtiene todos los participantes con filtro opcional.
        
        Args:
            filtro: 'todos', 'jugadores', 'arbitros'
            solo_activos: Si True, solo retorna participantes activos
            
        Returns:
            Lista de Participante
        """
        participantes = []
        query = QSqlQuery()
        
        sql = "SELECT id, nombre, fecha_nacimiento, curso, es_jugador, es_arbitro, posicion, activo FROM participantes WHERE 1=1"
        
        if filtro == "jugadores":
            sql += " AND es_jugador = 1"
        elif filtro == "arbitros":
            sql += " AND es_arbitro = 1"
        
        if solo_activos:
            sql += " AND activo = 1"
        
        sql += " ORDER BY nombre"
        
        if query.exec(sql):
            while query.next():
                participantes.append(Participante(
                    id=query.value(0),
                    nombre=query.value(1),
                    fecha_nacimiento=query.value(2),
                    curso=query.value(3),
                    es_jugador=query.value(4),
                    es_arbitro=query.value(5),
                    posicion=query.value(6),
                    activo=query.value(7)
                ))
        
        return participantes
