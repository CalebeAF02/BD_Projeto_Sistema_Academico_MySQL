-- =====================================================================
-- Seeds — 5+ registros por tabela (25 tabelas)
-- Executar APÓS: 00_criar_tabelas.sql, 01_views.sql,
--                02_procedures.sql, 03_triggers.sql, 04_alter_foto.sql
-- =====================================================================

USE projeto_unb;

-- Força UTF-8 na sessão, independente do codepage do cliente
-- (evita corrupção de acentos em clientes Windows com console cp850)
SET NAMES utf8mb4;

SET FOREIGN_KEY_CHECKS = 0;

-- =====================================================================
-- 1. DEPARTAMENTO
-- =====================================================================
INSERT INTO departamento (id, nome) VALUES
(1, 'Departamento de Ciência da Computação'),
(2, 'Departamento de Matemática'),
(3, 'Departamento de Engenharia Elétrica'),
(4, 'Departamento de Física'),
(5, 'Departamento de Estatística');

-- =====================================================================
-- 2. PESSOA (10 registros — 5 alunos + 5 professores)
-- =====================================================================
INSERT INTO pessoa (id, nome, cpf, sexo, data_nascimento) VALUES
(1,  'Ana Luiza Ferreira',     '11122233344', 'F', '2002-03-15'),
(2,  'Bruno Carvalho Santos',  '22233344455', 'M', '2001-07-22'),
(3,  'Carla Menezes Lima',     '33344455566', 'F', '2003-01-10'),
(4,  'Diego Alves Pereira',    '44455566677', 'M', '2002-11-05'),
(5,  'Eduarda Rocha Costa',    '55566677788', 'F', '2001-09-30'),
(6,  'Fernando Díbio',         '66677788899', 'M', '1975-04-18'),
(7,  'Gisele Monteiro',        '77788899900', 'F', '1980-12-03'),
(8,  'Hélio Tavares',          '88899900011', 'M', '1972-06-25'),
(9,  'Ingrid Nunes',           '99900011122', 'F', '1985-02-14'),
(10, 'João Fagundes',          '00011122233', 'M', '1968-08-09');

-- =====================================================================
-- 3. CURSO
-- =====================================================================
INSERT INTO curso (id, nome, sigla) VALUES
(1, 'Bacharelado em Ciência da Computação',  'BCC'),
(2, 'Bacharelado em Engenharia de Software', 'BES'),
(3, 'Licenciatura em Computação',            'LCC'),
(4, 'Bacharelado em Matemática',             'BMA'),
(5, 'Bacharelado em Estatística',            'BST');

-- =====================================================================
-- 4. SEMESTRE
-- =====================================================================
INSERT INTO semestre (id, nome, data_inicio, data_fim) VALUES
(1, '2024/1', '2024-03-18', '2024-07-20'),
(2, '2024/2', '2024-09-02', '2025-01-25'),
(3, '2025/1', '2025-03-17', '2025-07-19'),
(4, '2025/2', '2025-09-01', '2026-01-24'),
(5, '2026/1', '2026-03-16', '2026-07-18');

-- =====================================================================
-- 5. DISCIPLINA
-- =====================================================================
INSERT INTO disciplina (id, codigo, nome) VALUES
(1,  'CIC0004', 'Algoritmos e Programação de Computadores'),
(2,  'CIC0090', 'Banco de Dados'),
(3,  'CIC0097', 'Estruturas de Dados'),
(4,  'CIC0100', 'Grafos e Combinatória'),
(5,  'CIC0105', 'Redes de Computadores'),
(6,  'CIC0110', 'Inteligência Artificial'),
(7,  'CIC0130', 'Paradigmas de Linguagens de Programação'),
(8,  'MAT0025', 'Cálculo 1'),
(9,  'MAT0027', 'Álgebra Linear'),
(10, 'EST0001', 'Probabilidade e Estatística');

