import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos_sparks = c.find("const sparks = [];")
pos_missions = c.find("const SECTION_ORDER")

print("--- SPARKS SECTION ---")
print(c[pos_sparks:pos_missions])
