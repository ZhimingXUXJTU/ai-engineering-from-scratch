# Embodied VLAs: RT-2, OpenVLA, π0, GR00T | 具身 VLA：视觉-语言-动作模型与机器人控制

> The first time a model read a recipe off a website and executed it in a kitchen robot was RT-2 (Google DeepMind, July 2023). RT-2 discretized actions as text tokens, co-fine-tuned a VLM on web data plus robot-action data, and proved that web-scale vision-language knowledge transfers to robotic control. OpenVLA (June 2024) shipped the open 7B reference. Physical Intelligence's π0 series (2024-2025) added flow-matching action experts. NVIDIA's GR00T N1 (March 2025) delivered dual-system (System 1 / System 2) control for humanoid robots at scale. The VLA primitive — vision-language-action, a single model that sees, reads, and acts — is the bridge between this phase's understanding models and the autonomous systems in Phase 15.

> **【中文解读】** RT-2 首次证明网络级视觉语言知识可迁移到机器人控制：将关节动作离散化为文本 token，与 VLM 联合微调。OpenVLA 是开源 7B 参考，π0 引入流匹配动作专家，GR00T N1 实现双系统（快思考/慢思考）人形机器人控制。VLA（视觉-语言-动作）是连接多模态理解和自主系统的桥梁。

> **【拓展：Embodied VLA 到机器人产业】** VLA 模型正在从实验室走向产业：特斯拉 Optimus、Figure 01、1X Technologies 等人形机器人公司都在研发基于 VLA 的控制系统。在工业场景中，VLA 可用于仓储物流机器人、装配线操作机器人等。核心挑战是安全性和可靠性——VLA 的输出是建议而非命令，需要外层控制检查（关节限制、速度限制、工作空间边界）。

**Type:** Learn
**Languages:** Python (stdlib, action tokenizer + VLA inference skeleton)
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 15 (Autonomous Systems, referenced)
**Time:** ~180 minutes

> 🔗 **【前置】** 学本节前请先掌握：Phase 12·05（LLaVA VLM 基础）、Phase 15·01（Agent 循环）、控制理论基础（关节空间、末端执行器位姿）。VLA = VLM 输出从文本变成机器人动作，是 Phase 12 到 Phase 15（自主系统）的桥梁。
> 💡 **【类比】** VLA = "给机器人装大脑和眼睛"。传统机器人 = 程序员写死的 if-else 规则（看到红色就停下）；VLA = 像人一样看图说话做事（"把红色杯子放到桌上"→看到杯子→规划路径→控制关节执行）。RT-2 把动作离散成 token = 把动作当文字写进 prompt；π0 流匹配 = 输出连续动作而非离散 token，更精确。

## Learning Objectives

- Describe action tokenization: discrete bin encoding (RT-2), FAST efficient action tokens, continuous flow-matching actions (π0).
  中文翻译：描述动作分词化：离散 bin 编码（RT-2）、FAST 高效动作 token、连续流匹配动作（π0）。
- Explain why co-fine-tuning on web + robot data preserves general-knowledge transfer to novel tasks.
  中文翻译：解释为什么在网页+机器人数据上联合微调能保留通用知识迁移到新任务的能力。
- Compare OpenVLA (open 7B Llama+VLM), π0 (flow-matching), and GR00T N1 (dual-system) on the same robot task.
  中文翻译：在同一机器人任务上比较 OpenVLA（开放 7B Llama+VLM）、π0（流匹配）和 GR00T N1（双系统）。
- Name the Open X-Embodiment dataset and its role as the RT-X training corpus.
  中文翻译：列举 Open X-Embodiment 数据集及其作为 RT-X 训练语料的角色。

## The Problem | 问题引入

A robot that does chores from natural language instructions has been a research target since the 1970s. The 2020s answer: a vision-language-action (VLA) model. Same VLM architecture used for VQA, but output is actions (joint torques, end-effector poses, discrete commands) instead of text.

