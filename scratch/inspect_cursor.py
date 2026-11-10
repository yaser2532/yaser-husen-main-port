with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find("let targetCursorX")
print("targetCursorX at", pos)
print(text[pos:pos+600])
