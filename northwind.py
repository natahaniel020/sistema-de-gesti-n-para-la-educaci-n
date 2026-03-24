import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from aplicacion import Controlador
import traceback

# Crear ventana principal
root = tk.Tk()
root.geometry('900x700')  # Tamaño de la ventana
root.title("Sistema de Gestión Académica")  # Título

# Crear contenedor de pestañas
notebook = ttk.Notebook(root)

# Crear pestañas
tab_estudiante = ttk.Frame(notebook, name='estudiante')
tab_profesor   = ttk.Frame(notebook, name='profesor')
tab_asignatura = ttk.Frame(notebook, name='asignatura')
tab_curso      = ttk.Frame(notebook, name='curso')

# Agregar pestañas al notebook
notebook.add(tab_estudiante, text="Estudiante")
notebook.add(tab_profesor,   text="Profesor")
notebook.add(tab_asignatura, text="Asignatura")
notebook.add(tab_curso,      text="Curso")
notebook.pack(expand=True, fill="both")

# Instancia del controlador (lógica de negocio)
controlador = Controlador()


# Función para construir formularios dinámicamente
def construir_formulario(tab, titulo, color, campos):

    # Frame superior que contiene todo
    frame_superior = tk.Frame(tab)
    frame_superior.pack(fill="both", expand=True)

    # Título del formulario
    tk.Label(
        frame_superior,
        text=titulo,
        font=("Arial", 14, "bold"),
        fg=color
    ).pack(pady=10)

    # Canvas + Scroll (para formularios largos)
    canvas = tk.Canvas(frame_superior)
    scroll = ttk.Scrollbar(frame_superior, orient="vertical", command=canvas.yview)
    frame_inner = ttk.Frame(canvas)

    # Ajustar scroll dinámicamente
    frame_inner.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Insertar frame dentro del canvas
    canvas.create_window((0, 0), window=frame_inner, anchor="nw")
    canvas.configure(yscrollcommand=scroll.set)
    canvas.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")

    # Frame del formulario
    form = tk.Frame(frame_inner)
    form.pack(pady=10, padx=50, anchor="w")

    # Diccionario para guardar los widgets
    entries = {}

    # Crear campos dinámicamente
    for i, (etiqueta, obligatorio) in enumerate(campos):
        sufijo = " " if obligatorio else " (opcional)"

        # Etiqueta del campo
        tk.Label(
            form,
            text=etiqueta + sufijo + ":",
            font=("Arial", 12)
        ).grid(row=i, column=0, sticky="w", padx=(0, 10), pady=8)

        # ── Campo tipo fecha ──
        if "fecha" in etiqueta.lower():
            widget = DateEntry(
                form,
                width=28,
                font=("Arial", 12),
                date_pattern="yyyy-mm-dd",
                relief="solid",
                bd=1
            )

        # ── Campo para cargar fotografía ──
        elif etiqueta.lower() == "fotografia":
            foto_frame = tk.Frame(form)

            # Label que muestra nombre del archivo
            foto_label = tk.Label(
                foto_frame,
                text="Sin archivo",
                font=("Arial", 10),
                fg="gray"
            )
            foto_label.pack(side=tk.LEFT, padx=(5, 0))

            # Variable para guardar bytes de la imagen
            foto_var = {"valor": None}

            # Función para seleccionar imagen
            def seleccionar_foto(label=foto_label, var=foto_var):
                ruta = filedialog.askopenfilename(
                    title="Seleccionar fotografía",
                    filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.bmp")]
                )
                if ruta:
                    with open(ruta, "rb") as f:
                        var["valor"] = f.read()  # Guardar imagen en bytes
                    label.config(text=ruta.split("/")[-1], fg="black")

            # Botón para abrir explorador
            tk.Button(
                foto_frame,
                text="📁 Seleccionar",
                font=("Arial", 10),
                command=seleccionar_foto
            ).pack(side=tk.LEFT)

            foto_frame.grid(row=i, column=1, sticky="w", pady=8)

            # Clase para simular .get()
            class FotoWidget:
                def __init__(self, var): self.var = var
                def get(self): return self.var["valor"]

            widget = FotoWidget(foto_var)
            entries[etiqueta] = widget
            continue  # Saltar grid inferior

        # ── Campo de texto normal ──
        else:
            widget = tk.Entry(
                form,
                width=30,
                font=("Arial", 12),
                relief="solid",
                bd=1
            )

        # Posicionar widget
        widget.grid(row=i, column=1, sticky="w", pady=8)
        entries[etiqueta] = widget

    # Área para mostrar resultados
    frame_resultado = tk.Frame(tab, bd=1, relief="groove")
    frame_resultado.pack(fill="x", padx=10, pady=(0, 10))

    tk.Label(
        frame_resultado,
        text="Resultados de consulta",
        font=("Arial", 11, "bold"),
        anchor="w"
    ).pack(fill="x", padx=8, pady=(6, 2))

    # Scroll del área de resultados
    resultado_scroll = ttk.Scrollbar(frame_resultado, orient="vertical")

    # Caja de texto
    area_resultado = tk.Text(
        frame_resultado,
        height=8,
        font=("Courier", 11),
        relief="flat",
        bg="#f5f5f5",
        fg="#222222",
        state="disabled",
        wrap="word",
        yscrollcommand=resultado_scroll.set
    )

    resultado_scroll.config(command=area_resultado.yview)
    resultado_scroll.pack(side="right", fill="y")
    area_resultado.pack(fill="both", expand=True, padx=8, pady=(0, 8))

    # Crear botones CRUD
    construir_botones(tab, entries, area_resultado)


