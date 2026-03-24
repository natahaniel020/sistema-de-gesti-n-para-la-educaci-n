from fabrica import Fabrica
from persistencia import EstudianteRepositorio, ProfesorRepositorio, AsignaturaRepositorio, CursoRepositorio
from dominio import Estudiante, Profesor, Asignatura, Curso

class Controlador:

    # Diccionario que relaciona cada entidad del dominio con su repositorio correspondiente
    REPOSITORIOS = {
        Estudiante : EstudianteRepositorio,
        Profesor   : ProfesorRepositorio,
        Asignatura : AsignaturaRepositorio,
        Curso      : CursoRepositorio,
    }

    # Método interno para obtener el repositorio correcto según la entidad
    def _obtener_repositorio(self, entidad):
        
        # Si la entidad viene como string (desde la interfaz)
        if isinstance(entidad, str):
            # Se convierte el nombre en la clase correspondiente
            clave = {"estudiante": Estudiante, "profesor": Profesor,
                        "asignatura": Asignatura, "curso": Curso}.get(entidad.lower())
        else:
            # Si ya es un objeto, se obtiene su tipo (clase)
            clave = type(entidad)

        # Buscar el repositorio correspondiente en el diccionario
        clase = self.REPOSITORIOS.get(clave)

        # Validación: si no existe repositorio para esa entidad
        if not clase:
            raise ValueError(f"Entidad desconocida: {entidad}")
        
        # Retorna una instancia del repositorio
        return clase()


    # Método para guardar un registro
    def Guardar(self, datos: dict):
        # Crear objeto del dominio a partir de los datos
        obj_dominio = Fabrica.crear(datos)

        # Convertir objeto a tupla (formato para persistencia)
        tupla = Fabrica.a_tupla(obj_dominio)

        # Insertar en el repositorio correspondiente
        self._obtener_repositorio(obj_dominio).insertar(tupla)


    # Método para obtener todos los registros de una entidad
    def Obtener(self, nombre_entidad: str):
        # Obtener repositorio según el nombre
        repo = self._obtener_repositorio(nombre_entidad)

        # Obtener todos los registros
        resultados = repo.obtener()

        # Si no hay datos
        if not resultados:
            return "Sin registros encontrados."
        
        # Convertir resultados a string para mostrarlos
        return "\n".join(str(fila) for fila in resultados)


    # Método para actualizar un registro
    def Actualizar(self, datos: dict):
        # Crear objeto del dominio
        obj_dominio = Fabrica.crear(datos)

        # Convertir a tupla
        tupla = Fabrica.a_tupla(obj_dominio)

        # Ejecutar actualización en el repositorio correspondiente
        self._obtener_repositorio(obj_dominio).actualizar(tupla)


    # Método para eliminar un registro
    def Eliminar(self, datos: dict, nombre_entidad: str):
        # Diccionario que define el campo ID de cada entidad
        claves = {
            "estudiante": "numero_matricula",
            "profesor"  : "codigo_empleado",
            "asignatura": "codigo_asignatura",
            "curso"     : "codigo_curso"
        }

        # Obtener el nombre del campo ID según la entidad
        campo_id = claves.get(nombre_entidad.lower())

        # Obtener el valor del ID desde los datos ingresados
        id_valor = datos.get(campo_id)
    
        # Validación: si no se proporcionó el ID
        if not id_valor:
            raise ValueError(f"Debe ingresar el {campo_id} para eliminar.")
    
        # Llamar al método de eliminación del repositorio
        self._obtener_repositorio(nombre_entidad).eliminar_por_id(id_valor)