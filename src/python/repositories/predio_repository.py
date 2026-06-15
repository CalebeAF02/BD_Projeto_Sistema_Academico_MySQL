from repositories.base_repository import BaseRepository


class PredioRepository(BaseRepository):

    def create(self, id_departamento, nome, **endereco):
        cursor = self._cursor()
        cursor.execute(
            """INSERT INTO predio (id_departamento, nome, rua, numero, conjunto, ql, quadra, bairro, cidade, estado, cep)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (id_departamento, nome,
             endereco.get("rua"), endereco.get("numero"), endereco.get("conjunto"),
             endereco.get("ql"), endereco.get("quadra"), endereco.get("bairro"),
             endereco.get("cidade"), endereco.get("estado"), endereco.get("cep")),
        )
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_predio):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM predio WHERE id = %s", (id_predio,))
        return cursor.fetchone()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM predio ORDER BY nome")
        return cursor.fetchall()

    def update(self, id_predio, nome=None, **endereco):
        campos, valores = [], []
        if nome is not None:
            campos.append("nome = %s"); valores.append(nome)
        for col in ("rua", "numero", "conjunto", "ql", "quadra", "bairro", "cidade", "estado", "cep"):
            if col in endereco:
                campos.append(f"{col} = %s"); valores.append(endereco[col])
        if not campos:
            return 0
        valores.append(id_predio)
        cursor = self._cursor()
        cursor.execute(f"UPDATE predio SET {', '.join(campos)} WHERE id = %s", valores)
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_predio):
        cursor = self._cursor()
        cursor.execute("DELETE FROM predio WHERE id = %s", (id_predio,))
        self.conn.commit()
        return cursor.rowcount
