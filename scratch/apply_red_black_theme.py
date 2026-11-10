import re

# 1. Update index.html
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_code_line1 = '<span class="drone-code-line"><span class="code-line-num">01</span><span class="code-kw">export const</span> <span class="code-var">competencies</span>: <span class="code-type">TechStack</span> = [</span>'
new_code_line1 = '<span class="drone-code-line"><span class="code-line-num">01</span><span class="code-kw">const</span> <span class="code-var">skills</span> = [</span>'

if old_code_line1 in html:
    html = html.replace(old_code_line1, new_code_line1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Updated index.html code block line 01!")
else:
    print("Notice: old_code_line1 not found, checking if already updated...")

# 2. Update assets/js/drones.js
with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update THEME and PALETTE
old_theme_palette = """    const THEME = {

        gold: '#F5C542',

        purple: '#8B3DFF',

        turquoise: '#19E3D1',

        cyan: '#19E3D1',

        black: '#07060B',

        white: '#FFFFFF'

    };

    const PALETTE = [THEME.gold, THEME.purple, THEME.turquoise];"""

new_theme_palette = """    const THEME = {

        gold: '#F5C542',

        purple: '#8B3DFF',

        turquoise: '#19E3D1',

        cyan: '#19E3D1',

        bloodRed: '#8B0000',

        bloodCrimson: '#C4122D',

        bloodNeon: '#FF1E42',

        black: '#07060B',

        white: '#FFFFFF'

    };

    const PALETTE = [THEME.gold, THEME.purple, THEME.turquoise, '#FF1E42', '#C4122D'];"""

if old_theme_palette in js:
    js = js.replace(old_theme_palette, new_theme_palette)
    print("Updated THEME and PALETTE in drones.js!")
else:
    # Try normalized match
    print("Trying regex replace for THEME and PALETTE in drones.js...")
    theme_pattern = re.compile(r'const THEME = \{[^}]+\};\s*const PALETTE = \[[^\]]+\];', re.DOTALL)
    replacement = """const THEME = {
        gold: '#F5C542',
        purple: '#8B3DFF',
        turquoise: '#19E3D1',
        cyan: '#19E3D1',
        bloodRed: '#8B0000',
        bloodCrimson: '#C4122D',
        bloodNeon: '#FF1E42',
        black: '#07060B',
        white: '#FFFFFF'
    };
    const PALETTE = [THEME.gold, THEME.purple, THEME.turquoise, '#FF1E42', '#C4122D'];"""
    js, n = theme_pattern.subn(replacement, js, count=1)
    print(f"Regex replaced THEME & PALETTE: {n} match")

# Update plasmaPalette in emitPlasmaSparks
js = js.replace(
    "const plasmaPalette = [THEME.cyan, THEME.gold, THEME.white];",
    "const plasmaPalette = [THEME.cyan, THEME.gold, '#FF1E42', '#8B0000', THEME.white];"
)

# Update spark colors in emitSparks
js = js.replace(
    "color: [THEME.gold, THEME.turquoise, THEME.white][Math.floor(Math.random() * 3)]",
    "color: [THEME.gold, THEME.turquoise, '#FF1E42', THEME.white][Math.floor(Math.random() * 4)]"
)

with open('assets/js/drones.js', 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated drones.js with dark blood red & neon crimson plasma sparks and nanobot palette!")
