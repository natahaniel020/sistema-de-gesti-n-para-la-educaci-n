import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
from utils.helpers import UIHelpers, ImageProcessor # Importamos el procesador de imágenes
from utils.exceptions import ValidationError, DatabaseOperationError, EntityNotFoundError

# Intentar importar tkcalendar para que no rompa el sistema si no está instalado
try:
    from tkcalendar import DateEntry
except ImportError:
    DateEntry = None


class BaseView(ABC):
    """
    Clase base abstracta para todas las vistas del sistema (Tkinter).

    Responsabilidades:
    - Construcción de UI base (formulario + lista)
    - Manejo de eventos CRUD
    - Interacción con el controlador
    - Gestión de formularios dinámicos
    """

    def __init__(self, parent_frame, controller):
        # Frame padre donde se renderiza la vista
        self.parent_frame = parent_frame

        # Controlador asociado (capa intermedia)
        self.controller = controller

        # Contenedores principales de UI
        self.main_frame = None
        self.form_frame = None

        # Diccionario de campos del formulario (clave: nombre lógico)
        self.form_fields = {}

        # Diccionario para previews de imágenes
        self.image_labels = {}

        # Treeview para listar entidades
        self.tree = None

        # Nombre de la entidad (debe ser definido en clases hijas)
        self.entity_name = ""

        # Inicialización de UI y eventos
        self._setup_ui()
        self._bind_events()

    # =========================================================================
    # CONSTRUCCIÓN DE INTERFAZ
    # =========================================================================

    def _setup_ui(self):
        """
        Estructura base:
        - Frame principal
        - Panel izquierdo: formulario
        - Panel derecho: lista
        """
        self.main_frame = tk.Frame(self.parent_frame)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side="left", fill="y", padx=(0, 10))

        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side="right", fill="both", expand=True)

        self._create_form_section()
        self._create_list_section()

    def _create_form_section(self):
        """
        Construye la sección de formulario (lado izquierdo)
        """
        title_text = getattr(self, 'form_title', f"GESTIÓN DE {self.entity_name.upper()}S")

        tk.Label(
            self.left_frame, text=title_text,
            font=("Arial", 16, "bold"), fg="green"
        ).pack(pady=20)

        self.form_frame = tk.Frame(self.left_frame)
        self.form_frame.pack(pady=20, anchor="w", padx=20)

        # Campos definidos por clases hijas
        self._create_form_fields()

        self.button_frame = tk.Frame(self.left_frame)
        self.button_frame.pack(pady=20)

        # Botones CRUD
        self._create_buttons()

    def _create_list_section(self):
        """
        Construye la sección de listado (lado derecho)
        """
        tk.Label(
            self.right_frame,
            text=f"LISTA DE {self.entity_name.upper()}S",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        tree_frame = tk.Frame(self.right_frame)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview definido por clases hijas
        self._create_treeview(tree_frame)

        # Scroll vertical
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def _create_buttons(self):
        """
        Crea botones estándar CRUD
        """
        buttons_config = [
            ("Guardar",    "#4CAF50", self._on_save),
            ("Actualizar", "#2196F3", self._on_update),
            ("Eliminar",   "#f44336", self._on_delete),
            ("Buscar",     "#FF9800", self._on_search),
            ("Limpiar",    "#9E9E9E", self._on_clear),
        ]

        for text, color, command in buttons_config:
            tk.Button(
                self.button_frame, text=text,
                font=("Arial", 10), bg=color, fg="white",
                width=10, command=command
            ).pack(side=tk.LEFT, padx=3)

    # =========================================================================
    # MÉTODOS ABSTRACTOS (OBLIGATORIOS EN HIJOS)
    # =========================================================================

    @abstractmethod
    def _create_form_fields(self): pass

    @abstractmethod
    def _create_treeview(self, parent): pass

    @abstractmethod
    def _get_form_data(self): pass

    @abstractmethod
    def _populate_form(self, data): pass

    def _bind_events(self): pass

    # =========================================================================
    # EVENTOS DE INTERACCIÓN
    # =========================================================================

    def _on_tree_select(self, event):
        """
        Evento cuando el usuario selecciona un registro en la tabla
        """
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item['values']

            if values:
                # Convierte valores del tree en dict
                data = self._tree_values_to_dict(values)

                # Llena el formulario con esos datos
                self._populate_form(data)

    def _on_save(self):
        """
        Evento Guardar (CREATE)
        """
        try:
            data = self._get_form_data()
            result = self.controller.create(**data)

            if result:
                UIHelpers.show_success_message("Éxito", f"{self.entity_name} guardado correctamente")
                self._clear_form()
                self._refresh_list()

        except ValidationError as e:
            UIHelpers.show_error_message("Error de Validación", str(e))
        except DatabaseOperationError as e:
            UIHelpers.show_error_message("Error de Base de Datos", str(e))
        except Exception as e:
            UIHelpers.show_error_message("Error", f"Error inesperado: {str(e)}")

    def _on_update(self):
        """
        Evento Actualizar (UPDATE)
        """
        try:
            data = self._get_form_data()
            entity_id = self._get_entity_id_from_form()

            # Validación de ID
            if not entity_id:
                UIHelpers.show_error_message("Error", f"Debe ingresar un ID de {self.entity_name} válido")
                return

            result = self.controller.update(entity_id, **data)

            if result:
                UIHelpers.show_success_message("Éxito", f"{self.entity_name} actualizado correctamente")
                self._refresh_list()

        except ValidationError as e:
            UIHelpers.show_error_message("Error de Validación", str(e))
        except DatabaseOperationError as e:
            UIHelpers.show_error_message("Error de Base de Datos", str(e))
        except Exception as e:
            UIHelpers.show_error_message("Error", f"Error inesperado: {str(e)}")

    def _on_delete(self):
        """
        Evento Eliminar (DELETE)
        """
        try:
            entity_id = self._get_entity_id_from_form()

            if not entity_id:
                UIHelpers.show_error_message("Error", f"Debe ingresar un ID de {self.entity_name} válido")
                return

            # Confirmación antes de eliminar
            if UIHelpers.show_confirmation_dialog(
                "Confirmar", f"¿Está seguro de eliminar este {self.entity_name.lower()}?"
            ):
                result = self.controller.delete(entity_id)

                if result:
                    UIHelpers.show_success_message("Éxito", f"{self.entity_name} eliminado correctamente")
                    self._clear_form()
                    self._refresh_list()

        except ValidationError as e:
            UIHelpers.show_error_message("Error de Validación", str(e))
        except DatabaseOperationError as e:
            UIHelpers.show_error_message("Error de Base de Datos", str(e))
        except Exception as e:
            UIHelpers.show_error_message("Error", f"Error inesperado: {str(e)}")

    def _on_search(self):
        """
        Evento Buscar (READ por ID)
        """
        try:
            entity_id = self._get_entity_id_from_form()

            if not entity_id:
                UIHelpers.show_error_message("Error", f"Debe ingresar un ID de {self.entity_name} válido")
                return

            data = self.controller.get_by_id(entity_id)

            if data:
                self._populate_form(data)

        except EntityNotFoundError as e:
            UIHelpers.show_error_message("No encontrado", str(e))
        except ValidationError as e:
            UIHelpers.show_error_message("Error de Validación", str(e))
        except DatabaseOperationError as e:
            UIHelpers.show_error_message("Error de Base de Datos", str(e))
        except Exception as e:
            UIHelpers.show_error_message("Error", f"Error inesperado: {str(e)}")

    def _on_clear(self):
        """Limpia el formulario"""
        self._clear_form()

    # =========================================================================
    # UTILIDADES DE FORMULARIO
    # =========================================================================

    def create_form_field(self, row, label_text, field_name, field_type="entry", **kwargs):
        """
        Crea dinámicamente un campo de formulario.

        Soporta múltiples tipos:
        - entry
        - text
        - combobox
        - date (tkcalendar)
        - image (con preview)
        """
        tk.Label(
            self.form_frame, text=label_text, font=("Arial", 12)
        ).grid(row=row, column=0, sticky="w", padx=(0, 10), pady=8)

        # Selección de tipo de campo
        if field_type == "entry":
            field = tk.Entry(self.form_frame, width=kwargs.get('width', 25), font=("Arial", 12), relief="solid", bd=1)

        elif field_type == "text":
            field = tk.Text(self.form_frame, width=kwargs.get('width', 25), height=kwargs.get('height', 4), font=("Arial", 12), relief="solid", bd=1)

        elif field_type == "combobox":
            field = ttk.Combobox(self.form_frame, width=kwargs.get('width', 22), font=("Arial", 12), values=kwargs.get('values', []))

        elif field_type == "date" and DateEntry:
            field = DateEntry(self.form_frame, width=kwargs.get('width', 22), font=("Arial", 12), date_pattern='dd/mm/yyyy')

        elif field_type == "image":
            # Contenedor para imagen + botón
            container = tk.Frame(self.form_frame)
            container.grid(row=row, column=1, sticky="w", pady=8)

            # Label para previsualización
            preview_label = tk.Label(container, text="Sin imagen", bg="lightgrey", width=15, height=5)
            preview_label.pack(side=tk.LEFT, padx=5)

            # Campo oculto donde se guarda la ruta
            field = tk.Entry(container)

            # Botón para seleccionar imagen
            btn = tk.Button(container, text="Cargar", command=lambda: self._on_image_browse(field, preview_label))
            btn.pack(side=tk.LEFT)

            # Se guarda referencia del preview
            self.image_labels[field_name] = preview_label

            # Oculta el Entry (solo se usa internamente)
            field.pack_forget()

        else:
            field = tk.Entry(self.form_frame, width=kwargs.get('width', 25), font=("Arial", 12), relief="solid", bd=1)

        # Ubicación en grid (excepto imágenes)
        if field_type != "image":
            field.grid(row=row, column=1, sticky=kwargs.get('sticky', "w"), pady=8)

        # Registro del campo
        self.form_fields[field_name] = field
        return field

    def _on_image_browse(self, path_field, label):
        """Selecciona imagen y actualiza preview"""
        path = UIHelpers.select_image_file(self.parent_frame)

        if path:
            path_field.delete(0, tk.END)
            path_field.insert(0, path)
            self._update_image_preview(label, path)

    def _update_image_preview(self, label, path):
        """Renderiza la imagen en el label"""
        img = ImageProcessor.load_image_for_tkinter(path, size=(100, 100))

        if img:
            label.config(image=img, text="")
            label.image = img  # Evita recolección de basura
        else:
            label.config(image='', text="Error al cargar")

    def get_field_value(self, field_name):
        """
        Obtiene el valor de un campo, adaptándose al tipo
        """
        field = self.form_fields.get(field_name)
        if not field:
            return ""

        # Caso DateEntry (tkcalendar)
        if hasattr(field, 'get_date'):
            try:
                date_obj = field.get_date()
                return date_obj.strftime('%Y-%m-%d')
            except:
                return ""

        if isinstance(field, (tk.Entry, ttk.Combobox)):
            return field.get()

        elif isinstance(field, tk.Text):
            return field.get('1.0', tk.END).strip()

        return ""

    def set_field_value(self, field_name, value):
        """
        Asigna valor a un campo según su tipo
        """
        field = self.form_fields.get(field_name)
        if not field:
            return

        if isinstance(field, tk.Entry):
            field.delete(0, tk.END)

            if value:
                field.insert(0, str(value))

                # Si es imagen → actualizar preview
                if field_name in self.image_labels:
                    self._update_image_preview(self.image_labels[field_name], str(value))

        elif isinstance(field, tk.Text):
            field.delete('1.0', tk.END)
            if value:
                field.insert('1.0', str(value))

        elif isinstance(field, ttk.Combobox):
            field.set(str(value) if value else "")

        elif hasattr(field, 'set_date'):
            if value:
                field.set_date(value)

    def _clear_form(self):
        """
        Limpia todos los campos del formulario
        """
        for name, field_widget in self.form_fields.items():

            if isinstance(field_widget, tk.Entry):
                field_widget.delete(0, tk.END)

                # Reset de preview de imagen
                if name in self.image_labels:
                    self.image_labels[name].config(image='', text="Sin imagen")

            elif isinstance(field_widget, tk.Text):
                field_widget.delete('1.0', tk.END)

            elif hasattr(field_widget, 'set'):
                field_widget.set("")

    def _refresh_list(self):
        """
        Recarga los datos en el TreeView
        """
        try:
            # Limpia la tabla
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Obtiene datos desde el controlador
            entities = self.controller.get_all()

            # Inserta cada entidad
            for entity in entities:
                values = self._entity_to_tree_values(entity)
                self.tree.insert('', 'end', values=values)

        except Exception as e:
            UIHelpers.show_error_message("Error", f"Error cargando lista: {str(e)}")

    # =========================================================================
    # MÉTODOS DE ADAPTACIÓN (OVERRIDE EN HIJOS)
    # =========================================================================

    def _entity_to_tree_values(self, entity):
        """Convierte entidad a tupla para TreeView"""
        return ()

    def _tree_values_to_dict(self, values):
        """Convierte fila del TreeView a dict"""
        return {}

    def _get_entity_id_from_form(self):
        """Obtiene el ID desde el formulario"""
        return None

    # =========================================================================
    # UTILIDADES DE CONTROL DE UI
    # =========================================================================

    def focus_field(self, field_name):
        """Enfoca un campo"""
        field = self.form_fields.get(field_name)
        if field:
            field.focus_set()

    def disable_field(self, field_name):
        """Deshabilita un campo"""
        field = self.form_fields.get(field_name)
        if field:
            field.config(state='disabled')

    def enable_field(self, field_name):
        """Habilita un campo"""
        field = self.form_fields.get(field_name)
        if field:
            field.config(state='normal')