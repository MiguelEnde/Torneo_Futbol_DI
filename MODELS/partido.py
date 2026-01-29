"""
Modelo de datos para Partidos.
Define la estructura de un partido en el torneo.
"""

from dataclasses import dataclass
from typing import Optional, List, Tuple
from PySide6.QtSql import QSqlQuery


@dataclass
class Partido:
    """Clase que representa un partido del torneo."""
    
    id: Optional[int] = None
    equipo_local_id: int = 0
    equipo_visitante_id: int = 0
    arbitro_id: Optional[int] = None
    fecha_hora: str = ""  # Formato: yyyy-MM-dd HH:mm
    eliminatoria: str = ""
    goles_local: int = 0
    goles_visitante: int = 0
    finalizado: int = 0
    
    def __post_init__(self):
        """Validaciones después de la inicialización."""
        if not self.fecha_hora or not self.eliminatoria:
            raise ValueError("Fecha/hora y eliminatoria son obligatorios")
        if self.equipo_local_id == self.equipo_visitante_id:
            raise ValueError("Los equipos deben ser diferentes")
        if self.eliminatoria not in ["Octavos", "Cuartos", "Semifinal", "Final"]:
            raise ValueError("Eliminatoria no válida")
    
    def guardar(self) -> bool:
        """
        Guarda el partido en la base de datos.
        
        Returns:
            bool: True si se guardó correctamente
        """
        query = QSqlQuery()
        
        try:
            if self.id:
                # Actualizar
                query.prepare("""
                    UPDATE partidos 
                    SET equipo_local_id = ?, equipo_visitante_id = ?, arbitro_id = ?, 
                        fecha_hora = ?, eliminatoria = ?, goles_local = ?, 
                        goles_visitante = ?, finalizado = ?
                    WHERE id = ?
                """)
                query.addBindValue(self.equipo_local_id)
                query.addBindValue(self.equipo_visitante_id)
                query.addBindValue(self.arbitro_id)
                query.addBindValue(self.fecha_hora)
                query.addBindValue(self.eliminatoria)
                query.addBindValue(self.goles_local)
                query.addBindValue(self.goles_visitante)
                query.addBindValue(self.finalizado)
                query.addBindValue(self.id)
            else:
                # Crear
                query.prepare("""
                    INSERT INTO partidos 
                    (equipo_local_id, equipo_visitante_id, arbitro_id, fecha_hora, eliminatoria)
                    VALUES (?, ?, ?, ?, ?)
                """)
                query.addBindValue(self.equipo_local_id)
                query.addBindValue(self.equipo_visitante_id)
                query.addBindValue(self.arbitro_id)
                query.addBindValue(self.fecha_hora)
                query.addBindValue(self.eliminatoria)
            
            if query.exec():
                if not self.id:
                    self.id = query.lastInsertId()
                return True
            return False
        except Exception as e:
            print(f"Error al guardar partido: {e}")
            return False
    
    def eliminar(self) -> bool:
        """
        Elimina el partido de la base de datos.
        
        Returns:
            bool: True si se eliminó correctamente
        """
        if not self.id:
            return False
        
        query = QSqlQuery()
        query.prepare("DELETE FROM partidos WHERE id = ?")
        query.addBindValue(self.id)
        return query.exec()
    
    def registrar_gol(self, participante_id: int, minuto: int) -> bool:
        """
        Registra un gol en el partido.
        
        Args:
            participante_id: ID del jugador que marcó
            minuto: Minuto del gol
            
        Returns:
            bool: True si se registró correctamente
        """
        if not self.id:
            return False
        
        query = QSqlQuery()
        query.prepare("""
            INSERT INTO goles (partido_id, participante_id, minuto)
            VALUES (?, ?, ?)
        """)
        query.addBindValue(self.id)
        query.addBindValue(participante_id)
        query.addBindValue(minuto)
        
        if query.exec():
            # Actualizar conteo de goles
            self._actualizar_goles()
            return True
        return False
    
    def registrar_tarjeta(self, participante_id: int, tipo: str, minuto: int) -> bool:
        """
        Registra una tarjeta en el partido.
        
        Args:
            participante_id: ID del jugador
            tipo: 'amarilla' o 'roja'
            minuto: Minuto de la tarjeta
            
        Returns:
            bool: True si se registró correctamente
        """
        if not self.id or tipo not in ['amarilla', 'roja']:
            return False
        
        query = QSqlQuery()
        query.prepare("""
            INSERT INTO tarjetas (partido_id, participante_id, tipo, minuto)
            VALUES (?, ?, ?, ?)
        """)
        query.addBindValue(self.id)
        query.addBindValue(participante_id)
        query.addBindValue(tipo)
        query.addBindValue(minuto)
        
        return query.exec()
    
    def finalizar(self, goles_local: int, goles_visitante: int) -> bool:
        """
        Finaliza el partido con el resultado.
        
        Args:
            goles_local: Goles del equipo local
            goles_visitante: Goles del equipo visitante
            
        Returns:
            bool: True si se finalizó correctamente
        """
        if not self.id:
            return False
        
        self.goles_local = goles_local
        self.goles_visitante = goles_visitante
        self.finalizado = 1
        
        return self.guardar()
    
    def _actualizar_goles(self):
        """Actualiza el conteo de goles del partido."""
        if not self.id:
            return
        
        query = QSqlQuery()
        query.prepare("""
            SELECT ep.equipo_id, COUNT(g.id)
            FROM goles g
            INNER JOIN equipo_participante ep ON g.participante_id = ep.participante_id
            INNER JOIN partidos p ON g.partido_id = p.id
            WHERE g.partido_id = ? 
            GROUP BY ep.equipo_id
        """)
        query.addBindValue(self.id)
        
        if query.exec():
            while query.next():
                equipo_id = query.value(0)
                count = query.value(1) or 0
                
                # Determinar si es local o visitante
                if equipo_id == self.equipo_local_id:
                    self.goles_local = count
                elif equipo_id == self.equipo_visitante_id:
                    self.goles_visitante = count
    
    def obtener_goles_por_equipo(self) -> Tuple[int, int]:
        """
        Obtiene los goles de cada equipo.
        
        Returns:
            Tupla: (goles_local, goles_visitante)
        """
        self._actualizar_goles()
        return (self.goles_local, self.goles_visitante)
    
    def obtener_ganador(self) -> Optional[int]:
        """
        Determina el ganador del partido.
        
        Returns:
            ID del equipo ganador, None si hay empate o no está finalizado
        """
        if not self.finalizado:
            return None
        
        if self.goles_local > self.goles_visitante:
            return self.equipo_local_id
        elif self.goles_visitante > self.goles_local:
            return self.equipo_visitante_id
        
        return None  # Empate
    
    @staticmethod
    def obtener_por_id(partido_id: int) -> Optional['Partido']:
        """
        Obtiene un partido por su ID.
        
        Args:
            partido_id: ID del partido
            
        Returns:
            Partido o None
        """
        query = QSqlQuery()
        query.prepare("""
            SELECT id, equipo_local_id, equipo_visitante_id, arbitro_id, 
                   fecha_hora, eliminatoria, goles_local, goles_visitante, finalizado
            FROM partidos WHERE id = ?
        """)
        query.addBindValue(partido_id)
        
        if query.exec() and query.next():
            return Partido(
                id=query.value(0),
                equipo_local_id=query.value(1),
                equipo_visitante_id=query.value(2),
                arbitro_id=query.value(3),
                fecha_hora=query.value(4),
                eliminatoria=query.value(5),
                goles_local=query.value(6),
                goles_visitante=query.value(7),
                finalizado=query.value(8)
            )
        return None
    
    @staticmethod
    def obtener_todos(eliminatoria: str = "", solo_pendientes: bool = False) -> list['Partido']:
        """
        Obtiene todos los partidos con filtros opcionales.
        
        Args:
            eliminatoria: Filtrar por eliminatoria ('', 'Octavos', 'Cuartos', 'Semifinal', 'Final')
            solo_pendientes: Si True, solo retorna partidos no finalizados
            
        Returns:
            Lista de Partido
        """
        partidos = []
        query = QSqlQuery()
        
        sql = """
            SELECT id, equipo_local_id, equipo_visitante_id, arbitro_id, 
                   fecha_hora, eliminatoria, goles_local, goles_visitante, finalizado
            FROM partidos WHERE 1=1
        """
        
        if eliminatoria:
            sql += f" AND eliminatoria = '{eliminatoria}'"
        
        if solo_pendientes:
            sql += " AND finalizado = 0"
        
        sql += " ORDER BY fecha_hora ASC"
        
        if query.exec(sql):
            while query.next():
                partidos.append(Partido(
                    id=query.value(0),
                    equipo_local_id=query.value(1),
                    equipo_visitante_id=query.value(2),
                    arbitro_id=query.value(3),
                    fecha_hora=query.value(4),
                    eliminatoria=query.value(5),
                    goles_local=query.value(6),
                    goles_visitante=query.value(7),
                    finalizado=query.value(8)
                ))
        
        return partidos
