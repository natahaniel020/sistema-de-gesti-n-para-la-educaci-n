"""
Controlador base para todos los controladores de la aplicación
Corregido: create() ya no asume que el modelo retorna un ID (retorna True),
se documenta el contrato real de retorno.
"""

from abc import ABC, abstractmethod
from utils.exceptions import ValidationError, DatabaseOperationError, EntityNotFoundError


class BaseController(ABC):
    """
    Clase base abstracta para todos los controladores.
    
    Define la estructura estándar de operaciones CRUD y proporciona:
    - Validaciones comunes
    - Manejo uniforme de errores
    - Hooks (pre y post) para personalización en controladores hijos
    """

    def __init__(self, model):
        # Modelo asociado (capa de acceso a datos)
        self.model = model
        
        # Nombre de la entidad (usado en mensajes de error)
        self.entity_name = model.entity_name if hasattr(model, 'entity_name') else "Entidad"

    # =========================================================================
    # OPERACIONES CRUD PRINCIPALES
    # =========================================================================

    def create(self, **kwargs):
        """
        Crea una entidad.
        
        Flujo:
        1. Preprocesa datos (validaciones, limpieza, transformación)
        2. Llama al modelo para persistir
        3. Ejecuta lógica posterior (hook)
        
        CORRECCIÓN:
        - El modelo retorna True (no ID)
        - El ID se obtiene desde los datos procesados
        """
        try:
            # Validación y transformación previa
            processed_data = self._preprocess_create_data(**kwargs)

            # Llamada al modelo (retorna True/False)
            success = self.model.create(**processed_data)

            # Se obtiene el ID desde los datos, no desde el modelo
            entity_id = processed_data.get(self._get_primary_key_field())

            # Hook posterior (ej: logs, relaciones, etc.)
            self._postprocess_create(entity_id, **processed_data)

            return success

        except (ValidationError, DatabaseOperationError):
            # Se relanzan errores conocidos sin modificar
            raise

        except Exception as e:
            # Cualquier error inesperado se encapsula
            raise DatabaseOperationError(f"Error inesperado creando {self.entity_name}: {str(e)}")

    def get_by_id(self, entity_id):
        """Obtiene una entidad por su ID"""
        try:
            # Validación básica del ID
            if entity_id is None or str(entity_id).strip() == "":
                raise ValidationError("ID/Código", "no puede estar vacío")

            # Consulta al modelo
            entity_data = self.model.get_by_id(entity_id)

            # Transformación posterior (si aplica)
            return self._postprocess_get_data(entity_data)

        except (ValidationError, EntityNotFoundError):
            raise

        except Exception as e:
            raise DatabaseOperationError(f"Error obteniendo {self.entity_name}: {str(e)}")

    def update(self, entity_id, **kwargs):
        """Actualiza una entidad existente"""
        try:
            # Validación del ID
            if entity_id is None or str(entity_id).strip() == "":
                raise ValidationError("ID/Código", "es necesario para actualizar")

            # Preprocesamiento (validación + limpieza)
            processed_data = self._preprocess_update_data(entity_id, **kwargs)

            # Actualización en el modelo
            result = self.model.update(entity_id, **processed_data)

            # Hook posterior
            self._postprocess_update(entity_id, **processed_data)

            return result

        except (ValidationError, EntityNotFoundError):
            raise

        except Exception as e:
            raise DatabaseOperationError(f"Error actualizando {self.entity_name}: {str(e)}")

    def delete(self, entity_id):
        """Elimina una entidad"""
        try:
            # Validación del ID
            if entity_id is None or str(entity_id).strip() == "":
                raise ValidationError("ID/Código", "es necesario para eliminar")

            # Hook previo (ej: validaciones de integridad)
            self._preprocess_delete(entity_id)

            # Eliminación en el modelo
            result = self.model.delete(entity_id)

            # Hook posterior
            self._postprocess_delete(entity_id)

            return result

        except (ValidationError, EntityNotFoundError):
            raise

        except Exception as e:
            raise DatabaseOperationError(f"Error eliminando {self.entity_name}: {str(e)}")

    def get_all(self):
        """Obtiene todas las entidades"""
        try:
            # Consulta al modelo
            entities = self.model.get_all()

            # Se aplica postprocesamiento a cada entidad
            return [self._postprocess_get_data(entity) for entity in entities]

        except Exception as e:
            raise DatabaseOperationError(f"Error obteniendo lista de {self.entity_name}: {str(e)}")

    def exists(self, entity_id):
        """
        Verifica si una entidad existe.
        
        Delega directamente al modelo (sin validaciones adicionales).
        """
        return self.model.exists(entity_id)

    # =========================================================================
    # MÉTODOS DE SOPORTE REUTILIZABLES
    # =========================================================================

    def validate_required_fields(self, data, required_fields):
        """
        Valida que los campos requeridos no estén vacíos.
        
        - Verifica existencia
        - Verifica que no sea None
        - Verifica que no sea string vacío
        """
        for field in required_fields:
            if field not in data or data[field] is None or str(data[field]).strip() == "":
                field_name = field.replace('_', ' ').title()
                raise ValidationError(field_name, "es requerido")

    def clean_string_data(self, data_dict, string_fields):
        """
        Limpia espacios en blanco en campos de texto.
        
        - Aplica strip()
        - Convierte strings vacíos a None
        - No modifica el diccionario original (copia defensiva)
        """
        cleaned_data = data_dict.copy()

        for field in string_fields:
            if field in cleaned_data and cleaned_data[field] is not None:
                value = str(cleaned_data[field]).strip()
                cleaned_data[field] = value if value else None

        return cleaned_data

    def safe_int(self, value, default=0):
        """
        Convierte a entero de forma segura.
        
        Casos:
        - None o vacío → default
        - Valor inválido → default
        - Valor válido → int(value)
        
        CORRECCIÓN:
        - Centraliza esta lógica para evitar duplicación en controladores hijos
        """
        try:
            if value is None or str(value).strip() == "":
                return default
            return int(value)

        except (ValueError, TypeError):
            return default

    # =========================================================================
    # HOOKS — Los controladores hijos los sobrescriben según necesidad
    # =========================================================================

    def _get_primary_key_field(self):
        """
        Retorna el nombre del campo PK de esta entidad.
        
        - Por defecto: "id"
        - Debe sobrescribirse si la PK tiene otro nombre
        """
        return "id"

    @abstractmethod
    def _preprocess_create_data(self, **kwargs):
        """
        Hook obligatorio.
        
        Se usa para:
        - Validaciones
        - Normalización de datos
        - Construcción del payload para el modelo
        """
        pass

    @abstractmethod
    def _preprocess_update_data(self, entity_id, **kwargs):
        """
        Hook obligatorio para actualización.
        
        Similar a create pero con contexto del ID.
        """
        pass

    def _preprocess_delete(self, entity_id):
        """
        Hook opcional antes de eliminar.
        
        Ejemplo:
        - Validar relaciones
        - Evitar borrado si hay dependencias
        """
        pass

    def _postprocess_create(self, entity_id, **kwargs):
        """
        Hook opcional después de crear.
        
        Ejemplo:
        - Logs
        - Auditoría
        - Crear relaciones secundarias
        """
        pass

    def _postprocess_update(self, entity_id, **kwargs):
        """
        Hook opcional después de actualizar.
        """
        pass

    def _postprocess_delete(self, entity_id):
        """
        Hook opcional después de eliminar.
        """
        pass

    def _postprocess_get_data(self, entity_data):
        """
        Hook opcional para transformar datos antes de enviarlos a la vista.
        
        Ejemplo:
        - Formatear fechas
        - Mapear nombres
        - Ocultar campos sensibles
        """
        return entity_data