with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'lampArm', text)]
for idx in matches:
    print(text[idx-40:idx+300])
    print('='*40)
