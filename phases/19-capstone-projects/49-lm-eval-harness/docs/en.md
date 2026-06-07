# Language Model Evaluation Harness | 评估 线束

> A model that does well on a task you cannot define is a model that does well by accident. The harness is the task definition, the metric, the runner, and the leaderboard, in one short, swappable shape.

> **【中文解读】** 本节是综合项目——构建 Agent 线束循环和契约验证系统。


**Type:** Build | **类型:** Build
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 19 lessons 42 to 45 | **前置知识:** Phase 19 lessons 42 to 45
**Time:** ~90 minutes | **时间:** ~90 minutes

## Learning Objectives | 学习目标

- Define a task as a JSONL file with `prompt`, `targets`, `metric`, and optional `extras` per example.
  中文翻译：Define a task as a JSONL file with `prompt`, `targets`, `metric`, and optional `extras` per example.
- Implement five metrics: exact match, rouge-l F1, executable check, multiple choice, and substring contains.
  中文翻译：Implement five metrics: exact match, rouge-l F1, executable check, multiple choice, and substring contains.
- Build a runner that batches examples per task and dispatches to a swappable model adapter.
  中文翻译：Build a runner that batches examples per task and dispatches to a swappable model adapter.
- Emit a leaderboard JSON with per-task scores, latency, and an overall average that is reproducible.
  中文翻译：Emit a leaderboard JSON with per-task scores, latency, and an overall average that is reproducible.

## The Problem | 问题

> **【中文解读】** 每周都有新语言模型发布，营销声称性能优异，但真正的问题是：在什么任务上优秀？没有评估线束，团队只能凭感觉比较两个模型。线束是昨天运行和今天运行之间的契约——固定任务集、固定度量、JSON 输出可 diff。核心陷阱是过度拟合线束到单一模型——线束必须足够小以在 15 分钟内读完，任务足够小可以随仓库分发，度量从零编写以便同事审计。

> **【拓展：lm-evaluation-harness 在 AI 行业中的地位】** EleutherAI 的 lm-evaluation-harness 是开源 LLM 评估的事实标准，HuggingFace 的 Open LLM Leaderboard 基于它构建。它支持 HellaSwag、ARC、MMLU、TruthfulQA 等核心基准。Meta 评估 LLaMA 时使用了定制版本，增加了代码生成和数学推理任务。评估线束的设计原则是：适配器（adapter）是唯一与模型相关的代码，交换适配器不影响任务和度量。

A new language model lands every week. The marketing claim is that it does well. The honest question is: well at what? The honest answer is the leaderboard you wrote yourself, because the vendor's leaderboard is the one they tuned to.

> 一个new language model lands every week. The marketing claim is that it does well. The honest question is: well at what? The honest answer is the leaderboard you wrote yourself, because the vendor's leaderboard is the one they tuned to.


Without a harness in your repo you compare two models by vibes. With a harness you compare them by score on a fixed task set with a fixed metric, on a JSON output you can diff. The harness is the contract between yesterday's run and today's run. Without it, regressions ship.

> 不使用a harness in your repo you compare two models by vibes. With a harness you compare them by score on a fixed task set with a fixed metric, on a JSON output you can diff. The harness is the contract between yesterday's run and today's run. Without it, regressions ship.


The trap is over-fitting the harness to a single model. The fix is the same trap in reverse: the harness is small enough to read in fifteen minutes, the tasks are small enough to ship in the repo, the metrics are written from scratch so a colleague can audit them, and the adapter is the only place model-specific code lives. Swap the adapter, the leaderboard moves; swap the tasks, the leaderboard moves. Nothing else should move.

> trap is over-fitting the harness to a single model. The fix is the same trap in reverse: the harness is small enough to read in fifteen minutes, the tasks are small enough to ship in the repo, the metrics are written from scratch so a colleague can audit them, and the adapter is the only place model-specific code lives. Swap the adapter, the leaderboard moves; swap the tasks, the leaderboard moves. Nothing else should move.


## The Concept | 概念

