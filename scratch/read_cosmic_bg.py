import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function initCosmicBackground')
if idx != -1:
    print('=== initCosmicBackground ===')
    print(text[idx:idx+2500])
