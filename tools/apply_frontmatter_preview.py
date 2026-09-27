#!/usr/bin/env python3
from pathlib import Path
import shutil
import sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: apply_frontmatter_preview.py <silverbullet-source-dir>")

root = Path(sys.argv[1]).resolve()
if not (root / "package.json").exists():
    raise SystemExit(f"Not a SilverBullet source tree: {root}")

overlay = Path(__file__).resolve().parent.parent / "overlay"

def replace_exact(path: Path, old: str, new: str, label: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"Patch anchor not found ({label}) in {path}")
    if text.count(old) != 1:
        raise SystemExit(
            f"Patch anchor occurs {text.count(old)} times ({label}) in {path}"
        )
    path.write_text(text.replace(old, new), encoding="utf-8")
    print(f"patched: {path} ({label})")

src = overlay / "client/codemirror/frontmatter_folding.ts"
dst = root / "client/codemirror/frontmatter_folding.ts"
shutil.copyfile(src, dst)
print(f"replaced: {dst}")

path = root / "client/codemirror/editor_state.ts"

replace_exact(
    path,
    '''import {
  frontmatterFoldingExtension,
  frontmatterFoldPlaceholderDOM,
  prepareFrontmatterFoldPlaceholder,
} from "./frontmatter_folding.ts";''',
    '''import {
  clientFrontmatterFoldingConfig,
  frontmatterFoldingExtension,
  frontmatterFoldPlaceholderDOM,
  prepareFrontmatterFoldPlaceholder,
} from "./frontmatter_folding.ts";''',
    "editor_state import",
)

replace_exact(
    path,
    '''    codeFolding({
      preparePlaceholder: prepareFrontmatterFoldPlaceholder,
      placeholderDOM: (view, onclick, prepared) =>
        frontmatterFoldPlaceholderDOM(view, onclick, prepared, client),
    }),''',
    '''    codeFolding({
      preparePlaceholder: (state, range) =>
        prepareFrontmatterFoldPlaceholder(
          state,
          range,
          clientFrontmatterFoldingConfig(client),
        ),
      placeholderDOM: (view, onclick, prepared) =>
        frontmatterFoldPlaceholderDOM(view, onclick, prepared, client),
    }),''',
    "editor_state folding callback",
)

path = root / "libraries/Library/Std/Config.md"
old = '''    foldByDefaultLines = {
      type = "number",
      default = 5,
      minimum = 1,
      multipleOf = 1,
      description = "Fold frontmatter automatically when it has more than this positive whole number of lines and auto-fold is set to long",
      ui = { category = "Editor", label = "Frontmatter auto-fold lines", priority = -2 },
    },
'''
new = old + '''    preview = {
      type = "array",
      description = "Fields to render while frontmatter is folded",
      items = {
        type = "object",
        properties = {
          field = {
            type = "string",
            description = "Frontmatter field to render",
          },
          type = {
            type = "string",
            enum = { "text", "markdown", "tags", "date" },
            default = "text",
            description = "How to render the field value",
          },
          template = {
            type = "string",
            default = "${value}",
            description = "Template used to render the field value",
          },
          separator = {
            type = "string",
            default = ", ",
            description = "Separator used for array values",
          },
        },
        required = { "field" },
        additionalProperties = false,
      },
    },
'''
replace_exact(path, old, new, "frontmatterFolding preview schema")

path = root / "client/styles/editor.scss"
old = '''  .cm-frontmatterFoldPlaceholder {
    box-sizing: border-box;
    cursor: pointer;
    display: inline-flex;
    align-items: baseline;
    gap: 3px;
    padding: 2px 7px !important;
    user-select: none;
    width: 100%;
  }

  .cm-frontmatterFoldStatus {
    color: var(--subtle-color);
    font-size: 0.85em;
    margin-left: 0.4em;
    opacity: 0.75;
  }
'''
new = '''  .cm-frontmatterFoldPlaceholder {
    box-sizing: border-box;
    cursor: pointer;
    display: inline-flex;
    flex-direction: column;
    align-items: stretch;
    gap: 3px;
    padding: 2px 7px !important;
    user-select: none;
    width: 100%;
  }

  .cm-frontmatterPreview {
    display: block;
    width: 100%;
    white-space: normal;
  }

  .cm-frontmatterPreview-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 3px;
  }

  .cm-frontmatterPreviewHeading {
    display: block;
    font-weight: bold;
  }

  .cm-frontmatterPreviewHeading-1 {
    font-size: 2em;
    line-height: 1.2;
    margin: 0.25em 0;
  }

  .cm-frontmatterPreviewHeading-2 {
    font-size: 1.5em;
    line-height: 1.25;
  }

  .cm-frontmatterPreview-markdown .wrapper {
    display: contents;
  }

  .cm-frontmatterFoldStatus {
    color: var(--subtle-color);
    font-size: 0.85em;
    opacity: 0.75;
  }
'''
replace_exact(path, old, new, "frontmatter preview CSS")

print("SilverBullet frontmatter preview prototype applied successfully.")
