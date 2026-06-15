-- =====================================================================
-- Adiciona coluna de foto (LONGBLOB) na tabela pessoa.
-- Executar APÓS 00_criar_tabelas.sql, ANTES dos seeds.
-- =====================================================================

USE projeto_unb;

ALTER TABLE pessoa
    ADD COLUMN foto LONGBLOB;
