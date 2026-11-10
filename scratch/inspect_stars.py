import sys
sys.stdout.reconfigure(encoding='utf-8')

print("=== gl-engine.js stars ===")
with open('assets/js/gl-engine.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if any(k in line for k in ['FG_STARS', 'BG_STARS', 'createStarfield', 'Starry Night', 'STARRY SKY BACKDROP']):
        start = max(0, i - 5)
        end = min(len(lines), i + 40)
        for j in range(start, end):
            print(f"{j+1}: {lines[j]}", end="")
        print("\n" + "="*50 + "\n")
        break

print("=== script.js stars ===")
with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    slines = f.readlines()
for i, line in enumerate(slines):
    if 'DYNAMIC COSMIC SPACE BACKGROUND' in line:
        start = max(0, i - 5)
        end = min(len(slines), i + 65)
        for j in range(start, end):
            print(f"{j+1}: {slines[j]}", end="")
        print("\n" + "="*50 + "\n")
        break
