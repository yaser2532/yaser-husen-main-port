with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'SECTION_ORDER\s*=\s*\[[^\]]+\]', text)
print(matches)
