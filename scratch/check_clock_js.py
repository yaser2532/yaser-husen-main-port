import subprocess

res = subprocess.run(['git', 'grep', 'clock-utc'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
print("clock-utc references:")
print(res.stdout)

res2 = subprocess.run(['git', 'grep', 'hero-live-clock'], capture_output=True, text=True, encoding='utf-8', errors='ignore')
print("hero-live-clock references:")
print(res2.stdout)