-- =====================================================================
-- 6. NOTIFICACAO
-- =====================================================================
INSERT INTO notificacao (id, titulo, descricao, tipo, mensagem) VALUES
(1, 'Bem-vindo ao Sistema',        'Notificação de boas-vindas',    'INFO',    'Seu cadastro foi realizado. Boas-vindas ao sistema acadêmico da UnB!'),
(2, 'Matrícula Confirmada',        'Confirmação de matrícula',      'SUCESSO', 'Sua matrícula na disciplina foi confirmada. Confira os detalhes no portal.'),
(3, 'Avaliação Agendada',          'Lembrete de avaliação próxima', 'ALERTA',  'Você tem uma avaliação nos próximos 7 dias. Prepare-se!'),
(4, 'Nota Lançada',                'Resultado disponível',          'INFO',    'Uma nova nota foi lançada em sua disciplina. Acesse o portal para visualizar.'),
(5, 'Frequência Abaixo do Mínimo', 'Alerta de frequência',          'ALERTA',  'Sua frequência está abaixo de 75% em uma ou mais disciplinas. Atenção!');

-- =====================================================================
-- 7. ALUNO (especialização de pessoa — ids 1 a 5)
-- =====================================================================
INSERT INTO aluno (id_pessoa, tipo) VALUES
(1, 'GRADUACAO'),
(2, 'GRADUACAO'),
(3, 'GRADUACAO'),
(4, 'POS_GRADUACAO'),
(5, 'GRADUACAO');

-- =====================================================================
-- 8. PROFESSOR (especialização de pessoa — ids 6 a 10)
-- =====================================================================
INSERT INTO professor (id_pessoa, id_departamento, tipo, nivel) VALUES
(6,  1, 'EFETIVO',    'ASSOCIADO'),
(7,  2, 'EFETIVO',    'ADJUNTO'),
(8,  3, 'COLABORADOR','ASSISTENTE'),
(9,  1, 'EFETIVO',    'ADJUNTO'),
(10, 1, 'EFETIVO',    'TITULAR');

-- =====================================================================
-- 9. CONTA (1 por pessoa)
-- =====================================================================
INSERT INTO conta (id, id_pessoa, email, senha, tipo, status) VALUES
(1,  1,  'ana.ferreira@aluno.unb.br',   '$2b$12$placeholderHashAluno1xxxx', 'ALUNO',     'ATIVA'),
(2,  2,  'bruno.santos@aluno.unb.br',   '$2b$12$placeholderHashAluno2xxxx', 'ALUNO',     'ATIVA'),
(3,  3,  'carla.lima@aluno.unb.br',     '$2b$12$placeholderHashAluno3xxxx', 'ALUNO',     'ATIVA'),
(4,  4,  'diego.pereira@aluno.unb.br',  '$2b$12$placeholderHashAluno4xxxx', 'ALUNO',     'ATIVA'),
(5,  5,  'eduarda.costa@aluno.unb.br',  '$2b$12$placeholderHashAluno5xxxx', 'ALUNO',     'ATIVA'),
(6,  6,  'fernando.dibio@unb.br',       '$2b$12$placeholderHashProf6xxxxx', 'PROFESSOR', 'ATIVA'),
(7,  7,  'gisele.monteiro@unb.br',      '$2b$12$placeholderHashProf7xxxxx', 'PROFESSOR', 'ATIVA'),
(8,  8,  'helio.tavares@unb.br',        '$2b$12$placeholderHashProf8xxxxx', 'PROFESSOR', 'ATIVA'),
(9,  9,  'ingrid.nunes@unb.br',         '$2b$12$placeholderHashProf9xxxxx', 'PROFESSOR', 'ATIVA'),
(10, 10, 'joao.fagundes@unb.br',        '$2b$12$placeholderHashProf10xxxx', 'PROFESSOR', 'ATIVA');

-- =====================================================================
-- 10. PREDIO
-- =====================================================================
INSERT INTO predio (id, id_departamento, nome, bairro, cidade, estado, cep) VALUES
(1, 1, 'CIC/EST — Bloco A', 'Asa Norte', 'Brasília', 'DF', '70910-900'),
(2, 1, 'CIC/EST — Bloco B', 'Asa Norte', 'Brasília', 'DF', '70910-900'),
(3, 2, 'MAT — Bloco A',     'Asa Norte', 'Brasília', 'DF', '70910-900'),
(4, 3, 'ENE — Bloco A',     'Asa Norte', 'Brasília', 'DF', '70910-900'),
(5, 4, 'FIS — Bloco A',     'Asa Norte', 'Brasília', 'DF', '70910-900');

