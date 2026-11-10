with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(8885, min(len(lines), 8930)):
    print(f"{i+1}: {lines[i].strip()}")
