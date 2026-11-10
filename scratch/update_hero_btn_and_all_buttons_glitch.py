with open("assets/css/style.css", "r", encoding="utf-8") as f:
    css = f.read()

# Fix the broken glitch block at line 8561
old_glitch_target = """.back-to-top:hover,

    background: linear-gradient(115deg, #19E3D1 0%, #F5C542 26%, #FF2A85 52%, #8B3DFF 76%, #19E3D1 100%) !important;"""

fixed_glitch_block = """.back-to-top:hover {

    background: linear-gradient(115deg, #19E3D1 0%, #F5C542 26%, #FF2A85 52%, #8B3DFF 76%, #19E3D1 100%) !important;"""

if old_glitch_target in css:
    css = css.replace(old_glitch_target, fixed_glitch_block, 1)
    print("Fixed missing opening brace in Button Glitch Hover State!")
else:
    print("old_glitch_target not found directly, checking variations...")

# Now add the comprehensive rules at the very end of style.css:
# 1. Hero "Explore My Work" button: transparent background, square-like with rounded corners (8px)
# 2. ALL buttons across the site on hover: gradient glitch out effect
# 3. Whole card elements box bending deformation support

appendix = """
/* =========================================================================
   HERO "EXPLORE MY WORK" BUTTON — SQUARE-LIKE WITH ROUNDED CORNERS (8px) & TRANSPARENT BG
   ========================================================================= */
.hero-actions .cta-button,
.hero-actions a.cta-button {
    background: transparent !important;
    border: 1.5px solid rgba(25, 227, 209, 0.75) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    box-shadow: 0 0 16px rgba(25, 227, 209, 0.25), inset 0 0 10px rgba(25, 227, 209, 0.08) !important;
    padding: 0.85rem 2.2rem !important;
    font-weight: 600 !important;
    transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease, border-color 0.25s ease, background 0.25s ease !important;
}

/* =========================================================================
   ALL BUTTONS ACROSS THE WEBSITE — GRADIENT GLITCHED-OUT HOVER EFFECT
   Every single button across all sections glitches with animated gradient on hover
   ========================================================================= */
.cta-button:hover,
.hero-actions .cta-button:hover,
.hero-actions a.cta-button:hover,
.btn:hover,
.filter-btn:hover,
.filter-btn.active:hover,
.project-filters .filter-btn:hover,
.project-filters .filter-btn.active:hover,
.nav-resume-btn:hover,
.dock-btn:hover,
.submit-btn:hover,
.btn-submit:hover,
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

/* Ensure inner text and icons have punchy dark contrast on hover */
.cta-button:hover *,
.hero-actions .cta-button:hover *,
.hero-actions a.cta-button:hover *,
.btn:hover *,
.filter-btn:hover *,
.filter-btn.active:hover *,
.project-filters .filter-btn:hover *,
.project-filters .filter-btn.active:hover *,
.nav-resume-btn:hover *,
.dock-btn:hover *,
.submit-btn:hover *,
.btn-submit:hover *,
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
}

/* =========================================================================
   WHOLE CARD ELEMENTS BOX BENDING & TORSIONAL DEFORMATION
   The entire card container bends and twists as a solid unit under cursor
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
    perspective: 950px !important;
    will-change: transform !important;
    transition: box-shadow 0.3s ease, border-color 0.3s ease !important;
}

/* Keep card text and inner elements firmly locked to card face — NO text deforming */
.react-3d-card p,
.react-3d-card h3,
.react-3d-card h4,
.react-3d-card span,
.react-3d-card a,
.react-3d-card .badge,
.react-3d-card .project-title,
.react-3d-card .project-desc,
.project-card p,
.project-card h3,
.project-card span {
    transform: none !important;
}
"""

with open("assets/css/style.css", "w", encoding="utf-8") as f:
    f.write(css + "\n" + appendix)

print("Successfully updated style.css with hero button, all-buttons glitch, and whole-card deformation!")
