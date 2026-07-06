# services/console_service.py
# Executa consultas somente-leitura vindas do "Console SQL" (área do
# desenvolvedor) e normaliza o resultado em colunas/linhas para o template.

import mysql.connector
from database.connection import get_connection

LIMITE_LINHAS_EXIBIDAS = 200


def executar_consulta(query: str) -> dict:
    """
    Executa a consulta (já validada por validators.validate_console_query)
    e retorna:
      {"ok": True, "colunas": [...], "linhas": [...], "truncado": bool, "linhas_afetadas": int}
      {"ok": False, "erro": "..."}
    """
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query.strip().rstrip(';'))

        colunas = []
        linhas = []
        linhas_afetadas = cursor.rowcount if cursor.rowcount and cursor.rowcount > 0 else 0

        if cursor.description:
            colunas = [d[0] for d in cursor.description]
            linhas = cursor.fetchall()
        else:
            # CALL a uma procedure retorna result sets via stored_results()
            for resultado in cursor.stored_results():
                linhas = resultado.fetchall()
                if resultado.description:
                    colunas = [d[0] for d in resultado.description]

        conn.commit()  # necessário caso a query seja um CALL que grava dado

        truncado = len(linhas) > LIMITE_LINHAS_EXIBIDAS
        if truncado:
            linhas = linhas[:LIMITE_LINHAS_EXIBIDAS]

        return {
            "ok": True,
            "colunas": colunas,
            "linhas": linhas,
            "truncado": truncado,
            "linhas_afetadas": linhas_afetadas,
        }

    except mysql.connector.Error as e:
        conn.rollback()
        return {"ok": False, "erro": str(e.msg)}
    except Exception as e:
        conn.rollback()
        return {"ok": False, "erro": str(e)}
    finally:
        conn.close()
