# 🎓 Sistema de Acompanhamento Acadêmico

Projeto desenvolvido para a disciplina de **Banco de Dados** do Departamento de Ciência da Computação (CIC) do Instituto de Ciências Exatas (IE) na **Universidade de Brasília (UnB)**.

O sistema consiste em uma plataforma de apoio voltada a auxiliar estudantes no acompanhamento detalhado de suas disciplinas, frequências, avaliações, materiais didáticos, notificações de desempenho e metas de estudo pessoais durante o semestre letivo, além de otimizar a gestão de turmas e diários de classe pelos professores.

---

## 👥 Integrantes do Grupo
* **Arthur Braga Moura de Jesus**
* **Calebe Alves Freitas**
* **Isabela de Souza Clímaco**
* **Vitor Ivan Gonçalves de Oliveira**

---

## 🚀 Principais Funcionalidades

### 👨‍🎓 Para o Aluno
* Consultar histórico de ofertas acadêmicas e disciplinas matriculadas.
* Visualizar notas, conceitos e feedbacks detalhados por avaliação.
* Acompanhar frequência detalhada integrada aos diários de classe.
* Receber alertas automáticos de desempenho e comunicados através da central de notificações.
* Consultar agendas e calendários de eventos vinculados às turmas.
* Definir, mensurar e acompanhar o progresso de metas de estudo individuais.

### 👨‍🏫 Para o Professor
* Gerenciar diários de classe com abertura de aulas e conteúdos programáticos.
* Registrar frequências de alunos de forma individualizada.
* Cadastrar e gerenciar avaliações com definição de pesos e notas máximas.
* Realizar o lançamento de notas, feedbacks e definição de status de aprovação.
* Disponibilizar links e materiais didáticos de estudo vinculados às disciplinas.
* Criar e divulgar eventos acadêmicos diretamente nas turmas que ministra.

---

## 📐 Estrutura de Modelagem do Banco de Dados

O ecossistema de banco de dados do projeto foi projetado seguindo as metodologias clássicas de engenharia de dados, estruturando-se através de:
1. **Documento de Requisitos (Levantamento de Escopo)**
2. **Modelo Entidade-Relacionamento (MER Textual)**
3. **Diagrama Entidade-Relacionamento (DER Conceitual)**
4. **Modelo Relacional Físico (Código DDL SQL)**

O banco de dados atende às regras de normalização e conta com **25 entidades mapeadas**, cobrindo desde a infraestrutura física da universidade (Departamentos, Prédios e Salas) até o controle lógico acadêmico.

---

### 📄 Modelo de Entidade-Relacionamento (MER)


### [MER](docs\entregas\2_textualizacao_MER.md)


> *Nota: O modelo original em formato de arquivo brModelo encontra-se dentro do diretório `/docs/entregas`.*

---

### 🖼️ Diagrama de Entidade-Relacionamento (DER)

![Diagrama Entidade-Relacionamento (DER)](src\uml\conceitual\DER.png)

> *Nota: O modelo original em formato de arquivo brModelo encontra-se dentro do diretório `/src/uml/conceitual`.*

---

### 🖼️ Modelo Relacional (MR)

![Diagrama Entidade-Relacionamento (DER)](src\uml\logico\MR.png)

> *Nota: O modelo original em formato de arquivo brModelo encontra-se dentro do diretório `/src/uml/logico`.*

---

## 🤖 Uso de Inteligência Artificial (IA)
Conforme as diretrizes e exigências estabelecidas na especificação do projeto da UnB, informamos o mapeamento do uso de ferramentas de IA no desenvolvimento desta etapa.

---

## 📂 Estrutura do Repositório

```text
├── docs/
│   ├── entregas/
│   │   ├── 1_analise_de_requesitos.md
│   │   └── 2_textualizacao_MER.md
│   └── especificacoes/
│       ├── especificacao_projeto.md
│       └── grupo_tema.md
├── src/
│   ├── sql/
│   │   └── 00_cria-banco-de-dados.sql # Script SQL DDL estruturado por dependência
│   ├── uml/
│   │   ├── conceitual/
│   │   │   ├── DER_CONCEITUAL.brM3      # Arquivo fonte do modelo conceitual (brModelo)
│   │   │   └── DER_CONCEITUAL.png       # Imagem exportada do modelo conceitual
│   │   └── logico/
│   │       ├── DER_LOGICO.puml          # Diagrama lógico em PlantUML
│   │       └── MR.brM3                  # Modelo Relacional no brModelo
│   └── sgbd/
│       └── MR.mwb                       # Arquivo de modelagem física do MySQL Workbench
└── README.md                            # Documentação principal do repositório
```

## 🛠️ Como Executar e Testar o Banco de Dados

1. Documentação Teórica
Para consultar os levantamentos de regras de negócio detalhados e fluxos lógicos relacionais textuais, acesse a pasta entregas/pdf/.

2. Criação da Estrutura Física (DDL)
Os scripts SQL contidos na pasta /scripts foram organizados de forma estrita respeitando a ordem de precedência de chaves estrangeiras (FOREIGN KEY). Para subir o banco:

Certifique-se de utilizar um SGBD relacional compatível (padrão ANSI SQL adaptado).

Execute o arquivo de scripts global para erguer a infraestrutura das 25 tabelas.

Para preenchimento rápido em modo de design no software brModelo, utilize os arquivos de texto preparados para inserção em lote na ferramenta Adicionar campos em série.

---
