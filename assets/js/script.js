/* ==========================================================================
   PORTFOLIO INTEGRATION & INTERACTIVE LOGIC
   ========================================================================== */

// ─── Birthday Wishes App Global State ─────────────────────────────────────
let personName = '';
let personDOB  = '';
let personAge  = 0;
let galleryPhotos = []; // Base64 image URLs uploaded by user
let galleryRunning = false;
let candlesOut = 0;
let totalCandles = 0;
let micStream = null;
let giftOpened = false;
let fortuneRevealed = false;

const wishesData = [
  { icon:'🌟', title:'Unlimited Joy',     text:'May every single day of this new year bring you more happiness than the last.' },
  { icon:'💫', title:'Dream Big',         text:'Chase every dream that lights a fire in your heart. The world is yours.' },
  { icon:'🏆', title:'Unstoppable You',   text:'You have already conquered so much - this year you will conquer even more.' },
  { icon:'💖', title:'Boundless Love',    text:'Surrounded by people who love you deeply, may you always feel truly cherished.' },
  { icon:'🌈', title:'New Adventures',    text:'May this year open doors you never even knew existed.' },
  { icon:'✨', title:'Inner Peace',       text:'May you find calm in chaos, strength in struggle, and light in every shadow.' },
  { icon:'🎯', title:'Every Goal Met',    text:'Set the targets high - because this year you will smash every single one.' },
  { icon:'🌸', title:'Good Health',       text:'Wishing you vibrant energy, glowing health, and a radiant smile always.' },
  { icon:'🔥', title:'Be Legendary',      text:'You were not born ordinary. Blaze so bright the whole sky notices.' },
];

const giftMessages = [
  'You are someone special and a reason to smile every single day. 💛',
  'The world is brighter, louder, and more beautiful because you are in it. 🌟',
  'Your laugh is the best song. Your heart is the best gift. 💖',
  'Today the universe wrapped all its magic into one person — YOU. ✨',
  'Keep being unapologetically, wonderfully you. The world needs exactly that. 🦋',
  'Every candle you blow out leaves a wish in the air. May all yours come true. 🕯️',
];

const fortunes = [
  { emoji:'🌟', title:'A year of breakthroughs', text:'The stars align for something big. A dream you have been chasing is finally within reach this year.' },
  { emoji:'💰', title:'Abundance incoming', text:'Unexpected opportunities will knock. Say yes more than no — the universe is routing resources your way.' },
  { emoji:'❤️', title:'Love will surprise you', text:'The heart you least expect will matter the most. Stay open, stay soft, stay you.' },
  { emoji:'🚀', title:'Your boldest chapter yet', text:'A leap of faith you take this year will define the next decade. Jump anyway.' },
  { emoji:'🌺', title:'Bloom where you are', text:'Growth is not always loud. Quiet, steady progress will take you further than you imagine.' },
  { emoji:'🎯', title:'Focus brings magic', text:'One goal. Full heart. Zero distractions. That formula will unlock something extraordinary for you.' },
  { emoji:'🦋', title:'Transformation awaits', text:'You will shed what no longer serves you and emerge lighter, freer, and more yourself than ever.' },
];

const ZODIACS = [
  { name:'Capricorn', symbol:'♑', dates:'Dec 22 – Jan 19', traits:['Ambitious','Disciplined','Practical'], stars:[[150,60],[120,90],[180,90],[100,130],[200,130],[150,170]] },
  { name:'Aquarius',  symbol:'♒', dates:'Jan 20 – Feb 18', traits:['Visionary','Rebel','Humanitarian'], stars:[[80,80],[130,60],[180,80],[150,120],[100,140],[160,160]] },
  { name:'Pisces',    symbol:'♓', dates:'Feb 19 – Mar 20', traits:['Dreamy','Empathetic','Artistic'], stars:[[100,70],[160,80],[120,120],[180,130],[90,160],[150,170]] },
  { name:'Aries',     symbol:'♈', dates:'Mar 21 – Apr 19', traits:['Bold','Energetic','Leader'], stars:[[150,50],[110,100],[190,100],[130,150],[170,150],[150,200]] },
  { name:'Taurus',    symbol:'♉', dates:'Apr 20 – May 20', traits:['Loyal','Patient','Sensual'], stars:[[150,60],[100,110],[200,110],[120,160],[180,160],[150,200]] },
  { name:'Gemini',    symbol:'♊', dates:'May 21 – Jun 20', traits:['Witty','Curious','Adaptable'], stars:[[100,60],[200,60],[100,110],[200,110],[120,160],[180,160]] },
  { name:'Cancer',    symbol:'♋', dates:'Jun 21 – Jul 22', traits:['Nurturing','Intuitive','Loyal'], stars:[[150,50],[90,100],[210,100],[120,150],[180,150],[150,200]] },
  { name:'Leo',       symbol:'♌', dates:'Jul 23 – Aug 22', traits:['Charismatic','Brave','Creative'], stars:[[150,40],[80,90],[220,90],[100,150],[200,150],[150,210]] },
  { name:'Virgo',     symbol:'♍', dates:'Aug 23 – Sep 22', traits:['Precise','Reliable','Intelligent'], stars:[[150,50],[100,100],[200,100],[130,155],[170,155],[150,200]] },
  { name:'Libra',     symbol:'♎', dates:'Sep 23 – Oct 22', traits:['Balanced','Charming','Fair'], stars:[[80,100],[220,100],[150,60],[130,140],[170,140],[150,200]] },
  { name:'Scorpio',   symbol:'♏', dates:'Oct 23 – Nov 21', traits:['Intense','Passionate','Magnetic'], stars:[[150,50],[90,110],[210,110],[110,160],[190,160],[150,210]] },
  { name:'Sagittarius',symbol:'♐',dates:'Nov 22 – Dec 21', traits:['Adventurous','Optimistic','Free'], stars:[[150,40],[90,100],[210,100],[120,160],[180,160],[150,220]] },
];

function getDefaultNote(name) {
  return `Dearest ${name},\n\nOn this beautiful day, I want you to know how incredibly special you are to me. Your presence makes the world brighter, your laughter is the best music I know, and your kindness inspires everyone around you.\n\nKeep being the extraordinary person you are. Today and every day, you deserve nothing but the absolute best.\n\nWith all my love,`;
}

