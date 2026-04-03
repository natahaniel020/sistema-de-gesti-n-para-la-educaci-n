# Sistema de Gestión Académica

## Descripción General

Sistema orientado a objetos desarrollado en Python para la gestión de entidades académicas. El sistema permite registrar y administrar estudiantes, profesores, asignaturas, cursos, aulas, calificaciones, periodos académicos, planes de estudio, material bibliográfico, préstamos y actividades extracurriculares.

El diseño sigue una arquitectura modular de cuatro capas con responsabilidades claramente separadas. Cada módulo tiene un único rol dentro del sistema y no conoce los detalles internos de los demás.

---

## Arquitectura del Sistema

```
Módulo 4  →  Módulo 5  →  Módulo 2  →  Módulo 3  →  Módulo 1
Tkinter      Infraest.    Controlador   Fábrica       Clases Puras
                                                    + Serializador
```

El flujo de datos es unidireccional. El usuario interactúa con Tkinter, que delega en la Infraestructura, que coordina con el Controlador, que usa la Fábrica para construir objetos, que finalmente son serializados y almacenados.

---

## Módulos

### Módulo 1 — Clases Puras y Serializador (`modulo1.py`)

Contiene las once clases del dominio del sistema y la clase `Serializador`.

**Responsabilidad:** Definir la estructura de datos de cada entidad y sus invariantes locales. Las clases no tienen lógica de base de datos, no conocen a los demás módulos y no saben que el serializador existe.

**Regla de oro:** Ninguna clase de este módulo tiene métodos que empiecen con `guardar`, `convertir`, `serializar` o `conectar`.

#### Clases del dominio

| Clase | Clave primaria |
|---|---|
| `Estudiante` | `numero_matricula` |
| `Profesor` | `codigo_empleado` |
| `Asignatura` | `codigo_asignatura` |
| `Curso` | `codigo_curso` |
| `PeriodoAcademico` | `codigo_periodo` |
| `Calificacion` | `id_calificacion` |
| `Aula` | `id_aula` |
| `PlanDeEstudios` | `codigo_plan` |
| `MaterialBibliografico` | `codigo_material` |
| `Prestamo` | `codigo_prestamo` |
| `ActividadExtracurricular` | `codigo_actividad` |

Cada clase:
- Tiene un `__init__` con sus atributos únicos tipados.
- Todos los atributos son públicos dado que el sistema en su estado actual solo registra información.
- Valida sus **invariantes locales** directamente en el constructor. Si los datos son inválidos, el objeto no se crea y se lanza una `ValueError`.
- No valida invariantes sistémicas (unicidad, integridad referencial) porque para eso necesitaría consultar el estado global del sistema, lo cual no es su responsabilidad.

#### Tipos de atributos utilizados

| Tipo Python | Uso |
|---|---|
| `str` | Textos, códigos, claves primarias y foráneas |
| `int` | Enteros como horas, créditos, capacidad |
| `float` | Valores decimales como calificaciones y porcentajes |
| `datetime.date` | Fechas |
| `Optional[str]` | Campos de texto opcionales |
| `Optional[int]` | Campos numéricos opcionales |
| `Optional[float]` | Campos decimales opcionales |
| `Optional[bytes]` | Archivos binarios como fotografías |
| `list[str]` | Listas de códigos (estudiantes, participantes) |
| `dict[int, list[str]]` | Asignaturas organizadas por nivel |
| `Optional[dict]` | Calendarios de actividades |
| `int \| uuid.UUID` | Clave primaria autogenerada de Calificacion |

#### Serializador Universal

Clase estática dentro del Módulo 1 que convierte cualquier objeto del dominio en un diccionario plano apto para ser almacenado.

```python
Serializador.convertir(objeto)  →  dict
```

Usa `vars(objeto)` para extraer los atributos de forma genérica sin importar el tipo de clase. Maneja las siguientes conversiones:

| Tipo de entrada | Resultado |
|---|---|
| `datetime.date` / `datetime` | `str` en formato ISO (`"2024-03-15"`) |
| `uuid.UUID` | `str` |
| `bytes` | `None` (los binarios no se almacenan en el dict) |
| `list` | Lista con cada elemento convertido recursivamente |
| `dict` | Diccionario con cada valor convertido recursivamente |
| `float` | `float` redondeado a 2 decimales |
| `str`, `int`, `bool`, `None` | Se pasan sin transformación |

