import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/hover-system.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for j in range(70, min(len(lines), 118)):
    print(f"{j+1}: {lines[j]}", end="")
