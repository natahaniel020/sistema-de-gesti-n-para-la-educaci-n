📚 Sistema de Gestión Académica
📌 Descripción

Este proyecto consiste en el desarrollo de un sistema de gestión académica implementado en Python, que permite administrar información relacionada con:

Estudiantes
Profesores
Asignaturas
Cursos

El sistema incluye una interfaz gráfica construida con Tkinter y está organizado siguiendo una arquitectura por capas, separando claramente la lógica de presentación, negocio y persistencia.

🏗️ Arquitectura del Sistema

El sistema está diseñado bajo un enfoque modular dividido en las siguientes capas:

1. Interfaz (UI)
Implementada con Tkinter
Uso de pestañas (Notebook) para cada entidad
Formularios dinámicos generados automáticamente
Soporte para:
Fechas (DateEntry)
Carga de imágenes
Campos opcionales y obligatorios
Operaciones CRUD disponibles:
Guardar
Obtener
Actualizar
Eliminar

2. Controlador
Actúa como intermediario entre la interfaz y la lógica del sistema
Recibe los datos del usuario
Coordina la creación de objetos y su almacenamiento
Selecciona dinámicamente el repositorio adecuado según la entidad

3. Fábrica (Factory Pattern)
Responsable de crear objetos del dominio a partir de diccionarios
Convierte tipos de datos (ej: fechas, enteros)
Determina automáticamente el tipo de entidad
Serializa objetos a tuplas para la persistencia

4. Dominio
Define las entidades principales del sistema:

Estudiante
Profesor
Asignatura
Curso

Estas clases representan la estructura de los datos y contienen los atributos necesarios para cada entidad.

5. Persistencia
Implementada con MySQL y pymysql
Uso de una clase base (BaseRepositorio) para manejar:
Conexión
Cursor
Ejecución de procedimientos almacenados
Repositorios específicos por entidad:
EstudianteRepositorio
ProfesorRepositorio
AsignaturaRepositorio
CursoRepositorio

Las operaciones se realizan mediante Stored Procedures (SP).

🔄 Flujo del Sistema
El usuario ingresa datos en la interfaz gráfica
El controlador recibe los datos
La fábrica crea un objeto del dominio
El objeto se convierte en tupla
El repositorio ejecuta un procedimiento almacenado
La base de datos procesa la operación
El resultado se muestra en la interfaz
🛠️ Tecnologías Utilizadas
Python 3
Tkinter
tkcalendar
MySQL
pymysql
📂 Estructura del Proyecto
/proyecto
│
├── interfaz.py
├── aplicacion.py (Controlador)
├── fabrica.py
├── dominio.py
├── persistencia.py
└── base de datos (MySQL)
⚙️ Requisitos
Python 3.x
MySQL Server

Librerías:

pip install pymysql tkcalendar
▶️ Ejecución
Configurar la base de datos en MySQL

Verificar credenciales en BaseRepositorio:

host="localhost"
user="root"
password="****"
database="gestion_academica"

Ejecutar el sistema:

python interfaz.py