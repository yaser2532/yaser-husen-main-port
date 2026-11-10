with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re

for line in css.splitlines():
    if 'glitch' in line.lower() and ':hover' in line.lower():
        print(line[:120])
