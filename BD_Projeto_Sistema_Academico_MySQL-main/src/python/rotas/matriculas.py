# rotas/matriculas.py
# Blueprint de matrículas.
# Usa vw_historico_aluno (View) e sp_matricular_aluno_em_turma (Procedure).

from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.connection import get_connection
from services.matricula_service import matricular_aluno_em_disciplina, buscar_historico_aluno

matriculas_bp = Blueprint('matriculas', __name__, url_prefix='/matriculas')


# ── Helpers ────────────────────────────────────────────────────────────

def _get_alunos_com_matricula():
    """Lista todos os alunos com sua matrícula em curso ativa."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.id, p.nome, mc.codigo AS matricula, mc.status,
               c.nome AS curso, c.sigla, mc.id AS id_matricula_curso
        FROM pessoa p
        JOIN aluno a         ON a.id_pessoa   = p.id
        JOIN matricula_curso mc ON mc.id_aluno = a.id_pessoa
        JOIN curso c         ON c.id          = mc.id_curso
        WHERE mc.status = 'ATIVA'
        ORDER BY p.nome
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def _get_ofertas_disponiveis():
    """Lista ofertas do semestre atual com vagas disponíveis."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT o.id AS id_oferta,
               d.nome AS disciplina,
               d.codigo AS codigo_disciplina,
               t.id AS id_turma,
               t.codigo AS turma,
               t.quantidade_vagas,
               s.nome AS semestre,
               COUNT(md.id) AS matriculados
        FROM oferta o
        JOIN disciplina d ON d.id = o.id_disciplina
        JOIN semestre   s ON s.id = o.id_semestre
        JOIN turma      t ON t.id_oferta = o.id
        LEFT JOIN matricula_disciplina md
               ON md.id_turma = t.id AND md.status != 'TRANCADO'
        WHERE s.nome = '2026/1'
        GROUP BY o.id, d.nome, d.codigo, t.id, t.codigo,
                 t.quantidade_vagas, s.nome
        HAVING matriculados < t.quantidade_vagas
        ORDER BY d.nome
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


# ════════════════════════════════════════════════════════════════════════
# LIST — todos os alunos com matrícula ativa
# ════════════════════════════════════════════════════════════════════════
@matriculas_bp.route('/')
def listar():
    alunos = _get_alunos_com_matricula()
    return render_template('matriculas/lista.html', alunos=alunos)


# ════════════════════════════════════════════════════════════════════════
# READ — histórico do aluno via VIEW vw_historico_aluno
# ════════════════════════════════════════════════════════════════════════
@matriculas_bp.route('/aluno/<int:id_pessoa>')
def historico(id_pessoa):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT p.nome, p.id
        FROM pessoa p WHERE p.id = %s
    """, (id_pessoa,))
    pessoa = cursor.fetchone()
    conn.close()

    if not pessoa:
        flash('Aluno não encontrado.', 'danger')
        return redirect(url_for('matriculas.listar'))

    # Usa a VIEW vw_historico_aluno
    historico = buscar_historico_aluno(id_pessoa)
    ofertas   = _get_ofertas_disponiveis()

    return render_template('matriculas/historico.html',
                           pessoa=pessoa,
                           historico=historico,
                           ofertas=ofertas)


# ════════════════════════════════════════════════════════════════════════
# CREATE — matrícula em disciplina via PROCEDURE
# ════════════════════════════════════════════════════════════════════════
@matriculas_bp.route('/aluno/<int:id_pessoa>/matricular', methods=['POST'])
def matricular(id_pessoa):
    id_oferta = request.form.get('id_oferta', '')

    if not id_oferta or not id_oferta.isdigit():
        flash('Selecione uma oferta válida.', 'danger')
        return redirect(url_for('matriculas.historico', id_pessoa=id_pessoa))

    # Chama a PROCEDURE via matricula_service
    resultado = matricular_aluno_em_disciplina(
        id_pessoa=id_pessoa,
        id_oferta=int(id_oferta)
    )

    if resultado['ok']:
        flash('Matrícula realizada com sucesso!', 'success')
    else:
        flash(f'Erro: {resultado["erro"]}', 'danger')

    return redirect(url_for('matriculas.historico', id_pessoa=id_pessoa))


# ════════════════════════════════════════════════════════════════════════
# UPDATE — trancar disciplina
# ════════════════════════════════════════════════════════════════════════
@matriculas_bp.route('/disciplina/<int:id_md>/trancar', methods=['POST'])
def trancar_disciplina(id_md):
    id_pessoa = request.form.get('id_pessoa', '')
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE matricula_disciplina
            SET status = 'TRANCADO', data_trancamento_disciplina = CURDATE()
            WHERE id = %s AND status = 'MATRICULADO'
        """, (id_md,))
        conn.commit()
        conn.close()
        flash('Disciplina trancada com sucesso.', 'success')
    except Exception:
        flash('Erro ao trancar disciplina.', 'danger')

    return redirect(url_for('matriculas.historico', id_pessoa=id_pessoa))
