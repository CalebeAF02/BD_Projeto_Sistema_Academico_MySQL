from repositories.base_repository import BaseRepository


class DisciplinaRepository(BaseRepository):

    def create(self, codigo, nome):
        cursor = self._cursor()
        cursor.execute("INSERT INTO disciplina (codigo, nome) VALUES (%s, %s)", (codigo, nome))
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_disciplina):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM disciplina WHERE id = %s", (id_disciplina,))
        return cursor.fetchone()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM disciplina ORDER BY codigo")
        return cursor.fetchall()

    def update(self, id_disciplina, codigo=None, nome=None):
        campos, valores = [], []
        if codigo is not None:
            campos.append("codigo = %s"); valores.append(codigo)
        if nome is not None:
            campos.append("nome = %s"); valores.append(nome)
        if not campos:
            return 0
        valores.append(id_disciplina)
        cursor = self._cursor()
        cursor.execute(f"UPDATE disciplina SET {', '.join(campos)} WHERE id = %s", valores)
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_disciplina):
        cursor = self._cursor()
        cursor.execute("DELETE FROM disciplina WHERE id = %s", (id_disciplina,))
        self.conn.commit()
        return cursor.rowcount
