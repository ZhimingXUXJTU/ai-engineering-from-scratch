# Tokenized Dataset with Sliding Window | 滑动窗口

> A pretraining run is a function from token ids to gradients. This lesson builds the conveyor that feeds the ids in.

> **【中文解读】** 本节是综合项目——构建 Token 化数据集和滑动窗口处理。


**Type:** Build | **类型:** Build
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 04 lessons, Phase 07 transformer lessons, Lesson 30 of this phase | **前置知识:** Phase 04 lessons, Phase 07 transformer lessons, Lesson 30 of this phase
**Time:** ~90 minutes | **时间:** ~90 minutes

## Learning Objectives | 学习目标
- Convert a raw corpus into a stream of token ids by calling the tokenizer once.
  中文翻译：Convert a raw corpus into a stream of token ids by calling the tokenizer once.
- Slice the id stream into fixed-length windows with a configurable overlap stride.
  中文翻译：Slice the id stream into fixed-length windows with a configurable overlap stride.
- Build a PyTorch Dataset that returns input and target tensors for next-token prediction.
  中文翻译：Build a PyTorch Dataset that returns input and target tensors for next-token prediction.
- Wrap the dataset in a DataLoader with a deterministic shuffle seeded per epoch.
  中文翻译：Wrap the dataset in a DataLoader with a deterministic shuffle seeded per epoch.
- Reason about the trade-off between stride, redundancy, and effective dataset size.
  中文翻译：Reason about the trade-off between stride, redundancy, and effective dataset size.

## The frame

> **【中文解读】** 预训练运行每次读取一个 batch 的 token ID 并更新模型。Batch 的形状固定为 `(B, T)` 输入 ID 和 `(B, T)` 目标 ID（目标 = 输入左移一位）。本节构建数据管线：分词器将文本转为扁平 ID 列表，滑动窗口将其切为训练样本，Dataset 暴露为张量，DataLoader 负责批处理和确定性洗牌。

> **【拓展：滑动窗口与上下文长度】** GPT-2 的上下文长度为 1024 token，GPT-3 增加到 2048，GPT-4 Turbo 达到 128K。滑动窗口的 stride 直接影响有效数据集大小：stride=T 时无重叠，stride=1 时数据集扩大 T 倍。实际预训练通常使用 stride 等于上下文长度，因为语料库已远超模型能在一个 epoch 中处理的量。RedPajama-V2 数据集包含超过 30 万亿 token，即使 stride=1 也无法在合理时间内遍历完。 The shape of each batch is fixed by the training contract. For a causal language model, the batch holds `(B, T)` input ids and `(B, T)` target ids where the target is the input shifted left by one. The job of the data pipeline is to produce that contract on demand, in a deterministic and reproducible way, from a corpus that may be several gigabytes of raw text.

This lesson builds the pipeline. The tokenizer from the previous lesson turns text into a long flat list of ids. A sliding window slices that list into training examples. A custom Dataset exposes the examples as tensors. A DataLoader batches them and shuffles them with a known seed.

> 本课构建该契约。


## The shape contract

A causal LM consumes ids of shape `(B, T)` where `B` is the batch size and `T` is the context length. The target at position `t` is the input at position `t+1`. That means every training example covers `T+1` raw ids. The window stride controls how much overlap exists between consecutive examples.

> 一个causal LM consumes ids of shape `(B, T)` where `B` is the batch size and `T` is the context length. The target at position `t` is the input at position `t+1`. That means every training example covers `T+1` raw ids. The window stride controls how much overlap exists between consecutive examples.


```mermaid
flowchart LR
    A[raw corpus text] --> B[tokenizer.encode]
    B --> C[flat list of ids]
    C --> D[sliding window slicer]
    D --> E[(id_window_0)]
    D --> F[(id_window_1)]
    D --> G[(id_window_n)]
    E --> H[PyTorch Dataset]
    F --> H
    G --> H
    H --> I[DataLoader with seeded shuffle]
    I --> J[batches of B x T+1 ids]
    J --> K[split into input and target]
```

The slicer never overlaps with the boundary of the corpus. If the last window does not have enough ids to fill `T+1` positions, the slicer drops it. Padding the tail with `<|pad|>` is also a valid choice but it complicates the loss mask. For this lesson we drop.

