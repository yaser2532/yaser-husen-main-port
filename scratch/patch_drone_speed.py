with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    content = f.read()

old_block = '''            sorted.forEach((el, order) => {
                const tag = el.tagName.toLowerCase();
                let type = 'card';
                let pullDuration = 680; // Card pull: 680ms (380 + 300ms)

                if (['h1', 'h2', 'h3'].includes(tag) || el.classList.contains('section-title') || el.classList.contains('section-tag')) {
                    type = 'title';
                    pullDuration = 1000; // Title scanline sweep: 1000ms (700 + 300ms)
                } else if (tag === 'p' || el.classList.contains('section-desc')) {
                    type = 'paragraph';
                    pullDuration = 850; // Paragraph line sweep: 850ms (550 + 300ms)
                } else if (['a', 'button'].includes(tag) || el.classList.contains('cta-button') || el.classList.contains('filter-btn') || el.classList.contains('message-btn')) {
                    type = 'button';
                    pullDuration = 580; // Button/link snap-in: 580ms (280 + 300ms)
                } else if (el.classList.contains('code-block-visual')) {
                    type = 'code-card';
                    pullDuration = 800; // Frame 800ms (500 + 300ms), then lines paced
                }'''

new_block = '''            sorted.forEach((el, order) => {
                const tag = el.tagName.toLowerCase();
                let type = 'card';
                let pullDuration = 380; // Card pull: 380ms (increased rendering speed by 0.3s)

                if (['h1', 'h2', 'h3'].includes(tag) || el.classList.contains('section-title') || el.classList.contains('section-tag')) {
                    type = 'title';
                    pullDuration = 700; // Title scanline sweep: 700ms (increased rendering speed by 0.3s)
                } else if (tag === 'p' || el.classList.contains('section-desc')) {
                    type = 'paragraph';
                    pullDuration = 550; // Paragraph line sweep: 550ms (increased rendering speed by 0.3s)
                } else if (['a', 'button'].includes(tag) || el.classList.contains('cta-button') || el.classList.contains('filter-btn') || el.classList.contains('message-btn')) {
                    type = 'button';
                    pullDuration = 280; // Button/link snap-in: 280ms (increased rendering speed by 0.3s)
                } else if (el.classList.contains('code-block-visual')) {
                    type = 'code-card';
                    pullDuration = 500; // Frame 500ms, then lines 70ms each (increased rendering speed by 0.3s)
                }'''

assert old_block in content, 'old_block not found in drones.js'
content = content.replace(old_block, new_block, 1)

old_beat = 'if (now - lastMissionFinishTime < 90) return; // 90ms clear beat between sequential elements'
new_beat = 'if (now - lastMissionFinishTime < 60) return; // Snappy 60ms beat between sequential elements'
assert old_beat in content, 'old_beat not found in drones.js'
content = content.replace(old_beat, new_beat, 1)

with open('assets/js/drones.js', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated rendering speeds in assets/js/drones.js successfully!')
