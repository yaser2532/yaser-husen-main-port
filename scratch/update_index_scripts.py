with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

target = '<script defer src="assets/js/hover-system.js"></script>'
replacement = """    <script defer src="assets/vendor/react/react.min.js"></script>

    <script defer src="assets/vendor/react/react-dom.min.js"></script>

    <script defer src="assets/js/react-3d-cards.js"></script>

    <script defer src="assets/js/hover-system.js"></script>"""

if target in html:
    html = html.replace(target, replacement, 1)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Successfully updated index.html with React and React-3D-Cards scripts!")
else:
    print("Target script tag not found in index.html!")
