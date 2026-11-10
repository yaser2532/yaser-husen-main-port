with open('scratch/run_full_verification.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('\r\n', '\n')

old_v5 = """        v5_pass = (
            durations.get('title') >= 1100 and
            durations.get('paragraph') >= 900 and
            durations.get('card') >= 600 and
            durations.get('button') >= 450
        )"""

new_v5 = """        v5_pass = (
            durations.get('title') <= 650 and
            durations.get('paragraph') <= 500 and
            durations.get('card') <= 400 and
            durations.get('button') <= 300
        )"""

if old_v5 in text:
    text = text.replace(old_v5, new_v5)
    print("Updated V5 duration check.")
else:
    print("Warning: old_v5 not found!")

with open('scratch/run_full_verification.py', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(text)

print("scratch/run_full_verification.py updated.")
