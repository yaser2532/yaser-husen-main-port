with open("assets/css/style.css", "r", encoding="utf-8") as f:
    text = f.read()

import re
print("--- #home CSS ---")
for m in re.finditer(r'(?:header\b|#home\b|\.hero\b)[^{]*\{[^}]+\}', text):
    if any(k in m.group(0) for k in ['fixed', 'sticky', 'z-index', 'position', 'height']):
        print(m.group(0)[:150])
        print('-'*30)
