import sys
import re

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('class="code-block-visual')
if start != -1:
    print("Code block visual HTML:")
    print(html[start-30:start+1200])

# Find headings and tags
for h in re.finditer(r'<h2[^>]*>(.*?)</h2>', html):
    print("H2:", h.group(0))

for btn in re.finditer(r'<(?:button|a)[^>]*class="[^"]*(?:btn|badge|status)[^"]*"[^>]*>(.*?)</(?:button|a)>', html):
    print("Btn/Badge:", btn.group(0)[:120])