-- =====================================================================
-- 11. SALA
-- =====================================================================
INSERT INTO sala (id, id_predio, codigo, capacidade) VALUES
(1, 1, 'CIC-I-01',  40),
(2, 1, 'CIC-I-02',  40),
(3, 2, 'CIC-II-01', 30),
(4, 3, 'MAT-01',    50),
(5, 4, 'ENE-01',    35);

-- =====================================================================
-- 12. MATRICULA_CURSO (1 por aluno)
-- =====================================================================
INSERT INTO matricula_curso (id, id_aluno, id_curso, codigo, data_matricula_curso, status) VALUES
(1, 1, 1, '20/0001234', '2020-03-18', 'ATIVA'),
(2, 2, 1, '21/0002345', '2021-03-18', 'ATIVA'),
(3, 3, 1, '22/0003456', '2022-03-18', 'ATIVA'),
(4, 4, 2, '21/0004567', '2021-03-18', 'ATIVA'),
(5, 5, 1, '22/0005678', '2022-03-18', 'ATIVA');

-- =====================================================================
-- 13. OFERTA (disciplinas ofertadas no semestre 2026/1 para BCC)
-- =====================================================================
INSERT INTO oferta (id, id_departamento, id_disciplina, id_curso, id_semestre, codigo_oferta) VALUES
(1, 1, 2, 1, 5, '2026/1-CIC0090-BCC'),
(2, 1, 3, 1, 5, '2026/1-CIC0097-BCC'),
(3, 1, 4, 1, 5, '2026/1-CIC0100-BCC'),
(4, 1, 5, 1, 5, '2026/1-CIC0105-BCC'),
(5, 1, 6, 1, 5, '2026/1-CIC0110-BCC');

-- =====================================================================
-- 14. TURMA
-- =====================================================================
INSERT INTO turma (id, id_oferta, codigo, quantidade_vagas) VALUES
(1, 1, 'BD-T01', 40),
(2, 2, 'ED-T01', 40),
(3, 3, 'GR-T01', 30),
(4, 4, 'RC-T01', 35),
(5, 5, 'IA-T01', 35);

-- =====================================================================
-- 15. PROFESSOR_TURMA
-- =====================================================================
INSERT INTO professor_turma (id, id_professor, id_turma, funcao, carga_horaria, data_inicio, data_fim) VALUES
(1, 6,  1, 'TITULAR', 60, '2026-03-16', '2026-07-18'),
(2, 9,  2, 'TITULAR', 60, '2026-03-16', '2026-07-18'),
(3, 10, 3, 'TITULAR', 60, '2026-03-16', '2026-07-18'),
(4, 8,  4, 'TITULAR', 60, '2026-03-16', '2026-07-18'),
(5, 7,  5, 'TITULAR', 60, '2026-03-16', '2026-07-18');

-- =====================================================================
-- 16. MATRICULA_DISCIPLINA
-- nota começa NULL — o trigger a preencherá ao inserir resultado_avaliacao
-- =====================================================================
INSERT INTO matricula_disciplina (id, id_matricula_curso, id_turma, codigo, data_matricula_disciplina, status) VALUES
(1, 1, 1, 'MD-1-1', '2026-03-20', 'MATRICULADO'),
(2, 2, 2, 'MD-2-2', '2026-03-20', 'MATRICULADO'),
(3, 3, 3, 'MD-3-3', '2026-03-20', 'MATRICULADO'),
(4, 4, 4, 'MD-4-4', '2026-03-20', 'MATRICULADO'),
(5, 5, 5, 'MD-5-5', '2026-03-20', 'MATRICULADO');

