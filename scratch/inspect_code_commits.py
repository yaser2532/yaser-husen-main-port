import subprocess

commits = ['10f5401', 'e2a94b8', '5513a9f', 'd338f4e', 'fa22bb3']
for c in commits:
    res = subprocess.run(['git', 'show', f'{c}:assets/css/style.css'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
    css = res.stdout
    lines = css.splitlines()
    for i, l in enumerate(lines):
        if '.code-block-visual' in l:
            print(f"=== Commit {c} ===")
            for j in range(i, min(len(lines), i+30)):
                print(lines[j])
            break
