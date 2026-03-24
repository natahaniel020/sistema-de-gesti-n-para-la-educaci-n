from datetime import date, datetime
from typing import Optional, Any
import uuid
        
    #1
# Clase que representa la entidad Estudiante en el dominio
class Estudiante():
        def __init__(self,
            numero_matricula: str,      # Identificador único del estudiante
            nombres: str,               # Nombres
            apellidos: str,             # Apellidos
            documento_identidad: str,   # Documento de identidad
            fecha_nacimiento: date,     # Fecha de nacimiento (tipo date)
            direccion: str,             # Dirección de residencia
            correo_electronico: str,    # Correo personal
            nombre_tutor: str,          # Nombre del tutor legal
            contacto_emergencia: str,   # Contacto de emergencia
            fecha_ingreso: date,        # Fecha de ingreso a la institución
            telefono: Optional[str] = None,  # Teléfono (opcional)
            fotografia: Optional[bytes] = None, # Fotografía en binario (opcional)
        ):
            # Asignación de atributos
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
# Clase que representa la entidad Profesor
class Profesor():
        def __init__(
            self,
            codigo_empleado: str,       # ID del profesor
            nombres: str,
            apellidos: str,
            documento_identidad: str,
            fecha_nacimiento: date,
            direccion: str,
            correo_institucional: str,  # Correo institucional
            nivel_formacion: str,       # Nivel académico
            especialidad: str,          # Área de especialización
            anios_experiencia: int,     # Años de experiencia (entero)
            fecha_contratacion: date,   # Fecha de contratación
            tipo_contrato: str,         # Tipo de contrato
            departamento: str,          # Departamento académico
            telefono: Optional[str] = None, # Teléfono opcional
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
# Clase que representa la entidad Asignatura
class Asignatura():
            def __init__(
                self,
                codigo_asignatura: str,   # ID de la asignatura
                nombre: str,              # Nombre
                area_conocimiento: str,   # Área (ej: matemáticas, ciencias)
                horas_teoricas: int,      # Horas teóricas
                horas_practicas: int,     # Horas prácticas
                creditos_academicos: int,# Créditos
                objetivos_generales: str,# Objetivos generales
                objetivos_especificos: str,# Objetivos específicos
                requisitos_previos: Optional[str] = None, # Opcional
                bibliografia: Optional[str] = None,       # Opcional
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
# Clase que representa la entidad Curso
class Curso():
        def __init__(
            self,
            codigo_curso: str,            # ID del curso
            periodo_academico: str,       # Periodo (ej: 2025-1)
            asignatura: str,              # Código o nombre de asignatura
            profesor_asignado: str,       # Profesor asignado
            aula: str,                   # Aula
            horario_dias: str,           # Días (ej: L-M-V)
            horario_horas: str,          # Horario (ej: 8-10)
            cupo_maximo: int,            # Máximo de estudiantes
            metodologia_evaluacion: str, # Forma de evaluación
            lista_estudiantes: list[str] = None, # Lista de IDs de estudiantes
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
            # Si no se pasa lista, se inicializa vacía (evita problemas de mutabilidad)
            self.lista_estudiantes      = lista_estudiantes if lista_estudiantes is not None else []

#-----------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------
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