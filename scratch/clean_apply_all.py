import subprocess
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

def write_crlf(path, text):
    # Normalize to \n first, then write with \r\n
    clean = text.replace('\r\n', '\n').replace('\n', '\r\n')
    with open(path, 'wb') as f:
        f.write(clean.encode('utf-8'))

# 1. index.html: Get from HEAD, remove the 9 prj-cyber-index divs
head_index = subprocess.check_output(['git', 'show', 'HEAD:index.html'], text=True, errors='replace')
count = len(re.findall(r'<div class="prj-cyber-index">.*?</div>', head_index, re.DOTALL))
print(f"index.html: Found {count} prj-cyber-index divs in HEAD")
new_index = re.sub(r'\s*<div class="prj-cyber-index">.*?</div>', '', head_index, flags=re.DOTALL)
write_crlf('index.html', new_index)
print("index.html: Cleaned and written.")

# 2. assets/css/style.css: Get from HEAD, remove .prj-cyber-index and .prj-sys-spec
head_style = subprocess.check_output(['git', 'show', 'HEAD:assets/css/style.css'], text=True, errors='replace')
new_style = re.sub(r'/\* Monospace Cyber Telemetry Metadata on Project Cards \*/\s*\.prj-cyber-index\s*\{[^}]*\}\s*\.prj-sys-spec\s*\{[^}]*\}', '', head_style)
write_crlf('assets/css/style.css', new_style)
print("assets/css/style.css: Cleaned and written.")

# 3. assets/css/drones.css: Get from HEAD, update .hero-transition-seam
head_drones_css = subprocess.check_output(['git', 'show', 'HEAD:assets/css/drones.css'], text=True, errors='replace')
seam_pattern = re.compile(r'\.hero-transition-seam\s*\{[^}]*\}', re.DOTALL)
new_seam = """.hero-transition-seam {
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 100%;
    height: 14rem;
    pointer-events: none;
    z-index: 5;
    background: linear-gradient(to bottom, 
        transparent 0%, 
        rgba(4, 2, 7, 0.20) 25%, 
        rgba(4, 2, 7, 0.60) 60%, 
        rgba(4, 2, 7, 0.92) 88%, 
        #040207 100%);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    mask-image: linear-gradient(to bottom, transparent 0%, rgba(0, 0, 0, 0.4) 30%, black 100%);
    -webkit-mask-image: linear-gradient(to bottom, transparent 0%, rgba(0, 0, 0, 0.4) 30%, black 100%);
    display: block;
}"""
new_drones_css = seam_pattern.sub(new_seam, head_drones_css)
write_crlf('assets/css/drones.css', new_drones_css)
print("assets/css/drones.css: Updated and written.")

# 4. assets/js/drones.js: Get from HEAD, apply drone speed + procedural paths + random order one-at-a-time
head_drones_js = subprocess.check_output(['git', 'show', 'HEAD:assets/js/drones.js'], text=True, errors='replace')

start_marker = "const PATH_TYPES = ['spiral-in', 'loop-the-loop', 'figure-8', 'noisy-arc', 'orbit-dive', 'zigzag-swoop'];"
idx_start = head_drones_js.find(start_marker)
idx_end = head_drones_js.find("return pathPoints;", idx_start)
idx_end = head_drones_js.find("}", idx_end) + 1

