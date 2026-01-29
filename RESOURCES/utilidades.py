"""
Utilidades y funciones auxiliares para la aplicación.
"""

from PySide6.QtSql import QSqlQuery
from datetime import datetime, date
from typing import Optional


class Validador:
    """Clase para validaciones comunes."""
    
    @staticmethod
    def validar_nombre(nombre: str) -> bool:
        """Valida que el nombre tenga al menos 2 caracteres."""
        return bool(nombre and len(nombre.strip()) >= 2)
    
    @staticmethod
    def validar_fecha(fecha_str: str, formato: str = "yyyy-MM-dd") -> bool:
        """Valida que la fecha sea válida."""
        try:
            datetime.strptime(fecha_str, formato.replace("y", "%Y").replace("M", "%m").replace("d", "%d"))
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validar_email(email: str) -> bool:
        """Valida formato de email (básico)."""
        return "@" in email and "." in email.split("@")[1]
    
    @staticmethod
    def calcular_edad(fecha_nacimiento: str) -> int:
        """Calcula la edad a partir de la fecha de nacimiento."""
        try:
            fecha = datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
            hoy = date.today()
            edad = hoy.year - fecha.year
            if (hoy.month, hoy.day) < (fecha.month, fecha.day):
                edad -= 1
            return edad
        except ValueError:
            return 0


class EstadisticasAuxiliar:
    """Clase para cálculos de estadísticas."""
    
    @staticmethod
    def obtener_promedio_goles_equipo(equipo_id: int) -> float:
        """Calcula el promedio de goles por partido de un equipo."""
        query = QSqlQuery()
        query.prepare("""
            SELECT 
                SUM(CASE WHEN equipo_local_id = ? THEN goles_local WHEN equipo_visitante_id = ? THEN goles_visitante ELSE 0 END) as goles,
                COUNT(CASE WHEN finalizado = 1 THEN 1 END) as partidos
            FROM partidos
            WHERE (equipo_local_id = ? OR equipo_visitante_id = ?) AND finalizado = 1
        """)
        
        for _ in range(4):
            query.addBindValue(equipo_id)
        
        if query.exec() and query.next():
            goles = query.value(0) or 0
            partidos = query.value(1) or 1
            return goles / partidos if partidos > 0 else 0
        return 0
    
    @staticmethod
    def obtener_promedio_goles_recibidos(equipo_id: int) -> float:
        """Calcula el promedio de goles recibidos por partido de un equipo."""
        query = QSqlQuery()
        query.prepare("""
            SELECT 
                SUM(CASE WHEN equipo_local_id = ? THEN goles_visitante WHEN equipo_visitante_id = ? THEN goles_local ELSE 0 END) as goles,
                COUNT(CASE WHEN finalizado = 1 THEN 1 END) as partidos
            FROM partidos
            WHERE (equipo_local_id = ? OR equipo_visitante_id = ?) AND finalizado = 1
        """)
        
        for _ in range(4):
            query.addBindValue(equipo_id)
        
        if query.exec() and query.next():
            goles = query.value(0) or 0
            partidos = query.value(1) or 1
            return goles / partidos if partidos > 0 else 0
        return 0
    
    @staticmethod
    def obtener_efectividad_goleador(participante_id: int) -> float:
        """Calcula la efectividad de un goleador (goles por partido)."""
        query = QSqlQuery()
        query.prepare("""
            SELECT COUNT(*) as goles FROM goles
            WHERE participante_id = ?
        """)
        query.addBindValue(participante_id)
        
        partidos = 0
        if query.exec() and query.next():
            goles = query.value(0) or 0
            
            query.prepare("""
                SELECT COUNT(DISTINCT partido_id) FROM goles
                WHERE participante_id = ?
            """)
            query.addBindValue(participante_id)
            
            if query.exec() and query.next():
                partidos = query.value(0) or 1
                return goles / partidos if partidos > 0 else 0
        
        return 0


