# Arquitetura: Interação Interface ↔ App.py

Guia completo sobre como o frontend (interface) se comunica com o backend (app.py) no Sistema Acadêmico UnB.

---

## Visão Geral

```
┌─────────────────────────────────────┐
│   Navegador do Usuário              │
│   (HTML + CSS + JavaScript)         │
└────────────────┬────────────────────┘
                 │ HTTP GET / POST / JSON
                 ▼
┌─────────────────────────────────────┐
│   app.py (Flask)                    │
│   - Recebe requisições              │
│   - Chama repositórios/services     │
│   - Renderiza templates             │
└────────────────┬────────────────────┘
                 │ SQL
                 ▼
┌─────────────────────────────────────┐
│   MySQL 8.0+                        │
│   - 25 tabelas                      │
│   - Views, Procedures, Triggers     │
└─────────────────────────────────────┘
```

---

## 1. Estrutura de Pastas

```
src/
├── interface/
│   ├── templates/           ← Arquivos HTML (Jinja2)
│   │   ├── index.html
│   │   ├── alunos.html
│   │   ├── professores.html
│   │   └── ...
│   └── css/
│       └── styles.css       ← Estilos CSS
│
├── python/
│   ├── app.py               ← Aplicação Flask (PRINCIPAL)
│   ├── SETUP.md
│   ├── API_METHODS.md
│   ├── database/            ← Conexão com banco
│   ├── repositories/        ← Acesso a dados (SQL puro)
│   ├── services/            ← Lógica de negócio
│   └── tests/
```

---

## 2. Fluxo de Uma Requisição (Passo a Passo)

### Exemplo: Usuário clica em "Listar Alunos"

#### **Passo 1: Navegador envia requisição HTTP**

```
GET http://localhost:5000/alunos
```

O navegador acessa a URL definida em uma rota do Flask.

---

#### **Passo 2: Flask recebe na rota `@app.route('/alunos')`**

**Arquivo: `app.py`**
```python
@app.route('/alunos')
def listar_alunos():
    # Passo 3: Conecta ao banco
    conn = get_connection()
    
    # Passo 4: Cria repositório
    repo = AlunoRepository(conn)
    
    # Passo 5: Busca dados
    lista_de_alunos = repo.find_all()
    
    # Passo 6: Fecha conexão
    conn.close()
    
    # Passo 7: Renderiza template com dados
    return render_template('alunos.html', alunos=lista_de_alunos)
```

---

#### **Passo 3: Conecta ao banco de dados**

```python
conn = get_connection()
```

Abre conexão com MySQL usando credenciais do `.env`.

---

#### **Passo 4: Cria repositório**

```python
repo = AlunoRepository(conn)
```

Repositório fornece métodos CRUD para tabela `aluno`.

---

#### **Passo 5: Busca dados**

```python
lista_de_alunos = repo.find_all()
```

Executa SQL e retorna lista de dicts:
```python
[
    {'id_pessoa': 1, 'nome': 'João Silva', 'cpf': '123...', 'tipo': 'GRADUACAO'},
    {'id_pessoa': 2, 'nome': 'Maria Santos', 'cpf': '456...', 'tipo': 'GRADUACAO'},
    # ...
]
```

---

#### **Passo 6: Fecha conexão**

```python
conn.close()
```

Libera conexão com o banco.

---

#### **Passo 7: Renderiza template com dados**

```python
return render_template('alunos.html', alunos=lista_de_alunos)
```

Passa dados para o arquivo HTML via `Jinja2 Template Engine`.

---

#### **Passo 8: Template HTML recebe dados**

**Arquivo: `src/interface/templates/alunos.html`**
```html
<table>
    <tbody>
        {% for aluno in alunos %}
        <tr>
            <td><strong>{{ aluno.nome }}</strong></td>
            <td>{{ aluno.cpf }}</td>
            <td>{{ aluno.sexo }}</td>
            <td>{{ aluno.data_nascimento }}</td>
            <td>{{ aluno.tipo }}</td>
        </tr>
        {% endfor %}
    </tbody>
</table>
```

O **Jinja2** substitui:
- `{% for aluno in alunos %}` → Loop na lista
- `{{ aluno.nome }}` → Valor do dicionário

