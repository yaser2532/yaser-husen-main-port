def update():
    # 1. Update react-3d-cards.js settle thresholds
    with open('assets/js/react-3d-cards.js', 'r', encoding='utf-8') as f:
        js = f.read()
    
    old_settle = """            const isSettled = !this.isHovered &&
                Math.abs(this.currentRotX) < 0.04 &&
                Math.abs(this.currentRotY) < 0.04 &&
                Math.abs(this.currentTransZ) < 0.05 &&
                Math.abs(this.currentMoveX) < 0.05 &&
                Math.abs(this.currentMoveY) < 0.05 &&
                Math.abs(this.currentScale - 1.0) < 0.003;"""
                
    new_settle = """            const isSettled = !this.isHovered &&
                Math.abs(this.currentRotX) < 0.35 &&
                Math.abs(this.currentRotY) < 0.35 &&
                Math.abs(this.currentTransZ) < 0.6 &&
                Math.abs(this.currentMoveX) < 0.4 &&
                Math.abs(this.currentMoveY) < 0.4 &&
                Math.abs(this.currentScale - 1.0) < 0.005;"""
                
    if old_settle in js:
        js = js.replace(old_settle, new_settle)
        with open('assets/js/react-3d-cards.js', 'w', encoding='utf-8') as f:
            f.write(js)
        print("Updated react-3d-cards.js settle threshold")
    else:
        print("Warning: old_settle not found")

    # 2. Update style.css layer rules
    with open('assets/css/style.css', 'r', encoding='utf-8') as f:
        css = f.read()
        
    old_css = """.react-3d-card .project-details h3,
.react-3d-card .project-title,
.react-3d-card .expertise-card h4,
.react-3d-card .cert-card h4,
.react-3d-card .stat-card h4,
.react-3d-card .hero-about-tile p {
    transform: translateZ(26px) !important;
    transform-style: preserve-3d !important;
    transition: transform 0.2s ease;
}

.react-3d-card .project-details p,
.react-3d-card .expertise-card p,
.react-3d-card .cert-card p,
.react-3d-card .stat-card .stat-label {
    transform: translateZ(18px) !important;
    transform-style: preserve-3d !important;
    transition: transform 0.2s ease;
}

.react-3d-card .badge,
.react-3d-card .holo-sticker,
.react-3d-card .torn-paper-sticker,
.react-3d-card .project-link,
.react-3d-card .view-cert-btn,
.react-3d-card .project-footer {
    transform: translateZ(40px) !important;
    transform-style: preserve-3d !important;
    transition: transform 0.2s ease;
}"""

    new_css = """.react-3d-card .project-details h3,
.react-3d-card .project-title,
.react-3d-card h3,
.react-3d-card h4,
.react-3d-card .hero-about-tile p {
    transform: translateZ(26px) !important;
    transform-style: preserve-3d !important;
    transition: transform 0.2s ease;
}

.react-3d-card .project-details p,
.react-3d-card p,
.react-3d-card .stat-label {
    transform: translateZ(18px) !important;
    transform-style: preserve-3d !important;
    transition: transform 0.2s ease;
}

.react-3d-card .badge,
.react-3d-card .holo-sticker,
.react-3d-card .torn-paper-sticker,
.react-3d-card .project-link,
.react-3d-card .view-cert-btn,
.react-3d-card a.cert-link,
.react-3d-card a.btn,
.react-3d-card .project-footer {
    transform: translateZ(40px) !important;
    transform-style: preserve-3d !important;
    transition: transform 0.2s ease;
}"""

    if old_css in css:
        css = css.replace(old_css, new_css)
        with open('assets/css/style.css', 'w', encoding='utf-8') as f:
            f.write(css)
        print("Updated style.css layer rules")
    else:
        print("Warning: old_css not found")

if __name__ == '__main__':
    update()
