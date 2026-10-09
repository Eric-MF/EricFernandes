"""Gera as três versões (Clássica, Moderna, Acolhedora) a partir do conteúdo real do index.html."""
import re, pathlib

raiz = pathlib.Path(__file__).resolve().parents[2]
S = (raiz / "index.html").read_text(encoding="utf-8")
ANTIGA = (raiz / "93115" / "index.html").read_text(encoding="utf-8")

def achar(padrao, texto=S, grupo=0):
    m = re.search(padrao, texto, re.S)
    if not m:
        raise SystemExit("não encontrado: " + padrao[:60])
    return m.group(grupo)

def svg_limpo(svg):
    svg = re.sub(r'\s(alt|width|height)="[^"]*"', "", svg, count=0)
    svg = re.sub(r'\sid="[^"]*"', "", svg)
    svg = svg.replace('fill="#25D366"', "").replace('fill="none"', "")
    return svg.replace("<svg", '<svg aria-hidden="true" focusable="false"', 1)

LOGO = svg_limpo(achar(r'<a href="\./" aria-label="Início">\s*(<svg.*?</svg>)', grupo=1))
WPP = svg_limpo(achar(r'<a id="whatsapp-contato"[^>]*>\s*(<svg.*?</svg>)', grupo=1))
EMAIL = svg_limpo(achar(r'<a href="mailto:[^"]*"[^>]*>\s*(<svg.*?</svg>)', grupo=1))
TEL = svg_limpo(achar(r'<a href="tel:[^"]*"[^>]*>\s*(<svg.*?</svg>)', grupo=1))
REDES = achar(r'<div class="redes">(.*?)</div>', ANTIGA, 1).strip()
MAPA = achar(r'data-src="(https://www\.google\.com/maps/embed[^"]*)"', grupo=1)
FAVICON = achar(r'<!-- favicon -->.*?webmanifest" />').replace('href="img/', 'href="../img/')
FONTE_INSS = "https://www.gov.br/inss/pt-br/assuntos/noticias/aposentadoria-por-idade-tudo-o-que-voce-precisa-saber-sobre-um-dos-beneficios-mais-populares"
FONTE_EC103 = "https://www.planalto.gov.br/ccivil_03/constituicao/emendas/emc/emc103.htm"
FONTE_SERVICO = achar(r'Fonte: <a href="(https://www\.gov\.br/pt-br/servicos/[^"]+)"', grupo=1)

def url(texto):
    return achar(r'<a (?:class="[^"]*" )?href="([^"]+)">' + re.escape(texto) + "</a>", grupo=1)

WA = "https://api.whatsapp.com/send?phone=5522998815479&amp;text=Ol%C3%A1,%20Eric!%20Saberia%20me%20esclarecer%20uma%20quest%C3%A3o?"
COMO_CHEGAR = "https://www.google.com/maps/dir/?api=1&amp;destination=R.+Prof.+Carlos+Goes,+71+-+Centro,+Campos+dos+Goytacazes+-+RJ,+28035-155"
FOTO_ALT = achar(r'<img class="banner_img"[^>]*\salt="([^"]*)"', grupo=1)
FOTO = f'<img src="../img/Eric.webp" alt="{FOTO_ALT}" width="1906" height="2771">'

def imagem(codigo, nome):
    """Caminho da imagem gerada, se ela já foi adicionada em <codigo>/img/."""
    return f"img/{nome}.webp" if (raiz / codigo / "img" / f"{nome}.webp").exists() else None

ICONES = {
    "idade": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
    "como": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
    "tipos": '<path d="M12 3v18M7 21h10M5 7h14M5 7l-3 7a3 3 0 0 0 6 0zM19 7l-3 7a3 3 0 0 0 6 0z"/>',
    "porque": '<circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6V14M12 17.5v.01"/>',
}

