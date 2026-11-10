/**
 * REACT-3D-CARDS.JS — React 18 Whole-Card 3D Bending & Deformation Engine
 * 
 * Delivers full-box physical 3D deformation across all portfolio cards:
 * - Powered by React 18 (React.useState, React.useEffect, ReactDOM.createRoot)
 * - The entire card container box deforms, bends, twists, and tilts as a single unified solid unit
 * - NO independent inner text warping or deforming
 * - 60fps spring-damping lerp physics: dynamic 3D perspective, torsional skew, and backward depth push
 * - ZERO artificial illumination bloom: pure physical 3D drop shadow elevation
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

            // 3D Physics State (Whole card element box deformation)
            this.currentRotX = 0;
            this.currentRotY = 0;
            this.currentSkewX = 0;
            this.currentSkewY = 0;
            this.currentMoveX = 0;
            this.currentMoveY = 0;
            this.currentTransZ = 0;

            this.targetRotX = 0;
            this.targetRotY = 0;
            this.targetSkewX = 0;
            this.targetSkewY = 0;
            this.targetMoveX = 0;
            this.targetMoveY = 0;
            this.targetTransZ = 0;

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

        handleMouseEnter() {
            this.isHovered = true;
            this.targetTransZ = -16; // Backward 3D depth sink into z-space
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

            // Whole card element box 3D tilt
            this.targetRotX = normY * 11.5;
            this.targetRotY = -normX * 11.5;

            // Whole card element box physical bending & torsional deformation
            this.targetSkewX = -normX * 2.8;
            this.targetSkewY = -normY * 2.0;

            // Kinetic motion drift
            this.targetMoveX = normX * 9.5;
            this.targetMoveY = normY * 7.5;
            this.targetTransZ = -18;
        }

        handleMouseLeave() {
            this.isHovered = false;
            this.targetRotX = 0;
            this.targetRotY = 0;
            this.targetSkewX = 0;
            this.targetSkewY = 0;
            this.targetMoveX = 0;
            this.targetMoveY = 0;
            this.targetTransZ = 0;

            this.startLoop();
        }

        startLoop() {
            if (!this.animId) {
                this.update = this.renderFrame.bind(this);
                this.animId = requestAnimationFrame(this.update);
            }
        }

        renderFrame() {
            // Spring damping interpolation (smooth physical flex & settling)
            const lerp = 0.14;

            this.currentRotX += (this.targetRotX - this.currentRotX) * lerp;
            this.currentRotY += (this.targetRotY - this.currentRotY) * lerp;
            this.currentSkewX += (this.targetSkewX - this.currentSkewX) * lerp;
            this.currentSkewY += (this.targetSkewY - this.currentSkewY) * lerp;
            this.currentMoveX += (this.targetMoveX - this.currentMoveX) * lerp;
            this.currentMoveY += (this.targetMoveY - this.currentMoveY) * lerp;
            this.currentTransZ += (this.targetTransZ - this.currentTransZ) * lerp;

            // Apply 3D perspective bending, skew torsional deformation, and backward displacement to the WHOLE BOX
            this.el.style.transform = `perspective(950px) translate3d(${this.currentMoveX.toFixed(1)}px, ${this.currentMoveY.toFixed(1)}px, ${this.currentTransZ.toFixed(1)}px) rotateX(${this.currentRotX.toFixed(2)}deg) rotateY(${this.currentRotY.toFixed(2)}deg) skew(${this.currentSkewX.toFixed(2)}deg, ${this.currentSkewY.toFixed(2)}deg) scale3d(0.978, 0.978, 0.978)`;

            const isSettled = !this.isHovered &&
                Math.abs(this.currentRotX) < 0.05 &&
                Math.abs(this.currentRotY) < 0.05 &&
                Math.abs(this.currentSkewX) < 0.05 &&
                Math.abs(this.currentSkewY) < 0.05 &&
                Math.abs(this.currentTransZ) < 0.05 &&
                Math.abs(this.currentMoveX) < 0.05 &&
                Math.abs(this.currentMoveY) < 0.05;

            if (isSettled) {
                this.el.style.transform = '';
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
                    console.log(`[React-3D-Cards] React ${React.version} controlling full-box 3D bending across ${count} cards.`);
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
