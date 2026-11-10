with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos_const = c.find("this.trail = [];")
pos_uf_end = c.find("updateFlight(now, dt)")
pos_ufl_end = c.find("updatePull(now, dt)")
pos_up_end = c.find("draw(ctx) {")
pos_draw_end = c.find("// Outer vivid neon firefly halo")

print("--- CONSTRUCTOR SNIPPET ---")
print(c[pos_const-100:pos_const+250])

print("--- UPDATE FOLLOW END SNIPPET ---")
print(c[pos_uf_end-350:pos_uf_end])

print("--- UPDATE FLIGHT END SNIPPET ---")
print(c[pos_ufl_end-250:pos_ufl_end])

print("--- UPDATE PULL & PUSH TRAIL SNIPPET ---")
print(c[pos_up_end-350:pos_up_end])

print("--- DRAW TAIL SNIPPET ---")
print(c[pos_up_end:pos_draw_end])
