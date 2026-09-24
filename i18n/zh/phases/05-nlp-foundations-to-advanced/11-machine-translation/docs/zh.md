# 机器翻译

> 翻译是为30年来支付了NLP研究的任务,
> 翻译是为NLP研究的30年任务,现在仍在继续.

> **【中文解读】**从统计机器翻译到神经机器翻译――现代用变压器――

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 10 (Attention Mechanism), Phase 5 · 04 (GloVe, FastText, Subword) | **前置知识:** Phase 5 · 10 (Attention Mechanism), Phase 5 · 04 (GloVe, FastText, Subword)
**Time:** ~75 minutes | **时间:** ~75 minutes


## 问题 问题引入

一个模型在一个语言中读出句子,并在另一个语言中生成句子.长度不同.词序不同.一些源词的地图为多个目标词和相反.语法拒绝单对单地图.法语中的"我想念你"是"tu me manques"字面上"你是我缺少的".没有单词级的排列可以存活下来.
> 模型读取一种语言的句子并产生另一种语言的句子――长度不同――词序不同――一些源词映射到多个目标词,反之亦然――习语拒绝对对对对映射――"我怀念你"的法语是"你让我遗憾" 字面意思是"你对我是缺失的"――没有词级对齐能经受这个――

> **【中文解读】**本节提出的问题是:如何在实际工程中正确理解和应用这一技术――理解问题背景有助于把握技术选择的关键决策点――在实际人工智能系统中,错误的技术选择往往比实现细节的错误成本更高――


机器翻译是迫使NLP发明编码解码器,注意力,变换器,最终整个LLM范式的任务.每一步都会进步,因为翻译质量是可测量的,人类和机器之间的差距是固执的.
> 机器翻译是迫使NLP发明编码器-解码器,注意力,变革器以及最终整个LLM范式的任务.

这一课跳过历史课程,并教导2026年的工作管道:预训练的多语言编码器-解码器 (NLLB-200或 mBART),字体代码化,光束搜索,BLEU和 chrF评估,以及数量未被捕的失败模式.
> 本课跳过历史课,教授 2026年工作流水线:预训练多语言编码器-解码器(NLLB-200或 mBART) 、子词分词、束搜索、BLEU 和 chrF 评估,以及少数仍将逃过检查进入生产失败模式――

## 概念的核心概念

> **【中文解读】**本节介绍核心概念和理论基础.掌握这些概念是后续动手实现的前提,同时也是面试和工程实践中高频考察的知识点.


![MT pipeline: tokenize → encode → decode with attention → detokenize](../assets/mt-pipeline.svg)
> ![MT 流水线：分词 → 编码 → 带注意力的解码 → 去分词](../assets/mt-pipeline.svg)

现代MT是一个以平行文本训练的变压器编码器-解码器.编码器在语言的标记中读取源头.解码器一次生成目标,一次一个字段,通过跨度注意力 (课10) 使用编码器输出.解码使用光束搜索以避免贪的解码陷.输出被解代,被破坏,并与参考进行分数.
> 现代MT是平行文本上训练的变压器编码器解码器.编码器以其语言分词读取源语言.解码器通过交叉注意力 (第十课) 使用编码器输出,每次生成一个子词的目标语言.解码使用束搜索避免贪心解码陷.

实际的MT质量是由三个操作选择来实现的.
> 三个运营选择驱动真实的世界MT质量――

- **Tokenizer.**语句Piece BPE 训练基于混合语言的语文. 语言之间的共享词汇是使NLLB中零射对成为可能的.
- **Model size.**电脑上可以安装NLLB-200蒸600M.NLLB-200 3.3B是公布的生产默认标准.54.5B是研究上限.
- **Decoding.**对于一般内容,光束宽度为4-5; 长度罚款以避免输出太短; 需要语法一致时限制解码.
> - **分词器。**在混合语言语料上训练的SentencePiece BPE──跨语言共享词表是NLLB支持零样本语言对的关键──
- **模型大小。**美国国家经济学部 (NLLB-200) 已发表的生产默认.
- **解码。**通用内容束宽度 4-5──长度惩罚避免输出过短──需要术语一致性时使用束解码──

