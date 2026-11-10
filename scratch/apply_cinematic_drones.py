with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update minDuration settings for cinematic, perceptible presence
js = js.replace("let minDuration = 350; // accelerated duration for cards (was 650ms)", "let minDuration = 800; // cinematic duration for cards")
js = js.replace("minDuration = 600; // accelerated duration for section titles (was 1100ms)", "minDuration = 750; // cinematic duration for section titles")
js = js.replace("minDuration = 450; // accelerated duration for paragraphs (was 900ms)", "minDuration = 650; // cinematic duration for paragraphs")
js = js.replace("minDuration = 250; // accelerated duration for buttons (was 450ms)", "minDuration = 500; // cinematic duration for buttons")
js = js.replace("minDuration = 850; // accelerated duration for code card (was 1400ms)", "minDuration = 1150; // cinematic duration for code terminal IDE card")

# 2. Update Drone updatePull method to hover in towing formation
old_update_pull = """        updatePull(now, dt) {

            // Latch onto target anchor with slight high-frequency micro-jitter

            const jitterX = Math.sin(now * 0.05 + this.id * 1.5) * 1.8;

            const jitterY = Math.cos(now * 0.06 + this.id * 1.2) * 1.8;

            this.x = this.targetAnchor.x + jitterX;

            this.y = this.targetAnchor.y + jitterY;

            this.opacity = 1.0;

        }"""

new_update_pull = """        updatePull(now, dt) {

            // Hover in airspace towing position with vertical tension and micro-jitter

            const hover = this.hoverPos || (this.targetAnchor ? { x: this.targetAnchor.x, y: this.targetAnchor.y - 65 } : { x: this.x, y: this.y });

            const jitterX = Math.sin(now * 0.045 + this.id * 1.7) * 2.5;

            const jitterY = Math.cos(now * 0.055 + this.id * 1.3) * 2.2 - 2.5; // upward towing tension

            this.x = hover.x + jitterX;

            this.y = hover.y + jitterY;

            this.opacity = 1.0;

        }"""

if old_update_pull in js:
    js = js.replace(old_update_pull, new_update_pull)
    print("Updated Drone.updatePull to hover in towing formation!")
else:
    print("Warning: old_update_pull not matched verbatim in drones.js, inspecting...")

# 3. Update computeAnchors to computeTractorGeometry with both contact anchors and airspace hover positions
old_compute_anchors = """    function computeAnchors(item) {

        const r = item.el.getBoundingClientRect();

        const anchors = [];

        const w = r.width;

        const h = r.height;

        anchors.push({ x: r.left + 16, y: r.top + h * 0.5 });

        anchors.push({ x: r.right - 16, y: r.top + h * 0.5 });

        anchors.push({ x: r.left + w * 0.35, y: r.top + 8 });

        anchors.push({ x: r.left + w * 0.65, y: r.bottom - 8 });

        return anchors;

    }"""

new_compute_anchors = """    function computeTractorGeometry(item) {

        const r = item.el.getBoundingClientRect();

        const w = Math.max(40, r.width);

        const h = Math.max(30, r.height);

        // Contact points ON the element where the tractor beams lock

        const anchors = [

            { x: r.left + Math.min(28, w * 0.20), y: r.top + 8 },

            { x: r.right - Math.min(28, w * 0.20), y: r.top + 8 },

            { x: r.left + w * 0.38, y: r.top + 6 },

            { x: r.left + w * 0.62, y: r.top + 6 }

        ];

        // Airspace positions 55px to 80px ABOVE/BESIDE the element where drones hover in towing formation

        const hoverPositions = [

            { x: r.left - 25, y: r.top - 60 },

            { x: r.right + 25, y: r.top - 60 },

            { x: r.left + w * 0.38 - 12, y: r.top - 75 },

            { x: r.left + w * 0.62 + 12, y: r.top - 75 }

        ];

        return { anchors, hoverPositions };

    }

    function computeAnchors(item) {

        return computeTractorGeometry(item).anchors;

    }"""

if old_compute_anchors in js:
    js = js.replace(old_compute_anchors, new_compute_anchors)
    print("Updated computeAnchors and added computeTractorGeometry!")
else:
    print("Warning: old_compute_anchors not matched verbatim, inspecting...")

# 4. Remove Failsafe 3 (the 1200ms watchdog that prematurely revealed pending elements)
old_failsafe_3 = """        // Failsafe 3: Active Viewport Emergency Watchdog

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

        });"""

