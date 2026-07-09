"""
Script de validação do CRUD - executa sem framework de testes formal.
Rode a partir de src/python/:
    python tests/test_crud.py

Importante: esse script deve ser o primeiro teste executado após criar o banco
and carregar os scripts SQL, pois alguns cenários dependem de dados já
presentes no banco (seeds, relacionamentos e IDs esperados). Alterações no
schema ou nos dados iniciais podem causar falhas em testes posteriores.
"""
import sys
import os
import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from database.connection import get_connection
from repositories.pessoa_repository import PessoaRepository
from repositories.aluno_repository import AlunoRepository
from repositories.professor_repository import ProfessorRepository
from repositories.departamento_repository import DepartamentoRepository
from repositories.curso_repository import CursoRepository
from repositories.disciplina_repository import DisciplinaRepository
from repositories.semestre_repository import SemestreRepository
from repositories.oferta_repository import OfertaRepository
from repositories.turma_repository import TurmaRepository
from repositories.matricula_curso_repository import MatriculaCursoRepository
from repositories.matricula_disciplina_repository import MatriculaDisciplinaRepository
from repositories.avaliacao_repository import AvaliacaoRepository
from repositories.resultado_avaliacao_repository import ResultadoAvaliacaoRepository
from services.matricula_service import matricular_aluno_em_disciplina, buscar_historico_aluno

PASS = "[OK]"
FAIL = "[FALHA]"
_erros = []


def ok(label, valor=None):
    msg = f"  {PASS} {label}"
    if valor is not None:
        msg += f" -> {valor}"
    print(msg)


def falha(label, detalhe=""):
    msg = f"  {FAIL} {label}"
    if detalhe:
        msg += f" → {detalhe}"
    print(msg)
    _erros.append(label)


def secao(titulo):
    print(f"\n{'='*60}")
    print(f"  {titulo}")
    print(f"{'='*60}")


# -----------------------------------------------------------------------
# Helpers de limpeza - removem registros criados pelo teste
# -----------------------------------------------------------------------
def limpar(conn, tabela, campo, valor):
    try:
        c = conn.cursor()
        c.execute(f"DELETE FROM {tabela} WHERE {campo} = %s", (valor,))
        conn.commit()
    except Exception:
        pass


# =====================================================================
# CRUD - PESSOA + FOTO (binário)
# =====================================================================
def testar_pessoa(conn):
    secao("CRUD - pessoa (inclui foto BLOB)")
    repo = PessoaRepository(conn)
    # Remove registro residual de execução anterior
    limpar(conn, "pessoa", "cpf", "99988877766")

    # CREATE
    id_p = repo.create("Teste CRUD", "99988877766", "M", datetime.date(2000, 1, 1))
    if id_p:
        ok("create pessoa", f"id={id_p}")
    else:
        falha("create pessoa"); return

    # READ
    p = repo.find_by_id(id_p)
    if p and p["nome"] == "Teste CRUD":
        ok("find_by_id pessoa", p["nome"])
    else:
        falha("find_by_id pessoa")

    # UPDATE
    rows = repo.update(id_p, nome="Teste CRUD Atualizado")
    p2 = repo.find_by_id(id_p)
    if rows and p2["nome"] == "Teste CRUD Atualizado":
        ok("update pessoa", p2["nome"])
    else:
        falha("update pessoa")

    # FOTO - dado binário
    foto_bytes = b"\x89PNG\r\nFAKE_IMAGE_BYTES_FOR_TEST"
    repo.update_foto(id_p, foto_bytes)
    foto_lida = repo.find_foto(id_p)
    if foto_lida == foto_bytes:
        ok("update_foto / find_foto (BLOB)", f"{len(foto_lida)} bytes gravados e lidos corretamente")
    else:
        falha("update_foto / find_foto (BLOB)")

    # FIND ALL
    todos = repo.find_all()
    if todos:
        ok("find_all pessoa", f"{len(todos)} registros")
    else:
        falha("find_all pessoa")

    # DELETE
    repo.delete(id_p)
    if not repo.find_by_id(id_p):
        ok("delete pessoa")
    else:
        falha("delete pessoa")


