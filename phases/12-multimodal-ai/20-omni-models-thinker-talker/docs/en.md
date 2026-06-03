# Omni Models: Qwen2.5-Omni and the Thinker-Talker Split | 全能模型：Qwen2.5-Omni 与 Thinker-Talker 分离架构

> GPT-4o's product demo in May 2024 was disruptive not because of the underlying model but because of the product shape — a voice interface where you talk, the model sees what the camera sees, and it talks back in under 250ms. The open ecosystem spent the rest of 2024 and 2025 racing to reach that product surface. Qwen2.5-Omni (March 2025) is the reference open design: a Thinker (large text-generating transformer) plus a Talker (parallel speech-generating transformer), linked by streaming speech tokens. Mini-Omni simplified it, Moshi matched its latency, GLM-4-Voice extended it to Chinese. This lesson reads the Thinker-Talker architecture and the latency budget that makes streaming real-time dialogue work.

> **【中文解读】** GPT-4o 的突破不在于底层模型，而在于产品形态——250ms 内的语音交互体验。Qwen2.5-Omni 是开源世界的参考设计：Thinker（大型文本生成 Transformer）负责推理"说什么"，Talker（小型语音生成 Transformer）负责并行生成语音 token。两者通过流式 token 连接，实现实时对话。

**Type:** Build
**Languages:** Python (stdlib, streaming pipeline latency simulator + VAD loop)
**Prerequisites:** Phase 12 · 19 (audio-LLMs), Phase 12 · 16 (any-to-any)
**Time:** ~180 minutes

## Learning Objectives

- Split the inference pipeline into Thinker (text reasoning) and Talker (speech synthesis) and explain why parallel streaming works.
- Compute the time-to-first-audio-byte (TTFAB) budget for a conversational interaction, component by component.
- Describe TMRoPE's time-aligned position encoding across vision, audio, and text within the Thinker.
- Name the three real-time conversational patterns: half-duplex, turn-taking, full-duplex.

## The Problem

A real-time voice assistant has to do a lot, fast:

1. Hear the user. Real-time speech tokenization, voice activity detection (VAD) to know when they're done speaking.
2. Optionally see. Camera input at 2-4 FPS, streamed into the Thinker alongside audio.
3. Think. Compose a response conditioned on the conversation history.
4. Speak. Synthesize audio tokens, decode to waveform, stream to the user's speakers.

Each step adds latency. Conversational-feel requires total round-trip < 500ms — below that, the user stops noticing the lag. GPT-4o claims ~250ms. Moshi ~160ms. Qwen2.5-Omni ~350-500ms.

Every component needs to stream. Nothing can be "batch everything then decode."

## The Concept

### Thinker and Talker

Qwen2.5-Omni's decomposition:

- Thinker: a 7B-80B text-generating transformer. Consumes interleaved text + image + audio tokens. Outputs text tokens representing what to say.
- Talker: a smaller speech-generating transformer (200M-1B). Consumes Thinker's text output tokens plus recent speech-context tokens. Outputs discrete speech tokens (residual-VQ indices).
- Speech decoder: a streaming waveform decoder (SNAC, MoVQGAN family) that takes speech tokens to audio samples in real time.

The separation matters. Thinker has to be big for good reasoning. Talker can be small because its job is local — convert text to speech tokens. Bigger Talker is not more expressive; it's slower.

Running both in parallel:

1. Thinker emits text token t_i.
2. Talker consumes t_i (via streaming) and emits speech tokens s_i, s_{i+1}, ..., s_{i+k}.
3. Speech decoder consumes speech tokens as they come and emits audio samples.
4. By the time Thinker is at text token t_{i+3}, Talker has already streamed audio for t_0..t_{i+2}.

> **【中文解读】** Thinker 必须大（7B-80B）才能做好推理，Talker 可以小（200M-1B）因为它的任务是局部的——文本转语音 token。更大的 Talker 不会更有表现力，只会更慢。并行运行时，当 Thinker 在生成第 i+3 个文本 token 时，Talker 已经在播放第 0 到 i+2 个文本对应的音频了。

> **【拓展：Token 速率数学】** 16kHz 语音用 50Hz 基础语音 token，意味着每秒需要 50 个语音 token。Talker 每秒必须输出 >= 50 token 才能跟上。在 H100 上，200-300M 的 Talker 每秒可输出数百 token，远超需求；但 7B Talker 会跟不上。这就是为什么需要专用的小 Talker 模型而非直接用主模型。

### TMRoPE — time-aligned multimodal positions

Thinker needs to integrate image frames (arriving at, say, 4 FPS), audio frames (arriving at 50 frames/second), and text from conversation history. A naive sequence order (all images, then all audio, then text) loses temporal alignment.

TMRoPE assigns absolute timestamps to every token. Vision token at t=2.3s. Audio token at t=2.32s. Text token from the user "stop" at t=2.35s. RoPE rotates attention by timestamp; the model sees them as temporally concurrent.

This is the infrastructure for "he waved while saying hello" to work — the model sees the video frame and the audio at the same conceptual moment.

### Streaming speech synthesis

Speech tokens must stream. Mini-Omni (Xie & Wu, 2024) introduced "language models can hear, talk while thinking in streaming": Thinker output tokens and Talker output tokens interleave in the same sequence. Talker fires as soon as Thinker commits the next text token. No batch boundaries.

