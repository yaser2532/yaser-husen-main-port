# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pos1 = html.find('<div class="about-visual')
pos_end = html.find('</div>\n\n\n\n            </div>\n\n\n\n        </div>\n\n\n\n    </section>', pos1)
assert pos1 != -1 and pos_end != -1, "About visual block bounds not found in index.html"

new_about_visual = """<div class="about-visual">
                    <!-- Cyberpunk Terminal IDE -->
                    <div class="code-block-visual" data-drone-type="code-card">
                        <div class="terminal-header">
                            <div class="terminal-dots">
                                <span class="dot dot-close"></span>
                                <span class="dot dot-minimize"></span>
                                <span class="dot dot-expand"></span>
                            </div>
                            <div class="terminal-title">
                                <span class="terminal-icon">⚡</span>
                                <span class="terminal-filename">skills.matrix.ts</span>
                            </div>
                            <div class="terminal-badge">
                                <span class="pulse-indicator"></span>
                                <span class="badge-text">v2.6_ACTIVE</span>
                            </div>
                        </div>
                        <div class="terminal-body">
                            <pre class="terminal-pre"><code><span class="drone-code-line"><span class="code-line-num">01</span><span class="code-kw">export const</span> <span class="code-var">competencies</span>: <span class="code-type">SkillMatrix</span> <span class="code-op">=</span> <span class="code-punct">[</span></span>
<span class="drone-code-line"><span class="code-line-num">02</span>  <span class="code-str">'Bilingual / Native-level English'</span><span class="code-punct">,</span></span>
<span class="drone-code-line"><span class="code-line-num">03</span>  <span class="code-str">'Python &amp; JavaScript'</span><span class="code-punct">,</span></span>
<span class="drone-code-line"><span class="code-line-num">04</span>  <span class="code-str">'Data Analysis &amp; Advanced SQL'</span><span class="code-punct">,</span></span>
<span class="drone-code-line"><span class="code-line-num">05</span>  <span class="code-str">'Full-Stack Web Development'</span><span class="code-punct">,</span></span>
<span class="drone-code-line"><span class="code-line-num">06</span>  <span class="code-str">'Autonomous Agentic Architecture'</span><span class="code-punct">,</span></span>
<span class="drone-code-line"><span class="code-line-num">07</span>  <span class="code-str">'Vertex AI &amp; Gemini Live API'</span><span class="code-punct">,</span></span>
<span class="drone-code-line"><span class="code-line-num">08</span>  <span class="code-str">'LLM Fine-Tuning &amp; RAG Pipelines'</span><span class="code-punct">,</span></span>
<span class="drone-code-line"><span class="code-line-num">09</span>  <span class="code-str">'High-Performance Cloud Infrastructure'</span></span>
<span class="drone-code-line"><span class="code-line-num">10</span><span class="code-punct">];</span></span></code></pre>
                        </div>
                    </div>
                </div>"""

html = html[:pos1] + new_about_visual + html[pos_end:]
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("1. Successfully updated index.html!")

# 2. Update assets/css/drones.css
with open('assets/css/drones.css', 'r', encoding='utf-8') as f:
    dcss = f.read()

old_dcss_code = """/* 4. Code-IDE Card Line-by-Line Reveal by Clip */
.drone-code-line {
    display: block;
    position: relative;
    clip-path: inset(0 100% 0 0);
    transition: clip-path 0.14s cubic-bezier(0.16, 1, 0.3, 1);
}

.drone-code-line.revealed {
    clip-path: inset(0 0 0 0) !important;
}"""

new_dcss_code = """/* 4. Code-IDE Card Line-by-Line Reveal by Clip */
.drone-code-line {
    display: block;
    position: relative;
    clip-path: inset(0 0 0 0);
    opacity: 1;
    transition: clip-path 0.16s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.16s ease;
}

html.drones-active .code-block-visual[data-drone-state="pulling"] .drone-code-line:not(.revealed) {
    clip-path: inset(0 100% 0 0);
    opacity: 0.2;
}

.drone-code-line.revealed,
.code-block-visual[data-drone-state="built"] .drone-code-line,
.code-block-visual .drone-code-line,
html:not(.drones-active) .drone-code-line {
    clip-path: inset(0 0 0 0) !important;
    opacity: 1 !important;
}"""

assert old_dcss_code in dcss, "old_dcss_code not found in drones.css"
dcss = dcss.replace(old_dcss_code, new_dcss_code, 1)

with open('assets/css/drones.css', 'w', encoding='utf-8') as f:
    f.write(dcss)
print("2. Successfully updated assets/css/drones.css!")

# 3. Update assets/css/style.css
with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    scss = f.read()

pos_cb = scss.find('.code-block-visual {')
pos_cb_end = scss.find('/* ==========================================================================', pos_cb)
assert pos_cb != -1 and pos_cb_end != -1, "code-block-visual block not found in style.css"

new_terminal_css = """.about-visual {
    position: relative;
    width: 100%;
    opacity: 1 !important;
    transform: none !important;
}

.code-block-visual {
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

.var { color: #f2c14e; }

"""

