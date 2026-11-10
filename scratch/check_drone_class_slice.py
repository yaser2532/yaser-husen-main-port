import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx_class = text.find('class Drone {')
idx_pool = text.find('const drones = [];', idx_class)
print("=== Drone class slice ===")
print(text[idx_class:idx_class+800])
print("...")
print(text[idx_pool-400:idx_pool+100])
