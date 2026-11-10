with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

target = """    /* --- Modern Butter-Smooth Native & Anchor Glide Engine --- */
    (function initSmoothMomentumScroll() {
        let currentScrollY = window.scrollY || window.pageYOffset || 0;
        let targetScrollY = currentScrollY;
        let isScrolling = false;
        let maxScroll = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);

        function updateMaxScroll() {
            maxScroll = Math.max(0, document.documentElement.scrollHeight - window.innerHeight);
        }
        window.addEventListener('resize', updateMaxScroll, { passive: true });

        window.addEventListener('scroll', () => {
            if (!isScrolling) {
                currentScrollY = window.scrollY || window.pageYOffset || 0;
                targetScrollY = currentScrollY;
            }
        }, { passive: true });

        function scrollLoop() {
            const diff = targetScrollY - currentScrollY;
            if (Math.abs(diff) > 0.4) {
                currentScrollY += diff * 0.12;
                window.scrollTo(0, currentScrollY);
                requestAnimationFrame(scrollLoop);
            } else {
                currentScrollY = targetScrollY;
                window.scrollTo(0, targetScrollY);
                isScrolling = false;
            }
        }

        // Native hardware-accelerated scrolling handles mouse wheel with zero jitter.
        // Smooth anchor links and programmatic navigation:

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
    });"""

replacement = """    // Smooth Anchor Navigation & Native Hardware-Accelerated Scrolling
    document.addEventListener('click', (e) => {
        const anchor = e.target.closest('a[href^="#"]');
        if (!anchor) return;
        const hash = anchor.getAttribute('href');
        if (!hash || hash === '#') return;
        const targetEl = document.querySelector(hash);
        if (targetEl) {
            e.preventDefault();
            targetEl.scrollIntoView({ behavior: 'smooth' });
            history.pushState(null, '', hash);
        }
    });

    // Zero-thrash Active Link Tracking via IntersectionObserver
    if (window.IntersectionObserver) {
        const navObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const id = entry.target.getAttribute('id');
                    navLinks.forEach(link => {
                        link.classList.toggle('active', link.getAttribute('href') === `#${id}`);
                    });
                }
            });
        }, { threshold: 0.25, rootMargin: '-10% 0px -40% 0px' });
        sections.forEach(sec => navObserver.observe(sec));
    }

    // Fast passive scroll listener (Zero DOM geometry reads)
    window.addEventListener('scroll', () => {
        handleNavbarScroll();

        // Smooth parallax fade for hero content on scroll
        const scrolled = window.scrollY;
        const heroHeight = window.innerHeight;
        const headerContent = document.querySelector('.header-content');
        if (headerContent && scrolled <= heroHeight) {
            const percent = scrolled / heroHeight;
            headerContent.style.opacity = (1 - percent * 0.92).toFixed(3);
            headerContent.style.transform = `translate3d(0, ${(percent * 45).toFixed(1)}px, 0)`;
        }

        if (backToTop) {
            backToTop.style.opacity = (scrolled > 800) ? '1' : '0';
            backToTop.style.pointerEvents = (scrolled > 800) ? 'auto' : 'none';
        }
    }, { passive: true });"""

assert target in content, "target not found"
content = content.replace(target, replacement, 1)

with open('assets/js/script.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Replaced scroll hijacker with native scrolling & zero-thrash observer!")
