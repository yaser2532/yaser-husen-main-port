import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

card_classes = ['project-card', 'expertise-card', 'cert-card', 'hero-about-tile', 'stat-card', 'code-block-visual']

for cc in card_classes:
    m = re.search(r'(<div[^>]*class="[^"]*' + cc + r'[^"]*"[^>]*>[\s\S]*?</div>)', html)
    print(f"\n=== .{cc} ===")
    if m:
        snippet = m.group(1)[:300]
        print(snippet.encode('ascii', 'replace').decode('ascii'))
