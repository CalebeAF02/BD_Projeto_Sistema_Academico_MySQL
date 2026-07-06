# rotas/console.py
# "Console SQL" — área do desenvolvedor. Permite rodar consultas
# somente-leitura (SELECT/SHOW/DESCRIBE/EXPLAIN) e CALL de procedures
# diretamente pela interface, como bônus visual da demonstração.
# Validação em validators.validate_console_query bloqueia qualquer
# comando de escrita direta (INSERT/UPDATE/DELETE/DROP/...).

from flask import Blueprint, render_template, request

from services.console_service import executar_consulta
from validators import validate_console_query

console_bp = Blueprint('console', __name__, url_prefix='/console')

CONSULTAS_EXEMPLO = [
    {"titulo": "Ver tabelas do banco", "query": "SHOW TABLES;"},
    {"titulo": "Histórico do aluno (View)", "query": "SELECT nome_aluno, semestre, nome_disciplina, nota_final FROM vw_historico_aluno WHERE id_pessoa = 1;"},
    {"titulo": "Matricular em turma (Procedure)", "query": "CALL sp_matricular_aluno_em_turma(1, 5);"},
    {"titulo": "Notas lançadas", "query": "SELECT id, id_avaliacao, id_matricula_disciplina, nota, status FROM resultado_avaliacao ORDER BY id DESC;"},
]


@console_bp.route('/', methods=['GET', 'POST'])
def index():
    query = ''
    resultado = None

    if request.method == 'POST':
        query = request.form.get('query', '')
        erro_validacao = validate_console_query(query)

        if erro_validacao:
            resultado = {"ok": False, "erro": erro_validacao}
        else:
            resultado = executar_consulta(query)

    return render_template(
        'console/index.html',
        query=query,
        resultado=resultado,
        exemplos=CONSULTAS_EXEMPLO,
    )
