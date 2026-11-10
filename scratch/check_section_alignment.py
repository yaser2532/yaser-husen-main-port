with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
headers = re.findall(r'(\.section-[a-zA-Z0-9_-]+\s*\{[^}]+\})', css)
for h in headers[:10]:
    print(h)
