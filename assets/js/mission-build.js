(function () {
    'use strict';

    const SECTION_IDS = [
        'home', 'profile-expertise', 'about-me', 'projects',
        'creative-lab', 'certificates', 'secret-desk', 'contact'
    ];
    const CARDS = '.project-card,.cert-card,.expertise-card,.stat-card,.glass-card,.bday-card,.profile-card-wrapper,.onboard-card,.code-block-visual';
    const CONTENT = 'h1,h2,h3,h4,h5,h6,p,.section-title,.section-tag,.section-desc,.section-intro,.trait-tag,.stat-label,.badge,.project-type,.code-line,.mock-line,pre,code,a,button,input,textarea,select,.filter-btn,.cta-button,.message-btn,.dock-btn,.hero-traits-list,.modern-switch';
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const root = document.documentElement;
    const canvas = document.getElementById('nb-canvas');
    const context = canvas && canvas.getContext('2d');
    const sections = [];
    const sectionsByElement = new Map();
    const itemsByElement = new Map();
    const active = new Map();
    const frameCallbacks = new Set();
    const metrics = { events: [] };
    let activeCrews = 0;
    let observer;
    let frameId = 0;
    let intervalId = 0;
    let initialized = false;
    let sectionObserver;
    let lastScrollAt = performance.now();
    let lastScrollY = window.scrollY;
    let lastFastScrollAt = 0;
    let startupFallback = 0;

    window.DroneFrame = {
        add: function (callback) {
            frameCallbacks.add(callback);
            wakeLoop();
        },
        remove: function (callback) {
            frameCallbacks.delete(callback);
        }
    };

    window.DroneBuildMetrics = metrics;

    function record(type, item, extra) {
        metrics.events.push(Object.assign({
            type: type,
            id: item.id,
            section: item.section.id,
            time: Math.round(performance.now()),
            top: item.rect ? Math.round(item.rect.top) : null,
            visibleHeight: item.intersection ? Math.round(item.intersection.height) : null
        }, extra || {}));
    }

    function revealEverything() {
        clearTimeout(watchdog);
        if (observer) observer.disconnect();
        if (sectionObserver) sectionObserver.disconnect();
        if (intervalId) window.clearInterval(intervalId);
        active.forEach(function (mission) { finishItem(mission.item, true); });
        sections.forEach(function (section) {
            section.items.forEach(function (item) {
                item.state = 'built';
                item.el.inert = false;
                item.el.classList.remove('drone-pending', 'drone-active');
                item.el.classList.add('drone-placed');
                item.el.style.removeProperty('--drone-duration');
            });
            section.el.setAttribute('data-nb', 'built');
        });
        root.classList.remove('drone-ready');
        root.classList.add('drone-failed-open');
        if (window.DroneCanvas && window.DroneCanvas.releaseAll) {
            window.DroneCanvas.releaseAll();
        }
    }

    function orderedElements(section) {
        const found = new Set(section.querySelectorAll(CONTENT));
        section.querySelectorAll(CARDS).forEach(function (card) {
            if (card.parentElement && card.parentElement.closest(CARDS)) return;
            found.add(card);
            card.querySelectorAll(CONTENT).forEach(function (child) { found.add(child); });
        });

        const elements = Array.from(found).filter(function (el) {
            return !el.closest('nav,script,style,[aria-hidden="true"]') &&
                !(el.matches('input[type="checkbox"]') && el.closest('.modern-switch'));
        });
        function priority(el) {
            if (el.matches(CARDS)) return 3;
            if (el.closest(CARDS)) {
                return el.matches('a,button,input,textarea,select,.filter-btn,.cta-button,.message-btn,.dock-btn') ? 5 : 4;
            }
            if (el.matches('h1,h2,h3,.section-title,.section-tag')) return 1;
            if (el.matches('p,h4,h5,h6,.section-desc,.section-intro') && !el.closest(CARDS)) return 2;
            if (el.matches('a,button,.filter-btn,.cta-button,.message-btn,.dock-btn')) return 5;
            return 4;
        }
        return elements.sort(function (a, b) {
            const order = priority(a) - priority(b);
            if (order) return order;
            const relation = a.compareDocumentPosition(b);
            return relation & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1;
        });
    }

    function wrapCodeLines(section) {
        section.querySelectorAll('.code-block-visual code').forEach(function (code) {
            if (code.querySelector('.code-line')) return;
            let line = document.createElement('span');
            line.className = 'code-line';
            const nodes = Array.from(code.childNodes);
            const fragment = document.createDocumentFragment();
            nodes.forEach(function (node) {
                if (node.nodeName === 'BR') {
                    node.remove();
                    if (line.childNodes.length) fragment.appendChild(line);
                    line = document.createElement('span');
                    line.className = 'code-line';
                } else {
                    line.appendChild(node);
                }
            });
            if (line.childNodes.length) fragment.appendChild(line);
            code.appendChild(fragment);
        });
    }

    function createSection(id, index) {
        const el = document.getElementById(id);
        if (!el || sectionsByElement.has(el)) return;
        const section = {
            id: id,
            el: el,
            index: index,
            inBandSince: null,
            items: []
        };
        wrapCodeLines(el);
        orderedElements(el).forEach(function (element, elementIndex) {
            const item = {
                id: element.id || id + '-' + elementIndex,
                section: section,
                el: element,
                index: elementIndex,
                state: 'pending',
                visible: false,
                rect: null,
                intersection: null,
                gateOpenedAt: 0,
                travelTime: 0,
                timers: []
            };
            section.items.push(item);
            itemsByElement.set(element, item);
            element.classList.add('drone-managed', 'drone-pending');
            element.inert = true;
        });
        sections.push(section);
        sectionsByElement.set(el, section);
    }

    function createSections() {
        createSection(SECTION_IDS[0], 0);
        const hashId = window.location.hash.slice(1);
        const index = SECTION_IDS.indexOf(hashId);
        if (index > 0) createSection(hashId, index);
    }

    function observeUpcomingSections() {
        if (sectionObserver) sectionObserver.disconnect();
        sectionObserver = new IntersectionObserver(function (entries) {
            let changed = false;
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) return;
                const index = SECTION_IDS.indexOf(entry.target.id);
                if (index < 0 || sectionsByElement.has(entry.target)) return;
                sectionObserver.unobserve(entry.target);
                createSection(entry.target.id, index);
                changed = true;
            });
            if (changed) updateObservers();
        }, { rootMargin: '500px 0px' });
        SECTION_IDS.slice(1).forEach(function (id) {
            const el = document.getElementById(id);
            if (el && !sectionsByElement.has(el)) sectionObserver.observe(el);
        });
    }

    function measureVisibility(entry) {
        const rect = entry.boundingClientRect;
        const intersection = entry.intersectionRect;
        const bandHeight = entry.rootBounds ? entry.rootBounds.height : innerHeight * 0.8;
        const neededHeight = Math.min(rect.height, Math.min(innerHeight * 0.8, 600));
        const visibleHeight = Math.min(intersection.height, neededHeight);
        const visibleWidth = Math.min(intersection.width, rect.width);
        const visible = entry.isIntersecting &&
            visibleHeight >= neededHeight * 0.8 &&
            visibleWidth >= rect.width * 0.8;
        return { visible: visible, rect: rect, intersection: intersection, bandHeight: bandHeight };
    }

    function drawLoop(now) {
        frameId = 0;
        if (document.hidden || !context || !window.DroneCanvas) return;
        const dpr = Math.min(window.devicePixelRatio || 1, 2);
        context.setTransform(dpr, 0, 0, dpr, 0, 0);
        context.clearRect(0, 0, innerWidth, innerHeight);
        window.DroneCanvas.render(context, now);
        frameCallbacks.forEach(function (callback) {
            try {
                callback(now);
            } catch (error) {
                frameCallbacks.delete(callback);
                console.error('[Drone frame] Animation callback failed and was removed.', error);
            }
        });
        frameId = requestAnimationFrame(drawLoop);
    }

    function wakeLoop() {
        if (!frameId && !document.hidden && context && window.DroneCanvas) {
            frameId = requestAnimationFrame(drawLoop);
        }
    }

    function anchorsFor(rect) {
        const x1 = Math.max(4, Math.min(innerWidth - 4, rect.left + 8));
        const x2 = Math.max(4, Math.min(innerWidth - 4, rect.right - 8));
        const y1 = Math.max(4, Math.min(innerHeight - 4, rect.top + 8));
        const y2 = Math.max(4, Math.min(innerHeight - 4, rect.bottom - 8));
        return [
            { x: x1, y: y1 },
            { x: (x1 + x2) / 2, y: y1 },
            { x: x2, y: y1 },
            { x: x2, y: (y1 + y2) / 2 },
            { x: (x1 + x2) / 2, y: y2 }
        ];
    }

    function durationFor(item) {
        const el = item.el;
        if (el.matches('.code-block-visual')) return 700;
        if (el.matches('h1,h2,h3,.section-title,.section-tag')) return 1100;
        if (el.matches('p,h4,h5,h6,.section-desc,.section-intro')) return 900;
        if (el.matches('a,button,input,textarea,select,.filter-btn,.cta-button,.message-btn,.dock-btn')) return 450;
        if (el.matches(CARDS)) return 600;
        if (el.matches('.code-line,.mock-line,pre,code') && el.closest('.code-block-visual')) return 140;
        return 450;
    }

    function finishItem(item, instant) {
        item.timers.forEach(window.clearTimeout);
        item.timers.length = 0;
        if (item.state === 'built') return;
        item.state = 'built';
        item.el.inert = false;
        item.el.classList.remove('drone-pending', 'drone-active');
        item.el.classList.add('drone-placed');
        if (instant) {
            item.el.style.transitionDuration = '0ms';
            window.setTimeout(function () { item.el.style.removeProperty('transition-duration'); }, 0);
        }
        item.el.style.removeProperty('--drone-duration');
        const mission = active.get(item.id);
        if (mission) {
            active.delete(item.id);
            if (window.DroneCanvas && window.DroneCanvas.release) {
                const returnTime = window.DroneCanvas.release(mission.id) || 0;
                const timer = window.setTimeout(function () {
                    activeCrews = Math.max(0, activeCrews - 1);
                    wakeLoop();
                }, returnTime);
                item.timers.push(timer);
            } else {
                activeCrews = Math.max(0, activeCrews - 1);
            }
        }
        record('built', item, { duration: Math.round(performance.now() - item.gateOpenedAt) });
        if (item.section.id === 'about-me' && typeof window.animateCounters === 'function') {
            window.animateCounters();
        }
        if (item.section.items.every(function (entry) { return entry.state === 'built'; })) {
            item.section.el.setAttribute('data-nb', 'built');
        }
    }

    function placeItem(item, travelTime) {
        if (item.state === 'built') return;
        item.state = 'pull';
        item.el.inert = false;
        item.el.style.setProperty('--drone-duration', durationFor(item) + 'ms');
        item.el.classList.remove('drone-pending');
        item.el.classList.add('drone-active', 'drone-placed');
        if (item.el.matches('.code-line') && window.DroneCanvas.spark) {
            const rect = item.el.getBoundingClientRect();
            window.DroneCanvas.spark(rect.left + rect.width * 0.5, rect.top + rect.height * 0.5);
        }
        record('reveal', item, { travelTime: travelTime, state: item.state });
        const timer = window.setTimeout(function () {
            finishItem(item, false);
        }, durationFor(item) + (item.el.matches('.code-line,.mock-line') ? 0 : 60));
        item.timers.push(timer);
    }

    function startItem(item) {
        item.state = 'dispatch';
        item.gateOpenedAt = performance.now();
        const gate = measureVisibility({
            isIntersecting: item.visible,
            boundingClientRect: item.rect,
            intersectionRect: item.intersection,
            rootBounds: { height: innerHeight * 0.8 }
        });
        item.section.el.setAttribute('data-nb', 'building');
        if (reducedMotion) {
            record('dispatch', item, {
                gateVisible: gate.visible,
                speedSettled: performance.now() - lastFastScrollAt >= 200,
                sectionDwell: item.section.inBandSince === null ? 0 : Math.round(performance.now() - item.section.inBandSince)
            });
            item.state = 'arrived';
            item.travelTime = 0;
            return;
        }

        const crewId = item.id + '-' + Math.round(item.gateOpenedAt);
        const travelTime = window.DroneCanvas.dispatch(anchorsFor(item.rect), crewId);
        if (!travelTime) {
            item.state = 'pending';
            return;
        }
        record('dispatch', item, {
            gateVisible: gate.visible,
            speedSettled: performance.now() - lastFastScrollAt >= 200,
            sectionDwell: item.section.inBandSince === null ? 0 : Math.round(performance.now() - item.section.inBandSince)
        });
        const minFlight = Math.max(500, travelTime || 600);
        activeCrews++;
        active.set(item.id, { id: crewId, item: item });
        item.state = 'dispatch';
        wakeLoop();
        const failSafe = window.setTimeout(function () { finishItem(item, true); }, 3250);
        item.timers.push(failSafe);
        const dispatchTimer = window.setTimeout(function () {
            if (item.state !== 'built') {
                item.state = 'arrived';
                item.travelTime = minFlight;
                record('arrived', item, { travelTime: minFlight });
                scheduleMissions();
            }
        }, minFlight);
        item.timers.push(dispatchTimer);
    }

    function canStart(item, index, now) {
        if (item.state !== 'pending' || !item.visible || item.section.inBandSince === null) return false;
        if (item.section.id === 'home' && window.scrollY > innerHeight * 0.15) return false;
        const dwell = item.section.id === 'home' ? 0 : 400;
        if (now - item.section.inBandSince < dwell) return false;
        if (now - lastFastScrollAt < 200) return false;
        if (index > 0) {
            const previous = item.section.items[index - 1];
            if (previous.state === 'pending') return false;
        }
        return activeCrews < 3;
    }

    function scheduleMissions() {
        if (!initialized || document.hidden) return;
        const now = performance.now();
        sections.forEach(function (section) {
            section.items.forEach(function (item, index) {
                const predecessorBuilt = index === 0 || section.items[index - 1].state === 'built';
                if (item.state === 'arrived' && predecessorBuilt) {
                    placeItem(item, item.travelTime);
                }
            });
            for (let i = 0; i < section.items.length; i++) {
                const item = section.items[i];
                if (canStart(item, i, now)) {
                    startItem(item);
                }
            }
        });
    }

    function updateObservers() {
        if (observer) observer.disconnect();
        observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                const section = sectionsByElement.get(entry.target);
                if (section) {
                    if (entry.isIntersecting && entry.intersectionRect.height > 0) {
                        if (section.inBandSince === null) section.inBandSince = performance.now();
                    } else {
                        section.inBandSince = null;
                    }
                    return;
                }
                const item = itemsByElement.get(entry.target);
                if (!item || item.state !== 'pending') return;
                const measured = measureVisibility(entry);
                item.visible = measured.visible;
                item.rect = measured.rect;
                item.intersection = measured.intersection;
            });
            scheduleMissions();
        }, {
            rootMargin: '-8% 0px -12% 0px',
            threshold: [0, 0.01, 0.1, 0.25, 0.5, 0.75, 0.8, 1]
        });
        sections.forEach(function (section) {
            observer.observe(section.el);
            section.items.forEach(function (item) { observer.observe(item.el); });
        });
    }

    function retargetActive() {
        sections.forEach(function (section) { section.inBandSince = null; });
        active.forEach(function (mission, id) {
            const item = sections.reduce(function (found, section) {
                return found || section.items.find(function (entry) { return entry.id === id; });
            }, null);
            if (item && window.DroneCanvas.retarget) {
                const rect = item.el.getBoundingClientRect();
                window.DroneCanvas.retarget(mission.id, anchorsFor(rect));
            } else if (item) {
                finishItem(item, true);
            }
        });
        updateObservers();
    }

    function init() {
        if (initialized || root.classList.contains('drone-failed-open')) return;
        if (!window.IntersectionObserver || !context || !window.DroneCanvas || !window.DroneCanvas.dispatch) {
            revealEverything();
            return;
        }
        try {
            createSections();
            root.classList.add('drone-ready');
            initialized = true;
            clearTimeout(watchdog);
            clearTimeout(startupFallback);
            updateObservers();
            observeUpcomingSections();
            intervalId = window.setInterval(scheduleMissions, 50);
            window.DroneCanvas.setWake(wakeLoop);
            wakeLoop();
            document.querySelectorAll('.bg-video').forEach(function (video) {
                video.preload = 'none';
                const videoObserver = new IntersectionObserver(function (entries) {
                    entries.forEach(function (entry) {
                        if (entry.isIntersecting) {
                            video.play().catch(function (error) {
                                console.warn('[Drone build] Background video could not start:', error);
                            });
                        } else {
                            video.pause();
                        }
                    });
                }, { rootMargin: '300px' });
                videoObserver.observe(video);
            });
        } catch (error) {
            console.error('[Drone build] Initialization failed; revealing page content.', error);
            revealEverything();
        }
    }

    const watchdog = window.setTimeout(function () {
        if (!initialized) {
            console.warn('[Drone build] Startup watchdog reached; revealing page content.');
            revealEverything();
        }
    }, 2500);

    window.addEventListener('scroll', function () {
        const now = performance.now();
        const y = window.scrollY;
        const elapsed = Math.max(1, now - lastScrollAt);
        const speed = Math.abs(y - lastScrollY) * 1000 / elapsed;
        if (speed >= 800) lastFastScrollAt = now;
        lastScrollAt = now;
        lastScrollY = y;
        const home = sectionsByElement.get(document.getElementById('home'));
        if (home) {
            if (y > innerHeight * 0.15) home.inBandSince = null;
            else if (home.inBandSince === null) home.inBandSince = now;
        }
    }, { passive: true });

    window.addEventListener('resize', retargetActive, { passive: true });
    window.addEventListener('orientationchange', retargetActive, { passive: true });
    window.addEventListener('hashchange', function () {
        const id = decodeURIComponent(window.location.hash.slice(1));
        const index = SECTION_IDS.indexOf(id);
        if (index <= 0) return;
        createSection(id, index);
        updateObservers();
    });
    window.addEventListener('beforeprint', revealEverything);
    document.addEventListener('visibilitychange', function () {
        if (document.hidden && frameId) {
            cancelAnimationFrame(frameId);
            frameId = 0;
        } else {
            wakeLoop();
            scheduleMissions();
        }
    });

    window.addEventListener('error', function (event) {
        if (initialized && !root.classList.contains('drone-failed-open')) {
            console.error('[Drone build] Runtime error; revealing remaining content.', event.error || event.message);
            revealEverything();
        }
    });

    window.requestAnimationFrame(function () {
        window.requestAnimationFrame(function () {
            if ('requestIdleCallback' in window) {
                window.requestIdleCallback(init, { timeout: 350 });
            } else {
                window.setTimeout(init, 0);
            }
        });
    });
    startupFallback = window.setTimeout(init, 500);
})();
