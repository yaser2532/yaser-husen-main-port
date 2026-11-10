with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

start = css.find('.terminal-badge')
if start != -1:
    print(css[start:start+1800])
