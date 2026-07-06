# rotas/demo.py
# Painel de Demonstração de Requisitos — exercita ao vivo, dentro do app,
# cada item obrigatório da especificação do projeto:
#   - Chave primária automática (AUTO_INCREMENT)
#   - View (vw_historico_aluno)
#   - Procedure (sp_matricular_aluno_em_turma)
#   - Trigger (tg_atualiza_nota_final_insert/update)
#   - CRUD multi-tabela com integridade referencial
#
# Todas as ações que alteram dados são reversíveis por um botão "desfazer",
# para não sujar os dados de seed usados no restante da aplicação.

import datetime
import mysql.connector
from flask import Blueprint, render_template, request, redirect, url_for, flash

from database.connection import get_connection
from repositories.pessoa_repository import PessoaRepository
from repositories.aluno_repository import AlunoRepository
from repositories.matricula_curso_repository import MatriculaCursoRepository
from repositories.turma_repository import TurmaRepository
from repositories.oferta_repository import OfertaRepository
from repositories.avaliacao_repository import AvaliacaoRepository
from repositories.matricula_disciplina_repository import MatriculaDisciplinaRepository
from repositories.resultado_avaliacao_repository import ResultadoAvaliacaoRepository
from services.matricula_service import matricular_aluno_em_disciplina

demo_bp = Blueprint('demo', __name__, url_prefix='/demo')

CPF_PREFIXO_DEMO = '999'  # cpfs de demonstração começam com 999 para serem fáceis de identificar/limpar


# ════════════════════════════════════════════════════════════════════════
# PAINEL PRINCIPAL
# ════════════════════════════════════════════════════════════════════════
@demo_bp.route('/')
def painel():
    return render_template('demo/painel.html')


# ════════════════════════════════════════════════════════════════════════
# 1. CHAVE PRIMÁRIA AUTOMÁTICA (AUTO_INCREMENT)
# ════════════════════════════════════════════════════════════════════════
@demo_bp.route('/chave-primaria', methods=['GET', 'POST'])
def chave_primaria():
    conn = get_connection()
    resultado = None

    if request.method == 'POST':
        nome = f"Pessoa Demo {datetime.datetime.now().strftime('%H:%M:%S')}"
        cpf = CPF_PREFIXO_DEMO + datetime.datetime.now().strftime('%H%M%S%f')[:8]
        pessoa_repo = PessoaRepository(conn)
        # Note: não informamos "id" — o MySQL gera sozinho via AUTO_INCREMENT
        id_gerado = pessoa_repo.create(nome, cpf, 'F', datetime.date(2000, 1, 1))
        resultado = {"id_gerado": id_gerado, "nome": nome, "cpf": cpf}
        flash(f'Registro criado sem informar ID — MySQL gerou automaticamente: id = {id_gerado}', 'success')

    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, nome, cpf FROM pessoa WHERE cpf LIKE %s ORDER BY id DESC",
        (CPF_PREFIXO_DEMO + '%',),
    )
    demos = cursor.fetchall()
    conn.close()
    return render_template('demo/chave_primaria.html', resultado=resultado, demos=demos)


@demo_bp.route('/chave-primaria/<int:id_pessoa>/excluir', methods=['POST'])
def chave_primaria_excluir(id_pessoa):
    conn = get_connection()
    PessoaRepository(conn).delete(id_pessoa)
    conn.close()
    flash('Registro de demonstração removido.', 'success')
    return redirect(url_for('demo.chave_primaria'))


# ════════════════════════════════════════════════════════════════════════
# 2. VIEW — vw_historico_aluno
# ════════════════════════════════════════════════════════════════════════
@demo_bp.route('/view-historico')
def view_historico():
    conn = get_connection()
    aluno_repo = AlunoRepository(conn)
    alunos = aluno_repo.find_all()

    id_pessoa = request.args.get('id_pessoa', type=int)
    linhas = []
    if id_pessoa:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM vw_historico_aluno WHERE id_pessoa = %s ORDER BY semestre DESC",
            (id_pessoa,),
        )
        linhas = cursor.fetchall()
    conn.close()

    sql_executado = (
        "SELECT * FROM vw_historico_aluno WHERE id_pessoa = %s ORDER BY semestre DESC;"
        % (id_pessoa if id_pessoa else '<selecione um aluno>')
    )
    return render_template(
        'demo/view_historico.html',
        alunos=alunos,
        linhas=linhas,
        id_pessoa=id_pessoa,
        sql_executado=sql_executado,
    )


