# Capstone Lesson 26: Sandbox Runner with Denylist and Path Jail | 结业 运行器

> The verification gate decides whether a tool call should run. The sandbox decides what happens when it does. This lesson ships a subprocess runner that refuses dangerous executables, refuses dangerous argv shapes, jails every file path to a project root, truncates oversized output, and kills runaway processes on a wall-clock timeout. It is the second of two layers that sit between the model and the operating system.

> **【中文解读】** 本节是综合项目——构建沙盒运行器和拒绝名单。


**Type:** Build | **类型:** Build
**Languages:** Python (stdlib) | **语言:** Python (stdlib)
**Prerequisites:** Phase 19 · 25 (verification gates and observation budget), Phase 14 · 33 (instructions as constraints), Phase 14 · 38 (verification gates) | **前置知识:** Phase 19 · 25 (verification gates and observation budget), Phase 14 · 33 (instructions as constraints), Phase 14 · 38 (verification gates)

> 🔗 【前置】Agent Harness 7/10。验证门决定是否运行，沙箱决定运行时发生什么。
> 💡 沙箱 = "OS 防火墙"。subprocess 运行器拒绝危险可执行+危险 argv+路径锁项目根+输出截断+wall-clock 超时杀进程。这是模型和 OS 之间的两层防御之二（一是验证门）。Phase 15·14 Kill Switches 的实现细节。
**Time:** ~90 minutes | **时间:** ~90 minutes

## Learning Objectives | 学习目标

- Build a `Sandbox` class wrapping `subprocess.run` with timeout, capture, and truncation.
  中文翻译：Build a `Sandbox` class wrapping `subprocess.run` with timeout, capture, and truncation.
- Refuse a command by name against a denylist and by structure against an argv inspector.
  中文翻译：Refuse a command by name against a denylist and by structure against an argv inspector.
- Refuse any path argument that resolves outside a declared project root.
  中文翻译：Refuse any path argument that resolves outside a declared project root.
- Refuse shell metacharacters when shell mode is off.
  中文翻译：Refuse shell metacharacters when shell mode is off.
- Return a structured `SandboxResult` that downstream observability and the eval harness can ingest.
  中文翻译：Return a structured `SandboxResult` that downstream observability and the eval harness can ingest.

## The Problem | 问题

> **【中文解读】** 能执行 shell 命令的编码 Agent 可以在一个回合内安装后门、窃取密钥、损坏开发者笔记本和产生巨额云账单。三类故障反复出现：1）危险可执行文件（sudo, chmod -R 777, rm -rf, mkfs）；2）argv 把戏（python3 -c "import os; os.system('rm -rf /')"）；3）路径逃逸（读取 ../../etc/passwd）。沙盒不是操作系统意义的安全边界——它是开发时的护栏，使常见故障模式变得明显。

> **【拓展：沙盒技术在 AI Agent 产品中的演进】** Claude Code 的沙盒限制文件操作在项目目录内，shell 命令需要用户确认。Devin 使用 Docker 容器 + 文件系统只读挂载。OpenHands 使用 Firecracker microVM 提供内核级隔离。本课的 denylist + path jail + 超时 + 截断是这些方案的核心简化版本——覆盖了 90% 的常见 Agent 故障模式。

A coding agent that can shell out can install backdoors, exfiltrate keys, brick a developer laptop, and rack up a cloud bill in a single turn. The least costly defense is to not give it shell. The second least costly is a sandbox that says no to a precise list of patterns.

> 一个coding agent that can shell out can install backdoors, exfiltrate keys, brick a developer laptop, and rack up a cloud bill in a single turn. The least costly defense is to not give it shell. The second least costly is a sandbox that says no to a precise list of patterns.


Three classes of failure recur in agent traces.

The first is dangerous executables. A model under pressure to fix a path issue will try `sudo`, `chmod -R 777`, `rm -rf`, `mkfs`, `dd`. None of these belong in an agent run. The denylist catches them by name and by alias.

> first is dangerous executables. A model under pressure to fix a path issue will try `sudo`, `chmod -R 777`, `rm -rf`, `mkfs`, `dd`. None of these belong in an agent run. The denylist catches them by name and by alias.


The second is argv tricks. A model that has been told no shell will pipe an attack through an interpreter: `python3 -c "import os; os.system('rm -rf /')"`, `bash -c '...'`, `node -e '...'`, `perl -e '...'`. The sandbox needs to know that any interpreter run with a `-c`-like flag is just a shell call with extra steps.

> second is argv tricks. A model that has been told no shell will pipe an attack through an interpreter: `python3 -c "import os; os.system('rm -rf /')"`, `bash -c '...'`, `node -e '...'`, `perl -e '...'`. The sandbox needs to know that any interpreter run with a `-c`-like flag is just a shell call with extra steps.


