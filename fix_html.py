import re
import sys

try:
    log_path = "/Users/amulyaratnamaske/.gemini/antigravity/brain/1aa21b9d-c00e-4c09-ba28-3fc1e229b2f6/.system_generated/logs/overview.txt"
    with open(log_path, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = content.split('[diff_block_start]')
    if len(blocks) < 2:
        print("No diff block found!")
        sys.exit(1)

    last_block = blocks[-1].split('[diff_block_end]')[0]
    lines = last_block.split('\n')

    html_lines = []
    for line in lines:
        if line.startswith('@@'):
            html_lines = [] 
        elif line.startswith('+'):
            raw_line = line[1:]
            if 'input[type="range"] {' in raw_line and '-webkit-appearance: none;' in raw_line:
                if 'appearance: none;' not in raw_line:
                    raw_line = raw_line.replace('-webkit-appearance: none;', '-webkit-appearance: none; appearance: none;')
            html_lines.append(raw_line)

    if html_lines:
        with open('/Users/amulyaratnamaske/Documents/New project/SkillPilot_AI/index.html', 'w', encoding='utf-8') as f:
            f.write('\n'.join(html_lines))
        print(f"Wrote {len(html_lines)} lines to index.html")
    else:
        print("No HTML lines extracted.")
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
