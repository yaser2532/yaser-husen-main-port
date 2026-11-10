# 1. Patch assets/js/script.js
with open('assets/js/script.js', 'r', encoding='utf-8') as f:
    s_content = f.read()

old_stars_block = '''  // B. Mid-range Constellation Points (850 stars, size 2.4)



  const midStars = createStarfield(850, 2.4, 480, 360, 400, 0.96);



  scene.add(midStars);







  // C. Foreground Twinkling Stellar Points (90 stars, size 1.6, wide panoramic ratio, soft starlight)



  const foregroundStars = createStarfield(90, 1.6, 900, 680, 500, 0.58);



  scene.add(foregroundStars);'''

new_stars_block = '''  // B. Mid-range Constellation Points (Reduced from 850 down to 260 stars, size 1.8 for clean, uncluttered upper sky)



  const midStars = createStarfield(260, 1.8, 480, 360, 400, 0.88);



  scene.add(midStars);







  // C. Foreground Twinkling Stellar Points (Reduced from 90 down to 30 stars, size 1.4, subtle soft starlight)



  const foregroundStars = createStarfield(30, 1.4, 900, 680, 500, 0.50);



  scene.add(foregroundStars);'''

assert old_stars_block in s_content, 'old_stars_block not found in script.js'
s_content = s_content.replace(old_stars_block, new_stars_block, 1)

# Update diagnostic star count
old_diag = "getInfo: () => ({ tier: 'high', stars: 3800, active: true })"
new_diag = "getInfo: () => ({ tier: 'high', stars: 2890, active: true })"
s_content = s_content.replace(old_diag, new_diag, 1)

with open('assets/js/script.js', 'w', encoding='utf-8') as f:
    f.write(s_content)
print('Updated stars in assets/js/script.js!')

# 2. Patch assets/js/gl-engine.js
with open('assets/js/gl-engine.js', 'r', encoding='utf-8') as f:
    gl_content = f.read()

old_fg = 'const FG_STARS = 850;'
new_fg = 'const FG_STARS = 260; // Reduced from 850 down to 260 for clean, uncluttered upper sky'
assert old_fg in gl_content, 'old_fg not found in gl-engine.js'
gl_content = gl_content.replace(old_fg, new_fg, 1)

with open('assets/js/gl-engine.js', 'w', encoding='utf-8') as f:
    f.write(gl_content)
print('Updated stars in assets/js/gl-engine.js!')
