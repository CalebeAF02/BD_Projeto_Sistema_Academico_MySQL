from repositories.base_repository import BaseRepository


class ContaRepository(BaseRepository):

    def create(self, id_pessoa, email, senha, tipo, status="ATIVA"):
        cursor = self._cursor()
        cursor.execute(
            "INSERT INTO conta (id_pessoa, email, senha, tipo, status) VALUES (%s, %s, %s, %s, %s)",
            (id_pessoa, email, senha, tipo, status),
        )
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_conta):
        cursor = self._cursor()
        cursor.execute("SELECT id, id_pessoa, email, tipo, status, data_criacao FROM conta WHERE id = %s", (id_conta,))
        return cursor.fetchone()

    def find_by_email(self, email):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM conta WHERE email = %s", (email,))
        return cursor.fetchone()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute("SELECT id, id_pessoa, email, tipo, status, data_criacao FROM conta ORDER BY data_criacao DESC")
        return cursor.fetchall()

    def update(self, id_conta, email=None, senha=None, status=None):
        campos, valores = [], []
        if email is not None:
            campos.append("email = %s"); valores.append(email)
        if senha is not None:
            campos.append("senha = %s"); valores.append(senha)
        if status is not None:
            campos.append("status = %s"); valores.append(status)
        if not campos:
            return 0
        valores.append(id_conta)
        cursor = self._cursor()
        cursor.execute(f"UPDATE conta SET {', '.join(campos)} WHERE id = %s", valores)
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_conta):
        cursor = self._cursor()
        cursor.execute("DELETE FROM conta WHERE id = %s", (id_conta,))
        self.conn.commit()
        return cursor.rowcount
