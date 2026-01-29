# App Torneo de Fútbol

Una aplicación de escritorio para gestionar torneos de fútbol con sistema de eliminatorias.

## Características

- Gestión de Equipos: Crear, editar y eliminar equipos participantes
- Gestión de Participantes: Administrar jugadores y árbitros
- Programación de Partidos: Crear partidos y registrar resultados
- Cuadro Eliminatorio: Visualizar el progreso del torneo en octavos, cuartos, semifinal y final
- Exportación de Resultados: Guardar los resultados en CSV
- Interfaz Intuitiva: Diseño limpio y fácil de usar con soporte visual completo

## Requisitos del Sistema

### Software
- **Python**: 3.8 o superior
- **Dependencias principales**:
  - PySide6 >= 6.5.0 (para la interfaz gráfica)
  - SQLite3 (incluido en Python)

## Instalación

### Opción 1: Ejecutable (Recomendado para usuarios finales)

1. Ejecutar el main.py en Visual Estudio Code
2. Abrir el .exe 

## Estructura del Proyecto


Torneo_Futbol/
├── main.py                   
├── config.py                  
├── inicializar_db.py          
├── requirements.txt          
├── DATA/                      
│   └── torneoFutbol_sqlite.db 
├── MODELS/                   
│   ├── database.py           
│   ├── equipo.py             
│   ├── participante.py       
│   └── partido.py            
├── VIEWS/                     
│   ├── main_window.py       
│   ├── equipos.py            
│   ├── participantes.py      
│   ├── partidos.py           
│   └── ui/                   
├── CONTROLLERS/               
│   ├── equipos_controller.py
│   ├── participantes_controller.py
│   └── partidos_controller.py
├── WIDGET/                    
│   ├── ui_main_window.py
│   ├── ui_equipos.py
│   ├── ui_participantes.py
│   └── ui_partidos.py
├── RESOURCES/                 
│   ├── utilidades.py         
│   ├── qss/                  
│   ├── img/                  
│   └── iconos/               
└── dist/                      
    └── Torneo_Futbol/
        ├── Torneo_Futbol.exe
        └── _internal/        

## Base de Datos

### Configuración
- Tipo: SQLite3
- Archivo: `DATA/torneoFutbol_sqlite.db`
- Inicialización automática con `inicializar_db.py`

### Tablas principales
1. equipos: Nombre, curso, color
2. participantes: Nombre, rol (jugador/árbitro), equipo, posición
3. partidos: Equipos, fecha, resultado, árbitro, fase eliminatoria
4. goles: Relación de goles marcados por jugadores
5. tarjetas: Registro de tarjetas (amarillas/rojas)

## Guía de Uso

### Equipos
- Crear nuevos equipos con nombre, curso y color
- Modificar datos de equipos existentes
- Ver la lista de jugadores asignados al equipo
- Eliminar equipos

### Participantes
- Registrar jugadores y árbitros
- Un participante puede ser jugador, árbitro o ambos
- Especificar posición para jugadores (Portero, Defensa Central, Lateral, Centrocampista, Delantero)
- Ver estadísticas de goles y tarjetas

### Partidos
- Programar partidos por eliminatorias (Octavos, Cuartos, Semifinal, Final)
- Asignar árbitros a cada partido
- Registrar resultados y goles
- Ver cuadro completo de eliminatorias

### Consejos de uso
1. Crea primero los equipos y participantes
2. Asigna jugadores a los equipos
3. Programa los partidos de octavos
4. Registra los resultados para avanzar en el torneo
5. Exporta los datos en CSV cuando sea necesario

## Tecnologías Utilizadas

- Python 3.8+ - Lenguaje principal
- PySide6 - Interfaz gráfica (Qt6)
- SQLite - Base de datos
- Qt Designer - Diseño de interfaces

