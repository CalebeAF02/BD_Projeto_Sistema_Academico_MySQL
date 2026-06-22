from repositories.base_repository import BaseRepository


class OfertaRepository(BaseRepository):

    def create(self, id_departamento, id_disciplina, id_curso, id_semestre, codigo_oferta):
        cursor = self._cursor()
        cursor.execute(
            """INSERT INTO oferta (id_departamento, id_disciplina, id_curso, id_semestre, codigo_oferta)
               VALUES (%s, %s, %s, %s, %s)""",
            (id_departamento, id_disciplina, id_curso, id_semestre, codigo_oferta),
        )
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_oferta):
        cursor = self._cursor()
        cursor.execute(
            """SELECT o.*, d.nome AS disciplina, c.nome AS curso, s.nome AS semestre,
                      dep.nome AS departamento
               FROM oferta o
               JOIN disciplina d  ON d.id  = o.id_disciplina
               JOIN curso c       ON c.id  = o.id_curso
               JOIN semestre s    ON s.id  = o.id_semestre
               JOIN departamento dep ON dep.id = o.id_departamento
               WHERE o.id = %s""",
            (id_oferta,),
        )
        return cursor.fetchone()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute(
            """SELECT o.id, o.codigo_oferta, d.nome AS disciplina,
                      c.sigla AS curso, s.nome AS semestre
               FROM oferta o
               JOIN disciplina d ON d.id = o.id_disciplina
               JOIN curso c      ON c.id = o.id_curso
               JOIN semestre s   ON s.id = o.id_semestre
               ORDER BY s.data_inicio DESC, d.nome"""
        )
        return cursor.fetchall()

    def update(self, id_oferta, codigo_oferta):
        cursor = self._cursor()
        cursor.execute("UPDATE oferta SET codigo_oferta = %s WHERE id = %s", (codigo_oferta, id_oferta))
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_oferta):
        cursor = self._cursor()
        cursor.execute("DELETE FROM oferta WHERE id = %s", (id_oferta,))
        self.conn.commit()
        return cursor.rowcount
