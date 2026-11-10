import shutil
import os

artifact_dir = r"C:\Users\yhuse\.gemini\antigravity\brain\fc793577-a505-4be3-babf-536dd24e6ccd"

files_to_copy = [
    ("scratch/card_folded_in_3d.png", "card_folded_in_3d.png"),
    ("scratch/card_folded_out_3d.png", "card_folded_out_3d.png"),
    ("scratch/hero_button_hovered_bloodred.png", "hero_button_hovered_bloodred.png"),
    ("scratch/viewport_verified_1920.png", "viewport_verified_1920.png"),
    ("scratch/viewport_verified_375.png", "viewport_verified_375.png"),
]

for src, dst_name in files_to_copy:
    if os.path.exists(src):
        dst = os.path.join(artifact_dir, dst_name)
        shutil.copy2(src, dst)
        print(f"Copied {src} -> {dst}")
