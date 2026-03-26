import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from aplicacion import Controlador
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD
import traceback
import os

# -----------------------------------------------------------------
# FAVICON
# Ruta local al archivo de icono de la ventana.
# Reemplaza esta ruta con la ubicacion real de tu archivo .ico o .png
# Ejemplo: "img/icono.ico"  o  "assets/favicon.png"
# -----------------------------------------------------------------
FAVICON_RUTA = "img/icono.ico"  # <-- cambia esta ruta

def aplicar_favicon(root):
    """
    Aplica el icono de ventana desde una ruta local.
    Soporta archivos .ico directamente con iconbitmap,
    y archivos .png mediante conversion con Pillow.
    Si el archivo no existe o falla la carga, continua sin icono.
    """
    try:
        if not os.path.exists(FAVICON_RUTA):
            return  # Archivo no encontrado, continuar sin icono

        extension = os.path.splitext(FAVICON_RUTA)[1].lower()

        if extension == ".ico":
            # Formato nativo de Windows, carga directa
            root.iconbitmap(FAVICON_RUTA)

        elif extension in (".png", ".jpg", ".jpeg", ".bmp"):
            # Convertir imagen a formato compatible con Tkinter
            img = Image.open(FAVICON_RUTA).resize((32, 32))
            tk_img = ImageTk.PhotoImage(img)
            root.iconphoto(True, tk_img)
            # Guardar referencia para evitar que el GC elimine la imagen
            root._favicon_ref = tk_img

    except Exception:
        pass  # Si falla, la aplicacion continua sin icono


# -----------------------------------------------------------------
# TEMAS
# Define dos paletas de colores: claro y oscuro.
# Cada clave representa el rol visual de un tipo de widget.
# -----------------------------------------------------------------
TEMAS = {
    "claro": {
        "bg":           "#f5f5f5",  # Fondo general de frames
        "fg":           "#222222",  # Texto general
        "entry_bg":     "#ffffff",  # Fondo de campos de entrada
        "entry_fg":     "#222222",  # Texto de campos de entrada
        "panel_bg":     "#ffffff",  # Fondo del panel lateral de exportacion
        "btn_toggle":   "#333333",  # Color del boton de cambio de tema
        "resultado_bg": "#eeeeee",  # Fondo del area de resultados
        "canvas_foto":  "#e0e0e0",  # Fondo del recuadro de fotografia
        "lista_bg":     "#ffffff",  # Fondo del listbox de archivos generados
        "lista_fg":     "#222222",  # Texto del listbox de archivos generados
    },
    "oscuro": {
        "bg":           "#1e1e1e",
        "fg":           "#f0f0f0",
        "entry_bg":     "#2d2d2d",
        "entry_fg":     "#f0f0f0",
        "panel_bg":     "#252525",
        "btn_toggle":   "#f0f0f0",
        "resultado_bg": "#2d2d2d",
        "canvas_foto":  "#3a3a3a",
        "lista_bg":     "#2d2d2d",
        "lista_fg":     "#f0f0f0",
    }
}

# Estado global del tema activo
tema_actual = {"nombre": "claro"}

# Registro de widgets para repintado al cambiar tema.
# Cada elemento es una tupla (widget, rol).
widgets_tema = []


def registrar(widget, rol):
    """
    Registra un widget con su rol visual.
    Al cambiar el tema, aplicar_tema() recorre esta lista
    y aplica los colores correspondientes a cada rol.

    Roles disponibles:
        bg         : solo fondo
        fg         : solo texto
        bg+fg      : fondo y texto
        entry      : campo de entrada (fondo, texto, cursor)
        panel      : panel lateral de exportacion
        resultado  : area de texto de resultados
        canvas_foto: recuadro de fotografia
        lista      : listbox de archivos exportados
    """
    widgets_tema.append((widget, rol))


def aplicar_tema():
    """
    Recorre todos los widgets registrados y aplica los colores
    del tema actualmente seleccionado en tema_actual.
    """
    t = TEMAS[tema_actual["nombre"]]
    for widget, rol in widgets_tema:
        try:
            if rol == "bg":
                widget.config(bg=t["bg"])
            elif rol == "fg":
                widget.config(fg=t["fg"])
            elif rol == "bg+fg":
                widget.config(bg=t["bg"], fg=t["fg"])
            elif rol == "entry":
                # insertbackground define el color del cursor de escritura
                widget.config(
                    bg=t["entry_bg"],
                    fg=t["entry_fg"],
                    insertbackground=t["entry_fg"]
                )
            elif rol == "panel":
                widget.config(bg=t["panel_bg"])
            elif rol == "resultado":
                widget.config(bg=t["resultado_bg"], fg=t["fg"])
            elif rol == "canvas_foto":
                widget.config(bg=t["canvas_foto"])
            elif rol == "lista":
                widget.config(bg=t["lista_bg"], fg=t["lista_fg"])
        except Exception:
            pass  # Ignorar widgets destruidos o que no soporten el atributo


