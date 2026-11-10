with open('assets/css/drones.css', 'r', encoding='utf-8') as f:
    css = f.read()

pos1 = css.find('html.drones-active [data-drone-state="pending"]')
print(css[pos1:pos1+1000])
