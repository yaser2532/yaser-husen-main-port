import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    text = f.read()

for selector in ['stats-row', 'stat-card', 'cakeCanvas', 'bday-card', 'hero-details-container', 'filter-buttons', 'project-card']:
    matches = [m.start() for m in re.finditer(re.escape(selector), text)]
    print(f"Selector '{selector}': found {len(matches)} occurrences")
    for pos in matches[:2]:
        start = max(0, pos - 40)
        end = min(len(text), pos + 250)
        print(f"  Snippet: {text[start:end].replace('\n', ' ')}\n")
