# Painel de Demonstração de Requisitos

Página interna do próprio app (`/demo`, atrás do login) criada para
apresentar à professora, ao vivo, cada item obrigatório da especificação
do projeto — sem precisar abrir um cliente SQL separado.

## Rotas (`rotas/demo.py`, prefixo `/demo`)

| Rota | Requisito do PDF demonstrado |
|---|---|
| `/demo/chave-primaria` | Geração automática de PK (`AUTO_INCREMENT`) — insere sem informar `id` |
| `/demo/view-historico` | View `vw_historico_aluno` — consulta ao vivo, com o SQL executado exibido na tela |
| `/demo/procedure` | Procedure `sp_matricular_aluno_em_turma` — inclui o caminho de erro (`SIGNAL`) quando a turma está lotada |
| `/demo/trigger` | Triggers `tg_atualiza_nota_final_insert/update` — mostra nota antes/depois do INSERT |
| `/demo/multitabela` | CRUD multi-tabela (`matricular_aluno_em_disciplina`) — grava em 4 tabelas com integridade referencial validada |
| Link para `/alunos/<id>` | Dado binário (BLOB) — upload de foto já existente na tela de detalhe do aluno |

## Por que existe

A especificação exige que os componentes do banco (view, procedure,
trigger, PK automática, CRUD multi-tabela, BLOB) sejam **demonstrados
funcionando**, não só entregues como código. Em vez de depender só do
terminal MySQL durante a apresentação, o painel expõe cada um dentro da
própria aplicação Flask — o que também prova que a camada de persistência
está realmente usando esses recursos, e não reimplementando a lógica em
Python.

## Reversibilidade

Toda ação que grava dado (chave primária, procedure, trigger, multi-tabela)
tem um botão "Desfazer" que remove o registro criado, para não sujar os
dados de seed usados no resto da aplicação durante os testes e ensaios da
apresentação.

**Exceção:** o trigger de recálculo de nota não tem um trigger de `DELETE`
correspondente — ao desfazer um resultado de demonstração, a nota final
não volta sozinha ao valor anterior. Se precisar restaurar, basta editar
outro resultado da mesma matrícula para forçar um novo recálculo (dispara
`tg_atualiza_nota_final_update`).

## Console SQL (`/sql-console`) — extra

Além do painel por requisito acima, existe um **Console SQL** livre
(`rotas/console.py` + `services/console_service.py`), pensado como bônus
de portfólio: uma área "tipo terminal" dentro da própria interface, onde
dá pra digitar e rodar qualquer consulta.

Por segurança, só é permitido:
- `SELECT`, `SHOW`, `DESCRIBE`/`DESC`, `EXPLAIN` — sempre somente leitura
- `CALL` de procedure — pode gravar dado de verdade (ex:
  `sp_matricular_aluno_em_turma`), a interface avisa isso

Qualquer `INSERT`/`UPDATE`/`DELETE`/`DROP`/`ALTER`/... é bloqueado antes
de chegar ao MySQL (validação em `validators.validate_console_query`),
assim como múltiplos comandos separados por `;` ou comentários SQL.

**Importante:** para a demonstração oficial dos requisitos (View,
Procedure, Trigger, PK automática), o mais recomendado ainda é rodar no
terminal `mysql` puro — é uma ferramenta neutra, sem qualquer dúvida de
que o resultado não vem "arranjado" pela própria aplicação. O Console SQL
é um complemento visual, não substitui essa prova.

## Acesso

Requer login (o painel está atrás do guard de autenticação, como o resto
do sistema). Use a conta de demonstração:

```
E-mail: ana.ferreira@aluno.unb.br
Senha:  senha123
```

## Uso de IA

Claude (Anthropic) gerou o blueprint `rotas/demo.py`, os templates em
`templates/demo/` e os testes de fumaça (smoke tests com conexão MySQL
mockada) usados para validar cada rota antes do push, com o objetivo de
criar uma forma de demonstrar visualmente, dentro do próprio app, os
requisitos obrigatórios da especificação (view, procedure, trigger, PK
automática e CRUD multi-tabela). Também gerou o Console SQL
(`rotas/console.py`, `services/console_service.py`, validação em
`validators.py`), com o objetivo de oferecer uma área de consulta segura
e somente-leitura como complemento visual à demonstração.
