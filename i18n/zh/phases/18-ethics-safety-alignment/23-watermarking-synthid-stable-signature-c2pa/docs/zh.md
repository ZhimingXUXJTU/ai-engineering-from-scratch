# 标记水 合成ID,稳定签名,C2PA

> 据了解,在2026年, 通过"责任的GENAI工具包" (Responsible GenAI Toolkit) 发行了2023年8月的图像水标,文本+视频2024年5月 (Gemini + Veo),文本开源2024年10月,并与Gemini 3 Pro一起实现了2025年11月的多媒体检测器. 文字水标将下一个代币的样本抽象概率不知不觉地调整;图像/视频水标存活压缩,切割,过,率变化. 稳定签名 (Fernandez et al., ICCV 2023, arXiv:2303.15435) 细调隐藏扩散解码器,使每个输出都包含固定信息;在 FPR<1e-6 中,被切割的 (内容的10%) 生成的图像被检测到90%以上. 后续"稳定签名不稳定" (arXiv:2405.07145,2024年5月) 细调消除水印,同时保持质量. C2PA 加密签署的,具有改性明显的元数据标准 (C2PA 2.2解释器 2025). 水标和C2PA是互补的:可以删除元数据,但具有更丰富的来源;水标通过转码仍然存在,但具有更少的信息.

> **【中文解读】**本节介绍了AI水印技术SynthID、C2PA等标识AI 生产内容的方法──SynthID(Google DeepMind) 调整下一个代码 采样概率使生成包含更多的"绿色"令牌不可察知但可检测──稳定签名 微调潜在扩散解码器使每个输出包含固定二进制消息──C2PA是加密签名、防改的元数据标准──

> **【拓展：水印 → Deepfake 检测】**水印是检测的核心技术路径. 水印的跨模态检测器 (SynthID) 可以从文本,图像,音频和视频中读取信号.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, token-watermark embed + detect) | **语言:** Python（标准库，token 水印嵌入 + 检测）
**Prerequisites:** Phase 10 · 04 (sampling), Phase 01 · 09 (information theory) | **前置知识:** Phase 10 · 04 (采样), Phase 01 · 09 (信息论)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**学本节前请先掌握:阶段10·04(采样) 、阶段01·09(信息论) 。三大水印技术 + 内容追溯标准。
>  **【类比】**水印 = "AI 内容的隐形身份证"──SynthID(Google) = 调整下一个代码 采样偏好"绿色"代码,不可察觉但可检测;稳定签名 = 微调解码器让每张图都含有固定二进制消息(剪裁10% 仍 >90% 检出);C2PA = 加密签名元数据──互补:元数据可剥夺但信息丰富;水抗印转码但信息少──
> ️"稳定签名不稳定"2024.5:微调即可移除水印保质量――水印不是银弹――

## 学习目标

- 描述代币级水标 (SynthID文本式) 和可检测的机制.
- 描述稳定签名和2024年的移除攻击.
- 国家C2PA的作用以及为什么它是补充水标.
- 描述主要的限制:模型特定的信号,在抛词下强度和保持意义的攻击 (arXiv:2508.20228).

> 描述令牌级水印 (SynthID-text风格)及其可检测机制――描述稳定签名和2024年破坏其移除攻击――说明C2PA的角色以及为什么它与水印互补――描述关键局限性:模型特定信号、释义下鲁棒性和意义保持攻击――

## 问题问题

2023-2024年,深度假冒和人工智能生成的内容将进入政治和消费者背景.水标是拟议的技术来源信号:创建时标记几代人,后者检测. 2025年证据:没有水标是无条件的强大,但与C2PA元数据层叠加,组合提供可用的来源故事.

> 2023-2024年深度伪造和人工智能生成内容大规模进入政治和消费场景――水印是提出的技术来源信号:在创建时标记生成,后检测――2025年证据:没有水印是无条件的,但与C2PA元数据分层提供可用的来源故事――

## 概念的概念

