with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'expertise-card' in line:
        for j in range(i, min(len(lines), i+30)):
            print(f"{j+1}: {lines[j].encode('ascii', 'replace').decode('ascii').strip()}")
        break
