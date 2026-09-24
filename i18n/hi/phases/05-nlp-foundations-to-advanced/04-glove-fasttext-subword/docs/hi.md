# ग्लोव, फास्ट टेक्स्ट, और उपशब्द एम्बेडिंग

> Word2Vec ने प्रत्येक शब्द में एक एम्बेडिंग को प्रशिक्षित किया। ग्लोवे ने सह-अवसर मैट्रिक्स को कारक बनाया। फास्टटेक्स्ट ने टुकड़ों को एम्बेड किया। बीपीई ने ट्रांसफार्मरों से पुल बनाया।
> Word2Vec 为每一个词训练一个嵌入──GloVe 分解共现矩阵──FastText 嵌入词的组成部分──BPE 桥接到变压器──

> **【中文解读】**ग्लोवे का उपयोग करके संपूर्ण समकालीन आंकड़े, फास्टटेक्सट 处理子词解决 OOV 问题──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 03 (Word2Vec from Scratch) | **前置知识:** Phase 5 · 03（Word2Vec 从零实现）
**Time:** ~45 minutes | **时间:** ~45 分钟

## समस्या  समस्या परिचय

Word2Vec ने दो खुले प्रश्न छोड़े।

> Word2Vec  दो खुले प्रश्न  छोड़ दिया गया है

सबसे पहले, एक समानांतर शोध लाइन थी जो ऑनलाइन स्किप-ग्राम अपडेट करने के बजाय सीधे सह-घटना मैट्रिक्स (एलएसए, एचएएल) को कारगर करती थी। क्या वर्ड 2 वीईसी का पुनरावर्ती दृष्टिकोण मौलिक रूप से बेहतर था, या क्या अंतर दो तरीकों को संभालने के तरीके का एक कलाकृत्य था?**GloVe**उत्तर दिया किः एक ध्यान से चुना हानि के साथ मैट्रिक्स कारक मिलान या Word2Vec से अधिक है, और प्रशिक्षण के लिए कम लागत है।

> प्रथम, एक समवर्ती अध्ययन मार्ग है, सीधे समवर्ती रचने के लिए (LSA、HAL) , जो कि ऑनलाइन स्किप-ग्राम करने के बजाय बेहतर है, या केवल दो तरीकों से गणना करने के लिए मानव परिणामों में अंतर है?**GloVe**回答: संयोजन精心选择的损失函数的矩阵分解匹配或超过 Word2Vec,且训练成本较低──

दूसरा, किसी भी विधि में शब्दों के लिए एक कहानी नहीं थी जिसे उसने कभी नहीं देखा था।`Zoomer-approved`,`dogecoin`, पिछले सप्ताह का आविष्कार किया गया किसी भी उचित संज्ञा, दुर्लभ जड़ के प्रत्येक घुमावदार रूप।**FastText**यह n-ग्राम वर्णों को एम्बेड करके तय किया गयाः एक शब्द अपने हिस्सों का योग है, जिसमें मॉर्फेम शामिल हैं, इसलिए यहां तक कि शब्द संग्रह से बाहर शब्द एक समझदार वेक्टर प्राप्त करते हैं।

> दूसरा, दो प्रकार के शब्द हैं जिनका कभी सामना नहीं हुआ है।`Zoomer-approved``dogecoin`、上周刚造的任何专名词、稀有词根的每变形形式──**FastText**通过嵌入字符 n-gram 修复了这个问题:一个词是其各部分之和,包括语素,因此即使是词表外的词也能获得合理的向量──

तीसरा, जब ट्रांसफार्मर आए, तो सवाल फिर से बदल गया। शब्द स्तर की शब्दावली लगभग एक मिलियन प्रविष्टियों को कवर करती है; वास्तविक भाषा इससे अधिक खुली है। **Byte-pair encoding (BPE)**और उसके रिश्तेदारों ने अक्सर उपशब्द इकाइयों की एक शब्दावली को सीखकर यह हल किया जो सब कुछ कवर करता है। हर आधुनिक एलएलएम के लिए प्रत्येक आधुनिक टोकननाइज़र एक उपशब्द टोकननाइज़र है।

> तीसरा, जब ट्रांसफार्मर आया तो समस्या फिर से बदल गई।**字节对编码（Byte-Pair Encoding, BPE）** और उसके परिवर्तनों ने इस समस्या को हल किया है। प्रत्येक आधुनिक एमएलएम के प्रत्येक आधुनिक分词器 हैं।