new_path_gen = """const PATH_TYPES = [
        'spiral-in',
        'loop-the-loop',
        'figure-8',
        'noisy-arc',
        'orbit-dive',
        'zigzag-swoop',
        'hyperbolic-slingshot',
        'quantum-drift',
        'helix-corkscrew'
    ];

    let lastPathTypeIndex = -1;

    function generateProceduralPath(startX, startY, endX, endY, flightDuration) {
        let typeIndex = Math.floor(Math.random() * PATH_TYPES.length);
        if (typeIndex === lastPathTypeIndex) {
            typeIndex = (typeIndex + 1) % PATH_TYPES.length;
        }
        lastPathTypeIndex = typeIndex;
        const type = PATH_TYPES[typeIndex];

        const midX = (startX + endX) * 0.5;
        const midY = (startY + endY) * 0.5;
        const dx = endX - startX;
        const dy = endY - startY;
        const dist = Math.hypot(dx, dy) || 1;
        const normX = -dy / dist;
        const normY = dx / dist;

        const waypoints = [{ x: startX, y: startY }];
        const curvatureScale = Math.min(180, Math.max(50, dist * (0.28 + Math.random() * 0.22)));

        switch (type) {
            case 'spiral-in': {
                const s1 = (Math.random() > 0.5 ? 1 : -1) * curvatureScale;
                const rFactor = 0.8 + Math.random() * 0.4;
                waypoints.push({ x: startX + dx * 0.22 + normX * (s1 * rFactor), y: startY + dy * 0.22 + normY * (s1 * rFactor) });
                waypoints.push({ x: startX + dx * 0.60 - normX * (s1 * 0.65 * rFactor), y: startY + dy * 0.60 - normY * (s1 * 0.65 * rFactor) });
                waypoints.push({ x: startX + dx * 0.88 + normX * (s1 * 0.25), y: startY + dy * 0.88 + normY * (s1 * 0.25) });
                break;
            }
            case 'loop-the-loop': {
                const loopRadius = curvatureScale * (0.75 + Math.random() * 0.35);
                const sign = (Math.random() > 0.5 ? 1 : -1);
                waypoints.push({ x: midX + normX * (loopRadius * sign), y: midY + normY * (loopRadius * sign) });
                waypoints.push({ x: midX - dx * 0.12 + normX * (loopRadius * 1.35 * sign), y: midY - dy * 0.12 + normY * (loopRadius * 1.35 * sign) });
                waypoints.push({ x: midX + dx * 0.18 + normX * (loopRadius * 0.45 * sign), y: midY + dy * 0.18 + normY * (loopRadius * 0.45 * sign) });
                break;
            }
            case 'figure-8': {
                const fScale = curvatureScale * (0.70 + Math.random() * 0.30);
                const sign = (Math.random() > 0.5 ? 1 : -1);
                waypoints.push({ x: startX + dx * 0.28 + normX * (fScale * sign), y: startY + dy * 0.28 + normY * (fScale * sign) });
                waypoints.push({ x: midX + (Math.random() - 0.5) * 15, y: midY + (Math.random() - 0.5) * 15 });
                waypoints.push({ x: startX + dx * 0.72 - normX * (fScale * sign), y: startY + dy * 0.72 - normY * (fScale * sign) });
                break;
            }
            case 'orbit-dive': {
                const oSign = (Math.random() > 0.5 ? 1 : -1);
                const oAmp = curvatureScale * (0.9 + Math.random() * 0.4);
                waypoints.push({ x: startX + normX * (oAmp * oSign), y: startY + normY * (oAmp * oSign) });
                waypoints.push({ x: midX + normX * (oAmp * 1.25 * oSign), y: midY + normY * (oAmp * 1.25 * oSign) });
                waypoints.push({ x: endX - dx * 0.14 - normX * (oAmp * 0.35 * oSign), y: endY - dy * 0.14 - normY * (oAmp * 0.35 * oSign) });
                break;
            }
            case 'zigzag-swoop': {
                const zSign = (Math.random() > 0.5 ? 1 : -1);
                const zAmp = curvatureScale * (0.8 + Math.random() * 0.35);
                waypoints.push({ x: startX + dx * 0.22 + normX * (zAmp * zSign), y: startY + dy * 0.22 + normY * (zAmp * zSign) });
                waypoints.push({ x: startX + dx * 0.55 - normX * (zAmp * 0.9 * zSign), y: startY + dy * 0.55 - normY * (zAmp * 0.9 * zSign) });
                waypoints.push({ x: startX + dx * 0.82 + normX * (zAmp * 0.45 * zSign), y: startY + dy * 0.82 + normY * (zAmp * 0.45 * zSign) });
                break;
            }
            case 'hyperbolic-slingshot': {
                const hSign = (Math.random() > 0.5 ? 1 : -1);
                const hScale = curvatureScale * (1.1 + Math.random() * 0.3);
                waypoints.push({ x: startX + dx * 0.15 - normX * (hScale * 0.4 * hSign), y: startY + dy * 0.15 - normY * (hScale * 0.4 * hSign) });
                waypoints.push({ x: startX + dx * 0.45 + normX * (hScale * 1.3 * hSign), y: startY + dy * 0.45 + normY * (hScale * 1.3 * hSign) });
                waypoints.push({ x: startX + dx * 0.85 + normX * (hScale * 0.25 * hSign), y: startY + dy * 0.85 + normY * (hScale * 0.25 * hSign) });
                break;
            }
            case 'quantum-drift': {
                const qSign = (Math.random() > 0.5 ? 1 : -1);
                const j1 = (Math.random() - 0.5) * 28;
                const j2 = (Math.random() - 0.5) * 28;
                waypoints.push({ x: startX + dx * 0.30 + normX * (curvatureScale * 0.7 * qSign) + j1, y: startY + dy * 0.30 + normY * (curvatureScale * 0.7 * qSign) + j2 });
                waypoints.push({ x: midX - normX * (curvatureScale * 0.5 * qSign) - j2, y: midY - normY * (curvatureScale * 0.5 * qSign) + j1 });
                waypoints.push({ x: startX + dx * 0.80 + normX * (curvatureScale * 0.35 * qSign) + j1 * 0.5, y: startY + dy * 0.80 + normY * (curvatureScale * 0.35 * qSign) - j2 * 0.5 });
                break;
            }
            case 'helix-corkscrew': {
                const corkSign = (Math.random() > 0.5 ? 1 : -1);
                const rHelix = curvatureScale * (0.65 + Math.random() * 0.25);
                waypoints.push({ x: startX + dx * 0.20 + normX * (rHelix * corkSign), y: startY + dy * 0.20 + normY * (rHelix * corkSign) });
                waypoints.push({ x: startX + dx * 0.40 - normX * (rHelix * 0.8 * corkSign), y: startY + dy * 0.40 - normY * (rHelix * 0.8 * corkSign) });
                waypoints.push({ x: startX + dx * 0.65 + normX * (rHelix * 0.9 * corkSign), y: startY + dy * 0.65 + normY * (rHelix * 0.9 * corkSign) });
                waypoints.push({ x: startX + dx * 0.85 - normX * (rHelix * 0.4 * corkSign), y: startY + dy * 0.85 - normY * (rHelix * 0.4 * corkSign) });
                break;
            }
            default: // noisy-arc
            {
                const arcSign = (Math.random() > 0.5 ? 1 : -1);
                const jitter = (Math.random() - 0.5) * 35;
                const arcAmp = curvatureScale * (0.85 + Math.random() * 0.3);
                waypoints.push({ x: startX + dx * 0.33 + normX * (arcAmp * arcSign) + jitter, y: startY + dy * 0.33 + normY * (arcAmp * arcSign) + jitter });
                waypoints.push({ x: startX + dx * 0.68 + normX * (arcAmp * 0.8 * arcSign) - jitter * 0.5, y: startY + dy * 0.68 + normY * (arcAmp * 0.8 * arcSign) - jitter * 0.5 });
                break;
            }
        }

        waypoints.push({ x: endX, y: endY });

        if (waypoints.length < 4) {
            waypoints.splice(1, 0, {
                x: (startX + waypoints[1].x) * 0.5,
                y: (startY + waypoints[1].y) * 0.5
            });
        }

        const pathPoints = [
            { x: startX - (waypoints[1].x - startX) * 0.5, y: startY - (waypoints[1].y - startY) * 0.5 },
            ...waypoints,
            { x: endX + (endX - waypoints[waypoints.length - 2].x) * 0.5, y: endY + (endY - waypoints[waypoints.length - 2].y) * 0.5 }
        ];

        return pathPoints;
    }"""

