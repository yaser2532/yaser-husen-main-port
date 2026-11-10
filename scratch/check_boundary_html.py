import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

idx_home = html.find('id="home"')
idx_prof = html.find('id="profile-expertise"')

print("HTML between home and profile-expertise:")
print(html[idx_home+len('id="home"'):idx_prof])
