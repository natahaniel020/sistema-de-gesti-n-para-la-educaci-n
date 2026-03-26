# Sistema de Gestion Academica

Aplicacion de escritorio para la gestion de estudiantes, profesores, asignaturas y cursos. Permite registrar, consultar, actualizar y eliminar registros en una base de datos MySQL, y exportar reportes en formato Excel y PDF.

---

## Requisitos del sistema

- Python 3.10 o superior
- MySQL Server 8.0 o superior
- Windows 10 / 11 (el metodo `os.startfile` para abrir archivos exportados es exclusivo de Windows)
- pip actualizado

---

## Instalacion

### 1. Clonar o descargar el proyecto

```
git clone https://github.com/tu-usuario/gestion-academica.git
cd gestion-academica
```

O descomprimir el archivo `.zip` descargado y abrir la carpeta del proyecto.

---

### 2. Crear un entorno virtual (recomendado)

```
python -m venv venv
venv\Scripts\activate
```

---

### 3. Instalar dependencias de Python

```
pip install -r requirements.txt
```

Si no existe el archivo `requirements.txt`, instalar manualmente:

```
pip install pymysql
pip install tkcalendar
pip install tkinterdnd2
pip install pillow
pip install xlsxwriter
pip install reportlab
```

---

### 4. Configurar la base de datos

Abrir MySQL Workbench o cualquier cliente MySQL y ejecutar el script de creacion de base de datos:

```
source sql/gestion_academica.sql
```

Verificar que la base de datos `gestion_academica` exista y que los procedimientos almacenados esten creados correctamente.

---

### 5. Configurar la conexion a la base de datos

Abrir el archivo `persistencia.py` y ajustar los parametros de conexion en la propiedad `conexion` de la clase `BaseRepositorio`:

```python
self._conexion = pymysql.connect(
    host     = "localhost",   # Direccion del servidor MySQL
    user     = "root",        # Usuario de MySQL
    password = "tu_password", # Contrasena de MySQL
    database = "gestion_academica"
)
```

---

### 6. Configurar el favicon (opcional)

Abrir `interfaz.py` y cambiar la ruta en la variable `FAVICON_RUTA` por la ruta a tu archivo de icono:

```python
FAVICON_RUTA = "img/icono.ico"   # .ico o .png
```

Si no se dispone de un icono, dejar la ruta como esta. La aplicacion continuara sin favicon.

---

## Estructura del proyecto

```
gestion-academica/
├── interfaz.py        # Capa de presentacion (interfaz grafica Tkinter)
├── aplicacion.py      # Controlador (logica de negocio y exportacion)
├── dominio.py         # Clases de dominio (entidades del sistema)
├── fabrica.py         # Fabrica de objetos a partir de diccionarios
├── persistencia.py    # Repositorios y acceso a base de datos
├── sql/
│   └── gestion_academica.sql   # Script de creacion de BD y SPs
├── img/
│   └── icono.ico      # Icono de la aplicacion (opcional)
├── reportes/          # Carpeta generada automaticamente para exportaciones
└── README.md
```

---

## Ejecucion

Con el entorno virtual activo y la base de datos configurada, ejecutar:

```
python interfaz.py
```

---

## Uso de la aplicacion

### Navegacion

La ventana principal tiene cuatro pestanas: **Estudiante**, **Profesor**, **Asignatura** y **Curso**. Cada pestana contiene un formulario independiente con los campos de la entidad correspondiente.

---

### Operaciones CRUD

Cada formulario dispone de cuatro botones en la parte inferior:

| Boton      | Descripcion                                                                 |
|------------|-----------------------------------------------------------------------------|
| Guardar    | Inserta un nuevo registro con los datos ingresados en el formulario.        |
| Obtener    | Consulta todos los registros de la entidad y los muestra en el area inferior. |
| Actualizar | Modifica el registro cuyo identificador coincide con el campo de ID.        |
| Eliminar   | Elimina el registro correspondiente al ID ingresado.                        |

Los campos marcados sin la palabra **(opcional)** son obligatorios. Dejarlos vacios puede producir un error al guardar o actualizar.

---

### Campo de fotografia

El campo **fotografia** acepta imagenes en formato `.jpg`, `.jpeg`, `.png` y `.gif`.

Existen dos formas de cargar una imagen:

- **Arrastrar y soltar** el archivo directamente sobre el recuadro.
- **Hacer clic** sobre el recuadro para abrir el explorador de archivos.

El sistema muestra una miniatura de la imagen seleccionada dentro del recuadro. La ruta del archivo se almacena y se envia al controlador al momento de guardar o actualizar.

---

### Exportacion de reportes

El panel lateral derecho de cada pestana contiene los controles de exportacion:

| Boton          | Descripcion                                                        |
|----------------|--------------------------------------------------------------------|
| Exportar Excel | Genera un archivo `.xlsx` con todos los registros de la entidad.   |
| Exportar PDF   | Genera un archivo `.pdf` con todos los registros en formato tabla. |

Los archivos se guardan en la carpeta `reportes/` dentro del directorio del proyecto. El nombre del archivo corresponde al nombre de la entidad (por ejemplo, `estudiante.xlsx`).

Los archivos generados aparecen listados en el panel. Hacer **doble clic** sobre un elemento de la lista abre el archivo con el programa predeterminado del sistema.

---

### Cambio de tema

El boton **Oscuro / Claro** ubicado en la esquina superior derecha alterna entre el tema claro y el tema oscuro. El cambio se aplica inmediatamente a todos los elementos de la interfaz.

---

## Sololucion de problemas comunes

**La aplicacion no abre y muestra error de importacion**
Verificar que todas las dependencias esten instaladas con `pip list` y que el entorno virtual este activo.

**Error de conexion a la base de datos**
Revisar que MySQL este ejecutandose, que los datos en `persistencia.py` sean correctos y que el usuario tenga permisos sobre la base de datos `gestion_academica`.

**El drag and drop no funciona**
Confirmar que `tkinterdnd2` este instalado correctamente. En algunos sistemas puede requerir instalacion manual desde el repositorio oficial.

**Los archivos exportados no se abren con doble clic**
El metodo `os.startfile` solo funciona en Windows. En Linux o macOS se debe abrir el archivo manualmente desde la carpeta `reportes/`.

---

## Dependencias

| Paquete       | Version minima | Uso                                      |
|---------------|----------------|------------------------------------------|
| pymysql       | 1.0            | Conexion a base de datos MySQL           |
| tkcalendar    | 1.6            | Selector de fecha en formularios         |
| tkinterdnd2   | 0.3            | Soporte de drag and drop en Tkinter      |
| pillow        | 9.0            | Procesamiento de imagenes (fotografia)   |
| xlsxwriter    | 3.0            | Exportacion a Excel                      |
| reportlab     | 4.0            | Exportacion a PDF                        |