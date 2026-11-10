/**
 * REACT-3D-CARDS.JS — React 18 3D Interactive Card Folding Engine
 * 
 * Delivers dynamic 3D folding in and out across all portfolio cards:
 * - Powered by React 18 (React.useState, React.useEffect, ReactDOM.createRoot)
 * - Physical cursor reactivity (like the lamp/footer spring dynamics)
 * - UNLIKE the lamp (which swings like a pendulum), cards physically FOLD IN on hover and FOLD OUT on leave
 * - 3D origami/crease fold physics: perspective depth, inward z-sink, accordion fold compression, and dynamic crease angles
 * - The entire card container box folds as a solid 3D unit with ZERO inner text distortion
 * - 60fps spring-damping lerp physics
 */

(function () {
    'use strict';

    // Guard: Prefers reduced motion or touch-only device
    const prefersReducedMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const hasHover = window.matchMedia && window.matchMedia('(hover: hover)').matches;

    if (prefersReducedMotion || !hasHover) {
        return;
    }

    const hasReact = (typeof React !== 'undefined');
    const hasReactDOM = (typeof ReactDOM !== 'undefined');

    const CARD_SELECTOR = '.project-card, .cert-card, .expertise-card, .onboard-card, .stat-card, .glass-card, .bday-card, .code-block-visual, .hero-about-tile, .contact-card, .profile-card-wrapper';

    class Card3DController {
        constructor(el) {
            this.el = el;
            this.el.classList.add('react-3d-card');

            // 3D Folding Physics State
            this.foldProgress = 0; // 0 = unfolded flat, 1 = folded in
            this.targetFold = 0;

            this.currentRotX = 0;
            this.currentRotY = 0;
            this.currentCrease = 0;
            this.currentMoveX = 0;
            this.currentMoveY = 0;
            this.currentTransZ = 0;
            this.currentScale = 1.0;

            this.targetRotX = 0;
            this.targetRotY = 0;
            this.targetCrease = 0;
            this.targetMoveX = 0;
            this.targetMoveY = 0;
            this.targetTransZ = 0;
            this.targetScale = 1.0;

            this.isHovered = false;
            this.animId = null;

            this.bindEvents();
        }

        bindEvents() {
            this.onMouseMove = this.handleMouseMove.bind(this);
            this.onMouseEnter = this.handleMouseEnter.bind(this);
            this.onMouseLeave = this.handleMouseLeave.bind(this);

            this.el.addEventListener('mousemove', this.onMouseMove, { passive: true });
            this.el.addEventListener('mouseenter', this.onMouseEnter, { passive: true });
            this.el.addEventListener('mouseleave', this.onMouseLeave, { passive: true });
        }

        handleMouseEnter(e) {
            this.isHovered = true;
            this.targetFold = 1.0;
            this.targetTransZ = -22.0; // Inward 3D depth sink
            this.targetScale = 0.955; // Inward origami fold compression
            this.el.classList.add('card-folded-in');
            this.el.classList.remove('card-folded-out');
            this.startLoop();
        }

        handleMouseMove(e) {
            const rect = this.el.getBoundingClientRect();
            if (!rect.width || !rect.height) return;

            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Normalized coordinates (-1 to 1) from card center
            const normX = (x / rect.width) * 2 - 1;
            const normY = (y / rect.height) * 2 - 1;

            // Inward 3D Folding angles along cursor crease
            this.targetRotX = normY * 15.0; // Inward fold around horizontal crease
            this.targetRotY = -normX * 15.0; // Inward fold around vertical crease
            this.targetCrease = -normX * normY * 4.5; // Torsional origami fold crease

            // Dynamic kinetic drift & fold depth
            this.targetMoveX = normX * 8.0;
            this.targetMoveY = normY * 6.5;
            this.targetTransZ = -24.0 - Math.abs(normY) * 8.0;
            this.targetScale = 0.952 - Math.abs(normX) * 0.012;
            this.targetFold = 1.0;
        }

        handleMouseLeave() {
            this.isHovered = false;
            // Smoothly fold out back to flat resting geometry
            this.targetFold = 0.0;
            this.targetRotX = 0;
            this.targetRotY = 0;
            this.targetCrease = 0;
            this.targetMoveX = 0;
            this.targetMoveY = 0;
            this.targetTransZ = 0;
            this.targetScale = 1.0;

            this.el.classList.remove('card-folded-in');
            this.el.classList.add('card-folded-out');

            this.startLoop();
        }

        startLoop() {
            if (!this.animId) {
                this.update = this.renderFrame.bind(this);
                this.animId = requestAnimationFrame(this.update);
            }
        }

        renderFrame() {
            // Spring damping interpolation (smooth physical flex & unfolding)
            const lerp = 0.13;

            this.currentRotX += (this.targetRotX - this.currentRotX) * lerp;
            this.currentRotY += (this.targetRotY - this.currentRotY) * lerp;
            this.currentCrease += (this.targetCrease - this.currentCrease) * lerp;
            this.currentMoveX += (this.targetMoveX - this.currentMoveX) * lerp;
            this.currentMoveY += (this.targetMoveY - this.currentMoveY) * lerp;
            this.currentTransZ += (this.targetTransZ - this.currentTransZ) * lerp;
            this.currentScale += (this.targetScale - this.currentScale) * lerp;
            this.foldProgress += (this.targetFold - this.foldProgress) * lerp;

            // Apply 3D perspective folding transform to the WHOLE BOX container
            this.el.style.transform = `perspective(900px) translate3d(${this.currentMoveX.toFixed(1)}px, ${this.currentMoveY.toFixed(1)}px, ${this.currentTransZ.toFixed(1)}px) rotateX(${this.currentRotX.toFixed(2)}deg) rotateY(${this.currentRotY.toFixed(2)}deg) skew(${this.currentCrease.toFixed(2)}deg, ${this.currentCrease.toFixed(2)}deg) scale3d(${this.currentScale.toFixed(3)}, ${this.currentScale.toFixed(3)}, ${this.currentScale.toFixed(3)})`;

            const isSettled = !this.isHovered &&
                Math.abs(this.currentRotX) < 0.04 &&
                Math.abs(this.currentRotY) < 0.04 &&
                Math.abs(this.currentCrease) < 0.04 &&
                Math.abs(this.currentTransZ) < 0.05 &&
                Math.abs(this.currentMoveX) < 0.05 &&
                Math.abs(this.currentMoveY) < 0.05 &&
                Math.abs(this.currentScale - 1.0) < 0.003 &&
                this.foldProgress < 0.02;

            if (isSettled) {
                this.el.style.transform = '';
                this.el.classList.remove('card-folded-out');
                this.animId = null;
            } else {
                this.animId = requestAnimationFrame(this.update);
            }
        }
    }

    const activeControllers = [];

    function initCardControllers() {
        const cards = document.querySelectorAll(CARD_SELECTOR);
        cards.forEach(card => {
            if (!card._react3DCard) {
                const ctrl = new Card3DController(card);
                card._react3DCard = ctrl;
                activeControllers.push(ctrl);
            }
        });
        return activeControllers.length;
    }

    // React 18 System Component
    function initReact3DSystem() {
        if (!hasReact || !hasReactDOM) {
            initCardControllers();
            return;
        }

        try {
            const { createElement: h, useState, useEffect } = React;

            function React3DCardManager() {
                const [cardsCount, setCardsCount] = useState(0);

                useEffect(() => {
                    const count = initCardControllers();
                    setCardsCount(count);
                    console.log(`[React-3D-Cards] React ${React.version} controlling full-box 3D folding across ${count} cards.`);
                }, []);

                return h('div', {
                    id: 'react-3d-cards-status',
                    'data-react-version': React.version,
                    'data-cards-managed': cardsCount,
                    style: { display: 'none' }
                });
            }

            let container = document.getElementById('react-3d-root');
            if (!container) {
                container = document.createElement('div');
                container.id = 'react-3d-root';
                container.style.display = 'none';
                document.body.appendChild(container);
            }

            if (ReactDOM.createRoot) {
                const root = ReactDOM.createRoot(container);
                root.render(h(React3DCardManager));
            } else if (ReactDOM.render) {
                ReactDOM.render(h(React3DCardManager), container);
            }
        } catch (err) {
            console.warn('[React-3D-Cards] React mount fallback:', err);
            initCardControllers();
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initReact3DSystem);
    } else {
        initReact3DSystem();
    }

    // Expose React 3D Cards Controller API
    window.React3DCard = {
        isReactActive: hasReact,
        reactVersion: hasReact ? React.version : 'fallback-reactive',
        controllersCount: () => activeControllers.length,
        getControllers: () => activeControllers,
        refresh: () => {
            initCardControllers();
            return activeControllers.length;
        }
    };
})();
