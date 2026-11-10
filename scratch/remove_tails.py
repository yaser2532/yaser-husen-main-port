with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Constructor: replace tail block with clean comment
old_const = """            // Firefly Light Tail: Sleek, thin, agile trace appearing only when relocating to new positions

            this.trail = [];

            this.maxTrail = 6; // Reduced from 16 to 6 for a short, crisp tail

            this.tailAlpha = 0.0; // Dynamic intensity multiplier

            this.isRelocating = false;"""

new_const = """            this.trail = [];"""

assert old_const in c, "old_const not found"
c = c.replace(old_const, new_const, 1)

# 2. updateFollow: remove relocation and tail logic
old_uf = """            // Tail appears ONLY when moving from a fixed position to a new position

            const droneSpeed = Math.hypot(this.vx, this.vy);

            const distToDesired = Math.hypot(desiredX - this.x, desiredY - this.y);

            const cursorIsMoving = (now - lastCursorMoveTime < 240);

            const isRelocating = cursorIsMoving && (distToDesired > 5.0 || droneSpeed > 2.2);

            this.isRelocating = isRelocating;



            const targetTailAlpha = isRelocating ? Math.min(1.0, Math.max(0.25, (droneSpeed - 1.8) / 2.8)) : 0.0;

            const tailFadeRate = isRelocating ? Math.min(1.0, dt * 16) : Math.min(1.0, dt * 24);

            this.tailAlpha += (targetTailAlpha - this.tailAlpha) * tailFadeRate;

            if (!isRelocating && this.trail.length === 0) {

                this.tailAlpha = 0.0;

            }



            this.pushTrail();"""

new_uf = """"""

assert old_uf in c, "old_uf not found"
c = c.replace(old_uf, new_uf, 1)

# 3. updateFlight: remove tail logic
old_ufl = """            // Active mission flight between fixed positions across screen

            this.isRelocating = true;

            const targetTailAlpha = 1.0;

            this.tailAlpha += (targetTailAlpha - this.tailAlpha) * Math.min(1.0, dt * 14);



            this.pushTrail();"""

new_ufl = """"""

assert old_ufl in c, "old_ufl not found"
c = c.replace(old_ufl, new_ufl, 1)

# 4. updatePull: remove tail logic
old_up = """            // Stationed at fixed anchor while pulling: no tail

            this.isRelocating = false;

            const targetTailAlpha = 0.0;

            this.tailAlpha += (targetTailAlpha - this.tailAlpha) * Math.min(1.0, dt * 16);



            this.pushTrail();"""

new_up = """"""

assert old_up in c, "old_up not found"
c = c.replace(old_up, new_up, 1)

# 5. pushTrail method: remove entirely
old_pt = """        pushTrail() {

            if (this.isRelocating && this.tailAlpha > 0.08) {

                this.trail.unshift({ x: this.x, y: this.y, alpha: this.tailAlpha });

                if (this.trail.length > this.maxTrail) {

                    this.trail.pop();

                }

            } else {

                // Clean rapid dissolution when settled at fixed position

                if (this.trail.length > 2) {

                    this.trail.splice(-2);

                } else {

                    this.trail = [];

                }

                if (this.tailAlpha <= 0.05) {

                    this.trail = [];

                    this.tailAlpha = 0.0;

                }

            }

        }"""

new_pt = """"""

assert old_pt in c, "old_pt not found"
c = c.replace(old_pt, new_pt, 1)

# 6. draw(ctx): remove tail rendering block
old_draw_tail = """            // Firefly Light Tail: Appearing ONLY when moving to a new position; thin and sleek

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

new_draw_tail = """"""

assert old_draw_tail in c, "old_draw_tail not found"
c = c.replace(old_draw_tail, new_draw_tail, 1)

with open('assets/js/drones.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Tails completely removed from drones.js!")