> slicer never overlaps with the boundary of the corpus. If the last window does not have enough ids to fill `T+1` positions, the slicer drops it. Padding the tail with `<|pad|>` is also a valid choice but it complicates the loss mask. For this lesson we drop.


## Why a sliding window

> **【中文解读】** 如果模型只看到不重叠的窗口，每个训练样本都教它相同的 T 个边界位置。调整 stride 移动边界，让模型看到更多样化的"预测下一个 token"任务。stride=T 无重叠，stride=T/2 50% 重叠使有效数据集翻倍，stride=1 最大重叠使数据集扩大 T 倍。代价是每个 epoch 更多计算。

A pretraining corpus is one long stream of ids. If the model only saw non-overlapping windows, every training example would teach it the same `T` boundaries. Adjusting the stride moves those boundaries around so the model sees more diverse predict-next-token tasks.

> 一个pretraining corpus is one long stream of ids. If the model only saw non-overlapping windows, every training example would teach it the same `T` boundaries. Adjusting the stride moves those boundaries around so the model sees more diverse predict-next-token tasks.


A stride of `T` produces non-overlapping windows. A stride of `T // 2` produces fifty-percent overlap and doubles the effective dataset. A stride of `1` produces maximum overlap and increases the dataset by a factor of `T`. The cost is more compute per epoch. The benefit is more boundary diversity. Most pretraining runs use a stride equal to the context length because the corpus is already much larger than the model can finish in one epoch, so the boundary diversity argument is weaker.

> 一个stride of `T` produces non-overlapping windows. A stride of `T // 2` produces fifty-percent overlap and doubles the effective dataset. A stride of `1` produces maximum overlap and increases the dataset by a factor of `T`. The cost is more compute per epoch. The benefit is more boundary diversity. Most pretraining runs use a stride equal to the context length because the corpus is already much larger than the model can finish in one epoch, so the boundary diversity argument is weaker.


## The Dataset class

A PyTorch Dataset has two required methods. `__len__` returns the number of examples. `__getitem__` returns one example as a pair of tensors. Our Dataset stores the encoded id stream and the stride. Indexing into it computes the start of the window on the fly so the memory cost is one copy of the id stream regardless of how many examples the stride produces.

> 一个PyTorch Dataset has two required methods. `__len__` returns the number of examples. `__getitem__` returns one example as a pair of tensors. Our Dataset stores the encoded id stream and the stride. Indexing into it computes the start of the window on the fly so the memory cost is one copy of the id stream regardless of how many examples the stride produces.


```mermaid
sequenceDiagram
    participant Trainer
    participant DataLoader
    participant Dataset
    participant Tokenizer
    Trainer->>DataLoader: iter(dataloader)
    DataLoader->>Dataset: __len__
    DataLoader->>Dataset: __getitem__(i)
    Dataset->>Dataset: window = ids[start:start+T+1]
    Dataset->>DataLoader: (input_ids, target_ids)
    DataLoader->>Trainer: batch (B,T) input, (B,T) target
    Note over Tokenizer,Dataset: tokenizer.encode runs once at build time
```

The shift-by-one happens inside `__getitem__`. The Dataset returns `(input, target)` where `input = window[:-1]` and `target = window[1:]`. Both are PyTorch long tensors. The training loop treats them as ground truth.

> shift-by-one happens inside `__getitem__`. The Dataset returns `(input, target)` where `input = window[:-1]` and `target = window[1:]`. Both are PyTorch long tensors. The training loop treats them as ground truth.


## Deterministic shuffle

> **【中文解读】** 通过向 DataLoader 传递显式的 `torch.Generator`（每个 epoch 的种子为 `base_seed + epoch_index`），确保每次运行时看到相同的数据顺序。这对比较两个仅有一个超参数差异的运行至关重要——没有种子，两次运行看到不同的数据顺序，损失曲线的分歧可能与模型改动无关。

> **【拓展：大规模数据集的确定性训练】** LLM 预训练的复现性要求极高。Meta 在 LLaMA 训练中使用确定性的数据加载顺序和固定种子，使得消融实验具有可比性。PyTorch 的 DistributedSampler 通过 `set_epoch()` 同步各 rank 的随机状态。MosaicML 的 Composer 框架将种子管理提升为一等公民，支持跨 checkpoint 恢复的完全确定性复现。

