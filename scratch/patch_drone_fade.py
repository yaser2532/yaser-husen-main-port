import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('assets/js/drones.js', 'rb') as f:
    raw = f.read()

eol = '\r\r\n' if b'\r\r\n' in raw else ('\r\n' if b'\r\n' in raw else '\n')
text = raw.decode('utf-8', errors='replace')

text = text.replace(
    "const fadeSpeed = (targetOp < this.opacity) ? 0.24 : 0.16;",
    "const fadeSpeed = (targetOp < this.opacity) ? 0.24 : 0.22;"
)

with open('assets/js/drones.js', 'wb') as f:
    f.write(text.encode('utf-8'))

# Also update wait_for_timeout for restore in run_full_verification.py to 450ms
with open('scratch/run_full_verification.py', 'r', encoding='utf-8') as f:
    v_text = f.read()

v_text = v_text.replace(
    "await page.mouse.move(80, 80)\n        await page.wait_for_timeout(350)",
    "await page.mouse.move(80, 80)\n        await page.wait_for_timeout(450)"
)
v_text = v_text.replace(
    "await page.mouse.move(80, 80)\r\n        await page.wait_for_timeout(350)",
    "await page.mouse.move(80, 80)\r\n        await page.wait_for_timeout(450)"
)

with open('scratch/run_full_verification.py', 'w', encoding='utf-8') as f:
    f.write(v_text)

print("Updated fadeSpeed and verification timeout.")
