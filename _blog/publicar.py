#!/usr/bin/env python3
"""Gera as páginas do blog a partir dos artigos em _blog/artigos/*.md.

Uso (na pasta do projeto):
    python3 _blog/publicar.py

Não precisa instalar nada: usa só o Python que já vem no computador.
Veja _blog/LEIA-ME.md para escrever e publicar artigos.
"""
import datetime
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

PASTA_BLOG = Path(__file__).resolve().parent
RAIZ = PASTA_BLOG.parent
ARTIGOS = PASTA_BLOG / "artigos"
MODELOS = PASTA_BLOG / "modelos"
SAIDA = RAIZ / "previdenciario" / "blog"
ENDERECO_SITE = "https://eric.adv.br"
ENDERECO_BLOG = ENDERECO_SITE + "/previdenciario/blog/"
MARCA = "<!-- Página gerada por _blog/publicar.py. Não edite aqui: edite o artigo em _blog/artigos/. -->"
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]
CAMPOS_OBRIGATORIOS = ["titulo", "descricao", "data"]


class ErroArtigo(Exception):
    pass


# ---------- Leitura do artigo ----------

def ler_artigo(caminho):
    texto = caminho.read_text(encoding="utf-8").replace("\r\n", "\n")
    if not texto.startswith("---\n"):
        raise ErroArtigo("o arquivo precisa começar com o bloco de informações entre linhas '---'.")
    try:
        cabecalho, corpo = texto[4:].split("\n---\n", 1)
    except ValueError:
        raise ErroArtigo("falta a linha '---' que fecha o bloco de informações.")
    dados = {}
    for numero, linha in enumerate(cabecalho.splitlines(), start=2):
        if not linha.strip() or linha.lstrip().startswith("#"):
            continue
        if ":" not in linha:
            raise ErroArtigo(f"linha {numero}: use o formato 'campo: valor'.")
        chave, valor = linha.split(":", 1)
        dados[normalizar(chave.strip())] = valor.strip()
    for campo in CAMPOS_OBRIGATORIOS:
        if not dados.get(campo):
            raise ErroArtigo(f"falta o campo '{campo}'.")
    dados["data"] = ler_data(dados["data"], "data")
    dados["atualizado"] = ler_data(dados["atualizado"], "atualizado") if dados.get("atualizado") else None
    dados["rascunho"] = normalizar(dados.get("rascunho", "nao")) in ("sim", "s", "true")
    dados["endereco"] = caminho.stem
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", dados["endereco"]):
        raise ErroArtigo("o nome do arquivo deve ter só letras minúsculas sem acento, números e hífens, "
                         "por exemplo: aposentadoria-por-idade.md")
    dados["corpo"] = corpo.strip()
    return dados


def ler_data(valor, campo):
    try:
        return datetime.date.fromisoformat(valor)
    except ValueError:
        raise ErroArtigo(f"o campo '{campo}' deve estar no formato AAAA-MM-DD, por exemplo 2026-09-27.")


def normalizar(texto):
    sem_acento = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return sem_acento.lower()


def data_por_extenso(data):
    return f"{data.day} de {MESES[data.month - 1]} de {data.year}"


# ---------- Markdown simples → HTML ----------

def em_linha(texto):
    """Negrito, itálico e links dentro de um parágrafo."""
    texto = html.escape(texto, quote=False)
    texto = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: link(m.group(1), m.group(2)), texto)
    texto = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", texto)
    texto = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", texto)
    return texto


def link(rotulo, destino):
    destino = html.unescape(destino)
    externo = destino.startswith(("http://", "https://"))
    extra = ' rel="noopener"' if externo else ""
    return f'<a href="{html.escape(destino)}"{extra}>{rotulo}</a>'


def criar_id(texto, usados):
    base = re.sub(r"[^a-z0-9]+", "-", normalizar(re.sub(r"<[^>]+>", "", texto))).strip("-") or "secao"
    candidato, n = base, 2
    while candidato in usados:
        candidato, n = f"{base}-{n}", n + 1
    usados.add(candidato)
    return candidato


