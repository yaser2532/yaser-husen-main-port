with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

pos1 = css.find('.code-block-visual {')
print(repr(css[pos1-120:pos1]))
