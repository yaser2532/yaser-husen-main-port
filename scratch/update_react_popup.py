with open('assets/js/react-3d-cards.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """        handleMouseEnter(e) {
            this.isHovered = true;
            this.targetTransZ = 28.0; // Physical 3D lift forward
            this.targetScale = 1.025; // 3D expansion
            this.el.classList.add('card-3d-active');
            this.el.style.setProperty('transition', 'none', 'important');
            this.startLoop();
        }

        handleMouseMove(e) {
            const rect = this.el.getBoundingClientRect();
            if (!rect.width || !rect.height) return;

            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Normalized coordinates (-1 to 1) from card center
            const normX = (x / rect.width) * 2 - 1;
            const normY = (y / rect.height) * 2 - 1;

            // Authentic 3D Tilt angles tracking cursor (up to 18.5 degrees)
            const MAX_TILT = 18.5;
            this.targetRotX = -normY * MAX_TILT; // Tilts toward cursor in Y
            this.targetRotY = normX * MAX_TILT;  // Tilts toward cursor in X

            // 3D Elevation & Micro-magnetic drift
            this.targetTransZ = 32.0;
            this.targetScale = 1.028;
            this.targetMoveX = normX * 9.0;
            this.targetMoveY = normY * 7.0;"""

replacement = """        handleMouseEnter(e) {
            this.isHovered = true;
            this.targetTransZ = 32.0; // Physical 3D pop-up lift forward
            this.targetMoveY = -8.0;  // Spring pop-up elevation
            this.targetScale = 1.03;  // Pop-up scale
            this.el.classList.add('card-3d-active');
            this.el.style.setProperty('transition', 'none', 'important');
            this.startLoop();
        }

        handleMouseMove(e) {
            const rect = this.el.getBoundingClientRect();
            if (!rect.width || !rect.height) return;

            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            // Normalized coordinates (-1 to 1) from card center
            const normX = (x / rect.width) * 2 - 1;
            const normY = (y / rect.height) * 2 - 1;

            // Authentic 3D Tilt angles tracking cursor (up to 16.5 degrees)
            const MAX_TILT = 16.5;
            this.targetRotX = -normY * MAX_TILT; // Tilts toward cursor in Y
            this.targetRotY = normX * MAX_TILT;  // Tilts toward cursor in X

            // 3D Pop-Up Elevation & Micro-magnetic drift (AI Chat Box Pop-Up Physics)
            this.targetTransZ = 34.0;
            this.targetScale = 1.03;
            this.targetMoveX = normX * 8.0;
            this.targetMoveY = -10.0 + normY * 6.0;"""

if target in js:
    js = js.replace(target, replacement)
    with open('assets/js/react-3d-cards.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Updated react-3d-cards.js with pop-up elevation")
else:
    print("Warning: target block not found")