# ════════════════════════════════════════════════════════════════════════
# 3. PROCEDURE — sp_matricular_aluno_em_turma
# ════════════════════════════════════════════════════════════════════════
@demo_bp.route('/procedure', methods=['GET', 'POST'])
def procedure():
    conn = get_connection()
    mc_repo = MatriculaCursoRepository(conn)
    turma_repo = TurmaRepository(conn)
    matriculas_curso = mc_repo.find_all()
    turmas = turma_repo.find_all()

    resultado = None
    erro = None

    if request.method == 'POST':
        id_matricula_curso = request.form.get('id_matricula_curso', type=int)
        id_turma = request.form.get('id_turma', type=int)

        try:
            cursor = conn.cursor()
            cursor.callproc('sp_matricular_aluno_em_turma', [id_matricula_curso, id_turma])
            id_gerado = None
            for stored_result in cursor.stored_results():
                row = stored_result.fetchone()
                if row:
                    id_gerado = row[0]
            conn.commit()
            resultado = {
                "id_matricula_disciplina": id_gerado,
                "id_matricula_curso": id_matricula_curso,
                "id_turma": id_turma,
            }
            flash(f'Procedure executada com sucesso — matrícula criada (id = {id_gerado}).', 'success')
        except mysql.connector.Error as e:
            conn.rollback()
            erro = e.msg
            flash(f'Procedure bloqueou a operação: {erro}', 'danger')

    conn.close()
    return render_template(
        'demo/procedure.html',
        matriculas_curso=matriculas_curso,
        turmas=turmas,
        resultado=resultado,
        erro=erro,
    )


@demo_bp.route('/procedure/<int:id_matricula_disciplina>/desfazer', methods=['POST'])
def procedure_desfazer(id_matricula_disciplina):
    conn = get_connection()
    MatriculaDisciplinaRepository(conn).delete(id_matricula_disciplina)
    conn.close()
    flash('Matrícula de demonstração removida.', 'success')
    return redirect(url_for('demo.procedure'))


# ════════════════════════════════════════════════════════════════════════
# 4. TRIGGER — tg_atualiza_nota_final_insert / _update
# ════════════════════════════════════════════════════════════════════════
@demo_bp.route('/trigger', methods=['GET', 'POST'])
def trigger():
    conn = get_connection()
    md_repo = MatriculaDisciplinaRepository(conn)
    av_repo = AvaliacaoRepository(conn)
    matriculas = md_repo.find_all()
    avaliacoes = av_repo.find_all()

    comparacao = None

    if request.method == 'POST':
        id_matricula_disciplina = request.form.get('id_matricula_disciplina', type=int)
        id_avaliacao = request.form.get('id_avaliacao', type=int)
        nota = request.form.get('nota', type=float)

        antes = md_repo.find_by_id(id_matricula_disciplina)
        nota_antes = antes['nota'] if antes else None

        ra_repo = ResultadoAvaliacaoRepository(conn)
        id_resultado = ra_repo.create(
            id_avaliacao=id_avaliacao,
            id_matricula_disciplina=id_matricula_disciplina,
            nota=nota,
            status='CORRIGIDO',
            data_entrega=datetime.date.today(),
        )

        depois = md_repo.find_by_id(id_matricula_disciplina)
        nota_depois = depois['nota'] if depois else None

        comparacao = {
            "id_resultado": id_resultado,
            "id_matricula_disciplina": id_matricula_disciplina,
            "nota_antes": nota_antes,
            "nota_depois": nota_depois,
        }
        flash(
            f'Trigger disparou automaticamente: nota_final foi de {nota_antes} para {nota_depois} '
            f'sem nenhum UPDATE manual.', 'success'
        )

    conn.close()
    return render_template(
        'demo/trigger.html',
        matriculas=matriculas,
        avaliacoes=avaliacoes,
        comparacao=comparacao,
    )


@demo_bp.route('/trigger/<int:id_resultado>/desfazer', methods=['POST'])
def trigger_desfazer(id_resultado):
    conn = get_connection()
    ResultadoAvaliacaoRepository(conn).delete(id_resultado)
    conn.close()
    flash(
        'Resultado de demonstração removido. Obs: a nota final não volta sozinha '
        '(não existe trigger de DELETE) — se quiser restaurar o valor original, '
        'edite a nota de outro resultado da mesma matrícula para forçar o recálculo.',
        'info',
    )
    return redirect(url_for('demo.trigger'))


# ════════════════════════════════════════════════════════════════════════
# 5. CRUD MULTI-TABELA — matricular_aluno_em_disciplina
# ════════════════════════════════════════════════════════════════════════
@demo_bp.route('/multitabela', methods=['GET', 'POST'])
def multitabela():
    conn = get_connection()
    aluno_repo = AlunoRepository(conn)
    oferta_repo = OfertaRepository(conn)
    alunos = aluno_repo.find_all()
    ofertas = oferta_repo.find_all()
    conn.close()

    resultado = None

    if request.method == 'POST':
        id_pessoa = request.form.get('id_pessoa', type=int)
        id_oferta = request.form.get('id_oferta', type=int)
        resultado = matricular_aluno_em_disciplina(id_pessoa, id_oferta)
        if resultado['ok']:
            flash(
                f"Função tocou 4 tabelas numa operação só (aluno → matricula_curso → "
                f"turma → matricula_disciplina). ID gerado: {resultado['id_matricula_disciplina']}",
                'success',
            )
        else:
            flash(f"Integridade referencial validada — bloqueado: {resultado['erro']}", 'danger')

    return render_template('demo/multitabela.html', alunos=alunos, ofertas=ofertas, resultado=resultado)


@demo_bp.route('/multitabela/<int:id_matricula_disciplina>/desfazer', methods=['POST'])
def multitabela_desfazer(id_matricula_disciplina):
    conn = get_connection()
    MatriculaDisciplinaRepository(conn).delete(id_matricula_disciplina)
    conn.close()
    flash('Matrícula de demonstração removida.', 'success')
    return redirect(url_for('demo.multitabela'))
