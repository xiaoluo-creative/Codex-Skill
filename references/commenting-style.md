# CodeExplanation Commenting Style

## Required Line Shape

For ordinary code:

```c
// 注释：直接说明该行含义，必要时解释变量名。
// 逻辑：说明该行在算法中的作用。
original line
```

For German, English, or mixed-language original comments:

```c
// 原注释翻译：翻译原注释内容。
// 逻辑：说明这条注释所描述的控制意图。
// Original comment
```

Keep the original line exactly as it was. Preserve indentation, spacing, punctuation, and encoding-visible text in the original line. Add explanations above it only.

## What To Explain

For declarations and ports, explain signal direction, likely physical meaning, and naming hints.

Example:

```c
// 注释：声明输入端口 aMax_VL，推测为左前轮/VL(Vorne Links)的最大加速度。
// 逻辑：后续会把四个车轮的最大加速度放入本地数组，便于按轮速排序索引读取。
.Inport()aMax_VL
```

For assignments, explain source value, destination value, and whether the assignment initializes, stores history, updates state, or lands an output.

For conditions, explain each line of a multi-line condition separately. Mention the current condition fragment and how it contributes to the combined gate.

For braces, `else`, and block delimiters, explain structure:

```c
// 注释：进入低速参考支撑使能分支。
// 逻辑：所有前置条件满足后，在该代码块内打开支撑标志。
{
```

For blank lines, preserve blank lines without annotation unless the user explicitly requests every physical line including blanks.

## Translation Guidance

Translate German and English original comments before adding any broader interpretation. Use `原注释翻译：` instead of `注释：` for those lines.

Preserve the original comment text exactly, including spelling mistakes or transliterated German such as `fuer`, `Raeder`, `ueber`, and `zurueckgesetzt`. Explain the corrected meaning in Chinese when useful.

Common German control terms:

| German/source spelling | Chinese meaning |
| --- | --- |
| `Rad`, `Raeder` | 车轮 |
| `Achse`, `VA`, `HA` | 车轴、前轴、后轴 |
| `Druckaufbau` | 压力建立/增压 |
| `Druckabbau` | 压力下降/减压 |
| `Druckhalten` | 压力保持/保压 |
| `Anbremswert` | 制动开始值/制动起始参考值 |
| `Nachlaufzeit` | 后运行时间 |
| `Stotterbremse` | 点刹/高频断续制动 |
| `Schlupf` | 滑移 |
| `Instabiltendenz` | 失稳趋势 |
| `Vorgabe` | 给定请求/目标值 |

## Variable Inference Rules

Infer cautiously from:

- Nearby comments and block headings.
- Prefixes such as `v_` for speed, `a_` for acceleration, `T_` for time, `Nr_` for index/number, `Cnt_` for count, `Trig_` for trigger.
- Vehicle naming such as `FL/FR/RL/RR`, `VL/VR/HL/HR`, `FA/RA`, `VA/HA`.
- Repeated use in timers, thresholds, state decoders, and output self-assignments.

Use uncertainty language:

- `推测为...`
- `可能表示...`
- `结合上下文看...`

Avoid inventing hidden design intent when context is insufficient. Prefer a local explanation grounded in the visible code.

## Safety And Scope

Do not annotate the original source folder.

Do not make semantic edits while adding explanations.

Do not normalize generated-code quirks such as repeated self-assignments, unusual `.Inport()` lines, or mixed-language comments.

Do not remove or "fix" original comments, even when spelling is wrong. Place corrected translations above the original line.

When files are large, process in batches and validate each batch before moving on.
