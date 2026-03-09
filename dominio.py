"""
 1 Clases Puras + Serializador Clases puras (Data Classes)

- Estudiante
- Profesor
- Asignatura · Curso
- Aula · PeriodoAcademico
- alificacion · Prestamo
- MaterialBibliografico
- PlanDeEstudios · Actividad

Serializador Universal
- Recibe cualquier objeto
- Usa
- vars(objeto)
- genérico
- Convierte date → isoformat()
- Itera listas si aplica
- Ret1orna dict plano

"""
from datetime import date, datetime
from typing import Optional, Any
import uuid

class Serializador:
    """
    Utilidad encargada de convertir objetos del dominio en estructuras
    de datos serializables (diccionarios).

    Se utiliza principalmente para transformar objetos complejos en
    representaciones que puedan almacenarse, transmitirse o imprimirse.
    """

    @staticmethod
    def convertir(objeto: Any) -> dict:
        """
        Convierte un objeto en un diccionario serializable.

        El método obtiene los atributos del objeto utilizando `vars()`
        y construye un nuevo diccionario donde cada valor es procesado
        por `_convertir_valor` para asegurar que sea serializable.

        Args:
            objeto (Any): Instancia de una clase de dominio.

        Returns:
            dict: Diccionario con los atributos del objeto y valores
            convertidos a formatos serializables.
        """

        return {
            clave: Serializador._convertir_valor(valor)
            for clave, valor in vars(objeto).items()
        }


    @staticmethod
    def _convertir_valor(valor: Any) -> Any:
        """
        Convierte un valor a un formato serializable si es necesario.

        Este método maneja distintos tipos de datos que normalmente
        no pueden almacenarse o serializarse directamente, aplicando
        las conversiones correspondientes.

        Reglas de conversión:
        - date / datetime  -> cadena en formato ISO
        - UUID             -> cadena
        - bytes            -> None (se descarta el contenido binario)
        - list             -> se convierte recursivamente cada elemento
        - dict             -> se convierte recursivamente cada valor
        - float            -> redondeo a dos decimales
        - otros tipos      -> se retornan sin modificación

        Args:
            valor (Any): Valor a convertir.

        Returns:
            Any: Valor convertido a un tipo serializable o el mismo
            valor si no requiere transformación.
        """

        if isinstance(valor, (date, datetime)):
            return valor.isoformat()

        if isinstance(valor, uuid.UUID):
            return str(valor)

        if isinstance(valor, bytes):
            return None

        if isinstance(valor, list):
            return [
                Serializador._convertir_valor(item)
                for item in valor
            ]

        if isinstance(valor, dict):
            return {
                k: Serializador._convertir_valor(v)
                for k, v in valor.items()
            }

        if isinstance(valor, float):
            return round(valor, 2)

        return valor
    
#1
class Estudiante:
    def __init__(self,
        numero_matricula: str,
        nombres: str,
        apellidos: str,
        documento_identidad: str,
        fecha_nacimiento: date,
        direccion: str,
        correo_electronico: str,
        nombre_tutor: str,
        contacto_emergencia: str,
        fecha_ingreso: date,
        telefono: Optional[str] = None,
        fotografia: Optional[bytes] = None,
    ):
        self.numero_matricula     = numero_matricula
        self.nombres              = nombres
        self.apellidos            = apellidos
        self.documento_identidad  = documento_identidad
        self.fecha_nacimiento     = fecha_nacimiento
        self.direccion            = direccion
        self.correo_electronico   = correo_electronico
        self.nombre_tutor         = nombre_tutor
        self.contacto_emergencia  = contacto_emergencia
        self.fecha_ingreso        = fecha_ingreso
        self.telefono             = telefono
        self.fotografia           = fotografia
#2
class Profesor:
    def __init__(
        self,
        codigo_empleado: str,
        nombres: str,
        apellidos: str,
        documento_identidad: str,
        fecha_nacimiento: date,
        direccion: str,
        correo_institucional: str,
        nivel_formacion: str,
        especialidad: str,
        anios_experiencia: int,
        fecha_contratacion: date,
        tipo_contrato: str,
        departamento: str,
        telefono: Optional[str] = None,
    ):
        self.codigo_empleado      = codigo_empleado
        self.nombres              = nombres
        self.apellidos            = apellidos
        self.documento_identidad  = documento_identidad
        self.fecha_nacimiento     = fecha_nacimiento
        self.direccion            = direccion
        self.correo_institucional = correo_institucional
        self.nivel_formacion      = nivel_formacion
        self.especialidad         = especialidad
        self.anios_experiencia    = anios_experiencia
        self.fecha_contratacion   = fecha_contratacion
        self.tipo_contrato        = tipo_contrato
        self.departamento         = departamento
        self.telefono             = telefono
#3
    class Asignatura:
        def __init__(
            self,
            codigo_asignatura: str,
            nombre: str,
            area_conocimiento: str,
            horas_teoricas: int,
            horas_practicas: int,
            creditos_academicos: int,
            objetivos_generales: str,
            objetivos_especificos: str,
            requisitos_previos: Optional[str] = None,
            bibliografia: Optional[str] = None,
        ):
            self.codigo_asignatura    = codigo_asignatura
            self.nombre               = nombre
            self.area_conocimiento    = area_conocimiento
            self.horas_teoricas       = horas_teoricas
            self.horas_practicas      = horas_practicas
            self.creditos_academicos  = creditos_academicos
            self.objetivos_generales  = objetivos_generales
            self.objetivos_especificos = objetivos_especificos
            self.requisitos_previos   = requisitos_previos
            self.bibliografia         = bibliografia