head_drones_js = head_drones_js[:idx_start] + new_path_gen + head_drones_js[idx_end:]

# Update minDuration in registerElements
head_drones_js = re.sub(r'let minDuration = \d+;\s*\/\/\s*normal duration for cards', 'let minDuration = 350; // accelerated duration for cards (was 650ms)', head_drones_js)
head_drones_js = re.sub(r'minDuration = 1100;\s*\/\/\s*normal duration for section titles', 'minDuration = 600; // accelerated duration for section titles (was 1100ms)', head_drones_js)
head_drones_js = re.sub(r'minDuration = 900;\s*\/\/\s*normal duration for paragraphs', 'minDuration = 450; // accelerated duration for paragraphs (was 900ms)', head_drones_js)
head_drones_js = re.sub(r'minDuration = 450;\s*\/\/\s*normal duration for buttons', 'minDuration = 250; // accelerated duration for buttons (was 450ms)', head_drones_js)
head_drones_js = re.sub(r'minDuration = 1400;\s*\/\/\s*normal duration for code card', 'minDuration = 850; // accelerated duration for code card (was 1400ms)', head_drones_js)

# Update flight duration and return flight duration
head_drones_js = re.sub(
    r'const flightDuration = Math\.round\(550 \+ Math\.random\(\) \* 300\);.*',
    'const flightDuration = Math.round(250 + Math.random() * 200); // 250-450ms accelerated flight (was 550-850ms)',
    head_drones_js
)
head_drones_js = re.sub(
    r'if \(flightTime < 500\) \{\s*setTimeout\(\(\) => this\.startPull\(performance\.now\(\)\), 500 - flightTime\);\s*return;\s*\}',
    'if (flightTime < 250) {\n                    setTimeout(() => this.startPull(performance.now()), 250 - flightTime);\n                    return;\n                }',
    head_drones_js
)
head_drones_js = re.sub(
    r'drone\.flightDuration = Math\.round\(400 \+ Math\.random\(\) \* 250\);.*',
    'drone.flightDuration = Math.round(180 + Math.random() * 120); // 180-300ms accelerated return (was 400-650ms)',
    head_drones_js
)

