import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    text = f.read()

for query in ['SCROLL_SETTLE_MS', 'lastFastScrollTime', 'currentScrollSpeed', 'finishElementInstantly']:
    idx = text.find(query)
    while idx != -1:
        print(f"=== Match for {query} ===")
        print(text[max(0, idx-50):min(len(text), idx+200)])
        idx = text.find(query, idx+len(query)+20)
