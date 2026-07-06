# validators.py
# Funções de validação e sanitização de input.
# Seguindo princípios de separação de responsabilidade (SOLID),
# minimização de dados (LGPD Art. 6) e controle de entrada (ISO 27001 A.14.2).

import re
from datetime import date


# ── Sanitização ────────────────────────────────────────────────────────

def sanitize_str(value: str, max_length: int = 255) -> str:
    """Remove espaços extras e trunca ao limite máximo."""
    if not isinstance(value, str):
        return ''
    return value.strip()[:max_length]


def sanitize_digits(value: str) -> str:
    """Remove tudo que não for dígito."""
    return re.sub(r'\D', '', value or '')


def mask_cpf(cpf: str) -> str:
    """
    Mascara CPF para exibição — LGPD Art. 6 (minimização de dados).
    Entrada:  '11122233344'
    Saída:    '111.***.**-44'
    """
    cpf = sanitize_digits(cpf)
    if len(cpf) != 11:
        return cpf
    return f'{cpf[:3]}.***.**-{cpf[-2:]}'


# ── Validação de campos comuns ─────────────────────────────────────────

def validate_nome(nome: str) -> str | None:
    """Retorna mensagem de erro ou None se válido."""
    if not nome:
        return 'Nome é obrigatório.'
    if len(nome) < 3:
        return 'Nome deve ter pelo menos 3 caracteres.'
    if len(nome) > 150:
        return 'Nome deve ter no máximo 150 caracteres.'
    if re.search(r'[<>"\';]', nome):
        return 'Nome contém caracteres inválidos.'
    return None


def validate_cpf(cpf: str) -> str | None:
    """Valida formato do CPF (11 dígitos, não todos iguais)."""
    digits = sanitize_digits(cpf)
    if len(digits) != 11:
        return 'CPF deve ter 11 dígitos numéricos.'
    if len(set(digits)) == 1:
        return 'CPF inválido.'
    return None


def validate_data_nascimento(data_str: str) -> str | None:
    """Valida se a data é válida e não está no futuro."""
    if not data_str:
        return 'Data de nascimento é obrigatória.'
    try:
        dt = date.fromisoformat(data_str)
        if dt > date.today():
            return 'Data de nascimento não pode ser no futuro.'
        if dt.year < 1900:
            return 'Data de nascimento inválida.'
    except ValueError:
        return 'Data de nascimento inválida.'
    return None


def validate_sexo(sexo: str) -> str | None:
    if sexo not in ('M', 'F'):
        return 'Sexo inválido.'
    return None


# ── Validação de autenticação (login / registro / senha) ──────────────

EMAIL_REGEX = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


def validate_email(email: str) -> str | None:
    """Valida formato básico de e-mail."""
    if not email:
        return 'E-mail é obrigatório.'
    if len(email) > 150:
        return 'E-mail deve ter no máximo 150 caracteres.'
    if not EMAIL_REGEX.match(email):
        return 'E-mail inválido.'
    return None


def validate_senha(senha: str) -> str | None:
    """Exige no mínimo 8 caracteres, com letra e número (sem regras exóticas)."""
    if not senha:
        return 'Senha é obrigatória.'
    if len(senha) < 8:
        return 'Senha deve ter no mínimo 8 caracteres.'
    if not re.search(r'[A-Za-z]', senha) or not re.search(r'\d', senha):
        return 'Senha deve conter letras e números.'
    return None


def validate_login_form(form: dict) -> list[str]:
    erros = []
    email = sanitize_str(form.get('email', ''))
    senha = form.get('senha', '')
    erro = validate_email(email)
    if erro:
        erros.append(erro)
    if not senha:
        erros.append('Senha é obrigatória.')
    return erros


def validate_registro_form(form: dict) -> list[str]:
    """Valida cadastro de novo aluno + conta de acesso."""
    erros = []
    nome  = sanitize_str(form.get('nome', ''))
    cpf   = sanitize_digits(form.get('cpf', ''))
    sexo  = sanitize_str(form.get('sexo', ''))
    data  = sanitize_str(form.get('data_nascimento', ''))
    email = sanitize_str(form.get('email', ''))
    senha = form.get('senha', '')
    confirmar_senha = form.get('confirmar_senha', '')

    for fn, val in [
        (validate_nome, nome),
        (validate_cpf, cpf),
        (validate_sexo, sexo),
        (validate_data_nascimento, data),
        (validate_email, email),
        (validate_senha, senha),
    ]:
        erro = fn(val)
        if erro:
            erros.append(erro)

    if senha and confirmar_senha and senha != confirmar_senha:
        erros.append('As senhas não conferem.')

    return erros


def validate_esqueci_senha_form(form: dict) -> list[str]:
    """Valida a redefinição de senha (confirmação por e-mail + CPF)."""
    erros = []
    email = sanitize_str(form.get('email', ''))
    cpf   = sanitize_digits(form.get('cpf', ''))
    nova_senha = form.get('nova_senha', '')
    confirmar_senha = form.get('confirmar_senha', '')

    for fn, val in [
        (validate_email, email),
        (validate_cpf, cpf),
        (validate_senha, nova_senha),
    ]:
        erro = fn(val)
        if erro:
            erros.append(erro)
    if nova_senha and confirmar_senha and nova_senha != confirmar_senha:
        erros.append('As senhas não conferem.')

    return erros


# ── Validação específica de professor ─────────────────────────────────

TIPOS_PROFESSOR = ('EFETIVO', 'SUBSTITUTO', 'VISITANTE', 'COLABORADOR')
NIVEIS_PROFESSOR = ('AUXILIAR', 'ASSISTENTE', 'ADJUNTO', 'ASSOCIADO', 'TITULAR')


