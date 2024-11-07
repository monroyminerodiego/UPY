import psycopg2

class Conexion:

    def __init__(self,user:str = 'postgres',password:str = 'postgres',
                 db_name:str = 'postgres', host:str = 'localhost',
                 port:int = 5432, conexion = None):
        ''' '''
        self.user     = user
        self.password = password
        self.db_name  = db_name
        self.host     = host
        self.port     = port
        self.conexion = conexion

    def conectar_servidor(self):
        ''' Se conecta a una base de datos dados los parametros del init. (user,password,host,port) '''

        if not(self.conexion):
            self.conexion = psycopg2.connect(
                user     = self.user,
                password = self.password,
                database = self.db_name,
                host     = self.host,
                port     = self.port,
            )
            self.conexion.autocommit = True

        self.cursor = self.conexion.cursor()
    
    def ejecutar_query(self,query:str):
        ''' Ejecuta una sentencia SQL en la base de datos conectada 
        
        ## Args: 
        * query (str): Sentencia en SQL a ejecutar en la base de datos.

        ## Returns: 
        * results (str|list): Si el sql fue de tipo "SELECT", devuelve los datos buscados.
        '''
        try:
            self.cursor.execute(query)
        except Exception as e:
            self.conexion.rollback()
        finally:
            query = query.strip().upper()
            if "SELECT" in query.strip().upper():
                return self.cursor.fetchall()
            # return self.cursor.fetchall()
            
    def obtener_conexion(self):
        ''' Retorna el objeto de conexion a la base de datos. '''
        return self.conexion
    
    def cerrar_conexion(self):
        ''' Cierra el cursor y la conexión '''
        if self.cursor:   self.cursor.close()
        if self.conexion: self.conexion.close()