# =====================================================================
# CRUD - ALUNO
# =====================================================================
def testar_aluno(conn):
    secao("CRUD - aluno")
    p_repo = PessoaRepository(conn)
    a_repo = AlunoRepository(conn)
    limpar(conn, "pessoa", "cpf", "11100099988")

    id_p = p_repo.create("Aluno Teste", "11100099988", "F", datetime.date(2003, 5, 10))
    a_repo.create(id_p, "GRADUACAO")

    a = a_repo.find_by_id(id_p)
    if a and a["tipo"] == "GRADUACAO":
        ok("create + find_by_id aluno", a["nome"])
    else:
        falha("create + find_by_id aluno")

    a_repo.update(id_p, "POS_GRADUACAO")
    a2 = a_repo.find_by_id(id_p)
    if a2 and a2["tipo"] == "POS_GRADUACAO":
        ok("update aluno", a2["tipo"])
    else:
        falha("update aluno")

    todos = a_repo.find_all()
    ok("find_all aluno", f"{len(todos)} registros")

    a_repo.delete(id_p)
    p_repo.delete(id_p)
    if not a_repo.find_by_id(id_p):
        ok("delete aluno")
    else:
        falha("delete aluno")


# =====================================================================
# CRUD - PROFESSOR
# =====================================================================
def testar_professor(conn):
    secao("CRUD - professor")
    p_repo = PessoaRepository(conn)
    pr_repo = ProfessorRepository(conn)
    limpar(conn, "pessoa", "cpf", "33322211100")

    id_p = p_repo.create("Professor Teste", "33322211100", "M", datetime.date(1978, 3, 20))
    pr_repo.create(id_p, 1, "EFETIVO", "ADJUNTO")

    pr = pr_repo.find_by_id(id_p)
    if pr and pr["nivel"] == "ADJUNTO":
        ok("create + find_by_id professor", pr["nome"])
    else:
        falha("create + find_by_id professor")

    pr_repo.update(id_p, nivel="ASSOCIADO")
    pr2 = pr_repo.find_by_id(id_p)
    if pr2 and pr2["nivel"] == "ASSOCIADO":
        ok("update professor", pr2["nivel"])
    else:
        falha("update professor")

    todos = pr_repo.find_all()
    ok("find_all professor", f"{len(todos)} registros")

    pr_repo.delete(id_p)
    p_repo.delete(id_p)
    ok("delete professor")


# =====================================================================
# CRUD - DEPARTAMENTO
# =====================================================================
def testar_departamento(conn):
    secao("CRUD - departamento")
    repo = DepartamentoRepository(conn)

    id_d = repo.create("Depto Teste CRUD")
    d = repo.find_by_id(id_d)
    if d and d["nome"] == "Depto Teste CRUD":
        ok("create + find_by_id departamento", d["nome"])
    else:
        falha("create + find_by_id departamento")

    repo.update(id_d, "Depto Teste CRUD Atualizado")
    d2 = repo.find_by_id(id_d)
    if d2 and "Atualizado" in d2["nome"]:
        ok("update departamento", d2["nome"])
    else:
        falha("update departamento")

    ok("find_all departamento", f"{len(repo.find_all())} registros")

    repo.delete(id_d)
    if not repo.find_by_id(id_d):
        ok("delete departamento")
    else:
        falha("delete departamento")


# =====================================================================
# CRUD - CURSO
# =====================================================================
def testar_curso(conn):
    secao("CRUD - curso")
    repo = CursoRepository(conn)

    id_c = repo.create("Curso Teste CRUD", "CTC")
    c = repo.find_by_id(id_c)
    if c and c["sigla"] == "CTC":
        ok("create + find_by_id curso", c["nome"])
    else:
        falha("create + find_by_id curso")

    repo.update(id_c, sigla="CTA")
    c2 = repo.find_by_id(id_c)
    if c2 and c2["sigla"] == "CTA":
        ok("update curso", c2["sigla"])
    else:
        falha("update curso")

    ok("find_all curso", f"{len(repo.find_all())} registros")
    repo.delete(id_c)
    ok("delete curso")


