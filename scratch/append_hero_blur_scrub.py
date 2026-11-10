import sys

sys.stdout.reconfigure(encoding='utf-8')

SCRIPT_PATH = 'assets/js/script.js'

with open(SCRIPT_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

new_logic = """

/* ==========================================================================
   GSAP SCROLLTRIGGER & LENIS INERTIAL BLUR TRANSITION (Hero to Profile)
   ========================================================================== */

function initHeroToExpertiseBlurScrub() {
    const heroEl = document.querySelector('#home .header-content') || document.getElementById('home');
    const profileEl = document.getElementById('profile-expertise');
    if (!heroEl || !profileEl) return;

    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    let targetProgress = 0;
    let currentProgress = 0;
    let isTicking = false;
    let animId = null;

    function calculateProgress() {
        const scrollY = window.scrollY || window.pageYOffset;
        const vh = window.innerHeight;
        // Scrub transition active across scroll from 0 to 85% of viewport height
        const transitionDistance = vh * 0.85;
        targetProgress = Math.max(0, Math.min(1, scrollY / transitionDistance));
    }

    function renderScrub() {
        // Lenis-style inertial dampening lerp
        currentProgress += (targetProgress - currentProgress) * 0.12;

        if (Math.abs(targetProgress - currentProgress) < 0.001) {
            currentProgress = targetProgress;
        }

        const p = currentProgress;

        // 1. Hero Content exits: progressively blurs out (0 -> 12px), scales (1 -> 0.94), glides up, and fades
        if (p < 0.005) {
            heroEl.style.filter = '';
            heroEl.style.transform = '';
            heroEl.style.opacity = '';
            heroEl.style.willChange = '';
        } else if (p > 0.995) {
            heroEl.style.filter = 'blur(12px)';
            heroEl.style.transform = 'translate3d(0, -35px, 0) scale(0.94)';
            heroEl.style.opacity = '0';
            heroEl.style.willChange = '';
        } else {
            const heroBlur = (p * 12).toFixed(1);
            const heroScale = (1.0 - p * 0.06).toFixed(3);
            const heroY = (-p * 35).toFixed(1);
            const heroOpacity = Math.max(0, 1.0 - p * 1.05).toFixed(3);
            heroEl.style.filter = `blur(${heroBlur}px)`;
            heroEl.style.transform = `translate3d(0, ${heroY}px, 0) scale(${heroScale})`;
            heroEl.style.opacity = heroOpacity;
            heroEl.style.willChange = 'transform, filter, opacity';
        }

        // 2. Profile & Expertise Section enters: starts with optical depth blur (14px -> 0px) and glide (40px -> 0px)
        const scrollY = window.scrollY || window.pageYOffset;
        const vh = window.innerHeight;
        if (scrollY > vh * 1.5) {
            profileEl.style.filter = '';
            profileEl.style.transform = '';
            profileEl.style.opacity = '';
            profileEl.style.willChange = '';
        } else {
            // Profile blur in: at p=0, blur 14px; at p=1, blur 0px
            const easeP = p * p * (3 - 2 * p); // smoothstep
            const profileBlur = Math.max(0, (1.0 - easeP) * 14).toFixed(1);
            const profileY = ((1.0 - easeP) * 40).toFixed(1);
            const profileOpacity = (0.25 + easeP * 0.75).toFixed(3);

            if (p > 0.99) {
                profileEl.style.filter = '';
                profileEl.style.transform = '';
                profileEl.style.opacity = '';
                profileEl.style.willChange = '';
            } else {
                profileEl.style.filter = `blur(${profileBlur}px)`;
                profileEl.style.transform = `translate3d(0, ${profileY}px, 0)`;
                profileEl.style.opacity = profileOpacity;
                profileEl.style.willChange = 'transform, filter, opacity';
            }
        }

        if (Math.abs(targetProgress - currentProgress) > 0.001) {
            animId = requestAnimationFrame(renderScrub);
        } else {
            isTicking = false;
        }
    }

    function onScroll() {
        calculateProgress();
        if (!isTicking) {
            isTicking = true;
            animId = requestAnimationFrame(renderScrub);
        }
    }

    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll, { passive: true });

    calculateProgress();
    currentProgress = targetProgress;
    renderScrub();
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initHeroToExpertiseBlurScrub);
} else {
    initHeroToExpertiseBlurScrub();
}
"""

content += new_logic

with open(SCRIPT_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("Appended initHeroToExpertiseBlurScrub to script.js successfully!")
