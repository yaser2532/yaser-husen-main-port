with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(2870, min(len(lines), 2930)):
    print(f"{i+1}: {lines[i].encode('ascii', 'replace').decode('ascii').strip()}")
