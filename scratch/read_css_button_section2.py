with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(10345, min(len(lines), 10400)):
    print(f"{i+1}: {repr(lines[i])}")