# =====================================================================
# CRUD - DISCIPLINA
# =====================================================================
def testar_disciplina(conn):
    secao("CRUD - disciplina")
    repo = DisciplinaRepository(conn)

    id_d = repo.create("TST9999", "Disciplina Teste CRUD")
    d = repo.find_by_id(id_d)
    if d and d["codigo"] == "TST9999":
        ok("create + find_by_id disciplina", d["nome"])
    else:
        falha("create + find_by_id disciplina")

    repo.update(id_d, nome="Disciplina Teste Atualizada")
    d2 = repo.find_by_id(id_d)
    if d2 and "Atualizada" in d2["nome"]:
        ok("update disciplina", d2["nome"])
    else:
        falha("update disciplina")

    ok("find_all disciplina", f"{len(repo.find_all())} registros")
    repo.delete(id_d)
    ok("delete disciplina")


# =====================================================================
# CRUD - SEMESTRE
# =====================================================================
def testar_semestre(conn):
    secao("CRUD - semestre")
    repo = SemestreRepository(conn)

    id_s = repo.create("2099/1", datetime.date(2099, 3, 1), datetime.date(2099, 7, 31))
    s = repo.find_by_id(id_s)
    if s and s["nome"] == "2099/1":
        ok("create + find_by_id semestre", s["nome"])
    else:
        falha("create + find_by_id semestre")

    repo.update(id_s, nome="2099/1-A")
    s2 = repo.find_by_id(id_s)
    if s2 and s2["nome"] == "2099/1-A":
        ok("update semestre", s2["nome"])
    else:
        falha("update semestre")

    ok("find_all semestre", f"{len(repo.find_all())} registros")
    repo.delete(id_s)
    ok("delete semestre")


# =====================================================================
# CRUD - MATRICULA_CURSO
# =====================================================================
def testar_matricula_curso(conn):
    secao("CRUD - matricula_curso")
    repo = MatriculaCursoRepository(conn)

    mc = repo.find_by_aluno(1)
    if mc:
        ok("find_by_aluno (aluno seed id=1)", f"{len(mc)} matrículas")
    else:
        falha("find_by_aluno")

    mc_ativa = repo.find_ativa_por_aluno(1)
    if mc_ativa:
        ok("find_ativa_por_aluno (aluno seed id=1)", f"id={mc_ativa['id']}")
    else:
        falha("find_ativa_por_aluno")

    ok("find_all matricula_curso", f"{len(repo.find_all())} registros")


# =====================================================================
# CRUD - AVALIACAO + RESULTADO (trigger)
# =====================================================================
def testar_avaliacao_e_trigger(conn):
    secao("CRUD - avaliacao + resultado_avaliacao + trigger")
    av_repo = AvaliacaoRepository(conn)
    ra_repo = ResultadoAvaliacaoRepository(conn)
    md_repo = MatriculaDisciplinaRepository(conn)

    # Cria avaliação na turma 1 (seed)
    id_av = av_repo.create(
        id_turma=1, titulo="Prova Trigger Test", tipo="PROVA",
        peso=2.00, nota_maxima=10.0, data_aplicacao=datetime.date(2099, 4, 1)
    )
    ok("create avaliacao", f"id={id_av}")

    # Antes do resultado: nota da md=1
    md_antes = md_repo.find_by_id(1)
    nota_antes = md_antes["nota"]

    # INSERT em resultado_avaliacao - dispara trigger
    id_ra = ra_repo.create(
        id_avaliacao=id_av,
        id_matricula_disciplina=1,
        nota=10.0,
        status="CORRIGIDO",
        data_entrega=datetime.date(2099, 4, 2),
    )
    ok("create resultado_avaliacao (dispara trigger)", f"id={id_ra}")

    # Verifica que trigger atualizou a nota
    md_depois = md_repo.find_by_id(1)
    nota_depois = md_depois["nota"]
    if nota_depois != nota_antes:
        ok("trigger tg_atualiza_nota_final_insert", f"nota: {nota_antes} -> {nota_depois}")
    else:
        falha("trigger não atualizou nota_final")

    # UPDATE em resultado - dispara trigger update
    ra_repo.update(id_ra, nota=5.0)
    md_update = md_repo.find_by_id(1)
    nota_update = md_update["nota"]
    if nota_update != nota_depois:
        ok("trigger tg_atualiza_nota_final_update", f"nota após update: {nota_update}")
    else:
        falha("trigger update não recalculou nota")

    # Limpeza
    ra_repo.delete(id_ra)
    av_repo.delete(id_av)
    ok("delete avaliacao + resultado (limpeza)")


