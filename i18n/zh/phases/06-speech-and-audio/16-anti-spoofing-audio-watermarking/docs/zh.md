# 语音防伪与音频水印

> 语音克隆的运输速度比防御更快. 2026 年生产语音系统需要两件事:一个检测器 (AASIST,RawNet2) 将真实与假语音分类,以及一个能够存活压缩和编辑的水印 (AudioSeal).

> **【中文解读】**语音克隆技术在防线前面运行――2026年生产级语音系统需要两样东西:检测器:AASIST、RawNet2) 区分真假语音,水印(AudioSeal) 在压缩和编辑后仍然可以活着――不做这两件事就不需要上线语音克隆功能――

**Type:** Build | **类型:** 构建
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 6 · 06 (Speaker Recognition), Phase 6 · 08 (Voice Cloning) | **前置知识:** 阶段 6 · 06（说话人识别），阶段 6 · 08（语音克隆）
**Time:** ~75 minutes | **预计用时:** ~75 分钟

## 问题 问题引入

相关的三种防御:

> 三种相关防御手段:

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――


1. **Anti-spoofing / deepfake detection.**根据音频剪辑,它是合成还是真实的?ASVspoof基准 (ASVspoof 2019 → 2021 → 5) 是黄金标准.
   翻译: 中文**反欺骗/深度伪造检测。**给定一段音频,判断它是合成的还是真实的?ASVspoof 基准测试(ASVspoof 2019 → 2021 → 5) 是黄金标准──
2. **Audio watermarking.**嵌入一个不知晓的信号在生成的音频中,一个探测器可以稍后提取.
   翻译: 中文**音频水印。**在生成的音频中嵌入不可知信号,检测器后可以提取──AudioSeal(Meta) 和WavMark是开源选项──
3. **Authenticated provenance.**编码音频文件+元数据.C2PA/内容认证倡议.
   翻译: 中文**认证来源。**音频文件 + 元数据的加密签名──C2PA / 内容真实性倡议──

检测处理不合作的对手.水标处理合规性 人工智能生成的音频应该被识别为这样.两者都需要在2026年.

> 检测应对不配合的攻击者──水印应对合规性AI 生成的音频应被识别──2026年两者都是必需的──

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


![Anti-spoofing vs watermarking vs provenance — three defense layers](../assets/spoofing-watermark.svg)

### 美国国家标准5 2024-2025年基准

> 美国国家统计局5  2024-2025年基准测试

根据之前的版本,

> 与之前版本相比最大的变化:

- **Crowdsourced data**现实条件.
  翻译: 中文**众包数据**没有录音棚纯净数据
- **~2000 speakers**其他地方的子.
  翻译: 中文**约 2000 名说话人**之前约有100名.
- **32 attack algorithms.**语音转换+反击扰乱.
  翻译: 中文**32 种攻击算法。**语音转换 + 对抗性扰动
- **Two tracks.**反措施 (CM) 独立检测;生物识别系统的伪造强 ASV (SASV).
  翻译: 中文**两个赛道。**生物识别系统的反欺诈措施

美国avspoof5最新版本:~7.23%EER.旧avspoof2019LA:0.42%EER.现实世界部署:在野生片段上预计5-10%EER.

> 美国5上升的SOTA:约7.23% EER──在较旧的美国2019年上升的EER──0.42%实际部署:预期在野外音频上EER为5-10%──

### 检测模型家族AASIST和RawNet2

> 检测模型家族

**AASIST**现在的SOTA在ASVspoof 5反措施任务上.

> **AASIST**根据频谱特征的图注意力机制──ASVspoof 5 反制措施任务的当前SOTA──

**RawNet2.**曲式前端,超出原始波形+TDNN脊柱. 简单的基线;仍然具有细调的竞争力.

> **RawNet2。**基本线的简单化;微调后仍有竞争力.

**NeXt-TDNN + SSL features.**2025 变种:ECAPA 式 + WavLM 功能 + 焦点损失. 在 ASVspoof 2019 LA 上达到 0.42% EER.

> **NeXt-TDNN + SSL 特征。**2025年变体:ECAPA 风格 + WavLM 特征 +焦点损失──在ASVspoof 2019 LA上升达到0.42%EER──

