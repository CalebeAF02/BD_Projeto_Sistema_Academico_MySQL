# services/aluno_dashboard_service.py
# Agrega dados de várias tabelas pro Painel Geral do Aluno: resumo do
# semestre, percentual de frequência, alertas de nota e metas de estudo.
# Segue o mesmo padrão de matricula_service.buscar_historico_aluno —
# consultas agregadas multi-tabela ficam no service, não em repository.

from database.connection import get_connection

NOTA_MINIMA_APROVACAO = 6.0


def montar_painel_aluno(id_pessoa: int) -> dict:
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)

        # Perfil + matrícula de curso ativa
        cursor.execute(
            """SELECT p.nome, mc.id AS id_matricula_curso, mc.codigo,
                      c.nome AS curso, c.sigla
               FROM pessoa p
               JOIN aluno a ON a.id_pessoa = p.id
               LEFT JOIN matricula_curso mc
                      ON mc.id_aluno = a.id_pessoa AND mc.status = 'ATIVA'
               LEFT JOIN curso c ON c.id = mc.id_curso
               WHERE p.id = %s
               LIMIT 1""",
            (id_pessoa,),
        )
        perfil = cursor.fetchone()

        disciplinas = []
        media_geral = None
        percentual_frequencia = None
        alertas_nota = []

        if perfil and perfil["id_matricula_curso"]:
            id_mc = perfil["id_matricula_curso"]

            cursor.execute(
                """SELECT md.id, md.nota, md.status, d.nome AS disciplina,
                          d.codigo AS codigo_disciplina, t.codigo AS turma,
                          s.nome AS semestre
                   FROM matricula_disciplina md
                   JOIN turma t     ON t.id = md.id_turma
                   JOIN oferta o    ON o.id = t.id_oferta
                   JOIN disciplina d ON d.id = o.id_disciplina
                   JOIN semestre s  ON s.id = o.id_semestre
                   WHERE md.id_matricula_curso = %s
                   ORDER BY s.data_inicio DESC""",
                (id_mc,),
            )
            disciplinas = cursor.fetchall()

            notas_validas = [float(d["nota"]) for d in disciplinas if d["nota"] is not None]
            if notas_validas:
                media_geral = round(sum(notas_validas) / len(notas_validas), 2)

            alertas_nota = [
                d for d in disciplinas
                if d["nota"] is not None and float(d["nota"]) < NOTA_MINIMA_APROVACAO
            ]

            cursor.execute(
                """SELECT
                       SUM(CASE WHEN f.presente = 1 THEN 1 ELSE 0 END) AS presencas,
                       COUNT(*) AS total
                   FROM frequencia f
                   JOIN matricula_disciplina md ON md.id = f.id_matricula_disciplina
                   WHERE md.id_matricula_curso = %s""",
                (id_mc,),
            )
            freq = cursor.fetchone()
            if freq and freq["total"]:
                percentual_frequencia = round((freq["presencas"] / freq["total"]) * 100, 1)

        # Metas de estudo em andamento
        cursor.execute(
            """SELECT id, titulo, horas, prazo, status
               FROM meta_de_estudo
               WHERE id_aluno = %s AND status = 'EM_ANDAMENTO'
               ORDER BY prazo""",
            (id_pessoa,),
        )
        metas = cursor.fetchall()

        # Últimas 5 notificações da conta do aluno
        cursor.execute(
            """SELECT n.titulo, n.mensagem, n.tipo, nc.data_envio, nc.lida
               FROM notificacao_conta nc
               JOIN notificacao n ON n.id = nc.id_notificacao
               JOIN conta ct      ON ct.id = nc.id_conta
               WHERE ct.id_pessoa = %s
               ORDER BY nc.data_envio DESC
               LIMIT 5""",
            (id_pessoa,),
        )
        notificacoes = cursor.fetchall()

        return {
            "perfil": perfil,
            "disciplinas": disciplinas,
            "media_geral": media_geral,
            "percentual_frequencia": percentual_frequencia,
            "alertas_nota": alertas_nota,
            "metas": metas,
            "notificacoes": notificacoes,
        }
    finally:
        conn.close()
