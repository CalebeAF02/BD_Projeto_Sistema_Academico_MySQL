from repositories.base_repository import BaseRepository


class MatriculaDisciplinaRepository(BaseRepository):

    def create(self, id_matricula_curso, id_turma, codigo, data_matricula_disciplina, status="MATRICULADO"):
        cursor = self._cursor()
        cursor.execute(
            """INSERT INTO matricula_disciplina
               (id_matricula_curso, id_turma, codigo, data_matricula_disciplina, status)
               VALUES (%s, %s, %s, %s, %s)""",
            (id_matricula_curso, id_turma, codigo, data_matricula_disciplina, status),
        )
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_md):
        cursor = self._cursor()
        cursor.execute(
            """SELECT md.*, d.nome AS disciplina, t.codigo AS turma,
                      p.nome AS nome_aluno, s.nome AS semestre
               FROM matricula_disciplina md
               JOIN turma t        ON t.id  = md.id_turma
               JOIN oferta o       ON o.id  = t.id_oferta
               JOIN disciplina d   ON d.id  = o.id_disciplina
               JOIN semestre s     ON s.id  = o.id_semestre
               JOIN matricula_curso mc ON mc.id = md.id_matricula_curso
               JOIN aluno a        ON a.id_pessoa = mc.id_aluno
               JOIN pessoa p       ON p.id = a.id_pessoa
               WHERE md.id = %s""",
            (id_md,),
        )
        return cursor.fetchone()

    def find_by_matricula_curso(self, id_matricula_curso):
        cursor = self._cursor()
        cursor.execute(
            """SELECT md.id, md.codigo, md.nota, md.status, d.nome AS disciplina,
                      t.codigo AS turma, s.nome AS semestre
               FROM matricula_disciplina md
               JOIN turma t      ON t.id = md.id_turma
               JOIN oferta o     ON o.id = t.id_oferta
               JOIN disciplina d ON d.id = o.id_disciplina
               JOIN semestre s   ON s.id = o.id_semestre
               WHERE md.id_matricula_curso = %s
               ORDER BY s.data_inicio DESC""",
            (id_matricula_curso,),
        )
        return cursor.fetchall()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute(
            """SELECT md.id, md.codigo, md.nota, md.status,
                      p.nome AS aluno, d.nome AS disciplina, s.nome AS semestre
               FROM matricula_disciplina md
               JOIN turma t        ON t.id  = md.id_turma
               JOIN oferta o       ON o.id  = t.id_oferta
               JOIN disciplina d   ON d.id  = o.id_disciplina
               JOIN semestre s     ON s.id  = o.id_semestre
               JOIN matricula_curso mc ON mc.id = md.id_matricula_curso
               JOIN aluno a        ON a.id_pessoa = mc.id_aluno
               JOIN pessoa p       ON p.id = a.id_pessoa
               ORDER BY s.data_inicio DESC, p.nome"""
        )
        return cursor.fetchall()

    def update(self, id_md, status=None, nota=None, data_trancamento_disciplina=None):
        campos, valores = [], []
        if status is not None:
            campos.append("status = %s"); valores.append(status)
        if nota is not None:
            campos.append("nota = %s"); valores.append(nota)
        if data_trancamento_disciplina is not None:
            campos.append("data_trancamento_disciplina = %s"); valores.append(data_trancamento_disciplina)
        if not campos:
            return 0
        valores.append(id_md)
        cursor = self._cursor()
        cursor.execute(f"UPDATE matricula_disciplina SET {', '.join(campos)} WHERE id = %s", valores)
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_md):
        cursor = self._cursor()
        cursor.execute("DELETE FROM matricula_disciplina WHERE id = %s", (id_md,))
        self.conn.commit()
        return cursor.rowcount
