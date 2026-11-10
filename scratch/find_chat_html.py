with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = re.findall(r'<div[^>]*id=["\'][^"\']*chat[^"\']*["\'][^>]*>[\s\S]*?</div>', html, re.IGNORECASE)
for m in matches:
    print("Found in index.html:", m[:300].encode('ascii', 'replace').decode('ascii'))

# Also search for nano-chat in index.html
for m in re.finditer(r'nano-chat', html):
    start = max(0, m.start() - 100)
    end = min(len(html), m.end() + 200)
    print("nano-chat context in HTML:\n", html[start:end].encode('ascii', 'replace').decode('ascii'))
    break
