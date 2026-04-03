Sistema de Gestión Académica

Sistema de escritorio desarrollado en Python usando Tkinter para la interfaz gráfica, implementando una arquitectura MVC (Modelo-Vista-Controlador). Permite gestionar información de Asignaturas, Estudiantes y Profesores con soporte para base de datos MySQL.

Características
Gestión completa de Asignaturas:
Crear, actualizar, eliminar y listar asignaturas.
Campos como código, nombre, área de conocimiento, créditos y horas.
Soporte para objetivos y bibliografía.
Gestión de Estudiantes:
Registro de matrícula, datos personales, contacto de emergencia.
Campos de fecha con calendario (fecha de nacimiento e ingreso).
Vista previa de fotografía.
Gestión de Profesores:
Registro de datos personales, nivel académico, especialidad y departamento.
Campos de fecha con calendario (nacimiento y contratación).
Soporte para carga de fotografía.
Interfaz gráfica con pestañas, Treeviews y formularios con scroll.
Validación de campos obligatorios y control de errores.
Conexión a MySQL con manejo de errores y cierre seguro.
Requisitos
Python 3.10 o superior
MySQL Server
Paquetes Python necesarios:
pip install tk mysql-connector-python pillow
Sistema operativo: Windows, Linux o macOS.
Estructura del proyecto
├── config/
│   └── database.py          # Configuración y conexión a MySQL
├── controllers/
│   ├── asignatura_controller.py
│   ├── estudiante_controller.py
│   └── profesor_controller.py
├── models/
│   ├── asignatura.py
│   ├── estudiante.py
│   └── profesor.py
├── utils/
│   └── helpers.py           # Funciones auxiliares y utilidades UI
├── views/
│   ├── main_window.py
│   ├── asignatura_view.py
│   ├── estudiante_view.py
│   └── profesor_view.py
├── main.py                  # Punto de entrada del programa
└── README.md
Configuración de la base de datos
Crear la base de datos y las tablas necesarias en MySQL.
Editar config/database.py con los datos de conexión:
HOST = "localhost"
USER = "root"
PASSWORD = "tu_contraseña"
DATABASE = "gestion_academica"
Verificar la conexión ejecutando el programa.
Ejecución

Desde la raíz del proyecto, ejecutar:

python main.py

La aplicación abrirá una ventana con pestañas para Asignaturas, Estudiantes y Profesores.

Notas
Todos los campos con asterisco (*) son obligatorios.
La carga de fotografías se almacena en la base de datos en formato binario.
La interfaz utiliza Treeview para listar datos y formularios con scroll para campos largos.
Autor

Nathaniel – Estudiante de programación y desarrollo de software.