new_failsafe_3 = """        // Failsafe 3: Deep In-View Graceful Watchdog (Guarantees drones have ample time to pull each element)

        // Only after an element has remained un-pulled in view for > 18.0s (e.g. user parked on a section) does it fallback

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

        });"""

if old_failsafe_3 in js:
    js = js.replace(old_failsafe_3, new_failsafe_3)
    print("Replaced premature 1200ms watchdog with patient 18s fallback!")
else:
    print("Warning: old_failsafe_3 not matched verbatim, inspecting...")

# 5. Update dispatchMission, flight duration, and pulling motion
old_dispatch = """        item.el.setAttribute('data-drone-state', 'flight');

        const anchors = computeAnchors(item);

        item.anchors = anchors;

        const flightDuration = Math.round(250 + Math.random() * 200); // 250-450ms accelerated flight (was 550-850ms)
        

        const mission = {

            item,

            crew: crewDrones,

            dispatchedAt: now,

            flightDuration,

            arrivedCount: 0,

            pullStartedAt: 0,

            pullDuration: item.minDuration,

            onDroneArrived(drone) {

                this.arrivedCount++;

                if (drone.targetAnchor) {

                    emitPulseRing(drone.targetAnchor.x, drone.targetAnchor.y, THEME.cyan, 22, 220);

                    emitPlasmaSparks(drone.targetAnchor.x, drone.targetAnchor.y, 4);

                }

                if (this.arrivedCount >= this.crew.length) {

                    this.startPull(performance.now());

                }

            },

            startPull(pullNow) {

                const flightTime = pullNow - this.dispatchedAt;

                // Spectacle guarantee: reveal may start only after crew has flown >= 500ms

                if (flightTime < 250) {

                    setTimeout(() => this.startPull(performance.now()), 250 - flightTime);

                    return;

                }

                this.pullStartedAt = pullNow;

                this.item.state = 'pulling';

                this.item.el.setAttribute('data-drone-state', 'pulling');

                // Arrival flourish: 80ms RGB-split & spark burst

                this.item.el.classList.add('drone-arrival-flourish');

                setTimeout(() => this.item.el.classList.remove('drone-arrival-flourish'), 160);

                this.anchors.forEach(a => {

                    emitPulseRing(a.x, a.y, THEME.gold, 26, 260);

                    emitPlasmaSparks(a.x, a.y, 8);

                });

            }

        };

        // Assign procedural path to each crew drone & emit launch gravitational pulse ring

        crewDrones.forEach((drone, idx) => {

            drone.state = 'DISPATCH';

            drone.activeMission = mission;

            drone.crewIndex = idx;

            drone.flightStart = now;

            drone.flightDuration = flightDuration + idx * 20; // tighter stagger

            const anchor = anchors[idx % anchors.length];

            drone.targetAnchor = anchor;

            drone.pathPoints = generateProceduralPath(drone.x, drone.y, anchor.x, anchor.y, drone.flightDuration);

            // Gravitational launch pulse ring

            emitPulseRing(drone.x, drone.y, drone.color, 24, 250);

        });"""

new_dispatch = """        item.el.setAttribute('data-drone-state', 'flight');

        const geom = computeTractorGeometry(item);

        item.anchors = geom.anchors;

        item.hoverPositions = geom.hoverPositions;

        const flightDuration = Math.round(450 + Math.random() * 150); // 450-600ms cinematic flight

        const mission = {

            item,

            crew: crewDrones,

            dispatchedAt: now,

            flightDuration,

            arrivedCount: 0,

            pullStartedAt: 0,

            pullDuration: item.minDuration,

            onDroneArrived(drone) {

                this.arrivedCount++;

                if (drone.targetAnchor) {

                    emitPulseRing(drone.targetAnchor.x, drone.targetAnchor.y, THEME.cyan, 26, 240);

                    emitPlasmaSparks(drone.targetAnchor.x, drone.targetAnchor.y, 4);

                }

                if (this.arrivedCount >= this.crew.length) {

                    this.startPull(performance.now());

                }

            },

            startPull(pullNow) {

                this.pullStartedAt = pullNow;

                this.item.state = 'pulling';

                this.item.el.setAttribute('data-drone-state', 'pulling');

                // Arrival flourish: 120ms RGB-split & spark burst

                this.item.el.classList.add('drone-arrival-flourish');

                setTimeout(() => this.item.el.classList.remove('drone-arrival-flourish'), 160);

                this.anchors.forEach(a => {

                    emitPulseRing(a.x, a.y, THEME.gold, 30, 280);

                    emitPlasmaSparks(a.x, a.y, 6);

                });

            }

        };

        // Assign procedural curved paths to airspace hover positions ABOVE the element

        crewDrones.forEach((drone, idx) => {

            drone.state = 'DISPATCH';

            drone.activeMission = mission;

            drone.crewIndex = idx;

            drone.flightStart = now;

            drone.flightDuration = flightDuration + idx * 30;

            const anchor = geom.anchors[idx % geom.anchors.length];

            const hover = geom.hoverPositions[idx % geom.hoverPositions.length];

            drone.targetAnchor = anchor;

            drone.hoverPos = hover;

            // Drones fly to the towing airspace position, NOT into the element surface!

            drone.pathPoints = generateProceduralPath(drone.x, drone.y, hover.x, hover.y, drone.flightDuration);

            // Gravitational launch pulse ring

            emitPulseRing(drone.x, drone.y, drone.color, 24, 250);

        });"""

