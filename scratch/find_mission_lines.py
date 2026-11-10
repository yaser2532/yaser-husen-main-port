with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    js = f.read()

for i, line in enumerate(js.splitlines()):
    if 'mission' in line.lower() or 'dispatch' in line.lower() or 'startpull' in line.lower():
        print(f"{i}: {line[:100]}")
