import re

style_path = 'assets/css/style.css'
script_path = 'assets/js/script.js'

# --- 1. Update style.css ---
with open(style_path, 'r', encoding='utf-8') as f:
    style_text = f.read().replace('\r\n', '\n')

# Replace Navbar Desktop section (around line 370)
nav_pattern = r'/\* ==========================================================================\s*Navigation\s*========================================================================== \*/.*?\.burger div \{.*?\}'

nav_replacement = """/* ==========================================================================
   Navigation
   ========================================================================== */
#navbar {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    z-index: 1000;
    transition: padding 0.25s cubic-bezier(0.16, 1, 0.3, 1), background-color 0.25s ease, backdrop-filter 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
    padding: 0.75rem 0;
    background: rgba(7, 6, 11, 0.35);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

#navbar.scrolled {
    padding: 0.45rem 0;
    background-color: rgba(7, 6, 11, 0.92);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border-bottom: 1px solid rgba(25, 227, 209, 0.22);
    box-shadow: 0 0.25rem 1.75rem rgba(0, 0, 0, 0.75), 0 0 15px rgba(25, 227, 209, 0.08);
}

.nav-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 82rem;
    margin: 0 auto;
    padding: 0 1.75rem;
    position: relative;
}

.logo {
    font-family: var(--font-headings);
    font-size: 1.35rem;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.5px;
    user-select: none;
    transition: transform 0.2s ease;
}

.logo:hover {
    transform: scale(1.05);
}

.logo-accent {
    background: linear-gradient(135deg, var(--accent-color) 0%, var(--accent-hover) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.nav-links {
    display: flex;
    align-items: center;
    gap: clamp(0.6rem, 1.6vw, 1.65rem);
    list-style: none;
    margin: 0;
    padding: 0;
}

.nav-links li {
    display: inline-flex;
}

.nav-links a {
    font-family: 'Space Grotesk', var(--font-headings);
    font-size: clamp(0.82rem, 1.0vw, 0.92rem);
    font-weight: 600;
    letter-spacing: 0.02em;
    color: #cbd5e1;
    position: relative;
    padding: 0.35rem 0.75rem;
    border-radius: 20px;
    border: 1px solid transparent;
    text-decoration: none;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.nav-links a:hover {
    color: #ffffff;
    background: rgba(25, 227, 209, 0.08);
    border-color: rgba(25, 227, 209, 0.3);
    box-shadow: 0 0 12px rgba(25, 227, 209, 0.2);
    transform: translateY(-1px);
}

.nav-links a:active {
    transform: scale(0.96);
}

.nav-links a.active {
    color: #ffffff !important;
    background: rgba(25, 227, 209, 0.12) !important;
    border-color: rgba(25, 227, 209, 0.45) !important;
    box-shadow: 0 0 14px rgba(25, 227, 209, 0.3) !important;
}

.nav-links a.active::before {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 50%;
    transform: translateX(-50%);
    width: 14px;
    height: 2px;
    border-radius: 2px;
    background: var(--cp-gold);
    box-shadow: 0 0 8px var(--cp-gold);
}

.nav-actions {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    flex-shrink: 0;
}

.nav-resume-btn {
    padding: 0.38rem 1.05rem !important;
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.04em !important;
    border-radius: 2rem !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 0.45rem !important;
    text-decoration: none !important;
}

.nav-sound-btn {
    width: 2.15rem !important;
    height: 2.15rem !important;
    border-radius: 50% !important;
    font-size: 0.85rem !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(25, 227, 208, 0.35) !important;
    color: var(--cp-turquoise) !important;
    cursor: pointer !important;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
}

.nav-sound-btn:hover {
    border-color: var(--cp-turquoise) !important;
    box-shadow: 0 0 14px rgba(25, 227, 209, 0.5) !important;
    transform: scale(1.08) !important;
}

.nav-sound-btn:active {
    transform: scale(0.92) !important;
}

.burger {
    display: none;
    cursor: pointer;
    background: transparent;
    border: none;
    outline: none;
}

.burger div {
    width: 22px;
    height: 2px;
    background-color: var(--text-primary);
    margin: 4px 0;
    transition: transform 0.25s ease, opacity 0.25s ease, background-color 0.25s ease;
    border-radius: 2px;
}"""