> **【中文解读】**本节通过代码实现从零到核心算法――这种"从零开始"的方式可以帮助理解框架背后的原理,遇到问题时不会被黑盒困住――

> **【拓展：大语言模型的工程实践】**从GPT到ChatGPT,NLP领域经历了从"每个任务训练一个模型"到"一个模型解决所有任务"的范式转变. 在实际工程中,LLM的部署需要考虑代币限制,延迟,成本,安全审查等问题.

> **【拓展：RAG 与企业知识库】**检索增强生成 (RAG) 是当前企业人工智能应用中最流行的架构:将用户查询先检索相关文档片段,再将检索结果作为上下文给LLM 生成答案――这种方式解决了LLM 知识过时和幻觉问题――向量数据库――如Milvus、Pinecone、Weaviate) 是RAG系统的核心组件――

> **【拓展：NLP 的多语言挑战】**全球有7000多种语言,但NLP研究主要集中在英语等少数语言.跨语言迁移学习,多语言预训模型 (如 mBERT,XLM-R) 是解决低资源语言NLP的主要方法.


## 建立它,实现它.
```figure
seq2seq-alignment
```

## 建立它

### 步骤1:预训练式MT调用
> 现在,我知道.`src_lang`告诉分词器使用哪种文字和分分.`forced_bos_token_id`告诉解码器生成哪种语言──两者都是NLLB特有的技巧;mBART 和 M2M-100 使用各自的约定,不可互换──

```python
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

model_id = "facebook/nllb-200-distilled-600M"
tok = AutoTokenizer.from_pretrained(model_id, src_lang="eng_Latn")
model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

src = "The cats are running."
inputs = tok(src, return_tensors="pt")

out = model.generate(
    **inputs,
    forced_bos_token_id=tok.convert_tokens_to_ids("fra_Latn"),
    num_beams=5,
    length_penalty=1.0,
    max_new_tokens=64,
)
print(tok.batch_decode(out, skip_special_tokens=True)[0])
```

```text
Les chats courent.
```

这里有三个重要的事情.`src_lang`告诉代币器应使用哪个脚本和细分. `forced_bos_token_id`它们都是NLLB特定的技巧; mBART和M2M-100使用自己的规范,它们不能互换.
> 蓝色测量输出与参考之间的n-gram 重叠──四种参考n-gram 大小(1-4),精确率的几何平均,对过短输出的简洁惩罚──分数在 [0, 100]──常用但难以解读:30蓝色是"可用";40是"好";50是"出色";1蓝色以内差异是噪音──

### 步骤2:蓝色和色
>  测字符级 F 分数――对蓝色的低估匹配的形态丰富语言更敏感――通常与蓝色的起报――

蓝色测量输出和参考之间的 n-gram重叠.四个参考 n-gram尺寸 (1-4),精度的几何平均值,过短输出的短暂处罚. 积分在 [0, 100].通常使用. 解释时令人丧: 30 蓝色是"可用"; 40 是"好"; 50 是"例外"; 1 蓝色的差异是噪音.
> 始终使用`sacrebleu`△它归结分词使分数跨论文可比.

chrF测量字符级F分. 对于蓝色字母不足的语言更敏感. 通常与蓝色字母一起报告.
> 现代MT 评估使用三个互补指标族――至少使用两个发布――

```python
import sacrebleu

hypotheses = ["Les chats courent."]
references = [["Les chats courent."]]

bleu = sacrebleu.corpus_bleu(hypotheses, references)
chrf = sacrebleu.corpus_chrf(hypotheses, references)
print(f"BLEU: {bleu.score:.1f}  chrF: {chrf.score:.1f}")
```

总是使用`sacrebleu`通过将自己的蓝色计算进行调整,误导性基准会发生.
> - **启发式**根据参考可解释 对于释义不敏感 用于遗留比较和归归检测
- **学习型**由于2023年与MT研究关联最高,是2026年质量重要的生产默认选择.
- **LLM 评委**评委在评分标准设计良好时与人类一致性约80%──用于没有参考的开放内容──

