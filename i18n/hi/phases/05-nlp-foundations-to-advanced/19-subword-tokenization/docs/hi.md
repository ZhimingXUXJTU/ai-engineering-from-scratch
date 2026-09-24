# उपशब्द टोकनाइज़ेशन  BPE, WordPiece, Unigram, SentencePiece  子词分词  BPE、WordPiece、SentencePiece

> शब्द टोकन बनाने वाले अदृश्य शब्दों पर थूक जाते हैं। वर्ण टोकन करने वाले अनुक्रम की लंबाई को बढ़ा देते हैं। उपशब्द टोकन करने वाले अंतर को विभाजित करते हैं। हर आधुनिक LLM एक पर जहाज करता है।
> 词级分词器在未见词上卡住──字符分词器爆炸序列长度──子词分词器取中值──每现代 LLM 都用子词分词──

> **【中文解读】**बीपीई जीपीटी उपयोग का分词算法 है, वर्डपीस उपयोग का BERT है

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 5 · 04 (GloVe / FastText / Subword) | **前置知识:** Phase 5 · 01（文本处理），Phase 5 · 04（GloVe / FastText / 子词）
**Time:** ~60 minutes | **时间:** ~60 分钟

## समस्या  समस्या परिचय

आपके शब्दावली में 50,000 शब्द हैं। एक उपयोगकर्ता टाइप करता है "अनटोकनेज"। आपका टोकनेज़र वापस आता है।`[UNK]`. मॉडल में अब शब्द के बारे में कोई संकेत नहीं है. और इससे भी बदतर: आपके कॉर्पस में 90वें प्रतिशत दस्तावेज़ में 40 दुर्लभ शब्द हैं, जिसका अर्थ है कि प्रति दस्तावेज़ 40 बिट्स की जानकारी गिर गई है.

> आपके शब्द का नाम है 50,000 个词―― उपयोगकर्ता "असंज्ञनीय" में प्रवेश करे――आपका分词器 वापसी `[UNK]`◊ मॉडल अब इस शब्द के लिए कोई संकेत नहीं है। इससे भी बदतर यह हैः भाषा सामग्री में 90 वीं प्रतिशत के दस्तावेजों में 40 दुर्लभ शब्द हैं, जिसका अर्थ है कि प्रत्येक दस्तावेज में 40 जानकारी खो गई है।

> **【中文解读】**इस खंड में प्रश्न उठे हैं कि इस तकनीक को वास्तविक इंजीनियरिंग में सही ढंग से कैसे समझा जाए और लागू किया जाए।

उपशब्द टोकनकरण इस समस्या का समाधान करता है. सामान्य शब्द एकल टोकन बने रहते हैं. दुर्लभ शब्द सार्थक टुकड़ों में विघटित होते हैंः`untokenizable`→ `un`,`token`,`izable`प्रशिक्षण डेटा सब कुछ शामिल है क्योंकि किसी भी स्ट्रिंग अंततः बाइट्स का एक अनुक्रम है।

> 子词分词 solve this problem──常见词保持单个标志──罕见词分解为有意义的片段:`untokenizable`→ `un``token``izable` प्रशिक्षण डेटा सब कुछ कवर, क्योंकि किसी भी वर्ण अंततः वर्ण क्रम हैं

2026 में हर फ्रंटियर एलएलएम तीन एल्गोरिदम (बीपीई, यूनिग्राम, वर्डपीस) में से एक पर जहाज करता है, तीन पुस्तकालयों (टिकटोकन, सेंटेन्सपीस, एचएफ टोकनइज़र) में से एक में लपेटा जाता है। आप एक चुनने के बिना भाषा मॉडल नहीं भेज सकते।

> 2026 के प्रत्येक अग्रिम LLM के लिए तीन प्रकार के एल्गोरिदमों में से एक (BPE, Unigram, WordPiece) पर आधारित है, जो कि तीन प्रकार के संग्रहों में से एक (टिकटोकन, सेन्टेन्सपीस, एचएफ टोकन बनाने वालों) में से एक है।

## अवधारणा का मूल अवधारणा

> **【中文解读】**इस भाग में मूल अवधारणाओं और सिद्धांतों की आधारभूत जानकारी दी गई है। इन अवधारणाओं को प्राप्त करना बाद में होने वाली प्रक्रियाओं के लिए एक शर्त है।

![BPE vs Unigram vs WordPiece, character-by-character](../assets/subword-tokenization.svg)