### 音频密码 2024年水印默认

> 音频密封  2024 年的水印默认方案

标签**AudioSeal**基本设计:

> 标签:**AudioSeal**核心设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计: 设计:

- **Localized.**检测每一个的水印,在16 kHz样本分辨率 (1/16000s) 上.
  翻译: 中文**局部化。**以 16 kHz 采样分辨率逐个检测水印
- **Generator + detector jointly trained.**发电机学会嵌入无声信号;探测器通过增强学习找到它.
  翻译: 中文**生成器 + 检测器联合训练。**生成机学习嵌入不可听信号;检测机学习通过增强找到它.
- **Robust.**能保持MP3/AAC压缩,EQ,速度变化 ±10%,噪音混合 +10 dB SNR.
  翻译: 中文**鲁棒。**能经受 MP3/AAC 压缩,均衡, ±10% 变速, +10 dB SNR 噪声混合.
- **Fast.**探测器的速度是485倍,比WavMark快1000倍.
  翻译: 中文**快速。**检测器运行速度为485倍;比WavMark快1000倍.
- **Capacity.**16位实用载荷 (可编码模型ID,生成时间印,用户ID) 可嵌入每个语句.
  翻译: 中文**容量。**16位载荷(可编码模型ID、生成时间、用户ID) 可嵌入每个语音段──

### 波音标

音频密封前的开放基线,可逆神经网络,32位/秒.

> 之前的开源基线──可逆神经网络,32位/秒──问题:

- 同步的速度很慢.
  中文翻译:同步暴力破解很慢──
- 通过高斯噪音或MP3压缩可以移除.
  中文翻译:可被高斯噪音或MP3 压缩删除
- 不是实时友好的.
  中文翻译:不适合实时场景――

### 波动验证 (2025年7月)

解决AudioSeal的弱点 具体用于时间操作 (逆转,速度).使用基于FiLM的发电机 +专家混合探测器.在标准攻击上与AudioSeal竞争力;处理时间编辑.

> 波浪验证 (WaveVerify) 解决了AudioSeal的弱点特别是时间操作反转变速度) 使用基于FiLM的生成器+MoE检测器在标准攻击上与AudioSeal相当;能处理时间编辑

### 敌人利用的差距

根据AudioMarkBench的数据, "在音速转移下,所有水标显示Bit恢复精度低于0.6,表明几乎完全删除. "**Pitch-shift is the universal attack.**无2026水标完全适用于攻击性音调修改.

> 攻击者利用的漏洞──来自AudioMarkBench:"在音高偏移下,所有水印的位恢复准确率低于0.6,表明几乎完全被删除──"**音高偏移是通用攻击。**没有任何2026年水印能完全抵御激进的音高修改.

### 内容真实性倡议

无线电技术 一个显现格式.音频文件包含加密签名的创建工具,作者,日期的元数据.Audobox/无使用它.好来源;如果一个坏演员重新编码和排行元数据,什么都不做.

> 内容真实性倡议――不是机器学习技术――是一种清单格式――音频文件带着关于创建工具,作者,日期加密签名元数据――Audobox/无使用它――有利于追溯源;但如果恶意行为者重新编码并剥离元数据则无效――

> **【拓展：语音 AI 的产品化】**语音技术在产品化中面临着独特的挑战:不同口音,背景噪音,远场拾音,多人说话等.

> **【拓展：多语言语音技术】**全球语言的语音特性差异巨大:声调语言的音高携带语义,低资源语言缺乏训练数据――Meta的MMS模型支持1000多种语言的语音识别,语在多语言场景表现出色,但仍然需要针对特定语言微调――

> **【拓展：语音隐私与安全】**语音数据包含大量个人隐私信息 (声纹、对话内容) ◦深度伪造 (Deepfake) 语音技术可被滥用作弊 (欺诈) 音频水印 (音频水印) ◎音纹反欺诈 (反欺诈) ◎反欺诈 (反欺诈) ◎是当前的研究热点.




## 建立它,实现它.

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

```figure
v4-audio-watermark
```

## 建立它

