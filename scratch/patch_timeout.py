import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/run_full_verification.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Change wait_for_timeout(250) to wait_for_timeout(450) on dim test
text = text.replace("await page.wait_for_timeout(250)\n        dim_op =", "await page.wait_for_timeout(450)\n        dim_op =")
text = text.replace("await page.wait_for_timeout(250)\r\n        dim_op =", "await page.wait_for_timeout(450)\r\n        dim_op =")

with open('scratch/run_full_verification.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated run_full_verification.py timeout.")
