import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    text = f.read()

media_queries = re.findall(r'@media[^{]+\{', text)
print(f'Total media queries in style.css: {len(media_queries)}')
for mq in set(media_queries):
    print(' ', mq.strip())