Resultado final (HTML renderizado):
```html
<table>
    <tbody>
        <tr>
            <td><strong>João Silva</strong></td>
            <td>123...</td>
            <td>M</td>
            <td>1990-05-15</td>
            <td>GRADUACAO</td>
        </tr>
        <tr>
            <td><strong>Maria Santos</strong></td>
            <td>456...</td>
            <td>F</td>
            <td>1992-03-20</td>
            <td>GRADUACAO</td>
        </tr>
    </tbody>
</table>
```

---

#### **Passo 9: Navegador exibe página**

HTML renderizado é enviado ao navegador e exibido ao usuário.

---

## 3. Configuração do Flask (app.py)

### Caminhos para Templates e Static

```python
import os
from flask import Flask, render_template

# Detecta diretório atual (python/)
CORRENTE_DIR = os.path.dirname(os.path.abspath(__file__))

# Sobe um nível (src/)
BASE_DIR = os.path.dirname(CORRENTE_DIR)

# Define caminhos para templates e CSS
TEMPLATE_DIR = os.path.join(BASE_DIR, "interface", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "interface", "css")

app = Flask(__name__, 
            template_folder=TEMPLATE_DIR,      # Onde estão os HTMLs
            static_folder=STATIC_DIR,          # Onde estão os CSSs
            static_url_path='/css')            # URL para acessar CSS
```

### Resultado:

- **Templates** (HTMLs) em: `src/interface/templates/`
- **Static** (CSSs) em: `src/interface/css/`
- Acessar CSS no HTML: `<link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">`

---

## 4. Rotas (Endpoints) Implementadas

### Rota: Home (Página Inicial)

```python
@app.route('/')
def home():
    return render_template('index.html')
```

- **URL:** `http://localhost:5000/`
- **Retorna:** `index.html` sem dados dinâmicos

---

### Rota: Listar Alunos

```python
@app.route('/alunos')
def listar_alunos():
    conn = get_connection()
    repo = AlunoRepository(conn)
    lista_de_alunos = repo.find_all()
    conn.close()
    return render_template('alunos.html', alunos=lista_de_alunos)
```

- **URL:** `http://localhost:5000/alunos`
- **Dados passados:** `alunos=lista_de_alunos`
- **Retorna:** `alunos.html` com lista de alunos

---

### Rota: Testar Conexão

```python
@app.route('/testar')
def rodar_teste_rapido():
    try:
        conn = get_connection()
        conn.close()
        return "<h3>Conexão com o banco efetuada com sucesso! [OK]</h3>"
    except Exception as e:
        return f"<h3>Falha ao conectar no banco: {str(e)}</h3>"
```

- **URL:** `http://localhost:5000/testar`
- **Função:** Valida conexão com MySQL

---

## 5. Transferência de Dados: app.py → Template HTML

### Método 1: Dados Simples

**app.py:**
```python
@app.route('/perfil/<int:id>')
def perfil_aluno(id):
    conn = get_connection()
    repo = AlunoRepository(conn)
    aluno = repo.find_by_id(id)
    conn.close()
    return render_template('perfil.html', aluno=aluno)
```

**perfil.html:**
```html
<h1>{{ aluno.nome }}</h1>
<p>CPF: {{ aluno.cpf }}</p>
<p>Tipo: {{ aluno.tipo }}</p>
```

---

### Método 2: Lista de Dados (Loop)

**app.py:**
```python
@app.route('/alunos')
def listar_alunos():
    conn = get_connection()
    repo = AlunoRepository(conn)
    lista = repo.find_all()
    conn.close()
    return render_template('alunos.html', alunos=lista)
```

**alunos.html:**
```html
{% for aluno in alunos %}
    <div>{{ aluno.nome }} - {{ aluno.cpf }}</div>
{% endfor %}
```

---

### Método 3: Múltiplas Variáveis

**app.py:**
```python
@app.route('/dashboard')
def dashboard():
    conn = get_connection()
    
    aluno_repo = AlunoRepository(conn)
    professor_repo = ProfessorRepository(conn)
    
    alunos = aluno_repo.find_all()
    professores = professor_repo.find_all()
    
    conn.close()
    
    return render_template('dashboard.html', 
                          alunos=alunos,
                          professores=professores)
```

**dashboard.html:**
```html
<h2>Total de Alunos: {{ alunos|length }}</h2>
<h2>Total de Professores: {{ professores|length }}</h2>
```

---

## 6. Sintaxe Jinja2 (Template Engine)

