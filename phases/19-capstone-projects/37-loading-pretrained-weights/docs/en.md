# Loading Pretrained Weights | 预训练 加载 权重

> Training a 124 million parameter model from scratch is a budget decision; loading a published checkpoint is a Tuesday. This lesson loads pretrained GPT-2 style weights from a safetensors file into the exact architecture from lesson 35, walks the parameter name mapping piece by piece, and sanity generates a continuation to prove the load worked. No network, no third party loaders, no opaque magic.

> **【中文解读】** 本节是综合项目——加载预训练权重。


**Type:** Build | **类型:** Build
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 19 lessons 30 to 36 | **前置知识:** Phase 19 lessons 30 to 36

> 🔗 【前置】Track B 8/20。基于 30-36。
> 💡 加载预训练权重 = "站在巨人肩膀上"。从零训练 124M 模型=预算决策；加载已发布 checkpoint=日常操作。本课从 safetensors 加载 GPT-2 风格权重到 35 课的架构，逐个走参数名映射，生成续写证明加载成功。无网络、无第三方 loader、无黑魔法。
**Time:** ~90 minutes | **时间:** ~90 minutes

## Learning Objectives | 学习目标

- Read a safetensors file with the `safetensors` Python library and inspect the tensor names and shapes.
  中文翻译：Read a safetensors file with the `safetensors` Python library and inspect the tensor names and shapes.
- Map each pretrained parameter name onto a parameter inside the lesson 35 GPT model.
  中文翻译：Map each pretrained parameter name onto a parameter inside the lesson 35 GPT model.
- Handle the two name conventions that differ between published GPT-2 weights and the model in this track: `wte/wpe/h.N.attn.c_attn/c_proj` and `mlp.c_fc/c_proj` versus the locally named `tok_embed/pos_embed/blocks.N.attn.qkv/out_proj` and `mlp.fc1/fc2`.
  中文翻译：Handle the two name conventions that differ between published GPT-2 weights and the model in this track: `wte/wpe/h.N.attn.c_attn/c_proj` and `mlp.c_fc/c_proj` versus the locally named `tok_embed/pos_embed/blocks.N.attn.qkv/out_proj` and `mlp.fc1/fc2`.
- Detect and refuse a shape mismatch with a clear error before any weight assignment happens.
  中文翻译：Detect and refuse a shape mismatch with a clear error before any weight assignment happens.
- Generate a short continuation with the loaded weights and confirm the tokens come from the loaded distribution, not the randomly initialized one.
  中文翻译：Generate a short continuation with the loaded weights and confirm the tokens come from the loaded distribution, not the randomly initialized one.

## The Problem | 问题

> **【中文解读】** 发布的权重不是为你的架构打包的。它们使用原始实现的命名约定。同一参数以三种微妙不同的身份出现（名称、形状、字节布局），加载器必须协调三者。盲目复制会把正确的张量放到错误的位置，得到一个生成垃圾的模型。

> **【拓展：HuggingFace 权重加载生态】** HuggingFace 的 `transformers` 库是权重加载的事实标准，支持 200+ 种模型架构。`from_pretrained()` 自动处理名称映射、形状检查、权重转置和 dtype 转换。`safetensors` 格式（本课使用）比传统 pickle 更安全（不执行任意代码）和更快（零拷贝加载）。GGUF 格式（用于 llama.cpp）支持量化权重，将 7B 模型的内存占用从 14GB 降到 4GB。AutoGPTQ 和 AutoAWQ 提供训练后量化方案。 They carry the names the original implementation used. The pretrained file has `transformer.h.0.attn.c_attn.weight` of shape `(2304, 768)`; your model expects `blocks.0.attn.qkv.weight` of shape `(2304, 768)` (which is the same matrix in a different layout convention) or your model uses `nn.Linear` which stores the matrix transposed. The same parameter shows up with three subtly different identities (name, shape, byte layout) and the loader has to reconcile all three.

A loader that copies blindly puts the right tensor in the wrong place and you get a model that generates nonsense. A loader that refuses to copy when the shape differs but logs nothing leaves you guessing which tensor failed to land. The loader in this lesson is explicit: every assignment is logged, every shape is checked, and a `LoadReport` summarizes hits, misses, and shape mismatches so you can read what happened.

