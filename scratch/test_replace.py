with open('index.html', 'r', encoding='utf-8') as f:
    h = f.read()

pos1 = h.find('<div class="about-visual')
pos2 = h.find('<!-- Projects Section -->', pos1)

print("Block found:")
print(repr(h[pos1:pos2]))
