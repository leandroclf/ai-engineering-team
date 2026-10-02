"""Carrega o modelo de rastreabilidade e deriva os vínculos reversos.

Uso: python docs/anexos/build/modelo.py   (verifica consistência e sai com 1 se houver erro)
"""
import pathlib
import re
import sys

import yaml

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]


def _ler(nome):
    return yaml.safe_load((AQUI / nome).read_text(encoding="utf-8"))


def carregar():
    m = {}
    m.update(_ler("modelo-regras.yaml"))
    m.update(_ler("modelo-requisitos.yaml"))  # inclui mapeamento_specs
    m.update(_ler("modelo-casos-de-uso.yaml"))
    m.update(_ler("modelo-recomendacoes.yaml"))
    rf = {r["id"]: r for r in m["requisitos_funcionais"]}
    uc = {u["id"]: u for u in m["casos_de_uso"]}
    ca = {c["id"]: c for c in m["criterios_de_aceitacao"]}
    # Vínculos reversos: tudo é derivado das regras para manter uma única fonte.
    for r in rf.values():
        r["rn"] = []
    for u in uc.values():
        u["rn"], u["rf"] = [], []
    for c in ca.values():
        c["rn"] = []
    for rn in m["regras"]:
        for i in rn["rf"]:
            rf[i]["rn"].append(rn["id"])
        for i in rn["uc"]:
            uc[i]["rn"].append(rn["id"])
            for f in rn["rf"]:
                if f not in uc[i]["rf"]:
                    uc[i]["rf"].append(f)
        for i in rn["ca"]:
            ca[i]["rn"].append(rn["id"])
    m["_rf"], m["_uc"], m["_ca"] = rf, uc, ca
    m["_rn"] = {r["id"]: r for r in m["regras"]}
    return m


def _existe(fonte):
    caminho, _, ancora = fonte.partition("#")
    p = RAIZ / caminho
    if not p.exists():
        return f"caminho inexistente: {caminho}"
    if ancora and p.is_file():
        if ancora.lower() not in p.read_text(encoding="utf-8", errors="ignore").lower():
            return f"âncora não encontrada em {caminho}: {ancora}"
    return None


def verificar(m):
    erros = []
    for chave, rotulo in [("regras", "RN"), ("requisitos_funcionais", "RF"), ("requisitos_nao_funcionais", "RNF"),
                          ("casos_de_uso", "UC"), ("criterios_de_aceitacao", "CA"), ("recomendacoes", "REC")]:
        ids = [x["id"] for x in m[chave]]
        if len(ids) != len(set(ids)):
            erros.append(f"{rotulo}: identificadores duplicados")
        for i in ids:
            if not re.fullmatch(rf"{rotulo}-\d{{3}}", i):
                erros.append(f"{rotulo}: identificador fora do padrão: {i}")
        esperados = [f"{rotulo}-{n:03d}" for n in range(1, len(ids) + 1)]
        if ids != esperados:
            erros.append(f"{rotulo}: sequência com lacunas ou fora de ordem")
    for rn in m["regras"]:
        for campo in ("rf", "uc", "ca", "fonte"):
            if not rn.get(campo):
                erros.append(f"{rn['id']}: sem {campo}")
        for i in rn["rf"]:
            if i not in m["_rf"]:
                erros.append(f"{rn['id']}: RF inexistente {i}")
        for i in rn["uc"]:
            if i not in m["_uc"]:
                erros.append(f"{rn['id']}: UC inexistente {i}")
        for i in rn["ca"]:
            if i not in m["_ca"]:
                erros.append(f"{rn['id']}: CA inexistente {i}")
            elif m["_ca"][i]["uc"] not in rn["uc"]:
                erros.append(f"{rn['id']}: {i} pertence a {m['_ca'][i]['uc']}, que a regra não cita")
        for f in rn["fonte"]:
            if (e := _existe(f)):
                erros.append(f"{rn['id']}: {e}")
    for r in m["requisitos_funcionais"]:
        if not r["rn"]:
            erros.append(f"{r['id']}: nenhuma regra vinculada")
        for f in r["origem"]:
            if (e := _existe(f)):
                erros.append(f"{r['id']}: {e}")
    for r in m["requisitos_nao_funcionais"]:
        for f in r["origem"]:
            if (e := _existe(f)):
                erros.append(f"{r['id']}: {e}")
    for u in m["casos_de_uso"]:
        if not u["rn"]:
            erros.append(f"{u['id']}: nenhuma regra vinculada")
        if not [c for c in m["criterios_de_aceitacao"] if c["uc"] == u["id"]]:
            erros.append(f"{u['id']}: sem critério de aceitação")
    for c in m["criterios_de_aceitacao"]:
        if c["uc"] not in m["_uc"]:
            erros.append(f"{c['id']}: UC inexistente {c['uc']}")
        if not c["rn"]:
            erros.append(f"{c['id']}: nenhuma regra vinculada")
        g = c["gherkin"]
        for kw in ("Dado ", "Quando ", "Então "):
            if kw not in g:
                erros.append(f"{c['id']}: Gherkin sem '{kw.strip()}'")
    # Todos os identificadores originais do OpenSpec devem estar mapeados, e cada destino deve existir.
    ids_spec = set()
    for arq in (RAIZ / "openspec" / "specs").glob("*/spec.md"):
        ids_spec |= set(re.findall(r"^#+ ([A-Z]+-\d{3}) ", arq.read_text(encoding="utf-8"), re.M))
    mapa = m["mapeamento_specs"]
    if set(mapa) != ids_spec:
        erros.append(f"mapeamento_specs diverge do OpenSpec: faltam {sorted(ids_spec - set(mapa))}, sobram {sorted(set(mapa) - ids_spec)}")
    todos = set(m["_rn"]) | set(m["_rf"])
    for origem, destinos in mapa.items():
        for d in destinos:
            if d not in todos:
                erros.append(f"mapeamento_specs: {origem} aponta para {d}, que não existe")
    for rec in m["recomendacoes"]:
        if rec["status"] not in ("Aplicada", "Pendente"):
            erros.append(f"{rec['id']}: status inválido {rec['status']}")
        if rec["status"] == "Pendente" and not all(rec.get("pendencia", {}).get(k) for k in ("motivo", "decisao", "proximo_passo")):
            erros.append(f"{rec['id']}: pendência sem motivo, decisão ou próximo passo")
        for a in rec.get("arquivos", []):
            if not (RAIZ / a).exists():
                erros.append(f"{rec['id']}: arquivo alterado inexistente {a}")
    return erros


if __name__ == "__main__":
    modelo = carregar()
    problemas = verificar(modelo)
    if problemas:
        print("\n".join(problemas))
        sys.exit(1)
    print(f"OK: {len(modelo['regras'])} RN, {len(modelo['requisitos_funcionais'])} RF, "
          f"{len(modelo['requisitos_nao_funcionais'])} RNF, {len(modelo['casos_de_uso'])} UC, "
          f"{len(modelo['criterios_de_aceitacao'])} CA, {len(modelo['recomendacoes'])} REC consistentes")
