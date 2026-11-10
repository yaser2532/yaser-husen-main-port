import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'function closeNavDrawer()' in l:
        for j in range(max(0, i - 5), min(len(lines), i + 45)):
            print(f"{j+1}: {lines[j]}", end="")
        break
