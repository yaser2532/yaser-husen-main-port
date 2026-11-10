import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(1490, 1620):
    print(f"{i}: {lines[i]}", end='')