// ─── DOM Elements & Initialization ────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
    
    /* --- 1. Mouse Glow Swarm & Cursor Tracker --- */
    const mouseGlow = document.getElementById('mouse-glow');
    if (mouseGlow) {
        let targetX = 0;
        let targetY = 0;
        let currentX = 0;
        let currentY = 0;
        const ease = 0.08;
        let targetScale = 1;
        let currentScale = 1;
        let isVisible = false;

        // Position initial offscreen
        mouseGlow.style.opacity = '0';

        // Pre-resolve root font size for rem conversions and handle resize
        let rootFontSize = parseFloat(getComputedStyle(document.documentElement).fontSize) || 16;
        window.addEventListener('resize', () => {
            rootFontSize = parseFloat(getComputedStyle(document.documentElement).fontSize) || 16;
        });

        // Create a pool of 8 colored gradient dots
        const NUM_DOTS = 8;
        const dots = [];
        const dotsData = [];
        let targetDotOpacity = 0;

        for (let i = 0; i < NUM_DOTS; i++) {
            const dot = document.createElement('div');
            dot.className = 'mouse-tracker-dot';
            dot.style.setProperty('--dot-idx', i);
            document.body.appendChild(dot);
            dots.push(dot);

            // Establish angular assignment & harmonic attract-repel bounce properties (never clusters to a single point)
            const baseAngle = i * (Math.PI * 2 / NUM_DOTS);
            
            dotsData.push({
                currentX: targetX + Math.cos(baseAngle) * 50,
                currentY: targetY + Math.sin(baseAngle) * 50,
                currentOpacity: 0,
                baseAngle: baseAngle,
                orbitSpeed: 0.82,
                pulseSpeed: 1.8 + (i % 3) * 0.35,
                phase: i * (Math.PI / 4),
                minDist: 26 + (i % 3) * 5, // closest approach point to cursor
                bounceDist: 62 + (i % 4) * 8, // repelled bounce distance
                ease: 0.16 + (i % 3) * 0.03
            });
        }

        document.addEventListener('mousemove', (e) => {
            targetX = e.clientX;
            targetY = e.clientY;
            ensureGlowLoop();

            const readableTarget = e.target.closest(
                'a, button, p, h1, h2, h3, h4, h5, h6, li, label, code, blockquote, ' +
                'input, textarea, .trait-tag, .section-tag, .badge, .status-txt, ' +
                '.project-type, .stat-label, .secret-text, .bday-title, .bday-desc'
            );
            document.body.classList.toggle('cursor-reading', Boolean(readableTarget));
            targetDotOpacity = readableTarget ? 0 : 0.9;

            if (!isVisible) {
                currentX = targetX;
                currentY = targetY;
                dotsData.forEach(data => {
                    data.currentX = targetX + Math.cos(data.baseAngle) * data.bounceDist;
                    data.currentY = targetY + Math.sin(data.baseAngle) * data.bounceDist;
                });
                isVisible = true;
                mouseGlow.style.opacity = '1';
                dots.forEach(dot => dot.classList.add('active'));
            }
        });

        document.addEventListener('mouseleave', () => {
            mouseGlow.style.opacity = '0';
            targetDotOpacity = 0;
            isVisible = false;
            document.body.classList.remove('cursor-reading');
        });

        // Hover tracking using event delegation
        const readableSelector = [
            'a', 'button', 'input', 'textarea', 'select', 'label',
            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'span',
            '.logo', '.badge', '.trait-tag', '.section-tag', '.section-desc',
            '.project-type', '.status-txt', '.stat-label', '.stat-number',
            '.highlight-text', '.bday-tag', '.bday-title', '.bday-desc'
        ].join(', ');

        const getEventElement = (target) => target instanceof Element ? target : null;
        const isReadableTarget = (target) => {
            const element = getEventElement(target);
            return Boolean(element && element.closest(readableSelector));
        };

        document.addEventListener('mouseover', (e) => {
            const target = e.target;
            document.body.classList.toggle('cursor-reading', isReadableTarget(target));
            const element = getEventElement(target);
            if (element && element.closest('a, button, .glass-card, .skill-tag, .modern-switch, .project-card, .cert-card')) {
                targetScale = 1.35;
            }
        });

        document.addEventListener('mouseout', (e) => {
            const target = e.target;
            const nextTarget = e.relatedTarget;
            document.body.classList.toggle('cursor-reading', isReadableTarget(nextTarget));
            const element = getEventElement(target);
            if (element && element.closest('a, button, .glass-card, .skill-tag, .modern-switch, .project-card, .cert-card')) {
                targetScale = 1.0;
            }
        });

        /* --- [B-03] Crew Mode & Swarm Control API with Multi-Phase Choreography --- */
        let assignedTargets = null;
        let currentPhase = 'idle'; // 'idle' | 'scout' | 'pull'
        let currentPhaseMeta = null;
        let isTouchDevice = window.matchMedia('(hover: none)').matches;
        let lastPointerTime = performance.now();
        let lastTouchTime = performance.now();
        let isGlowLoopRunning = false;

        function ensureGlowLoop() {
            lastPointerTime = performance.now();
            if (!isGlowLoopRunning) {
                isGlowLoopRunning = true;
                requestAnimationFrame(animateGlow);
            }
        }

        window.swarm = {
            setPhase(phase, meta) {
                currentPhase = phase || 'idle';
                currentPhaseMeta = meta || null;
                if (phase === 'scout') {
                    if (!isVisible) {
                        isVisible = true;
                        mouseGlow.style.opacity = '0.7';
                        dots.forEach(dot => dot.classList.add('active'));
                    }
                    targetDotOpacity = 0.95;
                } else if (phase === 'pull') {
                    if (meta && meta.targets) {
                        assignedTargets = meta.targets;
                    }
                    targetDotOpacity = 0.95;
                } else if (phase === 'idle') {
                    assignedTargets = null;
                    currentPhaseMeta = null;
                }
                ensureGlowLoop();
            },
            getPhase() {
                return currentPhase;
            },
            getPhaseMeta() {
                return currentPhaseMeta;
            },
            assign(targets) {
                currentPhase = 'pull';
                assignedTargets = Array.isArray(targets) && targets.length ? targets : null;
                if (!isVisible) {
                    isVisible = true;
                    mouseGlow.style.opacity = '1';
                    dots.forEach(dot => dot.classList.add('active'));
                    targetDotOpacity = 0.95;
                }
                ensureGlowLoop();
            },
            release() {
                currentPhase = 'idle';
                assignedTargets = null;
                currentPhaseMeta = null;
                ensureGlowLoop();
            },
            getDots() {
                return dots;
            },
            getDotsData() {
                return dotsData;
            },
            isAssigned() {
                return Boolean(assignedTargets) || currentPhase === 'pull';
            }
        };

        /* --- [B-04] Touch Support: follow touch point and lower third idle orbit --- */
        window.addEventListener('touchstart', (e) => {
            if (e.touches && e.touches[0]) {
                targetX = e.touches[0].clientX;
                targetY = e.touches[0].clientY;
                lastTouchTime = performance.now();
                if (!isVisible) {
                    isVisible = true;
                    mouseGlow.style.opacity = '0.6';
                    dots.forEach(dot => dot.classList.add('active'));
                    targetDotOpacity = 0.95;
                }
                ensureGlowLoop();
            }
        }, { passive: true });

        window.addEventListener('touchmove', (e) => {
            if (e.touches && e.touches[0]) {
                targetX = e.touches[0].clientX;
                targetY = e.touches[0].clientY;
                lastTouchTime = performance.now();
                ensureGlowLoop();
            }
        }, { passive: true });

        function animateGlow() {
            // Update main background glow
            currentX += (targetX - currentX) * ease;
            currentY += (targetY - currentY) * ease;
            currentScale += (targetScale - currentScale) * 0.15;
            
            // Convert positions to rem
            const glowXRem = currentX / rootFontSize;
            const glowYRem = currentY / rootFontSize;
            mouseGlow.style.transform = `translate3d(${glowXRem}rem, ${glowYRem}rem, 0) translate(-50%, -50%) scale(${currentScale})`;
            
            // Update individual dots in the cluster
            const time = performance.now() * 0.001;

            // [B-04] Touch idle orbit at lower third of viewport
            if (isTouchDevice && !assignedTargets && (currentPhase === 'idle') && (performance.now() - lastTouchTime > 2000)) {
                targetX = window.innerWidth * 0.5 + Math.cos(time * 0.8) * 35;
                targetY = window.innerHeight * 0.78 + Math.sin(time * 0.6) * 20;
            }
            
            for (let i = 0; i < NUM_DOTS; i++) {
                const dot = dots[i];
                const data = dotsData[i];
                
                // Swarming drift offset calculation [B-03 alive in crew mode]
                const driftX = Math.sin(time * data.freqX + data.phaseX) * data.ampX;
                const driftY = Math.cos(time * data.freqY + data.phaseY) * data.ampY;
                
                let targetDotX, targetDotY;

                if (currentPhase === 'scout') {
                    // Phase 1: Scouting reconnaissance sweep across incoming section
                    const tScout = time * 2.8;
                    let cx = window.innerWidth * 0.5;
                    let cy = window.innerHeight * 0.5;
                    if (currentPhaseMeta && currentPhaseMeta.bounds) {
                        const scrollYNow = window.scrollY || window.pageYOffset || 0;
                        cy = (currentPhaseMeta.bounds.pageTop - scrollYNow) + (currentPhaseMeta.bounds.height * 0.35);
                        cx = currentPhaseMeta.bounds.pageLeft + (currentPhaseMeta.bounds.width * 0.5);
                    }
                    const angle = tScout * (1.8 + (i % 3) * 0.6) + (i * Math.PI * 2 / NUM_DOTS);
                    const rx = Math.min(window.innerWidth * 0.38, 220 + (i % 4) * 50);
                    const ry = Math.min(window.innerHeight * 0.28, 140 + (i % 3) * 40);
                    const targetDotX = cx + Math.cos(angle) * rx + Math.sin(tScout * 2.5 + i) * 30;
                    const targetDotY = cy + Math.sin(angle * 1.3) * ry + Math.cos(tScout * 2.0 + i) * 25;
                    data.currentX += (targetDotX - data.currentX) * 0.16;
                    data.currentY += (targetDotY - data.currentY) * 0.16;
                } else if (assignedTargets && assignedTargets.length > 0) {
                    // Priority 1: Multipurpose firefly drones pull and hoist incoming section elements
                    const pt = assignedTargets[i % assignedTargets.length];
                    const targetDotX = pt.x + driftX * 0.5;
                    const targetDotY = pt.y + driftY * 0.5;
                    data.currentX += (targetDotX - data.currentX) * 0.25;
                    data.currentY += (targetDotY - data.currentY) * 0.25;
                } else {
                    // Priority 2: Harmonic Attract & Repel Bounce around Cursor (hover, approach, bounce off, never cluster)
                    const curAngle = data.baseAngle + time * data.orbitSpeed;
                    const cycle = time * data.pulseSpeed + data.phase;
                    const bounceFactor = Math.pow(Math.abs(Math.sin(cycle)), 0.65);
                    const currentDist = data.minDist + bounceFactor * (data.bounceDist - data.minDist);
                    const flutter = Math.sin(time * 3.2 + i * 1.5) * 3.0;

                    const targetDotX = targetX + Math.cos(curAngle) * (currentDist + flutter);
                    const targetDotY = targetY + Math.sin(curAngle) * (currentDist + flutter);

                    data.currentX += (targetDotX - data.currentX) * data.ease;
                    data.currentY += (targetDotY - data.currentY) * data.ease;
                }
                
                data.currentOpacity += (targetDotOpacity - data.currentOpacity) * 0.14;
            }

            // Mutual Dot-to-Dot Electrostatic Repulsion Force: guarantees dots NEVER cluster or touch
            for (let i = 0; i < NUM_DOTS; i++) {
                const di = dotsData[i];
                for (let j = i + 1; j < NUM_DOTS; j++) {
                    const dj = dotsData[j];
                    const dx = di.currentX - dj.currentX;
                    const dy = di.currentY - dj.currentY;
                    const d2 = dx * dx + dy * dy;
                    const minSeparation = 18; // 18px physical exclusion zone
                    if (d2 < minSeparation * minSeparation && d2 > 0.0001) {
                        const dist = Math.sqrt(d2);
                        const push = (minSeparation - dist) * 0.5;
                        const nx = dx / dist;
                        const ny = dy / dist;
                        di.currentX += nx * push;
                        di.currentY += ny * push;
                        dj.currentX -= nx * push;
                        dj.currentY -= ny * push;
                    }
                }
            }

            // Commit final position to DOM
            for (let i = 0; i < NUM_DOTS; i++) {
                const dot = dots[i];
                const data = dotsData[i];
                const dotXRem = data.currentX / rootFontSize;
                const dotYRem = data.currentY / rootFontSize;
                
                dot.style.transform = `translate3d(${dotXRem}rem, ${dotYRem}rem, 0) translate(-50%, -50%)`;
                dot.style.opacity = data.currentOpacity.toFixed(3);
            }

            requestAnimationFrame(animateGlow);
        }

        // Start glow loop
        ensureGlowLoop();
    }

    /* --- 2. Interactive Hanging Lamp & Focused Spotlight Logic --- */
    const lampArm = document.getElementById('lamp-swing-arm');
    const lampRefl = document.getElementById('lamp-reflection');
    const secretDeskSection = document.getElementById('secret-desk');
    const lampSwitch = document.getElementById('lamp-toggle');
    const secretTextEl = document.getElementById('secret-desk-text');
    const secretMsgBtn = document.getElementById('secret-message-btn');

    // Split secret text into individual character spans for pinpoint spotlight projection
    if (secretTextEl) {
        const rawText = secretTextEl.textContent.trim();
        secretTextEl.innerHTML = '';
        for (let i = 0; i < rawText.length; i++) {
            const ch = rawText[i];
            const span = document.createElement('span');
            span.className = 'lamp-char';
            span.textContent = ch;
            if (ch === ' ') {
                span.style.display = 'inline-block';
                span.style.width = '0.35em';
            }
            secretTextEl.appendChild(span);
        }
    }

    if (lampArm && lampRefl && secretDeskSection && lampSwitch) {
        lampSwitch.checked = false;
        secretDeskSection.classList.remove('is-lit');

        let isLampLit = false;
        let angle = 0;
        let chainFlex = 0;
        let swingPhase = 0;
        let isDragging = false;

        let dragStartX = 0;
        let dragStartY = 0;
        let hasMoved = false;

        const getHingePoint = () => {
            const rect = lampArm.getBoundingClientRect();
            return {
                x: rect.left + rect.width / 2,
                y: rect.top
            };
        };

        const handleStart = (clientX, clientY) => {
            isDragging = true;
            hasMoved = false;
            dragStartX = clientX;
            dragStartY = clientY;
        };

        const handleMove = (clientX, clientY) => {
            if (!isDragging) return;
            const dist = Math.hypot(clientX - dragStartX, clientY - dragStartY);
            if (dist > 6) {
                hasMoved = true;
            }
            const hinge = getHingePoint();
            const dx = clientX - hinge.x;
            const dy = clientY - hinge.y;
            let dragAngle = Math.atan2(dx, Math.max(dy, 30)) * (180 / Math.PI);
            dragAngle = Math.max(-25, Math.min(25, dragAngle));
            angle = dragAngle;
        };

        const handleEnd = () => {
            if (isDragging && !hasMoved) {
                // User clicked the lamp without dragging - toggle the light!
                lampSwitch.checked = !lampSwitch.checked;
                lampSwitch.dispatchEvent(new Event('change'));
            }
            isDragging = false;
        };

        const lampStructure = lampArm.querySelector('.lamp-structure');
        if (lampStructure) {
            lampStructure.style.cursor = 'pointer';
            lampStructure.addEventListener('mousedown', (e) => {
                e.preventDefault();
                handleStart(e.clientX, e.clientY);
            });
            lampStructure.addEventListener('touchstart', (e) => {
                if (e.touches.length > 0) {
                    handleStart(e.touches[0].clientX, e.touches[0].clientY);
                }
            }, { passive: true });
        }

        document.addEventListener('mousemove', (e) => {
            if (isDragging) {
                handleMove(e.clientX, e.clientY);
            }
        });
        document.addEventListener('touchmove', (e) => {
            if (isDragging && e.touches.length > 0) {
                handleMove(e.touches[0].clientX, e.touches[0].clientY);
            }
        }, { passive: true });
        document.addEventListener('mouseup', handleEnd);
        document.addEventListener('touchend', handleEnd);

        lampSwitch.addEventListener('change', () => {
            isLampLit = lampSwitch.checked;
            if (isLampLit) {
                secretDeskSection.classList.add('is-lit');
            } else {
                secretDeskSection.classList.remove('is-lit');
                if (secretTextEl) {
                    secretTextEl.querySelectorAll('.lamp-char').forEach(span => {
                        span.style.opacity = '';
                        span.style.color = '';
                        span.style.textShadow = '';
                        span.style.transform = '';
                    });
                }
                if (secretMsgBtn) {
                    secretMsgBtn.style.opacity = '';
                    secretMsgBtn.style.boxShadow = '';
                    secretMsgBtn.style.borderColor = '';
                }
            }
        });

        function swingLoop() {
            if (!isDragging) {
                if (isLampLit) {
                    // Gentle, graceful pendulum toggle right and left (~4.2s period, max +/- 6.8 deg)
                    swingPhase += 0.016;
                    const targetAngle = Math.sin(swingPhase) * 6.8;
                    angle += (targetAngle - angle) * 0.045;
                    chainFlex += (-angle * 0.1 - chainFlex) * 0.06;
                } else {
                    // Settle gently back to center 0 deg when switched off
                    angle += (0 - angle) * 0.06;
                    chainFlex += (0 - chainFlex) * 0.08;
                }
            } else {
                chainFlex += (-angle * 0.18 - chainFlex) * 0.12;
            }

            lampArm.style.transform = `rotate(${angle.toFixed(2)}deg) skewX(${chainFlex.toFixed(2)}deg)`;

            const shiftX = -Math.sin(angle * Math.PI / 180) * 140;
            lampRefl.style.transform = `translateX(calc(-50% + ${shiftX.toFixed(1)}px))`;

            // Spotlight intersection: smooth cosine blending on characters
            if (isLampLit && secretTextEl) {
                const hinge = getHingePoint();
                const textRect = secretTextEl.getBoundingClientRect();
                const H = Math.max(180, textRect.top + textRect.height / 2 - hinge.y);
                const beamCenterX = hinge.x + H * Math.tan(angle * Math.PI / 180);
                const beamRadius = 145; // Soft diffused spotlight radius

                const spans = secretTextEl.querySelectorAll('.lamp-char');
                spans.forEach(span => {
                    const r = span.getBoundingClientRect();
                    const charX = r.left + r.width / 2;
                    const dist = Math.abs(charX - beamCenterX);

                    if (dist < beamRadius) {
                        const norm = dist / beamRadius;
                        const factor = 0.5 * (1 + Math.cos(norm * Math.PI)); // 1.0 at center, smooth 0 at edge
                        span.style.opacity = (0.25 + 0.75 * factor).toFixed(2);
                        span.style.color = '#ffffff';
                        span.style.textShadow = `0 0 ${Math.round(10 * factor)}px #ffd873, 0 0 ${Math.round(22 * factor)}px #19e3d0`;
                        span.style.transform = `scale(${(1 + 0.12 * factor).toFixed(2)})`;
                    } else {
                        span.style.opacity = '0.2';
                        span.style.color = 'rgba(180, 150, 220, 0.4)';
                        span.style.textShadow = 'none';
                        span.style.transform = 'scale(1)';
                    }
                });

                if (secretMsgBtn) {
                    const btnRect = secretMsgBtn.getBoundingClientRect();
                    const btnX = btnRect.left + btnRect.width / 2;
                    const btnDist = Math.abs(btnX - beamCenterX);
                    const btnThreshold = beamRadius + btnRect.width * 0.4;
                    if (btnDist < btnThreshold) {
                        const norm = btnDist / btnThreshold;
                        const factor = 0.5 * (1 + Math.cos(norm * Math.PI));
                        secretMsgBtn.style.opacity = (0.5 + 0.5 * factor).toFixed(2);
                        secretMsgBtn.style.boxShadow = `0 0 ${Math.round(24 * factor)}px rgba(25, 227, 208, 0.65), inset 0 0 ${Math.round(14 * factor)}px rgba(242, 193, 78, 0.4)`;
                        secretMsgBtn.style.borderColor = factor > 0.35 ? 'var(--cp-turquoise)' : 'rgba(242, 193, 78, 0.5)';
                    } else {
                        secretMsgBtn.style.opacity = '0.35';
                        secretMsgBtn.style.boxShadow = 'none';
                        secretMsgBtn.style.borderColor = 'rgba(255, 255, 255, 0.2)';
                    }
                }
            }

            requestAnimationFrame(swingLoop);
        }

        requestAnimationFrame(swingLoop);
    }

    /* --- 2. Navbar Scroll and Active tracking --- */
    const navbar = document.getElementById('navbar');
    const backToTop = document.querySelector('.back-to-top');
    const sections = document.querySelectorAll('section, footer');
    const navLinks = document.querySelectorAll('.nav-link');

    const handleNavbarScroll = () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    };

    // Initialize navbar class on page load
    handleNavbarScroll();

    /* --- Modern Butter-Smooth Momentum Scrolling Engine --- */
    (function initSmoothMomentumScroll() {
        // Step aside on coarse/touch devices to preserve 120Hz native touch momentum
        const isTouch = ('ontouchstart' in window) || (navigator.maxTouchPoints > 0) || window.matchMedia('(hover: none)').matches;
        if (isTouch) return;

        let currentScrollY = window.scrollY || window.pageYOffset || 0;
        let targetScrollY = currentScrollY;
        let isScrolling = false;
        let maxScroll = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);

        function updateMaxScroll() {
            maxScroll = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
        }
        window.addEventListener('resize', updateMaxScroll, { passive: true });

        // Wheel interceptor with normalized delta & inertial decay
        window.addEventListener('wheel', (e) => {
            if (e.ctrlKey || e.metaKey || e.altKey) return;
            if (e.target.closest('#nano-chat-messages, .wishes-scroll-box, .modal-content, textarea')) return;

            e.preventDefault();
            updateMaxScroll();

            let delta = e.deltaY;
            if (e.deltaMode === 1) delta *= 32;
            else if (e.deltaMode === 2) delta *= window.innerHeight;

            targetScrollY = Math.max(0, Math.min(maxScroll, targetScrollY + delta * 0.95));

            if (!isScrolling) {
                isScrolling = true;
                requestAnimationFrame(scrollLoop);
            }
        }, { passive: false });

        function scrollLoop() {
            const diff = targetScrollY - currentScrollY;
            if (Math.abs(diff) > 0.4) {
                currentScrollY += diff * 0.082;
                window.scrollTo(0, currentScrollY);
                requestAnimationFrame(scrollLoop);
            } else {
                currentScrollY = targetScrollY;
                window.scrollTo(0, targetScrollY);
                isScrolling = false;
            }
        }

        window.addEventListener('scroll', () => {
            if (!isScrolling) {
                currentScrollY = window.scrollY || window.pageYOffset || 0;
                targetScrollY = currentScrollY;
            }
        }, { passive: true });

        // Keyboard navigation
        window.addEventListener('keydown', (e) => {
            if (['input', 'textarea'].includes(document.activeElement.tagName.toLowerCase())) return;

            updateMaxScroll();
            let keyDelta = 0;
            if (e.key === 'ArrowDown') keyDelta = 110;
            else if (e.key === 'ArrowUp') keyDelta = -110;
            else if (e.key === 'PageDown' || (e.key === ' ' && !e.shiftKey)) keyDelta = window.innerHeight * 0.78;
            else if (e.key === 'PageUp' || (e.key === ' ' && e.shiftKey)) keyDelta = -window.innerHeight * 0.78;
            else if (e.key === 'Home') keyDelta = -currentScrollY;
            else if (e.key === 'End') keyDelta = maxScroll - currentScrollY;

            if (keyDelta !== 0) {
                e.preventDefault();
                targetScrollY = Math.max(0, Math.min(maxScroll, targetScrollY + keyDelta));
                if (!isScrolling) {
                    isScrolling = true;
                    requestAnimationFrame(scrollLoop);
                }
            }
        });

        // Anchor links smooth glide
        document.addEventListener('click', (e) => {
            const anchor = e.target.closest('a[href^="#"]');
            if (!anchor) return;
            const hash = anchor.getAttribute('href');
            if (!hash || hash === '#') return;
            const targetEl = document.querySelector(hash);
            if (targetEl) {
                e.preventDefault();
                updateMaxScroll();
                const navHeight = 70;
                const rect = targetEl.getBoundingClientRect();
                const scrollOffset = rect.top + (window.scrollY || window.pageYOffset) - navHeight;
                targetScrollY = Math.max(0, Math.min(maxScroll, scrollOffset));
                if (!isScrolling) {
                    isScrolling = true;
                    requestAnimationFrame(scrollLoop);
                }
                history.pushState(null, '', hash);
            }
        });

        window.glideScrollTo = function(y) {
            updateMaxScroll();
            targetScrollY = Math.max(0, Math.min(maxScroll, y));
            if (!isScrolling) {
                isScrolling = true;
                requestAnimationFrame(scrollLoop);
            }
        };
    })();

    window.addEventListener('scroll', () => {
        handleNavbarScroll();

        // Smooth parallax fade for hero content on scroll (zero GPU composite strain)
        const scrolled = window.scrollY;
        const heroHeight = window.innerHeight;
        const headerContent = document.querySelector('.header-content');
        if (headerContent && scrolled <= heroHeight) {
            const percent = scrolled / heroHeight;
            headerContent.style.opacity = (1 - percent * 0.92).toFixed(3);
            headerContent.style.transform = `translate3d(0, ${(percent * 45).toFixed(1)}px, 0)`;
        }

        // Back to top visibility
        if (backToTop) {
            if (window.scrollY > 800) {
                backToTop.style.opacity = '1';
                backToTop.style.pointerEvents = 'auto';
            } else {
                backToTop.style.opacity = '0';
                backToTop.style.pointerEvents = 'none';
            }
        }

        // Active link tracking
        let current = '';
        sections.forEach(sec => {
            const top = sec.offsetTop;
            const height = sec.clientHeight;
            if (window.scrollY >= top - 200) {
                current = sec.getAttribute('id');
            }
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });

    /* --- 3. Mobile Burger Menu Toggle --- */
    const burger = document.querySelector('.burger');
    const navContainer = document.querySelector('.nav-container'); 
    
    if (burger) {
        burger.addEventListener('click', () => {
            navContainer.classList.toggle('nav-active');
            burger.classList.toggle('toggle');
        });
    }

    // Close menu when clicking navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navContainer.classList.remove('nav-active');
            if (burger) burger.classList.remove('toggle');
        });
    });

    /* --- 5. Project Grid Category Filtering --- */
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card');

    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            filterButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            const filterValue = button.getAttribute('data-filter');

            projectCards.forEach(card => {
                const cardCategory = card.getAttribute('data-category');

                if (filterValue === 'all' || cardCategory === filterValue) {
                    card.style.display = 'flex';
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0) scale(1)';
                    }, 50);
                } else {
                    card.style.opacity = '0';
                    card.style.transform = 'translateY(20px) scale(0.95)';
                    setTimeout(() => {
                        card.style.display = 'none';
                    }, 350);
                }
            });
        });
    });

    // Mock widgets inside Nova UI Design System card
    const toggleEl = document.querySelector('.ux-toggle');
    if (toggleEl) {
        toggleEl.addEventListener('click', () => {
            toggleEl.classList.toggle('active');
        });
    }

    /* --- 6. Stats Animation & Scroll Reveal --- */
    const statsNumbers = document.querySelectorAll('.stat-number');
    let animatedStats = false;

    function animateCounters() {
        if (animatedStats) return;
        statsNumbers.forEach(stat => {
            const target = parseInt(stat.getAttribute('data-target'), 10);
            let current = 0;
            const duration = 1500;
            const stepTime = Math.max(Math.floor(duration / target), 15);
            
            const counterInterval = setInterval(() => {
                current += Math.ceil(target / 25);
                if (current >= target) {
                    current = target;
                    clearInterval(counterInterval);
                }
                stat.textContent = stat.getAttribute('data-target') > 90 ? `${current}%` : `${current}+`;
            }, stepTime);
        });
        animatedStats = true;
    }
    window.animateCounters = animateCounters;

    const revealElements = document.querySelectorAll('.scroll-reveal');
    let revealQueue = [];
    let revealTimeout = null;

    function processRevealQueue() {
        if (revealQueue.length === 0) return;
        
        // Sort elements by their vertical offset top to ensure top-to-bottom sequence
        revealQueue.sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top);

        revealQueue.forEach((el, index) => {
            setTimeout(() => {
                el.classList.add('active');
                if (el.classList.contains('section-padding') && el.id === 'about-me') {
                    animateCounters();
                }
            }, index * 80); // Stagger by 80ms for a crisp, fast entry
        });
        revealQueue = [];
    }

    const revealObserver = new IntersectionObserver((entries) => {
        // [C-04] When Pull-to-Build is active, reveals are gated to section snap
        if (document.documentElement.classList.contains('nb-ready') && !document.documentElement.classList.contains('nb-done')) {
            return;
        }
        let added = false;
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                if (!el.classList.contains('active') && !revealQueue.includes(el)) {
                    revealQueue.push(el);
                    revealObserver.unobserve(el);
                    added = true;
                }
            }
        });
        if (added) {
            if (revealTimeout) clearTimeout(revealTimeout);
            revealTimeout = setTimeout(processRevealQueue, 30); // 30ms debounce window
        }
    }, { threshold: 0.12 });

    revealElements.forEach(el => revealObserver.observe(el));

    /* --- 7. Human-Cadence Cyberpunk Typewriter Sequence --- */
    function typeHuman(element, text, baseSpeed = 70) {
        return new Promise((resolve) => {
            let i = 0;
            element.textContent = '';
            function step() {
                if (i < text.length) {
                    const char = text.charAt(i);
                    element.textContent += char;
                    i++;
                    // Natural human typing rhythm variation
                    let delay = baseSpeed * (0.75 + Math.random() * 0.65);
                    if (char === ' ') delay += 50;
                    if (char === ',' || char === '.' || char === '|' || char === '&') delay += 130;
                    setTimeout(step, delay);
                } else {
                    resolve();
                }
            }
            step();
        });
    }

    function backspaceText(element, speed = 20) {
        return new Promise((resolve) => {
            function step() {
                const current = element.textContent;
                if (current.length > 0) {
                    element.textContent = current.slice(0, -1);
                    setTimeout(step, speed);
                } else {
                    resolve();
                }
            }
            step();
        });
    }

    function setupHero3dNamePhysics(nameEl) {
        if (!nameEl) return;
        const text = "YASER HUSEN";
        const words = text.split(' ');
        nameEl.innerHTML = words.map(word => {
            const chars = word.split('').map(c => `<span class="hero-3d-char" data-char="${c}">${c}</span>`).join('');
            return `<span class="hero-3d-word">${chars}</span>`;
        }).join(' ');

        const charSpans = nameEl.querySelectorAll('.hero-3d-char');
        if (!charSpans.length) return;

        window.addEventListener('mousemove', (e) => {
            const mx = e.clientX;
            const my = e.clientY;
            const repelRadius = 85;

            charSpans.forEach(span => {
                const rect = span.getBoundingClientRect();
                const cx = rect.left + rect.width * 0.5;
                const cy = rect.top + rect.height * 0.5;
                const dx = cx - mx;
                const dy = cy - my;
                const dist = Math.hypot(dx, dy);

                if (dist < repelRadius && dist > 0) {
                    const force = Math.pow(1 - dist / repelRadius, 1.4) * 32;
                    const nx = dx / dist;
                    const ny = dy / dist;
                    const tx = nx * force;
                    const ty = ny * force;
                    const rotZ = (nx * 14).toFixed(1);
                    const rotX = (-ny * 20).toFixed(1);

                    span.style.transform = `translate3d(${tx.toFixed(1)}px, ${ty.toFixed(1)}px, 20px) rotateZ(${rotZ}deg) rotateX(${rotX}deg) scale(1.15)`;
                    span.classList.add('is-repelled');
                } else {
                    span.style.transform = '';
                    span.classList.remove('is-repelled');
                }
            });
        }, { passive: true });
    }

    async function startHeroAnimations() {
        const nameEl = document.getElementById('tp-name');
        const subtitleEl = document.getElementById('tp-subtitle');
        const aboutEl = document.getElementById('tp-about');
        
        const nameCursor = document.getElementById('name-cursor');
        const subtitleCursor = document.getElementById('subtitle-cursor');
        const aboutCursor = document.getElementById('about-cursor');
        const detailsContainer = document.getElementById('hero-details');

        if (!nameEl) return;

        // Step 1: Type Yaser Husen with authentic human keystrokes
        if (nameCursor) nameCursor.classList.remove('hidden');
        await typeHuman(nameEl, "YASER HUSEN", 85);
        if (nameCursor) nameCursor.classList.add('hidden');

        // Transform into 3D interactive character blocks with mouse physics
        setupHero3dNamePhysics(nameEl);

        // Step 2: Reveal trait tags and about card
        if (detailsContainer) {
            detailsContainer.classList.add('reveal');
        }

        // Step 3: Type description
        if (aboutEl && aboutCursor) {
            aboutCursor.classList.remove('hidden');
            await typeHuman(aboutEl, "I bridge technical data science, scalable artificial intelligence, and high-velocity web platforms to build unified intelligent systems.", 35);
            aboutCursor.classList.add('hidden');
        }

        // Step 4: Continuous rotating dynamic skill titles
        const SKILL_TITLES = [
            "Prompt Engineering & LLM Architecture",
            "AI Systems & API Pipeline Integration",
            "Data Science, Machine Learning & Analytics",
            "Advanced SQL Analytics & Predictive Modeling",
            "High-Performance 3D Web & Intelligent Systems"
        ];

        let titleIndex = 0;
        async function loopTitles() {
            if (!subtitleEl) return;
            if (subtitleCursor) subtitleCursor.classList.remove('hidden');

            while (true) {
                const titleToType = SKILL_TITLES[titleIndex % SKILL_TITLES.length];
                await typeHuman(subtitleEl, titleToType, 50);
                // Pause to let visitor read comfortably
                await new Promise(r => setTimeout(r, 2600));
                // Smooth backspacing
                await backspaceText(subtitleEl, 20);
                await new Promise(r => setTimeout(r, 450));
                titleIndex++;
            }
        }

        loopTitles();
    }

    startHeroAnimations();

    /* --- 8. Contact Form Mock Submission --- */
    const contactForm = document.getElementById('contact-form');
    const formStatus = document.getElementById('form-status');
    const submitBtn = document.getElementById('submit-btn');

    if (contactForm && formStatus && submitBtn) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();

            submitBtn.disabled = true;
            const originalBtnHtml = submitBtn.innerHTML;
            submitBtn.innerHTML = `<span>Sending...</span> <i class="fa-solid fa-spinner fa-spin"></i>`;
            formStatus.className = 'form-status';
            formStatus.textContent = '';

            const name = document.getElementById('name').value.trim();
            const email = document.getElementById('email').value.trim();
            const subject = document.getElementById('subject').value.trim();
            const message = document.getElementById('message').value.trim();

            if (!name || !email || !subject || !message) {
                setTimeout(() => {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalBtnHtml;
                    formStatus.className = 'form-status error';
                    formStatus.textContent = 'Please fill out all fields.';
                    if (window.PortfolioSounds) window.PortfolioSounds.playError();
                }, 600);
                return;
            }

            // Simulate server request delay
            setTimeout(() => {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalBtnHtml;
                formStatus.className = 'form-status success';
                formStatus.textContent = 'Message sent! Yaser will contact you shortly.';
                if (window.PortfolioSounds) window.PortfolioSounds.playSuccess();
                
                contactForm.reset();
                setTimeout(() => { 
                    formStatus.textContent = ''; 
                    const modal = document.getElementById('contact-modal');
                    if (modal) modal.classList.remove('active');
                }, 2500);
            }, 1800);
        });
    }

    /* --- 8b. Contact Pop-up Modal Logic --- */
    const contactModal = document.getElementById('contact-modal');
    const closeContactModal = document.getElementById('close-contact-modal');
    const contactTriggers = [];

    const footerTrigger = document.getElementById('contact-trigger-btn');
    if (footerTrigger) contactTriggers.push(footerTrigger);

    const navContactLinks = document.querySelectorAll('a[href="#contact"]');
    navContactLinks.forEach(link => contactTriggers.push(link));

    if (contactModal && closeContactModal) {
        contactTriggers.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                contactModal.classList.add('active');
                if (window.PortfolioSounds) window.PortfolioSounds.playClick();
            });
        });

        closeContactModal.addEventListener('click', (e) => {
            e.stopPropagation();
            contactModal.classList.remove('active');
            if (window.PortfolioSounds) window.PortfolioSounds.playClick();
        });

        contactModal.addEventListener('click', (e) => {
            if (e.target === contactModal) {
                contactModal.classList.remove('active');
                if (window.PortfolioSounds) window.PortfolioSounds.playClick();
            }
        });
    }

    /* --- 9. Check URL Parameters for Auto-Launch of Birthday Lab --- */
    const params = new URLSearchParams(window.location.search);
    const urlName = params.get('name');
    const urlDOB  = params.get('dob');

    if (urlName && urlDOB) {
        personName = urlName;
        personDOB  = urlDOB;
        personAge  = calculateAge(urlDOB);
        launchMainPage();
        return;
    }

    const sName = sessionStorage.getItem('bdayName');
    const sDOB  = sessionStorage.getItem('bdayDOB');
    if (sName && sDOB) {
        personName = sName;
        personDOB  = sDOB;
        personAge  = calculateAge(sDOB);
        launchMainPage();
    }

    // Initialize cosmic background starting from the about section
    if (typeof initCosmicBackground === 'function') {
        initCosmicBackground();
    }

    /* --- 10. Kinetic Cyberpunk Hero Row & Audio-Reactive Visualizer --- */
    function initHeroKineticCollage() {
        // A. Live UTC Precision Clock
        const clockEl = document.getElementById('clock-utc');
        if (clockEl) {
            const updateClock = () => {
                const d = new Date();
                const hh = String(d.getUTCHours()).padStart(2, '0');
                const mm = String(d.getUTCMinutes()).padStart(2, '0');
                const ss = String(d.getUTCSeconds()).padStart(2, '0');
                clockEl.textContent = `UTC ${hh}:${mm}:${ss}`;
            };
            updateClock();
            setInterval(updateClock, 1000);
        }
    }
    initHeroKineticCollage();

    /* --- 11. Project Cards 3D Parallax Tilt & Specular Sweep --- */
    function initProjectCardTilt() {
        const cards = document.querySelectorAll('.project-card');
        cards.forEach(card => {
            let ticking = false;
            let targetNormX = 0;
            let targetNormY = 0;
            let targetPxX = 0;
            let targetPxY = 0;

            const handleMove = (e) => {
                const rect = card.getBoundingClientRect();
                const mouseX = e.clientX - rect.left;
                const mouseY = e.clientY - rect.top;
                targetNormX = ((mouseX / rect.width) - 0.5) * 2;
                targetNormY = ((mouseY / rect.height) - 0.5) * 2;
                targetPxX = mouseX;
                targetPxY = mouseY;

                if (!ticking) {
                    ticking = true;
                    requestAnimationFrame(() => {
                        card.style.setProperty('--tilt-x', targetNormX.toFixed(3));
                        card.style.setProperty('--tilt-y', targetNormY.toFixed(3));
                        card.style.setProperty('--card-mouse-x', `${targetPxX.toFixed(1)}px`);
                        card.style.setProperty('--card-mouse-y', `${targetPxY.toFixed(1)}px`);
                        ticking = false;
                    });
                }
            };

            const handleLeave = () => {
                card.style.setProperty('--tilt-x', '0');
                card.style.setProperty('--tilt-y', '0');
                card.style.setProperty('--card-mouse-x', '50%');
                card.style.setProperty('--card-mouse-y', '50%');
            };

            card.addEventListener('mousemove', handleMove, { passive: true });
            card.addEventListener('mouseleave', handleLeave, { passive: true });
        });
    }
    initProjectCardTilt();
});


