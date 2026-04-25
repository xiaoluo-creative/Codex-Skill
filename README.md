# CodeOCR

CodeOCR is a Codex skill for transcribing code from screenshots into `.c` files with line-number-aware verification.

It is designed for tasks such as:

- OCR code from screenshots.
- Preserve indentation, braces, blank lines, and unusual generated-code statements.
- Use visible left-side line numbers to avoid mixed or missing lines.
- Repair obvious German comment mojibake using conservative ASCII German spelling.
- Save the recovered code into the current workspace as a `.c` file.

See `安装教程.md` for installation steps.
