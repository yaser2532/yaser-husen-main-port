with open("assets/js/script.js", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find('filterButtons.forEach')
print(text[idx:idx+600])
