# 艺术和视觉监狱中断

> 江,徐,努,西安,拉马苏布拉曼尼安,李,普韦德兰, "艺术:ASCII艺术基于的监狱突破攻击对符合法律的 LLM" (ACL 2024, arXiv:2402.11753). 隐藏安全相关的代币,以 ASCII 艺术的相同字母进行替换, 它们都无法认出ASCII艺术代币. 攻击绕过PPL (杂性过器), 抛物线防御和回归化. 相关:ViTC基准测量识别非语义视觉提示; StructuralSleight将无常文本编码结构 (树木,图形,嵌套JSON) 作为编码攻击的家族.

> **【中文解读】**本节介绍了ASCII 艺术视觉越狱文本图形绕过安全过器的攻击技术――ArtPrompt(ACL 2024) 两步攻击:识别安全相关词,使用ASCII 艺术染替换――安全过器看无害的标点符号网格,模型看一个词――GPT-4、Gemini、Claude、Llama-2 全部失败,攻击成功率超过75%――

> **【拓展：ArtPrompt → 编码攻击家族】**标准防御 (困惑度过、释义、重新分词) 在ArtPrompt 上全部失败,因为安全过器在令牌/语义级操作中,而ArtPrompt 在视觉识别级操作中.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, ArtPrompt token-masking harness) | **语言:** Python（标准库，ArtPrompt token 掩码框架）
**Prerequisites:** Phase 18 · 12 (PAIR), Phase 18 · 13 (MSJ) | **前置知识:** Phase 18 · 12 (PAIR), Phase 18 · 13 (MSJ)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**学本节前请先掌握:阶段 18·12-13──视觉越狱 = 用ASCII 艺术/树状图/JSON等编码攻击绕过文本过器──
>  **【类比】**亚斯基亚越狱 = "隐形墨水"――安全过器看无害的标点网格,模型视觉理解为一个词――艺术提示ACL 2024:GPT-4/Gemini/Claude/Llama-2 全失败,>75% 攻击成功率――绕过PPL 过、改写、重代币 化防御――结构性变种(结构性Sleight) 扩展到树/图/嵌套 JSON所有非语义视觉提示都是攻击面――

## 学习目标

- 描述ArtPrompt攻击:字符识别步骤,ASCII-art替代,最后的罩提示.

> 描述ArtPrompt 攻击:词识别步骤、ASCII 艺术替换、最终伪装提示──

- 解释为什么标准防御 (PPL,抛物线,重定性) 在ArtPrompt上失败.

> 解释为什么标准防御(困惑度过、释义、重新分词) 在ArtPrompt上失败──

- 定义ViTC并描述它衡量什么.

> 定义ViTC并描述它衡量的内容.

- 描述 StructuralSleight作为任意不常见文本编码结构的通用化.

> 描述结构性 作为对任意罕见文本编码结构的推广.

## 问题问题

通过抛词和角色扮演 (课 12) 和通过长文本 (课 13) 攻击运行在文本级别的模式上.ArtPrompt 在识别级别上运行:模型不会分析禁止的代币.它分析以字符呈现的图像.安全过器看到无害的分类.模型看到一个词.

> 通过释义和角色扮演 (Lection 12) 和长上下文 (Lection 13) 的攻击在文本级模式上操作.

## 概念的概念

> **【中文解读】**艺术简单 两步攻击的细节:第一步给定有害请求,使用LLM 识别安全相关词语(如"炸弹"在"如何制作炸弹"中);第二步将每个识别词换为其ASCII 艺术染(7x5或7x7 字符块形成字母形状) ;;模型收到标点和空格网格,足够强大的模型可以识别为词;安全过器只看到网格;;

### 艺术即时,两个步骤

步骤 1. 词识别. 鉴于有害的请求,攻击者使用LLM识别安全相关的词 (例如"如何制造炸弹"中的"炸弹").

步骤 2. 隐藏的即时生成.将每个已识别的字体取代为ASCII艺术染 (一个7x5或7x7字符块形成字母形状).模型收到一个符号格格和一个足够有能力的模型可以识别的空间格格;安全过器只看到格格.

结果:GPT-4,双胞胎,克劳德,拉马-2,GPT-3.5都失败.攻击成功率超过75%在他们的基准子集.

> 结果:GPT-4、Gemini、Claude、Llama-2、GPT-3.5 全部失败──攻击成功率在基准子集上超过75%──

> **【拓展：防御失败 → 多层安全启示】**困惑度过器失败是因为合法结构化输入也得分高;释义失败是因为释义 LLM 常保留或重建ASCII 艺术;重新分词失败是因为识别是视觉的而不是令牌级的――安全必须泛化到模型能解析的所有结构化表示这个集合很大并且正在增长――

### 为什么标准防御系统失败

- **PPL (perplexity filter).**亚斯基艺术具有高度的困惑,但所有新型输入都如此.阻碍ArtPrompt的门选择也阻碍了合法结构化输入.

> **困惑度过滤。**艺术具有高困惑度,但所有新输入也是如此.

- **Paraphrase.**实际上,抛词 LLM 往往保存或重建艺术.

> **释义。**释义提示会破坏ASCII艺术――实际上,释义 LLM 常常保留或重建艺术――

- **Retokenization.**通过不同方式分开代币,并不会改变模型的视觉识别字母形状.

> **重新分词。**不同地分令牌不会改变模型的视觉在识别字母形状的事实.

基本问题是安全过器是代币或语义级别;

> 根本问题是安全过器在令牌或语义级操作中;ArtPrompt在视觉识别级操作中.

> **【中文解读】**维特斯基准:ArtPrompt的有效性与模型读视觉文本的能力相关ViTC准确率越来越高,ArtPrompt越有效.

### 维特证指标

