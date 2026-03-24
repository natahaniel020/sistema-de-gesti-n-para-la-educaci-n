import pymysql
from abc import ABC, abstractmethod
import traceback 


# Clase base abstracta para todos los repositorios
class BaseRepositorio(ABC):

    def __init__(self):
        self._conexion = None   # Conexión a la base de datos
        self._cursor   = None   # Cursor para ejecutar consultas

    # Propiedad para manejar la conexión (lazy loading)
    @property
    def conexion(self):
        # Si no existe conexión o está cerrada, se crea una nueva
        if self._conexion is None or not self._conexion.open:
            self._conexion = pymysql.connect(
                host     = "localhost",
                user     = "root",
                password = "24284240",
                database = "gestion_academica"
            )
            self._cursor = self._conexion.cursor()
        return self._conexion

    # Propiedad para obtener el cursor activo
    @property
    def cursor(self):
        _ = self.conexion   # Garantiza que la conexión esté activa
        return self._cursor

    # Método genérico para ejecutar procedimientos almacenados
    def ejecutar_sp(self, nombre_sp, params=None, fetch=False):
        try:
            print(">>> SP:", nombre_sp)     # Log del procedimiento
            print(">>> PARAMS:", params)    # Log de parámetros

            # Ejecutar procedimiento almacenado
            self.cursor.callproc(nombre_sp, params or [])

            # Si se esperan resultados
            if fetch:
                resultados = []
                while True:
                    rows = self.cursor.fetchall()  # Obtener filas
                    if rows:
                        resultados.extend(rows)
                    # Verificar si hay más conjuntos de resultados
                    if not self.cursor.nextset():
                        break
                print(">>> RESULTADOS:", resultados)
                return resultados
            else:
                # Confirmar cambios en la BD
                self.conexion.commit()
                print(">>> COMMIT OK")

        except Exception as e:
            # Revertir cambios en caso de error
            self.conexion.rollback()
            print(">>> ERROR SQL:", e)
            raise e  # Relanzar excepción

    # Métodos abstractos que deben implementar los repositorios concretos
    @abstractmethod
    def insertar(self, obj): pass

    @abstractmethod
    def obtener(self): pass

    @abstractmethod
    def actualizar(self, obj): pass

    @abstractmethod
    def eliminar_por_id(self, id): pass


# Repositorio de Estudiante
class EstudianteRepositorio(BaseRepositorio):

    def insertar(self, est):
        self.ejecutar_sp("sp_estudiante_insertar", est)

    def obtener(self):
        return self.ejecutar_sp("sp_estudiante_obtener_todos",   fetch=True)

    def actualizar(self, est):
        self.ejecutar_sp("sp_estudiante_actualizar", est)

    def eliminar_por_id(self, id):
        self.ejecutar_sp("sp_estudiante_eliminar",(id,))


# Repositorio de Profesor
class ProfesorRepositorio(BaseRepositorio):

    def insertar(self, prf):
        self.ejecutar_sp("sp_profesor_insertar", prf)

    def obtener(self): 
        return self.ejecutar_sp("sp_profesor_obtener_todos",   fetch=True)

    def actualizar(self, prf):
        self.ejecutar_sp("sp_profesor_actualizar", prf)
    
    # Nota: este método no sigue la misma firma que la clase base
    def eliminar(self, prf):
        self.ejecutar_sp("sp_profesor_eliminar", (prf.codigo_empleado,))


# Repositorio de Asignatura
class AsignaturaRepositorio(BaseRepositorio):

    def insertar(self, asg):
        self.ejecutar_sp("sp_asignatura_insertar", asg)

    def obtener(self):
        return self.ejecutar_sp("sp_asignatura_obtener_todos",   fetch=True)

    def actualizar(self, asg):
        self.ejecutar_sp("sp_asignatura_actualizar", asg)

    # Recibe objeto completo pero usa solo su ID
    def eliminar_por_id(self, asg):
        self.ejecutar_sp("sp_asignatura_eliminar", (asg.codigo_asignatura,))


# Repositorio de Curso
class CursoRepositorio(BaseRepositorio):

    def insertar(self, crs):
        self.ejecutar_sp("sp_curso_insertar", crs)

    def obtener(self):
        return self.ejecutar_sp("sp_curso_obtener_todos",   fetch=True)
    
    def actualizar(self, crs):
        self.ejecutar_sp("sp_curso_actualizar", crs)

    # Igual que arriba: recibe objeto pero usa solo el ID
    def eliminar_por_id(self, crs):
        self.ejecutar_sp("sp_curso_eliminar", (crs.codigo_curso,))  # ✅ sin S