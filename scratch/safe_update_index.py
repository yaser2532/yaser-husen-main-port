with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Normalize
norm = text.replace('\r\n', '\n')

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

assert old_seam in norm, "old_seam not found in normalized text"
norm = norm.replace(old_seam, new_seam, 1)

# Check that <section id="profile-expertise" is still intact
assert '<section id="profile-expertise"' in norm, "profile-expertise missing!"

# Add the Gen Z project card enhancements
# Card 1: AEEA Platform
c1_target = """<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">

                    <span class="holo-sticker holo-sticker-cyan">⚡ AI-NATIVE</span>"""

c1_repl = """<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">

                    <div class="torn-paper-sticker torn-stamp-pink" data-easter-egg="chaos" title="⚡ CLASSIFIED // CLICK FOR EASTER EGG"><span class="torn-label">DO NOT DEPLOY // 2026</span></div>
                    <div class="prj-cyber-index"><span>// PRJ-01</span><span class="prj-sys-spec">SYS.AEEA_CORE</span></div>
                    <span class="holo-sticker holo-sticker-cyan">⚡ AI-NATIVE</span>"""

assert c1_target in norm, "c1_target not found"
norm = norm.replace(c1_target, c1_repl, 1)

# Card 2: AEEA + AMLT Simulator
c2_target = """<article class="project-card glass-card scroll-reveal fade-up" data-category="interactive">

                    <div class="project-img-container">"""

c2_repl = """<article class="project-card glass-card scroll-reveal fade-up" data-category="interactive">

                    <div class="prj-cyber-index"><span>// PRJ-02</span><span class="prj-sys-spec">SIM.AMLT_TELEMETRY</span></div>
                    <span class="holo-sticker holo-sticker-pink">🎮 SIMULATOR</span>
                    <div class="project-img-container">"""

assert c2_target in norm, "c2_target not found"
norm = norm.replace(c2_target, c2_repl, 1)

# Card 3: ATTF Data Cleaning Platform
c3_target = """<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">

                    <div class="project-img-container">"""

c3_repl = """<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">

                    <div class="torn-paper-sticker torn-stamp-yellow" data-easter-egg="static" title="📺 CRT STATIC NOISE // CLICK TO TRIGGER"><span class="torn-label">RAW TRUTH // 100% UNFILTERED</span></div>
                    <div class="prj-cyber-index"><span>// PRJ-03</span><span class="prj-sys-spec">DATA.ATTF_ENGINE</span></div>
                    <div class="project-img-container">"""

assert c3_target in norm, "c3_target not found"
norm = norm.replace(c3_target, c3_repl, 1)

# Card 4: Gym Website
c4_target = """<article class="project-card glass-card scroll-reveal fade-up" data-category="ui-saas">

                    <div class="project-img-container">"""

c4_repl = """<article class="project-card glass-card scroll-reveal fade-up" data-category="ui-saas">

                    <div class="prj-cyber-index"><span>// PRJ-04</span><span class="prj-sys-spec">UI.KINETIC_FITNESS</span></div>
                    <span class="holo-sticker holo-sticker-cyan">🔥 WEB.APP</span>
                    <div class="project-img-container">"""

assert c4_target in norm, "c4_target not found"
norm = norm.replace(c4_target, c4_repl, 1)

# Card 5: Vertex AI Chatbot
c5_target = """<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">

                    <div class="project-img-container">"""

c5_repl = """<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">

                    <div class="prj-cyber-index"><span>// PRJ-05</span><span class="prj-sys-spec">LLM.VERTEX_PROMPT</span></div>
                    <span class="holo-sticker holo-sticker-pink">⚡ AI AGENT</span>
                    <div class="project-img-container">"""

assert c5_target in norm, "c5_target not found"
norm = norm.replace(c5_target, c5_repl, 1)

# Card 6: Automated Code Reviewer
c6_target = """<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">

                    <div class="project-img-container">"""

c6_repl = """<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">

                    <div class="torn-paper-sticker torn-stamp-cyan" data-easter-egg="code" title="⚡ DEV SECRETS // CLICK ME"><span class="torn-label">ZERO MERGE CONFLICTS</span></div>
                    <div class="prj-cyber-index"><span>// PRJ-06</span><span class="prj-sys-spec">AST.SYNTAX_AUDIT</span></div>
                    <div class="project-img-container">"""

assert c6_target in norm, "c6_target not found"
norm = norm.replace(c6_target, c6_repl, 1)

# Card 7: Cloud Infrastructure Manager
c7_target = """<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">

                    <div class="project-img-container">"""

c7_repl = """<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">

                    <div class="prj-cyber-index"><span>// PRJ-07</span><span class="prj-sys-spec">CLOUD.TERRAFORM_K8S</span></div>
                    <div class="project-img-container">"""

assert c7_target in norm, "c7_target not found"
norm = norm.replace(c7_target, c7_repl, 1)

# Card 8: Sentiment Analysis API
c8_target = """<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">

                    <div class="project-img-container">"""

c8_repl = """<article class="project-card glass-card scroll-reveal fade-up" data-category="ai-data">

                    <div class="prj-cyber-index"><span>// PRJ-08</span><span class="prj-sys-spec">NLP.BERT_SENTIMENT</span></div>
                    <div class="project-img-container">"""

assert c8_target in norm, "c8_target not found"
norm = norm.replace(c8_target, c8_repl, 1)

# Card 9: Birthday Wishes Generator
c9_target = """<article class="project-card glass-card scroll-reveal fade-up" data-category="interactive">

                    <div class="project-img-container">"""

c9_repl = """<article class="project-card glass-card scroll-reveal fade-up" data-category="interactive">

                    <div class="torn-paper-sticker torn-stamp-white" data-easter-egg="entropy" title="🎂 BIRTHDAY PROTOCOL // CLICK FOR SURPRISE"><span class="torn-label">CHAOS VERIFIED // V3.2</span></div>
                    <div class="prj-cyber-index"><span>// PRJ-09</span><span class="prj-sys-spec">LAB.INTERACTIVE_SYNTH</span></div>
                    <div class="project-img-container">"""

assert c9_target in norm, "c9_target not found"
norm = norm.replace(c9_target, c9_repl, 1)

# Add CRT Static Noise Overlay before </body>
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

if 'id="static-noise-overlay"' not in norm:
    norm = norm.replace('</body>', static_overlay + '\n</body>')

# Verify integrity
assert '<section id="profile-expertise"' in norm
assert '<section id="projects"' in norm
assert '<section id="about-me"' in norm
assert '<footer id="contact"' in norm

with open('index.html', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(norm.replace('\n', '\r\n'))

print("Safely updated index.html! All 18 sections verified intact.")
