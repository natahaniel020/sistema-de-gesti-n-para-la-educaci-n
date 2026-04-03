import tkinter as tk
from tkinter import ttk
from views.base_view import BaseView
from utils.helpers import UIHelpers, safe_str


class AsignaturaView(BaseView):
    """
    Vista concreta para la gestión de Asignaturas.

    Responsabilidades:
    - Construir el formulario específico de asignaturas
    - Definir cómo se muestran los datos en el TreeView
    - Mapear datos entre UI ↔ controlador
    """

    def __init__(self, parent_frame, controller):
        # Título visible en la UI
        self.form_title = "GESTIÓN DE ASIGNATURAS"

        # Nombre lógico de la entidad
        self.entity_name = "Asignatura"

        # Inicialización base
        super().__init__(parent_frame, controller)

    def _create_form_fields(self):
        """
        Crea un formulario con scroll vertical para manejar muchos campos.
        """

        # 1. Contenedor principal con scroll
        container = tk.Frame(self.left_frame)
        container.pack(fill="both", expand=True)

        # Canvas necesario para implementar scroll en Tkinter
        canvas = tk.Canvas(container, highlightthickness=0)

        # Barra de desplazamiento vertical
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)

        # Frame interno que contendrá los campos reales
        self.scrollable_frame = tk.Frame(canvas)

        # Actualiza la región scrollable dinámicamente
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Inserta el frame dentro del canvas
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        # Conecta scroll con canvas
        canvas.configure(yscrollcommand=scrollbar.set)

        # Redefine el form_frame para que apunte al contenedor scrollable
        self.form_frame = self.scrollable_frame

        # Renderizado de componentes
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # =========================================================================
        # DEFINICIÓN DE CAMPOS
        # =========================================================================

        # Clave primaria
        self.create_form_field(0,  "Código Asignatura*:", "codigo_asignatura")

        # Campos simples
        self.create_form_field(1,  "Nombre*:",             "nombre")
        self.create_form_field(2,  "Área Conocimiento*:",  "area_conocimiento")
        self.create_form_field(3,  "Créditos*:",           "creditos_academicos")
        self.create_form_field(4,  "Horas Teóricas:",      "horas_teoricas")
        self.create_form_field(5,  "Horas Prácticas:",     "horas_practicas")

        # Campos de texto largo
        self.create_form_field(
            6, "Objetivos Generales*:", "objetivos_generales",
            field_type="text", height=3
        )

        self.create_form_field(
            7, "Objetivos Específicos*:", "objetivos_especificos",
            field_type="text", height=3
        )

        self.create_form_field(
            8, "Requisitos Previos:", "requisitos_previos",
            field_type="text", height=2
        )

        self.create_form_field(
            9, "Bibliografía:", "bibliografia",
            field_type="text", height=2
        )

        # Nota de campos obligatorios
        tk.Label(
            self.form_frame,
            text="* Campos obligatorios",
            font=("Arial", 8, "italic"),
            fg="red"
        ).grid(row=10, column=0, columnspan=2, sticky="w", pady=(10, 20))

    def _create_treeview(self, parent):
        """
        Configura la tabla de visualización de asignaturas
        """
        columns = ('Código', 'Nombre', 'Área', 'Créditos', 'H. Teóricas', 'H. Prácticas')

        # Creación del TreeView
        self.tree = ttk.Treeview(parent, columns=columns, show='headings', height=20)

        # Configuración de anchos de columna
        widths = {
            'Código': 100,
            'Nombre': 200,
            'Área': 150,
            'Créditos': 70,
            'H. Teóricas': 90,
            'H. Prácticas': 90
        }

        # Definición de encabezados y formato
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths.get(col, 100), anchor='center')

        # Alineación específica de columnas de texto
        self.tree.column('Nombre', anchor='w')
        self.tree.column('Área',   anchor='w')

        # Estilos de filas alternas
        self.tree.tag_configure('oddrow',  background='#f0f0f0')
        self.tree.tag_configure('evenrow', background='white')

        # Evento de selección
        self.tree.bind('<<TreeviewSelect>>', self._on_tree_select)

        self.tree.pack(fill="both", expand=True)

    def _get_form_data(self):
        """
        Extrae datos del formulario hacia un dict (UI → controlador)
        """
        return {
            'codigo_asignatura':     self.get_field_value('codigo_asignatura'),
            'nombre':                self.get_field_value('nombre'),
            'area_conocimiento':     self.get_field_value('area_conocimiento'),
            'creditos_academicos':   self.get_field_value('creditos_academicos'),
            'horas_teoricas':        self.get_field_value('horas_teoricas'),
            'horas_practicas':       self.get_field_value('horas_practicas'),
            'objetivos_generales':   self.get_field_value('objetivos_generales'),
            'objetivos_especificos': self.get_field_value('objetivos_especificos'),
            'requisitos_previos':    self.get_field_value('requisitos_previos'),
            'bibliografia':          self.get_field_value('bibliografia'),
        }

    def _populate_form(self, data):
        """
        Llena el formulario con datos (controlador → UI)
        """
        if not data:
            return

        # Limpia antes de cargar
        self._clear_form()

        # Asigna cada campo
        for key in self.form_fields:
            self.set_field_value(key, data.get(key, ''))

    def _tree_values_to_dict(self, values):
        """
        Convierte una fila del TreeView en dict mínimo (solo ID)

        IMPORTANTE:
        Aquí solo se devuelve la PK → el resto se obtiene vía controller.get_by_id
        """
        return {'codigo_asignatura': values[0]} if values else {}

    def _entity_to_tree_values(self, entity):
        """
        Convierte una entidad (dict) a tupla para el TreeView
        """
        return (
            safe_str(entity.get('codigo_asignatura', '')),
            safe_str(entity.get('nombre',             '')),
            safe_str(entity.get('area_conocimiento',  '')),
            safe_str(entity.get('creditos_academicos','')),
            safe_str(entity.get('horas_teoricas',     '')),
            safe_str(entity.get('horas_practicas',    '')),
        )

    def _get_entity_id_from_form(self):
        """
        Obtiene la PK desde el formulario
        """
        return self.get_field_value('codigo_asignatura') or None

    def _clear_form(self):
        """
        Limpia formulario y enfoca el campo principal
        """
        super()._clear_form()

        # UX: foco automático en PK
        self.focus_field('codigo_asignatura')