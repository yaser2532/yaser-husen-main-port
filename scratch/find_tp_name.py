import glob

files = glob.glob('assets/**/*.js', recursive=True) + glob.glob('assets/**/*.css', recursive=True)

for fpath in files:
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    if '#tp-name' in text or 'tp-name' in text:
        print(f"=== {fpath} ===")
        for i, l in enumerate(text.split('\n')):
            if 'tp-name' in l:
                print(f"  {i+1}: {l.strip()[:100]}")
