/**
 * PULL-BUILD SCROLL MODULE [C-01 ... C-07, PF-01 ... PF-12]
 * Framework-agnostic vanilla JS module.
 * Manages section ghost blueprints, swarm crew dispatch, glowing tethers,
 * mechanical pull-to-build scroll reveals, and snap sparks.
 */
(function () {
    'use strict';

    // ─── 1. Feature Detection & Failsafe [PF-11, 4.2] ───────────────────────
    if (
        typeof window === 'undefined' ||
        !window.IntersectionObserver ||
        !window.ResizeObserver ||
        !window.requestAnimationFrame ||
        !document.createElement('canvas').getContext
    ) {
        return; // Failsafe: exit, everything remains visible
    }

    const docEl = document.documentElement;
    const isReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    // Failsafe timeout: 3 seconds to guarantee content visibility [4.2]
    const failsafeTimer = setTimeout(() => {
        if (!docEl.classList.contains('nb-done')) {
            console.warn('[Pull-Build] Failsafe timer reached. Revealing all content.');
            docEl.classList.remove('nb-ready');
            docEl.classList.add('nb-done');
            revealAllInstantly();
        }
    }, 3000);

    function revealAllInstantly() {
        document.querySelectorAll('[data-nb]').forEach(el => {
            el.setAttribute('data-nb', 'built');
            el.style.opacity = '';
            el.style.transform = '';
            el.style.willChange = '';
            if (el.classList.contains('scroll-reveal')) el.classList.add('active');
            el.querySelectorAll('.scroll-reveal').forEach(child => child.classList.add('active'));
        });
        if (typeof window.animateCounters === 'function') {
            window.animateCounters();
        }
        if (window.swarm && typeof window.swarm.release === 'function') {
            window.swarm.release();
        }
    }

    // ─── 2. Audited DOM Sections in Strict Page Order [Fact 1, 4.1] ────────
    const SECTION_IDS = [
        'home',
        'profile-expertise',
        'about-me',
        'projects',
        'creative-lab',
        'certificates',
        'secret-desk',
        'contact'
    ];

    // ─── 3. Section Data & State Tracking ──────────────────────────────────
    const sections = [];
    let sectionMap = {};

    function updateCachedRects() {
        if (!sections.length) return;
        const scrollY = window.scrollY || window.pageYOffset;
        sections.forEach(item => {
            const r = item.el.getBoundingClientRect();
            item.pageTop = r.top + scrollY;
            item.pageLeft = r.left;
            item.width = r.width;
            item.height = r.height;
        });
    }

    // ─── 4. Canvas Setup [PF-01, PF-03] ────────────────────────────────────
    let canvas = document.getElementById('nb-canvas');
    if (!canvas) {
        canvas = document.createElement('canvas');
        canvas.id = 'nb-canvas';
        canvas.setAttribute('aria-hidden', 'true');
        document.body.insertBefore(canvas, document.body.firstChild);
    }

    const ctx = canvas.getContext('2d');
    let viewW = window.innerWidth;
    let viewH = window.innerHeight;
    const dpr = Math.min(window.devicePixelRatio || 1, 1.5);

    function resizeCanvas() {
        viewW = window.innerWidth;
        viewH = window.innerHeight;
        canvas.width = Math.round(viewW * dpr);
        canvas.height = Math.round(viewH * dpr);
        ctx.setTransform(1, 0, 0, 1, 0, 0);
        ctx.scale(dpr, dpr);
        updateCachedRects();
    }

    function debounce(fn, wait) {
        let t;
        return function () {
            clearTimeout(t);
            t = setTimeout(fn, wait);
        };
    }

    window.addEventListener('resize', debounce(resizeCanvas, 150), { passive: true });
    resizeCanvas();

    function initSections() {
        SECTION_IDS.forEach((id, index) => {
            const el = document.getElementById(id);
            if (!el) return;

            // Ensure section has positioning context for rim flash
            if (!el.classList.contains('nb-section-wrap')) {
                el.classList.add('nb-section-wrap');
            }

            const isHero = (id === 'home');
            const item = {
                id,
                el,
                index,
                isHero,
                state: 'pending', // 'pending' | 'dispatch' | 'pulling' | 'snapping' | 'built'
                pageTop: 0,
                pageLeft: 0,
                width: 0,
                height: 0,
                startTime: 0,
                duration: 1400,
                animProgress: 0
            };

            if (isReducedMotion) {
                item.state = 'built';
                el.setAttribute('data-nb', 'built');
            } else {
                el.setAttribute('data-nb', 'pending');
            }

            sections.push(item);
            sectionMap[id] = item;
        });

        updateCachedRects();
    }

    // ─── 5. Reduced Motion Guard [PF-10] ───────────────────────────────────
    if (isReducedMotion) {
        clearTimeout(failsafeTimer);
        docEl.classList.add('nb-done');
        initSections();
        revealAllInstantly();
        return;
    }

    // Initialize pending states and activate module
    initSections();
    docEl.classList.add('nb-ready');
    clearTimeout(failsafeTimer);

    // ─── 6. Spark Particles Pool [Phase 5 SNAP, PF-01, PF-03] ──────────────
    const sparks = [];
    function emitSparks(x, y, count = 10) {
        for (let i = 0; i < count; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = 1.5 + Math.random() * 3.5;
            sparks.push({
                x,
                y,
                vx: Math.cos(angle) * speed,
                vy: Math.sin(angle) * speed - 1.0,
                life: 1.0,
                decay: 0.03 + Math.random() * 0.04,
                size: 2 + Math.random() * 2
            });
        }
    }

    // ─── 7. Pull Queue & Scheduling [C-01 ... C-06] ────────────────────────
    let currentPullingItem = null;
    let pullQueue = [];
    let isLoopRunning = false;

    // Cubic-bezier(0.16, 1, 0.3, 1) approximation
    function easeOutQuint(x) {
        return 1 - Math.pow(1 - x, 4);
    }

    function getInnerBoxes(item, currentYOffset) {
        const scrollY = window.scrollY || window.pageYOffset;
        // Targets both card containers AND individual text headings/paragraphs [Section 4]
        const selectors = [
            'h1, h2, h3, h4, .section-title, .section-header, .card-title, .onboard-title',
            '.section-desc, p, .about-bio, .stat-desc, .project-details p, .timeline-text, .hero-tagline',
            '.project-card, .cert-card, .expertise-card, .onboard-card, .stat-item, .contact-card, .glass-card',
            '.hero-traits-list, .filter-buttons, .tech-badges'
        ].join(', ');

        const rawEls = Array.from(item.el.querySelectorAll(selectors));
        const validBoxes = [];

        rawEls.forEach(el => {
            const r = el.getBoundingClientRect();
            // Filter elements that have actual layout dimensions
            if (r.width > 28 && r.height > 14) {
                const tag = el.tagName.toLowerCase();
                const isText = ['h1', 'h2', 'h3', 'h4', 'p', 'span'].includes(tag) || el.classList.contains('section-desc') || el.classList.contains('section-title');
                validBoxes.push({
                    el,
                    isText,
                    x: r.left,
                    y: r.top + currentYOffset,
                    w: r.width,
                    h: r.height
                });
            }
        });

        // Select up to 6 prominent elements (headings, text paragraphs, and cards)
        return validBoxes.slice(0, 6);
    }

    function computeAnchorPoints(item, currentYOffset) {
        const scrollY = window.scrollY || window.pageYOffset;
        const screenTop = item.pageTop - scrollY + currentYOffset;
        const screenLeft = item.pageLeft;
        const w = item.width;
        const h = item.height;

        const boxes = getInnerBoxes(item, currentYOffset);
        const anchors = [];

        if (boxes.length >= 4) {
            // 4 boxes: 2 drones per box
            boxes.forEach(b => {
                anchors.push({ x: b.x + 10, y: b.y + 10 });
                anchors.push({ x: b.x + b.w - 10, y: b.y + 10 });
            });
        } else if (boxes.length === 3) {
            // 3 boxes: 3 on box 1, 3 on box 2, 2 on box 3
            anchors.push({ x: boxes[0].x, y: boxes[0].y });
            anchors.push({ x: boxes[0].x + boxes[0].w, y: boxes[0].y });
            anchors.push({ x: boxes[0].x + boxes[0].w * 0.5, y: boxes[0].y + boxes[0].h });

            anchors.push({ x: boxes[1].x, y: boxes[1].y });
            anchors.push({ x: boxes[1].x + boxes[1].w, y: boxes[1].y });
            anchors.push({ x: boxes[1].x + boxes[1].w * 0.5, y: boxes[1].y + boxes[1].h });

            anchors.push({ x: boxes[2].x, y: boxes[2].y });
            anchors.push({ x: boxes[2].x + boxes[2].w, y: boxes[2].y });
        } else if (boxes.length === 2) {
            // 2 boxes: 4 drones per box wrapping around each
            boxes.forEach(b => {
                anchors.push({ x: b.x, y: b.y });
                anchors.push({ x: b.x + b.w, y: b.y });
                anchors.push({ x: b.x + b.w, y: b.y + b.h });
                anchors.push({ x: b.x, y: b.y + b.h });
            });
        } else if (boxes.length === 1) {
            // 1 box: 8 drones encircling all 4 corners and midpoints
            const b = boxes[0];
            anchors.push({ x: b.x, y: b.y });
            anchors.push({ x: b.x + b.w * 0.5, y: b.y });
            anchors.push({ x: b.x + b.w, y: b.y });
            anchors.push({ x: b.x + b.w, y: b.y + b.h * 0.5 });
            anchors.push({ x: b.x + b.w, y: b.y + b.h });
            anchors.push({ x: b.x + b.w * 0.5, y: b.y + b.h });
            anchors.push({ x: b.x, y: b.y + b.h });
            anchors.push({ x: b.x, y: b.y + b.h * 0.5 });
        } else {
            // Fallback to outer section perimeter
            anchors.push(
                { x: screenLeft, y: screenTop },
                { x: screenLeft + w, y: screenTop },
                { x: screenLeft + w * 0.3, y: screenTop },
                { x: screenLeft + w * 0.7, y: screenTop },
                { x: screenLeft, y: screenTop + Math.min(100, h * 0.2) },
                { x: screenLeft + w, y: screenTop + Math.min(100, h * 0.2) },
                { x: screenLeft + w * 0.15, y: screenTop + 8 },
                { x: screenLeft + w * 0.85, y: screenTop + 8 }
            );
        }

        return anchors.slice(0, 8);
    }

    function startPull(item, fastMode = false) {
        if (!item || item.state === 'built') return;

        currentPullingItem = item;
        item.state = 'dispatch';
        item.startTime = performance.now();
        item.duration = fastMode ? 1150 : (item.isHero ? 1350 : 2100); // Cinematic slowed down pace (+0.75s)
        item.el.setAttribute('data-nb', 'pulling');
        item.el.style.willChange = 'transform, opacity'; // [PF-05]

        const maxOffset = Math.min(90, viewH * 0.10); // min(90px, 10vh) [PF-09]
        const targets = computeAnchorPoints(item, maxOffset);

        if (window.swarm && typeof window.swarm.assign === 'function') {
            window.swarm.assign(targets);
        }

        ensureLoop();
    }

    function finishPull(item) {
        item.state = 'built';
        item.el.setAttribute('data-nb', 'built');
        item.el.style.opacity = '';
        item.el.style.transform = '';
        item.el.style.willChange = ''; // [PF-05]

        // Snap sparks [Phase 5]
        const scrollY = window.scrollY || window.pageYOffset;
        const screenTop = item.pageTop - scrollY;
        emitSparks(item.pageLeft + 20, screenTop + 10, 8);
        emitSparks(item.pageLeft + item.width - 20, screenTop + 10, 8);

        // Stagger reveal children [4.2]
        if (item.el.classList.contains('scroll-reveal')) {
            item.el.classList.add('active');
        }
        if (item.id === 'about-me' && typeof window.animateCounters === 'function') {
            window.animateCounters();
        }
        const revealChildren = item.el.querySelectorAll('.scroll-reveal');
        revealChildren.forEach((child, idx) => {
            setTimeout(() => {
                child.classList.add('active');
            }, idx * 80);
        });

        // Release dots [Phase 6, 4.3]
        if (window.swarm && typeof window.swarm.release === 'function') {
            window.swarm.release();
        }

        currentPullingItem = null;

        // Check if all sections built [C-07]
        checkCompletion();

        // Process next item in queue [C-01]
        processNextInQueue();
    }

    function processNextInQueue() {
        if (currentPullingItem) return;

        // Find next pending section in strict DOM order [C-01]
        const next = sections.find(s => s.state === 'pending');
        if (!next) return;

        const scrollY = window.scrollY || window.pageYOffset;
        const triggerY = scrollY + viewH * 0.90; // Top crosses 85-90% viewport height [4.3]

        if (next.pageTop <= triggerY || next.isHero) {
            // Check if fast scrolling [C-02]
            const pendingInView = sections.filter(s => s.state === 'pending' && s.pageTop <= scrollY + viewH);
            const isFast = pendingInView.length > 1;
            startPull(next, isFast);
        }
    }

    function checkCompletion() {
        const allBuilt = sections.every(s => s.state === 'built');
        if (allBuilt) {
            docEl.classList.add('nb-done');
            docEl.classList.remove('nb-ready');
            ctx.clearRect(0, 0, viewW, viewH);
            if (observer) observer.disconnect();
        }
    }

    // ─── 8. IntersectionObserver for Section Triggering [4.2, C-01] ─────────
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const item = sectionMap[entry.target.id];
                if (item && item.state === 'pending') {
                    // Check Anchor Jump [C-03]: if section is already above viewport, build instantly
                    const scrollY = window.scrollY || window.pageYOffset;
                    if (item.pageTop + item.height < scrollY) {
                        item.state = 'built';
                        item.el.setAttribute('data-nb', 'built');
                        item.el.querySelectorAll('.scroll-reveal').forEach(c => c.classList.add('active'));
                        return;
                    }
                    processNextInQueue();
                }
            }
        });
    }, {
        threshold: 0.05,
        rootMargin: '100px 0px 50px 0px'
    });

    sections.forEach(item => {
        if (!item.isHero) {
            observer.observe(item.el);
        }
    });

    // Handle scroll for fast scrolling and queue triggering [C-02, C-03]
    window.addEventListener('scroll', () => {
        // Fast anchor jump check [C-03]
        const scrollY = window.scrollY || window.pageYOffset;
        sections.forEach(s => {
            if (s.state === 'pending' && s.pageTop + 50 < scrollY) {
                // Section was jumped past
                s.state = 'built';
                s.el.setAttribute('data-nb', 'built');
                if (s.el.classList.contains('scroll-reveal')) s.el.classList.add('active'); s.el.querySelectorAll('.scroll-reveal').forEach(c => c.classList.add('active')); if (s.id === 'about-me' && typeof window.animateCounters === 'function') window.animateCounters();
            }
        });

        processNextInQueue();
        ensureLoop();
    }, { passive: true });

    // ─── 9. Animation Frame Loop [PF-01, PF-04, PF-06] ─────────────────────
    function renderFrame(now) {
        ctx.clearRect(0, 0, viewW, viewH);

        const scrollY = window.scrollY || window.pageYOffset;
        let hasActiveDrawing = false;

        // 1. Draw Ghost Blueprints [Phase 1 GHOST, 4.3]
        if (!docEl.classList.contains('nb-done')) {
            sections.forEach(item => {
                if (item.state === 'pending' && !item.isHero) {
                    const screenTop = item.pageTop - scrollY;
                    // Draw if within ~1 viewport below
                    if (screenTop > -item.height && screenTop < viewH * 1.5) {
                        ctx.save();
                        ctx.strokeStyle = 'rgba(157, 77, 255, 0.25)'; // Faint dashed purple outline
                        ctx.lineWidth = 1;
                        ctx.setLineDash([5, 5]);
                        ctx.strokeRect(item.pageLeft + 8, screenTop + 8, item.width - 16, Math.min(item.height - 16, viewH * 0.9));
                        ctx.restore();
                        hasActiveDrawing = true;
                    }
                }
            });
        }

        // 2. Animate Active Pull [Phase 3 TETHER & Phase 4 PULL, 4.3]
        if (currentPullingItem) {
            hasActiveDrawing = true;
            const item = currentPullingItem;
            const elapsed = now - item.startTime;
            const totalDur = item.duration;
            const t = Math.min(1, elapsed / totalDur);

            const dispatchRatio = 0.25; // 25% dispatch, 65% pull, 10% snap
            const pullRatio = 0.90;
            const maxOffset = Math.min(90, viewH * 0.10);

            let currentOffset = maxOffset;
            let currentOpacity = 0;
            let currentScale = 0.92;

            if (t < dispatchRatio) {
                // Phase 2: Dispatch
                item.state = 'dispatch';
                currentOffset = maxOffset;
                currentOpacity = (t / dispatchRatio) * 0.4;
                currentScale = 0.92;
            } else if (t < pullRatio) {
                // Phase 4: Pull
                item.state = 'pulling';
                const pullT = (t - dispatchRatio) / (pullRatio - dispatchRatio);
                const eased = easeOutQuint(pullT);
                currentOffset = maxOffset * (1 - eased);
                currentOpacity = 0.4 + eased * 0.6;
                currentScale = 0.92 + eased * 0.08;
            } else {
                // Phase 5: Snap
                if (item.state !== 'snapping') {
                    item.state = 'snapping';
                    item.el.setAttribute('data-nb', 'snapping');
                }
                currentOffset = 0;
                currentOpacity = 1;
                currentScale = 1;
            }

            // Apply transform to section DOM element
            item.el.style.opacity = currentOpacity.toFixed(3);
            item.el.style.transform = `translate3d(0, ${currentOffset.toFixed(1)}px, 0) scale(${currentScale.toFixed(3)})`;

            // Update swarm anchor targets so dots move with the top edge
            const anchors = computeAnchorPoints(item, currentOffset);
            if (window.swarm && typeof window.swarm.assign === 'function') {
                window.swarm.assign(anchors);
            }

            // Draw inner box & text laser scan & weld line sweep [AU-04, Section 4]
            const innerBoxes = getInnerBoxes(item, currentOffset);
            if (t >= dispatchRatio && t < 0.95) {
                innerBoxes.forEach(b => {
                    ctx.save();
                    if (b.isText) {
                        // Cyberpunk corner reticles around text elements
                        const cornerLen = Math.min(12, b.w * 0.15);
                        ctx.strokeStyle = 'rgba(255, 216, 115, 0.75)'; // Neon Gold for text
                        ctx.lineWidth = 1.5;
                        
                        // Top-left
                        ctx.beginPath();
                        ctx.moveTo(b.x, b.y + cornerLen);
                        ctx.lineTo(b.x, b.y);
                        ctx.lineTo(b.x + cornerLen, b.y);
                        ctx.stroke();

                        // Top-right
                        ctx.beginPath();
                        ctx.moveTo(b.x + b.w - cornerLen, b.y);
                        ctx.lineTo(b.x + b.w, b.y);
                        ctx.lineTo(b.x + b.w, b.y + cornerLen);
                        ctx.stroke();

                        // Bottom-left
                        ctx.beginPath();
                        ctx.moveTo(b.x, b.y + b.h - cornerLen);
                        ctx.lineTo(b.x, b.y + b.h);
                        ctx.lineTo(b.x + cornerLen, b.y + b.h);
                        ctx.stroke();

                        // Bottom-right
                        ctx.beginPath();
                        ctx.moveTo(b.x + b.w - cornerLen, b.y + b.h);
                        ctx.lineTo(b.x + b.w, b.y + b.h);
                        ctx.lineTo(b.x + b.w, b.y + b.h - cornerLen);
                        ctx.stroke();
                    } else {
                        // Turquoise laser scan contour around cards
                        ctx.strokeStyle = 'rgba(25, 227, 208, 0.55)';
                        ctx.lineWidth = 1.5;
                        ctx.setLineDash([8, 6]);
                        ctx.strokeRect(b.x, b.y, b.w, b.h);
                    }

                    // Bright gold weld line sweep across box or text
                    const sweepProgress = Math.min(1.0, (t - dispatchRatio) / (pullRatio - dispatchRatio));
                    const sweepX = b.x + b.w * sweepProgress;
                    ctx.beginPath();
                    ctx.moveTo(sweepX, b.y - 2);
                    ctx.lineTo(sweepX, b.y + b.h + 2);
                    ctx.strokeStyle = 'rgba(255, 216, 115, 0.95)';
                    ctx.lineWidth = 2.5;
                    ctx.shadowColor = '#ffd873';
                    ctx.shadowBlur = 10;
                    ctx.stroke();
                    ctx.restore();
                });
            }

            // Draw glowing tethers between swarm dots and inner box anchors [Phase 3 TETHER]
            if (t >= dispatchRatio && t < 0.95 && window.swarm && typeof window.swarm.getDots === 'function') {
                const dots = window.swarm.getDots();
                const vibration = Math.sin(now * 0.035) * 1.5;

                for (let i = 0; i < Math.min(dots.length, anchors.length); i++) {
                    const dotRect = dots[i].getBoundingClientRect();
                    const dotX = dotRect.left + dotRect.width * 0.5;
                    const dotY = dotRect.top + dotRect.height * 0.5;
                    const anchor = anchors[i];

                    const midX = (dotX + anchor.x) * 0.5 + vibration;
                    const midY = (dotY + anchor.y) * 0.5;

                    ctx.save();
                    // Outer 3.5px violet beam
                    ctx.beginPath();
                    ctx.moveTo(dotX, dotY);
                    ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);
                    ctx.strokeStyle = 'rgba(157, 77, 255, 0.35)';
                    ctx.lineWidth = 3.5;
                    ctx.stroke();

                    // Middle 2px turquoise beam
                    ctx.beginPath();
                    ctx.moveTo(dotX, dotY);
                    ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);
                    ctx.strokeStyle = 'rgba(25, 227, 208, 0.55)';
                    ctx.lineWidth = 2;
                    ctx.stroke();

                    // Inner 1px bright gold core
                    ctx.beginPath();
                    ctx.moveTo(dotX, dotY);
                    ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);
                    ctx.strokeStyle = 'rgba(255, 216, 115, 0.95)';
                    ctx.lineWidth = 1;
                    ctx.stroke();
                    ctx.restore();
                }
            }

            if (t >= 1) {
                finishPull(item);
            }
        }

        // 3. Draw and update sparks [PF-01]
        if (sparks.length > 0) {
            hasActiveDrawing = true;
            for (let i = sparks.length - 1; i >= 0; i--) {
                const s = sparks[i];
                s.x += s.vx;
                s.y += s.vy;
                s.life -= s.decay;

                if (s.life <= 0) {
                    sparks.splice(i, 1);
                    continue;
                }

                ctx.save();
                ctx.fillStyle = `rgba(255, 216, 115, ${s.life.toFixed(2)})`;
                ctx.beginPath();
                ctx.arc(s.x, s.y, s.size * s.life, 0, Math.PI * 2);
                ctx.fill();
                ctx.restore();
            }
        }

        if (hasActiveDrawing) {
            requestAnimationFrame(renderFrame);
        } else {
            isLoopRunning = false;
        }
    }

    function ensureLoop() {
        if (!isLoopRunning && !docEl.classList.contains('nb-done')) {
            isLoopRunning = true;
            requestAnimationFrame(renderFrame);
        }
    }

    // ─── 10. Initial Hero Pull [4.5] ────────────────────────────────────────
    window.addEventListener('DOMContentLoaded', () => {
        const heroItem = sectionMap['home'];
        if (heroItem) {
            setTimeout(() => {
                startPull(heroItem, false);
            }, 100);
        }
    });

    // Pause on page hidden [PF-06]
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            isLoopRunning = false;
        } else {
            ensureLoop();
        }
    });

})();
