import os

filepath = r'c:\Users\Prathamesh\OneDrive\Desktop\ignisia codee\index.html'

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Keep lines 1-1580 (index 0-1579) which end with the new GLB drawIdealGhost closing brace
# Skip lines 1581-1767 (index 1580-1766) which are corrupted old code
# Keep lines 1768+ (index 1767+) which contain the rest of the application

# But first, check if line 1767 (0-indexed) already has 'function completeStep' 
# If the real completeStep was at a different line, we need to find it
good_start = None
for i in range(1580, len(lines)):
    if 'function completeSession()' in lines[i]:
        good_start = i
        break

# Find where completeStep body starts (if it exists)
cs_start = None
for i in range(1580, len(lines)):
    stripped = lines[i].strip()
    if stripped.startswith('completedSteps') or stripped.startswith('function completeSession'):
        # The old completeStep body or completeSession
        break

# Build the replacement section
insert = """
        function completeStep(index) {
            completedSteps.push(index);
            if (index > 0 && !completedSteps.includes(index - 1)) skippedSteps.push(index - 1);

            // Mark step mini progress as done
            const miniDone = document.getElementById(`step-mini-${index}`);
            if (miniDone) { miniDone.style.width = '100%'; miniDone.style.background = 'var(--success)'; }

            currentStepIndex++;
            dwellStartTime = null;
            dwellAccumulated = 0;

            updateStepUI();

            if (currentStepIndex >= currentProcedure.steps.length) {
                completeSession();
            }
        }

"""

# Find the exact cut points
# Good code ends after line containing "updateGhostHand3D(idealLm, isCorrect);" and its closing brace
cut_start = None
for i in range(1570, min(1590, len(lines))):
    if 'updateGhostHand3D(idealLm, isCorrect);' in lines[i]:
        # Next line(s) should be the closing brace
        j = i + 1
        while j < len(lines) and lines[j].strip() in ['', '}', '}\\n', '}\\\\n']:
            j += 1
        cut_start = j
        break

if cut_start is None:
    print("Could not find cut_start!")
    exit(1)

# Find where the good code resumes (completeSession function)
cut_end = None
for i in range(cut_start, len(lines)):
    if 'function completeSession()' in lines[i]:
        cut_end = i
        break

if cut_end is None:
    print("Could not find completeSession!")
    exit(1)

print(f"Cutting lines {cut_start+1} to {cut_end} (0-indexed: {cut_start} to {cut_end-1})")
print(f"First cut line: {lines[cut_start].rstrip()}")
print(f"Last cut line: {lines[cut_end-1].rstrip()}")
print(f"Resume at: {lines[cut_end].rstrip()}")

# Build new file
new_lines = lines[:cut_start]
new_lines.append(insert)
new_lines.extend(lines[cut_end:])

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Done! File now has {len(new_lines)} lines (was {len(lines)})")
