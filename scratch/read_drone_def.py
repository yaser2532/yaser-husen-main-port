import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('pushTrail() {')
if idx == -1:
    idx = text.find('pushTrail')
print(text[idx-50:idx+600])

idx_d = text.find('function drawDrone')
print('\n=== drawDrone ===')
print(text[idx_d:idx_d+1000])