if re.search(nav_pattern, style_text, re.DOTALL):
    style_text = re.sub(nav_pattern, nav_replacement, style_text, count=1, flags=re.DOTALL)
    print("Replaced Navbar styles in style.css.")
else:
    print("Warning: nav_pattern not found in style.css!")

# Replace Footer & Dock Bar styles (decreased height)
footer_pattern = r'footer\.cyber-dock-footer, footer \{.*?\.dock-btn \{.*?\n\}'

footer_replacement = """footer.cyber-dock-footer, footer {
    background-color: transparent !important;
    padding: 0.65rem 0 0.85rem !important; /* Decreased overall height */
    border-top: none;
    position: relative;
    z-index: 10;
}

.cyber-dock-bar {
    max-width: 68rem;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0.42rem 1.25rem;
    border-radius: 2rem;
    background: rgba(14, 7, 26, 0.75) !important;
    border: 1px solid rgba(157, 77, 255, 0.32) !important;
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    box-shadow: 0 0.35rem 1.5rem rgba(0, 0, 0, 0.65), 0 0 1rem rgba(157, 77, 255, 0.15);
    gap: 0.9rem;
    flex-wrap: wrap;
}

/* Brand & Status Column */
.dock-brand-col {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    flex-shrink: 0;
}

.dock-logo {
    font-family: 'Space Grotesk', var(--font-headings);
    font-size: 1.05rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -0.02em;
}

.dock-dot {
    color: var(--cp-turquoise);
}

.dock-status-indicator {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(25, 227, 208, 0.08);
    border: 1px solid rgba(25, 227, 208, 0.28);
    padding: 0.15rem 0.5rem;
    border-radius: 2rem;
}

.dock-status-label {
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    color: var(--cp-turquoise);
}

.dock-copy {
    font-size: 0.75rem;
    color: var(--text-muted);
}

/* Center Social Column */
.dock-social-col {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.dock-icon-btn {
    width: 1.95rem;
    height: 1.95rem;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.12);
    color: #f3eeff;
    font-size: 0.82rem;
    transition: all 0.2s ease;
}

.dock-icon-btn:hover {
    background: rgba(25, 227, 208, 0.18);
    border-color: var(--cp-turquoise);
    color: var(--cp-turquoise);
    box-shadow: 0 0 10px rgba(25, 227, 208, 0.5);
    transform: translateY(-2px);
}

/* Right Action Buttons Column */
.dock-actions-col {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    flex-shrink: 0;
}

.dock-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.32rem 0.85rem !important;
    border-radius: 2rem;
    font-size: 0.78rem !important;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}"""

if re.search(footer_pattern, style_text, re.DOTALL):
    style_text = re.sub(footer_pattern, footer_replacement, style_text, count=1, flags=re.DOTALL)
    print("Replaced Footer styles in style.css.")
else:
    print("Warning: footer_pattern not found in style.css!")

# Update mobile media queries for nav drawer and footer dock
mobile_nav_pattern = r'/\* Mobile burger navigation menu \*/.*?\.toggle \.line3 \{.*?\}'

