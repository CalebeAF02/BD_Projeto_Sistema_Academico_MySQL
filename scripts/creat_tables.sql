CREATE DATABASE projeto_unb;
USE projeto_unb;

-- =====================================================
-- PESSOA
-- =====================================================

CREATE TABLE pessoa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    cpf VARCHAR(11) UNIQUE NOT NULL,
    sexo CHAR(1),
    data_nascimento DATE NOT NULL
);

-- =====================================================
-- CURSO
-- =====================================================

CREATE TABLE curso (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    sigla VARCHAR(10) NOT NULL UNIQUE
);

-- =====================================================
-- ALUNO
-- =====================================================

CREATE TABLE aluno (
    id INT PRIMARY KEY,
    matricula VARCHAR(20) UNIQUE NOT NULL,
    curso_id INT NOT NULL,

    FOREIGN KEY (id)
        REFERENCES pessoa(id)
        ON DELETE CASCADE,

    FOREIGN KEY (curso_id)
        REFERENCES curso(id)
);
    
-- =====================================================
-- PROFESSOR
-- =====================================================

CREATE TABLE professor (
    id INT PRIMARY KEY,

    FOREIGN KEY (id)
        REFERENCES pessoa(id)
        ON DELETE CASCADE
);

-- =====================================================
-- CONTA
-- =====================================================

CREATE TABLE conta (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    tipo ENUM('ALUNO','PROFESSOR') NOT NULL,
    pessoa_id INT NOT NULL UNIQUE,

    FOREIGN KEY (pessoa_id)
        REFERENCES pessoa(id)
        ON DELETE CASCADE
);

-- =====================================================
-- DISCIPLINA
-- =====================================================

CREATE TABLE disciplina (
    id INT AUTO_INCREMENT PRIMARY KEY,
    curso_id INT NOT NULL,

    codigo VARCHAR(20) UNIQUE NOT NULL,
    nome VARCHAR(100) NOT NULL,

    FOREIGN KEY (curso_id)
        REFERENCES curso(id)
);
    
-- =====================================================
-- PROFESSOR_DISCIPLINA
-- =====================================================

CREATE TABLE professor_disciplina (
    id INT AUTO_INCREMENT PRIMARY KEY,

    professor_id INT NOT NULL,
    disciplina_id INT NOT NULL,

    semestre VARCHAR(10),
    carga_horaria INT,

    data_inicio DATE,
    data_fim DATE,

    FOREIGN KEY (professor_id)
        REFERENCES professor(id),

    FOREIGN KEY (disciplina_id)
        REFERENCES disciplina(id)
);

-- =====================================================
-- TURMA
-- =====================================================

CREATE TABLE turma (
    id INT AUTO_INCREMENT PRIMARY KEY,

    disciplina_id INT NOT NULL,
    professor_id INT NOT NULL,

    quantidade_vagas INT NOT NULL,

    FOREIGN KEY (disciplina_id)
        REFERENCES disciplina(id),

    FOREIGN KEY (professor_id)
        REFERENCES professor(id)
);

-- =====================================================
-- MATRICULA_DISCIPLINA
-- =====================================================

CREATE TABLE matricula_disciplina (
    id INT AUTO_INCREMENT PRIMARY KEY,

    aluno_id INT NOT NULL,
    turma_id INT NOT NULL,

    data_matricula DATE NOT NULL,

    status VARCHAR(30)
        DEFAULT 'Matriculado',

    FOREIGN KEY (aluno_id)
        REFERENCES aluno(id)
        ON DELETE CASCADE,

    FOREIGN KEY (turma_id)
        REFERENCES turma(id)
        ON DELETE CASCADE
);

-- =====================================================
-- AVALIACAO
-- =====================================================

CREATE TABLE avaliacao (
    id INT AUTO_INCREMENT PRIMARY KEY,

    turma_id INT NOT NULL,

    titulo VARCHAR(100) NOT NULL,
    descricao TEXT,

    tipo VARCHAR(50),

    peso DECIMAL(4,2),
    nota_maxima DECIMAL(5,2),

    data_aplicacao DATE,
    prazo DATE,

    FOREIGN KEY (turma_id)
        REFERENCES turma(id)
        ON DELETE CASCADE
);

-- =====================================================
-- RESULTADO_AVALIACAO
-- =====================================================

