with open('assets/js/hover-system.js', 'r', encoding='utf-8') as f:
    content = f.read()

old_card_block = '''    /* =========================================================================
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

            // Max 6.5 degrees tilt for buttery smooth response without jitter
            const maxTilt = 6.5;
            const rotX = -normY * maxTilt;
            const rotY = normX * maxTilt;

            card.style.transition = 'none';
            card.style.transform = `perspective(900px) rotateX(${rotX.toFixed(2)}deg) rotateY(${rotY.toFixed(2)}deg) scale3d(1.018, 1.018, 1.018)`;
            card.style.setProperty('--card-mouse-x', `${(x / rect.width * 100).toFixed(1)}%`);
            card.style.setProperty('--card-mouse-y', `${(y / rect.height * 100).toFixed(1)}%`);
        });

        card.addEventListener('mouseleave', () => {
            card.style.transition = 'transform 0.45s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s ease, border-color 0.3s ease';
            card.style.transform = 'perspective(900px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
        });
    });'''

new_card_block = '''    /* =========================================================================
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
    });'''

assert old_card_block in content, 'old_card_block not found in hover-system.js'
content = content.replace(old_card_block, new_card_block, 1)

with open('assets/js/hover-system.js', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated card hover behavior in hover-system.js successfully!')
