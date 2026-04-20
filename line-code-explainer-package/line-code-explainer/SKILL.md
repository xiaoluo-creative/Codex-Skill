---
name: line-code-explainer
description: This skill should be used when the user asks to "逐行解释代码", "按行讲解代码", "根据截图识别并解释代码", "保留原代码高亮", "固定格式输出代码解释", or requests line-by-line explanation of pasted code or screenshots with preserved original code, visible line numbers, comment-style explanation blocks, and German comment restoration or translation. Produce explanations in a fixed `c` code-block layout with exact source preservation, variable interpretation, underlying logic, and German restoration or translation when present.
---

# Line Code Explainer

## Overview

Produce strict, reusable code explanations from screenshots or pasted
code.

Preserve the original code exactly as shown, follow the visible line
numbers, and place the explanation directly below each source line in
comment form.

## Workflow

1. Read the screenshot or pasted code carefully.
2. Follow the visible line numbers exactly.
3. Explain every visible line in order.
4. Preserve the original code text and indentation exactly.
5. Keep all explanation text inside a `c` code block unless the user
   explicitly requests a different block style.

## Required Output Rules

- Use a single `c` code block unless the user requests a different split.
- For each source line, output this sequence:
  `/* 第X行 */`
  original code line
  `// 含义：...`
  `// 变量猜测/解释：...`
  `// 背后逻辑：...`
- Add `// 德语翻译：...` when the line contains German, or when German
  translation is helpful.
- Keep the original code on its own line.
- Preserve the original indentation of the code line exactly as shown in
  the screenshot or pasted text.
- Do not rewrite, normalize, correct, or complete the original code.
- Do not skip lines, merge lines, or reorder lines.
- If a line is blank, state that it is a blank line.
- If multiple lines belong to one statement, still explain them one by
  one instead of combining them.

## Comment Wrapping Rules

- Keep the explanation readable within the visible block width.
- When a `//` comment line becomes long, wrap manually onto the next
  `//` line.
- Do not keep extending one long `//` line across the full width.
- Keep wrapped comment lines aligned with the surrounding explanation.
- Do not move wrapped explanation text onto the original code line.

Use this style:

```c
/* 第328行 */
    // v_Fzg folgt steigungsbegrenzt der Bezugsgeschwindigkeit
// 含义：v_Fzg 会以斜率受限的方式跟随参考速度。
// 变量猜测/解释：v_Fzg 是车辆速度；
// steigungsbegrenzt 是斜率受限；
// Bezugsgeschwindigkeit 是参考速度。
// 背后逻辑：参考速度算出来后，整车速度估计不会瞬间
// 跳过去，而是按限制斜率逐步贴近。
// 德语翻译：v_Fzg folgt steigungsbegrenzt der
// Bezugsgeschwindigkeit = v_Fzg 将以斜率受限的方式
// 跟随参考速度。
```

## German Handling

- Keep the original code line unchanged, even when the screenshot shows
  garbled German text.
- Restore garbled German in the explanation only.
- Translate German words, phrases, and full sentences naturally into
  Chinese.
- Prefer restoring likely original umlauts and common technical wording
  when the screenshot clearly shows encoding damage.
- If the exact restoration is uncertain, explain based on the most
  plausible restoration without changing the source line.

## Explanation Guidance

- Explain the literal meaning of the line first.
- Infer variable meaning from naming, control context, and nearby logic.
- Explain the engineering or control purpose behind the line.
- Prefer concise but specific explanations.
- Use the user's language unless the user requests another language.

## Screenshot Handling

- Read only the visible lines in the screenshot unless the user provides
  more context.
- If OCR uncertainty exists, keep the visible text as the original code
  line and explain based on the most likely reading.
- Do not invent hidden lines outside the screenshot.
- If the screenshot starts or ends in the middle of a block, explain the
  visible lines normally and infer context only when necessary.

## Default Format Template

```c
/* 第X行 */
    original code
// 含义：...
// 变量猜测/解释：...
// 背后逻辑：...
// 德语翻译：...
```

## Adaptation Rules

- Follow the user's explicit formatting changes when the user overrides
  the default layout.
- Reuse this exact layout when the user asks for the same house style
  again.
- Keep using a `c` code block when the user wants this visual style,
  even if the source language is not C-like.
