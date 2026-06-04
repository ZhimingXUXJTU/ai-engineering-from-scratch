# Experiment Runner | 实验 运行器

> The loop is only as honest as its measurements. Build the runner that takes a spec, executes it in a sandboxed subprocess, and emits a json metrics blob the evaluator can trust.

> **【中文解读】** 本节是综合项目——构建实验运行器。


**类型：** 构建
**语言：** Python
**前置知识：** Phase 19 Track A lessons 20-29
**预计时间：** ~90 minutes

## Learning Objectives | 学习目标
- Encode an experiment as a typed spec the runner can serialise to a subprocess.
- Launch a subprocess with a hard wall clock timeout and a soft memory cap, and surface both as terminal conditions.
- Capture stdout, stderr, and the structured metrics blob into a single result record.
- Build an ablation table that sweeps one configuration knob at a time over a fixed base spec.
- Keep every result deterministic given a seed so the evaluator sees the same numbers across runs.

## Why a subprocess

> **【中文解读】** 研究循环运行不受信任的代码——假设来自采样器，实验脚本也来自同一路径。将它们视为进程内安全的是在邀请崩溃。子进程是最简单的隔离：独立地址空间，父进程有信号句柄。本课的运行器不实现完整沙盒（无 cgroup、seccomp、namespace），但有墙钟超时、内存轮询和终止路径——这是所有更复杂沙盒扩展的运行时契约。

> **【拓展：实验隔离在 AI 科研平台中的实践】** Google 的 Vertex AI Experiments 和 Weights & Biases 的 Sweeps 都使用容器化隔离运行实验脚本。Meta 的 ADBench 使用 Kubernetes Job 运行对比实验。子进程 + 超时 + 内存限制是这些工业方案的核心简化版本。关键设计原则：运行器从不因非零退出码抛异常——而是记录在结果的 `terminal` 字段中，让评估器决定如何处理。

A research loop runs untrusted code. The hypothesis came from a sampler, the experiment script came from the same path; treating either as safe in-process is asking for a crash that takes the orchestrator down. Subprocesses are the simplest isolation the language ships: a separate process, an independent address space, a signal handle on the parent side.

The runner here does not implement full sandboxing. There is no cgroup, no seccomp filter, no namespace remapping. What it does have is a wall clock timeout, a polling loop for memory growth, and a kill path that terminates the process on either limit. That is the runtime contract every more elaborate sandbox extends. The lesson keeps the contract small enough to read in one sitting.

## The ExperimentSpec shape

> **【拓展：实验规格在 MLOps 中的标准化】** 本课的 ExperimentSpec 映射到 MLOps 中的实验追踪标准。MLflow 的 Experiment + Run、Weights & Biases 的 Sweep Config、Determined AI 的 Experiment Config 都采用类似的声明式规格。关键字段：hypothesis_id（关联研究问题）、config（可复现的参数）、seed（确定性保证）、metric_keys（评估器需要读的字段）。标准化实验规格使得实验可复现、可比较、可审计。

```text
ExperimentSpec
  spec_id        : str            (stable id, "exp_001")
  hypothesis_id  : int            (link back to the queue from lesson 50)
  script_path    : str            (path to the python script to run)
  config         : dict           (passed to the script as one json arg)
  seed           : int            (deterministic seed for the experiment)
  wall_timeout_s : float          (hard timeout, killed on exceed)
  memory_cap_mb  : int            (soft cap, polled; killed on exceed)
  metric_keys    : list[str]      (which fields the evaluator will read)
```

The script lives on disk; the runner writes the config to a temp file path that the script reads. The script is expected to print a single json line on stdout whose keys are a superset of `metric_keys`. Anything else on stdout is captured but ignored by the metrics parser.

## 架构 | 架构

```mermaid
flowchart TD
    A[ExperimentSpec] --> B[serialise config to temp file]
    B --> C[spawn subprocess]
    C --> D[stdout / stderr pipes]
    C --> E[wall clock timer]
    C --> F[memory poller]
    E -- exceeded --> K[kill process]
    F -- exceeded --> K
    D --> P[parse final json line]
    K --> R[result with terminal=timeout or oom]
    P --> R[result with metrics]
    R --> O[ExperimentResult]
```

The runner is one class with one main method. The poller is a small thread that wakes once every poll interval and reads the subprocess `psutil` equivalent from the proc filesystem when available, falling back to no op when the platform does not expose it.

## Why a soft memory cap

Hard memory caps need `resource.setrlimit` and only work on POSIX. The lesson ships a portable approach: poll the resident set size from the platform and kill the subprocess if it exceeds the cap. The cap is soft because the poller has a non zero interval; a process can spike above the cap between polls and then drop back. The runner records the maximum observed RSS so the evaluator can see how close the run came to the limit.

On systems without process inspection support, the poller logs a one time warning and disables itself. The wall clock timeout still applies. The lesson tests cover both paths.

