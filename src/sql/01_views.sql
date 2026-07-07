-- =====================================================================
-- Views do projeto
-- =====================================================================

USE projeto_unb;

-- Força UTF-8 na sessão, independente do codepage do cliente
-- (evita corrupção de acentos em clientes Windows com console cp850)
SET NAMES utf8mb4;

-- ---------------------------------------------------------------------
-- vw_historico_aluno
-- Histórico escolar completo de um aluno: todas as disciplinas
-- matriculadas com nota final, semestre, curso e status.
-- Uso: buscar_historico_aluno(id_aluno) filtra por id_pessoa.
-- ---------------------------------------------------------------------
CREATE OR REPLACE VIEW vw_historico_aluno AS
SELECT
    p.id                            AS id_pessoa,
    p.nome                          AS nome_aluno,
    p.cpf,
    mc.id                           AS id_matricula_curso,
    mc.codigo                       AS matricula_curso_codigo,
    mc.status                       AS status_matricula_curso,
    c.id                            AS id_curso,
    c.nome                          AS nome_curso,
    c.sigla                         AS sigla_curso,
    s.id                            AS id_semestre,
    s.nome                          AS semestre,
    s.data_inicio,
    s.data_fim,
    d.id                            AS id_disciplina,
    d.codigo                        AS codigo_disciplina,
    d.nome                          AS nome_disciplina,
    t.id                            AS id_turma,
    t.codigo                        AS codigo_turma,
    md.id                           AS id_matricula_disciplina,
    md.codigo                       AS matricula_disciplina_codigo,
    md.nota                         AS nota_final,
    md.status                       AS status_matricula_disciplina,
    md.data_matricula_disciplina,
    md.data_trancamento_disciplina
FROM pessoa p
JOIN aluno               a  ON a.id_pessoa          = p.id
JOIN matricula_curso     mc ON mc.id_aluno           = a.id_pessoa
JOIN curso               c  ON c.id                 = mc.id_curso
JOIN matricula_disciplina md ON md.id_matricula_curso = mc.id
JOIN turma               t  ON t.id                 = md.id_turma
JOIN oferta              o  ON o.id                 = t.id_oferta
JOIN disciplina          d  ON d.id                 = o.id_disciplina
JOIN semestre            s  ON s.id                 = o.id_semestre;
