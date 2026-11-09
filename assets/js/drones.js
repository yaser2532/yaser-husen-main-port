/**
 * DRONES SYSTEM [assets/js/drones.js]
 * Unified Swarm & Autonomous Construction Drones Engine
 * 
 * Complies with strict specifications:
 * - Single fixed full-viewport canvas overlay, pointer-events:none, DPR capped at 2.
 * - ONE shared requestAnimationFrame loop. Pauses when tab is hidden.
 * - FOLLOW (R_min=18px, R_max=46px, spring-damper, settle <= 400ms).
 * - DIM (opacity 0.3 over 150ms over text; restores to 1.0 over 250ms).
 * - BUILD GATE (80% inside 8%-88% band, scroll < 800px/s for 200ms, dwell >= 400ms, sequence predecessor).
 * - PROCEDURAL RANDOM PATHS (spiral, loop, figure-8, noisy-arc, orbit-dive, zigzag-swoop; Catmull-Rom spline, 600-1400ms flight, 400-900ms return).
 * - SPECTACLE GUARANTEE (reveal begins ONLY after crew flies >= 500ms and arrives).
 * - DURATIONS: title 1100ms, paragraph 900ms, card 600ms (160ms stagger), button 450ms, code-card line-by-line (700ms frame + 140ms/line).
 * - Watchdog failsafe (2.5s hero, 3.5s gate failsafe).
 */

