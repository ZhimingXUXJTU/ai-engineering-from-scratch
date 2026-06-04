# Cosine LR with Linear Warmup | 余弦 预热

> The learning-rate schedule is the second most important decision after the loss function. AdamW with a cosine decay and a linear warmup is the modern default for language-model training because it lets the model see a small effective step size during the brittle first thousand updates, ramps up to a configured peak, and decays smoothly back toward zero. This lesson builds that schedule, plots the curve over training steps, logs gradient norms next to the schedule, and proves the schedule honors warmup, peak, and decay boundaries.

> **【中文解读】** 本节是综合项目——实现余弦学习率调度和预热。


**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 19 lessons 30-37
**Time:** ~90 minutes

## Learning Objectives | 学习目标

- Implement an AdamW optimizer wired to a cosine learning-rate schedule with linear warmup.
- Compute the schedule's exact value at any step without floating-point drift across runs.
- Log gradient L2 norm side by side with the learning rate so training health is observable.
- Render the schedule to a text plot the eye can read and a CSV any tool can consume.

## The Problem | 问题

> **【中文解读】** 训练初期的更新最为剧烈——模型权重接近初始化值，优化器的二阶矩估计尚未稳定，梯度范数大且噪声高。如果学习率在此阶段处于峰值，模型要么直接发散，要么陷入无法逃脱的损失平台。余弦预热调度有三个区域：线性预热（0 到 warmup_steps）、余弦衰减（warmup_steps 到 total_steps）、以及底部夹持（total_steps 之后固定在 lr_min）。

> **【拓展：学习率调度在 GPT-4 和 LLaMA 训练中的应用】** GPT-4 的训练使用了 cosine decay with linear warmup，预热步数约为总步数的 2%。LLaMA 2 使用了 cosine schedule 并设置 lr_min 为 lr_max 的 10%，避免学习率归零导致训练停滞。GPT-3 的论文指出学习率是训练稳定性最敏感的超参数——甚至比模型架构更重要。

The first thousand training updates are the loudest. The model's weights are still close to initialization. The optimizer's running second-moment estimate has not stabilised. The gradient norm is large and noisy. If the learning rate is at its peak during these updates the model either diverges outright or settles into a loss plateau it never escapes. The two well-known fixes are gradient clipping, which is the subject of Phase 19 lesson 45, and a learning-rate schedule that starts small and ramps up.

The cosine-with-warmup schedule has three regions. From step zero to step `warmup_steps` the learning rate scales linearly from zero to the configured peak `lr_max`. From step `warmup_steps` to step `total_steps` the learning rate follows the upper half of a cosine curve, decaying from `lr_max` to `lr_min`. After `total_steps` the learning rate is pinned at `lr_min` so a misconfigured trainer that overshoots does not silently exit the schedule.

The build problem is that schedules are easy to get wrong off by one. The off-by-one shows up six hours into a training run as a learning rate that is 1 percent too high or too low at the moment the model starts overfitting, which is invisible unless the schedule is exhaustively tested at boundaries.

## The Concept | 概念

```mermaid
flowchart TD
  Step[Training step] --> Branch{step state}
  Branch -- step <= warmup --> Linear[Linear ramp from 0 to lr_max]
  Branch -- warmup < step <= total --> Cosine[Cosine decay from lr_max to lr_min]
  Branch -- step > total --> Floor[Pin at lr_min]
  Linear --> Apply[AdamW.step]
  Cosine --> Apply
  Floor --> Apply
  Apply --> GradNorm[Compute gradient L2 norm]
  GradNorm --> Log[Step log row]
  Log --> Plot[Text plot + CSV]
```

### Warmup formula

> **【中文解读】** 预热公式：当 `step` 在 `[0, warmup_steps]` 范围内时，学习率为 `lr_max * step / warmup_steps`。退化的 `warmup_steps = 0` 情况被视为"无预热"——调度从 step 0 直接以 lr_max 开始并立即进入余弦衰减。预热使优化器在最脆弱的初期使用小步长，逐步过渡到峰值。

For `step` in `[0, warmup_steps]` with `warmup_steps > 0`, the learning rate is `lr_max * step / warmup_steps`. The degenerate `warmup_steps = 0` case is treated as "no warmup": the schedule starts directly at `lr_max` at step zero and immediately enters cosine decay. Some test harnesses pass `warmup_steps = 0` to check the schedule still produces a usable curve.

