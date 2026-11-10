with open("assets/css/style.css", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Find rules for card hover and pseudo elements
patterns = [
    r'(\.project-card|\.cp-3d-card|\.expertise-card|\.cert-card|\.glass-card|\.stat-card)[^{}]*(?:::before|::after|\:hover)[^{}]*\{[^}]*\}',
]

for p in patterns:
    matches = list(re.finditer(p, text))
    print(f"Pattern {p} matches: {len(matches)}")
    for m in matches[-15:]:  # print last 15
        snippet = m.group(0).replace('\n', ' ')
        print("  ->", snippet[:130])
