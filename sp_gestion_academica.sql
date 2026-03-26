
-- ══════════════════════════════════════════════════════════════════
-- 1. ESTUDIANTE
-- ══════════════════════════════════════════════════════════════════

DELIMITER $$

-- ── 1 INSERT ────────────────────────────────────────────────────────
CREATE PROCEDURE sp_estudiante_insertar(
    IN p_numero_matricula    VARCHAR(20),
    IN p_nombres             VARCHAR(100),
    IN p_apellidos           VARCHAR(100),
    IN p_documento_identidad VARCHAR(20),
    IN p_fecha_nacimiento    DATE,
    IN p_direccion           VARCHAR(255),
    IN p_correo_electronico  VARCHAR(150),
    IN p_nombre_tutor        VARCHAR(200),
    IN p_contacto_emergencia VARCHAR(200),
    IN p_fecha_ingreso       DATE,
    IN p_telefono            VARCHAR(20),
    IN p_fotografia          LONGBLOB
)
BEGIN
    INSERT INTO estudiante (
        numero_matricula, nombres, apellidos, documento_identidad,
        fecha_nacimiento, direccion, correo_electronico,
        nombre_tutor, contacto_emergencia, fecha_ingreso,
        telefono, fotografia
    ) VALUES (
        p_numero_matricula, p_nombres, p_apellidos, p_documento_identidad,
        p_fecha_nacimiento, p_direccion, p_correo_electronico,
        p_nombre_tutor, p_contacto_emergencia, p_fecha_ingreso,
        p_telefono, p_fotografia
    );
END

-- ──2 SELECT ALL ────────────────────────────────────────────────────
CREATE PROCEDURE sp_estudiante_obtener_todos()
BEGIN
    SELECT
        numero_matricula, nombres, apellidos, documento_identidad,
        fecha_nacimiento, direccion, correo_electronico,
        nombre_tutor, contacto_emergencia, fecha_ingreso,
        telefono
    FROM estudiante
    ORDER BY apellidos, nombres;
END

-- ──3 SELECT BY PK ──────────────────────────────────────────────────
CREATE PROCEDURE sp_estudiante_obtener_por_id(
    IN p_numero_matricula VARCHAR(20)
)
BEGIN
    SELECT
        numero_matricula, nombres, apellidos, documento_identidad,
        fecha_nacimiento, direccion, correo_electronico,
        nombre_tutor, contacto_emergencia, fecha_ingreso,
        telefono
    FROM estudiante
    WHERE numero_matricula = p_numero_matricula;
END

-- ──4 UPDATE ────────────────────────────────────────────────────────
CREATE PROCEDURE sp_estudiante_actualizar(
    IN p_numero_matricula    VARCHAR(20),
    IN p_nombres             VARCHAR(100),
    IN p_apellidos           VARCHAR(100),
    IN p_documento_identidad VARCHAR(20),
    IN p_fecha_nacimiento    DATE,
    IN p_direccion           VARCHAR(255),
    IN p_correo_electronico  VARCHAR(150),
    IN p_nombre_tutor        VARCHAR(200),
    IN p_contacto_emergencia VARCHAR(200),
    IN p_fecha_ingreso       DATE,
    IN p_telefono            VARCHAR(20),
    IN p_fotografia          LONGBLOB
)
BEGIN
    UPDATE estudiante SET
        nombres             = p_nombres,
        apellidos           = p_apellidos,
        documento_identidad = p_documento_identidad,
        fecha_nacimiento    = p_fecha_nacimiento,
        direccion           = p_direccion,
        correo_electronico  = p_correo_electronico,
        nombre_tutor        = p_nombre_tutor,
        contacto_emergencia = p_contacto_emergencia,
        fecha_ingreso       = p_fecha_ingreso,
        telefono            = p_telefono,
        fotografia          = p_fotografia
    WHERE numero_matricula = p_numero_matricula;
END

-- ── 5 DELETE ────────────────────────────────────────────────────────
CREATE PROCEDURE sp_estudiante_eliminar(
    IN p_numero_matricula VARCHAR(20)
)
BEGIN
    DELETE FROM estudiante
    WHERE numero_matricula = p_numero_matricula;
END


-- ══════════════════════════════════════════════════════════════════
-- 2. PROFESOR
-- ══════════════════════════════════════════════════════════════════

