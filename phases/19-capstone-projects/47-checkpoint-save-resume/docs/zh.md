# Checkpoint Save and Resume | 检查点

> Train interrupts kill runs; checkpoints let them continue. Save model, optimizer, scheduler, loss history, step counter, and RNG state, atomically, so a kill at any moment leaves a valid file on disk.

> **【中文解读】** 本节是综合项目——实现检查点保存和恢复。


**类型：** 构建
**语言：** Python
**前置知识：** Phase 19 lessons 42 to 45
**预计时间：** ~90 minutes

## Learning Objectives | 学习目标

- Capture the full training state into a single payload that can be reloaded into a fresh process.
- Implement atomic save with write-to-temp then rename so a crash never leaves a half-written file.
- Restore the RNG state for Python, NumPy, and PyTorch so the post-resume loss matches the uninterrupted baseline.
- Build a sharded checkpoint layout for models that no longer fit in a single file, with hash-verified shards and a JSON index.

## 问题引入 | 问题

> **【中文解读】** 训练作业设置 18 小时但集群墙钟上限 4 小时，第 11 小时内核升级导致重启。没有检查点则从头开始，即使模型权重存活，AdamW 动量矩也丢失了。正确的检查点包含五个状态桶：模型参数、优化器状态、调度器状态、训练计数器、以及所有随机数生成器（RNG）状态。没有 RNG 状态，恢复后的损失曲线是不同的曲线。原子保存通过先写入临时文件再重命名实现——崩溃不会留下半写文件。

> **【拓展：检查点在 LLM 训练中的工程挑战】** LLaMA 2 70B 的单检查点文件约 140GB。Meta 使用分片检查点，每个 GPU 写入自己的参数分片，通过 JSON 索引文件关联。GPT-4 训练使用异步检查点——训练继续运行的同时，后台线程将检查点写入分布式文件系统，避免训练暂停。恢复时需要在数千个 GPU 上并行加载分片，加载时间本身就是一个工程优化目标。

You set a training job for 18 hours. The wallclock cap is 4 hours. The cluster reboots at hour 11 because someone above your pay grade approved a kernel upgrade. Without checkpoints you start over. Without resume you also lose the optimizer state that took the first 11 hours to learn, so even if the model weights survived, the AdamW moments are gone and the next step lurches in a direction the training trajectory had already moved past.

The right artifact is a single file that holds everything needed to continue: model parameters, optimizer state, scheduler state, the loss history for plots, the current step and epoch and batch-in-epoch counters, and the RNG state for every source of randomness. Without the RNG state the resumed loss curve is a different curve. Same model, same data, different shuffle, different dropout mask, different number on the dashboard.

Atomic save is the other half of the contract. Writing into the final filename means a crash mid-write leaves a corrupt file; the resume reads garbage. Writing into a temporary file in the same directory and then renaming means a crash mid-write leaves the previous good file untouched. The rename is atomic on POSIX file systems.

## 核心概念 | 概念

```mermaid
flowchart TD
  ckpt[checkpoint payload] --> m[model state_dict]
  ckpt --> o[optimizer state_dict]
  ckpt --> s[scheduler state_dict]
  ckpt --> tr[train state: step, epoch, batch_in_epoch, losses]
  ckpt --> rng[rng state: python, numpy, torch_cpu, torch_cuda]
  ckpt --> meta[wall_saved_at, schema]
  ckpt --> write[atomic write: tmp file then os.replace]
```

### The five state buckets

| Bucket | Why it matters |
|--------|----------------|
| Model | Weights and buffers; what the model is. |
| Optimizer | Momentum and adaptive moments; without these the next step is a different optimization problem. |
| Scheduler | Where the learning rate is on its curve; cosine schedules in particular care. |
| Train counters | Step, epoch, batch-in-epoch, plus the loss history that draws the dashboard. |
| RNG state | Determinism for dropout, data shuffling, and any sampling inside the model. |

### Atomic save

