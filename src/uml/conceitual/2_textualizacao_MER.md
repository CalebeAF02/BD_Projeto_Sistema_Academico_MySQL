```
UNIVERSIDADE DE BRASÍLIA
INSTITUTO DE CIÊNCIAS EXATAS
DEPARTAMENTO DE CIÊNCIA DA COMPUTAÇÃO
DISCIPLINA: BANCO DE DADOS
```
MODELO ENTIDADE-RELACIONAMENTO TEXTUAL (ENTREGA 2)
---

TEMA: SISTEMA DE ACOMPANHAMENTO ACADÊMICO
---

### Descrição Conceitual e Regras de Negócio do Modelo Lógico

1. **PESSOA, ALUNO E PROFESSOR (Herança):** A entidade Pessoa funciona como a entidade base do sistema (contendo os atributos primordiais id, nome, cpf, sexo e data_nascimento). Ela se especializa de forma exclusiva em Aluno (caracterizado pelo atributo tipo) ou em Professor (caracterizado pelos atributos tipo e nivel).

2. **CONTA (Autenticação):** Uma Pessoa pode possuir no máximo uma Conta de acesso ao ambiente digital (relacionamento 1:1 parcial). A entidade Conta armazena informações de credenciais, contendo os atributos id, email, senha, tipo, data_criacao e status.

3. **INFRAESTRUTURA CAMPUS:** Um Departamento atua como unidade administrativa centralizadora (atributos id e nome). Um Departamento possui uma ou mais estruturas de Predio (relação 1:n). Cada Predio (contendo id, nome e agregados de endereco) possui uma ou mais estruturas de Sala (relação 1:n), caracterizadas por id, codigo e capacidade.

4. **ALOCAÇÃO DE ESPAÇO FÍSICO:** Uma Sala e uma Turma se interconectam por meio de uma entidade associativa de relacionamento n:m mapeada como Alocacao_Sala. Esta entidade gerencia os horários de ocupação física guardando os atributos próprios id, dia_semana, hora_abertura, hora_fechamento e status.

5. **ESTRUTURAÇÃO ACADÊMICA VIGENTE (Oferta):** A entidade Oferta atua como o nó central de amarração do semestre letivo. Ela agrega em um único registro os relacionamentos vindos em cascata de: um Curso (1:n), um Semestre (1:n), uma Disciplina (1:n) e o Departamento responsável. Uma Oferta possui os atributos id e codigo_oferta, e pode gerar uma ou várias Turmas (relação 1:n).

6. **TURMA:** A entidade Turma (atributos id, codigo e quantidade_vagas) materializa as turmas abertas a partir de uma oferta.

7. **VÍNCULO DOCENTE:** Professores ministram turmas através da entidade associativa n:m denominada Professor_Disciplina (relacionando Professor e Turma). Esta tabela armazena dados contextuais da atuação do professor na respectiva classe através dos atributos id, funcao, carga_horaria, data_inicio e data_fim.

8. **MATRÍCULAS DOS ESTUDANTES:** Um Aluno realiza uma ou mais Matricula_Curso (relação 1:n) para oficializar seu ingresso na universidade. Para se inscrever nas matérias do semestre, ocorre o cruzamento n:m entre a tabela de Matricula_Curso e a tabela de Turma, gerando a entidade central Matricula_Disciplina. Esta possui os atributos id, codigo, data_matricula, data_trancamento, nota final e status.

9. **REPOSITÓRIO DE APOIO:** Cada Disciplina cadastrada no sistema pode possuir um ou mais registros de Material_Estudo associados (relação 1:n). Esta tabela armazena os metadados de suporte através dos atributos id, titulo, descricao, tipo e link.

10. **DIÁRIO DE CLASSE E FREQUÊNCIA:** Uma Turma possui uma sequência de Aulas registradas em seu diário (relação 1:n). A presença do estudante é gerenciada por meio de um cruzamento n:m entre as entidades Aula e Matricula_Disciplina, dando origem à tabela Frequencia. Ela mapeia o diário nominal guardando os atributos id, presente (booleano), data_registro e observacao.

11. **AVALIAÇÕES E RESULTADOS:** Uma Turma cria e gerencia uma ou mais Avaliacao ao longo do período letivo (relação 1:n). Para documentar o histórico de notas, cada Avaliacao se conecta de forma n:m com a tabela de alunos inscritos (Matricula_Disciplina), gerando a entidade Resultado_Avaliacao. Ela rastreia as métricas do aluno através dos atributos id, nota, feedback, status e data_entrega.

12. **AGENDA E EVENTOS:** Uma Turma pode organizar ou receber múltiplos eventos acadêmicos (relação 1:n). A entidade Evento é monitorada através dos atributos id, titulo, descricao, tipo, data_inicio, data_fim e local.

13. **GESTÃO DE METAS PESSOAIS:** Cada Aluno cadastrado possui autonomia para gerenciar de forma exclusiva o seu painel de Meta_Estudo (relação 1:n). Esta entidade monitora o engajamento individual pelos atributos id, titulo, horas, prazo e status.

14. **CENTRAL DE LOG DE NOTIFICAÇÕES:** O sistema emite registros globais na tabela Notificacao. O envio direcionado dessas mensagens para as contas dos usuários ocorre de forma n:m através da entidade associativa Notificacao_Conta. Ela atua como um log de controle avançado contendo os atributos id, data_envio, data_recebimento, lida (booleano) e mensagem_resposta.
