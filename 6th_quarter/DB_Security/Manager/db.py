import os, sys

sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(__file__))
))

from Connection.connect import Conexion

class database_manager(Conexion):

    def __init__(self,conexion = None):
        ''' 

        ### Returns
        * `conexion`: Retorna el objeto con el cuál se hizo la conexion.
        '''
        super().__init__()

        self.conectar_servidor()
        print("database_manager iniciado")

    # ===== Base de Datos
    def crear_base_datos(self,nombre_bd:str):
        ''' Crea una nueva base de datos. '''
        self.ejecutar_query(f"CREATE DATABASE {nombre_bd};")
        print(f"Se creó la base de datos '{nombre_bd}'")

    def eliminar_base_datos(self,nombre_bd:str):
        ''' Elimina una base de datos. '''
        self.ejecutar_query(f"DROP DATABASE {nombre_bd};")
        print(f"Se eliminó la base de datos '{nombre_bd}'")

    def listar_bds(self):
        ''' Lista las bases de datos disponibles. 
        
        ### Returns:
        * list (str): Lista con las bases de datos disponibles.
        '''
        dbs = self.ejecutar_query("SELECT datname FROM pg_database WHERE datistemplate = false;")
        print(f"Las bases de datos disponibles son {dbs}")
        return dbs
    
    def conectar_bd(self,nombre_bd:str):
        ''' Se desconecta del servidor actual para cambiar la conexion de base de datos.
        
        ### Args:
        * `nombre_bd` (str): Nombre de la base de datos a la que se quiere conectar.
        '''
        
        self.cerrar_conexion()

        self.db_name = nombre_bd
        self.conexion = None

        self.conectar_servidor()

        sql = self.ejecutar_query("SELECT current_database();")
        print(f"Se conectó a la base de datos '{sql[0][0]}'")

    # ===== Tablas
    def crear_tabla_dummy(self):
        ''' Crea una tabla dummy llamada 'students' y la llena con 3 datos ficticios.

        ### Args:
        * `nombre_bd` (str): Nombre de la base de datos a la que se quiere conectar.
        '''

        sql = """
        CREATE TABLE students (
            student_id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(100),
            sex VARCHAR(1),
            ip VARCHAR(15) DEFAULT 'active'
        );
        """
        self.ejecutar_query(sql)
        print("Se genero la tabla dummy: 'students'")

        sql = """
        INSERT INTO students (first_name, last_name, email, sex, ip)
        VALUES
            ('Diego','Monroy','2109110@upy.edu.mx','M','127.0.0.0'),
            ('Valeria','Dominguez','2109111@upy.edu.mx','F','127.0.0.1'),
            ('Eduardo','Garcia','2109112@upy.edu.mx','M','127.0.0.2');
        """
        self.ejecutar_query(sql)
        print("Se insertaron 3 alumnos ficticios a la tabla: 'students'")

    def eliminar_tabla(self,nombre_tabla:str):
        ''' Elimina una tabla de la base de datos conectada.

        ### Args:
        * `nombre_tabla` (str): Nombre de la tabla a la que se quiere eliminar.
        '''
        sql = f"DROP TABLE {nombre_tabla};"
        self.ejecutar_query(sql)
        print(f"Se eliminó la tabla: '{nombre_tabla}'")

    def listar_tablas(self):
        ''' Lista las tablas disponibles de la base de datos conectada. '''
        sql = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE';
        """
        tablas = self.ejecutar_query(sql)
        print(f"Las tablas disponibles son {tablas}")

    def mostrar_datos_tabla(self,nombre_tabla:str):
        ''' Imprime toda la información de una tabla. '''
        try:
            print(f"TABLE {nombre_tabla};")
            query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{nombre_tabla}'"
            sql = self.ejecutar_query(query)
            columns = [row[0] for row in sql]
            len_columns = {}
            for index,column in enumerate(columns):
                if index == len(columns) - 1: string = f" {column} "
                else: string = f" {column} |"
                len_columns[index] = int(len(string))
                print(string,end='')
            print('')
            for column_index in len_columns:
                if column_index == len(columns) - 1: string = f"{'-'*int(len_columns[column_index])}"
                else: string = f"{'-'*int(len_columns[column_index]-1)}+"
                print(string,end='')
            print('')

            query = f"SELECT * FROM {nombre_tabla};"
            sql = self.ejecutar_query(query)
            for row in sql:
                for index,value in enumerate(row):
                    value = str(value)
                    if index == len(columns) - 1: string = f" {value[:int(len_columns[index]-1)]}"
                    else: string = f" {value[:int(len_columns[index]-3)]} |"
                    print(string,end='')
                print('')

        except Exception as ex:
            ex_str = str(ex).strip().lower()
            if 'no results to fetch' in ex_str: print(f"Se intentó buscar la tabla '{nombre_tabla}', pero no fue localizada")

            
        

    # ===== Conexion
    def cerrar_sesion(self):
        ''' Se cierra sesion con la conexion establecida '''
        self.cerrar_conexion()
        print("Se cerro sesion con la conexion establecida")