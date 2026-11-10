with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function handleNavbarScroll' in l:
        for j in range(i, min(len(lines), i+30)):
            print(f"{j+1}: {lines[j].encode('ascii', 'replace').decode('ascii').strip()}")
        break
