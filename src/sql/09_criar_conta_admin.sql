-- =====================================================================
-- Cria a conta de administrador de demonstração (papel ADMIN).
-- Necessária porque os seeds originais (05_seeds.sql) só têm contas
-- ALUNO e PROFESSOR — sem isso, ninguém consegue acessar /demo e
-- /sql-console depois da restrição de acesso por papel.
-- Executar APÓS 08_recriar_procedure_utf8.sql.
-- =====================================================================

USE projeto_unb;

SET NAMES utf8mb4;

-- Pessoa "administrativa" — não é aluno nem professor, só existe pra
-- amarrar a conta de login (pessoa.id é FK obrigatória de conta.id_pessoa).
INSERT INTO pessoa (id, nome, cpf, sexo, data_nascimento)
VALUES (11, 'Administrador do Sistema', '00000000000', 'M', '1990-01-01')
ON DUPLICATE KEY UPDATE nome = VALUES(nome);

-- Senha: admin123 (hash gerado com werkzeug scrypt, igual aos demais).
INSERT INTO conta (id, id_pessoa, email, senha, tipo, status)
VALUES (
    11,
    11,
    'admin@sga.unb.br',
    'scrypt:32768:8:1$gHCqVl2VGK4AnvW9$4dcd8b3c3dd6b368d14761f129ee403101f4526f46ddfe818bc8e0040641f98efe7ccdb1be06845a27e6c891fe7e2873dad23bcdd5acdb667b3caec0cff56706',
    'ADMIN',
    'ATIVA'
)
ON DUPLICATE KEY UPDATE senha = VALUES(senha), status = VALUES(status);
