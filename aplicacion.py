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
    """
    Controlador central del sistema.

    Su responsabilidad es recibir datos de entrada, crear el objeto de dominio
    correspondiente mediante la fábrica, serializarlo a diccionario y almacenarlo
    en la estructura de datos interna según el tipo de entidad.
    """

    # Almacén en memoria organizado por tipo de entidad
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
        """
        Registra una nueva entidad en el sistema.

        Proceso:
        1. Utiliza la fábrica para crear el objeto de dominio a partir del diccionario recibido.
        2. Convierte el objeto a un diccionario mediante el serializador.
        3. Almacena el diccionario en la estructura interna correspondiente.

        Args:
            datos (dict): Diccionario con los datos necesarios para crear la entidad.

        Returns:
            dict: Diccionario serializado del objeto creado.
        """

        objeto = Fabrica.crear(datos)
        diccionario = Serializador.convertir(objeto)
        self._almacenar(diccionario)
        return diccionario


    def _almacenar(self, diccionario: dict):
        """
        Guarda el diccionario de una entidad en el almacén correspondiente.

        Determina la tabla y la clave mediante el método `_resolver_destino`
        y luego almacena el registro dentro del diccionario global `datos`.

        Args:
            diccionario (dict): Representación serializada del objeto.
        """

        tabla, clave = self._resolver_destino(diccionario)
        Controlador.datos[tabla][clave] = diccionario


    def _resolver_destino(self, diccionario: dict) -> tuple[str, str]:
        """
        Determina en qué colección del sistema debe almacenarse el diccionario
        y cuál será su clave primaria.

        La decisión se toma analizando qué identificador contiene el diccionario.

        Args:
            diccionario (dict): Diccionario de la entidad serializada.

        Returns:
            tuple[str, str]:
                - nombre de la tabla donde se almacenará
                - clave única del registro

        Raises:
            ValueError: Si el diccionario no corresponde a ninguna entidad conocida.
        """

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