with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    c = f.read()

pos_uf = c.find("updateFollow(now, dt)")
pos_ufl = c.find("updateFlight(now, dt)")
pos_up = c.find("updatePull(now, dt)")
pos_pt = c.find("pushTrail() {")
pos_draw = c.find("draw(ctx) {")
pos_next = c.find("// Outer vivid neon firefly halo", pos_draw)

print("--- updateFollow tail ---")
print(c[pos_ufl-400:pos_ufl])

print("--- updateFlight tail ---")
print(c[pos_up-400:pos_up])

print("--- updatePull tail & pushTrail ---")
print(c[pos_pt-200:pos_draw])

print("--- draw(ctx) tail drawing ---")
print(c[pos_draw:pos_next])