class FormatoAuxiliar:
    """Clase para formateo de datos."""
    
    @staticmethod
    def formato_fecha_corto(fecha_str: str) -> str:
        """Convierte formato de fecha a dd/MM/yyyy."""
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
            return fecha.strftime("%d/%m/%Y")
        except ValueError:
            return fecha_str
    
    @staticmethod
    def formato_fecha_completa(fecha_str: str) -> str:
        """Convierte formato de fecha a formato completo."""
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
            dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
            meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio",
                    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
            dia_semana = dias[fecha.weekday()]
            mes = meses[fecha.month - 1]
            return f"{dia_semana}, {fecha.day} de {mes} de {fecha.year}"
        except ValueError:
            return fecha_str
    
    @staticmethod
    def formato_resultado(goles_local: int, goles_visitante: int) -> str:
        """Formatea el resultado de un partido."""
        return f"{goles_local} - {goles_visitante}"
    
    @staticmethod
    def formato_duracion(segundos: int) -> str:
        """Convierte segundos a formato MM:SS."""
        minutos = segundos // 60
        segs = segundos % 60
        return f"{minutos:02d}:{segs:02d}"


class ColoAuxiliar:
    """Clase para colores y estilos."""
    
    COLOR_PRIMARIO = "#DC143C"  # Rojo crimson
    COLOR_SECUNDARIO = "#2C2C2C"  # Gris oscuro
    COLOR_EXITO = "#00A86B"  # Verde
    COLOR_ERROR = "#FF0000"  # Rojo
    COLOR_ADVERTENCIA = "#FFB300"  # Naranja
    COLOR_INFO = "#0066CC"  # Azul
    
    @staticmethod
    def obtener_color_estado(finalizado: bool) -> str:
        """Obtiene color según estado del partido."""
        return ColoAuxiliar.COLOR_EXITO if finalizado else ColoAuxiliar.COLOR_ADVERTENCIA
    
    @staticmethod
    def obtener_color_resultado(local: int, visitante: int, es_local: bool = True) -> str:
        """Obtiene color según resultado (ganada, empatada, perdida)."""
        if es_local:
            if local > visitante:
                return ColoAuxiliar.COLOR_EXITO
            elif local < visitante:
                return ColoAuxiliar.COLOR_ERROR
        else:
            if visitante > local:
                return ColoAuxiliar.COLOR_EXITO
            elif visitante < local:
                return ColoAuxiliar.COLOR_ERROR
        
        return ColoAuxiliar.COLOR_ADVERTENCIA  # Empate


def obtener_ruta_recurso(ruta_relativa: str) -> str:
    """
    Obtiene la ruta absoluta de un recurso.
    Compatible con PyInstaller y con ejecución normal.
    
    Args:
        ruta_relativa: Ruta relativa del recurso (ej: "img/campo.avif", "RESOURCES/img/campo.avif", etc)
        
    Returns:
        str: Ruta absoluta del recurso
    """
    import sys
    import os
    
    # Normalizar la ruta relativa (convertir barras)
    ruta_relativa = ruta_relativa.replace("\\", "/")
    
    if getattr(sys, 'frozen', False):
        # Cuando se ejecuta desde PyInstaller (_MEIPASS apunta a _internal/)
        # En PyInstaller: _internal/RESOURCES/img/campo.avif
        base_path = sys._MEIPASS
        print(f"[FROZEN] base_path (sys._MEIPASS): {base_path}")
        
        # Asegurar que empieza con RESOURCES/
        if not ruta_relativa.startswith("RESOURCES/"):
            ruta_relativa = "RESOURCES/" + ruta_relativa
    else:
        # Cuando se ejecuta desde Python normal
        # Estamos en RESOURCES/utilidades.py, así que ir dos niveles arriba
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print(f"[NORMAL] base_path: {base_path}")
        
        # Si empieza con RESOURCES/, ya podemos usarla directamente
        # Si no, anadimos RESOURCES/
        if not ruta_relativa.startswith("RESOURCES/"):
            ruta_relativa = "RESOURCES/" + ruta_relativa
    
    ruta_completa = os.path.join(base_path, ruta_relativa)
    print(f"[obtener_ruta_recurso] Ruta final: {ruta_completa}")
    return ruta_completa
