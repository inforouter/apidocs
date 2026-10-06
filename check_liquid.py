"""Fails when a page would break GitHub Pages' Jekyll build, or show Liquid tags on the zensical site.

The site is built by zensical (.github/workflows/docs.yml), but GitHub also runs its own Jekyll build of
docs/, and Jekyll first runs every page through Liquid:

- {{ ... }} is a Liquid variable: it prints as nothing, and one that ends in a single } - like the Word
  template syntax {{Due}:format(dd.MM.yyyy)} - stops the whole build with "Variable was not properly
  terminated".
- {% ... %} is a Liquid tag.

A page that shows such text wraps it in a raw block written inside HTML comments, which Liquid obeys and
markdown hides:

    <!-- {% raw %} -->
    ...{{placeholders}}...
    <!-- {% endraw %} -->

A bare {% raw %} works for Jekyll but prints as text on the zensical site, so it is refused too.
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
TOKEN = re.compile(r"\{%.*?%\}|\{\{.*?\}\}?", re.S)
RAW_BLOCK = re.compile(r"<!--\s*\{%-?\s*raw\s*-?%\}\s*-->.*?<!--\s*\{%-?\s*endraw\s*-?%\}\s*-->", re.S)


def problems(text):
    raw = [(m.start(), m.end()) for m in RAW_BLOCK.finditer(text)]
    for m in TOKEN.finditer(text):
        if any(a <= m.start() < b for a, b in raw):
            continue
        line = text.count("\n", 0, m.start()) + 1
        token = m.group(0)
        if token.startswith("{%"):
            yield line, f"Liquid tag {token[:50]!r}: wrap the text in <!-- {{% raw %}} --> ... <!-- {{% endraw %}} -->"
        else:
            yield line, f"Liquid variable {token[:50]!r}: wrap the text in <!-- {{% raw %}} --> ... <!-- {{% endraw %}} -->"


def main():
    count = 0
    for name in sorted(os.listdir(DOCS)):
        if name.endswith(".md"):
            with open(os.path.join(DOCS, name), encoding="utf-8-sig") as f:
                for line, message in problems(f.read()):
                    print(f"docs/{name}:{line}: {message}")
                    count += 1
    if count:
        print(f"{count} Liquid problem(s): GitHub's Jekyll build would fail or blank these out.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
