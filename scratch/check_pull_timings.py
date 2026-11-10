with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    js = f.read()

import re

for line in js.splitlines():
    if 'minDuration' in line or 'duration' in line.lower() or 'flight' in line.lower() or 'pulling' in line.lower() or 'startMission' in line:
        if len(line.strip()) < 120:
            print(line.strip())