> **【中文解读】**文本水印机(Kirchenbauer 等人 2023,由 Google 产品化):每个解码步骤将前 K 个令牌哈希产生词汇表的伪随机"绿色"和"红色"分区,向绿色逻辑 添加 delta 偏置采样――生成包含随机比更多的绿色令牌――检测:重新哈希每个前,计量生成中的绿色令牌,计算 z 分数――水印文本 z > 0,人类文本 z ~ 0。

### 文字水标 (SynthID-text风格)

基尔堡等人2023机制,由谷歌生产:

1. 在每一步解码时,将前一个K代码加密起来,以产生词汇的伪随机分区为"绿色"和"红色"的集合.
2. 通过添加 δ 给绿色的logits来对绿色集合进行偏差样本.
3. 代子含有比偶然产生的更多的绿色代币.

检测:重新检查每个前,在生成中计算绿色代币,计算z分数.z分数为>0用于水标文本, ~0用于人类文本.

性能:
- 读者无法感知 (δ 足够小,质量损失是微不足道的).
- 通过访问词汇分区功能可检测.
- 转写文本破坏信号.

通过谷歌的"负责任GenAI工具包"2024年10月,

> **【中文解读】**稳定签名(Fernandez 等人, ICCV 2023) 微调潜在扩散解码器使每个生成图像包含固定二进制消息──剪切到原始内容10%的图像在 FPR<1e-6 下检测率 >90%──但2024年5月"稳定签名是不稳定的"证明微调解码器可以在保持图像质量同时移动水印对抗性生成后微调成本低──

### 稳定签名 (图片)

费尔南德斯等人.ICCV 2023. 细调隐藏扩散解码器,使每一个生成的图像都包含嵌入隐藏表示中的固定二进制信息.检测通过神经解码器从隐藏中解码.在FPR<1e-6时,切割的图像被检测到90%以上.

> 稳定签名 微调潜在扩散解码器使每个生成图像包含固定二进制消息──剪切到10%的图像在 FPR<1e-6 下检测率 >90%──

2024年5月"稳定签名不稳定" (arXiv:2405.07145):微调解码器删除水印,同时保持图像质量.对抗后代微调是便宜的;水印的对抗强度有限.

> 2024 年 5 月"稳定签名不稳定"证明微调解码器可以在保持图像质量同时移动水印――对抗性后产生微调成本低;水印的对抗性有限――

### 综合ID统一检测器 (2025年11月)

双子座3 Pro:一个多媒体探测器,可以在一个API中读取文字,图像,音频和视频的SynthID信号.

> 随着双子座3 Pro:一个跨模态检测器,可从文本,图像,音频和视频中读取SynthID信号.

> **【拓展：C2PA + 水印互补 → EU AI Act Article 50】**通过转码持久但只带有少量比特. Google 在搜索,广告和"关于此图片"中集成两者.

### 化剂

内容来源和真实性联盟.加密签署的伪造性明显的元数据标准.C2PA 2.2解释器 (2025).C2PA明示记录来源声明 (谁创建,何时,什么变化) 签署的创作者密钥.

> 密码签名,防改的元数据标准,C2PA 清单记录来源声明,由创始人签名.

补充水标:
- 转换数据可以删除;水印不能 (很容易).
- 转载数据的数据是丰富的 (完整的来源链);水标携带比特.
- 基于平台的采用,水标自动嵌入.

> 通过转码持久但只携带少量比特――C2PA依赖平台采用;水印自动嵌入――

谷歌将搜索,广告和"关于这个图像"都整合起来.

> 谷歌在搜索,广告和"关于此图片"中集成了两者.

> **【拓展：水印局限性 → 模型特定信号问题】**关键局限性:SynthID 水印仅来自启用SynthID的模型――"无SynthID 信号"不等于真实性证明未启用SynthID的模型生成的任何内容都不会有水印――此外,arXiv:2508.20228(2025) 显示了保持攻击的意义可以同时破坏文本水印和多种图像水印――

### 限制

