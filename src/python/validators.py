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
