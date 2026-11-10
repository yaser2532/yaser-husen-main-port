import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/css/drones.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(120, len(lines)):
    l = lines[i].rstrip('\r\n')
    if l:
        print(f"{i+1}: {l}")
