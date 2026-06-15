from repositories.base_repository import BaseRepository


class EventoRepository(BaseRepository):

    def create(self, id_turma, titulo, descricao=None, tipo=None, data_inicio=None, data_fim=None, local=None):
        cursor = self._cursor()
        cursor.execute(
            "INSERT INTO evento (id_turma, titulo, descricao, tipo, data_inicio, data_fim, local) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (id_turma, titulo, descricao, tipo, data_inicio, data_fim, local),
        )
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_evento):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM evento WHERE id = %s", (id_evento,))
        return cursor.fetchone()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM evento ORDER BY data_inicio DESC")
        return cursor.fetchall()

    def update(self, id_evento, titulo=None, descricao=None, tipo=None, data_inicio=None, data_fim=None, local=None):
        campos, valores = [], []
        for col, val in [("titulo", titulo), ("descricao", descricao), ("tipo", tipo),
                         ("data_inicio", data_inicio), ("data_fim", data_fim), ("local", local)]:
            if val is not None:
                campos.append(f"{col} = %s"); valores.append(val)
        if not campos:
            return 0
        valores.append(id_evento)
        cursor = self._cursor()
        cursor.execute(f"UPDATE evento SET {', '.join(campos)} WHERE id = %s", valores)
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_evento):
        cursor = self._cursor()
        cursor.execute("DELETE FROM evento WHERE id = %s", (id_evento,))
        self.conn.commit()
        return cursor.rowcount
