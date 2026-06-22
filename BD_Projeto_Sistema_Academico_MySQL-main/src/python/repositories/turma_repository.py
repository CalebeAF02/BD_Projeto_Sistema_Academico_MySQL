from repositories.base_repository import BaseRepository


class TurmaRepository(BaseRepository):

    def create(self, id_oferta, codigo, quantidade_vagas):
        cursor = self._cursor()
        cursor.execute(
            "INSERT INTO turma (id_oferta, codigo, quantidade_vagas) VALUES (%s, %s, %s)",
            (id_oferta, codigo, quantidade_vagas),
        )
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_turma):
        cursor = self._cursor()
        cursor.execute(
            """SELECT t.*, o.codigo_oferta, d.nome AS disciplina, s.nome AS semestre
               FROM turma t
               JOIN oferta o     ON o.id = t.id_oferta
               JOIN disciplina d ON d.id = o.id_disciplina
               JOIN semestre s   ON s.id = o.id_semestre
               WHERE t.id = %s""",
            (id_turma,),
        )
        return cursor.fetchone()

    def find_by_oferta(self, id_oferta):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM turma WHERE id_oferta = %s", (id_oferta,))
        return cursor.fetchall()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute(
            """SELECT t.id, t.codigo, t.quantidade_vagas, d.nome AS disciplina, s.nome AS semestre
               FROM turma t
               JOIN oferta o     ON o.id = t.id_oferta
               JOIN disciplina d ON d.id = o.id_disciplina
               JOIN semestre s   ON s.id = o.id_semestre
               ORDER BY s.data_inicio DESC, d.nome"""
        )
        return cursor.fetchall()

    def update(self, id_turma, codigo=None, quantidade_vagas=None):
        campos, valores = [], []
        if codigo is not None:
            campos.append("codigo = %s"); valores.append(codigo)
        if quantidade_vagas is not None:
            campos.append("quantidade_vagas = %s"); valores.append(quantidade_vagas)
        if not campos:
            return 0
        valores.append(id_turma)
        cursor = self._cursor()
        cursor.execute(f"UPDATE turma SET {', '.join(campos)} WHERE id = %s", valores)
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_turma):
        cursor = self._cursor()
        cursor.execute("DELETE FROM turma WHERE id = %s", (id_turma,))
        self.conn.commit()
        return cursor.rowcount
