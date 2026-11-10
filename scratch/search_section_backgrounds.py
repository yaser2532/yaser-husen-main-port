import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    style_css = f.read()

with open('assets/css/drones.css', 'r', encoding='utf-8') as f:
    drones_css = f.read()

# Let's search for rules affecting #home or header or #profile-expertise or section
for name, css in [('style.css', style_css), ('drones.css', drones_css)]:
    print(f"\n=== Searching in {name} ===")
    for line_num, line in enumerate(css.splitlines()):
        if any(k in line for k in ['header', '#home', '#profile-expertise', 'hero-transition-seam']):
            if '{' in line or ':' in line:
                print(f"Line {line_num+1}: {line.strip()[:100]}")
