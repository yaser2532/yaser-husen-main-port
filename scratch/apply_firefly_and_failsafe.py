import subprocess
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Update assets/css/drones.css to make .hero-transition-seam background transparent (no black line)
with open('assets/css/drones.css', 'rb') as f:
    raw_dcss = f.read()

eol_dcss = '\r\r\n' if b'\r\r\n' in raw_dcss else ('\r\n' if b'\r\n' in raw_dcss else '\n')
dcss = raw_dcss.decode('utf-8', errors='replace')

new_seam = """.hero-transition-seam {
    position: absolute;
    bottom: -12rem;
    left: 0;
    width: 100%;
    height: 24rem;
    pointer-events: none;
    z-index: 3;
    background: transparent;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    mask-image: linear-gradient(to bottom, transparent 0%, rgba(0, 0, 0, 0.5) 25%, black 50%, rgba(0, 0, 0, 0.5) 75%, transparent 100%);
    -webkit-mask-image: linear-gradient(to bottom, transparent 0%, rgba(0, 0, 0, 0.5) 25%, black 50%, rgba(0, 0, 0, 0.5) 75%, transparent 100%);
    display: block;
}""".replace('\n', eol_dcss)

seam_pattern = re.compile(r'\.hero-transition-seam\s*\{[^}]*\}', re.DOTALL)
dcss = seam_pattern.sub(new_seam, dcss)

with open('assets/css/drones.css', 'wb') as f:
    f.write(dcss.encode('utf-8'))
print("assets/css/drones.css updated: .hero-transition-seam background is transparent.")

# 2. Update assets/js/drones.js: Drone class (firefly light tail, unpredictable flutter) & checkBuildGate (fast-scroll failsafe)
with open('assets/js/drones.js', 'rb') as f:
    raw_djs = f.read()

eol_djs = '\r\r\n' if b'\r\r\n' in raw_djs else ('\r\n' if b'\r\n' in raw_djs else '\n')
djs = raw_djs.decode('utf-8', errors='replace')

# Replace Drone class
idx_drone_start = djs.find("class Drone {")
if idx_drone_start == -1:
    print("ERROR: could not find class Drone")
    sys.exit(1)

idx_drone_end = djs.find("const drones = [];", idx_drone_start)
if idx_drone_end == -1:
    print("ERROR: could not find const drones = [];")
    sys.exit(1)