if old_dispatch in js:
    js = js.replace(old_dispatch, new_dispatch)
    print("Updated dispatchMission with hover geometry and cinematic flight!")
else:
    print("Warning: old_dispatch not matched verbatim, inspecting...")

# 6. Update updateActiveMissions pulling displacement
old_pull_motion = """            if (item.state === 'pulling') {

                const pullElapsed = now - m.pullStartedAt;

                const progress = Math.min(1.0, pullElapsed / m.pullDuration);

                const easeProg = easeOutQuart(progress);

                // Compositor-friendly transform & opacity

                const offsetY = Math.round(32 * (1 - easeProg));

                item.el.style.transform = `translate3d(0, ${offsetY}px, 0)`;

                item.el.style.opacity = Math.min(1.0, 0.25 + easeProg * 0.75).toFixed(3);

                item.el.style.filter = `blur(${Math.max(0, (1 - easeProg) * 2).toFixed(1)}px)`;

                // Dynamic laser weld sparks along edge

                if (Math.random() < 0.35) {

                    const r = item.el.getBoundingClientRect();

                    emitSparks(r.left + Math.random() * r.width, r.top + r.height * easeProg, 2);

                }"""

new_pull_motion = """            if (item.state === 'pulling') {

                const pullElapsed = now - m.pullStartedAt;

                const progress = Math.min(1.0, pullElapsed / m.pullDuration);

                const easeProg = easeOutQuart(progress);

                // Physically pull the element out of depth: from 55px down & 0.94 scale to 0px & 1.0 scale!

                const offsetY = Math.round(55 * (1 - easeProg));

                const scale = (0.94 + 0.06 * easeProg).toFixed(3);

                const opacity = Math.min(1.0, 0.15 + easeProg * 0.85).toFixed(3);

                const blur = Math.max(0, (1 - easeProg) * 4).toFixed(1);

                item.el.style.transform = `translate3d(0, ${offsetY}px, 0) scale(${scale})`;

                item.el.style.opacity = opacity;

                item.el.style.filter = `blur(${blur}px)`;

                // Dynamic quantum welding sparks along tractor contact anchors

                if (Math.random() < 0.45) {

                    const cAnchor = m.anchors[Math.floor(Math.random() * m.anchors.length)];

                    if (cAnchor) emitPlasmaSparks(cAnchor.x, cAnchor.y, 2);

                }"""

if old_pull_motion in js:
    js = js.replace(old_pull_motion, new_pull_motion)
    print("Updated pulling displacement to 55px scale/blur physically hauling into place!")
else:
    print("Warning: old_pull_motion not matched verbatim, inspecting...")

# Update anchor tracking during scroll
old_scroll_track = """            // Recompute anchors if element moves during scroll

            m.anchors = computeAnchors(item);

            m.crew.forEach((d, idx) => {

                if (m.anchors[idx % m.anchors.length]) {

                    d.targetAnchor = m.anchors[idx % m.anchors.length];

                }

            });"""

new_scroll_track = """            // Recompute anchors and hover positions if element moves during scroll

            const geom = computeTractorGeometry(item);

            m.anchors = geom.anchors;

            m.hoverPositions = geom.hoverPositions;

            m.crew.forEach((d, idx) => {

                d.targetAnchor = geom.anchors[idx % geom.anchors.length];

                d.hoverPos = geom.hoverPositions[idx % geom.hoverPositions.length];

            });"""

if old_scroll_track in js:
    js = js.replace(old_scroll_track, new_scroll_track)
    print("Updated scroll tracking for hover positions and anchors!")

with open('assets/js/drones.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Saved assets/js/drones.js successfully!")
