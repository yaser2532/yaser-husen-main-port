import re
with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()
ids = re.findall(r'<section[^>]*id=["\']([^"\']+)["\']', c)
print('Section IDs in index.html:', ids)
all_ids = re.findall(r'id=["\']([^"\']+)["\']', c)
for sec in ['home', 'profile-expertise', 'about-me', 'about', 'skills', 'projects', 'creative-lab', 'certificates', 'secret-desk', 'contact']:
    print(f"Exists '{sec}':", sec in all_ids)
