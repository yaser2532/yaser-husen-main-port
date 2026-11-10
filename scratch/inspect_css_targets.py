with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re

for selector in ['.section-title', '.filter-btn', '.project-card', '.contact', '.about-stat', '.bday-btn']:
    pos = css.find(selector)
    if pos != -1:
        print(f"=== {selector} ===")
        print(css[pos:pos+500])
        print("...")
