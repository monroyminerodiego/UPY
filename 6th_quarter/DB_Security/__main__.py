import os, platform
from Creation.db import database_manager

os.system('cls') if platform.system() == 'Windows' else os.system('clear')

# ===== Instancia de clases
conexion = database_manager()
cursor = conexion.obtener_cursor()

# ===== Ejemplo
def ejemplo_uso():
    print(f"{'='*5} Ingresando a ejemplo de uso...")

    # ===== Verificar la conexion con Postgres
    version = cursor.ejecutar_script_sql("SELECT version();")
    print(f"La Version de Postgres es:  {version}\n")

    # ===== Crear una base de datos y Verificar las bases de datos
    conexion.listar_bds()
    conexion.crear_base_datos('prueba')

    # ===== Conectarse a una base de datos
    conexion.conectar_bd('prueba')
    conexion.listar_bds()

    # ===== Elimina una base de datos
    conexion.conectar_bd('postgres')
    conexion.eliminar_base_datos('prueba')

    print(f"{'='*5} Fin de ejemplo de uso...")

# ===== Cerrar sesion con base de datos
conexion.cerrar_sesion()
