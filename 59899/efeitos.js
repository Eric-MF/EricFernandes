/* Efeitos de rolagem no estilo Apple.
   Com "reduzir movimento" ativado no aparelho, tudo aparece parado e visível. */
(() => {
    const reduzir = matchMedia("(prefers-reduced-motion: reduce)").matches;
    document.documentElement.classList.toggle("com-movimento", !reduzir);
    if (reduzir) return;

    // Grupos surgem em sequência, um item depois do outro
    [".numeros-grade", ".duvidas .container", ".contato-lista", ".redes", ".endereco-grade"].forEach(seletor =>
        document.querySelectorAll(seletor).forEach(grupo =>
            [...grupo.children].forEach((item, indice) => {
                item.classList.add("revelar");
                item.style.transitionDelay = Math.min(indice, 6) * 110 + "ms";
            })));

    // Conteúdo surge ao entrar na tela
    const observarRevelar = new IntersectionObserver(entradas => entradas.forEach(entrada => {
        if (!entrada.isIntersecting) return;
        entrada.target.classList.add("visivel");
        observarRevelar.unobserve(entrada.target);
    }), {rootMargin: "0px 0px -10% 0px"});
    document.querySelectorAll(".revelar").forEach(elemento => observarRevelar.observe(elemento));

    // Números começam do zero e contam até o valor final quando aparecem
    const observarNumeros = new IntersectionObserver(entradas => entradas.forEach(entrada => {
        if (!entrada.isIntersecting) return;
        observarNumeros.unobserve(entrada.target);
        const alvo = Number(entrada.target.dataset.contar);
        const inicio = performance.now() + 250;
        const passo = agora => {
            const t = Math.min(1, Math.max(0, (agora - inicio) / 1400));
            entrada.target.textContent = Math.round(alvo * (1 - Math.pow(1 - t, 4)));
            if (t < 1) requestAnimationFrame(passo);
        };
        requestAnimationFrame(passo);
    }), {threshold: .6});
    document.querySelectorAll("[data-contar]").forEach(numero => {
        numero.textContent = "0";
        observarNumeros.observe(numero);
    });

    // Seções que acompanham a rolagem: --progresso vai de 0 a 1 enquanto a seção passa
    const secoes = [...document.querySelectorAll("[data-rolagem]")];
    let pedido = false;
    function atualizar(){
        pedido = false;
        const alturaTela = innerHeight;
        secoes.forEach(secao => {
            const caixa = secao.getBoundingClientRect();
            if (caixa.bottom < -alturaTela || caixa.top > alturaTela * 2) return;
            const percurso = caixa.height - alturaTela;
            const progresso = percurso > 0
                ? Math.min(1, Math.max(0, -caixa.top / percurso))
                : Math.min(1, Math.max(0, (alturaTela - caixa.top) / (alturaTela + caixa.height)));
            secao.style.setProperty("--progresso", progresso.toFixed(4));
            if (secao.dataset.rolagem === "passos") secao.dataset.ativo = Math.min(3, Math.floor(progresso * 3.2) + 1);
            // Na abertura, o texto deixa de ser clicável depois que some
            if (secao.dataset.rolagem === "cinema") secao.dataset.fase = progresso < .45 ? "1" : "2";
            const video = secao.querySelector(".video-rolagem");
            if (video && video.duration) {
                const tempo = progresso * (video.duration - .05);
                if (Math.abs(video.currentTime - tempo) > 1 / 30) video.currentTime = tempo;
            }
        });
    }
    function agendar(){
        if (pedido) return;
        pedido = true;
        requestAnimationFrame(atualizar);
    }
    addEventListener("scroll", agendar, {passive: true});
    addEventListener("resize", agendar);
    // A capa (balança pronta) fica só para quem não tem movimento; aqui o vídeo começa do primeiro quadro
    document.querySelectorAll(".video-rolagem").forEach(video => {
        video.removeAttribute("poster");
        const primeiroQuadro = () => {
            video.currentTime = .001;
            agendar();
        };
        if (video.readyState >= 1) primeiroQuadro();
        else video.addEventListener("loadedmetadata", primeiroQuadro);
    });
    atualizar();
})();
