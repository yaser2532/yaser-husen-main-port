import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

card2_old = '''                <article class="project-card glass-card scroll-reveal fade-up" data-category="interactive">\n                    <div class="project-img-container">'''
card2_new = '''                <article class="project-card glass-card scroll-reveal fade-up" data-category="interactive">\n                    <span class="holo-sticker holo-sticker-pink">[CHAOS // 0x4A]</span>\n                    <div class="project-img-container">'''

card3_old = '''                <article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">\n                    <div class="project-img-container">'''
# Be careful: card3 is the next occurrence of project-card with ai-data after card1
if card2_old in content:
    content = content.replace(card2_old, card2_new, 1)
    print("Added sticker to card 2.")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated card 2 sticker.")
