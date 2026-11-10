with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

pos2 = css.find('.project-filters {')
print(repr(css[pos2-150:pos2]))
