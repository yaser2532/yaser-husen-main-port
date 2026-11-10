# Update assets/css/drones.css
with open('assets/css/drones.css', 'r', encoding='utf-8') as f:
    dcss = f.read()

pos_pending = dcss.find('html.drones-active [data-drone-state="pulling"] {')
assert pos_pending != -1, "pulling rule not found in drones.css"

override_rule = """html.drones-active .code-block-visual[data-drone-state="pending"],
html.drones-active .code-block-visual[data-drone-state="flight"] {
    opacity: 0.80 !important;
    transform: translate3d(0, 14px, 0) !important;
    filter: blur(0.5px) !important;
    pointer-events: auto !important;
}

"""

dcss = dcss[:pos_pending] + override_rule + dcss[pos_pending:]
with open('assets/css/drones.css', 'w', encoding='utf-8') as f:
    f.write(dcss)
print("Updated drones.css with code-block-visual graceful preview rule!")

# Update assets/js/drones.js getPrio
with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    djs = f.read()

pos_prio = djs.find('const getPrio = (el) => {')
pos_prio_end = djs.find('const sorted = rawElements.sort', pos_prio)
assert pos_prio != -1 and pos_prio_end != -1, "getPrio not found in drones.js"

new_prio_fn = """const getPrio = (el) => {
                const tag = el.tagName.toLowerCase();
                if (['h1', 'h2', 'h3'].includes(tag) || el.classList.contains('section-title') || el.classList.contains('section-tag')) return 1;
                if (el.classList.contains('code-block-visual')) return 2; // Pull code card early
                if (['p'].includes(tag) || el.classList.contains('section-desc')) return 3;
                if (el.matches(cardSelector) || el.classList.contains('stats-row')) return 4;
                return 5;
            };

            """

djs = djs[:pos_prio] + new_prio_fn + djs[pos_prio_end:]
with open('assets/js/drones.js', 'w', encoding='utf-8') as f:
    f.write(djs)
print("Updated getPrio in drones.js to prioritize code-block-visual!")
