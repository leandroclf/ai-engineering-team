"""Preenche os blocos '<!-- BEGIN:gerado:nome -->' dos Markdown de docs/ a partir do modelo de rastreabilidade.

Uso: python docs/anexos/build/gerar.py
O texto fora dos blocos é escrito à mão e nunca é alterado. Falha se o modelo estiver inconsistente.
"""
import collections
import pathlib
import re
import sys

import modelo

DOCS = modelo.RAIZ / "docs"
ARQ = {"RN": "05-regras-de-negocio.md", "RF": "03-requisitos-funcionais.md", "RNF": "04-requisitos-nao-funcionais.md",
       "UC": "06-casos-de-uso.md", "CA": "06-casos-de-uso.md", "REC": "08-observacoes-analises.md"}
AQUI = pathlib.Path(__file__).resolve().parent


def lk(i):
    return f"[{i}]({ARQ[i.split('-')[0]]}#{i.lower()})"


def lks(ids):
    return ", ".join(lk(i) for i in ids) if ids else "-"


def cel(t):
    return str(t).replace("|", "\\|").replace("\n", " ")


def tabela(cab, linhas):
    out = ["| " + " | ".join(cab) + " |", "| " + " | ".join("---" for _ in cab) + " |"]
    out += ["| " + " | ".join(cel(c) for c in l) + " |" for l in linhas]
    return "\n".join(out)


def situacao(verificacao):
    for prefixo, rotulo in (("Validado", "Validado"), ("Parcial", "Parcial"), ("Não validado", "Não validado"),
                            ("Não aplicável", "Não aplicável"), ("Estrutura", "Somente estrutura")):
        if verificacao.startswith(prefixo):
            return rotulo
    return "Indefinido"


def fontes(lista):
    return "<br>".join(f"`{f}`" for f in lista)


