with open("assets/css/style.css", "r", encoding="utf-8") as f:
    css = f.read()

rule = """
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
}
"""

with open("assets/css/style.css", "w", encoding="utf-8") as f:
    f.write(css + "\n" + rule)

print("Applied ultra-high specificity all-buttons glitch hover rule!")
