with open("assets/js/drones.js", "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update MAX_ACTIVE_CREWS to 2
old_crew = "const MAX_ACTIVE_CREWS = 1;        // Strictly one element rendered at a time in sequence"
new_crew = "const MAX_ACTIVE_CREWS = 2;        // Render two random properties simultaneously in sequence"
assert old_crew in code, "old_crew not found"
code = code.replace(old_crew, new_crew, 1)

# 2. Update chaotic turbulence in stream flight
old_stream = """            if (this.pathPoints.length >= 4) {
                const pos = getSplinePoint(this.pathPoints, easeT);
                // Flocking curl-noise offset for ribbon followers
                const curlFreq = now * 0.014 + this.crewIndex * 2.2;
                const curlAmp = this.isLead ? 0 : (Math.sin(easeT * Math.PI) * (isQualityLow ? 4.0 : 8.0));
                this.x = pos.x + Math.sin(curlFreq) * curlAmp;
                this.y = pos.y + Math.cos(curlFreq) * curlAmp;
            } else {"""

new_stream = """            if (this.pathPoints.length >= 4) {
                const pos = getSplinePoint(this.pathPoints, easeT);
                // Chaotic high-energy turbulence & darting micro-vectors for erratic swarm flight
                const chaoticAngle = (now * 0.026) + (this.crewIndex * 3.4) + (this.id * 1.618);
                const chaoticAmp = Math.sin(easeT * Math.PI) * (isQualityLow ? 7.0 : 16.0) * (0.6 + 0.8 * Math.sin(now * 0.04));
                const flutterX = Math.sin(chaoticAngle * 1.35) * chaoticAmp + (Math.sin(now * 0.05 + this.id) * 3.5);
                const flutterY = Math.cos(chaoticAngle * 0.95) * chaoticAmp + (Math.cos(now * 0.06 + this.id) * 3.5);
                this.x = pos.x + flutterX;
                this.y = pos.y + flutterY;
            } else {"""
assert old_stream in code, "old_stream not found"
code = code.replace(old_stream, new_stream, 1)

# 3. Add chaotic waypoints in generateProceduralPath
old_waypoints = """        waypoints.push({ x: endX, y: endY });

        // Clamp waypoints to viewport boundaries
        waypoints.forEach(wp => {"""

new_waypoints = """        waypoints.push({ x: endX, y: endY });

        // Inject chaotic perturbations into intermediate waypoints for wild flight trajectories
        for (let w = 1; w < waypoints.length - 1; w++) {
            const jitterScale = curvatureScale * (0.35 + Math.random() * 0.30);
            waypoints[w].x += (Math.random() - 0.5) * jitterScale;
            waypoints[w].y += (Math.random() - 0.5) * jitterScale;
        }

        // Clamp waypoints to viewport boundaries
        waypoints.forEach(wp => {"""
assert old_waypoints in code, "old_waypoints not found"
code = code.replace(old_waypoints, new_waypoints, 1)

# 4. Update the dispatch loop for 2 random properties simultaneously
old_dispatch_loop = """        // Strictly one element rendered at a time in sequence
        if (activeMissions.length >= MAX_ACTIVE_CREWS) return;
        if (now - lastMissionFinishTime < 60) return; // Snappy 60ms beat between sequential elements

        // Sequence Order & Band Evaluation: >= 80% inside viewport band [8%, 88%]
        for (let s = 0; s < SECTION_ORDER.length; s++) {
            const secId = SECTION_ORDER[s];
            const sec = sectionMap[secId];
            if (!sec || (!sec.dwellMet && !sec.isHero)) continue;

            const pendingElements = sec.elements.filter(item => item.state === 'pending');
            if (pendingElements.length === 0) continue;

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

                if (!satisfiesBand) continue;

                // Allocate crew from available follow drones + burst pool
                const availableFollowDrones = drones.filter(d => d.state === 'FOLLOW');
                const crewDrones = [];

                for (let k = 0; k < availableFollowDrones.length && crewDrones.length < CREW_SIZE; k++) {
                    crewDrones.push(availableFollowDrones[k]);
                }
                while (crewDrones.length < CREW_SIZE) {
                    const burst = leaseBurstDrone();
                    if (!burst) break;
                    crewDrones.push(burst);
                }

                if (crewDrones.length < CREW_SIZE) return;

                // Gate opens! Dispatch mission
                dispatchMission(item, crewDrones, now);
                return;
            }
        }"""

new_dispatch_loop = """        // Pull out two random properties simultaneously in sequence
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
            }

            if (bandSatisfiedElements.length === 0) continue;

            // Slots available for simultaneous pull (up to 2)
            const availableSlots = MAX_ACTIVE_CREWS - activeMissions.length;
            if (availableSlots <= 0) return;

            // Pick up to availableSlots random properties from the visible pool
            const toDispatch = [];
            const pool = [...bandSatisfiedElements];
            while (toDispatch.length < availableSlots && pool.length > 0) {
                const randIdx = Math.floor(Math.random() * pool.length);
                toDispatch.push(pool.splice(randIdx, 1)[0]);
            }

            for (let d = 0; d < toDispatch.length; d++) {
                const item = toDispatch[d];

                // Allocate crew from available follow drones + burst pool
                const availableFollowDrones = drones.filter(drone => drone.state === 'FOLLOW');
                const crewDrones = [];

                for (let k = 0; k < availableFollowDrones.length && crewDrones.length < CREW_SIZE; k++) {
                    crewDrones.push(availableFollowDrones[k]);
                }
                while (crewDrones.length < CREW_SIZE) {
                    const burst = leaseBurstDrone();
                    if (!burst) break;
                    crewDrones.push(burst);
                }

                if (crewDrones.length >= 2) {
                    dispatchMission(item, crewDrones, now);
                }
            }
            return;
        }"""
assert old_dispatch_loop in code, "old_dispatch_loop not found"
code = code.replace(old_dispatch_loop, new_dispatch_loop, 1)

with open("assets/js/drones.js", "w", encoding="utf-8") as f:
    f.write(code)

print("Successfully updated drones.js with 2 simultaneous random properties and chaotic paths!")
