"""
--- MÓDULO 2 Controlador --- Coordinador Central
- Responsabilidad
Coordinar el flujo completo entre todos los módulos. No crea objetos ni accede a datos directamente.

Flujo por operación
- Recibe dict del Módulo 4
- Llama Módulo 3 → obtiene objeto puro
- Llama Serializador → obtiene dict
- Almacena en estructura de datos
- Retorna confirmación al Módulo 4
"""

from dominio import Serializador
from fabrica import Fabrica


class Controlador:

    datos = {
        'estudiantes'   : {},
        'profesores'    : {},
        'asignaturas'   : {},
        'cursos'        : {},
        'periodos'      : {},
        'calificaciones': {},
        'aulas'         : {},
        'planes'        : {},
        'materiales'    : {},
        'prestamos'     : {},
        'actividades'   : {},
    }

    def registrar(self, datos: dict) -> dict:
        objeto      = Fabrica.crear(datos)
        diccionario = Serializador.convertir(objeto)
        self._almacenar(diccionario)
        return diccionario

    def _almacenar(self, diccionario: dict):
        tabla, clave = self._resolver_destino(diccionario)
        Controlador.datos[tabla][clave] = diccionario

    def _resolver_destino(self, diccionario: dict) -> tuple[str, str]:
        if 'numero_matricula'  in diccionario: return 'estudiantes',    diccionario['numero_matricula']
        if 'codigo_empleado'   in diccionario: return 'profesores',     diccionario['codigo_empleado']
        if 'codigo_asignatura' in diccionario: return 'asignaturas',    diccionario['codigo_asignatura']
        if 'codigo_curso'      in diccionario: return 'cursos',         diccionario['codigo_curso']
        if 'codigo_periodo'    in diccionario: return 'periodos',       diccionario['codigo_periodo']
        if 'id_calificacion'   in diccionario: return 'calificaciones', diccionario['id_calificacion']
        if 'id_aula'           in diccionario: return 'aulas',          diccionario['id_aula']
        if 'codigo_plan'       in diccionario: return 'planes',         diccionario['codigo_plan']
        if 'codigo_material'   in diccionario: return 'materiales',     diccionario['codigo_material']
        if 'codigo_prestamo'   in diccionario: return 'prestamos',      diccionario['codigo_prestamo']
        if 'codigo_actividad'  in diccionario: return 'actividades',    diccionario['codigo_actividad']
        raise ValueError("El diccionario no corresponde a ninguna entidad conocida.")