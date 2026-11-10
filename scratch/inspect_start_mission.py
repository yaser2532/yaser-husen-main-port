import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos_sm = c.find("function startMission(item) {")
pos_am = c.find("function updateActiveMissions(now, dt)")

print("--- START MISSION SNIPPET ---")
print(c[pos_sm:pos_am])