**BPE (Byte-Pair Encoding).**वर्ण स्तर की शब्दावली से शुरू करें. प्रत्येक आसन्न जोड़ी की गणना करें. सबसे अधिक बार होने वाली जोड़ी को नए टोकन में मिलाएं. जब तक आप लक्ष्य शब्दावली आकार को नहीं प्राप्त करते तब तक दोहराएं। प्रभुत्व वाला एल्गोरिथ्मः GPT-2/3/4, Llama, Gemma, Qwen2, Mistral।

> **BPE（字节对编码）。**से字符级词表开始──统计每个相邻对对──将最频繁的对合并为新代币──重复直到达到目标词表大小──主导算法:GPT-2/3/4、Llama、Gemma、Qwen2、Mistral──

**Byte-level BPE.**वही एल्गोरिथ्म लेकिन यूनिकोड वर्णों के बजाय कच्चे बाइट्स (256 बेस टोकन) पर।`[UNK]`टोकन  किसी भी बाइट अनुक्रम कोड। GPT-2 50,257 टोकन (256 बाइट + 50,000 विलय + 1 विशेष) का उपयोग करता है।

> **字节级 BPE。**समान एल्गोरिथ्म पर मूल में{\displaystyle \mathbb {\mathbb {\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathbb}{\mathb}{\mathbb}{\mathb}{\mathb}{\mathb}{\mathbright}{\mathbright}{\mathbright}{\mathbright}{\mathbright}{{{{{{{{{{{{{{{{{{{{{{{{{}}}}}}}}}}}}}}}{{{{{}}}}}}}}}{{{{{}}}}}}}}}{{{{{}}}}}}}}}{{{{}}}}}}}}}{{{{{}}}}}}}}}}}}}{{{{{{}}}}}}}}}}}}}}}}{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}}}{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}{{{{{{{{{{{}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}}`[UNK]`टोकन  任何字节序列都可编码──GPT-2 使用 50,257 个 टोकन──

**Unigram.**एक विशाल शब्दावली से शुरू करें. प्रत्येक टोकन को एक एकल-सूची की संभावना असाइन करें. प्रतिवर्ती रूप से टोकन काटें जिनकी हटाने से कॉर्पस लॉग-संभावना कम से कम बढ़ जाती है। निष्कर्ष पर संभावनाः टोकन के नमूने कर सकते हैं। T5, mBART, ALBERT, XLNet, Gemma द्वारा उपयोग किया जाता है।

> **Unigram。**                                                                                                                                                                                                                                                              

**WordPiece.**मिश्रण जोड़े जो कच्चे आवृत्ति की बजाय प्रशिक्षण corpus की संभावना को अधिकतम करते हैं।

> **WordPiece。**合并使训练语料似然最大化而非原始频率最高对──用于BERT、DistilBERT、ELECTRA──

**SentencePiece vs tiktoken.**SentencePiece वह पुस्तकालय है जो *ट्रेन* शब्दावली (बीपीई या यूनोग्राम) को सीधे कच्चे यूनिकोड पाठ पर, श्वेत क्षेत्र को कोडिंग के रूप में `▁`. tiktoken पूर्व निर्मित शब्दावली के खिलाफ OpenAI का तेज *encoder* है; यह प्रशिक्षण नहीं देता है।

> **SentencePiece vs tiktoken。**SentencePiece is in मूल यूनिकोड 文本上* प्रशिक्षण* शब्द表的库,将空格编码为 `▁` टिक टोकन एक ओपन एआई है                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    

अंगूठे का नियमः

> 经验法则:

- **Training a new vocabulary:**SentencePiece (बहुभाषी, कोई पूर्व-टोकनाइज़ेशन नहीं) या HF Tokenizers।
  **训练新词表：**वाक्यपीस ((多语言,无预分词) या एचएफ टोकनाइजर्स。
- **Fast inference against GPT vocab:**tiktoken (cl100k_base, o200k_base) ।
  **针对 GPT 词表的快速推理：**टिक्टोकन
- **Both:**एचएफ टोकनेजर्स  एक पुस्तकालय, प्रशिक्षण + सेवा।
  **两者兼有：**एचएफ टोकन बनाने वाले  एक भंडार, प्रशिक्षण + 服务。

> **【中文解读】**इस भाग के माध्यम से कोड को शून्य से लागू किया जा सकता है कोर एल्गोरिदम। इस तरह के "शुरुआत से" तरीके से फ्रेमवर्क के पीछे के सिद्धांत को समझने में मदद मिलेगी, समस्याओं का सामना करते समय ब्लैक बॉक्स में फंस नहीं जाएगा।
```figure
bpe-merge
```

## इसे बनाओ

> **【拓展：大语言模型的工程实践】**जीपीटी से चैटजीपीटी, एनएलपी के क्षेत्र में "प्रत्येक कार्य को प्रशिक्षित करने के लिए एक मॉडल" से "एक मॉडल सभी कार्य को हल करने के लिए" के लिए एक प्रकार के परिवर्तन का अनुभव किया गया है।

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) वर्तमान उद्यम एआई 应用 में सबसे लोकप्रिय संरचना हैः उपयोगकर्ता पूछताछ पहले संबंधित दस्तावेज टुकड़े को जांचें, फिर से जांच परिणाम के रूप में ऊपर नीचे दिए गए LLM  生成答案── इस तरह LLM ज्ञान过时和幻觉问题──向量数据库── जैसे कि Milvus、Pinecone、Weaviate) RAG 系统 का मूल घटक है──

> **【拓展：NLP 的多语言挑战】**विश्व में 7000 से अधिक भाषाएं हैं, लेकिन एनएलपी अध्ययन मुख्य रूप से अंग्रेजी जैसे कुछ भाषाओं पर केंद्रित है।

## इसे बनाओ, इसे पूरा करो।

> **【中文解读】**इस भाग के माध्यम से कोड को शून्य से लागू किया जा सकता है कोर एल्गोरिदम। इस तरह के "शुरुआत से" तरीके से फ्रेमवर्क के पीछे के सिद्धांत को समझने में मदद मिलेगी, समस्याओं का सामना करते समय ब्लैक बॉक्स में फंस नहीं जाएगा।

### चरण 1: खरोंच से बीपीई

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

विलय क्रम महत्वपूर्ण है। बीपीई प्रशिक्षण क्रम में विलय लागू करता है, इसलिए पहले के विलय लंबे टोकन बनाते हैं जो बाद के टोकन को ब्लॉक करते हैं। यही कारण है कि बीपीई शब्दावली मॉडल के बीच पोर्टेबल नहीं होती है।

> 合并顺序很重要──BPE 按训练顺序应用合并,所以较早的合并创建更长的代币,阻止后续合并──这就是为什么BPE 词表不能跨模型移植──

### चरण 2: टिक टोकन और SentencePiece के साथ टोकनकरण

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

### चरण 3: प्रजनन क्षमता की तुलना

```python
def fertility(text, tokenizer_fn):
    return len(tokenizer_fn(text))

# BPE on English: ~1.3 tokens/word
# BPE on Hindi: ~3.5 tokens/word
# BPE on Amharic: ~8 tokens/word
```

> **【中文解读】**इस भाग में दिखाया गया है कि इस तकनीक को कैसे तेजी से लागू किया जाए। इस प्रकार के एक परिपक्व ढांचे का उपयोग करके बग कम किए जा सकते हैं और विकास दक्षता में सुधार किया जा सकता है।

> **【拓展：Prompt Engineering 与 LLM 应用】**शीघ्र इंजीनियरिंग  नेल्पी  इंजीनियरों के मूल कौशल बन गए हैं  शून्य-शॉट से लेकर कुछ-शॉट तक, सोच-विचार श्रृंखला से लेकर प्रतिक्रिया तक, विभिन्न सुझाव रणनीति विभिन्न परिदृश्यों के लिए लागू होती हैं                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

## इसे फ्रेमवर्क के साथ लागू करें

पारिस्थितिकी तंत्र के अनुसार चुनें।

> 按生态系统选择──

- **OpenAI models (GPT-4, GPT-4o):**tiktoken. OpenAI के टोकनकरण का त्वरित, सटीक पुनरुत्पादन. / tiktoken──快速、精确复现 OpenAI 分词──
- **Multilingual / custom training:**वाक्य टुकड़ा. कच्चे पाठ से ट्रेन, किसी भी स्क्रिप्ट को संभालता है. / वाक्य टुकड़ा.
- **Hugging Face models:**ऑटो टोकनराइज़र. स्वचालित रूप से दाएं बैकेंड को लपेटता है. / ऑटो टोकनराइज़र.
- **Maximum speed at inference:**HF टोकनाइज़र (रस्ट बैकेंड) या टिक टोकन (पायथन + सी) । / 推理最高速度:HF टोकनाइज़र या टिक टोकन。

> **【中文解读】**इस खंड में इस बात पर ध्यान दिया गया है कि मॉडल को उपलब्ध उत्पादों के रूप में कैसे तैनात किया जाए। मूल से लेकर उत्पादन स्तर तक, प्रदर्शन अनुकूलन, त्रुटि प्रसंस्करण, निगरानी आदि के कई आयामों पर विचार करने की आवश्यकता है।

## इसे भेजें उत्पाद

`outputs/prompt-tokenizer-picker.md`:

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

> **【中文解读】**练习题按照易/中级/难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## अभ्यास विषय

1. **Easy.**एक छोटे से कॉर्पस (1000 शब्दों) पर बीपीई को प्रशिक्षित करें। 20 परीक्षण शब्दों को एन्कोड और डिकोड करें। वापसी यात्रा की निष्ठा सत्यापित करें। / **简单。**️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️
2. **Medium.**टिकटोक के cl100k_base का उपयोग करके अंग्रेजी, चीनी और हिंदी के लिए टोकनकरण प्रजनन क्षमता की तुलना करें। प्रत्येक के लिए टोकन-प्रति-शब्द रिपोर्ट करें। / **中等。**उपयोग टिकटोक तुलना करें अंग्रेजी, चीनी और भारतीय भाषाओं में分词繁殖率―― रिपोर्ट प्रति भाषा में प्रत्येक शब्द टोकन संख्या――
3. **Hard.**एक मिश्रित अंग्रेजी-हिंदी कॉर्पस पर एक SentencePiece Unigram मॉडल को प्रशिक्षित करें। एक ही डेटा पर प्रशिक्षित बीपीई मॉडल के साथ प्रजनन क्षमता की तुलना करें। / **困难。**एक ही डेटा पर प्रशिक्षित बीपीई मॉडल के साथ तुलनात्मक प्रजनन दरों में।

> **【中文解读】**术语表中的"क्या लोग कहते हैं" बनाम "क्या वास्तव में इसका मतलब है" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──

## कीवर्ड्स  शब्द खोज तालिका

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| BPE（字节对编码） | GPT's tokenizer / GPT 的分词器 | Iteratively merge most frequent adjacent pairs. / 迭代合并最频繁的相邻对。 |
| Unigram | T5's tokenizer / T5 的分词器 | Prune tokens from large vocabulary by likelihood. / 按似然从大词表剪枝。 |
| WordPiece | BERT's tokenizer / BERT 的分词器 | Merge pairs that maximize corpus likelihood. / 合并使语料似然最大化的对。 |
| SentencePiece | Training library / 训练库 | Train BPE or Unigram on raw text. Encodes whitespace as `▁`. / 在原始文本上训练 BPE 或 Unigram。 |
| tiktoken | OpenAI's encoder / OpenAI 编码器 | Fast encoding against pre-built GPT vocabularies. / 针对预构建 GPT 词表的快速编码。 |
| Fertility（繁殖率） | Tokens per word / 每词 token 数 | How many subword tokens a word produces. Lower is better. / 一个词产生多少子词 token。越低越好。 |

> **【中文解读】**延伸阅读 प्रदान करता है गहन सीखने के लिए उच्च गुणवत्ता वाले संसाधनों। ये लेख और पाठ्यक्रम इस क्षेत्र के लिए क्लासिक संदर्भ हैं, जो गहन समझ की आवश्यकता वाले पाठकों के लिए उपयुक्त हैं।

## आगे पढ़ना 延伸閱讀

- [Sennrich et al. (2016). Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) बीपीई पेपर. / बीपीई 论文。
- [Kudo (2018). Subword Regularization](https://arxiv.org/abs/1804.10959) यूनिग्राम पेपर. / यूनिग्राम 论文。
- [SentencePiece documentation](https://github.com/google/sentencepiece) प्रशिक्षण और सेवा. / 訓練和服務。
- [tiktoken](https://github.com/openai/tiktoken) OpenAI का तेजी से टोकनराइज़र. / OpenAI 快速分词器──
- [Hugging Face Tokenizers](https://huggingface.co/docs/tokenizers/) रस्ट-आधारित प्रशिक्षण + सेवा। / रस्ट 后端 प्रशिक्षण + 服务。