- **Model-specific.**通过SynthID启用模型的SynthID水标代.没有SynthID的模型的一代没有水标,因此"没有SynthID信号"并不是认证真实性的证明.
- **Paraphrase.**文字水标没有保存含义的表达.
- **Transformation attacks.**文件的含义是: arXiv:2508.20228 (2025) 显示了破坏文本水标和许多图像水标的含义保护攻击.
- **Fine-tune removal.**根据"稳定签名不稳定",后代细调取消嵌入式水标.

### 欧盟人工智能法第50条

通过人工智能生成的内容标签的透明度法规 (第一个草案2025年12月,第二个草案2026年3月,预计2026年6月将最终通过[European Commission status page](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content)) 该法规将于2026年4月起继续起草,时间表可能会发生变化.要求技术层的监管层.必须标记深度假.

### 在这个阶段的第18阶段

课程22-23讲述了模型所发射的信息 (私人数据,来源信号).课程27涵盖了培训数据治理.课程24是要求这些技术措施的监管框架.

> 课程22-23 关于模型发出什么(私有数据、来源信号) ・课程27 涵盖训练数据管理――课程24 要求这些技术措施的监管框架――

## 用它使用方法
```figure
an-watermark-greenlist
```

## 用它

`code/main.py`标记是整数0..N-1;标记是对 Hash定义的绿色集合的样本偏差.一个探测器计算了绿色标记 z-score.你可以观察1000代标的检测,观看对象的破坏信号,测量人类文本上的虚假阳性率.

> `code/main.py`构建玩具文本水印――令牌是整数0.N-1;水印采样偏向哈希定义的绿色集――检测器计算绿色令牌 z 分数――你可以观察1000个令牌生成的检测、释义破坏信号以及人类文本上的误报率――

## 发射上线

这一课产生了`outputs/skill-provenance-audit.md`鉴于内容部署有 provenance 索赔,它审计:水标机制 (如果有的话),C2PA签署链 (如果有的话),每个内容的反抗性强度,以及每种模式覆盖性.

> 本课产出发 `outputs/skill-provenance-audit.md`提供有源声明内容部署,审计:水印机制,C2PA签名链,各自的反抗性以及每种模式覆盖.

## 练习题

1. 跑步`code/main.py`报告水标1000代币生成与人为作文的z分数. 确定 95%的可信度门时的虚假阳性率.

2. 执行一个抛物语攻击,以代码替换30%的代码.

3. 阅读Kirchenbauer等2023第6节关于强度. 为什么文字水标在表达中失败,但图像水标在剪切中存活下来?

4. 设计一个使用SynthID-text + C2PA元数据的部署.描述消费者看到的来源链.确定每个组件的一个故障模式.

5. 2024 年"稳定签名不稳定"结果显示,微调取消了图像水印.设计一个限制攻击的部署控制,例如,需要签署的微调检查站.

## 关键词 关键词

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| SynthID | "Google's watermark" | Cross-modal provenance signal; text, image, audio, video |
| Token watermark | "Kirchenbauer-style" | Biased-sampling text watermark detectable via green-token z-score |
| Stable Signature | "image watermark" | Fine-tuned-decoder watermark; ICCV 2023 |
| C2PA | "the metadata standard" | Cryptographically signed tamper-evident provenance metadata |
| Paraphrase robustness | "does rewording break it" | Text watermark property; currently limited |
| Fine-tune removal | "adversarial unwatermark" | Attack that removes image watermark via decoder fine-tuning |
| Cross-modal detector | "unified SynthID" | November 2025 unified API across modalities |

## 继续阅读 继续阅读

- [Kirchenbauer et al. — A Watermark for Large Language Models (ICML 2023, arXiv:2301.10226)](https://arxiv.org/abs/2301.10226)标志水标机制
- [Fernandez et al. — Stable Signature (ICCV 2023, arXiv:2303.15435)](https://arxiv.org/abs/2303.15435)图像水印纸
- ["Stable Signature is Unstable" (arXiv:2405.07145)](https://arxiv.org/abs/2405.07145)移除攻击
- [Google DeepMind — SynthID](https://deepmind.google/models/synthid/)跨模式水标
- [C2PA 2.2 Explainer (2025)](https://c2pa.org/specifications/specifications/2.2/explainer/Explainer.html)元数据标准
