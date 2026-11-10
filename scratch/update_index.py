import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove the hero-scroll-pill and hero-horizon-beam
old_seam = """        <!-- Smooth Hero to Content Transition Horizon Seam -->

        <div class="hero-transition-seam" aria-hidden="true">

            <div class="hero-horizon-beam"></div>

            <a href="#profile-expertise" class="hero-scroll-pill" aria-label="Scroll to Explore">

                <span class="scroll-mouse-icon"><span class="scroll-wheel"></span></span>

                <span class="scroll-label">Scroll to Explore</span>

            </a>

        </div>"""

new_seam = """        <!-- Smooth Hero to Content Blended Transition Seam -->
        <div class="hero-transition-seam" aria-hidden="true"></div>"""

# Normalize spaces to match
assert "hero-scroll-pill" in html, "hero-scroll-pill not found in index.html"

# Regex replace for seam
html = re.sub(
    r'<!-- Smooth Hero to Content Transition Horizon Seam -->\s*<div class="hero-transition-seam" aria-hidden="true">.*?</div>\s*</div>',
    new_seam,
    html,
    flags=re.DOTALL
)

# 2. Add CRT Static Noise Overlay before </body>
static_overlay = """    <!-- CRT Static Noise Easter Egg Overlay -->
    <div id="static-noise-overlay" class="static-noise-overlay" aria-hidden="true">
        <canvas id="static-noise-canvas"></canvas>
        <div class="static-noise-scanlines"></div>
        <div class="static-noise-toast" id="static-noise-toast">
            <span class="static-toast-tag">⚡ EASTER EGG UNLOCKED</span>
            <span class="static-toast-msg" id="static-toast-msg">SYSTEM ENTROPY OVERCLOCKED // CHAOS PROTOCOL 2026 ACTIVE</span>
        </div>
    </div>
"""

if 'id="static-noise-overlay"' not in html:
    html = html.replace('</body>', static_overlay + '\n</body>')

# 3. Enhance Project Cards with Gen Z Telemetry Tags & Torn Paper Easter Eggs
# Card 1: AEEA Platform
c1_target = '<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">\n\n                    <span class="holo-sticker holo-sticker-cyan">⚡ AI-NATIVE</span>'
c1_repl = """<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">
                    <div class="torn-paper-sticker torn-stamp-pink" data-easter-egg="chaos" title="⚡ CLASSIFIED // CLICK FOR EASTER EGG"><span class="torn-label">DO NOT DEPLOY // 2026</span></div>
                    <div class="prj-cyber-index"><span>// PRJ-01</span><span class="prj-sys-spec">SYS.AEEA_CORE</span></div>
                    <span class="holo-sticker holo-sticker-cyan">⚡ AI-NATIVE</span>"""

# Card 2: AEEA + AMLT Simulator
c2_target = '<article class="project-card glass-card scroll-reveal fade-up" data-category="interactive">\n\n                    <div class="project-img-container">'
c2_repl = """<article class="project-card glass-card scroll-reveal fade-up" data-category="interactive">
                    <div class="prj-cyber-index"><span>// PRJ-02</span><span class="prj-sys-spec">SIM.AMLT_TELEMETRY</span></div>
                    <span class="holo-sticker holo-sticker-pink">🎮 SIMULATOR</span>
                    <div class="project-img-container">"""

# Card 3: ATTF Data Cleaning Platform
c3_target = '<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">\n\n                    <div class="project-img-container">'
c3_repl = """<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">
                    <div class="torn-paper-sticker torn-stamp-yellow" data-easter-egg="static" title="📺 CRT STATIC NOISE // CLICK TO TRIGGER"><span class="torn-label">RAW TRUTH // 100% UNFILTERED</span></div>
                    <div class="prj-cyber-index"><span>// PRJ-03</span><span class="prj-sys-spec">DATA.ATTF_ENGINE</span></div>
                    <div class="project-img-container">"""

