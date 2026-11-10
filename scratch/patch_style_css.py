with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

# 1. Line ~2252: remove transform from .expertise-card:hover
found1 = False
for i in range(2240, 2260):
    if 'transform: translateY(-4px) scale(1.02);' in lines[i]:
        lines[i] = '    /* 3D tilt handled by React 3D physics */\n'
        found1 = True
        print(f"1. Removed transform from line {i+1}")
        break
assert found1, "Could not find target 1"

# 2. Line ~2665-2675: clean .project-card transform & transition
found2 = False
for i in range(2660, 2680):
    if 'transform: perspective(1000px)' in lines[i]:
        # find the transition line right after
        lines[i] = ''
        found2 = True
        print(f"2a. Cleared transform at line {i+1}")
    if found2 and 'transition: transform 0.15s ease-out' in lines[i]:
        lines[i] = '    transition: border-color 0.25s ease, box-shadow 0.25s ease;\n'
        print(f"2b. Updated transition at line {i+1}")
        break
assert found2, "Could not find target 2"

# 3. Line ~8823: multi-card transition
found3 = False
for i in range(8815, 8835):
    if 'transition: transform 0.25s cubic-bezier' in lines[i]:
        lines[i] = '    transition: box-shadow 0.25s ease, border-color 0.25s ease !important;\n'
        found3 = True
        print(f"3. Updated multi-card transition at line {i+1}")
        break
assert found3, "Could not find target 3"

# 4. Line ~10036: remove !important from box-shadow
found4 = False
for i in range(10025, 10045):
    if 'box-shadow: 0 20px 42px rgba(0, 0, 0, 0.75), 0 6px 14px rgba(0, 0, 0, 0.50) !important;' in lines[i]:
        lines[i] = '    box-shadow: 0 20px 42px rgba(0, 0, 0, 0.75), 0 6px 14px rgba(0, 0, 0, 0.50);\n'
        found4 = True
        print(f"4. Removed !important from hover box-shadow at line {i+1}")
        break
assert found4, "Could not find target 4"

# 5. Lines ~10180-10212: Replace react-3d-card and inner elements
start_idx = None
end_idx = None
for i in range(10170, 10220):
    if '.react-3d-card,' in lines[i]:
        start_idx = i
        break
for i in range(start_idx, min(len(lines), start_idx + 40)):
    if 'transform: none !important;' in lines[i]:
        # end is after the closing brace
        end_idx = i + 2
        break

print(f"5. Replacing lines {start_idx+1} to {end_idx} with multi-layer 3D CSS...")
new_block = [
    "/* Card 3D Base & Perspective Containers */\n",
    ".projects-grid,\n",
    ".expertise-cards-grid,\n",
    ".certifications-grid,\n",
    ".about-grid,\n",
    ".hero-stats-grid {\n",
    "    perspective: 1200px !important;\n",
    "    transform-style: preserve-3d !important;\n",
    "}\n",
    "\n",
    ".react-3d-card,\n",
    ".project-card,\n",
    ".cert-card,\n",
    ".expertise-card,\n",
    ".onboard-card,\n",
    ".stat-card,\n",
    ".glass-card,\n",
    ".bday-card,\n",
    ".code-block-visual,\n",
    ".hero-about-tile,\n",
    ".contact-card,\n",
    ".profile-card-wrapper {\n",
    "    transform-style: preserve-3d !important;\n",
    "    will-change: transform !important;\n",
    "}\n",
    "\n",
    ".card-3d-active {\n",
    "    transition: none !important;\n",
    "}\n",
    "\n",
    "/* 3D Specular Glare Reflection Sheen */\n",
    ".react-3d-card::before {\n",
    "    content: '';\n",
    "    position: absolute;\n",
    "    inset: 0;\n",
    "    border-radius: inherit;\n",
    "    background: radial-gradient(circle 380px at var(--card-glare-x, 50%) var(--card-glare-y, 50%), rgba(25, 227, 209, 0.14), rgba(255, 255, 255, 0.05) 30%, transparent 70%);\n",
    "    opacity: 0;\n",
    "    pointer-events: none;\n",
    "    z-index: 10;\n",
    "    transition: opacity 0.3s ease;\n",
    "}\n",
    "\n",
    ".react-3d-card.card-3d-active::before {\n",
    "    opacity: 1;\n",
    "}\n",
    "\n",
    "/* Authentic Multi-Layer 3D Parallax Depth — Floating without text deformation */\n",
    ".react-3d-card .project-img-container,\n",
    ".react-3d-card .expertise-icon,\n",
    ".react-3d-card .cert-img-wrapper,\n",
    ".react-3d-card .terminal-header {\n",
    "    transform: translateZ(34px) !important;\n",
    "    transform-style: preserve-3d !important;\n",
    "    transition: transform 0.2s ease;\n",
    "}\n",
    "\n",
    ".react-3d-card .project-details h3,\n",
    ".react-3d-card .project-title,\n",
    ".react-3d-card .expertise-card h4,\n",
    ".react-3d-card .cert-card h4,\n",
    ".react-3d-card .stat-card h4,\n",
    ".react-3d-card .hero-about-tile p {\n",
    "    transform: translateZ(26px) !important;\n",
    "    transform-style: preserve-3d !important;\n",
    "    transition: transform 0.2s ease;\n",
    "}\n",
    "\n",
    ".react-3d-card .project-details p,\n",
    ".react-3d-card .expertise-card p,\n",
    ".react-3d-card .cert-card p,\n",
    ".react-3d-card .stat-card .stat-label {\n",
    "    transform: translateZ(18px) !important;\n",
    "    transform-style: preserve-3d !important;\n",
    "    transition: transform 0.2s ease;\n",
    "}\n",
    "\n",
    ".react-3d-card .badge,\n",
    ".react-3d-card .holo-sticker,\n",
    ".react-3d-card .torn-paper-sticker,\n",
    ".react-3d-card .project-link,\n",
    ".react-3d-card .view-cert-btn,\n",
    ".react-3d-card .project-footer {\n",
    "    transform: translateZ(40px) !important;\n",
    "    transform-style: preserve-3d !important;\n",
    "    transition: transform 0.2s ease;\n",
    "}\n",
    "\n"
]

lines[start_idx:end_idx] = new_block

# 6. Line ~10349: remove perspective: 900px !important;
found6 = False
for i in range(len(lines) - 60, len(lines)):
    if 'perspective: 900px !important;' in lines[i]:
        lines[i] = '    /* perspective on parent grid container */\n'
        found6 = True
        print(f"6. Removed perspective 900px from line {i+1}")
        break

with open('assets/css/style.css', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("SUCCESS: assets/css/style.css fully patched.")
