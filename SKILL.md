---
name: Code Explanation
description: This skill should be used when the user asks to "创建中文逐行注释副本", "在副本上给每行代码加中文注释", "逐行解释 C 代码并保留原文件", "翻译代码里的德语或英语注释", "给变量名添加中文释义", or asks to annotate many source files by making a copied folder first.
---

# Code Explanation

## Purpose

Create a safe annotated copy of source code files, then add concise Chinese explanations above each original non-empty line. Preserve the original folder and original code text. Use the annotated copy as a reading aid for control algorithms, embedded C, generated model code, and similar technical codebases.

Use this skill for batch code explanation tasks where the requested deliverable is a copied folder containing annotated source files, especially when the user wants Chinese comments, translation of German or English comments, variable-name interpretation, and behind-the-logic explanations.

## Core Contract

Keep the source directory unchanged. Create a sibling copy folder first, then edit only the copied files.

Preserve every original source line exactly in the copy. Insert explanation lines above original lines; never rewrite, normalize, re-indent, translate, or delete the original line itself.

Write the annotated copy as UTF-8 when Chinese text is added. Mention UTF-8 if the user's terminal or editor displays mojibake.

Default to annotating non-empty original lines. Preserve blank lines as blank lines unless the user explicitly asks for blank-line annotations.

## Standard Folder Workflow

1. Locate the source folder or file path from the user request.
2. Inventory target files before editing. Prefer `rg --files` or platform-native file listing. For C code, default to `.c` and include `.h` only when requested or clearly part of the same task.
3. Choose a destination folder name beside the source folder. Use `<source-folder-name>_中文逐行注释副本` unless the user names a different destination.
4. Check whether the destination already exists. Avoid overwriting an existing annotated folder without explicit user approval. If a non-conflicting destination is needed, append a short timestamp or ask for confirmation.
5. Copy the entire source folder to the destination folder before making edits.
6. Read representative files and nearby context to infer domain vocabulary, variable naming, units, control states, and comment language.
7. Annotate only files in the destination folder.
8. Validate that original non-empty lines are still present and have the required annotation lines immediately above them.
9. Summarize the output folder path, file count, and validation result.

## Annotation Format

For normal source code lines, insert exactly two lines immediately above the original line:

```c
// 注释：说明该行的直接含义，并在变量出现时给出中文释义或合理推测。
// 逻辑：说明该行在算法、控制流程、数据流或安全保护中的作用。
original_line;
```

For original German, English, or mixed-language comment lines, insert:

```c
// 原注释翻译：自然翻译原注释，不改变原注释文本。
// 逻辑：说明这条注释对应的代码块为什么存在、控制目的是什么。
// Original comment line
```

For separator comments, block-comment delimiters, braces, `else`, and continuation lines, still add two concise explanation lines. Explain structural meaning rather than inventing behavior.

Use the comment syntax appropriate to the language:

| Language/file type | Annotation prefix |
| --- | --- |
| C, C++, Java, JavaScript, TypeScript | `//` |
| Python, shell, YAML, TOML | `#` |
| MATLAB | `%` |

Prefer the existing language's ordinary line-comment syntax. For C-like generated code, use `//` even when the original line is inside a block comment, because the goal is an explanatory reading copy.

## Explanation Rules

Explain literal meaning first, then inferred purpose. Keep each line short enough to remain readable in a code editor.

Infer variable names from local context and naming conventions. Mark uncertain meanings with `推测为`, `可能表示`, or `结合上下文看`. Do not present guesses as facts.

Translate German and English comments with priority. Keep the original comment line unchanged below the translation. Restore obvious German technical terms in the explanation when helpful, for example `fuehrt` as `führt`, `Raeder` as `Räder`, `Nachlaufzeit` as `后运行时间`.

For control code, identify state-machine meaning, threshold checks, timer behavior, signal memory, wheel or axle naming, fault gating, saturation, and safety fallback. Mention units only when clear from names or comments.

Treat self-assignments such as `x = x;` as generated-code output landing or signal-retention patterns unless context proves otherwise.

Avoid changing program behavior. Do not add TODOs, refactors, formatting changes, or corrected source code unless the user separately requests a code fix.

## Validation

After annotation, run a structural validation. Check that:

- Source files still exist unchanged in the original folder.
- The destination contains the same target file set.
- Every non-empty original line appears in the destination after exactly two annotation lines.
- The first annotation line starts with `注释：` or `原注释翻译：` after the language comment marker.
- The second annotation line starts with `逻辑：` after the language comment marker.
- Original line text is byte-for-byte or string-exact after UTF-8 decoding.

Use `scripts/validate_annotated_copy.py` for C-like `//` annotated folders when available. For other languages, adapt the marker arguments or perform an equivalent check.

## Additional Resources

- `references/commenting-style.md` - Detailed annotation style, translation guidance, and examples.
- `scripts/validate_annotated_copy.py` - Utility to verify that an annotated copy preserves original lines and includes the required annotation prefixes.