def blocos(m):
    rf, uc, ca, rn = m["_rf"], m["_uc"], m["_ca"], m["_rn"]
    recs = m["recomendacoes"]
    aplicadas = [r for r in recs if r["status"] == "Aplicada"]
    pendentes = [r for r in recs if r["status"] == "Pendente"]
    b = {}

    cont = collections.Counter(situacao(r["verificacao"]) for r in m["requisitos_funcionais"])
    b["resumo-numeros"] = "### Números da análise\n\n" + tabela(
        ["Elemento", "Quantidade"],
        [["Regras de negócio (RN)", len(m["regras"])], ["Requisitos funcionais (RF)", len(m["requisitos_funcionais"])],
         ["Requisitos não funcionais (RNF)", len(m["requisitos_nao_funcionais"])], ["Casos de uso (UC)", len(m["casos_de_uso"])],
         ["Critérios de aceitação (CA)", len(m["criterios_de_aceitacao"])],
         ["Recomendações aplicadas", len(aplicadas)], ["Recomendações pendentes", len(pendentes)],
         ["RF validados por execução", cont["Validado"]], ["RF parcialmente validados", cont["Parcial"]],
         ["RF não validados ou apenas estruturais", cont["Não validado"] + cont["Somente estrutura"] + cont["Não aplicável"]]])

    b["rf-resumo"] = "## Situação de verificação\n\n" + tabela(
        ["ID", "Requisito", "Situação"], [[lk(r["id"]), r["nome"], situacao(r["verificacao"])] for r in m["requisitos_funcionais"]]
    ) + "\n\n" + ", ".join(f"{k}: {v}" for k, v in sorted(cont.items())) + "."

    partes = []
    for r in m["requisitos_funcionais"]:
        partes.append(f'### <a id="{r["id"].lower()}"></a>{r["id"]} — {r["nome"]}\n\n'
                      f'- **Descrição:** {r["descricao"]}\n- **Origem:** ' + "; ".join(f"`{o}`" for o in r["origem"]) +
                      f'\n- **Regras de negócio:** {lks(r["rn"])}\n- **Verificação:** {r["verificacao"]}')
    b["rf-detalhe"] = "\n\n".join(partes)

    trace = (modelo.RAIZ / "openspec/changes/validate-agentic-framework/traceability.md").read_text(encoding="utf-8")
    com_cenario = set(re.findall(r"^\| ([A-Z]+-\d{3}) ", trace, re.M))
    b["mapa-specs"] = tabela(["ID original", "Destino nesta documentação", "Cenário no traceability.md da fonte"],
                             [[i, lks(d), "Sim" if i in com_cenario else "Não"] for i, d in m["mapeamento_specs"].items()])

    b["rnf-tabela"] = tabela(
        ["ID", "Categoria", "Requisito", "Status", "Meta, valor observado ou lacuna", "Origem"],
        [[r["id"], r["categoria"], f'**{r["nome"]}.** {r["descricao"]}', r["status"], r["meta"],
          "<br>".join(f"`{o}`" for o in r["origem"])] for r in m["requisitos_nao_funcionais"]])

    por_tipo = collections.defaultdict(list)
    por_area = collections.defaultdict(list)
    for r in m["regras"]:
        por_tipo[r["tipo"]].append(r["id"])
        por_area[r["area"]].append(r["id"])
    b["rn-por-tipo"] = ("## Distribuição\n\n" + tabela(["Tipo", "Qtd", "Regras"], [[t, len(v), lks(v)] for t, v in sorted(por_tipo.items())])
                        + "\n\n" + tabela(["Área", "Qtd", "Regras"], [[t, len(v), lks(v)] for t, v in sorted(por_area.items())]))
    b["rn-resumo"] = tabela(["ID", "Regra", "Tipo", "Área", "Etapa", "Impacto", "Fonte"],
                            [[lk(r["id"]), r["nome"], r["tipo"], r["area"], r["etapa"], r["impacto"], fontes(r["fonte"])] for r in m["regras"]])
    partes = []
    for r in m["regras"]:
        marca = "🔄 Alterado após validação" if r["id"] in ("RN-005", "RN-018") else "✅ Confirmado"
        partes.append(f'### <a id="{r["id"].lower()}"></a>{r["id"]} — {r["nome"]}\n\n'
                      f'- **Descrição:** {r["descricao"]}\n- **Situação:** {marca}\n'
                      f'- **Tipo:** {r["tipo"]} · **Área:** {r["area"]} · **Etapa:** {r["etapa"]} · **Impacto:** {r["impacto"]}\n'
                      f'- **Fonte:** ' + "; ".join(f"`{f}`" for f in r["fonte"]) +
                      f'\n- **Requisitos:** {lks(r["rf"])}\n- **Casos de uso:** {lks(r["uc"])}\n- **Critérios:** {lks(r["ca"])}')
    b["rn-lista"] = "\n\n".join(partes)

    cont_uc = collections.Counter(situacao(u["verificacao"]) for u in m["casos_de_uso"])
    b["uc-resumo"] = "## Visão geral\n\n" + tabela(
        ["ID", "Caso de uso", "Cenário de validação", "Situação"],
        [[lk(u["id"]), u["nome"], u["cenario"], situacao(u["verificacao"])] for u in m["casos_de_uso"]]
    ) + "\n\n" + ", ".join(f"{k}: {v}" for k, v in sorted(cont_uc.items())) + "."
    partes = []
    for u in m["casos_de_uso"]:
        passos = "\n".join(f"  {n}. {p}" for n, p in enumerate(u["fluxo"], 1))
        exc = "\n".join(f"  - {e}" for e in u["excecoes"])
        cas = [c["id"] for c in m["criterios_de_aceitacao"] if c["uc"] == u["id"]]
        partes.append(f'### <a id="{u["id"].lower()}"></a>{u["id"]} — {u["nome"]}\n\n- **Ator:** {u["ator"]}\n'
                      f'- **Pré-condição:** {u["pre"]}\n- **Fluxo principal:**\n{passos}\n'
                      f'- **Exceções e alternativas:**\n{exc}\n- **Pós-condição:** {u["pos"]}\n'
                      f'- **Regras de negócio:** {lks(u["rn"])}\n- **Requisitos funcionais:** {lks(u["rf"])}\n'
                      f'- **Critérios de aceitação:** {lks(cas)}\n- **Cenário de validação:** {u["cenario"]}\n'
                      f'- **Verificação:** {u["verificacao"]}')
    b["uc-detalhe"] = "\n\n".join(partes)

    partes = []
    for u in m["casos_de_uso"]:
        itens = []
        for c in [c for c in m["criterios_de_aceitacao"] if c["uc"] == u["id"]]:
            corpo = "\n".join("  " + l for l in c["gherkin"].strip().splitlines())
            itens.append(f'<a id="{c["id"].lower()}"></a>\n**{c["id"]} — {c["titulo"]}.** Regras: {lks(c["rn"])}\n\n'
                         f'```gherkin\n# language: pt\nCenário: {c["titulo"]}\n{corpo}\n```')
        partes.append(f"### Critérios de {u['id']} — {u['nome']}\n\n" + "\n\n".join(itens))
    b["ca-gherkin"] = "\n\n".join(partes)

    n = len(m["regras"])
    b["cobertura"] = "## Cobertura e consistência\n\n" + tabela(
        ["Verificação", "Resultado"],
        [["Regras com ao menos um requisito, caso de uso, critério e fonte", f"{n} de {n}"],
         ["Requisitos funcionais com ao menos uma regra", f"{len(m['requisitos_funcionais'])} de {len(m['requisitos_funcionais'])}"],
         ["Casos de uso com ao menos uma regra e um critério", f"{len(m['casos_de_uso'])} de {len(m['casos_de_uso'])}"],
         ["Critérios com ao menos uma regra e um caso de uso", f"{len(m['criterios_de_aceitacao'])} de {len(m['criterios_de_aceitacao'])}"],
         ["Fontes citadas que existem no repositório", "todas (verificado por `modelo.py`)"],
         ["Identificadores originais do OpenSpec mapeados", f"{len(m['mapeamento_specs'])} de {len(m['mapeamento_specs'])}"]]
    ) + "\n\n**Cobertura de validação por execução:** a rastreabilidade documental está completa, mas a evidência de execução não. " \
        "Casos de uso com evidência de execução: " + lks([u["id"] for u in m["casos_de_uso"] if situacao(u["verificacao"]) == "Validado"]) + \
        ". Parciais: " + lks([u["id"] for u in m["casos_de_uso"] if situacao(u["verificacao"]) == "Parcial"]) + \
        ". Sem evidência de execução: " + lks([u["id"] for u in m["casos_de_uso"] if situacao(u["verificacao"]) in ("Não validado", "Somente estrutura", "Não aplicável")]) + "."
    b["matriz"] = tabela(["Regra de negócio", "Requisitos", "Casos de uso", "Critérios de aceitação", "Fonte"],
                         [[f'{lk(r["id"])} {r["nome"]}', lks(r["rf"]), lks(r["uc"]), lks(r["ca"]), fontes(r["fonte"])] for r in m["regras"]])
    b["matriz-rf"] = tabela(["Requisito", "Regras", "Casos de uso (via regras)"],
                            [[f'{lk(r["id"])} {r["nome"]}', lks(r["rn"]),
                              lks(sorted({u["id"] for u in uc.values() if r["id"] in u["rf"]}))] for r in m["requisitos_funcionais"]])
    b["matriz-uc"] = tabela(["Caso de uso", "Regras", "Requisitos", "Critérios"],
                            [[f'{lk(u["id"])} {u["nome"]}', lks(u["rn"]), lks(u["rf"]),
                              lks([c["id"] for c in m["criterios_de_aceitacao"] if c["uc"] == u["id"]])] for u in m["casos_de_uso"]])

    partes = []
    for r in recs:
        marca = "🔄 **Alterado**" if r["status"] == "Aplicada" else "⚠️ **Atenção (pendente)**"
        arq = "; ".join(f"`{a}`" for a in r["arquivos"]) if r["arquivos"] else "nenhum"
        txt = (f'### <a id="{r["id"].lower()}"></a>{r["id"]} — {r["titulo"]}\n\n- {marca}\n- **Problema:** {r["problema"]}\n'
               f'- **Justificativa:** {r["justificativa"]}\n- **Ação:** {r["acao"]}\n- **Arquivos alterados:** {arq}\n'
               f'- **Seção:** {r["secao"]}')
        if r["status"] == "Pendente":
            p = r["pendencia"]
            txt += f'\n- **Motivo da pendência:** {p["motivo"]}\n- **Decisão ou informação necessária:** {p["decisao"]}\n- **Próximo passo:** {p["proximo_passo"]}'
        partes.append(txt)
    b["rec-detalhe"] = "\n\n".join(partes)
    b["rec-registro"] = tabela(
        ["Recomendação", "Arquivo(s) Alterado(s)", "Seção", "Status"],
        [[f'{lk(r["id"])} {r["titulo"]}', "<br>".join(f"`{a}`" for a in r["arquivos"]) or "Nenhum", r["secao"], r["status"]] for r in recs])

    ver = AQUI / "verificacoes.md"
    b["verificacoes"] = ver.read_text(encoding="utf-8").strip() if ver.exists() else "⚠️ **Atenção:** verificações ainda não registradas."
    dif = AQUI / "alteracoes.diff"
    b["diffs"] = "```diff\n" + dif.read_text(encoding="utf-8").strip() + "\n```" if dif.exists() else "Sem diff registrado."

    frase = ("Todas as recomendações foram aplicadas e registradas." if not pendentes else
             "Todas as recomendações aplicáveis foram implementadas e registradas. As pendências estão documentadas com seus motivos e próximos passos.")
    b["conclusao"] = (
        f"A análise produziu {len(m['regras'])} regras de negócio, {len(m['requisitos_funcionais'])} requisitos funcionais, "
        f"{len(m['requisitos_nao_funcionais'])} requisitos não funcionais, {len(m['casos_de_uso'])} casos de uso e "
        f"{len(m['criterios_de_aceitacao'])} critérios de aceitação em Gherkin, todos rastreáveis entre si e a fontes verificáveis, "
        f"além de sete diagramas, o contrato do GitHub consumido pelo transporte e a identidade visual aplicada aos PDFs.\n\n"
        f"**Implementado ({len(aplicadas)}):** " + "; ".join(f"{r['id']} ({r['titulo'][0].lower() + r['titulo'][1:]})" for r in aplicadas) + ".\n\n"
        f"**Pendente ({len(pendentes)}), com motivo, decisão e próximo passo em cada item:** " + ", ".join(r["id"] for r in pendentes) +
        ". Nenhuma pendência é apresentada como concluída. As mais relevantes para a confiança no sistema são a independência real entre as contas "
        "do Atlas e do Sentinel (REC-015), a validação ao vivo dos Dots (REC-017) e a exigência dos statuses de revisão por proteção de branch (REC-016).\n\n"
        f"**{frase}**")
    return b


