from pathlib import Path
import sys, re
root = Path(r'D:\lmy-graduate\workspace\docs\mynotes\tmp\pdfs\extracted')
stem = sys.argv[1]
for p in sys.argv[2:]:
    path = root / f'{stem}__p{int(p):02d}.txt'
    s = path.read_text(encoding='utf-8')
    s = re.sub(r'[ \t]{2,}', ' ', s)
    s = re.sub(r'\n{3,}', '\n\n', s)
    print(f'\n===== {stem} PAGE {p} =====\n{s}')
