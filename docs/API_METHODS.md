# API de Funcionalidades — Backend Python

Guia completo com exemplos de cada método implementado no backend do Sistema Acadêmico UnB.

---

## Índice

1. [Padrão Base (BaseRepository)](#padrão-base)
2. [Repositórios CRUD Básicos](#repositórios-crud-básicos)
   - [PessoaRepository](#pessoarepository)
   - [AlunoRepository](#alunorepository)
3. [Repositórios CRUD Complexos](#repositórios-crud-complexos)
   - [MatriculaDisciplinaRepository](#matriculadisciplinarepository)
4. [Services (Lógica de Negócio)](#services)
   - [MatriculaService](#matriculaservice)
5. [Métodos Especiais](#métodos-especiais)
6. [Padrões e Convenções](#padrões-e-convenções)

---

## Padrão Base

### BaseRepository

Todas as classes de repositório herdam de `BaseRepository`, que fornece acesso à conexão do banco:

```python
class BaseRepository:
    def __init__(self, connection):
        self.conn = connection
    
    def _cursor(self):
        return self.conn.cursor(dictionary=True)
```

**Uso:**
```python
from database.connection import get_connection
from repositories.pessoa_repository import PessoaRepository

conn = get_connection()
pessoa_repo = PessoaRepository(conn)
# Agora pode chamar qualquer método do repositório
```

---

## Repositórios CRUD Básicos

### PessoaRepository

Gerencia dados de **pessoas** (alunos, professores, coordenadores, etc.) com suporte a **fotos em BLOB**.

#### `create(nome, cpf, sexo, data_nascimento, foto=None)`

Cria nova pessoa no sistema.

**Parâmetros:**
- `nome` (str): Nome completo
- `cpf` (str): CPF sem formatação
- `sexo` (str): 'M' ou 'F'
- `data_nascimento` (str): 'YYYY-MM-DD'
- `foto` (bytes, opcional): Foto em BLOB

**Retorna:** ID da pessoa criada

**Exemplo:**
```python
pessoa_repo = PessoaRepository(conn)

id_pessoa = pessoa_repo.create(
    nome="João Silva",
    cpf="12345678901",
    sexo="M",
    data_nascimento="1990-05-15",
    foto=None  # Pode ser None ou bytes de imagem
)
print(f"Pessoa criada com ID: {id_pessoa}")  # Saída: Pessoa criada com ID: 1
```

---

#### `find_by_id(id_pessoa)`

Busca uma pessoa pelo ID.

**Parâmetros:**
- `id_pessoa` (int): ID da pessoa

**Retorna:** Dict com dados da pessoa ou None

**Exemplo:**
```python
pessoa = pessoa_repo.find_by_id(1)
if pessoa:
    print(pessoa)
    # {'id': 1, 'nome': 'João Silva', 'cpf': '12345678901', 'sexo': 'M', 'data_nascimento': '1990-05-15'}
else:
    print("Pessoa não encontrada")
```

---

#### `find_all()`

Lista todas as pessoas cadastradas, ordenadas por nome.

**Retorna:** Lista de dicts com dados das pessoas

**Exemplo:**
```python
pessoas = pessoa_repo.find_all()
for p in pessoas:
    print(f"{p['id']} - {p['nome']} ({p['cpf']})")
    # 1 - João Silva (12345678901)
    # 2 - Maria Santos (98765432101)
    # 3 - Pedro Oliveira (55566677788)
```

---

#### `update(id_pessoa, nome=None, sexo=None, data_nascimento=None)`

Atualiza dados de uma pessoa (atualização parcial).

**Parâmetros:**
- `id_pessoa` (int): ID da pessoa
- Campos opcionais: apenas os que deseja atualizar

**Retorna:** Número de registros afetados (0 ou 1)

**Exemplo:**
```python
# Atualizar apenas o nome
linhas = pessoa_repo.update(1, nome="João Silva Santos")
print(f"Linhas atualizadas: {linhas}")  # Saída: Linhas atualizadas: 1

# Atualizar nome e data de nascimento
linhas = pessoa_repo.update(1, nome="João Silva Santos", data_nascimento="1990-06-20")
print(f"Linhas atualizadas: {linhas}")  # Saída: Linhas atualizadas: 1
```

---

#### `update_foto(id_pessoa, foto_bytes)`

Atualiza/insere foto (BLOB) de uma pessoa.

**Parâmetros:**
- `id_pessoa` (int): ID da pessoa
- `foto_bytes` (bytes): Imagem em bytes

**Retorna:** Número de registros afetados

**Exemplo:**
```python
# Ler imagem do disco
with open("foto.jpg", "rb") as f:
    foto_bytes = f.read()

linhas = pessoa_repo.update_foto(1, foto_bytes)
print(f"Foto atualizada: {linhas == 1}")  # Saída: Foto atualizada: True
```

---

#### `find_foto(id_pessoa)`

Recupera a foto de uma pessoa.

**Parâmetros:**
- `id_pessoa` (int): ID da pessoa

**Retorna:** Bytes da foto ou None

**Exemplo:**
```python
foto_bytes = pessoa_repo.find_foto(1)
if foto_bytes:
    with open("foto_recuperada.jpg", "wb") as f:
        f.write(foto_bytes)
    print("Foto salva com sucesso")
else:
    print("Pessoa não tem foto")
```

---

#### `delete(id_pessoa)`

Deleta uma pessoa.

**Parâmetros:**
- `id_pessoa` (int): ID da pessoa

**Retorna:** Número de registros afetados

**Exemplo:**
```python
linhas = pessoa_repo.delete(1)
if linhas > 0:
    print("Pessoa deletada")
else:
    print("Pessoa não encontrada")
```

---

### AlunoRepository

Gerencia dados de **alunos** (herança de Pessoa com tipo de aluno).

#### `create(id_pessoa, tipo="GRADUACAO")`

Cria registro de aluno. **Nota:** A pessoa deve existir em `pessoa` primeiro.

**Parâmetros:**
- `id_pessoa` (int): ID da pessoa (chave estrangeira)
- `tipo` (str): 'GRADUACAO', 'POS_GRADUACAO', 'ESPECIALIZACAO' (padrão: 'GRADUACAO')

**Retorna:** ID da pessoa (aluno)

**Exemplo:**
```python
aluno_repo = AlunoRepository(conn)

# Primeiro criar a pessoa
id_pessoa = pessoa_repo.create(
    nome="Carlos Silva",
    cpf="11122233344",
    sexo="M",
    data_nascimento="2000-03-10"
)

# Depois criar o aluno
aluno_repo.create(id_pessoa, tipo="GRADUACAO")
print(f"Aluno criado com ID: {id_pessoa}")
```

---

#### `find_by_id(id_pessoa)`

Busca aluno com dados pessoais unidos (JOIN com pessoa).

**Retorna:** Dict com dados do aluno + dados pessoais

**Exemplo:**
```python
aluno = aluno_repo.find_by_id(1)
if aluno:
    print(aluno)
    # {'id_pessoa': 1, 'nome': 'Carlos Silva', 'cpf': '11122233344', 
    #  'sexo': 'M', 'data_nascimento': '2000-03-10', 'tipo': 'GRADUACAO'}
```

---

#### `find_all()`

Lista todos os alunos com dados pessoais, ordenados por nome.

**Exemplo:**
```python
alunos = aluno_repo.find_all()
for a in alunos:
    print(f"{a['nome']} - Tipo: {a['tipo']}")
    # Carlos Silva - Tipo: GRADUACAO
    # Ana Costa - Tipo: POS_GRADUACAO
```

---

#### `update(id_pessoa, tipo)`

Atualiza tipo de aluno.

**Exemplo:**
```python
linhas = aluno_repo.update(1, tipo="POS_GRADUACAO")
print(f"Aluno atualizado: {linhas > 0}")  # Saída: Aluno atualizado: True
```

---

#### `delete(id_pessoa)`

Deleta registro de aluno.

**Exemplo:**
```python
linhas = aluno_repo.delete(1)
print(f"Aluno deletado: {linhas > 0}")
```

---

## Repositórios CRUD Complexos

### MatriculaDisciplinaRepository

Gerencia **matrículas de alunos em disciplinas** (turmas). Inclui JOINs complexos com 7+ tabelas.

#### `create(id_matricula_curso, id_turma, codigo, data_matricula_disciplina, status="MATRICULADO")`

Cria matrícula de aluno em disciplina/turma.

**Parâmetros:**
- `id_matricula_curso` (int): ID da matrícula em curso (aluno vinculado ao curso)
- `id_turma` (int): ID da turma
- `codigo` (str): Código único da matrícula
- `data_matricula_disciplina` (str): Data em 'YYYY-MM-DD'
- `status` (str): 'MATRICULADO', 'CURSANDO', 'APROVADO', 'REPROVADO', 'TRANCADO'

**Retorna:** ID da matrícula disciplina

**Exemplo:**
```python
md_repo = MatriculaDisciplinaRepository(conn)

id_md = md_repo.create(
    id_matricula_curso=5,
    id_turma=3,
    codigo="MAT-2024-001",
    data_matricula_disciplina="2024-01-15",
    status="MATRICULADO"
)
print(f"Matrícula disciplina criada: {id_md}")
```

---

#### `find_by_id(id_md)`

Busca matrícula disciplina com todos os dados relacionados (aluno, disciplina, turma, semestre).

**Retorna:** Dict rico com JOIN de 7 tabelas

**Exemplo:**
```python
md = md_repo.find_by_id(1)
print(md)
# {
#   'id': 1,
#   'nota': 8.5,
#   'status': 'MATRICULADO',
#   'disciplina': 'Cálculo I',
#   'turma': 'A01',
#   'nome_aluno': 'Carlos Silva',
#   'semestre': '2024.1'
# }
```

---

#### `find_by_matricula_curso(id_matricula_curso)`

Lista todas as disciplinas em que um aluno está matriculado.

**Retorna:** Lista de matrículas disciplina com dados relacionados

**Exemplo:**
```python
# Buscar todas as disciplinas do aluno na matrícula 5
disciplinas = md_repo.find_by_matricula_curso(5)
for d in disciplinas:
    print(f"{d['disciplina']} ({d['turma']}) - Nota: {d['nota']}")
    # Cálculo I (A01) - Nota: 8.5
    # Álgebra Linear (B02) - Nota: 7.0
```

---

#### `find_all()`

Lista todas as matrículas de disciplina do sistema.

**Exemplo:**
```python
todas_md = md_repo.find_all()
print(f"Total de matrículas: {len(todas_md)}")
```

---

#### `update(id_md, status=None, nota=None, data_trancamento_disciplina=None)`

Atualiza status, nota ou data de trancamento de matrícula.

**Exemplo:**
```python
# Atualizar nota
linhas = md_repo.update(1, nota=9.0)
print(f"Nota atualizada")

# Trancar disciplina
from datetime import date
linhas = md_repo.update(1, status="TRANCADO", data_trancamento_disciplina=str(date.today()))
print(f"Disciplina trancada")
```

---

#### `delete(id_md)`

Deleta matrícula de disciplina.

**Exemplo:**
```python
linhas = md_repo.delete(1)
print(f"Matrícula deletada")
```

---

## Services

Services implementam **lógica de negócio complexa** que envolve múltiplos repositórios e regras.

### MatriculaService

Gerencia operações de matrícula que envolvem validações e múltiplas tabelas.

#### `matricular_aluno_em_disciplina(id_pessoa, id_oferta)`

**Lógica:**
1. Valida que `id_pessoa` é um aluno cadastrado
2. Verifica se aluno tem matrícula **ativa** em curso
3. Busca turmas da oferta que têm vagas
4. Chama procedure `sp_matricular_aluno_em_turma` (validação no banco)
5. Retorna resultado com ID da matrícula ou erro

**Parâmetros:**
- `id_pessoa` (int): ID do aluno
- `id_oferta` (int): ID da oferta (disciplina em semestre)

**Retorna:** Dict com resultado

```python
{
    "ok": True,
    "id_matricula_disciplina": 42,
    "id_matricula_curso": 5,
    "id_turma": 3,
    "mensagem": "Matrícula realizada com sucesso."
}
```

Ou em caso de erro:

```python
{
    "ok": False,
    "erro": "Aluno não possui matrícula em curso ativa."
}
```

**Exemplo:**
```python
from services.matricula_service import matricular_aluno_em_disciplina

resultado = matricular_aluno_em_disciplina(id_pessoa=15, id_oferta=8)

if resultado["ok"]:
    print(f"Matrícula criada com sucesso!")
    print(f"ID: {resultado['id_matricula_disciplina']}")
else:
    print(f"Erro: {resultado['erro']}")
```

---

#### `buscar_historico_aluno(id_aluno)`

Consulta a **view** `vw_historico_aluno` e retorna histórico completo do aluno.

**Retorna:** Lista de dicts com histórico escolar completo

**Exemplo:**
```python
historico = buscar_historico_aluno(15)

for disciplina in historico:
    print(f"{disciplina['nome_disciplina']} - Semestre: {disciplina['semestre']}")
    print(f"  Nota: {disciplina['nota']} - Status: {disciplina['status']}")
    # Cálculo I - Semestre: 2024.1
    #   Nota: 8.5 - Status: APROVADO
    # Álgebra Linear - Semestre: 2024.1
    #   Nota: 7.0 - Status: APROVADO
```

---

## Métodos Especiais

### Padrões de Busca Específica

Alguns repositórios têm métodos além do CRUD padrão para buscas especializadas.

**Exemplo: `TurmaRepository.find_by_oferta(id_oferta)`**
```python
turma_repo = TurmaRepository(conn)
turmas = turma_repo.find_by_oferta(8)

for t in turmas:
    print(f"Turma {t['codigo']} - Vagas: {t['vagas_disponiveis']}")
```

**Exemplo: `MatriculaCursoRepository.find_ativa_por_aluno(id_aluno)`**
```python
mc_repo = MatriculaCursoRepository(conn)
matricula_ativa = mc_repo.find_ativa_por_aluno(15)

if matricula_ativa:
    print(f"Aluno matriculado no curso: {matricula_ativa['nome_curso']}")
```

---

## Padrões e Convenções

### 1. **Padrão de Conexão**

```python
from database.connection import get_connection

conn = get_connection()
try:
    # Usar repositório
    pass
finally:
    conn.close()
```

### 2. **Retorno de Métodos CRUD**

| Método | Retorna |
|--------|---------|
| `create()` | ID do registro criado (int) |
| `find_by_id()` | Dict ou None |
| `find_all()` | Lista de dicts |
| `find_*()` | Lista de dicts ou None |
| `update()` | Número de linhas afetadas (int) |
| `delete()` | Número de linhas afetadas (int) |

### 3. **Tratamento de Erros**

```python
try:
    resultado = matricular_aluno_em_disciplina(15, 8)
    if not resultado["ok"]:
        print(f"Erro: {resultado['erro']}")
except Exception as e:
    print(f"Erro na conexão: {str(e)}")
```

### 4. **Parametrização Segura (Proteção SQL Injection)**

Todos os repositórios usam `%s` e tuplas para parametrização:

```python
# ✅ CORRETO
cursor.execute("SELECT * FROM pessoa WHERE id = %s", (id_pessoa,))

# ❌ INCORRETO (Vulnerável)
cursor.execute(f"SELECT * FROM pessoa WHERE id = {id_pessoa}")
```

---

## Próximos Passos

- Implementar novos métodos especializados (ex: `find_by_status()`)
- Adicionar logging de operações
- Criar decoradores para validação de entrada
- Documentar endpoints da API (Flask/Django)