```mermaid
flowchart TD
  tasks[task JSONLs: prompt, targets, metric, extras] --> loader[load_all_tasks]
  loader --> runner[run_leaderboard]
  runner --> adapter[ModelAdapter.generate batch]
  adapter --> metrics[METRIC_FNS dispatch by name]
  metrics --> scores[per example score]
  scores --> board[Leaderboard: per task + overall]
  board --> out[leaderboard.json]
```

### Task spec

Every example is one JSONL line:

```json
{"id": "arith-00", "prompt": "compute: 2 + 2", "targets": ["4"], "metric": "exact_match"}
```

For metrics that need scoring helpers, `extras` carries the side payload:

> For metrics that need scoring helpers, `extras` carries the side payload:（翻译）


```json
{
  "id": "code-00",
  "prompt": "python: write a function f that doubles its input",
  "targets": ["ok"],
  "metric": "code_exec",
  "extras": {"io_pairs": [[1, 2], [3, 6]]}
}
```

A task is a `.jsonl` file under `outputs/tasks/`. The file name is the task name. All examples in a file share a metric.

> 一个task is a `.jsonl` file under `outputs/tasks/`. The file name is the task name. All examples in a file share a metric.


### The five fixture tasks

> **【中文解读】** 五个内置任务覆盖不同评估维度：算术（exact_match，token 级正确性）、摘要（rouge_l，最长公共子序列 F1）、代码执行（code_exec，输入输出对验证）、多选（multiple_choice，首字母匹配）、生成（substring_contains，自由文本包含目标子串）。code_exec 指标在剥离的 builtins 命名空间中执行预测——断言 `import os` 会失败。

| Task | Metric | What it tests |
|------|--------|---------------|
| arithmetic | exact_match | Token-level correctness on a deterministic answer |
| summary | rouge_l | Longest common subsequence F1 against a one-line reference summary |
| code-exec | code_exec | Executable test: the predicted function must satisfy a list of input-output pairs |
| multiple-choice | multiple_choice | First letter of the prediction must match an allowed letter |
| generation | substring_contains | Free-form text must contain at least one target substring |

### The metric contract

> **【中文解读】** 每个度量是从 `(prediction, targets, extras)` 到 `[0.0, 1.0]` 的函数。线束将每例得分平均得到任务得分，再将任务得分平均得到总分。度量函数都极小：exact_match 做小写化和空白归一化后比较相等性；rouge_l 计算最长公共子序列的 F1；code_exec 在受限命名空间执行预测并验证输入输出对。

Every metric is a function from `(prediction, targets, extras) -> float in [0.0, 1.0]`. The harness averages the per-example scores to get a task score, then averages task scores to get the overall. The metric functions are tiny:

> 每个metric is a function from `(prediction, targets, extras) -> float in [0.0, 1.0]`. The harness averages the per-example scores to get a task score, then averages task scores to get the overall. The metric functions are tiny:


- `exact_match`: lowercase, collapse whitespace, equality.
  中文翻译：`exact_match`: lowercase, collapse whitespace, equality.
- `substring_contains`: same normalization, substring test.
  中文翻译：`substring_contains`: same normalization, substring test.
- `multiple_choice`: first character uppercased.
  中文翻译：`multiple_choice`: first character uppercased.
- `rouge_l`: LCS length divided by lengths of prediction and reference, F1 of precision and recall.
  中文翻译：`rouge_l`: LCS length divided by lengths of prediction and reference, F1 of precision and recall.
- `code_exec`: execute the prediction in a restricted namespace, call `f(x)` on every input-output pair, count matches.
  中文翻译：`code_exec`: execute the prediction in a restricted namespace, call `f(x)` on every input-output pair, count matches.

The code_exec metric runs the prediction in a stripped builtins namespace. The lesson's test asserts that `import os` blows up because `os` is not in the namespace; you cannot reach the filesystem from a code prediction.

> code_exec metric runs the prediction in a stripped builtins namespace. The lesson's test asserts that `import os` blows up because `os` is not in the namespace; you cannot reach the filesystem from a code prediction.