### 步骤1:简单的光谱特征探测器 (玩具)

> 步骤1:简单的频谱特征检测器 (玩具版)

```python
def spectral_rolloff(spec, percentile=0.85):
    cum = 0
    total = sum(spec)
    if total == 0:
        return 0
    threshold = total * percentile
    for k, v in enumerate(spec):
        cum += v
        if cum >= threshold:
            return k
    return len(spec) - 1

def is_suspicious(audio):
    spec = magnitude_spectrum(audio)
    rolloff = spectral_rolloff(spec)
    return rolloff / len(spec) > 0.92
```

合成语音通常具有异常平坦的高频能量. 生产探测器使用AASIST,而不是这. 但直觉是正确的.

> 合成语音通常具有异常平坦的高频能量.

### 步骤2: 音频密码嵌入+检测

> 步骤2:AudioSeal 嵌入 + 检测

```python
from audioseal import AudioSeal
import torch

generator = AudioSeal.load_generator("audioseal_wm_16bits")
detector = AudioSeal.load_detector("audioseal_detector_16bits")

audio = load_wav("generated.wav", sr=16000)[None, None, :]
payload = torch.tensor([[1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0]])
watermark = generator.get_watermark(audio, sample_rate=16000, message=payload)
watermarked = audio + watermark

result, decoded_payload = detector.detect_watermark(watermarked, sample_rate=16000)
# result: float in [0, 1] — probability of watermark presence
# decoded_payload: 16 bits; match against embedded payload
```

### 评估 EER

> 步骤3:评估  EER(等错误率)

```python
def eer(real_scores, fake_scores):
    thresholds = sorted(set(real_scores + fake_scores))
    best = (1.0, 0.0)
    for t in thresholds:
        far = sum(1 for s in fake_scores if s >= t) / len(fake_scores)
        frr = sum(1 for s in real_scores if s < t) / len(real_scores)
        if abs(far - frr) < best[0]:
            best = (abs(far - frr), (far + frr) / 2)
    return best[1]
```

### 步骤4:生产一体化

> 步骤4:生产阶段集成

```python
def safe_tts(text, voice, clone_reference=None):
    if clone_reference is not None:
        verify_consent(user_id, clone_reference)
    audio = tts_model.synthesize(text, voice)
    audio_with_wm = audioseal_embed(audio, payload=build_payload(user_id, model_id))
    manifest = c2pa_sign(audio_with_wm, user_id, timestamp=now())
    return audio_with_wm, manifest
```

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.


每一代船舶: (1) 水标, (2) 签署的公告, (3) 保持政策的审计记录.

> 每次生成的输出都包含: 1) 水印, 2) 签名清单, 3) 符合保留策略的审计日志.




> **【拓展：语音与情感计算】**语音不仅传递文字信息,还携带丰富的情感信号 (语调、语速、音高变化) 情感语音识别 (语音识别,语音情感识别,SER) 在客服质检,心理健康监测,智能教育等领域广泛应用.

## 用它实现框架

| Use case | Defense |
|----------|---------|
| Shipping TTS / voice cloning / 上线 TTS/语音克隆 | AudioSeal embed on every output (non-negotiable) / 每次输出嵌入 AudioSeal（不可妥协） |
| Biometric voice unlock / 生物识别语音解锁 | AASIST + ECAPA ensemble; liveness challenge / AASIST + ECAPA 集成；活体挑战 |
| Call-center fraud detection / 呼叫中心欺诈检测 | AASIST on 20% sample of incoming calls / 对 20% 的来电做 AASIST 检测 |
| Podcast authenticity / 播客真实性 | C2PA signing on upload, AudioSeal if AI-generated / 上传时 C2PA 签名，AI 生成则加 AudioSeal |
| Research / training detectors / 研究/训练检测器 | ASVspoof 5 train/dev/eval sets / ASVspoof 5 训练/开发/评估集 |



## 陷

> 常见陷

- **Watermark without detector ever running.**没有意义,把探测器送进你的信息中心.
  翻译: 中文**嵌入水印但从未运行检测器。**没有意义.把检测器集成到CI中.
