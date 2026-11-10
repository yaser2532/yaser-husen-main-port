with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos = html.find('drone-code-line')
if pos != -1:
    print(repr(html[pos:pos+300]))
