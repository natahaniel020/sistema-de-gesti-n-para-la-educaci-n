from datetime import date
from typing import Optional
from dominio import Estudiante, Profesor, Asignatura, Curso


class Fabrica:
   
    # Convierte un objeto de dominio a una tupla usando sus atributos.
    # Se usa para enviar datos a la capa de persistencia (por ejemplo, procedimientos almacenados).
    @staticmethod
    def a_tupla(obj) -> tuple:
        return tuple(vars(obj).values())
    
    # Convierte un string en formato ISO (yyyy-mm-dd) a un objeto date.
    # Lanza error si el valor está vacío o es inválido.
    @staticmethod
    def _parse_fecha(valor):
        if not valor or valor.strip() == "":
            raise ValueError("Fecha obligatoria")
        return date.fromisoformat(valor)
    
    # Método principal de la fábrica.
    # Determina qué tipo de objeto crear según las claves del diccionario.
    @staticmethod
    def crear(datos: dict):

        # Selección del tipo de entidad según presencia de claves
        if 'numero_matricula'  in datos: return Fabrica._crear_estudiante(datos)
        if 'codigo_empleado'   in datos: return Fabrica._crear_profesor(datos)
        if 'codigo_asignatura' in datos: return Fabrica._crear_asignatura(datos)
        if 'codigo_curso'      in datos: return Fabrica._crear_curso(datos)
        if 'codigo_periodo'    in datos: return Fabrica._crear_periodo(datos)
        if 'id_calificacion'   in datos: return Fabrica._crear_calificacion(datos)
        if 'id_aula'           in datos: return Fabrica._crear_aula(datos)
        if 'codigo_plan'       in datos: return Fabrica._crear_plan(datos)
        if 'codigo_material'   in datos: return Fabrica._crear_material(datos)
        if 'codigo_prestamo'   in datos: return Fabrica._crear_prestamo(datos)
        if 'codigo_actividad'  in datos: return Fabrica._crear_actividad(datos)

        # Si no coincide con ninguna entidad conocida
        raise ValueError("El diccionario no corresponde a ninguna entidad conocida.")

