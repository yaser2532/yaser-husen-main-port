with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update hero-3d-char:hover gradient to include dark blood red
old_hero_glitch = '''    background: linear-gradient(135deg, #FFFFFF 0%, #19E3D1 24%, #F5C542 48%, #FF2A85 74%, #8B3DFF 100%);

    background-size: 260% 260%;

    -webkit-background-clip: text;

    background-clip: text;

    -webkit-text-fill-color: transparent;

    text-shadow: none;

    animation: heroCharGradientShift 1.2s ease infinite alternate;

    filter: drop-shadow(-2px 0 0 rgba(25, 227, 209, 0.95)) 

            drop-shadow(2px 0 0 rgba(255, 42, 133, 0.95)) 

            drop-shadow(0 0 16px rgba(245, 197, 66, 0.85));'''

new_hero_glitch = '''    background: linear-gradient(135deg, #FFFFFF 0%, #19E3D1 18%, #8B0000 38%, #F5C542 58%, #FF1E42 78%, #8B3DFF 100%);

    background-size: 260% 260%;

    -webkit-background-clip: text;

    background-clip: text;

    -webkit-text-fill-color: transparent;

    text-shadow: none;

    animation: heroCharGradientShift 1.2s ease infinite alternate;

    filter: drop-shadow(-2px 0 0 rgba(25, 227, 209, 0.95)) 

            drop-shadow(2px 0 0 rgba(139, 0, 0, 0.95)) 

            drop-shadow(0 0 16px rgba(245, 197, 66, 0.85));'''

assert old_hero_glitch in content, 'old_hero_glitch not found'
content = content.replace(old_hero_glitch, new_hero_glitch, 1)

# 2. Update Top Accent Glitch Gradient Bar for Cards
old_card_accent = '''    background: linear-gradient(90deg, #19E3D1 0%, #F5C542 33%, #FF2A85 66%, #8B3DFF 100%);'''
new_card_accent = '''    background: linear-gradient(90deg, #8B0000 0%, #19E3D1 18%, #4A000A 36%, #F5C542 56%, #8B0000 76%, #8B3DFF 100%);'''
assert old_card_accent in content, 'old_card_accent not found'
content = content.replace(old_card_accent, new_card_accent, 1)

# 3. Append dark blood red & backward deformation enhancements
addon = '''

/* ==========================================================================
   Cyberpunk Dark Blood Red Integration & Backward Card Deformation
   ========================================================================== */

/* 1. Section Title Cyber Underscore - Blood Red & Cyan */
.section-title::after {
    background: linear-gradient(90deg, transparent, #8B0000 25%, #19E3D1 50%, #8B0000 75%, transparent) !important;
    box-shadow: 0 0 12px rgba(139, 0, 0, 0.55), 0 0 20px rgba(25, 227, 209, 0.25) !important;
}

/* 2. Category Filter Buttons - Dark Blood Red & Neon Edges */
.filter-btn:hover {
    color: #FF5A78 !important;
    border-color: rgba(180, 20, 40, 0.55) !important;
    background: rgba(74, 0, 10, 0.35) !important;
    box-shadow: 0 0 14px rgba(139, 0, 0, 0.40), inset 0 0 10px rgba(139, 0, 0, 0.25) !important;
}

.filter-btn.active {
    color: #FFFFFF !important;
    border-color: rgba(255, 30, 66, 0.75) !important;
    background: linear-gradient(135deg, rgba(88, 5, 18, 0.92) 0%, rgba(139, 0, 0, 0.70) 100%) !important;
    box-shadow: 0 0 20px rgba(139, 0, 0, 0.50), inset 0 0 12px rgba(74, 0, 10, 0.45) !important;
}

/* 3. Project Card Tech Tags & Cyber Badges */
.tag:hover,
.project-tag:hover,
.cert-badge:hover {
    border-color: rgba(139, 0, 0, 0.65) !important;
    background: rgba(55, 5, 15, 0.55) !important;
    color: #FFA4B2 !important;
    box-shadow: 0 0 12px rgba(139, 0, 0, 0.35) !important;
}

/* 4. Navbar Resume Button Hover State */
.nav-resume-btn:hover {
    background: linear-gradient(135deg, rgba(74, 0, 10, 0.80) 0%, rgba(20, 10, 35, 0.80) 100%) !important;
    border-color: rgba(180, 20, 40, 0.70) !important;
    box-shadow: 0 0 18px rgba(139, 0, 0, 0.45), 0 0 8px rgba(245, 197, 66, 0.30) !important;
}

/* 5. Terminal Code Header - Blood Red Status & Dot */
.terminal-dot.close {
    background: #8B0000 !important;
    box-shadow: 0 0 8px rgba(139, 0, 0, 0.85) !important;
}
.terminal-tag {
    background: rgba(55, 5, 15, 0.55) !important;
    border-color: rgba(139, 0, 0, 0.50) !important;
    color: #FFA4B2 !important;
}

/* 6. Card Backward Deformation Supporting Depth & Glitch Hover */
.cp-3d-card {
    transform-style: preserve-3d !important;
    will-change: transform, box-shadow !important;
    transition: transform 0.45s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.35s ease, border-color 0.3s ease !important;
}

.cp-3d-card:hover {
    border-color: rgba(25, 227, 209, 0.85) !important;
    box-shadow: 
        -3px 0 20px rgba(25, 227, 209, 0.45),
        3px 0 24px rgba(139, 0, 0, 0.65),
        0 0 32px rgba(245, 197, 66, 0.25),
        inset 0 4px 24px rgba(0, 0, 0, 0.88),
        inset 0 0 20px rgba(139, 0, 0, 0.40),
        0 8px 30px rgba(0, 0, 0, 0.75) !important;
}

.cp-chromatic-split {
    text-shadow: -2.5px 0 var(--cp-turquoise), 2.5px 0 #8B0000, 0 0 16px rgba(139, 0, 0, 0.45) !important;
}
'''

content += addon

with open('assets/css/style.css', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated assets/css/style.css with glitch and dark blood red styling!')
