import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

DRONES_PATH = 'assets/js/drones.js'

with open(DRONES_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Original content length: {len(content)}")

# 1. Replace generateProceduralPath block
start_marker = "const PATH_TYPES = ['spiral-in', 'loop-the-loop', 'figure-8', 'noisy-arc', 'orbit-dive', 'zigzag-swoop'];"
idx_start = content.find(start_marker)
if idx_start == -1:
    print("ERROR: could not find start_marker for PATH_TYPES")
    sys.exit(1)

# Find the end of generateProceduralPath: return pathPoints;\n\n    }
idx_end = content.find("return pathPoints;\n\n    }", idx_start)
if idx_end == -1:
    idx_end = content.find("return pathPoints;\r\n\r\n    }", idx_start)
if idx_end == -1:
    idx_end = content.find("return pathPoints;", idx_start)
    idx_end = content.find("}", idx_end) + 1
else:
    idx_end = idx_end + len("return pathPoints;\n\n    }")

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
        // Guarantee no same archetype twice in a row, fully randomized selection
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

        // Ensure at least 4 waypoints for Catmull-Rom
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

content = content[:idx_start] + new_path_gen + content[idx_end:]
print("Replaced procedural path generator successfully.")

# 2. Update checkBuildGate block
idx_gate_start = content.find("function checkBuildGate(now) {")
if idx_gate_start == -1:
    print("ERROR: could not find function checkBuildGate")
    sys.exit(1)

idx_dispatch = content.find("function dispatchMission(", idx_gate_start)
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

        // Automatic Section-Triggered Sequence: When section covers most of the screen
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

        // Failsafe Watchdog: elements never stay hidden > 3.5s after gate open
        elementList.forEach(item => {
            if (item.gateOpenedTime > 0 && item.state !== 'built') {
                if (now - item.gateOpenedTime > 3500) {
                    finishElementInstantly(item);
                }
            }
        });

        // Check scroll settled condition: scroll speed < 800 px/s for 100ms
        const scrollSettled = (now - lastFastScrollTime >= SCROLL_SETTLE_MS);
        if (!scrollSettled) return;

        // Strictly ONE element pulled at a time across the viewport
        if (activeMissions.length >= 1) return;

        // Available drones pool check: need at least CREW_SIZE available drones
        const availableDrones = drones.filter(d => d.state === 'FOLLOW');
        if (availableDrones.length < CREW_SIZE) return;

        // Find candidate sections in view
        for (let s = 0; s < SECTION_ORDER.length; s++) {
            const secId = SECTION_ORDER[s];
            const sec = sectionMap[secId];
            if (!sec || (!sec.dwellMet && !sec.isHero)) continue;

            const secRect = sec.el.getBoundingClientRect();
            if (secRect.bottom < 0 || secRect.top > viewH * 1.15) continue;

            // Section must not have an active mission already
            const isSectionBusy = sec.elements.some(e => e.state === 'dispatched' || e.state === 'pulling');
            if (isSectionBusy) continue;

            // Collect reachable pending elements in this section
            const reachablePending = sec.elements.filter(item => {
                if (item.state !== 'pending') return false;
                const r = item.el.getBoundingClientRect();
                return r.width > 0 && r.height > 0 && r.top <= viewH * 1.15 && r.bottom >= -50;
            });

            if (reachablePending.length === 0) continue;

            // Pick a RANDOM pending element in this section (random order, one at a time!)
            const randomIndex = Math.floor(Math.random() * reachablePending.length);
            const chosenItem = reachablePending[randomIndex];

            // Gate opens! Automatically dispatch mission for this chosen element
            dispatchMission(chosenItem, availableDrones.slice(0, CREW_SIZE), now);
            break; // Strictly one element at a time!
        }
    }

    """

content = content[:idx_gate_start] + new_check_gate + content[idx_dispatch:]
print("Replaced checkBuildGate block successfully.")

# 3. Update minDuration values in registerElements (accelerate by 0.5s)
content = re.sub(r'let minDuration = \d+;\s*\/\/\s*normal duration for cards', 'let minDuration = 350; // accelerated duration for cards (was 650ms)', content)
content = re.sub(r'minDuration = 1100;\s*\/\/\s*normal duration for section titles', 'minDuration = 600; // accelerated duration for section titles (was 1100ms)', content)
content = re.sub(r'minDuration = 900;\s*\/\/\s*normal duration for paragraphs', 'minDuration = 450; // accelerated duration for paragraphs (was 900ms)', content)
content = re.sub(r'minDuration = 450;\s*\/\/\s*normal duration for buttons', 'minDuration = 250; // accelerated duration for buttons (was 450ms)', content)
content = re.sub(r'minDuration = 1400;\s*\/\/\s*normal duration for code card', 'minDuration = 850; // accelerated duration for code card (was 1400ms)', content)

# 4. Update flight duration and return flight duration
content = re.sub(
    r'const flightDuration = Math\.round\(550 \+ Math\.random\(\) \* 300\);.*',
    'const flightDuration = Math.round(250 + Math.random() * 200); // 250-450ms accelerated flight (was 550-850ms)',
    content
)
content = re.sub(
    r'if \(flightTime < 500\) \{\s*setTimeout\(\(\) => this\.startPull\(performance\.now\(\)\), 500 - flightTime\);\s*return;\s*\}',
    'if (flightTime < 250) {\n                    setTimeout(() => this.startPull(performance.now()), 250 - flightTime);\n                    return;\n                }',
    content
)
content = re.sub(
    r'drone\.flightDuration = Math\.round\(400 \+ Math\.random\(\) \* 250\);.*',
    'drone.flightDuration = Math.round(180 + Math.random() * 120); // 180-300ms accelerated return (was 400-650ms)',
    content
)

with open(DRONES_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully written {DRONES_PATH}. Final length: {len(content)}")
