from repositories.base_repository import BaseRepository


class ProfessorTurmaRepository(BaseRepository):

    def create(self, id_professor, id_turma, funcao="TITULAR", carga_horaria=None, data_inicio=None, data_fim=None):
        cursor = self._cursor()
        cursor.execute(
            """INSERT INTO professor_turma (id_professor, id_turma, funcao, carga_horaria, data_inicio, data_fim)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (id_professor, id_turma, funcao, carga_horaria, data_inicio, data_fim),
        )
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_pt):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM professor_turma WHERE id = %s", (id_pt,))
        return cursor.fetchone()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM professor_turma")
        return cursor.fetchall()

    def update(self, id_pt, funcao=None, carga_horaria=None, data_inicio=None, data_fim=None):
        campos, valores = [], []
        for col, val in [("funcao", funcao), ("carga_horaria", carga_horaria), ("data_inicio", data_inicio), ("data_fim", data_fim)]:
            if val is not None:
                campos.append(f"{col} = %s"); valores.append(val)
        if not campos:
            return 0
        valores.append(id_pt)
        cursor = self._cursor()
        cursor.execute(f"UPDATE professor_turma SET {', '.join(campos)} WHERE id = %s", valores)
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_pt):
        cursor = self._cursor()
        cursor.execute("DELETE FROM professor_turma WHERE id = %s", (id_pt,))
        self.conn.commit()
        return cursor.rowcount
