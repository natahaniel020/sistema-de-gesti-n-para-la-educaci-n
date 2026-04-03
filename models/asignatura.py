"""
Modelo para la entidad Asignatura
Corregido: usa self.call_procedure() en todos los métodos,
_format_entity_data sin field_mapping (DictCursor), y sin commit duplicado.
"""

from models.base_model import BaseModel
from utils.exceptions import DatabaseOperationError, EntityNotFoundError


class Asignatura(BaseModel):
    """
    Modelo de acceso a datos para la entidad Asignatura.

    Responsabilidades:
    - Ejecutar procedimientos almacenados (SP)
    - Transformar resultados de BD en estructuras utilizables
    - Encapsular errores de base de datos
    """

    def __init__(self, db_connection):
        # Inicializa el modelo base con la conexión a BD
        super().__init__(db_connection)

        # Nombre de tabla (referencial, no crítico si todo va por SP)
        self.table_name = "asignatura"

        # Nombre lógico de la entidad
        self.entity_name = "Asignatura"

        # Referencia documental del orden de campos
        # NOTA: el orden real lo define el procedimiento almacenado
        self.field_mapping = [
            'codigo_asignatura', 'nombre', 'area_conocimiento',
            'horas_teoricas', 'horas_practicas', 'creditos_academicos',
            'objetivos_generales', 'objetivos_especificos',
            'requisitos_previos', 'bibliografia'
        ]

    def create(self, **kwargs):
        """Inserta una nueva asignatura"""
        try:
            # Construcción de parámetros en el orden esperado por el SP
            parameters = (
                kwargs.get('codigo_asignatura'),
                kwargs.get('nombre'),
                kwargs.get('area_conocimiento'),
                kwargs.get('horas_teoricas', 0),
                kwargs.get('horas_practicas', 0),
                kwargs.get('creditos_academicos'),
                kwargs.get('objetivos_generales'),
                kwargs.get('objetivos_especificos'),
                kwargs.get('requisitos_previos'),
                kwargs.get('bibliografia')
            )

            # CORRECCIÓN:
            # - Se usa método centralizado del BaseModel
            # - Manejo de commit/rollback ya está encapsulado
            self.call_procedure("sp_asignatura_insertar", parameters, fetch=False)

            return True

        except Exception as e:
            # Encapsula cualquier error en excepción del dominio
            raise DatabaseOperationError(f"Error al crear asignatura: {str(e)}")

    def get_by_id(self, codigo_asignatura):
        """Obtiene una asignatura por su código"""
        # Llamada al SP correspondiente
        results = self.call_procedure(
            "sp_asignatura_obtener_por_id",
            (codigo_asignatura,)
        )

        # Validación de existencia
        if not results:
            raise EntityNotFoundError(self.entity_name, codigo_asignatura)

        # CORRECCIÓN:
        # - No se hace mapeo manual
        # - DictCursor ya devuelve dict
        return self._format_entity_data(results[0])

    def get_all(self):
        """Obtiene todas las asignaturas"""
        # Obtiene lista completa desde el SP
        results = self.call_procedure("sp_asignatura_obtener_todos")

        # Se formatea cada fila (copia defensiva)
        return [self._format_entity_data(row) for row in results]

    def update(self, codigo_asignatura, **kwargs):
        """Actualiza una asignatura existente"""
        try:
            # Función local para conversión segura a entero
            # (protege contra strings no numéricos)
            def safe_int(key):
                val = kwargs.get(key, 0)
                if isinstance(val, str) and not val.isdigit():
                    return 0
                return int(val) if val is not None else 0

            # Construcción de parámetros para el SP
            parameters = (
                codigo_asignatura,
                kwargs.get('nombre'),
                kwargs.get('area_conocimiento'),
                safe_int('horas_teoricas'),
                safe_int('horas_practicas'),
                safe_int('creditos_academicos'),
                kwargs.get('objetivos_generales'),
                kwargs.get('objetivos_especificos'),
                kwargs.get('requisitos_previos'),
                kwargs.get('bibliografia')
            )

            # Ejecución del procedimiento de actualización
            self.call_procedure("sp_asignatura_actualizar", parameters, fetch=False)

            return True

        except Exception as e:
            raise DatabaseOperationError(f"Error al actualizar asignatura: {str(e)}")

    def delete(self, codigo_asignatura):
        """Elimina una asignatura"""
        try:
            # Llamada al SP de eliminación
            self.call_procedure(
                "sp_asignatura_eliminar",
                (codigo_asignatura,),
                fetch=False
            )

            return True

        except Exception as e:
            raise DatabaseOperationError(f"Error al eliminar asignatura: {str(e)}")