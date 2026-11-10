with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(3410, min(len(lines), 3460)):
    print(f"{i+1}: {lines[i].encode('ascii', 'replace').decode('ascii').strip()}")
