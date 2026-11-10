import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('isOverText')
while idx != -1:
    print(text[idx-50:idx+250])
    print('---')
    idx = text.find('isOverText', idx+10)
