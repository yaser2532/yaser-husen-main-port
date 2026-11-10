import subprocess

res = subprocess.run(['git', 'show', 'e0a091d'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
diff = res.stdout

for line in diff.splitlines():
    if ':hover' in line or 'hero' in line.lower():
        if len(line.strip()) < 120 and ('+' in line[:2] or '-' in line[:2]):
            print(line.strip())