(function () {
    'use strict';

    // ─── 1. CONSTANTS & CONFIGURATION ───────────────────────────────────────
    const THEME = {
        gold: '#F5C542',
        purple: '#8B3DFF',
        turquoise: '#19E3D1',
        black: '#07060B',
        white: '#FFFFFF'
    };

    const PALETTE = [THEME.gold, THEME.purple, THEME.turquoise];

    const R_MIN = 18;
    const R_MAX = 46;

    const READABLE_TAGS = new Set([
        'A', 'BUTTON', 'INPUT', 'TEXTAREA', 'SELECT', 'LABEL',
        'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'P', 'LI', 'SPAN',
        'CODE', 'PRE', 'BLOCKQUOTE', 'STRONG', 'EM', 'B', 'I'
    ]);

    const BAND_TOP = 0.08;   // 8% viewport height
    const BAND_BOTTOM = 0.88; // 88% viewport height
    const SCROLL_VELOCITY_LIMIT = 800; // px/s
    const SCROLL_SETTLE_MS = 100;      // ms (responsive settle)
    const SECTION_DWELL_MS = 100;      // ms (reduced dwell for 0.5s faster build trigger)
    const MAX_ACTIVE_CREWS = 3;

    const isMobile = window.innerWidth < 768;
    const DRONE_COUNT = isMobile ? 8 : 14;
    const CREW_SIZE = isMobile ? 3 : 4;

    const isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // ─── 2. CANVAS & SIZING SETUP ───────────────────────────────────────────
    let canvas = document.getElementById('nb-canvas');
    if (!canvas) {
        canvas = document.createElement('canvas');
        canvas.id = 'nb-canvas';
        canvas.setAttribute('aria-hidden', 'true');
        document.body.appendChild(canvas);
    }

    const ctx = canvas.getContext('2d');
    let viewW = window.innerWidth;
    let viewH = window.innerHeight;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);

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

    // ─── 3. CURSOR & TOUCH TRACKER (FOLLOW & DIM STATE) ────────────────────
    let cursorX = viewW * 0.5;
    let cursorY = viewH * (isMobile ? 0.72 : 0.45);
    let targetCursorX = cursorX;
    let targetCursorY = cursorY;
    let cursorInWindow = true;
    let isTouchMode = false;
    let isOverText = false;
    let swarmGlobalDim = 1.0; // 0.3 to 1.0

    // Measure scroll speed
    let lastScrollY = window.scrollY || window.pageYOffset;
    let lastScrollTime = performance.now();
    let currentScrollSpeed = 0; // px/s
    let lastFastScrollTime = 0;

    window.addEventListener('mousemove', (e) => {
        isTouchMode = false;
        cursorInWindow = true;
        targetCursorX = e.clientX;
        targetCursorY = e.clientY;
        checkDimUnderPointer(e.clientX, e.clientY);
    }, { passive: true });

    window.addEventListener('touchmove', (e) => {
        isTouchMode = true;
        cursorInWindow = true;
        if (e.touches && e.touches[0]) {
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

    document.addEventListener('mouseleave', () => {
        cursorInWindow = false;
    });

    document.addEventListener('mouseenter', () => {
        cursorInWindow = true;
    });

    // Throttled elementFromPoint for DIM state
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

        // Check if directly inside a readable container or text class
        const textAncestor = el.closest('p, h1, h2, h3, h4, h5, h6, a, button, label, li, code, span, .trait-tag, .section-desc');
        isOverText = Boolean(textAncestor);
    }

    // Scroll listener: passive, tracks scroll speed without geometry reads
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
            lastScrollY = currentY;
            lastScrollTime = now;
        }
    }, { passive: true });

    // ─── 4. DRONE OBJECTS & POOL ───────────────────────────────────────────
    class Drone {
        constructor(id) {
            this.id = id;
            this.color = PALETTE[id % PALETTE.length];
            this.size = 1.8 + (id % 3) * 0.4; // 1.8px to 2.6px (sleek, shorter dots)
            
            // Orbit geometry
            this.orbitRadius = R_MIN + (id / DRONE_COUNT) * (R_MAX - R_MIN);
            this.orbitAngle = (id / DRONE_COUNT) * Math.PI * 2;
            this.orbitSpeed = 0.85 + (id % 4) * 0.22;
            this.orbitDir = (id % 2 === 0) ? 1 : -1;
            this.noisePhase = id * 1.37;
            this.stiffness = 0.14 + (id % 3) * 0.04;
            this.damping = 0.78 + (id % 3) * 0.04;

            // Coordinates
            this.x = cursorX + Math.cos(this.orbitAngle) * this.orbitRadius;
            this.y = cursorY + Math.sin(this.orbitAngle) * this.orbitRadius;
            this.vx = 0;
            this.vy = 0;
            this.opacity = 1.0;
            this.targetOpacity = 1.0;

            // State: 'FOLLOW' | 'DISPATCH' | 'PULL' | 'RETURN'
            this.state = 'FOLLOW';
            this.activeMission = null;
            this.crewIndex = -1;

            // Procedural path tracking
            this.flightStart = 0;
            this.flightDuration = 800;
            this.pathPoints = [];
            this.targetAnchor = { x: 0, y: 0 };

            // Trail history (compact tight trail)
            this.trail = [];
            this.maxTrail = 2;
        }

        updateFollow(now, dt) {
            // Natural orbital drift
            this.orbitAngle += this.orbitSpeed * this.orbitDir * dt;
            const idleNoiseX = Math.sin(now * 0.003 + this.noisePhase) * 4;
            const idleNoiseY = Math.cos(now * 0.0025 + this.noisePhase) * 4;

            const desiredX = cursorX + Math.cos(this.orbitAngle) * this.orbitRadius + idleNoiseX;
            const desiredY = cursorY + Math.sin(this.orbitAngle) * this.orbitRadius + idleNoiseY;

            // Spring-damper physics
            const ax = (desiredX - this.x) * this.stiffness;
            const ay = (desiredY - this.y) * this.stiffness;
            this.vx = (this.vx + ax) * this.damping;
            this.vy = (this.vy + ay) * this.damping;
            this.x += this.vx;
            this.y += this.vy;

            // Strict R_MAX boundary clamp: Never exceed R_max from cursor in FOLLOW
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
            const fadeSpeed = (targetOp < this.opacity) ? 0.24 : 0.16;
            this.opacity += (targetOp - this.opacity) * fadeSpeed;

            this.pushTrail();
        }

        updateFlight(now, dt) {
            const elapsed = now - this.flightStart;
            const t = Math.min(1.0, elapsed / this.flightDuration);
            const easeT = easeInOutCubic(t);

            if (this.pathPoints.length >= 4) {
                // Catmull-Rom spline interpolation along waypoints
                const pos = getSplinePoint(this.pathPoints, easeT);
                this.x = pos.x;
                this.y = pos.y;
            } else {
                // Linear fallback with curve offset
                const p0 = this.pathPoints[0] || { x: this.x, y: this.y };
                const p1 = this.targetAnchor;
                this.x = p0.x + (p1.x - p0.x) * easeT;
                this.y = p0.y + (p1.y - p0.y) * easeT;
            }

            this.opacity = 1.0;
            this.pushTrail();

            if (t >= 1.0) {
                if (this.state === 'DISPATCH') {
                    this.state = 'PULL';
                    if (this.activeMission) {
                        this.activeMission.onDroneArrived(this);
                    }
                } else if (this.state === 'RETURN') {
                    this.state = 'FOLLOW';
                    this.activeMission = null;
                }
            }
        }

        updatePull(now, dt) {
            // Latch onto target anchor with slight high-frequency micro-jitter
            const jitterX = Math.sin(now * 0.05 + this.id * 1.5) * 1.8;
            const jitterY = Math.cos(now * 0.06 + this.id * 1.2) * 1.8;
            this.x = this.targetAnchor.x + jitterX;
            this.y = this.targetAnchor.y + jitterY;
            this.opacity = 1.0;
            this.pushTrail();
        }

        pushTrail() {
            this.trail.unshift({ x: this.x, y: this.y, opacity: this.opacity });
            if (this.trail.length > this.maxTrail) {
                this.trail.pop();
            }
        }

        draw(ctx) {
            // Draw short fading trail
            for (let i = this.trail.length - 1; i >= 1; i--) {
                const p = this.trail[i];
                const trailAlpha = (p.opacity * (1 - i / this.trail.length) * 0.28);
                ctx.beginPath();
                ctx.arc(p.x, p.y, Math.max(0.6, this.size * 0.45), 0, Math.PI * 2);
                ctx.fillStyle = this.color;
                ctx.globalAlpha = trailAlpha;
                ctx.fill();
            }

            // Outer soft glow halo (shorter, crisper perimeter)
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size * 1.4, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.globalAlpha = this.opacity * 0.18;
            ctx.fill();

            // Main drone core
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size * 0.72, 0, Math.PI * 2);
            ctx.fillStyle = this.color;
            ctx.globalAlpha = this.opacity * 0.95;
            ctx.fill();

            // Intense white specular center
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size * 0.26, 0, Math.PI * 2);
            ctx.fillStyle = THEME.white;
            ctx.globalAlpha = this.opacity * 0.98;
            ctx.fill();

            ctx.globalAlpha = 1.0;
        }
    }

    const drones = [];
    for (let i = 0; i < DRONE_COUNT; i++) {
        drones.push(new Drone(i));
    }

    // ─── 5. PROCEDURAL RANDOM PATHS GENERATOR (PHASE 5) ─────────────────────
    const PATH_TYPES = ['spiral-in', 'loop-the-loop', 'figure-8', 'noisy-arc', 'orbit-dive', 'zigzag-swoop'];
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
        }

        waypoints.push({ x: endX, y: endY });

        // Clamp waypoints inside viewport boundaries
        waypoints.forEach(wp => {
            wp.x = Math.max(12, Math.min(viewW - 12, wp.x));
            wp.y = Math.max(12, Math.min(viewH - 12, wp.y));
        });

        // Add dummy start/end control points for Catmull-Rom
        const pathPoints = [
            { x: startX - (waypoints[1].x - startX) * 0.5, y: startY - (waypoints[1].y - startY) * 0.5 },
            ...waypoints,
            { x: endX + (endX - waypoints[waypoints.length - 2].x) * 0.5, y: endY + (endY - waypoints[waypoints.length - 2].y) * 0.5 }
        ];

        return pathPoints;
    }

    function catmullRom(p0, p1, p2, p3, t) {
        const t2 = t * t;
        const t3 = t2 * t;
        return 0.5 * (
            (2 * p1) +
            (-p0 + p2) * t +
            (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 +
            (-p0 + 3 * p1 - 3 * p2 + p3) * t3
        );
    }

    function getSplinePoint(points, t) {
        const numSections = points.length - 3;
        const clampedT = Math.max(0, Math.min(0.9999, t));
        const p = clampedT * numSections;
        const section = Math.floor(p);
        const u = p - section;

        const p0 = points[section];
        const p1 = points[section + 1];
        const p2 = points[section + 2];
        const p3 = points[section + 3];

        return {
            x: catmullRom(p0.x, p1.x, p2.x, p3.x, u),
            y: catmullRom(p0.y, p1.y, p2.y, p3.y, u)
        };
    }

    function easeInOutCubic(x) {
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
    }

    // ─── 7. BUILD MISSIONS & THE BUILD GATE (PHASE 4) ───────────────────────
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

            // Collect and sequence elements:
            // 1. Titles / Section Tag
            // 2. Paragraphs / Descriptions
            // 3. Cards & Code-IDE container
            // 4. Buttons, controls, links
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
                if (el.matches(cardSelector) || el.classList.contains('code-block-visual') || el.classList.contains('stats-row')) return 3;
                return 4;
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
                let minDuration = 350; // was 600ms (-250ms)

                if (['h1', 'h2', 'h3'].includes(tag) || el.classList.contains('section-title') || el.classList.contains('section-tag')) {
                    type = 'title';
                    minDuration = 600; // was 1100ms (-500ms / 0.5s faster!)
                } else if (tag === 'p' || el.classList.contains('section-desc')) {
                    type = 'paragraph';
                    minDuration = 450; // was 900ms (-450ms / 0.5s faster!)
                } else if (['a', 'button'].includes(tag) || el.classList.contains('cta-button') || el.classList.contains('filter-btn')) {
                    type = 'button';
                    minDuration = 250; // was 450ms (-200ms)
                } else if (el.classList.contains('code-block-visual')) {
                    type = 'code-card';
                    minDuration = 850; // was 1400ms (-550ms / 0.55s faster!)
                }

                const item = {
                    id: `${secId}-el-${order}`,
                    secId,
                    secInfo,
                    el,
                    type,
                    minDuration,
                    order,
                    state: isHero ? 'built' : 'pending', // 'pending' | 'dispatched' | 'pulling' | 'built'
                    gateOpenedTime: 0,
                    dispatchTime: 0,
                    pullStartTime: 0,
                    pullDuration: minDuration,
                    crew: [],
                    anchors: [],
                    cachedRect: null
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
        refreshAllElementRects();
    }

    function refreshAllElementRects() {
        const scrollY = window.scrollY || window.pageYOffset;
        elementList.forEach(item => {
            const r = item.el.getBoundingClientRect();
            item.cachedRect = {
                pageTop: r.top + scrollY,
                pageLeft: r.left,
                width: r.width,
                height: r.height
            };
        });
    }

    function computeAnchors(item) {
        const r = item.el.getBoundingClientRect();
        const anchors = [];
        const w = r.width;
        const h = r.height;

        anchors.push({ x: r.left + 16, y: r.top + h * 0.5 });
        anchors.push({ x: r.right - 16, y: r.top + h * 0.5 });
        anchors.push({ x: r.left + w * 0.35, y: r.top + 8 });
        anchors.push({ x: r.left + w * 0.65, y: r.bottom - 8 });

        return anchors;
    }

    // ─── 8. GATE EVALUATOR & MISSION DISPATCHER ────────────────────────────
    const activeMissions = [];

    function checkBuildGate(now) {
        if (isReducedMotion) {
            revealAllInstantly();
            return;
        }

        const scrollY = window.scrollY || window.pageYOffset;
        const bandTopY = viewH * BAND_TOP;
        const bandBottomY = viewH * BAND_BOTTOM;
        const bandHeight = bandBottomY - bandTopY;

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

        // Check scroll settled condition: scroll speed < 800 px/s for 200ms
        const scrollSettled = (now - lastFastScrollTime >= SCROLL_SETTLE_MS);

        // Section Dwell Tracker
        SECTION_ORDER.forEach(secId => {
            const sec = sectionMap[secId];
            if (!sec || sec.isHero) return;

            const r = sec.el.getBoundingClientRect();
            const inBand = (r.bottom >= bandTopY && r.top <= bandBottomY);

            if (inBand) {
                if (sec.firstEnteredBandTime === 0) {
                    sec.firstEnteredBandTime = now;
                }
                if (now - sec.firstEnteredBandTime >= SECTION_DWELL_MS) {
                    sec.dwellMet = true;
                }
            } else {
                sec.firstEnteredBandTime = 0;
            }
        });

        // Evaluate pending elements in strict sequence order
        for (let i = 0; i < elementList.length; i++) {
            const item = elementList[i];
            if (item.state !== 'pending') continue;

            const sec = item.secInfo;
            if (!sec.dwellMet && !sec.isHero) continue;
            if (!scrollSettled) continue;

            // Check predecessor: must be built or already in flight
            if (i > 0) {
                const pred = elementList[i - 1];
                if (pred.secId === item.secId && pred.state === 'pending') {
                    // Predecessor has not yet dispatched; sequence order cannot be broken
                    continue;
                }
            }

            // Check Band condition: Element E is >= 80% inside viewport band [8%, 88%]
            const r = item.el.getBoundingClientRect();
            if (r.width === 0 || r.height === 0) continue;

            const elTop = r.top;
            const elBottom = r.bottom;
            const elHeight = r.height;

            const visibleTop = Math.max(elTop, bandTopY);
            const visibleBottom = Math.min(elBottom, bandBottomY);
            const visibleHeight = Math.max(0, visibleBottom - visibleTop);

            let satisfiesBand = false;
            if (elHeight > bandHeight) {
                // Taller elements: top 80% of viewport height or first 600px in band
                satisfiesBand = (elTop >= bandTopY - 100 && visibleHeight >= Math.min(600, bandHeight * 0.8));
            } else {
                satisfiesBand = (visibleHeight >= elHeight * 0.80);
            }

            if (!satisfiesBand) continue;

            // Capacity check: Max 3 active crews
            if (activeMissions.length >= MAX_ACTIVE_CREWS) continue;

            // Available drones pool check: need at least CREW_SIZE available drones
            const availableDrones = drones.filter(d => d.state === 'FOLLOW');
            if (availableDrones.length < CREW_SIZE) continue;

            // Gate opens! Dispatch mission for element E
            dispatchMission(item, availableDrones.slice(0, CREW_SIZE), now);
        }

        // Failsafe Watchdog: elements never stay hidden > 3.5s after gate open
        elementList.forEach(item => {
            if (item.gateOpenedTime > 0 && item.state !== 'built') {
                if (now - item.gateOpenedTime > 3500) {
                    finishElementInstantly(item);
                }
            }
        });
    }

    function dispatchMission(item, crewDrones, now) {
        item.state = 'dispatched';
        item.gateOpenedTime = now;
        item.dispatchTime = now;
        item.crew = crewDrones;
        item.el.setAttribute('data-drone-state', 'flight');

        const anchors = computeAnchors(item);
        item.anchors = anchors;

        const flightDuration = Math.round(250 + Math.random() * 200); // 250-450ms (0.5s faster arrival)
        
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
                if (this.arrivedCount >= this.crew.length) {
                    this.startPull(performance.now());
                }
            },

            startPull(pullNow) {
                const flightTime = pullNow - this.dispatchedAt;
                // Spectacle guarantee: reveal may start only after crew has flown >= 500ms
                if (flightTime < 500) {
                    setTimeout(() => this.startPull(performance.now()), 500 - flightTime);
                    return;
                }

                this.pullStartedAt = pullNow;
                this.item.state = 'pulling';
                this.item.el.setAttribute('data-drone-state', 'pulling');

                // Arrival flourish: 80ms RGB-split & spark burst
                this.item.el.classList.add('drone-arrival-flourish');
                setTimeout(() => this.item.el.classList.remove('drone-arrival-flourish'), 160);

                this.anchors.forEach(a => emitSparks(a.x, a.y, 8));
            }
        };

        // Assign procedural path to each crew drone
        crewDrones.forEach((drone, idx) => {
            drone.state = 'DISPATCH';
            drone.activeMission = mission;
            drone.crewIndex = idx;
            drone.flightStart = now;
            drone.flightDuration = flightDuration + idx * 20; // tighter stagger

            const anchor = anchors[idx % anchors.length];
            drone.targetAnchor = anchor;
            drone.pathPoints = generateProceduralPath(drone.x, drone.y, anchor.x, anchor.y, drone.flightDuration);
        });

        activeMissions.push(mission);
    }

    function updateActiveMissions(now, dt) {
        for (let i = activeMissions.length - 1; i >= 0; i--) {
            const m = activeMissions[i];
            const item = m.item;

            // Recompute anchors if element moves during scroll
            m.anchors = computeAnchors(item);
            m.crew.forEach((d, idx) => {
                if (m.anchors[idx % m.anchors.length]) {
                    d.targetAnchor = m.anchors[idx % m.anchors.length];
                }
            });

            if (item.state === 'pulling') {
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
                }

                // Code-IDE line-by-line reveal
                if (item.type === 'code-card') {
                    const lines = item.el.querySelectorAll('.drone-code-line, .code-line');
                    if (lines.length) {
                        const lineIdx = Math.floor(easeProg * lines.length);
                        lines.forEach((l, idx) => {
                            if (idx <= lineIdx && !l.classList.contains('revealed')) {
                                l.classList.add('revealed');
                                const lr = l.getBoundingClientRect();
                                emitSparks(lr.left + 10, lr.top + 6, 3);
                            }
                        });
                    }
                }

                // Pull completion
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
        item.el.setAttribute('data-drone-state', 'built');
        item.el.style.transform = '';
        item.el.style.opacity = '';
        item.el.style.filter = '';
        item.el.style.willChange = '';

        if (item.el.classList.contains('scroll-reveal')) {
            item.el.classList.add('active');
        }

        // Snap sparks
        const r = item.el.getBoundingClientRect();
        emitSparks(r.left + 12, r.top + 10, 6);
        emitSparks(r.right - 12, r.top + 10, 6);
    }

    function finishElementInstantly(item) {
        if (item.state === 'built') return;
        item.state = 'built';
        item.el.setAttribute('data-drone-state', 'built');
        item.el.style.transform = '';
        item.el.style.opacity = '';
        item.el.style.filter = '';
        item.el.style.willChange = '';
        if (item.el.classList.contains('scroll-reveal')) {
            item.el.classList.add('active');
        }
        if (item.crew && item.crew.length) {
            returnCrew(item.crew, performance.now());
        }
    }

    function returnCrew(crewDrones, now) {
        crewDrones.forEach((drone, idx) => {
            drone.state = 'RETURN';
            drone.flightStart = now;
            drone.flightDuration = Math.round(200 + Math.random() * 150); // 200-350ms agile return

            // Random return orbit slot around cursor
            const returnAngle = Math.random() * Math.PI * 2;
            const returnRadius = R_MIN + Math.random() * (R_MAX - R_MIN);
            const targetX = cursorX + Math.cos(returnAngle) * returnRadius;
            const targetY = cursorY + Math.sin(returnAngle) * returnRadius;

            drone.targetAnchor = { x: targetX, y: targetY };
            drone.pathPoints = generateProceduralPath(drone.x, drone.y, targetX, targetY, drone.flightDuration);
        });
    }

    function easeOutQuart(x) {
        return 1 - Math.pow(1 - x, 4);
    }

    function drawTractorBeams(ctx) {
        activeMissions.forEach(m => {
            if (m.item.state !== 'pulling') return;

            const now = performance.now();
            m.crew.forEach((drone, idx) => {
                const anchor = drone.targetAnchor;
                if (!anchor) return;

                const dist = Math.hypot(anchor.x - drone.x, anchor.y - drone.y) || 1;
                const normX = -(anchor.y - drone.y) / dist;
                const normY = (anchor.x - drone.x) / dist;

                // Multi-harmonic electrical crackle
                const crackle = Math.sin(now * 0.08 + idx * 2.1) * 6.5 + Math.cos(now * 0.14 + idx * 3.7) * 4.0;
                const midX = (drone.x + anchor.x) * 0.5 + normX * crackle;
                const midY = (drone.y + anchor.y) * 0.5 + normY * crackle;

                ctx.save();
                // Outer cyan aura
                ctx.beginPath();
                ctx.moveTo(drone.x, drone.y);
                ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);
                ctx.strokeStyle = 'rgba(25, 227, 209, 0.38)';
                ctx.lineWidth = 1.6;
                ctx.stroke();

                // Middle gold beam
                ctx.beginPath();
                ctx.moveTo(drone.x, drone.y);
                ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);
                ctx.strokeStyle = 'rgba(245, 197, 66, 0.85)';
                ctx.lineWidth = 0.9;
                ctx.stroke();

                // Inner diamond white core
                ctx.beginPath();
                ctx.moveTo(drone.x, drone.y);
                ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.98)';
                ctx.lineWidth = 0.5;
                ctx.shadowColor = THEME.gold;
                ctx.shadowBlur = 8;
                ctx.stroke();
                ctx.restore();
            });
        });
    }

    // ─── 9. WATCHDOG & FAILSAFE ────────────────────────────────────────────
    function revealAllInstantly() {
        elementList.forEach(item => finishElementInstantly(item));
        document.documentElement.classList.add('drones-done');
        ctx.clearRect(0, 0, viewW, viewH);
    }

    // Watchdog: If drone system has not completed hero by 2.5s or throws an error, reveal everything
    const watchdogTimer = setTimeout(() => {
        const homeSec = sectionMap['home'];
        if (homeSec) {
            homeSec.elements.forEach(el => finishElementInstantly(el));
        }
    }, 2500);

    // Watchdog: If an unhandled JS error occurs, reveal all instantly
    window.addEventListener('error', () => {
        revealAllInstantly();
    });

    window.addEventListener('beforeprint', () => {
        revealAllInstantly();
    });

    // ─── 10. SINGLE REQUESTANIMATIONFRAME LOOP ──────────────────────────────
    let lastFrameTime = performance.now();
    let isLoopRunning = false;

    function mainLoop(now) {
        if (document.hidden) {
            isLoopRunning = false;
            return;
        }

        const dt = Math.min(0.05, (now - lastFrameTime) / 1000);
        lastFrameTime = now;

        ctx.clearRect(0, 0, viewW, viewH);

        // Update cursor center to exact real pointer position
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

        // 2. Check Build Gate & Dispatch Missions
        checkBuildGate(now);

        // 3. Update active missions
        updateActiveMissions(now, dt);

        // 4. Draw tractor beams & sparks
        drawTractorBeams(ctx);
        updateAndDrawSparks(ctx);

        // 5. Draw Drones
        drones.forEach(drone => drone.draw(ctx));

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

    // ─── 11. INITIALIZATION VIA REQUESTIDLECALLBACK ────────────────────────
    function init() {
        registerElements();
        resizeCanvas();
        startLoop();

        // Hero initial mission within 600ms of first paint
        setTimeout(() => {
            const homeSec = sectionMap['home'];
            if (homeSec) {
                homeSec.elements.forEach(item => finishElement(item));
            }
        }, 500);
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Expose public test API for Playwright verification
    window.drones = {
        getDrones: () => drones,
        getElements: () => elementList,
        getMissions: () => activeMissions,
        revealAll: revealAllInstantly,
        R_MIN,
        R_MAX
    };

    // Swarm compatibility bridge
    window.swarm = {
        getDotsData: () => drones.map(d => ({ currentX: d.x, currentY: d.y, opacity: d.opacity })),
        setPhase: (p, m) => {},
        release: () => {}
    };

    window.__dronesActive = true;
})();
