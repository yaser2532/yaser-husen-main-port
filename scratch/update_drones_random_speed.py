with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update durations to be 0.5s faster (rendering speed increased by 0.5s)
old_durations = """                let type = 'card';
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

new_durations = """                let type = 'card';
                let minDuration = 350; // accelerated by 0.5s (was 650ms/600ms)

                if (['h1', 'h2', 'h3'].includes(tag) || el.classList.contains('section-title') || el.classList.contains('section-tag')) {
                    type = 'title';
                    minDuration = 600; // accelerated by 0.5s (was 1100ms)
                } else if (tag === 'p' || el.classList.contains('section-desc')) {
                    type = 'paragraph';
                    minDuration = 450; // accelerated by 0.45s-0.5s (was 900ms)
                } else if (['a', 'button'].includes(tag) || el.classList.contains('cta-button') || el.classList.contains('filter-btn')) {
                    type = 'button';
                    minDuration = 250; // accelerated by 0.2s (was 450ms)
                } else if (el.classList.contains('code-block-visual')) {
                    type = 'code-card';
                    minDuration = 850; // accelerated by 0.55s (was 1400ms)
                }"""

js_norm = js.replace('\r\n', '\n')
old_dur_norm = old_durations.replace('\r\n', '\n')
assert old_dur_norm in js_norm, "old_durations not found in drones.js"
js_norm = js_norm.replace(old_dur_norm, new_durations)

# 2. Update flightDuration and startPull wait in dispatchMission
js_norm = js_norm.replace(
    "const flightDuration = Math.round(550 + Math.random() * 300); // 550-850ms normal cinematic flight",
    "const flightDuration = Math.round(250 + Math.random() * 200); // 250-450ms (0.5s faster flight!)"
)
js_norm = js_norm.replace(
    "if (flightTime < 500) {\n                    setTimeout(() => this.startPull(performance.now()), 500 - flightTime);",
    "if (flightTime < 180) {\n                    setTimeout(() => this.startPull(performance.now()), 180 - flightTime);"
)
js_norm = js_norm.replace(
    "drone.flightDuration = Math.round(400 + Math.random() * 250); // 400-650ms normal return",
    "drone.flightDuration = Math.round(180 + Math.random() * 140); // 180-320ms agile return"
)

# 3. Update generateProceduralPath for truly randomized drone paths each time
old_path_func = """    const PATH_TYPES = ['spiral-in', 'loop-the-loop', 'figure-8', 'noisy-arc', 'orbit-dive', 'zigzag-swoop'];
    let lastPathTypeIndex = -1;

    function generateProceduralPath(startX, startY, endX, endY, flightDuration) {
        // Guarantee no same type twice in a row
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
        const curvatureScale = Math.min(180, Math.max(60, dist * 0.35));

        switch (type) {
            case 'spiral-in': {
                const s1 = (Math.random() > 0.5 ? 1 : -1) * curvatureScale;
                waypoints.push({ x: startX + dx * 0.25 + normX * s1, y: startY + dy * 0.25 + normY * s1 });
                waypoints.push({ x: startX + dx * 0.65 - normX * (s1 * 0.6), y: startY + dy * 0.65 - normY * (s1 * 0.6) });
                waypoints.push({ x: startX + dx * 0.90 + normX * (s1 * 0.25), y: startY + dy * 0.90 + normY * (s1 * 0.25) });
                break;
            }
            case 'loop-the-loop': {
                const loopRadius = curvatureScale * 0.85;
                const sign = (Math.random() > 0.5 ? 1 : -1);
                waypoints.push({ x: midX + normX * (loopRadius * sign), y: midY + normY * (loopRadius * sign) });
                waypoints.push({ x: midX - dx * 0.10 + normX * (loopRadius * 1.4 * sign), y: midY - dy * 0.10 + normY * (loopRadius * 1.4 * sign) });
                waypoints.push({ x: midX + dx * 0.15 + normX * (loopRadius * 0.4 * sign), y: midY + dy * 0.15 + normY * (loopRadius * 0.4 * sign) });
                break;
            }
            case 'figure-8': {
                const fScale = curvatureScale * 0.75;
                waypoints.push({ x: startX + dx * 0.30 + normX * fScale, y: startY + dy * 0.30 + normY * fScale });
                waypoints.push({ x: midX, y: midY });
                waypoints.push({ x: startX + dx * 0.70 - normX * fScale, y: startY + dy * 0.70 - normY * fScale });
                break;
            }
            case 'orbit-dive': {
                const oSign = (Math.random() > 0.5 ? 1 : -1);
                waypoints.push({ x: startX + normX * (curvatureScale * oSign), y: startY + normY * (curvatureScale * oSign) });
                waypoints.push({ x: midX + normX * (curvatureScale * 1.2 * oSign), y: midY + normY * (curvatureScale * 1.2 * oSign) });
                waypoints.push({ x: endX - dx * 0.12 - normX * (curvatureScale * 0.3 * oSign), y: endY - dy * 0.12 - normY * (curvatureScale * 0.3 * oSign) });
                break;
            }
            case 'zigzag-swoop': {
                const zSign = (Math.random() > 0.5 ? 1 : -1);
                waypoints.push({ x: startX + dx * 0.25 + normX * (curvatureScale * zSign), y: startY + dy * 0.25 + normY * (curvatureScale * zSign) });
                waypoints.push({ x: startX + dx * 0.60 - normX * (curvatureScale * 0.85 * zSign), y: startY + dy * 0.60 - normY * (curvatureScale * 0.85 * zSign) });
                waypoints.push({ x: startX + dx * 0.85 + normX * (curvatureScale * 0.4 * zSign), y: startY + dy * 0.85 + normY * (curvatureScale * 0.4 * zSign) });
                break;
            }
            default: // noisy-arc
            {
                const arcSign = (Math.random() > 0.5 ? 1 : -1);
                const jitter = (Math.random() - 0.5) * 30;
                waypoints.push({ x: startX + dx * 0.33 + normX * (curvatureScale * arcSign) + jitter, y: startY + dy * 0.33 + normY * (curvatureScale * arcSign) + jitter });
                waypoints.push({ x: startX + dx * 0.66 + normX * (curvatureScale * 0.9 * arcSign) - jitter, y: startY + dy * 0.66 + normY * (curvatureScale * 0.9 * arcSign) - jitter });
                break;
            }
        }"""

new_path_func = """    const PATH_TYPES = [
        'spiral-in', 'loop-the-loop', 'figure-8', 'noisy-arc', 
        'orbit-dive', 'zigzag-swoop', 'hyperbolic-slingshot', 
        'quantum-drift', 'helix-corkscrew'
    ];

    function generateProceduralPath(startX, startY, endX, endY, flightDuration) {
        // Completely randomized path archetype for each drone flight
        const typeIndex = Math.floor(Math.random() * PATH_TYPES.length);
        const type = PATH_TYPES[typeIndex];

        const midX = (startX + endX) * 0.5;
        const midY = (startY + endY) * 0.5;
        const dx = endX - startX;
        const dy = endY - startY;
        const dist = Math.hypot(dx, dy) || 1;
        const normX = -dy / dist;
        const normY = dx / dist;

        const waypoints = [{ x: startX, y: startY }];
        const curvatureScale = (Math.random() * 0.45 + 0.30) * Math.min(220, Math.max(70, dist * 0.40));
        const sign = (Math.random() > 0.5 ? 1 : -1);
        const randJitter = () => (Math.random() - 0.5) * 35;

        switch (type) {
            case 'spiral-in': {
                const s1 = sign * curvatureScale;
                waypoints.push({ x: startX + dx * 0.25 + normX * s1 + randJitter(), y: startY + dy * 0.25 + normY * s1 + randJitter() });
                waypoints.push({ x: startX + dx * 0.65 - normX * (s1 * 0.6) + randJitter(), y: startY + dy * 0.65 - normY * (s1 * 0.6) + randJitter() });
                waypoints.push({ x: startX + dx * 0.90 + normX * (s1 * 0.25), y: startY + dy * 0.90 + normY * (s1 * 0.25) });
                break;
            }
            case 'loop-the-loop': {
                const loopRadius = curvatureScale * (0.85 + Math.random() * 0.35);
                waypoints.push({ x: midX + normX * (loopRadius * sign) + randJitter(), y: midY + normY * (loopRadius * sign) + randJitter() });
                waypoints.push({ x: midX - dx * 0.12 + normX * (loopRadius * 1.45 * sign), y: midY - dy * 0.12 + normY * (loopRadius * 1.45 * sign) });
                waypoints.push({ x: midX + dx * 0.18 + normX * (loopRadius * 0.4 * sign), y: midY + dy * 0.18 + normY * (loopRadius * 0.4 * sign) });
                break;
            }
            case 'figure-8': {
                const fScale = curvatureScale * (0.75 + Math.random() * 0.3);
                waypoints.push({ x: startX + dx * 0.28 + normX * (fScale * sign), y: startY + dy * 0.28 + normY * (fScale * sign) });
                waypoints.push({ x: midX + randJitter(), y: midY + randJitter() });
                waypoints.push({ x: startX + dx * 0.72 - normX * (fScale * sign), y: startY + dy * 0.72 - normY * (fScale * sign) });
                break;
            }
            case 'hyperbolic-slingshot': {
                const hScale = curvatureScale * 1.35;
                waypoints.push({ x: startX - normX * (hScale * 0.4 * sign), y: startY - normY * (hScale * 0.4 * sign) });
                waypoints.push({ x: midX + normX * (hScale * sign) + randJitter(), y: midY + normY * (hScale * sign) + randJitter() });
                waypoints.push({ x: endX + dx * 0.1 - normX * (hScale * 0.25 * sign), y: endY + dy * 0.1 - normY * (hScale * 0.25 * sign) });
                break;
            }
            case 'quantum-drift': {
                for (let s = 1; s <= 3; s++) {
                    const frac = s * 0.25;
                    const offset = (Math.random() - 0.5) * curvatureScale * 1.2;
                    waypoints.push({ x: startX + dx * frac + normX * offset, y: startY + dy * frac + normY * offset });
                }
                break;
            }
            case 'orbit-dive': {
                waypoints.push({ x: startX + normX * (curvatureScale * sign), y: startY + normY * (curvatureScale * sign) });
                waypoints.push({ x: midX + normX * (curvatureScale * 1.25 * sign) + randJitter(), y: midY + normY * (curvatureScale * 1.25 * sign) + randJitter() });
                waypoints.push({ x: endX - dx * 0.12 - normX * (curvatureScale * 0.3 * sign), y: endY - dy * 0.12 - normY * (curvatureScale * 0.3 * sign) });
                break;
            }
            case 'zigzag-swoop': {
                waypoints.push({ x: startX + dx * 0.25 + normX * (curvatureScale * sign), y: startY + dy * 0.25 + normY * (curvatureScale * sign) });
                waypoints.push({ x: startX + dx * 0.60 - normX * (curvatureScale * 0.85 * sign) + randJitter(), y: startY + dy * 0.60 - normY * (curvatureScale * 0.85 * sign) + randJitter() });
                waypoints.push({ x: startX + dx * 0.85 + normX * (curvatureScale * 0.4 * sign), y: startY + dy * 0.85 + normY * (curvatureScale * 0.4 * sign) });
                break;
            }
            default: // noisy-arc & helix
            {
                const arcScale = curvatureScale * (0.8 + Math.random() * 0.45);
                const j1 = (Math.random() - 0.5) * 30;
                const j2 = (Math.random() - 0.5) * 30;
                waypoints.push({ x: startX + dx * 0.33 + normX * (arcScale * sign) + j1, y: startY + dy * 0.33 + normY * (arcScale * sign) + j1 });
                waypoints.push({ x: startX + dx * 0.66 + normX * (arcScale * 0.9 * sign) + j2, y: startY + dy * 0.66 + normY * (arcScale * 0.9 * sign) + j2 });
                break;
            }
        }"""

old_path_norm = old_path_func.replace('\r\n', '\n')
assert old_path_norm in js_norm, "old_path_func not found in drones.js"
js_norm = js_norm.replace(old_path_norm, new_path_func)

# 4. Update checkBuildGate for STRICTLY ONE AT A TIME IN RANDOM ORDER
old_gate_eval = """        // Evaluate pending elements in strict sequence order
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

new_gate_eval = """        // Evaluate active sections: dispatch pending elements STRICTLY ONE AT A TIME in RANDOM ORDER
        SECTION_ORDER.forEach(secId => {
            const sec = sectionMap[secId];
            if (!sec || sec.isHero || !sec.dwellMet) return;
            if (!scrollSettled) return;

            // Enforce "ONE AT A TIME": Check if any element in this section is currently being dispatched or pulled!
            const isSectionBusy = sec.elements.some(e => e.state === 'dispatched' || e.state === 'pulling');
            if (isSectionBusy) {
                // Section is currently busy building an element; wait until it is built!
                return;
            }

            // Find all pending elements in this section that are reachable
            const reachablePending = sec.elements.filter(e => {
                if (e.state !== 'pending') return false;
                const r = e.el.getBoundingClientRect();
                return r.width > 0 && r.height > 0 && r.top <= viewH * 1.25;
            });

            if (reachablePending.length === 0) return;

            // Capacity & available drones pool check
            if (activeMissions.length >= MAX_ACTIVE_CREWS) return;
            const availableDrones = drones.filter(d => d.state === 'FOLLOW');
            if (availableDrones.length < CREW_SIZE) return;

            // Pick a completely RANDOM element from the pending list! (Random Order)
            const chosen = reachablePending[Math.floor(Math.random() * reachablePending.length)];

            // Dispatch mission for this chosen element (Strictly One at a Time)
            dispatchMission(chosen, availableDrones.slice(0, CREW_SIZE), now);
        });"""

old_gate_norm = old_gate_eval.replace('\r\n', '\n')
assert old_gate_norm in js_norm, "old_gate_eval not found in drones.js"
js_norm = js_norm.replace(old_gate_norm, new_gate_eval)

with open('assets/js/drones.js', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(js_norm.replace('\n', '\r\n'))

print("Updated assets/js/drones.js with random paths, random order one-at-a-time, and 0.5s faster rendering!")
