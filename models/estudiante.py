"""
Modelo para la entidad Estudiante
Corregido: eliminado commit duplicado (ya lo hace database.py),
_format_entity_data sin field_mapping (DictCursor).
"""

from models.base_model import BaseModel
from utils.exceptions import EntityNotFoundError, DatabaseOperationError


class Estudiante(BaseModel):
    """
    Modelo de acceso a datos para la entidad Estudiante.

    Responsabilidades:
    - Ejecutar procedimientos almacenados (SP)
    - Transformar resultados de la base de datos
    - Encapsular errores técnicos en excepciones del dominio
    """

    def __init__(self, db_connection):
        # Inicialización del modelo base con la conexión
        super().__init__(db_connection)

        # Nombre de tabla (referencial)
        self.table_name = "estudiante"

        # Nombre lógico de la entidad
        self.entity_name = "Estudiante"

        # Referencia documental del orden de columnas esperado por el SP
        # NOTA: no se usa para mapear, solo como guía
        self.field_mapping = [
            'numero_matricula', 'nombres', 'apellidos',
            'documento_identidad', 'fecha_nacimiento', 'direccion',
            'correo_electronico', 'nombre_tutor', 'contacto_emergencia',
            'fecha_ingreso', 'telefono', 'fotografia'
        ]

    def create(self, **kwargs):
        """Crea un nuevo estudiante"""
        try:
            # Construcción de parámetros en el orden requerido por el SP
            parameters = (
                kwargs.get('numero_matricula'),
                kwargs.get('nombres'),
                kwargs.get('apellidos'),
                kwargs.get('documento_identidad'),
                kwargs.get('fecha_nacimiento'),
                kwargs.get('direccion'),
                kwargs.get('correo_electronico'),
                kwargs.get('nombre_tutor'),
                kwargs.get('contacto_emergencia'),
                kwargs.get('fecha_ingreso'),
                kwargs.get('telefono'),
                kwargs.get('fotografia')
            )

            # CORRECCIÓN:
            # - No se hace commit manual
            # - La transacción se gestiona en la capa de conexión
            self.call_procedure("sp_estudiante_insertar", parameters, fetch=False)

            return True

        except Exception as e:
            # Encapsula error técnico
            raise DatabaseOperationError(f"No se pudo crear el estudiante: {str(e)}")

    def get_by_id(self, numero_matricula):
        """Obtiene un estudiante por su número de matrícula"""
        # Llamada al procedimiento almacenado
        results = self.call_procedure(
            "sp_estudiante_obtener_por_id",
            (numero_matricula,)
        )

        # Validación de existencia
        if not results:
            raise EntityNotFoundError(self.entity_name, numero_matricula)

        # DictCursor ya devuelve dict → solo copia defensiva
        return self._format_entity_data(results[0])

    def get_all(self):
        """Obtiene todos los estudiantes"""
        # Consulta completa vía SP
        results = self.call_procedure("sp_estudiante_obtener_todos")

        # Transformación uniforme de cada fila
        return [self._format_entity_data(row) for row in results]

    def update(self, numero_matricula, **kwargs):
        """Actualiza un estudiante existente"""
        try:
            # Construcción de parámetros en orden esperado por el SP
            parameters = (
                numero_matricula,
                kwargs.get('nombres'),
                kwargs.get('apellidos'),
                kwargs.get('documento_identidad'),
                kwargs.get('fecha_nacimiento'),
                kwargs.get('direccion'),
                kwargs.get('correo_electronico'),
                kwargs.get('nombre_tutor'),
                kwargs.get('contacto_emergencia'),
                kwargs.get('fecha_ingreso'),
                kwargs.get('telefono'),
                kwargs.get('fotografia')
            )

            # CORRECCIÓN:
            # - Eliminado commit duplicado
            # - Se usa método centralizado
            self.call_procedure("sp_estudiante_actualizar", parameters, fetch=False)

            return True

        except Exception as e:
            raise DatabaseOperationError(
                f"Error al actualizar el estudiante {numero_matricula}: {str(e)}"
            )

    def delete(self, numero_matricula):
        """Elimina un estudiante"""
        try:
            # Ejecución del SP de eliminación
            self.call_procedure(
                "sp_estudiante_eliminar",
                (numero_matricula,),
                fetch=False
            )

            return True

        except Exception as e:
            raise DatabaseOperationError(
                f"Error al eliminar el estudiante {numero_matricula}: {str(e)}"
            )