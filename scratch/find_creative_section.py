with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('id="creative-lab"')
if pos != -1:
    print(text[pos-40:pos+1500])
