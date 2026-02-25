import os
import re
import glob

pattern = re.compile(r'\]\((?!http|#|/|\.\/)([A-Za-z0-9_\-]+)\)')

for path in glob.glob('docs/**/*.md', recursive=True):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    fixed = pattern.sub(r'](\1.md)', content)
    if fixed != content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(fixed)
        print('Fixed links:', os.path.basename(path))

print('Done.')