-- ── 6 INSERT ────────────────────────────────────────────────────────
CREATE PROCEDURE sp_profesor_insertar(
    IN p_codigo_empleado      VARCHAR(20),
    IN p_nombres              VARCHAR(100),
    IN p_apellidos            VARCHAR(100),
    IN p_documento_identidad  VARCHAR(20),
    IN p_fecha_nacimiento     DATE,
    IN p_direccion            VARCHAR(255),
    IN p_correo_institucional VARCHAR(150),
    IN p_nivel_formacion      VARCHAR(50),
    IN p_especialidad         VARCHAR(100),
    IN p_anios_experiencia    SMALLINT,
    IN p_fecha_contratacion   DATE,
    IN p_tipo_contrato        VARCHAR(30),
    IN p_departamento         VARCHAR(100),
    IN p_telefono             VARCHAR(20)
)
BEGIN
    INSERT INTO profesor (
        codigo_empleado, nombres, apellidos, documento_identidad,
        fecha_nacimiento, direccion, correo_institucional,
        nivel_formacion, especialidad, anios_experiencia,
        fecha_contratacion, tipo_contrato, departamento, telefono
    ) VALUES (
        p_codigo_empleado, p_nombres, p_apellidos, p_documento_identidad,
        p_fecha_nacimiento, p_direccion, p_correo_institucional,
        p_nivel_formacion, p_especialidad, p_anios_experiencia,
        p_fecha_contratacion, p_tipo_contrato, p_departamento, p_telefono
    );
END

-- ── 7 SELECT ALL ────────────────────────────────────────────────────
CREATE PROCEDURE sp_profesor_obtener_todos()
BEGIN
    SELECT
        codigo_empleado, nombres, apellidos, documento_identidad,
        fecha_nacimiento, direccion, correo_institucional,
        nivel_formacion, especialidad, anios_experiencia,
        fecha_contratacion, tipo_contrato, departamento, telefono
    FROM profesor
    ORDER BY apellidos, nombres;
END

-- ──8  SELECT BY PK ──────────────────────────────────────────────────
CREATE PROCEDURE sp_profesor_obtener_por_id(
    IN p_codigo_empleado VARCHAR(20)
)
BEGIN
    SELECT
        codigo_empleado, nombres, apellidos, documento_identidad,
        fecha_nacimiento, direccion, correo_institucional,
        nivel_formacion, especialidad, anios_experiencia,
        fecha_contratacion, tipo_contrato, departamento, telefono
    FROM profesor
    WHERE codigo_empleado = p_codigo_empleado;
END

-- ──9 UPDATE ────────────────────────────────────────────────────────
CREATE PROCEDURE sp_profesor_actualizar(
    IN p_codigo_empleado      VARCHAR(20),
    IN p_nombres              VARCHAR(100),
    IN p_apellidos            VARCHAR(100),
    IN p_documento_identidad  VARCHAR(20),
    IN p_fecha_nacimiento     DATE,
    IN p_direccion            VARCHAR(255),
    IN p_correo_institucional VARCHAR(150),
    IN p_nivel_formacion      VARCHAR(50),
    IN p_especialidad         VARCHAR(100),
    IN p_anios_experiencia    SMALLINT,
    IN p_fecha_contratacion   DATE,
    IN p_tipo_contrato        VARCHAR(30),
    IN p_departamento         VARCHAR(100),
    IN p_telefono             VARCHAR(20)
)
BEGIN
    UPDATE profesor SET
        nombres              = p_nombres,
        apellidos            = p_apellidos,
        documento_identidad  = p_documento_identidad,
        fecha_nacimiento     = p_fecha_nacimiento,
        direccion            = p_direccion,
        correo_institucional = p_correo_institucional,
        nivel_formacion      = p_nivel_formacion,
        especialidad         = p_especialidad,
        anios_experiencia    = p_anios_experiencia,
        fecha_contratacion   = p_fecha_contratacion,
        tipo_contrato        = p_tipo_contrato,
        departamento         = p_departamento,
        telefono             = p_telefono
    WHERE codigo_empleado = p_codigo_empleado;
END

-- ──10 DELETE ────────────────────────────────────────────────────────
CREATE PROCEDURE sp_profesor_eliminar(
    IN p_codigo_empleado VARCHAR(20)
)
BEGIN
    DELETE FROM profesor
    WHERE codigo_empleado = p_codigo_empleado;
END


