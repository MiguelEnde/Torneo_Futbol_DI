"""
Modelo de datos para Equipos.
Define la estructura de un equipo en el torneo.
"""

from dataclasses import dataclass
from typing import Optional
from PySide6.QtSql import QSqlQuery


@dataclass
class Equipo:
    """Clase que representa un equipo."""
    
    id: Optional[int] = None
    nombre: str = ""
    curso: str = ""
    color_camiseta: str = ""
    logo: Optional[str] = None
    activo: int = 1
    
    def __post_init__(self):
        """Validaciones después de la inicialización."""
        if not self.nombre or not self.curso:
            raise ValueError("El nombre y curso son obligatorios")
    
    def guardar(self) -> bool:
        """
        Guarda el equipo en la base de datos.
        
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        query = QSqlQuery()
        
        try:
            if self.id:
                # Actualizar
                query.prepare("""
                    UPDATE equipos 
                    SET nombre = ?, curso = ?, color_camiseta = ?, logo = ?
                    WHERE id = ?
                """)
                query.addBindValue(self.nombre)
                query.addBindValue(self.curso)
                query.addBindValue(self.color_camiseta)
                query.addBindValue(self.logo)
                query.addBindValue(self.id)
            else:
                # Crear
                query.prepare("""
                    INSERT INTO equipos (nombre, curso, color_camiseta, logo)
                    VALUES (?, ?, ?, ?)
                """)
                query.addBindValue(self.nombre)
                query.addBindValue(self.curso)
                query.addBindValue(self.color_camiseta)
                query.addBindValue(self.logo)
            
            if query.exec():
                if not self.id:
                    self.id = query.lastInsertId()
                return True
            return False
        except Exception as e:
            print(f"Error al guardar equipo: {e}")
            return False
    
    def eliminar(self) -> bool:
        """
        Elimina el equipo (soft delete).
        
        Returns:
            bool: True si se eliminó correctamente
        """
        if not self.id:
            return False
        
        query = QSqlQuery()
        query.prepare("UPDATE equipos SET activo = 0 WHERE id = ?")
        query.addBindValue(self.id)
        return query.exec()
    
    @staticmethod
    def obtener_por_id(equipo_id: int) -> Optional['Equipo']:
        """
        Obtiene un equipo por su ID.
        
        Args:
            equipo_id: ID del equipo
            
        Returns:
            Equipo o None
        """
        query = QSqlQuery()
        query.prepare("""
            SELECT id, nombre, curso, color_camiseta, logo, activo
            FROM equipos WHERE id = ?
        """)
        query.addBindValue(equipo_id)
        
        if query.exec() and query.next():
            return Equipo(
                id=query.value(0),
                nombre=query.value(1),
                curso=query.value(2),
                color_camiseta=query.value(3),
                logo=query.value(4),
                activo=query.value(5)
            )
        return None
    
    @staticmethod
    def obtener_todos(solo_activos: bool = True) -> list['Equipo']:
        """
        Obtiene todos los equipos.
        
        Args:
            solo_activos: Si True, solo retorna equipos activos
            
        Returns:
            Lista de Equipo
        """
        equipos = []
        query = QSqlQuery()
        
        sql = "SELECT id, nombre, curso, color_camiseta, logo, activo FROM equipos"
        if solo_activos:
            sql += " WHERE activo = 1"
        sql += " ORDER BY nombre"
        
        if query.exec(sql):
            while query.next():
                equipos.append(Equipo(
                    id=query.value(0),
                    nombre=query.value(1),
                    curso=query.value(2),
                    color_camiseta=query.value(3),
                    logo=query.value(4),
                    activo=query.value(5)
                ))
        
        return equipos
