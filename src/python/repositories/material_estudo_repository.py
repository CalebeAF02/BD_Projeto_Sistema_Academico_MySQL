from repositories.base_repository import BaseRepository


class MaterialEstudoRepository(BaseRepository):

    def create(self, id_disciplina, titulo, descricao=None, tipo=None, link=None):
        cursor = self._cursor()
        cursor.execute(
            "INSERT INTO material_de_estudo (id_disciplina, titulo, descricao, tipo, link) VALUES (%s, %s, %s, %s, %s)",
            (id_disciplina, titulo, descricao, tipo, link),
        )
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_material):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM material_de_estudo WHERE id = %s", (id_material,))
        return cursor.fetchone()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM material_de_estudo ORDER BY titulo")
        return cursor.fetchall()

    def update(self, id_material, titulo=None, descricao=None, tipo=None, link=None):
        campos, valores = [], []
        for col, val in [("titulo", titulo), ("descricao", descricao), ("tipo", tipo), ("link", link)]:
            if val is not None:
                campos.append(f"{col} = %s"); valores.append(val)
        if not campos:
            return 0
        valores.append(id_material)
        cursor = self._cursor()
        cursor.execute(f"UPDATE material_de_estudo SET {', '.join(campos)} WHERE id = %s", valores)
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_material):
        cursor = self._cursor()
        cursor.execute("DELETE FROM material_de_estudo WHERE id = %s", (id_material,))
        self.conn.commit()
        return cursor.rowcount
