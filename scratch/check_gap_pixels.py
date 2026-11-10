from PIL import Image
import os

images = [f for f in os.listdir('scratch') if f.startswith('gap_check_') and f.endswith('.png')]
for img_name in sorted(images):
    path = os.path.join('scratch', img_name)
    im = Image.open(path)
    w, h = im.size
    # Sample right 15 pixels across height
    right_pixels = []
    for x in range(w-15, w):
        for y in range(0, h, 20):
            right_pixels.append(im.getpixel((x, y)))
    
    # Check if rightmost 10px are pure black (0,0,0) or nearly black while the rest of the image has content
    all_black_right = all(p[0] < 12 and p[1] < 12 and p[2] < 12 for p in right_pixels[:50])
    print(f"[{img_name}] {w}x{h}: right edge sample color: {right_pixels[-1]}")
