-- =====================================================================
-- Recria SOMENTE a procedure sp_matricular_aluno_em_turma.
-- Use este script se 07_corrigir_matricula_duplicada.sql já rodou uma
-- vez e falhou depois com "Duplicate key name 'uq_matricula_curso_turma'"
-- em uma re-execução — isso indica que a constraint já existe e só
-- falta garantir que a procedure foi recriada com UTF-8 correto.
-- =====================================================================

USE projeto_unb;

-- Força UTF-8 na sessão, independente do codepage do cliente
-- (evita corrupção de acentos em clientes Windows com console cp850)
SET NAMES utf8mb4;

DROP PROCEDURE IF EXISTS sp_matricular_aluno_em_turma;

DELIMITER //

CREATE PROCEDURE sp_matricular_aluno_em_turma(
    IN p_id_matricula_curso INT,
    IN p_id_turma           INT
)
BEGIN
    DECLARE v_vagas          INT;
    DECLARE v_matriculados   INT;
    DECLARE v_ja_matriculado INT;
    DECLARE v_codigo         VARCHAR(30);

    SELECT quantidade_vagas INTO v_vagas
    FROM turma
    WHERE id = p_id_turma;

    IF v_vagas IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Turma não encontrada';
    END IF;

    SELECT COUNT(*) INTO v_ja_matriculado
    FROM matricula_disciplina
    WHERE id_matricula_curso = p_id_matricula_curso
      AND id_turma = p_id_turma
      AND status != 'TRANCADO';

    IF v_ja_matriculado > 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Aluno já matriculado nesta turma';
    END IF;

    SELECT COUNT(*) INTO v_matriculados
    FROM matricula_disciplina
    WHERE id_turma = p_id_turma
      AND status != 'TRANCADO';

    IF v_matriculados >= v_vagas THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Turma sem vagas disponíveis';
    END IF;

    SET v_codigo = CONCAT('MD-', p_id_matricula_curso, '-', p_id_turma);

    INSERT INTO matricula_disciplina (
        id_matricula_curso,
        id_turma,
        codigo,
        data_matricula_disciplina,
        status
    ) VALUES (
        p_id_matricula_curso,
        p_id_turma,
        v_codigo,
        CURDATE(),
        'MATRICULADO'
    );

    SELECT LAST_INSERT_ID() AS id_matricula_disciplina;
END //

DELIMITER ;
