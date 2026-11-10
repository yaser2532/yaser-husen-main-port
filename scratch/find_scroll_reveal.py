with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'scroll-reveal' in l:
        print(f"{i+1}: {l.strip()[:80]}")
