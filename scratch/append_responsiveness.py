with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

responsive_addon = '''

/* ==========================================================================
   Comprehensive Responsiveness & Mobile/Tablet Ergonomics Polish
   ========================================================================== */

/* 1. Global Container & Fluid Breathing Room */
.container {
    width: 100% !important;
    max-width: 75rem !important;
    margin-left: auto !important;
    margin-right: auto !important;
    padding-left: clamp(1rem, 4vw, 1.75rem) !important;
    padding-right: clamp(1rem, 4vw, 1.75rem) !important;
    box-sizing: border-box !important;
}

/* 2. Responsive Headings & Fluid Section Typography */
@media (max-width: 64rem) {
    .section-padding {
        padding: clamp(3.2rem, 7vw, 5rem) 0 !important;
    }
    .section-title {
        font-size: clamp(1.8rem, 5.5vw, 2.35rem) !important;
    }
    .section-desc {
        font-size: clamp(0.92rem, 2.5vw, 1.05rem) !important;
        max-width: 38rem !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding: 0 0.5rem !important;
    }
}

/* 3. Hero Section Fluid Scaling (Mobile & Tablet) */
@media (max-width: 48rem) {
    .hero-title {
        font-size: clamp(1.9rem, 7.5vw, 2.75rem) !important;
        line-height: 1.25 !important;
        margin-bottom: 0.65rem !important;
        word-break: break-word !important;
    }
    .hero-subtitle {
        font-size: clamp(1.0rem, 3.8vw, 1.25rem) !important;
        line-height: 1.4 !important;
        margin-bottom: 1rem !important;
    }
    .hero-details-container {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    .hero-about-tile {
        padding: 1.1rem 1.25rem !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    .utc-clock-badge,
    .status-badge,
    .cyber-spec-stamp {
        font-size: clamp(0.70rem, 2.4vw, 0.80rem) !important;
        padding: 0.35rem 0.75rem !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    .hero-cta-group {
        display: flex !important;
        flex-direction: column !important;
        width: 100% !important;
        gap: 0.75rem !important;
    }
    .hero-cta-group .cta-button {
        width: 100% !important;
        text-align: center !important;
        justify-content: center !important;
        padding: 0.85rem 1.5rem !important;
        min-height: 48px !important;
    }
}

/* 4. About Me & Code Block Visual Responsiveness */
@media (max-width: 48rem) {
    .about-grid {
        grid-template-columns: 1fr !important;
        gap: 2rem !important;
    }
    .stats-row {
        display: flex !important;
        flex-direction: column !important;
        gap: 0.85rem !important;
        width: 100% !important;
        margin-top: 1.5rem !important;
        box-sizing: border-box !important;
    }
    .stats-row .stat-card {
        width: 100% !important;
        box-sizing: border-box !important;
        padding: 1.1rem 1rem !important;
    }
    .code-block-visual {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    .terminal-header {
        padding: 0.55rem 0.85rem !important;
        flex-wrap: wrap !important;
        gap: 0.4rem !important;
    }
    .terminal-body {
        padding: 0.85rem 0.75rem !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
    }
    .drone-code-line, .code-line {
        font-size: clamp(0.70rem, 2.2vw, 0.82rem) !important;
        line-height: 1.55 !important;
    }
}

/* 5. Featured Projects & Filter Buttons */
@media (max-width: 48rem) {
    .project-filters {
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 0.5rem !important;
        margin-bottom: 2rem !important;
    }
    .filter-btn {
        white-space: nowrap !important;
        font-size: clamp(0.78rem, 2.4vw, 0.88rem) !important;
        padding: 0.5rem 1.1rem !important;
        min-height: 40px !important;
        border-radius: 2rem !important;
    }
    .projects-grid {
        grid-template-columns: 1fr !important;
        gap: 1.5rem !important;
    }
    .project-card {
        padding: 1.25rem !important;
        border-radius: 1rem !important;
    }
}

/* 6. Tablet Multi-Column Balance (48rem - 64rem) */
@media (min-width: 48.01rem) and (max-width: 64rem) {
    .expertise-grid,
    .projects-grid,
    .certificates-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 1.5rem !important;
    }
    .about-grid {
        grid-template-columns: 1fr !important;
        gap: 2.5rem !important;
    }
    .stats-row {
        display: grid !important;
        grid-template-columns: repeat(3, 1fr) !important;
        gap: 1rem !important;
    }
}

/* 7. Interactive & Creative Lab Canvases Fluidity */
.bday-card canvas,
.cake-visual canvas,
.gift-box-visual canvas,
.star-map-visual canvas,
#cakeCanvas,
#giftCanvas,
#starCanvas {
    max-width: 100% !important;
    height: auto !important;
    box-sizing: border-box !important;
}

/* 8. Mobile Form Touch Accessibility & iOS Zoom Prevention */
@media (max-width: 48rem) {
    .contact-form input,
    .contact-form textarea,
    .input-group input {
        font-size: 16px !important; /* Prevents unwanted iOS/Safari zoom */
        min-height: 44px !important;
        box-sizing: border-box !important;
    }
    .contact-form textarea {
        min-height: 120px !important;
    }
    .cyber-dock-bar {
        padding: 1rem 0.85rem !important;
        gap: 0.85rem !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    .dock-actions-col {
        width: 100% !important;
        justify-content: center !important;
        gap: 0.6rem !important;
    }
    .dock-btn {
        min-height: 42px !important;
        padding: 0.5rem 0.9rem !important;
    }
}

/* 9. Touch Devices Hover & 3D Tilt Cleanup */
@media (hover: none) {
    .project-card,
    .stat-card,
    .cert-card,
    .expertise-card,
    .bday-card,
    .cp-3d-card {
        transform: none !important;
    }
    * {
        -webkit-tap-highlight-color: transparent;
    }
}
'''

with open('assets/css/style.css', 'a', encoding='utf-8') as f:
    f.write(responsive_addon)

print('Appended responsive enhancements to assets/css/style.css!')
