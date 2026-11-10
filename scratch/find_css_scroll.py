with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l.lower() for k in ['scroll-behavior', 'smooth-scroll', 'overscroll', 'overflow-y', 'scroll-snap']):
        print(f"Line {i+1}: {l.strip()[:100]}")
