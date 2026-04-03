"""
Funciones auxiliares para la aplicación Northwind
"""
import os
import shutil
from datetime import datetime
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox
from utils.exceptions import FileOperationError, ImageProcessingError


class FileManager:
    """Clase para manejar operaciones de archivos"""

    @staticmethod
    def ensure_directory_exists(directory_path):
        """
        Asegura que un directorio existe, creándolo si es necesario

        Args:
            directory_path (str): Ruta del directorio

        Returns:
            bool: True si el directorio existe o se creó exitosamente
        """
        try:
            if not os.path.exists(directory_path):
                os.makedirs(directory_path, exist_ok=True)
            return True
        except Exception as e:
            raise FileOperationError(f"No se pudo crear el directorio {directory_path}: {e}")

    @staticmethod
    def copy_file(source_path, destination_path):
        """
        Copia un archivo de origen a destino

        Args:
            source_path (str): Ruta del archivo origen
            destination_path (str): Ruta del archivo destino

        Returns:
            bool: True si se copió exitosamente
        """
        try:
            if not os.path.exists(source_path):
                raise FileOperationError(f"El archivo origen {source_path} no existe")

            # Asegurar que el directorio destino existe
            dest_dir = os.path.dirname(destination_path)
            FileManager.ensure_directory_exists(dest_dir)

            shutil.copy2(source_path, destination_path)
            return True
        except Exception as e:
            raise FileOperationError(f"Error copiando archivo: {e}")

    @staticmethod
    def move_file(source_path, destination_path):
        """
        Mueve un archivo de origen a destino

        Args:
            source_path (str): Ruta del archivo origen
            destination_path (str): Ruta del archivo destino

        Returns:
            bool: True si se movió exitosamente
        """
        try:
            if not os.path.exists(source_path):
                raise FileOperationError(f"El archivo origen {source_path} no existe")

            # Asegurar que el directorio destino existe
            dest_dir = os.path.dirname(destination_path)
            FileManager.ensure_directory_exists(dest_dir)

            shutil.move(source_path, destination_path)
            return True
        except Exception as e:
            raise FileOperationError(f"Error moviendo archivo: {e}")

    @staticmethod
    def delete_file(file_path):
        """
        Elimina un archivo

        Args:
            file_path (str): Ruta del archivo a eliminar

        Returns:
            bool: True si se eliminó exitosamente
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            return True
        except Exception as e:
            raise FileOperationError(f"Error eliminando archivo {file_path}: {e}")

    @staticmethod
    def get_file_size(file_path):
        """
        Obtiene el tamaño de un archivo en bytes

        Args:
            file_path (str): Ruta del archivo

        Returns:
            int: Tamaño en bytes
        """
        try:
            return os.path.getsize(file_path) if os.path.exists(file_path) else 0
        except Exception:
            return 0

    @staticmethod
    def get_file_extension(file_path):
        """
        Obtiene la extensión de un archivo

        Args:
            file_path (str): Ruta del archivo

        Returns:
            str: Extensión del archivo (incluyendo el punto)
        """
        return os.path.splitext(file_path)[1].lower()


class ImageProcessor:
    """Clase para procesamiento de imágenes"""

    THUMBNAIL_SIZE = (150, 150)
    SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    @staticmethod
    def is_valid_image(file_path):
        """
        Verifica si un archivo es una imagen válida

        Args:
            file_path (str): Ruta del archivo

        Returns:
            bool: True si es una imagen válida
        """
        try:
            if not os.path.exists(file_path):
                return False

            # Verificar extensión
            ext = FileManager.get_file_extension(file_path)
            if ext not in ImageProcessor.SUPPORTED_FORMATS:
                return False

            # Intentar abrir la imagen
            with Image.open(file_path) as img:
                img.verify()

            return True
        except Exception:
            return False

    @staticmethod
    def create_thumbnail(source_path, destination_path, size=None):
        """
        Crea una miniatura de una imagen

        Args:
            source_path (str): Ruta de la imagen origen
            destination_path (str): Ruta donde guardar la miniatura
            size (tuple): Tamaño de la miniatura (ancho, alto)

        Returns:
            bool: True si se creó exitosamente
        """
        try:
            if not ImageProcessor.is_valid_image(source_path):
                raise ImageProcessingError("El archivo no es una imagen válida")

            size = size or ImageProcessor.THUMBNAIL_SIZE

            with Image.open(source_path) as img:
                # Convertir a RGB si es necesario
                if img.mode in ('RGBA', 'LA', 'P'):
                    img = img.convert('RGB')

                # Crear miniatura manteniendo proporción
                img.thumbnail(size, Image.Resampling.LANCZOS)

                # Asegurar que el directorio destino existe
                dest_dir = os.path.dirname(destination_path)
                FileManager.ensure_directory_exists(dest_dir)

                # Guardar miniatura
                img.save(destination_path, 'JPEG', quality=85, optimize=True)

            return True
        except Exception as e:
            raise ImageProcessingError(f"Error creando miniatura: {e}")

    @staticmethod
    def resize_image(source_path, destination_path, max_width=800, max_height=600):
        """
        Redimensiona una imagen manteniendo la proporción

        Args:
            source_path (str): Ruta de la imagen origen
            destination_path (str): Ruta donde guardar la imagen redimensionada
            max_width (int): Ancho máximo
            max_height (int): Alto máximo

        Returns:
            bool: True si se redimensionó exitosamente
        """
        try:
            if not ImageProcessor.is_valid_image(source_path):
                raise ImageProcessingError("El archivo no es una imagen válida")

            with Image.open(source_path) as img:
                # Obtener dimensiones originales
                width, height = img.size

                # Calcular nueva dimensión manteniendo proporción
                ratio = min(max_width / width, max_height / height)

                if ratio < 1:  # Solo redimensionar si es necesario
                    new_width = int(width * ratio)
                    new_height = int(height * ratio)

                    # Convertir a RGB si es necesario
                    if img.mode in ('RGBA', 'LA', 'P'):
                        img = img.convert('RGB')

                    # Redimensionar
                    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

                # Asegurar que el directorio destino existe
                dest_dir = os.path.dirname(destination_path)
                FileManager.ensure_directory_exists(dest_dir)

                # Guardar imagen
                img.save(destination_path, 'JPEG', quality=90, optimize=True)

            return True
        except Exception as e:
            raise ImageProcessingError(f"Error redimensionando imagen: {e}")

    @staticmethod
    def load_image_for_tkinter(image_path, size=None):
        """
        Carga una imagen para mostrar en Tkinter

        Args:
            image_path (str): Ruta de la imagen
            size (tuple): Tamaño deseado (ancho, alto)

        Returns:
            ImageTk.PhotoImage: Imagen lista para Tkinter o None si hay error
        """
        try:
            if not os.path.exists(image_path):
                return None

            with Image.open(image_path) as img:
                if size:
                    img = img.resize(size, Image.Resampling.LANCZOS)

                # Convertir para Tkinter
                return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error cargando imagen para Tkinter: {e}")
            return None


class UIHelpers:
    """Funciones auxiliares para la interfaz de usuario"""

    @staticmethod
    def center_window(window, width=None, height=None):
        """
        Centra una ventana en la pantalla

        Args:
            window: Ventana de Tkinter
            width (int): Ancho deseado (opcional)
            height (int): Alto deseado (opcional)
        """
        window.update_idletasks()

        # Obtener dimensiones actuales si no se especifican
        if width is None:
            width = window.winfo_width()
        if height is None:
            height = window.winfo_height()

        # Calcular posición para centrar
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        window.geometry(f'{width}x{height}+{x}+{y}')

    @staticmethod
    def show_error_message(title, message, parent=None):
        """
        Muestra un mensaje de error

        Args:
            title (str): Título del mensaje
            message (str): Mensaje de error
            parent: Ventana padre (opcional)
        """
        messagebox.showerror(title, message, parent=parent)

    @staticmethod
    def show_success_message(title, message, parent=None):
        """
        Muestra un mensaje de éxito

        Args:
            title (str): Título del mensaje
            message (str): Mensaje de éxito
            parent: Ventana padre (opcional)
        """
        messagebox.showinfo(title, message, parent=parent)

    @staticmethod
    def show_confirmation_dialog(title, message, parent=None):
        """
        Muestra un diálogo de confirmación

        Args:
            title (str): Título del diálogo
            message (str): Mensaje de confirmación
            parent: Ventana padre (opcional)

        Returns:
            bool: True si el usuario confirma
        """
        return messagebox.askyesno(title, message, parent=parent)

    @staticmethod
    def select_image_file(parent=None, title="Seleccionar imagen"):
        """
        Abre un diálogo para seleccionar un archivo de imagen

        Args:
            parent: Ventana padre (opcional)
            title (str): Título del diálogo

        Returns:
            str: Ruta del archivo seleccionado o None si se cancela
        """
        filetypes = [
            ("Imágenes", "*.jpg *.jpeg *.png *.gif *.bmp"),
            ("JPEG", "*.jpg *.jpeg"),
            ("PNG", "*.png"),
            ("GIF", "*.gif"),
            ("Todos los archivos", "*.*")
        ]

        return filedialog.askopenfilename(
            parent=parent,
            title=title,
            filetypes=filetypes
        )

    @staticmethod
    def format_date_for_display(date_obj):
        """
        Formatea una fecha para mostrar en la interfaz

        Args:
            date_obj (datetime): Objeto datetime

        Returns:
            str: Fecha formateada o cadena vacía si es None
        """
        if date_obj is None:
            return ""

        if isinstance(date_obj, datetime):
            return date_obj.strftime("%d/%m/%Y")

        return str(date_obj)

    @staticmethod
    def format_currency(amount):
        """
        Formatea un monto como moneda

        Args:
            amount (float): Monto a formatear

        Returns:
            str: Monto formateado como moneda
        """
        if amount is None:
            return "$0.00"

        try:
            return f"${float(amount):,.2f}"
        except (ValueError, TypeError):
            return "$0.00"

    @staticmethod
    def truncate_text(text, max_length=50):
        """
        Trunca un texto si es demasiado largo

        Args:
            text (str): Texto a truncar
            max_length (int): Longitud máxima

        Returns:
            str: Texto truncado
        """
        if not text:
            return ""

        if len(text) <= max_length:
            return text

        return text[:max_length - 3] + "..."


class DataFormatter:
    """Funciones para formatear datos"""

    @staticmethod
    def clean_phone_number(phone):
        """
        Limpia y formatea un número de teléfono

        Args:
            phone (str): Número de teléfono

        Returns:
            str: Número limpio
        """
        if not phone:
            return ""

        # Remover caracteres no numéricos excepto + al inicio
        import re
        cleaned = re.sub(r'[^\d+]', '', phone)

        # Asegurar que + solo esté al inicio
        if '+' in cleaned:
            parts = cleaned.split('+')
            cleaned = '+' + ''.join(parts[1:])

        return cleaned

    @staticmethod
    def format_postal_code(postal_code, country=None):
        """
        Formatea un código postal según el país

        Args:
            postal_code (str): Código postal
            country (str): País (opcional)

        Returns:
            str: Código postal formateado
        """
        if not postal_code:
            return ""

        # Formateo básico - remover espacios extra
        return postal_code.strip().upper()

    @staticmethod
    def capitalize_name(name):
        """
        Capitaliza correctamente un nombre

        Args:
            name (str): Nombre a capitalizar

        Returns:
            str: Nombre capitalizado
        """
        if not name:
            return ""

        # Capitalizar cada palabra
        return ' '.join(word.capitalize() for word in name.split())


# Funciones de utilidad globales
def safe_int(value, default=0):
    """
    Convierte un valor a entero de forma segura

    Args:
        value: Valor a convertir
        default (int): Valor por defecto si falla la conversión

    Returns:
        int: Valor convertido o valor por defecto
    """
    try:
        if value is None or value == "":
            return default
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value, default=0.0):
    """
    Convierte un valor a float de forma segura

    Args:
        value: Valor a convertir
        default (float): Valor por defecto si falla la conversión

    Returns:
        float: Valor convertido o valor por defecto
    """
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (ValueError, TypeError):
        return default


def safe_str(value, default=""):
    """
    Convierte un valor a string de forma segura

    Args:
        value: Valor a convertir
        default (str): Valor por defecto si es None

    Returns:
        str: Valor convertido o valor por defecto
    """
    if value is None:
        return default
    return str(value)


def is_empty_or_none(value):
    """
    Verifica si un valor está vacío o es None

    Args:
        value: Valor a verificar

    Returns:
        bool: True si está vacío o es None
    """
    return value is None or (isinstance(value, str) and not value.strip())