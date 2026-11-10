import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

cards = re.findall(r'<article class="project-card.*?</article>', text, re.DOTALL)
for idx, c in enumerate(cards):
    title = re.search(r'<h3>(.*?)</h3>', c)
    t = title.group(1) if title else 'No title'
    print(f"--- CARD {idx+1}: {t} ---")
    header = c[:250].strip()
    print("TOP:", header.replace('\n', ' '))