scss = scss[:pos_cb] + new_terminal_css + scss[pos_cb_end:]
with open('assets/css/style.css', 'w', encoding='utf-8') as f:
    f.write(scss)
print("3. Successfully updated assets/css/style.css!")

# 4. Update assets/js/drones.js
with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    djs = f.read()

# A. Smaller dot elements: 2.2px to 3.85px (was 3.2px to 5.6px)
pos_size = djs.find('this.size = 3.2')
pos_size_end = djs.find(';', pos_size)
djs = djs[:pos_size] + 'this.size = 2.2 + (id % 4) * 0.55' + djs[pos_size_end:]

# B. Smaller drawing radii in Drone.draw
pos_draw_halo = djs.find('ctx.arc(this.x, this.y, this.size * 2.4')
if pos_draw_halo != -1:
    djs = djs.replace('ctx.arc(this.x, this.y, this.size * 2.4', 'ctx.arc(this.x, this.y, this.size * 2.0)', 1)

pos_draw_core = djs.find('ctx.arc(this.x, this.y, this.size * 0.95')
if pos_draw_core != -1:
    djs = djs.replace('ctx.arc(this.x, this.y, this.size * 0.95', 'ctx.arc(this.x, this.y, this.size * 0.88)', 1)

pos_draw_center = djs.find('ctx.arc(this.x, this.y, this.size * 0.40')
if pos_draw_center != -1:
    djs = djs.replace('ctx.arc(this.x, this.y, this.size * 0.40', 'ctx.arc(this.x, this.y, this.size * 0.36)', 1)

# C. Update finishElement and finishElementInstantly to reveal code lines and activate about-visual
old_finish_fn = """    function finishElement(item) {

        item.state = 'built';

        item.el.setAttribute('data-drone-state', 'built');

        item.el.style.transform = '';

        item.el.style.opacity = '';

        item.el.style.filter = '';

        item.el.style.willChange = '';



        if (item.el.classList.contains('scroll-reveal')) {

            item.el.classList.add('active');

        }



        // Snap sparks

        const r = item.el.getBoundingClientRect();

        emitSparks(r.left + 12, r.top + 10, 6);

        emitSparks(r.right - 12, r.top + 10, 6);

    }



    function finishElementInstantly(item) {

        if (item.state === 'built') return;

        item.state = 'built';

        item.el.setAttribute('data-drone-state', 'built');

        item.el.style.transform = '';

        item.el.style.opacity = '';

        item.el.style.filter = '';

        item.el.style.willChange = '';

        if (item.el.classList.contains('scroll-reveal')) {

            item.el.classList.add('active');

        }

        if (item.crew && item.crew.length) {

            returnCrew(item.crew, performance.now());

        }

    }"""

new_finish_fn = """    function finishElement(item) {

        item.state = 'built';

        item.el.setAttribute('data-drone-state', 'built');

        item.el.style.transform = '';

        item.el.style.opacity = '';

        item.el.style.filter = '';

        item.el.style.willChange = '';



        if (item.el.classList.contains('scroll-reveal')) {

            item.el.classList.add('active');

        }

        if (item.el.parentElement && item.el.parentElement.classList.contains('about-visual')) {

            item.el.parentElement.classList.add('active');

        }



        // Ensure all lines in code-IDE visual cards are immediately 100% revealed and unclipped

        const codeLines = item.el.querySelectorAll('.drone-code-line, .code-line');

        if (codeLines.length) {

            codeLines.forEach(l => {

                l.classList.add('revealed');

                l.style.clipPath = 'inset(0 0 0 0)';

                l.style.opacity = '1';

            });

        }



        // Snap sparks

        const r = item.el.getBoundingClientRect();

        emitSparks(r.left + 12, r.top + 10, 6);

        emitSparks(r.right - 12, r.top + 10, 6);

    }



    function finishElementInstantly(item) {

        if (item.state === 'built') return;

        item.state = 'built';

        item.el.setAttribute('data-drone-state', 'built');

        item.el.style.transform = '';

        item.el.style.opacity = '';

        item.el.style.filter = '';

        item.el.style.willChange = '';

        if (item.el.classList.contains('scroll-reveal')) {

            item.el.classList.add('active');

        }

        if (item.el.parentElement && item.el.parentElement.classList.contains('about-visual')) {

            item.el.parentElement.classList.add('active');

        }



        // Ensure all lines in code-IDE visual cards are immediately 100% revealed and unclipped

        const codeLines = item.el.querySelectorAll('.drone-code-line, .code-line');

        if (codeLines.length) {

            codeLines.forEach(l => {

                l.classList.add('revealed');

                l.style.clipPath = 'inset(0 0 0 0)';

                l.style.opacity = '1';

            });

        }



        if (item.crew && item.crew.length) {

            returnCrew(item.crew, performance.now());

        }

    }"""

assert old_finish_fn in djs, "old_finish_fn not found in drones.js"
djs = djs.replace(old_finish_fn, new_finish_fn, 1)

with open('assets/js/drones.js', 'w', encoding='utf-8') as f:
    f.write(djs)
print("4. Successfully updated assets/js/drones.js!")