# Update checkBuildGate
idx_gate_start = head_drones_js.find("function checkBuildGate(now) {")
idx_dispatch = head_drones_js.find("function dispatchMission(", idx_gate_start)

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

        // Failsafe Watchdog: elements never stay hidden > 3.5s after gate open
        elementList.forEach(item => {
            if (item.gateOpenedTime > 0 && item.state !== 'built') {
                if (now - item.gateOpenedTime > 3500) {
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

    """

head_drones_js = head_drones_js[:idx_gate_start] + new_check_gate + head_drones_js[idx_dispatch:]
write_crlf('assets/js/drones.js', head_drones_js)
print("assets/js/drones.js: Updated and written.")

# 5. assets/js/script.js: Get from HEAD, append initHeroToExpertiseBlurScrub
head_script = subprocess.check_output(['git', 'show', 'HEAD:assets/js/script.js'], text=True, errors='replace')
new_blur_scrub = """

/* ==========================================================================
   GSAP SCROLLTRIGGER & LENIS INERTIAL BLUR TRANSITION (Hero to Profile)
   ========================================================================== */

function initHeroToExpertiseBlurScrub() {
    const heroEl = document.querySelector('#home .header-content') || document.getElementById('home');
    const profileEl = document.getElementById('profile-expertise');
    if (!heroEl || !profileEl) return;

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    let targetProgress = 0;
    let currentProgress = 0;
    let isTicking = false;
    let animId = null;

    function calculateProgress() {
        const scrollY = window.scrollY || window.pageYOffset;
        const vh = window.innerHeight;
        const transitionDistance = vh * 0.75;
        targetProgress = Math.max(0, Math.min(1, scrollY / transitionDistance));
    }

    function renderScrub() {
        if (targetProgress >= 1.0) {
            currentProgress += (1.0 - currentProgress) * 0.25;
        } else {
            currentProgress += (targetProgress - currentProgress) * 0.18;
        }

        if (Math.abs(targetProgress - currentProgress) < 0.01) {
            currentProgress = targetProgress;
        }

        const p = currentProgress;

        if (p < 0.01) {
            heroEl.style.filter = '';
            heroEl.style.transform = '';
            heroEl.style.opacity = '';
            heroEl.style.willChange = '';
        } else if (p >= 0.98) {
            heroEl.style.filter = 'blur(12px)';
            heroEl.style.transform = 'translate3d(0, -35px, 0) scale(0.94)';
            heroEl.style.opacity = '0';
            heroEl.style.willChange = '';
        } else {
            const heroBlur = (p * 12).toFixed(1);
            const heroScale = (1.0 - p * 0.06).toFixed(3);
            const heroY = (-p * 35).toFixed(1);
            const heroOpacity = Math.max(0, 1.0 - p * 1.05).toFixed(3);
            heroEl.style.filter = `blur(${heroBlur}px)`;
            heroEl.style.transform = `translate3d(0, ${heroY}px, 0) scale(${heroScale})`;
            heroEl.style.opacity = heroOpacity;
            heroEl.style.willChange = 'transform, filter, opacity';
        }

        if (p >= 0.90) {
            profileEl.style.filter = '';
            profileEl.style.transform = '';
            profileEl.style.opacity = '';
            profileEl.style.willChange = '';
        } else {
            const easeP = p * p * (3 - 2 * p);
            const profileBlur = Math.max(0, (1.0 - easeP) * 14).toFixed(1);
            const profileY = ((1.0 - easeP) * 40).toFixed(1);
            const profileOpacity = (0.25 + easeP * 0.75).toFixed(3);

            profileEl.style.filter = `blur(${profileBlur}px)`;
            profileEl.style.transform = `translate3d(0, ${profileY}px, 0)`;
            profileEl.style.opacity = profileOpacity;
            profileEl.style.willChange = 'transform, filter, opacity';
        }

        if (Math.abs(targetProgress - currentProgress) > 0.002) {
            animId = requestAnimationFrame(renderScrub);
        } else {
            isTicking = false;
        }
    }

    function onScroll() {
        calculateProgress();
        if (!isTicking) {
            isTicking = true;
            animId = requestAnimationFrame(renderScrub);
        }
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });

    calculateProgress();
    currentProgress = targetProgress;
    renderScrub();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHeroToExpertiseBlurScrub);
} else {
    initHeroToExpertiseBlurScrub();
}
"""
new_script = head_script + new_blur_scrub
write_crlf('assets/js/script.js', new_script)
print("assets/js/script.js: Updated and written.")
print("=== ALL FILES CLEANLY RE-APPLIED WITH CRLF ===")
