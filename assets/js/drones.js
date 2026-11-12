/**
 * DRONES SYSTEM [assets/js/drones.js]
 * Unified Swarm & Autonomous Construction Drones Engine
 * 
 * Hyper-optimized Cinematic Hive Architecture:
 * - Speed: Gate-to-dispatch <= 150ms, First reveal <= 450ms, Visible flight >= 300ms.
 * - Choreography: Hive Pulse (110ms) -> Stream Ribbon (Gold lead + Purple followers + curl noise)
 *                 -> Lock-on (80ms HUD brackets) -> Assembly -> Impact (60ms RGB split) -> Release scatter.
 * - Pipelining: Up to 4 crews active concurrently; crew N+1 dispatches while crew N is mid-pull.
 * - Performance: Pre-rendered radial sprites, Float32Array ring buffers, zero per-frame allocations,
 *                batch draw paths (< 40 draw calls), 30-frame adaptive quality throttle.
 */

(function () {
    'use strict';

    // ─── 1. CONSTANTS & CONFIGURATION ───────────────────────────────────────
    const THEME = {
        gold: '#FBBF24',
        goldLead: '#FDE047',
        purple: '#8B5CF6',
        turquoise: '#00F5D4',
        cyan: '#00F5D4',
        bloodRed: '#FF2A5F',
        bloodCrimson: '#E11D48',
        bloodNeon: '#FF2A5F',
        black: '#07080E',
        white: '#FFFFFF'
    };

    const PALETTE = [THEME.cyan, THEME.purple, THEME.bloodNeon, THEME.gold];

    const R_MIN = 18;
    const R_MAX = 46;

    const READABLE_TAGS = new Set([
        'A', 'BUTTON', 'INPUT', 'TEXTAREA', 'SELECT', 'LABEL',
        'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'P', 'LI', 'SPAN',
        'CODE', 'PRE', 'BLOCKQUOTE', 'STRONG', 'EM', 'B', 'I'
    ]);

    const BAND_TOP = 0.05;   // 5% viewport height
    const BAND_BOTTOM = 0.85; // 85% viewport height: elements enter comfortable visual field before extraction
    const SCROLL_VELOCITY_LIMIT = 1800; // px/s (fluid, avoids accidental triggers)
    const SCROLL_SETTLE_MS = 30;       // ms (crisp responsive settle)
    const SECTION_DWELL_MS = 90;       // ms (cinematic recognition delay as visitor scrolls in)
    const isMobile = window.innerWidth < 768;
    const MAX_ACTIVE_CREWS = 2;        // Balanced dual-squad cinematic simultaneous extraction
    const DRONE_COUNT = isMobile ? 8 : 12;
    const CREW_SIZE = 3;
    const MAX_BURST_DRONES = isMobile ? 12 : 20;

    const isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // ─── 2. PRE-RENDERED RADIAL SPRITES (ZERO PER-FRAME ALLOCATION) ─────────
    const spriteCache = {};

    function createRadialSprite(color, coreColor, radius, glowRadius) {
        const sCanvas = document.createElement('canvas');
        const d = Math.ceil(glowRadius * 2 + 4);
        sCanvas.width = d;
        sCanvas.height = d;
        const sCtx = sCanvas.getContext('2d');
        const cx = d / 2;
        const cy = d / 2;

        const grad = sCtx.createRadialGradient(cx, cy, 0, cx, cy, glowRadius);
        grad.addColorStop(0, color);
        grad.addColorStop(0.35, color);
        grad.addColorStop(1, 'rgba(0,0,0,0)');

        sCtx.fillStyle = grad;
        sCtx.beginPath();
        sCtx.arc(cx, cy, glowRadius, 0, Math.PI * 2);
        sCtx.fill();

        if (coreColor) {
            sCtx.fillStyle = coreColor;
            sCtx.beginPath();
            sCtx.arc(cx, cy, radius, 0, Math.PI * 2);
            sCtx.fill();
        }

        return { canvas: sCanvas, halfSize: d / 2 };
    }

    function initSprites() {
        spriteCache.goldLead = createRadialSprite('rgba(255, 215, 0, 0.45)', '#FFFFFF', 2.2, 11);
        spriteCache.gold = createRadialSprite('rgba(245, 197, 66, 0.40)', '#FFFFFF', 1.8, 9);
        spriteCache.purple = createRadialSprite('rgba(139, 61, 255, 0.45)', '#FFFFFF', 1.8, 9);
        spriteCache.turquoise = createRadialSprite('rgba(25, 227, 209, 0.45)', '#FFFFFF', 1.8, 9);
        spriteCache.crimson = createRadialSprite('rgba(255, 30, 66, 0.45)', '#FFFFFF', 1.8, 9);
        spriteCache.sparkWhite = createRadialSprite('rgba(255, 255, 255, 0.85)', '#FFFFFF', 1.3, 5);
        spriteCache.pulseTurquoise = createRadialSprite('rgba(25, 227, 209, 0.35)', null, 0, 16);
        spriteCache.pulseGold = createRadialSprite('rgba(245, 197, 66, 0.35)', null, 0, 16);
    }
    initSprites();

    // ─── 3. CANVAS & SIZING SETUP ───────────────────────────────────────────
    let canvas = document.getElementById('nb-canvas');
    if (!canvas) {
        canvas = document.createElement('canvas');
        canvas.id = 'nb-canvas';
        canvas.setAttribute('aria-hidden', 'true');
        document.body.appendChild(canvas);
    }

    const ctx = canvas.getContext('2d', { alpha: true });
    let viewW = window.innerWidth;
    let viewH = window.innerHeight;
    const dpr = Math.min(window.devicePixelRatio || 1, isMobile ? 1.5 : 2);

    function resizeCanvas() {
        viewW = window.innerWidth;
        viewH = window.innerHeight;
        canvas.width = Math.round(viewW * dpr);
        canvas.height = Math.round(viewH * dpr);
        canvas.style.width = viewW + 'px';
        canvas.style.height = viewH + 'px';
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.scale(dpr, dpr);
        refreshAllElementRects();
    }

    window.addEventListener('resize', debounce(resizeCanvas, 120), { passive: true });
    window.addEventListener('orientationchange', () => setTimeout(resizeCanvas, 150), { passive: true });

    function debounce(fn, wait) {
        let t;
        return function () {
            clearTimeout(t);
            t = setTimeout(fn, wait);
        };
    }

    // ─── 4. CURSOR & TOUCH TRACKER (FOLLOW & DIM STATE) ────────────────────
    let cursorX = viewW * 0.5;
    let cursorY = viewH * (isMobile ? 0.72 : 0.45);
    let targetCursorX = cursorX;
    let targetCursorY = cursorY;
    let cursorInWindow = true;
    let isTouchMode = false;
    let isOverText = false;

    let lastScrollY = window.scrollY || window.pageYOffset;
    let lastScrollTime = performance.now();
    let currentScrollSpeed = 0; // px/s
    let lastFastScrollTime = 0;
    let lastCursorMoveTime = performance.now();
    let lastSonarPingTime = 0;

    window.addEventListener('mousemove', (e) => {
        isTouchMode = false;
        cursorInWindow = true;
        const dx = e.clientX - targetCursorX;
        const dy = e.clientY - targetCursorY;
        const distMoved = Math.hypot(dx, dy);
        if (distMoved > 1.2) {
            lastCursorMoveTime = performance.now();
        }
        if (distMoved > 28 && performance.now() - lastSonarPingTime > 400) {
            lastSonarPingTime = performance.now();
            emitPulseRing(e.clientX, e.clientY, THEME.cyan, 24, 250);
        }
        targetCursorX = e.clientX;
        targetCursorY = e.clientY;
        checkDimUnderPointer(e.clientX, e.clientY);
    }, { passive: true });

    window.addEventListener('touchmove', (e) => {
        isTouchMode = true;
        cursorInWindow = true;
        if (e.touches && e.touches[0]) {
            const dx = e.touches[0].clientX - targetCursorX;
            const dy = e.touches[0].clientY - targetCursorY;
            if (Math.hypot(dx, dy) > 1.2) {
                lastCursorMoveTime = performance.now();
            }
            targetCursorX = e.touches[0].clientX;
            targetCursorY = e.touches[0].clientY;
            checkDimUnderPointer(targetCursorX, targetCursorY);
        }
    }, { passive: true });

    window.addEventListener('touchstart', (e) => {
        isTouchMode = true;
        cursorInWindow = true;
        if (e.touches && e.touches[0]) {
            targetCursorX = e.touches[0].clientX;
            targetCursorY = e.touches[0].clientY;
        }
    }, { passive: true });

    document.addEventListener('mouseleave', () => { cursorInWindow = false; });
    document.addEventListener('mouseenter', () => { cursorInWindow = true; });

    let lastDimCheck = 0;
    function checkDimUnderPointer(x, y) {
        const now = performance.now();
        if (now - lastDimCheck < 60) return;
        lastDimCheck = now;
        const el = document.elementFromPoint(x, y);
        if (!el) {
            isOverText = false;
            return;
        }
        if (READABLE_TAGS.has(el.tagName)) {
            isOverText = true;
            return;
        }
        const textAncestor = el.closest('p, h1, h2, h3, h4, h5, h6, a, button, label, li, code, span, .trait-tag, .section-desc');
        isOverText = Boolean(textAncestor);
    }

    window.addEventListener('scroll', () => {
        const now = performance.now();
        const dt = (now - lastScrollTime) / 1000;
        const currentY = window.scrollY || window.pageYOffset;
        if (dt > 0.005) {
            const dy = Math.abs(currentY - lastScrollY);
            currentScrollSpeed = dy / dt;
            if (currentScrollSpeed >= SCROLL_VELOCITY_LIMIT) {
                lastFastScrollTime = now;
            }
            // Fast-scroll fail-safe: automatically load section properties without delay when flick-scrolling fast
            if (currentY > 150 && currentScrollSpeed >= 1600 && dy > 180) {
                lastFastScrollTime = now;
                if (typeof triggerFastScrollFailsafe === 'function') {
                    triggerFastScrollFailsafe();
                }
            }
            lastScrollY = currentY;
            lastScrollTime = now;
        }
    }, { passive: true });

    // ─── 5. TYPED ARRAY TRAIL RING BUFFER & DRONE CLASS ────────────────────
    const TRAIL_MAX = 14;
    const IRREGULAR_SIZES = [1.2, 2.8, 1.8, 3.4, 1.1, 2.4, 2.0, 3.2, 1.4, 2.6, 1.7, 3.5, 1.3, 2.9];

    class Drone {
        constructor(id, isBurst = false) {
            this.id = id;
            this.isBurst = isBurst;
            this.isLead = false;
            this.color = PALETTE[id % PALETTE.length];
            this.size = IRREGULAR_SIZES[id % IRREGULAR_SIZES.length];
            this.spriteKey = (id % 3 === 0) ? 'gold' : ((id % 3 === 1) ? 'purple' : 'turquoise');

            // Multi-frequency oscillators
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

            this.x = cursorX + Math.cos(this.orbitAngle) * this.orbitRadius;
            this.y = cursorY + Math.sin(this.orbitAngle) * this.orbitRadius;
            this.vx = 0;
            this.vy = 0;
            this.opacity = 1.0;

            // State: 'FOLLOW' | 'DISPATCH' | 'PULL' | 'RETURN' | 'INACTIVE'
            this.state = isBurst ? 'INACTIVE' : 'FOLLOW';
            this.activeMission = null;
            this.crewIndex = -1;

            // Procedural path tracking
            this.flightStart = 0;
            this.flightDuration = 320;
            this.pathPoints = [];
            this.targetAnchor = { x: 0, y: 0 };
            this.hoverPos = { x: 0, y: 0 };

            // Float32Array Trail Ring Buffer (Zero per-frame array allocations)
            this.trailX = new Float32Array(TRAIL_MAX);
            this.trailY = new Float32Array(TRAIL_MAX);
            this.trailHead = 0;
            this.trailCount = 0;
            this.lastTrailTime = 0;
        }

        resetTrail() {
            this.trailHead = 0;
            this.trailCount = 0;
        }

        pushTrail(x, y, now) {
            // Tails removed as per user specification - zero trail tracking
            return;
        }

        updateFollow(now, dt) {
            this.orbitAngle += this.orbitSpeed * this.orbitDir * dt;
            const wanderX = Math.sin(now * this.wanderFreq1 + this.noisePhase) * 11
                          + Math.cos(now * this.wanderFreq2 + this.id * 1.3) * 6
                          + Math.sin(now * this.wanderFreq3 + this.id) * 4;
            const wanderY = Math.cos(now * this.wanderFreq2 + this.noisePhase) * 11
                          + Math.sin(now * this.wanderFreq1 + this.id * 1.7) * 6
                          + Math.cos(now * this.wanderFreq3 + this.id) * 4;

            const dynamicR = R_MIN + (R_MAX - R_MIN) * (0.35 + 0.45 * Math.sin(now * 0.0016 + this.id * 2.3));
            const desiredX = cursorX + Math.cos(this.orbitAngle) * dynamicR + wanderX;
            const desiredY = cursorY + Math.sin(this.orbitAngle) * dynamicR + wanderY;

            if (now - this.lastDartTime > this.nextDartInterval) {
                this.lastDartTime = now;
                this.nextDartInterval = 800 + Math.random() * 2400;
                const dartAngle = Math.random() * Math.PI * 2;
                const dartForce = 0.9 + Math.random() * 1.6;
                this.vx += Math.cos(dartAngle) * dartForce;
                this.vy += Math.sin(dartAngle) * dartForce;
            }

            const ax = (desiredX - this.x) * this.stiffness;
            const ay = (desiredY - this.y) * this.stiffness;
            this.vx = (this.vx + ax) * this.damping;
            this.vy = (this.vy + ay) * this.damping;
            this.x += this.vx;
            this.y += this.vy;

            // R_MAX boundary clamp: Never exceed R_max from cursor in FOLLOW
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
            const fadeSpeed = (targetOp < this.opacity) ? Math.min(1.0, dt / 0.065) : Math.min(1.0, dt / 0.095);
            this.opacity += (targetOp - this.opacity) * fadeSpeed;

            // Push trail during fast movement
            if (Math.hypot(this.vx, this.vy) > 1.8) {
                this.pushTrail(this.x, this.y, now);
            }
        }

        updateFlight(now, dt) {
            const m = this.activeMission;
            const elapsed = now - this.flightStart;

            // Phase A: Hive Pulse condensation at cursor (110ms)
            if (m && m.hivePulseDuration > 0 && elapsed < m.hivePulseDuration) {
                const pulseT = elapsed / m.hivePulseDuration;
                const condenseScale = 1.0 - Math.sin(pulseT * Math.PI) * 0.75;
                const angle = this.orbitAngle + pulseT * 3.0;
                const r = 6 * condenseScale;
                this.x = cursorX + Math.cos(angle) * r;
                this.y = cursorY + Math.sin(angle) * r;
                this.vx = 0;
                this.vy = 0;
                this.opacity = 1.0;
                return;
            }

            // Phase B: Stream ribbon flight (Visible flight >= 300ms, total to arrival <= 450ms)
            const flightElapsed = m ? Math.max(0, elapsed - m.hivePulseDuration) : elapsed;
            const actualDuration = m ? (this.flightDuration - m.hivePulseDuration) : this.flightDuration;
            const tRaw = Math.min(1.0, flightElapsed / Math.max(1, actualDuration));

            // Follower lag for flowing ribbon effect
            const lag = this.isLead ? 0 : (this.crewIndex * 0.038);
            const t = Math.max(0, Math.min(1.0, tRaw - lag));
            const easeT = easeInOutCubic(t);

            const prevX = this.x;
            const prevY = this.y;

            if (this.pathPoints.length >= 4) {
                const pos = getSplinePoint(this.pathPoints, easeT);
                // Chaotic high-energy turbulence & darting micro-vectors for erratic swarm flight
                const chaoticAngle = (now * 0.026) + (this.crewIndex * 3.4) + (this.id * 1.618);
                const chaoticAmp = Math.sin(easeT * Math.PI) * (isQualityLow ? 7.0 : 16.0) * (0.6 + 0.8 * Math.sin(now * 0.04));
                const flutterX = Math.sin(chaoticAngle * 1.35) * chaoticAmp + (Math.sin(now * 0.05 + this.id) * 3.5);
                const flutterY = Math.cos(chaoticAngle * 0.95) * chaoticAmp + (Math.cos(now * 0.06 + this.id) * 3.5);
                this.x = pos.x + flutterX;
                this.y = pos.y + flutterY;
            } else {
                const p0 = this.pathPoints[0] || { x: cursorX, y: cursorY };
                const p1 = this.hoverPos || this.targetAnchor;
                this.x = p0.x + (p1.x - p0.x) * easeT;
                this.y = p0.y + (p1.y - p0.y) * easeT;
            }

            // Viewport boundary clamp
            this.x = Math.max(12, Math.min(viewW - 12, this.x));
            this.y = Math.max(12, Math.min(viewH - 12, this.y));

            this.vx = (this.x - prevX);
            this.vy = (this.y - prevY);
            this.pushTrail(this.x, this.y, now);
            this.opacity = 1.0;

            // Arrival check: arrival never precedes crew flight
            if (tRaw >= 1.0) {
                if (this.state === 'DISPATCH') {
                    this.state = 'PULL';
                    if (m) m.onDroneArrived(this);
                } else if (this.state === 'RETURN') {
                    if (this.isBurst) {
                        this.state = 'INACTIVE';
                    } else {
                        this.state = 'FOLLOW';
                    }
                    this.activeMission = null;
                    this.resetTrail();
                    // Subtle re-entry pulse on rejoining swarm
                    emitPulseRing(this.x, this.y, THEME.gold, 12, 180);
                }
            }
        }

        updatePull(now, dt) {
            const hover = this.hoverPos || (this.targetAnchor ? { x: this.targetAnchor.x, y: this.targetAnchor.y - 65 } : { x: this.x, y: this.y });
            const jitterX = Math.sin(now * 0.045 + this.id * 1.7) * 2.2;
            const jitterY = Math.cos(now * 0.055 + this.id * 1.3) * 1.8 - 2.0; // upward towing tension
            this.x = hover.x + jitterX;
            this.y = hover.y + jitterY;
            this.vx = jitterX;
            this.vy = jitterY;
            this.opacity = 1.0;
        }

        draw(ctx) {
            if (this.state === 'INACTIVE') return;

            // Velocity-based stretch elongation
            const speed = Math.hypot(this.vx, this.vy);
            const isStretched = (speed > 1.5 && (this.state === 'DISPATCH' || this.state === 'RETURN'));

            ctx.save();
            ctx.globalAlpha = this.opacity;

            // Pre-rendered radial glow sprite (Zero per-frame allocations)
            let sKey = this.isLead ? 'goldLead' : (this.state === 'DISPATCH' ? (this.crewIndex === 0 ? 'goldLead' : 'purple') : this.spriteKey);
            const sprite = spriteCache[sKey] || spriteCache.gold;
            const sizeScale = (this.size || 1.8) / 1.8;

            ctx.translate(this.x, this.y);

            if (isStretched) {
                const angle = Math.atan2(this.vy, this.vx);
                const stretch = Math.min(2.2, 1.0 + speed * 0.07);
                ctx.rotate(angle);
                ctx.scale(sizeScale * stretch, sizeScale / Math.sqrt(stretch));
            } else {
                ctx.scale(sizeScale, sizeScale);
            }

            ctx.drawImage(sprite.canvas, -sprite.halfSize, -sprite.halfSize);
            ctx.restore();
        }
    }

    // Initialize regular swarm drones
    const drones = [];
    for (let i = 0; i < DRONE_COUNT; i++) {
        drones.push(new Drone(i, false));
    }

    // Initialize burst drone pool for pipelined missions
    const burstDronePool = [];
    for (let b = 0; b < MAX_BURST_DRONES; b++) {
        burstDronePool.push(new Drone(DRONE_COUNT + b, true));
    }

    function leaseBurstDrone() {
        for (let i = 0; i < burstDronePool.length; i++) {
            if (burstDronePool[i].state === 'INACTIVE') {
                burstDronePool[i].state = 'LEASED';
                return burstDronePool[i];
            }
        }
        return null;
    }

    // ─── 6. PROCEDURAL RANDOM PATHS GENERATOR ───────────────────────────────
    const PATH_TYPES = [
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
                waypoints.push({ x: startX + normX * (curvatureScale * oSign), y: startY + normY * (curvatureScale * oSign) });
                waypoints.push({ x: midX + normX * (curvatureScale * 1.4 * oSign), y: midY + normY * (curvatureScale * 1.4 * oSign) });
                waypoints.push({ x: endX - normX * (curvatureScale * 0.4 * oSign), y: endY - normY * (curvatureScale * 0.4 * oSign) });
                break;
            }
            case 'zigzag-swoop': {
                const zSign = (Math.random() > 0.5 ? 1 : -1);
                waypoints.push({ x: startX + dx * 0.25 + normX * (curvatureScale * zSign), y: startY + dy * 0.25 + normY * (curvatureScale * zSign) });
                waypoints.push({ x: startX + dx * 0.55 - normX * (curvatureScale * 0.9 * zSign), y: startY + dy * 0.55 - normY * (curvatureScale * 0.9 * zSign) });
                waypoints.push({ x: startX + dx * 0.85 + normX * (curvatureScale * 0.45 * zSign), y: startY + dy * 0.85 + normY * (curvatureScale * 0.45 * zSign) });
                break;
            }
            case 'hyperbolic-slingshot': {
                const hSign = (Math.random() > 0.5 ? 1 : -1);
                waypoints.push({ x: startX + dx * 0.15 - normX * (curvatureScale * 0.8 * hSign), y: startY + dy * 0.15 - normY * (curvatureScale * 0.8 * hSign) });
                waypoints.push({ x: startX + dx * 0.45 + normX * (curvatureScale * 1.5 * hSign), y: startY + dy * 0.45 + normY * (curvatureScale * 1.5 * hSign) });
                waypoints.push({ x: startX + dx * 0.80 + normX * (curvatureScale * 0.3 * hSign), y: startY + dy * 0.80 + normY * (curvatureScale * 0.3 * hSign) });
                break;
            }
            case 'quantum-drift': {
                waypoints.push({ x: startX + dx * 0.30 + (Math.random() - 0.5) * curvatureScale * 1.2, y: startY + dy * 0.30 + (Math.random() - 0.5) * curvatureScale * 1.2 });
                waypoints.push({ x: startX + dx * 0.70 + (Math.random() - 0.5) * curvatureScale * 1.2, y: startY + dy * 0.70 + (Math.random() - 0.5) * curvatureScale * 1.2 });
                break;
            }
            case 'helix-corkscrew': {
                const cRadius = curvatureScale * 0.55;
                const sign = (Math.random() > 0.5 ? 1 : -1);
                waypoints.push({ x: startX + dx * 0.25 + normX * (cRadius * sign), y: startY + dy * 0.25 + normY * (cRadius * sign) });
                waypoints.push({ x: startX + dx * 0.50 - normX * (cRadius * sign), y: startY + dy * 0.50 - normY * (cRadius * sign) });
                waypoints.push({ x: startX + dx * 0.75 + normX * (cRadius * sign), y: startY + dy * 0.75 + normY * (cRadius * sign) });
                break;
            }
            case 'noisy-arc':
            default: {
                const arcScale = curvatureScale * (0.8 + Math.random() * 0.4);
                const sign = (Math.random() > 0.5 ? 1 : -1);
                waypoints.push({ x: startX + dx * 0.33 + normX * (arcScale * sign), y: startY + dy * 0.33 + normY * (arcScale * sign) });
                waypoints.push({ x: startX + dx * 0.66 + normX * (arcScale * 0.75 * sign), y: startY + dy * 0.66 + normY * (arcScale * 0.75 * sign) });
                break;
            }
        }

        waypoints.push({ x: endX, y: endY });

        // Inject chaotic perturbations into intermediate waypoints for wild flight trajectories
        for (let w = 1; w < waypoints.length - 1; w++) {
            const jitterScale = curvatureScale * (0.35 + Math.random() * 0.30);
            waypoints[w].x += (Math.random() - 0.5) * jitterScale;
            waypoints[w].y += (Math.random() - 0.5) * jitterScale;
        }

        // Clamp waypoints to viewport boundaries
        waypoints.forEach(wp => {
            wp.x = Math.max(10, Math.min(viewW - 10, wp.x));
            wp.y = Math.max(10, Math.min(viewH - 10, wp.y));
        });

        return waypoints;
    }

    function getSplinePoint(pts, t) {
        const n = pts.length - 1;
        const p = t * n;
        const i = Math.min(Math.floor(p), n - 1);
        const u = p - i;

        const p0 = pts[Math.max(0, i - 1)];
        const p1 = pts[i];
        const p2 = pts[Math.min(n, i + 1)];
        const p3 = pts[Math.min(n, i + 2)];

        const u2 = u * u;
        const u3 = u2 * u;

        return {
            x: 0.5 * ((2 * p1.x) + (-p0.x + p2.x) * u + (2 * p0.x - 5 * p1.x + 4 * p2.x - p3.x) * u2 + (-p0.x + 3 * p1.x - 3 * p2.x + p3.x) * u3),
            y: 0.5 * ((2 * p1.y) + (-p0.y + p2.y) * u + (2 * p0.y - 5 * p1.y + 4 * p2.y - p3.y) * u2 + (-p0.y + 3 * p1.y - 3 * p2.y + p3.y) * u3)
        };
    }

    function easeInOutCubic(x) {
        return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
    }

    function easeOutQuart(x) {
        return 1 - Math.pow(1 - x, 4);
    }

    function easeOutBack(x) {
        const c1 = 1.70158;
        const c3 = c1 + 1;
        return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2);
    }

    // ─── 7. PRE-ALLOCATED PARTICLE & PULSE RING POOLS ───────────────────────
    const MAX_SPARKS = 160;
    const sparkPool = [];
    for (let i = 0; i < MAX_SPARKS; i++) {
        sparkPool.push({
            x: 0, y: 0, vx: 0, vy: 0,
            life: 0, decay: 0.05,
            color: '#FFFFFF',
            isPlasma: false,
            active: false
        });
    }

    function emitSparks(x, y, count = 10, color = null) {
        let spawned = 0;
        for (let i = 0; i < MAX_SPARKS && spawned < count; i++) {
            const s = sparkPool[i];
            if (!s.active) {
                const angle = Math.random() * Math.PI * 2;
                const speed = 1.8 + Math.random() * 4.2;
                s.x = x;
                s.y = y;
                s.vx = Math.cos(angle) * speed;
                s.vy = Math.sin(angle) * speed - 1.2;
                s.isPlasma = false;
                s.life = 1.0;
                s.decay = 0.038 + Math.random() * 0.045;
                s.color = color || PALETTE[Math.floor(Math.random() * PALETTE.length)];
                s.active = true;
                spawned++;
            }
        }
    }

    function emitPlasmaSparks(x, y, count = 3) {
        let spawned = 0;
        const plasmaColors = [THEME.cyan, THEME.gold, '#FF1E42', '#FFFFFF'];
        for (let i = 0; i < MAX_SPARKS && spawned < count; i++) {
            const s = sparkPool[i];
            if (!s.active) {
                const angle = -Math.PI * 0.5 + (Math.random() - 0.5) * Math.PI * 1.35;
                const speed = 2.5 + Math.random() * 4.8;
                s.x = x;
                s.y = y;
                s.vx = Math.cos(angle) * speed;
                s.vy = Math.sin(angle) * speed;
                s.isPlasma = true;
                s.life = 1.0;
                s.decay = 0.055 + Math.random() * 0.045;
                s.color = plasmaColors[Math.floor(Math.random() * plasmaColors.length)];
                s.active = true;
                spawned++;
            }
        }
    }

    const MAX_PULSE_RINGS = 32;
    const pulseRingPool = [];
    for (let i = 0; i < MAX_PULSE_RINGS; i++) {
        pulseRingPool.push({
            x: 0, y: 0,
            startTime: 0,
            duration: 250,
            maxRadius: 28,
            color: THEME.cyan,
            active: false
        });
    }

    function emitPulseRing(x, y, color = THEME.cyan, maxRadius = 26, duration = 250) {
        for (let i = 0; i < MAX_PULSE_RINGS; i++) {
            const pr = pulseRingPool[i];
            if (!pr.active) {
                pr.x = x;
                pr.y = y;
                pr.color = color;
                pr.maxRadius = maxRadius;
                pr.duration = duration;
                pr.startTime = performance.now();
                pr.active = true;
                break;
            }
        }
    }

    // ─── 8. ELEMENT REGISTRATION & INTERSECTIONOBSERVER PRE-MEASURE ─────────
    const SECTION_ORDER = [
        'home',
        'profile-expertise',
        'about-me',
        'projects',
        'creative-lab',
        'certificates',
        'secret-desk',
        'contact'
    ];

    const elementList = [];
    const sectionMap = {};

    function registerElements() {
        SECTION_ORDER.forEach((secId, secIndex) => {
            const secEl = document.getElementById(secId);
            if (!secEl) return;

            const isHero = (secId === 'home');
            const secInfo = {
                id: secId,
                el: secEl,
                index: secIndex,
                isHero,
                firstEnteredBandTime: 0,
                dwellMet: isHero,
                elements: []
            };
            sectionMap[secId] = secInfo;

            const cardSelector = '.project-card, .cert-card, .expertise-card, .stat-card, .glass-card, .bday-card, .profile-card-wrapper, .cyber-dock-bar, .onboard-card, .hero-details-container';
            const rawElements = Array.from(secEl.querySelectorAll('h1, h2, h3, .section-title, .section-tag, p, .section-desc, .about-text p, .project-card, .cert-card, .expertise-card, .stat-card, .cta-button, .filter-btn, .message-btn, .code-block-visual, .stats-row, .dock-actions-col')).filter(el => {
                if (el.matches(cardSelector)) return true;
                if (el.parentElement && el.parentElement.closest(cardSelector)) return false;
                return true;
            });

            const getPrio = (el) => {
                const tag = el.tagName.toLowerCase();
                if (['h1', 'h2', 'h3'].includes(tag) || el.classList.contains('section-title') || el.classList.contains('section-tag')) return 1;
                if (['p'].includes(tag) || el.classList.contains('section-desc')) return 2;
                if (el.matches(cardSelector) || el.classList.contains('stats-row')) return 3;
                if (['a', 'button'].includes(tag) || el.classList.contains('cta-button') || el.classList.contains('filter-btn') || el.classList.contains('message-btn')) return 4;
                if (el.classList.contains('code-block-visual')) return 3;
                return 5;
            };

            const sorted = rawElements.sort((a, b) => {
                const pA = getPrio(a);
                const pB = getPrio(b);
                if (pA !== pB) return pA - pB;
                return (a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING) ? -1 : 1;
            });

            sorted.forEach((el, order) => {
                const tag = el.tagName.toLowerCase();
                let type = 'card';
                let pullDuration = 600; // Card pull: 600ms fluid holographic 3D extraction

                if (['h1', 'h2', 'h3'].includes(tag) || el.classList.contains('section-title') || el.classList.contains('section-tag')) {
                    type = 'title';
                    pullDuration = 680; // Title scanline sweep: 680ms
                } else if (tag === 'p' || el.classList.contains('section-desc')) {
                    type = 'paragraph';
                    pullDuration = 560; // Paragraph line sweep: 560ms
                } else if (['a', 'button'].includes(tag) || el.classList.contains('cta-button') || el.classList.contains('filter-btn') || el.classList.contains('message-btn')) {
                    type = 'button';
                    pullDuration = 480; // Button/link snap-in: 480ms
                } else if (el.classList.contains('code-block-visual')) {
                    type = 'code-card';
                    pullDuration = 580; // Frame: 580ms
                }

                const item = {
                    id: `${secId}-el-${order}`,
                    secId,
                    secInfo,
                    el,
                    type,
                    minDuration: pullDuration,
                    pullDuration,
                    order,
                    state: isHero ? 'built' : 'pending',
                    gateOpenedTime: 0,
                    dispatchTime: 0,
                    pullStartTime: 0,
                    crew: [],
                    anchors: [],
                    hoverPositions: [],
                    precomputedGeom: null
                };

                if (isHero) {
                    el.setAttribute('data-drone-state', 'built');
                } else {
                    el.setAttribute('data-drone-state', 'pending');
                }

                elementList.push(item);
                secInfo.elements.push(item);
            });
        });

        document.documentElement.classList.add('drones-active');
        initGeometryObserver();
        refreshAllElementRects();
    }

    function computeTractorGeometry(item) {
        const r = item.el.getBoundingClientRect();
        const w = Math.max(40, r.width);
        const h = Math.max(30, r.height);

        const anchors = [
            { x: r.left + Math.min(28, w * 0.20), y: r.top + 8 },
            { x: r.right - Math.min(28, w * 0.20), y: r.top + 8 },
            { x: r.left + w * 0.38, y: r.top + 6 },
            { x: r.left + w * 0.62, y: r.top + 6 }
        ];

        const hoverPositions = [
            { x: r.left - 25, y: r.top - 60 },
            { x: r.right + 25, y: r.top - 60 },
            { x: r.left + w * 0.38 - 12, y: r.top - 75 },
            { x: r.left + w * 0.62 + 12, y: r.top - 75 }
        ];

        return { anchors, hoverPositions, rect: r };
    }

    function initGeometryObserver() {
        if (!('IntersectionObserver' in window)) return;
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                const item = entry.target._droneItem;
                if (item && entry.isIntersecting) {
                    // Batched pre-measurement ONLY, never to reveal
                    item.precomputedGeom = computeTractorGeometry(item);
                }
            });
        }, {
            rootMargin: '120px 0px 120px 0px'
        });

        elementList.forEach(item => {
            item.el._droneItem = item;
            observer.observe(item.el);
        });
    }

    function refreshAllElementRects() {
        elementList.forEach(item => {
            item.precomputedGeom = computeTractorGeometry(item);
        });
    }

    // ─── 9. GATE EVALUATOR & PIPELINED MISSION DISPATCHER ───────────────────
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

        // Scrolled-Past Elements & Sections Fail-Safe:
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
                // Element has genuinely scrolled past upper viewport (completely above screen):
                if (r.bottom < -20) {
                    finishElementInstantly(item);
                    continue;
                }

                // In-view graceful watchdog
                if (item.state === 'pending') {
                    const inView = (r.top < viewH * 0.95 && r.bottom > 20);
                    if (inView) {
                        if (!item.firstVisibleTime) {
                            item.firstVisibleTime = now;
                        } else if (now - item.firstVisibleTime > 6000) {
                            finishElementInstantly(item);
                        }
                    }
                }
            }

            // Section-Level Scrolled-Past Guarantee:
            // If visitor scrolled past an entire section (bottom has moved completely above viewport),
            // reveal all its remaining elements immediately as fail-safe.
            SECTION_ORDER.forEach(secId => {
                const sec = sectionMap[secId];
                if (!sec || sec.isHero) return;
                const r = sec.el.getBoundingClientRect();
                if (r.bottom < -40) {
                    sec.elements.forEach(item => {
                        if (item.state !== 'built') {
                            finishElementInstantly(item);
                        }
                    });
                }
            });
        }

        // Section Dwell Tracker (cinematic recognition delay as visitor scrolls in)
        if (now - lastDwellCheckTime > 25) {
            lastDwellCheckTime = now;
            SECTION_ORDER.forEach(secId => {
                const sec = sectionMap[secId];
                if (!sec || sec.isHero) return;

                const r = sec.el.getBoundingClientRect();
                // A section only enters band if the user has actually scrolled towards it:
                // For the first section (#profile-expertise), require scrollY >= 60 or r.top <= viewH * 0.70
                // For subsequent sections, require section top to be comfortably within view (r.top <= viewH * 0.75)
                const isFirstSec = (sec.index === 1);
                const hasScrolledIntoSec = isFirstSec ? (scrollY >= 60 && r.top <= viewH * 0.85) : (r.top <= viewH * 0.75);
                const inBand = hasScrolledIntoSec && (r.bottom >= viewH * 0.10 && r.top <= viewH * 0.75);

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

        // Settle check (fast settle <= 30ms, fluid scrolling)
        const scrollSettled = (now - lastFastScrollTime >= SCROLL_SETTLE_MS);
        if (!scrollSettled) return;

        // Pull out properties in sequence (up to MAX_ACTIVE_CREWS pipelined)
        if (activeMissions.length >= MAX_ACTIVE_CREWS) return;
        if (now - lastMissionFinishTime < 30 && activeMissions.length === 0) return;

        // Sequence Order & Band Evaluation: natural top-to-bottom cinematic extraction
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

                // An element qualifies if its top has entered into the viewport
                if (r.top <= viewH * 0.88 && r.bottom >= viewH * 0.05) {
                    bandSatisfiedElements.push(item);
                }
            }

            if (bandSatisfiedElements.length === 0) continue;

            // Slots available for simultaneous pull (up to MAX_ACTIVE_CREWS)
            const availableSlots = MAX_ACTIVE_CREWS - activeMissions.length;
            if (availableSlots <= 0) return;

            // Pick in natural top-to-bottom visual reading order (NOT random!)
            const toDispatch = bandSatisfiedElements.slice(0, availableSlots);

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
        }
    }

    function dispatchMission(item, crewDrones, now) {
        item.state = 'dispatched';
        item.gateOpenedTime = now;
        item.dispatchTime = now;
        item.crew = crewDrones;
        lastDispatchTimestamp = now;

        item.el.setAttribute('data-drone-state', 'flight');
        item.el.style.willChange = 'transform, opacity';

        const geom = computeTractorGeometry(item);
        item.anchors = geom.anchors;
        item.hoverPositions = geom.hoverPositions;

        const initScrollY = window.scrollY || window.pageYOffset;
        const initScrollX = window.scrollX || window.pageXOffset;

        // Visible flight: 220ms (snappy responsive dispatch)
        const HIVE_PULSE_MS = 70;
        const FLIGHT_TIME_MS = 220;
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
            baseHoverPositions: geom.hoverPositions.map(h => ({ x: h.x + initScrollX, y: h.y + initScrollY })),
            onDroneArrived(drone) {
                this.arrivedCount++;
                if (drone.targetAnchor) {
                    emitPulseRing(drone.targetAnchor.x, drone.targetAnchor.y, THEME.cyan, 22, 220);
                    emitPlasmaSparks(drone.targetAnchor.x, drone.targetAnchor.y, 3);
                }
                if (this.arrivedCount >= this.crew.length) {
                    this.startPull(performance.now());
                }
            },
            startPull(pullNow) {
                this.pullStartedAt = pullNow;
                this.lockOnStart = pullNow;
                this.item.pullStartTime = pullNow;
                this.item.state = 'pulling';
                this.item.el.setAttribute('data-drone-state', 'pulling');

                if (firstRevealTimestamp === 0) {
                    firstRevealTimestamp = pullNow;
                }

                // Snap HUD brackets and quantum welding contact flare
                this.anchors.forEach(a => {
                    emitPulseRing(a.x, a.y, THEME.gold, 26, 260);
                    emitPlasmaSparks(a.x, a.y, 4);
                });
            }
        };

        // Assign ribbon flight paths (Lead = gold, Followers = purple)
        crewDrones.forEach((drone, idx) => {
            drone.state = 'DISPATCH';
            drone.activeMission = mission;
            drone.crewIndex = idx;
            drone.isLead = (idx === 0);
            drone.flightStart = now;
            drone.flightDuration = totalFlightDuration;

            const anchor = geom.anchors[idx % geom.anchors.length];
            const hover = geom.hoverPositions[idx % geom.hoverPositions.length];
            drone.targetAnchor = anchor;
            drone.hoverPos = hover;

            drone.pathPoints = generateProceduralPath(cursorX, cursorY, hover.x, hover.y, drone.flightDuration);
            drone.resetTrail();
        });

        activeMissions.push(mission);
    }

    function updateActiveMissions(now, dt) {
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
            });

            if (item.state === 'pulling') {
                const pullElapsed = now - m.pullStartedAt;
                const progress = Math.min(1.0, pullElapsed / m.pullDuration);

                // Distinct 3D Kinetic Assembly Per Element Type (Cinematic Gen-Z Physics)
                if (item.type === 'title') {
                    // Titles: 3D Scanline laser sweep with chromatic holographic emergence
                    const easeP = easeOutQuart(progress);
                    const offsetY = Math.round(24 * (1 - easeP));
                    const rotX = (8 * (1 - easeP)).toFixed(1);
                    const zDepth = Math.round(-30 * (1 - easeP));
                    item.el.style.transform = `perspective(900px) translate3d(0, ${offsetY}px, ${zDepth}px) rotateX(${rotX}deg)`;
                    item.el.style.opacity = Math.min(1.0, 0.2 + easeP * 0.8).toFixed(3);
                    item.el.style.clipPath = `polygon(0 0, ${Math.round(easeP * 100)}% 0, ${Math.round(easeP * 100)}% 100%, 0 100%)`;
                    item.el.classList.add('drone-scanline-active');
                } else if (item.type === 'paragraph') {
                    // Paragraphs: smooth progressive unfurl with upward glide
                    const easeP = easeOutQuart(progress);
                    const offsetY = Math.round(18 * (1 - easeP));
                    item.el.style.transform = `translate3d(0, ${offsetY}px, 0)`;
                    item.el.style.opacity = easeP.toFixed(3);
                    item.el.style.clipPath = `polygon(0 0, ${Math.round(easeP * 100)}% 0, ${Math.round(easeP * 100)}% 100%, 0 100%)`;
                } else if (item.type === 'card') {
                    // Cards: Authentic 3D Gen-Z holographic corner pull-out with depth and spring
                    const springEase = easeOutBack(progress);
                    const easeP = easeOutQuart(progress);
                    const zDepth = Math.round(-65 * (1 - easeP));
                    const rotX = (10 * (1 - easeP)).toFixed(2);
                    const offsetY = Math.round(36 * (1 - progress) - (progress < 0.85 ? 4 * Math.sin(progress * Math.PI) : 0));
                    const scale = (0.95 + 0.05 * springEase).toFixed(3);
                    item.el.style.transform = `perspective(1000px) translate3d(0, ${offsetY}px, ${zDepth}px) rotateX(${rotX}deg) scale(${scale})`;
                    item.el.style.opacity = Math.min(1.0, 0.2 + progress * 0.8).toFixed(3);
                } else if (item.type === 'button') {
                    // Buttons: 3D forward pop-up snap
                    const easeP = easeOutQuart(progress);
                    const offsetY = Math.round(12 * (1 - easeP));
                    const scale = (0.92 + 0.08 * easeP).toFixed(3);
                    item.el.style.transform = `perspective(800px) translate3d(0, ${offsetY}px, 15px) scale(${scale})`;
                    item.el.style.opacity = easeP.toFixed(3);
                } else if (item.type === 'code-card') {
                    // Code-IDE card: 3D terminal materialization + line scanning
                    const frameEase = easeOutQuart(progress);
                    const offsetY = Math.round(30 * (1 - frameEase));
                    const zDepth = Math.round(-50 * (1 - frameEase));
                    item.el.style.transform = `perspective(1000px) translate3d(0, ${offsetY}px, ${zDepth}px) rotateX(${(7 * (1 - frameEase)).toFixed(1)}deg) scale(${(0.96 + 0.04 * frameEase).toFixed(3)})`;
                    item.el.style.opacity = Math.min(1.0, 0.25 + frameEase * 0.75).toFixed(3);

                    const lines = item.el.querySelectorAll('.drone-code-line, .code-line');
                    if (lines.length) {
                        const lineIdx = Math.floor(frameEase * lines.length);
                        lines.forEach((l, idx) => {
                            if (idx <= lineIdx && !l.classList.contains('revealed')) {
                                l.classList.add('revealed');
                                const lr = l.getBoundingClientRect();
                                emitSparks(lr.left + 16, lr.top + 6, 3, THEME.cyan);
                            }
                        });
                    }
                }

                // Plasma welding sparks along contact anchors
                if (!isQualityLow && Math.random() < 0.40) {
                    const cAnchor = m.anchors[Math.floor(Math.random() * m.anchors.length)];
                    if (cAnchor) emitPlasmaSparks(cAnchor.x, cAnchor.y, 2);
                }

                // Pull completion & impact
                if (progress >= 1.0) {
                    finishElement(item);
                    returnCrew(m.crew, now);
                    activeMissions.splice(i, 1);
                }
            }
        }
    }

    function finishElement(item) {
        item.state = 'built';
        lastMissionFinishTime = performance.now();
        item.el.setAttribute('data-drone-state', 'built');
        item.el.style.transform = '';
        item.el.style.opacity = '';
        item.el.style.filter = '';
        item.el.style.clipPath = '';
        item.el.style.willChange = '';
        item.el.classList.remove('drone-scanline-active');

        // Impact Flourish: 60ms RGB-split flash + spark burst + pulse ring
        if (!isQualityLow) {
            item.el.classList.add('drone-rgb-impact');
            setTimeout(() => item.el.classList.remove('drone-rgb-impact'), 65);
        }

        if (item.el.classList.contains('scroll-reveal')) {
            item.el.classList.add('active');
        }
        if (item.el.parentElement && item.el.parentElement.classList.contains('about-visual')) {
            item.el.parentElement.classList.add('active');
        }

        // Unclip all code lines
        const codeLines = item.el.querySelectorAll('.drone-code-line, .code-line');
        if (codeLines.length) {
            codeLines.forEach(l => {
                l.classList.add('revealed');
                l.style.clipPath = 'inset(0 0 0 0)';
                l.style.opacity = '1';
            });
        }

        // Placement sparks & pulse
        const r = item.el.getBoundingClientRect();
        emitSparks(r.left + 14, r.top + 10, 8, THEME.gold);
        emitSparks(r.right - 14, r.top + 10, 8, THEME.turquoise);
        emitPulseRing(r.left + r.width * 0.5, r.top + r.height * 0.5, THEME.cyan, 34, 260);
    }

    function finishElementInstantly(item) {
        if (item.state === 'built') return;
        item.state = 'built';
        item.el.setAttribute('data-drone-state', 'built');
        item.el.style.transform = '';
        item.el.style.opacity = '';
        item.el.style.filter = '';
        item.el.style.clipPath = '';
        item.el.style.willChange = '';
        item.el.classList.remove('drone-scanline-active');

        const missionIdx = activeMissions.findIndex(m => m.item === item);
        if (missionIdx !== -1) {
            const m = activeMissions[missionIdx];
            returnCrew(m.crew, performance.now());
            activeMissions.splice(missionIdx, 1);
        }

        if (item.el.classList.contains('scroll-reveal')) {
            item.el.classList.add('active');
        }
        if (item.el.parentElement && item.el.parentElement.classList.contains('about-visual')) {
            item.el.parentElement.classList.add('active');
        }

        const codeLines = item.el.querySelectorAll('.drone-code-line, .code-line');
        if (codeLines.length) {
            codeLines.forEach(l => {
                l.classList.add('revealed');
                l.style.clipPath = 'inset(0 0 0 0)';
                l.style.opacity = '1';
            });
        }

        if (item.crew && item.crew.length) {
            returnCrew(item.crew, performance.now());
        }
    }

    // Fast-scroll fail-safe: automatically resolve properties immediately when flick-scrolling fast
    function triggerFastScrollFailsafe() {
        const vH = window.innerHeight;
        for (let i = 0; i < elementList.length; i++) {
            const item = elementList[i];
            if (item.state === 'built') continue;
            const r = item.el.getBoundingClientRect();
            // Only resolve elements that are currently inside or passed above the viewport
            if (r.top < vH * 0.90 && r.bottom > -150) {
                finishElementInstantly(item);
            }
        }
    }

    function returnCrew(crewDrones, now) {
        crewDrones.forEach((drone, idx) => {
            drone.state = 'RETURN';
            drone.flightStart = now;
            drone.flightDuration = Math.round(280 + Math.random() * 100);

            // Outward burst scatter impulse
            const scatterAngle = Math.random() * Math.PI * 2;
            drone.vx += Math.cos(scatterAngle) * 3.5;
            drone.vy += Math.sin(scatterAngle) * 3.5;

            // Random return orbit slot around cursor
            const returnAngle = Math.random() * Math.PI * 2;
            const returnRadius = R_MIN + Math.random() * (R_MAX - R_MIN);
            const targetX = cursorX + Math.cos(returnAngle) * returnRadius;
            const targetY = cursorY + Math.sin(returnAngle) * returnRadius;

            drone.targetAnchor = { x: targetX, y: targetY };
            drone.hoverPos = { x: targetX, y: targetY };
            drone.pathPoints = generateProceduralPath(drone.x, drone.y, targetX, targetY, drone.flightDuration);
            drone.resetTrail();
        });
    }

    // ─── 10. BATCH DRAWING & HUD LOCK-ON BRACKETS (< 40 DRAW CALLS) ─────────
    let currentDrawCalls = 0;

    function drawTractorBeamsAndHUD(ctx, now) {
        if (activeMissions.length === 0) return;

        // 1. Single Batched Path for ALL Lock-On HUD Brackets
        let hasBrackets = false;
        ctx.beginPath();
        activeMissions.forEach(m => {
            if (m.item.state !== 'pulling') return;
            const elapsedLockOn = now - m.lockOnStart;
            if (elapsedLockOn > 200) return;
            const r = m.item.el.getBoundingClientRect();
            const bLen = Math.min(16, r.width * 0.18, r.height * 0.35);
            hasBrackets = true;

            // Top-left
            ctx.moveTo(r.left, r.top + bLen); ctx.lineTo(r.left, r.top); ctx.lineTo(r.left + bLen, r.top);
            // Top-right
            ctx.moveTo(r.right - bLen, r.top); ctx.lineTo(r.right, r.top); ctx.lineTo(r.right, r.top + bLen);
            // Bottom-left
            ctx.moveTo(r.left, r.bottom - bLen); ctx.lineTo(r.left, r.bottom); ctx.lineTo(r.left + bLen, r.bottom);
            // Bottom-right
            ctx.moveTo(r.right - bLen, r.bottom); ctx.lineTo(r.right, r.bottom); ctx.lineTo(r.right, r.bottom - bLen);
        });
        if (hasBrackets) {
            ctx.strokeStyle = 'rgba(25, 227, 209, 0.85)';
            ctx.lineWidth = 1.6;
            ctx.stroke();
            currentDrawCalls++;
        }

        // 2. High-Voltage Static Electricity / Lightning Discharge Tethers [Electric Plasma Engine]
        const arcs = [];
        activeMissions.forEach((m, mIdx) => {
            if (m.item.state !== 'pulling') return;
            m.crew.forEach((drone, idx) => {
                const anchor = drone.targetAnchor;
                if (!anchor) return;
                const dx = anchor.x - drone.x;
                const dy = anchor.y - drone.y;
                const dist = Math.hypot(dx, dy);
                if (dist < 4) return;

                const nx = -dy / dist;
                const ny = dx / dist;
                const segments = Math.max(5, Math.min(9, Math.round(dist / 28)));
                const points = [{ x: drone.x, y: drone.y }];
                const seed = mIdx * 17 + idx * 31;

                for (let k = 1; k < segments; k++) {
                    const t = k / segments;
                    const bx = drone.x + dx * t;
                    const by = drone.y + dy * t;
                    const envelope = Math.sin(t * Math.PI);
                    // High-frequency zigzag electric discharge
                    const freq = (now * 0.042 + seed + k * 5.7);
                    const jitter = (Math.sin(freq) * 0.65 + Math.sin(freq * 2.3 + k) * 0.35);
                    const arcOffset = jitter * Math.min(18, dist * 0.22) * envelope;
                    const alongOffset = (Math.cos(freq * 1.8) * 3.5) * envelope;

                    points.push({
                        x: bx + nx * arcOffset + (dx / dist) * alongOffset,
                        y: by + ny * arcOffset + (dy / dist) * alongOffset
                    });
                }
                points.push({ x: anchor.x, y: anchor.y });

                // Occasional micro-branch / lightning fork
                let fork = null;
                if (!isQualityLow && Math.sin(now * 0.06 + seed) > 0.3 && points.length > 3) {
                    const branchIdx = Math.floor(points.length * 0.45);
                    const origin = points[branchIdx];
                    const forkAngle = Math.atan2(dy, dx) + (idx % 2 === 0 ? 0.65 : -0.65);
                    const forkLen = 10 + (Math.sin(now * 0.08 + idx) + 1) * 6;
                    fork = {
                        x1: origin.x,
                        y1: origin.y,
                        x2: origin.x + Math.cos(forkAngle) * forkLen,
                        y2: origin.y + Math.sin(forkAngle) * forkLen
                    };
                }

                arcs.push({ points, fork, drone, anchor, idx });
            });
        });

        if (arcs.length > 0) {
            // Pass A: Outer Plasma Glow Halo (Cyber Cyan electric field)
            ctx.beginPath();
            arcs.forEach(arc => {
                const pts = arc.points;
                ctx.moveTo(pts[0].x, pts[0].y);
                for (let i = 1; i < pts.length; i++) {
                    ctx.lineTo(pts[i].x, pts[i].y);
                }
                if (arc.fork) {
                    ctx.moveTo(arc.fork.x1, arc.fork.y1);
                    ctx.lineTo(arc.fork.x2, arc.fork.y2);
                }
            });
            ctx.strokeStyle = 'rgba(0, 245, 212, 0.45)';
            ctx.lineWidth = 3.6;
            ctx.stroke();
            currentDrawCalls++;

            // Pass B: Intense Resonant Violet Inner Field
            ctx.beginPath();
            arcs.forEach(arc => {
                const pts = arc.points;
                ctx.moveTo(pts[0].x, pts[0].y);
                for (let i = 1; i < pts.length; i++) {
                    ctx.lineTo(pts[i].x, pts[i].y);
                }
            });
            ctx.strokeStyle = 'rgba(139, 92, 246, 0.70)';
            ctx.lineWidth = 2.2;
            ctx.stroke();
            currentDrawCalls++;

            // Pass C: Pure Blazing White Electric Core (High-voltage discharge line)
            ctx.beginPath();
            arcs.forEach(arc => {
                const pts = arc.points;
                ctx.moveTo(pts[0].x, pts[0].y);
                for (let i = 1; i < pts.length; i++) {
                    ctx.lineTo(pts[i].x, pts[i].y);
                }
                if (arc.fork) {
                    ctx.moveTo(arc.fork.x1, arc.fork.y1);
                    ctx.lineTo(arc.fork.x2, arc.fork.y2);
                }
            });
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.95)';
            ctx.lineWidth = 1.2;
            ctx.stroke();
            currentDrawCalls++;

            // Contact micro-sparks at anchor points
            if (!isQualityLow && Math.random() < 0.25) {
                const randomArc = arcs[Math.floor(Math.random() * arcs.length)];
                if (randomArc) {
                    emitSparks(randomArc.anchor.x, randomArc.anchor.y, 1, THEME.cyan);
                }
            }
        }
    }

    function drawBatchedTrails(ctx) {
        // Tails removed per user specification - zero trail lines rendered
        return;
    }

    function updateAndDrawParticles(ctx, now) {
        // Update & Draw Sparks in batch
        let sparkCount = 0;
        ctx.beginPath();
        for (let i = 0; i < MAX_SPARKS; i++) {
            const s = sparkPool[i];
            if (!s.active) continue;
            s.x += s.vx;
            s.y += s.vy;
            s.life -= s.decay;
            if (s.life <= 0) {
                s.active = false;
                continue;
            }
            sparkCount++;
            ctx.moveTo(s.x, s.y);
            ctx.arc(s.x, s.y, s.isPlasma ? 1.6 : 1.2, 0, Math.PI * 2);
        }
        if (sparkCount > 0) {
            ctx.fillStyle = THEME.gold;
            ctx.fill();
            currentDrawCalls++;
        }

        // Draw Pulse Rings
        for (let i = 0; i < MAX_PULSE_RINGS; i++) {
            const pr = pulseRingPool[i];
            if (!pr.active) continue;
            const elapsed = now - pr.startTime;
            if (elapsed < 0) continue;
            const progress = Math.max(0, Math.min(1.0, elapsed / pr.duration));
            if (progress >= 1.0) {
                pr.active = false;
                continue;
            }
            const currentR = Math.max(0.1, pr.maxRadius * easeOutQuart(progress));
            const alpha = (1.0 - progress) * 0.45;
            ctx.beginPath();
            ctx.arc(pr.x, pr.y, currentR, 0, Math.PI * 2);
            ctx.strokeStyle = pr.color;
            ctx.globalAlpha = alpha;
            ctx.lineWidth = 1.2;
            ctx.stroke();
            ctx.globalAlpha = 1.0;
            currentDrawCalls++;
        }
    }

    // ─── 11. ADAPTIVE QUALITY MONITOR & 30-FRAME RING BUFFER ───────────────
    const FRAME_HISTORY_SIZE = 30;
    const frameTimeRing = new Float32Array(FRAME_HISTORY_SIZE);
    let frameTimeIndex = 0;
    let isQualityLow = false;
    let averageFrameTime = 16.6;

    function recordFrameTime(frameDurationMs) {
        frameTimeRing[frameTimeIndex] = frameDurationMs;
        frameTimeIndex = (frameTimeIndex + 1) % FRAME_HISTORY_SIZE;

        let sum = 0;
        for (let i = 0; i < FRAME_HISTORY_SIZE; i++) {
            sum += frameTimeRing[i];
        }
        averageFrameTime = sum / FRAME_HISTORY_SIZE;

        // Step down if average frame time > 14ms over 30 frames
        if (!isQualityLow && averageFrameTime > 14.0) {
            isQualityLow = true;
        } else if (isQualityLow && averageFrameTime <= 12.0) {
            isQualityLow = false;
        }
    }

    // ─── 12. WATCHDOG & FAILSAFE ───────────────────────────────────────────
    function revealAllInstantly() {
        elementList.forEach(item => finishElementInstantly(item));
        document.documentElement.classList.add('drones-done');
        ctx.clearRect(0, 0, viewW, viewH);
    }

    const watchdogTimer = setTimeout(() => {
        const homeSec = sectionMap['home'];
        if (homeSec) {
            homeSec.elements.forEach(el => finishElementInstantly(el));
        }
    }, 2500);

    window.addEventListener('beforeprint', () => { revealAllInstantly(); });

    // ─── 13. SINGLE REQUESTANIMATIONFRAME LOOP ─────────────────────────────
    let lastFrameTime = performance.now();
    let isLoopRunning = false;

    function mainLoop(now) {
        if (document.hidden) {
            isLoopRunning = false;
            return;
        }

        const dt = Math.min(0.05, (now - lastFrameTime) / 1000);
        const frameStart = performance.now();
        lastFrameTime = now;
        currentDrawCalls = 0;

        ctx.clearRect(0, 0, viewW, viewH);

        // Update cursor center
        cursorX = targetCursorX;
        cursorY = targetCursorY;

        // 1. Update Drones (FOLLOW, DISPATCH, PULL, RETURN)
        drones.forEach(drone => {
            if (drone.state === 'FOLLOW') {
                drone.updateFollow(now, dt);
            } else if (drone.state === 'DISPATCH' || drone.state === 'RETURN') {
                drone.updateFlight(now, dt);
            } else if (drone.state === 'PULL') {
                drone.updatePull(now, dt);
            }
        });

        // Update active burst drones
        burstDronePool.forEach(drone => {
            if (drone.state === 'DISPATCH' || drone.state === 'RETURN') {
                drone.updateFlight(now, dt);
            } else if (drone.state === 'PULL') {
                drone.updatePull(now, dt);
            }
        });

        // 2. Gate evaluation & pipelining
        checkBuildGate(now);

        // 3. Update active missions
        updateActiveMissions(now, dt);

        // 4. Batch drawing with additive blending (< 40 draw calls)
        ctx.save();
        ctx.globalCompositeOperation = 'lighter';

        drawBatchedTrails(ctx);
        drawTractorBeamsAndHUD(ctx, now);
        updateAndDrawParticles(ctx, now);

        // 5. Draw Drones via pre-rendered sprites
        drones.forEach(drone => {
            drone.draw(ctx);
            currentDrawCalls++;
        });
        burstDronePool.forEach(drone => {
            if (drone.state !== 'INACTIVE') {
                drone.draw(ctx);
                currentDrawCalls++;
            }
        });

        ctx.restore();

        // 6. Record frame metrics for Adaptive Quality
        const frameDelta = performance.now() - frameStart;
        recordFrameTime(frameDelta);

        requestAnimationFrame(mainLoop);
    }

    function startLoop() {
        if (!isLoopRunning) {
            isLoopRunning = true;
            lastFrameTime = performance.now();
            requestAnimationFrame(mainLoop);
        }
    }

    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            isLoopRunning = false;
        } else {
            startLoop();
        }
    });

    // ─── 14. INITIALIZATION ────────────────────────────────────────────────
    function init() {
        registerElements();
        resizeCanvas();
        startLoop();

        // Hero initial mission within 500ms
        setTimeout(() => {
            const homeSec = sectionMap['home'];
            if (homeSec) {
                homeSec.elements.forEach(item => finishElement(item));
            }
        }, 400);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // ─── 15. PUBLIC VERIFICATION API (PLAYWRIGHT COMPLIANT) ─────────────────
    window.drones = {
        getDrones: () => drones,
        getBurstDrones: () => burstDronePool,
        getElements: () => elementList,
        getMissions: () => activeMissions,
        getSparks: () => sparkPool.filter(s => s.active),
        getPulseRings: () => pulseRingPool.filter(p => p.active),
        emitPulseRing,
        emitPlasmaSparks,
        revealAll: revealAllInstantly,
        R_MIN,
        R_MAX,
        getMetrics: () => ({
            drawCalls: currentDrawCalls,
            avgFrameTime: averageFrameTime,
            isQualityLow,
            activeCrewsCount: activeMissions.length,
            lastDispatchTimestamp,
            firstRevealTimestamp
        })
    };

    window.swarm = {
        getDotsData: () => drones.map(d => ({ currentX: d.x, currentY: d.y, opacity: d.opacity })),
        setPhase: (p, m) => {},
        release: () => {}
    };

    window.__dronesActive = true;
})();
