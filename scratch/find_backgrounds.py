import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('=== Canvases in index.html ===')
for m in re.finditer(r'<canvas[^>]*>', text):
    print('  ', m.group(0))

print('\n=== Background / Hero structure in index.html ===')
for m in re.finditer(r'<(?:header|section|div)[^>]*id=[\'"]([^\'"]+)[\'"][^>]*>', text):
    tag = m.group(0)
    if any(k in tag for k in ['home', 'hero', 'profile', 'canvas', 'star', 'bg', 'background', 'seam']):
        print('  ', tag[:120])
