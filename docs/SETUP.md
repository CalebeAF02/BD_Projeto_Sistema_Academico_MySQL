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

**3. Suba o banco de dados** — execute os scripts na ordem abaixo.

⚠️ **Windows/PowerShell:** NÃO use `Get-Content arquivo.sql | mysql ...`.
O PowerShell 5.1 não lê o arquivo como UTF-8 por padrão, e os acentos
(á, ã, ç, ê...) chegam corrompidos no banco — inclusive dentro de
mensagens de erro de procedures/triggers. Use o comando `source` do
próprio cliente MySQL, que lê o arquivo direto do disco:

```powershell
mysql -u root -p --default-character-set=utf8mb4 -e "source C:/caminho/completo/src/sql/00_criar_tabelas.sql"
mysql -u root -p --default-character-set=utf8mb4 -e "source C:/caminho/completo/src/sql/04_alter_foto.sql"
mysql -u root -p --default-character-set=utf8mb4 -e "source C:/caminho/completo/src/sql/01_views.sql"
mysql -u root -p --default-character-set=utf8mb4 -e "source C:/caminho/completo/src/sql/02_procedures.sql"
mysql -u root -p --default-character-set=utf8mb4 -e "source C:/caminho/completo/src/sql/03_triggers.sql"
mysql -u root -p --default-character-set=utf8mb4 -e "source C:/caminho/completo/src/sql/05_seeds.sql"
mysql -u root -p --default-character-set=utf8mb4 -e "source C:/caminho/completo/src/sql/06_atualizar_senhas.sql"
mysql -u root -p --default-character-set=utf8mb4 -e "source C:/caminho/completo/src/sql/07_corrigir_matricula_duplicada.sql"
```
(use `/` no caminho, mesmo no Windows — o cliente MySQL prefere assim.
Troque `C:/caminho/completo` pelo caminho real do seu clone.)

**Linux/macOS:**
```bash
mysql -u root -p < src/sql/00_criar_tabelas.sql
mysql -u root -p < src/sql/04_alter_foto.sql
mysql -u root -p < src/sql/01_views.sql
mysql -u root -p < src/sql/02_procedures.sql
mysql -u root -p < src/sql/03_triggers.sql
mysql -u root -p < src/sql/05_seeds.sql
mysql -u root -p < src/sql/06_atualizar_senhas.sql
mysql -u root -p < src/sql/07_corrigir_matricula_duplicada.sql
```

Todos os scripts a partir de agora começam com `SET NAMES utf8mb4;`
logo após o `USE projeto_unb;` — isso garante que a sessão do cliente
usa UTF-8 independente do codepage do terminal (cp850 no Windows,
latin1 em algumas instalações padrão), então mesmo se alguém usar um
método diferente de carregar o arquivo, o risco de corrupção é bem menor.

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
| Migração de senhas | `06_atualizar_senhas.sql` | Hashes reais (werkzeug scrypt) para as 10 contas de seed — senha padrão `senha123` |
| Correção matrícula duplicada | `07_corrigir_matricula_duplicada.sql` | Limpa duplicatas de teste, adiciona `UNIQUE(id_matricula_curso, id_turma)` e recria a procedure com checagem de "já matriculado" |
| Recriação isolada da procedure | `08_recriar_procedure_utf8.sql` | Só recria `sp_matricular_aluno_em_turma` — use se `07` já rodou uma vez e a 2ª execução falhar com "Duplicate key" antes de chegar na procedure |

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
