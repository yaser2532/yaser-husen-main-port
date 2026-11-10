with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    js = f.read()

pos = js.find('isHoveringReadable')
if pos == -1:
    pos = js.find('READABLE_TAGS')
if pos != -1:
    print(js[pos-50:pos+800])
