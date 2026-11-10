with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos1 = text.find("window.addEventListener('mousemove'")
print("mousemove snippet:")
print(text[pos1:pos1+300])

pos2 = text.find("class Drone")
pos3 = text.find("function startLoop")
print("\nDrone class snippet (start):")
print(text[pos2:pos2+400])

pos_draw = text.find("draw(ctx) {", pos2)
print("\nDrone draw(ctx) snippet:")
print(text[pos_draw:pos_draw+600])
