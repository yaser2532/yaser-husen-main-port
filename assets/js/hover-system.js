/**
 * HOVER-SYSTEM.JS — Cyberpunk Interactive Micro-Interactions [H-01 ... H-06]
 * Features:
 *   - H-01: Main titles chromatic split (turquoise & gold offset) + draw underline
 *   - H-02: Body text soft turquoise-tinted highlight
 *   - H-03: Magnetic pull on buttons (max 6px) + neon border sweep + spark on press
 *   - H-04: Links turquoise underline draw + nav active gold dot
 *   - H-05 / 3D-03: Cards 3D perspective tilt (max 8°) + turquoise specular highlight
 *   - H-06: Cursor integration (bots step aside on input focus)
 */

(function () {
    'use strict';

    // Touch and reduced motion guards
    const hasHover = window.matchMedia && window.matchMedia('(hover: hover)').matches;
    const isReduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!hasHover || isReduced) {
        return; // Disabled on mobile touch and reduced motion
    }

    /* =========================================================================
       H-01: MAIN TITLES CHROMATIC SPLIT & UNDERLINE DRAW
       ========================================================================= */
    const titles = document.querySelectorAll('h1, h2, .section-title, .hero-title, .onboard-title');
    titles.forEach(title => {
        title.classList.add('cp-hover-title');

        title.addEventListener('mouseenter', () => {
            title.classList.add('cp-chromatic-split');
            setTimeout(() => {
                title.classList.remove('cp-chromatic-split');
            }, 180);
        });
    });

    /* =========================================================================
       H-03: MAGNETIC BUTTON PULL & PRESS SPARK
       ========================================================================= */
    const buttons = document.querySelectorAll('.btn, .cta-btn, .filter-btn, .nav-btn, .submit-btn, button[type="submit"]');
    buttons.forEach(btn => {
        btn.classList.add('cp-magnetic-btn');

        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;
            
            // Limit pull to 6px maximum
            const maxPull = 6.0;
            const pullX = Math.max(-maxPull, Math.min(maxPull, (e.clientX - centerX) * 0.25));
            const pullY = Math.max(-maxPull, Math.min(maxPull, (e.clientY - centerY) * 0.25));

            btn.style.transform = `translate3d(${pullX.toFixed(1)}px, ${pullY.toFixed(1)}px, 0)`;
        });

        btn.addEventListener('mouseleave', () => {
            btn.style.transform = 'translate3d(0, 0, 0)';
        });

        btn.addEventListener('mousedown', (e) => {
            btn.style.transform = 'translate3d(0, 0, 0) scale(0.95)';
        });

        btn.addEventListener('mouseup', () => {
            btn.style.transform = 'translate3d(0, 0, 0) scale(1.0)';
        });
    });

    /* =========================================================================
       H-05 / 3D-03: CARDS 3D PERSPECTIVE TILT & SPECULAR HIGHLIGHT
       ========================================================================= */
    const cards = document.querySelectorAll('.project-card, .cert-card, .expertise-card, .onboard-card, .stat-card, .contact-card');
    cards.forEach(card => {
        card.classList.add('cp-3d-card');

        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Normalize -1 to 1
            const normX = (x / rect.width) * 2 - 1;
            const normY = (y / rect.height) * 2 - 1;

            // Max 8 degrees tilt
            const maxTilt = 7.5;
            const rotX = -normY * maxTilt;
            const rotY = normX * maxTilt;

            card.style.transform = `perspective(900px) rotateX(${rotX.toFixed(2)}deg) rotateY(${rotY.toFixed(2)}deg) scale3d(1.018, 1.018, 1.018)`;
            card.style.setProperty('--card-mouse-x', `${(x / rect.width * 100).toFixed(1)}%`);
            card.style.setProperty('--card-mouse-y', `${(y / rect.height * 100).toFixed(1)}%`);
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'perspective(900px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
        });
    });

    /* =========================================================================
       H-06: TEXT INPUTS BOT STEP-ASIDE
       ========================================================================= */
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(inp => {
        inp.addEventListener('focus', () => {
            document.body.classList.add('cp-input-focused');
        });
        inp.addEventListener('blur', () => {
            document.body.classList.remove('cp-input-focused');
        });
    });

    console.log('[Hover-System] Interactive micro-interactions initialized.');
})();
