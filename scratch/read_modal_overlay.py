with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(8170, min(len(lines), 8215)):
    print(f"{i+1}: {lines[i].strip()}")
