with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

lines = css.splitlines()
print("\n".join(lines[-40:]))
