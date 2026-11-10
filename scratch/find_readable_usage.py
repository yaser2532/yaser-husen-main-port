with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    js = f.read()

pos = js.find('READABLE_TAGS.has')
if pos != -1:
    print(js[pos-100:pos+600])
