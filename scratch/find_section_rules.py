import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    text = f.read()

pattern = re.compile(r'(?:^|\n)\s*(section[^{]*\{[^}]*\})', re.DOTALL)
for m in pattern.finditer(text):
    clean = '\n'.join([line.strip() for line in m.group(1).splitlines() if line.strip()])
    print("--- Section rule ---")
    print(clean[:300])
