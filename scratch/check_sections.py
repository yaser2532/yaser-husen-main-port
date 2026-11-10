with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Check mousemove block
pos_mm = c.find("window.addEventListener('mousemove'")
print("--- MOUSEMOVE ---")
print(c[pos_mm:pos_mm+400])

# Check constructor
pos_d = c.find("class Drone")
print("--- CONSTRUCTOR ---")
print(c[pos_d:pos_d+800])