def markdown(texto, sumario=None, usados=None):
    usados = set() if usados is None else usados
    linhas = texto.split("\n")
    saida, i = [], 0
    while i < len(linhas):
        linha = linhas[i]
        if not linha.strip():
            i += 1
            continue
        titulo = re.match(r"(#{2,3})\s+(.+?)(?:\s+\{#([a-z0-9-]+)\})?\s*$", linha)
        if titulo:
            nivel = len(titulo.group(1))
            conteudo = em_linha(titulo.group(2))
            ident = titulo.group(3) or criar_id(conteudo, usados)
            usados.add(ident)
            if sumario is not None and nivel == 2:
                sumario.append((ident, conteudo))
            saida.append(f'<h{nivel} id="{ident}">{conteudo}</h{nivel}>')
            i += 1
            continue
        if linha.startswith(">"):
            bloco = []
            while i < len(linhas) and linhas[i].startswith(">"):
                bloco.append(re.sub(r"^> ?", "", linhas[i]))
                i += 1
            interno = markdown("\n".join(bloco), usados=usados)
            saida.append(f'<blockquote class="citacao">\n{interno}\n</blockquote>')
            continue
        if re.match(r"\s*([-*]|\d+\.)\s+", linha):
            ordenada = bool(re.match(r"\s*\d+\.", linha))
            itens = []
            while i < len(linhas) and re.match(r"\s*([-*]|\d+\.)\s+", linhas[i]):
                itens.append(re.sub(r"^\s*([-*]|\d+\.)\s+", "", linhas[i]))
                i += 1
                while i < len(linhas) and linhas[i].startswith("  ") and linhas[i].strip():
                    itens[-1] += " " + linhas[i].strip()
                    i += 1
            marca = "ol" if ordenada else "ul"
            saida.append(f"<{marca}>\n" + "\n".join(f"<li>{em_linha(item)}</li>" for item in itens) + f"\n</{marca}>")
            continue
        if linha.lstrip().startswith("<"):
            bloco = []
            while i < len(linhas) and linhas[i].strip():
                bloco.append(linhas[i])
                i += 1
            saida.append("\n".join(bloco))
            continue
        paragrafo = []
        while i < len(linhas) and linhas[i].strip() and not re.match(r"(#{2,3}\s|>|\s*([-*]|\d+\.)\s)", linhas[i]):
            paragrafo.append(linhas[i].strip())
            i += 1
        texto_paragrafo = " ".join(paragrafo)
        if normalizar(texto_paragrafo).startswith("fonte:"):
            saida.append(f'<p class="fonte">{em_linha(texto_paragrafo)}</p>')
        else:
            saida.append(f"<p>{em_linha(texto_paragrafo)}</p>")
    return "\n".join(saida)


# ---------- Montagem das páginas ----------

def preencher(modelo, valores):
    # Partes comuns (topo e rodapé) ficam em _blog/modelos/partes/
    for parte in (MODELOS / "partes").glob("*.html"):
        valores.setdefault(parte.stem, parte.read_text(encoding="utf-8").strip())
    def trocar(m):
        chave = m.group(1)
        if chave not in valores:
            raise ErroArtigo(f"o modelo usa {{{{{chave}}}}}, que não existe.")
        return valores[chave]
    return re.sub(r"\{\{(\w+)\}\}", trocar, modelo)


def tempo_de_leitura(corpo):
    palavras = len(re.findall(r"\w+", re.sub(r"\(https?://[^)]*\)", "", corpo)))
    minutos = max(1, round(palavras / 180))
    return f"{minutos} minuto{'s' if minutos > 1 else ''} de leitura"


def pagina_artigo(artigo, modelo):
    sumario = []
    conteudo = markdown(artigo["corpo"], sumario)
    bloco_sumario = ""
    if len(sumario) >= 3:
        itens = "\n".join(f'<li><a href="#{ident}">{texto}</a></li>' for ident, texto in sumario)
        bloco_sumario = ('<nav class="sumario" aria-labelledby="sumario-titulo">\n'
                         '<h2 id="sumario-titulo">Neste artigo</h2>\n'
                         f"<ol>\n{itens}\n</ol>\n</nav>")
    atualizado = ""
    if artigo["atualizado"] and artigo["atualizado"] != artigo["data"]:
        atualizado = (f' · Atualizado em <time datetime="{artigo["atualizado"].isoformat()}">'
                      f'{data_por_extenso(artigo["atualizado"])}</time>')
    endereco = f'{ENDERECO_BLOG}{artigo["endereco"]}.html'
    dados_estruturados = json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": artigo["titulo"],
        "description": artigo["descricao"],
        "datePublished": artigo["data"].isoformat(),
        "dateModified": (artigo["atualizado"] or artigo["data"]).isoformat(),
        "author": {"@type": "Person", "name": "Eric Fernandes", "url": ENDERECO_SITE},
        "mainEntityOfPage": endereco,
        "inLanguage": "pt-BR",
    }, ensure_ascii=False)
    return preencher(modelo, {
        "marca": MARCA,
        "titulo": html.escape(artigo["titulo"]),
        "descricao": html.escape(artigo["descricao"]),
        "endereco": endereco,
        "data_iso": artigo["data"].isoformat(),
        "data_extenso": data_por_extenso(artigo["data"]),
        "atualizado": atualizado,
        "leitura": tempo_de_leitura(artigo["corpo"]),
        "sumario": bloco_sumario,
        "conteudo": conteudo,
        "dados_estruturados": dados_estruturados,
    })


