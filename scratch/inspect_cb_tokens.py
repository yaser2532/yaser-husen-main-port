with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

pos1 = css.find('.code-line-num {')
pos2 = css.find('/* ==========================================================================\n\n   Projects Section')
print(css[pos1:pos2])
