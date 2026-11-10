import sys
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

for name in ['inspect_seam_scroll_0.png', 'inspect_seam_scroll_250.png', 'inspect_seam_scroll_500.png']:
    path = f"C:/Users/yhuse/.gemini/antigravity/brain/fc793577-a505-4be3-babf-536dd24e6ccd/{name}"
    img = Image.open(path)
    w, h = img.size
    print(f"\n=== {name} ({w}x{h}) ===")
    # Sample brightness along the vertical centerline around y = 650 to 900
    mid_x = w // 2
    samples = []
    for y in range(h - 220, h, 20):
        r, g, b = img.getpixel((mid_x, y))[:3]
        brightness = (r + g + b) / 3
        samples.append((y, f"rgb({r},{g},{b})", round(brightness, 1)))
    print("Vertical brightness profile near bottom of viewport:")
    for y, rgb, br in samples:
        print(f"  y={y}: {rgb} (brightness={br})")