-- =====================================================================
-- 17. AULA
-- =====================================================================
INSERT INTO aula (id, id_turma, data, tipo, conteudo) VALUES
(1, 1, '2026-03-18', 'TEORICA', 'Introdução a Banco de Dados e Modelo Relacional'),
(2, 1, '2026-03-20', 'TEORICA', 'Modelo Entidade-Relacionamento'),
(3, 2, '2026-03-18', 'PRATICA', 'Revisão de Ponteiros e Alocação Dinâmica'),
(4, 3, '2026-03-19', 'TEORICA', 'Conceitos de Grafos e Representações'),
(5, 4, '2026-03-18', 'TEORICA', 'Introdução a Redes: Modelo OSI e TCP/IP');

-- =====================================================================
-- 18. AVALIACAO
-- =====================================================================
INSERT INTO avaliacao (id, id_turma, titulo, descricao, tipo, peso, nota_maxima, data_aplicacao, status) VALUES
(1, 1, 'Prova 1 — Modelo Relacional',      'Conteúdo: MER e normalização',          'PROVA',    3.00, 10.00, '2026-04-20', 'PLANEJADA'),
(2, 1, 'Trabalho Prático — SQL',            'Implementação de schema + queries',     'TRABALHO', 3.00, 10.00, '2026-05-10', 'PLANEJADA'),
(3, 2, 'Prova 1 — Estruturas Lineares',     'Conteúdo: listas, pilhas, filas',       'PROVA',    4.00, 10.00, '2026-04-25', 'PLANEJADA'),
(4, 3, 'Prova 1 — Teoria de Grafos',        'Conteúdo: terminologia e BFS/DFS',      'PROVA',    5.00, 10.00, '2026-04-22', 'PLANEJADA'),
(5, 4, 'Prova 1 — Camada Física e Enlace',  'Conteúdo: OSI, TCP/IP, enlace',         'PROVA',    4.00, 10.00, '2026-04-21', 'PLANEJADA');

-- =====================================================================
-- 19. RESULTADO_AVALIACAO
-- Estes INSERTs disparam tg_atualiza_nota_final_insert,
-- que recalcula e grava nota em matricula_disciplina automaticamente.
-- =====================================================================
INSERT INTO resultado_avaliacao (id, id_avaliacao, id_matricula_disciplina, nota, feedback, status, data_entrega) VALUES
(1, 1, 1, 8.50, 'Boa compreensão do MER. Atenção à normalização na 3FN.',        'CORRIGIDO', '2026-04-22'),
(2, 2, 1, 9.00, 'Excelente implementação SQL. Queries bem otimizadas.',           'CORRIGIDO', '2026-05-12'),
(3, 3, 2, 7.00, 'Demonstrou domínio de listas ligadas. Rever árvores binárias.', 'CORRIGIDO', '2026-04-27'),
(4, 4, 3, 9.50, 'Excelente! Resolveu BFS e DFS corretamente.',                   'CORRIGIDO', '2026-04-24'),
(5, 5, 4, 6.50, 'Compreendeu o modelo OSI. Reforçar a camada de enlace.',        'CORRIGIDO', '2026-04-23');

-- =====================================================================
-- 20. FREQUENCIA
-- =====================================================================
INSERT INTO frequencia (id, id_aula, id_matricula_disciplina, presente, data_registro) VALUES
(1, 1, 1, TRUE,  '2026-03-18'),
(2, 2, 1, TRUE,  '2026-03-20'),
(3, 3, 2, TRUE,  '2026-03-18'),
(4, 4, 3, TRUE,  '2026-03-19'),
(5, 5, 4, FALSE, '2026-03-18');

