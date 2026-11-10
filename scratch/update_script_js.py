with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update lines 2873-2941
old_scroll_listener = """    window.addEventListener('scroll', () => {



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

new_scroll_listener = """    let navScrollTicking = false;
    const headerContentEl = document.querySelector('.header-content');

    window.addEventListener('scroll', () => {
        if (!navScrollTicking) {
            navScrollTicking = true;
            requestAnimationFrame(() => {
                handleNavbarScroll();

                const scrolled = window.scrollY;
                const heroHeight = window.innerHeight;

                if (headerContentEl && scrolled <= heroHeight) {
                    const percent = scrolled / heroHeight;
                    headerContentEl.style.opacity = (1 - percent * 0.92).toFixed(3);
                    headerContentEl.style.transform = `translate3d(0, ${(percent * 45).toFixed(1)}px, 0)`;
                }

                if (backToTop) {
                    backToTop.style.opacity = (scrolled > 800) ? '1' : '0';
                    backToTop.style.pointerEvents = (scrolled > 800) ? 'auto' : 'none';
                }

                navScrollTicking = false;
            });
        }
    }, { passive: true });"""

if old_scroll_listener in content:
    content = content.replace(old_scroll_listener, new_scroll_listener)
    print("Replaced scroll listener in script.js")
else:
    print("Error: old_scroll_listener not matched exactly")

# 2. Update lines 8603-8675 to eliminate filter: blur(...)
old_blur_scrub = """        if (p < 0.01) {

            heroEl.style.filter = '';

            heroEl.style.transform = '';

            heroEl.style.opacity = '';

            heroEl.style.willChange = '';

        } else if (p >= 0.98) {

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



        if (p >= 0.90) {

            profileEl.style.filter = '';

            profileEl.style.transform = '';

            profileEl.style.opacity = '';

            profileEl.style.willChange = '';

        } else {

            const easeP = p * p * (3 - 2 * p);

            const profileBlur = Math.max(0, (1.0 - easeP) * 14).toFixed(1);

            const profileY = ((1.0 - easeP) * 40).toFixed(1);

            const profileOpacity = (0.25 + easeP * 0.75).toFixed(3);



            profileEl.style.filter = `blur(${profileBlur}px)`;

            profileEl.style.transform = `translate3d(0, ${profileY}px, 0)`;

            profileEl.style.opacity = profileOpacity;

            profileEl.style.willChange = 'transform, filter, opacity';

        }"""

new_blur_scrub = """        if (p < 0.01) {
            heroEl.style.filter = '';
            heroEl.style.transform = '';
            heroEl.style.opacity = '';
            heroEl.style.willChange = '';
        } else if (p >= 0.98) {
            heroEl.style.filter = '';
            heroEl.style.transform = 'translate3d(0, -35px, 0) scale(0.94)';
            heroEl.style.opacity = '0';
            heroEl.style.willChange = '';
        } else {
            const heroScale = (1.0 - p * 0.06).toFixed(3);
            const heroY = (-p * 35).toFixed(1);
            const heroOpacity = Math.max(0, 1.0 - p * 1.05).toFixed(3);

            heroEl.style.filter = '';
            heroEl.style.transform = `translate3d(0, ${heroY}px, 0) scale(${heroScale})`;
            heroEl.style.opacity = heroOpacity;
            heroEl.style.willChange = 'transform, opacity';
        }

        if (p >= 0.90) {
            profileEl.style.filter = '';
            profileEl.style.transform = '';
            profileEl.style.opacity = '';
            profileEl.style.willChange = '';
        } else {
            const easeP = p * p * (3 - 2 * p);
            const profileY = ((1.0 - easeP) * 40).toFixed(1);
            const profileOpacity = (0.25 + easeP * 0.75).toFixed(3);

            profileEl.style.filter = '';
            profileEl.style.transform = `translate3d(0, ${profileY}px, 0)`;
            profileEl.style.opacity = profileOpacity;
            profileEl.style.willChange = 'transform, opacity';
        }"""

if old_blur_scrub in content:
    content = content.replace(old_blur_scrub, new_blur_scrub)
    print("Replaced blur scrub in script.js")
else:
    print("Error: old_blur_scrub not matched exactly")

with open('assets/js/script.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished updating script.js")
