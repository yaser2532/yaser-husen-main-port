import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'createStarfield\([^\)]*\)', text):
    print(m.group(0))