mobile_nav_replacement = """/* Mobile burger navigation menu (Reactive & Accessible) */
    .nav-links {
        display: flex;
        flex-direction: column;
        position: absolute;
        top: 100%;
        left: 0;
        width: 100%;
        background-color: rgba(7, 5, 14, 0.96);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        text-align: center;
        padding: 1.25rem 1rem 1.5rem;
        gap: 0.65rem;
        transform: translateY(-130%);
        opacity: 0;
        pointer-events: none;
        transition: transform 0.32s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.22s ease;
        box-shadow: 0 1rem 2.5rem rgba(0, 0, 0, 0.85);
        border-bottom: 1px solid rgba(25, 227, 209, 0.25);
        z-index: 999;
    }

    .nav-active .nav-links {
        transform: translateY(0%);
        opacity: 1;
        pointer-events: auto;
    }

    .nav-links li {
        width: 100%;
    }

    .nav-links a {
        width: 100%;
        padding: 0.75rem 1.25rem;
        font-size: 1.05rem;
        border-radius: 0.75rem;
        min-height: 44px;
        justify-content: center;
    }

    .burger {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        width: 38px;
        height: 38px;
        cursor: pointer;
        padding: 6px;
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.12);
        transition: all 0.2s ease;
        margin-left: 0.25rem;
    }

    .burger:hover {
        background: rgba(25, 227, 209, 0.12);
        border-color: var(--cp-turquoise);
    }

    .toggle .line1 { transform: rotate(-45deg) translate(-4px, 4.5px); background-color: var(--cp-turquoise); }
    .toggle .line2 { opacity: 0; transform: translateX(8px); }
    .toggle .line3 { transform: rotate(45deg) translate(-4px, -4.5px); background-color: var(--cp-turquoise); }"""

if re.search(mobile_nav_pattern, style_text, re.DOTALL):
    style_text = re.sub(mobile_nav_pattern, mobile_nav_replacement, style_text, count=1, flags=re.DOTALL)
    print("Replaced mobile nav drawer styles.")
else:
    print("Warning: mobile_nav_pattern not found!")

# Save style.css
with open(style_path, 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(style_text)
print("Saved style.css successfully.")


# --- 2. Update script.js ---
with open(script_path, 'r', encoding='utf-8') as f:
    script_text = f.read().replace('\r\n', '\n')

# Replace mobile burger logic with full reactive handlers
burger_old = """    /* --- 3. Mobile Burger Menu Toggle --- */
    const burger = document.querySelector('.burger');
    const navContainer = document.querySelector('.nav-container'); 
    
    if (burger) {
        burger.addEventListener('click', () => {
            navContainer.classList.toggle('nav-active');
            burger.classList.toggle('toggle');
        });
    }

    // Close menu when clicking navigation links
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            navContainer.classList.remove('nav-active');
            if (burger) burger.classList.remove('toggle');
        });
    });"""

burger_new = """    /* --- 3. Mobile Burger Menu Toggle & Reactive Listeners --- */
    const burger = document.querySelector('.burger');
    const navContainer = document.querySelector('.nav-container'); 
    
    function closeNavDrawer() {
        if (navContainer && navContainer.classList.contains('nav-active')) {
            navContainer.classList.remove('nav-active');
            if (burger) {
                burger.classList.remove('toggle');
                burger.setAttribute('aria-expanded', 'false');
            }
        }
    }

    if (burger) {
        burger.setAttribute('aria-expanded', 'false');
        burger.addEventListener('click', (e) => {
            e.stopPropagation();
            const isOpen = navContainer.classList.toggle('nav-active');
            burger.classList.toggle('toggle');
            burger.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
        });
    }

    // Close menu on link click
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            closeNavDrawer();
        });
    });

    // Close menu on outside click
    document.addEventListener('click', (e) => {
        if (!e.target.closest('#navbar')) {
            closeNavDrawer();
        }
    });

    // Close menu on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeNavDrawer();
        }
    });

    // Auto-close menu if resized above mobile breakpoint
    window.addEventListener('resize', () => {
        if (window.innerWidth > 960) {
            closeNavDrawer();
        }
    }, { passive: true });"""

if burger_old in script_text:
    script_text = script_text.replace(burger_old, burger_new)
    print("Updated burger menu script in script.js.")
else:
    print("Warning: burger_old not found in script.js!")

with open(script_path, 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(script_text)
print("Saved script.js successfully.")
