with open('assets/js/react-3d-cards.js', 'r', encoding='utf-8') as f:
    code = f.read()

target = "const CARD_SELECTOR = '.project-card, .cert-card, .expertise-card, .onboard-card, .stat-card, .glass-card, .bday-card, .code-block-visual, .hero-about-tile, .contact-card, .profile-card-wrapper, .nano-chat-card, .cyber-dock-bar';"
replacement = "const CARD_SELECTOR = '.project-card, .cert-card, .expertise-card, .onboard-card, .stat-card, .glass-card, .bday-card, .code-block-visual, .hero-about-tile, .contact-card, .nano-chat-card, .cyber-dock-bar';"

if target in code:
    code = code.replace(target, replacement)
    with open('assets/js/react-3d-cards.js', 'w', encoding='utf-8') as f:
        f.write(code)
    print("SUCCESS: Removed .profile-card-wrapper from react-3d-cards.js CARD_SELECTOR")
else:
    print("Warning: target not found in react-3d-cards.js")
