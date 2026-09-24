# ट्रांसफार्मर से पहले पाठ पीढ़ी  N-gram भाषा मॉडल  ट्रांसफार्मर  पिछला पाठ पीढ़ी  N-gram 语言模型

> यदि कोई शब्द आश्चर्यजनक है, तो मॉडल बुरा है. भ्रम एक संख्या को आश्चर्यचकित करता है. चिकनाई इसे अंतहीन रखती है।
> यदि एक शब्द आश्चर्यजनक है, तो मॉडल खराब है।

> **【中文解读】**N-gram 统计词频预测下一个词──GPT 就是更强大的语言模型──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 01 (Text Processing), Phase 2 · 14 (Naive Bayes) | **前置知识:** Phase 5 · 01（文本处理），Phase 2 · 14（朴素贝叶斯）
**Time:** ~45 minutes | **时间:** ~45 分钟

## समस्या  समस्या परिचय

ट्रांसफार्मर से पहले, आरएनएन से पहले, शब्द एम्बेडिंग से पहले, एक भाषा मॉडल ने अगले शब्द की भविष्यवाणी की, यह गिनकर कि यह पिछले शब्द के बाद कितनी बार होता है `n-1`शब्द. "मक्खी" → "बैठा" 47 बार गिनें, "मक्खी" → "उड़ गया" 12 बार, "मक्खी" → "फ्रिजरेटर" 0 बार. एक संभावना वितरण प्राप्त करने के लिए सामान्यीकरण.

> 之前,之前 RNN 之前,之前词嵌入之前,语言模型通过统计前 `n-1`个词后面跟着当前词的频率来预测下一个词――统计 " बिल्ली " → " बैठ " 出现 47 次, " बिल्ली " → " कूद " 出现 12 次, " बिल्ली " → " रेफ्रिजरेटर " 出现 0 次──归结得到概率分布──

> **【中文解读】**इस खंड में प्रश्न उठे हैं कि इस तकनीक को वास्तविक इंजीनियरिंग में सही ढंग से कैसे समझा जाए और लागू किया जाए।

यह एक n-ग्राम भाषा मॉडल है. यह 1980 से 2015 तक हर भाषण पहचानकर्ता, हर वर्तनी जांचकर्ता और हर वाक्यांश आधारित मशीन अनुवाद प्रणाली चलाता है. यह अभी भी तब चलता है जब आपको सस्ते डिवाइस पर भाषा मॉडलिंग की आवश्यकता होती है.

> यह n-gram भाषा मॉडल है। 1980 से 2015 तक, यह प्रत्येक भाषा पहचानकर्ता में काम करता था, प्रत्येक वर्तनी परीक्षक में और प्रत्येक लघु भाषा आधारित मशीन अनुवाद प्रणाली में। जब आपको सस्ते उपकरण के लिए भाषा मॉडल की आवश्यकता होती है, तो यह अभी भी काम कर रहा है।

दिलचस्प समस्या यह है कि अदृश्य n-ग्राम के बारे में क्या करना है। एक कच्चे गिनती-आधारित मॉडल किसी भी चीज़ को शून्य संभावना देता है जिसे उसने नहीं देखा है, जो विनाशकारी है क्योंकि वाक्य लंबे हैं और लगभग हर लंबे वाक्य में कम से कम एक अदृश्य अनुक्रम होता है। पचास साल के चिकनाई अनुसंधान ने इसे तय किया। Kneser-Ney चिकनाई इसका परिणाम है, और आधुनिक गहरी शिक्षा ने अपनी अनुभवजन्य परंपरा को विरासत में दिया।

> दिलचस्प प्रश्न यह है कि: अप्रत्याशित n-ग्राम को कैसे संभालें। किसी भी अप्रत्याशित चीज़ के लिए शून्य संभावना के वितरण के लिए मूल गणना आधारित मॉडल, यह विनाशकारी है, क्योंकि वाक्य लंबे हैं, लगभग प्रत्येक लंबे वाक्य में कम से कम एक अप्रत्याशित क्रम शामिल है।

