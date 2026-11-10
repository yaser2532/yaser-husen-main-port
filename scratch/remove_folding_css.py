with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

target = """/* =========================================================================
   3D CARD FOLDING MECHANICS \ufffd REACTIVE FOLD IN AND FOLD OUT
   Cards physically fold inward on hover and smoothly unfold out on mouse leave
   ========================================================================= */
.react-3d-card,
.project-card,
.cert-card,
.expertise-card,
.onboard-card,
.stat-card,
.glass-card,
.bday-card,
.code-block-visual,
.hero-about-tile,
.contact-card,
.profile-card-wrapper {
    transform-style: preserve-3d !important;
    /* perspective on parent grid container */
    transform-origin: center center !important;
    will-change: transform !important;
    transition: box-shadow 0.28s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.28s ease !important;
}

.react-3d-card.card-folded-in {
    box-shadow: 0 26px 52px rgba(0, 0, 0, 0.85), 0 8px 20px rgba(0, 0, 0, 0.55), inset 0 0 28px rgba(0, 0, 0, 0.52) !important;
    border-color: rgba(255, 255, 255, 0.22) !important;
}

.react-3d-card.card-folded-out {
    box-shadow: 0 12px 28px rgba(0, 0, 0, 0.5) !important;
}"""

# Try finding by boundary if exact string encoding differs
idx1 = css.find('/* =========================================================================\n   3D CARD FOLDING MECHANICS')
if idx1 == -1:
    idx1 = css.find('/* =========================================================================\r\n   3D CARD FOLDING MECHANICS')

idx2 = css.find('/* On mobile viewports, prevent any horizontal scroll push from fade animations */')

if idx1 != -1 and idx2 != -1:
    css = css[:idx1] + css[idx2:]
    with open('assets/css/style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Successfully removed redundant folding block from style.css")
else:
    print(f"Warning: boundaries not found: idx1={idx1}, idx2={idx2}")
