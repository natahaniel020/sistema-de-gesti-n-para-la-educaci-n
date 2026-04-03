"""
Controlador para la gestión de Profesores
Corregido: eliminados prints de debug en _postprocess_get_data,
safe_int() delegado a BaseController.
"""

import re
from controllers.base_controller import BaseController
from utils.exceptions import ValidationError


class ProfesorController(BaseController):
    """
    Controlador específico para la entidad Profesor.

    Responsabilidades:
    - Validar datos de entrada
    - Limpiar y normalizar información
    - Aplicar reglas de negocio
    - Adaptar datos para la vista
    """

    def __init__(self, profesor_model):
        # Inicialización del controlador base con el modelo correspondiente
        super().__init__(profesor_model)

        # Campos obligatorios para la creación de un profesor
        self.required_fields = [
            'codigo_empleado', 'nombres', 'apellidos', 'documento_identidad',
            'fecha_nacimiento', 'correo_institucional', 'nivel_formacion',
            'fecha_contratacion', 'tipo_contrato', 'departamento'
        ]

        # Campos considerados como texto para limpieza (strip, normalización)
        self.string_fields = [
            'codigo_empleado', 'nombres', 'apellidos', 'documento_identidad',
            'direccion', 'correo_institucional', 'nivel_formacion',
            'especialidad', 'tipo_contrato', 'departamento', 'telefono'
        ]

    def _get_primary_key_field(self):
        """
        Define la clave primaria lógica de la entidad.
        """
        return "codigo_empleado"

    # =========================================================================
    # HOOKS
    # =========================================================================

    def _preprocess_create_data(self, **kwargs):
        """
        Preprocesamiento antes de crear:
        - Delega toda la validación a un método centralizado
        """
        return self._validate_and_clean_profesor_data(kwargs, is_update=False)

    def _preprocess_update_data(self, entity_id, **kwargs):
        """
        Preprocesamiento antes de actualizar:
        - Cambia comportamiento de validación según flag is_update
        """
        return self._validate_and_clean_profesor_data(kwargs, is_update=True)

    def _preprocess_delete(self, entity_id):
        """
        Hook previo a eliminación (no implementado).
        """
        pass

    def _postprocess_create(self, entity_id, **kwargs):
        """
        Hook posterior a creación (no implementado).
        """
        pass

    def _postprocess_update(self, entity_id, **kwargs):
        """
        Hook posterior a actualización (no implementado).
        """
        pass

    def _postprocess_delete(self, entity_id):
        """
        Hook posterior a eliminación (no implementado).
        """
        pass

    def _postprocess_get_data(self, entity_data):
        """
        Transforma datos para la vista.

        CORRECCIÓN:
        - Se eliminaron prints de debug (evita fuga de información y ruido en logs)

        Agrega:
        - nombre_completo
        - display_name (útil para listas o selects)
        """
        if not entity_data:
            return entity_data

        # Construcción de nombre completo
        nombres = entity_data.get('nombres', '')
        apellidos = entity_data.get('apellidos', '')
        entity_data['nombre_completo'] = f"{apellidos}, {nombres}"

        # Identificador visual combinado
        codigo = entity_data.get('codigo_empleado', 'S/C')
        entity_data['display_name'] = f"{codigo} - {entity_data['nombre_completo']}"

        return entity_data

    # =========================================================================
    # VALIDACIÓN Y LIMPIEZA
    # =========================================================================

    def _validate_and_clean_profesor_data(self, data, is_update=False):
        """
        Método central de validación y limpieza.

        Maneja los ~15 campos del modelo profesor.

        Parámetros:
        - data: diccionario de entrada
        - is_update: indica si es actualización (afecta validación de requeridos)
        """

        # En actualización:
        # - codigo_empleado no viene en el body (viene como parámetro externo)
        campos_a_validar = self.required_fields.copy()

        if is_update and 'codigo_empleado' in campos_a_validar:
            campos_a_validar.remove('codigo_empleado')

        # 1. Validación de campos obligatorios
        self.validate_required_fields(data, campos_a_validar)

        # 2. Limpieza de strings (trim, normalización de vacíos a None)
        data = self.clean_string_data(data, self.string_fields)

        # 3. Normalización de nombres (capitalización)
        if data.get('nombres'):
            data['nombres'] = data['nombres'].title()

        if data.get('apellidos'):
            data['apellidos'] = data['apellidos'].title()

        # 4. Validación de formato de correo institucional
        correo = data.get('correo_institucional', '')

        # Regex básica (suficiente para validación general)
        if correo and not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            raise ValidationError("Correo Institucional", "el formato es inválido")

        # 5. Conversión segura de años de experiencia
        # CORRECCIÓN: evita errores por valores no numéricos
        data['anios_experiencia'] = self.safe_int(data.get('anios_experiencia', 0))

        # 6. Manejo de fotografía
        # Normaliza valores vacíos a None para consistencia en BD
        if 'fotografia' not in data or data.get('fotografia') == "":
            data['fotografia'] = None

        return data