def toggle_tema(btn):
    """
    Alterna entre tema claro y oscuro.
    Actualiza el texto del boton y repinta todos los widgets registrados.
    """
    tema_actual["nombre"] = "oscuro" if tema_actual["nombre"] == "claro" else "claro"
    btn.config(text="Claro" if tema_actual["nombre"] == "oscuro" else "Oscuro")
    aplicar_tema()


# -----------------------------------------------------------------
# VENTANA PRINCIPAL
# TkinterDnD.Tk() reemplaza tk.Tk() para habilitar drag & drop
# en toda la aplicacion.
# -----------------------------------------------------------------
root = TkinterDnD.Tk()
root.geometry('1100x700')
root.title("Sistema de Gestion Academica")
aplicar_favicon(root)

# Barra superior con boton de cambio de tema
barra_top = tk.Frame(root, height=40)
barra_top.pack(fill="x", side="top")
registrar(barra_top, "bg")

btn_tema = tk.Button(
    barra_top, text="Oscuro",
    font=("Arial", 10), relief="flat", cursor="hand2",
    command=lambda: toggle_tema(btn_tema)
)
btn_tema.pack(side="right", padx=12, pady=6)
registrar(btn_tema, "bg+fg")

# Contenedor de pestanas. El name de cada Frame se usa como
# identificador de entidad en el controlador.
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

tab_estudiante = ttk.Frame(notebook, name='estudiante')
tab_profesor   = ttk.Frame(notebook, name='profesor')
tab_asignatura = ttk.Frame(notebook, name='asignatura')
tab_curso      = ttk.Frame(notebook, name='curso')

notebook.add(tab_estudiante, text="Estudiante")
notebook.add(tab_profesor,   text="Profesor")
notebook.add(tab_asignatura, text="Asignatura")
notebook.add(tab_curso,      text="Curso")

# Instancia unica del controlador compartida por todos los formularios
controlador = Controlador()


# -----------------------------------------------------------------
# CAMPO FOTOGRAFIA
# Widget personalizado con Canvas de 120x120 px que muestra
# una miniatura de la imagen seleccionada.
# Soporta seleccion por clic y por arrastre (drag & drop).
# Retorna un objeto FotoWidget con metodo .get() -> str | None
# -----------------------------------------------------------------
def construir_campo_foto(form, i):
    """
    Construye y posiciona el campo de fotografia en el formulario.

    Parametros:
        form : Frame padre donde se posiciona el widget
        i    : Numero de fila en el grid del formulario

    Retorna:
        FotoWidget con metodo .get() que devuelve la ruta del archivo
        seleccionado, o None si no se ha cargado ninguna imagen.
    """
    EXTENSIONES_VALIDAS = (".jpg", ".jpeg", ".png", ".gif")

    # Diccionario mutable para compartir estado entre closures.
    # tk_img se conserva como referencia para evitar que el
    # recolector de basura elimine la imagen de memoria.
    foto_var = {"ruta": None, "tk_img": None}

    # Canvas que actua como zona de drop y previa de la imagen
    canvas_foto = tk.Canvas(
        form, width=120, height=120,
        relief="solid", bd=1,
        bg=TEMAS[tema_actual["nombre"]]["canvas_foto"],
        cursor="hand2"
    )
    canvas_foto.grid(row=i, column=1, sticky="w", pady=8)
    registrar(canvas_foto, "canvas_foto")

    # Texto de instruccion inicial centrado en el canvas
    canvas_foto.create_text(
        60, 55,
        text="Arrastra\nuna foto\naqui",
        font=("Arial", 10),
        fill="gray",
        justify="center",
        tags="placeholder"
    )

    def cargar_imagen(ruta):
        """
        Carga una imagen desde la ruta indicada, la redimensiona
        manteniendo proporciones y la muestra en el canvas.
        Valida la extension antes de procesar.
        """
        if not ruta:
            return

        # tkinterdnd2 envuelve rutas con espacios entre llaves
        ruta = ruta.strip().strip("{}")

        if not ruta.lower().endswith(EXTENSIONES_VALIDAS):
            messagebox.showwarning(
                "Formato no valido",
                f"Solo se aceptan: {', '.join(EXTENSIONES_VALIDAS)}"
            )
            return

        # Abrir y redimensionar conservando proporciones (max 120x120)
        img = Image.open(ruta)
        img.thumbnail((120, 120), Image.LANCZOS)

        # Convertir a formato compatible con Tkinter
        tk_img = ImageTk.PhotoImage(img)

        # Actualizar estado y mostrar imagen en el canvas
        foto_var["ruta"]   = ruta
        foto_var["tk_img"] = tk_img
        canvas_foto.delete("all")
        canvas_foto.create_image(60, 60, image=tk_img, anchor="center")

    # Registrar canvas como destino de arrastre de archivos
    canvas_foto.drop_target_register(DND_FILES)
    canvas_foto.dnd_bind("<<Drop>>", lambda e: cargar_imagen(e.data))

    # Clic izquierdo abre el explorador de archivos como alternativa
    canvas_foto.bind("<Button-1>", lambda e: cargar_imagen(
        filedialog.askopenfilename(
            title="Seleccionar fotografia",
            filetypes=[("Imagenes", "*.jpg *.jpeg *.png *.gif")]
        )
    ))

    # Clase interna que simula la interfaz .get() de los demas widgets
    class FotoWidget:
        def __init__(self, var):
            self.var = var
        def get(self):
            return self.var["ruta"]

    return FotoWidget(foto_var)


