import tkinter as tk
from tkinter import ttk

"""
Interfaz gráfica del Sistema de Gestión Académica.

Este módulo construye la interfaz usando Tkinter. La aplicación organiza
los formularios por entidad académica mediante un Notebook (pestañas).
Cada pestaña contiene un formulario que permite capturar la información
necesaria para registrar, actualizar o eliminar registros del sistema.

La construcción de formularios se realiza mediante funciones genéricas
para evitar repetición de código.
"""

import tkinter as tk
from tkinter import ttk


root = tk.Tk()
root.geometry('900x700')
root.title("Sistema de Gestión Académica")

"""
Notebook funciona como contenedor de pestañas.
Cada pestaña representa una entidad del sistema.
"""
notebook = ttk.Notebook(root)

"""
Cada Frame representa el contenedor visual donde se
dibujará el formulario correspondiente a la entidad.
"""

tab_estudiante   = ttk.Frame(notebook)
tab_profesor     = ttk.Frame(notebook)
tab_asignatura   = ttk.Frame(notebook)
tab_curso        = ttk.Frame(notebook)
tab_periodo      = ttk.Frame(notebook)
tab_calificacion = ttk.Frame(notebook)
tab_aula         = ttk.Frame(notebook)
tab_plan         = ttk.Frame(notebook)
tab_material     = ttk.Frame(notebook)
tab_prestamo     = ttk.Frame(notebook)
tab_actividad    = ttk.Frame(notebook)


"""
Registro de cada pestaña dentro del Notebook.
El parámetro text define el nombre visible en la interfaz.
"""

notebook.add(tab_estudiante,   text="Estudiante")
notebook.add(tab_profesor,     text="Profesor")
notebook.add(tab_asignatura,   text="Asignatura")
notebook.add(tab_curso,        text="Curso")
notebook.add(tab_periodo,      text="Periodo")
notebook.add(tab_calificacion, text="Calificación")
notebook.add(tab_aula,         text="Aula")
notebook.add(tab_plan,         text="Plan de Estudios")
notebook.add(tab_material,     text="Material")
notebook.add(tab_prestamo,     text="Préstamo")
notebook.add(tab_actividad,    text="Actividad")

notebook.pack(expand=True, fill="both")



def construir_formulario(tab, titulo, color, campos):
    """
    Construye dinámicamente un formulario dentro de una pestaña.

    Args:
        tab (Frame):
            Contenedor donde se dibujará el formulario.

        titulo (str):
            Texto que se mostrará como encabezado del formulario.

        color (str):
            Color del título para diferenciar visualmente
            cada tipo de formulario.

        campos (list[tuple]):
            Lista de campos del formulario.
            Cada elemento contiene:
                (nombre_campo, obligatorio)

            obligatorio (bool):
                True  -> campo requerido
                False -> campo opcional
    """

    tk.Label(
        tab,
        text=titulo,
        font=("Arial", 14, "bold"),
        fg=color
    ).pack(pady=10)

    """
    Canvas + Scrollbar permiten que el formulario
    sea desplazable cuando tiene muchos campos.
    """

    canvas = tk.Canvas(tab)
    scroll = ttk.Scrollbar(tab, orient="vertical", command=canvas.yview)
    frame_inner = ttk.Frame(canvas)

    frame_inner.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=frame_inner, anchor="nw")
    canvas.configure(yscrollcommand=scroll.set)

    canvas.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")

    """
    Contenedor donde se colocarán los campos
    del formulario usando grid.
    """

    form = tk.Frame(frame_inner)
    form.pack(pady=10, padx=50, anchor="w")

    """
    Generación dinámica de etiquetas y campos de entrada.
    """

    for i, (etiqueta, obligatorio) in enumerate(campos):

        sufijo = " *" if obligatorio else " (opcional)"

        tk.Label(
            form,
            text=etiqueta + sufijo + ":",
            font=("Arial", 12)
        ).grid(row=i, column=0, sticky="w", padx=(0, 10), pady=8)

        tk.Entry(
            form,
            width=30,
            font=("Arial", 12),
            relief="solid",
            bd=1
        ).grid(row=i, column=1, sticky="w", pady=8)

    """
    Agrega los botones de acción del formulario.
    """
    construir_botones(tab)




