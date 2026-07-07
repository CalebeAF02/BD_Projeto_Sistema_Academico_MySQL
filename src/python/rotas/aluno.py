# rotas/aluno.py
# Painel Geral do Aluno — resumo do semestre, frequência, alertas de
# nota e metas de estudo. Página inicial de quem loga como ALUNO.

from flask import Blueprint, render_template, session

from services.aluno_dashboard_service import montar_painel_aluno

aluno_bp = Blueprint('aluno', __name__, url_prefix='/aluno')


@aluno_bp.route('/painel')
def painel():
    # Acesso restrito a contas ALUNO é garantido pelo guard em app.py
    # (BLUEPRINTS_SOMENTE_ALUNO), não precisa checar de novo aqui.
    dados = montar_painel_aluno(session['id_pessoa'])
    return render_template('aluno/painel.html', **dados)