> 一个loader that copies blindly puts the right tensor in the wrong place and you get a model that generates nonsense. A loader that refuses to copy when the shape differs but logs nothing leaves you guessing which tensor failed to land. The loader in this lesson is explicit: every assignment is logged, every shape is checked, and a `LoadReport` summarizes hits, misses, and shape mismatches so you can read what happened.


## The Concept | 概念

```mermaid
flowchart LR
  SF[safetensors file<br/>gpt2-stub.safetensors] --> R[Reader<br/>safe_open]
  R --> N[Parameter name iterator]
  N --> M[Name mapper<br/>pretrained -> local]
  M --> S[Shape check]
  S -- match --> A[Assign tensor<br/>under torch.no_grad]
  S -- mismatch --> E[Log mismatch<br/>do not assign]
  A --> RP[LoadReport]
  E --> RP
  RP --> G[generate<br/>sanity sample]
```

The name mapper is just a function from string to string. The shape check is one if. The assignment happens inside `torch.no_grad()` so autograd does not track the load. The report holds the outcome of every name.

> name mapper is just a function from string to string. The shape check is one if. The assignment happens inside `torch.no_grad()` so autograd does not track the load. The report holds the outcome of every name.


### The GPT-2 naming convention

> **【中文解读】** 发布的 GPT-2 权重使用 `wte`（token 嵌入）、`wpe`（位置嵌入）、`h.N.attn.c_attn`（融合 QKV 线性）等命名。两个关键注意点：(1) `c_attn`、`c_proj`、`c_fc` 等线性层以转置形式存储（相对于 `nn.Linear.weight` 的期望），加载时需要转置；(2) LM head 不在文件中——模型通过 `wte` 的权值绑定获取 head。

Published GPT-2 weights live under names like:

| Pretrained name | Shape | Meaning |
|-----------------|-------|---------|
| `wte.weight` | (50257, 768) | Token embedding |
| `wpe.weight` | (1024, 768) | Position embedding |
| `h.N.ln_1.weight` | (768,) | LayerNorm 1 scale at block N |
| `h.N.ln_1.bias` | (768,) | LayerNorm 1 shift at block N |
| `h.N.attn.c_attn.weight` | (768, 2304) | Fused QKV linear weight |
| `h.N.attn.c_attn.bias` | (2304,) | Fused QKV linear bias |
| `h.N.attn.c_proj.weight` | (768, 768) | Attention output projection |
| `h.N.attn.c_proj.bias` | (768,) | Attention output projection bias |
| `h.N.ln_2.weight` | (768,) | LayerNorm 2 scale |
| `h.N.ln_2.bias` | (768,) | LayerNorm 2 shift |
| `h.N.mlp.c_fc.weight` | (768, 3072) | MLP fc1 weight |
| `h.N.mlp.c_fc.bias` | (3072,) | MLP fc1 bias |
| `h.N.mlp.c_proj.weight` | (3072, 768) | MLP fc2 weight |
| `h.N.mlp.c_proj.bias` | (768,) | MLP fc2 bias |
| `ln_f.weight` | (768,) | Final LayerNorm scale |
| `ln_f.bias` | (768,) | Final LayerNorm shift |

Two surprises to plan for. The `c_attn`, `c_proj`, `c_fc` linears are stored with the matrix transposed relative to what `nn.Linear.weight` expects. The loader transposes during assignment. The LM head is not in the file at all; the model relies on weight tying with `wte`, so the head is set by aliasing once `wte` lands.

> Two surprises to plan for.


### The local naming convention

The model in this track uses descriptive names:

| Local name | Meaning |
|------------|---------|
| `tok_embed.weight` | Token embedding |
| `pos_embed.weight` | Position embedding |
| `blocks.N.ln1.scale` | LayerNorm 1 scale at block N |
| `blocks.N.ln1.shift` | LayerNorm 1 shift |
| `blocks.N.attn.qkv.weight` | Fused QKV |
| `blocks.N.attn.qkv.bias` | Fused QKV bias |
| `blocks.N.attn.out_proj.weight` | Attention output projection |
| `blocks.N.attn.out_proj.bias` | Output projection bias |
| `blocks.N.ln2.scale` | LayerNorm 2 scale |
| `blocks.N.ln2.shift` | LayerNorm 2 shift |
| `blocks.N.mlp.fc1.weight` | MLP fc1 |
| `blocks.N.mlp.fc1.bias` | MLP fc1 bias |
| `blocks.N.mlp.fc2.weight` | MLP fc2 |
| `blocks.N.mlp.fc2.bias` | MLP fc2 bias |
| `final_ln.scale` | Final LayerNorm scale |
| `final_ln.shift` | Final LayerNorm shift |