CREATE TABLE resultado_avaliacao (
    id INT AUTO_INCREMENT PRIMARY KEY,

    avaliacao_id INT NOT NULL,
    matricula_disciplina_id INT NOT NULL,

    nota DECIMAL(5,2),

    feedback TEXT,

    status VARCHAR(30),

    data_entrega DATE,

    FOREIGN KEY (avaliacao_id)
        REFERENCES avaliacao(id)
        ON DELETE CASCADE,

    FOREIGN KEY (matricula_disciplina_id)
        REFERENCES matricula_disciplina(id)
        ON DELETE CASCADE
);

-- =====================================================
-- AULA
-- =====================================================

CREATE TABLE aula (
    id INT AUTO_INCREMENT PRIMARY KEY,

    turma_id INT NOT NULL,

    data DATE NOT NULL,

    tipo VARCHAR(50),

    conteudo TEXT,

    FOREIGN KEY (turma_id)
        REFERENCES turma(id)
        ON DELETE CASCADE
);

-- =====================================================
-- FREQUENCIA
-- =====================================================

CREATE TABLE frequencia (
    id INT AUTO_INCREMENT PRIMARY KEY,

    aula_id INT NOT NULL,
    matricula_disciplina_id INT NOT NULL,

    presente BOOLEAN NOT NULL,

    data_registro DATE,

    observacao TEXT,

    FOREIGN KEY (aula_id)
        REFERENCES aula(id)
        ON DELETE CASCADE,

    FOREIGN KEY (matricula_disciplina_id)
        REFERENCES matricula_disciplina(id)
        ON DELETE CASCADE
);

-- =====================================================
-- EVENTO
-- =====================================================

CREATE TABLE evento (
    id INT AUTO_INCREMENT PRIMARY KEY,

    turma_id INT NOT NULL,

    titulo VARCHAR(100) NOT NULL,

    descricao TEXT,

    tipo VARCHAR(50),

    data_inicio DATETIME,
    data_fim DATETIME,

    local VARCHAR(100),

    FOREIGN KEY (turma_id)
        REFERENCES turma(id)
        ON DELETE CASCADE
);

-- =====================================================
-- MATERIAL DE ESTUDO
-- =====================================================

CREATE TABLE material_estudo (
    id INT AUTO_INCREMENT PRIMARY KEY,

    disciplina_id INT NOT NULL,

    titulo VARCHAR(100) NOT NULL,

    descricao TEXT,

    tipo VARCHAR(50),

    link TEXT,

    FOREIGN KEY (disciplina_id)
        REFERENCES disciplina(id)
        ON DELETE CASCADE
);

-- =====================================================
-- META DE ESTUDO
-- =====================================================

CREATE TABLE meta_estudo (
    id INT AUTO_INCREMENT PRIMARY KEY,

    aluno_id INT NOT NULL,

    titulo VARCHAR(100),

    horas INT NOT NULL,

    prazo DATE,

    FOREIGN KEY (aluno_id)
        REFERENCES aluno(id)
        ON DELETE CASCADE
);

-- =====================================================
-- NOTIFICACAO
-- =====================================================

CREATE TABLE notificacao (
    id INT AUTO_INCREMENT PRIMARY KEY,

    conta_id INT NOT NULL,

    tipo VARCHAR(50),

    mensagem TEXT NOT NULL,

    data_envio DATETIME,

    lida BOOLEAN DEFAULT FALSE,

    FOREIGN KEY (conta_id)
        REFERENCES conta(id)
        ON DELETE CASCADE
);

-- =====================================================
-- PREDIO
-- =====================================================

CREATE TABLE predio (
    id INT AUTO_INCREMENT PRIMARY KEY,

    nome VARCHAR(100) NOT NULL,
    bloco VARCHAR(50)
);

-- =====================================================
-- SALA
-- =====================================================

CREATE TABLE sala (
    id INT AUTO_INCREMENT PRIMARY KEY,

    predio_id INT NOT NULL,

    codigo VARCHAR(20) NOT NULL,

    capacidade INT NOT NULL,

    FOREIGN KEY (predio_id)
        REFERENCES predio(id)
        ON DELETE CASCADE
);

-- =====================================================
-- ALOCACAO_SALA
-- =====================================================

CREATE TABLE alocacao_sala (
    id INT AUTO_INCREMENT PRIMARY KEY,

    turma_id INT NOT NULL,
    sala_id INT NOT NULL,

    dia_semana VARCHAR(20),

    hora_abertura TIME,
    hora_fechamento TIME,

    status BOOLEAN DEFAULT TRUE,

    FOREIGN KEY (turma_id)
        REFERENCES turma(id)
        ON DELETE CASCADE,

    FOREIGN KEY (sala_id)
        REFERENCES sala(id)
        ON DELETE CASCADE
);