यह सबक तीनों को बताता है, फिर बताता है कि किसको कब तक पहुंचना है।

> इस वर्ग में इन तीनों को एक-एक करके समझाएं, फिर समझाएं कि कब कौन सा उपयोग करना है।

## अवधारणा का मूल अवधारणा

> **【中文解读】**इस भाग में मूल अवधारणाओं और सिद्धांतों की आधारभूत जानकारी दी गई है। इन अवधारणाओं को प्राप्त करना बाद में होने वाली प्रक्रियाओं के लिए एक शर्त है।

**GloVe (Global Vectors).**शब्द-शब्द सह-प्रकृति मैट्रिक्स का निर्माण करें `X`कहाँ`X[i][j]`कितनी बार शब्द है `j`शब्द के संदर्भ में दिखाई देता है `i`. रेल वेक्टर ऐसे कि `v_i · v_j + b_i + b_j ≈ log(X[i][j])`वजन कम करने के लिए इतनी बार जोड़े प्रभुत्व नहीं है.

> **GloVe（全局向量）。**构建词-词共现矩阵 `X`, उनमें से `X[i][j]` 是词`j` 出现在词 `i`上下文中的频率── प्रशिक्षण向量使 `v_i · v_j + b_i + b_j ≈ log(X[i][j])`                                                                                                                                                                                                                                                              

**FastText.**एक शब्द अपने वर्ण n-ग्राम के योग है और शब्द स्वयं। `where`बन जाता है`<wh, whe, her, ere, re>, <where>`. शब्द वेक्टर उन घटक वेक्टरों का योग है. Word2Vec के रूप में प्रशिक्षित करें. लाभः अदृश्य शब्द (`whereupon`) ज्ञात n-ग्राम से बने होते हैं।

> **FastText。**एक शब्द है उसके वर्ण n-ग्राम 之和加上词本身──`where`变成 `<wh, whe, her, ere, re>, <where>`△ शब्द के आकार में ये तत्व होते हैं और △ जैसे Word2Vec एक ही तरह का प्रशिक्षण देते हैं।`whereupon`) से ज्ञात n-ग्राम 组合而成

**BPE (Byte-Pair Encoding).**प्रत्येक बाइट (या वर्ण) की शब्दावली से शुरू करें। कॉर्पस में प्रत्येक आसन्न जोड़ी को गिनें। सबसे अधिक बार होने वाली जोड़ी को नए टोकन में मिलाएं।`k`परिणाम: एक शब्दावली`k + 256`टोकन जहां आवृत्ति क्रम (`ing`,`tion`,`the`) एकल टोकन हैं और दुर्लभ शब्द परिचित टुकड़ों में टूट जाते हैं। प्रत्येक वाक्य कुछ टोकन में बदल जाता है।

> **BPE（字节对编码）。**से单个字节 (或字符) के शब्द表开始──统计语料 में प्रत्येक समीपस्थ प्रति के उद्भव की आवृत्ति── सबसे अधिक बार प्रति के नए टोकन के लिए एकत्रित होने का आवृत्ति──重复`k`अगला 代── परिणाम: एक `k + 256`个标志的词表,其中高频序列(`ing``tion``the`) एक ही प्रतीक है, दुर्लभ शब्द को परिचित टुकड़ों में विभाजित किया जाता है। प्रत्येक वाक्य को किसी न किसी रूप में विभाजित किया जा सकता है।

> **【拓展：大语言模型的工程实践】**जीपीटी से चैटजीपीटी, एनएलपी के क्षेत्र में "प्रत्येक कार्य को प्रशिक्षित करने के लिए एक मॉडल" से "एक मॉडल सभी कार्य को हल करने के लिए" के लिए एक प्रकार के परिवर्तन का अनुभव किया गया है।

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) वर्तमान उद्यम एआई 应用 में सबसे लोकप्रिय संरचना हैः उपयोगकर्ता पूछताछ पहले संबंधित दस्तावेज टुकड़े को जांचें, फिर से जांच परिणाम के रूप में ऊपर नीचे दिए गए LLM  生成答案── इस तरह LLM ज्ञान过时和幻觉问题──向量数据库── जैसे कि Milvus、Pinecone、Weaviate) RAG 系统 का मूल घटक है──