#---------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------
    """
        Crea un objeto Estudiante a partir de un diccionario.

        Convierte campos necesarios como fechas y asigna valores
        opcionales cuando están presentes.

        Args:
            datos (dict): Información del estudiante.

        Returns:
            Estudiante: Instancia del modelo de dominio Estudiante.
    """
    @staticmethod
    def _crear_estudiante(datos: dict) -> Estudiante:
        return Estudiante(
            numero_matricula    = datos['numero_matricula'],   # ID principal
            nombres             = datos['nombres'],            # Nombres del estudiante
            apellidos           = datos['apellidos'],          # Apellidos
            documento_identidad = datos['documento_identidad'],# Documento
            fecha_nacimiento    = Fabrica._parse_fecha(datos.get('fecha_nacimiento')), # Conversión a date
            direccion           = datos['direccion'],          # Dirección
            correo_electronico  = datos['correo_electronico'], # Email
            nombre_tutor        = datos['nombre_tutor'],       # Tutor legal
            contacto_emergencia = datos['contacto_emergencia'],# Contacto de emergencia
            fecha_ingreso       = Fabrica._parse_fecha(datos.get('fecha_ingreso')), # Fecha de ingreso
            telefono            = datos.get('telefono'),       # Campo opcional
            fotografia          = datos.get('fotografia'),     # Binario opcional
        )

    # Crea un objeto Profesor
    @staticmethod
    def _crear_profesor(datos: dict) -> Profesor:
        return Profesor(
            codigo_empleado      = datos['codigo_empleado'],   # ID del profesor
            nombres              = datos['nombres'],
            apellidos            = datos['apellidos'],
            documento_identidad  = datos['documento_identidad'],
            fecha_nacimiento     = Fabrica._parse_fecha(datos.get('fecha_nacimiento')),
            direccion            = datos['direccion'],
            correo_institucional = datos['correo_institucional'],
            nivel_formacion      = datos['nivel_formacion'],
            especialidad         = datos['especialidad'],
            anios_experiencia    = int(datos['anios_experiencia']), # Conversión a entero
            fecha_contratacion   = date.fromisoformat(datos['fecha_contratacion']), # Conversión directa
            tipo_contrato        = datos['tipo_contrato'],
            departamento         = datos['departamento'],
            telefono             = datos.get('telefono'),
        )

    # Crea un objeto Asignatura
    @staticmethod
    def _crear_asignatura(datos: dict) -> Asignatura:
        return Asignatura(
            codigo_asignatura     = datos['codigo_asignatura'],  # ID
            nombre                = datos['nombre'],
            area_conocimiento     = datos['area_conocimiento'],
            horas_teoricas        = int(datos['horas_teoricas']),  # Conversión a entero
            horas_practicas       = int(datos['horas_practicas']),
            creditos_academicos   = int(datos['creditos_academicos']),
            objetivos_generales   = datos['objetivos_generales'],
            objetivos_especificos = datos['objetivos_especificos'],
            requisitos_previos    = datos.get('requisitos_previos'), # Opcional
            bibliografia          = datos.get('bibliografia'),
        )

    # Crea un objeto Curso
    @staticmethod
    def _crear_curso(datos: dict) -> Curso:
        return Curso(
            codigo_curso            = datos['codigo_curso'],   # ID
            periodo_academico       = datos['periodo_academico'],
            asignatura              = datos['asignatura'],
            profesor_asignado       = datos['profesor_asignado'],
            aula                    = datos['aula'],
            horario_dias            = datos['horario_dias'],
            horario_horas           = datos['horario_horas'],
            cupo_maximo             = int(datos['cupo_maximo']), # Conversión a entero
            metodologia_evaluacion  = datos['metodologia_evaluacion'],
            lista_estudiantes       = datos.get('lista_estudiantes', []), # Lista por defecto
        )
    
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------

    @staticmethod
    def _crear_periodo(datos: dict) -> PeriodoAcademico:
        """
        Construye un objeto PeriodoAcademico.

        Args:
            datos (dict): Información del periodo académico.

        Returns:
            PeriodoAcademico: Instancia del periodo.
        """
        return PeriodoAcademico(
            codigo_periodo         = datos['codigo_periodo'],
            descripcion            = datos['descripcion'],
            fecha_inicio           = date.fromisoformat(datos['fecha_inicio']),
            fecha_finalizacion     = date.fromisoformat(datos['fecha_finalizacion']),
            estado_actual          = datos['estado_actual'],
            calendario_actividades = datos.get('calendario_actividades'),
        )

    @staticmethod
    def _crear_calificacion(datos: dict) -> Calificacion:
        """
        Genera una instancia de Calificacion que representa
        una evaluación realizada a un estudiante.

        Args:
            datos (dict): Datos de la calificación.

        Returns:
            Calificacion: Objeto calificación.
        """
        return Calificacion(
            estudiante      = datos['estudiante'],
            curso           = datos['curso'],
            tipo_evaluacion = datos['tipo_evaluacion'],
            fecha           = date.fromisoformat(datos['fecha']),
            valor_numerico  = float(datos['valor_numerico']),
            porcentaje      = float(datos['porcentaje']),
            observaciones   = datos.get('observaciones'),
        )

    @staticmethod
    def _crear_aula(datos: dict) -> Aula:
        """
        Construye un objeto Aula que representa un espacio físico
        dentro de la institución.

        Args:
            datos (dict): Información del aula.

        Returns:
            Aula: Instancia del aula.
        """
        return Aula(
            id_aula       = datos['id_aula'],
            edificio      = datos['edificio'],
            piso          = int(datos['piso']),
            capacidad     = int(datos['capacidad']),
            tipo          = datos['tipo'],
            estado_actual = datos['estado_actual'],
            equipamiento  = datos.get('equipamiento'),
        )

    @staticmethod
    def _crear_plan(datos: dict) -> PlanDeEstudios:
        """
        Crea un objeto PlanDeEstudios que describe la estructura
        curricular de una carrera.

        Args:
            datos (dict): Información del plan.

        Returns:
            PlanDeEstudios: Instancia del plan académico.
        """
        return PlanDeEstudios(
            codigo_plan            = datos['codigo_plan'],
            carrera                = datos['carrera'],
            fecha_aprobacion       = date.fromisoformat(datos['fecha_aprobacion']),
            asignaturas_por_nivel  = datos['asignaturas_por_nivel'],
            creditos_totales       = int(datos['creditos_totales']),
            requisitos_graduacion  = datos['requisitos_graduacion'],
        )

    @staticmethod
    def _crear_material(datos: dict) -> MaterialBibliografico:
        """
        Genera una instancia de MaterialBibliografico que representa
        un recurso disponible en biblioteca.

        Args:
            datos (dict): Información del material.

        Returns:
            MaterialBibliografico: Objeto del catálogo bibliográfico.
        """
        return MaterialBibliografico(
            codigo_material      = datos['codigo_material'],
            titulo               = datos['titulo'],
            autores              = datos['autores'],
            categoria_tematica   = datos['categoria_tematica'],
            formato              = datos['formato'],
            editorial            = datos.get('editorial'),
            anio_publicacion     = int(datos['anio_publicacion']) if datos.get('anio_publicacion') else None,
            edicion              = datos.get('edicion'),
            isbn                 = datos.get('isbn'),
            ubicacion_fisica     = datos.get('ubicacion_fisica'),
            cantidad_ejemplares  = int(datos['cantidad_ejemplares']) if datos.get('cantidad_ejemplares') else None,
        )

    @staticmethod
    def _crear_prestamo(datos: dict) -> Prestamo:
        """
        Crea un objeto Prestamo que representa el registro de
        préstamo de un material bibliográfico.

        Args:
            datos (dict): Información del préstamo.

        Returns:
            Prestamo: Instancia del préstamo registrado.
        """
        return Prestamo(
            codigo_prestamo       = datos['codigo_prestamo'],
            fecha_prestamo        = date.fromisoformat(datos['fecha_prestamo']),
            fecha_devolucion_prog = date.fromisoformat(datos['fecha_devolucion_prog']),
            material_prestado     = datos['material_prestado'],
            solicitante           = datos['solicitante'],
            estado                = datos['estado'],
            multa_aplicada        = float(datos['multa_aplicada']) if datos.get('multa_aplicada') else None,
        )

    @staticmethod
    def _crear_actividad(datos: dict) -> ActividadExtracurricular:
        """
        Genera una instancia de ActividadExtracurricular que representa
        una actividad institucional fuera del currículo académico.

        Args:
            datos (dict): Información de la actividad.

        Returns:
            ActividadExtracurricular: Objeto actividad.
        """
        return ActividadExtracurricular(
            codigo_actividad     = datos['codigo_actividad'],
            nombre               = datos['nombre'],
            tipo                 = datos['tipo'],
            profesor_responsable = datos['profesor_responsable'],
            horario              = datos['horario'],
            lugar                = datos['lugar'],
            cupo                 = int(datos['cupo']),
            descripcion          = datos.get('descripcion'),
            lista_participantes  = datos.get('lista_participantes', []),
        )