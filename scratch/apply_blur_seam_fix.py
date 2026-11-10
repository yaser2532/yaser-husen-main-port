import subprocess
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Update assets/css/drones.css
with open('assets/css/drones.css', 'rb') as f:
    raw_dcss = f.read()

eol_dcss = '\r\r\n' if b'\r\r\n' in raw_dcss else ('\r\n' if b'\r\n' in raw_dcss else '\n')
dcss = raw_dcss.decode('utf-8', errors='replace')

# Replace .hero-transition-seam
new_seam = """.hero-transition-seam {
    position: absolute;
    bottom: -12rem;
    left: 0;
    width: 100%;
    height: 24rem;
    pointer-events: none;
    z-index: 3;
    background: linear-gradient(to bottom, 
        transparent 0%, 
        rgba(5, 2, 10, 0.20) 20%, 
        rgba(139, 61, 255, 0.05) 38%,
        rgba(3, 1, 8, 0.70) 50%, 
        rgba(139, 61, 255, 0.05) 62%,
        rgba(5, 2, 10, 0.20) 80%, 
        transparent 100%);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    mask-image: linear-gradient(to bottom, transparent 0%, rgba(0, 0, 0, 0.6) 25%, black 50%, rgba(0, 0, 0, 0.6) 75%, transparent 100%);
    -webkit-mask-image: linear-gradient(to bottom, transparent 0%, rgba(0, 0, 0, 0.6) 25%, black 50%, rgba(0, 0, 0, 0.6) 75%, transparent 100%);
    display: block;
}""".replace('\n', eol_dcss)

seam_pattern = re.compile(r'\.hero-transition-seam\s*\{[^}]*\}', re.DOTALL)
dcss = seam_pattern.sub(new_seam, dcss)

# Replace #profile-expertise::before
new_prof_before = """#profile-expertise::before {
    content: '';
    position: absolute;
    top: -8rem;
    left: 0;
    width: 100%;
    height: 18rem;
    background: radial-gradient(ellipse 85% 100% at 50% 30%, rgba(139, 61, 255, 0.09) 0%, rgba(25, 227, 209, 0.03) 45%, transparent 80%);
    pointer-events: none;
    z-index: 0;
}""".replace('\n', eol_dcss)

prof_before_pattern = re.compile(r'#profile-expertise::before\s*\{[^}]*\}', re.DOTALL)
dcss = prof_before_pattern.sub(new_prof_before, dcss)

with open('assets/css/drones.css', 'wb') as f:
    f.write(dcss.encode('utf-8'))
print("assets/css/drones.css updated.")

# 2. Update assets/css/style.css to smooth header::before and .overlay masks
with open('assets/css/style.css', 'rb') as f:
    raw_style = f.read()

eol_style = '\r\r\n' if b'\r\r\n' in raw_style else ('\r\n' if b'\r\n' in raw_style else '\n')
style = raw_style.decode('utf-8', errors='replace')

# Smooth header::before mask
old_h_mask = "-webkit-mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, 0.85) 60%, rgba(0, 0, 0, 0) 100%);"
new_h_mask = "-webkit-mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, 0.88) 40%, rgba(0, 0, 0, 0.40) 75%, rgba(0, 0, 0, 0) 100%);"
style = style.replace(old_h_mask, new_h_mask)

old_h_mask2 = "mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, 0.85) 60%, rgba(0, 0, 0, 0) 100%);"
new_h_mask2 = "mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, 0.88) 40%, rgba(0, 0, 0, 0.40) 75%, rgba(0, 0, 0, 0) 100%);"
style = style.replace(old_h_mask2, new_h_mask2)

# Smooth .overlay mask
old_o_mask = "-webkit-mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, 0.85) 65%, rgba(0, 0, 0, 0) 100%);"
new_o_mask = "-webkit-mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, 0.88) 45%, rgba(0, 0, 0, 0.35) 80%, rgba(0, 0, 0, 0) 100%);"
style = style.replace(old_o_mask, new_o_mask)

old_o_mask2 = "mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, 0.85) 65%, rgba(0, 0, 0, 0) 100%);"
new_o_mask2 = "mask-image: linear-gradient(to bottom, rgba(0, 0, 0, 1) 0%, rgba(0, 0, 0, 0.88) 45%, rgba(0, 0, 0, 0.35) 80%, rgba(0, 0, 0, 0) 100%);"
style = style.replace(old_o_mask2, new_o_mask2)

with open('assets/css/style.css', 'wb') as f:
    f.write(style.encode('utf-8'))
print("assets/css/style.css updated.")
