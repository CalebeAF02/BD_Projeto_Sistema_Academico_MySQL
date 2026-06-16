from repositories.base_repository import BaseRepository


class DepartamentoRepository(BaseRepository):

    def create(self, nome):
        cursor = self._cursor()
        cursor.execute("INSERT INTO departamento (nome) VALUES (%s)", (nome,))
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_departamento):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM departamento WHERE id = %s", (id_departamento,))
        return cursor.fetchone()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM departamento ORDER BY nome")
        return cursor.fetchall()

    def update(self, id_departamento, nome):
        cursor = self._cursor()
        cursor.execute("UPDATE departamento SET nome = %s WHERE id = %s", (nome, id_departamento))
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_departamento):
        cursor = self._cursor()
        cursor.execute("DELETE FROM departamento WHERE id = %s", (id_departamento,))
        self.conn.commit()
        return cursor.rowcount