-- ══════════════════════════════════════════════════════════════════
-- 3. ASIGNATURA
-- ══════════════════════════════════════════════════════════════════
-- ──11 INSERT ────────────────────────────────────────────────────────
CREATE PROCEDURE sp_asignatura_insertar(
    IN p_codigo_asignatura    VARCHAR(20),
    IN p_nombre               VARCHAR(150),
    IN p_area_conocimiento    VARCHAR(100),
    IN p_horas_teoricas       SMALLINT,
    IN p_horas_practicas      SMALLINT,
    IN p_creditos_academicos  SMALLINT,
    IN p_objetivos_generales  TEXT,
    IN p_objetivos_especificos TEXT,
    IN p_requisitos_previos   TEXT,
    IN p_bibliografia         TEXT
)
BEGIN
    INSERT INTO asignatura (
        codigo_asignatura, nombre, area_conocimiento,
        horas_teoricas, horas_practicas, creditos_academicos,
        objetivos_generales, objetivos_especificos,
        requisitos_previos, bibliografia
    ) VALUES (
        p_codigo_asignatura, p_nombre, p_area_conocimiento,
        p_horas_teoricas, p_horas_practicas, p_creditos_academicos,
        p_objetivos_generales, p_objetivos_especificos,
        p_requisitos_previos, p_bibliografia
    );
END

-- ── 12 SELECT ALL ────────────────────────────────────────────────────
CREATE PROCEDURE sp_asignatura_obtener_todos()
BEGIN
    SELECT
        codigo_asignatura, nombre, area_conocimiento,
        horas_teoricas, horas_practicas, creditos_academicos,
        objetivos_generales, objetivos_especificos,
        requisitos_previos, bibliografia
    FROM asignatura
    ORDER BY nombre;
END

-- ──13 SELECT BY PK ──────────────────────────────────────────────────
CREATE PROCEDURE sp_asignatura_obtener_por_id(
    IN p_codigo_asignatura VARCHAR(20)
)
BEGIN
    SELECT
        codigo_asignatura, nombre, area_conocimiento,
        horas_teoricas, horas_practicas, creditos_academicos,
        objetivos_generales, objetivos_especificos,
        requisitos_previos, bibliografia
    FROM asignatura
    WHERE codigo_asignatura = p_codigo_asignatura;
END

-- ──14 UPDATE ────────────────────────────────────────────────────────
CREATE PROCEDURE sp_asignatura_actualizar(
    IN p_codigo_asignatura     VARCHAR(20),
    IN p_nombre                VARCHAR(150),
    IN p_area_conocimiento     VARCHAR(100),
    IN p_horas_teoricas        SMALLINT,
    IN p_horas_practicas       SMALLINT,
    IN p_creditos_academicos   SMALLINT,
    IN p_objetivos_generales   TEXT,
    IN p_objetivos_especificos TEXT,
    IN p_requisitos_previos    TEXT,
    IN p_bibliografia          TEXT
)
BEGIN
    UPDATE asignatura SET
        nombre                = p_nombre,
        area_conocimiento     = p_area_conocimiento,
        horas_teoricas        = p_horas_teoricas,
        horas_practicas       = p_horas_practicas,
        creditos_academicos   = p_creditos_academicos,
        objetivos_generales   = p_objetivos_generales,
        objetivos_especificos = p_objetivos_especificos,
        requisitos_previos    = p_requisitos_previos,
        bibliografia          = p_bibliografia
    WHERE codigo_asignatura = p_codigo_asignatura;
END

-- ──15 DELETE ────────────────────────────────────────────────────────

CREATE PROCEDURE sp_asignatura_eliminar(
    IN p_codigo_asignatura VARCHAR(20)
)
BEGIN
    DELETE FROM asignatura
    WHERE codigo_asignatura = p_codigo_asignatura;
END


-- ══════════════════════════════════════════════════════════════════
-- 4. CURSO
-- ══════════════════════════════════════════════════════════════════

-- ──16 INSERT ────────────────────────────────────────────────────────
CREATE PROCEDURE sp_curso_insertar(
    IN p_codigo_curso            VARCHAR(20),
    IN p_periodo_academico       VARCHAR(20),
    IN p_asignatura              VARCHAR(20),
    IN p_profesor_asignado       VARCHAR(20),
    IN p_aula                    VARCHAR(20),
    IN p_horario_dias            VARCHAR(100),
    IN p_horario_horas           VARCHAR(100),
    IN p_cupo_maximo             SMALLINT,
    IN p_metodologia_evaluacion  TEXT
)
BEGIN
    INSERT INTO curso (
        codigo_curso, periodo_academico, asignatura,
        profesor_asignado, aula, horario_dias, horario_horas,
        cupo_maximo, metodologia_evaluacion
    ) VALUES (
        p_codigo_curso, p_periodo_academico, p_asignatura,
        p_profesor_asignado, p_aula, p_horario_dias, p_horario_horas,
        p_cupo_maximo, p_metodologia_evaluacion
    );