# -----------------------------------------------------------------
# PANEL LATERAL DE EXPORTACION
# Panel de ancho fijo a la derecha del formulario con botones
# para exportar a Excel y PDF, y un listbox que acumula los
# archivos generados en la sesion actual.
# -----------------------------------------------------------------
def construir_panel_exportar(contenedor, nombre_entidad):
    """
    Construye el panel lateral de exportacion dentro del contenedor.

    Parametros:
        contenedor     : Frame padre (layout horizontal)
        nombre_entidad : Nombre de la pestaña/entidad activa

    Retorna el Frame del panel para uso externo si se necesita.
    """
    t = TEMAS[tema_actual["nombre"]]

    panel = tk.Frame(contenedor, width=350, bd=1, relief="groove")
    panel.pack(side="right", fill="y", padx=(5, 8), pady=8)
    panel.pack_propagate(False)  # Mantener ancho fijo de 220 px
    registrar(panel, "panel")

    tk.Label(
        panel, text="Exportar",
        font=("Arial", 12, "bold")
    ).pack(pady=(12, 4))

    # Boton para exportar a Excel
    tk.Button(
        panel, text="Exportar Excel",
        font=("Arial", 11), bg="#1D6F42", fg="white",
        relief="flat", cursor="hand2", width=18,
        command=lambda: _exportar("excel", nombre_entidad, lista_archivos)
    ).pack(pady=(8, 4), padx=10)

    # Boton para exportar a PDF
    tk.Button(
        panel, text="Exportar PDF",
        font=("Arial", 11), bg="#C0392B", fg="white",
        relief="flat", cursor="hand2", width=18,
        command=lambda: _exportar("pdf", nombre_entidad, lista_archivos)
    ).pack(pady=4, padx=10)

    # Etiqueta de seccion para el historial de archivos
    tk.Label(
        panel, text="Archivos generados:",
        font=("Arial", 10, "bold")
    ).pack(pady=(14, 2))

    # Frame interno para el listbox con barra de desplazamiento
    frame_lista = tk.Frame(panel)
    frame_lista.pack(fill="both", expand=True, padx=6, pady=(0, 8))

    scroll_lista = ttk.Scrollbar(frame_lista, orient="vertical")

    lista_archivos = tk.Listbox(
        frame_lista,
        font=("Arial", 9),
        relief="flat",
        bg=t["lista_bg"], fg=t["lista_fg"],
        selectbackground="#4a90d9",
        activestyle="none",
        yscrollcommand=scroll_lista.set,
        cursor="hand2"
    )
    scroll_lista.config(command=lista_archivos.yview)
    scroll_lista.pack(side="right", fill="y")
    lista_archivos.pack(fill="both", expand=True)
    registrar(lista_archivos, "lista")

    # Doble clic sobre un elemento abre el archivo con el programa
    # predeterminado del sistema operativo
    lista_archivos.bind(
        "<Double-Button-1>",
        lambda e: _abrir_archivo(lista_archivos)
    )

    tk.Label(
        panel, text="(doble clic para abrir)",
        font=("Arial", 8), fg="gray"
    ).pack(pady=(0, 6))

    return panel


