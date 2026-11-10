import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx_class = text.find('class Drone {')
idx_pool = text.find('const drones = [];', idx_class)
lines = text[idx_class:idx_pool].splitlines()
for i, l in enumerate(lines):
    if l.strip():
        print(f"{i+1}: {l.strip()}")
