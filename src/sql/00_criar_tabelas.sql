-- =====================================================================
-- PROJETO DE BANCO DE DADOS - UnB
-- Disciplina: Banco de Dados
-- Sistema Acadêmico Integrado
-- =====================================================================


DROP DATABASE IF EXISTS projeto_unb;
CREATE DATABASE projeto_unb
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;
USE projeto_unb;

-- Força UTF-8 na sessão, independente do codepage do cliente
-- (evita corrupção de acentos em clientes Windows com console cp850)
SET NAMES utf8mb4;

-- =====================================================================
-- 1. ENTIDADES BASE (sem FKs)
-- =====================================================================

-- PESSOA -------------------------------------------------------------
CREATE TABLE pessoa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    sexo CHAR(1),
    data_nascimento DATE NOT NULL
);

-- DEPARTAMENTO -------------------------------------------------------
CREATE TABLE departamento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL UNIQUE
);

-- CURSO --------------------------------------------------------------
CREATE TABLE curso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    sigla VARCHAR(10) NOT NULL UNIQUE
);

-- SEMESTRE -----------------------------------------------------------
CREATE TABLE semestre (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(20) NOT NULL UNIQUE,  -- ex: "2026/1"
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL
);

-- DISCIPLINA ---------------------------------------------------------
-- Disciplina não tem mais vínculo direto com curso (vai via OFERTA).
CREATE TABLE disciplina (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    nome VARCHAR(150) NOT NULL
);

-- NOTIFICACAO --------------------------------------------------------
-- Template/conteúdo da notificação (envio fica em notificacao_conta).
CREATE TABLE notificacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(150) NOT NULL,
    descricao TEXT,
    tipo VARCHAR(50) NOT NULL,
    mensagem TEXT NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================================
-- 2. ESPECIALIZAÇÕES DE PESSOA
-- =====================================================================

-- ALUNO --------------------------------------------------------------
CREATE TABLE aluno (
    id_pessoa INT PRIMARY KEY,
    tipo ENUM('GRADUACAO', 'POS_GRADUACAO', 'EXTENSAO') NOT NULL DEFAULT 'GRADUACAO',
    FOREIGN KEY (id_pessoa) REFERENCES pessoa(id) ON DELETE CASCADE
);

-- PROFESSOR ----------------------------------------------------------
CREATE TABLE professor (
    id_pessoa INT PRIMARY KEY,
    id_departamento INT NOT NULL,
    tipo ENUM('EFETIVO', 'SUBSTITUTO', 'VISITANTE', 'COLABORADOR') NOT NULL DEFAULT 'EFETIVO',
    nivel ENUM('AUXILIAR', 'ASSISTENTE', 'ADJUNTO', 'ASSOCIADO', 'TITULAR') NOT NULL DEFAULT 'ADJUNTO',
    FOREIGN KEY (id_pessoa) REFERENCES pessoa(id) ON DELETE CASCADE,
    FOREIGN KEY (id_departamento) REFERENCES departamento(id)
);

-- CONTA --------------------------------------------------------------
CREATE TABLE conta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_pessoa INT NOT NULL UNIQUE,
    email VARCHAR(150) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo ENUM('ALUNO', 'PROFESSOR', 'ADMIN') NOT NULL,
    data_criacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('ATIVA', 'INATIVA', 'SUSPENSA') NOT NULL DEFAULT 'ATIVA',
    FOREIGN KEY (id_pessoa) REFERENCES pessoa(id) ON DELETE CASCADE
);

-- =====================================================================
-- 3. INFRAESTRUTURA FÍSICA
-- =====================================================================

-- PREDIO -------------------------------------------------------------
CREATE TABLE predio (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_departamento INT NOT NULL,
    nome VARCHAR(100) NOT NULL,
    rua VARCHAR(100),
    numero INT,
    conjunto VARCHAR(20),
    ql VARCHAR(20),
    quadra VARCHAR(20),
    bairro VARCHAR(100),
    cidade VARCHAR(100),
    estado CHAR(2),
    cep varchar(15),
    FOREIGN KEY (id_departamento) REFERENCES departamento(id)
);

-- SALA ---------------------------------------------------------------
CREATE TABLE sala (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_predio INT NOT NULL,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    capacidade INT NOT NULL,
    FOREIGN KEY (id_predio) REFERENCES predio(id) ON DELETE CASCADE
);

-- =====================================================================
-- 4. MATRÍCULAS E OFERTA ACADÊMICA
-- =====================================================================

