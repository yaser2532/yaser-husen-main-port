with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(780, min(len(lines), 815)):
    print(f"{i+1}: {lines[i].strip()}")
