with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'setupHero3dNamePhysics' in l:
        for j in range(i, min(len(lines), i+80)):
            print(f"{j+1}: {lines[j].encode('ascii', 'replace').decode('ascii').strip()}")
        break
