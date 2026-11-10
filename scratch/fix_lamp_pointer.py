def fix_lamp_pointer():
    with open('assets/css/style.css', 'r', encoding='utf-8') as f:
        css = f.read()

    target = """.lamp-scene {

    position: relative;

    width: 20rem;

    height: 25rem;

    display: flex;

    justify-content: center;

    transform: scale(1.35);

    transform-origin: top center;

    margin-top: -3rem; 

}"""

    replacement = """.lamp-scene {

    position: relative;

    width: 20rem;

    height: 25rem;

    display: flex;

    justify-content: center;

    transform: scale(1.35);

    transform-origin: top center;

    margin-top: -3rem; 

    pointer-events: none;

}

.lamp-structure {

    pointer-events: auto;

}"""

    assert target in css, "lamp-scene target not found"
    css = css.replace(target, replacement)

    with open('assets/css/style.css', 'w', encoding='utf-8') as f:
        f.write(css)
    print("Successfully added pointer-events: none to lamp-scene.")

if __name__ == '__main__':
    fix_lamp_pointer()