> 用自然语言指令让机器人做家务自 1970 年代就是研究目标。2020 年代的答案：视觉-语言-动作（VLA）模型。与 VQA 使用相同的 VLM 架构，但输出是动作（关节力矩、末端执行器位姿、离散命令）而非文本。

Challenges specific to VLAs:

> VLA 特有的挑战：

1. Action spaces are continuous (joint angles, forces) and high-dimensional (7-DOF arm + 3-DOF gripper = 10 dims at 30 Hz).
   中文翻译：动作空间是连续的（关节角度、力）且高维（7 自由度臂 + 3 自由度夹爪 = 30Hz 下 10 维）。
2. Robot-specific training data is scarce. Open X-Embodiment has ~1M trajectories; web text-image is 5B+.
   中文翻译：机器人专用训练数据稀缺。Open X-Embodiment 约 100 万条轨迹；网页文本-图像有 50 亿+。
3. Control frequency matters. 30 Hz control loop means 33ms budget per action.
   中文翻译：控制频率很重要。30Hz 控制回路意味着每个动作 33ms 预算。
4. Safety. A wrong action damages hardware, humans, or property.
   中文翻译：安全性。错误的动作会损坏硬件、伤害人员或财产。

## The Concept | 核心概念

> **【中文解读】** 具身视觉-语言-动作模型（VLA）让机器人理解语言指令和视觉场景后执行物理动作。OpenVLA 是开源 VLA，pi0（Physical Intelligence）和 NVIDIA Groot 是具身智能的代表性模型。VLA = 视觉编码器 + LLM + 动作解码器。

> **【拓展：具身智能的进展** OpenVLA-7B 在 Google Robot 上实现约 80% 的任务成功率。pi0 使用流匹配（flow matching）生成连续动作轨迹，比传统离散动作更平滑。NVIDIA Groot 专注于人形机器人。具身智能的核心挑战是数据稀缺——不像文本和图像，机器人操作数据难以大规模收集。


### Action tokenization (RT-2)

RT-2's trick: represent each joint target as a quantized text token. Discretize the normalized [-1, 1] range into 256 bins, map each bin to a vocabulary ID. A 10-DOF action becomes 10 tokens at each control step.

> RT-2 的技巧：将每个关节目标表示为量化文本 token。将归一化的 [-1, 1] 范围离散化为 256 个 bin，每个 bin 映射到一个词汇 ID。10 自由度动作在每个控制步变成 10 个 token。

Co-fine-tune a PaLM-X VLM on a mixture:

> 在混合数据上联合微调 PaLM-X VLM：

- Web image-text pairs (captioning, VQA).
  中文翻译：网页图文对（描述、VQA）。
- Robot demonstrations, action as tokens.
  中文翻译：机器人演示，动作为 token。

The model sees "pick up the red cube" (language) → image (vision) → 10-token action sequence (discretized joint targets). Web pretraining preserves general-knowledge transfer: RT-2 can follow "move towards the fast-moving object" even though "fast-moving" isn't in training data.

> 模型看到"拿起红色方块"（语言）→ 图像（视觉）→ 10 token 动作序列（离散化关节目标）。网页预训练保留了通用知识迁移：RT-2 能执行"移向快速移动的物体"，即使"快速移动"不在训练数据中。

Inference at 3-5 Hz in the RT-2 paper, limited by VLM autoregressive decode.

> RT-2 论文中推理速度 3-5 Hz，受限于 VLM 自回归解码。

### OpenVLA — the open 7B reference

OpenVLA (Kim et al., June 2024) is the open-weights RT-2 equivalent. 7B Llama backbone, DINOv2 + SigLIP dual vision encoder, action tokenization over 256 bins.

> OpenVLA 是开放权重的 RT-2 等价物。7B Llama 主干，DINOv2 + SigLIP 双视觉编码器，256 bin 动作分词化。

Trained on Open X-Embodiment (970k trajectories across 22 robots). Ships with LoRA fine-tuning support for adapting to new robots.

