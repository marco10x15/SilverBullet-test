# Configurazione di prova

Inserire nella pagina di configurazione dello Space:

```space-lua
config.set("frontmatterFolding", {
  foldByDefault = "long",
  foldByDefaultLines = 5,

  preview = {
    {
      field = "displayName",
      type = "markdown",
      template = "# ${value}",
    },
    {
      field = "description",
      type = "text",
      template = "📒 ${value}",
    },
    {
      field = "date",
      type = "date",
      template = "📅 ${value}",
    },
    {
      field = "luoghi",
      type = "markdown",
      template = "🗺️ ${value}",
      separator = " · ",
    },
    {
      field = "tags",
      type = "tags",
    },
  },
})
```

Frontmatter di prova:

```yaml
---
displayName: Torino e Superga
description: Visita del centro storico e della Basilica
date: 2026-09-27
luoghi:
  - "[[Luoghi/Torino]]"
  - "[[Luoghi/Superga]]"
tags:
  - viaggio
  - piemonte
---
```

Risultato atteso:

```text
Torino e Superga
📒 Visita del centro storico e della Basilica
📅 27.09.2026
🗺️ Torino · Superga
#viaggio #piemonte
<N> frontmatter lines hidden
```
