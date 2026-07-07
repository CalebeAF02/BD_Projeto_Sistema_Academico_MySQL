-- =====================================================================
-- Adiciona coluna de foto (LONGBLOB) na tabela pessoa.
-- Executar APÓS 00_criar_tabelas.sql, ANTES dos seeds.
-- =====================================================================

USE projeto_unb;

-- Força UTF-8 na sessão, independente do codepage do cliente
-- (evita corrupção de acentos em clientes Windows com console cp850)
SET NAMES utf8mb4;

ALTER TABLE pessoa
    ADD COLUMN foto LONGBLOB;