## Capturing stdout and stderr

> **【中文解读】** 运行器读取 stdout 和 stderr 管道。Stdout 逐行扫描——最后一个解析为 JSON 且包含所有必需 `metric_keys` 的行作为度量数据块。先前的 JSON 行保留在 `intermediate_metrics` 中，评估器可用于学习曲线。Stderr 原样捕获。非零退出码记录但不抛异常，标记为 `"crash"`。

The runner reads both pipes drained on completion. Stdout is scanned line by line; the last line that parses as json with all required `metric_keys` is taken as the metrics blob. Earlier json lines are kept in the result as `intermediate_metrics`; the evaluator can use these for learning curves.

Stderr is captured verbatim into the result. The runner never raises on a non zero exit code; instead it records the code in the result. Any non zero exit is labelled `"crash"` even when the script printed metrics, so the evaluator treats partial runs as failures by default.

## Ablation table

> **【中文解读】** 消融表（Ablation Table）一次只变一个参数。完整因子设计指数爆炸且评估器无法解释。单参数消融产生评估器可以绘图的干净坐标轴。本课支持多参数扫描，但作为重复的单参数消融由调用者组合。每个 spec 从基础 spec 派生，获得 `spec_id = "{base}_{knob}_{value}"` 格式的标识符。

> **【拓展：消融实验在 LLM 论文中的标准地位】** GPT-4、LLaMA、Mistral 等论文都包含大量消融实验：模型大小消融（7B vs 13B vs 34B vs 70B）、训练数据消融（1T vs 2T tokens）、注意力机制消融（MHA vs GQA vs MQA）。消融表是 AI 论文中验证"哪个组件贡献了什么"的核心工具。

```python
def ablate(base: ExperimentSpec, knob: str, values: list[Any]) -> list[ExperimentSpec]:
    ...
```

Given a base spec and a knob name, the helper returns one spec per value with `config[knob]` overridden. Each spec gets a derived `spec_id` (`f"{base.spec_id}_{knob}_{value}"`). The runner ships an `AblationRunner` that runs them in order and returns an `AblationTable` keyed by knob value.

Why one knob at a time. Full factorial sweeps blow up exponentially and produce results the evaluator cannot interpret. One knob at a time produces a clean axis the evaluator can plot. The lesson supports multi knob sweeps only as repeated single knob ablations, composed by the caller.

## Determinism

> **【中文解读】** 每个 spec 携带种子，运行器通过 `config["__seed"]` 传递给脚本。模拟实验脚本使用 numpy random pass 生成确定性度量。评估器依赖此特性——没有确定性，一次"回归"可能只是不同的随机初始化。本课消融表中的两次运行断言产生相同的度量值。

Every spec carries a seed. The runner forwards the seed to the script via the config dict (`config["__seed"] = spec.seed`). The mock experiment scripts in `code/experiments/` honour the seed and produce identical metrics across runs. The evaluator in lesson fifty-three depends on this; without determinism a "regression" might be a different random initialisation.

## The mock experiment script

The lesson ships one experiment script: `code/experiments/sparsity_experiment.py`. It is a real script that reads its config file, simulates a small training run with a numpy random pass, and prints a json metrics blob. The script honours a `sleep_s` knob for testing timeouts and an `allocate_mb` knob for testing the memory poller.

The simulation is not training anything real. It is a numerical computation that mimics the shape of a training loop: a loss curve, a final perplexity, a wall time. The point of the lesson is the runner, not the simulation. A real experiment script would import a model.

## 结果形状

```text
ExperimentResult
  spec_id              : str
  hypothesis_id        : int
  exit_code            : int
  terminal             : "ok" | "timeout" | "oom" | "crash"
  wall_time_s          : float
  peak_rss_mb          : float | None
  metrics              : dict
  intermediate_metrics : list[dict]
  stdout_tail          : str
  stderr_tail          : str
```

The evaluator reads `metrics` and `terminal` first. If terminal is anything other than `"ok"` the experiment counts as a failed run and the evaluator's verdict is automatic. Otherwise the metrics are passed through the significance test.

## 如何阅读代码

`code/main.py` defines `ExperimentSpec`, `ExperimentResult`, `ExperimentRunner`, `AblationRunner`, and a deterministic demo. The subprocess management is one class. The memory poller is a small thread. The ablation helper is a single function.

`code/experiments/sparsity_experiment.py` is the mock experiment used in tests. It reads its config file path from argv and writes a single json metrics line on completion.

`code/tests/test_runner.py` covers the success path, the timeout path, the crash path, the ablation table, and the determinism check across two runs.

## Where this slots in

Lesson fifty generates the hypothesis. Lesson fifty-one filters out anything the literature already settled. Lesson fifty-two runs the experiment for what is left. Lesson fifty-three reads the result, runs the significance test, and writes the verdict the orchestrator stores against the hypothesis id.
