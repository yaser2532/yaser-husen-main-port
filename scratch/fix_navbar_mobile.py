with open('assets/css/style.css', 'r', encoding='utf-8') as f:
    scss = f.read()

scss += """
@media (max-width: 480px) {
    .navbar {
        padding-left: 0.85rem !important;
        padding-right: 0.85rem !important;
        max-width: 100vw !important;
        box-sizing: border-box !important;
    }
    .burger {
        margin-right: 0 !important;
        position: relative !important;
    }
}
"""

with open('assets/css/style.css', 'w', encoding='utf-8') as f:
    f.write(scss)
print("Added navbar mobile padding rule!")