---

### Módulo 2 — Controlador (`modulo2.py`)

**Responsabilidad:** Coordinar el flujo completo entre todos los módulos. No crea objetos, no valida datos de negocio y no accede a la estructura de datos directamente más allá de almacenar el resultado.

Esta clase no tiene constructor porque no recibe atributos de instancia. La estructura de datos es un atributo de clase compartido por todas las instancias.

#### Estructura de datos interna

```python
datos = {
    'estudiantes'   : {},   # clave: numero_matricula
    'profesores'    : {},   # clave: codigo_empleado
    'asignaturas'   : {},   # clave: codigo_asignatura
    'cursos'        : {},   # clave: codigo_curso
    'periodos'      : {},   # clave: codigo_periodo
    'calificaciones': {},   # clave: id_calificacion
    'aulas'         : {},   # clave: id_aula
    'planes'        : {},   # clave: codigo_plan
    'materiales'    : {},   # clave: codigo_material
    'prestamos'     : {},   # clave: codigo_prestamo
    'actividades'   : {},   # clave: codigo_actividad
}
```

#### Método principal

```python
def registrar(self, datos: dict) -> dict
```

Flujo exacto por cada llamada:

```
1. Recibe dict con datos crudos del Módulo 5
2. Llama a Fabrica.crear(datos)        → obtiene objeto puro
3. Llama a Serializador.convertir(obj) → obtiene dict serializado
4. Almacena el dict en la estructura de datos
5. Retorna el dict al Módulo 5
```

#### Métodos de apoyo internos

| Método | Responsabilidad |
|---|---|
| `_almacenar(diccionario)` | Determina la tabla y clave, y guarda el dict |
| `_resolver_destino(diccionario)` | Identifica a qué colección pertenece el dict según su clave primaria |

#### Apertura a base de datos

El Controlador está diseñado para que en el futuro, si se migra a una base de datos real, solo sea necesario modificar el método `_almacenar`. El flujo principal `registrar` no cambia.

---

### Módulo 3 — Fábrica de Objetos (`modulo3.py`)

**Responsabilidad:** Recibir un diccionario de datos crudos proveniente de Tkinter (donde todos los valores son `str`), identificar a qué clase pertenece, convertir los tipos necesarios e instanciar el objeto correspondiente.

Esta clase no tiene constructor.

#### Método principal

```python
def crear(self, datos: dict) -> objeto
```

Identifica la clase destino inspeccionando qué clave primaria está presente en el diccionario recibido:

| Clave detectada | Clase instanciada |
|---|---|
| `numero_matricula` | `Estudiante` |
| `codigo_empleado` | `Profesor` |
| `codigo_asignatura` | `Asignatura` |
| `codigo_curso` | `Curso` |
| `codigo_periodo` | `PeriodoAcademico` |
| `id_calificacion` | `Calificacion` |
| `id_aula` | `Aula` |
| `codigo_plan` | `PlanDeEstudios` |
| `codigo_material` | `MaterialBibliografico` |
| `codigo_prestamo` | `Prestamo` |
| `codigo_actividad` | `ActividadExtracurricular` |

#### Conversiones de tipo que realiza

Dado que Tkinter entrega todos los valores como `str`, la Fábrica realiza las siguientes conversiones antes de instanciar:

| Conversión | Ejemplo |
|---|---|
| `str` → `datetime.date` | `"2024-03-15"` → `date.fromisoformat(...)` |
| `str` → `int` | `"30"` → `int(...)` |
| `str` → `float` | `"4.5"` → `float(...)` |
| Campo ausente → `None` | `datos.get('telefono')` |
| Campo lista ausente → `[]` | `datos.get('lista_estudiantes', [])` |

#### Apertura a invariantes

Cada método privado de creación tiene una zona claramente definida para agregar validaciones en el futuro sin modificar la estructura:

```python
def _crear_aula(self, datos):

    # Zona 1 — conversión de tipos
    piso      = int(datos['piso'])
    capacidad = int(datos['capacidad'])

    # Zona 2 — invariantes (se agregan aquí cuando corresponda)
    # if capacidad <= 0:
    #     raise ValueError(...)

    # Zona 3 — instanciación
    return Aula(piso=piso, capacidad=capacidad, ...)
```

