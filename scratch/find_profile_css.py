with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l for k in ['.profile-card-wrapper', '.profile-details-img', '.profile-showcase', '.profile-card-glow']):
        print(f"Line {i+1}: {l.strip()[:100]}")
