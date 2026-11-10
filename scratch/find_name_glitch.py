with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l for k in ['#tp-name', '.hero-title', 'tp-name:hover', 'hero-title:hover', 'glitch']):
        if ':hover' in l or '@keyframes' in l or 'tp-name' in l:
            print(f"Line {i+1}: {l.strip()[:100]}")
