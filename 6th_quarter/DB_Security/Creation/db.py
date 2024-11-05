import os, sys

sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(__file__))
))

from Connection.connect import Conexion

class database_manager:

    def __init__(self,conexion = None):
        ''' 

        ### Returns
        * `conexion`: Retorna el objeto con el cuál se hizo la conexion.
        '''
        if not(conexion): self.conexion = Conexion()
        else: self.conexion = Conexion(conexion=conexion)
        
        self.conexion.conectar_servidor()

    def crear_base_datos(self,nombre_bd:str):
        ''' Crea una nueva base de datos. '''
        self.conexion.ejecutar_script_sql(f"CREATE DATABASE {nombre_bd};")
        print(f"Se creó la base de datos '{nombre_bd}'")

    def eliminar_base_datos(self,nombre_bd:str):
        ''' Elimina una base de datos. '''
        self.conexion.ejecutar_script_sql(f"DROP DATABASE {nombre_bd};")
        print(f"Se eliminó la base de datos '{nombre_bd}'")

    def listar_bds(self) -> str:
        ''' Lista las bases de datos disponibles. 
        
        ### Returns:
        * list (str): Lista con las bases de datos disponibles.
        '''
        dbs = self.conexion.ejecutar_script_sql("SELECT datname FROM pg_database WHERE datistemplate = false;")
        print(f"Las bases de datos disponibles son {dbs}")
        return dbs
    
    def conectar_bd(self,nombre_bd:str):
        ''' Se desconecta del servidor actual para cambiar la conexion de base de datos.
        
        ### Args:
        * `nombre_bd` (str): Nombre de la base de datos a la que se quiere conectar.
        '''
        
        self.conexion.cerrar_conexion()

        self.conexion.db_name = nombre_bd
        self.conexion.conexion = None

        self.conexion.conectar_servidor()

        sql = self.conexion.ejecutar_script_sql("SELECT current_database();")
        print(f"Se conectó a la base de datos '{sql[0][0]}'")

    def cerrar_sesion(self):
        ''' 
        '''
        self.conexion.cerrar_conexion()
        print("Se cerro sesion con la conexion establecida")


    def obtener_cursor(self):
        return self.conexion