# =====================================================================
# Função multi-tabela - matricular_aluno_em_disciplina
# =====================================================================
def testar_matricula_multitabela():
    secao("Função multi-tabela - matricular_aluno_em_disciplina")

    # Aluno 2 (Bruno) na oferta 3 (Grafos - turma com vagas)
    resultado = matricular_aluno_em_disciplina(id_pessoa=2, id_oferta=3)
    if resultado["ok"]:
        ok("matricular_aluno_em_disciplina", f"id_md={resultado['id_matricula_disciplina']}")
        id_md_novo = resultado["id_matricula_disciplina"]
    else:
        falha("matricular_aluno_em_disciplina", resultado["erro"])
        id_md_novo = None

    # Testa erro: pessoa inválida
    res_invalido = matricular_aluno_em_disciplina(id_pessoa=9999, id_oferta=1)
    if not res_invalido["ok"] and "aluno" in res_invalido["erro"].lower():
        ok("erro esperado para id_pessoa inválido", res_invalido["erro"])
    else:
        falha("não retornou erro para id_pessoa inválido")

    # Limpeza
    if id_md_novo:
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM matricula_disciplina WHERE id = %s", (id_md_novo,))
        conn.commit()
        conn.close()
        ok("limpeza matrícula criada pelo teste")


# =====================================================================
# View - buscar_historico_aluno
# =====================================================================
def testar_historico_aluno():
    secao("View - buscar_historico_aluno (vw_historico_aluno)")

    try:
        historico = buscar_historico_aluno(id_aluno=1)
    except Exception as e:
        falha("buscar_historico_aluno lançou exceção", str(e))
        return
    
    
    if historico:
        h = historico[0]
        ok("buscar_historico_aluno (aluno seed id=1)", f"{len(historico)} linha(s)")
        ok("campos retornados", f"semestre={h['semestre']}, disciplina={h['nome_disciplina']}, nota={h['nota_final']}")
    else:
        falha("buscar_historico_aluno retornou vazio")


# =====================================================================
# FIND ALL - seeds (verifica 5+ registros por tabela)
# =====================================================================
def testar_seeds_count(conn):
    secao("Seeds - contagem de registros (>=5 por tabela)")
    tabelas = [
        "pessoa", "departamento", "curso", "semestre", "disciplina",
        "notificacao", "aluno", "professor", "conta", "predio", "sala",
        "matricula_curso", "oferta", "turma", "professor_turma",
        "matricula_disciplina", "aula", "avaliacao", "resultado_avaliacao",
        "frequencia", "evento", "material_de_estudo", "meta_de_estudo",
        "notificacao_conta", "alocacao_sala",
    ]
    cursor = conn.cursor()
    for t in tabelas:
        cursor.execute(f"SELECT COUNT(*) FROM {t}")
        (count,) = cursor.fetchone()
        if count >= 5:
            ok(f"{t}", f"{count} registros")
        else:
            falha(f"{t} tem menos de 5 registros", f"encontrados: {count}")


# =====================================================================
# MAIN
# =====================================================================
if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("  TESTE DE CRUD - Sistema Acadêmico UnB")
    print("=" * 60)

    conn = get_connection()
    try:
        testar_pessoa(conn)
        testar_aluno(conn)
        testar_professor(conn)
        testar_departamento(conn)
        testar_curso(conn)
        testar_disciplina(conn)
        testar_semestre(conn)
        testar_matricula_curso(conn)
        testar_avaliacao_e_trigger(conn)
        testar_seeds_count(conn)
    finally:
        conn.close()

    testar_matricula_multitabela()
    testar_historico_aluno()

    print("\n" + "=" * 60)
    if _erros:
        print(f"  RESULTADO: {len(_erros)} FALHA(S)")
        for e in _erros:
            print(f"    - {e}")
    else:
        print("  RESULTADO: TODOS OS TESTES PASSARAM")
    print("=" * 60 + "\n")