### 三层次评估层次 (2026)
> 2026 年实用技术:`sacrebleu`蓝色和色的色,`unbabel-comet`在信任生产数据之前,针对50-100个个人标志样本校准每个标志.

现代MT评估使用了三个互补的指标组.
> 没有参考指标 (COMET-QE、BLEURT-QE、LLM 评委) 让你在没有参考的情况下评估翻译,这对没有参考翻译的长尾语言对很重要.

- **Heuristic**快速,基于参考,可解释,对抛词无关.用于传统的比较和回归检测.
- **Learned**根据人类判断训练的神经模型;对译文与源和参考的语义相似性进行比较.自2023年以来,COMET与MT研究有着最高的关联,在质量方面是2026年生产默认.
- **LLM-as-judge**提供一个大型模型,以评分翻译的流利性,足够性,语调,文化适用性.GPT-4作为法官与人同意相匹配~80%的时间,当标题设计得很好.在没有引用的情况下,用于开放式内容.
> 上面的工作流水线 80% 的时间能流翻译,剩下的 20% 会静默失败──已命名的失败模式:

实际的2026堆:`sacrebleu`对于BLEU和chRF,`unbabel-comet`在依靠生产数据之前,将每一个指标与50-100个标记的人类示例进行校准.
> - **幻觉。**模型发明源中没有内容──在未熟的领域词汇中常见──症状:输出流但声称源没有陈述的事实──缓解:对领域术语的约束解码,对受监管的内容的人工审查,监控输出比输入长得多的异常──
- **偏离目标语言生成。**模型翻译成错误的语言.NLLB 在罕见的语言对上出奇地容易出错.缓解:验证`forced_bos_token_id`并始终使用语言识别模型检查输出.
- **术语漂移。**在文档1中"登录"变成"登录",在文档2中变成"创意"──对于 UI 文本和面向用户的字符串,一致性比原始质量更重要──缓解:词汇表约束解码或后编辑字典──
- **语体不匹配。**法语 "tu" vs "vous",日语敬语级别――模型选择训练中更常见的形式――对于面向客户的内容,这通常是错误的――缓解:如果模型支持,用语体标志作为提示前,或仅在正式语料上微调小模型――
- **短输入长度爆炸。**非常短的输入句子经常产生过长的翻译,因为长度惩罚在约5个源代币下面急剧下降.

没有引用的指标 (COMET-QE,BLEURT-QE,LLM-as-judge) 允许您评估没有引用的翻译,这对于没有引用翻译的长尾语言对象是重要的.
> 预训模型是通才.法律、医疗或游戏对话 译:从平行数据的微调中可测量地受益.方案并不复杂:

### 步骤3:生产中什么断
> 几千个高质量平行样本胜过几十万个噪音网络抓取样本――训练数据质量是最大的生产杆――

上面的工作管道将在80%的时间流动地翻译,剩余20%的时间默默地失败.

- **Hallucination.**模型发明内容不存在源头.在未熟悉的域词汇中很常见. 症状:输出流动,但声称来源没有声明的事实. 缓解:域名术语上的限制解码,监管的内容的人类审查,输出的监测时间远远超过输入.
- **Off-target generation.**模特翻译成错误的语言.NLLB在罕见的语言对象上有惊人的倾向.`forced_bos_token_id`并且总是使用语言ID模型检查输出.
- **Terminology drift.**"登录"成为doc1中的"s'inscribe"和doc2中的"creer un compte".对于UI文本和面向用户的字符串,一致性比原始质量更重要.减轻:词典限制式解码或后编辑词典.
- **Formality mismatch.**简单的"你"与"你"的法语,日本礼貌水平.模型选择了训练中最常见的形式.对于面向客户的内容,这通常是错误的.减轻:提示前,如果模型支持它,或在正式的体验中调整一个小模型.
- **Length explosion on short input.**非常短的输入句子通常产生过长的翻译,因为长度罚款落在源代币低于5个悬崖.减轻:硬最大长度盖相对应于源长度.

### 步骤4:为域进行细节调整

