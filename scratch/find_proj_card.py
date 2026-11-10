with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'project-card' in line:
        print(f"{i+1}: {line.strip()[:100]}")
        for j in range(i+1, min(len(lines), i+25)):
            print(f"  {lines[j].strip()[:100]}")
        break
