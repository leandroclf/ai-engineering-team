"""Verifica a documentação produzida: front matter YAML, links relativos e âncoras, imagens e identificadores.

Uso: python docs/anexos/build/verificar_docs.py   (sai com 1 se houver erro)
"""
import pathlib
import re
import sys
import unicodedata

import yaml

import modelo

DOCS = modelo.RAIZ / "docs"
MD = sorted(DOCS.glob("0[0-8]-*.md")) + [DOCS / "anexos/identidade/README.md", DOCS / "anexos/swagger/README.md"]
OBRIGATORIOS = ("titulo", "autor", "data", "versao")


def ancoras(texto):
    """Âncoras que o GitHub geraria para os títulos, mais os <a id> explícitos."""
    out = set(re.findall(r'<a id="([^"]+)"', texto))
    for h in re.findall(r"^#{1,6} (.+)$", texto, re.M):
        v = unicodedata.normalize("NFC", h.strip().lower())
        out.add(re.sub(r" ", "-", re.sub(r"[^\w\- ]", "", v)))
    return out


def main():
    erros, n_links, n_ids, n_pdf = [], 0, 0, 0
    m = modelo.carregar()
    ids = {i for chave in ("_rn", "_rf", "_uc", "_ca") for i in m[chave]}
    ids |= {r["id"] for r in m["requisitos_nao_funcionais"]} | {r["id"] for r in m["recomendacoes"]}
    textos = {p: p.read_text(encoding="utf-8") for p in MD}
    for p, t in textos.items():
        rel = p.relative_to(DOCS.parent)
        fm = re.match(r"---\n(.*?)\n---\n", t, re.S)
        if not fm:
            erros.append(f"{rel}: sem front matter")
            continue
        try:
            meta = yaml.safe_load(fm.group(1))
        except yaml.YAMLError as e:
            erros.append(f"{rel}: front matter inválido: {e}")
            continue
        for c in OBRIGATORIOS:
            if not meta.get(c):
                erros.append(f"{rel}: front matter sem {c}")
        corpo = t[fm.end():]
        sem_codigo = re.sub(r"```.*?```", "", corpo, flags=re.S)
        for alvo in re.findall(r"(?<!\!)\[[^\]]*\]\(([^)]+)\)", sem_codigo):
            if re.match(r"^(https?:|mailto:)", alvo):
                continue
            n_links += 1
            caminho, _, anc = alvo.partition("#")
            destino = (p.parent / caminho).resolve() if caminho else p
            if not destino.exists():
                erros.append(f"{rel}: link quebrado {alvo}")
            elif anc and destino.suffix == ".md" and anc not in ancoras(destino.read_text(encoding="utf-8")):
                erros.append(f"{rel}: âncora inexistente {alvo}")
        for img in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", corpo):
            if not (p.parent / img).exists():
                erros.append(f"{rel}: imagem inexistente {img}")
        for ident in set(re.findall(r"\b(RN|RF|RNF|UC|CA|REC)-(\d{3})\b", sem_codigo)):
            n_ids += 1
            if f"{ident[0]}-{ident[1]}" not in ids:
                erros.append(f"{rel}: identificador inexistente {ident[0]}-{ident[1]}")
        if "<!-- BEGIN:gerado" in corpo and re.search(r"BEGIN:gerado:(\S+) -->\n\s*<!-- END", corpo):
            erros.append(f"{rel}: bloco gerado vazio")
        # Os PDFs não são versionados (embutem material de marca); só se confere se foram gerados localmente.
        n_pdf += p.with_suffix(".pdf").exists()
    for mmd in sorted((DOCS / "anexos/diagramas").glob("*.mmd")):
        if not mmd.with_suffix(".png").exists():
            erros.append(f"{mmd.name}: PNG ausente")
    # Diagramas referenciados nos documentos devem existir como fonte e imagem.
    for p, t in textos.items():
        for mm in re.findall(r"\]\((anexos/diagramas/[^)]+\.mmd)\)", t):
            if not (p.parent / mm).exists():
                erros.append(f"{p.name}: fonte de diagrama ausente {mm}")
    if erros:
        print("\n".join(erros))
        return 1
    print(f"OK: {len(MD)} documentos, {n_links} links relativos, {n_ids} referências de identificador, front matter, imagens verificados; PDFs locais presentes: {n_pdf} de {len(MD)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