---

### Módulo 4 — Interfaz Gráfica Tkinter (`modulo4.py`)

**Responsabilidad:** Presentar los formularios al usuario y capturar los datos ingresados. No tiene lógica de negocio, no valida datos y no conoce al Controlador ni a la Fábrica.

Contiene once pestañas, una por cada entidad del sistema. Cada formulario es generado por una función genérica que recibe el título, color y lista de campos.

#### Función genérica `construir_formulario`

```python
construir_formulario(tab, titulo, color, campos)
```

Recibe una lista de tuplas `(etiqueta, obligatorio)` y construye el formulario completo con scroll vertical, marcando cada campo con `*` si es obligatorio u `(opcional)` si no lo es.

#### Botones disponibles en cada formulario

| Botón | Color | Función futura |
|---|---|---|
| Guardar | Verde | Registrar nuevo dato |
| Actualizar | Azul | Modificar dato existente |
| Eliminar | Rojo | Eliminar dato existente |
| Limpiar | Naranja | Vaciar los campos del formulario |

Los botones no tienen funcionalidad asignada todavía. Su conexión con el sistema se realizará a través del Módulo 5.

---

### Módulo 5 — Infraestructura (`modulo5.py`)

> ⚠️ **Este módulo no tiene implementación.**

Su rol es actuar como puente entre el Módulo 4 (Tkinter) y el Módulo 2 (Controlador). Se encargará de:

- Recolectar los valores de los campos `Entry` de Tkinter y construir el diccionario de datos crudos.
- Pasar ese diccionario al Controlador.
- Recibir el resultado o excepción del Controlador y traducirlo a un mensaje visible en la interfaz.
- Limpiar los formularios tras un registro exitoso.

La razón por la que este módulo no está implementado es que su funcionamiento requiere conocimientos de conexión entre eventos de Tkinter y lógica de aplicación que aún no han sido cubiertos en el curso.

Cuando se implemente, el Módulo 4 solo conocerá al Módulo 5 y el Módulo 5 solo conocerá al Módulo 2. Tkinter y el sistema permanecerán completamente desacoplados.

---

## Estructura de Archivos

```
proyecto/
│
├── modulo1.py   — Clases puras del dominio + Serializador
├── modulo2.py   — Controlador
├── modulo3.py   — Fábrica de objetos
├── modulo4.py   — Interfaz gráfica Tkinter
├── modulo5.py   — Infraestructura (sin implementación)
└── README.md    — Este archivo
```

---

## Flujo Completo de un Registro

```
Usuario llena formulario en Tkinter (Módulo 4)
        ↓
Módulo 5 recolecta los Entry y construye dict  ← pendiente
        ↓
Módulo 2 recibe dict y coordina el flujo
        ↓
Módulo 3 identifica la clase, convierte tipos e instancia el objeto
        ↓
Módulo 1 valida invariantes locales en el constructor
        ↓
Módulo 1 Serializador convierte el objeto a dict
        ↓
Módulo 2 almacena el dict en la estructura de datos
        ↓
Módulo 5 muestra confirmación en Tkinter  ← pendiente
```

---

## Decisiones de Diseño

**Atributos públicos.** Dado que el sistema en su estado actual solo registra información sin operaciones de modificación o eliminación, todos los atributos de las clases son públicos. Esta decisión se revisará cuando el sistema incorpore operaciones de actualización.

**Clases sin herencia.** Ninguna entidad hereda de otra porque ninguna cumple la relación "ES UN". Las relaciones entre entidades son asociaciones mediante claves foráneas (`str` con el código de referencia).

**Fábrica universal.** En lugar de una fábrica por cada clase, existe una única clase `Fabrica` que identifica el tipo de objeto a construir inspeccionando las claves del diccionario recibido. Esto simplifica el Controlador, que siempre llama al mismo punto de entrada.

**Serializador universal.** En lugar de un método `to_dict()` en cada clase, existe una clase estática que usa `vars(objeto)` para extraer los atributos de cualquier objeto de forma genérica. Las clases del dominio permanecen limpias.

**Invariantes en el constructor.** Cada clase valida sus propias reglas locales al momento de ser instanciada. Si los datos son inválidos, el objeto no nace. Las reglas que requieren consultar el estado global del sistema son invariantes sistémicas y le corresponden al Controlador.