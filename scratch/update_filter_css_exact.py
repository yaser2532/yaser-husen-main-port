with open("assets/css/style.css", "r", encoding="utf-8") as f:
    css = f.read()

target = """.project-filters .filter-btn,
.project-filters .filter-btn.active,
.project-filters .filter-btn:hover,
.project-filters .filter-btn.active:hover,
.project-filters .filter-btn:focus,
.filter-btn,
.filter-btn.active {
    background: rgba(22, 14, 38, 0.82) !important;
    border: 1px solid rgba(168, 85, 247, 0.42) !important;
    color: #f1f5f9 !important;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
    text-shadow: none !important;
    animation: none !important;
    filter: none !important;
    cursor: pointer !important;
    transition: background 0.22s ease, border-color 0.22s ease, box-shadow 0.22s ease, transform 0.22s ease !important;
}

.project-filters .filter-btn:hover,
.project-filters .filter-btn.active:hover,
.filter-btn:hover,
.filter-btn.active:hover {
    background: rgba(34, 20, 56, 0.92) !important;
    border: 1px solid rgba(192, 132, 252, 0.65) !important;
    color: #ffffff !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.14) !important;
    transform: translateY(-2px) !important;
}

.project-filters .filter-btn:hover *,
.project-filters .filter-btn.active:hover *,
.filter-btn:hover *,
.filter-btn.active:hover * {
    color: #ffffff !important;
    text-shadow: none !important;
}"""

replacement = """/* =========================================================================
   PROJECT FILTERS — 100% UNIFORM COLOR FORMAT (STATIONARY & HOVER)
   All 4 buttons ('All Projects', 'AI & Data Science Projects', 'Web Apps', 'Creative Labs')
   maintain the EXACT same background, border, text color, and format in stationary position
   and when a cursor hovers over them.
   ========================================================================= */
.project-filters .filter-btn,
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
}

.project-filters .filter-btn:hover,
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

if target in css:
    css = css.replace(target, replacement)
    with open("assets/css/style.css", "w", encoding="utf-8") as f:
        f.write(css)
    print("Successfully updated filter-btn CSS with 100% identical color format across stationary & hover!")
else:
    print("Target not found in CSS!")
