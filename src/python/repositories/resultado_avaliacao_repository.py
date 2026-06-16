from repositories.base_repository import BaseRepository


class ResultadoAvaliacaoRepository(BaseRepository):

    def create(self, id_avaliacao, id_matricula_disciplina, nota=None,
               feedback=None, status="PENDENTE", data_entrega=None):
        cursor = self._cursor()
        cursor.execute(
            """INSERT INTO resultado_avaliacao
               (id_avaliacao, id_matricula_disciplina, nota, feedback, status, data_entrega)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (id_avaliacao, id_matricula_disciplina, nota, feedback, status, data_entrega),
        )
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_resultado):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM resultado_avaliacao WHERE id = %s", (id_resultado,))
        return cursor.fetchone()

    def find_by_matricula_disciplina(self, id_md):
        cursor = self._cursor()
        cursor.execute(
            """SELECT ra.*, av.titulo, av.peso, av.nota_maxima
               FROM resultado_avaliacao ra
               JOIN avaliacao av ON av.id = ra.id_avaliacao
               WHERE ra.id_matricula_disciplina = %s""",
            (id_md,),
        )
        return cursor.fetchall()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM resultado_avaliacao")
        return cursor.fetchall()

    def update(self, id_resultado, nota=None, feedback=None, status=None, data_entrega=None):
        campos, valores = [], []
        for col, val in [("nota", nota), ("feedback", feedback), ("status", status), ("data_entrega", data_entrega)]:
            if val is not None:
                campos.append(f"{col} = %s"); valores.append(val)
        if not campos:
            return 0
        valores.append(id_resultado)
        cursor = self._cursor()
        cursor.execute(f"UPDATE resultado_avaliacao SET {', '.join(campos)} WHERE id = %s", valores)
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_resultado):
        cursor = self._cursor()
        cursor.execute("DELETE FROM resultado_avaliacao WHERE id = %s", (id_resultado,))
        self.conn.commit()
        return cursor.rowcount
