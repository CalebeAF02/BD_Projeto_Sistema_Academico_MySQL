# rotas/professor.py
# Painel Geral do Professor — turmas sob responsabilidade, avaliações
# pendentes de correção e próximos eventos. Página inicial de quem
# loga como PROFESSOR.

from flask import Blueprint, render_template, session

from services.professor_dashboard_service import montar_painel_professor

professor_bp = Blueprint('professor', __name__, url_prefix='/professor')


@professor_bp.route('/painel')
def painel():
    # Acesso restrito a contas PROFESSOR é garantido pelo guard em app.py
    # (BLUEPRINTS_SOMENTE_PROFESSOR), não precisa checar de novo aqui.
    dados = montar_painel_professor(session['id_pessoa'])
    return render_template('professor/painel.html', **dados)