ARQUIVOS = {
    "01-contexto.md": ["resumo-numeros"],
    "03-requisitos-funcionais.md": ["rf-resumo", "rf-detalhe", "mapa-specs"],
    "04-requisitos-nao-funcionais.md": ["rnf-tabela"],
    "05-regras-de-negocio.md": ["rn-por-tipo", "rn-resumo", "rn-lista"],
    "06-casos-de-uso.md": ["uc-resumo", "uc-detalhe", "ca-gherkin"],
    "07-matriz-rastreabilidade.md": ["cobertura", "matriz", "matriz-rf", "matriz-uc"],
    "08-observacoes-analises.md": ["rec-detalhe", "verificacoes", "conclusao", "rec-registro", "diffs"],
}


def main():
    m = modelo.carregar()
    erros = modelo.verificar(m)
    if erros:
        print("Modelo inconsistente; nada foi gerado:\n" + "\n".join(erros))
        return 1
    b = blocos(m)
    for nome, lista in ARQUIVOS.items():
        p = DOCS / nome
        txt = p.read_text(encoding="utf-8")
        for bloco in lista:
            padrao = re.compile(rf"(<!-- BEGIN:gerado:{bloco} -->\n).*?(<!-- END:gerado:{bloco} -->)", re.S)
            if not padrao.search(txt):
                print(f"{nome}: marcador ausente: {bloco}")
                return 1
            txt = padrao.sub(lambda mo: mo.group(1) + "\n" + b[bloco] + "\n\n" + mo.group(2), txt)
        p.write_text(txt, encoding="utf-8")
    print("OK: blocos gerados em", len(ARQUIVOS), "arquivos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
