# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add interactive title attributes to the kinetic row elements
old_row = """            <div class="hero-kinetic-row">

                <div class="hero-sticker-badge">

                    <span class="pulse-dot"></span>

                    <span class="sticker-text">STATUS // DEPLOYING INTEL</span>

                </div>

                <div class="hero-clock-pill" id="hero-live-clock">

                    <i class="fa-regular fa-clock"></i> <span id="clock-utc">UTC 00:00:00</span>

                </div>

                <div class="hero-spec-stamp">[AGENTIC_V4.2]</div>

            </div>"""

new_row = """            <div class="hero-kinetic-row">

                <div class="hero-sticker-badge" title="System Status: Operational // Intel Deployed" tabindex="0">

                    <span class="pulse-dot"></span>

                    <span class="sticker-text">STATUS // DEPLOYING INTEL</span>

                </div>

                <div class="hero-clock-pill" id="hero-live-clock" title="Click to toggle Local / UTC Time" tabindex="0">

                    <i class="fa-regular fa-clock"></i> <span id="clock-utc">UTC 00:00:00</span>

                </div>

                <div class="hero-spec-stamp" title="Agentic Architecture Matrix v4.2" tabindex="0">[AGENTIC_V4.2]</div>

            </div>"""

if old_row in html:
    html = html.replace(old_row, new_row)
    print("Updated hero-kinetic-row in index.html with interactive titles & accessibility!")
else:
    print("Warning: old_row not matched verbatim in index.html, checking slice...")
    # Try normalized match
    pos = html.find('class="hero-kinetic-row"')
    if pos != -1:
        end_pos = html.find('</h1>', pos)
        print("Slice around kinetic row:")
        print(repr(html[pos:pos+350]))

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update assets/css/style.css
with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

pos1 = css.find('.hero-kinetic-row {')
pos2 = css.find('.hero-content .eyebrow {')

