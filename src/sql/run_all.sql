-- =====================================================================
-- run_all.sql
-- Executa todos os scripts de setup do banco em ordem, de uma vez só.
-- Evita esquecer algum script individual ao recriar o ambiente.
--
-- Uso (a partir da pasta src/sql/):
--     mysql -u root -p < run_all.sql
--
-- Se preferir rodar de outro diretório, entre no cliente mysql e use
-- SOURCE com o caminho completo para cada arquivo, na mesma ordem.
-- =====================================================================

SOURCE 00_criar_tabelas.sql
SOURCE 01_views.sql
SOURCE 02_procedures.sql
SOURCE 03_triggers.sql
SOURCE 04_alter_foto.sql
SOURCE 05_seeds.sql
