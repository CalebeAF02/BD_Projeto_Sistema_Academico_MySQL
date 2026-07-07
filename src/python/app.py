import os
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session

CORRENTE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR      = os.path.dirname(CORRENTE_DIR)
TEMPLATE_DIR  = os.path.join(BASE_DIR, "interface", "templates")
STATIC_DIR    = os.path.join(BASE_DIR, "interface", "css")

app = Flask(__name__,
            template_folder=TEMPLATE_DIR,
            static_folder=STATIC_DIR,
            static_url_path='/css')

app.secret_key = 'sga-unb-2026'

from database.connection import get_connection
from repositories.pessoa_repository import PessoaRepository
from repositories.aluno_repository import AlunoRepository
from rotas.professores import professores_bp
from rotas.disciplinas import disciplinas_bp
from rotas.matriculas import matriculas_bp
from rotas.turmas import turmas_bp
from rotas.auth import auth_bp
from rotas.demo import demo_bp
from rotas.console import console_bp
from rotas.aluno import aluno_bp
from rotas.professor import professor_bp
app.register_blueprint(professores_bp)
app.register_blueprint(disciplinas_bp)
app.register_blueprint(matriculas_bp)
app.register_blueprint(turmas_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(demo_bp)
app.register_blueprint(console_bp)
app.register_blueprint(aluno_bp)
app.register_blueprint(professor_bp)

# ── Guard de autenticação ────────────────────────────────────────────
# Bloqueia acesso a qualquer rota fora de /auth e /css sem sessão ativa.
ENDPOINTS_PUBLICOS = {'auth.login', 'auth.registrar', 'auth.esqueci_senha', 'static'}

# Blueprints restritos a contas tipo ADMIN (procedures/triggers/views e
# o console SQL cru não fazem sentido pro usuário final — aluno/professor
# não devem nem ver esses menus).
BLUEPRINTS_SOMENTE_ADMIN = {'demo', 'console'}
ENDPOINTS_SOMENTE_ADMIN = {'rodar_teste_rapido'}

# Blueprints restritos a contas tipo ALUNO.
BLUEPRINTS_SOMENTE_ALUNO = {'aluno'}

# Blueprints restritos a contas tipo PROFESSOR.
BLUEPRINTS_SOMENTE_PROFESSOR = {'professor'}


@app.before_request
def exigir_login():
    if request.endpoint in ENDPOINTS_PUBLICOS or request.endpoint is None:
        return None
    if not session.get('id_conta'):
        flash('Faça login para continuar.', 'info')
        return redirect(url_for('auth.login'))
    eh_area_admin = (
        request.blueprint in BLUEPRINTS_SOMENTE_ADMIN
        or request.endpoint in ENDPOINTS_SOMENTE_ADMIN
    )
    if eh_area_admin and session.get('tipo') != 'ADMIN':
        flash('Essa área é restrita a contas de administrador.', 'danger')
        return redirect(url_for('home'))
    if request.blueprint in BLUEPRINTS_SOMENTE_ALUNO and session.get('tipo') != 'ALUNO':
        flash('Essa área é exclusiva para contas de aluno.', 'danger')
        return redirect(url_for('home'))
    if request.blueprint in BLUEPRINTS_SOMENTE_PROFESSOR and session.get('tipo') != 'PROFESSOR':
        flash('Essa área é exclusiva para contas de professor.', 'danger')
        return redirect(url_for('home'))
    return None


@app.context_processor
def injetar_usuario_logado():
    return {
        'usuario_logado': {
            'nome': session.get('nome'),
            'email': session.get('email'),
            'tipo': session.get('tipo'),
        } if session.get('id_conta') else None
    }

def get_aluno_completo(id_pessoa):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.id_pessoa, p.nome, p.cpf, p.sexo, p.data_nascimento, a.tipo
        FROM aluno a JOIN pessoa p ON p.id = a.id_pessoa
        WHERE a.id_pessoa = %s
    """, (id_pessoa,))
    aluno = cursor.fetchone()
    conn.close()
    return aluno

@app.route('/')
def home():
    if session.get('tipo') == 'ALUNO':
        return redirect(url_for('aluno.painel'))
    if session.get('tipo') == 'PROFESSOR':
        return redirect(url_for('professor.painel'))
    return render_template('index.html')

@app.route('/alunos')
def listar_alunos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.id_pessoa, p.nome, p.cpf, p.sexo, p.data_nascimento, a.tipo
        FROM aluno a JOIN pessoa p ON p.id = a.id_pessoa ORDER BY p.nome
    """)
    alunos = cursor.fetchall()
    conn.close()
    return render_template('alunos.html', alunos=alunos)