// ════════════════════════════════════════════════════════════
//  INTERACTIVE BIRTHDAY APP LOGIC (GLOBAL METHODS)
// ════════════════════════════════════════════════════════════

function startWishing() {
  const nameInput = document.getElementById('inputName');
  const dobInput  = document.getElementById('inputDOB');

  const name = nameInput.value.trim();
  const dob  = dobInput.value;

  if (!name) { 
    showToast('Please enter their name 🌸'); 
    nameInput.focus(); 
    if (window.PortfolioSounds) window.PortfolioSounds.playError();
    return; 
  }
  if (!dob) { 
    showToast('Please enter their date of birth 🎂'); 
    dobInput.focus(); 
    if (window.PortfolioSounds) window.PortfolioSounds.playError();
    return; 
  }

  personName = name;
  personDOB  = dob;
  personAge  = calculateAge(dob);

  sessionStorage.setItem('bdayName', name);
  sessionStorage.setItem('bdayDOB',  dob);

  launchMainPage();
}

function launchMainPage() {
  const overlay = document.getElementById('birthday-overlay');
  overlay.style.display = 'block';
  setTimeout(() => {
    overlay.classList.add('active');
  }, 50);

  // Lock scroll on main portfolio body
  document.body.style.overflow = 'hidden';

  populatePage();
  spawnFloatingEmojis();
  launchEntryConfetti();
  startBgMusic();

  const closeBtn = document.getElementById('close-birthday-lab');
  if (closeBtn) {
      closeBtn.onclick = () => {
          overlay.classList.remove('active');
          document.body.style.overflow = 'auto';
          
          // Stop mic streams if listening
          if (micStream) {
              micStream.getTracks().forEach(track => track.stop());
          }
          
          // Pause and reset audio
          const music = document.getElementById('bgMusic');
          if (music) { music.pause(); music.currentTime = 0; }
          
          setTimeout(() => {
              overlay.style.display = 'none';
          }, 600);
      };
  }
}

