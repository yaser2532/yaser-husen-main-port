with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update Drone size and trail
js = js.replace(
    "this.size = 1.8 + (id % 3) * 0.4; // 1.8px to 2.6px (sleek, shorter dots)",
    "this.size = 3.2 + (id % 4) * 0.8; // 3.2px to 5.6px (reverted back to normal, vibrant size)"
)
js = js.replace(
    "this.maxTrail = 2;",
    "this.maxTrail = 4;"
)

# 2. Update draw(ctx) inside Drone class
old_draw = """        draw(ctx) {
            // Draw short fading trail
            for (let i = this.trail.length - 1; i >= 1; i--) {
                const p = this.trail[i];
                const trailAlpha = (p.opacity * (1 - i / this.trail.length) * 0.28);
                ctx.beginPath();
                ctx.arc(p.x, p.y, Math.max(0.6, this.size * 0.45), 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.globalAlpha = trailAlpha;
                ctx.fill();
            }

            // Outer soft glow halo (shorter, crisper perimeter)
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size * 1.4, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.globalAlpha = this.opacity * 0.18;
            ctx.fill();

            // Main drone core
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size * 0.72, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.globalAlpha = this.opacity * 0.95;
            ctx.fill();

            // Intense white specular center
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size * 0.26, 0, Math.PI * 2);
            ctx.fillStyle = THEME.white;
            ctx.globalAlpha = this.opacity * 0.98;
            ctx.fill();

            ctx.globalAlpha = 1.0;
        }"""

new_draw = """        draw(ctx) {
            // Draw graceful fading comet trail
            for (let i = this.trail.length - 1; i >= 1; i--) {
                const p = this.trail[i];
                const trailAlpha = (p.opacity * (1 - i / this.trail.length) * 0.35);
                ctx.beginPath();
                ctx.arc(p.x, p.y, Math.max(0.8, this.size * 0.50), 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.globalAlpha = trailAlpha;
                ctx.fill();
            }

            // Outer vivid neon halo
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size * 2.2, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.globalAlpha = this.opacity * 0.22;
            ctx.fill();

            // Main glowing drone core
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size * 0.92, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.globalAlpha = this.opacity * 0.95;
            ctx.fill();

            // Intense white specular center
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size * 0.36, 0, Math.PI * 2);
            ctx.fillStyle = THEME.white;
            ctx.globalAlpha = this.opacity * 0.98;
            ctx.fill();

            ctx.globalAlpha = 1.0;
        }"""

js_norm = js.replace('\r\n', '\n')
old_draw_norm = old_draw.replace('\r\n', '\n')
assert old_draw_norm in js_norm, "old_draw not found in drones.js"
js_norm = js_norm.replace(old_draw_norm, new_draw)

# 3. Revert rendering durations to normal
old_durations = """                let type = 'card';
                let minDuration = 350; // was 600ms (-250ms)

                if (['h1', 'h2', 'h3'].includes(tag) || el.classList.contains('section-title') || el.classList.contains('section-tag')) {
                    type = 'title';
                    minDuration = 600; // was 1100ms (-500ms / 0.5s faster!)
                } else if (tag === 'p' || el.classList.contains('section-desc')) {
                    type = 'paragraph';
                    minDuration = 450; // was 900ms (-450ms / 0.5s faster!)
                } else if (['a', 'button'].includes(tag) || el.classList.contains('cta-button') || el.classList.contains('filter-btn')) {
                    type = 'button';
                    minDuration = 250; // was 450ms (-200ms)
                } else if (el.classList.contains('code-block-visual')) {
                    type = 'code-card';
                    minDuration = 850; // was 1400ms (-550ms / 0.55s faster!)
                }"""

