from repositories.base_repository import BaseRepository


class AulaRepository(BaseRepository):

    def create(self, id_turma, data, tipo=None, conteudo=None):
        cursor = self._cursor()
        cursor.execute("INSERT INTO aula (id_turma, data, tipo, conteudo) VALUES (%s, %s, %s, %s)", (id_turma, data, tipo, conteudo))
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_aula):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM aula WHERE id = %s", (id_aula,))
        return cursor.fetchone()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM aula ORDER BY data DESC")
        return cursor.fetchall()

    def update(self, id_aula, data=None, tipo=None, conteudo=None):
        campos, valores = [], []
        for col, val in [("data", data), ("tipo", tipo), ("conteudo", conteudo)]:
            if val is not None:
                campos.append(f"{col} = %s"); valores.append(val)
        if not campos:
            return 0
        valores.append(id_aula)
        cursor = self._cursor()
        cursor.execute(f"UPDATE aula SET {', '.join(campos)} WHERE id = %s", valores)
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_aula):
        cursor = self._cursor()
        cursor.execute("DELETE FROM aula WHERE id = %s", (id_aula,))
        self.conn.commit()
        return cursor.rowcount