> **【中文解读】** 原子保存的两条规则：1）临时文件与目标文件在同一目录，确保重命名在同一文件系统内（跨设备重命名不是原子操作）；2）临时名称每次唯一，防止两个写入者互相覆盖。崩溃在重命名前发生则原文件不变，崩溃在重命名后发生则新文件已有效。

```mermaid
flowchart LR
  payload[payload] --> tmpf[write to .ckpt.pt.XXXX.tmp]
  tmpf --> rename[os.replace to ckpt.pt]
  rename --> done[ckpt.pt is valid]
  crash1[crash before rename] --> orig[ckpt.pt unchanged]
  crash2[crash after rename] --> done
```

Two rules. First, the temporary file lives in the same directory as the target so the rename stays within the same file system; cross-device renames are not atomic. Second, the temporary name is unique per attempt so two writers do not stomp.

### Sharded checkpoints

> **【中文解读】** 当模型变大时，单文件检查点太大无法快速加载、难以检查、网络共享读取易出错。分片方案将参数状态按轮询方式（round-robin）分配到 N 个分片，写入包含每个分片 sha256 的 JSON 索引。加载器在合并前验证每个分片的哈希——静默截断的下载是最糟糕的 bug 类型。

> **【拓展：分片检查点在 Megatron-LM 中的应用】** NVIDIA 的 Megatron-LM 使用类似架构：每个 GPU 写入自己的参数分片（约 2GB），一个主索引文件记录所有分片的路径和校验和。恢复训练时，数千个 GPU 并行读取各自的分片，加载时间从数小时降低到分钟级。这种模式也是 PyTorch FSDP 的原生检查点格式。

When the model gets large the single-file payload becomes too big to load fast, too big to inspect, and too painful when a network share hiccups mid-read. The fix is to split the parameter state into shards and write a small index that ties them together.

```mermaid
flowchart LR
  state[state_dict] --> split[split keys round robin into N shards]
  split --> s0[model.shard-000.pt]
  split --> s1[model.shard-001.pt]
  split --> sN[model.shard-NNN.pt]
  s0 --> idx[index.json]
  s1 --> idx
  sN --> idx
  meta[meta.pt: optimizer + scheduler + train_state + rng] --> idx
```

The index records the shard count, the sha256 of each shard, and the sha256 of the meta file. The loader fails loudly when any hash mismatches. The shards can land on different physical disks; the meta is small and reads first.

### Resume continues mid epoch

> **【中文解读】** 恢复训练可以在 epoch 中间继续，通过 `(epoch, batch_in_epoch)` 加 RNG 状态实现。加载后训练循环快进随机数生成器跳过当前 epoch 已消耗的批次。本课代码严格实现此逻辑——断言恢复后的损失轨迹与未中断基线在 1e-4 范围内一致。

A resume that snaps to the start of the next epoch wastes anywhere from minutes to a day. The fix is `(epoch, batch_in_epoch)` plus the RNG state. After load, the training loop fast-forwards the random number generator past the batches already consumed in the current epoch and continues from `batch_in_epoch`. The lesson code does this exactly; the assertion is that the loss trajectory after resume matches the uninterrupted baseline within 1e-4.

## 动手实现 | 动手构建

`code/main.py` provides four primitives and a demo driver.

### Step 1: capture and restore RNG state

`capture_rng_state` returns a dict with Python's `random.getstate`, NumPy's `np.random.get_state`, and PyTorch CPU and CUDA RNG bytes. `restore_rng_state` reverses it. The CPU tensor is a uint8 byte buffer that PyTorch's RNG knows how to consume.

### Step 2: atomic save

`atomic_save` writes the payload to a temp file in the target directory, then `os.replace` swaps it into the final name. `atomic_write_json` does the same for the sharded index.

### Step 3: full checkpoint round trip

`save_checkpoint` packages the model, optimizer, scheduler, train state, and RNG into one dict. `load_checkpoint` reverses it and returns a `TrainState`. The schema field is the upgrade hook: future format changes bump the version string and the loader dispatches.