### Cosine formula

> **【中文解读】** 余弦公式：当 `step` 在 `(warmup_steps, total_steps]` 范围内时，学习率为 `lr_min + 0.5 * (lr_max - lr_min) * (1 + cos(pi * progress))`。在 warmup_steps 处 cos(0) = 1，给出 lr_max；在 total_steps 处 cos(pi) = -1，给出 lr_min。两端连续性不是偶然——这是为什么调度实现为单个函数而非三个函数拼接的原因。

For `step` in `(warmup_steps, total_steps]` the learning rate is `lr_min + 0.5 * (lr_max - lr_min) * (1 + cos(pi * progress))` where `progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)`. At `step = warmup_steps` the cosine evaluates to `cos(0) = 1`, which gives `lr_max`, matching the warmup endpoint exactly. At `step = total_steps` the cosine evaluates to `cos(pi) = -1`, which gives `lr_min`, matching the decay endpoint exactly.

The continuity at both endpoints is not an accident. It is the reason the schedule is implemented as a single function over `step`, not as three different functions glued together. A glued schedule loses one boundary the first time `lr_max` is changed.

### Floor after total steps

For `step > total_steps` the learning rate stays at `lr_min`. The contract is explicit: the schedule does not error out and does not extrapolate; it pins at the floor and lets the trainer log a warning. Trainers that need to extend training change the schedule's `total_steps`, not the loop.

### Gradient norm logging alongside the rate

> **【中文解读】** 调度是训练健康的一半，梯度范数是另一半。训练循环每步记录学习率和梯度 L2 范数。发散的训练在损失曲线显示异常之前，梯度范数就会飙升；良好的预热表现为范数随学习率线性增长；过于激进的峰值表现为预热后范数持续偏高。日志格式 `step, lr, grad_l2_norm, loss` 是唯一的持久化记录。

> **【拓展：训练监控在工业界的实践】** Weights & Biases 和 TensorBoard 都将学习率曲线和梯度范数并排展示。DeepMind 的 Chinchilla 论文通过监控梯度范数发现了训练不稳定的根因。Meta 的 LLaMA 训练日志显示，梯度裁剪触发率是判断 warmup 是否充分的关键指标。

The schedule is half of training health. The gradient norm is the other half. The training loop logs both per step. A divergent training run shows the gradient norm spike before the loss does; a well-tuned warmup keeps the norm rising linearly with the rate; a too-aggressive peak shows up as a norm that stays high after warmup. The dataset on disk is `step, lr, grad_l2_norm, loss`. The CSV is the only durable record.

## Build It | 动手构建

`code/main.py` implements:

- `CosineWithWarmup` - a stateless function `lr(step) -> float` over the configured schedule.
- `TrainState` - wraps a model, an `AdamW` optimizer, and the schedule into a single step function.
- `TrainState.step` - runs one forward pass, one backward pass, logs gradient L2 norm, and applies `lr(step)` to the optimizer.
- `plot_schedule_ascii` - renders the schedule as a text plot the eye can read.
- `write_schedule_csv` - emits one row per step with the learning rate.

A demo at the bottom of the file builds a tiny `nn.Linear` model, trains for 20 steps over a fixed input batch, and prints the per-step learning rate, gradient norm, and loss. The schedule is also rendered as a text plot for the visual sanity check.

Run it:

```bash
python3 code/main.py
```

The script exits zero and prints a per-step training log plus the schedule plot.

## Production Patterns

> **【中文解读】** 四个生产模式：1）调度参数来自配置文件而非代码，确保可复现和可审计；2）步数计数器是单调递增且与 epoch 解耦的，从检查点恢复后继续正确位置；3）每次训练运行在输出目录写入调度图，PR 审查时无需重新运行；4）日志行 schema 固定（step, lr, grad_l2_norm, loss），下游 notebook 或仪表板依赖此 schema。

Four patterns elevate the schedule to a production artifact.

**Schedule lives in a config, not in code.** The trainer reads `warmup_steps`, `total_steps`, `lr_max`, `lr_min` from a YAML or JSON config that is committed to git. The schedule is reproducible because the config is content-addressed; the schedule is auditable because the config is part of the PR diff.

