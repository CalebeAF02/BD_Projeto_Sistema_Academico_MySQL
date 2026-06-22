from repositories.base_repository import BaseRepository


class MetaEstudoRepository(BaseRepository):

    def create(self, id_aluno, horas, titulo=None, prazo=None, status="EM_ANDAMENTO"):
        cursor = self._cursor()
        cursor.execute(
            "INSERT INTO meta_de_estudo (id_aluno, titulo, horas, prazo, status) VALUES (%s, %s, %s, %s, %s)",
            (id_aluno, titulo, horas, prazo, status),
        )
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_meta):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM meta_de_estudo WHERE id = %s", (id_meta,))
        return cursor.fetchone()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM meta_de_estudo ORDER BY prazo")
        return cursor.fetchall()

    def update(self, id_meta, titulo=None, horas=None, prazo=None, status=None):
        campos, valores = [], []
        for col, val in [("titulo", titulo), ("horas", horas), ("prazo", prazo), ("status", status)]:
            if val is not None:
                campos.append(f"{col} = %s"); valores.append(val)
        if not campos:
            return 0
        valores.append(id_meta)
        cursor = self._cursor()
        cursor.execute(f"UPDATE meta_de_estudo SET {', '.join(campos)} WHERE id = %s", valores)
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_meta):
        cursor = self._cursor()
        cursor.execute("DELETE FROM meta_de_estudo WHERE id = %s", (id_meta,))
        self.conn.commit()
        return cursor.rowcount
