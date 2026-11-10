import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for j in range(7544, min(len(lines), 7680)):
    print(f"{j+1}: {lines[j]}", end="")