# Escribir resultados en el área de texto
def escribir_resultado(area, texto):
    area.config(state="normal")
    area.delete("1.0", tk.END)
    area.insert(tk.END, texto)
    area.config(state="disabled")


# Ejecutar acción con manejo de errores
def ejecutar(accion, area_resultado, mensaje_exito):
    try:
        print(">>> ejecutando...")
        resultado = accion()
        print(">>> OK")
        messagebox.showinfo("✔ Éxito", mensaje_exito)
        if resultado:
            escribir_resultado(area_resultado, resultado)
    except Exception as e:
        print(">>> ERROR REAL:", e)
        traceback.print_exc()
        messagebox.showerror("❌ Error", str(e))


# Crear botones CRUD
def construir_botones(tab, entries, area_resultado):

    nombre_entidad = tab.winfo_name()  # Nombre de la pestaña

    btn_frame = tk.Frame(tab)
    btn_frame.pack(pady=15)

    # Botón Guardar
    tk.Button(
        btn_frame, text="Guardar",
        font=("Arial", 12), bg="#4CAF50", fg="white", width=10,
        command=lambda: ejecutar(
            lambda: controlador.Guardar({k: v.get() for k, v in entries.items()}),
            area_resultado,
            "✔ Registro guardado correctamente.")
    ).pack(side=tk.LEFT, padx=5)

    # Botón Obtener
    tk.Button(
        btn_frame, text="Obtener",
        font=("Arial", 12), bg="#FF9800", fg="white", width=10,
        command=lambda: ejecutar(
            lambda: controlador.Obtener(nombre_entidad),
            area_resultado,
            "✔ Consulta realizada correctamente.")
    ).pack(side=tk.LEFT, padx=5)

    # Botón Actualizar
    tk.Button(
        btn_frame, text="Actualizar",
        font=("Arial", 12), bg="#2196F3", fg="white", width=10,
        command=lambda: ejecutar(
            lambda: controlador.Actualizar({k: v.get() for k, v in entries.items()}),
            area_resultado,
            "✔ Registro actualizado correctamente.")
    ).pack(side=tk.LEFT, padx=5)

    # Botón Eliminar
    tk.Button(
        btn_frame, text="Eliminar",
        font=("Arial", 12), bg="#f44336", fg="white", width=10,
        command=lambda: ejecutar(
            lambda: controlador.Eliminar(
                {k: v.get() for k, v in entries.items()},
                nombre_entidad
            ),
            area_resultado,
            "✔ Registro eliminado correctamente.")
    ).pack(side=tk.LEFT, padx=5)


# ─────────────── CREACIÓN DE FORMULARIOS ───────────────

# Formulario Estudiante
construir_formulario(tab_estudiante, "FORMULARIO DE ESTUDIANTE", "blue", [
    ("numero_matricula", True), ("nombres", True), ("apellidos", True),
    ("documento_identidad", True), ("fecha_nacimiento", True), ("direccion", True),
    ("correo_electronico", True), ("nombre_tutor", True), ("contacto_emergencia", True),
    ("fecha_ingreso", True), ("telefono", False), ("fotografia", False)
])

# Formulario Profesor
construir_formulario(tab_profesor, "FORMULARIO DE PROFESOR", "darkgreen", [
    ("codigo_empleado", True), ("nombres", True), ("apellidos", True),
    ("documento_identidad", True), ("fecha_nacimiento", True), ("direccion", True),
    ("correo_institucional", True), ("nivel_formacion", True), ("especialidad", True),
    ("anios_experiencia", True), ("fecha_contratacion", True), ("tipo_contrato", True),
    ("departamento", True), ("telefono", False),
])

# Formulario Asignatura
construir_formulario(tab_asignatura, "FORMULARIO DE ASIGNATURA", "purple", [
    ("codigo_asignatura", True), ("nombre", True), ("area_conocimiento", True),
    ("horas_teoricas", True), ("horas_practicas", True), ("creditos_academicos", True),
    ("objetivos_generales", True), ("objetivos_especificos", True),
    ("requisitos_previos", False), ("bibliografia", False),
])

# Formulario Curso
construir_formulario(tab_curso, "FORMULARIO DE CURSO", "darkorange", [
    ("codigo_curso", True), ("periodo_academico", True), ("asignatura", True),
    ("profesor_asignado", True), ("aula", True), ("horario_dias", True),
    ("horario_horas", True), ("cupo_maximo", True), ("metodologia_evaluacion", True),
    ("lista_estudiantes", False),
])

# Ejecutar aplicación
root.mainloop()