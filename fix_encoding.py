import os, glob, re

for path in glob.glob('docs/**/*.md', recursive=True):
    with open(path, 'rb') as f:
        data = f.read()

    # Strip UTF-8 BOM
    if data[:3] == b'\xef\xbb\xbf':
        data = data[3:]

    # Decode bytes: replace any invalid UTF-8 sequence with U+FFFD, then swap to '-'
    text = data.decode('utf-8', errors='replace')

    dirty = '\ufffd' in text or data[:3] == b'\xef\xbb\xbf'
    if dirty:
        text = text.replace('\ufffd', '-')

    # Remove "For detailed documentation visit" footer line (with surrounding blank lines)
    cleaned = re.sub(r'\n*\*For detailed documentation visit:.*\*\s*$', '', text, flags=re.MULTILINE)
    if cleaned != text:
        dirty = True
        text = cleaned

    if dirty:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        print('Fixed:', os.path.basename(path))

print('Done.')
