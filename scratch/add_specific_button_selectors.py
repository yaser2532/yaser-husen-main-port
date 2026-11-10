def add_selectors():
    with open('assets/css/style.css', 'r', encoding='utf-8') as f:
        css = f.read()

    target = """.message-btn:hover,"""
    replacement = """.message-btn:hover,
#secret-message-btn:hover,
a#secret-message-btn:hover,
#submit-btn:hover,
button[type="submit"]:hover,
.btn-submit:hover,
#footer-resume-btn:hover,
.dock-btn-resume:hover,"""

    assert target in css, "target not found"
    css = css.replace(target, replacement)

    target_inner = """.message-btn:hover *,"""
    replacement_inner = """.message-btn:hover *,
#secret-message-btn:hover *,
a#secret-message-btn:hover *,
#submit-btn:hover *,
button[type="submit"]:hover *,
.btn-submit:hover *,
#footer-resume-btn:hover *,
.dock-btn-resume:hover *,"""

    assert target_inner in css, "target_inner not found"
    css = css.replace(target_inner, replacement_inner)

    with open('assets/css/style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Successfully added specific button hover selectors to style.css")

if __name__ == '__main__':
    add_selectors()