> 在 Open X-Embodiment 上训练（22 个机器人共 97 万条轨迹）。内置 LoRA 微调支持，适配新机器人。

Inference: 4-5 Hz on an A100 with quantization. Fast enough for slow manipulation, not for high-frequency control.

> 推理：A100 上量化后 4-5 Hz。对慢速操作足够，不适合高频控制。

### FAST tokenizer — faster action decode

Pertsch et al. (2024) showed that discrete-bin tokenization is inefficient — most actions cluster in a small region of bin-space. FAST (Frequency-domain Action Sequence Tokenizer) compresses action sequences via DCT and quantizes the coefficients.

> Pertsch 等人（2024）表明离散 bin 分词化效率低——大多数动作聚集在 bin 空间的小区域。FAST（频域动作序列分词器）通过 DCT 压缩动作序列并量化系数。

A 30-step action trajectory becomes ~10 FAST tokens instead of 300 discrete-bin tokens. Inference speeds up 3-5x without quality loss.

> 30 步动作轨迹变成约 10 个 FAST token，而非 300 个离散 bin token。推理速度提升 3-5 倍，质量无损。

### π0 and flow-matching actions

Physical Intelligence's π0 (Black et al., October 2024) replaces discrete action tokens with a flow-matching action expert:

> Physical Intelligence 的 π0 用流匹配动作专家替代离散动作 token：

- A small action transformer reads the VLM's hidden states and outputs a continuous 50-step action sequence via rectified flow.
  中文翻译：小型动作 Transformer 读取 VLM 隐藏状态，通过矫正流输出连续的 50 步动作序列。
- The action head trains with flow-matching loss; VLM pretraining stays unchanged.
  中文翻译：动作头用流匹配损失训练；VLM 预训练不变。
- Inference: full action sequence emitted in ~5 denoising steps, effectively 50 Hz control.
  中文翻译：推理：完整动作序列在约 5 步去噪中输出，等效 50Hz 控制。

π0's claim: beats OpenVLA and Octo on a wide suite of manipulation tasks. The continuous-action formulation preserves smoothness that discretization destroys.

> π0 声称：在广泛的操作任务上击败 OpenVLA 和 Octo。连续动作表达保留了离散化会破坏的动作平滑性。

> **【中文解读】** π0 用流匹配替代离散动作 token：一个小的动作 Transformer 读取 VLM 隐藏状态，通过矫正流输出连续的 50 步动作序列。推理时仅需约 5 步去噪，实现等效 50Hz 控制频率。连续动作表达保留了离散化会破坏的动作平滑性。

π0.5 and π0-FAST are incremental upgrades. π0-FAST combines FAST tokenization with flow matching.

> π0.5 和 π0-FAST 是增量升级。π0-FAST 结合了 FAST 分词化和流匹配。

### GR00T N1 — dual-system for humanoids

NVIDIA's GR00T N1 (March 2025) is built for humanoid robots (>30 DOF, full-body):

> NVIDIA 的 GR00T N1 为人形机器人设计（>30 自由度，全身）：

- System 2: a large VLM reading scene + instruction, producing high-level subgoals at ~1 Hz.
  中文翻译：系统 2：大型 VLM 读取场景+指令，以约 1Hz 生成高层子目标。
- System 1: a small action-head transformer producing low-level 50-100 Hz joint commands conditioned on the subgoals.
  中文翻译：系统 1：小型动作头 Transformer 根据子目标生成底层 50-100Hz 关节命令。

The split maps to Kahneman's fast-and-slow thinking: System 2 plans, System 1 acts. Benefits: slow VLM-sized planning does not block fast control; System 1 stays small for latency.

> 这种分离映射到卡尼曼的快慢思考：系统 2 规划，系统 1 执行。优势：慢速 VLM 级规划不会阻塞快速控制；系统 1 保持小规模以保证低延迟。

