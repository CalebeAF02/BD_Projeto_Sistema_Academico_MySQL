from repositories.base_repository import BaseRepository


class MatriculaCursoRepository(BaseRepository):

    def create(self, id_aluno, id_curso, codigo, data_matricula_curso, status="ATIVA"):
        cursor = self._cursor()
        cursor.execute(
            """INSERT INTO matricula_curso
               (id_aluno, id_curso, codigo, data_matricula_curso, status)
               VALUES (%s, %s, %s, %s, %s)""",
            (id_aluno, id_curso, codigo, data_matricula_curso, status),
        )
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_matricula_curso):
        cursor = self._cursor()
        cursor.execute(
            """SELECT mc.*, p.nome AS nome_aluno, c.nome AS nome_curso
               FROM matricula_curso mc
               JOIN aluno a  ON a.id_pessoa = mc.id_aluno
               JOIN pessoa p ON p.id = a.id_pessoa
               JOIN curso c  ON c.id = mc.id_curso
               WHERE mc.id = %s""",
            (id_matricula_curso,),
        )
        return cursor.fetchone()

    def find_by_aluno(self, id_aluno):
        cursor = self._cursor()
        cursor.execute(
            """SELECT mc.*, c.nome AS nome_curso, c.sigla
               FROM matricula_curso mc
               JOIN curso c ON c.id = mc.id_curso
               WHERE mc.id_aluno = %s ORDER BY mc.data_matricula_curso DESC""",
            (id_aluno,),
        )
        return cursor.fetchall()

    def find_ativa_por_aluno(self, id_aluno):
        cursor = self._cursor()
        cursor.execute(
            "SELECT * FROM matricula_curso WHERE id_aluno = %s AND status = 'ATIVA' LIMIT 1",
            (id_aluno,),
        )
        return cursor.fetchone()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute(
            """SELECT mc.id, mc.codigo, mc.status, p.nome AS aluno, c.sigla AS curso
               FROM matricula_curso mc
               JOIN aluno a  ON a.id_pessoa = mc.id_aluno
               JOIN pessoa p ON p.id = a.id_pessoa
               JOIN curso c  ON c.id = mc.id_curso
               ORDER BY mc.data_matricula_curso DESC"""
        )
        return cursor.fetchall()

    def update(self, id_matricula_curso, status=None, data_trancamento_curso=None):
        campos, valores = [], []
        if status is not None:
            campos.append("status = %s"); valores.append(status)
        if data_trancamento_curso is not None:
            campos.append("data_trancamento_curso = %s"); valores.append(data_trancamento_curso)
        if not campos:
            return 0
        valores.append(id_matricula_curso)
        cursor = self._cursor()
        cursor.execute(f"UPDATE matricula_curso SET {', '.join(campos)} WHERE id = %s", valores)
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_matricula_curso):
        cursor = self._cursor()
        cursor.execute("DELETE FROM matricula_curso WHERE id = %s", (id_matricula_curso,))
        self.conn.commit()
        return cursor.rowcount