END

-- ──17 SELECT ALL ────────────────────────────────────────────────────
CREATE PROCEDURE sp_curso_obtener_todos()
BEGIN
    SELECT
        c.codigo_curso, c.periodo_academico,
        c.asignatura, a.nombre AS nombre_asignatura,
        c.profesor_asignado,
        CONCAT(p.nombres, ' ', p.apellidos) AS nombre_profesor,
        c.aula, c.horario_dias, c.horario_horas,
        c.cupo_maximo, c.metodologia_evaluacion
    FROM curso c
    INNER JOIN Asignatura a ON c.asignatura       = a.codigo_asignatura
    INNER JOIN Profesor   p ON c.profesor_asignado = p.codigo_empleado
    ORDER BY c.periodo_academico, a.nombre;
END

-- ──18 SELECT BY PK ──────────────────────────────────────────────────
CREATE PROCEDURE sp_curso_obtener_por_id(
    IN p_codigo_curso VARCHAR(20)
)
BEGIN
    SELECT
        c.codigo_curso, c.periodo_academico,
        c.asignatura, a.nombre AS nombre_asignatura,
        c.profesor_asignado,
        CONCAT(p.nombres, ' ', p.apellidos) AS nombre_profesor,
        c.aula, c.horario_dias, c.horario_horas,
        c.cupo_maximo, c.metodologia_evaluacion
    FROM curso c
    INNER JOIN Asignatura a ON c.asignatura        = a.codigo_asignatura
    INNER JOIN Profesor   p ON c.profesor_asignado = p.codigo_empleado
    WHERE c.codigo_curso = p_codigo_curso;
END

-- ── 19 UPDATE ────────────────────────────────────────────────────────
CREATE PROCEDURE sp_curso_actualizar(
    IN p_codigo_curso           VARCHAR(20),
    IN p_periodo_academico      VARCHAR(20),
    IN p_asignatura             VARCHAR(20),
    IN p_profesor_asignado      VARCHAR(20),
    IN p_aula                   VARCHAR(20),
    IN p_horario_dias           VARCHAR(100),
    IN p_horario_horas          VARCHAR(100),
    IN p_cupo_maximo            SMALLINT,
    IN p_metodologia_evaluacion TEXT
)
BEGIN
    UPDATE curso SET
        periodo_academico      = p_periodo_academico,
        asignatura             = p_asignatura,
        profesor_asignado      = p_profesor_asignado,
        aula                   = p_aula,
        horario_dias           = p_horario_dias,
        horario_horas          = p_horario_horas,
        cupo_maximo            = p_cupo_maximo,
        metodologia_evaluacion = p_metodologia_evaluacion
    WHERE codigo_curso = p_codigo_curso;
END

-- ──20 DELETE ────────────────────────────────────────────────────────
CREATE PROCEDURE sp_curso_eliminar(
    IN p_codigo_curso VARCHAR(20)
)
BEGIN
    DELETE FROM curso
    WHERE codigo_curso = p_codigo_curso;
END

DELIMITER ;


-- ══════════════════════════════════════════════════════════════════
-- EJEMPLOS DE USO
-- ══════════════════════════════════════════════════════════════════

-- Insertar estudiante
-- CALL sp_estudiante_insertar('MAT001','Ana','García','1234567890','2000-03-15','Calle 10 #5-20','ana@mail.com','Pedro García','Pedro García 300-000-0000','2024-01-15','300-000-0000',NULL);

-- Consultar todos los estudiantes
-- CALL sp_estudiante_obtener_todos();

-- Consultar estudiante por matrícula
-- CALL sp_estudiante_obtener_por_id('MAT001');

-- Actualizar estudiante
-- CALL sp_estudiante_actualizar('MAT001','Ana María','García','1234567890','2000-03-15','Carrera 5 #10-30','ana@mail.com','Pedro García','Pedro García 300-000-0000','2024-01-15','310-000-0000',NULL);

-- Eliminar estudiante
-- CALL sp_estudiante_eliminar('MAT001');
SHOW PROCEDURE STATUS;
