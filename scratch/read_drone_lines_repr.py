with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(782, 803):
    print(f"{i+1}: {repr(lines[i])}")
