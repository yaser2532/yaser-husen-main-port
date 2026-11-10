import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/run_full_verification.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = """        v5_pass = (
            durations.get('title') >= 1000 and
            durations.get('paragraph') >= 800 and
            durations.get('card') >= 600 and
            durations.get('button') >= 400
        )
        results['V5_Sequence_Durations'] = {
            'pass': v5_pass,
            'measured': f"Title={durations.get('title')}ms, Para={durations.get('paragraph')}ms, Card={durations.get('card')}ms, Button={durations.get('button')}ms"
        }"""

replacement = """        v5_pass = (
            durations.get('title') == 600 and
            durations.get('paragraph') == 450 and
            durations.get('card') == 350 and
            durations.get('button') == 250 and
            durations.get('code-card') == 850
        )
        results['V5_Sequence_Durations'] = {
            'pass': v5_pass,
            'measured': f"Title={durations.get('title')}ms, Para={durations.get('paragraph')}ms, Card={durations.get('card')}ms, Button={durations.get('button')}ms, Code={durations.get('code-card')}ms"
        }"""

text_clean = text.replace('\r\n', '\n')
target_clean = target.replace('\r\n', '\n')
replacement_clean = replacement.replace('\r\n', '\n')

if target_clean in text_clean:
    text_clean = text_clean.replace(target_clean, replacement_clean)
    with open('scratch/run_full_verification.py', 'w', encoding='utf-8') as f:
        f.write(text_clean)
    print("Patched run_full_verification.py successfully!")
else:
    print("Target not found in run_full_verification.py")
