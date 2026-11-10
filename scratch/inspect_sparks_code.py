with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    js = f.read()

pos = js.find('function createWeldingSparks')
if pos != -1:
    print(js[pos:pos+600])

pos2 = js.find('function createPulseRing')
if pos2 != -1:
    print(js[pos2:pos2+600])
