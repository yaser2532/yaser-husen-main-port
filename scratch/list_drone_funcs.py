with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', text)
print("Functions in drones.js:")
print(matches)
