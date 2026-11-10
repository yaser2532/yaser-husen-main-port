with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Locate the button section to replace
idx_start = css.find('/* =========================================================================\n   ALL BUTTONS GRADIENT GLITCH HOVER')
if idx_start == -1:
    idx_start = css.find('/* =========================================================================\r\n   ALL BUTTONS GRADIENT GLITCH HOVER')

idx_end = css.find('/* =========================================================================\n   ZERO HORIZONTAL OVERFLOW & FULL-BLEED SECTIONS')
if idx_end == -1:
    idx_end = css.find('/* =========================================================================\r\n   ZERO HORIZONTAL OVERFLOW & FULL-BLEED SECTIONS')

assert idx_start != -1, "Button section start not found"
assert idx_end != -1, "Zero horizontal overflow section start not found"

new_section = """/* =========================================================================
   ALL BUTTONS & NAVBAR LINKS GLITCHED-OUT GRADIENT HOVER EFFECT
   Matches the hero section name (#tp-name / .hero-3d-char) glitched-out aesthetic:
   - Dynamic animated gradient: #FFFFFF, #19E3D1, #8B0000, #F5C542, #FF1E42, #8B3DFF
   - Continuous hero gradient sweep (heroCharGradientShift)
   - Chromatic RGB split drop-shadow & text-shadow
   - Glitch jitter animation with cyan and magenta slice displacement
   ========================================================================= */

@keyframes btnGlitchJitter {
    0% { transform: translateY(-3px) scale(1.028) skew(0deg); }
    25% { transform: translateY(-3.5px) scale(1.028) skew(-1.5deg) translate(-2px, 0); }
    50% { transform: translateY(-2.5px) scale(1.028) skew(1.5deg) translate(2px, 0); }
    75% { transform: translateY(-3.5px) scale(1.028) skew(-0.5deg) translate(-1px, 0); }
    100% { transform: translateY(-3px) scale(1.028) skew(0deg); }
}

@keyframes navLinkGlitch {
    0% { transform: skew(0deg) translate(0, 0); }
    25% { transform: skew(-1deg) translate(-1.5px, 0.5px); }
    50% { transform: skew(1deg) translate(1.5px, -0.5px); }
    75% { transform: skew(-0.5deg) translate(-1px, 0); }
    100% { transform: skew(0deg) translate(0, 0); }
}

/* ALL BUTTONS GLITCHED-OUT GRADIENT HOVER */
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
#secret-message-btn:hover,
a#secret-message-btn:hover,
#submit-btn:hover,
button[type="submit"]:hover,
.btn-submit:hover,
#footer-resume-btn:hover,
.dock-btn-resume:hover,
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
    background: linear-gradient(135deg, #FFFFFF 0%, #19E3D1 18%, #8B0000 38%, #F5C542 58%, #FF1E42 78%, #8B3DFF 100%) !important;
    background-size: 260% 260% !important;
    animation: heroCharGradientShift 1.2s ease infinite alternate, btnGlitchJitter 0.28s steps(2) infinite !important;
    border-color: #19E3D1 !important;
    box-shadow: 
        -3.5px 0 0 rgba(25, 227, 209, 0.95),
        3.5px 0 0 #8B0000,
        0 0 28px rgba(25, 227, 209, 0.75),
        0 0 45px rgba(139, 0, 0, 0.65),
        inset 0 0 14px rgba(25, 227, 209, 0.40) !important;
    color: #07060B !important;
    -webkit-text-fill-color: #07060B !important;
    font-weight: 800 !important;
    text-shadow: 
        -2px 0 0 #19E3D1,
        2px 0 0 #FF1E42,
        0 0 10px rgba(255, 255, 255, 0.9) !important;
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
#secret-message-btn:hover *,
a#secret-message-btn:hover *,
#submit-btn:hover *,
button[type="submit"]:hover *,
.btn-submit:hover *,
#footer-resume-btn:hover *,
.dock-btn-resume:hover *,
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
    -webkit-text-fill-color: #07060B !important;
    text-shadow: none !important;
}

/* NAVBAR LINKS & FILTERS GLITCHED-OUT GRADIENT HOVER */
.nav-link:hover,
.nav-links a:hover,
header nav a:hover,
#nav-menu a:hover,
.mobile-nav a:hover,
.mobile-nav-link:hover,
.nav-brand:hover,
a.nav-link:hover {
    background: linear-gradient(135deg, #FFFFFF 0%, #19E3D1 18%, #8B0000 38%, #F5C542 58%, #FF1E42 78%, #8B3DFF 100%) !important;
    background-size: 260% 260% !important;
    -webkit-background-clip: text !important;
    background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    color: transparent !important;
    animation: heroCharGradientShift 1.2s ease infinite alternate, navLinkGlitch 0.28s steps(2) infinite !important;
    filter: drop-shadow(-2px 0 0 rgba(25, 227, 209, 0.95))
            drop-shadow(2px 0 0 rgba(139, 0, 0, 0.95))
            drop-shadow(0 0 16px rgba(245, 197, 66, 0.85)) !important;
}

.nav-link:hover::after,
.nav-links a:hover::after,
header nav a:hover::after {
    width: 100% !important;
    background: linear-gradient(90deg, #19E3D1, #8B0000, #F5C542, #FF1E42, #19E3D1) !important;
    background-size: 200% 100% !important;
    box-shadow: 0 0 12px #19E3D1, 0 0 20px #8B0000 !important;
    animation: navGradSweep 1.2s linear infinite !important;
}

/* =========================================================================
   CARDS AI CHAT BOX POP-UP WINDOW BEHAVIOR
   All cards behave like the AI chat box pop-up window:
   - Spring scaling, forward pop-up elevation
   - Cyber chromatic neon rim & deep shadow
   - Frosted glassmorphism backdrop blur
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
    background: rgba(20, 10, 36, 0.72) !important;
    border: 1px solid rgba(157, 77, 255, 0.35) !important;
    backdrop-filter: blur(14px) !important;
    -webkit-backdrop-filter: blur(14px) !important;
    box-shadow: 0 0.5rem 2.5rem rgba(0, 0, 0, 0.65), 0 0 1.5rem rgba(157, 77, 255, 0.22);
    border-radius: 1rem !important;
    transform-origin: center center !important;
    transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.35s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.25s ease !important;
}

.react-3d-card:hover,
.project-card:hover,
.cert-card:hover,
.expertise-card:hover,
.onboard-card:hover,
.stat-card:hover,
.glass-card:hover,
.bday-card:hover,
.code-block-visual:hover,
.hero-about-tile:hover,
.contact-card:hover,
.profile-card-wrapper:hover,
.card-3d-active {
    border-color: #19E3D1 !important;
    background: rgba(20, 10, 36, 0.85) !important;
    box-shadow: 
        0 24px 60px rgba(0, 0, 0, 0.88),
        -4px 0 24px rgba(25, 227, 209, 0.55),
        4px 0 24px rgba(255, 42, 133, 0.45),
        0 0 35px rgba(245, 197, 66, 0.35),
        inset 0 0 20px rgba(25, 227, 209, 0.08) !important;
}

/* =========================================================================
   CARD POP-UP MODAL WINDOW (LIGHTBOX NODE INSPECTION)
   Identical architecture & motion to the nano-chat AI pop-up window
   ========================================================================= */
.card-popup-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(4, 2, 8, 0.88);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    z-index: 99998;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 1.5rem;
    opacity: 0;
    visibility: hidden;
    pointer-events: none;
    transition: opacity 0.3s ease, visibility 0.3s ease;
}

.card-popup-overlay.active {
    opacity: 1;
    visibility: visible;
    pointer-events: auto;
}

.card-popup-window {
    width: 100%;
    max-width: 48rem;
    max-height: 88vh;
    display: flex;
    flex-direction: column;
    transform: scale(0.92) translateY(20px);
    transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.card-popup-overlay.active .card-popup-window {
    transform: scale(1) translateY(0);
}

.card-popup-card {
    margin: 0;
    width: 100%;
    max-width: 100%;
    max-height: 85vh;
    overflow-y: auto;
    background: rgba(20, 10, 36, 0.90) !important;
    border: 1px solid #19E3D1 !important;
    box-shadow: 
        0 24px 60px rgba(0, 0, 0, 0.92),
        -4px 0 25px rgba(25, 227, 209, 0.6),
        4px 0 25px rgba(255, 42, 133, 0.5),
        0 0 40px rgba(245, 197, 66, 0.35) !important;
    padding: 1.6rem !important;
}

.card-popup-body {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
    margin: 1.2rem 0;
}

.card-popup-img-wrap {
    width: 100%;
    max-height: 18rem;
    border-radius: 0.75rem;
    overflow: hidden;
    border: 1px solid rgba(25, 227, 209, 0.3);
    background: rgba(0, 0, 0, 0.6);
}

.card-popup-img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
}

.card-popup-item-title {
    font-family: 'Space Grotesk', var(--font-headings);
    color: #ffffff;
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    margin-bottom: 0.5rem;
}

.card-popup-item-desc {
    color: rgba(230, 230, 245, 0.88);
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 0.8rem;
}

.card-popup-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.card-popup-footer {
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 1rem;
    border-top: 1px solid rgba(157, 77, 255, 0.25);
    padding-top: 1rem;
    margin-top: 0.5rem;
}
"""

css = css[:idx_start] + new_section + "\n\n\n" + css[idx_end:]

with open('assets/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("SUCCESS: Updated style.css with buttons & nav glitched hover, cards pop-up behavior, and modal window styles!")