## अवधारणा का मूल अवधारणा

> **【中文解读】**इस भाग में मूल अवधारणाओं और सिद्धांतों की आधारभूत जानकारी दी गई है। इन अवधारणाओं को प्राप्त करना बाद में होने वाली प्रक्रियाओं के लिए एक शर्त है।

![N-gram model: count, smooth, generate](../assets/ngram.svg)

### भविष्यवाणी खेल

इस तरह की कोई भी मशीन मौजूद होने से पहले, एक प्रयोग में भाषा मॉडल क्या है, यह परिभाषित किया गया था। अंग्रेजी वाक्य के अगले अक्षर को कवर करें। किसी से यह अनुमान लगाने के लिए कहें, एक समय में एक अनुमान, जब तक वे इसे सही नहीं करते। अनुमान संख्या लिखें। कुछ सौ अक्षरों के लिए दोहराएं।

अनुमान गणना कोई मामूली बात नहीं है. वे पाठ का एक निर्दोष पुनः एन्कोडिंग हैं: गणना अनुक्रम को दूसरे, समान अनुमानकर्ता को सौंपें और वे प्रत्येक अक्षर को पुनः निर्माण कर सकते हैं, क्योंकि प्रत्येक स्थिति में वे ठीक से जानते हैं कि कौन से अनुमान पहले आते हैं। एक संदेश जिसे आप कम प्रतीकों में पुनः एन्कोड कर सकते हैं, प्रति प्रतीक कम जानकारी ले जाता है, इसलिए अनुमान संख्या सांख्यिकी अंग्रेजी के एंट्रॉपिया पर एक छत डालती है।

शैनन ने 1951 में यह किया और एक संख्या प्राप्त की जो अभी भी क्षेत्र को नियंत्रित करती है। एक 27 प्रतीक वर्णमाला (26 अक्षर प्लस स्पेस) ले जा सकता है।`log2(27) ≈ 4.75`एक मॉडल को सीखने के लिए आवश्यक संरचना को किसी भी मॉडल को सीखने से पहले मापा जाता है।

इस खेल का प्रत्येक भाषा मॉडल एक यांत्रिक खिलाड़ी है, और इस पाठ में प्रत्येक मूल्यांकन संख्या स्कोर किया गया खेल हैः

- **Cross-entropy loss**एक LM को प्रशिक्षित करने से अनुमान लगाने के खेल में उसके स्कोर को कम किया जा रहा है।
- **Perplexity**है `2^bits`(या `e^nats`): मॉडल के अनुमान के बाद भी शाखा कारक का सामना करना पड़ता है। 27 प्रतीकों पर एक समान अनुमानित है; एक 1-बिट प्रति अक्षर खिलाड़ी में 2 है।
- **Context length is the player's memory.**एक त्रिकोण मॉडल दो मेमोरी टोकन के साथ खेलता है. एक ट्रांसफार्मर 100K टोकन के साथ एक ही खेल खेलता है. नियम कभी नहीं बदला; खिलाड़ी बेहतर हो गया।

ट्रैक पर एक इकाई स्विचः प्रति अक्षर बिट्स में खेल स्कोर (`log2`), जबकि नीचे दिए गए n-ग्राम सूत्रों में प्रति शब्द टोकन में nats (प्राकृतिक लॉग)  और चूंकि उलझन `e^H`नाट्स में बराबर `2^H`बिट्स में, दो दृश्य अलग अलग इकाइयों में एक ही माप हैं।

```figure
prediction-game
```

**N-gram probability:** `P(w_i | w_{i-n+1}, ..., w_{i-1})`. ठीक करें `n`(आमतौर पर त्रिकोण के लिए 3 और चार ग्राम के लिए 4) गणना से करेंः

