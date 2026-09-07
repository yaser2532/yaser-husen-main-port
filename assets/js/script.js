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

        for (let i = 0; i < NUM_DOTS; i++) {
            const dot = document.createElement('div');
            dot.className = 'mouse-tracker-dot';
            document.body.appendChild(dot);
            dots.push(dot);

            // Establish random directional angles and offset distances to form an organic cluster
            const angle = Math.random() * Math.PI * 2;
            const distance = 6 + Math.random() * 8;
            
            dotsData.push({
                currentX: targetX,
                currentY: targetY,
              ease: 0.08 + Math.random() * 0.04,
                dx: Math.cos(angle) * distance,
                dy: Math.sin(angle) * distance,
              freqX: 0.7 + Math.random() * 0.8,
              freqY: 0.7 + Math.random() * 0.8,
              ampX: 1.5 + Math.random() * 2.5,
              ampY: 1.5 + Math.random() * 2.5,
                phaseX: Math.random() * Math.PI * 2,
                phaseY: Math.random() * Math.PI * 2
            });
        }

        document.addEventListener('mousemove', (e) => {
            targetX = e.clientX;
            targetY = e.clientY;
            if (!isVisible) {
              currentX = targetX;
              currentY = targetY;
              dotsData.forEach(data => {
                data.currentX = targetX + data.dx;
                data.currentY = targetY + data.dy;
              });
                isVisible = true;
                mouseGlow.style.opacity = '1';
                dots.forEach(dot => dot.classList.add('active'));
            }
        });

        document.addEventListener('mouseleave', () => {
            mouseGlow.style.opacity = '0';
            dots.forEach(dot => dot.classList.remove('active'));
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
            
            for (let i = 0; i < NUM_DOTS; i++) {
                const dot = dots[i];
                const data = dotsData[i];
                
                // Swarming drift offset calculation
                const driftX = Math.sin(time * data.freqX + data.phaseX) * data.ampX;
                const driftY = Math.cos(time * data.freqY + data.phaseY) * data.ampY;
                
                const targetDotX = targetX + data.dx + driftX;
                const targetDotY = targetY + data.dy + driftY;
                
                data.currentX += (targetDotX - data.currentX) * data.ease;
                data.currentY += (targetDotY - data.currentY) * data.ease;
                
                const dotXRem = data.currentX / rootFontSize;
                const dotYRem = data.currentY / rootFontSize;
                
                dot.style.transform = `translate3d(${dotXRem}rem, ${dotYRem}rem, 0) translate(-50%, -50%) scale(${currentScale})`;
            }
            
            requestAnimationFrame(animateGlow);
        }
        requestAnimationFrame(animateGlow);
    }

    /* --- 2. Interactive Hanging Lamp swinging physics --- */
    const lampArm = document.getElementById('lamp-swing-arm');
    const lampRefl = document.getElementById('lamp-reflection');
    
    if (lampArm && lampRefl) {
        let angle = 0;
        let velocity = 0;
        const damping = 0.985;
        const restoringForce = 0.002;
        
        let isDragging = false;
        
        const getHingePoint = () => {
            const rect = lampArm.getBoundingClientRect();
            return {
                x: rect.left + rect.width / 2,
                y: rect.top
            };
        };

        const handleStart = (clientX, clientY) => {
            isDragging = true;
            velocity = 0;
            handleMove(clientX, clientY);
        };

        const handleMove = (clientX, clientY) => {
            if (!isDragging) return;
            const hinge = getHingePoint();
            const dx = clientX - hinge.x;
            const dy = clientY - hinge.y;
            
            // Calculate angle relative to vertical downward axis
            let dragAngle = Math.atan2(dx, Math.max(dy, 20)) * (180 / Math.PI);
            
            // Clamp drag angle
            if (dragAngle > 45) dragAngle = 45;
            if (dragAngle < -45) dragAngle = -45;
            
            velocity = dragAngle - angle; 
            angle = dragAngle;
        };

        const handleEnd = () => {
            isDragging = false;
        };

        // Attach mouse events for direct drag interactions
        const lampStructure = lampArm.querySelector('.lamp-structure');
        if (lampStructure) {
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
            } else {
                // Hover swing start kick
                const mouseX = e.clientX;
                const mouseY = e.clientY;
                const hinge = getHingePoint();
                const dx = mouseX - hinge.x;
                const dy = mouseY - hinge.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 250) {
                    const force = (e.movementX || 0) * 0.0012 * (1 - distance / 250);
                    velocity += force;
                }
            }
        });

        document.addEventListener('touchmove', (e) => {
            if (isDragging && e.touches.length > 0) {
                handleMove(e.touches[0].clientX, e.touches[0].clientY);
            }
        }, { passive: true });

        document.addEventListener('mouseup', handleEnd);
        document.addEventListener('touchend', handleEnd);

        let ambientTime = 0;

        function swingLoop() {
            if (!isDragging) {
                ambientTime += 0.01;
                const ambientForce = Math.sin(ambientTime) * 0.00015;
                
                const acceleration = -restoringForce * angle + ambientForce;
                velocity += acceleration;
                velocity *= damping;
                angle += velocity;
                
                if (angle > 50) angle = 50;
                if (angle < -50) angle = -50;
            }
            
            lampArm.style.transform = `rotate(${angle}deg)`;
            
            const shiftX = -angle * 5.5; 
            lampRefl.style.transform = `translateX(calc(-50% + ${shiftX}px))`;
            
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

    window.addEventListener('scroll', () => {
        handleNavbarScroll();

        // 3D page-flip scroll transition for hero section
        const scrolled = window.scrollY;
        const heroHeight = window.innerHeight;
        const header = document.querySelector('header');
        if (header) {
            if (scrolled <= heroHeight) {
                const percent = scrolled / heroHeight;
                const rotateX = percent * -25;
                const scale = 1 - (percent * 0.15);
                const opacity = 1 - (percent * 0.95);
                header.style.transform = `perspective(1000px) rotateX(${rotateX}deg) scale(${scale})`;
                header.style.opacity = opacity;
                header.style.visibility = 'visible';
            } else {
                header.style.transform = 'perspective(1000px) rotateX(-25deg) scale(0.85)';
                header.style.opacity = 0;
                header.style.visibility = 'hidden';
            }
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

    /* --- 4. Secret Desk Lamp Logic --- */
    const secretDeskSection = document.getElementById('secret-desk');
    const lampSwitch = document.getElementById('lamp-toggle');

    if (secretDeskSection && lampSwitch) {
        lampSwitch.checked = false;
        secretDeskSection.classList.remove('is-lit');

        lampSwitch.addEventListener('change', () => {
            secretDeskSection.classList.toggle('is-lit');
        });
    }

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

    /* --- 7. Typewriter Sequence --- */
    function typeText(element, text, speed) {
        return new Promise((resolve) => {
            let i = 0;
            element.textContent = '';
            function type() {
                if (i < text.length) {
                    element.textContent += text.charAt(i);
                    i++;
                    setTimeout(type, speed);
                } else {
                    resolve();
                }
            }
            type();
        });
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

        // Step 1: Type name
        await typeText(nameEl, "YASER HUSEN", 130);
        nameCursor.classList.add('hidden');

        // Step 2: Type subtitle
        if (subtitleEl && subtitleCursor) {
            subtitleCursor.classList.remove('hidden');
            await typeText(subtitleEl, "AI Developer, UI/UX & SaaS Integrator", 80);
            subtitleCursor.classList.add('hidden');
        }

        // Step 3: Reveal trait tags and about card
        if (detailsContainer) {
            detailsContainer.classList.add('reveal');
        }

        // Step 4: Type description
        if (aboutEl && aboutCursor) {
            aboutCursor.classList.remove('hidden');
            await typeText(aboutEl, "I bridge technical data science, scalable artificial intelligence, and beautiful custom frontends to build unified high-velocity web platforms.", 50);
        }
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
  const COLORS = ['#ffe66d','#ff4d8d','#00e5ff','#c084fc','#39ff14','#ff8c00'];
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
//  DYNAMIC COSMIC SPACE BACKGROUND (STARS & NEBULA) WITH THREE.JS
// ════════════════════════════════════════════════════════════
function initCosmicBackground() {
  const container = document.getElementById('cosmic-bg-container');
  const canvas = document.getElementById('cosmic-canvas');
  if (!container || !canvas || typeof THREE === 'undefined') return;

  const scene = new THREE.Scene();
  scene.background = null; // Transparent to blend with CSS gradient

  // Camera - Perspective Camera for 3D depth parallax
  const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.z = 80;

  // WebGL Renderer with alpha channel enabled
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

  // Particle texture generator (creates a soft radial glow circle)
  function createCircleTexture() {
    const texCanvas = document.createElement('canvas');
    texCanvas.width = 16;
    texCanvas.height = 16;
    const ctx = texCanvas.getContext('2d');
    const grad = ctx.createRadialGradient(8, 8, 0, 8, 8, 8);
    grad.addColorStop(0, 'rgba(255, 255, 255, 1)');
    grad.addColorStop(0.3, 'rgba(255, 255, 255, 0.8)');
    grad.addColorStop(1, 'rgba(255, 255, 255, 0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 16, 16);
    
    const texture = new THREE.CanvasTexture(texCanvas);
    return texture;
  }

  const starTexture = createCircleTexture();

  // Create starfields (2 independent layers for depth/parallax feel)
  function createStarfield(count, size, range, opacity) {
    const geo = new THREE.BufferGeometry();
    const positions = [];
    const colors = [];
    
    // Sleek space colors corresponding to the website aesthetics
    const starColors = [
      new THREE.Color(0xffffff), // Pure White
      new THREE.Color(0xa7d8ff), // Neon Cyan-Blue
      new THREE.Color(0xe0b5ff), // Bright Purple
      new THREE.Color(0xfff3d1)  // Warm Gold
    ];

    for (let i = 0; i < count; i++) {
      // Scatter randomly in a 3D box
      positions.push(
        (Math.random() - 0.5) * range * 2.2,
        (Math.random() - 0.5) * range * 1.6,
        (Math.random() - 0.5) * range
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

  // 2000 tiny far stars, 450 larger twinkling near stars (kept at high visibility)
  const farStars = createStarfield(2000, 0.32, 220, 0.8);
  const nearStars = createStarfield(450, 0.6, 160, 0.95);
  scene.add(farStars);
  scene.add(nearStars);

  // Gaseous Nebula cloud texture generator
  function createNebulaTexture(colorHex1, colorHex2) {
    const texCanvas = document.createElement('canvas');
    texCanvas.width = 512;
    texCanvas.height = 512;
    const ctx = texCanvas.getContext('2d');
    ctx.clearRect(0, 0, 512, 512);

    // Large radial gradient for soft smoke appearance
    const grad = ctx.createRadialGradient(256, 256, 15, 256, 256, 240);
    grad.addColorStop(0, colorHex1);
    grad.addColorStop(0.5, colorHex2);
    grad.addColorStop(1, 'rgba(0, 0, 0, 0)');

    ctx.fillStyle = grad;
    ctx.beginPath();
    ctx.arc(256, 256, 256, 0, Math.PI * 2);
    ctx.fill();

    const texture = new THREE.CanvasTexture(texCanvas);
    return texture;
  }

  // Generate three custom color maps for the nebulas (reduced intensity for subtle drifting patches)
  const nebulaTexPurple = createNebulaTexture('rgba(139, 92, 246, 0.12)', 'rgba(109, 40, 217, 0.04)'); // --accent-color matching purple
  const nebulaTexCyan = createNebulaTexture('rgba(6, 182, 212, 0.09)', 'rgba(8, 145, 178, 0.02)');   // --accent-hover matching cyan
  const nebulaTexMagenta = createNebulaTexture('rgba(236, 72, 153, 0.07)', 'rgba(190, 24, 74, 0.01)'); // Magenta highlights

  const nebulaPlanes = [];
  const nebulaSpecs = [
    { tex: nebulaTexPurple, size: 85, pos: [-35, 15, -55], rotSpeed: 0.0006, driftX: 4, driftY: 3 },
    { tex: nebulaTexCyan, size: 95, pos: [35, -8, -75], rotSpeed: -0.0005, driftX: 5, driftY: 2 },
    { tex: nebulaTexMagenta, size: 75, pos: [-10, -25, -65], rotSpeed: 0.0003, driftX: 3, driftY: 4 },
    { tex: nebulaTexPurple, size: 105, pos: [20, 25, -95], rotSpeed: -0.0002, driftX: 4, driftY: 3 }
  ];

  nebulaSpecs.forEach(spec => {
    const geo = new THREE.PlaneGeometry(spec.size, spec.size);
    const mat = new THREE.MeshBasicMaterial({
      map: spec.tex,
      transparent: true,
      depthWrite: false,
      blending: THREE.AdditiveBlending,
      opacity: 0.45
    });
    const plane = new THREE.Mesh(geo, mat);
    plane.position.set(spec.pos[0], spec.pos[1], spec.pos[2]);
    plane.rotation.z = Math.random() * Math.PI * 2;
    scene.add(plane);
    nebulaPlanes.push({ mesh: plane, spec });
  });

  // Ambient lighting
  scene.add(new THREE.AmbientLight(0xffffff, 0.5));

  // Cursor Parallax Tracker
  let mouseX = 0, mouseY = 0;
  let targetMouseX = 0, targetMouseY = 0;
  const isTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;

  if (!isTouch) {
    document.addEventListener('mousemove', (e) => {
      targetMouseX = (e.clientX / window.innerWidth) * 2 - 1;
      targetMouseY = (e.clientY / window.innerHeight) * 2 - 1;
    });
  }

  // Scroll Fade Trigger Logic
  const triggerSection = document.getElementById('profile-expertise');
  let isBackgroundActive = false;

  function handleScrollOpacity() {
    if (!triggerSection) return;
    const triggerTop = triggerSection.getBoundingClientRect().top + window.scrollY;
    
    // Fade starts when the top of the trigger section starts entering the screen
    const triggerPoint = triggerTop - window.innerHeight;
    const fadeDistance = window.innerHeight * 0.6; // Fade completes over 60% viewport distance
    const scrolled = window.scrollY;

    if (scrolled > triggerPoint) {
      const progress = Math.min(1, (scrolled - triggerPoint) / fadeDistance);
      container.style.opacity = progress;
      isBackgroundActive = true;
    } else {
      container.style.opacity = 0;
      isBackgroundActive = false;
    }
  }

  // Run immediately and hook to window scroll
  handleScrollOpacity();
  window.addEventListener('scroll', handleScrollOpacity);

  // Dynamic animation render loop
  let time = 0;
  function animateScene() {
    requestAnimationFrame(animateScene);

    // Freeze render loop execution when scrolled above section to save performance
    if (!isBackgroundActive) return;

    time += 0.01;

    // Slow orbital rotation of starfields
    farStars.rotation.y = time * 0.004;
    farStars.rotation.x = time * 0.001;
    nearStars.rotation.y = -time * 0.007;

    // Twinkling light fluctuations (brighter limits)
    farStars.material.opacity = 0.65 + Math.sin(time * 1.6) * 0.15;
    nearStars.material.opacity = 0.78 + Math.cos(time * 2.2) * 0.15;

    // Swirl and shift gaseous cloud plane meshes
    nebulaPlanes.forEach(p => {
      p.mesh.rotation.z += p.spec.rotSpeed;
      p.mesh.position.x = p.spec.pos[0] + Math.sin(time * 0.12 + p.spec.pos[2]) * p.spec.driftX;
      p.mesh.position.y = p.spec.pos[1] + Math.cos(time * 0.10 + p.spec.pos[0]) * p.spec.driftY;
    });

    // Camera parallax dampening
    mouseX += (targetMouseX - mouseX) * 0.06;
    mouseY += (targetMouseY - mouseY) * 0.06;

    camera.position.x = mouseX * 7;
    camera.position.y = -mouseY * 5;
    camera.lookAt(0, 0, -100);

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