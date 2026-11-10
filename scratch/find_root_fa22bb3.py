import subprocess

res = subprocess.run(['git', 'show', 'fa22bb3:assets/css/style.css'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
css = res.stdout

lines = css.splitlines()
for i, l in enumerate(lines[:60]):
    print(f"{i}: {l}")
