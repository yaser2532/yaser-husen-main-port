with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    code = f.read()

bad_line = "secret: '✨ SECRET FOUND: \"You discovered Yaser Husen's hidden cyber vault!\"'"
good_line = 'secret: "✨ SECRET FOUND: \\"You discovered Yaser Husen\'s hidden cyber vault!\\""'

assert bad_line in code, "bad_line not found"
code = code.replace(bad_line, good_line)

with open('assets/js/script.js', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(code.replace('\r\n', '\n').replace('\n', '\r\n'))

print("Fixed unescaped quote in assets/js/script.js!")

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = css.replace(
    ".torn-paper-sticker {\n    position: absolute;",
    ".torn-paper-sticker {\n    position: absolute;\n    pointer-events: auto !important;"
)

with open('assets/css/style.css', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(css.replace('\r\n', '\n').replace('\n', '\r\n'))

print("Added pointer-events: auto to .torn-paper-sticker!")
