# services/professor_dashboard_service.py
# Agrega dados pro Painel Geral do Professor: turmas sob responsabilidade
# no semestre vigente, total de alunos, avaliações pendentes de correção
# e próximos eventos. Mesmo padrão de aluno_dashboard_service.py.

from database.connection import get_connection


def montar_painel_professor(id_pessoa: int) -> dict:
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """SELECT p.nome, pr.nivel, pr.tipo, d.nome AS departamento
               FROM professor pr
               JOIN pessoa p ON p.id = pr.id_pessoa
               JOIN departamento d ON d.id = pr.id_departamento
               WHERE pr.id_pessoa = %s""",
            (id_pessoa,),
        )
        perfil = cursor.fetchone()

        # Turmas do professor no semestre mais recente em que ele leciona,
        # já com a contagem de alunos matriculados (exclui trancados).
        cursor.execute(
            """SELECT t.id AS id_turma, t.codigo AS turma, t.quantidade_vagas,
                      d.nome AS disciplina, d.codigo AS codigo_disciplina,
                      s.nome AS semestre, pt.funcao,
                      (SELECT COUNT(*) FROM matricula_disciplina md
                        WHERE md.id_turma = t.id AND md.status != 'TRANCADO') AS matriculados
               FROM professor_turma pt
               JOIN turma t      ON t.id = pt.id_turma
               JOIN oferta o     ON o.id = t.id_oferta
               JOIN disciplina d ON d.id = o.id_disciplina
               JOIN semestre s   ON s.id = o.id_semestre
               WHERE pt.id_professor = %s
               ORDER BY s.data_inicio DESC, d.nome""",
            (id_pessoa,),
        )
        turmas = cursor.fetchall()

        ids_turma = [t["id_turma"] for t in turmas]
        total_alunos = sum(t["matriculados"] for t in turmas)

        avaliacoes_pendentes = []
        proximos_eventos = []

        if ids_turma:
            placeholders = ",".join(["%s"] * len(ids_turma))

            # Resultados de avaliação ainda não corrigidos, nas turmas do professor
            cursor.execute(
                f"""SELECT ra.id, av.titulo AS avaliacao, d.nome AS disciplina,
                           t.codigo AS turma, ra.status
                    FROM resultado_avaliacao ra
                    JOIN avaliacao av  ON av.id = ra.id_avaliacao
                    JOIN turma t       ON t.id = av.id_turma
                    JOIN oferta o      ON o.id = t.id_oferta
                    JOIN disciplina d  ON d.id = o.id_disciplina
                    WHERE av.id_turma IN ({placeholders})
                      AND ra.status IN ('PENDENTE', 'ENTREGUE')
                    ORDER BY ra.data_entrega""",
                ids_turma,
            )
            avaliacoes_pendentes = cursor.fetchall()

            # Próximos eventos (a partir de hoje) nas turmas do professor
            cursor.execute(
                f"""SELECT ev.id, ev.titulo, ev.tipo, ev.data_inicio, ev.local,
                           d.nome AS disciplina, t.codigo AS turma
                    FROM evento ev
                    JOIN turma t      ON t.id = ev.id_turma
                    JOIN oferta o     ON o.id = t.id_oferta
                    JOIN disciplina d ON d.id = o.id_disciplina
                    WHERE ev.id_turma IN ({placeholders})
                      AND ev.data_inicio >= CURDATE()
                    ORDER BY ev.data_inicio
                    LIMIT 5""",
                ids_turma,
            )
            proximos_eventos = cursor.fetchall()

        return {
            "perfil": perfil,
            "turmas": turmas,
            "total_alunos": total_alunos,
            "avaliacoes_pendentes": avaliacoes_pendentes,
            "proximos_eventos": proximos_eventos,
        }
    finally:
        conn.close()
