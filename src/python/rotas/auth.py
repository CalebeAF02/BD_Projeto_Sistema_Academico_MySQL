# rotas/auth.py
# Blueprint de autenticação — login, logout, registro e redefinição de senha.
# Validação delegada ao validators.py (separação de responsabilidade).
# Sessão de usuário mantida via flask.session (server-side, cookie assinado).

import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session

from services.auth_service import autenticar, registrar_aluno, redefinir_senha
from validators import (
    sanitize_str,
    sanitize_digits,
    validate_login_form,
    validate_registro_form,
    validate_esqueci_senha_form,
)

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# ════════════════════════════════════════════════════════════════════════
# LOGIN
# ════════════════════════════════════════════════════════════════════════
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('id_conta'):
        return redirect(url_for('home'))

    if request.method == 'POST':
        erros = validate_login_form(request.form)
        if erros:
            for e in erros:
                flash(e, 'danger')
            return render_template('auth/login.html', form=request.form)

        email = sanitize_str(request.form.get('email', ''))
        senha = request.form.get('senha', '')

        resultado = autenticar(email, senha)
        if not resultado['ok']:
            flash(resultado['erro'], 'danger')
            return render_template('auth/login.html', form=request.form)

        conta = resultado['conta']
        session['id_conta'] = conta['id']
        session['id_pessoa'] = conta['id_pessoa']
        session['nome'] = conta['nome']
        session['email'] = conta['email']
        session['tipo'] = conta['tipo']

        flash(f'Bem-vindo(a), {conta["nome"]}!', 'success')
        return redirect(url_for('home'))

    return render_template('auth/login.html', form={})


# ════════════════════════════════════════════════════════════════════════
# LOGOUT
# ════════════════════════════════════════════════════════════════════════
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    flash('Sessão encerrada com sucesso.', 'success')
    return redirect(url_for('auth.login'))


# ════════════════════════════════════════════════════════════════════════
# REGISTRO (auto-cadastro de aluno)
# ════════════════════════════════════════════════════════════════════════
@auth_bp.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if session.get('id_conta'):
        return redirect(url_for('home'))

    if request.method == 'POST':
        erros = validate_registro_form(request.form)
        if erros:
            for e in erros:
                flash(e, 'danger')
            return render_template('auth/registrar.html', form=request.form)

        nome  = sanitize_str(request.form.get('nome', ''))
        cpf   = sanitize_digits(request.form.get('cpf', ''))
        sexo  = sanitize_str(request.form.get('sexo', ''))
        data  = sanitize_str(request.form.get('data_nascimento', ''))
        email = sanitize_str(request.form.get('email', ''))
        senha = request.form.get('senha', '')

        resultado = registrar_aluno(
            nome, cpf, sexo, datetime.date.fromisoformat(data), email, senha
        )
        if not resultado['ok']:
            flash(resultado['erro'], 'danger')
            return render_template('auth/registrar.html', form=request.form)

        flash('Cadastro realizado com sucesso! Faça login para continuar.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/registrar.html', form={})


# ════════════════════════════════════════════════════════════════════════
# ESQUECI MINHA SENHA
# ════════════════════════════════════════════════════════════════════════
@auth_bp.route('/esqueci-senha', methods=['GET', 'POST'])
def esqueci_senha():
    if request.method == 'POST':
        erros = validate_esqueci_senha_form(request.form)
        if erros:
            for e in erros:
                flash(e, 'danger')
            return render_template('auth/esqueci_senha.html', form=request.form)

        email = sanitize_str(request.form.get('email', ''))
        cpf   = sanitize_digits(request.form.get('cpf', ''))
        nova_senha = request.form.get('nova_senha', '')

        resultado = redefinir_senha(email, cpf, nova_senha)
        if not resultado['ok']:
            flash(resultado['erro'], 'danger')
            return render_template('auth/esqueci_senha.html', form=request.form)

        flash('Senha redefinida com sucesso! Faça login com a nova senha.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/esqueci_senha.html', form={})
