with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    js = f.read()

pos = js.find('// If an element is within the active viewport')
if pos != -1:
    print(js[pos-200:pos+800])
