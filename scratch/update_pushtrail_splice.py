with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    c = f.read()

old_pt = """        pushTrail() {

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

new_pt = """        pushTrail() {

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

assert old_pt in c, "old_pt block not found"
c = c.replace(old_pt, new_pt, 1)

with open('assets/js/drones.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated pushTrail in drones.js!")