new_drone_class = """class Drone {
        constructor(id) {
            this.id = id;
            this.color = PALETTE[id % PALETTE.length];
            this.size = 3.2 + (id % 4) * 0.8; // 3.2px to 5.6px vibrant glowing core

            // Organic firefly multi-frequency oscillators for unpredictable wandering
            this.wanderFreq1 = 0.0022 + (id * 0.00063) % 0.0028;
            this.wanderFreq2 = 0.0044 + (id * 0.00085) % 0.0036;
            this.wanderFreq3 = 0.0016 + (id * 0.00041) % 0.0022;
            this.lastDartTime = 0;
            this.nextDartInterval = 600 + Math.random() * 2000;

            // Orbit geometry
            this.orbitRadius = R_MIN + (id / DRONE_COUNT) * (R_MAX - R_MIN);
            this.orbitAngle = (id / DRONE_COUNT) * Math.PI * 2;
            this.orbitSpeed = 0.85 + (id % 4) * 0.22;
            this.orbitDir = (id % 2 === 0) ? 1 : -1;
            this.noisePhase = id * 1.37;
            this.stiffness = 0.14 + (id % 3) * 0.04;
            this.damping = 0.78 + (id % 3) * 0.04;

            // Coordinates
            this.x = cursorX + Math.cos(this.orbitAngle) * this.orbitRadius;
            this.y = cursorY + Math.sin(this.orbitAngle) * this.orbitRadius;
            this.vx = 0;
            this.vy = 0;
            this.opacity = 1.0;
            this.targetOpacity = 1.0;

            // State: 'FOLLOW' | 'DISPATCH' | 'PULL' | 'RETURN'
            this.state = 'FOLLOW';
            this.activeMission = null;
            this.crewIndex = -1;

            // Procedural path tracking
            this.flightStart = 0;
            this.flightDuration = 800;
            this.pathPoints = [];
            this.targetAnchor = { x: 0, y: 0 };

            // Firefly Light Tail: 16 history points of dissolving light trace
            this.trail = [];
            this.maxTrail = 16;
        }

        updateFollow(now, dt) {
            // Unpredictable organic firefly flight: multi-harmonic bio-flutter
            this.orbitAngle += this.orbitSpeed * this.orbitDir * dt;

            const wanderX = Math.sin(now * this.wanderFreq1 + this.noisePhase) * 11
                          + Math.cos(now * this.wanderFreq2 + this.id * 1.3) * 6
                          + Math.sin(now * this.wanderFreq3 + this.id) * 4;
            const wanderY = Math.cos(now * this.wanderFreq2 + this.noisePhase) * 11
                          + Math.sin(now * this.wanderFreq1 + this.id * 1.7) * 6
                          + Math.cos(now * this.wanderFreq3 + this.id) * 4;

            // Dynamic fluctuating radius for unpredictable distance
            const dynamicR = R_MIN + (R_MAX - R_MIN) * (0.35 + 0.45 * Math.sin(now * 0.0016 + this.id * 2.3));

            const desiredX = cursorX + Math.cos(this.orbitAngle) * dynamicR + wanderX;
            const desiredY = cursorY + Math.sin(this.orbitAngle) * dynamicR + wanderY;

            // Spontaneous erratic micro-dart impulses (like live firefly fluttering)
            if (now - this.lastDartTime > this.nextDartInterval) {
                this.lastDartTime = now;
                this.nextDartInterval = 800 + Math.random() * 2400;
                const dartAngle = Math.random() * Math.PI * 2;
                const dartForce = 0.9 + Math.random() * 1.6;
                this.vx += Math.cos(dartAngle) * dartForce;
                this.vy += Math.sin(dartAngle) * dartForce;
            }

            // Spring-damper physics
            const ax = (desiredX - this.x) * this.stiffness;
            const ay = (desiredY - this.y) * this.stiffness;
            this.vx = (this.vx + ax) * this.damping;
            this.vy = (this.vy + ay) * this.damping;
            this.x += this.vx;
            this.y += this.vy;

            // Strict R_MAX boundary clamp: Never exceed R_max from cursor in FOLLOW
            const dx = this.x - cursorX;
            const dy = this.y - cursorY;
            const dist = Math.hypot(dx, dy);
            if (dist > R_MAX) {
                const ratio = R_MAX / dist;
                this.x = cursorX + dx * ratio;
                this.y = cursorY + dy * ratio;
                this.vx *= 0.5;
                this.vy *= 0.5;
            }

            // Smooth DIM transition: 150ms fade to 0.3 over text, 250ms restore to 1.0
            const targetOp = (!cursorInWindow) ? 0.60 : (isOverText ? 0.30 : 1.0);
            const fadeSpeed = (targetOp < this.opacity) ? 0.24 : 0.22;
            this.opacity += (targetOp - this.opacity) * fadeSpeed;

            this.pushTrail();
        }

        updateFlight(now, dt) {
            const elapsed = now - this.flightStart;
            const t = Math.min(1.0, elapsed / this.flightDuration);
            const easeT = easeInOutCubic(t);

            if (this.pathPoints.length >= 4) {
                // Catmull-Rom spline interpolation with unpredictable organic sway
                const pos = getSplinePoint(this.pathPoints, easeT);
                const swayAmp = Math.sin(t * Math.PI) * 7.5;
                const swayPhase = now * 0.012 + this.id * 2.8;
                this.x = pos.x + Math.cos(swayPhase) * swayAmp;
                this.y = pos.y + Math.sin(swayPhase) * swayAmp;
            } else {
                const p0 = this.pathPoints[0] || { x: this.x, y: this.y };
                const p1 = this.targetAnchor;
                this.x = p0.x + (p1.x - p0.x) * easeT;
                this.y = p0.y + (p1.y - p0.y) * easeT;
            }

            this.opacity = 1.0;
            this.pushTrail();

            if (t >= 1.0) {
                if (this.state === 'DISPATCH') {
                    this.state = 'PULL';
                    if (this.activeMission) {
                        this.activeMission.onDroneArrived(this);
                    }
                } else if (this.state === 'RETURN') {
                    this.state = 'FOLLOW';
                    this.activeMission = null;
                }
            }
        }

        updatePull(now, dt) {
            // Latch onto target anchor with slight high-frequency micro-jitter
            const jitterX = Math.sin(now * 0.05 + this.id * 1.5) * 1.8;
            const jitterY = Math.cos(now * 0.06 + this.id * 1.2) * 1.8;
            this.x = this.targetAnchor.x + jitterX;
            this.y = this.targetAnchor.y + jitterY;
            this.opacity = 1.0;
            this.pushTrail();
        }

        pushTrail() {
            this.trail.unshift({ x: this.x, y: this.y, opacity: this.opacity });
            if (this.trail.length > this.maxTrail) {
                this.trail.pop();
            }
        }

        draw(ctx) {
            // Firefly Light Tail: Smooth glowing ribbon of disappearing bioluminescent light
            if (this.trail.length > 2) {
                ctx.save();
                
                // 1. Outer luminous aura ribbon
                ctx.beginPath();
                ctx.moveTo(this.trail[0].x, this.trail[0].y);
                for (let i = 1; i < this.trail.length - 1; i++) {
                    const xc = (this.trail[i].x + this.trail[i + 1].x) * 0.5;
                    const yc = (this.trail[i].y + this.trail[i + 1].y) * 0.5;
                    ctx.quadraticCurveTo(this.trail[i].x, this.trail[i].y, xc, yc);
                }
                ctx.strokeStyle = this.color;
                ctx.lineWidth = Math.max(1.4, this.size * 1.5);
                ctx.lineCap = 'round';
                ctx.lineJoin = 'round';
                ctx.globalAlpha = this.opacity * 0.35;
                ctx.shadowBlur = 10;
                ctx.shadowColor = this.color;
                ctx.stroke();

                // 2. Inner intense white filament core of disappearing light
                ctx.beginPath();
                ctx.moveTo(this.trail[0].x, this.trail[0].y);
                for (let i = 1; i < this.trail.length - 1; i++) {
                    const xc = (this.trail[i].x + this.trail[i + 1].x) * 0.5;
                    const yc = (this.trail[i].y + this.trail[i + 1].y) * 0.5;
                    ctx.quadraticCurveTo(this.trail[i].x, this.trail[i].y, xc, yc);
                }
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.90)';
                ctx.lineWidth = Math.max(0.7, this.size * 0.65);
                ctx.globalAlpha = this.opacity * 0.70;
                ctx.shadowBlur = 6;
                ctx.shadowColor = THEME.gold;
                ctx.stroke();

                // 3. Fading bioluminescent firefly embers along the trail
                for (let i = 2; i < this.trail.length; i += 2) {
                    const pt = this.trail[i];
                    const age = i / this.trail.length;
                    const sporeAlpha = this.opacity * Math.pow(1 - age, 1.6) * 0.42;
                    if (sporeAlpha > 0.02) {
                        ctx.beginPath();
                        ctx.arc(pt.x, pt.y, Math.max(0.6, this.size * (1 - age * 0.65)), 0, Math.PI * 2);
                        ctx.fillStyle = this.color;
                        ctx.globalAlpha = sporeAlpha;
                        ctx.shadowBlur = 5;
                        ctx.shadowColor = this.color;
                        ctx.fill();
                    }
                }
                ctx.restore();
            }

            // Outer vivid neon firefly halo
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size * 2.4, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.globalAlpha = this.opacity * 0.25;
            ctx.fill();

            // Main glowing firefly core
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size * 0.95, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.globalAlpha = this.opacity * 0.95;
            ctx.fill();

            // Intense white specular center
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size * 0.40, 0, Math.PI * 2);
            ctx.fillStyle = THEME.white;
            ctx.globalAlpha = this.opacity * 0.98;
            ctx.fill();

            ctx.globalAlpha = 1.0;
        }
    }

    """.replace('\n', eol_djs)