function calculateAge(dob) {
  const today = new Date();
  const birth  = new Date(dob);
  let age = today.getFullYear() - birth.getFullYear();
  const m = today.getMonth() - birth.getMonth();
  if (m < 0 || (m === 0 && today.getDate() < birth.getDate())) age--;
  return Math.max(age, 0);
}

function formatDate(dob) {
  const d = new Date(dob + 'T00:00:00');
  return d.toLocaleDateString('en-IN', { day: 'numeric', month: 'long', year: 'numeric' });
}

function populatePage() {
  document.getElementById('navName').textContent = personName;
  const hbND = document.getElementById('hbNameDisplay');
  if (hbND) hbND.textContent = personName;

  document.getElementById('ageBadge').textContent  = `🎂 Turning ${personAge} Today!`;
  document.getElementById('heroName').textContent   = personName;
  document.getElementById('heroDate').textContent   = ` Born: ${formatDate(personDOB)}`;
  
  // Clean count countdown element duplication
  const strip = document.querySelector('.next-bday-strip');
  if (strip) strip.remove();
  
  startNextBdayCountdown(personDOB);

  document.querySelectorAll('.dynamic-name').forEach(el => el.textContent = personName);

  const saved = localStorage.getItem('bdayNote_' + personName);
  document.getElementById('noteText').textContent = saved || getDefaultNote(personName);
  document.getElementById('noteSig').textContent  = `— With Love 💖`;

  renderWishes();

  const url = `${window.location.origin}${window.location.pathname}?name=${encodeURIComponent(personName)}&dob=${encodeURIComponent(personDOB)}`;
  document.getElementById('shareUrl').textContent = url;

  document.title = ` Happy Birthday, ${personName}!`;
  
  // Init 3D features
  setTimeout(() => {
      window._cakeCandleCount = Math.min(Math.max(personAge || 5, 1), 10);
      totalCandles = window._cakeCandleCount;
      candlesOut = 0;
      if (typeof initCake3D === 'function') initCake3D();
  }, 300);

  setTimeout(() => {
      if (typeof initGift3D === 'function') initGift3D();
  }, 450);

  startFunStats(personDOB);
  initZodiac(personDOB);

  // Scroll observe inside wishes
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, { threshold: 0.1 });
  
  setTimeout(() => {
      document.querySelectorAll('.gif-card, .wish-card').forEach(el => observer.observe(el));
  }, 600);
}

