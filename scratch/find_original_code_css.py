import subprocess

res = subprocess.run(['git', 'show', 'fa22bb3:assets/css/style.css'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
css = res.stdout

lines = css.splitlines()
for i, l in enumerate(lines):
    if 'code-block-visual' in l or 'about-visual' in l:
        print(f"--- Line {i} ---")
        for j in range(max(0, i-5), min(len(lines), i+40)):
            print(f"{j}: {lines[j]}")
        break
