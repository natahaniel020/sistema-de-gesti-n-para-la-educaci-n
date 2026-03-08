"""
----Fábrica de Objetos Responsabilidad----

Recibir datos crudos, validar todas las invariantes del diccionario de datos y retornar objetos correctamente construidos.

Acciones
- Convierte tipos (str → date, etc.)
- Valida campos obligatorios
- Verifica valores permitidos
- Lanza excepción si hay violación
- Retorna instancia del objeto puro
"""
from datetime import date
from typing import Optional
from dominio import (
    Estudiante, Profesor, Asignatura, Curso,
    PeriodoAcademico, Calificacion, Aula,
    PlanDeEstudios, MaterialBibliografico,
    Prestamo, ActividadExtracurricular
)


class Fabrica:

    def crear(self, datos: dict):
        if 'numero_matricula'  in datos: return self._crear_estudiante(datos)
        if 'codigo_empleado'   in datos: return self._crear_profesor(datos)
        if 'codigo_asignatura' in datos: return self._crear_asignatura(datos)
        if 'codigo_curso'      in datos: return self._crear_curso(datos)
        if 'codigo_periodo'    in datos: return self._crear_periodo(datos)
        if 'id_calificacion'   in datos: return self._crear_calificacion(datos)
        if 'id_aula'           in datos: return self._crear_aula(datos)
        if 'codigo_plan'       in datos: return self._crear_plan(datos)
        if 'codigo_material'   in datos: return self._crear_material(datos)
        if 'codigo_prestamo'   in datos: return self._crear_prestamo(datos)
        if 'codigo_actividad'  in datos: return self._crear_actividad(datos)
        raise ValueError("El diccionario no corresponde a ninguna entidad conocida.")

    def _crear_estudiante(self, datos: dict) -> Estudiante:
        return Estudiante(
            numero_matricula    = datos['numero_matricula'],
            nombres             = datos['nombres'],
            apellidos           = datos['apellidos'],
            documento_identidad = datos['documento_identidad'],
            fecha_nacimiento    = date.fromisoformat(datos['fecha_nacimiento']),
            direccion           = datos['direccion'],
            correo_electronico  = datos['correo_electronico'],
            nombre_tutor        = datos['nombre_tutor'],
            contacto_emergencia = datos['contacto_emergencia'],
            fecha_ingreso       = date.fromisoformat(datos['fecha_ingreso']),
            telefono            = datos.get('telefono'),
            fotografia          = datos.get('fotografia'),
        )

    def _crear_profesor(self, datos: dict) -> Profesor:
        return Profesor(
            codigo_empleado      = datos['codigo_empleado'],
            nombres              = datos['nombres'],
            apellidos            = datos['apellidos'],
            documento_identidad  = datos['documento_identidad'],
            fecha_nacimiento     = date.fromisoformat(datos['fecha_nacimiento']),
            direccion            = datos['direccion'],
            correo_institucional = datos['correo_institucional'],
            nivel_formacion      = datos['nivel_formacion'],
            especialidad         = datos['especialidad'],
            anios_experiencia    = int(datos['anios_experiencia']),
            fecha_contratacion   = date.fromisoformat(datos['fecha_contratacion']),
            tipo_contrato        = datos['tipo_contrato'],
            departamento         = datos['departamento'],
            telefono             = datos.get('telefono'),
        )

    def _crear_asignatura(self, datos: dict) -> Asignatura:
        return Asignatura(
            codigo_asignatura     = datos['codigo_asignatura'],
            nombre                = datos['nombre'],
            area_conocimiento     = datos['area_conocimiento'],
            horas_teoricas        = int(datos['horas_teoricas']),
            horas_practicas       = int(datos['horas_practicas']),
            creditos_academicos   = int(datos['creditos_academicos']),
            objetivos_generales   = datos['objetivos_generales'],
            objetivos_especificos = datos['objetivos_especificos'],
            requisitos_previos    = datos.get('requisitos_previos'),
            bibliografia          = datos.get('bibliografia'),
        )

    def _crear_curso(self, datos: dict) -> Curso:
        return Curso(
            codigo_curso            = datos['codigo_curso'],
            periodo_academico       = datos['periodo_academico'],
            asignatura              = datos['asignatura'],
            profesor_asignado       = datos['profesor_asignado'],
            aula                    = datos['aula'],
            horario_dias            = datos['horario_dias'],
            horario_horas           = datos['horario_horas'],
            cupo_maximo             = int(datos['cupo_maximo']),
            metodologia_evaluacion  = datos['metodologia_evaluacion'],
            lista_estudiantes       = datos.get('lista_estudiantes', []),
        )

    def _crear_periodo(self, datos: dict) -> PeriodoAcademico:
        return PeriodoAcademico(
            codigo_periodo         = datos['codigo_periodo'],
            descripcion            = datos['descripcion'],
            fecha_inicio           = date.fromisoformat(datos['fecha_inicio']),
            fecha_finalizacion     = date.fromisoformat(datos['fecha_finalizacion']),
            estado_actual          = datos['estado_actual'],
            calendario_actividades = datos.get('calendario_actividades'),
        )

    def _crear_calificacion(self, datos: dict) -> Calificacion:
        return Calificacion(
            estudiante      = datos['estudiante'],
            curso           = datos['curso'],
            tipo_evaluacion = datos['tipo_evaluacion'],
            fecha           = date.fromisoformat(datos['fecha']),
            valor_numerico  = float(datos['valor_numerico']),
            porcentaje      = float(datos['porcentaje']),
            observaciones   = datos.get('observaciones'),
        )

    def _crear_aula(self, datos: dict) -> Aula:
        return Aula(
            id_aula       = datos['id_aula'],
            edificio      = datos['edificio'],
            piso          = int(datos['piso']),
            capacidad     = int(datos['capacidad']),
            tipo          = datos['tipo'],
            estado_actual = datos['estado_actual'],
            equipamiento  = datos.get('equipamiento'),
        )

    def _crear_plan(self, datos: dict) -> PlanDeEstudios:
        return PlanDeEstudios(
            codigo_plan            = datos['codigo_plan'],
            carrera                = datos['carrera'],
            fecha_aprobacion       = date.fromisoformat(datos['fecha_aprobacion']),
            asignaturas_por_nivel  = datos['asignaturas_por_nivel'],
            creditos_totales       = int(datos['creditos_totales']),
            requisitos_graduacion  = datos['requisitos_graduacion'],
        )

    def _crear_material(self, datos: dict) -> MaterialBibliografico:
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

    def _crear_prestamo(self, datos: dict) -> Prestamo:
        return Prestamo(
            codigo_prestamo       = datos['codigo_prestamo'],
            fecha_prestamo        = date.fromisoformat(datos['fecha_prestamo']),
            fecha_devolucion_prog = date.fromisoformat(datos['fecha_devolucion_prog']),
            material_prestado     = datos['material_prestado'],
            solicitante           = datos['solicitante'],
            estado                = datos['estado'],
            multa_aplicada        = float(datos['multa_aplicada']) if datos.get('multa_aplicada') else None,
        )

    def _crear_actividad(self, datos: dict) -> ActividadExtracurricular:
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