预训练的模型是一般主义者. 法律,医学或游戏对话翻译可以通过对域的并行数据进行微调来得到相当大的好处.

```python
from transformers import Trainer, TrainingArguments
from datasets import Dataset

pairs = [
    {"src": "The defendant pleaded guilty.", "tgt": "L'accusé a plaidé coupable."},
]

ds = Dataset.from_list(pairs)


def preprocess(ex):
    return tok(
        ex["src"],
        text_target=ex["tgt"],
        truncation=True,
        max_length=128,
        padding="max_length",
    )


ds = ds.map(preprocess, remove_columns=["src", "tgt"])

args = TrainingArguments(output_dir="out", per_device_train_batch_size=4, num_train_epochs=3, learning_rate=3e-5)
Trainer(model=model, args=args, train_dataset=ds).train()
```

> **【中文解读】**本节展示了如何使用成熟框架 (如PyTorch、HuggingFace等) 快速应用该技术.


几千个高质量的平行例子比几百万个有噪音的网页剪辑比较高.


> **【拓展：Prompt Engineering 与 LLM 应用】**快速工程已成为NLP工程师的核心技能. 从零射到少射,从思想链到反应,不同的提示策略适用于不同场景. 在实际项目中,系统提示 (系统提示) 的设计直接影响了LLM应用的稳定性和输出质量.

## 用它实现框架

对于MT的2026年生产堆:
> 2026 年的MT 生产技术:

| Use case | Recommended starting point |
|---------|---------------------------|
| Any-to-any, 200 languages | `facebook/nllb-200-distilled-600M` (laptop) or `nllb-200-3.3B` (production) |
| English-centric, high quality, 50 languages | `facebook/mbart-large-50-many-to-many-mmt` |
| Short runs, cheap inference, English-French/German/Spanish | Helsinki-NLP / Marian models |
| Latency-critical browser-side | ONNX-quantized Marian (~50 MB) |
| Maximum quality, willing to pay | GPT-4 / Claude / Gemini with translation prompts |
> 让我们开始.
|---------|---------|
| 任意到任意，200 种语言 | `facebook/nllb-200-distilled-600M`（笔记本）或 `nllb-200-3.3B`（生产） |
| 以英语为中心，高质量，50 种语言 | `facebook/mbart-large-50-many-to-many-mmt` |
| 短任务，廉价推理，英语-法语/德语/西班牙语 | Helsinki-NLP / Marian 模型 |
| 延迟敏感的浏览器端 | ONNX 量化的 Marian（约 50 MB） |
| 最高质量，愿意付费 | GPT-4 / Claude / Gemini 配合翻译提示 |

现在,从2026年开始,LLM在几种语言对上超过了专业的MT模型,特别是在语法内容和长文本上.交易是每代币成本和延迟.当环境长度,风格一致性或域名适应性通过提示问题超过吞吐量时选择LLM.
> 截至2026年,LLM在多种语言对已超越专业的MT模型,特别是在习语内容和长上下文上.

> **【中文解读】**本节关注如何将模型部署为可用的产品. 从原型到生产级系统需要考虑性能优化,错误处理,监控等多个维度.


## 运送它.

保存如`outputs/skill-mt-evaluator.md`其他:
> 保存为`outputs/skill-mt-evaluator.md`其他:

```markdown
---
name: mt-evaluator
description: Evaluate a machine translation output for shipping.
version: 1.0.0
phase: 5
lesson: 11
tags: [nlp, translation, evaluation]
---

Given a source text and a candidate translation, output:

1. Automatic score estimate. BLEU and chrF ranges you would expect. State whether a reference is available.
2. Five-point human-verifiable check list: (a) content preservation (no hallucinations), (b) correct language, (c) register / formality match, (d) terminology consistency with glossary if provided, (e) no truncation or length explosion.
3. One domain-specific issue to probe. E.g., for legal: named entities and statute citations. For medical: drug names and dosages. For UI: placeholder variables `{name}`.
4. Confidence flag. "Ship" / "Ship with review" / "Do not ship". Tie to the severity of issues found in step 2.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。


Refuse to ship a translation without a language-ID check on output. Refuse to evaluate without a reference unless the user explicitly opts in to reference-free scoring (COMET-QE, BLEURT-QE). Flag any content over 1000 tokens as likely needing chunked translation.
```

