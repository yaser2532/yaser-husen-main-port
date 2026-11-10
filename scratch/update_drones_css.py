with open('assets/css/drones.css', 'r', encoding='utf-8') as f:
    css = f.read()

old_block = """/* 5. Smooth Hero to Content Transition */
.hero-transition-seam {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 6rem;
    pointer-events: none;
    z-index: 5;
    background: linear-gradient(to bottom, transparent 0%, rgba(7, 6, 11, 0.4) 60%, rgba(7, 6, 11, 0.85) 100%);
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    align-items: center;
    padding-bottom: 1.25rem;
}

.hero-horizon-beam {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 1px;
    background: linear-gradient(90deg, 
        transparent 0%, 
        rgba(25, 227, 209, 0.25) 20%, 
        rgba(245, 197, 66, 0.45) 50%, 
        rgba(139, 61, 255, 0.25) 80%, 
        transparent 100%);
    box-shadow: 0 0 12px rgba(25, 227, 209, 0.45);
}

.hero-scroll-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    background: rgba(18, 10, 32, 0.65);
    border: 1px solid rgba(25, 227, 209, 0.35);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    padding: 0.4rem 0.95rem;
    border-radius: 2rem;
    cursor: pointer;
    pointer-events: auto;
    transition: all 0.3s ease;
    animation: heroScrollFloat 2.6s ease-in-out infinite;
    text-decoration: none;
}

.hero-scroll-pill:hover {
    border-color: var(--drone-gold);
    box-shadow: 0 0 16px rgba(245, 197, 66, 0.35);
    transform: translateY(-2px);
}

.scroll-mouse-icon {
    width: 14px;
    height: 22px;
    border: 1.5px solid var(--drone-turquoise);
    border-radius: 9px;
    position: relative;
    display: inline-block;
}

.scroll-wheel {
    position: absolute;
    top: 4px;
    left: 50%;
    width: 2px;
    height: 4px;
    background: var(--drone-gold);
    border-radius: 1px;
    transform: translateX(-50%);
    animation: scrollWheelAnim 1.6s ease-in-out infinite;
}

.scroll-label {
    font-family: 'Space Grotesk', var(--font-headings);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: #e2e8f0;
    text-transform: uppercase;
}

@keyframes heroScrollFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(5px); }
}

@keyframes scrollWheelAnim {
    0% { opacity: 0; transform: translate(-50%, 0); }
    40% { opacity: 1; }
    100% { opacity: 0; transform: translate(-50%, 6px); }
}"""

new_block = """/* 5. Seamless Atmospheric Hero-to-Content Blended Transition */
.hero-transition-seam {
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 100%;
    height: 12rem;
    pointer-events: none;
    z-index: 5;
    background: linear-gradient(to bottom, 
        transparent 0%, 
        rgba(4, 2, 7, 0.25) 30%, 
        rgba(4, 2, 7, 0.65) 65%, 
        rgba(4, 2, 7, 0.95) 90%, 
        #040207 100%);
    display: block;
}"""

css_norm = css.replace('\r\n', '\n')
old_norm = old_block.replace('\r\n', '\n')
assert old_norm in css_norm, "old_block not found in drones.css"
css_norm = css_norm.replace(old_norm, new_block)

with open('assets/css/drones.css', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(css_norm.replace('\n', '\r\n'))

print("Updated assets/css/drones.css successfully!")