The third is path escape. The model is told to read `./src/main.py` and instead reads `../../etc/passwd`. The sandbox jails every path argument by resolving it through `os.path.realpath` and asserting the prefix.

> third is path escape. The model is told to read `./src/main.py` and instead reads `../../etc/passwd`. The sandbox jails every path argument by resolving it through `os.path.realpath` and asserting the prefix.


The sandbox is not a security boundary in the operating system sense. A determined attacker with code execution can still break out. The sandbox is a development-time guardrail: it makes the common failure modes loud and stops the agent from doing damage out of sheer ineptitude.

> sandbox is not a security boundary in the operating system sense. A determined attacker with code execution can still break out. The sandbox is a development-time guardrail: it makes the common failure modes loud and stops the agent from doing damage out of sheer ineptitude.


## The Concept | 概念

> **【中文解读】** 沙盒有四个拒绝轴：名称（denylist 检查可执行文件名）、argv（检查解释器 -c 模式和 shell 元字符）、路径（通过 realpath 检查路径是否在 project_root 内）、结构（shell=False 时拒绝管道和重定向）。每个轴是纯函数，子进程只在所有轴通过后才启动。路径监狱是最精巧的部分——通过 `os.path.realpath` 解析符号链接，防止符号链接逃逸攻击。

```mermaid
flowchart TD
  Call[ToolCall<br/>already passed gate chain] --> Run["Sandbox.run()"]
  Run --> S1[1. resolve executable against denylist<br/>rm, sudo, mkfs, ...]
  S1 --> S2[2. inspect argv<br/>interpreter -c, shell metachars when shell=False]
  S2 --> S3[3. resolve path-like arguments<br/>against project_root via realpath]
  S3 --> S4[4. spawn subprocess<br/>capture, wall-clock timeout, env scrub]
  S4 --> S5[5. truncate stdout/stderr to max_output_bytes]
  S5 --> Result[SandboxResult<br/>exit_code, stdout, stderr,<br/>truncated, timed_out, denied, reason]
```

The sandbox has four refusal axes: name, argv, path, structure. Each axis is a pure function of the call, no subprocess yet. The subprocess only spawns after every axis has passed.

> sandbox has four refusal axes: name, argv, path, structure. Each axis is a pure function of the call, no subprocess yet. The subprocess only spawns after every axis has passed.


The `SandboxResult` exit codes are the conventional ones: 0 success, non-zero failure, plus three sentinel codes for denied (-100), timed_out (-101), and truncated (the exit code is the real one, with a flag set). Downstream lessons read this structured result rather than parsing stderr.

> `SandboxResult` exit codes are the conventional ones: 0 success, non-zero failure, plus three sentinel codes for denied (-100), timed_out (-101), and truncated (the exit code is the real one, with a flag set). Downstream lessons read this structured result rather than parsing stderr.


## Architecture | 架构

> **【拓展：从 denylist 到 seccomp 的安全升级路径】** 本课的 denylist 方案覆盖了约 90% 的常见 Agent 故障。生产级升级路径：1）Docker 容器（文件系统隔离 + 网络隔离）；2）gVisor（用户态内核，系统调用过滤）；3）Firecracker microVM（完整虚拟化，KVM 后端）；4）seccomp-bpf（精确的系统调用白名单）。OpenHands 使用 Docker + seccomp，Devin 使用 Firecracker。每一步升级增加安全边界但减少灵活性——denylist 是最灵活但最弱的选择。

```mermaid
flowchart LR
  Harness[AgentHarness<br/>lesson 20-25] -->|call| Sandbox[Sandbox<br/>denylist<br/>path jail<br/>argv inspect<br/>timeout<br/>truncation]
  Sandbox -->|exec| Popen[subprocess.Popen]
  Sandbox --> Result[SandboxResult]
```

The denylist is a frozenset of executable basenames. Aliases (`/bin/rm`, `/usr/bin/rm`) all resolve to the same basename. The argv inspector knows the interpreter shape: any argv where argv[0] is an interpreter and any later arg starts with `-c` or `-e` is denied. Shell metacharacters (`;`, `|`, `&`, `>`, `<`, backticks, `$()`) cause refusal when the call did not explicitly request a shell.

> denylist is a frozenset of executable basenames. Aliases (`/bin/rm`, `/usr/bin/rm`) all resolve to the same basename. The argv inspector knows the interpreter shape: any argv where argv[0] is an interpreter and any later arg starts with `-c` or `-e` is denied. Shell metacharacters (`;`, `|`, `&`, `>`, `<`, backticks, `$()`) cause refusal when the call did not explicitly request a shell.