djs = djs[:idx_drone_start] + new_drone_class + djs[idx_drone_end:]

# Replace checkBuildGate with fast-scroll failsafe
idx_gate_start = djs.find("function checkBuildGate(now) {")
if idx_gate_start == -1:
    print("ERROR: could not find function checkBuildGate")
    sys.exit(1)

idx_dispatch = djs.find("function dispatchMission(", idx_gate_start)
if idx_dispatch == -1:
    print("ERROR: could not find function dispatchMission")
    sys.exit(1)

new_check_gate = """function checkBuildGate(now) {
        if (isReducedMotion) {
            revealAllInstantly();
            return;
        }

        const scrollY = window.scrollY || window.pageYOffset;

        // Footer reached: guarantee all elements are built
        const isAtBottom = (window.innerHeight + scrollY >= document.documentElement.scrollHeight - 100);
        if (isAtBottom) {
            elementList.forEach(item => {
                if (item.state !== 'built') {
                    finishElementInstantly(item);
                }
            });
            return;
        }

        // ─── FAST-SCROLL FAILSAFE SYSTEM ──────────────────────────────────
        // Failsafe 1: Scrolled-Past Elements Guarantee
        // Any element that has been scrolled completely above the viewport MUST be finished instantly.
        // This guarantees that if the user scrolls fast down the page and scrolls back up, 100% of content is visible.
        elementList.forEach(item => {
            if (item.state !== 'built') {
                const r = item.el.getBoundingClientRect();
                if (r.bottom < -20) {
                    finishElementInstantly(item);
                }
            }
        });

        // Failsafe 2: High-Velocity Rapid Scroll Catch-up
        // When fast scrolling exceeds 1200 px/s, immediately reveal sections that have been passed
        if (currentScrollSpeed > 1200) {
            SECTION_ORDER.forEach(secId => {
                const sec = sectionMap[secId];
                if (!sec || sec.isHero) return;
                const r = sec.el.getBoundingClientRect();
                if (r.bottom < viewH * 0.6) {
                    sec.elements.forEach(item => {
                        if (item.state !== 'built') finishElementInstantly(item);
                    });
                }
            });
        }

        // Failsafe 3: Active Viewport Emergency Watchdog
        // If an element is within the active viewport for > 1200ms and hasn't started pulling, reveal it instantly
        elementList.forEach(item => {
            if (item.state === 'pending') {
                const r = item.el.getBoundingClientRect();
                const inView = (r.top < viewH * 0.95 && r.bottom > 20);
                if (inView) {
                    if (!item.firstVisibleTime) {
                        item.firstVisibleTime = now;
                    } else if (now - item.firstVisibleTime > 1200) {
                        finishElementInstantly(item);
                    }
                }
            }
        });

        // Automatic Section-Triggered Sequence: When section covers most of the screen
        SECTION_ORDER.forEach(secId => {
            const sec = sectionMap[secId];
            if (!sec || sec.isHero) return;

            const r = sec.el.getBoundingClientRect();
            const visTop = Math.max(0, r.top);
            const visBottom = Math.min(viewH, r.bottom);
            const visHeight = Math.max(0, visBottom - visTop);

            const coversMostOfScreen = (visHeight >= viewH * 0.42) || 
                                       (r.top <= viewH * 0.45 && r.bottom >= viewH * 0.50);

            if (coversMostOfScreen) {
                sec.dwellMet = true;
            }
        });

        // Failsafe Watchdog: elements never stay hidden > 3.0s after gate open
        elementList.forEach(item => {
            if (item.gateOpenedTime > 0 && item.state !== 'built') {
                if (now - item.gateOpenedTime > 3000) {
                    finishElementInstantly(item);
                }
            }
        });

        const scrollSettled = (now - lastFastScrollTime >= SCROLL_SETTLE_MS);
        if (!scrollSettled) return;

        // Strictly ONE element pulled at a time across the viewport
        if (activeMissions.length >= 1) return;

        const availableDrones = drones.filter(d => d.state === 'FOLLOW');
        if (availableDrones.length < CREW_SIZE) return;

        for (let s = 0; s < SECTION_ORDER.length; s++) {
            const secId = SECTION_ORDER[s];
            const sec = sectionMap[secId];
            if (!sec || (!sec.dwellMet && !sec.isHero)) continue;

            const secRect = sec.el.getBoundingClientRect();
            if (secRect.bottom < 0 || secRect.top > viewH * 1.15) continue;

            const isSectionBusy = sec.elements.some(e => e.state === 'dispatched' || e.state === 'pulling');
            if (isSectionBusy) continue;

            const reachablePending = sec.elements.filter(item => {
                if (item.state !== 'pending') return false;
                const r = item.el.getBoundingClientRect();
                return r.width > 0 && r.height > 0 && r.top <= viewH * 1.15 && r.bottom >= -50;
            });

            if (reachablePending.length === 0) continue;

            // Pick a RANDOM pending element in this section (random order, one at a time!)
            const randomIndex = Math.floor(Math.random() * reachablePending.length);
            const chosenItem = reachablePending[randomIndex];

            dispatchMission(chosenItem, availableDrones.slice(0, CREW_SIZE), now);
            break; // Strictly one element at a time!
        }
    }

    """.replace('\n', eol_djs)

djs = djs[:idx_gate_start] + new_check_gate + djs[idx_dispatch:]

with open('assets/js/drones.js', 'wb') as f:
    f.write(djs.encode('utf-8'))

print("assets/js/drones.js updated with firefly light tail, unpredictable flutter, and fast-scroll failsafe.")
