from repositories.base_repository import BaseRepository


class PessoaRepository(BaseRepository):

    def create(self, nome, cpf, sexo, data_nascimento, foto=None):
        cursor = self._cursor()
        cursor.execute(
            """INSERT INTO pessoa (nome, cpf, sexo, data_nascimento, foto)
               VALUES (%s, %s, %s, %s, %s)""",
            (nome, cpf, sexo, data_nascimento, foto),
        )
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_pessoa):
        cursor = self._cursor()
        cursor.execute("SELECT id, nome, cpf, sexo, data_nascimento FROM pessoa WHERE id = %s", (id_pessoa,))
        return cursor.fetchone()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute("SELECT id, nome, cpf, sexo, data_nascimento FROM pessoa ORDER BY nome")
        return cursor.fetchall()

    def update(self, id_pessoa, nome=None, sexo=None, data_nascimento=None):
        campos, valores = [], []
        if nome is not None:
            campos.append("nome = %s"); valores.append(nome)
        if sexo is not None:
            campos.append("sexo = %s"); valores.append(sexo)
        if data_nascimento is not None:
            campos.append("data_nascimento = %s"); valores.append(data_nascimento)
        if not campos:
            return 0
        valores.append(id_pessoa)
        cursor = self._cursor()
        cursor.execute(f"UPDATE pessoa SET {', '.join(campos)} WHERE id = %s", valores)
        self.conn.commit()
        return cursor.rowcount

    def update_foto(self, id_pessoa, foto_bytes):
        cursor = self._cursor()
        cursor.execute("UPDATE pessoa SET foto = %s WHERE id = %s", (foto_bytes, id_pessoa))
        self.conn.commit()
        return cursor.rowcount

    def find_foto(self, id_pessoa):
        cursor = self._cursor()
        cursor.execute("SELECT foto FROM pessoa WHERE id = %s", (id_pessoa,))
        row = cursor.fetchone()
        return row["foto"] if row else None

    def delete(self, id_pessoa):
        cursor = self._cursor()
        cursor.execute("DELETE FROM pessoa WHERE id = %s", (id_pessoa,))
        self.conn.commit()
        return cursor.rowcount