A DataLoader with `shuffle=True` reads from a PyTorch random generator. By passing an explicit `torch.Generator` seeded per epoch, we get the same shuffle every time the run is restarted. That property matters when you want to compare two runs that differ only in a single hyperparameter. Without a seed, two runs see the data in different orders and the loss curves diverge for reasons unrelated to the change.

> 一个DataLoader with `shuffle=True` reads from a PyTorch random generator. By passing an explicit `torch.Generator` seeded per epoch, we get the same shuffle every time the run is restarted. That property matters when you want to compare two runs that differ only in a single hyperparameter. Without a seed, two runs see the data in different orders and the loss curves diverge for reasons unrelated to the change.


The seed contract in this lesson is simple. `epoch_seed = base_seed + epoch_index`. The base seed is passed at construction. The epoch index is incremented by the trainer at the top of each epoch. A re-run with the same base seed always sees the same order in every epoch.

> seed contract in this lesson is simple. `epoch_seed = base_seed + epoch_index`. The base seed is passed at construction. The epoch index is incremented by the trainer at the top of each epoch. A re-run with the same base seed always sees the same order in every epoch.


## Batch sampler

The default sampler in PyTorch picks indices uniformly at random with replacement disabled. That is what we want for pretraining. For finetuning on a small dataset the contract is the same. The DataLoader assembles a batch by calling `__getitem__` `B` times and stacking the results. Because every example is the same length by construction, no padding logic is needed.

> default sampler in PyTorch picks indices uniformly at random with replacement disabled. That is what we want for pretraining. For finetuning on a small dataset the contract is the same. The DataLoader assembles a batch by calling `__getitem__` `B` times and stacking the results. Because every example is the same length by construction, no padding logic is needed.


The lesson keeps `num_workers=0` for simplicity. In a production run the workers parallelize the `__getitem__` calls. With our pipeline that is mostly a no-op because the work is just a slice of an in-memory tensor, but the same Dataset API supports workers cleanly.

> lesson keeps `num_workers=0` for simplicity. In a production run the workers parallelize the `__getitem__` calls. With our pipeline that is mostly a no-op because the work is just a slice of an in-memory tensor, but the same Dataset API supports workers cleanly.


## Counting examples

For an id stream of length `N`, a context length `T`, and a stride `S`, the number of examples is `max(0, 1 + (N - (T + 1)) // S)`. The lesson exposes that calculation as a static method on the Dataset so the trainer can compute total steps per epoch without iterating.

> 对于an id stream of length `N`, a context length `T`, and a stride `S`, the number of examples is `max(0, 1 + (N - (T + 1)) // S)`. The lesson exposes that calculation as a static method on the Dataset so the trainer can compute total steps per epoch without iterating.


## What this lesson does not do

> **【中文解读】** 本课不处理磁盘流式读取——语料全部加载到内存。不处理多文档——语料被视为一条连续 ID 流，文档边界通过插入 `<|endoftext|>` ID 编码。这两种能力在大规模预训练中必不可少，但它们替换的是存储层，不影响 Dataset 的契约接口。

It does not stream from disk. The corpus is encoded fully in memory and held as a single tensor. For a corpus of a few million ids that is well under a hundred megabytes and is the right shape for the lesson. Disk streaming is a separate concern that plugs in by replacing the storage but keeps the Dataset contract.

> It does not stream from disk.


It does not handle multiple documents. The corpus is treated as one continuous id stream. The next-document boundary is encoded by inserting `<|endoftext|>` ids when the corpus is built from multiple documents. The model learns to predict around the boundary.

> It does not handle multiple documents.


## How to read the code

`main.py` defines two classes and one helper. `SlidingWindowDataset` is the PyTorch Dataset. `make_dataloader` returns a configured DataLoader with a seeded generator. `_encode_corpus_to_ids` is the one-shot tokenizer call. The demo at the bottom builds a small tokenizer in-process, encodes a built-in corpus, constructs the dataset and dataloader, prints one batch, and asserts the shape contract. The tests in `code/tests/test_dataset.py` pin the window count formula, the shift-by-one property, the deterministic shuffle, and the stride trade-off.

> `main.


Run the demo. Then change the context length from 16 to 32 and watch how the number of examples per epoch falls. That number is your steps-per-epoch budget.

> Run the demo.

