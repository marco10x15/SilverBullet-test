#!/usr/bin/env python3
from pathlib import Path
import sys

if len(sys.argv) != 2:
    raise SystemExit("Usage: patch_frontmatter_tests.py <silverbullet-source-dir>")

root = Path(sys.argv[1]).resolve()
path = root / "client/codemirror/frontmatter_folding.test.ts"
text = path.read_text(encoding="utf-8")

def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(
            f"Test patch anchor count={count}, expected=1 ({label}) in {path}"
        )
    text = text.replace(old, new)
    print(f"patched test: {label}")

replace_once(
    '      foldByDefaultLines: 12,\n    });',
    '      foldByDefaultLines: 12,\n'
    '      preview: [\n'
    '        {\n'
    '          field: "tags",\n'
    '          type: "tags",\n'
    '          template: "${value}",\n'
    '          separator: " ",\n'
    '        },\n'
    '      ],\n'
    '    });',
    "partial config includes default preview",
)

replace_once(
    '      foldByDefaultLines: 5,\n    });',
    '      foldByDefaultLines: 5,\n'
    '      preview: [\n'
    '        {\n'
    '          field: "tags",\n'
    '          type: "tags",\n'
    '          template: "${value}",\n'
    '          separator: " ",\n'
    '        },\n'
    '      ],\n'
    '    });',
    "default config includes preview",
)

replace_once(
    '      lines: 4,\n      tags: [],\n    });',
    '      lines: 4,\n      preview: [],\n    });',
    "prepared placeholder uses preview",
)

replace_once(
    '        lines: 4,\n        tags: [],\n      }),',
    '        lines: 4,\n        preview: [],\n      }),',
    "placeholder text test uses preview",
)

replace_once(
    '{ type: "frontmatter", from: 0, to: 17, editPos: 4, lines: 4, tags: [] },',
    '{ type: "frontmatter", from: 0, to: 17, editPos: 4, lines: 4, preview: [] },',
    "DOM empty placeholder uses preview",
)

replace_once(
    '        lines: 4,\n        tags: ["feature", "beta"],\n      },',
    '        lines: 4,\n'
    '        preview: [\n'
    '          {\n'
    '            config: {\n'
    '              field: "tags",\n'
    '              type: "tags",\n'
    '              template: "${value}",\n'
    '              separator: " ",\n'
    '            },\n'
    '            value: ["feature", "beta"],\n'
    '          },\n'
    '        ],\n'
    '      },',
    "DOM tags preview",
)

replace_once(
    '          lines: 4,\n          tags: ["feature"],\n        },\n        {\n          config: {',
    '          lines: 4,\n'
    '          preview: [\n'
    '            {\n'
    '              config: {\n'
    '                field: "tags",\n'
    '                type: "tags",\n'
    '                template: "${value}",\n'
    '                separator: " ",\n'
    '              },\n'
    '              value: ["feature"],\n'
    '            },\n'
    '          ],\n'
    '        },\n'
    '        {\n'
    '          config: {',
    "tag navigation preview",
)

replace_once(
    '          lines: 4,\n          tags: ["feature"],\n        },\n      );',
    '          lines: 4,\n'
    '          preview: [\n'
    '            {\n'
    '              config: {\n'
    '                field: "tags",\n'
    '                type: "tags",\n'
    '                template: "${value}",\n'
    '                separator: " ",\n'
    '              },\n'
    '              value: ["feature"],\n'
    '            },\n'
    '          ],\n'
    '        },\n'
    '      );',
    "background click preview",
)

path.write_text(text, encoding="utf-8")
print("SilverBullet frontmatter folding tests updated successfully.")
