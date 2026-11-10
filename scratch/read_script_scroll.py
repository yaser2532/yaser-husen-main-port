with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for start in [2868, 7878, 8700]:
    print(f"\n--- Line {start} ---")
    for i in range(start, min(len(lines), start + 30)):
        print(f"{i+1}: {lines[i].encode('ascii', 'replace').decode('ascii').strip()}")