def _exportar(tipo, nombre_entidad, lista_archivos):
    """
    Llama al metodo de exportacion del controlador segun el tipo,
    agrega el nombre del archivo al historial del panel y muestra
    un mensaje de confirmacion o error segun el resultado.

    Parametros:
        tipo           : "excel" o "pdf"
        nombre_entidad : Identificador de la entidad activa
        lista_archivos : Listbox donde se registran los archivos
    """
    try:
        if tipo == "excel":
            ruta  = controlador.exportar_a_excel(nombre_entidad)
            prefijo = "[XLS]"
        else:
            ruta  = controlador.exportar_a_pdf(nombre_entidad)
            prefijo = "[PDF]"

        nombre_archivo = os.path.basename(ruta) if ruta else f"{nombre_entidad}.{tipo}"
        lista_archivos.insert(0, f"{prefijo} {nombre_archivo}")
        messagebox.showinfo("Exito", f"Archivo generado:\n{nombre_archivo}")

    except Exception as e:
        traceback.print_exc()
        messagebox.showerror("Error", str(e))


def _abrir_archivo(lista_archivos):
    """
    Abre el archivo seleccionado en el listbox usando el programa
    predeterminado del sistema. Muestra advertencia si no se
    encuentra el archivo en disco.
    """
    sel = lista_archivos.curselection()
    if not sel:
        return

    # Extraer nombre de archivo eliminando el prefijo [XLS] o [PDF]
    nombre = lista_archivos.get(sel[0]).split(" ", 1)[-1].strip()

    if os.path.exists(nombre):
        os.startfile(nombre)  # Disponible solo en Windows
    else:
        messagebox.showwarning(
            "No encontrado",
            f"No se encontro el archivo:\n{nombre}"
        )