-- MATRICULA_CURSO ----------------------------------------------------
-- Vínculo do aluno com um curso específico.
CREATE TABLE matricula_curso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_aluno INT NOT NULL,
    id_curso INT NOT NULL,
    codigo VARCHAR(20) UNIQUE NOT NULL,  -- número de matrícula UnB
    data_matricula_curso DATE NOT NULL,
    data_trancamento_curso DATE,
    status ENUM('ATIVA', 'TRANCADA', 'CONCLUIDA', 'CANCELADA') NOT NULL DEFAULT 'ATIVA',
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_pessoa) ON DELETE CASCADE,
    FOREIGN KEY (id_curso) REFERENCES curso(id)
);

-- OFERTA -------------------------------------------------------------
-- Disciplina ofertada num semestre por um departamento, para um curso.
CREATE TABLE oferta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_departamento INT NOT NULL,
    id_disciplina INT NOT NULL,
    id_curso INT NOT NULL,
    id_semestre INT NOT NULL,
    codigo_oferta VARCHAR(30) UNIQUE NOT NULL,
    FOREIGN KEY (id_departamento) REFERENCES departamento(id),
    FOREIGN KEY (id_disciplina) REFERENCES disciplina(id),
    FOREIGN KEY (id_curso) REFERENCES curso(id),
    FOREIGN KEY (id_semestre) REFERENCES semestre(id)
);

-- TURMA --------------------------------------------------------------
-- Cada oferta gera uma ou mais turmas.
CREATE TABLE turma (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_oferta INT NOT NULL,
    codigo VARCHAR(20) UNIQUE NOT NULL,
    quantidade_vagas INT NOT NULL,
    FOREIGN KEY (id_oferta) REFERENCES oferta(id) ON DELETE CASCADE
);

-- PROFESSOR_DISCIPLINA -----------------------------------------------
-- Liga professor à disciplina (relação 'ministra' do DER conceitual).
CREATE TABLE professor_turma (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_professor INT NOT NULL,
    id_turma INT NOT NULL,
    funcao ENUM('TITULAR', 'CO_RESPONSAVEL', 'MONITOR') NOT NULL DEFAULT 'TITULAR',
    carga_horaria INT,
    data_inicio DATE,
    data_fim DATE,
    FOREIGN KEY (id_professor) REFERENCES professor(id_pessoa),
    FOREIGN KEY (id_turma) REFERENCES turma(id) ON DELETE CASCADE
);

-- MATRICULA_DISCIPLINA -----------------------------------------------
-- Liga a matrícula no curso à turma específica que o aluno vai cursar.
CREATE TABLE matricula_disciplina (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_matricula_curso INT NOT NULL,
    id_turma INT NOT NULL,
    codigo VARCHAR(30) NOT NULL,
    data_matricula_disciplina DATE NOT NULL,
    data_trancamento_disciplina DATE,
    nota DECIMAL(5,2),  -- nota final consolidada
    status ENUM('MATRICULADO', 'APROVADO', 'REPROVADO', 'TRANCADO') NOT NULL DEFAULT 'MATRICULADO',
    FOREIGN KEY (id_matricula_curso) REFERENCES matricula_curso(id) ON DELETE CASCADE,
    FOREIGN KEY (id_turma) REFERENCES turma(id) ON DELETE CASCADE
);

-- =====================================================================
-- 5. AULAS, AVALIAÇÕES E FREQUÊNCIA
-- =====================================================================

-- AULA ---------------------------------------------------------------
CREATE TABLE aula (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_turma INT NOT NULL,
    data DATE NOT NULL,
    tipo VARCHAR(50),
    conteudo TEXT,
    FOREIGN KEY (id_turma) REFERENCES turma(id) ON DELETE CASCADE
);

-- AVALIACAO ----------------------------------------------------------
CREATE TABLE avaliacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_turma INT NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    descricao TEXT,
    tipo VARCHAR(50),
    peso DECIMAL(4,2),
    nota_maxima DECIMAL(5,2),
    data_aplicacao DATE,
    prazo DATE,
    status ENUM('PLANEJADA', 'APLICADA', 'CORRIGIDA', 'CANCELADA') NOT NULL DEFAULT 'PLANEJADA',
    FOREIGN KEY (id_turma) REFERENCES turma(id) ON DELETE CASCADE
);