Moshi (Défossez et al., October 2024) is the fastest open implementation. 160ms TTFAB on a single A100. Architecture: a single 7B transformer that emits text and speech tokens on alternating positions, with an "inner monologue" that separates the thinking stream from the speaking stream. This is effectively Thinker + Talker fused into one model with careful training.

### VAD and turn-taking

Voice activity detection runs on the input side. Two patterns:

- Half-duplex: user speaks, model listens. Model speaks, user listens. Clear handoff via VAD silence detection (~200ms).
- Full-duplex: both can speak simultaneously. Model can backchannel ("uh-huh") or interrupt. Much harder. Moshi supports this.

Qwen2.5-Omni supports half-duplex by default, with turn-taking via silence threshold. Full-duplex requires application-layer handling.

### Qwen3-Omni (November 2025)

The successor. Qwen3-80B Thinker, larger Talker, improved TMRoPE-v2. Latency close to GPT-4o's 250ms. Open weights. Benchmarks on OmniBench competitive with Gemini 2.0 Live.

### Production latency budget

For a typical streaming interaction:

- Mic -> audio tokens: 40-80ms.
- Prefill (prompt + history): 100-200ms at 7B, much more at 70B.
- First Thinker text token: 40ms.
- Talker processes first text token: 20ms.
- First speech tokens commit: 40ms.
- Residual-VQ decode: 30ms.
- Speech waveform decode: 50-80ms.

Total TTFAB: 320-510ms at 7B, 600-900ms at 70B. Frontier quality usually means 70B+; hence the frontier latency gap.

### Token-rate math

At 16kHz speech with 50 Hz base speech tokens, you need 50 speech tokens per second of output. Talker must emit ≥50 tok/s to keep up. At a typical LLM throughput of 30-80 tok/s on an H100, a small (200-300M) Talker is fast enough; a 7B Talker would fall behind.

This is why small dedicated Talker models exist rather than "just use the main model."

## Use It

`code/main.py`:

- Simulates a Thinker-Talker pipeline with mock token-emission rates.
- Computes TTFAB for configurable model sizes and mic sample rates.
- Demonstrates half-duplex turn-taking with VAD silence threshold.

## Ship It

This lesson produces `outputs/skill-omni-streaming-budget.md`. Given a real-time voice product's target TTFAB and feature set (vision-in, bilingual, full-duplex), picks Qwen2.5-Omni, Qwen3-Omni, Moshi, or Mini-Omni and sizes the Thinker/Talker.

## Exercises

1. Your target TTFAB is 300ms. On a 7B Thinker and 300M Talker, write out every component's latency. 你的 TTFAB 目标是 300ms。在 7B Thinker 和 300M Talker 上，列出每个组件的延迟。

2. Qwen2.5-Omni uses TMRoPE. Describe what the model sees for a prompt where the user starts speaking at t=1s and the camera catches a gesture at t=1.2s. Qwen2.5-Omni 使用 TMRoPE。描述模型在用户 t=1s 开始说话、摄像头 t=1.2s 捕获手势时看到的输入。

3. Full-duplex support requires the model to emit audio while listening. Propose a training data format that teaches this. 全双工支持要求模型在监听时同时输出音频。设计一个训练数据格式来教授这种能力。

4. Read Moshi's paper Section 4. Describe the "inner monologue" separation and why it avoids the Thinker-Talker split. 阅读 Moshi 论文第 4 节，描述"内心独白"分离机制及为何它避免了 Thinker-Talker 分离。

5. Compute the throughput budget: how fast must a Talker emit tokens to keep up with 16kHz speech at 50 base-layer tokens/sec? 计算吞吐量预算：Talker 需要多快的速度输出 token 才能跟上 16kHz 语音（50 基础层 token/秒）？

## Key Terms

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| Thinker | "Reasoning brain" 思考者 | Large text-generating transformer producing what to say 生成"说什么"的大型文本生成 Transformer |
| Talker | "Speech-generating mouth" 说话者 | Small transformer producing discrete speech tokens from Thinker's text 将 Thinker 文本转为语音 token 的小型 Transformer |
| TTFAB | "Latency budget" 首音频字节延迟 | Time-to-first-audio-byte: from user speech end to first audio sample out 从用户说话结束到首个音频样本输出的延迟 |
| TMRoPE | "Time-aligned RoPE" 时间对齐旋转位置编码 | Position encoding using absolute timestamps across vision, audio, text 跨视觉、音频、文本使用绝对时间戳的位置编码 |
| Half-duplex | "Turn-taking" 半双工 | User and model alternate; VAD silence detects user-done 用户和模型交替说话；VAD 静音检测用户说完 |
| Full-duplex | "Simultaneous" 全双工 | Model can speak and listen at the same time; backchannel capable 模型可同时说话和监听；支持回话 |
| Inner monologue | "Moshi separation" 内心独白 | Single-model design where thinking-stream and speaking-stream interleave 单模型设计，思考流和说话流交替出现 |

## Further Reading

- [Xu et al. — Qwen2.5-Omni (arXiv:2503.20215)](https://arxiv.org/abs/2503.20215)
- [Qwen Team — Qwen3-Omni (arXiv:2509.17765)](https://arxiv.org/html/2509.17765v1)
- [Xie & Wu — Mini-Omni (arXiv:2408.16725)](https://arxiv.org/abs/2408.16725)
- [Défossez et al. — Moshi (arXiv:2410.00037)](https://arxiv.org/abs/2410.00037)
- [Zeng et al. — GLM-4-Voice (arXiv:2412.02612)](https://arxiv.org/abs/2412.02612)
