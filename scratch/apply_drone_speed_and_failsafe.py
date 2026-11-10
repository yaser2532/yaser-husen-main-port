with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Constants (BAND_TOP, BAND_BOTTOM, SCROLL_VELOCITY_LIMIT, SCROLL_SETTLE_MS, SECTION_DWELL_MS, MAX_ACTIVE_CREWS)
old_constants = """    const BAND_TOP = 0.08;   // 8% viewport height
    const BAND_BOTTOM = 0.88; // 88% viewport height
    const SCROLL_VELOCITY_LIMIT = 800; // px/s
    const SCROLL_SETTLE_MS = 80;       // ms (responsive settle <= 80ms)
    const SECTION_DWELL_MS = 120;      // ms (dwell <= 120ms)
    const MAX_ACTIVE_CREWS = 2;        // Render two random properties simultaneously in sequence"""

new_constants = """    const BAND_TOP = 0.02;   // 2% viewport height (fast identification at viewport edge)
    const BAND_BOTTOM = 0.96; // 96% viewport height
    const SCROLL_VELOCITY_LIMIT = 1600; // px/s (fluid, does not freeze on normal mouse/laptop scrolling)
    const SCROLL_SETTLE_MS = 25;       // ms (instant responsive dispatch)
    const SECTION_DWELL_MS = 20;       // ms (instant dwell recognition)
    const MAX_ACTIVE_CREWS = isMobile ? 3 : 4; // Pipeline up to 4 crews simultaneously"""

if old_constants in content:
    content = content.replace(old_constants, new_constants)
    print("Replaced constants in drones.js")
else:
    print("Error: old_constants not found")

# 2. Update pull durations (+0.3s increase across all element types)
old_durations = """                const tag = el.tagName.toLowerCase();
                let type = 'card';
                let pullDuration = 280; // Card pull: 280ms (reduced speed by 0.1s)

                if (['h1', 'h2', 'h3'].includes(tag) || el.classList.contains('section-title') || el.classList.contains('section-tag')) {
                    type = 'title';
                    pullDuration = 500; // Title scanline sweep: 500ms (reduced speed by 0.1s)
                } else if (tag === 'p' || el.classList.contains('section-desc')) {
                    type = 'paragraph';
                    pullDuration = 350; // Paragraph line sweep: 350ms (reduced speed by 0.1s)
                } else if (['a', 'button'].includes(tag) || el.classList.contains('cta-button') || el.classList.contains('filter-btn') || el.classList.contains('message-btn')) {
                    type = 'button';
                    pullDuration = 250; // Button/link snap-in: 250ms (reduced speed by 0.1s)
                } else if (el.classList.contains('code-block-visual')) {
                    type = 'code-card';
                    pullDuration = 350; // Frame 350ms, then lines 50ms each (reduced speed by 0.1s)
                }"""

new_durations = """                const tag = el.tagName.toLowerCase();
                let type = 'card';
                let pullDuration = 580; // Card pull: 580ms (+0.3s increase as requested)

                if (['h1', 'h2', 'h3'].includes(tag) || el.classList.contains('section-title') || el.classList.contains('section-tag')) {
                    type = 'title';
                    pullDuration = 800; // Title scanline sweep: 800ms (+0.3s increase as requested)
                } else if (tag === 'p' || el.classList.contains('section-desc')) {
                    type = 'paragraph';
                    pullDuration = 650; // Paragraph line sweep: 650ms (+0.3s increase as requested)
                } else if (['a', 'button'].includes(tag) || el.classList.contains('cta-button') || el.classList.contains('filter-btn') || el.classList.contains('message-btn')) {
                    type = 'button';
                    pullDuration = 550; // Button/link snap-in: 550ms (+0.3s increase as requested)
                } else if (el.classList.contains('code-block-visual')) {
                    type = 'code-card';
                    pullDuration = 650; // Frame 650ms (+0.3s increase as requested)
                }"""

if old_durations in content:
    content = content.replace(old_durations, new_durations)
    print("Replaced pull durations in drones.js")
else:
    print("Error: old_durations not found")

