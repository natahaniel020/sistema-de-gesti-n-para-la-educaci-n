"""
Excepciones personalizadas para la aplicación Northwind
"""


class NorthwindException(Exception):
    """Excepción base para todas las excepciones de la aplicación"""
    pass


class DatabaseConnectionError(NorthwindException):
    """Excepción para errores de conexión a la base de datos"""
    pass


class DatabaseOperationError(NorthwindException):
    """Excepción para errores en operaciones de base de datos"""
    pass


class ValidationError(NorthwindException):
    """Excepción para errores de validación de datos"""
    def __init__(self, field_name, message):
        self.field_name = field_name
        self.message = message
        super().__init__(f"Error en campo '{field_name}': {message}")


class EntityNotFoundError(NorthwindException):
    """Excepción cuando no se encuentra una entidad"""
    def __init__(self, entity_type, entity_id):
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} con ID {entity_id} no encontrado")


class EntityInUseError(NorthwindException):
    """Excepción cuando se intenta eliminar una entidad que está en uso"""
    def __init__(self, entity_type, entity_id, used_in):
        self.entity_type = entity_type
        self.entity_id = entity_id
        self.used_in = used_in
        super().__init__(f"No se puede eliminar {entity_type} con ID {entity_id}: está siendo usado en {used_in}")


class ImageProcessingError(NorthwindException):
    """Excepción para errores en procesamiento de imágenes"""
    pass


class FileOperationError(NorthwindException):
    """Excepción para errores en operaciones de archivos"""
    pass