### Variáveis

```html
{{ nome_variavel }}                    <!-- Exibe valor -->
{{ aluno.nome }}                       <!-- Acessa dicionário -->
{{ lista[0] }}                         <!-- Acessa índice -->
```

### Condições

```html
{% if aluno.tipo == 'GRADUACAO' %}
    <p>Aluno de Graduação</p>
{% else %}
    <p>Aluno de Pós-Graduação</p>
{% endif %}
```

### Loops

```html
{% for aluno in alunos %}
    <li>{{ aluno.nome }}</li>
{% endfor %}
```

### Filtros

```html
{{ alunos|length }}                    <!-- Conta itens -->
{{ nome|upper }}                       <!-- Maiúsculas -->
{{ valor|round(2) }}                   <!-- Arredonda -->
```

---

## 7. Como Adicionar Nova Rota

### Cenário: Criar página que lista professores

#### **Passo 1: Criar template HTML**

**Arquivo: `src/interface/templates/professores.html`**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Professores</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='styles.css') }}">
</head>
<body>
    <h1>👨‍🏫 Professores</h1>
    
    <table>
        <thead>
            <tr>
                <th>Nome</th>
                <th>CPF</th>
                <th>Departamento</th>
            </tr>
        </thead>
        <tbody>
            {% for prof in professores %}
            <tr>
                <td>{{ prof.nome }}</td>
                <td>{{ prof.cpf }}</td>
                <td>{{ prof.departamento }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
```

#### **Passo 2: Adicionar rota em app.py**

```python
from repositories.professor_repository import ProfessorRepository

@app.route('/professores')
def listar_professores():
    conn = get_connection()
    repo = ProfessorRepository(conn)
    lista_professores = repo.find_all()
    conn.close()
    return render_template('professores.html', professores=lista_professores)
```

#### **Passo 3: Adicionar link no index.html**

```html
<a href="/professores">Ver Professores</a>
```

#### **Passo 4: Testar**

Acesse: `http://localhost:5000/professores`

---

## 8. Fluxo Completo: Exemplo Prático

### Objetivo: Exibir histórico de disciplinas de um aluno

#### **app.py:**
```python
from services.matricula_service import buscar_historico_aluno

@app.route('/historico/<int:id_aluno>')
def historico(id_aluno):
    # Busca histórico via service
    historico = buscar_historico_aluno(id_aluno)
    return render_template('historico.html', historico=historico)
```

#### **historico.html:**
```html
<h1>Histórico Escolar</h1>

{% if historico %}
    <table>
        <thead>
            <tr>
                <th>Disciplina</th>
                <th>Semestre</th>
                <th>Nota</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody>
            {% for disciplina in historico %}
            <tr>
                <td>{{ disciplina.nome_disciplina }}</td>
                <td>{{ disciplina.semestre }}</td>
                <td>{{ disciplina.nota }}</td>
                <td>{{ disciplina.status }}</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
{% else %}
    <p>Nenhuma disciplina encontrada.</p>
{% endif %}
```

---

## 9. Checklist para Criar Nova Página

- [ ] Criar arquivo HTML em `src/interface/templates/`
- [ ] Importar repositório/service necessário em `app.py`
- [ ] Criar rota `@app.route('/rota')`
- [ ] Buscar dados do banco
- [ ] Chamar `render_template('arquivo.html', variavel=dados)`
- [ ] Usar Jinja2 no HTML para exibir dados
- [ ] Testar acessando `http://localhost:5000/rota`

---

## 10. Troubleshooting

| Problema | Solução |
|----------|---------|
| Template não encontrado | Verificar caminho em `TEMPLATE_DIR` |
| CSS não carrega | Verificar `static_folder` e `{{ url_for('static', filename='...') }}` |
| Dados vazios na página | Verificar se `repo.find_all()` retorna dados |
| Erro SQL | Verificar credenciais no `.env` |
| Jinja2 syntax não funciona | Verificar `{{ }}` ou `{% %}` corretos |

---

## Resumo

```
Usuário acessa URL
    ↓
Flask recebe requisição em @app.route()
    ↓
app.py conecta ao banco
    ↓
app.py usa repositório para buscar dados
    ↓
app.py passa dados para template HTML
    ↓
Jinja2 renderiza HTML com dados
    ↓
Navegador exibe página final
```

Cada página do sistema segue este padrão!

