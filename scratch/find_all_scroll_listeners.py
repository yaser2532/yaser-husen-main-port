import glob, re

files = glob.glob('assets/**/*.js', recursive=True)

for fpath in files:
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    if 'scroll' in text.lower():
        print(f"\n=== {fpath} ===")
        for i, l in enumerate(text.split('\n')):
            if any(k in l.lower() for k in ['addeventlistener(\'scroll\'', 'addeventlistener("scroll"', 'scrolltop', 'scrollto', 'scrollby', 'scrollintoview', 'wheel', 'smoothscroll']):
                print(f"  {i+1}: {l.strip()[:100]}")
