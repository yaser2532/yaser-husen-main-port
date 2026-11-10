with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(964, min(len(lines), 1025)):
    line_clean = lines[i].encode('ascii', 'replace').decode('ascii').strip()
    print(f"{i+1}: {line_clean}")
