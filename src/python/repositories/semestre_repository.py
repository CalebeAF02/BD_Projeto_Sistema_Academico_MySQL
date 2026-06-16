from repositories.base_repository import BaseRepository


class SemestreRepository(BaseRepository):

    def create(self, nome, data_inicio, data_fim):
        cursor = self._cursor()
        cursor.execute(
            "INSERT INTO semestre (nome, data_inicio, data_fim) VALUES (%s, %s, %s)",
            (nome, data_inicio, data_fim),
        )
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_semestre):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM semestre WHERE id = %s", (id_semestre,))
        return cursor.fetchone()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM semestre ORDER BY data_inicio DESC")
        return cursor.fetchall()

    def update(self, id_semestre, nome=None, data_inicio=None, data_fim=None):
        campos, valores = [], []
        if nome is not None:
            campos.append("nome = %s"); valores.append(nome)
        if data_inicio is not None:
            campos.append("data_inicio = %s"); valores.append(data_inicio)
        if data_fim is not None:
            campos.append("data_fim = %s"); valores.append(data_fim)
        if not campos:
            return 0
        valores.append(id_semestre)
        cursor = self._cursor()
        cursor.execute(f"UPDATE semestre SET {', '.join(campos)} WHERE id = %s", valores)
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_semestre):
        cursor = self._cursor()
        cursor.execute("DELETE FROM semestre WHERE id = %s", (id_semestre,))
        self.conn.commit()
        return cursor.rowcount
