"""
Módulo de gestión de base de datos SQLite para el torneo de fútbol.
Gestiona la conexión y creación de tablas.
"""

from PySide6.QtSql import QSqlDatabase, QSqlQuery
import os
import sys

def obtener_ruta_db():
    """
    Obtiene la ruta absoluta de la base de datos.
    Compatible con PyInstaller.
    La BD se encuentra en la carpeta DATA.
    """
    if getattr(sys, 'frozen', False):
        # Ejecutable empaquetado
        base_path = sys._MEIPASS
        return os.path.join(base_path, "DATA", "torneoFutbol_sqlite.db")
    else:
        # Desarrollo - obtener ruta relativa desde el directorio del proyecto
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_dir = os.path.dirname(current_dir)
        return os.path.join(project_dir, "DATA", "torneoFutbol_sqlite.db")

def conectar():
    """
    Establece la conexión con la base de datos SQLite.
    Activa las foreign keys y crea las tablas necesarias.
    
    Returns:
        QSqlDatabase: Objeto de conexión a la base de datos
        
    Raises:
        Exception: Si no se puede abrir la base de datos
    """
    db = QSqlDatabase.addDatabase("QSQLITE")
    db_path = obtener_ruta_db()
    db.setDatabaseName(db_path)
    
    if not db.open():
        raise Exception(f"No se pudo abrir la BD en {db_path}")
    
    query = QSqlQuery()
    query.exec("PRAGMA foreign_keys = ON;")
    
    crear_tablas(query)
    
    return db

def crear_tablas(query):
    """
    Crea todas las tablas necesarias para el torneo si no existen.
    
    Tablas:
        - equipos: Datos de los equipos
        - participantes: Jugadores y árbitros
        - equipo_participante: Relación N:M entre equipos y jugadores
        - partidos: Información de los partidos
        - goles: Registro de goles por partido
        - tarjetas: Registro de tarjetas por partido
    """
    
    # Tabla de equipos
    query.exec("""
        CREATE TABLE IF NOT EXISTS equipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            curso TEXT NOT NULL,
            color_camiseta TEXT NOT NULL,
            logo TEXT,
            activo INTEGER DEFAULT 1
        )
    """)
    
    # Tabla de participantes (jugadores y árbitros)
    query.exec("""
        CREATE TABLE IF NOT EXISTS participantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            fecha_nacimiento TEXT NOT NULL,
            curso TEXT NOT NULL,
            es_jugador INTEGER DEFAULT 0,
            es_arbitro INTEGER DEFAULT 0,
            posicion TEXT,
            activo INTEGER DEFAULT 1
        )
    """)
    
    # Relación N:M entre equipos y participantes (jugadores)
    query.exec("""
        CREATE TABLE IF NOT EXISTS equipo_participante (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipo_id INTEGER NOT NULL,
            participante_id INTEGER NOT NULL,
            FOREIGN KEY (equipo_id) REFERENCES equipos(id) ON DELETE CASCADE,
            FOREIGN KEY (participante_id) REFERENCES participantes(id) ON DELETE CASCADE,
            UNIQUE(equipo_id, participante_id)
        )
    """)
    
    # Tabla de partidos
    query.exec("""
        CREATE TABLE IF NOT EXISTS partidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipo_local_id INTEGER NOT NULL,
            equipo_visitante_id INTEGER NOT NULL,
            arbitro_id INTEGER,
            fecha_hora TEXT NOT NULL,
            eliminatoria TEXT NOT NULL,
            goles_local INTEGER DEFAULT 0,
            goles_visitante INTEGER DEFAULT 0,
            finalizado INTEGER DEFAULT 0,
            FOREIGN KEY (equipo_local_id) REFERENCES equipos(id),
            FOREIGN KEY (equipo_visitante_id) REFERENCES equipos(id),
            FOREIGN KEY (arbitro_id) REFERENCES participantes(id)
        )
    """)
    
    # Tabla de goles detallados
    query.exec("""
        CREATE TABLE IF NOT EXISTS goles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partido_id INTEGER NOT NULL,
            participante_id INTEGER NOT NULL,
            minuto INTEGER,
            FOREIGN KEY (partido_id) REFERENCES partidos(id) ON DELETE CASCADE,
            FOREIGN KEY (participante_id) REFERENCES participantes(id)
        )
    """)
    
    # Tabla de tarjetas
    query.exec("""
        CREATE TABLE IF NOT EXISTS tarjetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partido_id INTEGER NOT NULL,
            participante_id INTEGER NOT NULL,
            tipo TEXT NOT NULL CHECK(tipo IN ('amarilla', 'roja')),
            minuto INTEGER,
            FOREIGN KEY (partido_id) REFERENCES partidos(id) ON DELETE CASCADE,
            FOREIGN KEY (participante_id) REFERENCES participantes(id)
        )
    """)
    
    print("Tablas creadas correctamente")
    
    # Insertar datos de ejemplo si las tablas están vacías
    insertar_datos_iniciales(query)


