/* Consentimento de cookies (LGPD).
   Nada de terceiros que use cookies (Google Tag Manager e mapa do Google) é carregado
   antes de a pessoa escolher. A escolha fica guardada só no navegador dela. */
(() => {
    const CHAVE = "consentimento-cookies";
    const VERSAO = 1;
    const GTM_ID = "GTM-T9L6ZZSM";
    const pastaPrivacidade = document.currentScript.src.replace(/consentimento\.js.*$/, "");

    function lerEscolha(){
        try {
            const escolha = JSON.parse(localStorage.getItem(CHAVE));
            return escolha && escolha.versao === VERSAO ? escolha : null;
        } catch {
            return null;
        }
    }

    function salvarEscolha(estatisticas, mapa){
        const escolha = {estatisticas, mapa, versao: VERSAO, data: new Date().toISOString()};
        try {
            localStorage.setItem(CHAVE, JSON.stringify(escolha));
        } catch {
            // Sem armazenamento: a escolha vale só nesta visita
        }
        return escolha;
    }

    // Estatísticas: o Google Tag Manager só é carregado com permissão
    let gtmCarregado = false;
    function carregarEstatisticas(){
        if (gtmCarregado) return;
        gtmCarregado = true;
        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push({"gtm.start": Date.now(), event: "gtm.js"});
        const script = document.createElement("script");
        script.async = true;
        script.src = "https://www.googletagmanager.com/gtm.js?id=" + GTM_ID;
        document.head.appendChild(script);
    }

    function apagarCookiesDeEstatistica(){
        const partes = location.hostname.split(".");
        const dominios = ["", location.hostname];
        for (let i = 1; i < partes.length - 1; i++) dominios.push("." + partes.slice(i).join("."));
        document.cookie.split(";").map(c => c.split("=")[0].trim())
            .filter(nome => /^(_ga|_gid|_gat|_gcl)/.test(nome))
            .forEach(nome => dominios.forEach(dominio => {
                document.cookie = nome + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/" + (dominio ? "; domain=" + dominio : "");
            }));
    }

    // Mapa do Google: fica no lugar um aviso com o botão "Mostrar mapa"
    function aplicarMapas(permitir){
        document.querySelectorAll("iframe[data-src]").forEach(iframe => {
            let aviso = iframe.previousElementSibling;
            if (!aviso || !aviso.classList.contains("mapa-bloqueado")) aviso = null;
            if (permitir) {
                if (!iframe.src) iframe.src = iframe.dataset.src;
                iframe.hidden = false;
                if (aviso) aviso.remove();
                return;
            }
            iframe.hidden = true;
            if (aviso) return;
            aviso = document.createElement("div");
            aviso.className = "mapa-bloqueado";
            aviso.innerHTML =
                "<p>O mapa é fornecido pelo Google, que pode usar cookies. Ele só aparece se você permitir.</p>" +
                "<button type=\"button\">Mostrar mapa</button>";
            aviso.querySelector("button").addEventListener("click", () => {
                const atual = lerEscolha();
                aplicar(salvarEscolha(atual ? atual.estatisticas : false, true));
            });
            iframe.before(aviso);
        });
    }

    function aplicar(escolha){
        if (escolha.estatisticas) carregarEstatisticas();
        aplicarMapas(escolha.mapa);
    }

    // Aviso de cookies
    let aviso;
    function abrirOpcoes(){
        const atual = lerEscolha();
        const opcoes = aviso.querySelector(".cookies-opcoes");
        opcoes.hidden = false;
        opcoes.elements.estatisticas.checked = !!(atual && atual.estatisticas);
        opcoes.elements.mapa.checked = !!(atual && atual.mapa);
        const botao = aviso.querySelector(".cookies-escolher");
        botao.textContent = "Salvar minhas escolhas";
        botao.dataset.acao = "salvar";
    }

    function mostrarAviso(comOpcoes){
        if (!aviso) {
            aviso = document.createElement("section");
            aviso.className = "cookies";
            aviso.setAttribute("aria-labelledby", "cookies-titulo");
            aviso.innerHTML =
                "<h2 id=\"cookies-titulo\" class=\"cookies-titulo\">Sua privacidade</h2>" +
                "<p>Usamos cookies do Google para contar visitas e mostrar o mapa, só se você permitir. " +
                "Dá para mudar depois, no rodapé. <a href=\"" + pastaPrivacidade + "\">Política de privacidade</a>.</p>" +
                "<fieldset class=\"cookies-opcoes\" hidden>" +
                    "<legend>Escolha o que permitir:</legend>" +
                    "<label><input type=\"checkbox\" name=\"estatisticas\"> Estatísticas de visitas (Google Analytics)</label>" +
                    "<label><input type=\"checkbox\" name=\"mapa\"> Mapa do Google</label>" +
                "</fieldset>" +
                "<div class=\"cookies-botoes\">" +
                    "<button type=\"button\" data-acao=\"aceitar\">Aceitar</button>" +
                    "<button type=\"button\" data-acao=\"recusar\">Recusar</button>" +
                    "<button type=\"button\" data-acao=\"escolher\" class=\"cookies-escolher\">Escolher</button>" +
                "</div>";
            aviso.addEventListener("click", evento => {
                const acao = evento.target.dataset && evento.target.dataset.acao;
                if (!acao) return;
                const opcoes = aviso.querySelector(".cookies-opcoes");
                if (acao === "escolher" && opcoes.hidden) {
                    abrirOpcoes();
                    return;
                }
                const anterior = lerEscolha();
                let escolha;
                if (acao === "aceitar") escolha = salvarEscolha(true, true);
                else if (acao === "recusar") escolha = salvarEscolha(false, false);
                else escolha = salvarEscolha(opcoes.elements.estatisticas.checked, opcoes.elements.mapa.checked);
                aviso.hidden = true;
                // Retirar uma permissão já dada exige recarregar a página sem os serviços do Google
                const retirou = anterior && ((anterior.estatisticas && !escolha.estatisticas) || (anterior.mapa && !escolha.mapa));
                if (retirou) {
                    apagarCookiesDeEstatistica();
                    location.reload();
                    return;
                }
                aplicar(escolha);
            });
            document.body.appendChild(aviso);
        }
        aviso.hidden = false;
        if (comOpcoes) abrirOpcoes();
        aviso.querySelector("h2").setAttribute("tabindex", "-1");
        if (comOpcoes) aviso.querySelector("h2").focus();
    }

    function iniciar(){
        const escolha = lerEscolha();
        aplicarMapas(escolha ? escolha.mapa : false);
        if (escolha) aplicar(escolha);
        else mostrarAviso(false);
        document.querySelectorAll("[data-preferencias-cookies]").forEach(botao =>
            botao.addEventListener("click", () => mostrarAviso(true)));
    }

    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", iniciar);
    else iniciar();
})();