new_durations = """                let type = 'card';
                let minDuration = 650; // normal duration for cards

                if (['h1', 'h2', 'h3'].includes(tag) || el.classList.contains('section-title') || el.classList.contains('section-tag')) {
                    type = 'title';
                    minDuration = 1100; // normal duration for section titles
                } else if (tag === 'p' || el.classList.contains('section-desc')) {
                    type = 'paragraph';
                    minDuration = 900; // normal duration for paragraphs
                } else if (['a', 'button'].includes(tag) || el.classList.contains('cta-button') || el.classList.contains('filter-btn')) {
                    type = 'button';
                    minDuration = 450; // normal duration for buttons
                } else if (el.classList.contains('code-block-visual')) {
                    type = 'code-card';
                    minDuration = 1400; // normal duration for code card
                }"""

old_durations_norm = old_durations.replace('\r\n', '\n')
assert old_durations_norm in js_norm, "old_durations not found in drones.js"
js_norm = js_norm.replace(old_durations_norm, new_durations)

# 4. Update checkBuildGate for automatic sequential section-triggered pulling
old_gate = """        // Section Dwell Tracker
        SECTION_ORDER.forEach(secId => {
            const sec = sectionMap[secId];
            if (!sec || sec.isHero) return;

            const r = sec.el.getBoundingClientRect();
            const inBand = (r.bottom >= bandTopY && r.top <= bandBottomY);

            if (inBand) {
                if (sec.firstEnteredBandTime === 0) {
                    sec.firstEnteredBandTime = now;
                }
                if (now - sec.firstEnteredBandTime >= SECTION_DWELL_MS) {
                    sec.dwellMet = true;
                }
            } else {
                sec.firstEnteredBandTime = 0;
            }
        });

        // Evaluate pending elements in strict sequence order
        for (let i = 0; i < elementList.length; i++) {
            const item = elementList[i];
            if (item.state !== 'pending') continue;

            const sec = item.secInfo;
            if (!sec.dwellMet && !sec.isHero) continue;
            if (!scrollSettled) continue;

            // Check predecessor: must be built or already in flight
            if (i > 0) {
                const pred = elementList[i - 1];
                if (pred.secId === item.secId && pred.state === 'pending') {
                    // Predecessor has not yet dispatched; sequence order cannot be broken
                    continue;
                }
            }

            // Check Band condition: Element E is >= 80% inside viewport band [8%, 88%]
            const r = item.el.getBoundingClientRect();
            if (r.width === 0 || r.height === 0) continue;

            const elTop = r.top;
            const elBottom = r.bottom;
            const elHeight = r.height;

            const visibleTop = Math.max(elTop, bandTopY);
            const visibleBottom = Math.min(elBottom, bandBottomY);
            const visibleHeight = Math.max(0, visibleBottom - visibleTop);

            let satisfiesBand = false;
            if (elHeight > bandHeight) {
                // Taller elements: top 80% of viewport height or first 600px in band
                satisfiesBand = (elTop >= bandTopY - 100 && visibleHeight >= Math.min(600, bandHeight * 0.8));
            } else {
                satisfiesBand = (visibleHeight >= elHeight * 0.80);
            }

            if (!satisfiesBand) continue;

            // Capacity check: Max 3 active crews
            if (activeMissions.length >= MAX_ACTIVE_CREWS) continue;

            // Available drones pool check: need at least CREW_SIZE available drones
            const availableDrones = drones.filter(d => d.state === 'FOLLOW');
            if (availableDrones.length < CREW_SIZE) continue;

            // Gate opens! Dispatch mission for element E
            dispatchMission(item, availableDrones.slice(0, CREW_SIZE), now);
        }"""

