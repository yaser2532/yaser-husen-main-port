with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Remove dart pulse ring from updateFollow
old_dart_pulse = """                // Micro-sonar radar ping on energetic dart

                if (Math.random() < 0.40 && pulseRings.length < 8) {

                    emitPulseRing(this.x, this.y, this.color, 18, 220);

                }"""

new_dart_pulse = """"""

assert old_dart_pulse in c, "old_dart_pulse not found"
c = c.replace(old_dart_pulse, new_dart_pulse, 1)

# 2. Add cursor movement sonar ping (throttled to 400ms, clean & minimal)
old_mouse = """        const dx = e.clientX - targetCursorX;

        const dy = e.clientY - targetCursorY;

        if (Math.hypot(dx, dy) > 1.2) {

            lastCursorMoveTime = performance.now();

        }

        targetCursorX = e.clientX;

        targetCursorY = e.clientY;"""

new_mouse = """        const dx = e.clientX - targetCursorX;

        const dy = e.clientY - targetCursorY;

        const distMoved = Math.hypot(dx, dy);

        if (distMoved > 1.2) {

            lastCursorMoveTime = performance.now();

        }

        if (distMoved > 24 && performance.now() - lastSonarPingTime > 400) {

            lastSonarPingTime = performance.now();

            emitPulseRing(e.clientX, e.clientY, THEME.cyan, 26, 260);

        }

        targetCursorX = e.clientX;

        targetCursorY = e.clientY;"""

assert old_mouse in c, "old_mouse not found"
c = c.replace(old_mouse, new_mouse, 1)

# Add let lastSonarPingTime = 0; near lastCursorMoveTime
old_lcm = """    let lastCursorMoveTime = performance.now();"""
new_lcm = """    let lastCursorMoveTime = performance.now();

    let lastSonarPingTime = 0;"""

assert old_lcm in c, "old_lcm not found"
c = c.replace(old_lcm, new_lcm, 1)

with open('assets/js/drones.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Refined pulse rings to be clean, minimal and zero clutter!")
