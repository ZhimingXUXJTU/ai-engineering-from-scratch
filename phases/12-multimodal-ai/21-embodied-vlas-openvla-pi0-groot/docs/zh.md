# Embodied VLAs: RT-2, OpenVLA, π0, GR00T | 具身 VLA：视觉-语言-动作模型与机器人控制

> The first time a model read a recipe off a website and executed it in a kitchen robot was RT-2 (Google DeepMind, July 2023). RT-2 discretized actions as text tokens, co-fine-tuned a VLM on web data plus robot-action data, and proved that web-scale vision-language knowledge transfers to robotic control. OpenVLA (June 2024) shipped the open 7B reference. Physical Intelligence's π0 series (2024-2025) added flow-matching action experts. NVIDIA's GR00T N1 (March 2025) delivered dual-system (System 1 / System 2) control for humanoid robots at scale. The VLA primitive — vision-language-action, a single model that sees, reads, and acts — is the bridge between this phase's understanding models and the autonomous systems in Phase 15.

> **【中文解读】** RT-2 首次证明网络级视觉语言知识可迁移到机器人控制：将关节动作离散化为文本 token，与 VLM 联合微调。OpenVLA 是开源 7B 参考，π0 引入流匹配动作专家，GR00T N1 实现双系统（快思考/慢思考）人形机器人控制。VLA（视觉-语言-动作）是连接多模态理解和自主系统的桥梁。

> **【拓展：Embodied VLA 到机器人产业】** VLA 模型正在从实验室走向产业：特斯拉 Optimus、Figure 01、1X Technologies 等人形机器人公司都在研发基于 VLA 的控制系统。在工业场景中，VLA 可用于仓储物流机器人、装配线操作机器人等。核心挑战是安全性和可靠性——VLA 的输出是建议而非命令，需要外层控制检查（关节限制、速度限制、工作空间边界）。

**Type:** Learn
**Languages:** Python (stdlib, action tokenizer + VLA inference skeleton)
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 15 (Autonomous Systems, referenced)
**Time:** ~180 minutes

## 学习目标

- Describe action tokenization: discrete bin encoding (RT-2), FAST efficient action tokens, continuous flow-matching actions (π0).
- Explain why co-fine-tuning on web + robot data preserves general-knowledge transfer to novel tasks.
- Compare OpenVLA (open 7B Llama+VLM), π0 (flow-matching), and GR00T N1 (dual-system) on the same robot task.
- Name the Open X-Embodiment dataset and its role as the RT-X training corpus.

## 问题引入

A robot that does chores from natural language instructions has been a research target since the 1970s. The 2020s answer: a vision-language-action (VLA) model. Same VLM architecture used for VQA, but output is actions (joint torques, end-effector poses, discrete commands) instead of text.

Challenges specific to VLAs:

1. Action spaces are continuous (joint angles, forces) and high-dimensional (7-DOF arm + 3-DOF gripper = 10 dims at 30 Hz).
2. Robot-specific training data is scarce. Open X-Embodiment has ~1M trajectories; web text-image is 5B+.
3. Control frequency matters. 30 Hz control loop means 33ms budget per action.
4. Safety. A wrong action damages hardware, humans, or property.

## 核心概念

> **【中文解读】** 具身视觉-语言-动作模型（VLA）让机器人理解语言指令和视觉场景后执行物理动作。OpenVLA 是开源 VLA，pi0（Physical Intelligence）和 NVIDIA Groot 是具身智能的代表性模型。VLA = 视觉编码器 + LLM + 动作解码器。

> **【拓展：具身智能的进展** OpenVLA-7B 在 Google Robot 上实现约 80% 的任务成功率。pi0 使用流匹配（flow matching）生成连续动作轨迹，比传统离散动作更平滑。NVIDIA Groot 专注于人形机器人。具身智能的核心挑战是数据稀缺——不像文本和图像，机器人操作数据难以大规模收集。


### Action tokenization (RT-2)

RT-2's trick: represent each joint target as a quantized text token. Discretize the normalized [-1, 1] range into 256 bins, map each bin to a vocabulary ID. A 10-DOF action becomes 10 tokens at each control step.

Co-fine-tune a PaLM-X VLM on a mixture:

- Web image-text pairs (captioning, VQA).
- Robot demonstrations, action as tokens.

The model sees "pick up the red cube" (language) → image (vision) → 10-token action sequence (discretized joint targets). Web pretraining preserves general-knowledge transfer: RT-2 can follow "move towards the fast-moving object" even though "fast-moving" isn't in training data.

Inference at 3-5 Hz in the RT-2 paper, limited by VLM autoregressive decode.

### OpenVLA — the open 7B reference

OpenVLA (Kim et al., June 2024) is the open-weights RT-2 equivalent. 7B Llama backbone, DINOv2 + SigLIP dual vision encoder, action tokenization over 256 bins.

Trained on Open X-Embodiment (970k trajectories across 22 robots). Ships with LoRA fine-tuning support for adapting to new robots.

Inference: 4-5 Hz on an A100 with quantization. Fast enough for slow manipulation, not for high-frequency control.

### FAST tokenizer — faster action decode

Pertsch et al. (2024) showed that discrete-bin tokenization is inefficient — most actions cluster in a small region of bin-space. FAST (Frequency-domain Action Sequence Tokenizer) compresses action sequences via DCT and quantizes the coefficients.

A 30-step action trajectory becomes ~10 FAST tokens instead of 300 discrete-bin tokens. Inference speeds up 3-5x without quality loss.

### π0 and flow-matching actions

Physical Intelligence's π0 (Black et al., October 2024) replaces discrete action tokens with a flow-matching action expert:

- A small action transformer reads the VLM's hidden states and outputs a continuous 50-step action sequence via rectified flow.
- The action head trains with flow-matching loss; VLM pretraining stays unchanged.
- Inference: full action sequence emitted in ~5 denoising steps, effectively 50 Hz control.

π0's claim: beats OpenVLA and Octo on a wide suite of manipulation tasks. The continuous-action formulation preserves smoothness that discretization destroys.

> **【中文解读】** π0 用流匹配替代离散动作 token：一个小的动作 Transformer 读取 VLM 隐藏状态，通过矫正流输出连续的 50 步动作序列。推理时仅需约 5 步去噪，实现等效 50Hz 控制频率。连续动作表达保留了离散化会破坏的动作平滑性。

π0.5 and π0-FAST are incremental upgrades. π0-FAST combines FAST tokenization with flow matching.

### GR00T N1 — dual-system for humanoids

NVIDIA's GR00T N1 (March 2025) is built for humanoid robots (>30 DOF, full-body):

- System 2: a large VLM reading scene + instruction, producing high-level subgoals at ~1 Hz.
- System 1: a small action-head transformer producing low-level 50-100 Hz joint commands conditioned on the subgoals.

The split maps to Kahneman's fast-and-slow thinking: System 2 plans, System 1 acts. Benefits: slow VLM-sized planning does not block fast control; System 1 stays small for latency.

GR00T N1.7 (late 2025) improves data scaling. GR00T fine-tunes with sim-to-real data from Omniverse.

### Open X-Embodiment

The training data. RT-X (October 2023) assembled 22 datasets covering 1M trajectories across 22 robots. Open X-Embodiment is the corpus everyone uses:

- ALOHA / Bridge V2 / Droid / RT-2 Kitchen / Language Table.
- Each sample: (robot state, camera views, instruction, action sequence).
- Training hygiene: unify action space, normalize joint ranges, resize cameras.

OpenVLA and π0 train on Open X-Embodiment. Domain gap to any specific robot is closed by LoRA fine-tuning on 100-1000 task-specific demos.

### Co-fine-tuning vs robot-only

Co-fine-tuning mixes web VQA data with robot trajectories. The ratio matters: too much VQA and the model forgets actions; too much robot data and the model loses general knowledge.

RT-2's ratio: ~1:1. OpenVLA: ~0.5:1 web-to-robot. π0: similar. The precise ratio is a hyperparameter to tune per dataset size.

Robot-only training produces task-specific models that fail on out-of-distribution instructions. Co-fine-tuning is the difference between "pick up the red cube (in demo)" and "pick up the third largest object from the left (novel phrasing)."

### Safety and action limits

Every production VLA ships with:

- Hard joint limits (can't torque past spec).
- Velocity limits (soft clipping).
- Workspace bounds (end-effector cannot leave the table).
- Human-in-the-loop approval for novel tasks.

These sit outside the VLA as control-layer checks. The VLA's output is a suggestion, not a command.

## 用框架实现

`code/main.py`:

- Implements 256-bin action tokenization and de-tokenization.
- Sketches a FAST tokenizer based on DCT + quantization.
- Compares token-count per action step across (discrete-bin, FAST, continuous-flow).
- Prints a lineage summary of RT-2 → OpenVLA → π0 → GR00T.

## 产出物

This lesson produces `outputs/skill-vla-action-format-picker.md`. Given a robot task (manipulation, navigation, humanoid whole-body), picks between discrete-bin + RT-2, FAST + OpenVLA, flow-matching + π0, or dual-system + GR00T.

## 练习题

1. A 10-DOF arm at 30 Hz control rate. Discrete-bin tokenization at 256 bins emits how many tokens per second? Can a 7B VLM keep up? 10 自由度机械臂，30Hz 控制频率，256 离散 bin。每秒产生多少 token？7B VLM 能跟上吗？

2. FAST tokenization compresses 30-step trajectories to ~10 tokens. What does the user lose if the trajectory has high-frequency motion (e.g., drumming)? FAST 将 30 步轨迹压缩为约 10 token。如果轨迹包含高频运动（如击鼓），会丢失什么？

3. π0's flow-matching head denoises in ~5 steps. Compare throughput to OpenVLA's autoregressive decode at 4-5 Hz. π0 的流匹配头在约 5 步去噪。对比 OpenVLA 4-5 Hz 自回归解码的吞吐量。

4. GR00T's System 1 / System 2 split maps to Kahneman. Propose a different split (System 3?) that might help bipedal walking. GR00T 的系统1/系统2分离对应卡尼曼理论。提出一个不同的分离方案（系统3？）来帮助双足行走。

5. Read Open X-Embodiment Section 4 on dataset curation. Name the three curation rules that prevent domain leakage. 阅读 Open X-Embodiment 第 4 节关于数据集管理的部分。列举防止领域泄漏的三条规则。

## 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| VLA | "Vision-language-action" 视觉-语言-动作模型 | Model that takes image + instruction and outputs action commands 接受图像+指令并输出动作命令的模型 | |
| Action tokenization | "Discrete bins" 离散 bin 编码 | Quantize continuous joint targets into 256 bins per dim, each a vocab ID 将连续关节目标量化为每维 256 个 bin，每个 bin 对应一个词表 ID | |
| FAST tokenizer | "Frequency action tokens" 频域动作 token | DCT + quantize to compress 30-step trajectories to ~10 tokens 用 DCT + 量化将 30 步轨迹压缩为约 10 个 token | |
| Co-fine-tune | "Mix web + robot" 混合微调 | Train on web VQA data alongside robot demos to preserve general knowledge 在网络 VQA 数据和机器人演示上联合训练以保留通用知识 | |
| Flow-matching action head | "pi0 continuous output" 流匹配动作头 | Small transformer that outputs a 50-step action sequence via rectified flow 通过矫正流输出 50 步连续动作序列的小型 Transformer | |
| System 1 / System 2 | "Dual-system control" 双系统控制 | Large VLM plans slowly, small action head acts quickly; GR00T pattern 大 VLM 慢规划，小动作头快执行；GR00T 模式 | |
| Open X-Embodiment | "RT-X dataset" 开放具身数据集 | 1M-trajectory cross-robot dataset; the training corpus 100 万轨迹跨机器人数据集；标准训练语料 | |

## 延伸阅读

- [Brohan et al. — RT-2 (arXiv:2307.15818)](https://arxiv.org/abs/2307.15818)
- [Kim et al. — OpenVLA (arXiv:2406.09246)](https://arxiv.org/abs/2406.09246)
- [Black et al. — π0 (arXiv:2410.24164)](https://arxiv.org/abs/2410.24164)
- [NVIDIA — GR00T N1 (arXiv:2503.14734)](https://arxiv.org/abs/2503.14734)
- [Open X-Embodiment Collab — RT-X (arXiv:2310.08864)](https://arxiv.org/abs/2310.08864)
