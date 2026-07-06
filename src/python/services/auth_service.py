# services/auth_service.py
# Regras de negócio de autenticação: hashing, login, registro e redefinição.
# Hash de senha via werkzeug (scrypt) — nunca armazenar senha em texto puro.

import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from database.connection import get_connection
from repositories.pessoa_repository import PessoaRepository
from repositories.aluno_repository import AlunoRepository
from repositories.conta_repository import ContaRepository


def gerar_hash_senha(senha: str) -> str:
    return generate_password_hash(senha, method='scrypt')


def conferir_senha(hash_senha: str, senha: str) -> bool:
    if not hash_senha:
        return False
    return check_password_hash(hash_senha, senha)


def autenticar(email: str, senha: str) -> dict:
    """
    Verifica credenciais de login.
    Retorna {"ok": True, "conta": {...}} ou {"ok": False, "erro": "..."}.
    """
    conn = get_connection()
    try:
        conta_repo = ContaRepository(conn)
        conta = conta_repo.find_by_email(email)

        if not conta:
            return {"ok": False, "erro": "E-mail ou senha inválidos."}

        if not conferir_senha(conta["senha"], senha):
            return {"ok": False, "erro": "E-mail ou senha inválidos."}

        if conta["status"] != "ATIVA":
            return {"ok": False, "erro": "Conta inativa ou suspensa. Procure a secretaria."}

        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT nome FROM pessoa WHERE id = %s", (conta["id_pessoa"],))
        pessoa = cursor.fetchone()

        return {
            "ok": True,
            "conta": {
                "id": conta["id"],
                "id_pessoa": conta["id_pessoa"],
                "email": conta["email"],
                "tipo": conta["tipo"],
                "nome": pessoa["nome"] if pessoa else "",
            },
        }
    finally:
        conn.close()


def registrar_aluno(nome, cpf, sexo, data_nascimento, email, senha) -> dict:
    """
    Cria Pessoa + Aluno + Conta em uma única operação (multi-tabela),
    garantindo integridade referencial (rollback se qualquer etapa falhar).
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT id FROM pessoa WHERE cpf = %s", (cpf,))
        if cursor.fetchone():
            return {"ok": False, "erro": "Já existe uma pessoa cadastrada com esse CPF."}

        cursor.execute("SELECT id FROM conta WHERE email = %s", (email,))
        if cursor.fetchone():
            return {"ok": False, "erro": "Já existe uma conta cadastrada com esse e-mail."}

        pessoa_repo = PessoaRepository(conn)
        aluno_repo = AlunoRepository(conn)
        conta_repo = ContaRepository(conn)

        id_pessoa = pessoa_repo.create(nome, cpf, sexo, data_nascimento)
        aluno_repo.create(id_pessoa, "GRADUACAO")
        senha_hash = gerar_hash_senha(senha)
        id_conta = conta_repo.create(id_pessoa, email, senha_hash, "ALUNO", "ATIVA")

        return {"ok": True, "id_pessoa": id_pessoa, "id_conta": id_conta}

    except Exception as ex:
        conn.rollback()
        return {"ok": False, "erro": f"Erro ao registrar: {ex}"}
    finally:
        conn.close()


def redefinir_senha(email: str, cpf: str, nova_senha: str) -> dict:
    """
    Redefine a senha de uma conta existente, confirmando a identidade
    do titular por e-mail + CPF (sem depender de envio de e-mail real).
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """SELECT c.id AS id_conta, c.id_pessoa
               FROM conta c
               JOIN pessoa p ON p.id = c.id_pessoa
               WHERE c.email = %s AND p.cpf = %s""",
            (email, cpf),
        )
        registro = cursor.fetchone()
        if not registro:
            return {"ok": False, "erro": "E-mail e CPF não correspondem a nenhuma conta."}

        conta_repo = ContaRepository(conn)
        senha_hash = gerar_hash_senha(nova_senha)
        conta_repo.update(registro["id_conta"], senha=senha_hash)

        return {"ok": True}
    finally:
        conn.close()
