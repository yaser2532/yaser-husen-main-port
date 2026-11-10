with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

replacements = [
    ('<a href="https://aeea-web-eight.vercel.app/" class="project-link has-text" target="_blank">',
     '<a href="https://aeea-web-eight.vercel.app/" class="project-link has-text" target="_blank" rel="noopener noreferrer">'),
    ('<a href="https://amlt-demo-simulator-ov6a.vercel.app/" class="project-link has-text" target="_blank">',
     '<a href="https://amlt-demo-simulator-ov6a.vercel.app/" class="project-link has-text" target="_blank" rel="noopener noreferrer">'),
    ('<a href="https://attf-data-cleaning-platform.vercel.app/" class="project-link has-text" target="_blank">',
     '<a href="https://attf-data-cleaning-platform.vercel.app/" class="project-link has-text" target="_blank" rel="noopener noreferrer">'),
    ('<a href="https://gympro-for-bros.netlify.app/" class="project-link" target="_blank">',
     '<a href="https://gympro-for-bros.netlify.app/" class="project-link" target="_blank" rel="noopener noreferrer">'),
    ('<a href="https://github.com/yaser2532" target="_blank" aria-label="GitHub">',
     '<a href="https://github.com/yaser2532" target="_blank" rel="noopener noreferrer" aria-label="GitHub">'),
    ('<a href="https://www.linkedin.com/in/yaser-husen-154a80378/" target="_blank" aria-label="LinkedIn">',
     '<a href="https://www.linkedin.com/in/yaser-husen-154a80378/" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">'),
    ('<a href="https://x.com/husen_yase85815" target="_blank" aria-label="Twitter/X">',
     '<a href="https://x.com/husen_yase85815" target="_blank" rel="noopener noreferrer" aria-label="Twitter/X">')
]

for old, new in replacements:
    assert old in content, f"Missing: {old}"
    content = content.replace(old, new)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated all target='_blank' links with rel='noopener noreferrer'!")
