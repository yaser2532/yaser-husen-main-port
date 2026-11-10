with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    scss = f.read()

cleanup_rule = """
/* Mobile Viewport Polish & 0 Overflow Guarantee */
@media (max-width: 480px) {
    html, body {
        overflow-x: hidden !important;
        max-width: 100vw !important;
    }
    .container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    .desk-content-wrapper,
    .secret-text,
    .light-floor-reflection,
    .light-beam-visual,
    .desk-container {
        max-width: 100% !important;
        box-sizing: border-box !important;
        overflow: hidden !important;
    }
    .burger {
        right: 1.25rem !important;
    }
    .terminal-body {
        max-width: 100% !important;
        box-sizing: border-box !important;
        overflow-x: auto !important;
    }
    .terminal-pre {
        max-width: 100% !important;
        box-sizing: border-box !important;
        overflow-x: auto !important;
        white-space: pre-wrap !important;
        word-break: break-word !important;
    }
}
"""

scss += cleanup_rule

with open('assets/css/style.css', 'w', encoding='utf-8') as f:
    f.write(scss)
print("Added mobile polish rules to style.css!")