function renderWishes() {
  const grid = document.getElementById('wishesGrid');
  if (!grid) return;
  
  grid.innerHTML = wishesData.map((w, i) => `
    <div class="wish-card" style="transition-delay:${i * 50}ms">
      <span class="wish-icon">${w.icon}</span>
      <div class="wish-title">${w.title}</div>
      <p class="wish-text">${w.text.replace(/you/g, personName || 'you')}</p>
    </div>
  `).join('');
}

function saveNote() {
  const val = document.getElementById('customNote').value.trim();
  if (!val) { 
    showToast('Please write something first ✏️'); 
    if (window.PortfolioSounds) window.PortfolioSounds.playError();
    return; 
  }
  localStorage.setItem('bdayNote_' + personName, val);
  document.getElementById('noteText').textContent = val;
  showToast('Note saved! 💾');
  if (window.PortfolioSounds) window.PortfolioSounds.playSuccess();
}

function startBgMusic() {
  const music = document.getElementById('bgMusic');
  if (!music) return;
  music.volume = 0.35;
  if (window.PortfolioSounds && window.PortfolioSounds.isMuted()) {
    music.muted = true;
  } else {
    music.muted = false;
  }
  const playPromise = music.play();
  if (playPromise !== undefined) {
    playPromise.catch(() => {
      const tryPlay = () => {
        music.play().catch(() => {});
        document.removeEventListener('click', tryPlay);
        document.removeEventListener('touchstart', tryPlay);
      };
      document.addEventListener('click', tryPlay, { once: true });
      document.addEventListener('touchstart', tryPlay, { once: true });
    });
  }
}

