with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update mousemove / touchmove to track lastCursorMoveTime
old_mouse = """    window.addEventListener('mousemove', (e) => {

        isTouchMode = false;

        cursorInWindow = true;

        targetCursorX = e.clientX;

        targetCursorY = e.clientY;

        checkDimUnderPointer(e.clientX, e.clientY);

    }, { passive: true });



    window.addEventListener('touchmove', (e) => {

        isTouchMode = true;

        cursorInWindow = true;

        if (e.touches && e.touches[0]) {

            targetCursorX = e.touches[0].clientX;

            targetCursorY = e.touches[0].clientY;

            checkDimUnderPointer(targetCursorX, targetCursorY);

        }

    }, { passive: true });"""

new_mouse = """    let lastCursorMoveTime = performance.now();

    window.addEventListener('mousemove', (e) => {

        isTouchMode = false;

        cursorInWindow = true;

        const dx = e.clientX - targetCursorX;

        const dy = e.clientY - targetCursorY;

        if (Math.hypot(dx, dy) > 1.2) {

            lastCursorMoveTime = performance.now();

        }

        targetCursorX = e.clientX;

        targetCursorY = e.clientY;

        checkDimUnderPointer(e.clientX, e.clientY);

    }, { passive: true });



    window.addEventListener('touchmove', (e) => {

        isTouchMode = true;

        cursorInWindow = true;

        if (e.touches && e.touches[0]) {

            const dx = e.touches[0].clientX - targetCursorX;

            const dy = e.touches[0].clientY - targetCursorY;

            if (Math.hypot(dx, dy) > 1.2) {

                lastCursorMoveTime = performance.now();

            }

            targetCursorX = e.touches[0].clientX;

            targetCursorY = e.touches[0].clientY;

            checkDimUnderPointer(targetCursorX, targetCursorY);

        }

    }, { passive: true });"""

assert old_mouse in c, "old_mouse block not found"
c = c.replace(old_mouse, new_mouse, 1)

# 2. Update Drone constructor trail definition
old_constructor_trail = """            // Firefly Light Tail: 16 history points of dissolving light trace

            this.trail = [];

            this.maxTrail = 16;"""

new_constructor_trail = """            // Firefly Light Tail: Sleek, thin, agile trace appearing only when relocating to new positions

            this.trail = [];

            this.maxTrail = 6; // Reduced from 16 to 6 for a short, crisp tail

            this.tailAlpha = 0.0; // Dynamic intensity multiplier

            this.isRelocating = false;"""

assert old_constructor_trail in c, "old_constructor_trail block not found"
c = c.replace(old_constructor_trail, new_constructor_trail, 1)

# 3. Update updateFollow tail logic
old_update_follow_tail = """            // Smooth DIM transition: 150ms fade to 0.3 over text, 250ms restore to 1.0

            const targetOp = (!cursorInWindow) ? 0.60 : (isOverText ? 0.30 : 1.0);

            const fadeSpeed = (targetOp < this.opacity) ? Math.min(1.0, dt / 0.065) : Math.min(1.0, dt / 0.095);

            this.opacity += (targetOp - this.opacity) * fadeSpeed;



            this.pushTrail();"""

new_update_follow_tail = """            // Smooth DIM transition: 150ms fade to 0.3 over text, 250ms restore to 1.0

            const targetOp = (!cursorInWindow) ? 0.60 : (isOverText ? 0.30 : 1.0);

            const fadeSpeed = (targetOp < this.opacity) ? Math.min(1.0, dt / 0.065) : Math.min(1.0, dt / 0.095);

            this.opacity += (targetOp - this.opacity) * fadeSpeed;



            // Tail appears ONLY when moving from a fixed position to a new position

            const droneSpeed = Math.hypot(this.vx, this.vy);

            const distToDesired = Math.hypot(desiredX - this.x, desiredY - this.y);

            const cursorIsMoving = (now - lastCursorMoveTime < 240);

            const isRelocating = cursorIsMoving && (distToDesired > 5.0 || droneSpeed > 2.2);

            this.isRelocating = isRelocating;



            const targetTailAlpha = isRelocating ? Math.min(1.0, Math.max(0.2, (droneSpeed - 1.8) / 3.0)) : 0.0;

            const tailFadeRate = isRelocating ? Math.min(1.0, dt * 14) : Math.min(1.0, dt * 10);

            this.tailAlpha += (targetTailAlpha - this.tailAlpha) * tailFadeRate;



            this.pushTrail();"""