@app.route('/alunos/novo', methods=['GET', 'POST'])
def criar_aluno():
    if request.method == 'POST':
        nome = request.form.get('nome', '').strip()
        cpf  = request.form.get('cpf', '').strip().replace('.','').replace('-','')
        sexo = request.form.get('sexo', '')
        data = request.form.get('data_nascimento', '')
        tipo = request.form.get('tipo', 'GRADUACAO')
        erros = []
        if not nome: erros.append('Nome é obrigatório.')
        if len(cpf) != 11 or not cpf.isdigit(): erros.append('CPF deve ter 11 dígitos.')
        if not data: erros.append('Data de nascimento é obrigatória.')
        if sexo not in ('M','F'): erros.append('Sexo inválido.')
        if erros:
            for e in erros: flash(e, 'danger')
            return render_template('aluno_form.html', modo='criar', form=request.form)
        try:
            conn = get_connection()
            id_novo = PessoaRepository(conn).create(nome, cpf, sexo, datetime.date.fromisoformat(data))
            AlunoRepository(conn).create(id_novo, tipo)
            conn.close()
            flash(f'Aluno {nome} cadastrado com sucesso!', 'success')
            return redirect(url_for('listar_alunos'))
        except Exception as ex:
            flash(f'Erro ao cadastrar: {ex}', 'danger')
            return render_template('aluno_form.html', modo='criar', form=request.form)
    return render_template('aluno_form.html', modo='criar', form={})