def validate_tipo_professor(tipo: str) -> str | None:
    if tipo not in TIPOS_PROFESSOR:
        return f'Tipo de professor inválido. Valores aceitos: {", ".join(TIPOS_PROFESSOR)}.'
    return None


def validate_nivel_professor(nivel: str) -> str | None:
    if nivel not in NIVEIS_PROFESSOR:
        return f'Nível inválido. Valores aceitos: {", ".join(NIVEIS_PROFESSOR)}.'
    return None


def validate_id_departamento(id_dep: str) -> str | None:
    if not id_dep or not id_dep.isdigit() or int(id_dep) <= 0:
        return 'Departamento inválido.'
    return None


# ── Validação de disciplina ───────────────────────────────────────────

TIPOS_MATERIAL = ('SLIDE', 'LIVRO', 'PDF', 'VIDEO', 'LINK', 'OUTRO')


def validate_codigo_disciplina(codigo: str) -> str | None:
    if not codigo:
        return 'Código da disciplina é obrigatório.'
    if len(codigo) > 20:
        return 'Código deve ter no máximo 20 caracteres.'
    if re.search(r'[<>"\';]', codigo):
        return 'Código contém caracteres inválidos.'
    return None


def validate_disciplina_form(form: dict) -> list[str]:
    erros = []
    codigo = sanitize_str(form.get('codigo', ''))
    nome   = sanitize_str(form.get('nome', ''))
    for fn, val in [
        (validate_codigo_disciplina, codigo),
        (validate_nome, nome),
    ]:
        erro = fn(val)
        if erro:
            erros.append(erro)
    return erros


def validate_material_form(form: dict) -> list[str]:
    erros = []
    titulo = sanitize_str(form.get('titulo', ''))
    tipo   = sanitize_str(form.get('tipo', ''))
    if not titulo:
        erros.append('Título do material é obrigatório.')
    if tipo not in TIPOS_MATERIAL:
        erros.append(f'Tipo inválido. Aceitos: {", ".join(TIPOS_MATERIAL)}.')
    return erros


# ── Validador composto de professor ───────────────────────────────────

def validate_professor_form(form: dict, modo: str = 'criar') -> list[str]:
    """
    Valida todos os campos do formulário de professor.
    modo='criar' inclui validação de CPF.
    Retorna lista de erros (vazia = tudo ok).
    """
    erros = []

    nome  = sanitize_str(form.get('nome', ''))
    sexo  = sanitize_str(form.get('sexo', ''))
    data  = sanitize_str(form.get('data_nascimento', ''))
    tipo  = sanitize_str(form.get('tipo', ''))
    nivel = sanitize_str(form.get('nivel', ''))
    id_dep = sanitize_str(form.get('id_departamento', ''))

    for fn, val in [
        (validate_nome, nome),
        (validate_sexo, sexo),
        (validate_data_nascimento, data),
        (validate_tipo_professor, tipo),
        (validate_nivel_professor, nivel),
        (validate_id_departamento, id_dep),
    ]:
        erro = fn(val)
        if erro:
            erros.append(erro)

    if modo == 'criar':
        cpf = sanitize_digits(form.get('cpf', ''))
        erro_cpf = validate_cpf(cpf)
        if erro_cpf:
            erros.append(erro_cpf)

    return erros


# ── Validação do console SQL (área do desenvolvedor) ───────────────────

# Apenas comandos de leitura. CALL fica de fora do "somente leitura" no
# sentido estrito (procedures podem gravar), mas é permitido de propósito
# para demonstrar sp_matricular_aluno_em_turma — a interface avisa o risco.
COMANDOS_PERMITIDOS = ('SELECT', 'SHOW', 'DESCRIBE', 'DESC', 'EXPLAIN', 'CALL')

# Palavras que nunca podem aparecer, mesmo dentro de um CALL/SELECT
# (bloqueia sub-injeção de um segundo comando via ';' ou comentário).
PALAVRAS_BLOQUEADAS = (
    'INSERT', 'UPDATE', 'DELETE', 'DROP', 'ALTER', 'TRUNCATE',
    'GRANT', 'REVOKE', 'CREATE', 'REPLACE', 'RENAME', 'LOAD_FILE',
    'INTO OUTFILE', 'INTO DUMPFILE',
)


def validate_console_query(query: str) -> str | None:
    """
    Valida que a consulta do console é somente leitura (ou CALL de
    procedure). Retorna mensagem de erro ou None se estiver ok.
    """
    if not query or not query.strip():
        return 'Digite uma consulta SQL.'

    if len(query) > 2000:
        return 'Consulta muito longa (máximo 2000 caracteres).'

    corpo = query.strip().rstrip(';').strip()

    if ';' in corpo:
        return 'Apenas um comando por vez (não use ";" no meio da consulta).'

    if '--' in corpo or '/*' in corpo or '#' in corpo:
        return 'Comentários SQL não são permitidos no console.'

    primeira_palavra = corpo.split(None, 1)[0].upper() if corpo.split() else ''
    if primeira_palavra not in COMANDOS_PERMITIDOS:
        return (
            f'Comando "{primeira_palavra}" não permitido. '
            f'Use apenas: {", ".join(COMANDOS_PERMITIDOS)}.'
        )

    corpo_upper = corpo.upper()
    for palavra in PALAVRAS_BLOQUEADAS:
        if palavra in corpo_upper:
            return f'Palavra "{palavra}" não é permitida no console (somente leitura).'

    return None
