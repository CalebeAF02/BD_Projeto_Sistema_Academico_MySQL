```
UNIVERSIDADE DE BRASÍLIA
INSTITUTO DE CIÊNCIAS EXATAS
DEPARTAMENTO DE CIÊNCIA DA COMPUTAÇÃO
DISCIPLINA: BANCO DE DADOS
```
DOCUMENTO DE REQUISITOS (ENTREGA 1)
---

TEMA: SISTEMA DE ACOMPANHAMENTO ACADÊMICO
---

### 1. Visão Geral
Sistema de Apoio e Acompanhamento Acadêmico desenvolvido para apoiar as atividades dos estudantes da Universidade de Brasília (UnB)[cite: 1, 3]. O objetivo central do ecossistema é auxiliar o corpo discente durante o semestre letivo no monitoramento integrado de suas ofertas acadêmicas, turmas, notas, diários de classe com registros de frequência, eventos da agenda universitária, materiais de estudo fornecidos e gerenciamento de metas pessoais de desempenho[cite: 3].

### 2. Público-Alvo
* Alunos da instituição[cite: 5].
* Professores do departamento[cite: 5].

### 3. Requisitos Funcionais (RF)
* **RF01 – Autenticação de Usuários:** O sistema deve permitir a validação e controle de acesso seguro correlacionando as entidades Pessoa e Conta.
* **RF02 – Gerenciamento de Alunos:** Permitir o cadastro, consulta e manutenção de dados específicos dos alunos (como especialização da entidade Pessoa).
* **RF03 – Gerenciamento de Professores:** Permitir o cadastro, vínculo departamental e manutenção de dados dos docentes (como especialização da entidade Pessoa).
* **RF04 – Cadastro de Departamentos:** Permitir o registro e controle dos departamentos do instituto (ex: Departamento de Ciência da Computação - CIC).
* **RF05 – Mapeamento de Infraestrutura (Prédios):** Permitir o cadastro de prédios físicos vinculados diretamente a um departamento institucional.
* **RF06 – Mapeamento de Infraestrutura (Salas):** Permitir o cadastro de salas de aula físicas associadas às suas respectivas estruturas de prédios.
* **RF07 – Cadastro de Cursos:** Permitir o gerenciamento de cursos de graduação e pós-graduação da instituição (ex: Bacharelado em Ciência da Computação).
* **RF08 – Controle de Semestres Letivos:** Permitir a abertura e configuração dos períodos vigentes (ex: 2026/1) com data de início e término.
* **RF09 – Cadastro de Disciplinas:** Permitir o gerenciamento da grade de disciplinas pertencentes aos cursos da universidade.
* **RF10 – Configuração de Ofertas Acadêmicas:** Permitir a consolidação estrutural unindo um Curso, um Semestre, uma Disciplina e o Departamento responsável em uma Oferta unificada.
* **RF11 – Abertura de Turmas:** Permitir a criação de turmas específicas vinculadas obrigatoriamente a uma Oferta Acadêmica ativa.
* **RF12 – Alocação Física de Salas:** Permitir associar turmas a salas específicas, delimitando o dia da semana, horários de abertura/fechamento e status da alocação.
* **RF13 – Atribuição de Corpo Docente:** Permitir vincular professores a turmas através de uma tabela associativa, determinando sua função na classe e carga horária contratual.
* **RF14 – Registro de Matrícula em Curso:** Permitir criar o vínculo formal de ingresso e histórico de um Aluno em um Curso específico.
* **RF15 – Matrícula em Disciplinas (Turmas):** Permitir a inscrição de alunos vinculados a uma matrícula de curso dentro de turmas específicas das disciplinas do semestre.
* **RF16 – Diário de Classe (Aulas):** Permitir que o professor registre a ocorrência de aulas individuais em uma turma, apontando data, tipo e conteúdo programático.
* **RF17 – Lançamento de Frequência:** Permitir o controle nominal e diário de presença/ausência de um aluno matriculado com base nas aulas registradas no diário.
* **RF18 – Criação de Avaliações:** Permitir o agendamento e parametrização de testes, provas e trabalhos por turma, definindo pesos e notas máximas aplicáveis.
* **RF19 – Lançamento de Notas e Feedbacks:** Permitir o registro de notas alcançadas pelos alunos nas avaliações, incluindo comentários de feedback e status.
* **RF20 – Agenda de Eventos Acadêmicos:** Permitir o cadastro de eventos, palestras ou atividades extras diretamente associados ao ecossistema de uma turma.
* **RF21 – Repositório de Materiais de Estudo:** Permitir que materiais e links de apoio didático sejam acoplados diretamente ao escopo centralizado de uma disciplina.
* **RF22 – Painel de Metas de Estudo (Gamificação):** Permitir ao aluno criar planejamentos de horas de estudo individuais, estipular prazos e gerenciar o status de conclusão de suas metas.
* **RF23 – Distribuição de Notificações:** Permitir que a central envie comunicados do sistema para contas de usuários com controle de logs (data de envio, recebimento, leitura e resposta).

### 4. Requisitos Não Funcionais (RNF)
* **RNF01 – Arquitetura do Sistema:** Sistema baseado em plataforma Web.
* **RNF02 – Tecnologia do Backend:** Desenvolvimento da lógica de negócios e persistência na linguagem Python.
* **RNF03 – Tecnologia do Frontend:** Interface construída utilizando padrões estruturais de HTML.
* **RNF04 – Persistência de Dados:** Uso obrigatório de um Sistema Gerenciador de Banco de Dados Relacional (SGBD MySQL).
* **RNF05 – Segurança:** Controle rígido de autenticação e barramento de autorização com base no tipo de conta logada (Aluno/Professor).
* **RNF06 – Usabilidade:** Interface gráfica limpa, responsiva, simples e intuitiva focada na experiência de uso dos estudantes universitários.

### 5. Casos de Uso Principais
* Realizar Login no Sistema.
* Consultar Matrículas e Ofertas Acadêmicas do Semestre.
* Visualizar Notas, Conceitos e Históricos de Avaliações.
* Consultar Frequência Consolidada e Diário de Classe.
* Acessar Materiais de Apoio e Links Didáticos.
* Criar e Acompanhar Metas de Estudo Individuais.
* Consultar Calendário de Eventos Acadêmicos.
* Receber e Interagir com Notificações do Sistema.
