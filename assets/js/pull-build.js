/**
 * PULL-BUILD SCROLL & INTER-ELEMENT COORDINATION MODULE [C-01 ... C-07, PF-01 ... PF-12]
 * Framework-agnostic vanilla JS module.
 * 
 * Features:
 * - 3-Phase Interactive Choreography under 5 seconds (Target ~3.2s):
 *   Phase 1 (0.0s - 0.9s): Drones perform dynamic 3D reconnaissance spirals & sweeps across the empty space.
 *   Phase 2 (0.9s - 2.7s): Drones converge onto elements, tethers ignite, laser weld sweeps across text/cards, section hoists into view.
 *   Phase 3 (2.7s - 3.2s): Section snaps into place with gold rim flash, sparks emit, elements lock as assembled.
 * - Inter-Element State Coordinator: elements recognize drone proximity, ping each other, and ripple assembly.
 * - Queue Auto-Recovery: scrolling past a section immediately resolves it to built, clearing deadlocks instantly.
 * - Built sections stay built for smooth, reliable reading with zero visual desync.
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

    // Failsafe timeout: 4 seconds to guarantee content visibility [4.2]
    const failsafeTimer = setTimeout(() => {
        if (!docEl.classList.contains('nb-done')) {
            console.warn('[Pull-Build] Failsafe timer reached. Revealing all content.');
            docEl.classList.remove('nb-ready');
            docEl.classList.add('nb-done');
            revealAllInstantly();
        }
    }, 4000);

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

    // ─── 2. Inter-Element State Coordinator ────────────────────────────────
    const SectionCoordinator = {
        nodes: new Map(), // element -> { id, sectionId, el, state, isText, order }
        sectionStates: {}, // sectionId -> 'pending' | 'scouting' | 'pulling' | 'assembled'

        register(sectionId, el, isText = false, order = 0) {
            const id = el.id || `${sectionId}-node-${Math.random().toString(36).substr(2, 6)}`;
            const node = {
                id,
                sectionId,
                el,
                isText,
                state: 'unscouted',
                order
            };
            this.nodes.set(el, node);
            return node;
        },

        getNodesForSection(sectionId) {
            const list = [];
            this.nodes.forEach(n => {
                if (n.sectionId === sectionId) list.push(n);
            });
            return list.sort((a, b) => a.order - b.order);
        },

        checkProximity(dronePoints, sectionId) {
            if (!dronePoints || !dronePoints.length) return;
            const nodes = this.getNodesForSection(sectionId);
            nodes.forEach(n => {
                if (n.state !== 'unscouted') return;
                const r = n.el.getBoundingClientRect();
                const cx = r.left + r.width * 0.5;
                const cy = r.top + r.height * 0.5;
                
                for (let i = 0; i < dronePoints.length; i++) {
                    const dp = dronePoints[i];
                    const dx = dp.currentX - cx;
                    const dy = dp.currentY - cy;
                    if (dx * dx + dy * dy < 14400) { // Within 120px
                        n.state = 'scouted';
                        n.el.classList.add('drone-scouted');
                        break;
                    }
                }
            });
        },

        markAssembled(node) {
            if (node.state !== 'assembled') {
                node.state = 'assembled';
                node.el.classList.remove('drone-scouted');
                node.el.setAttribute('data-assembled', 'true');
                node.el.classList.add('cyber-ping');
                setTimeout(() => node.el.classList.remove('cyber-ping'), 600);
            }
        },

        assembleAll(sectionId) {
            this.getNodesForSection(sectionId).forEach(n => this.markAssembled(n));
            this.sectionStates[sectionId] = 'assembled';
        }
    };
    window.SectionCoordinator = SectionCoordinator;

    // ─── 3. Audited DOM Sections in Strict Page Order ──────────────────────
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

    // ─── 4. Section Data & State Tracking ──────────────────────────────────
    const sections = [];
    const sectionMap = {};

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

    // ─── 5. Canvas Setup ───────────────────────────────────────────────────
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

            if (!el.classList.contains('nb-section-wrap')) {
                el.classList.add('nb-section-wrap');
            }

            const isHero = (id === 'home');
            const item = {
                id,
                el,
                index,
                isHero,
                state: 'pending', // 'pending' | 'scouting' | 'pulling' | 'snapping' | 'built'
                pageTop: 0,
                pageLeft: 0,
                width: 0,
                height: 0,
                startTime: 0,
                duration: 3200, // Interactive visible pace under 5s
                animProgress: 0
            };

            // Register inner text blocks and cards into the coordinator
            const selectors = [
                'h1, h2, h3, h4, .section-title, .section-header, .card-title, .section-tag',
                '.section-desc, p, .about-text p, .trait-tag, .stat-label, .badge',
                '.project-card, .cert-card, .expertise-card, .stat-card, .glass-card',
                '.hero-traits-list, .filter-btn, .cta-button, .message-btn, .dock-btn, .cyber-dock-bar'
            ].join(', ');

            const childNodes = Array.from(el.querySelectorAll(selectors));
            childNodes.forEach((childEl, order) => {
                const tag = childEl.tagName.toLowerCase();
                const isText = ['h1', 'h2', 'h3', 'h4', 'p', 'span', 'a', 'button'].includes(tag);
                SectionCoordinator.register(id, childEl, isText, order);
            });

            if (isReducedMotion || isHero) {
                item.state = 'built';
                el.setAttribute('data-nb', 'built');
                SectionCoordinator.assembleAll(id);
            } else {
                el.setAttribute('data-nb', 'pending');
            }

            sections.push(item);
            sectionMap[id] = item;
        });

        updateCachedRects();
    }

    // ─── 6. Reduced Motion Guard ───────────────────────────────────────────
    if (isReducedMotion) {
        clearTimeout(failsafeTimer);
        docEl.classList.add('nb-done');
        initSections();
        revealAllInstantly();
        return;
    }

    initSections();
    docEl.classList.add('nb-ready');
    clearTimeout(failsafeTimer);

    // ─── 7. Spark Particles Pool ───────────────────────────────────────────
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

    // ─── 8. Pull Queue & Scheduling ────────────────────────────────────────
    let currentPullingItem = null;
    let isLoopRunning = false;

    function easeOutQuint(x) {
        return 1 - Math.pow(1 - x, 4);
    }

    function getInnerBoxes(item, currentYOffset) {
        const selectors = [
            'h1, h2, h3, h4, .section-title, .section-header, .card-title, .section-tag',
            '.section-desc, p, .about-text p, .trait-tag, .stat-label, .badge',
            '.project-card, .cert-card, .expertise-card, .stat-card, .glass-card',
            '.hero-traits-list, .filter-btn, .cta-button, .message-btn, .project-details'
        ].join(', ');

        const rawEls = Array.from(item.el.querySelectorAll(selectors));
        const validBoxes = [];

        rawEls.forEach(el => {
            const r = el.getBoundingClientRect();
            if (r.width > 20 && r.height > 12) {
                const tag = el.tagName.toLowerCase();
                const isText = ['h1', 'h2', 'h3', 'h4', 'p', 'span', 'a', 'button'].includes(tag) || 
                               el.classList.contains('section-desc') || 
                               el.classList.contains('section-title') ||
                               el.classList.contains('section-tag') ||
                               el.classList.contains('trait-tag') ||
                               el.classList.contains('stat-label');
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

        return validBoxes.slice(0, 16);
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
            boxes.forEach(b => {
                anchors.push({ x: b.x + 12, y: b.y + 10 });
                anchors.push({ x: b.x + b.w - 12, y: b.y + 10 });
            });
        } else if (boxes.length === 3) {
            anchors.push({ x: boxes[0].x, y: boxes[0].y });
            anchors.push({ x: boxes[0].x + boxes[0].w, y: boxes[0].y });
            anchors.push({ x: boxes[0].x + boxes[0].w * 0.5, y: boxes[0].y + boxes[0].h });

            anchors.push({ x: boxes[1].x, y: boxes[1].y });
            anchors.push({ x: boxes[1].x + boxes[1].w, y: boxes[1].y });
            anchors.push({ x: boxes[1].x + boxes[1].w * 0.5, y: boxes[1].y + boxes[1].h });

            anchors.push({ x: boxes[2].x, y: boxes[2].y });
            anchors.push({ x: boxes[2].x + boxes[2].w, y: boxes[2].y });
        } else if (boxes.length === 2) {
            boxes.forEach(b => {
                anchors.push({ x: b.x, y: b.y });
                anchors.push({ x: b.x + b.w, y: b.y });
                anchors.push({ x: b.x + b.w, y: b.y + b.h });
                anchors.push({ x: b.x, y: b.y + b.h });
            });
        } else if (boxes.length === 1) {
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
        if (!item || item.state === 'scouting' || item.state === 'pulling' || item.state === 'snapping' || item.state === 'built') return;

        currentPullingItem = item;
        item.state = 'scouting';
        item.startTime = performance.now();
        // Snappy, energetic pull-build under 1.5 seconds (~1.05s total)
        item.duration = fastMode ? 450 : 1050;
        item.el.setAttribute('data-nb', 'pulling');
        item.el.style.willChange = 'transform, opacity';

        // Notify swarm to initiate Phase 1: Reconnaissance
        if (window.swarm && typeof window.swarm.setPhase === 'function') {
            window.swarm.setPhase('scout', { bounds: item });
        }

        ensureLoop();
    }

    function finishPull(item, instant = false) {
        if (!item || item.state === 'built') return;

        item.state = 'built';
        item.el.setAttribute('data-nb', 'built');
        item.el.style.opacity = '';
        item.el.style.transform = '';
        item.el.style.willChange = '';

        // Mark all inner elements as assembled in coordinator and clear inline styles
        const nodes = SectionCoordinator.getNodesForSection(item.id);
        nodes.forEach(n => {
            SectionCoordinator.markAssembled(n);
            n.el.style.transform = '';
            n.el.style.opacity = '';
            n.el.style.filter = '';
        });
        SectionCoordinator.assembleAll(item.id);

        if (!instant) {
            // Snap sparks
            const scrollY = window.scrollY || window.pageYOffset;
            const screenTop = item.pageTop - scrollY;
            emitSparks(item.pageLeft + 20, screenTop + 10, 10);
            emitSparks(item.pageLeft + item.width - 20, screenTop + 10, 10);

            // Stagger reveal children
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
                }, idx * 75);
            });
        } else {
            // Instant reveal
            if (item.el.classList.contains('scroll-reveal')) {
                item.el.classList.add('active');
            }
            item.el.querySelectorAll('.scroll-reveal').forEach(c => c.classList.add('active'));
            if (item.id === 'about-me' && typeof window.animateCounters === 'function') {
                window.animateCounters();
            }
        }

        // Release dots
        if (window.swarm && typeof window.swarm.release === 'function') {
            window.swarm.release();
        }

        if (currentPullingItem === item) {
            currentPullingItem = null;
        }

        checkCompletion();
        processNextInQueue();
    }

    function processNextInQueue() {
        const scrollY = window.scrollY || window.pageYOffset;

        // Auto-recovery: if currentPullingItem is completely scrolled offscreen, finish it instantly
        if (currentPullingItem) {
            const r = currentPullingItem.el.getBoundingClientRect();
            const isOffscreen = (r.bottom < -60) || (r.top > viewH + 200);
            if (isOffscreen) {
                finishPull(currentPullingItem, true);
                currentPullingItem = null;
            } else {
                return; // Currently pulling a visible item
            }
        }

        // Check which pending section is currently entering or within the viewport
        let targetSection = null;

        for (let i = 0; i < sections.length; i++) {
            const s = sections[i];
            if (s.state === 'pending' && !s.isHero) {
                const r = s.el.getBoundingClientRect();
                // Visible in comfortable viewport reading window
                if (r.top < viewH * 0.85 && r.bottom > viewH * 0.15) {
                    targetSection = s;
                    break;
                }
            }
        }

        // Fallback: pick next pending section entering lower edge
        if (!targetSection) {
            for (let i = 0; i < sections.length; i++) {
                const s = sections[i];
                if (s.state === 'pending' && !s.isHero) {
                    const r = s.el.getBoundingClientRect();
                    if (r.top < viewH * 0.95 && r.bottom > 0) {
                        targetSection = s;
                        break;
                    }
                }
            }
        }

        if (targetSection) {
            startPull(targetSection, false);
        }
    }

    function checkCompletion() {
        const allBuilt = sections.every(s => s.state === 'built');
        if (allBuilt) {
            ctx.clearRect(0, 0, viewW, viewH);
        }
    }

    // ─── 9. IntersectionObserver with Deadlock Protection ──────────────────
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            const item = sectionMap[entry.target.id];
            if (!item || item.isHero) return;

            if (entry.isIntersecting) {
                if (item.state === 'pending') {
                    processNextInQueue();
                }
            }
        });
    }, {
        threshold: 0.08,
        rootMargin: '100px 0px 100px 0px'
    });

    sections.forEach(item => {
        if (!item.isHero) {
            observer.observe(item.el);
        }
    });

    // Handle scroll for bi-directional deconstruct/reconstruct & fast-scroll fail-safe
    window.addEventListener('scroll', () => {
        const scrollY = window.scrollY || window.pageYOffset;

        sections.forEach(s => {
            const r = s.el.getBoundingClientRect();
            s.pageTop = r.top + scrollY;
            s.height = r.height;

            // Fast-scroll fail-safe: if scrolled past while not built, resolve instantly so nothing is blank!
            if (s.state !== 'built' && (r.top < -60 || r.bottom < viewH * 0.35)) {
                finishPull(s, true);
            }

            // Bi-directional deconstruct: if section was built but has now scrolled out of view (> 0.5 viewports away),
            // safely deconstruct it so drones reconstruct it upon scrolling back!
            if (!s.isHero && s.state === 'built') {
                const isFarAway = (r.bottom < -viewH * 0.5) || (r.top > viewH * 1.5);
                if (isFarAway) {
                    s.state = 'pending';
                    s.el.setAttribute('data-nb', 'pending');
                    s.el.style.opacity = '0.2';
                    s.el.style.transform = 'translate3d(0, 45px, 0) scale(0.96)';
                    
                    const nodes = SectionCoordinator.getNodesForSection(s.id);
                    nodes.forEach(n => {
                        n.state = 'unscouted';
                        n.el.removeAttribute('data-assembled');
                        n.el.style.transform = 'translate3d(0, 28px, 0)';
                        n.el.style.opacity = '0.25';
                    });
                }
            }
        });

        processNextInQueue();
        ensureLoop();
    }, { passive: true });

    // ─── 10. Animation Frame Loop ──────────────────────────────────────────
    function renderFrame(now) {
        ctx.clearRect(0, 0, viewW, viewH);

        const scrollY = window.scrollY || window.pageYOffset;
        let hasActiveDrawing = false;

        // 0. Robotic Nano-Bots Swarm tracking (interconnected lightning & micro-arcs removed per user directive)
        if (window.swarm && typeof window.swarm.getDotsData === 'function') {
            const dotsData = window.swarm.getDotsData();
            if (dotsData && dotsData.length) {
                // Keep active drawing flag for smooth canvas lifecycle if needed
                hasActiveDrawing = false;
            }
        }

        // 1. Draw Ghost Blueprints for pending sections
        if (!docEl.classList.contains('nb-done')) {
            sections.forEach(item => {
                if (item.state === 'pending' && !item.isHero) {
                    const screenTop = item.pageTop - scrollY;
                    if (screenTop > -item.height && screenTop < viewH * 1.4) {
                        ctx.save();
                        ctx.strokeStyle = 'rgba(157, 77, 255, 0.22)';
                        ctx.lineWidth = 1;
                        ctx.setLineDash([6, 6]);
                        ctx.strokeRect(item.pageLeft + 8, screenTop + 8, item.width - 16, Math.min(item.height - 16, viewH * 0.9));
                        ctx.restore();
                        hasActiveDrawing = true;
                    }
                }
            });
        }

        // 2. Animate Active Pull
        if (currentPullingItem) {
            hasActiveDrawing = true;
            const item = currentPullingItem;
            const elapsed = now - item.startTime;
            const totalDur = item.duration;
            const t = Math.min(1, elapsed / totalDur);

            // Fast, energetic Phase Breakdown under 1.5 seconds:
            // 0.0s - 0.22s (t < 0.22): Phase 1 SCOUT (Fast reconnaissance sweep)
            // 0.22s - 0.88s (0.22 <= t < 0.88): Phase 2 PULL (Multipurpose firefly dots hoist child elements)
            // 0.88s - 1.05s (0.88 <= t <= 1.0): Phase 3 SNAP (Lock, gold sparks, normal constant site)
            const scoutRatio = 0.22;
            const pullRatio = 0.88;
            const maxOffset = Math.min(65, viewH * 0.08);

            let currentOffset = maxOffset;
            let currentOpacity = 0.25;
            let currentScale = 0.94;

            const screenTop = item.pageTop - scrollY;

            if (t < scoutRatio) {
                // PHASE 1: SCOUT / RECONNAISSANCE
                item.state = 'scouting';
                currentOffset = maxOffset;
                currentOpacity = 0.15 + (t / scoutRatio) * 0.15;
                currentScale = 0.94;

                // Pass drone proximity coordinates to coordinator
                if (window.swarm && typeof window.swarm.getDotsData === 'function') {
                    const dotsData = window.swarm.getDotsData();
                    SectionCoordinator.checkProximity(dotsData, item.id);
                }

                // Draw cyber scanning reticles and corner brackets across empty section
                ctx.save();
                ctx.strokeStyle = 'rgba(25, 227, 208, 0.45)';
                ctx.lineWidth = 1.5;
                const bracketLen = 22;
                
                // Outer corners of the scouted area
                const sx = item.pageLeft + 12;
                const sy = screenTop + 12;
                const sw = item.width - 24;
                const sh = Math.min(item.height - 24, viewH * 0.85);

                // Top-left
                ctx.beginPath();
                ctx.moveTo(sx, sy + bracketLen);
                ctx.lineTo(sx, sy);
                ctx.lineTo(sx + bracketLen, sy);
                ctx.stroke();

                // Top-right
                ctx.beginPath();
                ctx.moveTo(sx + sw - bracketLen, sy);
                ctx.lineTo(sx + sw, sy);
                ctx.lineTo(sx + sw, sy + bracketLen);
                ctx.stroke();

                // Bottom-left
                ctx.beginPath();
                ctx.moveTo(sx, sy + sh - bracketLen);
                ctx.lineTo(sx, sy + sh);
                ctx.lineTo(sx + bracketLen, sy + sh);
                ctx.stroke();

                // Bottom-right
                ctx.beginPath();
                ctx.moveTo(sx + sw - bracketLen, sy + sh);
                ctx.lineTo(sx + sw, sy + sh);
                ctx.lineTo(sx + sw, sy + sh - bracketLen);
                ctx.stroke();

                // Scanner sweep beam moving down
                const scanLineY = sy + (sh * (t / scoutRatio));
                ctx.beginPath();
                ctx.moveTo(sx, scanLineY);
                ctx.lineTo(sx + sw, scanLineY);
                ctx.strokeStyle = 'rgba(25, 227, 208, 0.65)';
                ctx.lineWidth = 2;
                ctx.shadowColor = '#19e3d0';
                ctx.shadowBlur = 8;
                ctx.stroke();
                ctx.restore();

            } else if (t < pullRatio) {
                // PHASE 2: MECHANICAL ANCHOR & PULL
                item.state = 'pulling';
                const pullT = (t - scoutRatio) / (pullRatio - scoutRatio);
                const eased = easeOutQuint(pullT);
                currentOffset = maxOffset * (1 - eased);
                currentOpacity = 0.30 + eased * 0.70;
                currentScale = 0.94 + eased * 0.06;

                // Individual child element micro-hoist & progressive assembly
                const nodes = SectionCoordinator.getNodesForSection(item.id);
                const totalNodes = nodes.length;
                const dynamicTargets = [];

                nodes.forEach((n, idx) => {
                    const staggerStart = (idx / Math.max(1, totalNodes)) * 0.55;
                    const childProgress = Math.max(0, Math.min(1, (pullT - staggerStart) / 0.45));
                    const childEase = easeOutQuint(childProgress);
                    
                    const childY = (1 - childEase) * 28;
                    const childOp = 0.25 + childEase * 0.75;
                    
                    n.el.style.transform = `translate3d(0, ${childY.toFixed(1)}px, 0)`;
                    n.el.style.opacity = childOp.toFixed(3);
                    
                    if (childProgress > 0 && childProgress < 0.95) {
                        const r = n.el.getBoundingClientRect();
                        if (r.width > 20 && r.height > 10) {
                            dynamicTargets.push({
                                x: r.left + r.width * 0.5,
                                y: r.top + r.height * 0.5
                            });
                        }
                    }
                    
                    if (childProgress >= 0.95 && n.state !== 'assembled') {
                        SectionCoordinator.markAssembled(n);
                    }
                });

                // Update swarm anchor targets so drones actively hoist the current active elements
                const anchors = dynamicTargets.length >= 4 
                    ? dynamicTargets.slice(0, 8) 
                    : computeAnchorPoints(item, currentOffset);

                if (window.swarm && typeof window.swarm.assign === 'function') {
                    window.swarm.assign(anchors);
                }

                // Inner box & text laser scan & weld line sweep
                const innerBoxes = getInnerBoxes(item, currentOffset);
                innerBoxes.forEach(b => {
                    ctx.save();
                    if (b.isText) {
                        const cornerLen = Math.min(10, b.w * 0.15);
                        ctx.strokeStyle = 'rgba(255, 216, 115, 0.80)'; // Neon Gold for text
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
                        ctx.strokeStyle = 'rgba(25, 227, 208, 0.60)';
                        ctx.lineWidth = 1.5;
                        ctx.setLineDash([8, 6]);
                        ctx.strokeRect(b.x, b.y, b.w, b.h);
                    }

                    // Bright gold weld line sweep
                    const sweepProgress = Math.min(1.0, pullT);
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

                // Draw glowing tethers between swarm dots and element anchors
                if (window.swarm && typeof window.swarm.getDotsData === 'function') {
                    const dotsData = window.swarm.getDotsData();
                    const vibration = Math.sin(now * 0.035) * 1.5;

                    for (let i = 0; i < Math.min(dotsData.length, anchors.length); i++) {
                        const dotX = dotsData[i].currentX;
                        const dotY = dotsData[i].currentY;
                        const anchor = anchors[i];

                        const midX = (dotX + anchor.x) * 0.5 + vibration;
                        const midY = (dotY + anchor.y) * 0.5;

                        ctx.save();
                        // Outer 3.5px violet beam
                        ctx.beginPath();
                        ctx.moveTo(dotX, dotY);
                        ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);
                        ctx.strokeStyle = 'rgba(157, 77, 255, 0.40)';
                        ctx.lineWidth = 3.5;
                        ctx.stroke();

                        // Middle 2px turquoise beam
                        ctx.beginPath();
                        ctx.moveTo(dotX, dotY);
                        ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);
                        ctx.strokeStyle = 'rgba(25, 227, 208, 0.65)';
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

            } else {
                // PHASE 3: SNAP & LOCK
                if (item.state !== 'snapping') {
                    item.state = 'snapping';
                    item.el.setAttribute('data-nb', 'snapping');
                    emitSparks(item.pageLeft + 25, screenTop + 15, 8);
                    emitSparks(item.pageLeft + item.width - 25, screenTop + 15, 8);
                }
                currentOffset = 0;
                currentOpacity = 1;
                currentScale = 1;
            }

            // Apply transform to section DOM element
            item.el.style.opacity = currentOpacity.toFixed(3);
            item.el.style.transform = `translate3d(0, ${currentOffset.toFixed(1)}px, 0) scale(${currentScale.toFixed(3)})`;

            if (t >= 1) {
                finishPull(item);
            }
        }

        // 3. Draw and update sparks
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

    // ─── 11. Initial Hero Assembly ─────────────────────────────────────────
    window.addEventListener('DOMContentLoaded', () => {
        const heroItem = sectionMap['home'];
        if (heroItem) {
            finishPull(heroItem, true);
        }
    });

    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            isLoopRunning = false;
        } else {
            ensureLoop();
        }
    });

})();