def pagina_lista(artigos, modelo):
    if artigos:
        cartoes = "\n".join(
            f'<li class="cartao-artigo">\n'
            f'<h2><a href="{a["endereco"]}.html">{html.escape(a["titulo"])}</a></h2>\n'
            f'<p class="detalhes"><time datetime="{a["data"].isoformat()}">{data_por_extenso(a["data"])}</time>'
            f' · {tempo_de_leitura(a["corpo"])}</p>\n'
            f'<p>{html.escape(a["descricao"])}</p>\n'
            f'<p class="ler"><a href="{a["endereco"]}.html" aria-hidden="true" tabindex="-1">Ler o artigo →</a></p>\n'
            f"</li>"
            for a in artigos)
        lista = f'<ol class="lista-artigos" reversed>\n{cartoes}\n</ol>'
    else:
        lista = "<p>Nenhum artigo publicado ainda.</p>"
    return preencher(modelo, {"marca": MARCA, "endereco": ENDERECO_BLOG, "lista": lista})


def gerar_sitemap(publicados):
    """Mapa do site para os buscadores. Não inclui as versões de teste (93115, 75946, 48652, 59899),
    que têm noindex e não devem aparecer no Google."""
    def entrada(endereco, ultima=None):
        marca = f"    <lastmod>{ultima.isoformat()}</lastmod>\n" if ultima else ""
        return f"  <url>\n    <loc>{endereco}</loc>\n{marca}  </url>"
    itens = [entrada(ENDERECO_SITE + "/"), entrada(ENDERECO_SITE + "/privacidade/")]
    if publicados:
        itens.append(entrada(ENDERECO_BLOG, max(a["atualizado"] or a["data"] for a in publicados)))
    for artigo in publicados:
        itens.append(entrada(f'{ENDERECO_BLOG}{artigo["endereco"]}.html', artigo["atualizado"] or artigo["data"]))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(itens) + "\n</urlset>\n")


def atualizar_inicio(publicados):
    """Põe os artigos mais recentes na página inicial, entre as marcas <!-- artigos:inicio --> e
    <!-- artigos:fim --> do index.html. Sem essas marcas, a página inicial não é alterada."""
    caminho = RAIZ / "index.html"
    texto = caminho.read_text(encoding="utf-8")
    ini, fim = "<!-- artigos:inicio -->", "<!-- artigos:fim -->"
    if ini not in texto:
        return False
    if fim not in texto:
        raise SystemExit("index.html tem a marca de início dos artigos, mas falta a marca <!-- artigos:fim -->.")
    cartoes = "\n".join(
        f'                <li class="artigo_cartao"><a href="previdenciario/blog/{a["endereco"]}.html">'
        f'{html.escape(a["titulo"])}</a><p>{html.escape(a["descricao"])}</p></li>'
        for a in publicados[:3])
    bloco = f'\n            <ul class="artigos_lista">\n{cartoes}\n            </ul>\n            '
    antes, resto = texto.split(ini, 1)
    _, depois = resto.split(fim, 1)
    caminho.write_text(antes + ini + bloco + fim + depois, encoding="utf-8")
    return True


def main():
    modelo_artigo = (MODELOS / "artigo.html").read_text(encoding="utf-8")
    modelo_lista = (MODELOS / "lista.html").read_text(encoding="utf-8")
    publicados, rascunhos, erros = [], [], []
    for caminho in sorted(ARTIGOS.glob("*.md")):
        try:
            artigo = ler_artigo(caminho)
        except ErroArtigo as erro:
            erros.append(f"  ✗ {caminho.name}: {erro}")
            continue
        (rascunhos if artigo["rascunho"] else publicados).append(artigo)
    if erros:
        print("Nada foi publicado. Corrija estes artigos:\n" + "\n".join(erros))
        sys.exit(1)

    publicados.sort(key=lambda a: a["data"], reverse=True)
    SAIDA.mkdir(parents=True, exist_ok=True)
    gerados = {"index.html"}
    for artigo in publicados:
        nome = f'{artigo["endereco"]}.html'
        (SAIDA / nome).write_text(pagina_artigo(artigo, modelo_artigo), encoding="utf-8")
        gerados.add(nome)
    (SAIDA / "index.html").write_text(pagina_lista(publicados, modelo_lista), encoding="utf-8")
    (RAIZ / "sitemap.xml").write_text(gerar_sitemap(publicados), encoding="utf-8")
    if atualizar_inicio(publicados):
        print("Página inicial atualizada com os artigos mais recentes")

    # Remove páginas de artigos que viraram rascunho ou foram apagados
    removidos = []
    for pagina in SAIDA.glob("*.html"):
        if pagina.name not in gerados and MARCA in pagina.read_text(encoding="utf-8"):
            pagina.unlink()
            removidos.append(pagina.name)

    print("Mapa do site atualizado em sitemap.xml")
    print(f"Blog atualizado em {SAIDA.relative_to(RAIZ)}/")
    for artigo in publicados:
        print(f'  ✓ {artigo["endereco"]}.html  ({artigo["titulo"]})')
    for artigo in rascunhos:
        print(f'  – {artigo["endereco"]}.md é rascunho: não foi publicado')
    for nome in removidos:
        print(f"  – {nome} foi retirado do blog")


if __name__ == "__main__":
    main()