function spawnFloatingEmojis() {
  const container = document.getElementById('floatingEmojis');
  if (!container) return;
  
  container.innerHTML = '';
  const emojis = ['🎉','🎊','✨','🌟','💖','🎂','🎁','🌸','💫','🎈','💕'];
  for (let i = 0; i < 15; i++) {
    const el = document.createElement('span');
    el.className = 'floating-emoji';
    el.textContent = emojis[Math.floor(Math.random() * emojis.length)];
    el.style.left = `${Math.random() * 100}%`;
    el.style.animationDelay = `${Math.random() * 5}s`;
    el.style.animationDuration = `${6 + Math.random() * 5}s`;
    el.style.fontSize = `${1 + Math.random() * 0.8}rem`;
    container.appendChild(el);
  }
}

function launchEntryConfetti() {
    // Confetti simulation using emoji bursts
    setTimeout(spawnEmojiBurst, 600);
    setTimeout(spawnEmojiBurst, 1800);
}

function triggerCelebrate() {
  const btn = document.getElementById('celebrateBtn');
  if (btn) {
    btn.classList.add('celebrate-pop');
    setTimeout(() => btn.classList.remove('celebrate-pop'), 600);
  }
  spawnEmojiBurst();
}

function spawnEmojiBurst() {
  const burst = ['🎆','✨','🎊','🎉','💥','🌟','🎈'];
  const container = document.body;
  const cx = window.innerWidth / 2;
  const cy = window.innerHeight / 2;

  for (let i = 0; i < 15; i++) {
    const el = document.createElement('span');
    el.className = 'burst-emoji';
    el.textContent = burst[Math.floor(Math.random() * burst.length)];
    el.style.cssText = `
      position: fixed;
      left: ${cx}px;
      top: ${cy}px;
      font-size: ${1.2 + Math.random() * 1.5}rem;
      pointer-events: none;
      z-index: 99999;
      transform: translate(-50%, -50%);
    `;
    container.appendChild(el);

    const angle = (i / 15) * Math.PI * 2 + (Math.random() - 0.5) * 0.3;
    const dist  = 100 + Math.random() * 150;
    const dx    = Math.cos(angle) * dist;
    const dy    = Math.sin(angle) * dist;

    requestAnimationFrame(() => {
      el.style.transition = `transform ${0.6 + Math.random() * 0.4}s ease-out, opacity 0.5s ease-in`;
      el.style.transform  = `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px)) scale(1.4)`;
      el.style.opacity    = '0';
    });

    setTimeout(() => el.remove(), 1200);
  }
}

function handlePhotoUploads(input) {
  const files = Array.from(input.files).slice(0, 4);
  if (files.length === 0) return;

  galleryPhotos = [];
  const previews = document.querySelectorAll('.upload-preview-img');
  previews.forEach(p => { p.src = ''; p.style.display = 'none'; });

  let loaded = 0;
  files.forEach((file, i) => {
    const reader = new FileReader();
    reader.onload = function (e) {
      galleryPhotos[i] = e.target.result;
      if (previews[i]) {
        previews[i].src = e.target.result;
        previews[i].style.display = 'block';
      }
      loaded++;
      const label = document.getElementById('uploadLabel');
      if (label) label.textContent = `${loaded} photo${loaded > 1 ? 's' : ''} selected ✅`;
    };
    reader.readAsDataURL(file);
  });
}

