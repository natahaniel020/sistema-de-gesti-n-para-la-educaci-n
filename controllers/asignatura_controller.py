"""
Controlador para la gestión de Asignaturas
Corregido: _validate_and_clean_logic ahora incluye TODOS los campos del modelo,
safe_int protegido contra strings no numéricos.
"""

from controllers.base_controller import BaseController
from utils.validators import Validator
from utils.helpers import safe_str
from utils.exceptions import ValidationError


class AsignaturaController(BaseController):
    """
    Controlador específico para la entidad Asignatura.

    Responsabilidades:
    - Validar datos de entrada
    - Limpiar/normalizar información
    - Aplicar reglas de negocio
    - Preparar datos antes de enviarlos al modelo
    """

    def __init__(self, model):
        # Inicializa el controlador base con el modelo correspondiente
        super().__init__(model)

        # Campos obligatorios para creación
        self.required_fields = [
            'codigo_asignatura', 'nombre', 'area_conocimiento',
            'creditos_academicos', 'objetivos_generales', 'objetivos_especificos'
        ]

        # Campos que deben tratarse como texto (limpieza, trim, etc.)
        self.string_fields = [
            'codigo_asignatura', 'nombre', 'area_conocimiento',
            'objetivos_generales', 'objetivos_especificos',
            'requisitos_previos', 'bibliografia'
        ]

    def _get_primary_key_field(self):
        """
        Define el campo PK de la entidad.
        En este caso no es 'id' sino 'codigo_asignatura'.
        """
        return "codigo_asignatura"

    # =========================================================================
    # HOOKS
    # =========================================================================

    def _preprocess_create_data(self, **kwargs):
        """
        Preprocesamiento antes de crear:
        - Valida campos obligatorios
        - Limpia y valida lógica de negocio
        """
        self.validate_required_fields(kwargs, self.required_fields)
        return self._validate_and_clean_logic(**kwargs)

    def _preprocess_update_data(self, entity_id, **kwargs):
        """
        Preprocesamiento antes de actualizar:
        - No exige todos los campos obligatorios
        - Solo valida los que vienen
        """
        return self._validate_and_clean_logic(**kwargs)

    def _postprocess_get_data(self, entity_data):
        """
        Postprocesamiento al obtener datos:
        - Agrega campo calculado 'horas_totales'
        
        Esto evita que la vista tenga que hacer cálculos.
        """
        if not entity_data:
            return entity_data

        # Obtiene valores asegurando que no sean None
        ht = entity_data.get('horas_teoricas', 0) or 0
        hp = entity_data.get('horas_practicas', 0) or 0

        # Campo derivado
        entity_data['horas_totales'] = ht + hp

        return entity_data

    # Hooks definidos pero no utilizados (extensión futura)
    def _postprocess_create(self, entity_id, **kwargs): pass
    def _postprocess_update(self, entity_id, **kwargs): pass
    def _preprocess_delete(self, entity_id): pass
    def _postprocess_delete(self, entity_id): pass

    # =========================================================================
    # VALIDACIÓN Y LIMPIEZA
    # =========================================================================

    def _validate_and_clean_logic(self, **kwargs):
        """
        Método central de validación y limpieza.

        CORRECCIÓN:
        - Incluye TODOS los campos del modelo
        - Evita pérdida de datos antes de llegar al procedimiento almacenado

        Responsabilidades:
        - Validar longitud de strings
        - Limpiar datos (safe_str)
        - Convertir tipos (int)
        - Aplicar reglas de negocio
        """
        cleaned = {}

        # --- Campos de texto con validación de longitud ---

        cleaned['codigo_asignatura'] = Validator.validate_string_length(
            safe_str(kwargs.get('codigo_asignatura')),
            "Código Asignatura",
            max_length=20,
            allow_empty=False
        )

        cleaned['nombre'] = Validator.validate_string_length(
            safe_str(kwargs.get('nombre')),
            "Nombre",
            max_length=150,
            allow_empty=False
        )

        cleaned['area_conocimiento'] = Validator.validate_string_length(
            safe_str(kwargs.get('area_conocimiento')),
            "Área de Conocimiento",
            max_length=100,
            allow_empty=False
        )

        cleaned['objetivos_generales'] = Validator.validate_string_length(
            safe_str(kwargs.get('objetivos_generales')),
            "Objetivos Generales",
            max_length=1000,
            allow_empty=False
        )

        cleaned['objetivos_especificos'] = Validator.validate_string_length(
            safe_str(kwargs.get('objetivos_especificos')),
            "Objetivos Específicos",
            max_length=1000,
            allow_empty=False
        )

        # --- Campos opcionales de texto ---

        cleaned['requisitos_previos'] = Validator.validate_string_length(
            safe_str(kwargs.get('requisitos_previos', '')),
            "Requisitos Previos",
            max_length=500,
            allow_empty=True
        )

        cleaned['bibliografia'] = Validator.validate_string_length(
            safe_str(kwargs.get('bibliografia', '')),
            "Bibliografía",
            max_length=1000,
            allow_empty=True
        )

        # --- Campos numéricos con protección segura ---

        # CORRECCIÓN: uso de safe_int para evitar fallos por strings inválidos
        cleaned['horas_teoricas'] = self.safe_int(kwargs.get('horas_teoricas', 0))
        cleaned['horas_practicas'] = self.safe_int(kwargs.get('horas_practicas', 0))
        cleaned['creditos_academicos'] = self.safe_int(kwargs.get('creditos_academicos'))

        # --- Regla de negocio crítica ---

        # No se permite una asignatura sin carga horaria
        if (cleaned['horas_teoricas'] + cleaned['horas_practicas']) <= 0:
            raise ValidationError(
                "Horas",
                "la suma de horas teóricas y prácticas debe ser mayor a 0"
            )

        return cleaned