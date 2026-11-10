with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update ease helpers and sparks section
old_sparks_section = """    function easeInOutCubic(x) {

        return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;

    }



    // ─── 6. SPARK PARTICLES & TRACTOR BEAMS ────────────────────────────────

    const sparks = [];

    function emitSparks(x, y, count = 12) {

        for (let i = 0; i < count; i++) {

            const angle = Math.random() * Math.PI * 2;

            const speed = 1.8 + Math.random() * 4.2;

            sparks.push({

                x,

                y,

                vx: Math.cos(angle) * speed,

                vy: Math.sin(angle) * speed - 1.2,

                life: 1.0,

                decay: 0.035 + Math.random() * 0.045,

                color: PALETTE[Math.floor(Math.random() * PALETTE.length)]

            });

        }

    }



    function updateAndDrawSparks(ctx) {

        for (let i = sparks.length - 1; i >= 0; i--) {

            const s = sparks[i];

            s.x += s.vx;

            s.y += s.vy;

            s.vy += 0.08; // gravity

            s.life -= s.decay;



            if (s.life <= 0) {

                sparks.splice(i, 1);

                continue;

            }



            ctx.beginPath();

            ctx.arc(s.x, s.y, 1.0 * s.life, 0, Math.PI * 2);

            ctx.fillStyle = s.color;

            ctx.globalAlpha = s.life;

            ctx.fill();

        }

        ctx.globalAlpha = 1.0;

    }"""

new_sparks_section = """    function easeInOutCubic(x) {

        return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;

    }



    function easeOutCubic(x) {

        return 1 - Math.pow(1 - x, 3);

    }



    // ─── 6. SPARK PARTICLES, PULSE RINGS & QUANTUM WELDING ──────────────────

    const sparks = [];

    function emitSparks(x, y, count = 12) {

        if (sparks.length >= 100) sparks.splice(0, count);

        for (let i = 0; i < count; i++) {

            const angle = Math.random() * Math.PI * 2;

            const speed = 1.8 + Math.random() * 4.2;

            sparks.push({

                x,

                y,

                vx: Math.cos(angle) * speed,

                vy: Math.sin(angle) * speed - 1.2,

                isPlasma: false,

                life: 1.0,

                decay: 0.035 + Math.random() * 0.045,

                color: PALETTE[Math.floor(Math.random() * PALETTE.length)]

            });

        }

    }



    // Quantum Welding Plasma Sparks: Directional molten plasma streaks spraying off tractor contact points

    function emitPlasmaSparks(x, y, count = 3) {

        if (sparks.length >= 100) sparks.splice(0, count);

        const plasmaPalette = [THEME.cyan, THEME.gold, THEME.white];

        for (let i = 0; i < count; i++) {

            const angle = -Math.PI * 0.5 + (Math.random() - 0.5) * Math.PI * 1.35;

            const speed = 2.5 + Math.random() * 4.8;

            sparks.push({

                x,

                y,

                vx: Math.cos(angle) * speed,

                vy: Math.sin(angle) * speed,

                isPlasma: true,

                life: 1.0,

                decay: 0.055 + Math.random() * 0.045, // fast 160-220ms life

                color: plasmaPalette[Math.floor(Math.random() * plasmaPalette.length)]

            });

        }

    }



    function updateAndDrawSparks(ctx) {

        for (let i = sparks.length - 1; i >= 0; i--) {

            const s = sparks[i];

            s.x += s.vx;

            s.y += s.vy;

            s.vy += s.isPlasma ? 0.04 : 0.08; // subtle gravity

            s.vx *= 0.94; // aerodynamic drag

            s.life -= s.decay;



            if (s.life <= 0) {

                sparks.splice(i, 1);

                continue;

            }



            ctx.save();

            if (s.isPlasma) {

                // Directional molten plasma streak

                ctx.beginPath();

                ctx.moveTo(s.x, s.y);

                ctx.lineTo(s.x - s.vx * 1.5, s.y - s.vy * 1.5);

                ctx.strokeStyle = s.color;

                ctx.lineWidth = Math.max(0.6, 1.3 * s.life);

                ctx.globalAlpha = s.life * 0.95;

                ctx.shadowColor = s.color;

                ctx.shadowBlur = 4;

                ctx.stroke();

            } else {

                ctx.beginPath();

                ctx.arc(s.x, s.y, 1.0 * s.life, 0, Math.PI * 2);

                ctx.fillStyle = s.color;

                ctx.globalAlpha = s.life;

                ctx.fill();

            }

            ctx.restore();

        }

        ctx.globalAlpha = 1.0;

    }



    // Gravitational Pulse Rings (Micro-Sonar Radar Pings)

    // Single ultra-fine concentric rings that rapidly expand & fade over ~250ms

    const pulseRings = [];

    function emitPulseRing(x, y, color = THEME.cyan, maxRadius = 26, duration = 260) {

        if (pulseRings.length >= 14) pulseRings.shift();

        pulseRings.push({

            x,

            y,

            color,

            maxRadius,

            duration,

            startTime: performance.now()

        });

    }



    function updateAndDrawPulseRings(ctx, now) {

        for (let i = pulseRings.length - 1; i >= 0; i--) {

            const ring = pulseRings[i];

            const elapsed = now - ring.startTime;

            const progress = elapsed / ring.duration;



            if (progress >= 1.0) {

                pulseRings.splice(i, 1);

                continue;

            }



            const easeP = easeOutCubic(progress);

            const r = easeP * ring.maxRadius;

            const fade = (1.0 - progress);

            const alpha = fade * fade * 0.85;



            ctx.save();

            // Outer ultra-fine expanding gravitational wave ring

            ctx.beginPath();

            ctx.arc(ring.x, ring.y, r, 0, Math.PI * 2);

            ctx.strokeStyle = ring.color;

            ctx.lineWidth = Math.max(0.4, 1.1 * fade);

            ctx.globalAlpha = alpha;

            ctx.shadowColor = ring.color;

            ctx.shadowBlur = 4 * fade;

            ctx.stroke();



            // Inner faint echo ping

            if (progress < 0.65) {

                ctx.beginPath();

                ctx.arc(ring.x, ring.y, r * 0.45, 0, Math.PI * 2);

                ctx.strokeStyle = THEME.white;

                ctx.lineWidth = 0.5 * fade;

                ctx.globalAlpha = alpha * 0.45;

                ctx.stroke();

            }

            ctx.restore();

        }

    }"""

