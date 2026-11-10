with open('assets/js/hover-system.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(74, min(len(lines), 95)):
    print(f"{i+1}: {lines[i].strip()}")
