# رمزية الكلمات الفرعية  BPE، WordPiece، Unigram، جملةقطع  子词分词  BPE、WordPiece、SentencePiece

> الـ "توكينيزر" الكلمات يختنقون بالكلمات غير المرئية، الـ "توكينيزر" الشخصيات ينفجر طول التسلسل، الـ "توكينيزر" الكلمات الفرعية، كل درجة ماجستير في العلوم الحديثة تُركب على واحدة.
> 词级分词器在未见词上卡住──字符分词器爆炸序列长度──子词分词器取中间值──每现代 LLM 都用子词分词──

> **【中文解读】**BPE هو GPT 用的分词算法,WordPiece هو BERT 用的──

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 5 · 04 (GloVe / FastText / Subword) | **前置知识:** Phase 5 · 01（文本处理），Phase 5 · 04（GloVe / FastText / 子词）
**Time:** ~60 minutes | **时间:** ~60 分钟

## المشكلة المشكلة المشكلة

قاموسك يحتوي على 50 ألف كلمة، يكتب المستخدم "غير قابل للتوجه"`[UNK]`النموذج الآن لا يحتوي على إشارة حول الكلمة. والأسوأ: الوثيقة التي تبلغ 90 في المائة في جسمك تحتوي على 40 كلمة نادرة، مما يعني 40 جزء من المعلومات التي تم إسقاطها لكل وثيقة.

> لديك 50،000 كلمة. المستخدم يستخدمها "غير قابلة للتأثير".`[UNK]` لا يوجد أي إشارة لهذا الكلمة الآن. أسوأ من ذلك: في المقالة التاسعة والعشرين في المئة من المواد، هناك 40 كلمة نادرة، مما يعني أن كل مادة من المقالة قد فقدت 40 كلمة.

> **【中文解读】**السؤال الذي يطرحه هذا القسم هو: كيف يمكن فهم هذه التقنية بشكل صحيح وتطبيقها في التجهيز العملي. فهم السياق يساعد على فهم النوع المختص من التكنولوجيا. في النظام الواقعي الذكاء الاصطناعي، فإن التكنولوجيا الخطأ غالباً ما تكون أكثر تكلفة من التنفيذ التفصيلي.

تُحلّ رمزية الكلمات الفرعية هذا. الكلمات الشائعة تبقى رموزًا واحدةً. الكلمات النادرة تتفكّك إلى قطع ذات معنى: `untokenizable``un`،`token`،`izable`بيانات التدريب تغطي كل شيء لأن أي سلسلة هي في نهاية المطاف تسلسل من البايتز.

> 子词分词 حل هذا المشكلة.`untokenizable``un`.`token`.`izable`تعليميات تغطي كل شيء، لأن أي حروف تكون في النهاية سلسلة حروف

كل ماجستير في مجال الحدود في عام 2026 يتم شحنها على واحد من ثلاثة خوارزميات (BPE، Unigram، WordPiece) ، مغلفة في واحدة من ثلاث مكتبات (tiktoken، SentencePiece، HF Tokenizers). لا يمكنك شحن نموذج لغة دون اختيار واحد.