function openGalleryShow() {
  if (galleryPhotos.length === 0) {
    showToast('Please upload some memory photos first 📸');
    return;
  }
  if (galleryRunning) return;
  galleryRunning = true;

  const overlay = document.getElementById('galleryOverlay');
  const img     = document.getElementById('galleryShowImg');
  const counter = document.getElementById('galleryCounter');

  overlay.style.display = 'flex';
  requestAnimationFrame(() => { overlay.classList.add('active'); });

  function showPhoto(i) {
    if (i >= galleryPhotos.length) {
      overlay.classList.remove('active');
      setTimeout(() => {
        overlay.style.display = 'none';
        galleryRunning = false;
        img.classList.remove('photo-popup');
        img.src = '';
      }, 500);
      return;
    }

    counter.textContent = `${i + 1} / ${galleryPhotos.length}`;
    img.classList.remove('photo-popup');
    img.style.opacity = '0';
    img.src = galleryPhotos[i];

    img.onload = function () {
      requestAnimationFrame(() => {
        img.style.opacity = '1';
        img.classList.add('photo-popup');
      });

      setTimeout(() => {
        img.classList.remove('photo-popup');
        img.classList.add('photo-exit');
        setTimeout(() => {
          img.classList.remove('photo-exit');
          showPhoto(i + 1);
        }, 400);
      }, 2400);
    };

    img.onerror = function () {
      setTimeout(() => showPhoto(i + 1), 300);
    };
  }

  showPhoto(0);
}

function startNextBdayCountdown(dobStr) {
  const strip = document.createElement('div');
  strip.className = 'next-bday-strip';
  strip.innerHTML = '<span class="nbs-label">🎂 Next birthday in</span> <span class="nbs-val" id="nbsVal">…</span>';

  const heroDate = document.getElementById('heroDate');
  if (heroDate && heroDate.parentNode) {
    heroDate.parentNode.insertBefore(strip, heroDate.nextSibling);
  }

  function update() {
    const now  = new Date();
    const dob  = new Date(dobStr);
    let next   = new Date(now.getFullYear(), dob.getMonth(), dob.getDate());
    if (next <= now) next.setFullYear(now.getFullYear() + 1);

    const diff = next - now;
    const days = Math.floor(diff / 86400000);
    const hrs  = Math.floor((diff % 86400000) / 3600000);
    const mins = Math.floor((diff % 3600000) / 60000);
    const secs = Math.floor((diff % 60000) / 1000);

    const el = document.getElementById('nbsVal');
    if (!el) return;
    if (days === 0 && hrs === 0 && mins === 0)
      el.textContent = '🎉 TODAY!';
    else if (days === 0)
      el.textContent = `${hrs}h ${mins}m ${secs}s`;
    else
      el.textContent = `${days}d ${hrs}h ${mins}m`;
  }
  update();
  setInterval(update, 1000);
}

function startMicBlow() {
  const hint = document.getElementById('micHint');
  if (!navigator.mediaDevices) { if(hint) hint.textContent = 'Mic not supported on this browser.'; return; }
  navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
    micStream = stream;
    if (hint) hint.textContent = '🎤 Listening… blow into your mic!';
    const ctx = new (window.AudioContext || window.webkitAudioContext)();
    const analyser = ctx.createAnalyser();
    const source = ctx.createMediaStreamSource(stream);
    source.connect(analyser);
    analyser.fftSize = 256;
    const data = new Uint8Array(analyser.frequencyBinCount);
    let blown = 0;
    
    function check() {
      if (candlesOut === totalCandles) { stream.getTracks().forEach(t=>t.stop()); return; }
      analyser.getByteFrequencyData(data);
      const vol = data.reduce((a,b)=>a+b,0)/data.length;
      if (vol > 30) {
        blown++;
        if (blown > 3) {
          if (typeof blowCandle3D === 'function') {
            const nextLit = window._cakeCandles3D.findIndex(c => c.lit);
            if (nextLit >= 0) blowCandle3D(nextLit);
          }
          blown = 0;
        }
      }
      requestAnimationFrame(check);
    }
    check();
  }).catch(() => { if(hint) hint.textContent = 'Mic access denied. Click candles instead!'; });
}

function startFunStats(dobStr) {
  function fmt(n) { return Math.floor(n).toLocaleString(); }
  function update() {
    const now  = Date.now();
    const born = new Date(dobStr).getTime();
    const ms   = now - born;
    const secs = ms / 1000;
    const mins = secs / 60;
    const hrs  = mins / 60;
    const days = hrs  / 24;

    const hb = document.getElementById('statHeartbeats');
    const br = document.getElementById('statBreaths');
    const ho = document.getElementById('statHours');
    const da = document.getElementById('statDays');
    const sl = document.getElementById('statSleep');
    const la = document.getElementById('statLaughs');

    if (hb) hb.textContent = fmt(secs * 1.2);      // ~72 bpm avg
    if (br) br.textContent = fmt(secs * 0.267);     // ~16 breaths/min
    if (ho) ho.textContent = fmt(hrs);
    if (da) da.textContent = fmt(days);
    if (sl) sl.textContent = fmt(hrs * 0.33);       // ~8hrs/day sleep
    if (la) la.textContent = fmt(days * 15);        // ~15 laughs/day
  }
  update();
  setInterval(update, 1000);
}

function openGift() {
  if (giftOpened) return;
  giftOpened = true;
  if (window.PortfolioSounds) window.PortfolioSounds.playPop();
  if (typeof openGift3D === 'function') {
    openGift3D();
  } else {
    const burst = document.getElementById('giftBurst');
    const msg  = document.getElementById('giftMessage');
    setTimeout(() => {
      if (burst) { burst.textContent = '🎉✨🎊💫🌟'; burst.classList.add('show'); }
    }, 400);
    setTimeout(() => {
      const m = giftMessages[Math.floor(Math.random() * giftMessages.length)];
      if (msg) { msg.textContent = m; msg.classList.add('show'); }
    }, 800);
  }
}

function revealFortune() {
  const smoke = document.getElementById('crystalSmoke');
  const text  = document.getElementById('crystalText');
  const result= document.getElementById('fortuneResult');
  if (!smoke) return;

  if (fortuneRevealed) {
    fortuneRevealed = false;
    if (result) result.classList.remove('show');
    if (text)  text.textContent = '✨';
  }

  if (window.PortfolioSounds) window.PortfolioSounds.playMagic();
  smoke.classList.add('swirling');
  if (text) text.textContent = '🔮';

  setTimeout(() => {
    smoke.classList.remove('swirling');
    const f = fortunes[Math.floor(Math.random() * fortunes.length)];
    if (text) text.textContent = f.emoji;
    if (result) {
      result.innerHTML = `<span class="fortune-emoji">${f.emoji}</span><strong>${f.title}</strong><br><span class="fortune-text">${f.text}</span><br><br><small style="color:var(--text-muted);font-size:0.75rem">Tap again for a new fortune ✨</small>`;
      result.classList.add('show');
    }
    fortuneRevealed = true;
  }, 1200);
}

function getZodiac(dobStr) {
  const d = new Date(dobStr);
  const m = d.getMonth() + 1, day = d.getDate();
  if ((m===12&&day>=22)||(m===1&&day<=19))  return ZODIACS[0];
  if ((m===1&&day>=20)||(m===2&&day<=18))   return ZODIACS[1];
  if ((m===2&&day>=19)||(m===3&&day<=20))   return ZODIACS[2];
  if ((m===3&&day>=21)||(m===4&&day<=19))   return ZODIACS[3];
  if ((m===4&&day>=20)||(m===5&&day<=20))   return ZODIACS[4];
  if ((m===5&&day>=21)||(m===6&&day<=20))   return ZODIACS[5];
  if ((m===6&&day>=21)||(m===7&&day<=22))   return ZODIACS[6];
  if ((m===7&&day>=23)||(m===8&&day<=22))   return ZODIACS[7];
  if ((m===8&&day>=23)||(m===9&&day<=22))   return ZODIACS[8];
  if ((m===9&&day>=23)||(m===10&&day<=22))  return ZODIACS[9];
  if ((m===10&&day>=23)||(m===11&&day<=21)) return ZODIACS[10];
  return ZODIACS[11];
}

function initZodiac(dobStr) {
  const z = getZodiac(dobStr);
  const sym  = document.getElementById('zodiacSymbol');
  const name = document.getElementById('zodiacName');
  const dates= document.getElementById('zodiacDates');
  const traits=document.getElementById('zodiacTraits');
  if (sym)   sym.textContent   = z.symbol;
  if (name)  name.textContent  = z.name;
  if (dates) dates.textContent = z.dates;
  if (traits) {
    traits.innerHTML = z.traits.map(t => `<span class="zodiac-trait">${t}</span>`).join('');
  }
  drawStarMap(z);
  if (window.PortfolioSounds) {
    setTimeout(() => window.PortfolioSounds.playMagic(), 850);
  }
}

