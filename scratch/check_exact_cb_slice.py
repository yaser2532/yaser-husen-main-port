with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

pos1 = css.find('.code-block-visual {')
pos2 = css.find('.project-filters {')
print(f"pos1={pos1}, pos2={pos2}")
print(repr(css[pos1:pos1+200]))
