-- =====================================================================
-- Correção: aluno conseguia ser matriculado várias vezes na mesma turma
-- (sp_matricular_aluno_em_turma não checava matrícula existente).
-- Executar APÓS 06_atualizar_senhas.sql.
-- =====================================================================

USE projeto_unb;

-- Força UTF-8 na sessão, independente do codepage do cliente
-- (evita corrupção de acentos em clientes Windows com console cp850)
SET NAMES utf8mb4;

-- ---------------------------------------------------------------------
-- 1. Limpa duplicatas já criadas em testes (mantém a matrícula mais
--    antiga de cada par aluno+turma, apaga as repetidas).
--    ON DELETE CASCADE já cuida de resultado_avaliacao e frequencia
--    ligados às linhas removidas.
-- ---------------------------------------------------------------------
DELETE md1 FROM matricula_disciplina md1
INNER JOIN matricula_disciplina md2
    ON md1.id_matricula_curso = md2.id_matricula_curso
   AND md1.id_turma = md2.id_turma
   AND md1.id > md2.id;

-- ---------------------------------------------------------------------
-- 2. Trava no nível do banco: mesmo que alguém insira direto via SQL
--    (sem passar pela procedure), o MySQL recusa duplicata.
--    Obs: TRANCADO também entra na constraint — não é possível
--    matricular > 1x na mesma turma nem depois de trancar, hoje.
--    Se o grupo quiser permitir re-matrícula após trancamento, essa
--    constraint precisaria virar uma unique parcial (não suportado
--    nativamente no MySQL) — fora do escopo desta correção.
-- ---------------------------------------------------------------------
ALTER TABLE matricula_disciplina
    ADD CONSTRAINT uq_matricula_curso_turma UNIQUE (id_matricula_curso, id_turma);

-- ---------------------------------------------------------------------
-- 3. Recria a procedure com a checagem de "já matriculado" (mesma
--    lógica já atualizada em src/sql/02_procedures.sql).
-- ---------------------------------------------------------------------
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
