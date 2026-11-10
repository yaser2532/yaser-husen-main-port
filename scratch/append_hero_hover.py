with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

hero_hover_block = """
/* ==========================================================================
   Hero Section Interactive Hover Ecosystem (UTC, Status, Spec, Tags, Subtitle)
   ========================================================================== */

/* 1. Hero UTC Live Clock Pill */
.hero-clock-pill {
    cursor: pointer !important;
    transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), 
                box-shadow 0.28s ease, 
                border-color 0.28s ease, 
                background 0.28s ease, 
                color 0.28s ease !important;
}

.hero-clock-pill:hover {
    transform: translateY(-3px) scale(1.05) !important;
    background: rgba(245, 197, 66, 0.20) !important;
    border-color: #F5C542 !important;
    color: #FFFFFF !important;
    box-shadow: 0 0 22px rgba(245, 197, 66, 0.65), 
                0 0 40px rgba(25, 227, 209, 0.35), 
                inset 0 0 12px rgba(245, 197, 66, 0.25) !important;
}

.hero-clock-pill:hover i {
    transform: rotate(180deg) scale(1.15) !important;
    color: #19E3D1 !important;
}

.hero-clock-pill:hover #clock-utc {
    color: #FFFFFF !important;
    text-shadow: 0 0 10px rgba(245, 197, 66, 0.95), 0 0 22px rgba(255, 255, 255, 0.70) !important;
    letter-spacing: 0.04em;
}

/* 2. Hero Status Deploying Intel Badge */
.hero-sticker-badge {
    cursor: pointer !important;
    transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), 
                box-shadow 0.28s ease, 
                border-color 0.28s ease, 
                background 0.28s ease, 
                color 0.28s ease !important;
}

.hero-sticker-badge:hover {
    transform: rotate(0deg) scale(1.06) translateY(-3px) !important;
    border-color: #FF1E42 !important;
    background: rgba(139, 0, 0, 0.45) !important;
    color: #FFFFFF !important;
    box-shadow: 0 0 24px rgba(255, 30, 66, 0.75), 
                0 0 45px rgba(180, 20, 40, 0.45), 
                inset 0 0 12px rgba(255, 30, 66, 0.30) !important;
}

.hero-sticker-badge:hover .pulse-dot {
    background: #FF1E42 !important;
    box-shadow: 0 0 14px #FF1E42, 0 0 24px rgba(255, 30, 66, 0.9) !important;
}

.hero-sticker-badge:hover .sticker-text {
    text-shadow: 0 0 10px rgba(255, 30, 66, 0.85), 0 0 18px rgba(255, 255, 255, 0.60) !important;
    letter-spacing: 0.11em;
}

/* 3. Hero Spec Stamp [AGENTIC_V4.2] */
.hero-spec-stamp {
    cursor: pointer !important;
    transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), 
                box-shadow 0.28s ease, 
                border-color 0.28s ease, 
                background 0.28s ease, 
                color 0.28s ease, 
                letter-spacing 0.28s ease !important;
}

.hero-spec-stamp:hover {
    transform: translateY(-3px) scale(1.06) !important;
    color: #19E3D1 !important;
    border-color: #19E3D1 !important;
    border-style: solid !important;
    background: rgba(25, 227, 209, 0.15) !important;
    box-shadow: 0 0 22px rgba(25, 227, 209, 0.65), 
                0 0 35px rgba(139, 61, 255, 0.30), 
                inset 0 0 10px rgba(25, 227, 209, 0.20) !important;
    letter-spacing: 0.12em !important;
    text-shadow: 0 0 10px rgba(25, 227, 209, 0.8) !important;
}

/* 4. Hero Subtitle Hover Glow */
.hero-subtitle {
    display: inline-block;
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), 
                text-shadow 0.3s ease, 
                color 0.3s ease !important;
}

.hero-subtitle:hover {
    color: #FFFFFF !important;
    transform: translateX(4px);
    text-shadow: 0 0 20px rgba(25, 227, 209, 0.95), 
                 0 0 32px rgba(245, 197, 66, 0.45), 
                 -2px 0 10px rgba(255, 30, 66, 0.50) !important;
}

/* 5. Hero About Tile Hover Elevation */
.hero-about-tile {
    cursor: pointer !important;
    transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), 
                box-shadow 0.3s ease, 
                border-color 0.3s ease !important;
}

.hero-about-tile:hover {
    transform: translateY(-4px) scale(1.015) !important;
    border-color: rgba(25, 227, 209, 0.75) !important;
    box-shadow: 0 18px 45px rgba(0, 0, 0, 0.85), 
                0 0 35px rgba(25, 227, 209, 0.40), 
                -4px 0 25px rgba(255, 30, 66, 0.30), 
                4px 0 25px rgba(245, 197, 66, 0.25) !important;
}

/* 6. Hero Trait Tags Hover */
.hero-traits-list .trait-tag {
    cursor: pointer !important;
    user-select: none;
    transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), 
                box-shadow 0.28s ease, 
                border-color 0.28s ease, 
                background 0.28s ease, 
                color 0.28s ease !important;
}

.hero-traits-list .trait-tag:hover {
    transform: translateY(-3px) scale(1.05) !important;
    border-color: #F5C542 !important;
    background: rgba(245, 197, 66, 0.18) !important;
    color: #FFFFFF !important;
    box-shadow: 0 0 20px rgba(245, 197, 66, 0.55), 
                0 0 35px rgba(25, 227, 209, 0.30), 
                inset 0 0 10px rgba(245, 197, 66, 0.20) !important;
    text-shadow: 0 0 8px rgba(245, 197, 66, 0.8) !important;
}
"""

css = css + hero_hover_block

with open('assets/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Appended high-priority hero hover ecosystem rules to style.css!")
