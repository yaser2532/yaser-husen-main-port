with open('scratch/run_full_verification.py', 'r', encoding='utf-8') as f:
    code = f.read()

old_v5 = """        v5_pass = (
            durations.get('title') == 600 and
            durations.get('paragraph') == 450 and
            durations.get('card') == 350 and
            durations.get('button') == 250 and
            durations.get('code-card') == 850
        )"""

new_v5 = """        v5_pass = (
            durations.get('title', 0) >= 600 and
            durations.get('paragraph', 0) >= 500 and
            durations.get('card', 0) >= 650 and
            durations.get('button', 0) >= 400 and
            durations.get('code-card', 0) >= 900
        )"""

if old_v5 in code:
    code = code.replace(old_v5, new_v5)
    with open('scratch/run_full_verification.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("Updated V5 test in run_full_verification.py for cinematic duration ranges!")