def cabeca(folhas_fontes, descricao, extra="", codigo=""):
    fontes_html = "\n    ".join(f'<link rel="stylesheet" href="../styles/{folha}">' for folha in folhas_fontes)
    return f'''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="robots" content="noindex">
    <meta name="description" content="{descricao}">
    <title>Eric | Advogado Previdenciarista</title>
    {FAVICON}
    <!-- fontes -->
    {fontes_html}
    <link rel="stylesheet" href="estilo.css">{extra}
    <link rel="stylesheet" href="../privacidade/consentimento.css">
    <script src="../privacidade/consentimento.js" defer></script>
    <script>document.documentElement.classList.add("js");
        // O blog usa a aparência da última versão do site visitada
        try {{ localStorage.setItem("versao-site", "{codigo}"); }} catch (erro) {{}}</script>
</head>
<body>
    <a class="pular" href="#conteudo">Pular para o conteúdo</a>
    <header class="topo" id="inicio">
        <p class="topo-telefone">
            <a href="tel:+5522998815479">{TEL}<span>Ligue: (22) 99881-5479</span></a>
        </p>
        <div class="topo-barra container">
            <a class="marca" href="#inicio">
                {LOGO}
                <span class="marca-texto">
                    <span class="marca-nome">Eric Fernandes</span>
                    <span class="marca-oab">Advogado · OAB/RJ 256 078</span>
                </span>
            </a>
            <a class="topo-fone" href="tel:+5522998815479">{TEL}<span><span class="topo-fone-oab">OAB/RJ 256 078</span>(22) 99881-5479</span></a>
            <button type="button" class="botao-menu" aria-expanded="false" aria-controls="menu">
                <span class="botao-menu-icone" aria-hidden="true"></span>Menu
            </button>
        </div>
        <nav id="menu" class="menu" aria-label="Menu principal">
            <ul class="container">
                <li><a href="#inicio">Início</a></li>
                <li><a href="#sobre">Sobre</a></li>
                <li><a href="#duvidas">Dúvidas</a></li>
                <li><a href="#contato">Contato</a></li>
                <li><a href="#endereco">Endereço</a></li>
                <li><a href="../previdenciario/blog/">Artigos</a></li>
            </ul>
        </nav>
    </header>
'''

