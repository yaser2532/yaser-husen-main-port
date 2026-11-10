# 1. Update assets/css/drones.css
with open('assets/css/drones.css', 'r', encoding='utf-8') as f:
    dcss = f.read()

# Remove the premature preview rule for code-block-visual
preview_rule = """html.drones-active .code-block-visual[data-drone-state="pending"],
html.drones-active .code-block-visual[data-drone-state="flight"] {
    opacity: 0.80 !important;
    transform: translate3d(0, 14px, 0) !important;
    filter: blur(0.5px) !important;
    pointer-events: auto !important;
}"""

if preview_rule in dcss:
    dcss = dcss.replace(preview_rule, "")
    print("Removed premature code block preview rule from drones.css!")

# Enhance data-drone-state rules for cinematic pulling
old_states = """html.drones-active [data-drone-state="pending"] {
    opacity: 0 !important;
    transform: translate3d(0, 32px, 0) !important;
    filter: blur(2px) !important;
    pointer-events: none !important;
    will-change: transform, opacity;
}

html.drones-active [data-drone-state="flight"] {
    opacity: 0 !important;
    transform: translate3d(0, 32px, 0) !important;
    filter: blur(2px) !important;
    pointer-events: none !important;
    will-change: transform, opacity;
}"""

new_states = """html.drones-active [data-drone-state="pending"] {
    opacity: 0 !important;
    transform: translate3d(0, 55px, 0) scale(0.94) !important;
    filter: blur(5px) !important;
    pointer-events: none !important;
    will-change: transform, opacity, filter;
}

html.drones-active [data-drone-state="flight"] {
    opacity: 0.08 !important;
    transform: translate3d(0, 55px, 0) scale(0.94) !important;
    filter: blur(5px) !important;
    pointer-events: none !important;
    will-change: transform, opacity, filter;
}"""

if old_states in dcss:
    dcss = dcss.replace(old_states, new_states)
    print("Updated pending and flight states with deep space offset in drones.css!")

with open('assets/css/drones.css', 'w', encoding='utf-8') as f:
    f.write(dcss)

# 2. Update assets/css/style.css for balanced Code Block Colors
with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    scss = f.read()

# Replace the syntax token colors to complement the website theme (turquoise strings, gold variables, purple types, crimson keywords & active badge)
old_syntax = """.code-line-num {
    display: inline-block;
    width: 2rem;
    color: #661824;
    user-select: none;
    font-size: 0.78rem;
    font-weight: 600;
}

.code-kw {
    color: #F43F5E;
    font-weight: 600;
    text-shadow: 0 0 8px rgba(244, 63, 94, 0.35);
}

.code-var {
    color: #F8FAFC;
    font-weight: 600;
}

.code-type {
    color: #C4122D;
    font-weight: 600;
}

.code-op {
    color: #F43F5E;
}

.code-str {
    color: #F43F5E;
    text-shadow: 0 0 6px rgba(244, 63, 94, 0.35);
    font-weight: 500;
}

.code-punct {
    color: #CBD5E1;
}

.keyword { color: #f43f5e; }

.var { color: #f8fafc; }"""

new_syntax = """.code-line-num {
    display: inline-block;
    width: 2rem;
    color: rgba(148, 163, 184, 0.40);
    user-select: none;
    font-size: 0.78rem;
    font-weight: 600;
}

/* Keywords: Dark Blood Red / Signature Crimson Accent */
.code-kw, .keyword {
    color: #F43F5E;
    font-weight: 600;
    text-shadow: 0 0 8px rgba(244, 63, 94, 0.40);
}

/* Variable Name: Cyberpunk Gold */
.code-var, .var {
    color: #F5C542;
    font-weight: 600;
}

/* Types: Electric Purple */
.code-type {
    color: #8B3DFF;
    font-weight: 600;
}

/* Operators: Warm Gold */
.code-op {
    color: #F5C542;
}

/* Strings / Competencies: Iconic Neon Turquoise */
.code-str {
    color: #19E3D1;
    text-shadow: 0 0 8px rgba(25, 227, 209, 0.35);
    font-weight: 500;
}

/* Punctuation: Clean Silver */
.code-punct {
    color: #E2E8F0;
}"""

if old_syntax in scss:
    scss = scss.replace(old_syntax, new_syntax)
    print("Updated code syntax tokens with balanced theme colors in style.css!")
else:
    print("Warning: old_syntax not matched verbatim in style.css, inspecting...")

# Update terminal window dots in style.css: Close=Red, Minimize=Gold, Expand=Green
old_dots = """.dot-close {
    background: #FF2A55;
    box-shadow: 0 0 8px rgba(255, 42, 85, 0.75);
}

.dot-minimize {
    background: #8B0000;
    box-shadow: 0 0 4px rgba(139, 0, 0, 0.5);
}

.dot-expand {
    background: #4A000A;
    border: 1px solid rgba(180, 20, 40, 0.4);
}"""

new_dots = """.dot-close {
    background: #FF2A55;
    box-shadow: 0 0 8px rgba(255, 42, 85, 0.75);
}

.dot-minimize {
    background: #FFBD2E;
    box-shadow: 0 0 6px rgba(255, 189, 46, 0.50);
}

.dot-expand {
    background: #27C93F;
    box-shadow: 0 0 6px rgba(39, 201, 63, 0.50);
}"""

if old_dots in scss:
    scss = scss.replace(old_dots, new_dots)
    print("Updated terminal dots to Red, Gold, Green in style.css!")

with open('assets/css/style.css', 'w', encoding='utf-8') as f:
    f.write(scss)

print("Saved drones.css and style.css successfully!")
