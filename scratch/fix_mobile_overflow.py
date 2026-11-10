with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    scss = f.read()

# 1. Update .about-grid in base
old_grid = """.about-grid {

    display: grid;

    grid-template-columns: 1fr 1fr;

    gap: 4rem;

    align-items: flex-start;

}"""

new_grid = """.about-grid {

    display: grid;

    grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);

    gap: 4rem;

    align-items: flex-start;

}"""

if old_grid in scss:
    scss = scss.replace(old_grid, new_grid, 1)
else:
    # try with different whitespace
    scss = scss.replace('grid-template-columns: 1fr 1fr;', 'grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);', 1)

# 2. Update .about-grid in media query
scss = scss.replace(
    '    .about-grid {\n\n        grid-template-columns: 1fr;\n\n        gap: 3rem;\n\n    }',
    '    .about-grid {\n\n        grid-template-columns: minmax(0, 1fr);\n\n        gap: 2.5rem;\n\n    }'
)

# 3. Update .about-visual and .code-block-visual sizing
old_terminal_css = """.about-visual {
    position: relative;
    width: 100%;
    opacity: 1 !important;
    transform: none !important;
}

.code-block-visual {
    background: rgba(10, 6, 20, 0.88);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 12px;
    border: 1px solid rgba(25, 227, 209, 0.25);
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.65), 0 0 24px rgba(25, 227, 209, 0.08);
    position: relative;
    overflow: hidden;
    padding: 0;
    font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
    font-size: 0.88rem;
    line-height: 1.6;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}"""

new_terminal_css = """.about-visual {
    position: relative;
    width: 100%;
    max-width: 100%;
    min-width: 0;
    box-sizing: border-box;
    opacity: 1 !important;
    transform: none !important;
}

.code-block-visual {
    width: 100%;
    max-width: 100%;
    min-width: 0;
    box-sizing: border-box;
    background: rgba(10, 6, 20, 0.88);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 12px;
    border: 1px solid rgba(25, 227, 209, 0.25);
    box-shadow: 0 12px 36px rgba(0, 0, 0, 0.65), 0 0 24px rgba(25, 227, 209, 0.08);
    position: relative;
    overflow: hidden;
    padding: 0;
    font-family: 'JetBrains Mono', 'Fira Code', 'Consolas', monospace;
    font-size: 0.88rem;
    line-height: 1.6;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}"""

if old_terminal_css in scss:
    scss = scss.replace(old_terminal_css, new_terminal_css, 1)

# 4. Add mobile terminal tweaks at end of style.css
mobile_terminal_rule = """
@media (max-width: 480px) {
    .terminal-body {
        font-size: 0.75rem !important;
        padding: 0.75rem 0.65rem !important;
    }
    .terminal-header {
        padding: 0.5rem 0.75rem !important;
    }
    .code-line-num {
        width: 1.5rem !important;
        font-size: 0.70rem !important;
    }
    .terminal-badge {
        display: none !important;
    }
}
"""

if '.terminal-badge {' in scss and '@media (max-width: 480px) {\n    .terminal-body' not in scss:
    scss += mobile_terminal_rule

with open('assets/css/style.css', 'w', encoding='utf-8') as f:
    f.write(scss)
print("Updated style.css with responsive constraints for about-grid & terminal!")
