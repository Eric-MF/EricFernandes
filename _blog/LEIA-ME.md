# Como gerenciar o blog

Os artigos são arquivos de texto simples, na pasta `_blog/artigos/`. Um script transforma esses arquivos nas páginas do blog, em `previdenciario/blog/`. Não precisa instalar nada.

## Escrever um artigo novo

1. Crie um arquivo em `_blog/artigos/`. O nome do arquivo vira o endereço da página, por isso use só letras minúsculas sem acento, números e hífens.
   Exemplo: `aposentadoria-por-idade.md` → `eric.adv.br/previdenciario/blog/aposentadoria-por-idade.html`
2. Comece o arquivo com o bloco de informações:

   ```
   ---
   titulo: Aposentadoria por idade
   descricao: Quem tem direito, quais os requisitos e como pedir.
   data: 2026-10-05
   rascunho: sim
   ---
   ```

   | Campo | Para que serve |
   |---|---|
   | `titulo` | Título do artigo (obrigatório). |
   | `descricao` | Resumo de uma ou duas frases. Aparece na lista de artigos e no Google (obrigatório). |
   | `data` | Data de publicação, no formato AAAA-MM-DD (obrigatório). |
   | `atualizado` | Data da última revisão, se houver (opcional). |
   | `rascunho` | `sim` para não publicar ainda, `não` para publicar. |

3. Escreva o texto abaixo do bloco.
4. Publique:

   ```
   python3 _blog/publicar.py
   ```

   O script avisa se faltar alguma informação e não publica nada até você corrigir.
5. Confira a página no navegador e faça o commit.

## Como escrever o texto

| Você escreve | Aparece como |
|---|---|
| `## Título da seção` | Título de seção (entra no sumário “Neste artigo”) |
| `### Subtítulo` | Subtítulo |
| `**texto**` | **negrito** |
| `*texto*` | *itálico* |
| `[texto do link](https://endereço)` | link |
| `- item` | lista com marcadores |
| `1. item` | lista numerada |
| `> texto` | citação de lei, em destaque |
| `Fonte: [Lei tal](https://...)` | linha de fonte, em letra menor |

Deixe uma linha em branco entre parágrafos. Para citar uma lei, use `>` em todas as linhas da citação, inclusive nas linhas em branco entre os incisos:

```
> **Art. 20.** O benefício de prestação continuada é a garantia de...
>
> Fonte: [Lei nº 8.742/1993, art. 20](https://www.planalto.gov.br/...)
```

Para um título de seção com endereço próprio, que dá para usar em links, acrescente `{#nome}`: `## Saúde {#saude}`. O link fica `[Saúde](#saude)`.

## Outras tarefas

- **Corrigir um artigo:** edite o `.md`, atualize o campo `atualizado` e rode o script de novo.
- **Tirar um artigo do ar:** mude para `rascunho: sim` ou apague o arquivo e rode o script. A página é removida.
- **Aparência:** o blog acompanha sozinho a última versão do site que a pessoa visitou (site atual, Clássica, Moderna, Acolhedora ou Futurista), e o link “Voltar ao site” leva para a mesma versão. Para ver um tema específico, acrescente ao endereço `?versao=` e o código, por exemplo `…/blog/?versao=48652`.
- **Mudar o visual:** as cores e letras ficam em `previdenciario/blog/blog.css`, com um bloco para cada tema. O cabeçalho e o rodapé de todas as páginas ficam em `_blog/modelos/partes/`.
- **Não edite** os arquivos `.html` de `previdenciario/blog/`. Eles são refeitos pelo script a cada publicação.

## Publicidade da advocacia

Os artigos devem ser informativos (Provimento 205/2021 do Conselho Federal da OAB). Evite prometer resultados, citar casos concretos de clientes ou usar frases que chamem para contratar. Todo artigo já sai com o aviso de que o conteúdo é informativo e com o seu nome e a inscrição na OAB.
