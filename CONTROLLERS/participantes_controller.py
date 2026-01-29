"""
Controlador para la gestión de participantes (jugadores y árbitros).
Maneja la lógica de negocio de participantes.
"""

from PySide6.QtSql import QSqlQuery
from MODELS.participante import Participante
from typing import List, Optional


class ParticipantesController:
    """Controlador para operaciones de participantes."""
    
    @staticmethod
    def crear_participante(nombre: str, fecha_nacimiento: str, curso: str,
                          es_jugador: bool = False, es_arbitro: bool = False,
                          posicion: Optional[str] = None) -> Participante:
        """
        Crea un nuevo participante.
        
        Args:
            nombre: Nombre del participante
            fecha_nacimiento: Fecha en formato yyyy-MM-dd
            curso: Curso del participante
            es_jugador: Si es jugador
            es_arbitro: Si es árbitro
            posicion: Posición del jugador (opcional)
            
        Returns:
            Participante creado
            
        Raises:
            ValueError: Si los datos no son válidos
        """
        participante = Participante(
            nombre=nombre,
            fecha_nacimiento=fecha_nacimiento,
            curso=curso,
            es_jugador=1 if es_jugador else 0,
            es_arbitro=1 if es_arbitro else 0,
            posicion=posicion
        )
        if participante.guardar():
            return participante
        raise ValueError("No se pudo crear el participante")
    
    @staticmethod
    def actualizar_participante(participante_id: int, nombre: str = None,
                               fecha_nacimiento: str = None, curso: str = None,
                               es_jugador: bool = None, es_arbitro: bool = None,
                               posicion: str = None) -> Optional[Participante]:
        """
        Actualiza un participante existente.
        
        Args:
            participante_id: ID del participante
            nombre: Nuevo nombre (opcional)
            fecha_nacimiento: Nueva fecha (opcional)
            curso: Nuevo curso (opcional)
            es_jugador: Nuevo estado (opcional)
            es_arbitro: Nuevo estado (opcional)
            posicion: Nueva posición (opcional)
            
        Returns:
            Participante actualizado o None
        """
        participante = Participante.obtener_por_id(participante_id)
        if not participante:
            return None
        
        if nombre:
            participante.nombre = nombre
        if fecha_nacimiento:
            participante.fecha_nacimiento = fecha_nacimiento
        if curso:
            participante.curso = curso
        if es_jugador is not None:
            participante.es_jugador = 1 if es_jugador else 0
        if es_arbitro is not None:
            participante.es_arbitro = 1 if es_arbitro else 0
        if posicion is not None:
            participante.posicion = posicion
        
        if participante.guardar():
            return participante
        return None
    
    @staticmethod
    def eliminar_participante(participante_id: int) -> bool:
        """
        Elimina un participante.
        
        Args:
            participante_id: ID del participante
            
        Returns:
            True si se eliminó correctamente
        """
        participante = Participante.obtener_por_id(participante_id)
        if participante:
            return participante.eliminar()
        return False
    
    @staticmethod
    def obtener_participante(participante_id: int) -> Optional[Participante]:
        """
        Obtiene un participante por ID.
        
        Args:
            participante_id: ID del participante
            
        Returns:
            Participante o None
        """
        return Participante.obtener_por_id(participante_id)
    
    @staticmethod
    def obtener_todos_participantes(filtro: str = "todos", solo_activos: bool = True) -> List[Participante]:
        """
        Obtiene todos los participantes.
        
        Args:
            filtro: 'todos', 'jugadores', 'arbitros'
            solo_activos: Si True, solo retorna participantes activos
            
        Returns:
            Lista de participantes
        """
        return Participante.obtener_todos(filtro, solo_activos)
    
    @staticmethod
    def obtener_estadisticas_participante(participante_id: int) -> dict:
        """
        Obtiene estadísticas de un participante.
        
        Args:
            participante_id: ID del participante
            
        Returns:
            Diccionario con estadísticas
        """
        participante = Participante.obtener_por_id(participante_id)
        if not participante:
            return {}
        
        stats = {
            'id': participante_id,
            'nombre': participante.nombre,
            'goles': participante.obtener_goles(),
            'tarjetas': participante.obtener_tarjetas()
        }
        
        # Obtener equipos
        query = QSqlQuery()
        query.prepare("""
            SELECT e.id, e.nombre
            FROM equipos e
            INNER JOIN equipo_participante ep ON e.id = ep.equipo_id
            WHERE ep.participante_id = ? AND e.activo = 1
        """)
        query.addBindValue(participante_id)
        
        equipos = []
        if query.exec():
            while query.next():
                equipos.append({
                    'id': query.value(0),
                    'nombre': query.value(1)
                })
        
        stats['equipos'] = equipos
        return stats
    
    @staticmethod
    def obtener_maximos_goleadores(limite: int = 10) -> List[dict]:
        """
        Obtiene los máximos goleadores del torneo.
        
        Args:
            limite: Número máximo de goleadores a retornar
            
        Returns:
            Lista de diccionarios con datos de goleadores
        """
        goleadores = []
        query = QSqlQuery()
        query.prepare("""
            SELECT p.id, p.nombre, e.nombre, COUNT(g.id) as goles
            FROM participantes p
            LEFT JOIN equipo_participante ep ON p.id = ep.participante_id
            LEFT JOIN equipos e ON ep.equipo_id = e.id
            LEFT JOIN goles g ON p.id = g.participante_id
            WHERE p.es_jugador = 1 AND p.activo = 1
            GROUP BY p.id, p.nombre, e.nombre
            ORDER BY goles DESC
            LIMIT ?
        """)
        query.addBindValue(limite)
        
        if query.exec():
            while query.next():
                goleadores.append({
                    'id': query.value(0),
                    'nombre': query.value(1),
                    'equipo': query.value(2) or 'Sin equipo',
                    'goles': query.value(3) or 0
                })
        
        return goleadores
    
    @staticmethod
    def obtener_mas_tarjetados(limite: int = 10) -> List[dict]:
        """
        Obtiene los jugadores más tarjetados del torneo.
        
        Args:
            limite: Número máximo de jugadores a retornar
            
        Returns:
            Lista de diccionarios con datos de tarjetas
        """
        tarjetados = []
        query = QSqlQuery()
        query.prepare("""
            SELECT p.id, p.nombre, e.nombre,
                   SUM(CASE WHEN t.tipo = 'amarilla' THEN 1 ELSE 0 END) as amarillas,
                   SUM(CASE WHEN t.tipo = 'roja' THEN 1 ELSE 0 END) as rojas
            FROM participantes p
            LEFT JOIN equipo_participante ep ON p.id = ep.participante_id
            LEFT JOIN equipos e ON ep.equipo_id = e.id
            LEFT JOIN tarjetas t ON p.id = t.participante_id
            WHERE p.es_jugador = 1 AND p.activo = 1
            GROUP BY p.id, p.nombre, e.nombre
            HAVING (amarillas > 0 OR rojas > 0)
            ORDER BY rojas DESC, amarillas DESC
            LIMIT ?
        """)
        query.addBindValue(limite)
        
        if query.exec():
            while query.next():
                tarjetados.append({
                    'id': query.value(0),
                    'nombre': query.value(1),
                    'equipo': query.value(2) or 'Sin equipo',
                    'amarillas': query.value(3) or 0,
                    'rojas': query.value(4) or 0
                })
        
        return tarjetados
    
    @staticmethod
    def asignar_jugador_a_equipo(participante_id: int, equipo_id: int) -> bool:
        """
        Asigna un jugador a un equipo.
        
        Args:
            participante_id: ID del participante
            equipo_id: ID del equipo
            
        Returns:
            True si se asignó correctamente
        """
        participante = Participante.obtener_por_id(participante_id)
        if participante:
            return participante.asignar_equipo(equipo_id)
        return False
    
    @staticmethod
    def desasignar_jugador_de_equipo(participante_id: int, equipo_id: int) -> bool:
        """
        Desasigna un jugador de un equipo.
        
        Args:
            participante_id: ID del participante
            equipo_id: ID del equipo
            
        Returns:
            True si se desasignó correctamente
        """
        participante = Participante.obtener_por_id(participante_id)
        if participante:
            return participante.desasignar_equipo(equipo_id)
        return False