> **N-gram 概率：** `P(w_i | w_{i-n+1}, ..., w_{i-1})` तय `n`(三元组 आमतौर पर 3,四元组 के लिए 4) ⋅ से गणना गणनाः

```text
P(w | context) = count(context, w) / count(context)
```

**The zero-count problem.**प्रशिक्षण में न देखे गए किसी भी n-ग्राम को शून्य संभावना मिलती है। ब्राउन कॉर्पस पर 2007 के एक अध्ययन में पाया गया कि 4 ग्राम मॉडल में भी प्रशिक्षण में न देखे गए 4 ग्राम का 30% था। आप बिना चिकनाई के किसी भी वास्तविक पाठ पर मूल्यांकन नहीं कर सकते।

> **零计数问题。**किसी भी प्रशिक्षण में न देखे गए n-ग्राम को शून्य संभावना प्राप्त हुई। 2007 में ब्राउन के भाषा सामग्री भंडार पर किए गए अध्ययन में पाया गया कि यहां तक कि चार-वैकल्पिक मॉडल में भी 30% के चार-वैकल्पिक समूह को प्रशिक्षण में न देखे जाने का अनुमान लगाया गया है।

**Smoothing approaches, in order of sophistication:**

> **平滑方法，按复杂度排序：**

1. **Laplace (add-one).**प्रत्येक गिनती में 1 जोड़ें. दुर्लभ घटनाओं पर सरल, भयानक।
   **拉普拉斯（加一）。** प्रत्येक गणना को 1  सरल, लेकिन दुर्लभ घटनाओं पर प्रभाव बहुत कम 
2. **Good-Turing.**आवृत्ति-आवृत्ति के आधार पर उच्च आवृत्ति घटनाओं से अप्रत्याशित घटनाओं के लिए संभावना द्रव्यमान को पुनः आवंटित करें।
   **Good-Turing。**आकृति की आवृत्ति के आधार पर, आकृति की गुणवत्ता को उच्च आवृत्ति घटनाओं से अप्रत्याशित घटनाओं में पुनः वितरित किया जाएगा
3. **Interpolation.**n-ग्राम, (n-1)-ग्राम, आदि अनुमानों को ट्यून करने योग्य वजनों के साथ मिलाएं।
   **插值。**उपयोग कर सकते हैं n-gram, n-1)-gram 等估计──
4. **Backoff.**यदि n-ग्राम शून्य गिनती है, (n-1)-ग्राम पर वापस गिर. Katz बैकॉफ यह सामान्य बनाता है.
   **回退。**यदि n-ग्राम 计数为零, लौट लौट लौट (n-1)-ग्राम――Katz लौट लौट लौट अपने归归化――
5. **Absolute discounting.**एक निश्चित छूट घटाएँ `D`हर गिनती से, अदृश्य में पुनः वितरण।
   **绝对折扣。**सभी खातों से घटाए गए फिक्स्ड डिस्काउंट`D`, अप्रत्याशित घटनाओं को पुनः वितरित किया गया।
6. **Kneser-Ney.**पूर्ण छूट प्लस निम्न क्रम मॉडल के लिए एक स्मार्ट विकल्पः कच्चे आवृत्ति के बजाय *अंतिम संभावना* (एक शब्द कितने संदर्भों में दिखाई देता है) का उपयोग करें।
   **Kneser-Ney。**绝对折扣加上低阶模型的巧妙选择:使用*续接概率*(一个词出现多少上下文中) बजाय原始频率──

Kneser-Ney अंतर्दृष्टि गहरी है। "सैन फ्रांसिस्को" एक आम बिग्राम है। "सैन" के बाद यूनिग्राम "फ्रांसिस्को" ज्यादातर दिखाई देता है। "सैन" के बाद "फ्रांसिस्को" की उच्च संभावना (क्योंकि गणना उच्च है) देता है। केनेसर-नी नोटिस करता है कि "फ्रांसिस्को" केवल एक संदर्भ में दिखाई देता है और तदनुसार इसके निरंतरता की संभावना को कम करता है। परिणाम: "फ्रांसिस्को" से समाप्त होने वाले एक उपन्यास बिग्राम को उचित कम संभावना मिलती है।

