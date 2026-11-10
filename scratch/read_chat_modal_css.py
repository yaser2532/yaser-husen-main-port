with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(8210, min(len(lines), 8255)):
    print(f"{i+1}: {lines[i].strip()}")
