import re

def update_css():
    with open('assets/css/style.css', 'r', encoding='utf-8') as f:
        css = f.read()

    # 1. Eliminate black gap on right end: Remove scale(0.98) from .scroll-reveal
    old_scroll_reveal = """.scroll-reveal {

    opacity: 0;

    transform: translateY(0.9375rem) scale(0.98);

    transition: opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1), transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);

    will-change: opacity, transform;

}

.scroll-reveal.active {

    opacity: 1;

    transform: translateY(0) scale(1);

}

.fade-left {

    transform: translateX(-0.9375rem) scale(0.98);

}

.fade-right {

    transform: translateX(0.9375rem) scale(0.98);

}

.scroll-reveal.fade-left.active,

.scroll-reveal.fade-right.active {

    transform: translate(0) scale(1);

}"""

    new_scroll_reveal = """.scroll-reveal {

    opacity: 0;

    transform: translateY(1.2rem);

    transition: opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1), transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);

    will-change: opacity, transform;

}

.scroll-reveal.active {

    opacity: 1;

    transform: translateY(0);

}

.fade-left {

    transform: translateX(-1.2rem);

}

.fade-right {

    transform: translateX(1.2rem);

}

.scroll-reveal.fade-left.active,

.scroll-reveal.fade-right.active {

    transform: translate(0);

}"""

    if old_scroll_reveal in css:
        css = css.replace(old_scroll_reveal, new_scroll_reveal)
        print("Updated .scroll-reveal to remove scale(0.98)")
    else:
        # Regex fallback
        pattern = r"\.scroll-reveal\s*\{[^}]*transform:\s*translateY\([^)]+\)\s*scale\(0\.98\);[^}]*\}"
        if re.search(pattern, css):
            css = re.sub(pattern, """.scroll-reveal {
    opacity: 0;
    transform: translateY(1.2rem);
    transition: opacity 0.5s cubic-bezier(0.16, 1, 0.3, 1), transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
    will-change: opacity, transform;
}""", css)
            print("Updated .scroll-reveal via regex")

    # Ensure html, body, section, header, footer have 100% width and overflow-x hidden
    global_full_width_block = """
/* =========================================================================
   ZERO HORIZONTAL OVERFLOW & FULL-BLEED SECTIONS (NO BLACK GAP ON RIGHT)
   ========================================================================= */
html, body {
    width: 100% !important;
    max-width: 100vw !important;
    overflow-x: hidden !important;
    box-sizing: border-box !important;
}

section, header, footer, main, .cyber-dock-footer {
    width: 100% !important;
    max-width: 100% !important;
    box-sizing: border-box !important;
}
"""

    if "ZERO HORIZONTAL OVERFLOW & FULL-BLEED SECTIONS" not in css:
        css = css + "\n" + global_full_width_block
        print("Added global full-width zero horizontal overflow rules")

    with open('assets/css/style.css', 'w', encoding='utf-8') as f:
        f.write(css)

if __name__ == '__main__':
    update_css()