-- =====================================================================
-- 21. EVENTO
-- =====================================================================
INSERT INTO evento (id, id_turma, titulo, descricao, tipo, data_inicio, data_fim, local) VALUES
(1, 1, 'Palestra: NoSQL vs SQL',           'Debate sobre paradigmas de BD',           'PALESTRA',  '2026-04-10 14:00:00', '2026-04-10 16:00:00', 'Auditório CIC'),
(2, 2, 'Maratona de Programação — Treino', 'Treino para o ICPC',                      'WORKSHOP',  '2026-04-15 08:00:00', '2026-04-15 18:00:00', 'Laboratório CIC-I-02'),
(3, 3, 'Seminário: Aplicações de Grafos',  'Apresentações de trabalhos dos alunos',   'SEMINARIO', '2026-05-05 10:00:00', '2026-05-05 12:00:00', 'CIC-I-01'),
(4, 4, 'Visita Técnica: Data Center UnB',  'Tour pelo data center da universidade',   'VISITA',    '2026-04-28 09:00:00', '2026-04-28 11:00:00', 'CPD UnB'),
(5, 5, 'Hackathon IA — Problema Real UnB', 'Desenvolvimento de solução com ML',       'HACKATHON', '2026-05-20 08:00:00', '2026-05-21 18:00:00', 'Auditório CIC');

-- =====================================================================
-- 22. MATERIAL_DE_ESTUDO
-- =====================================================================
INSERT INTO material_de_estudo (id, id_disciplina, titulo, descricao, tipo, link) VALUES
(1, 2, 'Slides: Modelo Relacional',         'Apresentação das aulas 1–3 de BD',     'SLIDE', 'https://moodle.unb.br/bd/slides-mr'),
(2, 2, 'Livro: Database System Concepts',   'Silberschatz, Korth & Sudarshan',      'LIVRO', 'https://db-book.com'),
(3, 3, 'Apostila: Estruturas de Dados',     'Material elaborado pelo professor',    'PDF',   'https://moodle.unb.br/ed/apostila'),
(4, 4, 'Slides: Grafos — Aulas 1–7',        'Revisão completa para a prova',        'SLIDE', 'https://moodle.unb.br/grafos/slides'),
(5, 6, 'Playlist: IA e Aprendizado de Máq.','Série de vídeos introdutórios',        'VIDEO', 'https://youtube.com/playlist?list=exemplo');

-- =====================================================================
-- 23. META_DE_ESTUDO
-- =====================================================================
INSERT INTO meta_de_estudo (id, id_aluno, titulo, horas, prazo, status) VALUES
(1, 1, 'Estudar SQL para a Prova 1',             20, '2026-04-19', 'EM_ANDAMENTO'),
(2, 2, 'Revisar Listas, Pilhas e Filas',         15, '2026-04-24', 'EM_ANDAMENTO'),
(3, 3, 'Completar lista de exercícios de Grafos', 25, '2026-04-21', 'CONCLUIDA'),
(4, 4, 'Estudar protocolo TCP/IP',               10, '2026-04-20', 'EM_ANDAMENTO'),
(5, 5, 'Implementar perceptron em Python',        30, '2026-05-19', 'EM_ANDAMENTO');

-- =====================================================================
-- 24. NOTIFICACAO_CONTA
-- =====================================================================
INSERT INTO notificacao_conta (id, id_conta, id_notificacao, data_envio, data_recebimento, lida) VALUES
(1, 1, 1, '2026-03-20 10:00:00', '2026-03-20 10:05:00', TRUE),
(2, 2, 1, '2026-03-20 10:00:00', '2026-03-20 10:10:00', TRUE),
(3, 1, 2, '2026-03-21 08:00:00', '2026-03-21 08:30:00', TRUE),
(4, 1, 4, '2026-04-23 09:00:00', NULL,                  FALSE),
(5, 2, 3, '2026-04-18 07:00:00', '2026-04-18 07:15:00', TRUE);

-- =====================================================================
-- 25. ALOCACAO_SALA
-- =====================================================================
INSERT INTO alocacao_sala (id, id_turma, id_sala, dia_semana, hora_abertura, hora_fechamento, status) VALUES
(1, 1, 1, 'TER', '10:00:00', '11:50:00', TRUE),
(2, 1, 1, 'QUI', '10:00:00', '11:50:00', TRUE),
(3, 2, 2, 'SEG', '08:00:00', '09:50:00', TRUE),
(4, 3, 3, 'QUA', '14:00:00', '15:50:00', TRUE),
(5, 4, 5, 'TER', '16:00:00', '17:50:00', TRUE);

SET FOREIGN_KEY_CHECKS = 1;
