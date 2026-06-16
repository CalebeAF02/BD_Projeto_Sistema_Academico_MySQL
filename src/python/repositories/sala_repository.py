from repositories.base_repository import BaseRepository


class SalaRepository(BaseRepository):

    def create(self, id_predio, codigo, capacidade):
        cursor = self._cursor()
        cursor.execute("INSERT INTO sala (id_predio, codigo, capacidade) VALUES (%s, %s, %s)", (id_predio, codigo, capacidade))
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_sala):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM sala WHERE id = %s", (id_sala,))
        return cursor.fetchone()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM sala ORDER BY codigo")
        return cursor.fetchall()

    def update(self, id_sala, codigo=None, capacidade=None):
        campos, valores = [], []
        if codigo is not None:
            campos.append("codigo = %s"); valores.append(codigo)
        if capacidade is not None:
            campos.append("capacidade = %s"); valores.append(capacidade)
        if not campos:
            return 0
        valores.append(id_sala)
        cursor = self._cursor()
        cursor.execute(f"UPDATE sala SET {', '.join(campos)} WHERE id = %s", valores)
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_sala):
        cursor = self._cursor()
        cursor.execute("DELETE FROM sala WHERE id = %s", (id_sala,))
        self.conn.commit()
        return cursor.rowcount
