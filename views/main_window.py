"""
Ventana principal de la aplicación de Gestión Académica
"""
import tkinter as tk
from tkinter import ttk

# Importación de vistas (UI)
from views.asignatura_view import AsignaturaView
from views.estudiante_view import EstudianteView
from views.profesor_view import ProfesorView

# Importación de controladores (lógica de negocio)
from controllers.asignatura_controller import AsignaturaController
from controllers.estudiante_controller import EstudianteController
from controllers.profesor_controller import ProfesorController

# Importación de modelos (acceso a datos)
from models.asignatura import Asignatura
from models.estudiante import Estudiante
from models.profesor import Profesor

# Utilidades de interfaz
from utils.helpers import UIHelpers


class MainWindow:
    """Ventana principal con pestañas para Asignaturas, Estudiantes y Profesores"""

    def __init__(self, root, db_connection):
        # Referencia a la ventana raíz de Tkinter
        self.root = root
        # Conexión a la base de datos compartida
        self.db = db_connection

        # Inicialización del sistema en orden
        self._setup_main_window()   # Configuración básica de la ventana
        self._setup_styles()        # Estilos visuales
        self._create_mvc_stack()    # Inicialización de modelos y controladores
        self._create_interface()    # Construcción de la UI
        self._load_initial_data()   # Carga inicial de datos

    def _setup_main_window(self):
        # Título de la ventana principal
        self.root.title("Sistema de Gestión Académica")
        # Tamaño inicial de la ventana
        self.root.geometry('1200x700')
        # Centra la ventana en la pantalla
        UIHelpers.center_window(self.root, 1200, 700)
        # Evento al cerrar la ventana
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _setup_styles(self):
        # Configuración de estilos de ttk
        style = ttk.Style()
        style.theme_use('clam')  # Tema visual

        # Estilo de pestañas
        style.configure('TNotebook.Tab', padding=[20, 5], font=("Arial", 10))
        # Estilo de encabezados de tablas
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

    def _create_mvc_stack(self):
        """Instancia modelos y controladores en orden correcto"""

        # =========================
        # MODELOS (acceso a datos)
        # =========================
        # Cada modelo recibe la conexión a la base de datos
        self.asignatura_model  = Asignatura(self.db)
        self.estudiante_model  = Estudiante(self.db)
        self.profesor_model    = Profesor(self.db)

        # =========================
        # CONTROLADORES (lógica)
        # =========================
        # Cada controlador recibe su modelo correspondiente
        self.asignatura_controller = AsignaturaController(self.asignatura_model)
        self.estudiante_controller = EstudianteController(self.estudiante_model)
        self.profesor_controller   = ProfesorController(self.profesor_model)

    def _create_interface(self):
        # =========================
        # HEADER (barra superior)
        # =========================
        header = tk.Frame(self.root, bg='#2c3e50', height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Título del sistema
        tk.Label(
            header,
            text="SISTEMA DE GESTIÓN ACADÉMICA",
            font=("Arial", 18, "bold"), fg="white", bg='#2c3e50'
        ).pack(expand=True)

        # =========================
        # NOTEBOOK (pestañas)
        # =========================
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(expand=True, fill="both", padx=10, pady=5)

        # -------- Pestaña Asignaturas --------
        self.tab_asignaturas = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_asignaturas, text=" Asignaturas ")

        # Se instancia la vista y se le pasa su controlador
        self.asignatura_view = AsignaturaView(
            self.tab_asignaturas, self.asignatura_controller
        )

        # -------- Pestaña Estudiantes --------
        self.tab_estudiantes = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_estudiantes, text=" Estudiantes ")

        self.estudiante_view = EstudianteView(
            self.tab_estudiantes, self.estudiante_controller
        )

        # -------- Pestaña Profesores --------
        self.tab_profesores = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_profesores, text=" Profesores ")

        self.profesor_view = ProfesorView(
            self.tab_profesores, self.profesor_controller
        )

        # =========================
        # BARRA DE ESTADO
        # =========================
        self.status_bar = tk.Label(
            self.root, text="Listo", bd=1, relief=tk.SUNKEN, anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def _load_initial_data(self):
        """Carga las listas al arrancar la aplicación"""
        try:
            # Refresca las listas de cada módulo
            self.asignatura_view._refresh_list()
            self.estudiante_view._refresh_list()
            # Nota: profesor_view ya carga datos en su constructor

            # Mensaje de estado exitoso
            self.status_bar.config(text="Base de datos conectada.")
        except Exception as e:
            # Manejo de errores en carga inicial
            self.status_bar.config(text=f"Advertencia al cargar datos: {e}")

    def _on_closing(self):
        # Confirmación antes de cerrar la aplicación
        if UIHelpers.show_confirmation_dialog("Salir", "¿Desea cerrar el sistema?"):
            # Cierra la conexión a la base de datos
            self.db.disconnect()
            # Destruye la ventana principal
            self.root.destroy()