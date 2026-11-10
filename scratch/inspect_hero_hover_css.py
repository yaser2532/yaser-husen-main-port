with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

import re

hero_selectors = [
    'hero-clock-pill', 'hero-sticker-badge', 'hero-spec-stamp',
    'hero-about-tile', 'trait-tag', 'hero-subtitle', 'hero-title'
]

for s in hero_selectors:
    for m in re.finditer(rf'(\.{s}[^{{]*\{{[^}}]+\}})', css):
        print(f"=== Rule for {s} ===")
        print(m.group(0))
    # Check hover rules
    for m in re.finditer(rf'(\.{s}:hover[^{{]*\{{[^}}]+\}})', css):
        print(f"=== Hover for {s} ===")
        print(m.group(0))
