-- =====================================================================
-- Comandos SQL da Apresentação — SGA UnB
-- Extraído do roteiro de fala, na ordem exata de uso.
-- Rodar no terminal: mysql -u root -p --default-character-set=utf8mb4 projeto_unb
-- =====================================================================


-- =====================================================================
-- VERIFICAÇÃO PRÉ-APRESENTAÇÃO (rodar ANTES de começar, sozinho)
-- Resultado esperado: 5
-- =====================================================================
SELECT COUNT(*) FROM matricula_disciplina;


-- =====================================================================
-- BLOCO 3 — CALEBE — Banco de Dados no SGBD
-- =====================================================================

-- Chave primária automática (AUTO_INCREMENT)
INSERT INTO departamento (nome) VALUES ('Departamento de Demonstração');
SELECT LAST_INSERT_ID();


-- =====================================================================
-- BLOCO 7 — VITOR — View (vw_historico_aluno)
-- =====================================================================

SELECT nome_aluno, semestre, nome_disciplina, nota_final, status_matricula_disciplina
FROM vw_historico_aluno
WHERE id_pessoa = 1
ORDER BY semestre DESC;


-- =====================================================================
-- BLOCO 8 — VITOR — Procedure (sp_matricular_aluno_em_turma)
-- =====================================================================

-- Demo 1: caso de sucesso
CALL sp_matricular_aluno_em_turma(1, 5);

-- Demo 2: caso de erro (turma inexistente)
CALL sp_matricular_aluno_em_turma(1, 9999);


-- =====================================================================
-- BLOCO 9 — CALEBE — Trigger (recálculo automático de nota)
-- =====================================================================

-- Nota ANTES (roda e guarda o resultado na cabeça pra comparar)
SELECT nota FROM matricula_disciplina WHERE id = 1;

-- Dispara o trigger (insere resultado de avaliação, sem UPDATE manual)
INSERT INTO resultado_avaliacao (id_avaliacao, id_matricula_disciplina, nota, status, data_entrega)
VALUES (1, 1, 9.0, 'CORRIGIDO', CURDATE());

-- Nota DEPOIS (deve ter mudado sozinha)
SELECT nota FROM matricula_disciplina WHERE id = 1;


-- =====================================================================
-- LIMPEZA PÓS-APRESENTAÇÃO (rodar depois de cada ENSAIO — não rodar
-- depois da apresentação de verdade, senão apaga a prova do que foi
-- mostrado)
-- =====================================================================

DELETE FROM departamento WHERE nome = 'Departamento de Demonstração';
DELETE FROM matricula_disciplina WHERE id_matricula_curso = 1 AND id_turma = 5;
DELETE FROM resultado_avaliacao WHERE id_avaliacao = 1 AND id_matricula_disciplina = 1 AND nota = 9.0;

-- Confirma que voltou ao normal (deve dar 5 de novo)
SELECT COUNT(*) FROM matricula_disciplina;
