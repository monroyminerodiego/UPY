from typing import Literal
import os, sys
sys.path.append(os.path.join(
    os.path.dirname(os.path.dirname(__file__))
))
from Manager.db import database_manager

class AC09:

    def __init__(self,forma_ejecucion:Literal['poner y quitar','solo poner','solo quitar'] = 'poner y quitar'):
        self.conexion = None
        self.forma_ejecucion = forma_ejecucion

    def api_configuration(self):
        print(f"\n{'='*5} API Configuration")
        self.conexion = database_manager()
        self.conexion.crear_base_datos('project_team4_6b')
        self.conexion.conectar_bd('project_team4_6b')

    def create_tables(self):
        print(f"\n{'='*5} Creating tables")
        query = """ CREATE TABLE Alumnos (
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

        query = """ CREATE TABLE Empleados (
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

        query = """ CREATE TABLE Maestros (
            empleado_id INT PRIMARY KEY,
            materia_id INT,
            horario VARCHAR(100),
            plan_estudios_id INT,
            FOREIGN KEY (empleado_id) REFERENCES Empleados(empleado_id),
            FOREIGN KEY (materia_id) REFERENCES Materias(materia_id),
            FOREIGN KEY (plan_estudios_id) REFERENCES Planes_de_Estudio(plan_estudios_id)
        );
        """
        self.conexion.ejecutar_query(query)
        print("Tabla 'Maestros' creada...")

        query = """ CREATE TABLE Materias (
            materia_id INT PRIMARY KEY,
            nombre VARCHAR(100),
            descripcion TEXT
        );
        """
        self.conexion.ejecutar_query(query)
        print("Tabla 'Materias' creada...")

        query = """ CREATE TABLE Planes_de_Estudio (
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

        query = """ CREATE TABLE Control_Escolar (
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

        query = """ CREATE TABLE Finanzas (
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

        query = """ CREATE TABLE Nomina (
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

        query = """ CREATE TABLE Historial_de_Pagos (
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

        query = """ CREATE TABLE Usuarios (
            usuario_id INT PRIMARY KEY,
            nombre_usuario VARCHAR(50),
            contraseña VARCHAR(255),
            rol VARCHAR(20)
        );
        """
        self.conexion.ejecutar_query(query)
        print("Tabla 'Usuarios' creada...")

    def desmontar_bd(self):
        ''''''
        self.conexion.conectar_bd('postgres')
        self.conexion.eliminar_base_datos('project_team4_6b')

    def main(self):
        ''' 
        '''

        self.api_configuration()

        if 'poner' in self.forma_ejecucion: self.create_tables()

        if 'quitar' in self.forma_ejecucion: self.desmontar_bd()