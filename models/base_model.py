"""
Clase base para todos los modelos de la aplicación
Corregida para PyMySQL con DictCursor y Stored Procedures
"""

from abc import ABC, abstractmethod
from utils.exceptions import EntityNotFoundError, DatabaseOperationError


class BaseModel(ABC):
    """
    Clase abstracta base para todos los modelos.

    Define:
    - Contrato CRUD obligatorio
    - Métodos comunes de acceso a datos
    - Manejo unificado de errores
    """

    def __init__(self, db_connection):
        # Instancia de conexión a base de datos (DatabaseConnection)
        self.db = db_connection

        # Nombre de la tabla (referencial, no siempre usado si se trabaja con SP)
        self.table_name = None

        # Nombre lógico de la entidad (para mensajes y logs)
        self.entity_name = "Entidad"

        # Mapeo de campos (se mantiene como referencia documental)
        self.field_mapping = []

    def call_procedure(self, procedure_name, parameters=None, fetch=True):
        """
        Ejecuta un procedimiento almacenado.

        IMPORTANTE:
        - Usa DictCursor → resultados ya vienen como dict
        - Centraliza el manejo de errores de base de datos

        Args:
            procedure_name (str): Nombre del procedimiento almacenado
            parameters (tuple): Parámetros de entrada
            fetch (bool):
                - True → se esperan resultados (SELECT)
                - False → no se esperan resultados (INSERT/UPDATE/DELETE)

        Returns:
            list[dict] | True
        """
        try:
            # Delegación directa a la capa de conexión
            success, results = self.db.call_procedure(
                procedure_name,
                parameters,
                fetch=fetch
            )

            # Si la capa DB reporta fallo, se traduce a excepción
            if not success:
                raise DatabaseOperationError(
                    f"La base de datos reportó un error en: {procedure_name}"
                )

            # Para operaciones sin retorno (INSERT/UPDATE/DELETE)
            if not fetch:
                return True

            # Asegura consistencia: siempre retorna lista
            return results if results is not None else []

        except DatabaseOperationError:
            # No se altera la excepción si ya es del dominio
            raise

        except Exception as e:
            # Se encapsula cualquier error técnico
            raise DatabaseOperationError(
                f"Error técnico ejecutando {procedure_name}: {str(e)}"
            )

    def execute_query(self, query, parameters=None):
        """
        Ejecuta una consulta SQL directa.

        Uso típico:
        - Consultas ad-hoc
        - Debug o utilidades
        - Casos donde no hay SP
        """
        try:
            return self.db.execute_query(query, parameters)

        except Exception as e:
            raise DatabaseOperationError(f"Error en consulta SQL: {str(e)}")

    # =========================================================================
    # CONTRATO CRUD (OBLIGATORIO PARA MODELOS HIJOS)
    # =========================================================================

    @abstractmethod
    def create(self, **kwargs):
        """Debe implementar la lógica de creación"""
        pass

    @abstractmethod
    def get_by_id(self, entity_id):
        """Debe retornar una entidad o lanzar EntityNotFoundError"""
        pass

    @abstractmethod
    def update(self, entity_id, **kwargs):
        """Debe actualizar una entidad existente"""
        pass

    @abstractmethod
    def delete(self, entity_id):
        """Debe eliminar una entidad"""
        pass

    @abstractmethod
    def get_all(self):
        """Debe retornar todas las entidades"""
        pass

    def exists(self, entity_id):
        """
        Verifica si una entidad existe.

        Estrategia:
        - Reutiliza get_by_id (evita duplicar lógica)
        - Usa excepción como control de flujo
        """
        try:
            self.get_by_id(entity_id)
            return True

        except EntityNotFoundError:
            return False

    def _format_entity_data(self, raw_data):
        """
        CORRECCIÓN PRINCIPAL:
        - DictCursor ya devuelve dict → no se requiere transformación
        - Se elimina necesidad de zip con field_mapping

        field_mapping queda como documentación del modelo.

        Args:
            raw_data (dict): Fila obtenida desde la base de datos

        Returns:
            dict: Copia del diccionario original
        """
        if not raw_data:
            return {}

        # Copia defensiva para evitar efectos secundarios
        return dict(raw_data)