# 3. Update checkBuildGate with enhanced identification and rock-solid scrolled-past fail-safe
old_gate = """        // Consolidated Watchdog & Scrolled-Past Check (throttled to every 120ms to prevent scroll thrashing)
        if (now - lastWatchdogTime > 120) {
            lastWatchdogTime = now;
            elementList.forEach(item => {
                if (item.state !== 'built') {
                    if (item.dispatchTime > 0 && now - item.dispatchTime > 4500) {
                        finishElementInstantly(item);
                        return;
                    }
                    const r = item.el.getBoundingClientRect();
                    if (r.bottom < -20) {
                        finishElementInstantly(item);
                        return;
                    }
                    if (item.state === 'pending') {
                        const inView = (r.top < viewH * 0.95 && r.bottom > 20);
                        if (inView) {
                            if (!item.firstVisibleTime) {
                                item.firstVisibleTime = now;
                            } else if (now - item.firstVisibleTime > 18000) {
                                finishElementInstantly(item);
                            }
                        }
                    }
                }
            });

            // High-Velocity Rapid Scroll Catch-up (> 1200 px/s)
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
        }

        // Section Dwell Tracker (throttled to every 40ms to eliminate redundant layout reflows)
        if (now - lastDwellCheckTime > 40) {
            lastDwellCheckTime = now;
            SECTION_ORDER.forEach(secId => {
                const sec = sectionMap[secId];
                if (!sec || sec.isHero) return;

                const r = sec.el.getBoundingClientRect();
                const inBand = (r.bottom >= bandTopY && r.top <= bandBottomY + 60);

                if (inBand) {
                    if (sec.firstEnteredBandTime === 0) {
                        sec.firstEnteredBandTime = now;
                    }
                    if (now - sec.firstEnteredBandTime >= SECTION_DWELL_MS) {
                        if (!sec.dwellMet) {
                            sec.dwellMet = true;
                            sec.dwellMetTime = now;
                        }
                    }
                } else if (r.bottom < 0 || r.top > viewH) {
                    sec.firstEnteredBandTime = 0;
                }
            });
        }

        // Settle check (scroll settle <= 80ms)
        const scrollSettled = (now - lastFastScrollTime >= SCROLL_SETTLE_MS);
        if (!scrollSettled) return;

        // Pull out two random properties simultaneously in sequence
        if (activeMissions.length >= MAX_ACTIVE_CREWS) return;
        if (now - lastMissionFinishTime < 60 && activeMissions.length === 0) return;

        // Sequence Order & Band Evaluation: >= 80% inside viewport band [8%, 88%]
        for (let s = 0; s < SECTION_ORDER.length; s++) {
            const secId = SECTION_ORDER[s];
            const sec = sectionMap[secId];
            if (!sec || (!sec.dwellMet && !sec.isHero)) continue;

            const pendingElements = sec.elements.filter(item => item.state === 'pending');
            if (pendingElements.length === 0) continue;

            // Gather all pending elements in this section that satisfy the band
            const bandSatisfiedElements = [];
            for (let i = 0; i < pendingElements.length; i++) {
                const item = pendingElements[i];
                const r = item.el.getBoundingClientRect();
                if (!r || r.width === 0 || r.height === 0) continue;

                const elTop = r.top;
                const elBottom = r.bottom;
                const elHeight = r.height;

                const visibleTop = Math.max(elTop, bandTopY);
                const visibleBottom = Math.min(elBottom, bandBottomY);
                const visibleHeight = Math.max(0, visibleBottom - visibleTop);

                let satisfiesBand = false;
                if (elHeight > bandHeight) {
                    satisfiesBand = (elTop >= bandTopY - 100 && visibleHeight >= Math.min(600, bandHeight * 0.80));
                } else {
                    satisfiesBand = (visibleHeight >= elHeight * 0.80);
                }

                if (satisfiesBand) {
                    bandSatisfiedElements.push(item);
                }
            }"""

