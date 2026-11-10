with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

pos1 = css.find('.hero-kinetic-row {')
pos2 = css.find('.hero-content .eyebrow {')
print(f"pos1={pos1}, pos2={pos2}")
print(css[pos1:pos2])
