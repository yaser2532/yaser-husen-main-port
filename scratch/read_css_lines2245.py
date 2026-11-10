with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(2245, 2256):
    print(f"{i+1}: {repr(lines[i])}")
