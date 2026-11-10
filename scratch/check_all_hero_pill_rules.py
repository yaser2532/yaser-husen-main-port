with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re

for line in css.splitlines():
    if 'hero-clock-pill' in line or 'hero-sticker-badge' in line or 'hero-spec-stamp' in line:
        print(line[:120])