### The model adapter

> **【中文解读】** 适配器是评估线束的接缝（seam）——`generate(prompts) -> list[str]` 是唯一的模型相关接口。本课提供 `ToyAdapter`（对固定任务返回正确答案的确定性模式匹配器）和 `HttpAdapter`（调用真实 API 的示例）。交换适配器，任务、度量和排行榜不变。

```python
class ModelAdapter(Protocol):
    def generate(self, prompts: Sequence[str]) -> List[str]: ...
    @property
    def name(self) -> str: ...
```

The adapter is the seam. The lesson ships `ToyAdapter`, a deterministic pattern matcher that returns the right answer for every prompt in the five fixture tasks. A real adapter calls the model and returns its output. The harness does not care which.

> adapter is the seam. The lesson ships `ToyAdapter`, a deterministic pattern matcher that returns the right answer for every prompt in the five fixture tasks. A real adapter calls the model and returns its output. The harness does not care which.


### The runner

`run_task` batches `batch_size` prompts at a time and dispatches to the metric function. `run_leaderboard` walks every task and averages. `write_leaderboard` emits JSON with a schema string so future format changes do not silently break dashboards.

> `run_task` batches `batch_size` prompts at a time and dispatches to the metric function.


```mermaid
flowchart LR
  examples[N examples] --> batches[B-sized batches]
  batches --> adapter[adapter.generate]
  adapter --> per[per example score 0..1]
  per --> avg[task score]
  avg --> over[overall = mean of task scores]
```

## Build It | 动手构建

`code/main.py` is the runnable artifact.

### Step 1: seed fixture tasks

`seed_fixture_tasks(target_dir)` writes the five `.jsonl` files. The first run of `main.py` seeds them when the directory is empty.

> `seed_fixture_tasks(target_dir)` writes the five `.


### Step 2: load tasks

`load_all_tasks(task_dir)` reads every `.jsonl` and returns a dict from task name to a list of `Example` records. Comment lines starting with `#` and blank lines are skipped so contributors can annotate the files.

> `load_all_tasks(task_dir)` reads every `.


### Step 3: implement metrics

Each metric is a small function with a unit test. The lesson's test suite includes 13 cases covering normalization, partial overlap, code execution, and unsafe code rejection.

> 每个metric is a small function with a unit test. The lesson's test suite includes 13 cases covering normalization, partial overlap, code execution, and unsafe code rejection.


### Step 4: write the runner

`run_task` iterates batches and produces a `TaskResult` with score, correct count, total count, and latency. `run_leaderboard` walks all tasks and produces a `Leaderboard` with the overall average.

> `run_task` iterates batches and produces a `TaskResult` with score, correct count, total count, and latency.


### Step 5: emit JSON

`write_leaderboard` serializes the board. The `--include-per-example` flag dumps the per-example records so you can diff predictions against the previous run when scores move.

> `write_leaderboard` serializes the board.


Run it:

```bash
python3 code/main.py
```

The script seeds the fixtures on first run, scores them with the toy adapter (which gets every fixture right), and writes `outputs/leaderboard.json`. Overall score is 1.0 with the toy adapter; the stub adapter test in `test_main.py` shows the same harness produces 0.0 when the adapter cannot answer.

> script seeds the fixtures on first run, scores them with the toy adapter (which gets every fixture right), and writes `outputs/leaderboard.json`. Overall score is 1.0 with the toy adapter; the stub adapter test in `test_main.py` shows the same harness produces 0.0 when the adapter cannot answer.


## Use It | 使用方法

> **【拓展：大语言模型评估基准的演进】** 2024-2026 年的评估基准经历了显著变化：1）MMLU 被证明存在数据污染，MMLU-Pro 被提出替代；2）HumanEval 扩展为 HumanEval+（增加测试用例）；3）IFEval（指令遵循评估）成为新标准；4）GPQA（研究生级别问答）取代 ARC 作为推理能力基准；5）LiveCodeBench 使用持续更新的 LeetCode 题目避免数据污染。本课的五任务设计是这些复杂基准的核心简化——相同的架构原则，更小的规模。

To plug a real model in, write an adapter. The shape:

```python
class HttpAdapter:
    name = "vendor.v1"

    def __init__(self, endpoint, api_key):
        self.endpoint = endpoint
        self.api_key = api_key

    def generate(self, prompts):
        out = []
        for prompt in prompts:
            response = http_post(self.endpoint, prompt, self.api_key)
            out.append(response["text"])
        return out
