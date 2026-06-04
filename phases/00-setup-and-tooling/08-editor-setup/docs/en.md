# Editor Setup | 编辑器配置

> Your editor is your co-pilot. Configure it once so it stays out of your way and starts pulling its weight.

**Type:** Build
**Languages:** --
**Prerequisites:** Phase 0, Lesson 01
**Time:** ~20 minutes

## Learning Objectives | 学习目标

- Install VS Code with essential extensions for Python, Jupyter, linting, and remote SSH
- Configure format-on-save, type checking, and notebook output scrolling for AI workflows
- Set up Remote SSH to edit and debug code on remote GPU machines as if they were local
- Evaluate editor alternatives (Cursor, Windsurf, Neovim) and their tradeoffs for AI work

> **【中文解读】**
> 编辑器是你写代码的主力工具。本章帮你配置 VS Code 用于 AI 开发：Python 支持、Jupyter 集成、远程 SSH 连接 GPU 服务器。配置一次，受益整个课程。

## The Problem | 问题描述

You'll spend thousands of hours inside your editor writing Python, running notebooks, debugging training loops, and SSH-ing into GPU boxes. A misconfigured editor turns every session into friction: no autocomplete, no type hints, no inline errors, manual formatting, and a clunky terminal workflow.

The right setup takes 20 minutes. Skipping it costs you 20 minutes every day.

> **【中文解读】**
> 配置编辑器只需 20 分钟，但不配置会让你每天多浪费 20 分钟。自动补全、类型检查、保存时格式化——这些小功能累积起来能省大量时间。

## The Concept | 核心概念

An AI engineering editor setup needs five things:

```mermaid
graph TD
    L5["5. Remote Development<br/>SSH into GPU boxes, cloud VMs"] --> L4
    L4["4. Terminal Integration<br/>Run scripts, debug, monitor GPU"] --> L3
    L3["3. AI-Specific Settings<br/>Auto-format, type checking, rulers"] --> L2
    L2["2. Extensions<br/>Python, Jupyter, Pylance, GitLens"] --> L1
    L1["1. Base Editor<br/>VS Code — free, extensible, universal"]
```

> **【中文解读】**
> AI 开发编辑器需要五层配置：基础编辑器 → 扩展插件 → AI 专用设置 → 终端集成 → 远程开发。其中远程 SSH 开发是最重要的——你需要在本地编辑器中直接操作远程 GPU 服务器。

## Build It | 动手实现

> **【拓展：VS Code 为什么是 AI 开发的首选编辑器】** VS Code 在 AI 开发中占据统治地位的原因：(1) 免费且轻量；(2) Jupyter Notebook 原生支持；(3) Remote SSH 直接连接 GPU 服务器编辑代码；(4) Python/Jupyter/Python Debugger 扩展生态完善；(5) AI 辅助编程扩展（Copilot、Cline、Continue）开箱即用。Cursor 和 Windsurf 是基于 VS Code 的 AI 增强版本，也值得尝试。

### Step 1: Install VS Code | 第1步：安装 VS Code

VS Code is the recommended editor. It is free, runs on every OS, has first-class Jupyter notebook support, and the extension ecosystem covers everything you need for AI work.