> केनेसर-नी की जानकारी बहुत गहरी है। "सैन फ्रांसिस्को" एक सामान्य दो-वैकंड समूह है। "सैन फ्रांसिस्को" एक सामान्य दो-वैकंड समूह है। "सैन" के बाद "सैन" को एक साधारण पूर्ण छूट मिलती है।

**Evaluation: perplexity.**एक लंबे समय तक चलने वाले परीक्षण सेट पर प्रति शब्द औसत नकारात्मक लॉग-संभाव्यता का एक्सपोनेंट। कम बेहतर है। 100 की उलझन का मतलब है कि मॉडल 100 शब्दों के बीच समान रूप से चुनता है।

> **评估：困惑度。**留出测试集上每词平均负对数似然的指数──越低越好──困惑度 100 मतलब मॉडल की困惑程度 100 个词中均选择的相当──

```text
perplexity = exp(- (1/N) * Σ log P(w_i | context_i))
```

> **【中文解读】**इस भाग के माध्यम से कोड को शून्य से लागू किया जा सकता है कोर एल्गोरिदम। इस तरह के "शुरुआत से" तरीके से फ्रेमवर्क के पीछे के सिद्धांत को समझने में मदद मिलेगी, समस्याओं का सामना करते समय ब्लैक बॉक्स में फंस नहीं जाएगा।

> **【拓展：大语言模型的工程实践】**जीपीटी से चैटजीपीटी, एनएलपी के क्षेत्र में "प्रत्येक कार्य को प्रशिक्षित करने के लिए एक मॉडल" से "एक मॉडल सभी कार्य को हल करने के लिए" के लिए एक प्रकार के परिवर्तन का अनुभव किया गया है।

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) वर्तमान उद्यम एआई 应用 में सबसे लोकप्रिय संरचना हैः उपयोगकर्ता पूछताछ पहले संबंधित दस्तावेज टुकड़े को जांचें, फिर से जांच परिणाम के रूप में ऊपर नीचे दिए गए LLM  生成答案── इस तरह LLM ज्ञान过时和幻觉问题──向量数据库── जैसे कि Milvus、Pinecone、Weaviate) RAG 系统 का मूल घटक है──

> **【拓展：NLP 的多语言挑战】**विश्व में 7000 से अधिक भाषाएं हैं, लेकिन एनएलपी अध्ययन मुख्य रूप से अंग्रेजी जैसे कुछ भाषाओं पर केंद्रित है।

## इसे बनाओ, इसे पूरा करो।

> **【中文解读】**इस भाग के माध्यम से कोड को शून्य से लागू किया जा सकता है कोर एल्गोरिदम। इस तरह के "शुरुआत से" तरीके से फ्रेमवर्क के पीछे के सिद्धांत को समझने में मदद मिलेगी, समस्याओं का सामना करते समय ब्लैक बॉक्स में फंस नहीं जाएगा।
```figure
ngram-backoff
```

## इसे बनाओ

### चरण 1: त्रिकोण गणना

```python
from collections import Counter, defaultdict


def train_ngram(corpus_tokens, n=3):
    ngrams = Counter()
    contexts = Counter()
    for sentence in corpus_tokens:
        padded = ["<s>"] * (n - 1) + sentence + ["</s>"]
        for i in range(len(padded) - n + 1):
            ctx = tuple(padded[i:i + n - 1])
            word = padded[i + n - 1]
            ngrams[ctx + (word,)] += 1
            contexts[ctx] += 1
    return ngrams, contexts


def raw_probability(ngrams, contexts, context, word):
    ctx = tuple(context)
    if contexts.get(ctx, 0) == 0:
        return 0.0
    return ngrams.get(ctx + (word,), 0) / contexts[ctx]
```

