with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re

for line in js.splitlines()[:60]:
    if 'THEME' in line or 'PALETTE' in line:
        print(line)

pos = js.find('const THEME')
if pos != -1:
    print(js[pos:pos+400])

pos2 = js.find('const PALETTE')
if pos2 != -1:
    print(js[pos2:pos2+200])
