import os
from flask import Flask, render_template

# 1. Configuração de caminhos para o Windows (Saindo de python/ e indo para src/)
CORRENTE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CORRENTE_DIR)

TEMPLATE_DIR = os.path.join(BASE_DIR, "interface", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "interface", "css")

app = Flask(__name__, 
            template_folder=TEMPLATE_DIR, 
            static_folder=STATIC_DIR, 
            static_url_path='/css')

# 2. Importações do seu Back-end (O que já veio pronto no seu projeto)
from database.connection import get_connection
from repositories.aluno_repository import AlunoRepository
from services.matricula_service import buscar_historico_aluno

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/alunos')
def listar_alunos():
    # Abre a conexão com o banco
    conn = get_connection()
    repo = AlunoRepository(conn)
    
    # Busca a lista de alunos (Usa o método find_all() da documentação)
    lista_de_alunos = repo.find_all()
    
    # Fecha a conexão para não travar o banco
    conn.close()
    
    # Envia os dados para a tela alunos.html
    return render_template('alunos.html', alunos=lista_de_alunos)

@app.route('/testar')
def rodar_teste_rapido():
    try:
        conn = get_connection()
        conn.close()
        return "<h3>Conexão com o banco efetuada com sucesso! [OK]</h3><a href='/'>Voltar</a>"
    except Exception as e:
        return f"<h3>Falha ao conectar no banco: {str(e)}</h3><a href='/'>Voltar</a>"

if __name__ == '__main__':
    app.run(debug=True)