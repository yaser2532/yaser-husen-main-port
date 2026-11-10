with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if any(k in l.lower() for k in ['modal', 'popup', 'pop-up', 'lightbox']):
        print(f"{i+1}: {l.strip()[:100].encode('ascii', 'replace').decode('ascii')}")