new_gate = """        // Scrolled-Past Elements & Sections Fail-Safe:
        // When a visitor scrolls past an element or section, instantly finish & reveal all passed properties
        // so if the visitor scrolls back up, the entire section is already 100% built and rendered properly!
        if (now - lastWatchdogTime > 60) {
            lastWatchdogTime = now;
            for (let i = 0; i < elementList.length; i++) {
                const item = elementList[i];
                if (item.state === 'built') continue;

                // Watchdog for hung dispatch
                if (item.dispatchTime > 0 && now - item.dispatchTime > 4500) {
                    finishElementInstantly(item);
                    continue;
                }

                const r = item.el.getBoundingClientRect();
                // Element has scrolled past upper viewport or above screen:
                if (r.bottom < viewH * 0.35) {
                    finishElementInstantly(item);
                    continue;
                }

                // In-view graceful watchdog
                if (item.state === 'pending') {
                    const inView = (r.top < viewH * 0.95 && r.bottom > 20);
                    if (inView) {
                        if (!item.firstVisibleTime) {
                            item.firstVisibleTime = now;
                        } else if (now - item.firstVisibleTime > 5000) {
                            finishElementInstantly(item);
                        }
                    }
                }
            }

            // Section-Level Scrolled-Past Guarantee:
            // If visitor scrolled past a section (bottom passed above 50% viewport or top < -100px),
            // reveal all its remaining elements immediately.
            SECTION_ORDER.forEach(secId => {
                const sec = sectionMap[secId];
                if (!sec || sec.isHero) return;
                const r = sec.el.getBoundingClientRect();
                if (r.bottom < viewH * 0.55 || r.top < -120) {
                    sec.elements.forEach(item => {
                        if (item.state !== 'built') {
                            finishElementInstantly(item);
                        }
                    });
                }
            });
        }

        // Section Dwell Tracker (ultra-fast 20ms recognition)
        if (now - lastDwellCheckTime > 25) {
            lastDwellCheckTime = now;
            SECTION_ORDER.forEach(secId => {
                const sec = sectionMap[secId];
                if (!sec || sec.isHero) return;

                const r = sec.el.getBoundingClientRect();
                const inBand = (r.bottom >= bandTopY && r.top <= bandBottomY + 80);

                if (inBand) {
                    if (sec.firstEnteredBandTime === 0) {
                        sec.firstEnteredBandTime = now;
                    }
                    if (now - sec.firstEnteredBandTime >= SECTION_DWELL_MS) {
                        if (!sec.dwellMet) {
                            sec.dwellMet = true;
                            sec.dwellMetTime = now;
                        }
                    }
                } else if (r.bottom < 0 || r.top > viewH) {
                    sec.firstEnteredBandTime = 0;
                }
            });
        }

        // Settle check (fast settle <= 25ms, fluid scrolling)
        const scrollSettled = (now - lastFastScrollTime >= SCROLL_SETTLE_MS);
        if (!scrollSettled) return;

        // Pull out properties in sequence (up to MAX_ACTIVE_CREWS pipelined)
        if (activeMissions.length >= MAX_ACTIVE_CREWS) return;
        if (now - lastMissionFinishTime < 30 && activeMissions.length === 0) return;

        // Sequence Order & Band Evaluation: fast identification as soon as entering viewport
        for (let s = 0; s < SECTION_ORDER.length; s++) {
            const secId = SECTION_ORDER[s];
            const sec = sectionMap[secId];
            if (!sec || (!sec.dwellMet && !sec.isHero)) continue;

            const pendingElements = sec.elements.filter(item => item.state === 'pending');
            if (pendingElements.length === 0) continue;

            // Gather all pending elements in this section that satisfy the band
            const bandSatisfiedElements = [];
            for (let i = 0; i < pendingElements.length; i++) {
                const item = pendingElements[i];
                const r = item.el.getBoundingClientRect();
                if (!r || r.width === 0 || r.height === 0) continue;

                const elTop = r.top;
                const elBottom = r.bottom;
                const elHeight = r.height;

                const visibleTop = Math.max(elTop, bandTopY);
                const visibleBottom = Math.min(elBottom, bandBottomY);
                const visibleHeight = Math.max(0, visibleBottom - visibleTop);

                // Responsive identification: fast recognition as soon as element enters the viewport
                let satisfiesBand = false;
                if (elHeight > bandHeight) {
                    satisfiesBand = (elTop >= bandTopY - 120 && visibleHeight >= 80);
                } else {
                    satisfiesBand = (visibleHeight >= Math.min(elHeight * 0.35, 100)) || (elTop >= bandTopY && elTop <= bandBottomY);
                }

                if (satisfiesBand) {
                    bandSatisfiedElements.push(item);
                }
            }"""

if old_gate in content:
    content = content.replace(old_gate, new_gate)
    print("Replaced checkBuildGate in drones.js")