### Step 4: sharded variant

`save_sharded_checkpoint` round-robins the parameter keys across N shards, writes each shard with its own atomic save, writes a meta file with optimizer and scheduler and train state, and writes the JSON index with shard sha256s. `load_sharded_checkpoint` verifies every shard before merging.

### Step 5: resume demo

`run_resume_demo` trains a small model for `total_steps`, saves a checkpoint at `interrupt_at`, then continues. A second process restores the checkpoint and runs the remaining steps. The function returns the max absolute difference between the two loss trajectories after the interruption point. With RNG restored, the difference is zero or floating-point noise.

Run it:

```bash
python3 code/main.py
```

The single-file and sharded demos both assert max-diff under 1e-4. The summary lands in `outputs/resume-demo.json`.

## 用框架实现 | 使用方法

> **【拓展：检查点策略在大规模训练中的权衡】** 检查点频率是关键权衡：太频繁浪费 I/O 带宽（LLaMA 70B 检查点约 140GB），太稀疏则崩溃时损失更多进度。工业实践：1）每 N 步保存（N=1000 是常见值）；2）每 M 分钟保存（M=30 是常见值）；3）异步保存（训练继续，后台线程写检查点）。PyTorch 的 DistributedSampler 和 FSDP 的 full_state_dict API 处理了分布式环境下的检查点一致性——只有 rank 0 写入完整状态。

Production training stacks ship checkpointing as part of the trainer. The shape is the same: model + optimizer + scheduler + counters + RNG, written atomically, named by step so the latest is easy to find. Sharded layouts power large model loading with parallel reads; the index.json is what makes that work.

Three patterns to enforce:

- **Schema is a string in the payload.** Migrations branch on it. Without it you cannot evolve the format without breaking old runs.
- **Sha256 every shard.** A silently truncated download is the worst kind of bug; the loader fails fast or it fails late.
- **Keep checkpoint cadence honest.** Save every N steps and every wallclock-minute, whichever is shorter. Otherwise the long step that crashes wastes a full window of work.

## 产出物 | 部署上线

`outputs/skill-checkpoint-save-resume.md` is the recipe for any new training script: payload shape, atomic write, RNG capture, sharded index. Drop the skill into a repo, wire `save_checkpoint` at the periodic save site, wire `load_checkpoint` at startup, and the run survives kills.

## 练习题 | 练习题

1. Replace round-robin sharding with sharding by parameter group (layers ending in `.weight` vs `.bias`). When is each layout preferable?
2. Extend the save loop to keep the last K checkpoints and prune older ones. What is the right K when the disk is small?
3. Add a `--ckpt-every-seconds` flag that triggers a save on a wallclock interval, not just step count.
4. Add a checksum verification path that runs at startup, scans every checkpoint in the directory, and reports which ones are corrupt.
5. Implement a `migrate_v1_to_v2` function that adds a new field to the payload and bumps the schema string. Make load tolerate both versions.

## 术语速查表 | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Atomic save | "Write and pray" | Write to a temp file in the same directory, then os.replace into the target name |
| State dict | "The weights" | Model parameters and buffers, keyed by parameter name |
| Sharded checkpoint | "Big model file" | Multiple files, one per shard, plus a meta file and a JSON index with sha256s |
| RNG state | "Random seed" | Captured state for python random, numpy, torch CPU, torch CUDA; not just the seed |
| Mid-epoch resume | "Restart" | Fast-forward the RNG and continue from the next batch in the same epoch |

## 延伸阅读 | 延伸阅读

- POSIX `rename` semantics for the atomicity claim that `os.replace` relies on.
- PyTorch documentation on `torch.save` and `torch.load`, including `map_location` for cross-device restores.
- Phase 19 lesson 46 covers the gradient accumulation that this lesson's checkpoint payload survives across.
- Phase 19 lesson 48 covers the distributed wrappers whose state dict format this scheme accommodates.
- The Linux kernel `fsync` documentation for the durability guarantee behind atomic rename.