इनपुट टोकन वाक्यों की एक सूची है। आउटपुट n-ग्राम गिनती और संदर्भ गिनती है। `<s>`और `</s>`वाक्य सीमाएं हैं।

> 输入是分词后的句子列表──输出是 n-gram 计数和上下文计数──`<s>`和 `</s>`                                                                                                                                                                                                                                                              

### चरण 2: लैप्लेस चिकनाई

```python
def laplace_probability(ngrams, contexts, vocab_size, context, word):
    ctx = tuple(context)
    numerator = ngrams.get(ctx + (word,), 0) + 1
    denominator = contexts.get(ctx, 0) + vocab_size
    return numerator / denominator
```

हर गिनती में 1 जोड़ें, जो कि दुर्लभ ज्ञात घटनाओं को भी नुकसान पहुंचाता है।

>  प्रत्येक गणना में 1  जोड़ें  सरल लेकिन अति-वितरण गुणवत्ता  अपूर्व घटनाओं को, तथा हानिकारक ज्ञात दुर्लभ घटनाओं को 

### चरण 3: Kneser-Ney (बिग्राम, इंटरपोलाटेड)

```python
def kneser_ney_bigram_model(corpus_tokens, discount=0.75):
    unigrams = Counter()
    bigrams = Counter()
    unigram_contexts = defaultdict(set)

    for sentence in corpus_tokens:
        padded = ["<s>"] + sentence + ["</s>"]
        for i, w in enumerate(padded):
            unigrams[w] += 1
            if i > 0:
                prev = padded[i - 1]
                bigrams[(prev, w)] += 1
                unigram_contexts[w].add(prev)

    total_unique_bigrams = sum(len(ctx_set) for ctx_set in unigram_contexts.values())
    continuation_prob = {
        w: len(ctx_set) / total_unique_bigrams for w, ctx_set in unigram_contexts.items()
    }

    context_totals = Counter()
    for (prev, w), count in bigrams.items():
        context_totals[prev] += count

    unique_follow = defaultdict(set)
    for (prev, w) in bigrams:
        unique_follow[prev].add(w)

    def prob(prev, w):
        count = bigrams.get((prev, w), 0)
        denom = context_totals.get(prev, 0)
        if denom == 0:
            return continuation_prob.get(w, 1e-9)
        first_term = max(count - discount, 0) / denom
        lambda_prev = discount * len(unique_follow[prev]) / denom
        return first_term + lambda_prev * continuation_prob.get(w, 1e-9)

    return prob
```

तीन चल भागों।`continuation_prob`"यह शब्द कितने अलग-अलग संदर्भों में दिखाई देता है? " (केनेसर-नी नवाचार) ।`lambda_prev`छूट द्वारा मुक्त द्रव्यमान है, जो बैकऑफ के वजन के लिए उपयोग किया जाता है। अंतिम संभावना छूट मुख्य अवधि प्लस वजन निरंतरता अवधि है।

> तीन गतिशील भागों`continuation_prob`捕获 "这个词出现在多少不同上下文中?"`lambda_prev`                                                                                                                                                                                                                                                              

### चरण 4: नमूनाकरण के साथ पाठ उत्पन्न करना

```python
import random


def generate(prob_fn, vocab, prefix, max_len=30, seed=0):
    rng = random.Random(seed)
    tokens = list(prefix)
    for _ in range(max_len):
        candidates = [(w, prob_fn(tokens[-1], w)) for w in vocab]
        total = sum(p for _, p in candidates)
        r = rng.random() * total
        acc = 0.0
        for w, p in candidates:
            acc += p
            if r <= acc:
                tokens.append(w)
                break
        if tokens[-1] == "</s>":
            break
    return tokens
```

