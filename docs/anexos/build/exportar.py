"""Exporta os Markdown da documentação para PDF com a identidade visual HIVEPlace.

Uso: python docs/anexos/build/exportar.py [arquivo.md ...]
Requisitos: Google Chrome, bibliotecas Python markdown e pyyaml, fonte Manrope instalada.
Os ativos visuais vêm de docs/anexos/identidade/ (arquivos oficiais, sem alteração).
"""
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata

import markdown
import yaml

AQUI = pathlib.Path(__file__).resolve().parent
DOCS = AQUI.parents[1]
IDENT = DOCS / "anexos" / "identidade"
CHROME = shutil.which("google-chrome") or shutil.which("chromium")
ALVOS = sorted(DOCS.glob("0[0-8]-*.md")) + [IDENT / "README.md", DOCS / "anexos" / "swagger" / "README.md"]
FRASE = "Transformando conexões invisíveis em inteligência coletiva"
# Documentos com tabelas largas usam página paisagem; a capa continua em retrato (página nomeada).
PAISAGEM = {"04-requisitos-nao-funcionais", "05-regras-de-negocio", "07-matriz-rastreabilidade"}


def uri(p):
    return pathlib.Path(p).resolve().as_uri()


def slug(valor, _sep):
    """Mesma regra usada pelo GitHub: minúsculas, sem pontuação, acentos preservados, espaço vira hífen."""
    v = unicodedata.normalize("NFC", valor.strip().lower())
    v = re.sub(r"[^\w\- ]", "", v)
    return re.sub(r" ", "-", v)


def separar(texto):
    m = re.match(r"---\n(.*?)\n---\n", texto, re.S)
    return (yaml.safe_load(m.group(1)), texto[m.end():]) if m else ({}, texto)


def reescrever(html, arquivo):
    base = arquivo.parent

    def href(m):
        alvo, _, ancora = m.group(1).partition("#")
        if re.match(r"^(https?:|mailto:)", alvo):
            return m.group(0)
        if alvo.endswith(".md"):
            destino = (base / alvo).resolve()
            if destino == arquivo.resolve():
                return f'href="#{ancora}"' if ancora else 'href="#"'
            return f'href="{pathlib.Path(alvo).with_suffix(".pdf").as_posix()}"'
        return m.group(0)

    html = re.sub(r'href="([^"]*)"', href, html)
    html = re.sub(r'src="([^"]+)"', lambda m: f'src="{uri(base / m.group(1))}"' if not m.group(1).startswith(("http", "file:")) else m.group(0), html)
    for classe, emoji in (("atencao", "⚠️"), ("confirmado", "✅"), ("alterado", "🔄")):
        html = re.sub(rf"<(li|p)>({re.escape(emoji)})", rf'<\1 class="{classe}">\2', html)
    return html


def pagina(meta, corpo, arquivo, css):
    titulo = meta.get("titulo", arquivo.stem)
    versao, data = meta.get("versao", "-"), meta.get("data", "-")
    titulo_capa = titulo.replace("ai-engineering-team", '<span class="nb">ai-engineering-team</span>')
    rodape_dir = f"{meta.get('projeto', 'ai-engineering-team')} · v{versao} · {data}"
    classe = "paisagem" if arquivo.stem in PAISAGEM else "retrato"
    larg, tam, mar = (261, "A4 landscape", "26mm 18mm 22mm 18mm") if arquivo.stem in PAISAGEM else (174, "A4", "30mm 18mm 24mm 18mm")
    paginas = f"""
@page {{ size: {tam}; margin: {mar};
  background: url("{uri(IDENT / 'padrao-hexagonos-claro.png')}") no-repeat right bottom / 105mm auto;
  @top-left {{ width: {larg}mm; content: "{titulo} · v{versao}"; text-align: right; font: 8pt Manrope; color: #404146;
    background: url("{uri(IDENT / 'hiveplace-logotipo-horizontal-fundo-claro.png')}") no-repeat left center / 36mm auto;
    border-bottom: .6pt solid #EFB41B; }}
  @bottom-left {{ width: {larg - 78}mm; content: "{FRASE}"; font: 7.5pt Manrope; color: #404146; padding-left: 8mm;
    background: url("{uri(IDENT / 'hiveplace-simbolo.png')}") no-repeat left center / auto 5mm; }}
  @bottom-right {{ width: 78mm; content: "{rodape_dir} · Página " counter(page) " de " counter(pages); font: 7pt Manrope; color: #404146; text-align: right; }} }}
"""
    capa = f"""
<section class="capa">
  <div class="padrao"></div>
  <img class="logo" src="{uri(IDENT / 'hiveplace-logotipo-horizontal.png')}" alt="HIVEPlace">
  <div class="bloco"><div class="rotulo">Documentação técnica</div><h1>{titulo_capa}</h1>
    <div class="sub">{meta.get('projeto', '')}</div><div class="filete"></div></div>
  <table class="meta">
    <tr><td>Projeto</td><td>{meta.get('projeto', '-')}</td></tr><tr><td>Versão</td><td>{versao}</td></tr>
    <tr><td>Data</td><td>{data}</td></tr><tr><td>Autor</td><td>{meta.get('autor', 'Não informado')}</td></tr>
    <tr><td>Classificação</td><td>{meta.get('classificacao', 'Não informada')}</td></tr>
    <tr><td>Status</td><td>{meta.get('status', '-')}</td></tr></table>
</section>"""
    css = css.replace("{{PADRAO_ESCURO}}", uri(IDENT / "padrao-hexagonos-a.png")).replace("{{PADRAO_CLARO}}", uri(IDENT / "padrao-hexagonos-claro.png"))
    return (f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{titulo}</title>'
            f"<style>{css}{paginas}</style></head><body class='{classe}'>{capa}<main>{corpo}</main></body></html>")


def exportar(arquivo, css, tmp):
    meta, texto = separar(arquivo.read_text(encoding="utf-8"))
    corpo = markdown.markdown(texto, extensions=["tables", "fenced_code", "attr_list", "sane_lists", "toc"],
                              extension_configs={"toc": {"slugify": slug}})
    corpo = reescrever(corpo, arquivo)
    html = tmp / (arquivo.stem + ".html")
    html.write_text(pagina(meta, corpo, arquivo, css), encoding="utf-8")
    pdf = arquivo.with_suffix(".pdf")
    r = subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                        "--allow-file-access-from-files", f"--print-to-pdf={pdf}", html.as_uri()],
                       capture_output=True, text=True, timeout=180)
    if not pdf.exists():
        print(f"FALHA ao gerar {pdf}: {r.stderr[-300:]}")
        return False
    print(f"OK {pdf.relative_to(DOCS.parent)}")
    return True


def main():
    if not CHROME:
        print("Google Chrome não encontrado; exportação pendente.")
        return 1
    css = (AQUI / "estilo.css").read_text(encoding="utf-8")
    alvos = [pathlib.Path(a).resolve() for a in sys.argv[1:]] or ALVOS
    with tempfile.TemporaryDirectory() as t:
        ok = [exportar(a, css, pathlib.Path(t)) for a in alvos]
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
