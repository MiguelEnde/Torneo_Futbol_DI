"""
Controlador para la gestión de equipos.
Maneja la lógica de negocio de equipos.
"""

from PySide6.QtSql import QSqlQuery
from MODELS.equipo import Equipo
from typing import List, Optional


class EquiposController:
    """Controlador para operaciones de equipos."""
    
    @staticmethod
    def crear_equipo(nombre: str, curso: str, color: str, logo: Optional[str] = None) -> Equipo:
        """
        Crea un nuevo equipo.
        
        Args:
            nombre: Nombre del equipo
            curso: Curso del equipo
            color: Color de la camiseta
            logo: Ruta del logo (opcional)
            
        Returns:
            Equipo creado
            
        Raises:
            ValueError: Si los datos no son válidos
        """
        equipo = Equipo(nombre=nombre, curso=curso, color_camiseta=color, logo=logo)
        if equipo.guardar():
            return equipo
        raise ValueError("No se pudo crear el equipo")
    
    @staticmethod
    def actualizar_equipo(equipo_id: int, nombre: str = None, curso: str = None, 
                         color: str = None, logo: str = None) -> Optional[Equipo]:
        """
        Actualiza un equipo existente.
        
        Args:
            equipo_id: ID del equipo
            nombre: Nuevo nombre (opcional)
            curso: Nuevo curso (opcional)
            color: Nuevo color (opcional)
            logo: Nuevo logo (opcional)
            
        Returns:
            Equipo actualizado o None
        """
        equipo = Equipo.obtener_por_id(equipo_id)
        if not equipo:
            return None
        
        if nombre:
            equipo.nombre = nombre
        if curso:
            equipo.curso = curso
        if color:
            equipo.color_camiseta = color
        if logo is not None:
            equipo.logo = logo
        
        if equipo.guardar():
            return equipo
        return None
    
    @staticmethod
    def eliminar_equipo(equipo_id: int) -> bool:
        """
        Elimina un equipo.
        
        Args:
            equipo_id: ID del equipo
            
        Returns:
            True si se eliminó correctamente
        """
        equipo = Equipo.obtener_por_id(equipo_id)
        if equipo:
            return equipo.eliminar()
        return False
    
    @staticmethod
    def obtener_equipo(equipo_id: int) -> Optional[Equipo]:
        """
        Obtiene un equipo por ID.
        
        Args:
            equipo_id: ID del equipo
            
        Returns:
            Equipo o None
        """
        return Equipo.obtener_por_id(equipo_id)
    
    @staticmethod
    def obtener_todos_equipos(solo_activos: bool = True) -> List[Equipo]:
        """
        Obtiene todos los equipos.
        
        Args:
            solo_activos: Si True, solo retorna equipos activos
            
        Returns:
            Lista de equipos
        """
        return Equipo.obtener_todos(solo_activos)
    
    @staticmethod
    def asignar_jugador_a_equipo(equipo_id: int, participante_id: int) -> bool:
        """
        Asigna un jugador a un equipo.
        
        Args:
            equipo_id: ID del equipo
            participante_id: ID del participante
            
        Returns:
            True si se asignó correctamente
        """
        query = QSqlQuery()
        query.prepare("""
            INSERT OR IGNORE INTO equipo_participante (equipo_id, participante_id)
            VALUES (?, ?)
        """)
        query.addBindValue(equipo_id)
        query.addBindValue(participante_id)
        return query.exec()
    
    @staticmethod
    def desasignar_jugador_de_equipo(equipo_id: int, participante_id: int) -> bool:
        """
        Desasigna un jugador de un equipo.
        
        Args:
            equipo_id: ID del equipo
            participante_id: ID del participante
            
        Returns:
            True si se desasignó correctamente
        """
        query = QSqlQuery()
        query.prepare("""
            DELETE FROM equipo_participante 
            WHERE equipo_id = ? AND participante_id = ?
        """)
        query.addBindValue(equipo_id)
        query.addBindValue(participante_id)
        return query.exec()
    
    @staticmethod
    def obtener_jugadores_equipo(equipo_id: int) -> List[dict]:
        """
        Obtiene todos los jugadores de un equipo.
        
        Args:
            equipo_id: ID del equipo
            
        Returns:
            Lista de diccionarios con datos de jugadores
        """
        jugadores = []
        query = QSqlQuery()
        query.prepare("""
            SELECT p.id, p.nombre, p.posicion, 
                   COALESCE((SELECT COUNT(*) FROM goles WHERE participante_id = p.id), 0) as goles,
                   COALESCE((
                       SELECT SUM(CASE WHEN tipo = 'amarilla' THEN 1 ELSE 0 END) 
                       FROM tarjetas WHERE participante_id = p.id
                   ), 0) as amarillas,
                   COALESCE((
                       SELECT SUM(CASE WHEN tipo = 'roja' THEN 1 ELSE 0 END) 
                       FROM tarjetas WHERE participante_id = p.id
                   ), 0) as rojas
            FROM participantes p
            INNER JOIN equipo_participante ep ON p.id = ep.participante_id
            WHERE ep.equipo_id = ? AND p.es_jugador = 1 AND p.activo = 1
            ORDER BY p.nombre
        """)
        query.addBindValue(equipo_id)
        
        if query.exec():
            while query.next():
                jugadores.append({
                    'id': query.value(0),
                    'nombre': query.value(1),
                    'posicion': query.value(2) or 'Sin posición',
                    'goles': query.value(3) or 0,
                    'amarillas': query.value(4) or 0,
                    'rojas': query.value(5) or 0
                })
        
        return jugadores
    
    @staticmethod
    def obtener_estadisticas_equipo(equipo_id: int) -> dict:
        """
        Obtiene estadísticas completas de un equipo.
        
        Args:
            equipo_id: ID del equipo
            
        Returns:
            Diccionario con estadísticas
        """
        stats = {
            'partidos_jugados': 0,
            'partidos_ganados': 0,
            'partidos_empatados': 0,
            'partidos_perdidos': 0,
            'goles_favor': 0,
            'goles_contra': 0,
            'diferencia_goles': 0,
            'puntos': 0
        }
        
        query = QSqlQuery()
        query.prepare("""
            SELECT 
                COUNT(*) as partidos,
                SUM(CASE WHEN finalizado = 1 AND (
                    (equipo_local_id = ? AND goles_local > goles_visitante) OR
                    (equipo_visitante_id = ? AND goles_visitante > goles_local)
                ) THEN 1 ELSE 0 END) as ganados,
                SUM(CASE WHEN finalizado = 1 AND goles_local = goles_visitante THEN 1 ELSE 0 END) as empatados,
                SUM(CASE WHEN finalizado = 1 AND (
                    (equipo_local_id = ? AND goles_local < goles_visitante) OR
                    (equipo_visitante_id = ? AND goles_visitante < goles_local)
                ) THEN 1 ELSE 0 END) as perdidos,
                SUM(CASE WHEN equipo_local_id = ? THEN goles_local WHEN equipo_visitante_id = ? THEN goles_visitante ELSE 0 END) as goles_favor,
                SUM(CASE WHEN equipo_local_id = ? THEN goles_visitante WHEN equipo_visitante_id = ? THEN goles_local ELSE 0 END) as goles_contra
            FROM partidos
            WHERE (equipo_local_id = ? OR equipo_visitante_id = ?) AND finalizado = 1
        """)
        
        for _ in range(9):
            query.addBindValue(equipo_id)
        
        if query.exec() and query.next():
            stats['partidos_jugados'] = query.value(0) or 0
            stats['partidos_ganados'] = query.value(1) or 0
            stats['partidos_empatados'] = query.value(2) or 0
            stats['partidos_perdidos'] = query.value(3) or 0
            stats['goles_favor'] = query.value(4) or 0
            stats['goles_contra'] = query.value(5) or 0
            stats['diferencia_goles'] = stats['goles_favor'] - stats['goles_contra']
            stats['puntos'] = (stats['partidos_ganados'] * 3) + (stats['partidos_empatados'] * 1)
        
        return stats