नमूनाकरण संभावना के अनुपात में होता है। हमेशा प्रति बीज अलग-अलग आउटपुट देता है। बीम-खोज-जैसे आउटपुट के लिए, प्रत्येक चरण (लाभकारी) पर argmax चुनें और एक छोटा यादृच्छिकता बटन (तापमान) जोड़ें।

> 概率 अनुपात से ️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️

### चरण 5: उलझन

```python
import math


def perplexity(prob_fn, sentences):
    total_log_prob = 0.0
    total_tokens = 0
    for sentence in sentences:
        padded = ["<s>"] + sentence + ["</s>"]
        for i in range(1, len(padded)):
            p = prob_fn(padded[i - 1], padded[i])
            total_log_prob += math.log(max(p, 1e-12))
            total_tokens += 1
    return math.exp(-total_log_prob / total_tokens)
```

ब्राउन कॉर्पस के लिए, एक अच्छी तरह से ट्यून 4-ग्राम केएन मॉडल 140 के आसपास की जटिलता को हिट करता है। एक ट्रांसफार्मर एलएम एक ही परीक्षण सेट पर 15-30 हिट करता है। अंतर लगभग 10 गुना है। यह अंतर है कि क्षेत्र आगे बढ़ गया है।

> 越低越好── ब्राउन 语料库 के लिए, एक精心调参的四元组 KN 模型困惑度约140── ट्रांसफॉर्मर 语言模型在同一测试集上达到15-30──差距约10倍── यह अंतर इस क्षेत्र में रुझान का कारण है──

> **【中文解读】**इस भाग में दिखाया गया है कि इस तकनीक को कैसे तेजी से लागू किया जाए। इस प्रकार के एक परिपक्व ढांचे का उपयोग करके बग कम किए जा सकते हैं और विकास दक्षता में सुधार किया जा सकता है।

> **【拓展：Prompt Engineering 与 LLM 应用】**शीघ्र इंजीनियरिंग  नेल्पी  इंजीनियरों के मूल कौशल बन गए हैं  शून्य-शॉट से लेकर कुछ-शॉट तक, सोच-विचार श्रृंखला से लेकर प्रतिक्रिया तक, विभिन्न सुझाव रणनीति विभिन्न परिदृश्यों के लिए लागू होती हैं                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

## इसे फ्रेमवर्क के साथ लागू करें

- **Classical NLP teaching.**सबसे स्पष्ट रूप से चिकनाई, एमएलई, और भ्रम के संपर्क में आप प्राप्त कर सकते हैं.
  **经典 NLP 教学。**आप प्राप्त कर सकते हैं सबसे स्पष्ट समतल, MLE और उलझन अनुभवों.
- **KenLM.**उत्पादन n-ग्राम पुस्तकालय. भाषण और एमटी प्रणालियों में एक रेस्कोर के रूप में उपयोग किया जाता है जहां कम विलंबता मायने रखता है।
  **KenLM。**उत्पादन श्रेणी n-ग्राम 库── उपयोग किया जाता है कम देरी से语音和MT 系统的重评分器──
- **On-device autocomplete.**कीबोर्ड में ट्रिग्राम मॉडल।
  **设备端自动补全。**键盘中的三元组模型── अभी भी उपयोग में है──
- **Baselines.**यदि आपका ट्रांसफार्मर KN को एक बड़े मार्जिन से नहीं हराता है, तो कुछ गलत है।
  **基线。**जब तक आप अपने तंत्रिका भाषा मॉडल को ठीक नहीं घोषित करते, तब तक हमेशा n-gram LM की गणना करें।

> **【中文解读】**इस खंड में इस बात पर ध्यान दिया गया है कि मॉडल को उपलब्ध उत्पादों के रूप में कैसे तैनात किया जाए। मूल से लेकर उत्पादन स्तर तक, प्रदर्शन अनुकूलन, त्रुटि प्रसंस्करण, निगरानी आदि के कई आयामों पर विचार करने की आवश्यकता है।

