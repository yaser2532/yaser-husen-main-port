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
                'h1, h2, h3, h4, .section-title, .card-title, .section-tag',
                '.section-desc, .section-intro, p, .about-text p, .trait-tag, .stat-label, .badge',
                '.project-card, .cert-card, .expertise-card, .stat-card, .glass-card, .bday-card, .profile-card-wrapper, .onboard-card',
                '.hero-traits-list, .filter-btn, .cta-button, .message-btn, .dock-btn, .cyber-dock-bar'
            ].join(', ');

            const cardSel = '.project-card, .cert-card, .expertise-card, .stat-card, .glass-card, .bday-card, .profile-card-wrapper, .cyber-dock-bar, .onboard-card';
            const childNodes = Array.from(el.querySelectorAll(selectors)).filter(childEl => {
                if (childEl.matches(cardSel)) {
                    return true;
                }
                if (childEl.closest(cardSel)) {
                    return false;
                }
                return true;
            });

            // Sequential interpreter order: Title strictly first, then paragraphs, then cards/divs, then buttons/links
            const getPriority = (element) => {
                const tag = element.tagName.toLowerCase();
                // 1. First line: Main section title / heading
                if (['h1', 'h2', 'h3'].includes(tag) || element.classList.contains('section-title') || element.classList.contains('section-tag')) {
                    return 1;
                }
                // 2. Second: Section descriptions, paragraphs, intro text
                if (['h4', 'h5', 'h6', 'p'].includes(tag) || element.classList.contains('section-desc') || element.classList.contains('section-intro') || element.classList.contains('about-text')) {
                    return 2;
                }
                // 3. Third: Content blocks, showcase cards, visual code blocks, stats
                if (element.matches(cardSel) || element.classList.contains('code-block-visual') || element.classList.contains('stats-row')) {
                    return 3;
                }
                // 4. Fourth: Buttons, controls, links, footer actions
                return 4;
            };

            const sortedChildNodes = childNodes.sort((a, b) => {
                const prioA = getPriority(a);
                const prioB = getPriority(b);
                if (prioA !== prioB) return prioA - prioB;
                return (a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING) ? -1 : 1;
            });

            sortedChildNodes.forEach((childEl, order) => {
                const tag = childEl.tagName.toLowerCase();
                const isText = ['h1', 'h2', 'h3', 'h4', 'p', 'span', 'a', 'button'].includes(tag);
                SectionCoordinator.register(id, childEl, isText, order);
                if (!isReducedMotion && !isHero) {
                    childEl.style.transform = 'translate3d(0, 20px, 0)';
                    childEl.style.opacity = '0';
                    childEl.style.willChange = 'transform, opacity';
                }
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
                if (r.bottom > 0 && r.top < viewH) {
                    validBoxes.push({
                        el,
                        isText,
                        x: r.left,
                        y: r.top,
                        w: r.width,
                        h: r.height
                    });
                }
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
        
        const nodes = SectionCoordinator.getNodesForSection(item.id);
        const GAP_MS = fastMode ? 150 : 500; // Strict 0.5s sequence gap per user directive
        const ELEM_DUR_MS = fastMode ? 250 : 450;
        const SCOUT_DUR_MS = fastMode ? 150 : 300;
        
        item.scoutDuration = SCOUT_DUR_MS;
        item.gapDuration = GAP_MS;
        item.elemDuration = ELEM_DUR_MS;
        item.duration = SCOUT_DUR_MS + Math.max(1, nodes.length) * GAP_MS + 250;
        
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

        // Auto-recovery: if currentPullingItem has scrolled completely out of view, finish it instantly
        if (currentPullingItem) {
            const r = currentPullingItem.el.getBoundingClientRect();
            const isOutOfFocus = (r.bottom < 0) || (r.top > viewH + 100);
            if (isOutOfFocus) {
                const prev = currentPullingItem;
                currentPullingItem = null;
                finishPull(prev, true);
                return;
            } else {
                return; // Currently pulling a visible item
            }
        }

        // Check which pending section is in view to begin cinematic assembly
        let targetSection = null;
        const isAtBottom = (window.innerHeight + scrollY >= document.documentElement.scrollHeight - 80);

        for (let i = 0; i < sections.length; i++) {
            const s = sections[i];
            if (s.state === 'pending' && !s.isHero) {
                const r = s.el.getBoundingClientRect();
                // Cinematic trigger: begins when top enters upper 75% of viewport so user sees the full pull
                const inCinematicView = (r.top <= viewH * 0.75 && r.bottom >= viewH * 0.15) ||
                                        (isAtBottom && s.id === 'contact');
                if (inCinematicView) {
                    targetSection = s;
                    break;
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
        threshold: 0.35,
        rootMargin: '0px 0px -40% 0px'
    });

    sections.forEach(item => {
        if (!item.isHero) {
            observer.observe(item.el);
        }
    });

    // 60FPS Smooth Throttled Scroll Listener (zero layout thrashing using cached geometry)
    let scrollScheduled = false;
    window.addEventListener('scroll', () => {
        if (!scrollScheduled) {
            requestAnimationFrame(() => {
                const scrollY = window.scrollY || window.pageYOffset;

                sections.forEach(s => {
                    const screenTop = s.pageTop - scrollY;
                    const screenBottom = screenTop + s.height;

                    // Fast-scroll fail-safe: if scrolled past while not built, resolve instantly so nothing is blank
                    if (s.state !== 'built' && (screenTop < -60 || screenBottom < viewH * 0.10)) {
                        finishPull(s, true);
                    }
                });

                processNextInQueue();
                ensureLoop();
                scrollScheduled = false;
            });
            scrollScheduled = true;
        }
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
            const scoutDur = item.scoutDuration || 300;
            const gapMs = item.gapDuration || 500; // Strict 0.5s sequence gap per user directive
            const elemDur = item.elemDuration || 450;
            const maxOffset = Math.min(50, viewH * 0.06);

            let currentOffset = maxOffset;
            let currentOpacity = 0.25;
            let currentScale = 0.96;

            const screenTop = item.pageTop - scrollY;

            if (elapsed < scoutDur) {
                // PHASE 1: SCOUT / RECONNAISSANCE SWEEP
                item.state = 'scouting';
                currentOffset = maxOffset;
                currentOpacity = 0.20 + (elapsed / scoutDur) * 0.20;
                currentScale = 0.96;

                // Pass drone proximity coordinates to coordinator
                if (window.swarm && typeof window.swarm.getDotsData === 'function') {
                    const dotsData = window.swarm.getDotsData();
                    SectionCoordinator.checkProximity(dotsData, item.id);
                }

                // Draw cyberpunk scanning reticles and corner brackets across empty section
                ctx.save();
                ctx.strokeStyle = 'rgba(0, 240, 255, 0.70)'; // Cyber Cyan
                ctx.lineWidth = 1.6;
                const bracketLen = 24;
                
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

                // Scanner sweep beam moving down: High-voltage Zesty Lemon laser sweep
                const scanLineY = sy + (sh * (elapsed / scoutDur));
                ctx.beginPath();
                ctx.moveTo(sx, scanLineY);
                ctx.lineTo(sx + sw, scanLineY);
                ctx.strokeStyle = 'rgba(255, 230, 0, 0.90)';
                ctx.lineWidth = 2.5;
                ctx.shadowColor = '#ffe600';
                ctx.shadowBlur = 12;
                ctx.stroke();

                // White laser core for the sweep beam
                ctx.beginPath();
                ctx.moveTo(sx, scanLineY);
                ctx.lineTo(sx + sw, scanLineY);
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.95)';
                ctx.lineWidth = 1.0;
                ctx.shadowColor = '#ffffff';
                ctx.shadowBlur = 5;
                ctx.stroke();
                ctx.restore();

            } else if (elapsed < item.duration - 250) {
                // PHASE 2: SEQUENTIAL ELEMENT-BY-ELEMENT PULL (0.5s GAP)
                item.state = 'pulling';
                const pullElapsed = elapsed - scoutDur;

                // Section container shell settles in smoothly
                const shellT = Math.min(1.0, pullElapsed / 600);
                const shellEase = easeOutQuint(shellT);
                currentOffset = maxOffset * (1 - shellEase);
                currentOpacity = 0.40 + shellEase * 0.60;
                currentScale = 0.96 + shellEase * 0.04;

                const nodes = SectionCoordinator.getNodesForSection(item.id);
                const dynamicTargets = [];
                let activeBox = null;

                nodes.forEach((n, idx) => {
                    const startMs = idx * gapMs; // Exactly 0.5s gap later for next element!
                    const endMs = startMs + elemDur;

                    if (pullElapsed < startMs) {
                        // Waiting its turn: stays pending and hidden
                        n.el.style.transform = 'translate3d(0, 20px, 0)';
                        n.el.style.opacity = '0';
                    } else if (pullElapsed >= startMs && pullElapsed < endMs) {
                        // ACTIVELY PULLING THIS ELEMENT (Refined & Smooth Cubic-Out Transition)
                        const p = (pullElapsed - startMs) / elemDur;
                        const childEase = 1 - Math.pow(1 - p, 3);
                        const childY = (1 - childEase) * 20;
                        const childScale = 0.985 + 0.015 * childEase;
                        const childOp = 0.10 + childEase * 0.90;

                        n.el.style.transform = `translate3d(0, ${childY.toFixed(1)}px, 0) scale(${childScale.toFixed(3)})`;
                        n.el.style.opacity = childOp.toFixed(3);

                        const r = n.el.getBoundingClientRect();
                        if (r.width > 10 && r.height > 6) {
                            dynamicTargets.push({ x: r.left, y: r.top }); // 0: Top-Left
                            dynamicTargets.push({ x: r.left + r.width * 0.5, y: r.top }); // 1: Top-Center
                            dynamicTargets.push({ x: r.right, y: r.top }); // 2: Top-Right
                            dynamicTargets.push({ x: r.right, y: r.top + r.height * 0.5 }); // 3: Right-Center
                            dynamicTargets.push({ x: r.right, y: r.bottom }); // 4: Bottom-Right
                            dynamicTargets.push({ x: r.left + r.width * 0.5, y: r.bottom }); // 5: Bottom-Center
                            dynamicTargets.push({ x: r.left, y: r.bottom }); // 6: Bottom-Left
                            dynamicTargets.push({ x: r.left + r.width * 0.5, y: r.top + r.height * 0.5 }); // 7: Centroid

                            activeBox = {
                                x: r.left,
                                y: r.top,
                                w: r.width,
                                h: r.height,
                                isText: n.isText,
                                progress: p
                            };
                        }
                    } else {
                        // Completed its sequential turn: locked into assembled state!
                        if (n.state !== 'assembled') {
                            SectionCoordinator.markAssembled(n);
                            n.el.style.transform = '';
                            n.el.style.opacity = '1';
                            const r = n.el.getBoundingClientRect();
                            emitSparks(r.left + r.width * 0.5, r.top + 8, 8);
                        }
                    }
                });

                // Drones converge directly onto the actively pulling element
                if (dynamicTargets.length > 0 && window.swarm && typeof window.swarm.assign === 'function') {
                    window.swarm.assign(dynamicTargets.slice(0, 8));
                }

                // Laser weld sweep beam across the actively pulling element
                if (activeBox) {
                    ctx.save();
                    // Subtle holographic construction shimmer inside element
                    ctx.fillStyle = `rgba(255, 230, 0, ${(0.035 * (1 - activeBox.progress)).toFixed(3)})`;
                    ctx.fillRect(activeBox.x, activeBox.y, activeBox.w, activeBox.h);
                    if (activeBox.isText) {
                        const cornerLen = Math.min(12, activeBox.w * 0.18);
                        ctx.strokeStyle = 'rgba(255, 230, 0, 0.95)'; // Electric Zesty Lemon for text
                        ctx.lineWidth = 1.5;
                        
                        // Top-left
                        ctx.beginPath();
                        ctx.moveTo(activeBox.x, activeBox.y + cornerLen);
                        ctx.lineTo(activeBox.x, activeBox.y);
                        ctx.lineTo(activeBox.x + cornerLen, activeBox.y);
                        ctx.stroke();

                        // Top-right
                        ctx.beginPath();
                        ctx.moveTo(activeBox.x + activeBox.w - cornerLen, activeBox.y);
                        ctx.lineTo(activeBox.x + activeBox.w, activeBox.y);
                        ctx.lineTo(activeBox.x + activeBox.w, activeBox.y + cornerLen);
                        ctx.stroke();

                        // Bottom-left
                        ctx.beginPath();
                        ctx.moveTo(activeBox.x, activeBox.y + activeBox.h - cornerLen);
                        ctx.lineTo(activeBox.x, activeBox.y + activeBox.h);
                        ctx.lineTo(activeBox.x + cornerLen, activeBox.y + activeBox.h);
                        ctx.stroke();

                        // Bottom-right
                        ctx.beginPath();
                        ctx.moveTo(activeBox.x + activeBox.w - cornerLen, activeBox.y + activeBox.h);
                        ctx.lineTo(activeBox.x + activeBox.w, activeBox.y + activeBox.h);
                        ctx.lineTo(activeBox.x + activeBox.w, activeBox.y + activeBox.h - cornerLen);
                        ctx.stroke();
                    } else {
                        ctx.strokeStyle = 'rgba(0, 240, 255, 0.75)'; // Cyber Cyan for boxes/cards
                        ctx.lineWidth = 1.5;
                        ctx.setLineDash([8, 6]);
                        ctx.strokeRect(activeBox.x, activeBox.y, activeBox.w, activeBox.h);
                    }

                    // Electric Zesty Lemon laser weld line sweep with diamond white core
                    const sweepX = activeBox.x + activeBox.w * activeBox.progress;
                    ctx.beginPath();
                    ctx.moveTo(sweepX, activeBox.y - 4);
                    ctx.lineTo(sweepX, activeBox.y + activeBox.h + 4);
                    ctx.strokeStyle = 'rgba(255, 230, 0, 0.95)';
                    ctx.lineWidth = 2.8;
                    ctx.shadowColor = '#ffe600';
                    ctx.shadowBlur = 14;
                    ctx.stroke();

                    ctx.beginPath();
                    ctx.moveTo(sweepX, activeBox.y - 2);
                    ctx.lineTo(sweepX, activeBox.y + activeBox.h + 2);
                    ctx.strokeStyle = 'rgba(255, 255, 255, 0.98)';
                    ctx.lineWidth = 1.0;
                    ctx.shadowColor = '#ffffff';
                    ctx.shadowBlur = 6;
                    ctx.stroke();
                    ctx.restore();
                }

                // Draw glowing cyberpunk tractor beams between swarm drones and active element
                if (dynamicTargets.length > 0 && window.swarm && typeof window.swarm.getDotsData === 'function') {
                    const dotsData = window.swarm.getDotsData();
                    const vibration = Math.sin(now * 0.035) * 1.5;

                    for (let i = 0; i < Math.min(dotsData.length, dynamicTargets.length); i++) {
                        const dotX = dotsData[i].currentX;
                        const dotY = dotsData[i].currentY;
                        const anchor = dynamicTargets[i];

                        const midX = (dotX + anchor.x) * 0.5 + vibration;
                        const midY = (dotY + anchor.y) * 0.5;

                        ctx.save();
                        // Outer 3.5px Cyber Cyan plasma aura
                        ctx.beginPath();
                        ctx.moveTo(dotX, dotY);
                        ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);
                        ctx.strokeStyle = 'rgba(0, 240, 255, 0.35)';
                        ctx.lineWidth = 3.5;
                        ctx.stroke();

                        // Middle 2px Electric Zesty Lemon beam
                        ctx.beginPath();
                        ctx.moveTo(dotX, dotY);
                        ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);
                        ctx.strokeStyle = 'rgba(255, 230, 0, 0.85)';
                        ctx.lineWidth = 2;
                        ctx.stroke();

                        // Inner brilliant laser diamond white core
                        ctx.beginPath();
                        ctx.moveTo(dotX, dotY);
                        ctx.quadraticCurveTo(midX, midY, anchor.x, anchor.y);
                        ctx.strokeStyle = 'rgba(255, 255, 255, 0.98)';
                        ctx.lineWidth = 1.2;
                        ctx.shadowColor = '#ffe600';
                        ctx.shadowBlur = 8;
                        ctx.stroke();
                        ctx.restore();
                    }
                }

            } else {
                // PHASE 3: FINAL SNAP & LOCK
                if (item.state !== 'snapping') {
                    item.state = 'snapping';
                    item.el.setAttribute('data-nb', 'snapping');
                    emitSparks(item.pageLeft + 25, screenTop + 15, 10);
                    emitSparks(item.pageLeft + item.width - 25, screenTop + 15, 10);
                }
                currentOffset = 0;
                currentOpacity = 1;
                currentScale = 1;
            }

            // Apply transform to section DOM element
            item.el.style.opacity = currentOpacity.toFixed(3);
            item.el.style.transform = `translate3d(0, ${currentOffset.toFixed(1)}px, 0) scale(${currentScale.toFixed(3)})`;

            if (elapsed >= item.duration) {
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
                ctx.fillStyle = (i % 2 === 0) 
                    ? `rgba(255, 230, 0, ${s.life.toFixed(2)})` 
                    : `rgba(0, 240, 255, ${s.life.toFixed(2)})`;
                ctx.shadowColor = (i % 2 === 0) ? '#ffe600' : '#00f0ff';
                ctx.shadowBlur = 4;
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
