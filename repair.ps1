$filepath = "c:\Users\Prathamesh\OneDrive\Desktop\ignisia codee\index.html"
$lines = [System.IO.File]::ReadAllLines($filepath)

# Find cut start: line after drawIdealGhost closing brace
$cutStart = -1
for ($i = 1570; $i -lt 1590; $i++) {
    if ($lines[$i] -match "updateGhostHand3D\(idealLm, isCorrect\)") {
        $j = $i + 1
        while ($j -lt $lines.Count -and ($lines[$j].Trim() -eq "" -or $lines[$j].Trim() -eq "}" -or $lines[$j] -match '\\n')) {
            $j++
        }
        $cutStart = $j
        break
    }
}

# Find cut end: completeSession function 
$cutEnd = -1
for ($i = $cutStart; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match "function completeSession\(\)") {
        $cutEnd = $i
        break
    }
}

Write-Host "Cutting from line $($cutStart+1) to $($cutEnd)"
Write-Host "First cut: $($lines[$cutStart])"
Write-Host "Resume at: $($lines[$cutEnd])"

$insert = @(
    ""
    "        function completeStep(index) {"
    "            completedSteps.push(index);"
    "            if (index > 0 && !completedSteps.includes(index - 1)) skippedSteps.push(index - 1);"
    ""
    "            // Mark step mini progress as done"
    '            const miniDone = document.getElementById(`step-mini-' + '${index}' + '`);'
    '            if (miniDone) { miniDone.style.width = "100%"; miniDone.style.background = "var(--success)"; }'
    ""
    "            currentStepIndex++;"
    "            dwellStartTime = null;"
    "            dwellAccumulated = 0;"
    ""
    "            updateStepUI();"
    ""
    "            if (currentStepIndex >= currentProcedure.steps.length) {"
    "                completeSession();"
    "            }"
    "        }"
    ""
)

$before = $lines[0..($cutStart-1)]
$after = $lines[$cutEnd..($lines.Count-1)]
$newLines = $before + $insert + $after

[System.IO.File]::WriteAllLines($filepath, $newLines)
Write-Host "Done! Was $($lines.Count) lines, now $($newLines.Count) lines"
