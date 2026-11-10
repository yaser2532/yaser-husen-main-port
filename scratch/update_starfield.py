import re

script_path = 'assets/js/script.js'

with open(script_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Normalize
text = text.replace('\r\n', '\n').replace('\r', '\n')

# 1. Update star texture gradient
old_tex = """    // Crisp glowing core
    const grad = ctx.createRadialGradient(8, 8, 0, 8, 8, 8);
    grad.addColorStop(0, 'rgba(255, 255, 255, 1)');
    grad.addColorStop(0.35, 'rgba(255, 255, 255, 0.85)');
    grad.addColorStop(0.7, 'rgba(255, 255, 255, 0.25)');
    grad.addColorStop(1, 'rgba(255, 255, 255, 0)');"""

new_tex = """    // Crisp glowing core - refined soft starlight
    const grad = ctx.createRadialGradient(8, 8, 0, 8, 8, 8);
    grad.addColorStop(0, 'rgba(255, 255, 255, 0.95)');
    grad.addColorStop(0.25, 'rgba(255, 255, 255, 0.65)');
    grad.addColorStop(0.6, 'rgba(255, 255, 255, 0.15)');
    grad.addColorStop(1, 'rgba(255, 255, 255, 0)');"""

if old_tex in text:
    text = text.replace(old_tex, new_tex)
    print("Updated starTexture gradient.")
else:
    print("Warning: old_tex not found!")

# 2. Update foregroundStars definition
old_fg = """  // C. Foreground Twinkling Stellar Points (350 stars, size 3.8)
  const foregroundStars = createStarfield(350, 3.8, 320, 240, 260, 0.98);
  scene.add(foregroundStars);"""

new_fg = """  // C. Foreground Twinkling Stellar Points (90 stars, size 1.6, wide panoramic ratio, soft starlight)
  const foregroundStars = createStarfield(90, 1.6, 900, 680, 500, 0.58);
  scene.add(foregroundStars);"""

if old_fg in text:
    text = text.replace(old_fg, new_fg)
    print("Updated foregroundStars definition.")
else:
    print("Warning: old_fg not found!")

# 3. Update depth travel speed and twinkling
old_loop = """    // 3D Depth Travel: Foreground stars travel through Z space towards camera
    const fgPos = foregroundStars.geometry.attributes.position.array;
    for (let i = 2; i < fgPos.length; i += 3) {
      fgPos[i] += 0.28;
      if (fgPos[i] > 75) {
        fgPos[i] = -220;
      }
    }
    foregroundStars.geometry.attributes.position.needsUpdate = true;

    // Atmospheric stellar twinkling
    deepStars.material.opacity = 0.84 + Math.sin(time * 1.8) * 0.12;
    foregroundStars.material.opacity = 0.88 + Math.cos(time * 2.4) * 0.12;"""

new_loop = """    // 3D Depth Travel: Foreground stars gently drift through Z space
    const fgPos = foregroundStars.geometry.attributes.position.array;
    for (let i = 2; i < fgPos.length; i += 3) {
      fgPos[i] += 0.10;
      if (fgPos[i] > 80) {
        fgPos[i] = -350;
      }
    }
    foregroundStars.geometry.attributes.position.needsUpdate = true;

    // Atmospheric stellar twinkling with balanced brightness
    deepStars.material.opacity = 0.82 + Math.sin(time * 1.5) * 0.10;
    foregroundStars.material.opacity = 0.52 + Math.cos(time * 1.6) * 0.12;"""

if old_loop in text:
    text = text.replace(old_loop, new_loop)
    print("Updated foregroundStars depth travel and twinkling loop.")
else:
    print("Warning: old_loop not found!")

with open(script_path, 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text)

print("assets/js/script.js successfully updated!")
