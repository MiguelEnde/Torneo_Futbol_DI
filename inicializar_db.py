"""
Script de inicialización de la base de datos.
Crea la BD e inserta datos de ejemplo usando sqlite3 directamente.
Se ejecuta automáticamente desde main.py si la BD está vacía.
"""

import sqlite3
import os
import sys

def obtener_ruta_db():
    """Obtiene la ruta de la base de datos."""
    # La ruta ahora será DATA/torneoFutbol_sqlite.db relativa a la carpeta del proyecto
    ruta_relativa = os.path.join("DATA", "torneoFutbol_sqlite.db")
    
    # Si estamos en desarrollo, retornamos la ruta absoluta
    if getattr(sys, 'frozen', False):
        # Ejecutable empaquetado
        return os.path.join(sys._MEIPASS, ruta_relativa)
    else:
        # Desarrollo: obtenemos la ruta absoluta
        return os.path.abspath(ruta_relativa)

def crear_tablas_si_no_existen(cursor):
    """Crea las tablas si no existen."""
    # Equipos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            curso TEXT,
            color_camiseta TEXT,
            activo INTEGER DEFAULT 1
        )
    """)
    
    # Participantes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS participantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            fecha_nacimiento DATE,
            curso TEXT,
            es_jugador INTEGER DEFAULT 0,
            es_arbitro INTEGER DEFAULT 0,
            posicion TEXT,
            activo INTEGER DEFAULT 1
        )
    """)
    
    # Equipo_Participante
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS equipo_participante (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            equipo_id INTEGER NOT NULL,
            participante_id INTEGER NOT NULL,
            UNIQUE(equipo_id, participante_id),
            FOREIGN KEY (equipo_id) REFERENCES equipos(id) ON DELETE CASCADE,
            FOREIGN KEY (participante_id) REFERENCES participantes(id) ON DELETE CASCADE
        )
    """)
    
    # Partidos
    cursor.execute("""
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
            FOREIGN KEY (equipo_local_id) REFERENCES equipos(id) ON DELETE CASCADE,
            FOREIGN KEY (equipo_visitante_id) REFERENCES equipos(id) ON DELETE CASCADE,
            FOREIGN KEY (arbitro_id) REFERENCES participantes(id)
        )
    """)
    
    # Goles
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS goles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partido_id INTEGER,
            participante_id INTEGER NOT NULL,
            minuto INTEGER,
            FOREIGN KEY (partido_id) REFERENCES partidos(id) ON DELETE CASCADE,
            FOREIGN KEY (participante_id) REFERENCES participantes(id) ON DELETE CASCADE
        )
    """)
    
    # Tarjetas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarjetas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partido_id INTEGER,
            participante_id INTEGER NOT NULL,
            tipo TEXT,
            minuto INTEGER,
            FOREIGN KEY (partido_id) REFERENCES partidos(id) ON DELETE CASCADE,
            FOREIGN KEY (participante_id) REFERENCES participantes(id) ON DELETE CASCADE
        )
    """)

def inicializar_datos():
    """Inserta datos de ejemplo en la BD."""
    db_path = obtener_ruta_db()
    
    # Asegurar que el directorio existe
    db_dir = os.path.dirname(db_path)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Crear tablas primero
        print("Creando tablas...")
        crear_tablas_si_no_existen(cursor)
        
        # Verificar si ya hay datos
        cursor.execute("SELECT COUNT(*) FROM equipos")
        if cursor.fetchone()[0] > 0:
            print("✓ Base de datos ya tiene datos iniciales.")
            conn.close()
            return
        
        print("Insertando datos iniciales de ejemplo...")
        
        # Equipos
        equipos = [
            (None, "Real Suciedad", "1º ESO A", "Rojo"),
            (None, "Aston Birras", "1º ESO B", "Azul"),
            (None, "Supernenas", "2º ESO A", "Verde"),
            (None, "Union de casados", "2º ESO B", "Amarillo"),
        ]
        cursor.executemany(
            "INSERT INTO equipos (id, nombre, curso, color_camiseta) VALUES (?, ?, ?, ?)",
            equipos
        )
        
        # Participantes
        participantes = [
            # Real Suciedad
            (None, "Carlos González", "2010-03-15", "1º ESO A", 1, 0, "Portero"),
            (None, "Miguel López", "2010-05-20", "1º ESO A", 1, 0, "Defensa"),
            (None, "Juan Martínez", "2010-07-10", "1º ESO A", 1, 0, "Centrocampista"),
            (None, "David Sánchez", "2010-04-25", "1º ESO A", 1, 0, "Delantero"),
            (None, "Pedro García", "2010-06-30", "1º ESO A", 1, 0, "Delantero"),
            
            # Aston Birras
            (None, "Roberto Fernández", "2010-02-12", "1º ESO B", 1, 0, "Portero"),
            (None, "Antonio Rodríguez", "2010-08-18", "1º ESO B", 1, 0, "Defensa"),
            (None, "Fernando Romero", "2010-09-22", "1º ESO B", 1, 0, "Centrocampista"),
            (None, "Luis Torres", "2010-01-05", "1º ESO B", 1, 0, "Delantero"),
            (None, "Ricardo Pérez", "2010-11-14", "1º ESO B", 1, 0, "Defensa"),
            
            # Super nenas
            (None, "Arturo Silva", "2009-03-10", "2º ESO A", 1, 0, "Portero"),
            (None, "Javier Vargas", "2009-05-20", "2º ESO A", 1, 0, "Defensa"),
            (None, "Sergio Castro", "2009-07-15", "2º ESO A", 1, 0, "Centrocampista"),
            (None, "Oscar Álvarez", "2009-04-28", "2º ESO A", 1, 0, "Delantero"),
            (None, "Manuel Díaz", "2009-06-12", "2º ESO A", 1, 0, "Delantero"),
            
            # Union de casados
            (None, "Enrique Moreno", "2009-02-08", "2º ESO B", 1, 0, "Portero"),
            (None, "Gonzalo Ruiz", "2009-08-19", "2º ESO B", 1, 0, "Defensa"),
            (None, "Jesús Soto", "2009-09-24", "2º ESO B", 1, 0, "Centrocampista"),
            (None, "Vicente Herrera", "2009-01-11", "2º ESO B", 1, 0, "Delantero"),
            (None, "Mariano Navarro", "2009-10-30", "2º ESO B", 1, 0, "Defensa"),
            
            # ÁRBITROS
            (None, "Profesor Antonio", "1970-05-15", "Profesorado", 0, 1, None),
            (None, "Profesor Juan", "1975-08-22", "Profesorado", 0, 1, None),
        ]
        cursor.executemany(
            """INSERT INTO participantes 
               (id, nombre, fecha_nacimiento, curso, es_jugador, es_arbitro, posicion) 
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            participantes
        )
        
        # Asignaciones de jugadores a equipos
        cursor.execute("SELECT id FROM equipos WHERE nombre = 'Real Suciedad'")
        real_suciedad_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM equipos WHERE nombre = 'Aston Birras'")
        aston_birras_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM equipos WHERE nombre = 'Supernenas'")
        supernenas_id = cursor.fetchone()[0]
        cursor.execute("SELECT id FROM equipos WHERE nombre = 'Union de casados'")
        union_casados_id = cursor.fetchone()[0]
        
        asignaciones = [
            # REAL SUCIEDAD
            (None, real_suciedad_id, 1),  # Carlos González
            (None, real_suciedad_id, 2),  # Miguel López
            (None, real_suciedad_id, 3),  # Juan Martínez
            (None, real_suciedad_id, 4),  # David Sánchez
            (None, real_suciedad_id, 5),  # Pedro García
            
            # ASTON BIRRAS
            (None, aston_birras_id, 6),  # Roberto Fernández
            (None, aston_birras_id, 7),  # Antonio Rodríguez
            (None, aston_birras_id, 8),  # Fernando Romero
            (None, aston_birras_id, 9),  # Luis Torres
            (None, aston_birras_id, 10), # Ricardo Pérez
            
            # SUPERNENAS
            (None, supernenas_id, 11), # Arturo Silva
            (None, supernenas_id, 12), # Javier Vargas
            (None, supernenas_id, 13), # Sergio Castro
            (None, supernenas_id, 14), # Oscar Álvarez
            (None, supernenas_id, 15), # Manuel Díaz
            
            # UNION DE CASADOS
            (None, union_casados_id, 16), # Enrique Moreno
            (None, union_casados_id, 17), # Gonzalo Ruiz
            (None, union_casados_id, 18), # Jesús Soto
            (None, union_casados_id, 19), # Vicente Herrera
            (None, union_casados_id, 20), # Mariano Navarro
        ]
        cursor.executemany(
            "INSERT INTO equipo_participante (id, equipo_id, participante_id) VALUES (?, ?, ?)",
            asignaciones
        )
        
        # Commit explícito
        conn.commit()
        
        print("Datos iniciales insertados correctamente")
        print(f"   - 4 equipos creados")
        print(f"   - 20 jugadores + 2 árbitros")
        print(f"   - 20 asignaciones jugador-equipo")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Error en base de datos: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inicializar_datos()
