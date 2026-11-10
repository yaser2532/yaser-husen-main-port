with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

pos1 = css.find('.code-block-visual {')
pos2 = css.find('/* ==========================================================================\n\n   Projects Section')
if pos2 == -1:
    pos2 = css.find('.project-filters {')

new_code_block_css = """/* ==========================================================================
   Code Block Visual - Authentic Original Red & Black Cyberpunk Terminal
   ========================================================================== */
.code-block-visual {
    width: 100%;
    max-width: 100%;
    min-width: 0;
    box-sizing: border-box;
    background: rgba(5, 2, 4, 0.96);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 12px;
    border: 1px solid rgba(180, 20, 40, 0.38);
    box-shadow: 0 16px 42px rgba(0, 0, 0, 0.90), 0 0 28px rgba(139, 0, 0, 0.22), inset 0 0 22px rgba(74, 0, 10, 0.35);
    position: relative;
    overflow: hidden;
    padding: 0;
    font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
    font-size: 0.88rem;
    line-height: 1.6;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.code-block-visual::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, #4A000A 0%, #8B0000 30%, #FF1E42 70%, #66000E 100%);
    z-index: 5;
}

.code-block-visual:hover {
    border-color: rgba(255, 30, 66, 0.70);
    box-shadow: 0 20px 48px rgba(0, 0, 0, 0.95), 0 0 36px rgba(255, 30, 66, 0.32), inset 0 0 28px rgba(139, 0, 0, 0.42);
}

.terminal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1.25rem;
    background: rgba(12, 3, 6, 0.96);
    border-bottom: 1px solid rgba(180, 20, 40, 0.22);
    user-select: none;
}

.terminal-dots {
    display: flex;
    align-items: center;
    gap: 0.45rem;
}

.terminal-dots .dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    display: inline-block;
}

.dot-close {
    background: #FF2A55;
    box-shadow: 0 0 8px rgba(255, 42, 85, 0.75);
}

.dot-minimize {
    background: #8B0000;
    box-shadow: 0 0 4px rgba(139, 0, 0, 0.5);
}

.dot-expand {
    background: #4A000A;
    border: 1px solid rgba(180, 20, 40, 0.4);
}

.terminal-title {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.8rem;
    color: #F8FAFC;
    font-weight: 500;
}

.terminal-icon {
    color: #FF1E42;
    text-shadow: 0 0 8px rgba(255, 30, 66, 0.65);
}

.terminal-filename {
    color: #F8FAFC;
    letter-spacing: 0.3px;
    font-weight: 600;
}

.terminal-badge {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.68rem;
    font-weight: 700;
    color: #FF2A55;
    letter-spacing: 0.8px;
    background: rgba(139, 0, 0, 0.22);
    padding: 0.2rem 0.55rem;
    border-radius: 100px;
    border: 1px solid rgba(255, 42, 85, 0.38);
    box-shadow: 0 0 10px rgba(180, 20, 40, 0.25);
}

.pulse-indicator {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #FF1E42;
    box-shadow: 0 0 8px #FF1E42;
    animation: pulseGlowBlood 1.8s infinite ease-in-out;
}

@keyframes pulseGlowBlood {
    0%, 100% { opacity: 1; transform: scale(1); box-shadow: 0 0 10px #FF1E42; }
    50% { opacity: 0.35; transform: scale(0.8); box-shadow: 0 0 4px #8B0000; }
}

.terminal-body {
    padding: 1.25rem 1.4rem;
    overflow-x: auto;
    background: rgba(5, 2, 4, 0.98);
}

.terminal-pre {
    margin: 0;
    font-family: inherit;
    font-size: inherit;
    background: transparent;
    padding: 0;
    border: none;
    white-space: pre-wrap;
    word-break: break-word;
}

.terminal-pre code {
    display: block;
    background: transparent;
    padding: 0;
    font-family: inherit;
}

.code-line-num {
    display: inline-block;
    width: 2rem;
    color: #661824;
    user-select: none;
    font-size: 0.78rem;
    font-weight: 600;
}

.code-kw {
    color: #F43F5E;
    font-weight: 600;
    text-shadow: 0 0 8px rgba(244, 63, 94, 0.35);
}

.code-var {
    color: #F8FAFC;
    font-weight: 600;
}

.code-type {
    color: #C4122D;
    font-weight: 600;
}

.code-op {
    color: #F43F5E;
}

.code-str {
    color: #F43F5E;
    text-shadow: 0 0 6px rgba(244, 63, 94, 0.35);
    font-weight: 500;
}

.code-punct {
    color: #CBD5E1;
}

.keyword { color: #f43f5e; }

.var { color: #f8fafc; }

"""