## इसे भेजें उत्पाद

`outputs/prompt-lm-baseline.md`:

> 保存为 `outputs/prompt-lm-baseline.md`:

```markdown
---
name: lm-baseline
description: Build a reproducible n-gram language model baseline before training a neural LM.
phase: 5
lesson: 16
---

Given a corpus and target use (next-word prediction, rescoring, perplexity baseline), output:

1. N-gram order. Trigram for general English, 4-gram if corpus is large, 5-gram for speech rescoring.
2. Smoothing. Modified Kneser-Ney is the default; Laplace only for teaching.
3. Library. `kenlm` for production, `nltk.lm` for teaching, roll your own only to learn.
4. Evaluation. Held-out perplexity with consistent tokenization between train and test sets.

Refuse to report perplexity computed with different tokenization between systems being compared — perplexity numbers are comparable only under identical tokenization. Flag OOV rate in test set; KN handles OOV poorly unless you reserve a special <UNK> token during training.
```

> **【中文解读】**练习题按照易/中级/难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## अभ्यास विषय

1. **Easy.**एक 1000 वाक्य शेक्सपियर कॉर्पस पर एक त्रिकोण LM को प्रशिक्षित करें। 20 वाक्य उत्पन्न करें। वे स्थानीय रूप से मान्य होंगे लेकिन वैश्विक रूप से असंगत होंगे। यह कैनोनिक डेमो है।
   **简单。**1000 वाक्यों में शशकाबिया के भाषी तत्वों पर प्रशिक्षण तीन-शृंगी भाषा मॉडल  उत्पन्न 20 वाक्यों  वे स्थानीय रूप से तर्कसंगत हैं लेकिन समग्र नहीं 
2. **Medium.**अपने KN मॉडल के लिए एक लंबे समय तक चले शेक्सपियर विभाजन पर उलझन लागू करें। लैपलेस के साथ तुलना करें। आपको KN उलझन 30-50% कम देखना चाहिए।
   **中等。**अपने लिए उलझन का एहसास करने के लिए अपने लिए उलझन का एहसास करने के लिए एक मॉडल बनाएं।
3. **Hard.**एक त्रिकोण वर्तनी सुधारक बनाएंः एक गलत वर्तनी शब्द और उसके संदर्भ को देखते हुए, संदर्भ संभावना के अनुसार सुधार उत्पन्न करें और LM के तहत रैंक करें। Birkbeck वर्तनी corpus (सार्वजनिक) पर मूल्यांकन करें।
   **困难。**构建三元组拼写纠错器:给定一个拼写错误的词及其上下文,生成纠正并按LM下的上下文概率排序──在 Birkbeck 拼写语料库(公开) 上评估──

> **【中文解读】**术语表中的"क्या लोग कहते हैं" बनाम "क्या वास्तव में इसका मतलब है" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──

## कीवर्ड्स  शब्द खोज तालिका

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| N-gram | Word sequence / 词序列 | Sequence of `n` consecutive tokens. / `n` 个连续 token 的序列。 |
| Smoothing（平滑） | Avoiding zeros / 避免零 | Reallocating probability mass so unseen events get non-zero probability. / 重新分配概率质量使未见事件获得非零概率。 |
| Perplexity（困惑度） | LM quality metric / LM 质量指标 | `exp(-average log-prob)` on held-out data. Lower is better. / 留出数据上的 `exp(-平均对数概率)`。越低越好。 |
| Backoff（回退） | Fallback to shorter context / 回退到更短上下文 | If trigram count is zero, use bigram. Katz backoff formalizes this. / 如果三元组计数为零，使用二元组。Katz 回退将其形式化。 |
| Kneser-Ney | Best smoothing for n-grams / 最佳 n-gram 平滑 | Absolute discounting + continuation probability for the lower-order model. / 绝对折扣 + 低阶模型的续接概率。 |
| Continuation probability（续接概率） | KN-specific / KN 特有 | `P(w)` weighted by number of contexts `w` appears in, not by raw count. / `P(w)` 按 `w` 出现的上下文数量加权，而非原始计数。 |

