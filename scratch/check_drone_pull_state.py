import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    js = f.read()

pos = js.find("case 'PULL'")
if pos == -1:
    pos = js.find("state === 'PULL'")
if pos != -1:
    print(js[pos-100:pos+800])
else:
    print("PULL state check not found, searching...")