# -----------------------------------------------------------------
# CONSTRUCTOR DE FORMULARIOS
# Genera dinamicamente el formulario de cada entidad a partir de
# una lista de campos. Detecta el tipo de widget segun el nombre
# del campo: DateEntry para fechas, FotoWidget para fotografia,
# y Entry de texto para el resto.
# -----------------------------------------------------------------
def construir_formulario(tab, titulo, color, campos):
    """
    Construye el formulario completo de una pestaña incluyendo:
      - Titulo con color de la entidad
      - Canvas con scroll vertical para formularios largos
      - Campos dinamicos segun tipo detectado
      - Area de resultados de consulta
      - Botones CRUD

    Parametros:
        tab    : Frame de la pestaña destino
        titulo : Texto del encabezado del formulario
        color  : Color del titulo (nombre o hex)
        campos : Lista de tuplas (nombre_campo, es_obligatorio)
    """
    t = TEMAS[tema_actual["nombre"]]

    # Contenedor horizontal principal: formulario a la izquierda,
    # panel de exportacion a la derecha
    contenedor = tk.Frame(tab)
    contenedor.pack(fill="both", expand=True)
    registrar(contenedor, "bg")

    # El panel se construye primero para que quede a la derecha
    # al usar pack con side="left" en el formulario
    nombre_entidad = tab.winfo_name()
    construir_panel_exportar(contenedor, nombre_entidad)

    # Columna izquierda: titulo + canvas con scroll + formulario
    frame_superior = tk.Frame(contenedor)
    frame_superior.pack(side="left", fill="both", expand=True)
    registrar(frame_superior, "bg")

    lbl_titulo = tk.Label(
        frame_superior, text=titulo,
        font=("Arial", 14, "bold"), fg=color
    )
    lbl_titulo.pack(pady=10)
    registrar(lbl_titulo, "bg")

    # Canvas + scrollbar para desplazar formularios con muchos campos
    canvas = tk.Canvas(frame_superior, highlightthickness=0)
    scroll = ttk.Scrollbar(frame_superior, orient="vertical", command=canvas.yview)
    frame_inner = ttk.Frame(canvas)

    # Actualizar la region de scroll cuando cambia el tamanio interno
    frame_inner.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=frame_inner, anchor="nw")
    canvas.configure(yscrollcommand=scroll.set)
    canvas.pack(side="left", fill="both", expand=True)
    scroll.pack(side="right", fill="y")

    # Frame interno donde se ubican etiquetas y widgets del formulario
    form = tk.Frame(frame_inner)
    form.pack(pady=10, padx=50, anchor="w")
    registrar(form, "bg")

    # Diccionario que almacena los widgets de entrada por nombre de campo
    entries = {}

    # Generacion dinamica de campos
    for i, (etiqueta, obligatorio) in enumerate(campos):

        # Indicar campos opcionales en la etiqueta
        sufijo = "" if obligatorio else " (opcional)"

        lbl = tk.Label(
            form,
            text=etiqueta + sufijo + ":",
            font=("Arial", 12)
        )
        lbl.grid(row=i, column=0, sticky="w", padx=(0, 10), pady=8)
        registrar(lbl, "bg+fg")

        # Campo de fecha: usa DateEntry con selector de calendario
        if "fecha" in etiqueta.lower():
            widget = DateEntry(
                form, width=28, font=("Arial", 12),
                date_pattern="yyyy-mm-dd", relief="solid", bd=1
            )

        # Campo de fotografia: widget personalizado con Pillow y DnD
        elif etiqueta.lower() == "fotografia":
            entries[etiqueta] = construir_campo_foto(form, i)
            continue  # El widget ya se posiciona internamente, saltar grid

        # Campo de texto generico para el resto de campos
        else:
            widget = tk.Entry(
                form, width=30, font=("Arial", 12),
                relief="solid", bd=1,
                bg=t["entry_bg"], fg=t["entry_fg"]
            )
            registrar(widget, "entry")

        # Posicionar el widget en la columna 1 del grid
        widget.grid(row=i, column=1, sticky="w", pady=8)
        entries[etiqueta] = widget

    # Area de resultados debajo del formulario, dentro de la pestaña
    # (fuera del canvas para que siempre sea visible sin hacer scroll)
    frame_resultado = tk.Frame(tab, bd=1, relief="groove")
    frame_resultado.pack(fill="x", padx=10, pady=(0, 5))
    registrar(frame_resultado, "bg")

    lbl_res = tk.Label(
        frame_resultado,
        text="Resultados de consulta",
        font=("Arial", 11, "bold"), anchor="w"
    )
    lbl_res.pack(fill="x", padx=8, pady=(4, 2))
    registrar(lbl_res, "bg+fg")

    resultado_scroll = ttk.Scrollbar(frame_resultado, orient="vertical")

    # Caja de texto de solo lectura para mostrar resultados de consultas
    area_resultado = tk.Text(
        frame_resultado,
        height=6,              # Reducido de 8 a 6 para minimizar espacio en blanco
        font=("Courier", 11),
        relief="flat",
        bg=t["resultado_bg"], fg=t["fg"],
        state="disabled",      # Solo lectura; se habilita al escribir
        wrap="word",
        yscrollcommand=resultado_scroll.set
    )
    registrar(area_resultado, "resultado")

    resultado_scroll.config(command=area_resultado.yview)
    resultado_scroll.pack(side="right", fill="y")
    area_resultado.pack(fill="x", padx=8, pady=(0, 4))

    # Botones CRUD justo debajo del area de resultados
    construir_botones(tab, entries, area_resultado)


# -----------------------------------------------------------------
# UTILIDADES DE INTERFAZ
# -----------------------------------------------------------------
def escribir_resultado(area, texto):
    """
    Escribe texto en el area de resultados.
    Habilita temporalmente la escritura, reemplaza el contenido
    y vuelve a deshabilitar para mantenerla de solo lectura.
    """
    area.config(state="normal")
    area.delete("1.0", tk.END)
    area.insert(tk.END, texto)
    area.config(state="disabled")


def ejecutar(accion, area_resultado, mensaje_exito):
    """
    Ejecuta una accion del controlador con manejo centralizado
    de errores. Muestra mensaje de exito y escribe el resultado
    en el area de consulta si lo hay.

    Parametros:
        accion          : Funcion lambda sin argumentos a ejecutar
        area_resultado  : Widget Text donde mostrar el resultado
        mensaje_exito   : Texto a mostrar en el dialogo de exito
    """
    try:
        resultado = accion()
        messagebox.showinfo("Exito", mensaje_exito)
        if resultado:
            escribir_resultado(area_resultado, resultado)
    except Exception as e:
        traceback.print_exc()
        messagebox.showerror("Error", str(e))