```

Swap `ToyAdapter` for `HttpAdapter` at the top of `main()`. The harness, the tasks, the metrics, and the leaderboard stay the same.

> Swap `ToyAdapter` for `HttpAdapter` at the top of `main()`.


Three patterns to enforce when shipping the harness in a real project:

> Three patterns to enforce when shipping the harness in a real project:（翻译）


- **Pin the task files.** The leaderboard.json carries hash-pinned task content or it carries the JSONLs alongside; otherwise the score moves when the task file does, and you cannot tell which.
  中文翻译：**Pin the task files.** The leaderboard.json carries hash-pinned task content or it carries the JSONLs alongside; otherwise the score moves when the task file does, and you cannot tell which.
- **Diff predictions, not just scores.** The `--include-per-example` flag lets you see what the model said the day the score dropped.
  中文翻译：**Diff predictions, not just scores.** The `--include-per-example` flag lets you see what the model said the day the score dropped.
- **Cap the batch size.** Real adapters have rate limits. A small batch size keeps the harness compatible across vendors.
  中文翻译：**Cap the batch size.** Real adapters have rate limits. A small batch size keeps the harness compatible across vendors.

## Ship It | 部署上线

`outputs/skill-lm-eval-harness.md` carries the recipe: JSONL task spec, five metrics, swappable adapter, batched runner, leaderboard JSON with schema string. The task files in `outputs/tasks/` are the fixtures; copy them into a real project as starters.

> `outputs/skill-lm-eval-harness.


## Exercises | 练习题

1. Add a sixth task with a custom metric you write from scratch (BLEU-like overlap, BLEURT-like reference scoring, anything with a clear contract).
2. Extend `code_exec` to capture stdout and accept a list of expected stdouts as targets.
3. Add a leaderboard diff command: given two `leaderboard.json` files, print which tasks moved and by how much.
4. Cap latency per example. Wrap the adapter call in a timeout; surface a separate `timeouts` column in the leaderboard.
5. Pin task content with a sha256 in the leaderboard so a future reader can verify they scored the same tasks.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Task spec | "The eval format" | JSONL file with prompt, targets, metric, optional extras per example |
| Metric | "How you score" | Function from (prediction, targets, extras) to a float in [0, 1] |
| Adapter | "The model client" | Object with a generate(prompts) -> list[str] method; the only model-specific code |
| Leaderboard | "The scoreboard" | JSON with per-task scores, total counts, latency, and an overall average |
| Code exec metric | "Run it and check" | Execute the prediction in a restricted namespace, compare against input-output pairs |

## Further Reading | 延伸阅读

- The original lm-evaluation-harness for the production reference, much larger but the same shape.
  中文翻译：The original lm-evaluation-harness for the production reference, much larger but the same shape.
- HuggingFace's lighteval for an alternative implementation of the same contract.
  中文翻译：HuggingFace's lighteval for an alternative implementation of the same contract.
- Phase 19 lesson 46 covers the gradient accumulation patterns used in the training stack the harness scores.
  中文翻译：Phase 19 lesson 46 covers the gradient accumulation patterns used in the training stack the harness scores.
- Phase 19 lesson 47 covers the checkpoint format you score against; pin the checkpoint hash in the leaderboard.
  中文翻译：Phase 19 lesson 47 covers the checkpoint format you score against; pin the checkpoint hash in the leaderboard.
- Phase 19 lesson 48 covers the distributed training stack that produced the model under test.
  中文翻译：Phase 19 lesson 48 covers the distributed training stack that produced the model under test.