#4
class Curso:
    def __init__(
        self,
        codigo_curso: str,
        periodo_academico: str,
        asignatura: str,
        profesor_asignado: str,
        aula: str,
        horario_dias: str,
        horario_horas: str,
        cupo_maximo: int,
        metodologia_evaluacion: str,
        lista_estudiantes: list[str] = None,
    ):
        self.codigo_curso           = codigo_curso
        self.periodo_academico      = periodo_academico
        self.asignatura             = asignatura
        self.profesor_asignado      = profesor_asignado
        self.aula                   = aula
        self.horario_dias           = horario_dias
        self.horario_horas          = horario_horas
        self.cupo_maximo            = cupo_maximo
        self.metodologia_evaluacion = metodologia_evaluacion
        self.lista_estudiantes      = lista_estudiantes if lista_estudiantes is not None else []
#5
class PeriodoAcademico:
    def __init__(
        self,
        codigo_periodo: str,
        descripcion: str,
        fecha_inicio: date,
        fecha_finalizacion: date,
        estado_actual: str,
        calendario_actividades: Optional[dict] = None,
    ):
        self.codigo_periodo         = codigo_periodo
        self.descripcion            = descripcion
        self.fecha_inicio           = fecha_inicio
        self.fecha_finalizacion     = fecha_finalizacion
        self.estado_actual          = estado_actual
        self.calendario_actividades = calendario_actividades
#6
class Calificacion:
    def __init__(
        self,
        estudiante: str,
        curso: str,
        tipo_evaluacion: str,
        fecha: date,
        valor_numerico: float,
        porcentaje: float,
        id_calificacion: int | uuid.UUID = None,
        observaciones: Optional[str] = None,
    ):
        self.id_calificacion = id_calificacion if id_calificacion is not None else uuid.uuid4()
        self.estudiante      = estudiante
        self.curso           = curso
        self.tipo_evaluacion = tipo_evaluacion
        self.fecha           = fecha
        self.valor_numerico  = valor_numerico
        self.porcentaje      = porcentaje
        self.observaciones   = observaciones
#7
class Aula:
    def __init__(
        self,
        id_aula: str,
        edificio: str,
        piso: int,
        capacidad: int,
        tipo: str,
        estado_actual: str,
        equipamiento: Optional[str] = None,
    ):
        self.id_aula       = id_aula
        self.edificio      = edificio
        self.piso          = piso
        self.capacidad     = capacidad
        self.tipo          = tipo
        self.estado_actual = estado_actual
        self.equipamiento  = equipamiento
#8
class PlanDeEstudios:
    def __init__(
        self,
        codigo_plan: str,
        carrera: str,
        fecha_aprobacion: date,
        asignaturas_por_nivel: dict[int, list[str]],
        creditos_totales: int,
        requisitos_graduacion: str,
    ):
        self.codigo_plan           = codigo_plan
        self.carrera               = carrera
        self.fecha_aprobacion      = fecha_aprobacion
        self.asignaturas_por_nivel = asignaturas_por_nivel
        self.creditos_totales      = creditos_totales
        self.requisitos_graduacion = requisitos_graduacion
#9
class MaterialBibliografico:
    def __init__(
        self,
        codigo_material: str,
        titulo: str,
        autores: str,
        categoria_tematica: str,
        formato: str,
        editorial: Optional[str] = None,
        anio_publicacion: Optional[int] = None,
        edicion: Optional[str] = None,
        isbn: Optional[str] = None,
        ubicacion_fisica: Optional[str] = None,
        cantidad_ejemplares: Optional[int] = None,
    ):
        self.codigo_material     = codigo_material
        self.titulo              = titulo
        self.autores             = autores
        self.categoria_tematica  = categoria_tematica
        self.formato             = formato
        self.editorial           = editorial
        self.anio_publicacion    = anio_publicacion
        self.edicion             = edicion
        self.isbn                = isbn
        self.ubicacion_fisica    = ubicacion_fisica
        self.cantidad_ejemplares = cantidad_ejemplares
#10
class Prestamo:
    def __init__(
        self,
        codigo_prestamo: str,
        fecha_prestamo: date,
        fecha_devolucion_prog: date,
        material_prestado: str,
        solicitante: str,
        estado: str,
        multa_aplicada: Optional[float] = None,
    ):
        self.codigo_prestamo      = codigo_prestamo
        self.fecha_prestamo       = fecha_prestamo
        self.fecha_devolucion_prog = fecha_devolucion_prog
        self.material_prestado    = material_prestado
        self.solicitante          = solicitante
        self.estado               = estado
        self.multa_aplicada       = multa_aplicada
#11
class ActividadExtracurricular:
    def __init__(
        self,
        codigo_actividad: str,
        nombre: str,
        tipo: str,
        profesor_responsable: str,
        horario: str,
        lugar: str,
        cupo: int,
        descripcion: Optional[str] = None,
        lista_participantes: list[str] = None,
    ):
        self.codigo_actividad      = codigo_actividad
        self.nombre                = nombre
        self.tipo                  = tipo
        self.profesor_responsable  = profesor_responsable
        self.horario               = horario
        self.lugar                 = lugar
        self.cupo                  = cupo
        self.descripcion           = descripcion
        self.lista_participantes   = lista_participantes if lista_participantes is not None else []