assert old_update_follow_tail in c, "old_update_follow_tail block not found"
c = c.replace(old_update_follow_tail, new_update_follow_tail, 1)

# 4. Update updateFlight tail logic
old_update_flight_tail = """            this.opacity = 1.0;

            this.pushTrail();"""

new_update_flight_tail = """            this.opacity = 1.0;



            // Active mission flight between fixed positions across screen

            this.isRelocating = true;

            const targetTailAlpha = 1.0;

            this.tailAlpha += (targetTailAlpha - this.tailAlpha) * Math.min(1.0, dt * 14);



            this.pushTrail();"""

assert old_update_flight_tail in c, "old_update_flight_tail block not found"
c = c.replace(old_update_flight_tail, new_update_flight_tail, 1)

# 5. Update updatePull tail logic
old_update_pull_tail = """            this.y = this.targetAnchor.y + jitterY;

            this.opacity = 1.0;

            this.pushTrail();"""

new_update_pull_tail = """            this.y = this.targetAnchor.y + jitterY;

            this.opacity = 1.0;



            // Stationed at fixed anchor while pulling: no tail

            this.isRelocating = false;

            const targetTailAlpha = 0.0;

            this.tailAlpha += (targetTailAlpha - this.tailAlpha) * Math.min(1.0, dt * 16);



            this.pushTrail();"""

assert old_update_pull_tail in c, "old_update_pull_tail block not found"
c = c.replace(old_update_pull_tail, new_update_pull_tail, 1)

# 6. Update pushTrail logic
old_push_trail = """        pushTrail() {

            this.trail.unshift({ x: this.x, y: this.y, opacity: this.opacity });

            if (this.trail.length > this.maxTrail) {

                this.trail.pop();

            }

        }"""

new_push_trail = """        pushTrail() {

            if (this.tailAlpha > 0.04) {

                this.trail.unshift({ x: this.x, y: this.y, alpha: this.tailAlpha });

                if (this.trail.length > this.maxTrail) {

                    this.trail.pop();

                }

            } else if (this.trail.length > 0) {

                // Rapidly drain trail when settled at fixed position

                this.trail.pop();

            }

        }"""

assert old_push_trail in c, "old_push_trail block not found"
c = c.replace(old_push_trail, new_push_trail, 1)

# 7. Update draw(ctx) tail rendering to be thin and only appear when tailAlpha > 0.03
old_draw_tail = """        draw(ctx) {

            // Firefly Light Tail: Smooth glowing ribbon of disappearing bioluminescent light

            if (this.trail.length > 2) {

                ctx.save();

                

                // 1. Outer luminous aura ribbon

                ctx.beginPath();

                ctx.moveTo(this.trail[0].x, this.trail[0].y);

                for (let i = 1; i < this.trail.length - 1; i++) {

                    const xc = (this.trail[i].x + this.trail[i + 1].x) * 0.5;

                    const yc = (this.trail[i].y + this.trail[i + 1].y) * 0.5;

                    ctx.quadraticCurveTo(this.trail[i].x, this.trail[i].y, xc, yc);

                }

                ctx.strokeStyle = this.color;

                ctx.lineWidth = Math.max(1.4, this.size * 1.5);

                ctx.lineCap = 'round';

                ctx.lineJoin = 'round';

                ctx.globalAlpha = this.opacity * 0.35;

                ctx.shadowBlur = 10;

                ctx.shadowColor = this.color;

                ctx.stroke();



                // 2. Inner intense white filament core of disappearing light

                ctx.beginPath();

                ctx.moveTo(this.trail[0].x, this.trail[0].y);

                for (let i = 1; i < this.trail.length - 1; i++) {

                    const xc = (this.trail[i].x + this.trail[i + 1].x) * 0.5;

                    const yc = (this.trail[i].y + this.trail[i + 1].y) * 0.5;

                    ctx.quadraticCurveTo(this.trail[i].x, this.trail[i].y, xc, yc);

                }

                ctx.strokeStyle = 'rgba(255, 255, 255, 0.90)';

                ctx.lineWidth = Math.max(0.7, this.size * 0.65);

                ctx.globalAlpha = this.opacity * 0.70;

                ctx.shadowBlur = 6;

                ctx.shadowColor = THEME.gold;

                ctx.stroke();



                // 3. Fading bioluminescent firefly embers along the trail

                for (let i = 2; i < this.trail.length; i += 2) {

                    const pt = this.trail[i];

                    const age = i / this.trail.length;

                    const sporeAlpha = this.opacity * Math.pow(1 - age, 1.6) * 0.42;

                    if (sporeAlpha > 0.02) {

                        ctx.beginPath();

                        ctx.arc(pt.x, pt.y, Math.max(0.6, this.size * (1 - age * 0.65)), 0, Math.PI * 2);

                        ctx.fillStyle = this.color;

                        ctx.globalAlpha = sporeAlpha;

                        ctx.shadowBlur = 5;

                        ctx.shadowColor = this.color;

                        ctx.fill();

                    }

                }

                ctx.restore();

            }"""

