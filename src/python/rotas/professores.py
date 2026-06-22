# rotas/professores.py
# Blueprint de professores — CRUD completo.
# Validação delegada ao validators.py (separação de responsabilidade).
# Queries parametrizadas em todos os acessos ao banco (anti SQL Injection).

import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash

from database.connection import get_connection
from repositories.pessoa_repository import PessoaRepository
from repositories.professor_repository import ProfessorRepository
from validators import (
    sanitize_str,
    sanitize_digits,
    mask_cpf,
    validate_professor_form,
    TIPOS_PROFESSOR,
    NIVEIS_PROFESSOR,
)

professores_bp = Blueprint('professores', __name__, url_prefix='/professores')


# ── Helper interno ─────────────────────────────────────────────────────

def _get_professor(id_pessoa: int) -> dict | None:
    """Busca professor completo por id_pessoa. Retorna None se não existir."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT pr.id_pessoa,
               p.nome,
               p.cpf,
               p.sexo,
               p.data_nascimento,
               pr.tipo,
               pr.nivel,
               pr.id_departamento,
               d.nome AS departamento
        FROM professor pr
        JOIN pessoa      p ON p.id  = pr.id_pessoa
        JOIN departamento d ON d.id = pr.id_departamento
        WHERE pr.id_pessoa = %s
    """, (id_pessoa,))
    row = cursor.fetchone()
    conn.close()
    return row


def _get_departamentos() -> list:
    """Retorna lista de departamentos para popular o <select>."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, nome FROM departamento ORDER BY nome")
    deps = cursor.fetchall()
    conn.close()
    return deps


# ════════════════════════════════════════════════════════════════════════
# LIST
# ════════════════════════════════════════════════════════════════════════
@professores_bp.route('/')
def listar():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT pr.id_pessoa,
               p.nome,
               p.cpf,
               p.sexo,
               pr.tipo,
               pr.nivel,
               d.nome AS departamento
        FROM professor pr
        JOIN pessoa      p ON p.id  = pr.id_pessoa
        JOIN departamento d ON d.id = pr.id_departamento
        ORDER BY p.nome
    """)
    professores = cursor.fetchall()
    conn.close()

    # Mascara CPF antes de enviar ao template (LGPD — minimização)
    for prof in professores:
        prof['cpf_exibido'] = mask_cpf(prof['cpf'])

    return render_template('professores/lista.html', professores=professores)


# ════════════════════════════════════════════════════════════════════════
# CREATE
# ════════════════════════════════════════════════════════════════════════
@professores_bp.route('/novo', methods=['GET', 'POST'])
def criar():
    departamentos = _get_departamentos()

    if request.method == 'POST':
        form = request.form.to_dict()
        erros = validate_professor_form(form, modo='criar')

        if erros:
            for e in erros:
                flash(e, 'danger')
            return render_template('professores/form.html',
                                   modo='criar', form=form,
                                   departamentos=departamentos,
                                   tipos=TIPOS_PROFESSOR,
                                   niveis=NIVEIS_PROFESSOR)

        try:
            nome   = sanitize_str(form['nome'], 150)
            cpf    = sanitize_digits(form['cpf'])
            sexo   = sanitize_str(form['sexo'], 1)
            dt     = datetime.date.fromisoformat(form['data_nascimento'])
            tipo   = sanitize_str(form['tipo'])
            nivel  = sanitize_str(form['nivel'])
            id_dep = int(form['id_departamento'])

            conn   = get_connection()
            p_repo = PessoaRepository(conn)
            pr_repo = ProfessorRepository(conn)

            id_novo = p_repo.create(nome, cpf, sexo, dt)
            pr_repo.create(id_novo, id_dep, tipo, nivel)
            conn.close()

            flash(f'Professor {nome} cadastrado com sucesso!', 'success')
            return redirect(url_for('professores.listar'))

        except Exception:
            # Não expõe detalhes técnicos do banco ao usuário (ISO 27001)
            flash('Erro interno ao cadastrar. Verifique os dados e tente novamente.', 'danger')
            return render_template('professores/form.html',
                                   modo='criar', form=form,
                                   departamentos=departamentos,
                                   tipos=TIPOS_PROFESSOR,
                                   niveis=NIVEIS_PROFESSOR)

    return render_template('professores/form.html',
                           modo='criar', form={},
                           departamentos=departamentos,
                           tipos=TIPOS_PROFESSOR,
                           niveis=NIVEIS_PROFESSOR)