# -----------------------------------------------------------------
# BOTONES CRUD
# Genera los cuatro botones de operacion para cada formulario.
# Cada boton ejecuta el metodo correspondiente del controlador
# pasando los datos actuales del formulario como diccionario.
# -----------------------------------------------------------------
def construir_botones(tab, entries, area_resultado):
    """
    Construye la barra de botones CRUD de un formulario.

    Parametros:
        tab            : Frame de la pestaña (para obtener nombre entidad)
        entries        : Diccionario {campo: widget} del formulario
        area_resultado : Widget Text para mostrar resultados
    """
    # El nombre de la pestaña identifica la entidad en el controlador
    nombre_entidad = tab.winfo_name()

    btn_frame = tk.Frame(tab)
    btn_frame.pack(pady=6)
    registrar(btn_frame, "bg")

    # Definicion de botones: (texto, color_fondo, accion, mensaje_exito)
    botones = [
        (
            "Guardar", "#4CAF50",
            lambda: controlador.Guardar({k: v.get() for k, v in entries.items()}),
            "Registro guardado correctamente."
        ),
        (
            "Obtener", "#FF9800",
            lambda: controlador.obtener(nombre_entidad),
            "Consulta realizada correctamente."
        ),
        (
            "Actualizar", "#2196F3",
            lambda: controlador.Actualizar({k: v.get() for k, v in entries.items()}),
            "Registro actualizado correctamente."
        ),
        (
            "Eliminar", "#f44336",
            lambda: controlador.Eliminar(
                {k: v.get() for k, v in entries.items()},
                nombre_entidad
            ),
            "Registro eliminado correctamente."
        ),
    ]

    for texto, color, accion, msg in botones:
        tk.Button(
            btn_frame, text=texto,
            font=("Arial", 12), bg=color, fg="white", width=10,
            command=lambda a=accion, m=msg: ejecutar(a, area_resultado, m)
        ).pack(side=tk.LEFT, padx=5)


# -----------------------------------------------------------------
# CREACION DE FORMULARIOS
# Un formulario por cada entidad del sistema.
# Los campos marcados con True son obligatorios.
# -----------------------------------------------------------------

construir_formulario(tab_estudiante, "FORMULARIO DE ESTUDIANTE", "blue", [
    ("numero_matricula",   True),
    ("nombres",            True),
    ("apellidos",          True),
    ("documento_identidad",True),
    ("fecha_nacimiento",   True),
    ("direccion",          True),
    ("correo_electronico", True),
    ("nombre_tutor",       True),
    ("contacto_emergencia",True),
    ("fecha_ingreso",      True),
    ("telefono",           False),
    ("fotografia",         False),
])

construir_formulario(tab_profesor, "FORMULARIO DE PROFESOR", "darkgreen", [
    ("codigo_empleado",    True),
    ("nombres",            True),
    ("apellidos",          True),
    ("documento_identidad",True),
    ("fecha_nacimiento",   True),
    ("direccion",          True),
    ("correo_institucional",True),
    ("nivel_formacion",    True),
    ("especialidad",       True),
    ("anios_experiencia",  True),
    ("fecha_contratacion", True),
    ("tipo_contrato",      True),
    ("departamento",       True),
    ("telefono",           False),
    ("fotografia",         False),
])

construir_formulario(tab_asignatura, "FORMULARIO DE ASIGNATURA", "purple", [
    ("codigo_asignatura",    True),
    ("nombre",               True),
    ("area_conocimiento",    True),
    ("horas_teoricas",       True),
    ("horas_practicas",      True),
    ("creditos_academicos",  True),
    ("objetivos_generales",  True),
    ("objetivos_especificos",True),
    ("requisitos_previos",   False),
    ("bibliografia",         False),
])

construir_formulario(tab_curso, "FORMULARIO DE CURSO", "darkorange", [
    ("codigo_curso",           True),
    ("periodo_academico",      True),
    ("asignatura",             True),
    ("profesor_asignado",      True),
    ("aula",                   True),
    ("horario_dias",           True),
    ("horario_horas",          True),
    ("cupo_maximo",            True),
    ("metodologia_evaluacion", True),
])

# Aplicar colores del tema inicial antes de mostrar la ventana
aplicar_tema()

root.mainloop()