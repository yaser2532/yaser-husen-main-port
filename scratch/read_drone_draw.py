import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('pushTrail')
if idx != -1:
    print('=== pushTrail and draw ===')
    print(text[idx-200:idx+1200])

idx_draw = text.find('function drawDrone(')
if idx_draw != -1:
    print('=== drawDrone ===')
    print(text[idx_draw:idx_draw+1400])
