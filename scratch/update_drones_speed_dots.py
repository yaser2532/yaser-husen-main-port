import re

drones_path = 'assets/js/drones.js'

with open(drones_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Normalize
text = text.replace('\r\n', '\n').replace('\r', '\n')

# 1. Update dwell and settle timing
old_timing = """    const SCROLL_SETTLE_MS = 200;      // ms
    const SECTION_DWELL_MS = 400;      // ms"""

new_timing = """    const SCROLL_SETTLE_MS = 100;      // ms (responsive settle)
    const SECTION_DWELL_MS = 100;      // ms (reduced dwell for 0.5s faster build trigger)"""

if old_timing in text:
    text = text.replace(old_timing, new_timing)
    print("Updated dwell and settle timing.")
else:
    print("Warning: old_timing not found!")

# 2. Update Drone size and trail in constructor
old_size = """            this.color = PALETTE[id % PALETTE.length];
            this.size = 3.2 + (id % 3) * 0.7; // 3.2px to 4.6px"""

new_size = """            this.color = PALETTE[id % PALETTE.length];
            this.size = 1.8 + (id % 3) * 0.4; // 1.8px to 2.6px (sleek, shorter dots)"""

if old_size in text:
    text = text.replace(old_size, new_size)
    print("Updated drone size.")
else:
    print("Warning: old_size not found!")

old_trail = """            // Trail history (short fading trail)
            this.trail = [];
            this.maxTrail = 4;"""

new_trail = """            // Trail history (compact tight trail)
            this.trail = [];
            this.maxTrail = 2;"""

if old_trail in text:
    text = text.replace(old_trail, new_trail)
    print("Updated drone maxTrail.")
else:
    print("Warning: old_trail not found!")

# 3. Update drawing routines for sleeker dots
old_draw = """            for (let i = this.trail.length - 1; i >= 1; i--) {
                const p = this.trail[i];
                const trailAlpha = (p.opacity * (1 - i / this.trail.length) * 0.35);
                ctx.beginPath();
                ctx.arc(p.x, p.y, Math.max(1, this.size * 0.65), 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.globalAlpha = trailAlpha;
                ctx.fill();
            }

            // Outer soft glow halo
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size * 2.2, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.globalAlpha = this.opacity * 0.28;
            ctx.fill();

            // Main drone core
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size * 0.85, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.globalAlpha = this.opacity * 0.95;
            ctx.fill();

            // Intense white specular center
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size * 0.35, 0, Math.PI * 2);
            ctx.fillStyle = THEME.white;
            ctx.globalAlpha = this.opacity * 0.98;
            ctx.fill();"""

new_draw = """            for (let i = this.trail.length - 1; i >= 1; i--) {
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
            ctx.fill();"""

if old_draw in text:
    text = text.replace(old_draw, new_draw)
    print("Updated drone draw function.")
else:
    print("Warning: old_draw not found!")

# 4. Update element minimum build durations (0.5s faster!)
old_durations = """                let type = 'card';
                let minDuration = 600;

                if (['h1', 'h2', 'h3'].includes(tag) || el.classList.contains('section-title') || el.classList.contains('section-tag')) {
                    type = 'title';
                    minDuration = 1100;
                } else if (tag === 'p' || el.classList.contains('section-desc')) {
                    type = 'paragraph';
                    minDuration = 900;
                } else if (['a', 'button'].includes(tag) || el.classList.contains('cta-button') || el.classList.contains('filter-btn')) {
                    type = 'button';
                    minDuration = 450;
                } else if (el.classList.contains('code-block-visual')) {
                    type = 'code-card';
                    minDuration = 1400;
                }"""

new_durations = """                let type = 'card';
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

if old_durations in text:
    text = text.replace(old_durations, new_durations)
    print("Updated element minimum durations.")
else:
    print("Warning: old_durations not found!")

# 5. Update flight duration and return duration
old_flight = """        const flightDuration = Math.round(650 + Math.random() * 450); // 650-1100ms (>= 500ms guaranteed)"""
new_flight = """        const flightDuration = Math.round(250 + Math.random() * 200); // 250-450ms (0.5s faster arrival)"""

if old_flight in text:
    text = text.replace(old_flight, new_flight)
    print("Updated dispatch flight duration.")
else:
    print("Warning: old_flight not found!")

old_stagger = """            drone.flightDuration = flightDuration + idx * 40; // subtle stagger"""
new_stagger = """            drone.flightDuration = flightDuration + idx * 20; // tighter stagger"""

if old_stagger in text:
    text = text.replace(old_stagger, new_stagger)
    print("Updated drone flight stagger.")
else:
    print("Warning: old_stagger not found!")

old_return = """            drone.flightDuration = Math.round(450 + Math.random() * 350); // 450-800ms return"""
new_return = """            drone.flightDuration = Math.round(200 + Math.random() * 150); // 200-350ms agile return"""

if old_return in text:
    text = text.replace(old_return, new_return)
    print("Updated drone return duration.")
else:
    print("Warning: old_return not found!")

# 6. Update tractor beams width and sparks
old_beams = """                ctx.strokeStyle = 'rgba(25, 227, 209, 0.38)';
                ctx.lineWidth = 3.2;
                ctx.stroke();

                // Core electric line
                ctx.beginPath();
                ctx.moveTo(drone.x, drone.y);
                ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);
                ctx.strokeStyle = 'rgba(245, 197, 66, 0.85)';
                ctx.lineWidth = 1.8;
                ctx.stroke();

                // Hot white filament
                ctx.beginPath();
                ctx.moveTo(drone.x, drone.y);
                ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.98)';
                ctx.lineWidth = 1.0;"""

new_beams = """                ctx.strokeStyle = 'rgba(25, 227, 209, 0.38)';
                ctx.lineWidth = 1.6; // sleeker width
                ctx.stroke();

                // Core electric line
                ctx.beginPath();
                ctx.moveTo(drone.x, drone.y);
                ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);
                ctx.strokeStyle = 'rgba(245, 197, 66, 0.85)';
                ctx.lineWidth = 0.9;
                ctx.stroke();

                // Hot white filament
                ctx.beginPath();
                ctx.moveTo(drone.x, drone.y);
                ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.98)';
                ctx.lineWidth = 0.5;"""

if old_beams in text:
    text = text.replace(old_beams, new_beams)
    print("Updated tractor beam widths.")
else:
    print("Warning: old_beams not found!")

old_sparks = """            ctx.arc(s.x, s.y, 1.8 * s.life, 0, Math.PI * 2);"""
new_sparks = """            ctx.arc(s.x, s.y, 1.0 * s.life, 0, Math.PI * 2);"""

if old_sparks in text:
    text = text.replace(old_sparks, new_sparks)
    print("Updated spark size.")
else:
    print("Warning: old_sparks not found!")

with open(drones_path, 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text)

print("assets/js/drones.js successfully updated!")
