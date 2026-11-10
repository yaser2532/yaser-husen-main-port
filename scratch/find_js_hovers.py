with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re

for line in js.splitlines():
    if 'hover' in line.lower() and ('text' in line.lower() or 'cursor' in line.lower() or 'dim' in line.lower()):
        print(line.strip())
