# rotas/admin.py
# Console Central — visão geral do ecossistema (contadores de usuários,
# turmas abertas, infraestrutura) e atalhos pras ferramentas de admin.
# Página inicial de quem loga como ADMIN.

from flask import Blueprint, render_template

from services.admin_dashboard_service import montar_painel_admin

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/painel')
def painel():
    # Acesso restrito a contas ADMIN já é garantido pelo guard em app.py
    # (BLUEPRINTS_SOMENTE_ADMIN), não precisa checar de novo aqui.
    dados = montar_painel_admin()
    return render_template('admin/painel.html', **dados)
