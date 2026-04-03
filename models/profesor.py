"""
Modelo para la entidad Profesor
Corregido: field_mapping con numeración correcta (15 campos),
eliminado commit duplicado, _format_entity_data sin field_mapping.
"""

from models.base_model import BaseModel
from utils.exceptions import EntityNotFoundError, DatabaseOperationError


class Profesor(BaseModel):
    """
    Modelo de acceso a datos para la entidad Profesor.

    Responsabilidades:
    - Ejecutar procedimientos almacenados (SP)
    - Encapsular acceso a base de datos
    - Retornar datos en formato consistente (dict)
    """

    def __init__(self, db_connection):
        # Inicialización del modelo base
        super().__init__(db_connection)

        # Nombre de tabla (referencial)
        self.table_name = "profesor"

        # Nombre lógico de la entidad
        self.entity_name = "Profesor"

        # CORRECCIÓN:
        # Lista completa de campos (15) en orden lógico/documental
        # NOTA: el orden real lo define el SP, no este arreglo
        self.field_mapping = [
            'codigo_empleado',      # 1
            'nombres',              # 2
            'apellidos',            # 3
            'documento_identidad',  # 4
            'fecha_nacimiento',     # 5
            'direccion',            # 6
            'correo_institucional', # 7
            'nivel_formacion',      # 8
            'especialidad',         # 9
            'anios_experiencia',    # 10
            'fecha_contratacion',   # 11
            'tipo_contrato',        # 12
            'departamento',         # 13
            'telefono',             # 14
            'fotografia'            # 15
        ]

    def create(self, **kwargs):
        """Crea un nuevo profesor"""
        try:
            # Construcción de parámetros en el orden esperado por el SP
            parameters = (
                kwargs.get('codigo_empleado'),
                kwargs.get('nombres'),
                kwargs.get('apellidos'),
                kwargs.get('documento_identidad'),
                kwargs.get('fecha_nacimiento'),
                kwargs.get('direccion'),
                kwargs.get('correo_institucional'),
                kwargs.get('nivel_formacion'),
                kwargs.get('especialidad'),
                kwargs.get('anios_experiencia'),
                kwargs.get('fecha_contratacion'),
                kwargs.get('tipo_contrato'),
                kwargs.get('departamento'),
                kwargs.get('telefono'),
                kwargs.get('fotografia')
            )

            # CORRECCIÓN:
            # - No se realiza commit manual
            # - La transacción se maneja en la capa de conexión
            self.call_procedure("sp_profesor_insertar", parameters, fetch=False)

            return True

        except Exception as e:
            # Encapsulación de errores técnicos
            raise DatabaseOperationError(f"Error al crear profesor: {str(e)}")

    def get_by_id(self, codigo_empleado):
        """Obtiene un profesor por su código de empleado"""
        # Llamada al procedimiento almacenado
        results = self.call_procedure(
            "sp_profesor_obtener_por_id",
            (codigo_empleado,)
        )

        # Validación de existencia
        if not results:
            raise EntityNotFoundError(self.entity_name, codigo_empleado)

        # DictCursor ya devuelve dict → solo copia defensiva
        return self._format_entity_data(results[0])

    def get_all(self):
        """Obtiene la lista completa de profesores"""
        # Consulta completa vía SP
        results = self.call_procedure("sp_profesor_obtener_todos")

        # Transformación uniforme de resultados
        return [self._format_entity_data(row) for row in results]

    def update(self, codigo_empleado, **kwargs):
        """Actualiza datos del profesor"""
        try:
            # Construcción de parámetros para el SP de actualización
            parameters = (
                codigo_empleado,
                kwargs.get('nombres'),
                kwargs.get('apellidos'),
                kwargs.get('documento_identidad'),
                kwargs.get('fecha_nacimiento'),
                kwargs.get('direccion'),
                kwargs.get('correo_institucional'),
                kwargs.get('nivel_formacion'),
                kwargs.get('especialidad'),
                kwargs.get('anios_experiencia'),
                kwargs.get('fecha_contratacion'),
                kwargs.get('tipo_contrato'),
                kwargs.get('departamento'),
                kwargs.get('telefono'),
                kwargs.get('fotografia')
            )

            # CORRECCIÓN:
            # - Eliminado commit duplicado
            # - Uso de método centralizado
            self.call_procedure("sp_profesor_actualizar", parameters, fetch=False)

            return True

        except Exception as e:
            raise DatabaseOperationError(
                f"Error al actualizar profesor {codigo_empleado}: {str(e)}"
            )

    def delete(self, codigo_empleado):
        """Elimina un profesor"""
        try:
            # Ejecución del SP de eliminación
            self.call_procedure(
                "sp_profesor_eliminar",
                (codigo_empleado,),
                fetch=False
            )

            return True

        except Exception as e:
            raise DatabaseOperationError(
                f"Error al eliminar profesor {codigo_empleado}: {str(e)}"
            )