with open("assets/css/style.css", "r", encoding="utf-8") as f:
    css = f.read()

target = """.project-filters .filter-btn,
.project-filters .filter-btn.active,
.project-filters .filter-btn:hover,
.project-filters .filter-btn.active:hover,
.project-filters .filter-btn:focus,
.filter-btn,
.filter-btn.active,
.filter-btn:hover,
.filter-btn.active:hover {
    background: rgba(22, 14, 38, 0.85) !important;
    border: 1px solid rgba(168, 85, 247, 0.45) !important;
    color: #f1f5f9 !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
    text-shadow: none !important;
    animation: none !important;
    filter: none !important;
    cursor: pointer !important;
    transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease !important;
}"""

replacement = """/* Filter Buttons: Stationary 100% Uniform Cyberpunk Glass */
.project-filters .filter-btn,
.project-filters .filter-btn.active,
.project-filters .filter-btn:focus,
.filter-btn,
.filter-btn.active {
    background: rgba(22, 14, 38, 0.85) !important;
    border: 1px solid rgba(168, 85, 247, 0.45) !important;
    color: #f1f5f9 !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
    text-shadow: none !important;
    filter: none !important;
    cursor: pointer !important;
    transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s ease, background 0.2s ease !important;
}"""

assert target in css, "target not found in style.css"
css = css.replace(target, replacement, 1)

with open("assets/css/style.css", "w", encoding="utf-8") as f:
    f.write(css)

print("Successfully updated stationary filter-btn rule to allow glitch hover!")
