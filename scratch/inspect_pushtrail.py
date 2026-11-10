with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find("pushTrail")
while pos != -1:
    print(f"pushTrail at {pos}:")
    print(text[max(0, pos-100):pos+300])
    pos = text.find("pushTrail", pos+1)
