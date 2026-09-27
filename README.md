# SilverBullet-test — Frontmatter Preview experimental build

Repository di build per una versione sperimentale di SilverBullet 2.11.1 con
preview configurabile del frontmatter collassato.

## Struttura da caricare

```text
.github/
  workflows/
    build-silverbullet-frontmatter-preview.yml
tools/
  apply_frontmatter_preview.py
overlay/
  client/
    codemirror/
      frontmatter_folding.ts
examples/
  frontmatter-preview-config.md
README.md
```

## Workflow

Il workflow manuale:

1. scarica `silverbulletmd/silverbullet` tag `2.11.1`;
2. applica il prototipo;
3. esegue `npm run check`;
4. esegue `npm run build`;
5. compila il server statico `linux/amd64`;
6. costruisce l'immagine con il `Dockerfile` ufficiale;
7. pubblica su GHCR:
   - `ghcr.io/marco10x15/silverbullet-frontmatter-preview:2.11.1-test`
   - `ghcr.io/marco10x15/silverbullet-frontmatter-preview:test`

## Prima build: variante SLIM

La prima build usa il `Dockerfile` SLIM ufficiale di SilverBullet 2.11.1.
È sufficiente per testare il frontmatter e riduce la complessità. Non include
Chromium/runtime API.

Dopo la prova positiva potremo aggiungere anche la build completa basata su
`Dockerfile.runtime-api`.

## Avvio

Dopo il caricamento:

1. aprire `marco10x15/SilverBullet-test`;
2. aprire **Actions**;
3. selezionare **Build SilverBullet frontmatter preview**;
4. scegliere **Run workflow**;
5. attendere il primo risultato.

Se fallisce, inviare il log del primo step rosso prima di modificare altro.

## GHCR

Il workflow dichiara:

```yaml
permissions:
  contents: read
  packages: write
```

Se il package viene creato privato, il NAS dovrà autenticarsi a GHCR. Se viene
reso pubblico, il pull potrà essere anonimo.

## Renderer del prototipo

- `text`
- `markdown`
- `tags`
- `date`

`date` converte `YYYY-MM-DD` in `DD.MM.YYYY`.

Senza `preview`, il comportamento di default resta la visualizzazione dei soli
tag, coerente con SilverBullet 2.11.1.


## Revisione v3

Correzioni dopo la prima esecuzione GitHub Actions:

- genera `version.json` prima del type-check usando `npm run build:plugs`;
- aggiorna separatamente i test upstream alla nuova struttura `preview`;
- esegue il test mirato del frontmatter prima della build completa.


## Correzione v4

Il type-check della v3 ha superato `npm run check`, ma il test mirato falliva
all'import perché `frontmatter_folding.ts` importava `parseHtmlString` da
`lua_widget.ts`. Quest'ultimo inizializza il sandbox iframe a livello di modulo
e richiede `document`, che non esiste nell'ambiente Node di Vitest.

La v4:
- rimuove l'import da `lua_widget.ts`;
- implementa localmente il piccolo parsing HTML necessario alla preview;
- non modifica il comportamento nel browser;
- rende nuovamente importabile `frontmatter_folding.ts` nei test Node.
