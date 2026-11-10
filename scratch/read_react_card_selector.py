with open('assets/js/react-3d-cards.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(25, 36):
    print(f"{i+1}: {repr(lines[i])}")