assert old_sparks_section in c, "old_sparks_section not found"
c = c.replace(old_sparks_section, new_sparks_section, 1)

# 2. Update Drone updateFollow spontaneous micro-dart to emit micro-pulse ring
old_dart = """            if (now - this.lastDartTime > this.nextDartInterval) {

                this.lastDartTime = now;

                this.nextDartInterval = 800 + Math.random() * 2400;

                const dartAngle = Math.random() * Math.PI * 2;

                const dartForce = 0.9 + Math.random() * 1.6;

                this.vx += Math.cos(dartAngle) * dartForce;

                this.vy += Math.sin(dartAngle) * dartForce;

            }"""

new_dart = """            if (now - this.lastDartTime > this.nextDartInterval) {

                this.lastDartTime = now;

                this.nextDartInterval = 800 + Math.random() * 2400;

                const dartAngle = Math.random() * Math.PI * 2;

                const dartForce = 0.9 + Math.random() * 1.6;

                this.vx += Math.cos(dartAngle) * dartForce;

                this.vy += Math.sin(dartAngle) * dartForce;



                // Micro-sonar radar ping on energetic dart

                if (Math.random() < 0.40 && pulseRings.length < 8) {

                    emitPulseRing(this.x, this.y, this.color, 18, 220);

                }

            }"""

assert old_dart in c, "old_dart not found"
c = c.replace(old_dart, new_dart, 1)

# 3. Update dispatchMission & mission lifecycle with pulse rings & plasma sparks
old_dispatch = """        // Assign procedural path to each crew drone

        crewDrones.forEach((drone, idx) => {

            drone.state = 'DISPATCH';

            drone.activeMission = mission;

            drone.crewIndex = idx;

            drone.flightStart = now;

            drone.flightDuration = flightDuration + idx * 20; // tighter stagger



            const anchor = anchors[idx % anchors.length];

            drone.targetAnchor = anchor;

            drone.pathPoints = generateProceduralPath(drone.x, drone.y, anchor.x, anchor.y, drone.flightDuration);

        });"""

