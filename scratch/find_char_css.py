with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'hero-3d-char' in l or 'is-repelled' in l:
        print(f"Line {i+1}: {l.strip()[:100]}")
