/* Canvas drone swarm, coordinated with the existing pull-build renderer. */
(function () {
    'use strict';

    const R_MIN = 18;
    const R_MAX = 46;
    const COLORS = ['#F5C542', '#8B3DFF', '#19E3D1'];
    const PATH_TYPES = ['spiral-in', 'loop-the-loop', 'figure-8', 'noisy-arc', 'orbit-dive', 'zig-zag'];
    const REDUCED = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const canvas = document.getElementById('nb-canvas');
    const ctx = canvas && canvas.getContext('2d');
    if (!canvas || !ctx) return;

    window.DroneCanvasEnabled = true;
    let count = 0;
    let drones = [];
    let cursor = {
        x: window.innerWidth * 0.5,
        y: window.matchMedia('(hover: none)').matches ? window.innerHeight * 0.72 : window.innerHeight * 0.5
    };
    let dimTarget = 1;
    let lastHitTest = 0;
    let hitTestTimer = 0;
    let wake = function () {};
    let missions = [];
    let sparks = [];
    let lastFrame = 0;
    let lastPathType = '';
    let pointerInside = true;
    const pathHistory = [];

    function clamp(value, min, max) {
        return Math.max(min, Math.min(max, value));
    }

    function randomPoint(start, target, progress, index, type) {
        const dx = target.x - start.x;
        const dy = target.y - start.y;
        const length = Math.hypot(dx, dy) || 1;
        const px = -dy / length;
        const py = dx / length;
        const side = index % 2 ? -1 : 1;
        const amplitude = Math.min(window.innerWidth, window.innerHeight) * (0.12 + Math.random() * 0.18);
        let offset;

        if (type === 'loop-the-loop') offset = Math.sin(progress * Math.PI * 2) * amplitude;
        else if (type === 'figure-8') offset = Math.sin(progress * Math.PI * 4) * amplitude * 0.7;
        else if (type === 'spiral-in') offset = side * amplitude * (1 - progress);
        else if (type === 'orbit-dive') offset = Math.sin(progress * Math.PI * 2.4 + index) * amplitude;
        else if (type === 'zig-zag') offset = side * amplitude;
        else offset = (Math.random() * 2 - 1) * amplitude;

        const jitter = (Math.random() - 0.5) * 70;
        return {
            x: clamp(start.x + dx * progress + px * (offset + jitter), 3, window.innerWidth - 3),
            y: clamp(start.y + dy * progress + py * (offset + jitter), 3, window.innerHeight - 3)
        };
    }

    function createRoute(start, target) {
        const choices = PATH_TYPES.filter(function (type) { return type !== lastPathType; });
        const type = choices[Math.floor(Math.random() * choices.length)];
        lastPathType = type;
        const count = 3 + Math.floor(Math.random() * 3);
        const points = [start];
        for (let i = 1; i <= count; i++) {
            points.push(randomPoint(start, target, i / (count + 1), i, type));
        }
        points.push(target);
        return { type: type, points: points };
    }

    function routePoint(points, progress) {
        progress = Number.isFinite(progress) ? clamp(progress, 0, 1) : 0;
        const segments = points.length - 1;
        const scaled = clamp(progress, 0, 1) * segments;
        const segment = Math.min(segments - 1, Math.floor(scaled));
        const t = scaled - segment;
        const p0 = points[Math.max(0, segment - 1)];
        const p1 = points[segment];
        const p2 = points[segment + 1];
        const p3 = points[Math.min(points.length - 1, segment + 2)];
        const t2 = t * t;
        const t3 = t2 * t;
        function coordinate(key) {
            return 0.5 * ((2 * p1[key]) + (-p0[key] + p2[key]) * t +
                (2 * p0[key] - 5 * p1[key] + 4 * p2[key] - p3[key]) * t2 +
                (-p0[key] + 3 * p1[key] - 3 * p2[key] + p3[key]) * t3);
        }
        return {
            x: clamp(coordinate('x'), 2, window.innerWidth - 2),
            y: clamp(coordinate('y'), 2, window.innerHeight - 2)
        };
    }

    function resizeSwarm() {
        const nextCount = window.innerWidth <= 600 ? 8 : 14;
        if (nextCount === count || missions.length) return;
        count = nextCount;
        drones = Array.from({ length: count }, function (_, i) {
            const angle = Math.PI * 2 * i / count;
            const radius = R_MIN + (R_MAX - R_MIN) * ((i * 7 % count) / Math.max(1, count - 1));
            const x = cursor.x + Math.cos(angle) * radius;
            const y = cursor.y + Math.sin(angle) * radius;
            return {
                x: x, y: y, vx: 0, vy: 0, angle: angle, radius: radius,
                speed: 0.16 + (i % 4) * 0.018, phase: i * 1.7,
                size: 3 + (i % 3), color: COLORS[i % COLORS.length],
                opacity: 1, currentOpacity: 1, currentX: x, currentY: y,
                trail: [{ x: x, y: y }, { x: x, y: y }, { x: x, y: y }]
            };
        });
    }

    function resizeCanvas() {
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        canvas.width = Math.round(window.innerWidth * dpr);
        canvas.height = Math.round(window.innerHeight * dpr);
        ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    function directText(node) {
        return Array.prototype.some.call(node.childNodes, function (child) {
            return child.nodeType === Node.TEXT_NODE && child.nodeValue.trim().length > 0;
        });
    }

    function checkReading(now) {
        if (!pointerInside) return;
        if (now - lastHitTest < 50) {
            if (!hitTestTimer) {
                hitTestTimer = window.setTimeout(function () {
                    hitTestTimer = 0;
                    checkReading(performance.now());
                }, 50 - (now - lastHitTest));
            }
            return;
        }
        if (hitTestTimer) {
            clearTimeout(hitTestTimer);
            hitTestTimer = 0;
        }
        lastHitTest = now;
        const target = document.elementFromPoint(cursor.x, cursor.y);
        const textSelector = 'p,h1,h2,h3,h4,h5,h6,li,label,a,button';
        const isText = Boolean(target && (
            target.closest(textSelector) ||
            ((target.matches('span,div') || target.closest('span,div')) &&
                directText(target.matches('span,div') ? target : target.closest('span,div')))
        ));
        dimTarget = isText ? 0.3 : 1;
        document.body.classList.toggle('cursor-reading', isText);
    }

    function setPointer(x, y, isTouch) {
        cursor.x = x;
        cursor.y = y;
        pointerInside = true;
        checkReading(performance.now());
        wake();
    }

    window.addEventListener('pointermove', function (event) {
        if (event.pointerType !== 'touch') setPointer(event.clientX, event.clientY, false);
    }, { passive: true });

    document.addEventListener('mouseleave', function () {
        pointerInside = false;
        dimTarget = 0.55;
        document.body.classList.remove('cursor-reading');
        wake();
    }, { passive: true });

    window.addEventListener('blur', function () {
        pointerInside = false;
        dimTarget = 0.55;
        wake();
    }, { passive: true });

    window.addEventListener('touchstart', function (event) {
        if (event.touches[0]) setPointer(event.touches[0].clientX, event.touches[0].clientY, true);
    }, { passive: true });

    window.addEventListener('touchmove', function (event) {
        if (event.touches[0]) setPointer(event.touches[0].clientX, event.touches[0].clientY, true);
    }, { passive: true });

    window.addEventListener('scroll', function () {
        checkReading(performance.now());
        wake();
    }, { passive: true });

    window.addEventListener('resize', function () {
        resizeSwarm();
        resizeCanvas();
    }, { passive: true });

    function clampOrbit(drone) {
        const dx = drone.x - cursor.x;
        const dy = drone.y - cursor.y;
        const distance = Math.hypot(dx, dy) || 1;
        const radius = Math.max(R_MIN, Math.min(R_MAX, distance));
        if (distance !== radius) {
            drone.x = cursor.x + dx / distance * radius;
            drone.y = cursor.y + dy / distance * radius;
        }
        drone.x = clamp(drone.x, 2, window.innerWidth - 2);
        drone.y = clamp(drone.y, 2, window.innerHeight - 2);
        const orbitX = drone.x - cursor.x;
        const orbitY = drone.y - cursor.y;
        if (Math.hypot(orbitX, orbitY) < 14) {
            let inwardX = window.innerWidth * 0.5 - cursor.x;
            let inwardY = window.innerHeight * 0.5 - cursor.y;
            const inwardLength = Math.hypot(inwardX, inwardY) || 1;
            inwardX /= inwardLength;
            inwardY /= inwardLength;
            drone.x = clamp(cursor.x + inwardX * R_MIN, 2, window.innerWidth - 2);
            drone.y = clamp(cursor.y + inwardY * R_MIN, 2, window.innerHeight - 2);
        }
    }

    function drawBeam(context, drone, anchor, now) {
        const flicker = 0.35 + (Math.sin(now * 0.027 + drone.phase) + 1) * 0.18;
        context.beginPath();
        context.moveTo(drone.x, drone.y);
        context.quadraticCurveTo((drone.x + anchor.x) * 0.5 + Math.sin(drone.phase) * 8,
            (drone.y + anchor.y) * 0.5 - 10, anchor.x, anchor.y);
        context.strokeStyle = drone.color;
        context.globalAlpha = flicker;
        context.lineWidth = 0.8;
        context.stroke();
    }

    function draw(context, now) {
        const elapsed = Math.min(2, Math.max(0, (now - (lastFrame || now)) / 16.67));
        lastFrame = now;
        const time = now * 0.001;

        missions = missions.filter(function (job) {
            if (job.stage === 'dispatch' && now - job.started >= job.dispatchTime) {
                job.stage = 'pull';
            }
            return job.stage !== 'return' || now - job.returnStarted < job.returnTime;
        });
        if (!missions.length) resizeSwarm();

        drones.forEach(function (drone, i) {
            const job = missions.find(function (active) { return active.crew.includes(i); });
            const crewIndex = job ? job.crew.indexOf(i) : -1;
            let tx;
            let ty;

            if (job && job.stage === 'dispatch') {
                const route = job.routes[i];
                const p = clamp((now - job.started) / job.dispatchTime, 0, 1);
                const eased = Math.pow(p, route.power);
                const point = routePoint(route.points, eased);
                tx = point.x;
                ty = point.y;
                drone.state = 'DISPATCH';
            } else if (job && job.stage === 'pull') {
                const anchor = job.targets[crewIndex % job.targets.length];
                const orbit = time * 5 + crewIndex * 2.4;
                tx = anchor.x + Math.cos(orbit) * 5;
                ty = anchor.y + Math.sin(orbit) * 5;
                drone.state = 'PULL';
            } else if (job && job.stage === 'return') {
                const route = job.routes[i];
                const p = clamp((now - job.returnStarted) / job.returnTime, 0, 1);
                const point = routePoint(route.points, Math.pow(p, route.power));
                tx = point.x;
                ty = point.y;
                drone.state = 'RETURN';
            } else {
                const angle = drone.angle + time * (REDUCED ? 0 : 0.17) + drone.phase * 0.025;
                const noise = REDUCED ? 0 : Math.sin(time * 1.4 + drone.phase) * 1.2;
                tx = cursor.x + Math.cos(angle) * (drone.radius + noise);
                ty = cursor.y + Math.sin(angle) * (drone.radius + noise);
                drone.state = dimTarget < 1 ? 'DIM' : 'FOLLOW';
            }

            const stiffness = drone.speed * elapsed;
            drone.vx = (drone.vx + (tx - drone.x) * stiffness) * (1 - 0.14 * elapsed);
            drone.vy = (drone.vy + (ty - drone.y) * stiffness) * (1 - 0.14 * elapsed);
            drone.x += drone.vx * elapsed;
            drone.y += drone.vy * elapsed;

            if (!job) clampOrbit(drone);
            drone.currentX = drone.x;
            drone.currentY = drone.y;

            const opacityTarget = pointerInside ? dimTarget : Math.min(dimTarget, 0.55);
            const fadeMs = opacityTarget < drone.opacity ? 150 : 250;
            drone.opacity += (opacityTarget - drone.opacity) * Math.min(1, elapsed * 16.67 / (fadeMs * 0.32));
            drone.currentOpacity = drone.opacity;
            drone.trail.unshift({ x: drone.x, y: drone.y });
            drone.trail.length = 4;
        });

        context.save();
        context.globalCompositeOperation = 'lighter';

        if (!REDUCED) {
            missions.forEach(function (job) {
                if (job.stage !== 'pull') return;
                job.crew.forEach(function (droneIndex, index) {
                    drawBeam(context, drones[droneIndex], job.targets[index % job.targets.length], now);
                });
            });
        }

        drones.forEach(function (drone) {
            for (let i = 1; i < drone.trail.length; i++) {
                const trail = drone.trail[i];
                context.beginPath();
                context.moveTo(drone.trail[i - 1].x, drone.trail[i - 1].y);
                context.lineTo(trail.x, trail.y);
                context.strokeStyle = drone.color;
                context.globalAlpha = drone.opacity * (1 - i / drone.trail.length) * 0.22;
                context.lineWidth = 1;
                context.stroke();
            }

            context.beginPath();
            context.arc(drone.x, drone.y, drone.size * 0.5, 0, Math.PI * 2);
            context.fillStyle = drone.color;
            context.globalAlpha = drone.opacity;
            context.shadowColor = drone.color;
            context.shadowBlur = 3;
            context.fill();
        });

        for (let i = sparks.length - 1; i >= 0; i--) {
            const spark = sparks[i];
            spark.life -= elapsed * 0.055;
            if (spark.life <= 0) {
                sparks.splice(i, 1);
                continue;
            }
            context.beginPath();
            context.arc(spark.x, spark.y, 1.5 * spark.life, 0, Math.PI * 2);
            context.fillStyle = spark.color;
            context.globalAlpha = spark.life;
            context.shadowBlur = 4;
            context.fill();
        }

        context.restore();
        return true;
    }

    function requestReducedFrame() {
        wake();
    }

    function releaseCrew(id) {
        const job = missions.find(function (mission) { return !id || mission.id === id; });
        if (!job) return 0;
        job.stage = 'return';
        job.returnStarted = performance.now();
        job.returnTime = 400 + Math.random() * 500;
        job.crew.forEach(function (droneIndex) {
            const drone = drones[droneIndex];
            const angle = Math.random() * Math.PI * 2;
            const radius = R_MIN + Math.random() * (R_MAX - R_MIN);
            const target = {
                x: clamp(cursor.x + Math.cos(angle) * radius, 2, window.innerWidth - 2),
                y: clamp(cursor.y + Math.sin(angle) * radius, 2, window.innerHeight - 2)
            };
            const route = createRoute({ x: drone.x, y: drone.y }, target);
            job.routes[droneIndex] = {
                points: route.points,
                type: route.type,
                power: 0.75 + Math.random() * 0.7
            };
        });
        job.targets.forEach(function (target) {
            for (let i = 0; i < 5; i++) {
                sparks.push({ x: target.x, y: target.y, color: COLORS[i % COLORS.length], life: 1 });
            }
        });
        wake();
        return job.returnTime;
    }

    window.DroneCanvas = {
        render: draw,
        setWake: function (callback) { wake = callback; },
        getCursor: function () { return { x: cursor.x, y: cursor.y }; },
        getDotsData: function () { return drones; },
        setPhase: function (phase, meta) {
            if (phase === 'idle' || (phase === 'scout' && meta)) releaseCrew();
            requestReducedFrame();
        },
        dispatch: function (targets, id) {
            if (!Array.isArray(targets) || !targets.length || missions.length >= 3) return 0;
            const occupied = new Set();
            missions.forEach(function (job) { job.crew.forEach(function (i) { occupied.add(i); }); });
            const available = drones.map(function (_, i) { return i; }).filter(function (i) { return !occupied.has(i); });
            const crewSize = Math.min(window.innerWidth <= 600 ? 4 : 5, available.length);
            if (crewSize < 3) return 0;
            const crew = available.slice(0, crewSize);
            const started = performance.now();
            const dispatchTime = 600 + Math.random() * 800;
            const job = {
                id: id || 'mission-' + Math.round(started),
                targets: targets,
                crew: crew,
                routes: {},
                stage: 'dispatch',
                started: started,
                dispatchTime: dispatchTime
            };
            crew.forEach(function (droneIndex, index) {
                const drone = drones[droneIndex];
                const target = targets[index % targets.length];
                drone.startX = drone.x;
                drone.startY = drone.y;
                const route = createRoute({ x: drone.x, y: drone.y }, target);
                job.routes[droneIndex] = {
                    points: route.points,
                    type: route.type,
                    power: 0.72 + Math.random() * 0.7
                };
            });
            pathHistory.push({
                id: job.id,
                types: crew.map(function (i) { return job.routes[i].type; }),
                waypoints: crew.map(function (i) { return job.routes[i].points.slice(1, -1); })
            });
            if (pathHistory.length > 20) pathHistory.shift();
            missions.push(job);
            wake();
            return dispatchTime;
        },
        assign: function (targets) { return this.dispatch(targets); },
        release: releaseCrew,
        releaseAll: function () {
            missions.slice().forEach(function (job) { releaseCrew(job.id); });
        },
        retarget: function (id, targets) {
            const job = missions.find(function (mission) { return mission.id === id; });
            if (!job || !Array.isArray(targets) || !targets.length) return;
            job.targets = targets;
            if (job.stage === 'dispatch') {
                job.started = performance.now();
                job.dispatchTime = Math.max(500, job.dispatchTime);
                job.crew.forEach(function (droneIndex, index) {
                    const drone = drones[droneIndex];
                    const route = createRoute({ x: drone.x, y: drone.y }, targets[index % targets.length]);
                    job.routes[droneIndex] = {
                        points: route.points,
                        type: route.type,
                        power: 0.72 + Math.random() * 0.7
                    };
                });
            }
            wake();
        },
        spark: function (x, y) {
            for (let i = 0; i < 3; i++) {
                sparks.push({ x: x, y: y, color: COLORS[i % COLORS.length], life: 1 });
            }
            wake();
        },
        getPathSignatures: function () {
            return pathHistory.slice();
        },
        isAssigned: function () { return missions.length > 0; },
        getPhase: function () {
            return missions.length ? missions[0].stage : 'follow';
        }
    };
    window.swarm = window.DroneCanvas;
    if (window.__pullBuildWake) window.DroneCanvas.setWake(window.__pullBuildWake);
    resizeCanvas();
    resizeSwarm();
    wake();

    document.addEventListener('visibilitychange', function () {
        if (!document.hidden) wake();
    });
})();
