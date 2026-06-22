from repositories.base_repository import BaseRepository


class AlunoRepository(BaseRepository):

    def create(self, id_pessoa, tipo="GRADUACAO"):
        cursor = self._cursor()
        cursor.execute(
            "INSERT INTO aluno (id_pessoa, tipo) VALUES (%s, %s)",
            (id_pessoa, tipo),
        )
        self.conn.commit()
        return id_pessoa

    def find_by_id(self, id_pessoa):
        cursor = self._cursor()
        cursor.execute(
            """SELECT a.id_pessoa, p.nome, p.cpf, p.sexo, p.data_nascimento, a.tipo
               FROM aluno a JOIN pessoa p ON p.id = a.id_pessoa
               WHERE a.id_pessoa = %s""",
            (id_pessoa,),
        )
        return cursor.fetchone()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute(
            """SELECT a.id_pessoa, p.nome, p.cpf, a.tipo
               FROM aluno a JOIN pessoa p ON p.id = a.id_pessoa
               ORDER BY p.nome"""
        )
        return cursor.fetchall()

    def update(self, id_pessoa, tipo):
        cursor = self._cursor()
        cursor.execute("UPDATE aluno SET tipo = %s WHERE id_pessoa = %s", (tipo, id_pessoa))
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_pessoa):
        cursor = self._cursor()
        cursor.execute("DELETE FROM aluno WHERE id_pessoa = %s", (id_pessoa,))
        self.conn.commit()
        return cursor.rowcount
