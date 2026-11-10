import shutil
import os

artifact_dir = r"C:\Users\yhuse\.gemini\antigravity\brain\fc793577-a505-4be3-babf-536dd24e6ccd"

files = [
    ("scratch/verify_clean_hero_to_content.png", "clean_hero_to_content.png"),
    ("scratch/verify_sleeker_drone_dots.png", "sleeker_drone_dots.png")
]

for src, dst_name in files:
    if os.path.exists(src):
        dst = os.path.join(artifact_dir, dst_name)
        shutil.copy2(src, dst)
        print(f"Copied {src} -> {dst}")
