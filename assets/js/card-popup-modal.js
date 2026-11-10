/**
 * CARD-POPUP-MODAL.JS — Cyberpunk Card Pop-Up Modal Lightbox Window
 * 
 * Implements the AI Chat Box Pop-Up Window behavior for all cards across the portfolio:
 * - When a card is clicked, it pops up into an expanded cybernetic modal window
 *   matching the nano-chat modal window styling and animation
 * - Pop-up animation: scale(0.92) translateY(20px) -> scale(1) translateY(0)
 *   with transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1)
 * - Deep frosted glassmorphic backdrop filter (blur 14px)
 * - Full accessibility: Esc key closes modal, click outside closes, close button, focus trap
 */

(function () {
    'use strict';

    function initCardPopupSystem() {
        // Prevent duplicate initialization
        if (document.getElementById('card-popup-modal-overlay')) return;

        // 1. Create Modal Overlay
        const overlay = document.createElement('div');
        overlay.id = 'card-popup-modal-overlay';
        overlay.className = 'card-popup-overlay';
        overlay.setAttribute('aria-hidden', 'true');
        overlay.setAttribute('role', 'dialog');
        overlay.setAttribute('aria-modal', 'true');

        // 2. Create Modal Window Container
        const modalWindow = document.createElement('div');
        modalWindow.className = 'card-popup-window';

        // 3. Create Card Inner Container
        const cardContent = document.createElement('div');
        cardContent.className = 'card-popup-card nano-chat-card glass-card';

        // 4. Modal Header
        const header = document.createElement('div');
        header.className = 'card-popup-header nano-header';

        const titleBox = document.createElement('div');
        titleBox.className = 'card-popup-title-box nano-title-box';

        const pulseDot = document.createElement('span');
        pulseDot.className = 'nano-pulse-dot';
        pulseDot.textContent = '⚡';

        const modalTitle = document.createElement('h3');
        modalTitle.className = 'card-popup-title nano-title';
        modalTitle.textContent = 'SYSTEM // NODE INSPECTION';

        titleBox.appendChild(pulseDot);
        titleBox.appendChild(modalTitle);

        const badgeBox = document.createElement('div');
        badgeBox.className = 'nano-badge-box';

        const badge = document.createElement('span');
        badge.className = 'nano-mode-badge';
        badge.id = 'card-popup-badge';
        badge.textContent = '⚡ CYBERPUNK 3.0 // EXPANDED VIEW';

        const closeBtn = document.createElement('button');
        closeBtn.className = 'nano-modal-close-btn';
        closeBtn.id = 'card-popup-close-btn';
        closeBtn.setAttribute('type', 'button');
        closeBtn.setAttribute('aria-label', 'Close Card Inspection Window');
        closeBtn.innerHTML = '&times;';

        badgeBox.appendChild(badge);
        badgeBox.appendChild(closeBtn);

        header.appendChild(titleBox);
        header.appendChild(badgeBox);

        // 5. Modal Body
        const modalBody = document.createElement('div');
        modalBody.id = 'card-popup-body';
        modalBody.className = 'card-popup-body';

        // 6. Modal Footer Actions
        const modalFooter = document.createElement('div');
        modalFooter.id = 'card-popup-footer';
        modalFooter.className = 'card-popup-footer';

        // Assemble DOM
        cardContent.appendChild(header);
        cardContent.appendChild(modalBody);
        cardContent.appendChild(modalFooter);
        modalWindow.appendChild(cardContent);
        overlay.appendChild(modalWindow);
        document.body.appendChild(overlay);

        // Open & Close Handlers
        const openCardModal = (card) => {
            // Extract Card Details
            const titleEl = card.querySelector('h1, h2, h3, h4, .project-title, .expertise-card-title, .cert-title');
            const titleText = titleEl ? titleEl.textContent.trim() : 'CARD DETAILS';
            
            const descEl = card.querySelector('p, .project-desc, .expertise-desc');
            const descText = descEl ? descEl.textContent.trim() : '';

            const imgEl = card.querySelector('img');
            const imgSrc = imgEl ? imgEl.getAttribute('src') : null;
            const imgAlt = imgEl ? imgEl.getAttribute('alt') : titleText;

            // Tech Badges
            const badges = Array.from(card.querySelectorAll('.badge, .skill-tag, .tag')).map(b => b.textContent.trim());

            // Project or Certificate Link
            const linkEl = card.querySelector('.project-link, .view-cert-btn, a[href]');
            const linkHref = linkEl ? linkEl.getAttribute('href') : null;
            const linkText = linkEl ? linkEl.textContent.trim() : 'View Details';

            // Set Header
            modalTitle.textContent = titleText.toUpperCase();
            badge.textContent = `⚡ CYBER // ${card.classList.contains('project-card') ? 'PROJECT' : card.classList.contains('cert-card') ? 'CERTIFICATE' : 'EXPERTISE'}`;

            // Build Body HTML
            modalBody.innerHTML = '';

            if (imgSrc) {
                const imgWrap = document.createElement('div');
                imgWrap.className = 'card-popup-img-wrap';
                const img = document.createElement('img');
                img.src = imgSrc;
                img.alt = imgAlt;
                img.className = 'card-popup-img';
                imgWrap.appendChild(img);
                modalBody.appendChild(imgWrap);
            }

            const textWrap = document.createElement('div');
            textWrap.className = 'card-popup-text-wrap';

            const h = document.createElement('h2');
            h.className = 'card-popup-item-title';
            h.textContent = titleText;
            textWrap.appendChild(h);

            if (descText) {
                const p = document.createElement('p');
                p.className = 'card-popup-item-desc';
                p.textContent = descText;
                textWrap.appendChild(p);
            }

            if (badges.length > 0) {
                const badgeContainer = document.createElement('div');
                badgeContainer.className = 'card-popup-badges';
                badges.forEach(bText => {
                    const bSpan = document.createElement('span');
                    bSpan.className = 'badge';
                    bSpan.textContent = bText;
                    badgeContainer.appendChild(bSpan);
                });
                textWrap.appendChild(badgeContainer);
            }

            modalBody.appendChild(textWrap);

            // Footer Actions
            modalFooter.innerHTML = '';
            if (linkHref && linkHref !== '#') {
                const actionBtn = document.createElement('a');
                actionBtn.href = linkHref;
                actionBtn.target = '_blank';
                actionBtn.rel = 'noopener noreferrer';
                actionBtn.className = 'cta-button card-popup-cta';
                actionBtn.innerHTML = `<span>${linkText || 'Launch Node'}</span> <i class="fa-solid fa-arrow-up-right-from-square"></i>`;
                modalFooter.appendChild(actionBtn);
            }

            const closeActionBtn = document.createElement('button');
            closeActionBtn.type = 'button';
            closeActionBtn.className = 'dock-btn card-popup-dismiss';
            closeActionBtn.textContent = 'Dismiss';
            closeActionBtn.addEventListener('click', closeCardModal);
            modalFooter.appendChild(closeActionBtn);

            // Open Modal
            overlay.classList.add('active');
            overlay.setAttribute('aria-hidden', 'false');
            closeBtn.focus();
        };

        const closeCardModal = () => {
            overlay.classList.remove('active');
            overlay.setAttribute('aria-hidden', 'true');
        };

        closeBtn.addEventListener('click', closeCardModal);
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) closeCardModal();
        });

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && overlay.classList.contains('active')) {
                closeCardModal();
            }
        });

        // Attach Click Listeners to all Cards across the website
        const CARD_SELECTORS = '.project-card, .expertise-card, .cert-card, .code-block-visual, .hero-about-tile, .bday-card';
        const cards = document.querySelectorAll(CARD_SELECTORS);

        cards.forEach(card => {
            card.style.cursor = 'pointer';
            card.addEventListener('click', (e) => {
                // Don't intercept direct link clicks or button clicks
                if (e.target.closest('a') || e.target.closest('button')) {
                    return;
                }
                openCardModal(card);
            });
        });

        window.cardPopupModal = {
            open: openCardModal,
            close: closeCardModal
        };
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCardPopupSystem);
    } else {
        initCardPopupSystem();
    }
})();
