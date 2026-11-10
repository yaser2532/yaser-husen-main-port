def update_drones():
    with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
        content = f.read()

    old_block = """                let type = 'card';
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
                }"""

    new_block = """                let type = 'card';
                let pullDuration = 180; // Card pull: 180ms (increased pulling speed by 0.3s)

                if (['h1', 'h2', 'h3'].includes(tag) || el.classList.contains('section-title') || el.classList.contains('section-tag')) {
                    type = 'title';
                    pullDuration = 400; // Title scanline sweep: 400ms (increased pulling speed by 0.3s)
                } else if (tag === 'p' || el.classList.contains('section-desc')) {
                    type = 'paragraph';
                    pullDuration = 250; // Paragraph line sweep: 250ms (increased pulling speed by 0.3s)
                } else if (['a', 'button'].includes(tag) || el.classList.contains('cta-button') || el.classList.contains('filter-btn') || el.classList.contains('message-btn')) {
                    type = 'button';
                    pullDuration = 150; // Button/link snap-in: 150ms (increased pulling speed by 0.3s)
                } else if (el.classList.contains('code-block-visual')) {
                    type = 'code-card';
                    pullDuration = 250; // Frame 250ms, then lines 40ms each (increased pulling speed by 0.3s)
                }"""

    assert old_block in content, "old_block not found in drones.js"
    content = content.replace(old_block, new_block)

    with open('assets/js/drones.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated drones.js pull durations (0.3s faster).")

if __name__ == '__main__':
    update_drones()
