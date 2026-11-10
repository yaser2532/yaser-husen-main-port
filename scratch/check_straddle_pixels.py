import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

img = Image.open("C:/Users/yhuse/.gemini/antigravity/brain/fc793577-a505-4be3-babf-536dd24e6ccd/test_straddling_seam.png")
w, h = img.size
print(f"Image size: {w}x{h}")

for y in range(435, 465):
    colors = [img.getpixel((x, y))[:3] for x in [200, 400, 720, 1000, 1200]]
    avg_color = [sum(c[i] for c in colors)//len(colors) for i in range(3)]
    print(f"y={y}: avg={avg_color}, mid(720)={colors[2]}, x(200)={colors[0]}")
