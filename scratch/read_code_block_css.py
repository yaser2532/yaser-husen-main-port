with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

start = css.find('.code-block-visual')
if start != -1:
    print("Code block CSS:")
    print(css[start:start+1800])
