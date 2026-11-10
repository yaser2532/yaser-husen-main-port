with open('assets/css/drones.css', 'r', encoding='utf-8') as f:
    css = f.read()

print(css[css.find('.code-block-visual'):css.find('.code-block-visual')+600])
