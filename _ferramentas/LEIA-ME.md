# Ferramentas do site

Esta pasta guarda os scripts usados para gerar e testar o site. Ela começa com `_`, então não é publicada no GitHub Pages.

## Regenerar as versões de teste

As versões 93115 (Clássica), 75946 (Moderna), 48652 (Acolhedora) e 59899 (Futurista) são geradas a partir do `index.html` e dos temas da pasta `versoes/`:

```
python3 _ferramentas/versoes/gerar_versoes.py
```

O script reescreve `index.html` e `estilo.css` de cada versão. Não edite esses arquivos à mão: altere o gerador ou os arquivos `base.css` e `tema-*.css`.

## Ver o site localmente

O site roda com o pm2, no endereço do Tailscale desta máquina:

```
pm2 restart site-eric
```

Depois abra o endereço do Tailscale desta máquina, na porta 8000.

As folhas de estilo da página inicial levam `?v=5` no endereço (em `index.html` e nos `@import` de `styles.css`). Ao mudar o CSS, aumente esse número nos dois lugares: o navegador de quem já visitou o site passa a baixar a versão nova.

O processo usa `_ferramentas/servidor.py`, que avisa o navegador para conferir se há versão nova a cada visita. Assim, mudanças no CSS aparecem sem precisar limpar o cache. Para recriar o processo:

```
pm2 start _ferramentas/servidor.py --name site-eric --interpreter python3 -- 8000 <endereço do Tailscale>
```

## Capturas de tela

`cdp.mjs` abre o Chrome em modo headless e tira capturas em tamanhos de celular e computador. Use para comparar a aparência antes e depois de uma mudança.
