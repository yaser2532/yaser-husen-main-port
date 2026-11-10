with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos1 = html.find('class="hero-kinetic-row"')
pos2 = html.find('</h1>', pos1)
print("=== index.html kinetic row ===")
print(repr(html[pos1-20:pos2]))

with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

pos = js.find('clock-utc')
print("=== script.js clock code ===")
print(repr(js[pos-100:pos+350]))
