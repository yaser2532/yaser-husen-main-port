import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos1 = html.find('<pre class="terminal-pre">')
pos2 = html.find('</pre>', pos1)
print(html[pos1:pos2+6])
