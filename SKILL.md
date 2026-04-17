---
name: "word-formula-layout-repair"
description: "This skill should be used when the user asks to \"检查 Word 公式乱码\", \"修复 Word 公式乱码\", \"检查 docx 公式排版\", \"修复公式符号乱码\", \"检查 Word 排版和公式\", or mentions broken equation symbols, OMATH corruption, placeholder residue, formula layout drift, or `乱码` inside a `.docx` file."
---

# Word Formula Layout Repair

## Purpose

Handle `.docx` files whose risk is concentrated in Word equations, formula symbols, or post-conversion layout drift. Combine Word MCP, Word COM, and OOXML checks to distinguish normal paragraph corruption from broken `OMaths`.

## Trigger Cues

Trigger on requests to:
- inspect whether a Word document still has formula garble or layout problems
- fix equation symbols that became meaningless characters
- inspect `OMaths` instead of plain text only
- clean placeholder residue such as `__EQ`
- export a Word file for layout review after formula repair

Skip this skill for ordinary document drafting when equations are not the main failure mode.

## Workflow

### 1. Triage plain text first

Start with Word MCP:
- use `get_document_outline` to locate affected chapters
- use `find_text_in_document` for `__EQ`, `~=`, `乱码`, `�`, `□`
- use `search_and_replace` or `replace_paragraph_block_below_header` for normal paragraph corruption

Escalate to equation-object inspection when the visible problem is inside formulas rather than prose.

### 2. Inspect Word equation objects

Run the bundled inspection script:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\inspect_word_omaths.ps1 -DocPath "C:\path\file.docx"
```

Use it to report:
- page count from Word COM
- paragraph count
- equation count
- each equation's page number and linear text

Treat this as the primary check when the user says formulas contain meaningless symbols.

### 3. Check OOXML for residue and corruption

Inspect `word/document.xml` when formula corruption is suspected. Look for:
- placeholder residue such as `__EQ`
- Unicode replacement characters
- empty-box style artifacts
- known broken symbol remnants after conversion

Use this pass even when visual rendering is unavailable.

### 4. Repair plain text vs equation objects correctly

For plain text problems:
- rewrite only the damaged paragraph blocks with Word MCP
- avoid rebuilding formulas when the damage is only in prose

For equation-object problems:
- repair by equation index, not by nearby paragraph text
- rebuild from highest index to lowest index to avoid `OMaths` index drift
- write to a fresh output file instead of overwriting an open source file
- if the source path contains non-ASCII characters, save through an ASCII temp copy before copying back to the requested output path

Run the bundled repair script with a JSON spec:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\repair_word_formula_symbols.ps1 `
  -DocPath "C:\path\broken.docx" `
  -RepairJsonPath "C:\path\repairs.json" `
  -OutputPath "C:\path\fixed.docx"
```

Repair spec example:

```json
[
  { "index": 26, "linear": "CfVxFltPT1 = 1 - e^(-T_s/τ)" },
  { "index": 25, "linear": "CfVxFltPT1 ≈ T_s/(T_s + τ)" }
]
```

### 5. Watch the common symbol failures

Treat these as common repair targets:
- conditional arrows turning into meaningless CJK characters
- `≈` turning into junk
- Greek letters such as `τ` turning into junk

Rebuild the entire equation object instead of editing one corrupted glyph in place.

### 6. Validate after every repair

After repair:
- rerun `inspect_word_omaths.ps1`
- confirm the previously bad equations no longer contain damaged symbols
- rerun Word MCP searches for `__EQ`, `~=`, `�`, `□`
- export to PDF with Word COM when a true layout review is needed

Trust Word COM page counts over lightweight metadata when pagination matters.

## Output

Return:
- whether the corruption is in plain text, formula objects, or both
- what was repaired
- the final output file path
- whether a true visual page review was completed or only structural checks were possible