with open('assets/js/gl-engine.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(275, min(len(lines), 310)):
    print(f"{i+1}: {lines[i].encode('ascii', 'replace').decode('ascii').strip()}")
