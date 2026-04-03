import tkinter as tk
from tkinter import ttk
from views.base_view import BaseView
from utils.helpers import UIHelpers, safe_str
import os

class ProfesorView(BaseView):

    def __init__(self, parent_frame, controller):
        # Título del formulario que se mostrará en la UI
        self.form_title = "GESTIÓN DE PROFESORES"
        # Nombre de la entidad manejada por esta vista
        self.entity_name = "Profesor"
        # Inicializa la vista base (crea UI y enlaza eventos)
        super().__init__(parent_frame, controller)
        # Carga inicial de datos en la tabla
        self._refresh_list()

    def _create_form_fields(self):
        """
        Implementación con Scrollbar y nuevos tipos de campo (Date e Image).
        """

        # Contenedor principal para habilitar scroll en formularios largos
        container = tk.Frame(self.left_frame)
        container.pack(fill="both", expand=True)

        # Canvas necesario para implementar scroll en Tkinter
        canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        
        # Frame interno que contendrá los campos del formulario
        self.scrollable_frame = tk.Frame(canvas)

        # Ajusta dinámicamente el área de scroll según el contenido
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Inserta el frame dentro del canvas
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Reemplaza el form_frame original por el frame con scroll
        self.form_frame = self.scrollable_frame
        
        # Posicionamiento de canvas y scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # =========================
        # Definición de campos
        # =========================

        # Campos básicos obligatorios
        self.create_form_field(0,  "Código Empleado*:",  "codigo_empleado")
        self.create_form_field(1,  "Nombres*:",          "nombres")
        self.create_form_field(2,  "Apellidos*:",        "apellidos")
        self.create_form_field(3,  "Doc. Identidad*:",   "documento_identidad")
        
        # Campo de fecha con selector (DateEntry)
        self.create_form_field(4,  "F. Nacimiento*:",    "fecha_nacimiento", field_type="date")
        
        # Campos adicionales
        self.create_form_field(5,  "Dirección*:",        "direccion")
        self.create_form_field(6,  "Teléfono:",          "telefono")
        self.create_form_field(7,  "Correo Inst.*:",     "correo_institucional")

        # ComboBox para nivel de formación
        niveles = ['Técnico', 'Tecnólogo', 'Pregrado', 'Especialización', 'Maestría', 'Doctorado']
        self.create_form_field(8,  "Nivel Formación*:", "nivel_formacion", field_type="combobox", values=niveles)

        # Campo opcional
        self.create_form_field(9,  "Especialidad:",      "especialidad")

        # Campo numérico (años de experiencia)
        self.create_form_field(10, "Años Exp.*:",        "anios_experiencia")
        
        # Campo de fecha de contratación
        self.create_form_field(11, "F. Contratación*:", "fecha_contratacion", field_type="date")

        # ComboBox para tipo de contrato
        tipos_contrato = ['Tiempo completo', 'Medio tiempo', 'Por horas']
        self.create_form_field(12, "Tipo Contrato*:", "tipo_contrato", field_type="combobox", values=tipos_contrato)

        # Campo de departamento
        self.create_form_field(13, "Departamento*:",    "departamento")
        
        # Campo de imagen (gestiona preview y selección desde BaseView)
        self.create_form_field(14, "Fotografía:",        "fotografia", field_type="image")

        # Nota visual indicando campos obligatorios
        tk.Label(
            self.form_frame, text="* Campos obligatorios",
            font=("Arial", 8, "italic"), fg="red"
        ).grid(row=15, column=0, columnspan=2, sticky="w", pady=(10, 20))

    def _create_treeview(self, parent):
        # Definición de columnas de la tabla
        columns = ('Codigo', 'Nombre Completo', 'Especialidad', 'Departamento', 'Contrato')
        self.tree = ttk.Treeview(parent, columns=columns, show='headings', height=15)

        # Encabezados de columnas
        self.tree.heading('Codigo',          text='Código')
        self.tree.heading('Nombre Completo', text='Profesor')
        self.tree.heading('Especialidad',    text='Especialidad')
        self.tree.heading('Departamento',    text='Depto')
        self.tree.heading('Contrato',        text='Tipo Contrato')

        # Configuración de ancho de columnas
        self.tree.column('Codigo',          width=100)
        self.tree.column('Nombre Completo', width=200)
        self.tree.column('Especialidad',    width=150)
        self.tree.column('Departamento',    width=80,  anchor="center")
        self.tree.column('Contrato',        width=120)

        # Evento al seleccionar una fila
        self.tree.bind('<<TreeviewSelect>>', self._on_tree_select)

        # Renderiza la tabla
        self.tree.pack(fill="both", expand=True)

    def _get_form_data(self):
        """
        Lee la ruta de la imagen y la convierte a bytes para el LONGBLOB de SQL.
        """

        # Obtiene la ruta de la imagen desde el formulario
        img_path = self.get_field_value('fotografia')
        fotografia_bytes = None
        
        # Verifica que exista el archivo antes de leerlo
        if img_path and os.path.exists(img_path):
            try:
                # Abre la imagen en modo binario
                with open(img_path, 'rb') as f:
                    fotografia_bytes = f.read()
            except Exception as e:
                # Manejo básico de error (solo imprime)
                print(f"Error leyendo imagen: {e}")

        # Retorna todos los datos del formulario
        return {
            'codigo_empleado':      self.get_field_value('codigo_empleado'),
            'nombres':              self.get_field_value('nombres'),
            'apellidos':            self.get_field_value('apellidos'),
            'documento_identidad':  self.get_field_value('documento_identidad'),
            'fecha_nacimiento':     self.get_field_value('fecha_nacimiento'),
            'direccion':            self.get_field_value('direccion'),
            'telefono':             self.get_field_value('telefono'),
            'correo_institucional': self.get_field_value('correo_institucional'),
            'nivel_formacion':      self.get_field_value('nivel_formacion'),
            'especialidad':         self.get_field_value('especialidad'),
            'anios_experiencia':    self.get_field_value('anios_experiencia'),
            'fecha_contratacion':   self.get_field_value('fecha_contratacion'),
            'tipo_contrato':        self.get_field_value('tipo_contrato'),
            'departamento':         self.get_field_value('departamento'),
            # Imagen convertida a bytes para almacenamiento en BD
            'fotografia':           fotografia_bytes, 
        }

    def _populate_form(self, data):
        # Llena el formulario con datos existentes
        if not data: return
        self._clear_form()
        for field in self.form_fields:
            # Maneja automáticamente texto, fechas, combos e imagen
            self.set_field_value(field, data.get(field, ''))

    def _entity_to_tree_values(self, entity):
        # Convierte un objeto entidad en una tupla para mostrar en la tabla
        return (
            safe_str(entity.get('codigo_empleado')),
            f"{entity.get('apellidos', '')}, {entity.get('nombres', '')}",
            safe_str(entity.get('especialidad')),
            safe_str(entity.get('departamento')),
            safe_str(entity.get('tipo_contrato')),
        )

    def _get_entity_id_from_form(self):
        # Obtiene el ID principal desde el formulario
        return self.get_field_value('codigo_empleado') or None

    def _clear_form(self):
        # Limpia el formulario usando la lógica base
        super()._clear_form()
        # Coloca el foco en el campo principal
        self.focus_field('codigo_empleado')