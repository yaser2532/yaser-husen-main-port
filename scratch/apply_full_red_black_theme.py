with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_l1 = '<span class="drone-code-line"><span class="code-line-num">01</span><span class="code-kw">export const</span> <span class="code-var">competencies</span>: <span class="code-type">SkillMatrix</span> <span class="code-op">=</span> <span class="code-punct">[</span></span>'
new_l1 = '<span class="drone-code-line"><span class="code-line-num">01</span><span class="code-kw">const</span> <span class="code-var">skills</span> <span class="code-op">=</span> <span class="code-punct">[</span></span>'

if old_l1 in html:
    html = html.replace(old_l1, new_l1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated index.html line 01 to const skills = [")

# Now update assets/css/style.css
with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Update :root with blood red variables
if '--blood-primary:' not in css:
    css = css.replace(
        ':root {',
        ''':root {
    /* Cyberpunk Dark Blood Red Design Tokens */
    --blood-darkest: #0a0103;
    --blood-deep: #200206;
    --blood-rich: #4A000A;
    --blood-primary: #8B0000;
    --blood-crimson: #C4122D;
    --blood-neon: #FF1E42;
    --blood-glow: rgba(180, 20, 40, 0.35);
    --shadow-blood: 0 0 25px rgba(180, 20, 40, 0.28);'''
    )
    print("Added dark blood red variables to :root!")

# 2. Update .code-block-visual and terminal styles to original red & black
old_code_block_css = """/* ==========================================================================
   Code Block Visual (Skills Terminal IDE Component)
   ========================================================================== */
.code-block-visual {
    width: 100%;
    max-width: 100%;
    min-width: 0;
    box-sizing: border-box;
    background: rgba(10, 6, 20, 0.88);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 12px;
    border: 1px solid rgba(25, 227, 209, 0.25);
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.65), 0 0 24px rgba(25, 227, 209, 0.08);
    position: relative;
    overflow: hidden;
    padding: 0;
    font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
    font-size: 0.88rem;
    line-height: 1.6;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.code-block-visual:hover {
    border-color: rgba(245, 197, 66, 0.50);
    box-shadow: 0 16px 44px rgba(0, 0, 0, 0.75), 0 0 32px rgba(245, 197, 66, 0.16);
}

.terminal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.75rem 1.25rem;
    background: rgba(18, 12, 34, 0.95);
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
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

.dot-close { background: #FF5F56; box-shadow: 0 0 6px rgba(255, 95, 86, 0.5); }
.dot-minimize { background: #FFBD2E; box-shadow: 0 0 6px rgba(255, 189, 46, 0.5); }
.dot-expand { background: #27C93F; box-shadow: 0 0 6px rgba(39, 201, 63, 0.5); }

.terminal-title {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.8rem;
    color: #94A3B8;
    font-weight: 500;
}

.terminal-filename {
    color: #E2E8F0;
    letter-spacing: 0.3px;
}

.terminal-badge {
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.68rem;
    font-weight: 700;
    color: var(--accent-turquoise, #19E3D1);
    letter-spacing: 0.8px;
    background: rgba(25, 227, 209, 0.10);
    padding: 0.2rem 0.55rem;
    border-radius: 100px;
    border: 1px solid rgba(25, 227, 209, 0.25);
}

.pulse-indicator {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #19E3D1;
    box-shadow: 0 0 8px #19E3D1;
    animation: pulseGlow 1.8s infinite ease-in-out;
}

@keyframes pulseGlow {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.4; transform: scale(0.85); }
}

.terminal-body {
    padding: 1.25rem 1.4rem;
    overflow-x: auto;
}

.terminal-pre {
    margin: 0;
    font-family: inherit;
    font-size: inherit;
    background: transparent;
    padding: 0;
    border: none;
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
    color: rgba(148, 163, 184, 0.35);
    user-select: none;
    font-size: 0.78rem;
}

.code-kw {
    color: #F43F5E;
    font-weight: 600;
}

.code-var {
    color: #F5C542;
    font-weight: 600;
}

.code-type {
    color: #8B3DFF;
    font-weight: 500;
}

.code-op {
    color: #F5C542;
}

.code-str {
    color: #19E3D1;
    text-shadow: 0 0 8px rgba(25, 227, 209, 0.25);
}

.code-punct {
    color: #E2E8F0;
}

.keyword { color: #f43f5e; }

.var { color: #f2c14e; }"""

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

.var { color: #f8fafc; }"""

if old_code_block_css in css:
    css = css.replace(old_code_block_css, new_code_block_css)
    print("Replaced code block CSS with original Red & Black theme!")
else:
    print("Warning: old_code_block_css not matched verbatim, looking for slice...")

with open('assets/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Saved assets/css/style.css successfully!")
