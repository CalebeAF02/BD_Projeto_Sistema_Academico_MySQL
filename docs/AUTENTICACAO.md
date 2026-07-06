# Autenticação — SGA UnB

Camada de autenticação integrada ao painel Flask existente, seguindo os
mesmos padrões do restante do projeto (blueprint, `validators.py`,
repositórios, categorias de flash `success`/`danger`/`info`).

## Rotas (`rotas/auth.py`, prefixo `/auth`)

| Rota | Método | Descrição |
|---|---|---|
| `/auth/login` | GET/POST | Autentica por e-mail + senha |
| `/auth/logout` | POST | Encerra a sessão |
| `/auth/registrar` | GET/POST | Auto-cadastro de aluno (cria Pessoa + Aluno + Conta) |
| `/auth/esqueci-senha` | GET/POST | Redefine a senha confirmando e-mail + CPF |

## Guard de acesso (`app.py`)

`@app.before_request` bloqueia qualquer rota fora de
`auth.login`, `auth.registrar`, `auth.esqueci_senha` e `static` quando não
há `session['id_conta']` ativa, redirecionando para o login.

## Segurança de senha

- Hash com `werkzeug.security.generate_password_hash(senha, method='scrypt')`.
- Nenhuma senha é armazenada ou logada em texto puro.
- `src/sql/06_atualizar_senhas.sql` substitui os hashes placeholder dos
  seeds por hashes scrypt reais — senha padrão de demonstração: `senha123`.

## Login de demonstração

```
E-mail: ana.ferreira@aluno.unb.br
Senha:  senha123
```

## Uso de IA

Claude (Anthropic) foi utilizado para gerar a camada de autenticação
(`services/auth_service.py`, `rotas/auth.py`, templates `auth/*.html`,
validadores de e-mail/senha em `validators.py` e a migração
`06_atualizar_senhas.sql`), com o objetivo de integrar login, registro e
redefinição de senha ao painel administrativo já existente, mantendo os
padrões de código do grupo (blueprints, repositórios, validação
centralizada).
