import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    text = f.read()

for sel in ['header', 'main', '.page-body-content', '#profile-expertise', '.hero-details', '.hero-actions']:
    pattern = re.compile(rf'(?:^|\n)\s*({re.escape(sel)}[^{{]*\{{[^}}]*\}})', re.DOTALL)
    for m in pattern.finditer(text):
        rule = m.group(1)
        if any(w in rule for w in ['border', 'shadow', 'line', 'hr', 'background', 'black', '#000']):
            clean = '\n'.join([l.strip() for l in rule.splitlines() if l.strip()])
            print(f"=== Rule for {sel} ===")
            print(clean)
