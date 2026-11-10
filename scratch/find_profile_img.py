with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l.lower() for k in ['profile-img', 'profile-image', 'profile-card', 'profile-avatar', 'hero-image', 'avatar']):
        print(f"Line {i+1}: {l.strip()[:100]}")