new_dispatch = """        // Assign procedural path to each crew drone & emit launch gravitational pulse ring

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

assert old_dispatch in c, "old_dispatch not found"
c = c.replace(old_dispatch, new_dispatch, 1)

# 4. Update onDroneArrived & startPull
old_arrive = """            onDroneArrived(drone) {

                this.arrivedCount++;

                if (this.arrivedCount >= this.crew.length) {

                    this.startPull(performance.now());

                }

            },"""

new_arrive = """            onDroneArrived(drone) {

                this.arrivedCount++;

                if (drone.targetAnchor) {

                    emitPulseRing(drone.targetAnchor.x, drone.targetAnchor.y, THEME.cyan, 22, 220);

                    emitPlasmaSparks(drone.targetAnchor.x, drone.targetAnchor.y, 4);

                }

                if (this.arrivedCount >= this.crew.length) {

                    this.startPull(performance.now());

                }

            },"""

assert old_arrive in c, "old_arrive not found"
c = c.replace(old_arrive, new_arrive, 1)

# 5. Update startPull to emit welding plasma bursts
old_startpull = """                this.anchors.forEach(a => emitSparks(a.x, a.y, 8));"""

new_startpull = """                this.anchors.forEach(a => {

                    emitPulseRing(a.x, a.y, THEME.gold, 26, 260);

                    emitPlasmaSparks(a.x, a.y, 8);

                });"""

assert old_startpull in c, "old_startpull not found"
c = c.replace(old_startpull, new_startpull, 1)

# 6. Update returnCrew to emit release pulse ring
old_return = """    function returnCrew(crewDrones, now) {

        crewDrones.forEach((drone, idx) => {

            drone.state = 'RETURN';"""

new_return = """    function returnCrew(crewDrones, now) {

        crewDrones.forEach((drone, idx) => {

            if (drone.targetAnchor) {

                emitPulseRing(drone.targetAnchor.x, drone.targetAnchor.y, THEME.cyan, 24, 240);

            }

            drone.state = 'RETURN';"""

assert old_return in c, "old_return not found"
c = c.replace(old_return, new_return, 1)

# 7. Update drawTractorBeams with Contact-Point Lens Bloom, Cross-Flares & Plasma Welding Arc Sputter
old_tb = """                // Inner diamond white core

                ctx.beginPath();

                ctx.moveTo(drone.x, drone.y);

                ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);

                ctx.strokeStyle = 'rgba(255, 255, 255, 0.98)';

                ctx.lineWidth = 0.8;

                ctx.shadowColor = THEME.gold;

                ctx.shadowBlur = 8;

                ctx.stroke();

                ctx.restore();

            });

        });

    }"""

new_tb = """                // Inner diamond white core

                ctx.beginPath();

                ctx.moveTo(drone.x, drone.y);

                ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);

                ctx.strokeStyle = 'rgba(255, 255, 255, 0.98)';

                ctx.lineWidth = 0.8;

                ctx.shadowColor = THEME.gold;

                ctx.shadowBlur = 8;

                ctx.stroke();

                ctx.restore();



                // ─── QUANTUM WELDING CONTACT-POINT LENS BLOOM & CROSS-FLARE ─

                ctx.save();

                // 1. Diffuse glowing plasma halo at weld anchor

                const haloRadius = 7.0 + 2.0 * Math.sin(now * 0.025 + idx * 1.5);

                ctx.beginPath();

                ctx.arc(anchor.x, anchor.y, haloRadius, 0, Math.PI * 2);

                ctx.fillStyle = (idx % 2 === 0) ? 'rgba(25, 227, 209, 0.40)' : 'rgba(245, 197, 66, 0.40)';

                ctx.shadowColor = THEME.cyan;

                ctx.shadowBlur = 10;

                ctx.fill();



                // 2. High-energy diamond white welding core

                ctx.beginPath();

                ctx.arc(anchor.x, anchor.y, 2.4 + 0.6 * Math.cos(now * 0.035 + idx), 0, Math.PI * 2);

                ctx.fillStyle = '#FFFFFF';

                ctx.shadowColor = THEME.white;

                ctx.shadowBlur = 6;

                ctx.fill();



                // 3. Rotating 4-ray diffraction cross-flare lens spikes

                const flareAngle = now * 0.003 + idx * 0.78;

                const flareLen = 7.0 + 3.0 * Math.sin(now * 0.04 + idx);

                ctx.beginPath();

                for (let k = 0; k < 4; k++) {

                    const a = flareAngle + (k * Math.PI / 2);

                    ctx.moveTo(anchor.x, anchor.y);

                    ctx.lineTo(anchor.x + Math.cos(a) * flareLen, anchor.y + Math.sin(a) * flareLen);

                }

                ctx.strokeStyle = 'rgba(255, 255, 255, 0.85)';

                ctx.lineWidth = 0.8;

                ctx.shadowColor = THEME.gold;

                ctx.shadowBlur = 5;

                ctx.stroke();

                ctx.restore();



                // 4. Directional quantum welding plasma sparks

                if (Math.random() < 0.45) {

                    emitPlasmaSparks(anchor.x, anchor.y, 2);

                }

            });

        });

    }"""

assert old_tb in c, "old_tb not found"
c = c.replace(old_tb, new_tb, 1)

# 8. Update mainLoop to draw pulse rings
old_mainloop_draw = """        // 4. Draw tractor beams & sparks

        drawTractorBeams(ctx);

        updateAndDrawSparks(ctx);"""

new_mainloop_draw = """        // 4. Draw tractor beams, welding sparks & pulse rings

        drawTractorBeams(ctx);

        updateAndDrawSparks(ctx);

        updateAndDrawPulseRings(ctx, now);"""

assert old_mainloop_draw in c, "old_mainloop_draw not found"
c = c.replace(old_mainloop_draw, new_mainloop_draw, 1)

# 9. Update window.drones API
old_api = """    window.drones = {

        getDrones: () => drones,

        getElements: () => elementList,

        getMissions: () => activeMissions,

        revealAll: revealAllInstantly,

        R_MIN,

        R_MAX

    };"""

new_api = """    window.drones = {

        getDrones: () => drones,

        getElements: () => elementList,

        getMissions: () => activeMissions,

        getPulseRings: () => pulseRings,

        getSparks: () => sparks,

        emitPulseRing,

        emitPlasmaSparks,

        revealAll: revealAllInstantly,

        R_MIN,

        R_MAX

    };"""

assert old_api in c, "old_api not found"
c = c.replace(old_api, new_api, 1)

with open('assets/js/drones.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Successfully applied Gravitational Pulse Rings & Quantum Welding to drones.js!")