**Step counter is monotonic and decoupled from epochs.** Some frameworks confuse step and epoch when the dataset is sharded or the dataloader restarts. The schedule reads `global_step` from the trainer's checkpoint, not from a local counter. A resumed run continues at the right schedule position because the step counter is the durable axis.

**Schedule plot in the run directory.** Every training run writes `outputs/lr_schedule.png` (or in this lesson a text plot) into its run directory. A reviewer who skims the directory can sanity-check the schedule without re-running anything. This catches the misconfigured-schedule class of bugs at PR time.

**Log row schema is fixed.** `step, lr, grad_l2_norm, loss` in that order. A downstream notebook or dashboard reads the schema; renaming a column without bumping a version invalidates every existing dashboard.

## Use It | 使用方法

> **【拓展：学习率调度的替代方案】** 除余弦衰减外，常见的调度策略包括：1）线性衰减（GPT-3 使用）；2）多项式衰减（更平滑的过渡）；3）Warm Restarts / SGDR（周期性重启，Loshchilov & Hutter 2017）；4）Inverse Square Root（Transformer 原论文使用）；5）Constant with Warmup（LLaMA 2 的消融实验显示在短训练中与 cosine 持平）。选择策略时考虑训练长度：短训练对调度敏感，长训练（>1T tokens）各种策略趋于收敛。

Production patterns:

- **Sweep peak before sweeping anything else.** `lr_max` is the most sensitive knob. Sweep it on a small model first; the optimal `lr_max` scales weakly with model size, so the small-model sweep is a strong prior.
- **Warmup is a fraction of total steps, not an absolute count.** A 200-million-step run with 2,000 warmup steps starts at peak almost immediately; a 20,000-step run with the same number warms up for 10 percent. Configure warmup as a fraction (typical: 1-3 percent) so the schedule scales with training duration.
- **`lr_min` is non-zero on purpose.** A floor that is 10 percent of `lr_max` keeps the optimizer learning during the long tail. A `lr_min = 0` schedule produces a training curve that looks great on a plot and a model that has not actually finished training.

## Ship It | 部署上线

`outputs/skill-cosine-warmup.md` would, on a real project, describe which config carries the schedule, which trainer step the global counter is read from, and what `lr_max` sweep produced the deployed value. This lesson ships the engine.

## Exercises | 练习题

1. Add an inverse-square-root variant of the schedule and compare it on a 200-step toy training run. Which curve produces the lower final loss?
2. Add a `--restart` flag that adds a second warmup at `total_steps / 2`. Defend whether warm restarts improve or hurt on the toy run.
3. Add a unit test that the schedule is continuous: for every step in `[0, total_steps]` the difference `|lr(step+1) - lr(step)|` is bounded by `lr_max / warmup_steps`.
4. Wire the schedule into a `torch.optim.lr_scheduler.LambdaLR` so it composes with framework code. The lesson uses a plain step function; what does the wrapper change?
5. Add a `--plot-png` flag that writes a real plot via `matplotlib`. Defend whether the lesson's text plot or the PNG is the better default for CI runs.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Warmup | "Slow start" | Linear ramp from zero to `lr_max` over the first `warmup_steps` updates |
| Cosine decay | "Smooth drop" | Upper-half cosine curve from `lr_max` to `lr_min` over the remaining steps |
| Floor | "After training" | The fixed `lr_min` value the schedule pins at past `total_steps` |
| Gradient norm | "L2 of grads" | The Euclidean norm of the concatenated gradient vector, logged each step |
| Global step | "Schedule axis" | A monotonic step counter that survives restarts and drives the schedule |

## Further Reading | 延伸阅读

- [Loshchilov and Hutter, SGDR: Stochastic Gradient Descent with Warm Restarts (arXiv 1608.03983)](https://arxiv.org/abs/1608.03983) - the cosine schedule's reference paper
- [Loshchilov and Hutter, Decoupled Weight Decay Regularization (arXiv 1711.05101)](https://arxiv.org/abs/1711.05101) - AdamW's reference paper
- [PyTorch torch.optim.lr_scheduler](https://docs.pytorch.org/docs/stable/optim.html#how-to-adjust-learning-rate) - how step functions compose with framework schedulers
- Phase 19 · 42 - the downloader whose corpus this schedule consumes
- Phase 19 · 43 - the dataloader the schedule co-evolves with
- Phase 19 · 45 - gradient clipping and AMP, the next layer in the loop
