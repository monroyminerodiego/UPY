import os, sys
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(__file__))
))
from Manager.db import database_manager

class AC07:
    
    def __init__(self):
        self.conexion = None

    def api_configuration(self):
        print(f"\n{'='*5} API Configuration")
        self.conexion = database_manager()
        self.conexion.conectar_bd('db_security')
        self.conexion.crear_tabla_dummy()

    def create_testUser_rol(self):
        print(f"{'='*5} test_user")
        query = f"""CREATE ROLE test_user LOGIN;"""
        self.conexion.ejecutar_query(query)
        print('Role created...')

    def revertir_main(self):
        print(f"\n{'='*5} Revirtiendo main")
        self.conexion.eliminar_tabla('students')

    def main(self):
        
        self.api_configuration()

        self.create_testUser_rol()

        self.revertir_main()

        self.conexion.cerrar_sesion()