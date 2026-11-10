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
    const buttons = document.querySelectorAll('.btn, .cta-btn, .cta-button, .filter-btn, .nav-btn, .nav-resume-btn, .dock-btn, .hero-scroll-pill, .btn-ai-chat, .message-btn, .submit-btn, button[type="submit"]');
    buttons.forEach(btn => {
        btn.classList.add('cp-magnetic-btn');

        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;
            
            // Limit pull to 5px maximum
            const maxPull = 4.5;
            const pullX = Math.max(-maxPull, Math.min(maxPull, (e.clientX - centerX) * 0.2));
            const pullY = Math.max(-maxPull, Math.min(maxPull, (e.clientY - centerY) * 0.2));

            btn.style.transition = 'none';
            btn.style.transform = `translate3d(${pullX.toFixed(1)}px, ${(pullY - 3).toFixed(1)}px, 0) scale(1.02)`;
        });

        btn.addEventListener('mouseleave', () => {
            btn.style.transition = 'transform 0.35s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.25s ease, border-color 0.25s ease';
            btn.style.transform = '';
        });

        btn.addEventListener('mousedown', () => {
            btn.style.transition = 'transform 0.1s ease';
            btn.style.transform = 'translate3d(0, 0, 0) scale(0.96)';
        });

        btn.addEventListener('mouseup', () => {
            btn.style.transition = 'transform 0.2s ease';
            btn.style.transform = '';
        });
    });

    /* =========================================================================
       H-05 / 3D-03: CARDS KINETIC CURSOR TRACKING & BACKWARD DEFORMATION
       Cards move around tracking cursor coordinates and deform backward into z-depth
       ========================================================================= */
    const cardSelector = '.project-card, .cert-card, .expertise-card, .onboard-card, .stat-card, .glass-card, .bday-card, .code-block-visual, .hero-about-tile, .contact-card, .profile-card-wrapper';
    const cards = document.querySelectorAll(cardSelector);
    cards.forEach(card => {
        card.classList.add('cp-3d-card');

        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Normalized coordinates (-1 to 1)
            const normX = (x / rect.width) * 2 - 1;
            const normY = (y / rect.height) * 2 - 1;

            // Kinetic motion: card drifts with cursor coordinates
            const moveX = (normX * 9.5).toFixed(1);
            const moveY = (normY * 7.5).toFixed(1);

            // Backward deformation: dips backward into z-space under cursor weight
            const rotX = (normY * 9.0).toFixed(2);
            const rotY = (-normX * 9.0).toFixed(2);
            const skewX = (-normX * 1.6).toFixed(2);
            const skewY = (-normY * 1.2).toFixed(2);

            card.style.transition = 'none';
            card.style.transform = `perspective(850px) translate3d(${moveX}px, ${moveY}px, -18px) rotateX(${rotX}deg) rotateY(${rotY}deg) skew(${skewX}deg, ${skewY}deg) scale3d(0.975, 0.975, 0.975)`;
            card.style.setProperty('--card-mouse-x', `${(x / rect.width * 100).toFixed(1)}%`);
            card.style.setProperty('--card-mouse-y', `${(y / rect.height * 100).toFixed(1)}%`);
        });

        card.addEventListener('mouseleave', () => {
            card.style.transition = 'transform 0.45s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.35s ease, border-color 0.3s ease';
            card.style.transform = 'perspective(850px) translate3d(0, 0, 0) rotateX(0deg) rotateY(0deg) skew(0deg, 0deg) scale3d(1, 1, 1)';
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
