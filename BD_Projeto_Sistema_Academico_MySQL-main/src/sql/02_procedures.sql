-- =====================================================================
-- Procedures do projeto
-- =====================================================================

USE projeto_unb;

DROP PROCEDURE IF EXISTS sp_matricular_aluno_em_turma;

DELIMITER //

-- ---------------------------------------------------------------------
-- sp_matricular_aluno_em_turma
-- Insere registro em matricula_disciplina após validar vagas.
-- Levanta SIGNAL '45000' se a turma não existir ou estiver lotada.
-- Retorna SELECT com o id gerado para consumo pelo Python.
-- ---------------------------------------------------------------------
CREATE PROCEDURE sp_matricular_aluno_em_turma(
    IN p_id_matricula_curso INT,
    IN p_id_turma           INT
)
BEGIN
    DECLARE v_vagas        INT;
    DECLARE v_matriculados INT;
    DECLARE v_codigo       VARCHAR(30);

    -- Valida se a turma existe e obtém a capacidade
    SELECT quantidade_vagas INTO v_vagas
    FROM turma
    WHERE id = p_id_turma;

    IF v_vagas IS NULL THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Turma não encontrada';
    END IF;

    -- Conta alunos ativos (exclui trancados)
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
