import glob, re

for f in sorted(glob.glob('assets/js/*.js')):
    with open(f, 'r', encoding='utf-8', errors='ignore') as fp:
        c = fp.read()
    rafs = [c[:m.start()].count('\n')+1 for m in re.finditer(r'requestAnimationFrame', c)]
    scrolls = [c[:m.start()].count('\n')+1 for m in re.finditer(r'["\']scroll["\']', c)]
    if rafs or scrolls:
        print(f'{f}:')
        if rafs:
            print(f'   RAF at lines: {rafs}')
        if scrolls:
            print(f'   Scroll at lines: {scrolls}')