GR00T N1.7 (late 2025) improves data scaling. GR00T fine-tunes with sim-to-real data from Omniverse.

> GR00T N1.7（2025 年末）改进了数据扩展。GR00T 用 Omniverse 的仿真到真实数据进行微调。

### Open X-Embodiment

The training data. RT-X (October 2023) assembled 22 datasets covering 1M trajectories across 22 robots. Open X-Embodiment is the corpus everyone uses:

> 训练数据。RT-X（2023 年 10 月）整合了 22 个数据集，覆盖 22 个机器人的 100 万条轨迹。Open X-Embodiment 是所有人使用的语料：

- ALOHA / Bridge V2 / Droid / RT-2 Kitchen / Language Table.
  中文翻译：ALOHA / Bridge V2 / Droid / RT-2 Kitchen / Language Table。
- Each sample: (robot state, camera views, instruction, action sequence).
  中文翻译：每个样本：（机器人状态、摄像头视图、指令、动作序列）。
- Training hygiene: unify action space, normalize joint ranges, resize cameras.
  中文翻译：训练规范：统一动作空间、归一化关节范围、统一摄像头分辨率。

OpenVLA and π0 train on Open X-Embodiment. Domain gap to any specific robot is closed by LoRA fine-tuning on 100-1000 task-specific demos.

> OpenVLA 和 π0 在 Open X-Embodiment 上训练。与特定机器人的领域差距通过 100-1000 个任务特定演示的 LoRA 微调来弥合。

### Co-fine-tuning vs robot-only

Co-fine-tuning mixes web VQA data with robot trajectories. The ratio matters: too much VQA and the model forgets actions; too much robot data and the model loses general knowledge.

> 联合微调将网页 VQA 数据与机器人轨迹混合。比例很重要：VQA 太多模型忘记动作；机器人数据太多模型失去通用知识。

RT-2's ratio: ~1:1. OpenVLA: ~0.5:1 web-to-robot. π0: similar. The precise ratio is a hyperparameter to tune per dataset size.

> RT-2 的比例约 1:1。OpenVLA 约 0.5:1（网页:机器人）。π0 类似。精确比例是按数据集大小调节的超参数。

Robot-only training produces task-specific models that fail on out-of-distribution instructions. Co-fine-tuning is the difference between "pick up the red cube (in demo)" and "pick up the third largest object from the left (novel phrasing)."

> 仅用机器人训练产生任务特定模型，在分布外指令上失败。联合微调是"拿起红色方块（演示中的）"和"拿起从左数第三个最大的物体（新表述）"之间的区别。

### Safety and action limits

Every production VLA ships with:

> 每个生产级 VLA 都配备：

