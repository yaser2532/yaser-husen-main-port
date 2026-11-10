with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('assets/vendor/three/three.min.js')
if pos != -1:
    print(text[pos-40:pos+800])
