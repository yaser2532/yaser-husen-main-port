import os, re

files = ['assets/js/hover-system.js', 'assets/js/script.js', 'assets/js/drones.js']

for fpath in files:
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        print(f"=== {fpath} ===")
        for i, line in enumerate(lines):
            if any(k in line.lower() for k in ['project-card', 'tilt', 'perspective', 'card-3d', 'rotatex', 'rotatey', 'translatez']):
                print(f"{i+1}: {line.strip()[:100]}")