- Hard joint limits (can't torque past spec).
  中文翻译：硬性关节限制（不能超过规格的力矩）。
- Velocity limits (soft clipping).
  中文翻译：速度限制（软截断）。
- Workspace bounds (end-effector cannot leave the table).
  中文翻译：工作空间边界（末端执行器不能离开桌面）。
- Human-in-the-loop approval for novel tasks.
  中文翻译：新任务的人工审批。

These sit outside the VLA as control-layer checks. The VLA's output is a suggestion, not a command.

> 这些位于 VLA 之外的控制层检查。VLA 的输出是建议，不是命令。

## Use It | 用框架实现

`code/main.py`:

- Implements 256-bin action tokenization and de-tokenization.
  中文翻译：实现 256 bin 动作分词化和反分词化。
- Sketches a FAST tokenizer based on DCT + quantization.
  中文翻译：基于 DCT + 量化勾勒 FAST 分词器。
- Compares token-count per action step across (discrete-bin, FAST, continuous-flow).
  中文翻译：比较离散 bin、FAST、连续流三种方式的每步 token 数。
- Prints a lineage summary of RT-2 → OpenVLA → π0 → GR00T.
  中文翻译：打印 RT-2 → OpenVLA → π0 → GR00T 的谱系摘要。

## Ship It | 产出物

This lesson produces `outputs/skill-vla-action-format-picker.md`. Given a robot task (manipulation, navigation, humanoid whole-body), picks between discrete-bin + RT-2, FAST + OpenVLA, flow-matching + π0, or dual-system + GR00T.

> 本课产出 `outputs/skill-vla-action-format-picker.md`。给定机器人任务（操作、导航、人形全身），在离散 bin+RT-2、FAST+OpenVLA、流匹配+π0 或双系统+GR00T 之间选择。

## Exercises | 练习题

1. A 10-DOF arm at 30 Hz control rate. Discrete-bin tokenization at 256 bins emits how many tokens per second? Can a 7B VLM keep up? 10 自由度机械臂，30Hz 控制频率，256 离散 bin。每秒产生多少 token？7B VLM 能跟上吗？

2. FAST tokenization compresses 30-step trajectories to ~10 tokens. What does the user lose if the trajectory has high-frequency motion (e.g., drumming)? FAST 将 30 步轨迹压缩为约 10 token。如果轨迹包含高频运动（如击鼓），会丢失什么？

3. π0's flow-matching head denoises in ~5 steps. Compare throughput to OpenVLA's autoregressive decode at 4-5 Hz. π0 的流匹配头在约 5 步去噪。对比 OpenVLA 4-5 Hz 自回归解码的吞吐量。

4. GR00T's System 1 / System 2 split maps to Kahneman. Propose a different split (System 3?) that might help bipedal walking. GR00T 的系统1/系统2分离对应卡尼曼理论。提出一个不同的分离方案（系统3？）来帮助双足行走。

5. Read Open X-Embodiment Section 4 on dataset curation. Name the three curation rules that prevent domain leakage. 阅读 Open X-Embodiment 第 4 节关于数据集管理的部分。列举防止领域泄漏的三条规则。

## Key Terms | 术语速查表

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| VLA | "Vision-language-action" 视觉-语言-动作模型 | Model that takes image + instruction and outputs action commands 接受图像+指令并输出动作命令的模型 | |
| Action tokenization | "Discrete bins" 离散 bin 编码 | Quantize continuous joint targets into 256 bins per dim, each a vocab ID 将连续关节目标量化为每维 256 个 bin，每个 bin 对应一个词表 ID | |
| FAST tokenizer | "Frequency action tokens" 频域动作 token | DCT + quantize to compress 30-step trajectories to ~10 tokens 用 DCT + 量化将 30 步轨迹压缩为约 10 个 token | |
| Co-fine-tune | "Mix web + robot" 混合微调 | Train on web VQA data alongside robot demos to preserve general knowledge 在网络 VQA 数据和机器人演示上联合训练以保留通用知识 | |
| Flow-matching action head | "pi0 continuous output" 流匹配动作头 | Small transformer that outputs a 50-step action sequence via rectified flow 通过矫正流输出 50 步连续动作序列的小型 Transformer | |
| System 1 / System 2 | "Dual-system control" 双系统控制 | Large VLM plans slowly, small action head acts quickly; GR00T pattern 大 VLM 慢规划，小动作头快执行；GR00T 模式 | |
| Open X-Embodiment | "RT-X dataset" 开放具身数据集 | 1M-trajectory cross-robot dataset; the training corpus 100 万轨迹跨机器人数据集；标准训练语料 | |

## Further Reading | 延伸阅读

- [Brohan et al. — RT-2 (arXiv:2307.15818)](https://arxiv.org/abs/2307.15818)
- [Kim et al. — OpenVLA (arXiv:2406.09246)](https://arxiv.org/abs/2406.09246)
- [Black et al. — π0 (arXiv:2410.24164)](https://arxiv.org/abs/2410.24164)
- [NVIDIA — GR00T N1 (arXiv:2503.14734)](https://arxiv.org/abs/2503.14734)
- [Open X-Embodiment Collab — RT-X (arXiv:2310.08864)](https://arxiv.org/abs/2310.08864)
