import re

for filename in ['assets/js/script.js', 'assets/js/drones.js', 'assets/js/react-3d-cards.js']:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error opening {filename}: {e}")
        continue
    print(f"=== {filename} ===")
    lines = content.split('\n')
    for idx, line in enumerate(lines):
        if 'scroll' in line.lower() and ('addeventlistener' in line.lower() or 'onscroll' in line.lower() or 'scrolltop' in line.lower() or 'scrollby' in line.lower() or 'scrollto' in line.lower()):
            print(f"Line {idx+1}: {line.strip()[:100]}")
