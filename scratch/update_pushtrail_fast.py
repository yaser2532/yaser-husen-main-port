with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    c = f.read()

# Update updateFollow tailFadeRate
old_uf = """            const targetTailAlpha = isRelocating ? Math.min(1.0, Math.max(0.2, (droneSpeed - 1.8) / 3.0)) : 0.0;

            const tailFadeRate = isRelocating ? Math.min(1.0, dt * 14) : Math.min(1.0, dt * 10);

            this.tailAlpha += (targetTailAlpha - this.tailAlpha) * tailFadeRate;"""

new_uf = """            const targetTailAlpha = isRelocating ? Math.min(1.0, Math.max(0.25, (droneSpeed - 1.8) / 2.8)) : 0.0;

            const tailFadeRate = isRelocating ? Math.min(1.0, dt * 16) : Math.min(1.0, dt * 24);

            this.tailAlpha += (targetTailAlpha - this.tailAlpha) * tailFadeRate;

            if (!isRelocating && this.trail.length === 0) {

                this.tailAlpha = 0.0;

            }"""

assert old_uf in c, "old_uf block not found"
c = c.replace(old_uf, new_uf, 1)

# Update pushTrail
old_pt = """        pushTrail() {

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

new_pt = """        pushTrail() {

            if (this.isRelocating && this.tailAlpha > 0.08) {

                this.trail.unshift({ x: this.x, y: this.y, alpha: this.tailAlpha });

                if (this.trail.length > this.maxTrail) {

                    this.trail.pop();

                }

            } else if (this.trail.length > 0) {

                // Instant clean dissolution when resting at fixed position

                this.trail.pop();

            }

        }"""

assert old_pt in c, "old_pt block not found"
c = c.replace(old_pt, new_pt, 1)

with open('assets/js/drones.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated pushTrail and tailFadeRate!")
