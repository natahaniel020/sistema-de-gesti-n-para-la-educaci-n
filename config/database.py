"""
Configuración y manejo de conexión a base de datos usando PyMySQL
"""

import pymysql
from pymysql import MySQLError
from utils.exceptions import DatabaseConnectionError, DatabaseOperationError


class DatabaseConnection:
    """Clase para manejar la conexión a la base de datos MySQL con PyMySQL"""

    def __init__(self):
        # Atributos principales de la conexión
        self.connection = None  # Objeto de conexión a MySQL
        self.cursor = None      # Cursor principal para ejecutar consultas
        
        # Configuración de conexión a la base de datos
        self.config = {
            'host': 'localhost',
            'database': 'gestion_academica',
            'user': 'root',
            'password': '24284240',
            'autocommit': False,  # Se maneja manualmente commit/rollback

        # CAMBIO 1: Charset para evitar problemas de codificación y collation
            'charset': 'utf8mb4',
            'use_unicode': True,

        # CAMBIO 2: Cursor tipo diccionario (resultados como dict en lugar de tuplas)
            'cursorclass': pymysql.cursors.DictCursor 
    }

    def connect(self):
        """Establece conexión con la base de datos"""
        try:
            # Solo crea la conexión si aún no existe (patrón lazy connection)
            if self.connection is None:
                self.connection = pymysql.connect(**self.config)
                self.cursor = self.connection.cursor()
            return True
        except MySQLError as e:
            # Se encapsula el error en una excepción personalizada
            raise DatabaseConnectionError(f"Error conectando a la base de datos: {e}")

    def disconnect(self):
        """Cierra la conexión con la base de datos"""
        try:
            # Cierra primero el cursor si existe
            if self.cursor:
                self.cursor.close()
                self.cursor = None

            # Luego cierra la conexión
            if self.connection:
                self.connection.close()
                self.connection = None

        except MySQLError as e:
            # Aquí no se lanza excepción, solo se imprime el error
            print(f"Error al cerrar conexión: {e}")

    def test_connection(self):
        """Prueba la conexión a la base de datos"""
        try:
            # Intenta conectarse y ejecutar una consulta simple
            self.connect()
            self.cursor.execute("SELECT 1")
            result = self.cursor.fetchone()

            # Retorna True si la consulta devuelve algo
            return result is not None

        except Exception:
            # Si ocurre cualquier error, se considera fallo de conexión
            return False

    # En config/database.py dentro de la clase DatabaseConnection

    def call_procedure(self, procedure_name, parameters=None, fetch=True):
        """
        Ejecuta un procedimiento almacenado
        """
        cursor = None
        try:
            # CORRECCIÓN: Se usa un cursor tipo DictCursor explícitamente
            cursor = self.connection.cursor(pymysql.cursors.DictCursor)
        
            # Llamada al procedimiento almacenado
            if parameters:
                # callproc permite pasar parámetros (incluyendo OUT)
                cursor.callproc(procedure_name, parameters)
            else:
                cursor.callproc(procedure_name)
            
            results = None

            if fetch:
                # IMPORTANTE: PyMySQL requiere fetchall después de callproc
                results = cursor.fetchall()
        
            # Se confirma la transacción explícitamente
            self.connection.commit()

            # Se cierra el cursor local
            cursor.close()

            # Retorna estado y resultados
            return True, results

        except Exception as e:
            # Manejo de errores: cerrar cursor y hacer rollback
            if cursor:
                cursor.close()

            if self.connection:
                self.connection.rollback()

            print(f"Error en DatabaseConnection.call_procedure: {e}")
            return False, None
    
    def execute_query(self, query, parameters=None):
        """
        Ejecuta una consulta SQL directa
        """
        try:
            # Asegura que haya conexión activa
            self.connect()

            # Ejecuta la consulta con o sin parámetros
            if parameters:
                self.cursor.execute(query, parameters)
            else:
                self.cursor.execute(query)

            # Retorna todos los resultados
            return self.cursor.fetchall()

        except MySQLError as e:
            # En caso de error, revierte cambios
            if self.connection:
                self.connection.rollback()

            # Lanza excepción personalizada
            raise DatabaseOperationError(f"Error ejecutando consulta: {e}")

    def commit(self):
        """Confirma las transacciones pendientes"""
        if self.connection:
            self.connection.commit()

    def rollback(self):
        """Revierte las transacciones pendientes"""
        if self.connection:
            self.connection.rollback()

    def is_connected(self):
        """Verifica si la conexión está activa"""
        return self.connection is not None