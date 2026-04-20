# line-code-explainer 安装教程

## 包内容

本安装包包含以下内容：

- `line-code-explainer/`
  完整技能目录，内含：
  - `SKILL.md`
  - `agents/openai.yaml`
- `line-code-explainer.zip`
  可直接分发的压缩安装包
- `安装教程.md`
  当前安装说明文件

## 适用场景

当需要把 `line-code-explainer` 技能安装到 Codex
全局技能目录，并在后续通过 `$line-code-explainer`
调用固定格式的逐行代码解释能力时，使用本安装包。

## 推荐安装方式：解压 zip 安装

1. 将 `line-code-explainer.zip` 解压。
2. 确认解压后得到目录：
   `line-code-explainer`
3. 将该目录复制到全局技能目录：
   `C:\Users\<你的用户名>\.codex\skills\`
4. 最终目录应为：
   `C:\Users\<你的用户名>\.codex\skills\line-code-explainer`

## 手动安装方式：直接复制目录

如果不使用 zip，也可以直接复制目录：

1. 复制 `line-code-explainer/`
2. 粘贴到：
   `C:\Users\<你的用户名>\.codex\skills\`
3. 确认以下文件存在：
   - `C:\Users\<你的用户名>\.codex\skills\line-code-explainer\SKILL.md`
   - `C:\Users\<你的用户名>\.codex\skills\line-code-explainer\agents\openai.yaml`

## 安装后校验

安装完成后，建议检查以下几点：

1. 技能目录存在且结构完整。
2. `SKILL.md` 可以正常打开。
3. `agents/openai.yaml` 存在且可读取。
4. Codex 技能列表中能看到 `Line Code Explainer`。
5. 可以尝试输入：
   `$line-code-explainer`
   观察是否能正常触发该技能。

## 功能说明

`line-code-explainer` 的核心能力包括：

- 按截图左侧行号逐行解释代码
- 原代码逐字保留，不改写
- 原代码缩进保持不变
- 统一使用 `c` 代码块输出
- 每行代码下方固定输出：
  - `// 含义`
  - `// 变量猜测/解释`
  - `// 背后逻辑`
  - `// 德语翻译`（有需要时）
- 注释内容过长时主动换行，不在一行内硬写到底
- 对截图中的德语乱码进行还原后再解释

## 升级方式

如果本机已经存在旧版 `line-code-explainer`：

1. 先备份旧目录：
   `C:\Users\<你的用户名>\.codex\skills\line-code-explainer`
2. 用新版本目录覆盖旧版本。
3. 刷新 Codex 技能列表或重启相关界面。

## 注意事项

- 不要把技能安装到 `.agents\skills\` 作为最终使用目录。
- `.agents\skills\` 更适合做 staging 或开发校验。
- 最终生效目录应为 `.codex\skills\`。
- 如果同时存在 staging 副本和全局副本，界面中可能会显示两个同名技能。

## 建议的最终目录

```text
C:\Users\<你的用户名>\.codex\skills\line-code-explainer\
├── SKILL.md
└── agents\
    └── openai.yaml
```
