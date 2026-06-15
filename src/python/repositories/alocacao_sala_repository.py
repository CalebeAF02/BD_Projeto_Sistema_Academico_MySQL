from repositories.base_repository import BaseRepository


class AlocacaoSalaRepository(BaseRepository):

    def create(self, id_turma, id_sala, dia_semana, hora_abertura, hora_fechamento, status=True):
        cursor = self._cursor()
        cursor.execute(
            """INSERT INTO alocacao_sala (id_turma, id_sala, dia_semana, hora_abertura, hora_fechamento, status)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (id_turma, id_sala, dia_semana, hora_abertura, hora_fechamento, status),
        )
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_aloc):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM alocacao_sala WHERE id = %s", (id_aloc,))
        return cursor.fetchone()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM alocacao_sala")
        return cursor.fetchall()

    def update(self, id_aloc, dia_semana=None, hora_abertura=None, hora_fechamento=None, status=None):
        campos, valores = [], []
        for col, val in [("dia_semana", dia_semana), ("hora_abertura", hora_abertura),
                         ("hora_fechamento", hora_fechamento), ("status", status)]:
            if val is not None:
                campos.append(f"{col} = %s"); valores.append(val)
        if not campos:
            return 0
        valores.append(id_aloc)
        cursor = self._cursor()
        cursor.execute(f"UPDATE alocacao_sala SET {', '.join(campos)} WHERE id = %s", valores)
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_aloc):
        cursor = self._cursor()
        cursor.execute("DELETE FROM alocacao_sala WHERE id = %s", (id_aloc,))
        self.conn.commit()
        return cursor.rowcount
