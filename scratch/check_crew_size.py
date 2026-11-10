import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    js = f.read()

pos = js.find('CREW_SIZE')
if pos != -1:
    print(js[pos-100:pos+500])
