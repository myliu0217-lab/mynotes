from pathlib import Path
import sys, re
root = Path(r'D:\lmy-graduate\workspace\docs\mynotes\tmp\pdfs\extracted')
stem = sys.argv[1]
words = sys.argv[2:] or ['circuit','noise','multiplex','crosstalk','in vivo','Fig.']
for path in sorted(root.glob(f'{stem}__p*.txt')):
    text = path.read_text(encoding='utf-8')
    hits = [w for w in words if re.search(re.escape(w), text, re.I)]
    if hits:
        print(path.stem[-3:], ', '.join(hits))