function drawStarMap(z) {
  const canvas = document.getElementById('starCanvas');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;
  ctx.clearRect(0,0,W,H);

  const bg = ctx.createRadialGradient(W/2,H/2,10,W/2,H/2,W/2);
  bg.addColorStop(0,'#110c28'); bg.addColorStop(1,'#04000b');
  ctx.fillStyle = bg; ctx.fillRect(0,0,W,H);

  for (let i=0; i<60; i++) {
    ctx.beginPath();
    ctx.arc(Math.random()*W, Math.random()*H, Math.random()*1.2, 0, Math.PI*2);
    ctx.fillStyle = `rgba(255,255,255,${0.25+Math.random()*0.5})`;
    ctx.fill();
  }

  ctx.strokeStyle = 'rgba(0, 229, 255, 0.25)';
  ctx.lineWidth = 1.2;
  ctx.setLineDash([4,5]);
  ctx.beginPath();
  z.stars.forEach((s,i) => { i===0 ? ctx.moveTo(s[0],s[1]) : ctx.lineTo(s[0],s[1]); });
  ctx.stroke();
  ctx.setLineDash([]);

  z.stars.forEach(s => {
    const grd = ctx.createRadialGradient(s[0],s[1],0,s[0],s[1],8);
    grd.addColorStop(0,'rgba(0, 229, 255, 1)');
    grd.addColorStop(0.5,'rgba(0, 229, 255, 0.4)');
    grd.addColorStop(1,'rgba(0, 229, 255, 0)');
    ctx.beginPath();
    ctx.arc(s[0],s[1],8,0,Math.PI*2);
    ctx.fillStyle = grd; ctx.fill();
    ctx.beginPath();
    ctx.arc(s[0],s[1],2.5,0,Math.PI*2);
    ctx.fillStyle = '#ffffff'; ctx.fill();
  });
}

// ─── Share Panel Link Utilities ──────────────────────────────────────────
function copyLink() {
  const url = document.getElementById('shareUrl').textContent;
  navigator.clipboard.writeText(url).then(() => {
    showToast('Onboarding link copied! 📋');
    if (window.PortfolioSounds) window.PortfolioSounds.playSuccess();
  }).catch(() => {
    showToast('Failed to copy. Copy manually.');
    if (window.PortfolioSounds) window.PortfolioSounds.playError();
  });
}

function shareWA() {
  const url = document.getElementById('shareUrl').textContent;
  const msg = `🎂 Happy Birthday, ${personName}! 🎉\n\nOpen your special customized birthday 3D wishes deck here:\n${url}`;
  window.open(`https://wa.me/?text=${encodeURIComponent(msg)}`, '_blank');
}

function shareTelegram() {
  const url = document.getElementById('shareUrl').textContent;
  const msg = `🎂 Happy Birthday, ${personName}! 🎉`;
  window.open(`https://t.me/share/url?url=${encodeURIComponent(url)}&text=${encodeURIComponent(msg)}`, '_blank');
}

// ─── Sparkle Mouse Trail ──────────────────────────────────────────────────
(function () {
  const COLORS = ['#ffd873','#f2c14e','#9d4dff','#c084fc','#ffb703','#ff4d8d'];
  let last = 0;
  document.addEventListener('mousemove', (e) => {
    const now = Date.now();
    if (now - last < 50) return; // Throttled for performance
    last = now;
    
    // Sparkle trail only active when birthday overlay is open
    const overlay = document.getElementById('birthday-overlay');
    if (!overlay || overlay.style.display !== 'block') return;

    const dot = document.createElement('div');
    dot.className = 'sparkle-dot';
    const size = 5 + Math.random() * 7;
    dot.style.cssText = `
      width:${size}px; height:${size}px;
      left:${e.clientX}px; top:${e.clientY}px;
      background:${COLORS[Math.floor(Math.random()*COLORS.length)]};
      box-shadow: 0 0 ${size*2}px ${COLORS[Math.floor(Math.random()*COLORS.length)]};
    `;
    document.body.appendChild(dot);
    setTimeout(() => dot.remove(), 700);
  });
})();

// ─── Toast Messaging Utility ──────────────────────────────────────────────
let toastTimer;
function showToast(msg) {
  const t = document.getElementById('toast');
  if (!t) return;
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => t.classList.remove('show'), 3000);
}

// ════════════════════════════════════════════════════════════
//  DYNAMIC COSMIC SPACE BACKGROUND (MINUSCULE STARS OVER HD GALAXY)
// ════════════════════════════════════════════════════════════
function initCosmicBackground() {
  const container = document.getElementById('cosmic-bg-container');
  const canvas = document.getElementById('cosmic-canvas');
  if (!container || !canvas || typeof THREE === 'undefined') return;

  const scene = new THREE.Scene();
  scene.background = null; // Transparent to blend seamlessly over the HD galaxy background

  // Camera - Perspective Camera for 3D astronomical depth parallax
  const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1400);
  camera.position.z = 90;

  // WebGL Renderer with alpha channel enabled
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  // Crisp Minuscule Star Texture (No Blobs)
  function createStarTexture() {
    const texCanvas = document.createElement('canvas');
    texCanvas.width = 16;
    texCanvas.height = 16;
    const ctx = texCanvas.getContext('2d');
    
    // Crisp glowing core
    const grad = ctx.createRadialGradient(8, 8, 0, 8, 8, 8);
    grad.addColorStop(0, 'rgba(255, 255, 255, 1)');
    grad.addColorStop(0.35, 'rgba(255, 255, 255, 0.85)');
    grad.addColorStop(0.7, 'rgba(255, 255, 255, 0.25)');
    grad.addColorStop(1, 'rgba(255, 255, 255, 0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 16, 16);

    return new THREE.CanvasTexture(texCanvas);
  }

  const starTexture = createStarTexture();

  // Multi-tier Starfield Generator across wide panoramic space
  function createStarfield(count, size, rangeX, rangeY, rangeZ, opacity) {
    const geo = new THREE.BufferGeometry();
    const positions = [];
    const colors = [];
    
    const starColors = [
      new THREE.Color(0xffffff), // Diamond Pure White
      new THREE.Color(0xa5f3fc), // Ice Cyan
      new THREE.Color(0xfde047), // Pale Gold
      new THREE.Color(0xffedd5), // Warm Starlight
      new THREE.Color(0xe9d5ff)  // Soft Cosmic Lavender
    ];

    for (let i = 0; i < count; i++) {
      positions.push(
        (Math.random() - 0.5) * rangeX,
        (Math.random() - 0.5) * rangeY,
        (Math.random() - 0.5) * rangeZ
      );
      
      const col = starColors[Math.floor(Math.random() * starColors.length)];
      colors.push(col.r, col.g, col.b);
    }

    geo.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));
    geo.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));

    const mat = new THREE.PointsMaterial({
      size,
      map: starTexture,
      transparent: true,
      opacity,
      vertexColors: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false
    });

    return new THREE.Points(geo, mat);
  }

  // A. Deep Universe Starfield (2,200 wide panoramic stars, size 0.20)
  const deepStars = createStarfield(2200, 0.20, 560, 420, 480, 0.92);
  scene.add(deepStars);

  // B. Mid-range Constellation Points (520 stars, size 0.38)
  const midStars = createStarfield(520, 0.38, 380, 300, 320, 0.95);
  scene.add(midStars);

  // C. Foreground Twinkling Stellar Points (180 stars, size 0.58)
  const foregroundStars = createStarfield(180, 0.58, 260, 200, 200, 0.98);
  scene.add(foregroundStars);

  // Adaptive Panoramic Screen Navigation Tracker (Scrolls around zoomed-in celestial viewport)
  let camX = 0, camY = 0;
  let targetCamX = 0, targetCamY = 0;
  let scrollParallaxY = 0;
  let targetScrollParallaxY = 0;

  const isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
  if (!isTouch) {
    document.addEventListener('mousemove', (e) => {
      const normX = (e.clientX / window.innerWidth) * 2 - 1;
      const normY = (e.clientY / window.innerHeight) * 2 - 1;
      // Panoramic glide across the zoomed-in starfield
      targetCamX = normX * 48;
      targetCamY = -normY * 36;
      container.style.setProperty('--bg-pan-x', `${(-normX * 18).toFixed(1)}px`);
      container.style.setProperty('--bg-pan-y', `${(-normY * 14).toFixed(1)}px`);
    }, { passive: true });
  }

  window.addEventListener('scroll', () => {
    targetScrollParallaxY = (window.scrollY || window.pageYOffset || 0) * 0.024;
  }, { passive: true });

  container.style.opacity = '1';

  // Dynamic animation render loop
  let time = 0;
  function animateScene() {
    requestAnimationFrame(animateScene);
    time += 0.012;

    // Slow celestial rotation of minuscule stars
    deepStars.rotation.y = time * 0.0003;
    midStars.rotation.y = -time * 0.0006;
    foregroundStars.rotation.y = time * 0.0008;

    // Atmospheric stellar twinkling
    deepStars.material.opacity = 0.82 + Math.sin(time * 1.8) * 0.12;
    foregroundStars.material.opacity = 0.86 + Math.cos(time * 2.4) * 0.14;

    // Smooth inertial pan across the zoomed-in celestial star screen
    camX += (targetCamX - camX) * 0.045;
    camY += (targetCamY - camY) * 0.045;
    scrollParallaxY += (targetScrollParallaxY - scrollParallaxY) * 0.07;

    camera.position.x = camX;
    camera.position.y = camY - scrollParallaxY;
    camera.lookAt(camX * 0.35, (camY - scrollParallaxY) * 0.35, -90);

    renderer.render(scene, camera);
  }
  animateScene();

  // Window Resize Listener
  window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
  });
}