"""
Controlador para la gestión de Estudiantes
Corregido: nombres de campos alineados con el modelo (numero_matricula,
documento_identidad, correo_electronico). Eliminado método get_by_course
que no existe en el modelo.
"""

import re
from controllers.base_controller import BaseController
from utils.exceptions import DatabaseOperationError, ValidationError


class EstudianteController(BaseController):
    """
    Controlador específico para la entidad Estudiante.

    Responsabilidades:
    - Validación de datos de entrada
    - Limpieza y normalización
    - Aplicación de reglas de negocio
    - Enriquecimiento de datos para la vista
    """

    def __init__(self, estudiante_model):
        # Inicializa el controlador base con el modelo correspondiente
        super().__init__(estudiante_model)

        # CORRECCIÓN: nombres alineados con el modelo (consistencia crítica)
        self.required_fields = [
            'numero_matricula',     # Identificador único
            'nombres',
            'apellidos',
            'documento_identidad',  # Documento legal
            'correo_electronico'    # Medio de contacto principal
        ]

        # Campos considerados como texto para limpieza (trim, normalización)
        self.string_fields = [
            'numero_matricula', 'nombres', 'apellidos',
            'documento_identidad', 'direccion',
            'correo_electronico', 'nombre_tutor',
            'contacto_emergencia', 'telefono'
        ]

    def _get_primary_key_field(self):
        """
        Define la clave primaria lógica de la entidad.
        """
        return "numero_matricula"

    # =========================================================================
    # HOOKS
    # =========================================================================

    def _preprocess_create_data(self, **kwargs):
        """
        Preprocesamiento antes de crear:
        - Valida campos obligatorios
        - Aplica limpieza y reglas de negocio
        """
        self.validate_required_fields(kwargs, self.required_fields)
        return self._validate_and_clean_estudiante_data(kwargs)

    def _preprocess_update_data(self, entity_id, **kwargs):
        """
        Preprocesamiento antes de actualizar:
        - No exige todos los campos obligatorios
        - Reutiliza la misma lógica de validación/limpieza
        """
        return self._validate_and_clean_estudiante_data(kwargs)

    def _postprocess_get_data(self, entity_data):
        """
        Postprocesamiento para la vista:
        - Construye nombre completo
        - Formatea fecha de nacimiento
        """
        if not entity_data:
            return entity_data

        # Construcción de nombre completo en formato: "Apellidos, Nombres"
        nombres = entity_data.get('nombres', '')
        apellidos = entity_data.get('apellidos', '')
        entity_data['nombre_completo'] = f"{apellidos}, {nombres}"

        # Formateo de fecha de nacimiento (si es datetime)
        fecha = entity_data.get('fecha_nacimiento')
        if fecha:
            entity_data['fecha_legible'] = (
                fecha.strftime('%d/%m/%Y') if hasattr(fecha, 'strftime') else str(fecha)
            )

        return entity_data

    # Hooks definidos para extensión futura
    def _postprocess_create(self, entity_id, **kwargs): pass
    def _postprocess_update(self, entity_id, **kwargs): pass
    def _preprocess_delete(self, entity_id): pass
    def _postprocess_delete(self, entity_id): pass

    # =========================================================================
    # VALIDACIÓN Y LIMPIEZA
    # =========================================================================

    def _validate_and_clean_estudiante_data(self, data):
        """
        Método central de validación y limpieza de estudiantes.

        Flujo:
        1. Limpieza de strings
        2. Normalización de nombres
        3. Validaciones específicas (correo, documento)
        4. Ajustes de campos opcionales
        """

        # 1. Limpieza de espacios en campos de texto
        # Usa método heredado (consistencia entre controladores)
        data = self.clean_string_data(data, self.string_fields)

        # 2. Capitalización de nombres y apellidos
        # Mejora presentación y consistencia de datos
        if data.get('nombres'):
            data['nombres'] = data['nombres'].title()

        if data.get('apellidos'):
            data['apellidos'] = data['apellidos'].title()

        # 3. Validación de formato de correo electrónico
        correo = data.get('correo_electronico', '')

        # Regex básica (no exhaustiva, pero suficiente para validación general)
        if correo and not re.match(r"[^@]+@[^@]+\.[^@]+", correo):
            raise ValidationError("Correo Electrónico", "el formato no es válido")

        # 4. Validación de documento de identidad
        dni = data.get('documento_identidad', '')

        # Regla mínima: longitud >= 8 caracteres
        if dni and len(str(dni).strip()) < 8:
            raise ValidationError("Documento de Identidad", "debe tener al menos 8 caracteres")

        # 5. Manejo de fotografía
        # Normaliza valores vacíos a None (importante para BD)
        if 'fotografia' not in data or data.get('fotografia') == "":
            data['fotografia'] = None

        return data

    # =========================================================================
    # MÉTODOS ADICIONALES
    # =========================================================================

    def get_resumen_academico(self, numero_matricula):
        """
        Obtiene un resumen enriquecido del estudiante.

        Agrega indicadores booleanos útiles para la vista:
        - Tiene correo
        - Tiene dirección
        - Tiene tutor
        """
        try:
            # Obtiene datos base usando método estándar
            estudiante = self.get_by_id(numero_matricula)

            # Copia defensiva para no mutar el original
            resumen = estudiante.copy()

            # Campos derivados booleanos (útiles para UI/lógica)
            resumen['tiene_correo'] = bool(estudiante.get('correo_electronico'))
            resumen['tiene_direccion'] = bool(estudiante.get('direccion'))
            resumen['tiene_tutor'] = bool(estudiante.get('nombre_tutor'))

            return resumen

        except Exception as e:
            # Encapsula cualquier error en excepción de capa de datos
            raise DatabaseOperationError(f"Error en resumen de estudiante: {str(e)}")

    # CORRECCIÓN:
    # Se eliminó get_estudiantes_por_curso porque el modelo no lo soporta.
    # Esto mantiene coherencia estricta entre controlador y modelo.