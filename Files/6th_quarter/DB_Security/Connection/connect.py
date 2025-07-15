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
    
    def ejecutar_query(self,query:str,args:tuple = None):
        ''' Ejecuta una sentencia SQL en la base de datos conectada 
        
        ## Args: 
        * query (str): Sentencia en SQL a ejecutar en la base de datos.
        * args (tuple, opcional): Tupla con los argumentos a pasar en el query. Recomendado para sanitizar consultas.

        ## Returns: 
        * results (str|list): Si el sql fue de tipo "SELECT", devuelve los datos buscados.
        '''
        try:
            if not(args):
                self.cursor.execute(query)
            else:
                self.cursor.execute(query,args)
        except Exception as e:
            self.conexion.rollback()
        finally:
            query = query.strip().upper()
            if "SELECT" in query.strip().upper():
                try:
                    return self.cursor.fetchall()
                except Exception as ex:
                    return f"Ocurrio un error: {ex}"

            # return self.cursor.fetchall()
            
    def obtener_conexion(self):
        ''' Retorna el objeto de conexion a la base de datos. '''
        return self.conexion
    
    def cerrar_conexion(self):
        ''' Cierra el cursor y la conexión '''
        if self.cursor:   self.cursor.close()
        if self.conexion: self.conexion.close()