css = css[:pos1] + new_code_block_css + css[pos2:]

# Now append the dark blood red key areas enhancement rules to the end of style.css
dark_blood_red_rules = """
/* ==========================================================================
   Cyberpunk Dark Blood Red Key Area Accents
   ========================================================================== */

/* 1. Section Title Cyber Underscore */
.section-title::after {
    content: '';
    display: block;
    width: 52px;
    height: 3px;
    background: linear-gradient(90deg, transparent, #8B0000 30%, #FF1E42 50%, #8B0000 70%, transparent);
    margin: 0.8rem auto 0 auto;
    border-radius: 2px;
    box-shadow: 0 0 10px rgba(255, 30, 66, 0.45);
}

/* 2. Category Filter Buttons */
.filter-btn:hover {
    color: #FF4D6D;
    border-color: rgba(180, 20, 40, 0.45);
    background: rgba(74, 0, 10, 0.25);
    box-shadow: 0 0 12px rgba(139, 0, 0, 0.25);
}

.filter-btn.active {
    color: #FFFFFF !important;
    border-color: rgba(255, 30, 66, 0.65) !important;
    background: linear-gradient(135deg, rgba(74, 0, 10, 0.85) 0%, rgba(139, 0, 0, 0.60) 100%) !important;
    box-shadow: 0 0 18px rgba(180, 20, 40, 0.38), inset 0 0 10px rgba(139, 0, 0, 0.30) !important;
}

/* 3. Featured Projects Badges & Card Hover */
.project-tech-badges .badge,
.project-card .badge {
    font-size: 0.72rem;
    font-weight: 700;
    color: #FF3355;
    background: rgba(45, 4, 8, 0.82);
    border: 1px solid rgba(180, 20, 40, 0.45);
    padding: 3px 0.55rem;
    border-radius: 0.35rem;
    box-shadow: 0 0 8px rgba(139, 0, 0, 0.25);
}

.project-card:hover {
    border-color: rgba(180, 20, 40, 0.50);
    box-shadow: 0 20px 48px rgba(0, 0, 0, 0.88), 0 0 32px rgba(139, 0, 0, 0.24);
}

/* 4. Hero Section Atmosphere & Badges */
.hero-sticker-badge,
.hero-status-pill {
    border-color: rgba(180, 20, 40, 0.45);
    background: rgba(42, 4, 8, 0.60);
    color: #FF3355;
    box-shadow: 0 0 16px rgba(139, 0, 0, 0.25);
}

/* 5. Contact Section Card & Interactive Form Elements */
.contact-form-wrap {
    background: radial-gradient(circle at 50% 0%, rgba(139, 0, 0, 0.14) 0%, rgba(6, 2, 5, 0.92) 65%);
    border: 1px solid rgba(180, 20, 40, 0.32);
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.85), 0 0 30px rgba(139, 0, 0, 0.16);
}

.info-icon {
    background: rgba(74, 0, 10, 0.50);
    border: 1px solid rgba(180, 20, 40, 0.40);
    color: #FF3355;
    box-shadow: 0 0 12px rgba(139, 0, 0, 0.28);
}

.contact-form .btn-primary,
.contact-form button[type="submit"] {
    background: linear-gradient(135deg, #4A000A 0%, #8B0000 50%, #C4122D 100%);
    border: 1px solid rgba(255, 30, 66, 0.5);
    color: #FFFFFF;
    box-shadow: 0 0 22px rgba(180, 20, 40, 0.45);
    transition: var(--transition-fast);
}

.contact-form .btn-primary:hover,
.contact-form button[type="submit"]:hover {
    background: linear-gradient(135deg, #66000E 0%, #A50014 50%, #E61938 100%);
    box-shadow: 0 0 32px rgba(255, 30, 66, 0.65);
    transform: translateY(-2px);
}
"""

css = css + dark_blood_red_rules

with open('assets/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Applied original red & black code block theme + dark blood red key areas successfully!")
