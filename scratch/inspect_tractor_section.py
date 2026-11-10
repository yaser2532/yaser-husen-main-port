import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos_tb = c.find("function drawTractorBeams(ctx) {")
pos_wd = c.find("function revealAllInstantly()")

print("--- TRACTOR BEAMS SECTION ---")
print(c[pos_tb:pos_wd])
