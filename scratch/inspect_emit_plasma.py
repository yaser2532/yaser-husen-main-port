with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    js = f.read()

pos = js.find('function emitPlasmaSparks')
if pos != -1:
    print(js[pos:pos+700])