> **【拓展：NLP 的多语言挑战】**विश्व में 7000 से अधिक भाषाएं हैं, लेकिन एनएलपी अध्ययन मुख्य रूप से अंग्रेजी जैसे कुछ भाषाओं पर केंद्रित है।

## इसे बनाओ, इसे पूरा करो।

> **【中文解读】**इस भाग के माध्यम से कोड को शून्य से लागू किया जा सकता है कोर एल्गोरिदम। इस तरह के "शुरुआत से" तरीके से फ्रेमवर्क के पीछे के सिद्धांत को समझने में मदद मिलेगी, समस्याओं का सामना करते समय ब्लैक बॉक्स में फंस नहीं जाएगा।
```figure
n5-subword-merge
```

## इसे बनाओ

### ग्लोवेः सह-अवसर मैट्रिक्स को फैक्टरीज़ करें

```python
import numpy as np
from collections import Counter


def build_cooccurrence(docs, window=5):
    pair_counts = Counter()
    vocab = {}
    for doc in docs:
        for token in doc:
            if token not in vocab:
                vocab[token] = len(vocab)
    for doc in docs:
        indexed = [vocab[t] for t in doc]
        for i, center in enumerate(indexed):
            for j in range(max(0, i - window), min(len(indexed), i + window + 1)):
                if i != j:
                    distance = abs(i - j)
                    pair_counts[(center, indexed[j])] += 1.0 / distance
    return vocab, pair_counts


def glove_train(vocab, pair_counts, dim=16, epochs=100, lr=0.05, x_max=100, alpha=0.75, seed=0):
    n = len(vocab)
    rng = np.random.default_rng(seed)
    W = rng.normal(0, 0.1, size=(n, dim))
    W_tilde = rng.normal(0, 0.1, size=(n, dim))
    b = np.zeros(n)
    b_tilde = np.zeros(n)

    for epoch in range(epochs):
        for (i, j), x_ij in pair_counts.items():
            weight = (x_ij / x_max) ** alpha if x_ij < x_max else 1.0
            diff = W[i] @ W_tilde[j] + b[i] + b_tilde[j] - np.log(x_ij)
            coef = weight * diff

            grad_W_i = coef * W_tilde[j]
            grad_W_tilde_j = coef * W[i]
            W[i] -= lr * grad_W_i
            W_tilde[j] -= lr * grad_W_tilde_j
            b[i] -= lr * coef
            b_tilde[j] -= lr * coef

    return W + W_tilde
```

दो चलती टुकड़े नाम देने लायक। वजन समारोह`f(x) = (x/x_max)^alpha`बहुत अधिक बार घटता है जोड़े (जैसे `(the, and)`) इसलिए वे हानि पर हावी नहीं होते हैं। अंतिम सम्मिलन राशि है `W`(केंद्र) और `W_tilde`(संदर्भ) तालिकाओं. दोनों को जोड़ना एक प्रकाशित चाल है जो केवल एक का उपयोग करके बेहतर प्रदर्शन करने की प्रवृत्ति है.

> दो उल्लेखनीय महत्वपूर्ण बिंदुएँ---अधिक शक्ति फ़ंक्शन `f(x) = (x/x_max)^alpha`降低非常频繁的对(如 `(the, and)`) का वजन, उसे हानि से वंचित रखता है।`W`(中心词) 和 `W_tilde`(上下文词)表之和──对两者求和 एक प्रकाशित तकनीक है, आमतौर पर केवल एक का उपयोग करने से बेहतर है──

### FastText: उपशब्दों के प्रति जागरूक एम्बेड

```python
def char_ngrams(word, n_min=3, n_max=6):
    wrapped = f"<{word}>"
    grams = {wrapped}
    for n in range(n_min, n_max + 1):
        for i in range(len(wrapped) - n + 1):
            grams.add(wrapped[i:i + n])
    return grams
```

```python
>>> char_ngrams("where")
{'<where>', '<wh', 'whe', 'her', 'ere', 're>', '<whe', 'wher', 'here', 'ere>', '<wher', 'where', 'here>'}
```

प्रत्येक शब्द को n-ग्राम (आमतौर पर 3 से 6 वर्ण) के सेट द्वारा दर्शाया जाता है। शब्द एम्बेडिंग इसके n-ग्राम एम्बेडिंग का योग है। स्किप-ग्राम प्रशिक्षण के लिए, इसे प्लग इन करें जहां Word2Vec ने एक एकल वेक्टर का उपयोग किया है।

