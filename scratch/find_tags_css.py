with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re
matches = re.findall(r'(\.[a-zA-Z0-9_-]*(?:tag|badge|pill|tech|card)[a-zA-Z0-9_-]*\s*\{[^}]+\})', css)
print("Count of tag/badge/tech/card selectors:", len(matches))
for m in matches[:15]:
    print(m[:120])
    print("---")
