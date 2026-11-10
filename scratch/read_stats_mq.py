with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for j in range(6655, 6685):
    print(f"{j+1}: {lines[j]}", end="")
