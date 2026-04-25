---
name: code-ocr
description: This skill should be used when the user asks to "OCR code from screenshots", "screenshot code to .c file", "transcribe code with line numbers", "preserve indentation", "avoid missing lines", "repair German comment mojibake", "shibie tuzhong daima", or requests saving code shown in screenshots as a .c file with exact line-count verification.
---

# CodeOCR

## Purpose

Transcribe source code from screenshots into editable `.c` files with line-number-aware accuracy. Preserve visible code, indentation, braces, blank lines, and statement order. Repair only obvious mojibake or encoding damage inside German comments, using conservative ASCII German replacements such as `fuer`, `ueber`, `zurueck`, `moeglich`, `Raeder`, `Groessen`, `Verzoegerung`, and `Stuetzung`.

Use this skill for screenshot-based code recovery tasks where the user emphasizes left-side line numbers, total line count, no line mixing, no missing lines, indentation fidelity, and saving the result into the current folder or a named destination file.

## Workflow

### 1. Establish The Target

Identify the requested output filename exactly, including spaces, capitalization, and extension. If no folder is specified, save the file in the current workspace folder. Prefer `.c` or `.C` exactly as requested by the user.

Read the screenshots in visible order. Use the left margin line numbers as the primary source of truth for sequence, overlap, and total length. Treat repeated boundary lines between screenshots as overlap anchors, not duplicated content.

### 2. Segment By Line Numbers

Divide the screenshots into contiguous ranges using the visible left-side line numbers. Record the first and last visible line in each screenshot before transcribing. When two images overlap, keep one copy of the repeated line range and continue from the next unseen line.

If a screenshot begins with a repeated line from the previous image, compare the repeated text and indentation. Prefer the clearer image for that repeated line, then continue with the later lines.

When the user gives an expected total such as `614` lines, make the final file contain exactly that many lines unless the screenshots clearly show a different final line number. If the total differs, report the mismatch and explain which visible line numbers support it.

### 3. Transcribe Code Conservatively

Preserve code tokens exactly as visible. Do not normalize identifiers, function names, operators, punctuation, or unusual generated-code constructs unless the screenshot is clearly unreadable and the correction is required to match nearby repeated patterns.

Preserve:

- `.Import()` versus `.Inport()` exactly as visible.
- Self-assignments such as `vVeh_Neg=vVeh_Neg;`.
- Double semicolons, unusual spacing, and one-line `if` bodies.
- Comment delimiters, brace placement, and blank lines.
- Indentation depth shown by the editor guides and brace nesting.

Avoid reformatting. Keep lines unwrapped unless the screenshot clearly shows a logical continuation line. For long conditions split across screenshot lines, preserve the visible line breaks and alignment.

### 4. Repair German Comment Mojibake

Repair only comment text, not executable code. Replace common mojibake artifacts by inferred German words when the meaning is clear from context.

Common ASCII repairs:

- Artifacts resembling `fuer` -> `fuer`
- Artifacts resembling `ueber` -> `ueber`
- Artifacts resembling `zurueck` -> `zurueck`
- Artifacts resembling `moeglich` -> `moeglich`
- Artifacts resembling `Raeder` -> `Raeder`
- Artifacts resembling `Groessen` -> `Groessen`
- Artifacts resembling `Verzoegerung` -> `Verzoegerung`
- Artifacts resembling `Stuetzung` -> `Stuetzung`
- Artifacts resembling `Massnahme` -> `Massnahme`
- Artifacts resembling `laeuft` -> `laeuft`
- Artifacts resembling `koennen` -> `koennen`

Use ASCII transliteration for consistency unless the surrounding file already uses Unicode German characters. When uncertain, leave the comment conservative rather than inventing a different technical meaning.

### 5. Save With Apply Patch

Create or update the requested `.c` file with `apply_patch`. Do not use shell redirection, `cat`, or Python file-writing for manual transcription. Keep the output file in the requested folder.

If the filename contains spaces, create it exactly with that spelling.

### 6. Verify Mechanically

After saving, run a line-count check:

```powershell
(Get-Content -Path '<file>').Count
```

Compare the count with the expected final line number. If the expected count is known, the count must match.

Print numbered excerpts around important boundaries:

```powershell
$lines = Get-Content -Path '<file>'
foreach($start in 1, 61, 121, 182, 240, 297, 352, 409, 464, 522, 569){
    $end=[Math]::Min($start+8,$lines.Count)
    for($i=$start; $i -le $end; $i++){ '{0,4}: {1}' -f $i, $lines[$i-1] }
}
```

Adapt boundary starts to the screenshot ranges. Inspect overlaps, screenshot transitions, and the final lines.

Optionally check brace balance as a warning signal:

```powershell
$lines = Get-Content -Path '<file>'
$balance=0
for($i=1; $i -le $lines.Count; $i++){
    $line=$lines[$i-1]
    $balance += ([regex]::Matches($line,'\{')).Count - ([regex]::Matches($line,'\}')).Count
}
"FINAL_BALANCE=$balance"
```

Treat nonzero brace balance as a review prompt, not automatic failure, because screenshots may show a generated-code fragment inside an outer function body.

### 7. Final Response

Report the saved file path and the verified line count. Mention that German comment mojibake was repaired conservatively. If verification found a possible issue, state the exact line number or boundary and what was done.
