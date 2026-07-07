# 🗺️ Arquitetura de Navegação e Lógica de Domínios (SGA UnB)

Este documento detalha o fluxo de navegação de páginas e o controle de acesso baseado em domínio de e-mail para o **Sistema de Gestão Acadêmica (SGA UnB)**, conectando a interface visual às tabelas do banco de dados MySQL.

---

## 🔐 1. Fluxo de Autenticação e Roteamento Inicial

O ponto de entrada do sistema é a tela de login. O redirecionamento e as permissões de navegação subsequentes são determinados pelo mapeamento estrito da string de domínio do e-mail cadastrado na tabela `CONTA`.

### 🛡️ Matriz de Perfis por Domínio de E-mail

| Domínio do E-mail | Perfil (*Role*) | Escopo de Páginas Permitidas | Rota de Destino Padrão |
| :--- | :--- | :--- | :--- |
| **`@aluno.unb.br`** | Aluno | Painel (Visão Aluno), Disciplinas, Matrículas, Turmas | `/painel/aluno` |
| **`@professor.unb.br`** | Professor | Painel (Visão Professor), Alunos, Disciplinas, Turmas | `/painel/professor` |
| **`@adm.unb.br`** | Administrador | **Acesso Completo** (Inclui Demonstração, Console SQL e Status DB) | `/admin/console` |

---

## 🔄 2. Macrofluxograma de Navegação (State Machine)

Use o código com cuidado.[ 🔐 TELA DE LOGIN ]│POST /login (Email, Password)│┌──────────────┴──────────────┐▼                             ▼[ Credenciais Inválidas ]     [ Credenciais Válidas ]│                             │Retorna Erro 401                       ▼Isolamento de CONTA.email│┌─────────────────────────────────────┼─────────────────────────────────────┐▼                                     ▼                                     ▼[ Domínio: @aluno.unb.br ]          [ Domínio: @professor.unb.br ]        [ Domínio: @adm.unb.br ]│                                     │                                     │Session: PERFIL="ALUNO"               Session: PERFIL="PROFESSOR"           Session: PERFIL="ADMIN"▼                                     ▼                                     ▼Redireciona: /painel/aluno          Redireciona: /painel/professor      Redireciona: /admin/console
---

## 🧭 3. Lógica de Telas por Módulo Acadêmico

### 🎓 3.1. Visão do Aluno (`@aluno.unb.br`)
Interface focada no autoacompanhamento pedagógico e gerenciamento de metas.

*   **`/painel/aluno` (Dashboard):** Exibe métricas consolidadas (percentual geral de presença, conceito parcial estimado e quantidade de notificações não lidas).
*   **`/matriculas` (Minhas Turmas):** Lista os registros ativos em `MATRICULA_DISCIPLINA`. Ao selecionar uma disciplina, o aluno navega para:
    *   **`/matriculas/notas`:** Consulta os dados na tabela `RESULTADO_AVALIACAO`.
    *   **`/matriculas/frequencia`:** Consulta o diário de faltas na tabela `FREQUENCIA`.
*   **`/disciplinas` (Catálogo):** Permite visualizar a grade curricular da instituição e baixar arquivos vinculados na tabela `MATERIAL_DE_ESTUDO`.
*   **`/metas` (Painel Pessoal):** Permite operações de CRUD completas (Criar, Ler, Atualizar, Deletar) na tabela `META_DE_ESTUDO`.

---

### 👨‍🏫 3.2. Visão do Professor (`@professor.unb.br`)
Interface focada na gestão de turmas ativas e lançamentos oficiais do diário de classe.

*   **`/painel/professor` (Dashboard):** Lista as turmas vinculadas ao docente através da tabela associativa `PROFESSOR_TURMA`.
*   **`/turma/gerenciar` (Painel da Classe):** Ao selecionar uma turma específica, o professor acessa as seguintes funcionalidades:
    *   **`/diario/aulas`:** Permite inserir um novo registro na tabela `AULA`. Ao salvar a aula, abre automaticamente o formulário de chamada.
    *   **`/diario/chamada`:** Realiza um *Bulk-Insert* (inserção múltipla) na tabela `FREQUENCIA` definindo a presença (booleano) para cada aluno matriculado.
    *   **`/avaliacoes`:** Permite cadastrar uma nova atividade na tabela `AVALIACAO` (vinculando peso e nota máxima).
    *   **`/avaliacoes/notas`:** Abre a planilha para lançamento de notas individuais na tabela `RESULTADO_AVALIACAO`.

---

### 💻 3.3. Visão do Administrador / Sistema (`@adm.unb.br`)
Módulo restrito com privilégios de manutenção, carga de dados e gerenciamento de infraestrutura física.

*   **`/admin/infraestrutura`:** Permite cadastrar novos blocos administrativos (`DEPARTAMENTO` ➔ `PREDIO` ➔ `SALA`).
*   **`/admin/ofertas`:** Cria o ponto central de amarração do semestre letivo na tabela `OFERTA`, vinculando uma disciplina a um curso específico antes de abrir as turmas.
*   **`/admin/demonstracao`:** Executa scripts isolados (*sandbox*) para popular as 25 tabelas do banco com dados simulados para apresentações acadêmicas.
*   **`/admin/console-sql`:** Interface para execução de comandos DDL/DML arbitrários direto no SGBD MySQL (restrito a engenheiros e administradores do sistema).
*   **`/admin/status-db`:** Monitora o número de conexões ativas e a integridade do armazenamento físico das tabelas.

---

## 🔒 4. Middleware de Segurança (Proteção contra Acesso Direto por URL)

Para evitar que um usuário pule etapas de navegação inserindo caminhos diretamente na barra de endereços do navegador (vulnerabilidade IDOR), cada requisição de página passa por um interceptador de rotas baseado nesta lógica de controle de acesso:

```python
def interceptador_de_rotas(requisicao, sessao_usuario):
    rota_alvo = requisicao.url_path
    
    # 1. Permite acesso livre para páginas públicas
    if rota_alvo in ["/login", "/recuperar-senha", "/public/style.css"]:
        return permitir_acesso()
        
    # 2. Bloqueia acessos anônimos se a sessão não existir
    if not sessao_usuario.esta_ativa():
        return redirecionar_para("/login", mensagem="Sessão expirada. Autentique-se.")
        
    # 3. Validação estrita de escopo por perfil de domínio
    if rota_alvo.startswith("/admin/") and sessao_usuario.perfil != "ADMIN":
        return emitir_erro_403_proibido()
        
    if rota_alvo.startswith("/turma/") and sessao_usuario.perfil != "PROFESSOR":
        return emitir_erro_403_proibido()
        
    if rota_alvo.startswith("/metas") and sessao_usuario.perfil != "ALUNO":
        return emitir_erro_403_proibido()
        
    # 4. Autorização concedida se o perfil corresponder à rota
    return renderizar_pagina_solicitada()
```