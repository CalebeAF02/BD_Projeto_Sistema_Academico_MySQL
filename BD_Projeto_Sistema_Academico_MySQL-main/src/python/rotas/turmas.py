# rotas/turmas.py
# Blueprint de turmas — CRUD completo.

from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.connection import get_connection

turmas_bp = Blueprint('turmas', __name__, url_prefix='/turmas')


# ── Helpers ────────────────────────────────────────────────────────────

def _get_turma(id_turma: int) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT t.id, t.codigo, t.quantidade_vagas,
               o.id AS id_oferta, o.codigo_oferta,
               d.id AS id_disciplina, d.nome AS disciplina, d.codigo AS codigo_disciplina,
               s.id AS id_semestre, s.nome AS semestre,
               c.id AS id_curso, c.nome AS curso, c.sigla AS sigla_curso,
               dep.nome AS departamento
        FROM turma t
        JOIN oferta o       ON o.id  = t.id_oferta
        JOIN disciplina d   ON d.id  = o.id_disciplina
        JOIN semestre s     ON s.id  = o.id_semestre
        JOIN curso c        ON c.id  = o.id_curso
        JOIN departamento dep ON dep.id = o.id_departamento
        WHERE t.id = %s
    """, (id_turma,))
    row = cursor.fetchone()
    conn.close()
    return row


def _get_ofertas():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.id, o.codigo_oferta,
               d.nome AS disciplina, d.codigo AS codigo_disciplina,
               s.nome AS semestre, c.sigla AS curso
        FROM oferta o
        JOIN disciplina d ON d.id = o.id_disciplina
        JOIN semestre   s ON s.id = o.id_semestre
        JOIN curso      c ON c.id = o.id_curso
        ORDER BY s.nome DESC, d.nome
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def _get_alunos_turma(id_turma: int) -> list:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.nome, p.cpf, md.codigo, md.nota, md.status
        FROM matricula_disciplina md
        JOIN matricula_curso mc ON mc.id  = md.id_matricula_curso
        JOIN aluno a            ON a.id_pessoa = mc.id_aluno
        JOIN pessoa p           ON p.id  = a.id_pessoa
        WHERE md.id_turma = %s
        ORDER BY p.nome
    """, (id_turma,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def _get_avaliacoes_turma(id_turma: int) -> list:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT id, titulo, tipo, peso, nota_maxima, data_aplicacao, status
        FROM avaliacao WHERE id_turma = %s ORDER BY data_aplicacao
    """, (id_turma,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def _get_vagas_ocupadas(id_turma: int) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM matricula_disciplina
        WHERE id_turma = %s AND status != 'TRANCADO'
    """, (id_turma,))
    count = cursor.fetchone()[0]
    conn.close()
    return count