> प्रत्येक शब्द से उसका n-ग्राम 集合 (आमतौर पर 3 से 6 个字符) इंगित करते हैं।

```python
def fasttext_vector(word, ngram_table):
    grams = char_ngrams(word)
    vecs = [ngram_table[g] for g in grams if g in ngram_table]
    if not vecs:
        return None
    return np.sum(vecs, axis=0)
```

एक अदृश्य शब्द के लिए, आप अभी भी एक वेक्टर मिलता है जब तक कुछ इसके n-ग्राम ज्ञात हैं। `whereupon`शेयर `<wh`,`her`,`ere`और `<where`के साथ`where`, तो दोनों एक दूसरे के करीब भूमि.

> अदृश्य शब्द के लिए, जब तक इसका भाग n-ग्राम ज्ञात है, आप अभी भी एक तरंग प्राप्त कर सकते हैं`whereupon``where`共享 `<wh``her``ere`和 `<where`तो दोनों एक दूसरे के करीब पड़े हैं।

### बीपीईः उपशब्दों का सीखा हुआ शब्दावली

```python
def learn_bpe(corpus, k_merges):
    vocab = Counter()
    for word, freq in corpus.items():
        tokens = tuple(word) + ("</w>",)
        vocab[tokens] = freq

    merges = []
    for _ in range(k_merges):
        pair_freq = Counter()
        for tokens, freq in vocab.items():
            for a, b in zip(tokens, tokens[1:]):
                pair_freq[(a, b)] += freq
        if not pair_freq:
            break
        best = pair_freq.most_common(1)[0][0]
        merges.append(best)

        new_vocab = Counter()
        for tokens, freq in vocab.items():
            new_tokens = []
            i = 0
            while i < len(tokens):
                if i + 1 < len(tokens) and (tokens[i], tokens[i + 1]) == best:
                    new_tokens.append(tokens[i] + tokens[i + 1])
                    i += 2
                else:
                    new_tokens.append(tokens[i])
                    i += 1
            new_vocab[tuple(new_tokens)] = freq
        vocab = new_vocab
    return merges


def apply_bpe(word, merges):
    tokens = list(word) + ["</w>"]
    for a, b in merges:
        new_tokens = []
        i = 0
        while i < len(tokens):
            if i + 1 < len(tokens) and tokens[i] == a and tokens[i + 1] == b:
                new_tokens.append(a + b)
                i += 2
            else:
                new_tokens.append(tokens[i])
                i += 1
        tokens = new_tokens
    return tokens
```

```python
>>> corpus = Counter({"low": 5, "lower": 2, "newest": 6, "widest": 3})
>>> merges = learn_bpe(corpus, k_merges=10)
>>> apply_bpe("lowest", merges)
['low', 'est</w>']
```

पहले पुनरावृत्ति सबसे आम आसन्न जोड़ी को मिलाता है। पर्याप्त पुनरावृत्ति के बाद, अक्सर उपशृंखला (`low`,`est`,`tion`) एकल टोकन बन जाते हैं और दुर्लभ शब्द साफ-साफ टूट जाते हैं।

> पहली बार 代合并 सबसे आम पड़ोसी ︎`low``est``tion`) एक एकल टोकन में बदल जाता है, दुर्लभ शब्द干净地分解──

वास्तविक GPT / BERT / T5 टोकन बनाने वाले 30k-100k विलय सीखते हैं। परिणामः कोई भी पाठ ज्ञात आईडी के सीमित लंबाई अनुक्रम में टोकन बनता है, कभी भी OOV नहीं।

> वास्तविक GPT / BERT / T5 分词器学习 3万到10万次合并── परिणाम: किसी भी ग्रंथ में किसी भी ज्ञात आईडी के लिए分词 होते हैं, कभी भी OOV नहीं होता──

> **【中文解读】**इस भाग में दिखाया गया है कि इस तकनीक को कैसे तेजी से लागू किया जाए। इस प्रकार के एक परिपक्व ढांचे का उपयोग करके बग कम किए जा सकते हैं और विकास दक्षता में सुधार किया जा सकता है।

> **【拓展：Prompt Engineering 与 LLM 应用】**शीघ्र इंजीनियरिंग  नेल्पी  इंजीनियरों के मूल कौशल बन गए हैं  शून्य-शॉट से लेकर कुछ-शॉट तक, सोच-विचार श्रृंखला से लेकर प्रतिक्रिया तक, विभिन्न सुझाव रणनीति विभिन्न परिदृश्यों के लिए लागू होती हैं                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

