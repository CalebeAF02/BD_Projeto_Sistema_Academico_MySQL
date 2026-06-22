# rotas/disciplinas.py
# Blueprint de disciplinas — CRUD completo + materiais de estudo vinculados.

from flask import Blueprint, render_template, request, redirect, url_for, flash
from database.connection import get_connection
from validators import (
    sanitize_str,
    validate_disciplina_form,
    validate_material_form,
    TIPOS_MATERIAL,
)

disciplinas_bp = Blueprint('disciplinas', __name__, url_prefix='/disciplinas')


# ── Helpers ────────────────────────────────────────────────────────────

def _get_disciplina(id_disciplina: int) -> dict | None:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM disciplina WHERE id = %s", (id_disciplina,))
    row = cursor.fetchone()
    conn.close()
    return row


def _get_materiais(id_disciplina: int) -> list:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM material_de_estudo WHERE id_disciplina = %s ORDER BY titulo",
        (id_disciplina,)
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


# ════════════════════════════════════════════════════════════════════════
# LIST
# ════════════════════════════════════════════════════════════════════════
@disciplinas_bp.route('/')
def listar():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT d.id, d.codigo, d.nome,
               COUNT(m.id) AS total_materiais
        FROM disciplina d
        LEFT JOIN material_de_estudo m ON m.id_disciplina = d.id
        GROUP BY d.id, d.codigo, d.nome
        ORDER BY d.codigo
    """)
    disciplinas = cursor.fetchall()
    conn.close()
    return render_template('disciplinas/lista.html', disciplinas=disciplinas)


# ════════════════════════════════════════════════════════════════════════
# CREATE
# ════════════════════════════════════════════════════════════════════════
@disciplinas_bp.route('/nova', methods=['GET', 'POST'])
def criar():
    if request.method == 'POST':
        form  = request.form.to_dict()
        erros = validate_disciplina_form(form)

        if erros:
            for e in erros:
                flash(e, 'danger')
            return render_template('disciplinas/form.html', modo='criar', form=form)

        try:
            codigo = sanitize_str(form['codigo'], 20).upper()
            nome   = sanitize_str(form['nome'], 150)
            conn   = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO disciplina (codigo, nome) VALUES (%s, %s)",
                (codigo, nome)
            )
            conn.commit()
            conn.close()
            flash(f'Disciplina {codigo} cadastrada com sucesso!', 'success')
            return redirect(url_for('disciplinas.listar'))
        except Exception:
            flash('Erro ao cadastrar. O código pode já estar em uso.', 'danger')
            return render_template('disciplinas/form.html', modo='criar', form=form)

    return render_template('disciplinas/form.html', modo='criar', form={})


# ════════════════════════════════════════════════════════════════════════
# READ (detalhe + materiais)
# ════════════════════════════════════════════════════════════════════════
@disciplinas_bp.route('/<int:id_disciplina>')
def ver(id_disciplina):
    disciplina = _get_disciplina(id_disciplina)
    if not disciplina:
        flash('Disciplina não encontrada.', 'danger')
        return redirect(url_for('disciplinas.listar'))
    materiais = _get_materiais(id_disciplina)
    return render_template('disciplinas/detalhe.html',
                           disciplina=disciplina,
                           materiais=materiais,
                           tipos_material=TIPOS_MATERIAL)


# ════════════════════════════════════════════════════════════════════════
# UPDATE
# ════════════════════════════════════════════════════════════════════════
@disciplinas_bp.route('/<int:id_disciplina>/editar', methods=['GET', 'POST'])
def editar(id_disciplina):
    disciplina = _get_disciplina(id_disciplina)
    if not disciplina:
        flash('Disciplina não encontrada.', 'danger')
        return redirect(url_for('disciplinas.listar'))

    if request.method == 'POST':
        form  = request.form.to_dict()
        erros = validate_disciplina_form(form)

        if erros:
            for e in erros:
                flash(e, 'danger')
            return render_template('disciplinas/form.html',
                                   modo='editar', disciplina=disciplina, form=form)

        try:
            codigo = sanitize_str(form['codigo'], 20).upper()
            nome   = sanitize_str(form['nome'], 150)
            conn   = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE disciplina SET codigo = %s, nome = %s WHERE id = %s",
                (codigo, nome, id_disciplina)
            )
            conn.commit()
            conn.close()
            flash(f'Disciplina {codigo} atualizada com sucesso!', 'success')
            return redirect(url_for('disciplinas.ver', id_disciplina=id_disciplina))
        except Exception:
            flash('Erro ao atualizar. O código pode já estar em uso.', 'danger')
            return render_template('disciplinas/form.html',
                                   modo='editar', disciplina=disciplina, form=form)

    return render_template('disciplinas/form.html',
                           modo='editar', disciplina=disciplina, form=disciplina)


# ════════════════════════════════════════════════════════════════════════
# DELETE
# ════════════════════════════════════════════════════════════════════════
@disciplinas_bp.route('/<int:id_disciplina>/deletar', methods=['POST'])
def deletar(id_disciplina):
    disciplina = _get_disciplina(id_disciplina)
    if not disciplina:
        flash('Disciplina não encontrada.', 'danger')
        return redirect(url_for('disciplinas.listar'))
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM disciplina WHERE id = %s", (id_disciplina,))
        conn.commit()
        conn.close()
        flash(f'Disciplina {disciplina["codigo"]} removida.', 'success')
    except Exception:
        flash('Erro ao remover. A disciplina pode ter ofertas ou materiais vinculados.', 'danger')
    return redirect(url_for('disciplinas.listar'))


# ════════════════════════════════════════════════════════════════════════
# MATERIAIS — CREATE
# ════════════════════════════════════════════════════════════════════════
@disciplinas_bp.route('/<int:id_disciplina>/materiais/novo', methods=['POST'])
def criar_material(id_disciplina):
    disciplina = _get_disciplina(id_disciplina)
    if not disciplina:
        flash('Disciplina não encontrada.', 'danger')
        return redirect(url_for('disciplinas.listar'))

    form  = request.form.to_dict()
    erros = validate_material_form(form)

    if erros:
        for e in erros:
            flash(e, 'danger')
        return redirect(url_for('disciplinas.ver', id_disciplina=id_disciplina))

    try:
        titulo    = sanitize_str(form.get('titulo', ''), 100)
        descricao = sanitize_str(form.get('descricao', ''), 500)
        tipo      = sanitize_str(form.get('tipo', ''))
        link      = sanitize_str(form.get('link', ''), 500)

        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO material_de_estudo
               (id_disciplina, titulo, descricao, tipo, link)
               VALUES (%s, %s, %s, %s, %s)""",
            (id_disciplina, titulo, descricao, tipo, link)
        )
        conn.commit()
        conn.close()
        flash(f'Material "{titulo}" adicionado com sucesso!', 'success')
    except Exception:
        flash('Erro ao adicionar material.', 'danger')

    return redirect(url_for('disciplinas.ver', id_disciplina=id_disciplina))


# ════════════════════════════════════════════════════════════════════════
# MATERIAIS — DELETE
# ════════════════════════════════════════════════════════════════════════
@disciplinas_bp.route('/<int:id_disciplina>/materiais/<int:id_material>/deletar', methods=['POST'])
def deletar_material(id_disciplina, id_material):
    try:
        conn   = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM material_de_estudo WHERE id = %s AND id_disciplina = %s",
            (id_material, id_disciplina)
        )
        conn.commit()
        conn.close()
        flash('Material removido.', 'success')
    except Exception:
        flash('Erro ao remover material.', 'danger')
    return redirect(url_for('disciplinas.ver', id_disciplina=id_disciplina))
