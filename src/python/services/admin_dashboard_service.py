# services/admin_dashboard_service.py
# Agrega contadores gerais do ecossistema pro Console Central do Admin:
# usuários por papel, turmas abertas no semestre vigente, infraestrutura
# física e matrículas ativas.

from database.connection import get_connection


def montar_painel_admin() -> dict:
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT COUNT(*) AS total FROM pessoa")
        total_pessoas = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM aluno")
        total_alunos = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM professor")
        total_professores = cursor.fetchone()["total"]

        cursor.execute(
            "SELECT COUNT(*) AS total FROM conta WHERE status = 'ATIVA'"
        )
        contas_ativas = cursor.fetchone()["total"]

        # Turmas do semestre mais recente cadastrado (o "vigente" no
        # sentido de dado disponível, não necessariamente a data de hoje)
        cursor.execute(
            """SELECT s.id, s.nome
               FROM semestre s
               ORDER BY s.data_inicio DESC
               LIMIT 1"""
        )
        semestre_atual = cursor.fetchone()

        turmas_abertas = 0
        if semestre_atual:
            cursor.execute(
                """SELECT COUNT(*) AS total
                   FROM turma t
                   JOIN oferta o ON o.id = t.id_oferta
                   WHERE o.id_semestre = %s""",
                (semestre_atual["id"],),
            )
            turmas_abertas = cursor.fetchone()["total"]

        cursor.execute(
            "SELECT COUNT(*) AS total FROM matricula_disciplina WHERE status = 'MATRICULADO'"
        )
        matriculas_ativas = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM departamento")
        total_departamentos = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM predio")
        total_predios = cursor.fetchone()["total"]

        cursor.execute("SELECT COUNT(*) AS total FROM sala")
        total_salas = cursor.fetchone()["total"]

        cursor.execute(
            """SELECT COUNT(*) AS total
               FROM information_schema.tables
               WHERE table_schema = DATABASE()"""
        )
        total_tabelas = cursor.fetchone()["total"]

        return {
            "total_pessoas": total_pessoas,
            "total_alunos": total_alunos,
            "total_professores": total_professores,
            "contas_ativas": contas_ativas,
            "semestre_atual": semestre_atual,
            "turmas_abertas": turmas_abertas,
            "matriculas_ativas": matriculas_ativas,
            "total_departamentos": total_departamentos,
            "total_predios": total_predios,
            "total_salas": total_salas,
            "total_tabelas": total_tabelas,
        }
    finally:
        conn.close()
