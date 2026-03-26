-- ============================================================
--  SISTEMA DE GESTIÓN ACADÉMICA
--  Base de Datos MySQL
--  Generado desde Diccionario de Datos
-- ============================================================

CREATE DATABASE IF NOT EXISTS gestion_academica
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE gestion_academica;

-- ============================================================
-- 1. Departamento
-- ============================================================
CREATE TABLE Departamento (
    codigo_departamento VARCHAR(20)  NOT NULL,
    nombre              VARCHAR(100) NOT NULL,
    descripcion         TEXT,
    CONSTRAINT pk_departamento PRIMARY KEY (codigo_departamento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- 2. Carrera
-- ============================================================
CREATE TABLE Carrera (
    codigo_carrera VARCHAR(20)  NOT NULL,
    nombre         VARCHAR(150) NOT NULL,
    descripcion    TEXT,
    CONSTRAINT pk_carrera PRIMARY KEY (codigo_carrera)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- 3. PeriodoAcademico
-- ============================================================
CREATE TABLE PeriodoAcademico (
    codigo_periodo         VARCHAR(20) NOT NULL,
    descripcion            VARCHAR(50) NOT NULL,
    fecha_inicio           DATE        NOT NULL,
    fecha_finalizacion     DATE        NOT NULL,
    estado_actual          VARCHAR(20) NOT NULL DEFAULT 'Planificado',
    calendario_actividades JSON,
    CONSTRAINT pk_periodo       PRIMARY KEY (codigo_periodo),
    CONSTRAINT chk_periodo_desc CHECK (descripcion IN ('Semestre', 'Trimestre', 'Anual')),
    CONSTRAINT chk_periodo_est  CHECK (estado_actual IN ('Planificado', 'En curso', 'Finalizado')),
    CONSTRAINT chk_periodo_fec  CHECK (fecha_finalizacion > fecha_inicio)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- 4. Aula
-- ============================================================
CREATE TABLE Aula (
    id_aula       VARCHAR(20)  NOT NULL,
    edificio      VARCHAR(100) NOT NULL,
    piso          SMALLINT     NOT NULL,
    capacidad     SMALLINT     NOT NULL,
    tipo          VARCHAR(30)  NOT NULL,
    equipamiento  TEXT,
    estado_actual VARCHAR(20)  NOT NULL DEFAULT 'Disponible',
    CONSTRAINT pk_aula       PRIMARY KEY (id_aula),
    CONSTRAINT chk_aula_piso CHECK (piso >= 0),
    CONSTRAINT chk_aula_cap  CHECK (capacidad > 0),
    CONSTRAINT chk_aula_tipo CHECK (tipo IN ('Teórica', 'Laboratorio', 'Taller')),
    CONSTRAINT chk_aula_est  CHECK (estado_actual IN ('Disponible', 'En mantenimiento', 'Fuera de servicio'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- 5. Asignatura
-- ============================================================
CREATE TABLE Asignatura (
    codigo_asignatura     VARCHAR(20)  NOT NULL,
    nombre                VARCHAR(150) NOT NULL,
    area_conocimiento     VARCHAR(100) NOT NULL,
    horas_teoricas        SMALLINT     NOT NULL DEFAULT 0,
    horas_practicas       SMALLINT     NOT NULL DEFAULT 0,
    creditos_academicos   SMALLINT     NOT NULL,
    requisitos_previos    TEXT,
    objetivos_generales   TEXT         NOT NULL,
    objetivos_especificos TEXT         NOT NULL,
    bibliografia          TEXT,
    CONSTRAINT pk_asignatura PRIMARY KEY (codigo_asignatura),
    CONSTRAINT chk_asig_ht   CHECK (horas_teoricas >= 0),
    CONSTRAINT chk_asig_hp   CHECK (horas_practicas >= 0),
    CONSTRAINT chk_asig_hsum CHECK (horas_teoricas + horas_practicas > 0),
    CONSTRAINT chk_asig_cred CHECK (creditos_academicos > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- 6. Estudiante
-- ============================================================
CREATE TABLE Estudiante (
    numero_matricula    VARCHAR(20)  NOT NULL,
    nombres             VARCHAR(100) NOT NULL,
    apellidos           VARCHAR(100) NOT NULL,
    documento_identidad VARCHAR(20)  NOT NULL,
    fecha_nacimiento    DATE         NOT NULL,
    direccion           VARCHAR(255) NOT NULL,
    telefono            VARCHAR(20),
    correo_electronico  VARCHAR(150) NOT NULL,
    fotografia          LONGBLOB,
    nombre_tutor        VARCHAR(200) NOT NULL,
    contacto_emergencia VARCHAR(200) NOT NULL,
    fecha_ingreso       DATE         NOT NULL,
    CONSTRAINT pk_estudiante     PRIMARY KEY (numero_matricula),
    CONSTRAINT uq_est_doc        UNIQUE (documento_identidad),
    CONSTRAINT uq_est_correo     UNIQUE (correo_electronico),
    CONSTRAINT chk_est_nombres   CHECK (CHAR_LENGTH(nombres) >= 2),
    CONSTRAINT chk_est_apellidos CHECK (CHAR_LENGTH(apellidos) >= 2),
    CONSTRAINT chk_est_doc_min   CHECK (CHAR_LENGTH(documento_identidad) >= 5),
    CONSTRAINT chk_est_edad      CHECK (TIMESTAMPDIFF(YEAR, fecha_nacimiento, fecha_ingreso) >= 5),
    CONSTRAINT chk_est_ingreso   CHECK (fecha_ingreso >= fecha_nacimiento),
    CONSTRAINT chk_est_correo    CHECK (correo_electronico REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$')
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- 7. Profesor
-- ============================================================
CREATE TABLE Profesor (
    codigo_empleado      VARCHAR(20)  NOT NULL,
    nombres              VARCHAR(100) NOT NULL,
    apellidos            VARCHAR(100) NOT NULL,
    documento_identidad  VARCHAR(20)  NOT NULL,
    fecha_nacimiento     DATE         NOT NULL,
    direccion            VARCHAR(255) NOT NULL,
    telefono             VARCHAR(20),
    correo_institucional VARCHAR(150) NOT NULL,
    nivel_formacion      VARCHAR(50)  NOT NULL,
    especialidad         VARCHAR(100) NOT NULL,
    anios_experiencia    SMALLINT     NOT NULL DEFAULT 0,
    fecha_contratacion   DATE         NOT NULL,
    tipo_contrato        VARCHAR(30)  NOT NULL,
    departamento         VARCHAR(20)  NOT NULL,
    CONSTRAINT pk_profesor       PRIMARY KEY (codigo_empleado),
    CONSTRAINT uq_prof_doc       UNIQUE (documento_identidad),
    CONSTRAINT uq_prof_correo    UNIQUE (correo_institucional),
    CONSTRAINT fk_prof_depto     FOREIGN KEY (departamento)
                                 REFERENCES Departamento(codigo_departamento)
                                 ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_prof_exp      CHECK (anios_experiencia >= 0),
    CONSTRAINT chk_prof_contrat  CHECK (fecha_contratacion >= fecha_nacimiento),
    CONSTRAINT chk_prof_nivel    CHECK (nivel_formacion IN
                                  ('Técnico','Tecnólogo','Pregrado','Especialización','Maestría','Doctorado')),
    CONSTRAINT chk_prof_contrato CHECK (tipo_contrato IN ('Tiempo completo','Medio tiempo','Por horas')),
    CONSTRAINT chk_prof_correo   CHECK (correo_institucional REGEXP '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$')
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- 8. Curso
-- ============================================================
CREATE TABLE Curso (
    codigo_curso           VARCHAR(20)  NOT NULL,
    periodo_academico      VARCHAR(20)  NOT NULL,
    asignatura             VARCHAR(20)  NOT NULL,
    profesor_asignado      VARCHAR(20)  NOT NULL,
    aula                   VARCHAR(20)  NOT NULL,
    horario_dias           VARCHAR(100) NOT NULL,
    horario_horas          VARCHAR(100) NOT NULL,
    cupo_maximo            SMALLINT     NOT NULL,
    metodologia_evaluacion TEXT         NOT NULL,
    CONSTRAINT pk_curso      PRIMARY KEY (codigo_curso),
    CONSTRAINT fk_curso_per  FOREIGN KEY (periodo_academico)
                             REFERENCES PeriodoAcademico(codigo_periodo)
                             ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_curso_asig FOREIGN KEY (asignatura)
                             REFERENCES Asignatura(codigo_asignatura)
                             ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_curso_prof FOREIGN KEY (profesor_asignado)
                             REFERENCES Profesor(codigo_empleado)
                             ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_curso_aula FOREIGN KEY (aula)
                             REFERENCES Aula(id_aula)
                             ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_curso_cupo CHECK (cupo_maximo > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- 9. Inscripcion (N:M Estudiante–Curso)
-- ============================================================
CREATE TABLE Inscripcion (
    numero_matricula  VARCHAR(20) NOT NULL,
    codigo_curso      VARCHAR(20) NOT NULL,
    fecha_inscripcion DATE        NOT NULL DEFAULT (CURDATE()),
    CONSTRAINT pk_inscripcion PRIMARY KEY (numero_matricula, codigo_curso),
    CONSTRAINT fk_insc_est    FOREIGN KEY (numero_matricula)
                              REFERENCES Estudiante(numero_matricula)
                              ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_insc_curso  FOREIGN KEY (codigo_curso)
                              REFERENCES Curso(codigo_curso)
                              ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- 10. Calificacion
-- ============================================================
CREATE TABLE Calificacion (
    id_calificacion BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
    estudiante      VARCHAR(20)     NOT NULL,
    curso           VARCHAR(20)     NOT NULL,
    tipo_evaluacion VARCHAR(30)     NOT NULL,
    fecha           DATE            NOT NULL,
    valor_numerico  DECIMAL(5,2)    NOT NULL,
    porcentaje      DECIMAL(5,2)    NOT NULL,
    observaciones   TEXT,
    CONSTRAINT pk_calificacion PRIMARY KEY (id_calificacion),
    CONSTRAINT fk_calif_est    FOREIGN KEY (estudiante)
                               REFERENCES Estudiante(numero_matricula)
                               ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_calif_curso  FOREIGN KEY (curso)
                               REFERENCES Curso(codigo_curso)
                               ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_calif_tipo  CHECK (tipo_evaluacion IN ('Parcial','Final','Trabajo','Proyecto')),
    CONSTRAINT chk_calif_nota  CHECK (valor_numerico BETWEEN 0.00 AND 5.00),
    CONSTRAINT chk_calif_porc  CHECK (porcentaje BETWEEN 0.01 AND 100.00)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- 11. PlanEstudios
-- ============================================================
CREATE TABLE PlanEstudios (
    codigo_plan           VARCHAR(20) NOT NULL,
    carrera               VARCHAR(20) NOT NULL,
    fecha_aprobacion      DATE        NOT NULL,
    creditos_totales      SMALLINT    NOT NULL,
    requisitos_graduacion TEXT        NOT NULL,
    CONSTRAINT pk_plan      PRIMARY KEY (codigo_plan),
    CONSTRAINT fk_plan_carr FOREIGN KEY (carrera)
                            REFERENCES Carrera(codigo_carrera)
                            ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_plan_cred CHECK (creditos_totales > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- 12. PlanEstudios_Asignatura (N:M con nivel)
-- ============================================================
CREATE TABLE PlanEstudios_Asignatura (
    codigo_plan       VARCHAR(20) NOT NULL,
    codigo_asignatura VARCHAR(20) NOT NULL,
    nivel             SMALLINT    NOT NULL,
    CONSTRAINT pk_plan_asig PRIMARY KEY (codigo_plan, codigo_asignatura),
    CONSTRAINT fk_pa_plan   FOREIGN KEY (codigo_plan)
                            REFERENCES PlanEstudios(codigo_plan)
                            ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_pa_asig   FOREIGN KEY (codigo_asignatura)
                            REFERENCES Asignatura(codigo_asignatura)
                            ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_pa_nivel CHECK (nivel >= 1)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- 13. MaterialBibliografico
-- ============================================================
CREATE TABLE MaterialBibliografico (
    codigo_material     VARCHAR(20)  NOT NULL,
    titulo              VARCHAR(255) NOT NULL,
    autores             VARCHAR(500) NOT NULL,
    editorial           VARCHAR(150),
    anio_publicacion    SMALLINT,
    edicion             VARCHAR(50),
    isbn                VARCHAR(20),
    categoria_tematica  VARCHAR(100) NOT NULL,
    formato             VARCHAR(20)  NOT NULL,
    ubicacion_fisica    VARCHAR(100),
    cantidad_ejemplares SMALLINT,
    CONSTRAINT pk_material     PRIMARY KEY (codigo_material),
    CONSTRAINT uq_mat_isbn     UNIQUE (isbn),
    CONSTRAINT chk_mat_formato CHECK (formato IN ('Físico', 'Digital')),
    CONSTRAINT chk_mat_anio    CHECK (anio_publicacion IS NULL OR
                                      anio_publicacion BETWEEN 1000 AND 2100),
    CONSTRAINT chk_mat_ejem    CHECK (cantidad_ejemplares IS NULL OR cantidad_ejemplares >= 0),
    CONSTRAINT chk_mat_ubic    CHECK (formato = 'Digital' OR ubicacion_fisica IS NOT NULL)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- 14. Prestamo
-- ============================================================
CREATE TABLE Prestamo (
    codigo_prestamo       VARCHAR(20)                  NOT NULL,
    fecha_prestamo        DATE                         NOT NULL,
    fecha_devolucion_prog DATE                         NOT NULL,
    fecha_devolucion_real DATE,
    material_prestado     VARCHAR(20)                  NOT NULL,
    solicitante_tipo      ENUM('Estudiante','Profesor') NOT NULL,
    solicitante           VARCHAR(20)                  NOT NULL,
    estado                VARCHAR(20)                  NOT NULL DEFAULT 'Vigente',
    multa_aplicada        DECIMAL(10,2),
    CONSTRAINT pk_prestamo      PRIMARY KEY (codigo_prestamo),
    CONSTRAINT fk_prest_mat     FOREIGN KEY (material_prestado)
                                REFERENCES MaterialBibliografico(codigo_material)
                                ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_prest_est    CHECK (estado IN ('Vigente', 'Devuelto', 'Retrasado')),
    CONSTRAINT chk_prest_fdprog CHECK (fecha_devolucion_prog > fecha_prestamo),
    CONSTRAINT chk_prest_fp     CHECK (fecha_prestamo <= CURDATE()),
    CONSTRAINT chk_prest_multa  CHECK (multa_aplicada IS NULL OR multa_aplicada >= 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- 15. ActividadExtracurricular
-- ============================================================
CREATE TABLE ActividadExtracurricular (
    codigo_actividad     VARCHAR(20)  NOT NULL,
    nombre               VARCHAR(150) NOT NULL,
    tipo                 VARCHAR(80)  NOT NULL,
    descripcion          TEXT,
    profesor_responsable VARCHAR(20)  NOT NULL,
    horario              VARCHAR(150) NOT NULL,
    lugar                VARCHAR(150) NOT NULL,
    cupo                 SMALLINT     NOT NULL,
    CONSTRAINT pk_actividad PRIMARY KEY (codigo_actividad),
    CONSTRAINT fk_act_prof  FOREIGN KEY (profesor_responsable)
                            REFERENCES Profesor(codigo_empleado)
                            ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT chk_act_cupo CHECK (cupo > 0)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


-- ============================================================
-- 16. Actividad_Participante (N:M Estudiante–Actividad)
-- ============================================================
CREATE TABLE Actividad_Participante (
    codigo_actividad VARCHAR(20) NOT NULL,
    numero_matricula VARCHAR(20) NOT NULL,
    CONSTRAINT pk_act_part PRIMARY KEY (codigo_actividad, numero_matricula),
    CONSTRAINT fk_ap_act   FOREIGN KEY (codigo_actividad)
                           REFERENCES ActividadExtracurricular(codigo_actividad)
                           ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_ap_est   FOREIGN KEY (numero_matricula)
                           REFERENCES Estudiante(numero_matricula)
                           ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ============================================================
-- FIN DEL SCRIPT
-- ============================================================