else:
    print("Error: old_gate not found")

# 4. Zero Layout Thrash in updateActiveMissions
old_dispatch = """        const geom = computeTractorGeometry(item);
        item.anchors = geom.anchors;
        item.hoverPositions = geom.hoverPositions;

        // Visible flight: 300ms (>= 300ms, total dispatch-to-reveal <= 450ms)
        const HIVE_PULSE_MS = 80;
        const FLIGHT_TIME_MS = 300;
        const totalFlightDuration = HIVE_PULSE_MS + FLIGHT_TIME_MS;

        // Hive pulse condensation at cursor
        emitPulseRing(cursorX, cursorY, THEME.gold, 32, 200);

        const mission = {
            item,
            crew: crewDrones,
            dispatchedAt: now,
            hivePulseDuration: HIVE_PULSE_MS,
            flightDuration: totalFlightDuration,
            arrivedCount: 0,
            pullStartedAt: 0,
            pullDuration: item.pullDuration,
            lockOnStart: 0,"""

new_dispatch = """        const geom = computeTractorGeometry(item);
        item.anchors = geom.anchors;
        item.hoverPositions = geom.hoverPositions;

        const initScrollY = window.scrollY || window.pageYOffset;
        const initScrollX = window.scrollX || window.pageXOffset;

        // Visible flight: 300ms
        const HIVE_PULSE_MS = 80;
        const FLIGHT_TIME_MS = 300;
        const totalFlightDuration = HIVE_PULSE_MS + FLIGHT_TIME_MS;

        // Hive pulse condensation at cursor
        emitPulseRing(cursorX, cursorY, THEME.gold, 32, 200);

        const mission = {
            item,
            crew: crewDrones,
            dispatchedAt: now,
            hivePulseDuration: HIVE_PULSE_MS,
            flightDuration: totalFlightDuration,
            arrivedCount: 0,
            pullStartedAt: 0,
            pullDuration: item.pullDuration,
            lockOnStart: 0,
            dispatchScrollY: initScrollY,
            dispatchScrollX: initScrollX,
            baseAnchors: geom.anchors.map(a => ({ x: a.x + initScrollX, y: a.y + initScrollY })),
            baseHoverPositions: geom.hoverPositions.map(h => ({ x: h.x + initScrollX, y: h.y + initScrollY })),"""

if old_dispatch in content:
    content = content.replace(old_dispatch, new_dispatch)
    print("Replaced dispatchMission in drones.js")
else:
    print("Error: old_dispatch not found")

old_update_missions = """    function updateActiveMissions(now, dt) {
        for (let i = activeMissions.length - 1; i >= 0; i--) {
            const m = activeMissions[i];
            const item = m.item;

            // Maintain anchor positions with scroll
            const geom = computeTractorGeometry(item);
            m.anchors = geom.anchors;
            m.hoverPositions = geom.hoverPositions;

            m.crew.forEach((d, idx) => {
                d.targetAnchor = geom.anchors[idx % geom.anchors.length];
                d.hoverPos = geom.hoverPositions[idx % geom.hoverPositions.length];
            });"""

new_update_missions = """    function updateActiveMissions(now, dt) {
        const curScrollY = window.scrollY || window.pageYOffset;
        const curScrollX = window.scrollX || window.pageXOffset;

        for (let i = activeMissions.length - 1; i >= 0; i--) {
            const m = activeMissions[i];
            const item = m.item;

            // Pure arithmetic scroll-offset tracking: ZERO forced layouts in rAF loop!
            m.anchors = m.baseAnchors.map(a => ({ x: a.x - curScrollX, y: a.y - curScrollY }));
            m.hoverPositions = m.baseHoverPositions.map(h => ({ x: h.x - curScrollX, y: h.y - curScrollY }));

            m.crew.forEach((d, idx) => {
                d.targetAnchor = m.anchors[idx % m.anchors.length];
                d.hoverPos = m.hoverPositions[idx % m.hoverPositions.length];
            });"""

if old_update_missions in content:
    content = content.replace(old_update_missions, new_update_missions)
    print("Replaced updateActiveMissions in drones.js")
else:
    print("Error: old_update_missions not found")

with open('assets/js/drones.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully written updated drones.js")