识别非语义视觉提示.测量模型阅读ASCII-art,wingdings和其他非文本语义视觉内容的能力.ArtPrompt的有效性与ViTC准确性有关:模型阅读视觉文本越好,ArtPrompt就更好地处理它.这是能力和安全性妥协.

> 非语义视觉提示的识别――衡量模型读取ASCII 艺术、 Wingdings 和其他非文本语义视觉内容的能力――ArtPrompt的有效性与 ViTC 准确率相关:模型读取视觉文本越好,ArtPrompt 效果越好――这是能力-安全权衡――

### 结构性

概括了ArtPrompt:不常见的文本编码结构 (UTES).树木,图形,嵌入式JSON,CSV-in-JSON,不同风格的代码块.如果一个结构在训练安全数据中很少存在,但可以通过模型解析,它可以隐藏有害内容.

> 推广 ArtPrompt:罕见文本编码结构(UTES) ――树、图、嵌套 JSON、JSON 中的 CSV、不同风格代码块──如果一个结构在训练安全数据中罕见但模型可解析,它可以隐藏有害内容──

防守的含义:安全必须在模型可以分析的结构性表示中概括.

> 防御启示:安全必须泛化到模型能解析的所有结构化表示.

### 图像模拟性

视觉LLM (GPT-5.2,双子座3 Pro,克劳德·奥普斯 4.5,格罗克 4.1) 扩大了攻击表面.使用实际图像的ArtPrompt类型攻击比ASCII艺术类型更强,因为图像编码器产生更丰富的信号.

> 视觉 LLM 扩大了攻击面──使用实际图像的ArtPrompt 式攻击比ASCII更强,因为图像编码器产生更丰富的信号──

### 在这个阶段的第18阶段

课时12-14描述了三种直角攻击向量:反复精炼 (PAIR),文本长度 (MSJ) 和编码 (ArtPrompt/StructuralSleight).课时15从模型中心攻击转向系统边界攻击 (间接提示注射).课时16描述了防御工具响应.

> 课时12-14 描述三个正交攻击向量:代改进 (PAIR) 、上下文长度(MSJ) 和编码(ArtPrompt/StructuralSleight) ・课时15 从模型中心攻击转向系统边界攻击――课时16 描述防御工具响应――

> **【拓展：视觉 LLM → 攻击面扩展】**视觉 LLM(GPT-5.2, Gemini 3 Pro,Claude Opus 4.5,Grok 4.1) 扩大了攻击面面──ArtPrompt式攻击使用实际图像比ASCII更强,因为图像编码器产生更丰富的信号──ViTC基准的相关性意味着提高多模态能力同时增加编码攻击的脆弱性.

## 用它使用方法
```figure
al-ascii-cloak
```

## 用它

`code/main.py`您可以用ASCII艺术字体掩盖一个有害查询中的特定字符,验证被掩盖的字符串通过关键字过器,并 (可选) 使用简单的识别器重新解码被掩盖的字符串.

> `code/main.py`构建一个玩具ArtPrompt──你可以使用ASCII 艺术字形伪装有害查询中的特定词,验证伪装字符串通过关键词过,并(可选地) 使用简单识别器解码──

## 发射上线

这一课产生了`outputs/skill-encoding-audit.md`鉴于 jailbreak防守报告,它列出了包含的编码攻击家族 (ASCII艺术,base64,Leet-speak,UTF-8同形字体,UTES) 和每个攻击的防守层.

> 本课产出发 `outputs/skill-encoding-audit.md`提供监狱防守报告,列举覆盖的编码攻击家族和每个对应的防守层.

## 练习题

1. 跑步`code/main.py`检查被掩盖的字符串通过简单的关键字过器. 报告所需的字符级别变化.

2. 实现第二个编码:base64用于相同的目标词. 比较过率与ArtPrompt和恢复难度.

3. 阅读江等人2024节4.3 (五个模型结果).提出克劳德的ArtPrompt抵抗力为什么在同一基准上高于双子座的原因.

4. 设计一个预生成防御,可以在提示中检测到ASCII艺术形状的区域. 测量合法代码,表格和数学符号上的虚假阳性率.

5. 结构Sleight列出了10个编码结构. 绘制一个处理10个的通用防御,并估计每一个被防御的提示的计算成本.

## 关键词 关键词

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| ArtPrompt | "the ASCII-art attack" | Two-step jailbreak that masks safety words with ASCII-art renderings |
| Cloaking | "hide the word" | Replace a forbidden token with a visual representation the model reads but the filter does not |
| UTES | "uncommon structure" | Uncommon Text-Encoded Structure — tree, graph, nested JSON, etc. used to smuggle content |
| ViTC | "visual-text capability" | Benchmark for model's ability to read non-semantic visual encoding |
| Perplexity filter | "PPL defense" | Reject prompts with high perplexity; fails because legitimate structured input also scores high |
| Retokenization | "tokenizer shift defense" | Pre-process the prompt with a different tokenizer; fails because recognition is visual |
| Homoglyph | "lookalike characters" | Unicode characters that look identical to Latin letters; bypass substring checks |

## 继续阅读 继续阅读

- [Jiang et al. — ArtPrompt (ACL 2024, arXiv:2402.11753)](https://arxiv.org/abs/2402.11753)ASCII艺术的破解监狱文件
- [Li et al. — StructuralSleight (arXiv:2406.08754)](https://arxiv.org/abs/2406.08754) UTES通用化
- [Chao et al. — PAIR (Lesson 12, arXiv:2310.08419)](https://arxiv.org/abs/2310.08419)补充反复攻击
- [Anil et al. — Many-shot Jailbreaking (Lesson 13)](https://www.anthropic.com/research/many-shot-jailbreaking)补充长度攻击
