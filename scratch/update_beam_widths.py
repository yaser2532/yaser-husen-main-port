with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\r\n', '\n')
text = text.replace('ctx.lineWidth = 3.2;', 'ctx.lineWidth = 1.6;')
text = text.replace('ctx.lineWidth = 1.8;', 'ctx.lineWidth = 0.9;')
text = text.replace('ctx.lineWidth = 1.0;\n                ctx.shadowColor = THEME.gold;', 'ctx.lineWidth = 0.5;\n                ctx.shadowColor = THEME.gold;')

with open('assets/js/drones.js', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text)

print("Updated beam line widths.")
