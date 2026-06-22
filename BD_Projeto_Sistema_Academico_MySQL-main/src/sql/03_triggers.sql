-- =====================================================================
-- Triggers do projeto
-- =====================================================================
-- MySQL não suporta AFTER INSERT OR UPDATE em um único trigger.
-- Dois triggers separados executam a mesma lógica de recálculo.
-- =====================================================================

USE projeto_unb;

DROP TRIGGER IF EXISTS tg_atualiza_nota_final_insert;
DROP TRIGGER IF EXISTS tg_atualiza_nota_final_update;

DELIMITER //

-- ---------------------------------------------------------------------
-- tg_atualiza_nota_final_insert
-- Dispara após cada INSERT em resultado_avaliacao.
-- Recalcula a média ponderada (SUM(nota*peso)/SUM(peso)) e grava
-- em matricula_disciplina.nota.
-- ---------------------------------------------------------------------
CREATE TRIGGER tg_atualiza_nota_final_insert
AFTER INSERT ON resultado_avaliacao
FOR EACH ROW
BEGIN
    DECLARE v_nota DECIMAL(5,2);

    SELECT SUM(ra.nota * av.peso) / NULLIF(SUM(av.peso), 0)
    INTO v_nota
    FROM resultado_avaliacao ra
    JOIN avaliacao av ON av.id = ra.id_avaliacao
    WHERE ra.id_matricula_disciplina = NEW.id_matricula_disciplina
      AND ra.nota IS NOT NULL;

    UPDATE matricula_disciplina
    SET nota = v_nota
    WHERE id = NEW.id_matricula_disciplina;
END //

-- ---------------------------------------------------------------------
-- tg_atualiza_nota_final_update
-- Dispara após cada UPDATE em resultado_avaliacao.
-- Mesma lógica de recálculo — garante consistência em correções.
-- ---------------------------------------------------------------------
CREATE TRIGGER tg_atualiza_nota_final_update
AFTER UPDATE ON resultado_avaliacao
FOR EACH ROW
BEGIN
    DECLARE v_nota DECIMAL(5,2);

    SELECT SUM(ra.nota * av.peso) / NULLIF(SUM(av.peso), 0)
    INTO v_nota
    FROM resultado_avaliacao ra
    JOIN avaliacao av ON av.id = ra.id_avaliacao
    WHERE ra.id_matricula_disciplina = NEW.id_matricula_disciplina
      AND ra.nota IS NOT NULL;

    UPDATE matricula_disciplina
    SET nota = v_nota
    WHERE id = NEW.id_matricula_disciplina;
END //

DELIMITER ;