## 练习题

1. **Easy.**通过使用 翻译5句的英语段落到法语,然后再转到英语`nllb-200-distilled-600M`测量回路与原始的距离. 你应该看到语义保存与词选择漂移.
2. **Medium.**通过使用 `fasttext lid.176`或`langdetect`集成到MT调用中,以便在返回之前,
3. **Hard.**精细调节`nllb-200-distilled-600M`在您选择的5000对域名体内测量BLEEU在细调之前和后的延长集.报告哪些句子改善了,哪些退缩.
> 1. **简单。**使用 `nllb-200-distilled-600M`将 5 句英语段落翻译成法语再翻回英语――测量往返与原本接近程度――你应该看到语义保留但用词漂移――
2. **中等。**使用 `fasttext lid.176`或`langdetect`实现翻译输出语言识别检查――集成到MT调用中,在返回前捕获偏离目标语言的生成――
3. **困难。**在您选择的 5000 个领域语料微调`nllb-200-distilled-600M`测微调前后在留出集中的BLEU. 报告哪些类型的句子改进了,哪些退步了.

> **【中文解读】**在团队协作中,统一术语定义可以避免大量沟通误解.


## 关键词 快速查找表

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| BLEU | Translation score | N-gram precision with brevity penalty. [0, 100]. |
| chrF | Character F-score | Character-level F-score. More sensitive for morphologically rich languages. |
| NMT | Neural MT | Transformer encoder-decoder trained on parallel text. The 2017+ default. |
| NLLB | No Language Left Behind | Meta's 200-language MT model family. |
| Constrained decoding | Controlled output | Force specific tokens or n-grams to appear / not appear in the output. |
| Hallucination | Invented content | Model output that is not supported by the source. |
> 现在,我们在这个世界里,
|------|-----------|---------|
| BLEU | 翻译分数 | 带简洁惩罚的 n-gram 精确率。[0, 100]。 |
| chrF | 字符 F 分数 | 字符级 F 分数。对形态丰富语言更敏感。 |
| NMT | 神经机器翻译 | 在平行文本上训练的 Transformer 编码器-解码器。2017+ 的默认。 |
| NLLB | No Language Left Behind | Meta 的 200 语言 MT 模型系列。 |
| 约束解码 | 控制输出 | 强制特定 token 或 n-gram 出现/不出现在输出中。 |
| 幻觉 | 发明内容 | 模型输出中不被源支持的内容。 |

> **【中文解读】**延伸阅读提供了深入学习的高质量资源. 这些论文和教程是该领域的经典参考文献,适合需要深入了解的读者.


## 继续阅读 继续阅读

- [Costa-jussà et al. (2022). No Language Left Behind: Scaling Human-Centered Machine Translation](https://arxiv.org/abs/2207.04672)NLLB论文.
- [Post (2018). A Call for Clarity in Reporting BLEU Scores](https://aclanthology.org/W18-6319/)为什么`sacrebleu`报告 BLEU的唯一正确方式.
- [Popović (2015). chrF: character n-gram F-score for automatic MT evaluation](https://aclanthology.org/W15-3049/)   纸
- [Hugging Face MT guide](https://huggingface.co/docs/transformers/tasks/translation)实用细调步行.
> - [Costa-jussà et al. (2022). No Language Left Behind: Scaling Human-Centered Machine Translation](https://arxiv.org/abs/2207.04672) 论文──
- [Post (2018). A Call for Clarity in Reporting BLEU Scores](https://aclanthology.org/W18-6319/)为什么?`sacrebleu`是报告BLEU唯一正确的方式.
- [Popović (2015). chrF: character n-gram F-score for automatic MT evaluation](https://aclanthology.org/W15-3049/) 论文:
- [Hugging Face MT guide](https://huggingface.co/docs/transformers/tasks/translation)实用微调演练
