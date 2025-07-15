from typing import Literal
import os, sys
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(__file__))
))
from Manager.db import database_manager

class AC09:

    def __init__(self,forma_ejecucion:Literal['poner y quitar','solo poner','solo quitar'] = 'poner y quitar',
                 user:str = 'postgres',password:str = 'postgres', db_name:str = 'postgres',
                 host:str = 'localhost', port:int = 5432):
        self.conexion        = None
        self.forma_ejecucion = forma_ejecucion
        self.user            = user
        self.password        = password
        self.db_name         = db_name
        self.host            = host
        self.port            = port

    def api_configuration(self):
        print(f"\n{'='*5} Creando base de datos...")
        self.conexion = database_manager(
            user     = self.user,
            password = self.password,
            db_name  = self.db_name,
            host     = self.host,
            port     = self.port,
            conexion = self.conexion,

        )
        self.conexion.crear_base_datos('project_team4_6b')
        self.conexion.conectar_bd('project_team4_6b')

    def create_tables(self):
        print(f"\n{'='*5} Creando tablas...")
        query = """ CREATE TABLE alumnos (
            alumno_id INT PRIMARY KEY,
            nombre VARCHAR(50),
            apellido_paterno VARCHAR(50),
            apellido_materno VARCHAR(50),
            fecha_nacimiento DATE,
            sexo CHAR(1),
            direccion VARCHAR(255),
            telefono VARCHAR(20),
            email VARCHAR(100),
            grado_actual VARCHAR(10),
            grupo_actual VARCHAR(10),
            estatus VARCHAR(20)
        );
        """
        self.conexion.ejecutar_query(query)
        print("Tabla 'Alumnos' creada...")

        query = """ CREATE TABLE empleados (
            empleado_id INT PRIMARY KEY,
            nombre VARCHAR(50),
            apellido_paterno VARCHAR(50),
            apellido_materno VARCHAR(50),
            fecha_nacimiento DATE,
            sexo CHAR(1),
            direccion VARCHAR(255),
            telefono VARCHAR(20),
            email VARCHAR(100),
            puesto VARCHAR(50),
            fecha_ingreso DATE,
            salario DECIMAL(10, 2)
        );
        """
        self.conexion.ejecutar_query(query)
        print("Tabla 'Empleados' creada...")

        query = """ CREATE TABLE maestros (
            empleado_id INT PRIMARY KEY,
            materia_id INT,
            horario VARCHAR(100),
            plan_estudios_id INT
        );
        """
        self.conexion.ejecutar_query(query)
        print("Tabla 'Maestros' creada...")

        query = """ CREATE TABLE materias (
            materia_id INT PRIMARY KEY,
            nombre VARCHAR(100),
            descripcion TEXT
        );
        """
        self.conexion.ejecutar_query(query)
        print("Tabla 'Materias' creada...")

        query = """ CREATE TABLE planes_de_estudio (
            plan_estudios_id INT PRIMARY KEY,
            grado VARCHAR(10),
            materia_id INT,
            semestre INT,
            horas_semanales INT,
            FOREIGN KEY (materia_id) REFERENCES Materias(materia_id)
        );
        """
        self.conexion.ejecutar_query(query)
        print("Tabla 'Planes_de_Estudio' creada...")

        query = """ CREATE TABLE control_escolar (
            control_id INT PRIMARY KEY,
            alumno_id INT,
            materia_id INT,
            calificacion_final DECIMAL(5, 2),
            asistencia INT,
            fecha DATE,
            FOREIGN KEY (alumno_id) REFERENCES Alumnos(alumno_id),
            FOREIGN KEY (materia_id) REFERENCES Materias(materia_id)
        );
        """
        self.conexion.ejecutar_query(query)
        print("Tabla 'Control_Escolar' creada...")

        query = """ CREATE TABLE finanzas (
            factura_id INT PRIMARY KEY,
            alumno_id INT,
            monto DECIMAL(10, 2),
            concepto VARCHAR(50),
            fecha_emision DATE,
            fecha_pago DATE,
            estatus_pago VARCHAR(20),
            FOREIGN KEY (alumno_id) REFERENCES Alumnos(alumno_id)
        );
        """
        self.conexion.ejecutar_query(query)
        print("Tabla 'Finanzas' creada...")

        query = """ CREATE TABLE nomina (
            nomina_id INT PRIMARY KEY,
            empleado_id INT,
            monto_pago DECIMAL(10, 2),
            fecha_pago DATE,
            deducciones DECIMAL(10, 2),
            bonificaciones DECIMAL(10, 2),
            total_pagado DECIMAL(10, 2),
            FOREIGN KEY (empleado_id) REFERENCES Empleados(empleado_id)
        );
        """
        self.conexion.ejecutar_query(query)
        print("Tabla 'Nomina' creada...")

        query = """ CREATE TABLE historial_de_pagos (
            pago_id INT PRIMARY KEY,
            alumno_id INT,
            factura_id INT,
            empleado_id INT,
            monto_pagado DECIMAL(10, 2),
            fecha_pago DATE,
            FOREIGN KEY (alumno_id) REFERENCES Alumnos(alumno_id),
            FOREIGN KEY (factura_id) REFERENCES Finanzas(factura_id),
            FOREIGN KEY (empleado_id) REFERENCES Empleados(empleado_id)
        );
        """
        self.conexion.ejecutar_query(query)
        print("Tabla 'Historial_de_Pagos' creada...")

        query = """ CREATE TABLE usuarios (
            usuario_id INT PRIMARY KEY,
            nombre_usuario VARCHAR(50),
            contraseña VARCHAR(255),
            rol VARCHAR(20)
        );
        """
        self.conexion.ejecutar_query(query)
        print("Tabla 'Usuarios' creada...")

    def create_roles(self):
        print(f"\n{'='*5} Creando roles...")

        # ===== ADMIN
        query = """CREATE ROLE admin WITH LOGIN PASSWORD 'admin';
        ALTER ROLE admin WITH SUPERUSER CREATEDB CREATEROLE;

        GRANT ALL PRIVILEGES ON DATABASE project_team4_6b TO admin;

        GRANT ALL PRIVILEGES ON SCHEMA public TO admin;
        GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO admin;
        GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO admin;

        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO admin;
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO admin;

        GRANT CONNECT ON DATABASE project_team4_6b TO admin;
        """
        self.conexion.ejecutar_query(query)
        print("Rol 'admin' creado... ")

        # ===== RECTOR
        query = """CREATE ROLE rector WITH LOGIN PASSWORD 'rector';
                        
        GRANT USAGE ON SCHEMA public TO rector;
        GRANT SELECT ON ALL TABLES IN SCHEMA public TO rector;
        
        ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO rector;

        GRANT CONNECT ON DATABASE project_team4_6b TO rector;
        """
        self.conexion.ejecutar_query(query)
        print("Rol 'rector' creado... ")
        
        # ===== Control Escolar
        query = """CREATE ROLE control_escolar WITH LOGIN PASSWORD 'control_escolar';
        
        GRANT USAGE ON SCHEMA public TO control_escolar;

        GRANT SELECT, INSERT, UPDATE ON TABLE public.alumnos TO control_escolar;
        GRANT SELECT, INSERT, UPDATE ON TABLE public.maestros TO control_escolar;
        GRANT SELECT, INSERT, UPDATE ON TABLE public.materias TO control_escolar;
        GRANT SELECT, INSERT, UPDATE ON TABLE public.planes_de_estudio TO control_escolar;
        GRANT SELECT, INSERT, UPDATE ON TABLE public.control_escolar TO control_escolar;
        GRANT SELECT, INSERT, UPDATE ON TABLE public.historial_de_pagos TO control_escolar;

        GRANT CONNECT ON DATABASE project_team4_6b TO control_escolar;
        """
        self.conexion.ejecutar_query(query)
        print("Rol 'control_escolar' creado... ")
        
        # ===== Finanzas
        query = """CREATE ROLE finanzas WITH LOGIN PASSWORD 'finanzas';
        GRANT CONNECT ON DATABASE project_team4_6b TO finanzas;"""
        self.conexion.ejecutar_query(query)
        
        query = """GRANT USAGE ON SCHEMA public TO finanzas;

        GRANT SELECT ON TABLE public.alumnos TO finanzas;
        GRANT SELECT ON TABLE public.empleados TO finanzas;
        GRANT SELECT ON TABLE public.maestros TO finanzas;
        GRANT SELECT ON TABLE public.finanzas TO finanzas;
        GRANT SELECT ON TABLE public.nomina TO finanzas;
        GRANT SELECT ON TABLE public.historial_de_pagos TO finanzas;"""
        self.conexion.ejecutar_query(query)
        print("Rol 'finanzas' creado... ")
        
        # ===== Maestros
        query = """CREATE ROLE maestros WITH LOGIN PASSWORD 'maestros';
        
        GRANT USAGE ON SCHEMA public TO maestros;

        GRANT SELECT, UPDATE ON TABLE public.alumnos TO maestros;
        GRANT SELECT, UPDATE ON TABLE public.maestros TO maestros;
        GRANT SELECT, UPDATE ON TABLE public.materias TO maestros;
        GRANT SELECT, UPDATE ON TABLE public.planes_de_estudio TO maestros;

        GRANT CONNECT ON DATABASE project_team4_6b TO maestros;"""
        self.conexion.ejecutar_query(query)
        print("Rol 'maestros' creado... ")
        
        # ===== Alumnos
        query = """CREATE ROLE alumnos WITH LOGIN PASSWORD 'alumnos';
        
        GRANT USAGE ON SCHEMA public TO alumnos;

        GRANT SELECT ON TABLE public.alumnos TO alumnos;
        GRANT SELECT ON TABLE public.materias TO alumnos;
        GRANT SELECT ON TABLE public.planes_de_estudio TO alumnos;
        GRANT SELECT ON TABLE public.historial_de_pagos TO alumnos;
        
        GRANT CONNECT ON DATABASE project_team4_6b TO alumnos;"""
        self.conexion.ejecutar_query(query)
        print("Rol 'alumnos' creado... ")


    def desmontar_bd(self):
        print(f"\n{'='*5} Desmontando Base de Datos...")
        
        # ===== Desmonta los roles
        for rol in ['rector','admin','control_escolar','finanzas','maestros','alumnos']:
            query = f"""REVOKE ALL ON SCHEMA public FROM {rol};
            REVOKE ALL ON ALL TABLES IN SCHEMA public FROM {rol};
            ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE SELECT ON TABLES FROM {rol};
            """
            self.conexion.ejecutar_query(query)
            query = f"DROP ROLE {rol};"
            self.conexion.ejecutar_query(query)
            print(f"Se eliminó el Rol {rol}")

        # ===== Desmonta las bd
        self.conexion.conectar_bd('postgres')
        self.conexion.eliminar_base_datos('project_team4_6b')

    def main(self):
        print(f"{'='*10} Iniciando Ejecución ({self.forma_ejecucion}) {'='*10}")

        self.api_configuration()

        if 'poner' in self.forma_ejecucion:
            self.create_tables()
            self.create_roles()

        if 'quitar' in self.forma_ejecucion: self.desmontar_bd()