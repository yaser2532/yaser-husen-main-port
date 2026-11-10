with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

pos = css.find('.contact-form')
if pos != -1:
    print(css[pos:pos+800])