The mapping is a fixed function. The lesson ships it as a dict that the loader iterates.

> MApping is a fixed function. The lesson ships it as a dict that the loader iterates.（翻译）


### The stub fixture

Real GPT-2 weights are 0.5 GB. The demo does not download them; it generates a small safetensors fixture at first run, with the exact GPT-2 naming convention and shapes appropriate to a 12-block model at d_model 192 instead of 768. The fixture has the right structure to exercise every code path in the loader. Swap the fixture for the real file and the loader works without modification.

> Real GPT-2 weights are 0.


## Build It | 动手构建

> **【中文解读】** 构建权重加载器的核心组件：名称映射函数（将预训练名称转换为本地模型名称）、safetensors 读取器（遍历张量名称、映射、检查形状、转置 conv1d 权重）、LoadReport（记录命中、缺失和形状不匹配）。演示步骤：随机初始化模型 -> 生成续写 -> 加载权重 -> 再次生成 -> 验证两次输出不同。

> **【拓展：权重加载在 LLM 工程中的实际场景】** 实际工程中权重加载远比本课复杂：1）LoRA 权重合并（base_weight + lora_A @ lora_B）；2）量化权重解量化（GPTQ/AWQ 的 scale 和 zero_point）；3）跨框架转换（PyTorch -> GGUF -> ONNX）；4）分片权重合并（Megatron-LM 的 TP 分片需要重新排列）。HuggingFace 的 `transformers` 库有超过 200 个模型的加载脚本，每个都是一组名称映射规则。

`code/main.py` implements:

- A small replica of the lesson 35 `GPTModel` so this lesson is self contained.
  中文翻译：A small replica of the lesson 35 `GPTModel` so this lesson is self contained.
- `make_pretrained_to_local(num_layers)` which expands the per-layer entries.
  中文翻译：`make_pretrained_to_local(num_layers)` which expands the per-layer entries.
- `load_safetensors(model, path)` which iterates names, maps them, checks shape, transposes the conv1d-style weights, and assigns under `torch.no_grad()`. Returns a `LoadReport`.
  中文翻译：`load_safetensors(model, path)` which iterates names, maps them, checks shape, transposes the conv1d-style weights, and assigns under `torch.no_grad()`. Returns a `LoadReport`.
- `make_stub_safetensors(path, cfg)` which generates a fixture file with the exact pretrained naming convention.
  中文翻译：`make_stub_safetensors(path, cfg)` which generates a fixture file with the exact pretrained naming convention.
- A demo that creates `outputs/gpt2-stub.safetensors` on first run, builds a fresh model, captures one generated continuation from random init, loads the stub, captures another continuation, prints both, and verifies the two are different (the load actually changed the model).
  中文翻译：A demo that creates `outputs/gpt2-stub.safetensors` on first run, builds a fresh model, captures one generated continuation from random init, loads the stub, captures another continuation, prints both, and verifies the two are different (the load actually changed the model).

Run it:

```bash
python3 code/main.py
```

Output: the fixture path, a per-name load log, a `LoadReport` summary, a continuation before the load, a continuation after the load, and a shape mismatch on a single intentionally bad tensor injected into the fixture so the failure path is exercised.

> Output: the fixture path, a per-name load log, a `LoadReport` summary, a continuation before the load, a continuation after the load, and a shape mismatch on a single intentionally bad tensor injected into the fixture so the failure path is exercised.


## Stack | 技术栈

- `safetensors` for the on disk format and a streaming reader.
  中文翻译：`safetensors` for the on disk format and a streaming reader.
- `torch` for the model and the assignment math.
  中文翻译：`torch` for the model and the assignment math.
- No `transformers`, no `huggingface_hub`, no network calls.
  中文翻译：No `transformers`, no `huggingface_hub`, no network calls.

## Production patterns in the wild

> **【拓展：跨架构权重迁移】** 加载器的名称映射模式是跨架构迁移的基础。LLaMA 的命名约定（`model.layers.N.self_attn.q_proj.weight`，无 bias，RMSNorm）与 GPT-2 完全不同。Conv1D vs Linear 的转置差异在 GPT-J/GPT-NeoX 中也存在。bitsandbytes 的 8-bit/4-bit 量化加载需要在加载时插入量化包装器。DeepSpeed ZeRO-3 的分片权重需要先 all-gather 再加载。统一的加载模式是：验证 -> 映射 -> 转换 -> 分配。

