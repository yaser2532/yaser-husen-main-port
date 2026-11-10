import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('pushTrail()')
if idx != -1:
    print('=== pushTrail definition ===')
    print(text[idx-100:idx+800])

idx_draw = text.find('function drawDrone')
if idx_draw != -1:
    print('=== drawDrone definition ===')
    print(text[idx_draw:idx_draw+1000])
