class BaseRepository:
    def __init__(self, connection):
        self.conn = connection

    def _cursor(self):
        return self.conn.cursor(dictionary=True)