@app.route('/alunos/<int:id_pessoa>')
def ver_aluno(id_pessoa):
    aluno = get_aluno_completo(id_pessoa)
    if not aluno:
        flash('Aluno nao encontrado.', 'danger')
        return redirect(url_for('listar_alunos'))
    conn = get_connection()
    p_repo = PessoaRepository(conn)
    foto = p_repo.find_foto(id_pessoa)
    aluno['tem_foto'] = foto is not None and len(foto) > 0
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT mc.id, mc.codigo, mc.status, c.nome AS nome_curso, c.sigla
        FROM matricula_curso mc
        JOIN curso c ON c.id = mc.id_curso
        WHERE mc.id_aluno = %s AND mc.status = 'ATIVA'
        LIMIT 1
    """, (id_pessoa,))
    aluno['matricula_curso'] = cursor.fetchone()
    cursor.execute('SELECT id, nome, sigla FROM curso ORDER BY nome')
    cursos = cursor.fetchall()
    conn.close()
    return render_template('aluno_detalhe.html', aluno=aluno, cursos=cursos)


@app.route('/alunos/<int:id_pessoa>/matricular-curso', methods=['POST'])
def matricular_em_curso(id_pessoa):
    """Cria matrícula em curso para o aluno."""
    import datetime
    id_curso = request.form.get('id_curso', '')

    if not id_curso or not id_curso.isdigit():
        flash('Selecione um curso válido.', 'danger')
        return redirect(url_for('ver_aluno', id_pessoa=id_pessoa))

    try:
        conn   = get_connection()
        cursor = conn.cursor(dictionary=True)

        # Verifica se já tem matrícula ativa nesse curso
        cursor.execute("""
            SELECT id FROM matricula_curso
            WHERE id_aluno = %s AND id_curso = %s AND status = 'ATIVA'
        """, (id_pessoa, int(id_curso)))
        if cursor.fetchone():
            flash('Aluno já possui matrícula ativa nesse curso.', 'danger')
            conn.close()
            return redirect(url_for('ver_aluno', id_pessoa=id_pessoa))

        # Gera código de matrícula: ano + id_pessoa preenchido com zeros
        ano = datetime.date.today().year % 100
        codigo = f'{ano:02d}/{id_pessoa:07d}'

        cursor.execute("""
            INSERT INTO matricula_curso
            (id_aluno, id_curso, codigo, data_matricula_curso, status)
            VALUES (%s, %s, %s, %s, 'ATIVA')
        """, (id_pessoa, int(id_curso), codigo, datetime.date.today()))
        conn.commit()
        conn.close()
        flash('Matrícula em curso realizada com sucesso!', 'success')
    except Exception as ex:
        flash(f'Erro ao matricular: {ex}', 'danger')

    return redirect(url_for('ver_aluno', id_pessoa=id_pessoa))

@app.route('/alunos/<int:id_pessoa>/foto')
def foto_aluno(id_pessoa):
    """Serve a foto do aluno como imagem binária direto do banco (BLOB)."""
    from flask import Response
    conn = get_connection()
    p_repo = PessoaRepository(conn)
    foto = p_repo.find_foto(id_pessoa)
    conn.close()
    if not foto:
        return '', 404
    return Response(foto, mimetype='image/jpeg')


@app.route('/alunos/<int:id_pessoa>/foto/upload', methods=['POST'])
def upload_foto_aluno(id_pessoa):
    """Recebe o arquivo de imagem e salva como BLOB no banco."""
    arquivo = request.files.get('foto')
    if not arquivo or arquivo.filename == '':
        flash('Nenhum arquivo selecionado.', 'danger')
        return redirect(url_for('ver_aluno', id_pessoa=id_pessoa))

    # Valida extensão
    extensoes_permitidas = {'jpg', 'jpeg', 'png', 'webp'}
    ext = arquivo.filename.rsplit('.', 1)[-1].lower()
    if ext not in extensoes_permitidas:
        flash('Formato inválido. Use JPG, PNG ou WEBP.', 'danger')
        return redirect(url_for('ver_aluno', id_pessoa=id_pessoa))

    # Limita tamanho: 2MB
    foto_bytes = arquivo.read()
    if len(foto_bytes) > 2 * 1024 * 1024:
        flash('Arquivo muito grande. Máximo 2MB.', 'danger')
        return redirect(url_for('ver_aluno', id_pessoa=id_pessoa))

    try:
        conn = get_connection()
        p_repo = PessoaRepository(conn)
        p_repo.update_foto(id_pessoa, foto_bytes)
        conn.close()
        flash('Foto atualizada com sucesso!', 'success')
    except Exception:
        flash('Erro ao salvar foto.', 'danger')

    return redirect(url_for('ver_aluno', id_pessoa=id_pessoa))

@app.route('/alunos/<int:id_pessoa>/editar', methods=['GET', 'POST'])
def editar_aluno(id_pessoa):
    aluno = get_aluno_completo(id_pessoa)
    if not aluno:
        flash('Aluno não encontrado.', 'danger')
        return redirect(url_for('listar_alunos'))
    if request.method == 'POST':
        nome = request.form.get('nome','').strip()
        sexo = request.form.get('sexo','')
        data = request.form.get('data_nascimento','')
        tipo = request.form.get('tipo','GRADUACAO')
        erros = []
        if not nome: erros.append('Nome é obrigatório.')
        if not data: erros.append('Data de nascimento é obrigatória.')
        if sexo not in ('M','F'): erros.append('Sexo inválido.')
        if erros:
            for e in erros: flash(e, 'danger')
            return render_template('aluno_form.html', modo='editar', aluno=aluno, form=request.form)
        try:
            conn = get_connection()
            PessoaRepository(conn).update(id_pessoa, nome=nome, sexo=sexo, data_nascimento=datetime.date.fromisoformat(data))
            AlunoRepository(conn).update(id_pessoa, tipo)
            conn.close()
            flash(f'Aluno {nome} atualizado!', 'success')
            return redirect(url_for('ver_aluno', id_pessoa=id_pessoa))
        except Exception as ex:
            flash(f'Erro: {ex}', 'danger')
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT mc.id, mc.codigo, mc.status, c.nome AS nome_curso, c.sigla
        FROM matricula_curso mc
        JOIN curso c ON c.id = mc.id_curso
        WHERE mc.id_aluno = %s AND mc.status = 'ATIVA'
        LIMIT 1
    """, (id_pessoa,))
    matricula_curso = cursor.fetchone()
    cursor.execute('SELECT id, nome, sigla FROM curso ORDER BY nome')
    cursos = cursor.fetchall()
    conn.close()
    return render_template('aluno_form.html', modo='editar', aluno=aluno, form=aluno,
                           matricula_curso=matricula_curso, cursos=cursos)

@app.route('/alunos/<int:id_pessoa>/deletar', methods=['POST'])
def deletar_aluno(id_pessoa):
    aluno = get_aluno_completo(id_pessoa)
    if not aluno:
        flash('Aluno não encontrado.', 'danger')
        return redirect(url_for('listar_alunos'))
    try:
        conn = get_connection()
        AlunoRepository(conn).delete(id_pessoa)
        PessoaRepository(conn).delete(id_pessoa)
        conn.close()
        flash(f'Aluno {aluno["nome"]} removido.', 'success')
    except Exception as ex:
        flash(f'Erro ao remover: {ex}', 'danger')
    return redirect(url_for('listar_alunos'))

@app.route('/testar')
def rodar_teste_rapido():
    try:
        get_connection().close()
        flash('Conexão com o banco efetuada com sucesso!', 'success')
    except Exception as e:
        flash(f'Falha: {e}', 'danger')
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