## इसे फ्रेमवर्क के साथ लागू करें

अभ्यास में, आप शायद ही कभी खुद इन में से किसी को प्रशिक्षित करते हैं. आप पूर्व-प्रशिक्षित चेकपोइंट लोड करते हैं।

> 實踐中,你几乎从不自从训练这些──你加载预训练检查点──

```python
import fasttext.util
fasttext.util.download_model("en", if_exists="ignore")
ft = fasttext.load_model("cc.en.300.bin")
print(ft.get_word_vector("whereupon").shape)
print(ft.get_word_vector("zoomerapproved").shape)
```

ट्रांसफार्मर युग में बीपीई शैली के उपशब्द टोकनकरण के लिएः

> 对于 ट्रांसफार्मर 时代的 BPE 风格子词分词:

```python
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("gpt2")
print(tok.tokenize("unbelievably tokenized"))
```

```
['un', 'bel', 'iev', 'ably', 'Ġtoken', 'ized']
```

`Ġ`प्रत्येक आधुनिक टोकनराइज़र एक बीपीई संस्करण, वर्डपीस (बीईआरटी) या सैंटेंसपीस (टी 5, एलएएमए) है।

> `Ġ`前标记词边界(GPT-2 的约定) ・・・ प्रत्येक आधुनिक分词器都是 BPE 变体、WordPiece(BERT) या SentencePiece(T5、LLaMA) ・・・

### कौन सी चुनना है

| Situation | Pick | 场景 | 选择 |
|-----------|------|------|------|
| Pretrained general-purpose word vectors, no OOV tolerance needed | GloVe 300d | 预训练通用词向量，不需要处理 OOV | GloVe 300 维 |
| Pretrained general-purpose word vectors, must handle misspellings / neologisms / morphologically rich languages | FastText | 预训练通用词向量，必须处理拼写错误 / 新词 / 形态丰富的语言 | FastText |
| Anything going into a transformer (training or inference) | Whatever tokenizer the model shipped with. Never swap. | 输入 Transformer 的任何场景（训练或推理） | 模型自带的分词器。永远不要替换。 |
| Training your own language model from scratch | Train a BPE or SentencePiece tokenizer on your corpus first | 从零训练自己的语言模型 | 先在你的语料上训练 BPE 或 SentencePiece 分词器 |
| Production text classification with a linear model | Still TF-IDF. Lesson 02. | 使用线性模型的生产文本分类 | 仍然用 TF-IDF。第 02 课。 |

> **【中文解读】**इस खंड में इस बात पर ध्यान दिया गया है कि मॉडल को उपलब्ध उत्पादों के रूप में कैसे तैनात किया जाए। मूल से लेकर उत्पादन स्तर तक, प्रदर्शन अनुकूलन, त्रुटि प्रसंस्करण, निगरानी आदि के कई आयामों पर विचार करने की आवश्यकता है।

## इसे भेजें उत्पाद

`outputs/skill-embeddings-picker.md`:

```markdown
---
name: tokenizer-picker
description: Pick a tokenization approach for a new language model or text pipeline.
version: 1.0.0
phase: 5
lesson: 04
tags: [nlp, tokenization, embeddings]
---

Given a task and dataset description, you output:

1. Tokenization strategy (word-level, BPE, WordPiece, SentencePiece, byte-level). One-sentence reason.
2. Vocabulary size target (e.g., 32k for an English-only LM, 64k-100k for multilingual).
3. Library call with the exact training command. Name the library. Quote the arguments.
4. One reproducibility pitfall. Tokenizer-model mismatch is the single most common silent production bug; call out which pair must be used together.

> **【中文解读】** 练习题按照 Easy/Medium/Hard 三个难度递进。建议至少完成 Medium 级别的题目，Hard 级别适合深入研究或面试准备。

Refuse to recommend training a custom tokenizer when the user is fine-tuning a pretrained LLM. Refuse to recommend word-level tokenization for any model targeting production inference. Flag non-English / multi-script corpora as needing SentencePiece with byte fallback.
```

## अभ्यास विषय

