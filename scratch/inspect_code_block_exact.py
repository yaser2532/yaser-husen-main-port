with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

pos1 = css.find('.code-block-visual')
pos2 = css.find('.project-filters')

print("Code block section length:", pos2 - pos1)
print(css[pos1:pos2])
