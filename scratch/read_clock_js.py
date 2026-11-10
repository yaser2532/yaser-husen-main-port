with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

pos = js.find('clock-utc')
if pos != -1:
    print(js[pos-100:pos+500])