**Always validate the file before any assignment.** Open the file, list every tensor name with its dtype and shape, run the full mapping with shape checks, and only on success start assigning. Half-loaded models are silent failure machines.

**Log every assignment with the source name and the destination name.** When something looks wrong, the log tells you which tensor landed where; the alternative is reading hexdumps. The `LoadReport` dataclass in this lesson tracks `loaded`, `missing`, `unexpected`, and `shape_mismatch` lists and prints a summary at the end.

**The LM head is a weight tying alias, not a separate copy.** Setting `model.lm_head.weight = model.tok_embed.weight` after loading `tok_embed` is the canonical pattern. Copying the embedding matrix into a fresh `lm_head.weight` parameter breaks tying and quietly doubles your parameter count.

## Use It | 使用方法

- The loader works for any safetensors file that uses the pretrained naming convention. Real GPT-2 files (small / medium / large / xl) work without code changes; only the model config differs.
  中文翻译：The loader works for any safetensors file that uses the pretrained naming convention. Real GPT-2 files (small / medium / large / xl) work without code changes; only the model config differs.
- The same pattern extends to LLaMA, Mistral, Qwen weights once you update the name map. The shape checks and the report stay identical.
  中文翻译：The same pattern extends to LLaMA, Mistral, Qwen weights once you update the name map. The shape checks and the report stay identical.
- Sanity generation after a load is a quick gate: if the post-load samples look like the pre-load samples, the load did not change the model, which means the mapping silently missed every tensor.
  中文翻译：Sanity generation after a load is a quick gate: if the post-load samples look like the pre-load samples, the load did not change the model, which means the mapping silently missed every tensor.

## Exercises | 练习题

1. Add a `dtype` argument to the loader that casts each tensor to a target dtype (`bfloat16`, `float16`, `float32`) during assignment. Confirm a `float32` model can be downcast to `bfloat16` and still generate.
2. Add an `expected_layers` argument that refuses to load a checkpoint whose `h.N` indices do not match the model's `num_layers`.
3. Plug the loader into the lesson 35 generation function and produce two side by side samples: one from random init, one from the loaded fixture.
4. Add an export path: write the current model state into a fresh safetensors file using the pretrained naming convention. Round trip the loader and confirm the report has zero shape mismatches.
5. Extend `NAME_MAP` to handle the LLaMA naming convention (no biases, RMSNorm, fused qkv layout) and re-run the loader on a stub LLaMA fixture you generate.

## Key Terms | 关键术语

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Name map | "Key remapping" | The function from pretrained tensor names to local parameter names; usually a literal dict with one entry per layer index expanded over a loop |
| Shape mismatch | "Bad shape" | The pretrained tensor exists under the mapped name but its dimensions disagree with the local parameter; the loader refuses to assign and logs the pair |
| Transpose-on-load | "Conv1d layout" | Published GPT-2 stores attention and MLP projections in the transpose of what nn.Linear expects; the loader transposes during assignment |
| Weight tying alias | "Shared LM head" | Setting model.lm_head.weight = model.tok_embed.weight so the head and embedding share storage; the head is not in the file because of this |
| Load report | "Coverage summary" | A small dataclass that tracks loaded, missing, unexpected, and shape_mismatch lists; printing it is how you tell whether the load succeeded |

## Further Reading | 延伸阅读

- Phase 19 lesson 35 for the architecture that receives the weights.
  中文翻译：Phase 19 lesson 35 for the architecture that receives the weights.
- Phase 19 lesson 36 for the training loop that produces a checkpoint of the same shape.
  中文翻译：Phase 19 lesson 36 for the training loop that produces a checkpoint of the same shape.
- Phase 10 lesson 11 (quantization) for what to do with the loaded weights when memory is tight.
  中文翻译：Phase 10 lesson 11 (quantization) for what to do with the loaded weights when memory is tight.
- Phase 10 lesson 13 (building a complete LLM pipeline) for the full lifecycle around load and inference.
  中文翻译：Phase 10 lesson 13 (building a complete LLM pipeline) for the full lifecycle around load and inference.
