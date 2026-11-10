with open('assets/js/drones.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update IRREGULAR_SIZES to sleeker, smaller sizes
old_sizes = 'const IRREGULAR_SIZES = [1.5, 3.8, 2.2, 4.6, 1.4, 3.2, 2.7, 4.4, 1.8, 3.5, 2.3, 4.8, 1.6, 3.9];'
new_sizes = 'const IRREGULAR_SIZES = [1.2, 2.8, 1.8, 3.4, 1.1, 2.4, 2.0, 3.2, 1.4, 2.6, 1.7, 3.5, 1.3, 2.9];'
assert old_sizes in content, 'old_sizes not found'
content = content.replace(old_sizes, new_sizes, 1)

# 2. Update initSprites radial glow sizes to match the sleeker dots
old_sprites = '''    function initSprites() {
        spriteCache.goldLead = createRadialSprite('rgba(255, 215, 0, 0.45)', '#FFFFFF', 2.8, 14);
        spriteCache.gold = createRadialSprite('rgba(245, 197, 66, 0.40)', '#FFFFFF', 2.2, 11);
        spriteCache.purple = createRadialSprite('rgba(139, 61, 255, 0.45)', '#FFFFFF', 2.2, 11);
        spriteCache.turquoise = createRadialSprite('rgba(25, 227, 209, 0.45)', '#FFFFFF', 2.2, 11);
        spriteCache.crimson = createRadialSprite('rgba(255, 30, 66, 0.45)', '#FFFFFF', 2.2, 11);
        spriteCache.sparkWhite = createRadialSprite('rgba(255, 255, 255, 0.85)', '#FFFFFF', 1.6, 6);
        spriteCache.pulseTurquoise = createRadialSprite('rgba(25, 227, 209, 0.35)', null, 0, 20);
        spriteCache.pulseGold = createRadialSprite('rgba(245, 197, 66, 0.35)', null, 0, 20);
    }'''

new_sprites = '''    function initSprites() {
        spriteCache.goldLead = createRadialSprite('rgba(255, 215, 0, 0.45)', '#FFFFFF', 2.2, 11);
        spriteCache.gold = createRadialSprite('rgba(245, 197, 66, 0.40)', '#FFFFFF', 1.8, 9);
        spriteCache.purple = createRadialSprite('rgba(139, 61, 255, 0.45)', '#FFFFFF', 1.8, 9);
        spriteCache.turquoise = createRadialSprite('rgba(25, 227, 209, 0.45)', '#FFFFFF', 1.8, 9);
        spriteCache.crimson = createRadialSprite('rgba(255, 30, 66, 0.45)', '#FFFFFF', 1.8, 9);
        spriteCache.sparkWhite = createRadialSprite('rgba(255, 255, 255, 0.85)', '#FFFFFF', 1.3, 5);
        spriteCache.pulseTurquoise = createRadialSprite('rgba(25, 227, 209, 0.35)', null, 0, 16);
        spriteCache.pulseGold = createRadialSprite('rgba(245, 197, 66, 0.35)', null, 0, 16);
    }'''

assert old_sprites in content, 'old_sprites not found'
content = content.replace(old_sprites, new_sprites, 1)

# 3. Update sizeScale base in Drone.draw
old_scale = 'const sizeScale = (this.size || 2.2) / 2.2;'
new_scale = 'const sizeScale = (this.size || 1.8) / 1.8;'
assert old_scale in content, 'old_scale not found'
content = content.replace(old_scale, new_scale, 1)

with open('assets/js/drones.js', 'w', encoding='utf-8') as f:
    f.write(content)

print('Updated assets/js/drones.js successfully!')