Download it from [code.visualstudio.com](https://code.visualstudio.com/).

Verify from the terminal:

```bash
code --version
```

If `code` is not found on macOS, open VS Code, press `Cmd+Shift+P`, type "Shell Command", and select "Install 'code' command in PATH".

### Step 2: Install Essential Extensions | 第2步：安装必备扩展

> **【中文解读】** AI 开发必备的 VS Code 扩展：Python（调试+Lint）、Jupyter（在编辑器中运行 Notebook）、Pylance（智能补全和类型检查）、GitLens（查看代码历史）。安装后在设置中开启"保存时格式化"，从此不用手动整理代码。

Open the integrated terminal in VS Code (`Ctrl+`` ` or `` Cmd+` ``) and install the extensions that matter for AI work:

```bash
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension ms-toolsai.jupyter
code --install-extension eamodio.gitlens
code --install-extension ms-vscode-remote.remote-ssh
code --install-extension ms-python.debugpy
code --install-extension ms-python.black-formatter
code --install-extension charliermarsh.ruff
```

What each one does:

| Extension | Why |
|-----------|-----|
| Python | Language support, virtual env detection, run/debug |
| Pylance | Fast type checking, autocomplete, import resolution |
| Jupyter | Run notebooks inside VS Code, variable explorer |
| GitLens | See who changed what, inline git blame |
| Remote SSH | Open a folder on a remote GPU box as if it were local |
| Debugpy | Step-through debugging for Python |
| Black Formatter | Auto-format on save, consistent style |
| Ruff | Fast linting, catches common mistakes |

The file `code/.vscode/extensions.json` in this lesson contains the full recommendations list. When you open the project folder, VS Code will prompt you to install them.

### Step 3: Configure Settings

Copy the settings from `code/.vscode/settings.json` in this lesson, or apply them manually through `Settings > Open Settings (JSON)`.

The key settings for AI work:

```jsonc
{
    "python.analysis.typeCheckingMode": "basic",
    "editor.formatOnSave": true,
    "editor.rulers": [88, 120],
    "notebook.output.scrolling": true,
    "files.autoSave": "afterDelay"
}
```

Why these matter:

- **Type checking on basic**: Catches wrong argument types before you run. Saves debugging time on tensor shape mismatches and wrong API parameters.
- **Format on save**: Never think about formatting again. Black handles it.
- **Rulers at 88 and 120**: Black wraps at 88. The 120 marker shows when docstrings and comments are getting too long.
- **Notebook output scrolling**: Training loops print thousands of lines. Without scrolling, the output panel explodes.
- **Auto-save**: You will forget to save. Your training script will run stale code. Auto-save prevents that.

### Step 4: Terminal Integration

VS Code's integrated terminal is where you run training scripts, monitor GPUs, and manage environments.

Set it up properly:

```jsonc
{
    "terminal.integrated.defaultProfile.osx": "zsh",
    "terminal.integrated.defaultProfile.linux": "bash",
    "terminal.integrated.fontSize": 13,
    "terminal.integrated.scrollback": 10000
}
```

Useful shortcuts:

| Action | macOS | Linux/Windows |
|--------|-------|---------------|
| Toggle terminal | `` Ctrl+` `` | `` Ctrl+` `` |
| New terminal | `Ctrl+Shift+`` ` | `Ctrl+Shift+`` ` |
| Split terminal | `Cmd+\` | `Ctrl+\` |

Split terminals are useful: one for running your script, one for monitoring GPU with `nvidia-smi -l 1` or `watch -n 1 nvidia-smi`.

### Step 5: Remote Development (SSH into GPU Boxes) | 第5步：远程开发（SSH 连接 GPU 服务器）

> **【拓展：Remote SSH 是 AI 开发的杀手级功能】** 大多数人没有本地 GPU，需要 SSH 到远程 GPU 服务器训练模型。VS Code 的 Remote SSH 扩展让你像编辑本地文件一样编辑远程代码——自动补全、调试、终端全都可用。这意味着你可以在轻薄本上开发，在远端 A100 上训练。

This is the most important extension for AI work. You will run training on remote machines (cloud VMs, lab servers, Lambda, Vast.ai). Remote SSH lets you open the remote filesystem, edit files, run terminals, and debug as if everything were local.

Setup:

1. Install the Remote SSH extension (done in Step 2).
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P`), type "Remote-SSH: Connect to Host".
3. Enter `user@your-gpu-box-ip`.
4. VS Code installs its server component on the remote machine automatically.

For passwordless access, set up SSH keys:

```bash
ssh-keygen -t ed25519 -C "your-email@example.com"
ssh-copy-id user@your-gpu-box-ip
```

Add the host to `~/.ssh/config` for convenience:

```
Host gpu-box
    HostName 203.0.113.50
    User ubuntu
    IdentityFile ~/.ssh/id_ed25519
    ForwardAgent yes
```

Now `Remote-SSH: Connect to Host > gpu-box` connects instantly.

## Alternatives | 替代方案

> **【拓展：AI 增强编辑器对比】** Cursor（基于 VS Code，内置 AI 编程助手，$20/月）和 Windsurf（Codeium 出品，免费层可用）都是 2024-2026 年兴起的 AI-native 编辑器。它们的核心优势：用自然语言描述需求，AI 自动生成代码。如果你已经在用 VS Code 扩展（如 Cline、Continue），迁移成本很低。

### Cursor

[cursor.com](https://cursor.com) is a VS Code fork with built-in AI code generation. It uses the same extension ecosystem and settings format. If you use Cursor, everything in this lesson still applies. Import the same `settings.json` and `extensions.json`.

### Windsurf

[windsurf.com](https://windsurf.com) is another AI-first VS Code fork. Same story: same extensions, same settings format, same Remote SSH support.

### Vim/Neovim

If you already use Vim or Neovim and are productive in it, stay there. The minimum setup for AI Python work:

- **pyright** or **pylsp** for type checking (via Mason or manual install)
- **nvim-lspconfig** for language server integration
- **jupyter-vim** or **molten-nvim** for notebook-like execution
- **telescope.nvim** for file/symbol search
- **none-ls.nvim** with black and ruff for formatting/linting

If you do not already use Vim, do not start now. The learning curve will compete with learning AI engineering. Use VS Code.

## Use It | 使用指南

> **【中文解读】** 推荐配置：VS Code + Python + Jupyter + Remote SSH。如果用远程 GPU 服务器，Remote SSH 是必须的。调试训练循环时，Jupyter 扩展让你在编辑器内直接查看张量形状和损失曲线。

With this setup, your daily workflow looks like:

1. Open the project folder in VS Code (or connect via Remote SSH to a GPU box).
2. Write Python in the editor with autocomplete, type hints, and inline errors.
3. Run Jupyter notebooks inline with the Jupyter extension.
4. Use the integrated terminal for training scripts, `uv pip install`, and GPU monitoring.
5. Review changes with GitLens before committing.

## Exercises | 练习题

1. Install VS Code and all extensions listed in Step 2
   安装 VS Code 和步骤 2 中列出的所有扩展
2. Copy the `settings.json` from this lesson into your VS Code config
   将本课的 `settings.json` 复制到你的 VS Code 配置中
3. Open a Python file and verify that Pylance shows type hints and Black formats on save
   打开一个 Python 文件，验证 Pylance 显示类型提示、Black 保存时自动格式化
4. If you have access to a remote machine, set up Remote SSH and open a folder on it
   如果有远程机器，设置 Remote SSH 并打开远程文件夹

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| LSP | "Autocomplete engine" | Language Server Protocol: a standard for editors to get type info, completions, and diagnostics from a language-specific server |
| Pylance | "The Python plugin" | Microsoft's Python language server using Pyright for type checking and IntelliSense |
| Remote SSH | "Working on the server" | VS Code extension that runs a lightweight server on a remote machine and streams the UI to your local editor |
| Format on save | "Auto-prettier" | The editor runs a formatter (Black, Ruff) every time you save, so code style is always consistent |

| 术语 | 俗称 | 实际含义 |
|------|------|---------|
| LSP | "自动补全引擎" | 语言服务器协议：编辑器获取类型信息、补全和诊断的标准 |
| Pylance | "Python 插件" | 微软的 Python 语言服务器，提供类型检查和智能提示 |
| Remote SSH | "在服务器上开发" | VS Code 在远程机器上运行轻量服务器，将 UI 传输到本地编辑器 |
| Format on save | "保存时自动格式化" | 每次保存时自动运行格式化工具，保持代码风格一致 |
