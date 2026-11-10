with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Add cyan alias to THEME
old_theme = """    const THEME = {

        gold: '#F5C542',

        purple: '#8B3DFF',

        turquoise: '#19E3D1',

        black: '#07060B',

        white: '#FFFFFF'

    };"""

new_theme = """    const THEME = {

        gold: '#F5C542',

        purple: '#8B3DFF',

        turquoise: '#19E3D1',

        cyan: '#19E3D1',

        black: '#07060B',

        white: '#FFFFFF'

    };"""

assert old_theme in c, "old_theme not found"
c = c.replace(old_theme, new_theme, 1)

# 2. Fix updateAndDrawPulseRings timestamp clamping and positive radius
old_draw_rings = """    function updateAndDrawPulseRings(ctx, now) {

        for (let i = pulseRings.length - 1; i >= 0; i--) {

            const ring = pulseRings[i];

            const elapsed = now - ring.startTime;

            const progress = elapsed / ring.duration;



            if (progress >= 1.0) {

                pulseRings.splice(i, 1);

                continue;

            }



            const easeP = easeOutCubic(progress);

            const r = easeP * ring.maxRadius;

            const fade = (1.0 - progress);

            const alpha = fade * fade * 0.85;



            ctx.save();

            // Outer ultra-fine expanding gravitational wave ring

            ctx.beginPath();

            ctx.arc(ring.x, ring.y, r, 0, Math.PI * 2);

            ctx.strokeStyle = ring.color;

            ctx.lineWidth = Math.max(0.4, 1.1 * fade);

            ctx.globalAlpha = alpha;

            ctx.shadowColor = ring.color;

            ctx.shadowBlur = 4 * fade;

            ctx.stroke();



            // Inner faint echo ping

            if (progress < 0.65) {

                ctx.beginPath();

                ctx.arc(ring.x, ring.y, r * 0.45, 0, Math.PI * 2);

                ctx.strokeStyle = THEME.white;

                ctx.lineWidth = 0.5 * fade;

                ctx.globalAlpha = alpha * 0.45;

                ctx.stroke();

            }

            ctx.restore();

        }

    }"""

new_draw_rings = """    function updateAndDrawPulseRings(ctx, now) {

        for (let i = pulseRings.length - 1; i >= 0; i--) {

            const ring = pulseRings[i];

            const elapsed = Math.max(0, now - ring.startTime);

            const progress = Math.min(1.0, elapsed / ring.duration);



            if (progress >= 1.0) {

                pulseRings.splice(i, 1);

                continue;

            }



            const easeP = easeOutCubic(progress);

            const r = Math.max(0.2, easeP * ring.maxRadius);

            const fade = (1.0 - progress);

            const alpha = fade * fade * 0.85;



            ctx.save();

            // Outer ultra-fine expanding gravitational wave ring

            ctx.beginPath();

            ctx.arc(ring.x, ring.y, r, 0, Math.PI * 2);

            ctx.strokeStyle = ring.color || THEME.turquoise;

            ctx.lineWidth = Math.max(0.4, 1.1 * fade);

            ctx.globalAlpha = alpha;

            ctx.shadowColor = ring.color || THEME.turquoise;

            ctx.shadowBlur = 4 * fade;

            ctx.stroke();



            // Inner faint echo ping

            if (progress < 0.65) {

                ctx.beginPath();

                ctx.arc(ring.x, ring.y, Math.max(0.1, r * 0.45), 0, Math.PI * 2);

                ctx.strokeStyle = THEME.white;

                ctx.lineWidth = 0.5 * fade;

                ctx.globalAlpha = alpha * 0.45;

                ctx.stroke();

            }

            ctx.restore();

        }

    }"""

assert old_draw_rings in c, "old_draw_rings not found"
c = c.replace(old_draw_rings, new_draw_rings, 1)

with open('assets/js/drones.js', 'w', encoding='utf-8') as f:
    f.write(c)

print("Fixed THEME.cyan and pulse ring radius clamping!")
