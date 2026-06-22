from repositories.base_repository import BaseRepository


class CursoRepository(BaseRepository):

    def create(self, nome, sigla):
        cursor = self._cursor()
        cursor.execute("INSERT INTO curso (nome, sigla) VALUES (%s, %s)", (nome, sigla))
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_curso):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM curso WHERE id = %s", (id_curso,))
        return cursor.fetchone()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM curso ORDER BY nome")
        return cursor.fetchall()

    def update(self, id_curso, nome=None, sigla=None):
        campos, valores = [], []
        if nome is not None:
            campos.append("nome = %s"); valores.append(nome)
        if sigla is not None:
            campos.append("sigla = %s"); valores.append(sigla)
        if not campos:
            return 0
        valores.append(id_curso)
        cursor = self._cursor()
        cursor.execute(f"UPDATE curso SET {', '.join(campos)} WHERE id = %s", valores)
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_curso):
        cursor = self._cursor()
        cursor.execute("DELETE FROM curso WHERE id = %s", (id_curso,))
        self.conn.commit()
        return cursor.rowcount
