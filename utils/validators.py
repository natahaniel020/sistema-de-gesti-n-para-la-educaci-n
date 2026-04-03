"""
Funciones de validación para la aplicación Northwind
"""
import re
from datetime import datetime
from utils.exceptions import ValidationError


class Validator:
    """Clase con métodos estáticos para validar diferentes tipos de datos"""

    @staticmethod
    def validate_required(value, field_name):
        """
        Valida que un campo requerido no esté vacío

        Args:
            value (str): Valor a validar
            field_name (str): Nombre del campo para el mensaje de error

        Returns:
            str: Valor limpio (sin espacios al inicio/final)

        Raises:
            ValidationError: Si el campo está vacío
        """
        if not value or not value.strip():
            raise ValidationError(field_name, "es requerido")
        return value.strip()

    @staticmethod
    def validate_numeric(value, field_name, allow_empty=True, min_value=None, max_value=None):
        """
        Valida que un valor sea numérico

        Args:
            value (str): Valor a validar
            field_name (str): Nombre del campo
            allow_empty (bool): Si permite valores vacíos
            min_value (float): Valor mínimo permitido
            max_value (float): Valor máximo permitido

        Returns:
            float or None: Valor numérico o None si está vacío y se permite

        Raises:
            ValidationError: Si no es un número válido o está fuera del rango
        """
        if not value or not value.strip():
            if allow_empty:
                return None
            else:
                raise ValidationError(field_name, "es requerido")

        try:
            num_value = float(value.strip()) if '.' in value else int(value.strip())

            if min_value is not None and num_value < min_value:
                raise ValidationError(field_name, f"debe ser mayor o igual a {min_value}")

            if max_value is not None and num_value > max_value:
                raise ValidationError(field_name, f"debe ser menor o igual a {max_value}")

            return num_value

        except ValueError:
            raise ValidationError(field_name, "debe ser un número válido")

    @staticmethod
    def validate_integer(value, field_name, allow_empty=True, min_value=None, max_value=None):
        """
        Valida que un valor sea un entero

        Args:
            value (str): Valor a validar
            field_name (str): Nombre del campo
            allow_empty (bool): Si permite valores vacíos
            min_value (int): Valor mínimo permitido
            max_value (int): Valor máximo permitido

        Returns:
            int or None: Valor entero o None si está vacío y se permite

        Raises:
            ValidationError: Si no es un entero válido o está fuera del rango
        """
        if not value or not value.strip():
            if allow_empty:
                return None
            else:
                raise ValidationError(field_name, "es requerido")

        try:
            int_value = int(value.strip())

            if min_value is not None and int_value < min_value:
                raise ValidationError(field_name, f"debe ser mayor o igual a {min_value}")

            if max_value is not None and int_value > max_value:
                raise ValidationError(field_name, f"debe ser menor o igual a {max_value}")

            return int_value

        except ValueError:
            raise ValidationError(field_name, "debe ser un número entero válido")

    @staticmethod
    def validate_date(date_string, field_name, allow_empty=True, date_format="%Y-%m-%d"):
        """
        Valida que una cadena sea una fecha válida

        Args:
            date_string (str): Cadena de fecha a validar
            field_name (str): Nombre del campo
            allow_empty (bool): Si permite valores vacíos
            date_format (str): Formato esperado de la fecha

        Returns:
            datetime or None: Objeto datetime o None si está vacío y se permite

        Raises:
            ValidationError: Si no es una fecha válida
        """
        if not date_string or not date_string.strip():
            if allow_empty:
                return None
            else:
                raise ValidationError(field_name, "es requerido")

        try:
            return datetime.strptime(date_string.strip(), date_format)
        except ValueError:
            raise ValidationError(field_name, f"debe estar en formato {date_format}")

    @staticmethod
    def validate_string_length(value, field_name, min_length=None, max_length=None, allow_empty=True):
        """
        Valida la longitud de una cadena

        Args:
            value (str): Cadena a validar
            field_name (str): Nombre del campo
            min_length (int): Longitud mínima
            max_length (int): Longitud máxima
            allow_empty (bool): Si permite valores vacíos

        Returns:
            str or None: Cadena limpia o None si está vacía y se permite

        Raises:
            ValidationError: Si la longitud no es válida
        """
        if not value or not value.strip():
            if allow_empty:
                return None
            else:
                raise ValidationError(field_name, "es requerido")

        clean_value = value.strip()
        length = len(clean_value)

        if min_length is not None and length < min_length:
            raise ValidationError(field_name, f"debe tener al menos {min_length} caracteres")

        if max_length is not None and length > max_length:
            raise ValidationError(field_name, f"no puede tener más de {max_length} caracteres")

        return clean_value

    @staticmethod
    def validate_email(email, field_name, allow_empty=True):
        """
        Valida que una cadena sea un email válido

        Args:
            email (str): Email a validar
            field_name (str): Nombre del campo
            allow_empty (bool): Si permite valores vacíos

        Returns:
            str or None: Email limpio o None si está vacío y se permite

        Raises:
            ValidationError: Si no es un email válido
        """
        if not email or not email.strip():
            if allow_empty:
                return None
            else:
                raise ValidationError(field_name, "es requerido")

        clean_email = email.strip()
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(email_pattern, clean_email):
            raise ValidationError(field_name, "debe ser un email válido")

        return clean_email

    @staticmethod
    def validate_phone(phone, field_name, allow_empty=True):
        """
        Valida que una cadena sea un teléfono válido

        Args:
            phone (str): Teléfono a validar
            field_name (str): Nombre del campo
            allow_empty (bool): Si permite valores vacíos

        Returns:
            str or None: Teléfono limpio o None si está vacío y se permite

        Raises:
            ValidationError: Si no es un teléfono válido
        """
        if not phone or not phone.strip():
            if allow_empty:
                return None
            else:
                raise ValidationError(field_name, "es requerido")

        clean_phone = phone.strip()
        # Permitir números, espacios, guiones, paréntesis y el signo +
        phone_pattern = r'^[\d\s\-\(\)\+]+$'

        if not re.match(phone_pattern, clean_phone):
            raise ValidationError(field_name, "debe contener solo números, espacios, guiones, paréntesis y +")

        # Verificar que tenga al menos 7 dígitos
        digits_only = re.sub(r'[\s\-\(\)\+]', '', clean_phone)
        if len(digits_only) < 7:
            raise ValidationError(field_name, "debe tener al menos 7 dígitos")

        return clean_phone

    @staticmethod
    def validate_price(price, field_name, allow_empty=True):
        """
        Valida que un valor sea un precio válido (número positivo)

        Args:
            price (str): Precio a validar
            field_name (str): Nombre del campo
            allow_empty (bool): Si permite valores vacíos

        Returns:
            float or None: Precio o None si está vacío y se permite

        Raises:
            ValidationError: Si no es un precio válido
        """
        numeric_value = Validator.validate_numeric(price, field_name, allow_empty, min_value=0)

        if numeric_value is not None and numeric_value < 0:
            raise ValidationError(field_name, "debe ser un valor positivo")

        return numeric_value