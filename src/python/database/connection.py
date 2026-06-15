import mysql.connector
from database.config import get_db_config


def get_connection():
    return mysql.connector.connect(**get_db_config())


if __name__ == "__main__":
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION(), DATABASE()")
    version, db = cursor.fetchone()
    print(f"Conectado com sucesso!")
    print(f"  MySQL versão : {version}")
    print(f"  Banco de dados: {db}")
    cursor.close()
    conn.close()