new_hero_kinetic_css = """/* ==========================================================================
   Hero Kinetic Row & Interactive Elements (Hover Physics & Lighting)
   ========================================================================== */
.hero-kinetic-row {
    display: flex;
    align-items: center;
    gap: 0.85rem;
    flex-wrap: wrap;
    margin-bottom: 1.25rem;
}

/* 1. Hero Sticker Badge (Status Intel) */
.hero-sticker-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    padding: 0.35rem 0.85rem;
    background: rgba(42, 4, 8, 0.65);
    border: 1px solid rgba(180, 20, 40, 0.45);
    color: #FF3355;
    border-radius: 4px;
    box-shadow: 0 0 16px rgba(139, 0, 0, 0.25), inset 0 0 8px rgba(139, 0, 0, 0.15);
    transform: rotate(-1.5deg);
    cursor: pointer;
    user-select: none;
    position: relative;
    transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), 
                box-shadow 0.28s ease, 
                border-color 0.28s ease, 
                background 0.28s ease, 
                color 0.28s ease;
}

.hero-sticker-badge:hover {
    transform: rotate(0deg) scale(1.06) translateY(-3px) !important;
    border-color: #FF1E42 !important;
    background: rgba(139, 0, 0, 0.40) !important;
    color: #FFFFFF !important;
    box-shadow: 0 0 24px rgba(255, 30, 66, 0.75), 
                0 0 45px rgba(180, 20, 40, 0.40), 
                inset 0 0 12px rgba(255, 30, 66, 0.30) !important;
}

.pulse-dot {
    width: 7px;
    height: 7px;
    background: #FF1E42;
    border-radius: 50%;
    box-shadow: 0 0 8px #FF1E42;
    animation: neon-pulse 1.4s infinite ease-in-out;
    transition: background 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease;
}

.hero-sticker-badge:hover .pulse-dot {
    background: #FF1E42 !important;
    box-shadow: 0 0 14px #FF1E42, 0 0 22px rgba(255, 30, 66, 0.9) !important;
    animation: pulseDotFast 0.5s infinite alternate ease-in-out;
}

@keyframes pulseDotFast {
    0% { transform: scale(1); opacity: 1; }
    100% { transform: scale(1.4); opacity: 0.7; }
}

@keyframes neon-pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.35; transform: scale(0.75); }
}

.hero-sticker-badge .sticker-text {
    transition: text-shadow 0.25s ease, letter-spacing 0.25s ease;
}

.hero-sticker-badge:hover .sticker-text {
    text-shadow: 0 0 10px rgba(255, 30, 66, 0.8), 0 0 18px rgba(255, 255, 255, 0.6);
    letter-spacing: 0.11em;
}

/* 2. Hero Live UTC Clock Pill (Interactive Hover & Pulse) */
.hero-clock-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    font-family: 'Courier New', monospace;
    font-size: 0.8rem;
    font-weight: 700;
    color: var(--cp-gold);
    background: rgba(242, 193, 78, 0.10);
    border: 1px solid rgba(242, 193, 78, 0.40);
    padding: 0.35rem 0.85rem;
    border-radius: 2rem;
    box-shadow: 0 0 12px rgba(242, 193, 78, 0.25);
    cursor: pointer;
    user-select: none;
    position: relative;
    transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), 
                box-shadow 0.28s ease, 
                border-color 0.28s ease, 
                background 0.28s ease, 
                color 0.28s ease;
}

.hero-clock-pill:hover {
    transform: translateY(-3px) scale(1.05);
    background: rgba(245, 197, 66, 0.20) !important;
    border-color: #F5C542 !important;
    color: #FFFFFF !important;
    box-shadow: 0 0 22px rgba(245, 197, 66, 0.65), 
                0 0 40px rgba(25, 227, 209, 0.35), 
                inset 0 0 12px rgba(245, 197, 66, 0.25) !important;
}

.hero-clock-pill i {
    transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1), color 0.3s ease;
}

.hero-clock-pill:hover i {
    transform: rotate(180deg);
    color: #19E3D1;
}

.hero-clock-pill #clock-utc {
    transition: all 0.25s ease;
}

.hero-clock-pill:hover #clock-utc {
    color: #FFFFFF;
    text-shadow: 0 0 10px rgba(245, 197, 66, 0.9), 0 0 20px rgba(255, 255, 255, 0.6);
    letter-spacing: 0.04em;
}

.hero-clock-pill:active {
    transform: translateY(-1px) scale(1.02);
    box-shadow: 0 0 30px rgba(25, 227, 209, 0.85);
}

.hero-clock-pill.clock-ping {
    animation: clockPing 0.35s ease-out;
}

@keyframes clockPing {
    0% { transform: scale(1.05); box-shadow: 0 0 40px rgba(245, 197, 66, 0.9); }
    50% { transform: scale(1.12); box-shadow: 0 0 60px rgba(25, 227, 209, 0.95); }
    100% { transform: scale(1.05); }
}

/* 3. Hero Spec Stamp [AGENTIC_V4.2] */
.hero-spec-stamp {
    font-family: 'Space Grotesk', monospace;
    font-size: 0.75rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    color: rgba(180, 160, 220, 0.85);
    border: 1px dashed rgba(180, 160, 220, 0.40);
    padding: 0.3rem 0.65rem;
    border-radius: 2px;
    cursor: pointer;
    user-select: none;
    position: relative;
    transition: transform 0.28s cubic-bezier(0.16, 1, 0.3, 1), 
                box-shadow 0.28s ease, 
                border-color 0.28s ease, 
                background 0.28s ease, 
                color 0.28s ease, 
                letter-spacing 0.28s ease;
}

.hero-spec-stamp:hover {
    transform: translateY(-3px) scale(1.06);
    color: #19E3D1 !important;
    border-color: #19E3D1 !important;
    border-style: solid !important;
    background: rgba(25, 227, 209, 0.15) !important;
    box-shadow: 0 0 22px rgba(25, 227, 209, 0.65), 
                0 0 35px rgba(139, 61, 255, 0.30), 
                inset 0 0 10px rgba(25, 227, 209, 0.20) !important;
    letter-spacing: 0.12em !important;
    text-shadow: 0 0 10px rgba(25, 227, 209, 0.8);
}

"""

