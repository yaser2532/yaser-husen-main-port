with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    content = f.read()

old_code = """    // ─── 9. GATE EVALUATOR & PIPELINED MISSION DISPATCHER ───────────────────
    const activeMissions = [];
    let lastDispatchTimestamp = 0;
    let firstRevealTimestamp = 0;
    let lastMissionFinishTime = 0;

    function checkBuildGate(now) {
        if (isReducedMotion) {
            revealAllInstantly();
            return;
        }

        const scrollY = window.scrollY || window.pageYOffset;
        const bandTopY = viewH * BAND_TOP;
        const bandBottomY = viewH * BAND_BOTTOM;
        const bandHeight = bandBottomY - bandTopY;

        // Footer reached failsafe
        const isAtBottom = (window.innerHeight + scrollY >= document.documentElement.scrollHeight - 100);
        if (isAtBottom) {
            elementList.forEach(item => {
                if (item.state !== 'built') finishElementInstantly(item);
            });
            return;
        }

        // Failsafe 1: Scrolled-Past Elements Guarantee
        elementList.forEach(item => {
            if (item.state !== 'built') {
                const r = item.el.getBoundingClientRect();
                if (r.bottom < -20) {
                    finishElementInstantly(item);
                }
            }
        });

        // Decay scroll speed if scrolling has stopped
        if (now - lastScrollTime > 60) {
            currentScrollSpeed = 0;
        }

        // Failsafe 2: High-Velocity Rapid Scroll Catch-up (> 1200 px/s)
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

        // Failsafe 3: Deep In-View Graceful Watchdog (18.0s)
        elementList.forEach(item => {
            if (item.state === 'pending') {
                const r = item.el.getBoundingClientRect();
                const inView = (r.top < viewH * 0.95 && r.bottom > 20);
                if (inView) {
                    if (!item.firstVisibleTime) {
                        item.firstVisibleTime = now;
                    } else if (now - item.firstVisibleTime > 18000) {
                        finishElementInstantly(item);
                    }
                }
            }
        });

        // Section Dwell Tracker (dwell <= 120ms)
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

        // Failsafe Watchdog: dispatched elements never hang > 4.5s
        elementList.forEach(item => {
            if (item.dispatchTime > 0 && item.state !== 'built') {
                if (now - item.dispatchTime > 4500) {
                    finishElementInstantly(item);
                }
            }
        });

        // Settle check (scroll settle <= 80ms)
        const scrollSettled = (now - lastFastScrollTime >= SCROLL_SETTLE_MS);
        if (!scrollSettled) return;"""

new_code = """    // ─── 9. GATE EVALUATOR & PIPELINED MISSION DISPATCHER ───────────────────
    const activeMissions = [];
    let lastDispatchTimestamp = 0;
    let firstRevealTimestamp = 0;
    let lastMissionFinishTime = 0;
    let lastWatchdogTime = 0;
    let lastDwellCheckTime = 0;

    function checkBuildGate(now) {
        if (isReducedMotion) {
            revealAllInstantly();
            return;
        }

        // Decay scroll speed if scrolling has stopped
        if (now - lastScrollTime > 60) {
            currentScrollSpeed = 0;
        }

        const scrollY = window.scrollY || window.pageYOffset;
        const bandTopY = viewH * BAND_TOP;
        const bandBottomY = viewH * BAND_BOTTOM;
        const bandHeight = bandBottomY - bandTopY;

        // Footer reached failsafe
        const isAtBottom = (window.innerHeight + scrollY >= document.documentElement.scrollHeight - 100);
        if (isAtBottom) {
            elementList.forEach(item => {
                if (item.state !== 'built') finishElementInstantly(item);
            });
            return;
        }

        // Consolidated Watchdog & Scrolled-Past Check (throttled to every 120ms to prevent scroll thrashing)
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
        if (!scrollSettled) return;"""

if old_code in content:
    content = content.replace(old_code, new_code)
    with open('assets/js/drones.js', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully optimized drones.js checkBuildGate")
else:
    print("Error: old_code block not found in drones.js")
