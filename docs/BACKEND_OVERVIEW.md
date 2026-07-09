# Backend — Sistema Acadêmico UnB

## O que faz?

Este backend Python implementa a **camada de persistência e acesso a dados** do Sistema Acadêmico UnB. Ele gerencia toda a comunicação entre a interface (frontend) e o banco de dados MySQL, fornecendo operações CRUD (Create, Read, Update, Delete) para 25 entidades do sistema.

---

## Principais funcionalidades

### 1. **Acesso ao Banco de Dados**
- Conexão direta com MySQL via `mysql-connector-python` (sem ORM)
- SQL puro para máxima flexibilidade e performance
- Gerenciamento de credenciais via `.env`

### 2. **25 Repositórios CRUD**
Acesso completo às principais entidades do sistema:

**Pessoas e Perfis:**
- Pessoa, Aluno, Professor, Departamento

**Gestão Acadêmica:**
- Curso, Disciplina, Semestre, Oferta, Turma

**Matrículas e Avaliações:**
- Matrícula (Curso), Matrícula (Disciplina)
- Avaliação, Resultado de Avaliação, Frequência

**Infraestrutura:**
- Prédio, Sala, Alocação de Sala

**Complementos:**
- Evento, Material de Estudo, Meta de Estudo
- Notificação, Conta

### 3. **Serviços de Negócio**
- `matricula_service.py` — Lógica complexa de matrícula (valida vagas, requerimentos, etc.)

### 4. **Componentes SQL Avançados**
- **Views:** `vw_historico_aluno` — histórico escolar completo
- **Procedures:** `sp_matricular_aluno_em_turma` — matrícula com validações
- **Triggers:** Recalcula nota final automaticamente
- **BLOBs:** Armazenamento de fotos em base64

### 5. **Testes Automatizados**
- `test_crud.py` — Valida todas as operações CRUD
- Deve ser o primeiro teste executado após criar o banco e carregar os scripts SQL
- Testa fotos, procedures, triggers, views
- Imprime `[OK]` ou `[FALHA]` para cada cenário
- É importante porque alguns cenários dependem de dados já presentes no banco (seeds e relacionamentos), então alterações no schema podem causar erros

---

## Arquitetura em Camadas

```
┌─────────────────────────────────────────┐
│   Interface (Frontend)                  │
│   - HTML/CSS/JavaScript                 │
└────────────────┬────────────────────────┘
                 │ HTTP
┌────────────────▼────────────────────────┐
│   Backend Python (app.py)               │
│   - Flask/Django (entrada de dados)     │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│   Services (Lógica de Negócio)          │
│   - matricula_service.py                │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│   Repositories (CRUD)                   │
│   - 25 arquivos de acesso a dados       │
│   - SQL Puro                            │
└────────────────┬────────────────────────┘
                 │
┌────────────────▼────────────────────────┐
│   Database (MySQL 8.0+)                 │
│   - 25 Tabelas                          │
│   - Views, Procedures, Triggers         │
└─────────────────────────────────────────┘
```

---

## Estrutura de Pastas

```
src/python/
├── app.py                    # Aplicação principal
├── SETUP.md                  # Guia de instalação
├── requirements.txt          # Dependências Python
├── .env.example              # Template de configuração
│
├── database/
│   ├── config.py             # Lê variáveis do .env
│   └── connection.py         # Conexão com MySQL
│
├── repositories/             # Camada de acesso a dados (SQL puro)
│   ├── base_repository.py    # Classe base para todos os repos
│   ├── pessoa_repository.py  # CRUD de pessoas + fotos
│   ├── aluno_repository.py
│   ├── professor_repository.py
│   ├── curso_repository.py
│   ├── disciplina_repository.py
│   ├── matricula_curso_repository.py
│   ├── matricula_disciplina_repository.py
│   └── ... (18 repositórios adicionais)
│
├── services/                 # Lógica de negócio
│   └── matricula_service.py  # Regras complexas de matrícula
│
└── tests/
    └── test_crud.py          # Testes automatizados
```

---

## Fluxo de Requisição

1. **Frontend envia requisição** → `app.py` (endpoint)
2. **app.py valida dados** e chama `services/` se necessário
3. **services/** executa regras de negócio
4. **services/** chama `repositories/` para acessar dados
5. **repositories/** executa SQL puro no MySQL
6. **MySQL retorna dados** → frontend recebe resposta JSON

---

## Tecnologias Utilizadas

| Componente | Tecnologia |
|---|---|
| Linguagem | Python 3.11+ |
| Driver BD | `mysql-connector-python` |
| Banco de Dados | MySQL 8.0+ |
| Acesso a Dados | **SQL Puro** (sem ORM) |
| Padrão de Arquitetura | **Repository Pattern** |

