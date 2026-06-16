from repositories.base_repository import BaseRepository


class NotificacaoRepository(BaseRepository):

    def create(self, titulo, tipo, mensagem, descricao=None):
        cursor = self._cursor()
        cursor.execute(
            "INSERT INTO notificacao (titulo, descricao, tipo, mensagem) VALUES (%s, %s, %s, %s)",
            (titulo, descricao, tipo, mensagem),
        )
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_notificacao):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM notificacao WHERE id = %s", (id_notificacao,))
        return cursor.fetchone()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM notificacao ORDER BY data_criacao DESC")
        return cursor.fetchall()

    def update(self, id_notificacao, titulo=None, tipo=None, mensagem=None, descricao=None):
        campos, valores = [], []
        for col, val in [("titulo", titulo), ("tipo", tipo), ("mensagem", mensagem), ("descricao", descricao)]:
            if val is not None:
                campos.append(f"{col} = %s"); valores.append(val)
        if not campos:
            return 0
        valores.append(id_notificacao)
        cursor = self._cursor()
        cursor.execute(f"UPDATE notificacao SET {', '.join(campos)} WHERE id = %s", valores)
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_notificacao):
        cursor = self._cursor()
        cursor.execute("DELETE FROM notificacao WHERE id = %s", (id_notificacao,))
        self.conn.commit()
        return cursor.rowcount


class NotificacaoContaRepository(BaseRepository):

    def create(self, id_conta, id_notificacao):
        cursor = self._cursor()
        cursor.execute(
            "INSERT INTO notificacao_conta (id_conta, id_notificacao) VALUES (%s, %s)",
            (id_conta, id_notificacao),
        )
        self.conn.commit()
        return cursor.lastrowid

    def find_by_id(self, id_nc):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM notificacao_conta WHERE id = %s", (id_nc,))
        return cursor.fetchone()

    def find_all(self):
        cursor = self._cursor()
        cursor.execute("SELECT * FROM notificacao_conta ORDER BY data_envio DESC")
        return cursor.fetchall()

    def marcar_lida(self, id_nc):
        from datetime import datetime
        cursor = self._cursor()
        cursor.execute(
            "UPDATE notificacao_conta SET lida = TRUE, data_recebimento = %s WHERE id = %s",
            (datetime.now(), id_nc),
        )
        self.conn.commit()
        return cursor.rowcount

    def update(self, id_nc, lida=None, mensagem_resposta=None):
        campos, valores = [], []
        if lida is not None:
            campos.append("lida = %s"); valores.append(lida)
        if mensagem_resposta is not None:
            campos.append("mensagem_resposta = %s"); valores.append(mensagem_resposta)
        if not campos:
            return 0
        valores.append(id_nc)
        cursor = self._cursor()
        cursor.execute(f"UPDATE notificacao_conta SET {', '.join(campos)} WHERE id = %s", valores)
        self.conn.commit()
        return cursor.rowcount

    def delete(self, id_nc):
        cursor = self._cursor()
        cursor.execute("DELETE FROM notificacao_conta WHERE id = %s", (id_nc,))
        self.conn.commit()
        return cursor.rowcount