def construir_botones(tab):
    """
    Crea los botones de operación del formulario.

    Operaciones disponibles:
        - Guardar      : crear registro
        - Actualizar   : modificar registro
        - Eliminar     : borrar registro
        - Limpiar      : vaciar campos del formulario
    """

    btn_frame = tk.Frame(tab)
    btn_frame.pack(pady=15)

    tk.Button(
        btn_frame,
        text="Guardar",
        font=("Arial", 12),
        bg="#4CAF50",
        fg="white",
        width=10
    ).pack(side=tk.TOP, padx=5)

    tk.Button(
        btn_frame,
        text="Actualizar",
        font=("Arial", 12),
        bg="#2196F3",
        fg="white",
        width=10
    ).pack(side=tk.TOP, padx=5)

    tk.Button(
        btn_frame,
        text="Eliminar",
        font=("Arial", 12),
        bg="#f44336",
        fg="white",
        width=10
    ).pack(side=tk.TOP, padx=5)

    tk.Button(
        btn_frame,
        text="Limpiar",
        font=("Arial", 12),
        bg="#FF9800",
        fg="white",
        width=10
    ).pack(side=tk.TOP, padx=5)




"""
Cada llamada a construir_formulario define
la estructura de campos que tendrá cada entidad.
"""

# ESTUDIANTE
construir_formulario(tab_estudiante, "FORMULARIO DE ESTUDIANTE", "blue", [
    ("Número de Matrícula",    True),
    ("Nombres",                True),
    ("Apellidos",              True),
    ("Documento de Identidad", True),
    ("Fecha de Nacimiento",    True),
    ("Dirección",              True),
    ("Correo Electrónico",     True),
    ("Nombre del Tutor",       True),
    ("Contacto de Emergencia", True),
    ("Fecha de Ingreso",       True),
    ("Teléfono",               False),
    ("Fotografía",             False),
])

# ══════════════════════════════════════════════════════════════════
# 2. PROFESOR
# ══════════════════════════════════════════════════════════════════
construir_formulario(tab_profesor, "FORMULARIO DE PROFESOR", "darkgreen", [
    ("Código de Empleado",     True),
    ("Nombres",                True),
    ("Apellidos",              True),
    ("Documento de Identidad", True),
    ("Fecha de Nacimiento",    True),
    ("Dirección",              True),
    ("Correo Institucional",   True),
    ("Nivel de Formación",     True),
    ("Especialidad",           True),
    ("Años de Experiencia",    True),
    ("Fecha de Contratación",  True),
    ("Tipo de Contrato",       True),
    ("Departamento",           True),
    ("Teléfono",               False),
])

# ══════════════════════════════════════════════════════════════════
# 3. ASIGNATURA
# ══════════════════════════════════════════════════════════════════
construir_formulario(tab_asignatura, "FORMULARIO DE ASIGNATURA", "purple", [
    ("Código de Asignatura",  True),
    ("Nombre",                True),
    ("Área de Conocimiento",  True),
    ("Horas Teóricas",        True),
    ("Horas Prácticas",       True),
    ("Créditos Académicos",   True),
    ("Objetivos Generales",   True),
    ("Objetivos Específicos", True),
    ("Requisitos Previos",    False),
    ("Bibliografía",          False),
])

# ══════════════════════════════════════════════════════════════════
# 4. CURSO
# ══════════════════════════════════════════════════════════════════
construir_formulario(tab_curso, "FORMULARIO DE CURSO", "darkorange", [
    ("Código de Curso",           True),
    ("Periodo Académico",         True),
    ("Asignatura",                True),
    ("Profesor Asignado",         True),
    ("Aula",                      True),
    ("Horario Días",              True),
    ("Horario Horas",             True),
    ("Cupo Máximo",               True),
    ("Metodología de Evaluación", True),
    ("Lista de Estudiantes",      False),
])

