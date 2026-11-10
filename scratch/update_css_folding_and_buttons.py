import re

def update_css():
    with open('assets/css/style.css', 'r', encoding='utf-8') as f:
        css = f.read()

    # 1. Update button hover styling with dark blood red, nav link aesthetic, and static glitched out mix of gradient colors
    old_btn_hover = """#submit-btn:hover,
.btn-submit:hover,
button[type="submit"]:hover {
    background: linear-gradient(115deg, #19E3D1 0%, #F5C542 26%, #FF2A85 52%, #8B3DFF 76%, #19E3D1 100%) !important;
    background-size: 260% 100% !important;
    animation: btnGlitchGradSweep 1.8s linear infinite, btnMicroJitter 0.24s cubic-bezier(0.25, 0.46, 0.45, 0.94) 1 !important;
    border-color: #19E3D1 !important;
    color: #07060B !important;
}


/* =========================================================================
   ALL BUTTONS GRADIENT GLITCH HOVER — ULTRA HIGH SPECIFICITY DOMINANCE
   ========================================================================= */
.project-filters .filter-btn:hover,
.project-filters button.filter-btn:hover,
.project-filters .filter-btn.active:hover,
.project-filters button.filter-btn.active:hover,
.contact-form button[type="submit"]:hover,
.contact-form .btn-submit:hover,
.contact-form #submit-btn:hover,
#submit-btn:hover,
.hero-actions .cta-button:hover,
.hero-actions a.cta-button:hover,
.cta-button:hover,
.nav-resume-btn:hover,
.dock-btn:hover,
.submit-btn:hover,
.btn-submit:hover,
.btn:hover,
.btn-ai-chat:hover,
.message-btn:hover,
.bday-start-btn:hover,
.bday-trigger-btn:hover,
.nav-sound-btn:hover,
.action-btn:hover,
button.contact-btn:hover,
.back-to-top:hover,
.project-link:hover,
.view-cert-btn:hover,
button:hover,
.btn-action:hover,
.hero-scroll-pill:hover,
a.cta-button:hover {
    background: linear-gradient(115deg, #19E3D1 0%, #F5C542 26%, #FF2A85 52%, #8B3DFF 76%, #19E3D1 100%) !important;
    background-size: 260% 100% !important;
    animation: btnGlitchGradSweep 1.8s linear infinite, btnMicroJitter 0.24s cubic-bezier(0.25, 0.46, 0.45, 0.94) 1 !important;
    border-color: #19E3D1 !important;
    box-shadow: 
        -3.5px 0 0 rgba(25, 227, 209, 0.9),
        3.5px 0 0 rgba(255, 42, 133, 0.9),
        0 0 28px rgba(25, 227, 209, 0.7),
        0 0 50px rgba(245, 197, 66, 0.35) !important;
    color: #07060B !important;
    font-weight: 700 !important;
    text-shadow: 0 1px 2px rgba(255, 255, 255, 0.6) !important;
    transform: translateY(-2px) scale(1.02) !important;
}

.project-filters .filter-btn:hover *,
.project-filters button.filter-btn:hover *,
.project-filters .filter-btn.active:hover *,
.project-filters button.filter-btn.active:hover *,
.contact-form button[type="submit"]:hover *,
.contact-form .btn-submit:hover *,
.contact-form #submit-btn:hover *,
#submit-btn:hover *,
.hero-actions .cta-button:hover *,
.hero-actions a.cta-button:hover *,
.cta-button:hover *,
.nav-resume-btn:hover *,
.dock-btn:hover *,
.submit-btn:hover *,
.btn-submit:hover *,
.btn:hover *,
.btn-ai-chat:hover *,
.message-btn:hover *,
.bday-start-btn:hover *,
.bday-trigger-btn:hover *,
.nav-sound-btn:hover *,
.action-btn:hover *,
button.contact-btn:hover *,
.back-to-top:hover *,
.project-link:hover *,
.view-cert-btn:hover *,
button:hover *,
.btn-action:hover *,
.hero-scroll-pill:hover *,
a.cta-button:hover * {
    color: #07060B !important;
    text-shadow: none !important;
}"""

    new_btn_hover = """/* =========================================================================
   ALL BUTTONS GRADIENT GLITCH HOVER — DARK BLOOD RED + NAV-LINK CHROMATIC MIX
   Static glitched-out mix of gradient colors incorporating dark blood red, cyan, and gold
   ========================================================================= */
.project-filters .filter-btn:hover,
.project-filters button.filter-btn:hover,
.project-filters .filter-btn.active:hover,
.project-filters button.filter-btn.active:hover,
.contact-form button[type="submit"]:hover,
.contact-form .btn-submit:hover,
.contact-form #submit-btn:hover,
#submit-btn:hover,
.hero-actions .cta-button:hover,
.hero-actions a.cta-button:hover,
.cta-button:hover,
.nav-resume-btn:hover,
.dock-btn:hover,
.submit-btn:hover,
.btn-submit:hover,
.btn:hover,
.btn-ai-chat:hover,
.message-btn:hover,
.bday-start-btn:hover,
.bday-trigger-btn:hover,
.nav-sound-btn:hover,
.action-btn:hover,
button.contact-btn:hover,
.back-to-top:hover,
.project-link:hover,
.view-cert-btn:hover,
button:hover,
.btn-action:hover,
.hero-scroll-pill:hover,
a.cta-button:hover {
    background: linear-gradient(115deg, #8B0000 0%, #19E3D1 18%, #45000A 36%, #FF1E42 54%, #F5C542 72%, #19E3D1 88%, #8B0000 100%) !important;
    background-size: 100% 100% !important;
    border-color: #19E3D1 !important;
    box-shadow: 
        -3px 0 0 rgba(25, 227, 209, 0.92),
        3px 0 0 #8B0000,
        0 0 24px rgba(139, 0, 0, 0.75),
        0 0 35px rgba(25, 227, 209, 0.50),
        inset 0 0 12px rgba(139, 0, 0, 0.40) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    font-weight: 700 !important;
    text-shadow: -1.5px 0 0 #19E3D1, 1.5px 0 0 #8B0000, 0 0 10px rgba(245, 197, 66, 0.6) !important;
    transform: translateY(-2px) scale(1.02) !important;
    animation: btnMicroJitter 0.24s cubic-bezier(0.25, 0.46, 0.45, 0.94) 1 !important;
}

.project-filters .filter-btn:hover *,
.project-filters button.filter-btn:hover *,
.project-filters .filter-btn.active:hover *,
.project-filters button.filter-btn.active:hover *,
.contact-form button[type="submit"]:hover *,
.contact-form .btn-submit:hover *,
.contact-form #submit-btn:hover *,
#submit-btn:hover *,
.hero-actions .cta-button:hover *,
.hero-actions a.cta-button:hover *,
.cta-button:hover *,
.nav-resume-btn:hover *,
.dock-btn:hover *,
.submit-btn:hover *,
.btn-submit:hover *,
.btn:hover *,
.btn-ai-chat:hover *,
.message-btn:hover *,
.bday-start-btn:hover *,
.bday-trigger-btn:hover *,
.nav-sound-btn:hover *,
.action-btn:hover *,
button.contact-btn:hover *,
.back-to-top:hover *,
.project-link:hover *,
.view-cert-btn:hover *,
button:hover *,
.btn-action:hover *,
.hero-scroll-pill:hover *,
a.cta-button:hover * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    text-shadow: -1px 0 0 #19E3D1, 1px 0 0 #8B0000 !important;
}"""

    if old_btn_hover in css:
        css = css.replace(old_btn_hover, new_btn_hover)
        print("Updated button hover rules.")
    else:
        print("Warning: old_btn_hover not found exactly; using regex")
        # Try replacing via regex
        pattern = r"#submit-btn:hover,\s*\.btn-submit:hover,\s*button\[type=\"submit\"\]:hover\s*\{[^}]+\}\s*/\* =========================================================================\s*ALL BUTTONS GRADIENT GLITCH HOVER.*?a\.cta-button:hover \* \{[^}]+\}"
        css = re.sub(pattern, new_btn_hover, css, flags=re.DOTALL)

    # 2. Add 3D Folding and Mobile Responsive Rules
    card_folding_block = """
/* =========================================================================
   3D CARD FOLDING MECHANICS — REACTIVE FOLD IN AND FOLD OUT
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
    perspective: 900px !important;
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
}

/* On mobile viewports, prevent any horizontal scroll push from fade animations */
@media (max-width: 768px) {
    .scroll-reveal.fade-left,
    .scroll-reveal.fade-right,
    .fade-left,
    .fade-right {
        transform: translateY(1.2rem) !important;
    }
    .scroll-reveal.fade-left.active,
    .scroll-reveal.fade-right.active {
        transform: translateY(0) !important;
    }
    .expertise-showcase,
    .expertise-cards-grid {
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
}
"""

    if "3D CARD FOLDING MECHANICS" not in css:
        css = css + "\n" + card_folding_block
        print("Added 3D card folding and mobile responsive rules.")

    with open('assets/css/style.css', 'w', encoding='utf-8') as f:
        f.write(css)

if __name__ == '__main__':
    update_css()
