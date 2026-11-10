with open("assets/css/style.css", "r", encoding="utf-8") as f:
    css = f.read()

# 1. Clean up .filter-btn from the glitch lists
css = css.replace(".filter-btn,\n\n", "")
css = css.replace(".filter-btn:hover,\n\n", "")
css = css.replace(".filter-btn.active:hover {\n\n", "")
css = css.replace(".filter-btn:hover *,\n\n", "")

# 2. Add the comprehensive React 3D Card & Zero Illumination & Uniform Filters CSS
appendix = """
/* =========================================================================
   REACT 18 3D CARD PARALLAX ENGINE & ZERO ILLUMINATION HOVER SYSTEM
   - Authentic React 18 multi-layer 3D depth parallax across all site cards
   - Complete removal of artificial illumination effects on hover (specular flares,
     radial blooms, top glitch sweep bars, and neon glowing box shadows)
   - Replaced by clean, physical 3D drop shadow elevation
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
    perspective: 1100px !important;
    will-change: transform !important;
}

/* Child layers with multi-level Z-depth parallax */
.card-3d-layer {
    transform-style: preserve-3d !important;
    transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1) !important;
    will-change: transform !important;
}

/* TOTAL REMOVAL OF CARD ILLUMINATION EFFECTS ON HOVER */
/* 1. Disable all radial gradient specular flares (::before) */
.react-3d-card::before,
.project-card::before,
.cert-card::before,
.expertise-card::before,
.stat-card::before,
.glass-card::before,
.bday-card::before,
.code-block-visual::before,
.hero-about-tile::before,
.contact-card::before,
.cp-3d-card::before,
.react-3d-card:hover::before,
.project-card:hover::before,
.cert-card:hover::before,
.expertise-card:hover::before,
.stat-card:hover::before,
.glass-card:hover::before,
.bday-card:hover::before,
.code-block-visual:hover::before,
.hero-about-tile:hover::before,
.contact-card:hover::before,
.cp-3d-card:hover::before {
    display: none !important;
    opacity: 0 !important;
    background: none !important;
    content: none !important;
    animation: none !important;
    visibility: hidden !important;
}

/* 2. Disable card top accent glowing glitch bars (::after) */
.project-card::after,
.expertise-card::after,
.cert-card::after,
.stat-card::after,
.glass-card::after,
.code-block-visual::after,
.hero-about-tile::after,
.contact-card::after,
.cp-3d-card::after,
.react-3d-card::after,
.project-card:hover::after,
.expertise-card:hover::after,
.cert-card:hover::after,
.stat-card:hover::after,
.glass-card:hover::after,
.code-block-visual:hover::after,
.hero-about-tile:hover::after,
.contact-card:hover::after,
.cp-3d-card:hover::after,
.react-3d-card:hover::after {
    display: none !important;
    opacity: 0 !important;
    background: none !important;
    content: none !important;
    animation: none !important;
    visibility: hidden !important;
}

/* 3. Pure Physical Non-Illuminated 3D Shadow on Card Hover */
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
.cp-3d-card:hover {
    box-shadow: 0 20px 42px rgba(0, 0, 0, 0.75), 0 6px 14px rgba(0, 0, 0, 0.50) !important;
    border-color: rgba(255, 255, 255, 0.16) !important;
    filter: none !important;
}

/* =========================================================================
   PROJECT FILTERS — 100% UNIFORM COLOR FORMAT (STATIONARY & HOVER)
   All 4 buttons ('All Projects', 'AI & Data Science Projects', 'Web Apps', 'Creative Labs')
   maintain identical visual styling across stationary and hovered states.
   ========================================================================= */
.project-filters .filter-btn,
.project-filters .filter-btn.active,
.project-filters .filter-btn:hover,
.project-filters .filter-btn.active:hover,
.project-filters .filter-btn:focus,
.filter-btn,
.filter-btn.active {
    background: rgba(22, 14, 38, 0.82) !important;
    border: 1px solid rgba(168, 85, 247, 0.42) !important;
    color: #f1f5f9 !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
    text-shadow: none !important;
    animation: none !important;
    filter: none !important;
    cursor: pointer !important;
    transition: background 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease, transform 0.22s ease !important;
}

.project-filters .filter-btn:hover,
.project-filters .filter-btn.active:hover,
.filter-btn:hover,
.filter-btn.active:hover {
    background: rgba(34, 20, 56, 0.92) !important;
    border: 1px solid rgba(192, 132, 252, 0.65) !important;
    color: #ffffff !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.14) !important;
    transform: translateY(-2px) !important;
}

.project-filters .filter-btn:hover *,
.project-filters .filter-btn.active:hover *,
.filter-btn:hover *,
.filter-btn.active:hover * {
    color: #ffffff !important;
    text-shadow: none !important;
}
"""

with open("assets/css/style.css", "w", encoding="utf-8") as f:
    f.write(css + "\n" + appendix)

print("Successfully applied React 3D Cards, Zero Illumination, and Uniform Filters CSS!")