if pos1 != -1 and pos2 != -1:
    css = css[:pos1] + new_hero_kinetic_css + css[pos2:]
    print("Replaced hero-kinetic-row styles in style.css!")
else:
    print("Warning: slice pos1/pos2 not found in style.css")

# Also ensure .hero-subtitle hover exists
if '.hero-subtitle:hover' not in css:
    css = css.replace(
        '.hero-subtitle {',
        """.hero-subtitle:hover {
    color: #FFFFFF !important;
    transform: translateX(4px);
    text-shadow: 0 0 20px rgba(25, 227, 209, 0.95), 0 0 32px rgba(245, 197, 66, 0.45), -2px 0 10px rgba(255, 30, 66, 0.50) !important;
}
.hero-subtitle {"""
    )
    print("Added .hero-subtitle:hover in style.css!")

with open('assets/css/style.css', 'w', encoding='utf-8') as f:
    f.write(css)

# 3. Update assets/js/script.js to toggle UTC / Local time and emit pulse ring on clock click
with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    sjs = f.read()

old_clock_code = """        // A. Live UTC Precision Clock

        const clockEl = document.getElementById('clock-utc');

        if (clockEl) {

            const updateClock = () => {

                const d = new Date();

                const hh = String(d.getUTCHours()).padStart(2, '0');

                const mm = String(d.getUTCMinutes()).padStart(2, '0');

                const ss = String(d.getUTCSeconds()).padStart(2, '0');

                clockEl.textContent = `UTC ${hh}:${mm}:${ss}`;

            };

            updateClock();

            setInterval(updateClock, 1000);

        }"""

new_clock_code = """        // A. Live UTC & Local Precision Clock with Interactive Toggle
        const clockEl = document.getElementById('clock-utc');
        const clockPill = document.getElementById('hero-live-clock');
        if (clockEl) {
            let isLocal = false;
            const updateClock = () => {
                const d = new Date();
                if (isLocal) {
                    const hh = String(d.getHours()).padStart(2, '0');
                    const mm = String(d.getMinutes()).padStart(2, '0');
                    const ss = String(d.getSeconds()).padStart(2, '0');
                    clockEl.textContent = `LOCAL ${hh}:${mm}:${ss}`;
                } else {
                    const hh = String(d.getUTCHours()).padStart(2, '0');
                    const mm = String(d.getUTCMinutes()).padStart(2, '0');
                    const ss = String(d.getUTCSeconds()).padStart(2, '0');
                    clockEl.textContent = `UTC ${hh}:${mm}:${ss}`;
                }
            };
            updateClock();
            setInterval(updateClock, 1000);

            if (clockPill) {
                clockPill.addEventListener('click', () => {
                    isLocal = !isLocal;
                    updateClock();
                    clockPill.classList.add('clock-ping');
                    setTimeout(() => clockPill.classList.remove('clock-ping'), 350);
                    if (window.drones && typeof window.drones.emitPulseRing === 'function') {
                        const r = clockPill.getBoundingClientRect();
                        window.drones.emitPulseRing(r.left + r.width / 2, r.top + r.height / 2, '#F5C542', 28, 250);
                    }
                });

                // Micro-hover spark effect from nearby nanobots
                clockPill.addEventListener('mouseenter', () => {
                    if (window.drones && typeof window.drones.emitPlasmaSparks === 'function') {
                        const r = clockPill.getBoundingClientRect();
                        window.drones.emitPlasmaSparks(r.left + r.width * 0.5, r.top + r.height * 0.5, 2);
                    }
                });
            }
        }"""

if old_clock_code in sjs:
    sjs = sjs.replace(old_clock_code, new_clock_code)
    print("Updated script.js with interactive UTC/Local toggle & hover effects!")
else:
    print("Warning: old_clock_code not matched verbatim in script.js, checking...")

with open('assets/js/script.js', 'w', encoding='utf-8') as f:
    f.write(sjs)

print("Saved all hero hover updates successfully!")
