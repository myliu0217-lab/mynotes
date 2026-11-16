from pathlib import Path
import json
from pypdf import PdfReader

root = Path(r'D:\lmy-graduate\workspace\docs\mynotes')
src = root / 'literature'
out = root / 'tmp' / 'pdfs' / 'extracted'
out.mkdir(parents=True, exist_ok=True)
records = []
for path in sorted(src.glob('*.pdf')):
    rec = {'file': path.name, 'bytes': path.stat().st_size}
    try:
        reader = PdfReader(str(path), strict=False)
        rec['pages'] = len(reader.pages)
        rec['metadata_title'] = str(reader.metadata.title or '') if reader.metadata else ''
        texts = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text(extraction_mode='layout') or ''
            texts.append(text)
            (out / f'{path.stem}__p{i+1:02d}.txt').write_text(text, encoding='utf-8')
        rec['page_chars'] = [len(t) for t in texts]
        rec['first_page'] = texts[0][:1200] if texts else ''
        rec['last_page'] = texts[-1][-1000:] if texts else ''
    except Exception as exc:
        rec['error'] = repr(exc)
    records.append(rec)
(out / 'manifest.json').write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding='utf-8')
for rec in records:
    print(json.dumps({k:rec.get(k) for k in ['file','bytes','pages','metadata_title','page_chars','error'] if k in rec}, ensure_ascii=False))
