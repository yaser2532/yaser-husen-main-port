with open("assets/js/script.js", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'filter-btn', text)]
print(f"Found {len(matches)} occurrences in script.js")
for idx in matches:
    print(text[max(0, idx-40):min(len(text), idx+200)])
    print("=" * 40)