# Card 4: Gym Website
c4_target = '<article class="project-card glass-card scroll-reveal fade-up" data-category="ui-saas">\n\n                    <div class="project-img-container">'
c4_repl = """<article class="project-card glass-card scroll-reveal fade-up" data-category="ui-saas">
                    <div class="prj-cyber-index"><span>// PRJ-04</span><span class="prj-sys-spec">UI.KINETIC_FITNESS</span></div>
                    <span class="holo-sticker holo-sticker-cyan">🔥 WEB.APP</span>
                    <div class="project-img-container">"""

# Card 5: Vertex AI Chatbot
c5_target = '<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">\n\n                    <div class="project-img-container">'
c5_repl = """<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">
                    <div class="prj-cyber-index"><span>// PRJ-05</span><span class="prj-sys-spec">LLM.VERTEX_PROMPT</span></div>
                    <span class="holo-sticker holo-sticker-pink">⚡ AI AGENT</span>
                    <div class="project-img-container">"""

# Card 6: Automated Code Reviewer
c6_target = '<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">\n\n                    <div class="project-img-container">'
c6_repl = """<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">
                    <div class="torn-paper-sticker torn-stamp-cyan" data-easter-egg="code" title="⚡ DEV SECRETS // CLICK ME"><span class="torn-label">ZERO MERGE CONFLICTS</span></div>
                    <div class="prj-cyber-index"><span>// PRJ-06</span><span class="prj-sys-spec">AST.SYNTAX_AUDIT</span></div>
                    <div class="project-img-container">"""

# Card 7: Cloud Infrastructure Manager
c7_target = '<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">\n\n                    <div class="project-img-container">'
c7_repl = """<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">
                    <div class="prj-cyber-index"><span>// PRJ-07</span><span class="prj-sys-spec">CLOUD.TERRAFORM_K8S</span></div>
                    <div class="project-img-container">"""

# Card 8: Sentiment Analysis API
c8_target = '<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">\n\n                    <div class="project-img-container">'
c8_repl = """<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">
                    <div class="prj-cyber-index"><span>// PRJ-08</span><span class="prj-sys-spec">NLP.BERT_SENTIMENT</span></div>
                    <div class="project-img-container">"""

# Card 9: Birthday Wishes Generator
c9_target = '<article class="project-card glass-card scroll-reveal fade-up" data-category="interactive">\n\n                    <div class="project-img-container">'
c9_repl = """<article class="project-card glass-card scroll-reveal fade-up" data-category="interactive">
                    <div class="torn-paper-sticker torn-stamp-white" data-easter-egg="entropy" title="🎂 BIRTHDAY PROTOCOL // CLICK FOR SURPRISE"><span class="torn-label">CHAOS VERIFIED // V3.2</span></div>
                    <div class="prj-cyber-index"><span>// PRJ-09</span><span class="prj-sys-spec">LAB.INTERACTIVE_SYNTH</span></div>
                    <div class="project-img-container">"""

# Perform replacements
replacements = [
    (c1_target, c1_repl),
    (c2_target, c2_repl),
    (c3_target, c3_repl),
    (c4_target, c4_repl),
    (c5_target, c5_repl),
    (c6_target, c6_repl),
    (c7_target, c7_repl),
    (c8_target, c8_repl),
    (c9_target, c9_repl)
]

for old, new in replacements:
    # Normalize \r\n to \n for matching
    html_norm = html.replace('\r\n', '\n')
    old_norm = old.replace('\r\n', '\n')
    if old_norm in html_norm:
        html_norm = html_norm.replace(old_norm, new, 1)
        html = html_norm
        print(f"Replaced card header: {new.splitlines()[1][:40]}")
    else:
        print(f"Warning: target not matched directly for a card. Finding with regex...")

with open('index.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(html.replace('\r\n', '\n').replace('\n', '\r\n'))

print("Updated index.html successfully!")
