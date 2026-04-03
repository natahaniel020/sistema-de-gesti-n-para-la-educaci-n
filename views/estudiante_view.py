import tkinter as tk
from tkinter import ttk
from views.base_view import BaseView
from utils.helpers import UIHelpers, safe_str


class EstudianteView(BaseView):
    """
    Vista concreta para la gestión de Estudiantes.

    Responsabilidades:
    - Construcción del formulario con múltiples tipos de campo (texto, fecha, imagen)
    - Representación de datos en TreeView
    - Conversión UI ↔ controlador
    """

    def __init__(self, parent_frame, controller):
        # Título visible en la interfaz
        self.form_title = "REGISTRO DE ESTUDIANTES"

        # Nombre lógico de la entidad
        self.entity_name = "Estudiante"

        # Inicialización base
        super().__init__(parent_frame, controller)

    def _create_form_fields(self):
        """
        Crea un formulario con scroll vertical y soporta campos complejos:
        - Fechas (DateEntry)
        - Imagen con preview
        """

        # =========================================================================
        # CONFIGURACIÓN DE SCROLL
        # =========================================================================

        container = tk.Frame(self.left_frame)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)

        # Frame interno desplazable
        self.scrollable_frame = tk.Frame(canvas)

        # Ajuste dinámico del scroll
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Inserta el frame dentro del canvas
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Vinculación scrollbar-canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Reasignación del form_frame base
        self.form_frame = self.scrollable_frame

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # =========================================================================
        # DEFINICIÓN DE CAMPOS
        # =========================================================================

        # Identificadores y datos básicos
        self.create_form_field(1,  "N° Matrícula*:",           "numero_matricula")
        self.create_form_field(2,  "Doc. Identidad*:",         "documento_identidad")
        self.create_form_field(3,  "Nombres*:",                "nombres")
        self.create_form_field(4,  "Apellidos*:",              "apellidos")
        self.create_form_field(5,  "Correo*:",                 "correo_electronico")
        self.create_form_field(6,  "Teléfono:",                "telefono")
        self.create_form_field(7,  "Dirección:",               "direccion")

        # Campos de fecha con selector visual (tkcalendar)
        self.create_form_field(8,  "F. Nacimiento*:",          "fecha_nacimiento", field_type="date")
        self.create_form_field(9,  "F. Ingreso*:",             "fecha_ingreso",    field_type="date")

        # Información adicional
        self.create_form_field(10, "Nombre Tutor*:",           "nombre_tutor")
        self.create_form_field(11, "Contacto Emergencia*:",    "contacto_emergencia")

        # Campo de imagen con preview
        self.create_form_field(12, "Fotografía Estudiante:",   "fotografia", field_type="image")

        # Nota de obligatoriedad
        tk.Label(
            self.form_frame,
            text="* Campos obligatorios",
            font=("Arial", 8, "italic"),
            fg="red"
        ).grid(row=13, column=0, columnspan=2, sticky="w", pady=(10, 20))

    def _create_treeview(self, parent):
        """
        Configura la tabla de visualización de estudiantes
        """
        columns = ('Matrícula', 'Nombre Completo', 'Documento', 'Correo')

        self.tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)

        # Encabezados
        self.tree.heading('Matrícula',       text='Matrícula')
        self.tree.heading('Nombre Completo', text='Nombre Estudiante')
        self.tree.heading('Documento',       text='Identidad')
        self.tree.heading('Correo',          text='Correo Electrónico')

        # Configuración de columnas
        self.tree.column('Matrícula',       width=100, anchor='center')
        self.tree.column('Nombre Completo', width=250, anchor='w')
        self.tree.column('Documento',       width=120, anchor='center')
        self.tree.column('Correo',          width=200, anchor='w')

        # Estilos de filas alternas
        self.tree.tag_configure('oddrow',  background='#f7f7f7')
        self.tree.tag_configure('evenrow', background='white')

        # Evento de selección
        self.tree.bind('<<TreeviewSelect>>', self._on_tree_select)

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

    def _get_form_data(self):
        """
        Extrae datos del formulario.

        NOTA IMPORTANTE:
        - Las fechas ya vienen en formato 'YYYY-MM-DD'
        - Esto es manejado automáticamente por BaseView
        """
        return {
            'numero_matricula':     self.get_field_value('numero_matricula'),
            'nombres':              self.get_field_value('nombres'),
            'apellidos':            self.get_field_value('apellidos'),
            'documento_identidad':  self.get_field_value('documento_identidad'),
            'fecha_nacimiento':     self.get_field_value('fecha_nacimiento'),
            'direccion':            self.get_field_value('direccion'),
            'telefono':             self.get_field_value('telefono'),
            'correo_electronico':   self.get_field_value('correo_electronico'),
            'nombre_tutor':         self.get_field_value('nombre_tutor'),
            'contacto_emergencia':  self.get_field_value('contacto_emergencia'),
            'fecha_ingreso':        self.get_field_value('fecha_ingreso'),
            'fotografia':           self.get_field_value('fotografia') or None,
        }

    def _populate_form(self, data):
        """
        Llena el formulario con datos existentes
        """
        if not data:
            return

        self._clear_form()

        # set_field_value ya maneja internamente fechas e imágenes
        for key in self.form_fields:
            self.set_field_value(key, data.get(key, ''))

    def _entity_to_tree_values(self, entity):
        """
        Convierte una entidad a formato fila del TreeView
        """
        nombre_completo = f"{entity.get('nombres', '')} {entity.get('apellidos', '')}".strip()

        return (
            safe_str(entity.get('numero_matricula',    '')),
            nombre_completo,
            safe_str(entity.get('documento_identidad', '')),
            safe_str(entity.get('correo_electronico',  '')),
        )

    def _tree_values_to_dict(self, values):
        """
        Extrae solo la PK desde el TreeView

        Diseño:
        - Se usa únicamente la matrícula
        - El resto de datos se obtienen vía get_by_id
        """
        return {'numero_matricula': values[0]} if values else {}

    def _get_entity_id_from_form(self):
        """
        Obtiene la PK desde el formulario
        """
        return self.get_field_value('numero_matricula') or None

    def _refresh_list(self):
        """
        Sobrescribe el comportamiento base para:
        - Añadir estilo de filas alternas
        """
        try:
            # Limpia la tabla
            for item in self.tree.get_children():
                self.tree.delete(item)

            # Obtiene datos
            entities = self.controller.get_all()

            # Inserta con estilo alternado
            for i, entity in enumerate(entities):
                tag = 'evenrow' if i % 2 == 0 else 'oddrow'

                self.tree.insert(
                    '',
                    'end',
                    values=self._entity_to_tree_values(entity),
                    tags=(tag,)
                )

        except Exception as e:
            UIHelpers.show_error_message("Error", f"No se pudo cargar la lista: {e}")