def insertar_datos_iniciales(query):
    """
    Inserta datos de ejemplo iniciales en la base de datos.
    Solo se ejecuta si las tablas están vacías.
    """
    # Verificar si ya hay equipos
    query.exec("SELECT COUNT(*) FROM equipos")
    if query.next() and query.value(0) > 0:
        return  # Ya hay datos, no hacer nada
    
    print("Insertando datos iniciales de ejemplo...")
    
    # Insertar equipos
    equipos = [
        ("Vipers", "1º ESO A", "Rojo"),
        ("Sharks", "1º ESO B", "Azul"),
        ("Tigers", "2º ESO A", "Verde"),
        ("Eagles", "2º ESO B", "Amarillo"),
    ]
    
    for nombre, curso, color in equipos:
        query.prepare("""
            INSERT INTO equipos (nombre, curso, color_camiseta)
            VALUES (?, ?, ?)
        """)
        query.addBindValue(nombre)
        query.addBindValue(curso)
        query.addBindValue(color)
        if not query.exec():
            print(f"Error inserting equipo: {query.lastError().text()}")
    
    # Insertar participantes (jugadores)
    participantes = [
        # VIPERS
        ("Carlos González", "2010-03-15", "1º ESO A", 1, 0, "Portero"),
        ("Miguel López", "2010-05-20", "1º ESO A", 1, 0, "Defensa"),
        ("Juan Martínez", "2010-07-10", "1º ESO A", 1, 0, "Centrocampista"),
        ("David Sánchez", "2010-04-25", "1º ESO A", 1, 0, "Delantero"),
        ("Pedro García", "2010-06-30", "1º ESO A", 1, 0, "Delantero"),
        
        # SHARKS
        ("Roberto Fernández", "2010-02-12", "1º ESO B", 1, 0, "Portero"),
        ("Antonio Rodríguez", "2010-08-18", "1º ESO B", 1, 0, "Defensa"),
        ("Fernando Romero", "2010-09-22", "1º ESO B", 1, 0, "Centrocampista"),
        ("Luis Torres", "2010-01-05", "1º ESO B", 1, 0, "Delantero"),
        ("Ricardo Pérez", "2010-11-14", "1º ESO B", 1, 0, "Defensa"),
        
        # TIGERS
        ("Arturo Silva", "2009-03-10", "2º ESO A", 1, 0, "Portero"),
        ("Javier Vargas", "2009-05-20", "2º ESO A", 1, 0, "Defensa"),
        ("Sergio Castro", "2009-07-15", "2º ESO A", 1, 0, "Centrocampista"),
        ("Oscar Álvarez", "2009-04-28", "2º ESO A", 1, 0, "Delantero"),
        ("Manuel Díaz", "2009-06-12", "2º ESO A", 1, 0, "Delantero"),
        
        # EAGLES
        ("Enrique Moreno", "2009-02-08", "2º ESO B", 1, 0, "Portero"),
        ("Gonzalo Ruiz", "2009-08-19", "2º ESO B", 1, 0, "Defensa"),
        ("Jesús Soto", "2009-09-24", "2º ESO B", 1, 0, "Centrocampista"),
        ("Vicente Herrera", "2009-01-11", "2º ESO B", 1, 0, "Delantero"),
        ("Mariano Navarro", "2009-10-30", "2º ESO B", 1, 0, "Defensa"),
        
        # ÁRBITROS
        ("Profesor Antonio", "1970-05-15", "Profesorado", 0, 1, None),
        ("Profesor Juan", "1975-08-22", "Profesorado", 0, 1, None),
    ]
    
    for nombre, fecha_nac, curso, es_jugador, es_arbitro, posicion in participantes:
        query.prepare("""
            INSERT INTO participantes (nombre, fecha_nacimiento, curso, es_jugador, es_arbitro, posicion)
            VALUES (?, ?, ?, ?, ?, ?)
        """)
        query.addBindValue(nombre)
        query.addBindValue(fecha_nac)
        query.addBindValue(curso)
        query.addBindValue(es_jugador)
        query.addBindValue(es_arbitro)
        query.addBindValue(posicion)
        if not query.exec():
            print(f"Error inserting participante: {query.lastError().text()}")
    
    # Asignar jugadores a equipos
    # Obtener IDs de equipos
    query.exec("SELECT id, nombre FROM equipos ORDER BY nombre")
    equipos_dict = {}
    while query.next():
        equipos_dict[query.value(1)] = query.value(0)
    
    # Definir asignaciones
    asignaciones = [
        ("ASIR", ["Carlos González", "Miguel López", "Juan Martínez", "David Sánchez", "Pedro García"]),
        ("DAM", ["Roberto Fernández", "Antonio Rodríguez", "Fernando Romero", "Luis Torres", "Ricardo Pérez"]),
        ("SMR", ["Arturo Silva", "Javier Vargas", "Sergio Castro", "Oscar Álvarez", "Manuel Díaz"]),
        ("DAW", ["Enrique Moreno", "Gonzalo Ruiz", "Jesús Soto", "Vicente Herrera", "Mariano Navarro"]),
    ]
    
    for equipo_nombre, jugadores in asignaciones:
        equipo_id = equipos_dict.get(equipo_nombre)
        if not equipo_id:
            continue
        
        for jugador_nombre in jugadores:
            query.prepare("""
                SELECT id FROM participantes WHERE nombre = ? AND es_jugador = 1
            """)
            query.addBindValue(jugador_nombre)
            
            if query.exec() and query.next():
                participante_id = query.value(0)
                query.prepare("""
                    INSERT OR IGNORE INTO equipo_participante (equipo_id, participante_id)
                    VALUES (?, ?)
                """)
                query.addBindValue(equipo_id)
                query.addBindValue(participante_id)
                if not query.exec():
                    print(f"Error assigning player: {query.lastError().text()}")
    
    print("Datos iniciales insertados correctamente")


def cerrar_conexion():
    """Cierra la conexión a la base de datos."""
    db = QSqlDatabase.database()
    if db.isOpen():
        db.close()
        print("Conexión cerrada")