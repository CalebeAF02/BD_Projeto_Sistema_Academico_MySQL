from database.connection import get_connection
from repositories.aluno_repository import AlunoRepository
from repositories.matricula_curso_repository import MatriculaCursoRepository
from repositories.turma_repository import TurmaRepository
from repositories.matricula_disciplina_repository import MatriculaDisciplinaRepository
import mysql.connector


def matricular_aluno_em_disciplina(id_pessoa: int, id_oferta: int) -> dict:
    """
    Matricula um aluno em uma turma associada à oferta informada.

    Passos:
      1. Verifica se id_pessoa é aluno cadastrado.
      2. Verifica se existe matricula_curso ATIVA para esse aluno.
      3. Busca a primeira turma com vagas da oferta.
      4. Chama sp_matricular_aluno_em_turma via procedure.
      5. Retorna dict com sucesso/erro e id_matricula_disciplina gerado.
    """
    conn = get_connection()
    try:
        aluno_repo = AlunoRepository(conn)
        mc_repo = MatriculaCursoRepository(conn)
        turma_repo = TurmaRepository(conn)

        # 1. Confirma que a pessoa é aluno
        aluno = aluno_repo.find_by_id(id_pessoa)
        if not aluno:
            return {"ok": False, "erro": f"Pessoa {id_pessoa} não é aluno cadastrado."}

        # 2. Verifica matrícula em curso ativa
        mc = mc_repo.find_ativa_por_aluno(id_pessoa)
        if not mc:
            return {"ok": False, "erro": f"Aluno {id_pessoa} não possui matrícula em curso ativa."}

        # 3. Busca turmas da oferta e escolhe a primeira com vaga
        turmas = turma_repo.find_by_oferta(id_oferta)
        if not turmas:
            return {"ok": False, "erro": f"Nenhuma turma encontrada para a oferta {id_oferta}."}

        id_turma_escolhida = turmas[0]["id"]

        # 4. Chama a procedure — ela valida vagas e insere
        cursor = conn.cursor()
        cursor.callproc("sp_matricular_aluno_em_turma", [mc["id"], id_turma_escolhida])

        id_matricula_disciplina = None
        for resultado in cursor.stored_results():
            row = resultado.fetchone()
            if row:
                id_matricula_disciplina = row[0]

        conn.commit()
        return {
            "ok": True,
            "id_matricula_disciplina": id_matricula_disciplina,
            "id_matricula_curso": mc["id"],
            "id_turma": id_turma_escolhida,
            "mensagem": "Matrícula realizada com sucesso.",
        }

    except mysql.connector.Error as e:
        conn.rollback()
        return {"ok": False, "erro": str(e.msg)}
    finally:
        conn.close()


def buscar_historico_aluno(id_aluno: int) -> list:
    """
    Consulta a view vw_historico_aluno e retorna o histórico completo
    de um aluno (todas as disciplinas matriculadas com notas e status).
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM vw_historico_aluno WHERE id_pessoa = %s ORDER BY semestre DESC, nome_disciplina",
            (id_aluno,),
        )
        return cursor.fetchall()
    finally:
        conn.close()
