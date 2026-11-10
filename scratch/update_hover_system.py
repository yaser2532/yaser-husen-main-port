with open("assets/js/hover-system.js", "r", encoding="utf-8") as f:
    content = f.read()

target = """    /* =========================================================================
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
    });"""

replacement = """    /* =========================================================================
       H-05 / 3D-03: CARDS KINETIC 3D DEPTH ENGINE (MANAGED BY REACT-3D-CARDS.JS)
       ========================================================================= */
    if (window.React3DCard) {
        // Defer 3D physics, multi-layer parallax, and backward depth push to React 3D Card Engine
        // No redundant event listeners attached to prevent frame contention
    } else {
        const cardSelector = '.project-card, .cert-card, .expertise-card, .onboard-card, .stat-card, .glass-card, .bday-card, .code-block-visual, .hero-about-tile, .contact-card, .profile-card-wrapper';
        const cards = document.querySelectorAll(cardSelector);
        cards.forEach(card => {
            card.classList.add('cp-3d-card');

            card.addEventListener('mousemove', (e) => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;

                const normX = (x / rect.width) * 2 - 1;
                const normY = (y / rect.height) * 2 - 1;

                const moveX = (normX * 9.5).toFixed(1);
                const moveY = (normY * 7.5).toFixed(1);

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
    }"""

# Normalize CRLF for matching
normalized_content = content.replace('\r\n', '\n')
normalized_target = target.replace('\r\n', '\n')

if normalized_target in normalized_content:
    updated = normalized_content.replace(normalized_target, replacement)
    with open("assets/js/hover-system.js", "w", encoding="utf-8") as f:
        f.write(updated)
    print("Successfully updated hover-system.js!")
else:
    print("Target not found in hover-system.js!")
