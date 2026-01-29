"""
Controlador para la gestión de partidos.
Maneja la lógica de negocio de partidos y eliminatorias.
"""

from PySide6.QtSql import QSqlQuery
from MODELS.partido import Partido
from typing import List, Optional, Tuple


class PartidosController:
    """Controlador para operaciones de partidos."""
    
    @staticmethod
    def crear_partido(equipo_local_id: int, equipo_visitante_id: int,
                     fecha_hora: str, eliminatoria: str,
                     arbitro_id: Optional[int] = None) -> Partido:
        """
        Crea un nuevo partido.
        
        Args:
            equipo_local_id: ID del equipo local
            equipo_visitante_id: ID del equipo visitante
            fecha_hora: Fecha y hora del partido (yyyy-MM-dd HH:mm)
            eliminatoria: Tipo de eliminatoria (Octavos, Cuartos, Semifinal, Final)
            arbitro_id: ID del árbitro (opcional)
            
        Returns:
            Partido creado
            
        Raises:
            ValueError: Si los datos no son válidos
        """
        partido = Partido(
            equipo_local_id=equipo_local_id,
            equipo_visitante_id=equipo_visitante_id,
            fecha_hora=fecha_hora,
            eliminatoria=eliminatoria,
            arbitro_id=arbitro_id
        )
        if partido.guardar():
            return partido
        raise ValueError("No se pudo crear el partido")
    
    @staticmethod
    def actualizar_partido(partido_id: int, equipo_local_id: int = None,
                          equipo_visitante_id: int = None,
                          fecha_hora: str = None,
                          arbitro_id: int = None) -> Optional[Partido]:
        """
        Actualiza un partido existente.
        
        Args:
            partido_id: ID del partido
            equipo_local_id: Nuevo equipo local (opcional)
            equipo_visitante_id: Nuevo equipo visitante (opcional)
            fecha_hora: Nueva fecha/hora (opcional)
            arbitro_id: Nuevo árbitro (opcional)
            
        Returns:
            Partido actualizado o None
        """
        partido = Partido.obtener_por_id(partido_id)
        if not partido:
            return None
        
        if equipo_local_id and equipo_local_id != partido.equipo_local_id:
            partido.equipo_local_id = equipo_local_id
        if equipo_visitante_id and equipo_visitante_id != partido.equipo_visitante_id:
            partido.equipo_visitante_id = equipo_visitante_id
        if fecha_hora:
            partido.fecha_hora = fecha_hora
        if arbitro_id is not None:
            partido.arbitro_id = arbitro_id
        
        if partido.guardar():
            return partido
        return None
    
    @staticmethod
    def eliminar_partido(partido_id: int) -> bool:
        """
        Elimina un partido.
        
        Args:
            partido_id: ID del partido
            
        Returns:
            True si se eliminó correctamente
        """
        partido = Partido.obtener_por_id(partido_id)
        if partido:
            return partido.eliminar()
        return False
    
    @staticmethod
    def obtener_partido(partido_id: int) -> Optional[Partido]:
        """
        Obtiene un partido por ID.
        
        Args:
            partido_id: ID del partido
            
        Returns:
            Partido o None
        """
        return Partido.obtener_por_id(partido_id)
    
    @staticmethod
    def obtener_todos_partidos(eliminatoria: str = "", solo_pendientes: bool = False) -> List[Partido]:
        """
        Obtiene todos los partidos.
        
        Args:
            eliminatoria: Filtrar por eliminatoria ('', 'Octavos', 'Cuartos', 'Semifinal', 'Final')
            solo_pendientes: Si True, solo retorna partidos no finalizados
            
        Returns:
            Lista de partidos
        """
        return Partido.obtener_todos(eliminatoria, solo_pendientes)
    
    @staticmethod
    def registrar_gol(partido_id: int, participante_id: int, minuto: int) -> bool:
        """
        Registra un gol en un partido.
        
        Args:
            partido_id: ID del partido
            participante_id: ID del jugador
            minuto: Minuto del gol
            
        Returns:
            True si se registró correctamente
        """
        partido = Partido.obtener_por_id(partido_id)
        if partido and not partido.finalizado:
            return partido.registrar_gol(participante_id, minuto)
        return False
    
    @staticmethod
    def registrar_tarjeta(partido_id: int, participante_id: int, tipo: str, minuto: int) -> bool:
        """
        Registra una tarjeta en un partido.
        
        Args:
            partido_id: ID del partido
            participante_id: ID del jugador
            tipo: 'amarilla' o 'roja'
            minuto: Minuto de la tarjeta
            
        Returns:
            True si se registró correctamente
        """
        partido = Partido.obtener_por_id(partido_id)
        if partido and not partido.finalizado:
            return partido.registrar_tarjeta(participante_id, tipo, minuto)
        return False
    
    @staticmethod
    def finalizar_partido(partido_id: int, goles_local: int, goles_visitante: int) -> bool:
        """
        Finaliza un partido con el resultado.
        
        Args:
            partido_id: ID del partido
            goles_local: Goles del equipo local
            goles_visitante: Goles del equipo visitante
            
        Returns:
            True si se finalizó correctamente
        """
        partido = Partido.obtener_por_id(partido_id)
        if partido:
            return partido.finalizar(goles_local, goles_visitante)
        return False
    
    @staticmethod
    def obtener_goles_partido(partido_id: int) -> Tuple[int, int]:
        """
        Obtiene los goles de un partido.
        
        Args:
            partido_id: ID del partido
            
        Returns:
            Tupla: (goles_local, goles_visitante)
        """
        partido = Partido.obtener_por_id(partido_id)
        if partido:
            return partido.obtener_goles_por_equipo()
        return (0, 0)
    
    @staticmethod
    def obtener_ganador(partido_id: int) -> Optional[int]:
        """
        Obtiene el ganador de un partido.
        
        Args:
            partido_id: ID del partido
            
        Returns:
            ID del equipo ganador, None si empate o no finalizado
        """
        partido = Partido.obtener_por_id(partido_id)
        if partido:
            return partido.obtener_ganador()
        return None
    
    @staticmethod
    def obtener_goles_partido_detallado(partido_id: int) -> List[dict]:
        """
        Obtiene los goles detallados de un partido.
        
        Args:
            partido_id: ID del partido
            
        Returns:
            Lista de diccionarios con datos de goles
        """
        goles = []
        query = QSqlQuery()
        query.prepare("""
            SELECT g.id, p.nombre, g.minuto, e.nombre as equipo
            FROM goles g
            INNER JOIN participantes p ON g.participante_id = p.id
            INNER JOIN equipo_participante ep ON p.id = ep.participante_id
            INNER JOIN equipos e ON ep.equipo_id = e.id
            INNER JOIN partidos par ON g.partido_id = par.id
            WHERE g.partido_id = ?
            ORDER BY g.minuto ASC
        """)
        query.addBindValue(partido_id)
        
        if query.exec():
            while query.next():
                goles.append({
                    'id': query.value(0),
                    'jugador': query.value(1),
                    'minuto': query.value(2),
                    'equipo': query.value(3)
                })
        
        return goles
    
    @staticmethod
    def obtener_tarjetas_partido_detallado(partido_id: int) -> List[dict]:
        """
        Obtiene las tarjetas detalladas de un partido.
        
        Args:
            partido_id: ID del partido
            
        Returns:
            Lista de diccionarios con datos de tarjetas
        """
        tarjetas = []
        query = QSqlQuery()
        query.prepare("""
            SELECT t.id, p.nombre, t.tipo, t.minuto, e.nombre as equipo
            FROM tarjetas t
            INNER JOIN participantes p ON t.participante_id = p.id
            INNER JOIN equipo_participante ep ON p.id = ep.participante_id
            INNER JOIN equipos e ON ep.equipo_id = e.id
            WHERE t.partido_id = ?
            ORDER BY t.minuto ASC
        """)
        query.addBindValue(partido_id)
        
        if query.exec():
            while query.next():
                tarjetas.append({
                    'id': query.value(0),
                    'jugador': query.value(1),
                    'tipo': query.value(2),
                    'minuto': query.value(3),
                    'equipo': query.value(4)
                })
        
        return tarjetas
    
    @staticmethod
    def obtener_proximos_partidos(limite: int = 5) -> List[dict]:
        """
        Obtiene los próximos partidos a jugarse.
        
        Args:
            limite: Número máximo de partidos a retornar
            
        Returns:
            Lista de diccionarios con datos de partidos
        """
        partidos = []
        query = QSqlQuery()
        query.prepare("""
            SELECT p.id, p.fecha_hora, el.nombre, ev.nombre, p.eliminatoria
            FROM partidos p
            INNER JOIN equipos el ON p.equipo_local_id = el.id
            INNER JOIN equipos ev ON p.equipo_visitante_id = ev.id
            WHERE p.finalizado = 0
            ORDER BY p.fecha_hora ASC
            LIMIT ?
        """)
        query.addBindValue(limite)
        
        if query.exec():
            while query.next():
                partidos.append({
                    'id': query.value(0),
                    'fecha_hora': query.value(1),
                    'local': query.value(2),
                    'visitante': query.value(3),
                    'eliminatoria': query.value(4)
                })
        
        return partidos
    
    @staticmethod
    def obtener_tabla_posiciones() -> List[dict]:
        """
        Obtiene la tabla de posiciones del torneo.
        
        Returns:
            Lista de diccionarios con posiciones ordenadas por puntos
        """
        posiciones = []
        query = QSqlQuery()
        query.exec("""
            SELECT e.id, e.nombre,
                   COUNT(CASE WHEN p.finalizado = 1 THEN 1 END) as pj,
                   SUM(CASE WHEN p.finalizado = 1 AND (
                       (p.equipo_local_id = e.id AND p.goles_local > p.goles_visitante) OR
                       (p.equipo_visitante_id = e.id AND p.goles_visitante > p.goles_local)
                   ) THEN 1 ELSE 0 END) as pg,
                   SUM(CASE WHEN p.finalizado = 1 AND p.goles_local = p.goles_visitante THEN 1 ELSE 0 END) as pe,
                   SUM(CASE WHEN p.finalizado = 1 AND (
                       (p.equipo_local_id = e.id AND p.goles_local < p.goles_visitante) OR
                       (p.equipo_visitante_id = e.id AND p.goles_visitante < p.goles_local)
                   ) THEN 1 ELSE 0 END) as pp,
                   SUM(CASE WHEN p.equipo_local_id = e.id THEN p.goles_local WHEN p.equipo_visitante_id = e.id THEN p.goles_visitante ELSE 0 END) as gf,
                   SUM(CASE WHEN p.equipo_local_id = e.id THEN p.goles_visitante WHEN p.equipo_visitante_id = e.id THEN p.goles_local ELSE 0 END) as gc
            FROM equipos e
            LEFT JOIN partidos p ON (p.equipo_local_id = e.id OR p.equipo_visitante_id = e.id)
            WHERE e.activo = 1
            GROUP BY e.id, e.nombre
            ORDER BY 
                (SUM(CASE WHEN p.finalizado = 1 AND (
                    (p.equipo_local_id = e.id AND p.goles_local > p.goles_visitante) OR
                    (p.equipo_visitante_id = e.id AND p.goles_visitante > p.goles_local)
                ) THEN 1 ELSE 0 END) * 3 +
                SUM(CASE WHEN p.finalizado = 1 AND p.goles_local = p.goles_visitante THEN 1 ELSE 0 END)) DESC,
                (SUM(CASE WHEN p.equipo_local_id = e.id THEN p.goles_local WHEN p.equipo_visitante_id = e.id THEN p.goles_visitante ELSE 0 END) - 
                 SUM(CASE WHEN p.equipo_local_id = e.id THEN p.goles_visitante WHEN p.equipo_visitante_id = e.id THEN p.goles_local ELSE 0 END)) DESC
        """)
        
        if query.exec():
            posicion = 1
            while query.next():
                pj = query.value(2) or 0
                pg = query.value(3) or 0
                pe = query.value(4) or 0
                pp = query.value(5) or 0
                gf = query.value(6) or 0
                gc = query.value(7) or 0
                
                posiciones.append({
                    'posicion': posicion,
                    'equipo_id': query.value(0),
                    'equipo': query.value(1),
                    'pj': pj,
                    'pg': pg,
                    'pe': pe,
                    'pp': pp,
                    'gf': gf,
                    'gc': gc,
                    'dg': gf - gc,
                    'pts': (pg * 3) + pe
                })
                posicion += 1
        
        return posiciones