- **Detection without calibration.**助手训练了美国的LA过度,现实世界精度下降.
  翻译: 中文**检测未校准。**在美国,LA上训练的AASIST会过拟;实际准确率下降.
- **Pitch-shift gap.**攻击性音调移除了大多数水印.
  翻译: 中文**音高偏移漏洞。**激进的音高偏移能去除大多数水印――准备检测作为后备――
- **Metadata strip-and-rehost.**通过重新编码,C2PA可以轻微绕过. 总是加加密 + 感知 (水印) 防御在一起.
  翻译: 中文**元数据剥离重新托管。**通过重新编码即可轻松绕过──始终同时使用加密 + 感知(水印) 防御──
- **Liveness as detection.**防止重播攻击,但不是实时克隆.
  翻译: 中文**活体检测作为检测手段。**让用户说一个随机短语. 可以防止重发攻击,但不能防止实时克隆.

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


## 运送它.

保存如`outputs/skill-spoof-defender.md`选择检测模型,水印,来源表和语音代码部署的操作操作手册.

> 保存为`outputs/skill-spoof-defender.md`◎为一个语音生成部署选择检测模型、水印、来源清单和运营手册──

## 练习题

1. **Easy.**跑步`code/main.py`玩具探测器+玩具水印嵌入/检测到合成音频.
   翻译: 中文**简单。**运行`code/main.py`△ 在合成音频上测试玩具检测器 + 玩具水印嵌入/检测。
2. **Medium.**安装`audioseal`通过噪音破坏音频,并测量位恢复精度.
   翻译: 中文**中等。**装备`audioseal`通过噪音损坏音频并测量位恢复准确率.
3. **Hard.**在 ASVspoof 2019 LA 上调整RawNet2或AASIST.测量EER.在F5-TTS生成的剪辑组上测试看OOD检测如何降低.
   翻译: 中文**困难。**在 ASVspoof 2019 LA 上微调 RawNet2 或 AASIST──测量 EER──在留下的 F5-TTS 生成音频集上测试观察 OOD 检测的退化程度──

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| ASVspoof | The benchmark | Biennial challenge; 2024 = ASVspoof 5. / 双年挑战赛；2024 = ASVspoof 5 |
| CM (countermeasure) | Detector | Classifier: real speech vs synthetic / converted. / 分类器：真实语音 vs 合成/转换语音 |
| SASV | Speaker verif + CM | Integrated biometric + spoof detection. / 集成生物识别 + 欺骗检测 |
| AudioSeal | Meta watermark | Localized, 16-bit payload, 485× faster than WavMark. / 局部化，16 位载荷，比 WavMark 快 485 倍 |
| Bit Recovery Accuracy | Watermark survival | Fraction of payload bits recovered after attack. / 攻击后恢复的载荷位比例 |
| C2PA | Provenance manifest | Cryptographic metadata about creation / authorship. / 关于创建/作者身份的加密元数据 |
| AASIST | Detector family | Graph-attention-based anti-spoofing SOTA. / 基于图注意力的反欺骗 SOTA |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [Todisco et al. (2024). ASVspoof 5](https://dl.acm.org/doi/10.1016/j.csl.2025.101825)目前的基准指数.
  美国人5当前基准.
- [Defossez et al. (2024). AudioSeal](https://arxiv.org/abs/2401.17264)默认的水标.
  水印默认方案.
- [Chen et al. (2025). WaveVerify](https://arxiv.org/abs/2507.21150) 时间攻击的 MoE 探测器.
  波浪验证对时间攻击的MOE检测器
- [Jung et al. (2022). AASIST](https://arxiv.org/abs/2110.01200) SOTA检测脊柱.
  等 (2022). 协助检测骨干
- [AudioMarkBench (2024)](https://proceedings.neurips.cc/paper_files/paper/2024/file/5d9b7775296a641a1913ab6b4425d5e8-Paper-Datasets_and_Benchmarks_Track.pdf)强度评估.
  鲁棒性评估──
- [C2PA specification](https://c2pa.org/specifications/specifications/)来源表格.
  根据C2PA规范,

> **【中文解读】**延伸阅读提供了深入学习的高质量资源,包括论文,教程和工具.

