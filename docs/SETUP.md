# CRUD — Sistema Acadêmico UnB (Python)

Camada de persistência do projeto de Banco de Dados da UnB.
Linguagem: Python 3.11+ · Driver: `mysql-connector-python` · Sem ORM.

---

## Pré-requisitos

- MySQL 8.0+ rodando localmente
- Python 3.11+

---

## Setup

**1. Crie e ative o ambiente virtual** (já existente neste repositório):

```bash
cd src/python
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
```

**2. Configure o arquivo `.env`** (copie o exemplo):

```bash
cp .env.example .env
# Edite .env com suas credenciais MySQL
```

**3. Suba o banco de dados** — execute os scripts na ordem abaixo no MySQL:

```bash
mysql -u root -p < src/sql/00_criar_tabelas.sql
mysql -u root -p < src/sql/04_alter_foto.sql
mysql -u root -p < src/sql/01_views.sql
mysql -u root -p < src/sql/02_procedures.sql
mysql -u root -p < src/sql/03_triggers.sql
mysql -u root -p < src/sql/05_seeds.sql
```

---

## Estrutura

```
src/python/
├── database/
│   ├── config.py          # Lê variáveis do .env
│   └── connection.py      # get_connection() → mysql.connector.connect()
├── repositories/          # Acesso direto ao banco (SQL puro)
│   ├── base_repository.py
│   ├── pessoa_repository.py      # CRUD completo + foto BLOB
│   ├── aluno_repository.py
│   ├── professor_repository.py
│   ├── departamento_repository.py
│   ├── curso_repository.py
│   ├── disciplina_repository.py
│   ├── semestre_repository.py
│   ├── oferta_repository.py
│   ├── turma_repository.py
│   ├── matricula_curso_repository.py
│   ├── matricula_disciplina_repository.py
│   ├── avaliacao_repository.py
│   └── ... (13 repositórios adicionais)
├── services/
│   └── matricula_service.py      # Funções de negócio multi-tabela
└── tests/
    └── test_crud.py              # Validação do CRUD completo
```

---

## Como rodar os testes

```bash
cd src/python
python tests/test_crud.py
```

O script conecta ao banco, exercita cada função CRUD, testa a foto (BLOB),
aciona a procedure `sp_matricular_aluno_em_turma`, verifica os triggers de
nota e consulta a view `vw_historico_aluno`. Imprime `[OK]` ou `[FALHA]`
para cada cenário.

---

## Componentes SQL implementados

| Componente | Arquivo | Descrição |
|---|---|---|
| View | `01_views.sql` | `vw_historico_aluno` — histórico escolar completo |
| Procedure | `02_procedures.sql` | `sp_matricular_aluno_em_turma` — valida vagas e insere |
| Trigger (×2) | `03_triggers.sql` | Recalcula nota final após INSERT/UPDATE em `resultado_avaliacao` |
| BLOB | `04_alter_foto.sql` | Coluna `foto LONGBLOB` em `pessoa` |
| Seeds | `05_seeds.sql` | 5+ registros nas 25 tabelas |

---

## Padrão de uso nos repositórios

```python
from database.connection import get_connection
from repositories.pessoa_repository import PessoaRepository

conn = get_connection()
repo = PessoaRepository(conn)

# Create
id_novo = repo.create("Maria Silva", "12345678900", "F", "2000-01-01")

# Read
pessoa = repo.find_by_id(id_novo)

# Foto (BLOB)
with open("foto.jpg", "rb") as f:
    repo.update_foto(id_novo, f.read())

# Update / Delete
repo.update(id_novo, nome="Maria S. Atualizada")
repo.delete(id_novo)
conn.close()
```

## Função multi-tabela

```python
from services.matricula_service import matricular_aluno_em_disciplina, buscar_historico_aluno

# Matricula o aluno (id_pessoa=1) na oferta 2
resultado = matricular_aluno_em_disciplina(id_pessoa=1, id_oferta=2)
print(resultado)  # {"ok": True, "id_matricula_disciplina": 6, ...}

# Histórico escolar via view
historico = buscar_historico_aluno(id_aluno=1)
for linha in historico:
    print(linha["nome_disciplina"], linha["nota_final"])
```
