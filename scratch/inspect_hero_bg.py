import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('cosmic-bg-container')
if idx != -1:
    print('=== cosmic-bg-container context ===')
    print(text[idx-50:idx+400])

idx_home = text.find('<header id="home"')
if idx_home != -1:
    idx_prof = text.find('id="profile-expertise"')
    print('\n=== Between <header id="home"> and <section id="profile-expertise"> ===')
    print(text[idx_prof-400:idx_prof+150])