> 2026 سنة كل قبل الدرجة العليا المتميزة على أساس ثلاثة خوارزميات واحدة ((BPE、Unigram、WordPiece) ، المعبأة في ثلاثة مجموعات واحدة ((Tiktoken、SentencePiece、HF Tokenizers)

## المفهوم الأساسي

> **【中文解读】**هذا المقطع يعرض المفاهيم والنظريات الأساسية. فهم هذه المفاهيم هو شرط لتحقيق التنفيذ التالي، وكذلك النقاط المعرفة في المقابلة والممارسة التجريبية.

![BPE vs Unigram vs WordPiece, character-by-character](../assets/subword-tokenization.svg)

**BPE (Byte-Pair Encoding).**ابدأ بمفردات على مستوى الأحرف، احصي كل زوج مجاور، دمج الزوج الأكثر تكرارًا في رمز جديد، كرر حتى تصل إلى حجم المفردات المستهدفة. الخوارزمية السائدة: GPT-2/3/4, Llama, Gemma, Qwen2, Mistral.

> **BPE（字节对编码）。**من الكلمات الصفرية لغة البداية. 统计每个相邻对. 将最频繁的对合并为新代币. 重复直到达到目标词表大小. 主导算法:GPT-2/3/4 拉马 格玛 格温  导语

**Byte-level BPE.**نفس الخوارزمية ولكن أكثر من البايتات الخام (256 رمزاً أساسية) بدلاً من أحرف يونيكود. الضمانات صفر `[UNK]`الوهم  أي رموز تسلسل البايت. GPT-2 تستخدم 50,257 رمزا (256 بايت + 50,000 دمج + 1 خاص).

> **字节级 BPE。**مشابهة للخوارزمية ولكن في الخطوط الأصلية ((256 个基础 token) بدلا من اليونيكود 字符上──保证零 `[UNK]`رمز  任何字节序列都可编码──GPT-2 使用 50,257 个代币──

**Unigram.**تبدأ مع مجموعة كبيرة من المفردات. تعيين لكل رمز احتمال واحد. تعيد قطع رموز التي يزيد إزالتها على الأقل من احتمالات سجل الجسم. احتمالية في الاستنتاج: يمكن أن تجريب رموز. يستخدمها T5 ، mBART ، ALBERT ، XLNet ، Gemma.

> **Unigram。**من الكلمات الكبيرة تبدأ. إلى كل رمز تمتدّل المفردات  احتمالية. بعد نقل الأغصان إلى المواد على عدد المشاركين زيادة أقل من الـ توكنات.

**WordPiece.**مزيج أزواج التي تعزز احتمالات جسم التدريب بدلا من التردد الخام.

> **WordPiece。**合并使训练语料似然最大化而非原始频率最高对──用于BERT、DistilBERT、ELECTRA──

**SentencePiece vs tiktoken.**SentencePiece هي المكتبة التي * تدرب* المفردات (BPE أو Unigram) مباشرة على نص يونيكود الخام، وتشفير الفضاء الأبيض على شكل `▁`. tiktoken هو *مُشفّر * سريع OpenAI ضد المفردات المُبنية مسبقاً؛ فإنه لا يتدرب.

> **SentencePiece vs tiktoken。**SentencePiece هو في المجموعة الأصلية من الكلمات المتعددة في Unicode`▁` التوكن هو OpenAI 针对预构建词表的快速*编码器*;它不训练──

قاعدة عامة:

> 经验法则:

- **Training a new vocabulary:**SentencePiece (متعددة اللغات، لا توكنيزية مسبقة) أو HF Tokenizers.
  **训练新词表：**جملة (Piece) ((多语言,无预分词) أو (HF Tokenizers)).
- **Fast inference against GPT vocab:**تيكتون (cl100k_base، o200k_base).
  **针对 GPT 词表的快速推理：**تيكتون
- **Both:**HF Tokenizers  مكتبة واحدة، تدريب + خدمة.
  **两者兼有：**إتش إف توكيينرز   库, تدريب + 服务。

> **【中文解读】**هذا المقطع من خلال الكود من الصفر لتحقيق الخوارزمية النووية. هذا النوع من "من الصفر" يمكن أن يساعد على فهم المبدأ الخلفي للإطار، عندما يواجهون مشكلة لن يتم تعقلها في الصندوق الأسود.
```figure
bpe-merge
```

## بناءها

> **【拓展：大语言模型的工程实践】**من GPT إلى ChatGPT، تمر NLP من "كل مهمة تدريب نموذج" إلى "نموذج حل جميع المهام" التحول النموذجية. في المشاريع العملية، تحتاج نشر LLM إلى النظر في إيقاع الاختيارات التوقيتية التأخير التكلفة والتحقق الأمني وغيرها من المشاكل.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) هي الهيكل الأكثر شعبية في التطبيقات التجارية للذكاء الاصطناعي: سوف يطلب المستخدم أولاً الاختبار المستندات ذات الصلة، ثم يبحث عن نتائج الاختبار كإجابة على الجامعة.

> **【拓展：NLP 的多语言挑战】**في جميع أنحاء العالم هناك 7000 + من اللغات، ولكن دراسة اللغة غير اللغوية تركز بشكل رئيسي على اللغة الإنجليزية وغيرها من اللغات.

## بناء ذلك تحرك لتحقيق

> **【中文解读】**هذا المقطع من خلال الكود من الصفر لتحقيق الخوارزمية النووية. هذا النوع من "من الصفر" يمكن أن يساعد على فهم المبدأ الخلفي للإطار، عندما يواجهون مشكلة لن يتم تعقلها في الصندوق الأسود.

### الخطوة الأولى: BPE من الصفر

```python
from collections import Counter, defaultdict


def train_bpe(corpus, vocab_size, special_tokens=None):
    """Train BPE tokenizer from a list of pre-tokenized word strings."""
    special_tokens = special_tokens or ["<unk>"]
    word_freqs = Counter(corpus)
    splits = {word: list(word) for word in word_freqs}
    merges = {}

    while len(special_tokens) + len(set(t for parts in splits.values() for t in parts)) + len(merges) < vocab_size:
        pair_counts = Counter()
        for word, freq in word_freqs.items():
            symbols = splits[word]
            for i in range(len(symbols) - 1):
                pair_counts[(symbols[i], symbols[i + 1])] += freq
        if not pair_counts:
            break
        best = max(pair_counts, key=pair_counts.get)
        new_token = best[0] + best[1]
        merges[best] = new_token
        for word in splits:
            symbols = splits[word]
            new_symbols = []
            i = 0
            while i < len(symbols):
                if i < len(symbols) - 1 and (symbols[i], symbols[i + 1]) == best:
                    new_symbols.append(new_token)
                    i += 2
                else:
                    new_symbols.append(symbols[i])
                    i += 1
            splits[word] = new_symbols
    return merges, special_tokens


def bpe_encode(text, merges, special_tokens):
    """Encode text using learned BPE merges."""
    tokens = list(text)
    for (a, b), merged in merges.items():
        new_tokens = []
        i = 0
        while i < len(tokens):
            if i < len(tokens) - 1 and tokens[i] == a and tokens[i + 1] == b:
                new_tokens.append(merged)
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1
        tokens = new_tokens
    return tokens
```

أمر الاندماج مهم. يطبق BPE الاندماج في ترتيب التدريب، لذلك فإن الاندماج السابق يخلق رموز أطول تحجب الآخرين. لهذا السبب لا يمكن نقل مفردات BPE عبر النماذج.

> 合并顺序很重要──BPE 按训练顺序应用合并,所以较早的合并创建更长的代币,阻止后续合并──这就是为什么BPE 词表不能跨模型移植──

### الخطوة 2: التكنولوجيا مع تيكتون و SentencePiece

```python
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")
tokens = enc.encode("Hello, world!")
print(tokens)           # [9906, 11, 1917, 0]
print(enc.decode(tokens))  # Hello, world!
```

```python
import sentencepiece as spm

spm.SentencePieceTrainer.train(input="corpus.txt", model_prefix="m", vocab_size=1000)
sp = spm.SentencePieceProcessor(model_file="m.model")
print(sp.encode("Hello world", out_type=str))  # ['▁Hello', '▁world']
```

### الخطوة الثالثة: مقارنة الخصوبة

```python
def fertility(text, tokenizer_fn):
    return len(tokenizer_fn(text))

# BPE on English: ~1.3 tokens/word
# BPE on Hindi: ~3.5 tokens/word
# BPE on Amharic: ~8 tokens/word
```

> **【中文解读】**هذا المقال يوضح كيفية استخدام إطار متقدم مثل PyTorch、HuggingFace وغيرها) سريعة تطبيق هذه التقنية.

> **【拓展：Prompt Engineering 与 LLM 应用】**أصبحت الهندسة السريعة مهارات أساسية لمهندسين النمط النووي. من الصفر إلى القليل من الأسلحة، من سلسلة التفكير إلى رد الفعل، تطبق استراتيجيات التفاصيل المختلفة على مختلف المواقف.

## استخدمها في إطار التنفيذ

اختر حسب النظام البيئي

> 按生态系统选择──

- **OpenAI models (GPT-4, GPT-4o):**تيكتون. إعادة إنتاج سريعة ودقيقة لتكنولوجيا OpenAI. / tiktoken──快速、精确复现 OpenAI 分词──
- **Multilingual / custom training:**جملة قطعة. تدرب من النص الخام، تتعامل مع أي نص. / جملة قطعة.
- **Hugging Face models:**أوتوتوكينيزر. يلف الخلفية اليمنى تلقائيا. / أوتوكينيزر.
- **Maximum speed at inference:**HF Tokenizers (Rust backend) أو tiktoken (Python + C). / 推理最高速度:HF Tokenizers 或 tiktoken。

> **【中文解读】**هذا المادة يركز على كيفية نشر النموذج كمنتج متاح. من النموذج الأصلي إلى النظام في مرحلة الإنتاج، تحتاج إلى النظر في العديد من الخصائص في تحسين الأداء والتعامل الخاطئ والتحكم.

## أرسلها .

إبقوا`outputs/prompt-tokenizer-picker.md`:

> 保存为 `outputs/prompt-tokenizer-picker.md`:

```markdown
---
name: tokenizer-picker
description: Pick the right tokenizer for a given model or training pipeline.
phase: 5
lesson: 19
---

Given a model family or training goal, output:

1. Algorithm. BPE (GPT family), Unigram (T5 family), WordPiece (BERT family).
2. Library. tiktoken (GPT inference), SentencePiece (training), HF Tokenizers (both).
3. Vocabulary size and its impact on context window utilization.
4. Fertility estimate for the target language(s).

Refuse to mix tokenizer families in the same pipeline without explicit encode/decode boundaries.
```

> **【中文解读】**练题按照易/中级/Hard 三个难度递进──建议至少完成 级级中级的题目,Hard 级适合深入研究或面试准备──

## تمارين التدريب

1. **Easy.**تدريب BPE على مجموعة صغيرة (1000 كلمة) تشفير و فك رمز 20 كلمة اختبار. التحقق من الوفاء رحلة ذهاب وإياب. / **简单。**في التدريب على لغات صغيرة BPE 编码解码 20 个测试词──验证往返保真度──
2. **Medium.**مقارنة خصوبة التوجيهات للإنجليزية والصينية والهندية باستخدام cl100k_base من tiktoken. تقرير الوهم لكل كلمة لكل. / **中等。**استخدام تيكتون مقارنة الإنجليزية والصينية والهندية 分词繁殖率──报告每种语言的每字代标号数──
3. **Hard.**قم بتدريب نموذج SentencePiece Unigram على مجموعة مختلطة من الإنجليزية والهندية. مقارنة الخصوبة مع نموذج BPE المدرب على نفس البيانات. / **困难。**في المزيج من اللغة الإنجليزية الهندية على المواد اللغة التدريبة جملة قطعة واحد النسخة 模型── مع BPE 模型 التدريب على نفس البيانات مقارنة معدل التكاثر──

> **【中文解读】**في لغة "ما يقوله الناس" مقابل "ما يعنيه في الواقع" تم التمييز بين لغة اليومية والتقنية المحددة.

## شروط الرئيسية

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| BPE（字节对编码） | GPT's tokenizer / GPT 的分词器 | Iteratively merge most frequent adjacent pairs. / 迭代合并最频繁的相邻对。 |
| Unigram | T5's tokenizer / T5 的分词器 | Prune tokens from large vocabulary by likelihood. / 按似然从大词表剪枝。 |
| WordPiece | BERT's tokenizer / BERT 的分词器 | Merge pairs that maximize corpus likelihood. / 合并使语料似然最大化的对。 |
| SentencePiece | Training library / 训练库 | Train BPE or Unigram on raw text. Encodes whitespace as `▁`. / 在原始文本上训练 BPE 或 Unigram。 |
| tiktoken | OpenAI's encoder / OpenAI 编码器 | Fast encoding against pre-built GPT vocabularies. / 针对预构建 GPT 词表的快速编码。 |
| Fertility（繁殖率） | Tokens per word / 每词 token 数 | How many subword tokens a word produces. Lower is better. / 一个词产生多少子词 token。越低越好。 |

> **【中文解读】**延伸阅读 يوفر موارد عالية الجودة للتعلم المتعمق.

## المزيد من القراءة

- [Sennrich et al. (2016). Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909)ورقة BPE. / BPE 论文。
- [Kudo (2018). Subword Regularization](https://arxiv.org/abs/1804.10959)ورقة يونيغرام.
- [SentencePiece documentation](https://github.com/google/sentencepiece) التدريب والخدمة. / 訓練和服務。
- [tiktoken](https://github.com/openai/tiktoken) إشارة سريعة OpenAI. / OpenAI 快速分词器──
- [Hugging Face Tokenizers](https://huggingface.co/docs/tokenizers/) تدريب مدعوم بالصدأ + خدمة. / Rust 后端训练 + 服务。
