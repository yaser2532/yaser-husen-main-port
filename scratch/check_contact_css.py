with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

pos = css.find('.contact-grid')
if pos != -1:
    print(css[pos:pos+1200])