new_draw_tail = """        draw(ctx) {

            // Firefly Light Tail: Appearing ONLY when moving to a new position; thin and sleek

            if (this.tailAlpha > 0.03 && this.trail.length >= 2) {

                ctx.save();



                // 1. Outer luminous aura ribbon - ultra thin (0.65px to 1.5px)

                ctx.beginPath();

                ctx.moveTo(this.trail[0].x, this.trail[0].y);

                for (let i = 1; i < this.trail.length - 1; i++) {

                    const xc = (this.trail[i].x + this.trail[i + 1].x) * 0.5;

                    const yc = (this.trail[i].y + this.trail[i + 1].y) * 0.5;

                    ctx.quadraticCurveTo(this.trail[i].x, this.trail[i].y, xc, yc);

                }

                ctx.strokeStyle = this.color;

                ctx.lineWidth = Math.max(0.65, this.size * 0.30) * this.tailAlpha;

                ctx.lineCap = 'round';

                ctx.lineJoin = 'round';

                ctx.globalAlpha = this.opacity * 0.40 * this.tailAlpha;

                ctx.shadowBlur = 4 * this.tailAlpha;

                ctx.shadowColor = this.color;

                ctx.stroke();



                // 2. Inner intense white filament core - razor thin (0.32px to 0.7px)

                ctx.beginPath();

                ctx.moveTo(this.trail[0].x, this.trail[0].y);

                for (let i = 1; i < this.trail.length - 1; i++) {

                    const xc = (this.trail[i].x + this.trail[i + 1].x) * 0.5;

                    const yc = (this.trail[i].y + this.trail[i + 1].y) * 0.5;

                    ctx.quadraticCurveTo(this.trail[i].x, this.trail[i].y, xc, yc);

                }

                ctx.strokeStyle = 'rgba(255, 255, 255, 0.95)';

                ctx.lineWidth = Math.max(0.32, this.size * 0.14) * this.tailAlpha;

                ctx.globalAlpha = this.opacity * 0.75 * this.tailAlpha;

                ctx.shadowBlur = 2 * this.tailAlpha;

                ctx.shadowColor = THEME.gold;

                ctx.stroke();



                // 3. Delicate micro-ember spore at tail tip

                if (this.trail.length >= 4) {

                    const tip = this.trail[this.trail.length - 1];

                    const sporeAlpha = this.opacity * 0.25 * this.tailAlpha;

                    if (sporeAlpha > 0.02) {

                        ctx.beginPath();

                        ctx.arc(tip.x, tip.y, Math.max(0.4, this.size * 0.18), 0, Math.PI * 2);

                        ctx.fillStyle = this.color;

                        ctx.globalAlpha = sporeAlpha;

                        ctx.fill();

                    }

                }



                ctx.restore();

            }"""

assert old_draw_tail in c, "old_draw_tail block not found"
c = c.replace(old_draw_tail, new_draw_tail, 1)

with open('assets/js/drones.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Successfully applied thin tail updates to assets/js/drones.js!")