# ══════════════════════════════════════════════════════════════════
# 5. PERIODO ACADÉMICO
# ══════════════════════════════════════════════════════════════════
construir_formulario(tab_periodo, "FORMULARIO DE PERIODO ACADÉMICO", "teal", [
    ("Código de Periodo",         True),
    ("Descripción",               True),
    ("Fecha de Inicio",           True),
    ("Fecha de Finalización",     True),
    ("Estado Actual",             True),
    ("Calendario de Actividades", False),
])

# ══════════════════════════════════════════════════════════════════
# 6. CALIFICACIÓN
# ══════════════════════════════════════════════════════════════════
construir_formulario(tab_calificacion, "FORMULARIO DE CALIFICACIÓN", "crimson", [
    ("Estudiante",         True),
    ("Curso",              True),
    ("Tipo de Evaluación", True),
    ("Fecha",              True),
    ("Valor Numérico",     True),
    ("Porcentaje",         True),
    ("Observaciones",      False),
])

# ══════════════════════════════════════════════════════════════════
# 7. AULA
# ══════════════════════════════════════════════════════════════════
construir_formulario(tab_aula, "FORMULARIO DE AULA", "steelblue", [
    ("ID Aula",       True),
    ("Edificio",      True),
    ("Piso",          True),
    ("Capacidad",     True),
    ("Tipo",          True),
    ("Estado Actual", True),
    ("Equipamiento",  False),
])

# ══════════════════════════════════════════════════════════════════
# 8. PLAN DE ESTUDIOS
# ══════════════════════════════════════════════════════════════════
construir_formulario(tab_plan, "FORMULARIO DE PLAN DE ESTUDIOS", "indigo", [
    ("Código de Plan",           True),
    ("Carrera",                  True),
    ("Fecha de Aprobación",      True),
    ("Asignaturas por Nivel",    True),
    ("Créditos Totales",         True),
    ("Requisitos de Graduación", True),
])

# ══════════════════════════════════════════════════════════════════
# 9. MATERIAL BIBLIOGRÁFICO
# ══════════════════════════════════════════════════════════════════
construir_formulario(tab_material, "FORMULARIO DE MATERIAL BIBLIOGRÁFICO", "saddlebrown", [
    ("Código de Material",  True),
    ("Título",              True),
    ("Autores",             True),
    ("Categoría Temática",  True),
    ("Formato",             True),
    ("Editorial",           False),
    ("Año de Publicación",  False),
    ("Edición",             False),
    ("ISBN",                False),
    ("Ubicación Física",    False),
    ("Cantidad Ejemplares", False),
])

# ══════════════════════════════════════════════════════════════════
# 10. PRÉSTAMO
# ══════════════════════════════════════════════════════════════════
construir_formulario(tab_prestamo, "FORMULARIO DE PRÉSTAMO", "darkred", [
    ("Código de Préstamo",     True),
    ("Fecha de Préstamo",      True),
    ("Fecha Devolución Prog.", True),
    ("Material Prestado",      True),
    ("Solicitante",            True),
    ("Estado",                 True),
    ("Multa Aplicada",         False),
])

# ══════════════════════════════════════════════════════════════════
# 11. ACTIVIDAD EXTRACURRICULAR
# ══════════════════════════════════════════════════════════════════
construir_formulario(tab_actividad, "FORMULARIO DE ACTIVIDAD EXTRACURRICULAR", "darkslategray", [
    ("Código de Actividad",  True),
    ("Nombre",               True),
    ("Tipo",                 True),
    ("Profesor Responsable", True),
    ("Horario",              True),
    ("Lugar",                True),
    ("Cupo",                 True),
    ("Descripción",          False),
    ("Lista Participantes",  False),
])


"""
Inicia el loop principal de la interfaz gráfica.
La aplicación permanece activa hasta que el usuario
cierre la ventana.
"""

root.mainloop()