> **【中文解读】**延伸阅读 प्रदान करता है गहन सीखने के लिए उच्च गुणवत्ता वाले संसाधनों। ये लेख और पाठ्यक्रम इस क्षेत्र के लिए क्लासिक संदर्भ हैं, जो गहन समझ की आवश्यकता वाले पाठकों के लिए उपयुक्त हैं।

## आगे पढ़ना 延伸閱讀

- [Jurafsky and Martin — Speech and Language Processing, Chapter 3 (2026 draft)](https://web.stanford.edu/~jurafsky/slp3/3.pdf) n-gram LM का कैनोनिक उपचार और चिकनाई. / n-gram 语言模型和平滑的经典教材──
- [Chen and Goodman (1998). An Empirical Study of Smoothing Techniques for Language Modeling](https://dash.harvard.edu/handle/1/25104739) पेपर जो Kneser-Ney को सर्वश्रेष्ठ n-ग्राम चिकनी के रूप में तय किया। / 确定 Kneser-Ney 为最佳 n-ग्राम 平滑器的论文──
- [Kneser and Ney (1995). Improved Backing-off for M-gram Language Modeling](https://ieeexplore.ieee.org/document/479394) मूल KN कागज. / 原始 KN 论文。
- [KenLM](https://kheafield.com/code/kenlm/) तेजी से उत्पादन n-gram LM, अभी भी 2026 में लटेंसी-संवेदनशील अनुप्रयोगों के लिए उपयोग किया जाता है। / 快速生产级 n-gram 语言模型,2026年仍用于延迟敏感应用──
| N-gram | Word sequence | Sequence of `n` consecutive tokens. |
| Smoothing | Avoiding zeros | Reallocating probability mass so unseen events get non-zero probability. |
| Perplexity | LM quality metric | `exp(-average log-prob)` on held-out data. Lower is better. |
| Backoff | Fallback to shorter context | If trigram count is zero, use bigram. Katz backoff formalizes this. |
| Kneser-Ney | Best smoothing for n-grams | Absolute discounting + continuation probability for the lower-order model. |
| Continuation probability | KN-specific | `P(w)` weighted by number of contexts `w` appears in, not by raw count. |
| Entropy of text | Information per symbol | Average bits needed to encode the next symbol given the context. Shannon's 1951 estimate for printed English with up to 100 letters of context: 0.6-1.3 bits/letter, measured before any model existed. |

## आगे पढ़ना

- [Shannon (1951). Prediction and Entropy of Printed English](https://www.princeton.edu/~wbialek/rome/refs/shannon_51.pdf) अनुमान-खेल प्रयोग जो लक्ष्य को परिभाषित करता है प्रत्येक भाषा मॉडल अभी भी अनुकूलित करता है।
- [Jurafsky and Martin — Speech and Language Processing, Chapter 3 (2026 draft)](https://web.stanford.edu/~jurafsky/slp3/3.pdf) n ग्राम एलएम का कैनोनिक उपचार और चिकनाई।
- [Chen and Goodman (1998). An Empirical Study of Smoothing Techniques for Language Modeling](https://dash.harvard.edu/handle/1/25104739) कागज जो Kneser-Ney को सबसे अच्छा n-ग्राम चिकनी के रूप में तय किया।
- [Kneser and Ney (1995). Improved Backing-off for M-gram Language Modeling](https://ieeexplore.ieee.org/document/479394) मूल KN कागज।
- [KenLM](https://kheafield.com/code/kenlm/) तेजी से उत्पादन n-ग्राम LM, जो 2026 में भी लटेंसी-संवेदनशील अनुप्रयोगों के लिए उपयोग किया जाता है।
