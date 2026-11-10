with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re

for line in js.splitlines():
    if 'sparks' in line.lower() or 'pulsering' in line.lower() or 'arc' in line.lower():
        print(line[:100])
