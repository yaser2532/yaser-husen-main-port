with open("assets/css/style.css", "r", encoding="utf-8") as f:
    css = f.read()

# Remove the block that forced filter-btn:hover back to dark glass rgba(22, 14, 38, 0.85)
old_filter_hover = """.project-filters .filter-btn:hover,
.project-filters .filter-btn.active:hover,
.filter-btn:hover,
.filter-btn.active:hover {
    /* Exact same color format as stationary, clean physical elevation lift */
    background: rgba(22, 14, 38, 0.85) !important;
    border: 1px solid rgba(168, 85, 247, 0.45) !important;
    color: #f1f5f9 !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.65), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
    transform: translateY(-2px) !important;
}

.project-filters .filter-btn:hover *,
.project-filters .filter-btn.active:hover *,
.filter-btn:hover *,
.filter-btn.active:hover * {
    color: #f1f5f9 !important;
    text-shadow: none !important;
}"""

if old_filter_hover in css:
    css = css.replace(old_filter_hover, "")
    print("Successfully removed dark filter-btn:hover override!")
else:
    print("old_filter_hover not found, checking alternatives...")

# Ensure .btn-submit, button[type="submit"], #submit-btn have animation enabled
submit_anim_override = """
#submit-btn:hover,
.btn-submit:hover,
button[type="submit"]:hover {
    background: linear-gradient(115deg, #19E3D1 0%, #F5C542 26%, #FF2A85 52%, #8B3DFF 76%, #19E3D1 100%) !important;
    background-size: 260% 100% !important;
    animation: btnGlitchGradSweep 1.8s linear infinite, btnMicroJitter 0.24s cubic-bezier(0.25, 0.46, 0.45, 0.94) 1 !important;
    border-color: #19E3D1 !important;
    color: #07060B !important;
}
"""

with open("assets/css/style.css", "w", encoding="utf-8") as f:
    f.write(css + "\n" + submit_anim_override)

print("Updated style.css successfully!")