1. **Easy.**दौड़ें`char_ngrams("playing")`और `char_ngrams("played")`. दो n-ग्राम सेटों के जैकार्ड ओवरलैप की गणना करें. आपको पर्याप्त साझा टुकड़े देखने चाहिए (`pla`,`lay`,`play`), यही कारण है कि फास्टटेक्सट मॉर्फोलॉजिकल वेरिएंट्स के बीच अच्छी तरह से स्थानांतरित करता है।
   **简单。**运行 `char_ngrams("playing")`和 `char_ngrams("played")`△ गणना दो n-ग्राम 集合 के जैकार्ड 重叠度──आपको बड़ी मात्रा में साझा片段 देखना चाहिए`pla``lay``play`), यही कारण है कि फास्टटेक्स्ट में रूप परिवर्तनों के बीच अच्छी गतिशीलता है।
2. **Medium.**विस्तार `learn_bpe`शब्द संग्रह की वृद्धि को ट्रैक करने के लिए। संलयन की संख्या के अनुसार प्रति कर्पस वर्ण टोकन का प्लॉट करें। आपको पहले तेजी से संपीड़न देखना चाहिए, प्रति टोकन लगभग 2-3 वर्णों को समझना चाहिए।
   **中等。**扩展 `learn_bpe`以跟踪词表增长──绘制每个语料字符的符号 数作为合并次数的函数──你应该看到开始时快速缩缩,在约2-3字符/符号附近渐近──
3. **Hard.**शेक्सपियर के पूर्ण कार्यों पर 1k-फ्यूजन बीपीई को प्रशिक्षित करें. सामान्य शब्दों की टोकनाइज़ेशन की तुलना दुर्लभ विशेषणों के साथ करें. प्रत्येक शब्द के लिए औसत टोकन का माप करें। जो आपको आश्चर्यचकित करता है उसे लिखें।
   **困难。**शशबिया के पूरे एपिसोड में 1000 बार एक साथ होने वाले BPE के परिणामों की तुलना सामान्य शब्दों से करें।

> **【中文解读】**练习题按照易/中级/难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## कीवर्ड्स  शब्द खोज तालिका

| Term | What people say | What it actually means | 术语 | 人们常说的 | 实际含义 |
|------|-----------------|-----------------------|------|-----------|---------|
| Co-occurrence matrix | Word-word frequency table | `X[i][j]` = how often word `j` appears in a window around word `i`. | 共现矩阵 | 词-词频率表 | `X[i][j]` = 词 `j` 在词 `i` 周围窗口中出现的频率。 |
| Subword | Piece of a word | A character n-gram (FastText) or learned token (BPE/WordPiece/SentencePiece). | 子词 | 词的片段 | 字符 n-gram（FastText）或学习到的 token（BPE/WordPiece/SentencePiece）。 |
| BPE | Byte-pair encoding | Iterative merging of most-frequent adjacent pairs until vocabulary hits target size. | BPE（字节对编码） | 字节对编码 | 迭代合并最频繁的相邻对，直到词表达到目标大小。 |
| OOV | Out of vocabulary | Word the model has never seen. Word2Vec/GloVe fail. FastText and BPE handle it. | OOV（词表外） | 词表外 | 模型从未见过的词。Word2Vec/GloVe 会失败。FastText 和 BPE 能处理。 |
| Byte-level BPE | BPE on raw bytes | GPT-2's scheme. Vocabulary starts with 256 bytes, so nothing is ever OOV. | 字节级 BPE | 对原始字节的 BPE | GPT-2 的方案。词表从 256 个字节开始，所以永远不会有 OOV。 |

> **【中文解读】**术语表中的"क्या लोग कहते हैं" बनाम "क्या वास्तव में इसका मतलब है" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──

## आगे पढ़ना 延伸閱讀

- [Pennington, Socher, Manning (2014). GloVe: Global Vectors for Word Representation](https://nlp.stanford.edu/pubs/glove.pdf) ग्लोवे पेपर, सात पृष्ठ, अभी भी हानि का सबसे अच्छा व्युत्पन्न है।
- [Bojanowski et al. (2017). Enriching Word Vectors with Subword Information](https://arxiv.org/abs/1607.04606) फास्टटेक्स्ट. / फास्टटेक्स्ट 论文。
- [Sennrich, Haddow, Birch (2016). Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) paper that introduced BPE to modern NLP. / 将 BPE 引入现代 NLP 的论文──
- [Hugging Face tokenizer summary](https://huggingface.co/docs/transformers/tokenizer_summary) कैसे BPE, WordPiece, और SentencePiece वास्तव में व्यवहार में भिन्न हैं।