def pergunta(chave, titulo, resposta, com_icone, aberta=False, avatar=None):
    icone = ""
    if avatar:
        icone = f'<span class="pergunta-avatar" aria-hidden="true"><img src="{avatar}" alt="" width="160" height="160"></span>'
    elif com_icone:
        icone = (f'<span class="pergunta-icone" aria-hidden="true"><svg viewBox="0 0 24 24" stroke="currentColor" '
                 f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{ICONES[chave]}</svg></span>')
    return f'''                <details class="pergunta" id="pergunta-{chave}"{" open" if aberta else ""}>
                    <summary>{icone}<h3>{titulo}</h3></summary>
                    <div class="resposta">
{resposta}
                    </div>
                </details>
'''

def duvidas(titulo, com_icone=False, avatares=None, ilustracao=None):
    avatares = avatares or {}
    r1 = f'''                        <p>Atualmente, no Regime Geral, as <strong>mulheres</strong> podem se aposentar com no mínimo <strong>62 anos de idade e 15 anos de contribuição</strong>.</p>
                        <p>Para os <strong>homens</strong>, a idade mínima é <strong>65 anos</strong>. O tempo de contribuição é de <strong>15 anos</strong> para quem já contribuía antes de 13/11/2019 e de <strong>20 anos</strong> para quem começou depois.</p>
                        <p>Os 15 anos equivalem a 180 meses de contribuição. Esses meses podem ser somados mesmo com intervalos, por exemplo, se a pessoa parou de contribuir por um tempo e depois voltou.</p>
                        <p>Importante: existem outras regras de transição que podem alterar esses valores.</p>
                        <p class="fonte">Fontes: <a href="{FONTE_INSS}">INSS: tudo sobre a aposentadoria por idade</a> e <a href="{FONTE_EC103}">Emenda Constitucional 103/2019 (arts. 18 e 19)</a></p>'''
    r2 = f'''                        <p>Quem já cumpre os requisitos mínimos precisa fazer duas etapas:</p>
                        <ol>
                            <li><strong>Pedir o benefício</strong> pelo <a href="{url("site")}">site do Meu INSS</a> ou pelo aplicativo Meu INSS (<a href="{url("Android")}">Android</a> ou <a href="{url("IOS")}">iPhone</a>), confirmando o serviço, o requerente, a unidade e as relações. Também é possível pedir pelo telefone <a href="tel:135">135</a>, de segunda a sábado, das 7h às 22h.</li>
                            <li><strong>Acompanhar a resposta</strong> do pedido, que demora em média 45 dias. No Meu INSS, use a opção “Consultar Pedidos”.</li>
                        </ol>
                        <p class="fonte">Fontes: <a href="{FONTE_SERVICO}">gov.br</a> e <a href="{FONTE_INSS}">INSS</a></p>'''
    r3 = f'''                        <p>Atualmente, as modalidades de aposentadoria são:</p>
                        <ol>
                            <li><a href="{url("Aposentadoria por idade")}">Aposentadoria por idade</a>: urbana, rural ou híbrida</li>
                            <li><a href="{url("Aposentadoria especial")}">Aposentadoria especial</a>: para quem trabalhou exposto a agentes nocivos à saúde</li>
                            <li><a href="{url("Aposentadoria por incapacidade permanente (antiga aposentadoria por invalidez)")}">Aposentadoria por incapacidade permanente</a> (antiga aposentadoria por invalidez)</li>
                            <li><a href="{url("Aposentadoria por tempo de contribuição")}">Aposentadoria por tempo de contribuição</a>: só pelas regras de transição, para quem já contribuía antes de 13/11/2019</li>
                            <li><a href="{url("Aposentadoria do professor")}">Aposentadoria do professor</a></li>
                            <li><a href="{url("Aposentadoria da pessoa com deficiência")}">Aposentadoria da pessoa com deficiência</a></li>
                        </ol>'''
    r4 = '''                        <p>O pedido de aposentadoria pode ser feito sem advogado na fase administrativa.</p>
                        <p>Um advogado pode analisar as regras de transição e os cálculos que se aplicam ao seu histórico e orientar sobre os seus direitos antes do pedido.</p>'''
    return (f'''        <section id="duvidas" class="duvidas">
            <div class="container">
                <div class="duvidas-topo">
                    <h2>{titulo}</h2>
                    {f'<img class="duvidas-ilustracao" src="{ilustracao}" alt="" width="800" height="800">' if ilustracao else ""}
                </div>
'''
            + pergunta("idade", "Qual é a idade mínima para se aposentar?", r1, com_icone, avatar=avatares.get("idade"), aberta=True)
            + pergunta("como", "Como a pessoa se aposenta?", r2, com_icone, avatar=avatares.get("como"))
            + pergunta("tipos", "Quais são os tipos de aposentadoria?", r3, com_icone, avatar=avatares.get("tipos"))
            + pergunta("porque", "Por que consultar um advogado?", r4, com_icone, avatar=avatares.get("porque"))
            + '''            </div>
        </section>
''')

def simulador(titulo):
    return f'''<form class="simulador" id="simulador">
                    <h2>{titulo}</h2>
                    <p>Confira os requisitos da aposentadoria por idade urbana. O resultado aparece sozinho enquanto você preenche. Os números ficam só no seu aparelho: nada é enviado.</p>
                    <fieldset>
                        <legend>Você é</legend>
                        <div class="opcoes">
                            <label class="opcao"><input type="radio" name="sexo" value="mulher"> Mulher</label>
                            <label class="opcao"><input type="radio" name="sexo" value="homem"> Homem</label>
                        </div>
                    </fieldset>
                    <fieldset id="pergunta-filiacao" hidden>
                        <legend>Você já contribuía para o INSS antes de 13 de novembro de 2019?</legend>
                        <div class="opcoes">
                            <label class="opcao"><input type="radio" name="filiacao" value="antes"> Sim</label>
                            <label class="opcao"><input type="radio" name="filiacao" value="depois"> Não, comecei depois</label>
                        </div>
                    </fieldset>
                    <div class="campos">
                        <label class="campo">Sua idade (em anos) <input type="number" name="idade" min="0" max="120" step="1" inputmode="numeric"></label>
                        <label class="campo">Anos de contribuição <input type="number" name="contribuicao" min="0" max="80" step="1" inputmode="numeric"></label>
                    </div>
                    <div class="simulador-resultado" id="resultado" role="status" aria-live="polite"></div>
                </form>'''

def contato(titulo, ilustracao=None):
    return f'''        <section id="contato" class="contato">
            <div class="container">
                <div class="contato-topo">
                    <div>
                        <h2>{titulo}</h2>
                        <p>Escolha a forma mais fácil para você.</p>
                    </div>
                    {f'<img class="contato-ilustracao" src="{ilustracao}" alt="" width="800" height="800" loading="lazy">' if ilustracao else ""}
                </div>
                <ul class="contato-lista">
                    <li><a class="contato-cartao" href="{WA}">{WPP}<span><span class="contato-rotulo">WhatsApp</span><span class="contato-valor">(22) 99881-5479</span></span></a></li>
                    <li><a class="contato-cartao" href="tel:+5522998815479">{TEL}<span><span class="contato-rotulo">Telefone</span><span class="contato-valor">(22) 99881-5479</span></span></a></li>
                    <li><a class="contato-cartao" href="mailto:ericmf@adv.oabrj.org.br">{EMAIL}<span><span class="contato-rotulo">E-mail</span><span class="contato-valor">ericmf@adv.oabrj.org.br</span></span></a></li>
                </ul>
                <p class="redes-titulo">Acompanhe nas redes sociais</p>
                <div class="redes">
                    {REDES}
                </div>
            </div>
        </section>
'''

def endereco(titulo):
    return f'''        <section id="endereco" class="endereco">
            <div class="container endereco-grade">
                <div>
                    <h2>{titulo}</h2>
                    <address>Rua Professor Carlos Goes, 71 – Centro<br>Campos dos Goytacazes – RJ<br>CEP 28035-155</address>
                    <a class="botao botao-contorno" href="{COMO_CHEGAR}">Como chegar</a>
                </div>
                <iframe title="Mapa do escritório" hidden data-src="{MAPA}" allowfullscreen="" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
            </div>
        </section>
'''

SCRIPT = '''    <script>
        const botaoMenu = document.querySelector(".botao-menu");
        const menu = document.getElementById("menu");
        function fecharMenu(){
            botaoMenu.setAttribute("aria-expanded", "false");
            menu.classList.remove("aberto");
        }
        botaoMenu.addEventListener("click", () => {
            const abrir = botaoMenu.getAttribute("aria-expanded") !== "true";
            botaoMenu.setAttribute("aria-expanded", abrir);
            menu.classList.toggle("aberto", abrir);
        });
        menu.querySelectorAll("a").forEach(link => link.addEventListener("click", fecharMenu));

        // Link para uma pergunta abre a resposta
        function abrirPergunta(){
            const alvo = location.hash && document.getElementById(location.hash.slice(1));
            if (alvo && alvo.tagName === "DETAILS") alvo.open = true;
        }
        window.addEventListener("hashchange", abrirPergunta);
        abrirPergunta();

        // Conferência dos requisitos da aposentadoria por idade urbana (EC 103/2019)
        const simulador = document.getElementById("simulador");
        if (simulador) {
            const resultado = document.getElementById("resultado");
            const perguntaFiliacao = document.getElementById("pergunta-filiacao");
            const campoIdade = simulador.elements.idade;
            const campoContribuicao = simulador.elements.contribuicao;
            const linkWhatsapp = document.querySelector(".whatsapp-flutuante").href;
            const anos = n => n === 1 ? "1 ano" : n + " anos";
            const aviso = "<p class=\\"aviso\\">Vale para a aposentadoria por idade urbana. Trabalhadores rurais, " +
                "professores e pessoas com deficiência têm regras próprias. É só uma estimativa: " +
                "detalhes do seu histórico podem mudar o resultado. Para uma análise individual, " +
                "<a href=\\"" + linkWhatsapp + "\\">fale pelo WhatsApp</a>.</p>";

            function regraAplicavel(sexo, filiacao){
                if (sexo === "mulher") return {idade: 62, contribuicao: 15, nome: "Regra para mulheres"};
                if (filiacao === "antes") return {idade: 65, contribuicao: 15, nome: "Regra de transição para homens que já contribuíam antes de 13/11/2019"};
                if (filiacao === "depois") return {idade: 65, contribuicao: 20, nome: "Regra para homens que começaram a contribuir depois de 13/11/2019"};
                return null;
            }

            function atualizar(){
                const dados = new FormData(simulador);
                const sexo = dados.get("sexo");
                perguntaFiliacao.hidden = sexo !== "homem";
                if (!campoIdade.validity.valid || !campoContribuicao.validity.valid) {
                    resultado.innerHTML = "<p>Digite apenas números inteiros: idade até 120 anos e contribuição até 80 anos.</p>";
                    return;
                }
                const regra = regraAplicavel(sexo, dados.get("filiacao"));
                if (sexo === "homem" && !regra) {
                    resultado.innerHTML = "<p>Responda se você já contribuía para o INSS antes de 13 de novembro de 2019 para ver o resultado.</p>";
                    return;
                }
                if (!regra || campoIdade.value === "" || campoContribuicao.value === "") {
                    resultado.innerHTML = "";
                    return;
                }
                const idade = Number(campoIdade.value);
                const contribuicao = Number(campoContribuicao.value);
                if (contribuicao > idade) {
                    resultado.innerHTML = "<p>O tempo de contribuição não pode ser maior que a sua idade. Confira os números.</p>";
                    return;
                }
                const faltaIdade = Math.max(0, regra.idade - idade);
                const faltaContribuicao = Math.max(0, regra.contribuicao - contribuicao);
                let resumo;
                if (!faltaIdade && !faltaContribuicao) {
                    resumo = "Por essa regra, você já tem a idade e o tempo de contribuição mínimos.";
                } else {
                    const faltas = [];
                    if (faltaIdade) faltas.push(anos(faltaIdade) + " de idade");
                    if (faltaContribuicao) faltas.push(anos(faltaContribuicao) + " de contribuição");
                    const plural = faltas.length > 1 || Math.max(faltaIdade, faltaContribuicao) > 1;
                    resumo = "Por essa regra, ainda falta" + (plural ? "m " : " ") + faltas.join(" e ") + ".";
                }
                resultado.innerHTML = "<p><strong>" + resumo + "</strong></p>" +
                    "<p>" + regra.nome + ": " + regra.idade + " anos de idade e " + regra.contribuicao + " anos de contribuição.</p>" +
                    aviso;
            }

            // Botões de opção atualizam na hora; números esperam a pessoa terminar de digitar
            let espera;
            simulador.addEventListener("input", evento => {
                clearTimeout(espera);
                if (evento.target.type === "number") espera = setTimeout(atualizar, 800);
                else atualizar();
            });
            simulador.addEventListener("change", evento => {
                if (evento.target.type !== "number") return;
                clearTimeout(espera);
                atualizar();
            });
            simulador.addEventListener("submit", evento => {
                evento.preventDefault();
                clearTimeout(espera);
                atualizar();
            });
        }
    </script>
'''

def rodape():
    return f'''    <footer class="rodape">
        <div class="container">
            <p class="rodape-nome">Eric Fernandes</p>
            <p>Advogado · OAB/RJ 256 078</p>
            <nav class="rodape-links" aria-label="Rodapé">
                <a href="#inicio">Início</a>
                <a href="#duvidas">Dúvidas</a>
                <a href="#contato">Contato</a>
                <a href="#endereco">Endereço</a>
                <a href="../previdenciario/blog/">Artigos</a>
                <a href="../privacidade/">Política de privacidade</a>
                <button type="button" data-preferencias-cookies>Preferências de cookies</button>
            </nav>
            <p class="rodape-direitos">Todos os direitos reservados.</p>
        </div>
    </footer>
    <a class="botao botao-whatsapp whatsapp-flutuante" href="{WA}">{WPP}<span>Falar no WhatsApp</span></a>
{SCRIPT}</body>
</html>
'''

SOBRE_TEXTO = ('Tenho experiência com <strong>Direito Previdenciário</strong>. Busco integrar o Direito à Tecnologia, '
               'trazendo a <strong>prática jurídica conciliada à inovação</strong>.')
DESCRICAO = "Eric Fernandes, advogado previdenciarista (OAB/RJ 256 078), em Campos dos Goytacazes – RJ. Informações sobre aposentadoria, requisitos e canais de atendimento."

# ---------- Versão Clássica ----------
MOLDURA_FUNDO = " com-fundo" if imagem("93115", "fundo-biblioteca") else ""
HEROI_TEXTURA = " com-textura" if imagem("93115", "textura-madeira") else ""
classica = (cabeca(["fontes.css", "fontes-serifas.css"], DESCRICAO, codigo="93115") + f"""    <main id="conteudo">
        <section class="titulo-faixa">
            <div class="container">
                <h1>Eric Fernandes <span class="titulo-divisor" aria-hidden="true">|</span> <span class="titulo-area">Advogado Previdenciarista</span></h1>
            </div>
        </section>
        <section class="heroi{HEROI_TEXTURA}">
            <div class="container heroi-grade">
                <div class="moldura{MOLDURA_FUNDO}">{FOTO}</div>
                <div class="heroi-texto">
                    <h2>Dúvidas sobre aposentadoria?</h2>
                    <ul class="lista-check">
                        <li><a href="#pergunta-idade">Qual é a idade mínima para se aposentar?</a></li>
                        <li><a href="#pergunta-como">Como a pessoa se aposenta?</a></li>
                        <li><a href="#pergunta-tipos">Quais são os tipos de aposentadoria?</a></li>
                        <li><a href="#pergunta-porque">Por que consultar um advogado?</a></li>
                    </ul>
                    <div class="acoes">
                        <a class="botao botao-ouro" href="#contato">Ver canais de atendimento</a>
                        <a class="botao botao-contorno-ouro" href="{WA}">{WPP}Falar no WhatsApp</a>
                    </div>
                </div>
            </div>
        </section>
        <section id="sobre" class="sobre">
            <div class="container">
                <h2>Quem é Eric?</h2>
                <p>{SOBRE_TEXTO}</p>
                <p>Advogado com foco em Advocacia Previdenciarista. Atualmente curso Ciência da Computação.</p>
            </div>
        </section>
""" + duvidas("Perguntas frequentes") + contato("Contato") + endereco("Endereço") + "    </main>\n" + rodape())

# ---------- Versão Moderna ----------
moderna = (cabeca(["fontes.css"], DESCRICAO, codigo="75946") + f'''    <main id="conteudo">
        <section class="apresentacao">
            <div class="container apresentacao-grade">
                <div>
                    <p class="selo">Advogado Previdenciarista · OAB/RJ 256 078</p>
                    <h1>Eric Fernandes</h1>
                    <p class="apresentacao-sub">Previdência &amp; Inovação</p>
                    <p class="apresentacao-lead">Direito e tecnologia juntos para ajudar você a entender e pedir a sua aposentadoria.</p>
                    <div class="acoes">
                        <a class="botao botao-whatsapp" href="{WA}">{WPP}Falar no WhatsApp</a>
                        <a class="botao botao-contorno" href="#simulador">Calcular requisitos</a>
                    </div>
                </div>
                <div class="apresentacao-foto">{FOTO}</div>
            </div>
        </section>
        <section id="sobre" class="sobre">
            <div class="container">
                <div class="sobre-cartao">
                    <h2>Quem é Eric?</h2>
                    <p>{SOBRE_TEXTO}</p>
                    <p>Advogado com foco em Advocacia Previdenciarista. Atualmente curso Ciência da Computação.</p>
                </div>
            </div>
        </section>
        <section class="secao-simulador">
            <div class="container">
                {simulador("Calcule os requisitos")}
            </div>
        </section>
''' + duvidas("Dúvidas frequentes", com_icone=True) + contato("Atendimento") + endereco("Onde estamos") + "    </main>\n" + rodape())

# ---------- Versão Acolhedora ----------
PASTA_ACOLHEDORA = raiz / "48652"
def imagem_acolhedora(nome):
    """Caminho da imagem gerada, se ela já foi adicionada em 48652/img/."""
    return f"img/{nome}.webp" if (PASTA_ACOLHEDORA / "img" / f"{nome}.webp").exists() else None

AVATARES = {chave: imagem_acolhedora(f"duvida-{chave}") for chave in ["idade", "como", "tipos", "porque"]}
FUNDO = " com-fundo" if imagem_acolhedora("fundo-escritorio") else ""
ONDA = ('<svg class="onda" viewBox="0 0 1440 90" preserveAspectRatio="none" aria-hidden="true" focusable="false">'
        '<path d="M0 45C240 95 480 95 720 60S1200 0 1440 40V90H0Z"/></svg>')

acolhedora = (cabeca(["fontes.css", "fontes-serifas.css"], DESCRICAO, codigo="48652") + f"""    <main id="conteudo">
        <section class="apresentacao">
            <div class="container apresentacao-grade">
                <div class="apresentacao-foto{FUNDO}">{FOTO}</div>
                <div>
                    <p class="saudacao">Bem-vindo! Sinta-se acolhido.</p>
                    <h1>Sua aposentadoria, explicada com clareza.</h1>
                    <p class="apresentacao-lead">Sou Eric Fernandes, advogado com foco em Direito Previdenciário. Aqui você tira suas dúvidas e confere os requisitos básicos em poucos passos.</p>
                    {simulador("Confira os requisitos")}
                </div>
            </div>
            {ONDA}
        </section>
""" + duvidas("Dúvidas sobre aposentadoria", com_icone=True, avatares={k: v for k, v in AVATARES.items() if v},
                ilustracao=imagem_acolhedora("ilustracao-duvidas")) + f"""        <section id="sobre" class="sobre">
            <div class="container">
                <div class="sobre-cartao">
                    <h2>Quem é Eric?</h2>
                    <p>{SOBRE_TEXTO}</p>
                    <p>Advogado com foco em Advocacia Previdenciarista. Atualmente curso Ciência da Computação.</p>
                    <a class="botao botao-whatsapp" href="{WA}">{WPP}Conversar com Eric no WhatsApp</a>
                </div>
            </div>
        </section>
""" + contato("Fale comigo", imagem_acolhedora("ilustracao-contato")) + endereco("Onde estamos") + "    </main>\n" + rodape())

# ---------- Versão Futurista (estilo Apple) ----------
def video_futurista(nome):
    """Vídeo gerado para a rolagem, se já foi adicionado em 59899/video/."""
    for extensao in ["webm", "mp4"]:
        if (raiz / "59899" / "video" / f"{nome}.{extensao}").exists():
            return f"video/{nome}.{extensao}"
    return None

VIDEO_CINEMA = video_futurista("cinema")
VIDEO_QUADRADO = video_futurista("cinema-quadrado")
if VIDEO_CINEMA:
    # Todos os quadros são quadros-chave, para o vídeo acompanhar a rolagem sem trancos
    CINEMA_MIDIA = ('<video class="video-rolagem" muted playsinline preload="auto" poster="video/cinema-capa.webp" aria-hidden="true">'
                    + (f'<source src="{VIDEO_QUADRADO}" media="(max-width: 47.99em)">' if VIDEO_QUADRADO else "")
                    + f'<source src="{VIDEO_CINEMA}"></video>')
else:
    CINEMA_MIDIA = '<div class="orbe" aria-hidden="true"><span></span><span></span><span></span></div>'

futurista = (cabeca(["fontes.css"], DESCRICAO, codigo="59899",
                    extra='\n    <script>if (!matchMedia("(prefers-reduced-motion: reduce)").matches) document.documentElement.classList.add("com-movimento");</script>'
                          '\n    <script src="efeitos.js" defer></script>') + f"""    <main id="conteudo">
        <section class="cinema" data-rolagem="cinema" aria-labelledby="abertura-titulo">
            <div class="cinema-fixo">
                {CINEMA_MIDIA}
                <div class="cinema-texto">
                    <p class="sobrelinha">Eric Fernandes · Advogado · OAB/RJ 256 078</p>
                    <h1 id="abertura-titulo">Aposentadoria,<br><span class="degrade">explicada com clareza.</span></h1>
                    <p class="cinema-lead">Informações sobre Direito Previdenciário em linguagem simples.</p>
                    <div class="acoes">
                        <a class="botao botao-whatsapp" href="{WA}">{WPP}Falar no WhatsApp</a>
                        <a class="botao botao-contorno" href="#simulador">Conferir requisitos</a>
                    </div>
                    <p class="rolar-dica" aria-hidden="true">Role a página <span>↓</span></p>
                </div>
                <p class="cinema-legenda">Direito e tecnologia, <span class="degrade">lado a lado.</span></p>
            </div>
        </section>

        <section id="sobre" class="apresentacao" data-rolagem="apresentacao">
            <div class="container apresentacao-grade">
                <div class="apresentacao-foto">{FOTO}</div>
                <div class="apresentacao-texto">
                    <p class="sobrelinha">Quem é Eric?</p>
                    <h2>Eric <span class="degrade">Fernandes.</span></h2>
                    <p class="apresentacao-cargo">Advogado previdenciarista · OAB/RJ 256 078</p>
                    <p>{SOBRE_TEXTO}</p>
                    <p>Advogado com foco em Advocacia Previdenciarista. Atualmente curso Ciência da Computação.</p>
                    <a class="botao botao-whatsapp" href="{WA}">{WPP}Falar no WhatsApp</a>
                </div>
            </div>
        </section>

        <section class="numeros" aria-labelledby="numeros-titulo">
            <div class="container">
                <h2 id="numeros-titulo" class="revelar">A regra geral, <span class="degrade">em três números.</span></h2>
                <div class="numeros-grade">
                    <div class="numero">
                        <p class="numero-valor"><span data-contar="62">62</span> <span class="numero-unidade">anos</span></p>
                        <p>Idade mínima para <strong>mulheres</strong>.</p>
                    </div>
                    <div class="numero">
                        <p class="numero-valor"><span data-contar="65">65</span> <span class="numero-unidade">anos</span></p>
                        <p>Idade mínima para <strong>homens</strong>.</p>
                    </div>
                    <div class="numero">
                        <p class="numero-valor"><span data-contar="15">15</span> <span class="numero-unidade">anos</span></p>
                        <p>De contribuição, ou 180 meses. <strong>Vale somar períodos com intervalos</strong>, se você parou e depois voltou a contribuir.</p>
                    </div>
                </div>
                <p class="nota revelar">Homens que começaram a contribuir depois de 13/11/2019 precisam de 20 anos de contribuição. Existem regras de transição. <a href="#duvidas">Veja as dúvidas frequentes</a>.</p>
            </div>
        </section>

        <section class="faixa-tipos" data-rolagem="faixa" aria-hidden="true">
            <p class="faixa-linha">Por idade · Especial · Incapacidade permanente · Professor · Pessoa com deficiência · Tempo de contribuição ·</p>
            <p class="faixa-linha faixa-inversa">Urbana · Rural · Híbrida · Regras de transição · Meu INSS · Telefone 135 ·</p>
        </section>

        <section class="passos" data-rolagem="passos" aria-labelledby="passos-titulo">
            <div class="passos-fixo container">
                <h2 id="passos-titulo">Como pedir a <span class="degrade">aposentadoria.</span></h2>
                <ol class="passos-lista">
                    <li class="passo">
                        <span class="passo-numero" aria-hidden="true">1</span>
                        <h3>Confira os requisitos</h3>
                        <p>Use a calculadora logo abaixo e leia as dúvidas frequentes.</p>
                    </li>
                    <li class="passo">
                        <span class="passo-numero" aria-hidden="true">2</span>
                        <h3>Peça no Meu INSS</h3>
                        <p>Pelo site ou aplicativo Meu INSS, ou pelo telefone <a href="tel:135">135</a>, de segunda a sábado, das 7h às 22h.</p>
                    </li>
                    <li class="passo">
                        <span class="passo-numero" aria-hidden="true">3</span>
                        <h3>Acompanhe a resposta</h3>
                        <p>Ela sai em média em 45 dias. No Meu INSS, use a opção “Consultar Pedidos”.</p>
                    </li>
                </ol>
            </div>
        </section>

        <section class="secao-simulador">
            <div class="container revelar">
                {simulador("Confira os requisitos")}
            </div>
        </section>
""" + duvidas("Dúvidas frequentes", com_icone=True) + contato("Fale comigo") + endereco("Onde estamos") + "    </main>\n" + rodape())

BASE = (pathlib.Path(__file__).parent / "base.css").read_text(encoding="utf-8")
for codigo, nome, html in [("93115", "classica", classica), ("75946", "moderna", moderna), ("48652", "acolhedora", acolhedora), ("59899", "futurista", futurista)]:
    pasta = raiz / codigo
    pasta.mkdir(exist_ok=True)
    (pasta / "index.html").write_text(html, encoding="utf-8")
    tema = (pathlib.Path(__file__).parent / f"tema-{nome}.css").read_text(encoding="utf-8")
    (pasta / "estilo.css").write_text(BASE + "\n" + tema, encoding="utf-8")
    print("ok", codigo, nome)
