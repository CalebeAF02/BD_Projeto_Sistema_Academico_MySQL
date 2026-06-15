from repositories.base_repository import BaseRepository


class ProfessorRepository(BaseRepository):

    def create(self, id_pessoa, id_departamento, tipo="EFETIVO", nivel="ADJUNTO"):
        cursor = self._cursor()
        cursor.execute(
            "INSERT INTO professor (id_pessoa, id_departamento, tipo, nivel) VALUES (%s, %s, %s, %s)",
            (id_pessoa, id_departamento, tipo, nivel),
        )
        self.conn.commit()
        return id_pessoa

    def find_by_id(self, id_pessoa):
        cursor = self._cursor()
        cursor.execute(
            """SELECT pr.id_pessoa, p.nome, p.cpf, pr.tipo, pr.nivel, d.nome AS departamento
               FROM professor pr
               JOIN pessoa p ON p.id = pr.id_pessoa
               JOIN departamento d ON d.id = pr.id_departamento
               WHERE pr.id_pessoa = %s""",
            (id_pessoa,),
        )
        return cursor.fetchone()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute(
            """SELECT pr.id_pessoa, p.nome, pr.tipo, pr.nivel, d.nome AS departamento
               FROM professor pr
               JOIN pessoa p ON p.id = pr.id_pessoa
               JOIN departamento d ON d.id = pr.id_departamento
               ORDER BY p.nome"""
        )
        return cursor.fetchall()

    def update(self, id_pessoa, id_departamento=None, tipo=None, nivel=None):
        campos, valores = [], []
        if id_departamento is not None:
            campos.append("id_departamento = %s"); valores.append(id_departamento)
        if tipo is not None:
            campos.append("tipo = %s"); valores.append(tipo)
        if nivel is not None:
            campos.append("nivel = %s"); valores.append(nivel)
        if not campos:
            return 0
        valores.append(id_pessoa)
        cursor = self._cursor()
        cursor.execute(f"UPDATE professor SET {', '.join(campos)} WHERE id_pessoa = %s", valores)
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_pessoa):
        cursor = self._cursor()
        cursor.execute("DELETE FROM professor WHERE id_pessoa = %s", (id_pessoa,))
        self.conn.commit()
        return cursor.rowcount
