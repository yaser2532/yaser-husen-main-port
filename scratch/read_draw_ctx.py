import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('draw(ctx) {')
print(text[idx:idx+1500])