new_gate = """        // Automatic Section-Triggered Sequence: When section covers most of the screen
        SECTION_ORDER.forEach(secId => {
            const sec = sectionMap[secId];
            if (!sec || sec.isHero) return;

            const r = sec.el.getBoundingClientRect();
            const visTop = Math.max(0, r.top);
            const visBottom = Math.min(viewH, r.bottom);
            const visHeight = Math.max(0, visBottom - visTop);

            // A section covers most of the screen when:
            // 1) It occupies at least 42% of the viewport height, OR
            // 2) It spans across the center of the viewport (top <= 45% and bottom >= 50%)
            const coversMostOfScreen = (visHeight >= viewH * 0.42) || 
                                       (r.top <= viewH * 0.45 && r.bottom >= viewH * 0.50);

            if (coversMostOfScreen) {
                sec.dwellMet = true;
            }
        });

        // Evaluate pending elements in strict sequence order
        for (let i = 0; i < elementList.length; i++) {
            const item = elementList[i];
            if (item.state !== 'pending') continue;

            const sec = item.secInfo;
            if (!sec.dwellMet && !sec.isHero) continue;
            if (!scrollSettled) continue;

            // Strict sequence cadence: wait for predecessor in section
            if (i > 0) {
                const pred = elementList[i - 1];
                if (pred.secId === item.secId) {
                    // Predecessor must be pulling or built before next element starts
                    if (pred.state === 'pending' || pred.state === 'dispatched') {
                        continue;
                    }
                    // Stagger cadence: at least 220ms after predecessor started pull
                    if (pred.pullStartTime && (now - pred.pullStartTime < 220)) {
                        continue;
                    }
                }
            }

            // Element must be within reachable view (top within 115% of viewport height)
            const r = item.el.getBoundingClientRect();
            if (r.width === 0 || r.height === 0) continue;
            if (r.top > viewH * 1.15) continue; // Will be pulled when scrolled closer

            // Capacity check: Max 3 active crews
            if (activeMissions.length >= MAX_ACTIVE_CREWS) continue;

            // Available drones pool check: need at least CREW_SIZE available drones
            const availableDrones = drones.filter(d => d.state === 'FOLLOW');
            if (availableDrones.length < CREW_SIZE) continue;

            // Gate opens! Automatically dispatch mission for element E in sequence
            dispatchMission(item, availableDrones.slice(0, CREW_SIZE), now);
        }"""

old_gate_norm = old_gate.replace('\r\n', '\n')
assert old_gate_norm in js_norm, "old_gate not found in drones.js"
js_norm = js_norm.replace(old_gate_norm, new_gate)

# 5. Update flight duration and arrival flourish in dispatchMission
js_norm = js_norm.replace(
    "const flightDuration = Math.round(250 + Math.random() * 200); // 250-450ms (0.5s faster arrival)",
    "const flightDuration = Math.round(550 + Math.random() * 300); // 550-850ms normal cinematic flight"
)
js_norm = js_norm.replace(
    "drone.flightDuration = Math.round(200 + Math.random() * 150); // 200-350ms agile return",
    "drone.flightDuration = Math.round(400 + Math.random() * 250); // 400-650ms normal return"
)

# 6. Update tractor beam stroke widths
js_norm = js_norm.replace(
    "ctx.strokeStyle = 'rgba(25, 227, 209, 0.38)';\n                ctx.lineWidth = 1.6;",
    "ctx.strokeStyle = 'rgba(25, 227, 209, 0.45)';\n                ctx.lineWidth = 2.4;"
)
js_norm = js_norm.replace(
    "ctx.strokeStyle = 'rgba(245, 197, 66, 0.85)';\n                ctx.lineWidth = 0.9;",
    "ctx.strokeStyle = 'rgba(245, 197, 66, 0.90)';\n                ctx.lineWidth = 1.3;"
)
js_norm = js_norm.replace(
    "ctx.strokeStyle = 'rgba(255, 255, 255, 0.98)';\n                ctx.lineWidth = 0.5;",
    "ctx.strokeStyle = 'rgba(255, 255, 255, 0.98)';\n                ctx.lineWidth = 0.8;"
)

with open('assets/js/drones.js', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(js_norm.replace('\n', '\r\n'))

print("Updated assets/js/drones.js successfully!")
