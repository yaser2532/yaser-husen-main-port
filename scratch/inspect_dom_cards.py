from bs4 import BeautifulSoup

with open('index.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

card_classes = ['project-card', 'expertise-card', 'cert-card', 'hero-about-tile', 'stat-card', 'code-block-visual']

for cc in card_classes:
    els = soup.select(f'.{cc}')
    print(f"\n=== .{cc} (found {len(els)}) ===")
    if els:
        el = els[0]
        children = [f"{c.name}.{'.'.join(c.get('class', []))}" for c in el.find_all(recursive=False)]
        print("Direct children:", children)
        # also print deeper interesting elements
        tags = [f"{c.name}.{'.'.join(c.get('class', []))}" for c in el.find_all(['img', 'h3', 'h4', 'span', 'p', 'a', 'div', 'button']) if c.get('class')]
        print("Sample inner tagged elements:", tags[:8])