The path jail is the most subtle piece. The sandbox accepts a `project_root` at construction. Any argument that looks like a path (contains `/` or matches an existing file) is normalized through `os.path.realpath`, then checked against the realpath of the project root. If the resolved target is not under the root, refusal. Symlink escape attempts (a symlink in the project root that points outside) are blocked by checking realpath, not the literal path.

> path jail is the most subtle piece. The sandbox accepts a `project_root` at construction. Any argument that looks like a path (contains `/` or matches an existing file) is normalized through `os.path.realpath`, then checked against the realpath of the project root. If the resolved target is not under the root, refusal. Symlink escape attempts (a symlink in the project root that points outside) are blocked by checking realpath, not the literal path.


## What you will build

The implementation is `main.py` plus a tests dir.

1. `SandboxResult` dataclass: exit_code, stdout, stderr, truncated, timed_out, denied, reason, duration_ms.
2. `SandboxConfig` dataclass: project_root, max_output_bytes, timeout_seconds, denylist, interpreter_block.
3. `Sandbox` class: `run(argv, *, shell=False, cwd=None)` returns a `SandboxResult`.
4. Internal refusal helpers: `_check_executable_denylist`, `_check_argv_interpreter`, `_check_shell_metachars`, `_check_path_jail`.
5. Output truncation with a clear `truncated` flag and a marker line in the captured stream.
6. Demo at the bottom: a sequence of legitimate and adversarial calls. Each is shown with its result.

The sandbox uses `subprocess.run` with `shell=False` by default and `capture_output=True`. The wall-clock timeout uses the `timeout` argument; on `TimeoutExpired`, the sandbox kills the process group and synthesizes a SandboxResult.

> sandbox uses `subprocess.run` with `shell=False` by default and `capture_output=True`. The wall-clock timeout uses the `timeout` argument; on `TimeoutExpired`, the sandbox kills the process group and synthesizes a SandboxResult.


## Why this is not a real sandbox

> **【中文解读】** 本课沙盒不使用 namespace、cgroup、seccomp、gVisor、Firecracker 或任何内核级隔离——子进程能做的沙盒也能做。保护是结构性的：拒绝最常见的危险调用，并将明确的拒绝记录到可观测性系统中。生产 Agent 需要在此基础上叠加：Docker 容器、microVM、降权、只读挂载、ulimit 等。

The lesson sandbox does not use namespaces, cgroups, seccomp, gVisor, Firecracker, or any kernel-level isolation. Anything the subprocess can do, the sandbox can do. The protection is structural: the agent is denied the most common dangerous invocations, and the loud refusal goes into observability instead of silently running.

> lesson sandbox does not use namespaces, cgroups, seccomp, gVisor, Firecracker, or any kernel-level isolation. Anything the subprocess can do, the sandbox can do. The protection is structural: the agent is denied the most common dangerous invocations, and the loud refusal goes into observability instead of silently running.


For production agents you layer on top: run inside an unprivileged Docker container, run inside a microVM, drop capabilities, mount the project root read-only and a scratch dir read-write, set ulimit on memory and CPU, scrub the environment to a known-safe whitelist. Lesson 29 does some of this. Operating-system isolation is out of scope for this lesson.

> 对于production agents you layer on top: run inside an unprivileged Docker container, run inside a microVM, drop capabilities, mount the project root read-only and a scratch dir read-write, set ulimit on memory and CPU, scrub the environment to a known-safe whitelist. Lesson 29 does some of this. Operating-system isolation is out of scope for this lesson.


## Running it | 运行

```bash
cd phases/19-capstone-projects/26-sandbox-runner-denylist
python3 code/main.py
python3 -m pytest code/tests/ -v
```

The demo creates a temp directory, drops a clean file into it, then runs a battery of calls. Legal calls succeed. Denied calls return SandboxResult with `denied=True` and a reason. Timeouts return `timed_out=True`. Truncation sets `truncated=True`. The demo prints a JSON table of outcomes and exits zero.

> demo creates a temp directory, drops a clean file into it, then runs a battery of calls. Legal calls succeed. Denied calls return SandboxResult with `denied=True` and a reason. Timeouts return `timed_out=True`. Truncation sets `truncated=True`. The demo prints a JSON table of outcomes and exits zero.


## How this composes with the rest of Track A

Lesson 25 produced the gate chain. Lesson 26 is the executor that runs after a gate ALLOW. Lesson 27's eval harness compares the sandbox results against the expected exit-code per task. Lesson 28 emits a `gen_ai.tool.execution` span around each `Sandbox.run` invocation. Lesson 29's end-to-end demo wires a real coding agent through both layers.

> Lesson 25 produced the gate chain.