# ════════════════════════════════════════════════════════════════════════
# READ
# ════════════════════════════════════════════════════════════════════════
@professores_bp.route('/<int:id_pessoa>')
def ver(id_pessoa):
    prof = _get_professor(id_pessoa)
    if not prof:
        flash('Professor não encontrado.', 'danger')
        return redirect(url_for('professores.listar'))

    prof['cpf_exibido'] = mask_cpf(prof['cpf'])
    return render_template('professores/detalhe.html', prof=prof)


# ════════════════════════════════════════════════════════════════════════
# UPDATE
# ════════════════════════════════════════════════════════════════════════
@professores_bp.route('/<int:id_pessoa>/editar', methods=['GET', 'POST'])
def editar(id_pessoa):
    prof = _get_professor(id_pessoa)
    if not prof:
        flash('Professor não encontrado.', 'danger')
        return redirect(url_for('professores.listar'))

    departamentos = _get_departamentos()

    if request.method == 'POST':
        form = request.form.to_dict()
        erros = validate_professor_form(form, modo='editar')

        if erros:
            for e in erros:
                flash(e, 'danger')
            return render_template('professores/form.html',
                                   modo='editar', prof=prof, form=form,
                                   departamentos=departamentos,
                                   tipos=TIPOS_PROFESSOR,
                                   niveis=NIVEIS_PROFESSOR)

        try:
            nome   = sanitize_str(form['nome'], 150)
            sexo   = sanitize_str(form['sexo'], 1)
            dt     = datetime.date.fromisoformat(form['data_nascimento'])
            tipo   = sanitize_str(form['tipo'])
            nivel  = sanitize_str(form['nivel'])
            id_dep = int(form['id_departamento'])

            conn    = get_connection()
            p_repo  = PessoaRepository(conn)
            pr_repo = ProfessorRepository(conn)

            p_repo.update(id_pessoa, nome=nome, sexo=sexo, data_nascimento=dt)
            pr_repo.update(id_pessoa, id_departamento=id_dep, tipo=tipo, nivel=nivel)
            conn.close()

            flash(f'Professor {nome} atualizado com sucesso!', 'success')
            return redirect(url_for('professores.ver', id_pessoa=id_pessoa))

        except Exception:
            flash('Erro interno ao atualizar. Tente novamente.', 'danger')
            return render_template('professores/form.html',
                                   modo='editar', prof=prof, form=form,
                                   departamentos=departamentos,
                                   tipos=TIPOS_PROFESSOR,
                                   niveis=NIVEIS_PROFESSOR)

    return render_template('professores/form.html',
                           modo='editar', prof=prof, form=prof,
                           departamentos=departamentos,
                           tipos=TIPOS_PROFESSOR,
                           niveis=NIVEIS_PROFESSOR)


# ════════════════════════════════════════════════════════════════════════
# DELETE
# ════════════════════════════════════════════════════════════════════════
@professores_bp.route('/<int:id_pessoa>/deletar', methods=['POST'])
def deletar(id_pessoa):
    prof = _get_professor(id_pessoa)
    if not prof:
        flash('Professor não encontrado.', 'danger')
        return redirect(url_for('professores.listar'))

    try:
        conn    = get_connection()
        pr_repo = ProfessorRepository(conn)
        p_repo  = PessoaRepository(conn)
        pr_repo.delete(id_pessoa)
        p_repo.delete(id_pessoa)
        conn.close()
        flash(f'Professor {prof["nome"]} removido com sucesso.', 'success')
    except Exception:
        flash('Erro ao remover. O professor pode ter vínculos ativos com turmas.', 'danger')

    return redirect(url_for('professores.listar'))
