from repositories.base_repository import BaseRepository


class AvaliacaoRepository(BaseRepository):

    def create(self, id_turma, titulo, tipo, peso, nota_maxima,
               descricao=None, data_aplicacao=None, prazo=None, status="PLANEJADA"):
        cursor = self._cursor()
        cursor.execute(
            """INSERT INTO avaliacao
               (id_turma, titulo, descricao, tipo, peso, nota_maxima, data_aplicacao, prazo, status)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (id_turma, titulo, descricao, tipo, peso, nota_maxima, data_aplicacao, prazo, status),
        )
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_avaliacao):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM avaliacao WHERE id = %s", (id_avaliacao,))
        return cursor.fetchone()

    def find_by_turma(self, id_turma):
        cursor = self._cursor()
        cursor.execute(
            "SELECT * FROM avaliacao WHERE id_turma = %s ORDER BY data_aplicacao",
            (id_turma,),
        )
        return cursor.fetchall()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM avaliacao ORDER BY data_aplicacao")
        return cursor.fetchall()

    def update(self, id_avaliacao, titulo=None, descricao=None, tipo=None,
               peso=None, nota_maxima=None, data_aplicacao=None, prazo=None, status=None):
        campos, valores = [], []
        for col, val in [("titulo", titulo), ("descricao", descricao), ("tipo", tipo),
                         ("peso", peso), ("nota_maxima", nota_maxima),
                         ("data_aplicacao", data_aplicacao), ("prazo", prazo), ("status", status)]:
            if val is not None:
                campos.append(f"{col} = %s"); valores.append(val)
        if not campos:
            return 0
        valores.append(id_avaliacao)
        cursor = self._cursor()
        cursor.execute(f"UPDATE avaliacao SET {', '.join(campos)} WHERE id = %s", valores)
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_avaliacao):
        cursor = self._cursor()
        cursor.execute("DELETE FROM avaliacao WHERE id = %s", (id_avaliacao,))
        self.conn.commit()
        return cursor.rowcount
