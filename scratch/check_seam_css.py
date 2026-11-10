import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/css/drones.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '.hero-transition-seam' in line:
        for j in range(max(0, i-2), min(len(lines), i+35)):
            print(f"{j+1}: {lines[j].rstrip()}")
        break