# ════════════════════════════════════════════════════════════════════════
# LIST
# ════════════════════════════════════════════════════════════════════════
@turmas_bp.route('/')
def listar():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT t.id, t.codigo, t.quantidade_vagas,
               d.nome AS disciplina, d.codigo AS codigo_disciplina,
               s.nome AS semestre, c.sigla AS curso,
               COUNT(md.id) AS matriculados
        FROM turma t
        JOIN oferta o       ON o.id  = t.id_oferta
        JOIN disciplina d   ON d.id  = o.id_disciplina
        JOIN semestre s     ON s.id  = o.id_semestre
        JOIN curso c        ON c.id  = o.id_curso
        LEFT JOIN matricula_disciplina md
                ON md.id_turma = t.id AND md.status != 'TRANCADO'
        GROUP BY t.id, t.codigo, t.quantidade_vagas,
                 d.nome, d.codigo, s.nome, c.sigla
        ORDER BY s.nome DESC, d.nome
    """)
    turmas = cursor.fetchall()
    conn.close()
    return render_template('turmas/lista.html', turmas=turmas)


# ════════════════════════════════════════════════════════════════════════
# CREATE
# ════════════════════════════════════════════════════════════════════════
@turmas_bp.route('/nova', methods=['GET', 'POST'])
def criar():
    ofertas = _get_ofertas()

    if request.method == 'POST':
        id_oferta = request.form.get('id_oferta', '')
        codigo    = request.form.get('codigo', '').strip().upper()
        vagas     = request.form.get('quantidade_vagas', '')

        erros = []
        if not id_oferta or not id_oferta.isdigit():
            erros.append('Selecione uma oferta.')
        if not codigo:
            erros.append('Código da turma é obrigatório.')
        if not vagas or not vagas.isdigit() or int(vagas) <= 0:
            erros.append('Número de vagas deve ser um inteiro positivo.')

        if erros:
            for e in erros: flash(e, 'danger')
            return render_template('turmas/form.html', modo='criar',
                                   form=request.form, ofertas=ofertas)
        try:
            conn   = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO turma (id_oferta, codigo, quantidade_vagas) VALUES (%s, %s, %s)",
                (int(id_oferta), codigo, int(vagas))
            )
            conn.commit()
            conn.close()
            flash(f'Turma {codigo} criada com sucesso!', 'success')
            return redirect(url_for('turmas.listar'))
        except Exception:
            flash('Erro ao criar turma. O código pode já estar em uso.', 'danger')
            return render_template('turmas/form.html', modo='criar',
                                   form=request.form, ofertas=ofertas)

    return render_template('turmas/form.html', modo='criar', form={}, ofertas=ofertas)


# ════════════════════════════════════════════════════════════════════════
# READ
# ════════════════════════════════════════════════════════════════════════
@turmas_bp.route('/<int:id_turma>')
def ver(id_turma):
    turma = _get_turma(id_turma)
    if not turma:
        flash('Turma não encontrada.', 'danger')
        return redirect(url_for('turmas.listar'))

    alunos      = _get_alunos_turma(id_turma)
    avaliacoes  = _get_avaliacoes_turma(id_turma)
    matriculados = _get_vagas_ocupadas(id_turma)

    return render_template('turmas/detalhe.html',
                           turma=turma,
                           alunos=alunos,
                           avaliacoes=avaliacoes,
                           matriculados=matriculados)


# ════════════════════════════════════════════════════════════════════════
# UPDATE
# ════════════════════════════════════════════════════════════════════════
@turmas_bp.route('/<int:id_turma>/editar', methods=['GET', 'POST'])
def editar(id_turma):
    turma   = _get_turma(id_turma)
    ofertas = _get_ofertas()

    if not turma:
        flash('Turma não encontrada.', 'danger')
        return redirect(url_for('turmas.listar'))

    if request.method == 'POST':
        codigo = request.form.get('codigo', '').strip().upper()
        vagas  = request.form.get('quantidade_vagas', '')

        erros = []
        if not codigo:
            erros.append('Código é obrigatório.')
        if not vagas or not vagas.isdigit() or int(vagas) <= 0:
            erros.append('Número de vagas deve ser um inteiro positivo.')

        if erros:
            for e in erros: flash(e, 'danger')
            return render_template('turmas/form.html', modo='editar',
                                   turma=turma, form=request.form, ofertas=ofertas)
        try:
            conn   = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE turma SET codigo = %s, quantidade_vagas = %s WHERE id = %s",
                (codigo, int(vagas), id_turma)
            )
            conn.commit()
            conn.close()
            flash(f'Turma {codigo} atualizada com sucesso!', 'success')
            return redirect(url_for('turmas.ver', id_turma=id_turma))
        except Exception:
            flash('Erro ao atualizar. O código pode já estar em uso.', 'danger')
            return render_template('turmas/form.html', modo='editar',
                                   turma=turma, form=request.form, ofertas=ofertas)

    return render_template('turmas/form.html', modo='editar',
                           turma=turma, form=turma, ofertas=ofertas)


# ════════════════════════════════════════════════════════════════════════
# DELETE
# ════════════════════════════════════════════════════════════════════════
@turmas_bp.route('/<int:id_turma>/deletar', methods=['POST'])
def deletar(id_turma):
    turma = _get_turma(id_turma)
    if not turma:
        flash('Turma não encontrada.', 'danger')
        return redirect(url_for('turmas.listar'))
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM turma WHERE id = %s", (id_turma,))
        conn.commit()
        conn.close()
        flash(f'Turma {turma["codigo"]} removida.', 'success')
    except Exception:
        flash('Erro ao remover. A turma pode ter alunos matriculados.', 'danger')
    return redirect(url_for('turmas.listar'))
