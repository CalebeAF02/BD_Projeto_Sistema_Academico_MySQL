# 🎓 SGA UnB — Como Rodar o Sistema

## Pré-requisitos
- Python 3.10+
- MySQL 8.4 instalado e rodando
- Git

---

## 1. Clonar o repositório

```bash
git clone https://github.com/CalebeAF02/BD_Projeto_Sistema_Academico_MySQL.git
cd BD_Projeto_Sistema_Academico_MySQL/src/python
```

---

## 2. Criar o ambiente virtual e instalar dependências

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install mysql-connector-python==9.7.0 python-dotenv==1.2.2 Flask
```

---

## 3. Configurar o banco de dados

Crie o arquivo `.env` dentro de `src/python/` com o seguinte conteúdo:

```
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=sua_senha_aqui
DB_NAME=projeto_unb
```

---

## 4. Criar o banco e popular os dados

Abra o MySQL e execute os scripts na ordem:

```sql
source caminho/src/sql/00_criar_tabelas.sql
source caminho/src/sql/04_alter_foto.sql
source caminho/src/sql/01_views.sql
source caminho/src/sql/02_procedures.sql
source caminho/src/sql/03_triggers.sql
source caminho/src/sql/05_seeds.sql
```

---

## 5. Rodar o sistema

```bash
python app.py
```

Acesse no navegador: **http://localhost:5000**

---

## Resumo rápido (uso diário)

```bash
# Windows — dentro de src/python/
venv\Scripts\activate
python app.py
```

Abrir: **http://localhost:5000**

---

## O que você pode fazer no sistema

| Módulo | Funcionalidades |
|---|---|
| **Alunos** | Cadastrar, editar, remover, foto, matrícula em curso |
| **Professores** | Cadastrar, editar, remover (CPF mascarado) |
| **Disciplinas** | Cadastrar, editar, remover, materiais de estudo |
| **Matrículas** | Ver histórico por aluno, matricular em disciplina, trancar |
| **Turmas** | Cadastrar, editar, ver alunos e avaliações |

---

## Observações

- O arquivo `.env` **não** está no repositório — cada máquina precisa criar o seu
- O banco precisa ser criado **uma vez** por máquina
- Para parar o servidor: `Ctrl + C`