-- RESULTADO_AVALIACAO ------------------------------------------------
CREATE TABLE resultado_avaliacao (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_avaliacao INT NOT NULL,
    id_matricula_disciplina INT NOT NULL,
    nota DECIMAL(5,2),
    feedback TEXT,
    status ENUM('PENDENTE', 'ENTREGUE', 'CORRIGIDO', 'NAO_ENTREGUE') NOT NULL DEFAULT 'PENDENTE',
    data_entrega DATE,
    FOREIGN KEY (id_avaliacao) REFERENCES avaliacao(id) ON DELETE CASCADE,
    FOREIGN KEY (id_matricula_disciplina) REFERENCES matricula_disciplina(id) ON DELETE CASCADE
);

-- FREQUENCIA ---------------------------------------------------------
CREATE TABLE frequencia (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_aula INT NOT NULL,
    id_matricula_disciplina INT NOT NULL,
    presente BOOLEAN NOT NULL,
    data_registro DATE,
    observacao TEXT,
    FOREIGN KEY (id_aula) REFERENCES aula(id) ON DELETE CASCADE,
    FOREIGN KEY (id_matricula_disciplina) REFERENCES matricula_disciplina(id) ON DELETE CASCADE
);

-- =====================================================================
-- 6. EVENTOS, MATERIAIS E METAS
-- =====================================================================

-- EVENTO -------------------------------------------------------------
CREATE TABLE evento (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_turma INT NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    descricao TEXT,
    tipo VARCHAR(50),
    data_inicio DATETIME,
    data_fim DATETIME,
    local VARCHAR(100),
    FOREIGN KEY (id_turma) REFERENCES turma(id) ON DELETE CASCADE
);

-- MATERIAL_DE_ESTUDO -------------------------------------------------
CREATE TABLE material_de_estudo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_disciplina INT NOT NULL,
    titulo VARCHAR(100) NOT NULL,
    descricao TEXT,
    tipo VARCHAR(50),
    link TEXT,
    FOREIGN KEY (id_disciplina) REFERENCES disciplina(id) ON DELETE CASCADE
);

-- META_DE_ESTUDO -----------------------------------------------------
CREATE TABLE meta_de_estudo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_aluno INT NOT NULL,
    titulo VARCHAR(100),
    horas INT NOT NULL,
    prazo DATE,
    status ENUM('EM_ANDAMENTO', 'CONCLUIDA', 'ATRASADA', 'CANCELADA') NOT NULL DEFAULT 'EM_ANDAMENTO',
    FOREIGN KEY (id_aluno) REFERENCES aluno(id_pessoa) ON DELETE CASCADE
);

-- =====================================================================
-- 7. NOTIFICAÇÕES
-- =====================================================================

-- NOTIFICACAO_CONTA --------------------------------------------------
-- Cada envio de uma notificação para uma conta específica.
CREATE TABLE notificacao_conta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_conta INT NOT NULL,
    id_notificacao INT NOT NULL,
    data_envio DATETIME DEFAULT CURRENT_TIMESTAMP,
    data_recebimento DATETIME,
    lida BOOLEAN DEFAULT FALSE,
    mensagem_resposta TEXT,
    FOREIGN KEY (id_conta) REFERENCES conta(id) ON DELETE CASCADE,
    FOREIGN KEY (id_notificacao) REFERENCES notificacao(id) ON DELETE CASCADE
);

-- =====================================================================
-- 8. ALOCAÇÃO DE SALAS
-- =====================================================================

-- ALOCACAO_SALA ------------------------------------------------------
-- Referenciada nos relacionamentos do DER (Sala RECEBE / Turma OCUPA).
-- A entidade ainda precisa ser declarada no PUML para alinhamento total.
CREATE TABLE alocacao_sala (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_turma INT NOT NULL,
    id_sala INT NOT NULL,
    dia_semana ENUM('SEG', 'TER', 'QUA', 'QUI', 'SEX', 'SAB') NOT NULL,
    hora_abertura TIME NOT NULL,
    hora_fechamento TIME NOT NULL,
    status BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (id_turma) REFERENCES turma(id) ON DELETE CASCADE,
    FOREIGN KEY (id_sala) REFERENCES sala(id) ON DELETE CASCADE
);

-- =====================================================================
-- ÍNDICES AUXILIARES (performance em buscas comuns)
-- =====================================================================

CREATE INDEX idx_pessoa_nome ON pessoa(nome);
CREATE INDEX idx_conta_email ON conta(email);
CREATE INDEX idx_matricula_curso_codigo ON matricula_curso(codigo);
CREATE INDEX idx_oferta_codigo ON oferta(codigo_oferta);
CREATE INDEX idx_aula_data ON aula(data);

