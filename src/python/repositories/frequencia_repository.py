from repositories.base_repository import BaseRepository


class FrequenciaRepository(BaseRepository):

    def create(self, id_aula, id_matricula_disciplina, presente, data_registro=None, observacao=None):
        cursor = self._cursor()
        cursor.execute(
            "INSERT INTO frequencia (id_aula, id_matricula_disciplina, presente, data_registro, observacao) VALUES (%s, %s, %s, %s, %s)",
            (id_aula, id_matricula_disciplina, presente, data_registro, observacao),
        )
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_frequencia):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM frequencia WHERE id = %s", (id_frequencia,))
        return cursor.fetchone()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM frequencia")
        return cursor.fetchall()

    def update(self, id_frequencia, presente=None, observacao=None):
        campos, valores = [], []
        if presente is not None:
            campos.append("presente = %s"); valores.append(presente)
        if observacao is not None:
            campos.append("observacao = %s"); valores.append(observacao)
        if not campos:
            return 0
        valores.append(id_frequencia)
        cursor = self._cursor()
        cursor.execute(f"UPDATE frequencia SET {', '.join(campos)} WHERE id = %s", valores)
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_frequencia):
        cursor = self._cursor()
        cursor.execute("DELETE FROM frequencia WHERE id = %s", (id_frequencia,))
        self.conn.commit()
        return cursor.rowcount
