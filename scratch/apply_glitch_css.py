import os

style_path = 'assets/css/style.css'

with open(style_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the hero-3d-char section
target_char_css = """.hero-3d-char {
    display: inline-block;
    position: relative;
    font-family: 'Space Grotesk', var(--font-headings);
    font-weight: 900;
    font-style: italic;
    color: #ffffff;
    cursor: default;
    user-select: none;
    transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), filter 0.22s ease, text-shadow 0.22s ease;
    text-shadow: 
        1px 1px 0 #ffd873,
        2px 2px 0 #f2c14e,
        3px 3px 0 #19e3d0,
        4px 4px 0 #9d4dff,
        5px 5px 14px rgba(25, 227, 208, 0.65),
        0 0 24px rgba(242, 193, 78, 0.4);
    will-change: transform;
}

.hero-3d-char.is-repelled {
    filter: brightness(1.35) drop-shadow(0 0 16px var(--cp-turquoise));
}"""

replacement_char_css = """.hero-3d-char {
    display: inline-block;
    position: relative;
    font-family: 'Space Grotesk', var(--font-headings);
    font-weight: 900;
    font-style: italic;
    color: #ffffff;
    cursor: default;
    user-select: none;
    transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), filter 0.22s ease, text-shadow 0.22s ease;
    text-shadow: 
        1px 1px 0 #ffd873,
        2px 2px 0 #f2c14e,
        3px 3px 0 #19e3d0,
        4px 4px 0 #9d4dff,
        5px 5px 14px rgba(25, 227, 208, 0.65),
        0 0 24px rgba(242, 193, 78, 0.4);
    will-change: transform;
    overflow: visible;
}

/* Chromatic Aberration Glitch Slices via Pseudo-Elements */
.hero-3d-char::before,
.hero-3d-char::after {
    content: attr(data-char);
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    opacity: 0;
    z-index: 2;
    -webkit-text-fill-color: initial;
    transition: opacity 0.1s ease;
}

.hero-3d-char::before {
    color: #19E3D1; /* Cyan Slice */
    clip-path: polygon(0 15%, 100% 15%, 100% 48%, 0 48%);
    transform: translate3d(-3px, -1px, 0);
}

.hero-3d-char::after {
    color: #FF2A85; /* Cyber Pink / Magenta Slice */
    clip-path: polygon(0 58%, 100% 58%, 100% 90%, 0 90%);
    transform: translate3d(3px, 1px, 0);
}

/* Glitched Out Color Gradient Effect on Hover & When Repelled */
.hero-3d-char:hover,
.hero-3d-char.is-repelled {
    background: linear-gradient(135deg, #FFFFFF 0%, #19E3D1 24%, #F5C542 48%, #FF2A85 74%, #8B3DFF 100%);
    background-size: 260% 260%;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: none;
    animation: heroCharGradientShift 1.2s ease infinite alternate;
    filter: drop-shadow(-2px 0 0 rgba(25, 227, 209, 0.95)) 
            drop-shadow(2px 0 0 rgba(255, 42, 133, 0.95)) 
            drop-shadow(0 0 16px rgba(245, 197, 66, 0.85));
}

.hero-3d-char:hover::before,
.hero-3d-char.is-repelled::before {
    opacity: 0.95;
    animation: charGlitchSliceCyan 0.22s steps(2, start) infinite;
}

.hero-3d-char:hover::after,
.hero-3d-char.is-repelled::after {
    opacity: 0.95;
    animation: charGlitchSliceMagenta 0.26s steps(2, start) infinite;
}

@keyframes charGlitchSliceCyan {
    0% {
        clip-path: polygon(0 12%, 100% 12%, 100% 45%, 0 45%);
        transform: translate3d(-3px, -1px, 0);
    }
    50% {
        clip-path: polygon(0 25%, 100% 25%, 100% 55%, 0 55%);
        transform: translate3d(-5px, 1px, 0) skewX(-3deg);
    }
    100% {
        clip-path: polygon(0 8%, 100% 8%, 100% 38%, 0 38%);
        transform: translate3d(-2px, -2px, 0);
    }
}

@keyframes charGlitchSliceMagenta {
    0% {
        clip-path: polygon(0 55%, 100% 55%, 100% 88%, 0 88%);
        transform: translate3d(3px, 1px, 0);
    }
    50% {
        clip-path: polygon(0 68%, 100% 68%, 100% 96%, 0 96%);
        transform: translate3d(5px, -1px, 0) skewX(3deg);
    }
    100% {
        clip-path: polygon(0 45%, 100% 45%, 100% 78%, 0 78%);
        transform: translate3d(2px, 2px, 0);
    }
}

@keyframes heroCharGradientShift {
    0% { background-position: 0% 50%; }
    100% { background-position: 100% 50%; }
}"""

# Normalize CRLF for matching
if target_char_css.replace('\r\n', '\n') in content.replace('\r\n', '\n'):
    content = content.replace('\r\n', '\n').replace(target_char_css.replace('\r\n', '\n'), replacement_char_css)
    print("Replaced .hero-3d-char styles successfully.")
else:
    print("Warning: target_char_css not found!")

# 2. Append the comprehensive glitch and Gen Z system at the end
glitch_genz_system = """

/* =========================================================================
   GEN Z CHAOTIC CYBERPUNK & GLITCHED-OUT COLOR GRADIENT SYSTEM
   ========================================================================= */

/* --- BUTTONS GLITCHED-OUT COLOR GRADIENT EFFECT --- */
.cta-button,
.filter-btn,
.nav-resume-btn,
.dock-btn,
.submit-btn,
.hero-scroll-pill,
.btn,
.btn-ai-chat,
.message-btn,
.bday-start-btn,
.bday-trigger-btn,
.nav-sound-btn,
.action-btn,
button.contact-btn,
.back-to-top {
    position: relative;
    overflow: hidden;
    transition: transform 0.22s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease, border-color 0.25s ease, background 0.25s ease !important;
}

/* Button Glitch Hover State */
.cta-button:hover,
.filter-btn:hover,
.nav-resume-btn:hover,
.dock-btn:hover,
.submit-btn:hover,
.hero-scroll-pill:hover,
.btn:hover,
.btn-ai-chat:hover,
.message-btn:hover,
.bday-start-btn:hover,
.bday-trigger-btn:hover,
.nav-sound-btn:hover,
.action-btn:hover,
button.contact-btn:hover,
.back-to-top:hover,
.filter-btn.active:hover {
    background: linear-gradient(115deg, #19E3D1 0%, #F5C542 26%, #FF2A85 52%, #8B3DFF 76%, #19E3D1 100%) !important;
    background-size: 260% 100% !important;
    animation: btnGlitchGradSweep 1.8s linear infinite, btnMicroJitter 0.24s cubic-bezier(0.25, 0.46, 0.45, 0.94) 1 !important;
    border-color: #19E3D1 !important;
    box-shadow: 
        -3.5px 0 0 rgba(25, 227, 209, 0.9),
        3.5px 0 0 rgba(255, 42, 133, 0.9),
        0 0 28px rgba(25, 227, 209, 0.7),
        0 0 50px rgba(245, 197, 66, 0.35),
        inset 0 0 14px rgba(245, 197, 66, 0.4) !important;
    color: #07060B !important;
    font-weight: 700 !important;
    text-shadow: 0 1px 2px rgba(255, 255, 255, 0.6) !important;
    transform: translateY(-3px) scale(1.02) !important;
}

/* Ensure inner text and icons have maximum punchy contrast on hover */
.cta-button:hover *,
.filter-btn:hover *,
.nav-resume-btn:hover *,
.dock-btn:hover *,
.submit-btn:hover *,
.btn:hover *,
.btn-ai-chat:hover *,
.message-btn:hover *,
.bday-start-btn:hover *,
.bday-trigger-btn:hover *,
.nav-sound-btn:hover *,
.action-btn:hover *,
button.contact-btn:hover *,
.back-to-top:hover * {
    color: #07060B !important;
    text-shadow: none !important;
}

.hero-scroll-pill:hover .scroll-label {
    color: #07060B !important;
}
.hero-scroll-pill:hover .scroll-mouse-icon {
    border-color: #07060B !important;
}
.hero-scroll-pill:hover .scroll-wheel {
    background: #07060B !important;
}

@keyframes btnGlitchGradSweep {
    0% { background-position: 0% 50%; }
    100% { background-position: 260% 50%; }
}

@keyframes btnMicroJitter {
    0% { transform: translateY(-2px) scale(1.01); }
    25% { transform: translateY(-4px) scale(1.03) skewX(-2deg); }
    50% { transform: translateY(-2px) scale(1.01) skewX(2deg); }
    75% { transform: translateY(-3.5px) scale(1.025) skewX(-1deg); }
    100% { transform: translateY(-3px) scale(1.02); }
}

/* --- LINKS GLITCHED-OUT COLOR GRADIENT EFFECT --- */
a.nav-link,
.project-link,
footer a,
.contact-link,
.bday-nav-link,
.social-icon-btn,
.social-link,
.view-all-link,
.author-link {
    position: relative;
    transition: all 0.22s ease;
}

a.nav-link:hover,
.project-link:hover,
footer a:hover,
.contact-link:hover,
.bday-nav-link:hover,
.view-all-link:hover,
.author-link:hover {
    background: linear-gradient(90deg, #19E3D1 0%, #F5C542 35%, #FF2A85 70%, #8B3DFF 100%) !important;
    background-size: 200% auto !important;
    -webkit-background-clip: text !important;
    background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    animation: linkGlitchGradFlow 1.4s linear infinite !important;
    filter: drop-shadow(-1.5px 0 0 rgba(25, 227, 209, 0.85)) drop-shadow(1.5px 0 0 rgba(255, 42, 133, 0.85)) drop-shadow(0 0 10px rgba(245, 197, 66, 0.6)) !important;
}

a.nav-link:hover i,
.project-link:hover i,
footer a:hover i,
.contact-link:hover i,
.bday-nav-link:hover i {
    color: #19E3D1 !important;
    -webkit-text-fill-color: #19E3D1 !important;
    filter: drop-shadow(0 0 6px #19E3D1);
}

/* Glitched underline draw on links */
a.nav-link::after,
.project-link::after,
.contact-link::after {
    content: '';
    position: absolute;
    left: 0;
    bottom: -3px;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, #19E3D1, #F5C542, #FF2A85, #8B3DFF);
    background-size: 200% 100%;
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    pointer-events: none;
}

a.nav-link:hover::after,
.project-link:hover::after,
.contact-link:hover::after {
    transform: scaleX(1);
    animation: linkGlitchGradFlow 1.4s linear infinite;
}

@keyframes linkGlitchGradFlow {
    0% { background-position: 0% 50%; }
    100% { background-position: 200% 50%; }
}

/* --- CARDS GLITCHED-OUT COLOR GRADIENT EFFECT --- */
.project-card,
.expertise-card,
.cert-card,
.glass-card,
.stat-card,
.code-block-visual,
.bday-card,
.hero-about-tile,
.nano-chat-card {
    position: relative;
    transition: transform 0.25s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease, border-color 0.25s ease !important;
}

/* Top Accent Glitch Gradient Bar for Cards */
.project-card::after,
.expertise-card::after,
.cert-card::after,
.stat-card::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, #19E3D1 0%, #F5C542 33%, #FF2A85 66%, #8B3DFF 100%);
    background-size: 250% 100%;
    opacity: 0;
    transition: opacity 0.3s ease;
    pointer-events: none;
    z-index: 4;
    border-radius: 1rem 1rem 0 0;
}

.project-card:hover::after,
.expertise-card:hover::after,
.cert-card:hover::after,
.stat-card:hover::after {
    opacity: 1;
    animation: cardTopGradSweep 2s linear infinite;
}

@keyframes cardTopGradSweep {
    0% { background-position: 0% 50%; }
    100% { background-position: 250% 50%; }
}

/* Card Hover Glitch Chromatic Border & Glow */
.project-card:hover,
.expertise-card:hover,
.cert-card:hover,
.stat-card:hover,
.code-block-visual:hover,
.bday-card:hover,
.hero-about-tile:hover,
.nano-chat-card:hover {
    border-color: #19E3D1 !important;
    box-shadow: 
        -4px 0 22px rgba(25, 227, 209, 0.55),
        4px 0 22px rgba(255, 42, 133, 0.45),
        0 0 35px rgba(245, 197, 66, 0.35),
        0 14px 45px rgba(0, 0, 0, 0.85) !important;
}

/* Specular + Scanline Interior Hologram */
.cp-3d-card:hover::before {
    opacity: 1 !important;
    background: 
        radial-gradient(circle 280px at var(--card-mouse-x, 50%) var(--card-mouse-y, 50%), rgba(25, 227, 208, 0.35), rgba(242, 193, 78, 0.22) 40%, rgba(255, 42, 133, 0.18) 65%, transparent 85%),
        repeating-linear-gradient(0deg, transparent, transparent 3px, rgba(25, 227, 209, 0.04) 3px, rgba(25, 227, 209, 0.04) 6px) !important;
}

/* --- 5. GEN Z CHAOTIC KINETIC MARQUEE TICKER & TELEMETRY ACCENTS --- */
.cyber-marquee-section {
    position: relative;
    width: 100%;
    overflow: hidden;
    background: rgba(10, 5, 20, 0.82);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-top: 1px solid rgba(25, 227, 209, 0.35);
    border-bottom: 1px solid rgba(245, 197, 66, 0.35);
    box-shadow: 0 0 25px rgba(25, 227, 209, 0.18), inset 0 0 15px rgba(139, 61, 255, 0.15);
    padding: 0.85rem 0;
    z-index: 12;
    margin: 1.5rem 0 2.5rem 0;
    user-select: none;
}

.cyber-marquee-track {
    display: flex;
    width: max-content;
    animation: marqueeScroll 26s linear infinite;
    will-change: transform;
}

.cyber-marquee-section:hover .cyber-marquee-track {
    animation-play-state: paused;
}

@keyframes marqueeScroll {
    0% { transform: translate3d(0, 0, 0); }
    100% { transform: translate3d(-50%, 0, 0); }
}

.cyber-marquee-group {
    display: flex;
    align-items: center;
    gap: 2rem;
    padding-right: 2rem;
}

.marquee-item {
    display: inline-flex;
    align-items: center;
    gap: 0.65rem;
    font-family: 'Space Grotesk', var(--font-headings);
    font-size: 0.88rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #f1f5f9;
    white-space: nowrap;
    cursor: default;
    transition: transform 0.2s ease, color 0.2s ease;
}

.marquee-item:hover {
    color: #19E3D1;
    transform: scale(1.08);
}

.marquee-star {
    color: #F5C542;
    font-size: 0.85rem;
    animation: marqueeStarSpin 4s linear infinite;
}

@keyframes marqueeStarSpin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.marquee-pill {
    padding: 0.2rem 0.65rem;
    border-radius: 12px;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    background: rgba(25, 227, 209, 0.15);
    border: 1px solid #19E3D1;
    color: #19E3D1;
    box-shadow: 0 0 10px rgba(25, 227, 209, 0.3);
}

.marquee-pill.gold {
    background: rgba(245, 197, 66, 0.15);
    border-color: #F5C542;
    color: #F5C542;
    box-shadow: 0 0 10px rgba(245, 197, 66, 0.3);
}

.marquee-pill.pink {
    background: rgba(255, 42, 133, 0.15);
    border-color: #FF2A85;
    color: #FF2A85;
    box-shadow: 0 0 10px rgba(255, 42, 133, 0.3);
}

.marquee-pill.purple {
    background: rgba(139, 61, 255, 0.15);
    border-color: #8B3DFF;
    color: #8B3DFF;
    box-shadow: 0 0 10px rgba(139, 61, 255, 0.3);
}

/* Telemetry Header Badges */
.cyber-telemetry-strip {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'Space Grotesk', monospace;
    font-size: 0.76rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: #19E3D1;
    margin-bottom: 0.6rem;
    background: rgba(18, 9, 32, 0.7);
    border: 1px solid rgba(25, 227, 209, 0.3);
    padding: 0.28rem 0.8rem;
    border-radius: 4px;
    box-shadow: 0 0 12px rgba(25, 227, 209, 0.2);
}

.cyber-telemetry-strip .telemetry-bracket {
    color: #F5C542;
    font-weight: 900;
}

.cyber-telemetry-strip .telemetry-pulse {
    width: 6px;
    height: 6px;
    background: #19E3D1;
    border-radius: 50%;
    display: inline-block;
    box-shadow: 0 0 8px #19E3D1;
    animation: telemetryPulseAnim 1.4s ease-in-out infinite alternate;
}

@keyframes telemetryPulseAnim {
    0% { transform: scale(0.8); opacity: 0.6; }
    100% { transform: scale(1.3); opacity: 1; box-shadow: 0 0 12px #19E3D1; }
}

.cyber-telemetry-strip .telemetry-flux {
    color: #ffd873;
    font-size: 0.72rem;
    opacity: 0.9;
}

/* Gen Z Holographic Project Card Stickers */
.holo-sticker {
    position: absolute;
    top: 12px;
    right: 12px;
    z-index: 6;
    padding: 0.25rem 0.65rem;
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.7rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border-radius: 4px;
    pointer-events: none;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
    transform: rotate(2.5deg);
    transition: transform 0.25s ease;
}

.holo-sticker-cyan {
    background: linear-gradient(135deg, rgba(25, 227, 209, 0.9), rgba(139, 61, 255, 0.9));
    border: 1px solid #19E3D1;
    color: #07060B;
    box-shadow: 0 0 12px rgba(25, 227, 209, 0.5);
}

.holo-sticker-pink {
    background: linear-gradient(135deg, rgba(255, 42, 133, 0.9), rgba(245, 197, 66, 0.9));
    border: 1px solid #FF2A85;
    color: #07060B;
    box-shadow: 0 0 12px rgba(255, 42, 133, 0.5);
    transform: rotate(-2.5deg);
}

.project-card:hover .holo-sticker {
    transform: rotate(0deg) scale(1.08);
}
"""

content = content + glitch_genz_system

# Write back in CRLF format
content_crlf = content.replace('\r\n', '\n').replace('\n', '\r\n')
with open(style_path, 'w', encoding='utf-8') as f:
    f.write(content_crlf)

print("style.css successfully updated with Glitch and Gen Z system!")
