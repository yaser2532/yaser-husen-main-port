import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern_index = re.compile(
    r'<div class="hero-kinetic-row">.*?<div class="hero-spec-stamp">\[AGENTIC_V4\.2\]</div>\s*</div>',
    re.DOTALL
)

replacement_index = """<div class="hero-kinetic-row">
                <div class="hero-sticker-badge" title="System Status: Operational // Intel Deployed" tabindex="0">
                    <span class="pulse-dot"></span>
                    <span class="sticker-text">STATUS // DEPLOYING INTEL</span>
                </div>
                <div class="hero-clock-pill" id="hero-live-clock" title="Click to toggle Local / UTC Time" tabindex="0">
                    <i class="fa-regular fa-clock"></i> <span id="clock-utc">UTC 00:00:00</span>
                </div>
                <div class="hero-spec-stamp" title="Agentic Architecture Matrix v4.2" tabindex="0">[AGENTIC_V4.2]</div>
            </div>"""

html, count1 = pattern_index.subn(replacement_index, html, count=1)
print(f"Replaced index.html kinetic row: {count1} match")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update assets/js/script.js
with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    js = f.read()

pattern_script = re.compile(
    r'// A\. Live UTC Precision Clock.*?setInterval\(updateClock, 1000\);\s*\}',
    re.DOTALL
)

replacement_script = """// A. Live UTC & Local Precision Clock with Interactive Toggle
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

js, count2 = pattern_script.subn(replacement_script, js, count=1)
print(f"Replaced script.js clock code: {count2} match")

with open('assets/js/script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Applied index.html and script.js updates successfully!")
