# नामित इकाई पहचान 命名实体识别 (NER)

> जब तक आप अस्पष्ट सीमाओं, घोंसले हुए संस्थाओं और डोमेन जार्गोन से निपट नहीं लेते तब तक नामों को बाहर निकालें।
> इसे सरल ढंग से सुनें, जब तक आप एक अमूर्त सीमा का सामना न करें,

> **【中文解读】**इस प्रकार, एक व्यक्ति के नाम, स्थान, संगठन आदि को पहचानने के लिए, यह जानकारी निकालने और ज्ञान के आधार पर आधारित है।

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word Embeddings) | **前置知识:** Phase 5 · 02（BoW + TF-IDF），Phase 5 · 03（词嵌入）
**Time:** ~75 minutes | **时间:** ~75 分钟

## समस्या  समस्या परिचय

"Apple ने Google को अपने iPhone खोज सौदे पर अमेरिका में मुकदमा दायर किया।" पांच संस्थाएंः Apple (ORG), Google (ORG), iPhone (PRODUCT), खोज सौदा (शायद), US (GPE) । एक अच्छी NER प्रणाली उन्हें सभी को सही प्रकार के साथ निकालती है। एक बुरा iPhone याद करता है, Apple को Apple कंपनी के साथ भ्रमित करता है, और "US" को PERSON के रूप में लेबल करता है।

> "Apple ने Google को अपने iPhone खोज सौदे पर अमेरिका में मुकदमा दायर किया।" 五个实体:Apple(ORG)、Google(ORG)、iPhone(PRODUCT)、搜索 सौदा(可能)、US(GPE)。 एक अच्छा NER 系统能正确提取所有实体及其类型──一个差的系统会遗漏 iPhone,把水果 Apple和公司 Apple 混,把"US" 标记为 PERSON──

एनईआर हर संरचित निष्कर्षण पाइपलाइन के नीचे काम का घोड़ा है. पुनरीक्षण विश्लेषण, अनुपालन लॉग स्कैन, चिकित्सा रिकॉर्ड अनामिकरण, खोज क्वेरी समझ, चैटबॉट प्रतिक्रियाओं के लिए ग्राउंडिंग, कानूनी अनुबंध निष्कर्षण। आप इसे कभी नहीं देखते हैं; आप हमेशा इस पर निर्भर करते हैं।

> एनईआर प्रत्येक संरचनात्मक निकासी के लिए एक कार्य इंजन है। आप इसे लगभग नहीं देखते हैं, लेकिन आप हमेशा इस पर निर्भर रहते हैं।

यह पाठ शास्त्रीय पथ (नियम आधारित, एचएमएम, सीआरएफ) को आधुनिक पथ (बीएलएसटीएम-सीआरएफ, फिर ट्रांसफार्मर) में ले जाता है। प्रत्येक चरण इससे पहले की एक विशिष्ट सीमा को हल करता है। पैटर्न सबक है।

> इस वर्ग में क्लासिक पथ से आधुनिक पथ की ओर बढ़ते हुए प्रत्येक चरण में पहले के चरण की विशिष्ट सीमाएं हल होती हैं।

## अवधारणा का मूल अवधारणा

> **【中文解读】**इस भाग में मूल अवधारणाओं और सिद्धांतों की आधारभूत जानकारी दी गई है। इन अवधारणाओं को प्राप्त करना बाद में होने वाली प्रक्रियाओं के लिए एक शर्त है।

**BIO tagging**(या BILOU) इकाई निकासी को एक अनुक्रम लेबलिंग समस्या में बदल देता है। प्रत्येक टोकन को `B-TYPE`(संस्था की शुरुआत), `I-TYPE`(आंतरिक इकाई), या `O`(किसी भी इकाई के बाहर) ।

> **BIO 标注**(या BILOU) को क्रमबद्ध चिह्नित प्रश्न में परिवर्तित किया जाएगा।`B-TYPE`(实体开始)`I-TYPE`(实体内部) या `O`(किसी भी शरीर में नहीं)

```
Apple    B-ORG
sued     O
Google   B-ORG
over     O
its      O
iPhone   B-PRODUCT
search   O
deal     O
in       O
the      O
US       B-GPE
.        O
```

बहु-टोकन संस्थाओं की श्रृंखलाः `New B-GPE`,`York I-GPE`,`City I-GPE`. एक मॉडल जो बायो को समझता है मनमानी स्पैन निकाल सकता है.

> 多 टोकन 实体链接:`New B-GPE``York I-GPE``City I-GPE` BIO के मॉडल को समझने के लिए किसी भी सीमा से 

वास्तुकला प्रगति:

> 架构演进:

- **Rule-based.**रेजेक्स + गजटियर खोजें. ज्ञात संस्थाओं पर उच्च सटीकता, नए पर शून्य कवरेज।
  **基于规则。**正则 + 地名词典查找──已知实体精确率高,对新实体零覆盖──
- **HMM.**छिपे हुए मार्कोव मॉडल, दिए गए टोकन टैग की उत्सर्जन संभावना, टैग-टू-टैग संक्रमण संभावना, विटरबी डिकोड, लेबल किए गए डेटा पर प्रशिक्षित।
  **HMM。**隐马尔可夫模型──给定标签的代币 发射概率,标签间转移概率──Viterbi 解码──在标签数据上训练──
- **CRF.**सशर्त यादृच्छिक क्षेत्र। एचएमएम की तरह लेकिन भेदभावपूर्ण, ताकि आप मनमाने ढंग से सुविधाओं (शब्द आकार, पूंजीकरण, पड़ोसी शब्दों) को मिला सकते हैं। अभी भी 2026 में कम संसाधन तैनाती के लिए क्लासिक उत्पादन कार्यघोड़ा।
  **CRF。**条件随机场── HMM के समान है, लेकिन判别式, इसलिए किसी भी विशेषता को मिश्रित किया जा सकता है
- **BiLSTM-CRF.**तंत्रिका सुविधाओं के बजाय हाथ से बनाई गई। LSTM वाक्य दोनों दिशाओं में पढ़ता है, CRF परत ऊपर लगातार टैग अनुक्रमों को लागू करता है।
  **BiLSTM-CRF。**神经特征代替手工特征──LSTM 双向读取句子, शीर्ष पर CRF 层强制一致的标签序列──
- **Transformer-based.**एक टोकन वर्गीकरण सिर के साथ बारीक-ट्यूनिंग BERT. सबसे अच्छी सटीकता. सबसे गणना.
  **基于 Transformer。**प्रयोग करें टोकन 分类头微调 BERT──最佳准确率──最多计算量──

> **【拓展：大语言模型的工程实践】**जीपीटी से चैटजीपीटी, एनएलपी के क्षेत्र में "प्रत्येक कार्य को प्रशिक्षित करने के लिए एक मॉडल" से "एक मॉडल सभी कार्य को हल करने के लिए" के लिए एक प्रकार के परिवर्तन का अनुभव किया गया है।

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) वर्तमान उद्यम एआई 应用 में सबसे लोकप्रिय संरचना हैः उपयोगकर्ता पूछताछ पहले संबंधित दस्तावेज टुकड़े को जांचें, फिर से जांच परिणाम के रूप में ऊपर नीचे दिए गए LLM  生成答案── इस तरह LLM ज्ञान过时和幻觉问题──向量数据库── जैसे कि Milvus、Pinecone、Weaviate) RAG 系统 का मूल घटक है──

> **【拓展：NLP 的多语言挑战】**विश्व में 7000 से अधिक भाषाएं हैं, लेकिन एनएलपी अध्ययन मुख्य रूप से अंग्रेजी जैसे कुछ भाषाओं पर केंद्रित है।

## इसे बनाओ, इसे पूरा करो।

> **【中文解读】**इस भाग के माध्यम से कोड को शून्य से लागू किया जा सकता है कोर एल्गोरिदम। इस तरह के "शुरुआत से" तरीके से फ्रेमवर्क के पीछे के सिद्धांत को समझने में मदद मिलेगी, समस्याओं का सामना करते समय ब्लैक बॉक्स में फंस नहीं जाएगा।
```figure
ner-bio-tagging
```

## इसे बनाओ

### चरण 1: बायो टैगिंग सहायक

```python
def spans_to_bio(tokens, spans):
    labels = ["O"] * len(tokens)
    for start, end, label in spans:
        labels[start] = f"B-{label}"
        for i in range(start + 1, end):
            labels[i] = f"I-{label}"
    return labels


def bio_to_spans(tokens, labels):
    spans = []
    current = None
    for i, label in enumerate(labels):
        if label.startswith("B-"):
            if current:
                spans.append(current)
            current = (i, i + 1, label[2:])
        elif label.startswith("I-") and current and current[2] == label[2:]:
            current = (current[0], i + 1, current[2])
        else:
            if current:
                spans.append(current)
                current = None
    if current:
        spans.append(current)
    return spans
```

```python
>>> tokens = ["Apple", "sued", "Google", "over", "iPhone", "sales", "."]
>>> labels = ["B-ORG", "O", "B-ORG", "O", "B-PRODUCT", "O", "O"]
>>> bio_to_spans(tokens, labels)
[(0, 1, 'ORG'), (2, 3, 'ORG'), (4, 5, 'PRODUCT')]
```

### चरण 2: हस्तनिर्मित विशेषताएं

क्लासिक (गैर-न्यूरल) एनईआर के लिए, विशेषताएं खेल हैं। उपयोगी हैंः

>  क्लासिक 非神经) NER के लिए, विशेषताएँ                                                                                                                                                                                                                                                       

```python
def token_features(token, prev_token, next_token):
    return {
        "lower": token.lower(),
        "is_upper": token.isupper(),
        "is_title": token.istitle(),
        "has_digit": any(c.isdigit() for c in token),
        "suffix_3": token[-3:].lower(),
        "shape": word_shape(token),
        "prev_lower": prev_token.lower() if prev_token else "<BOS>",
        "next_lower": next_token.lower() if next_token else "<EOS>",
    }


def word_shape(word):
    out = []
    for c in word:
        if c.isupper():
            out.append("X")
        elif c.islower():
            out.append("x")
        elif c.isdigit():
            out.append("d")
        else:
            out.append(c)
    return "".join(out)
```

`word_shape("iPhone")`रिटर्न `xXxxxx`. .`word_shape("USA-2024")`रिटर्न `XXX-dddd`. पूँजीकरण पैटर्न उचित संज्ञाओं के लिए उच्च संकेत हैं.

> `word_shape("iPhone")` लौटें `xXxxxx``word_shape("USA-2024")` लौटें `XXX-dddd`                                                                                                                                                                                                                                                              

### चरण 3: सरल नियम आधारित + शब्दकोश आधार

```python
ORG_GAZETTEER = {"Apple", "Google", "Microsoft", "OpenAI", "Meta", "Amazon", "Netflix"}
GPE_GAZETTEER = {"US", "USA", "UK", "India", "Germany", "France"}
PRODUCT_GAZETTEER = {"iPhone", "Android", "Windows", "ChatGPT", "Claude"}


def rule_based_ner(tokens):
    labels = []
    for token in tokens:
        if token in ORG_GAZETTEER:
            labels.append("B-ORG")
        elif token in GPE_GAZETTEER:
            labels.append("B-GPE")
        elif token in PRODUCT_GAZETTEER:
            labels.append("B-PRODUCT")
        else:
            labels.append("O")
    return labels
```

उत्पादन गजटर्स में विकिपीडिया और डीबीपीडिया से लाखों प्रविष्टियां स्क्रैप की गई हैं। कवरेज अच्छा है।`Apple`यह भयानक है। यही कारण है कि सांख्यिकीय मॉडल जीत गए।

> 生产地名词典有数百万条目,来自维基百科 和 DBpedia 抓取──覆盖率不错──消歧(公司 `Apple`水果 के साथ`apple`) बहुत बुरा है. यही कारण है कि यह सफल हुआ है.

### चरण 4: सीआरएफ चरण (स्केच, पूर्ण इंप्ल नहीं)

50 पंक्तियों में खरोंच से पूर्ण सीआरएफ संभावना सिद्धांत के आधार के बिना प्रकाश नहीं है। उपयोग `sklearn-crfsuite`इसके बजायः

>  बिना संभावना सिद्धांत के आधार के शून्य से 50 लाइनों के भीतर पूर्ण सीआरएफ को प्राप्त करना समझ में नहीं आता `sklearn-crfsuite`:

```python
import sklearn_crfsuite

def to_features(tokens):
    out = []
    for i, tok in enumerate(tokens):
        prev = tokens[i - 1] if i > 0 else ""
        nxt = tokens[i + 1] if i + 1 < len(tokens) else ""
        out.append({
            "word.lower()": tok.lower(),
            "word.isupper()": tok.isupper(),
            "word.istitle()": tok.istitle(),
            "word.isdigit()": tok.isdigit(),
            "word.suffix3": tok[-3:].lower(),
            "word.shape": word_shape(tok),
            "prev.word.lower()": prev.lower(),
            "next.word.lower()": nxt.lower(),
            "BOS": i == 0,
            "EOS": i == len(tokens) - 1,
        })
    return out


crf = sklearn_crfsuite.CRF(algorithm="lbfgs", c1=0.1, c2=0.1, max_iterations=100, all_possible_transitions=True)
X_train = [to_features(s) for s in sentences_tokenized]
crf.fit(X_train, bio_labels_train)
```

`c1`और `c2`L1 और L2 नियमितता है। `all_possible_transitions=True`मॉडल अवैध अनुक्रमों को सीखने देता है (जैसे, `I-ORG`के बाद`O`) संभावना नहीं है, जो कि बिना आप प्रतिबंध लिखने के लिए एक CRF जैव स्थिरता लागू करता है।

> `c1`和 `c2`है L1 और L2 सही ढंग से`all_possible_transitions=True`让模型学习非法序列 (जैसे)`O` इसके बाद आ रहा है `I-ORG`) असंभव है, यही है CRF में जबरदस्ती बायो एक-संयोजित तरीके से जबरदस्ती करने का तरीका है।

### चरण 5: BiLSTM-CRF क्या जोड़ता है

विशेषताएं सीख जाती हैं। इनपुटः टोकन एम्बेडिंग (ग्लोवे या फास्टटेक्स) । LSTM बाएं से दाएं और दाएं से बाएं पढ़ता है। संकीर्ण छिपे हुए राज्य CRF आउटपुट परत के माध्यम से जाते हैं। CRF अभी भी टैग-अनुक्रम सुसंगतता को लागू करता है; LSTM सीखने वाले लोगों के साथ हस्तनिर्मित सुविधाओं को बदल देता है।

> विशेषताएं बदलकर सीखने में प्राप्त की गयी हैं──输入:token 嵌入(GloVe या fastText)──LSTM Left to Right और Right to Left Reading──拼接的隐藏状态通过CRF 输出层──CRF 仍然强制标签序列一致性;LSTM 用到的特征替代手工特征──

```python
import torch
import torch.nn as nn


class BiLSTM_CRF_Head(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim, n_labels):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, bidirectional=True, batch_first=True)
        self.fc = nn.Linear(hidden_dim * 2, n_labels)

    def forward(self, token_ids):
        e = self.embed(token_ids)
        h, _ = self.lstm(e)
        emissions = self.fc(h)
        return emissions
```

> **【中文解读】**इस भाग में दिखाया गया है कि इस तकनीक को कैसे तेजी से लागू किया जाए। इस प्रकार के एक परिपक्व ढांचे का उपयोग करके बग कम किए जा सकते हैं और विकास दक्षता में सुधार किया जा सकता है।

सीआरएफ परत के लिए प्रयोग करें `torchcrf.CRF`हाथ से बनाई गई सीआरएफ पर लाभ मापने योग्य है लेकिन आप उम्मीद से कम है जब तक आप दसियों हजार लेबल वाक्य है।

> सीआरएफ 层使用 `torchcrf.CRF`(पिप इंस्टॉल pytorch-crf) ◊ तुलना में हस्तनिर्मित CRF का वृद्धि मापनीय है, लेकिन अपेक्षाकृत छोटा है, जब तक आपके पास हजारों अंक वाक्य नहीं हैं ◊

> **【拓展：Prompt Engineering 与 LLM 应用】**शीघ्र इंजीनियरिंग  नेल्पी  इंजीनियरों के मूल कौशल बन गए हैं  शून्य-शॉट से लेकर कुछ-शॉट तक, सोच-विचार श्रृंखला से लेकर प्रतिक्रिया तक, विभिन्न सुझाव रणनीति विभिन्न परिदृश्यों के लिए लागू होती हैं                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

## इसे फ्रेमवर्क के साथ लागू करें

spaCy उत्पादन-ग्रेड NER जहाजों को बॉक्स से बाहर निकालता है।

> उत्पादन स्तर के एनईआर प्रदान करने के लिए एक खुली बक्से में।

```python
import spacy

nlp = spacy.load("en_core_web_sm")
doc = nlp("Apple sued Google over its iPhone search deal in the US.")
for ent in doc.ents:
    print(f"{ent.text:20s} {ent.label_}")
```

```
Apple                ORG
Google               ORG
iPhone               ORG
US                   GPE
```

ध्यान दें `iPhone`लेबल`ORG``PRODUCT` spaCy के छोटे मॉडल में उत्पाद इकाई कवरेज कमजोर है।`en_core_web_lg`) बेहतर है। ट्रांसफार्मर मॉडल (`en_core_web_trf`) और भी बेहतर है।

> ध्यान दें`iPhone`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `ORG`और `PRODUCT` स्पेस साइ का छोटा मॉडल वस्तु वस्तुओं के आवरण से कमजोर है── बड़ा मॉडल(`en_core_web_lg`)更好──Transformer 模型(`en_core_web_trf`) बेहतर है.

BERT आधारित NER के लिए गले लगाना चेहराः

> BERT के आधार पर NER के साथ गले लगाना चेहरा:

```python
from transformers import pipeline

ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
print(ner("Apple sued Google over its iPhone in the US."))
```

```
[{'entity_group': 'ORG', 'word': 'Apple', ...},
 {'entity_group': 'ORG', 'word': 'Google', ...},
 {'entity_group': 'MISC', 'word': 'iPhone', ...},
 {'entity_group': 'LOC', 'word': 'US', ...}]
```

`aggregation_strategy="simple"`इसके बिना, आप टोकन स्तर लेबल मिलता है और खुद को मिलाया जाना है.

> `aggregation_strategy="simple"`एक पार के लिए एक निरंतर बी-एक्स, आई-एक्स टोकन 合并. इसके बिना, आपको एक टोकन 级 के लेबल मिलते हैं, स्वयं को एक साथ जोड़ने की आवश्यकता होती है.

### LLM आधारित NER (2026 विकल्प)

शून्य-शॉट और कुछ-शॉट एलएलएम एनईआर अब कई डोमेन पर ठीक-ठीक मॉडल के साथ प्रतिस्पर्धी है, और जब लेबल डेटा दुर्लभ है तो नाटकीय रूप से बेहतर है।

> 零样本和少样本 LLM NER अब कई क्षेत्रों में सूक्ष्म मॉडलों के साथ प्रतिस्पर्धी है, जबकि डेटा की कमी के समय लाभ अधिक है।

- **Zero-shot prompting.**एमएलएम को इकाई प्रकारों की सूची और एक उदाहरण योजना दें। JSON आउटपुट के लिए पूछें। बॉक्स से बाहर काम करता है; नवीन डोमेन पर सटीकता मध्यम है।
  **零样本提示。** LLM को एक भौतिक प्रकार की सूची और उदाहरण मॉडल प्रदान करना JSON 输出 开箱即用; नए क्षेत्र में सटीकता दर में等等
- **ZeroTuneBio-style prompting.**एक बहु-चरण प्रम्प्ट (एक शॉट नहीं) जैव चिकित्सा एनईआर पर सटीकता को काफी बढ़ाता है। कानूनी, वित्तीय और वैज्ञानिक क्षेत्रों के लिए एक ही पैटर्न काम करता है।
  **ZeroTuneBio 风格提示。**इस प्रकार के मॉडल को कानून, वित्त और विज्ञान के क्षेत्र में लागू किया गया है।
- **Dynamic prompting with RAG.**प्रत्येक निष्कर्ष कॉल के लिए एक छोटे से टिप्पणी वाले बीज सेट से सबसे समान लेबल वाले उदाहरण प्राप्त करें; उड़ान में कुछ-शॉट प्रॉम्प्ट बनाएं। 2026 बेंचमार्क में, यह स्थैतिक प्रॉम्प्ट से 11-12% बढ़ जाता है।
  **动态 RAG 提示。**प्रत्येक विचार को कम मात्रा में अंकन से क्रमशः सबसे समान अंकन नमूना का पता लगाने के लिए अनुकूलित किया गया है; गतिशीलता निर्माण कम नमूना सुझावों में 2026 के वर्ष के आधार पर परीक्षणों में, इसने जीपीटी-4 बायोमेडिसिन एनईआर एफ 1 को स्थिर सुझावों से 11-12% बढ़ा दिया है।
- **Per-entity-type decomposition.**लंबे दस्तावेजों के लिए, एक एकल कॉल जो एक ही समय में सभी इकाई प्रकारों को निकालता है, लंबाई बढ़ने के साथ याद करना खो देता है। प्रति इकाई प्रकार एक निष्कर्षण पास चलाएं। उच्च निष्कर्ष लागत, काफी अधिक सटीकता। यह नैदानिक नोट्स और कानूनी अनुबंधों के लिए मानक पैटर्न है।
  **按实体类型分解。**长文档, एक बार调用提取所有实体类型时,长度增加会丢失召回率―― प्रत्येक实体类型运行一次抽取――推理成本较高,但准确率显著较高―― यह नैदानिक नोट्स एवं कानूनी अनुबंधों का मानक模式――

2026 से उत्पादन की सिफारिशः प्रशिक्षण डेटा एकत्र करने से पहले एलएलएम शून्य शॉट बेसलाइन से शुरू करें। अक्सर एफ 1 पर्याप्त अच्छा होता है कि आपको कभी भी ठीक करने की आवश्यकता नहीं होती है।

> 2026 साल उत्पादन सुझावः प्रशिक्षण डेटा एकत्र करने से पहले, पहले एलएलएम 零样本基线 से शुरू करें।

### जहां क्लासिकल एनईआर अभी भी जीतता है

यहां तक कि LLM उपलब्ध होने पर भी, क्लासिकल NER तब जीतता है जबः

> यहां तक कि LLM के लिए भी उपलब्ध है, क्लासिक NER निम्नलिखित परिस्थितियों में जीत

- विलंबता बजट 50ms से नीचे है।
  延迟预算低于50毫秒──
- आपके पास हजारों लेबल वाले उदाहरण हैं और आपको 98% + F1 की आवश्यकता है।
  आप हजारों लेबल नमूने है और 98% + F1 की आवश्यकता है।
- डोमेन में एक स्थिर ओंटोलॉजी है जहां पूर्व प्रशिक्षित CRF या BiLSTM अच्छी तरह से स्थानांतरित होता है।
  क्षेत्र में स्थिर मूल, पूर्व प्रशिक्षण के CRF या BiLSTM 迁移良好──
- नियामक प्रतिबंधों के लिए एक स्थानीय, गैर-जनकारी मॉडल की आवश्यकता होती है।
  监管约束要求本地部署的非生成式模型──

### जहां यह टूट जाता है

- **Domain shift.**कानूनी अनुबंधों पर CoNLL प्रशिक्षित NER एक राजपत्रकार से भी बदतर प्रदर्शन करता है.
  **领域偏移。**CoNLL में प्रशिक्षण के लिए NER 处理法律合同时比地名词典还差──在你的领域上微调──
- **Nested entities.**"बैंक ऑफ अमेरिका टॉवर" एक ही समय में एक ORG और एक सुविधा है। मानक बायो ओवरलैप स्पैन का प्रतिनिधित्व नहीं कर सकता है। आपको घोंसले हुए NER (मल्टी-पास या स्पैन-आधारित मॉडल) की आवश्यकता है।
  **嵌套实体。**"बैंक ऑफ अमेरिका टॉवर" एक ही समय में ORG और सुविधा है।
- **Long entities.**"संयुक्त राज्य अमेरिका के संघीय जमा बीमा निगम. " टोकन स्तर के मॉडल कभी कभी इस विभाजित. उपयोग `aggregation_strategy`या प्रक्रिया के बाद।
  **长实体。**"संयुक्त राज्य अमेरिका संघीय जमा बीमा निगम"' टोकन 级别模型有时会分分这个──使用 `aggregation_strategy`या बाद में संसाधित किया गया।
- **Sparse types.**चिकित्सा NER लेबल जैसे DRUG_BRAND, ADVERSE_EVENT, DOSE. सामान्य प्रयोजन के मॉडल का कोई विचार नहीं है। Scispacy और BioBERT वहां प्रारंभिक बिंदु हैं।
  **稀疏类型。**医疗 NER 标签如 DRUG_BRAND、ADVERSE_EVENT、DOSE──通用模型一无所知──Scispacy 和 BioBERT यहीं की शुरुआत है──

> **【中文解读】**इस खंड में इस बात पर ध्यान दिया गया है कि मॉडल को उपलब्ध उत्पादों के रूप में कैसे तैनात किया जाए। मूल से लेकर उत्पादन स्तर तक, प्रदर्शन अनुकूलन, त्रुटि प्रसंस्करण, निगरानी आदि के कई आयामों पर विचार करने की आवश्यकता है।

## इसे भेजें उत्पाद

`outputs/skill-ner-picker.md`:

> 保存为 `outputs/skill-ner-picker.md`:

```markdown
---
name: ner-picker
description: Pick the right NER approach for a given extraction task.
version: 1.0.0
phase: 5
lesson: 06
tags: [nlp, ner, extraction]
---

Given a task description (domain, label set, language, latency, data volume), output:

1. Approach. Rule-based + gazetteer, CRF, BiLSTM-CRF, or transformer fine-tune.
2. Starting model. Name it (spaCy model ID, Hugging Face checkpoint ID, or "custom, trained from scratch").
3. Labeling strategy. BIO, BILOU, or span-based. Justify in one sentence.
4. Evaluation. Use `seqeval`. Always report entity-level F1 (not token-level).

Refuse to recommend fine-tuning a transformer for under 500 labeled examples unless the user already has a pretrained domain model. Flag nested entities as needing span-based or multi-pass models. Require a gazetteer audit if the user mentions "production scale" and labels are unchanged from CoNLL-2003.
```

> **【中文解读】**练习题按照易/中级/难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## अभ्यास विषय

1. **Easy.**कार्यान्वयन`bio_to_spans`(उपवर्जित `spans_to_bio`) और 10 वाक्य पर वापसी-यात्रा सुसंगतता की जांच करें।
   **简单。**实现 `bio_to_spans`(`spans_to_bio`                                                                                                                                                                                                                                                              
2. **Medium.**CoNLL-2003 अंग्रेजी NER डेटासेट पर ऊपर के sklearn-crfsuite CRF को प्रशिक्षित करें।`seqeval`. सामान्य परिणाम: ~ 84 F1.
   **中等。**को एनएलएल-2003 में अंग्रेजी NER डाटा集上 प्रशिक्षण उपर्युक्त sklearn-crfsuite CRF`seqeval`报告每类 F1──典型结果:~84 F1──
3. **Hard.**ठीक-ठीक `distilbert-base-cased`एक डोमेन-विशिष्ट एनईआर डेटासेट (चिकित्सा, कानूनी या वित्तीय) पर। spaCy छोटे मॉडल की तुलना करें। दस्तावेज़ डेटा रिसाव जांचें और आपको क्या आश्चर्यचकित किया है लिखें।
   **困难。**विशिष्ट क्षेत्र में NER डेटा集 (नियम या वित्त)`distilbert-base-cased`️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️

> **【中文解读】**术语表中的"क्या लोग कहते हैं" बनाम "क्या वास्तव में इसका मतलब है" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──

## कीवर्ड्स  शब्द खोज तालिका

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| NER（命名实体识别） | Extract names / 提取名字 | Label token spans with types (PERSON, ORG, GPE, DATE, ...). / 用类型（PERSON、ORG、GPE、DATE 等）标注 token 跨度。 |
| BIO | Tagging scheme / 标注方案 | `B-X` begins, `I-X` continues, `O` outside. / `B-X` 开始，`I-X` 继续，`O` 外部。 |
| BILOU | Better BIO / 更好的 BIO | Adds `L-X` (last), `U-X` (unit) for cleaner boundaries. / 添加 `L-X`（最后）、`U-X`（单元）以获得更清晰的边界。 |
| CRF（条件随机场） | Structured classifier / 结构化分类器 | Models transitions between labels, not just emissions. Enforces valid sequences. / 对标签间的转移建模，而不仅仅是发射。强制有效序列。 |
| Nested NER（嵌套 NER） | Overlapping entities / 重叠实体 | One span is a different entity than a sub-span of it. BIO cannot express this. / 一个跨度与其子跨度是不同的实体。BIO 无法表达这一点。 |
| Entity-level F1（实体级 F1） | Proper NER metric / 正确的 NER 指标 | Predicted span must match true span exactly. Token-level F1 overstates accuracy. / 预测跨度必须与真实跨度完全匹配。Token 级 F1 会高估准确率。 |

> **【中文解读】**延伸阅读 प्रदान करता है गहन सीखने के लिए उच्च गुणवत्ता वाले संसाधनों। ये लेख और पाठ्यक्रम इस क्षेत्र के लिए क्लासिक संदर्भ हैं, जो गहन समझ की आवश्यकता वाले पाठकों के लिए उपयुक्त हैं।

## आगे पढ़ना 延伸閱讀

- [Lample et al. (2016). Neural Architectures for Named Entity Recognition](https://arxiv.org/abs/1603.01360) BiLSTM-CRF पेपर. कैनोनिकल. / BiLSTM-CRF 论文──经典──
- [Devlin et al. (2018). BERT: Pre-training of Deep Bidirectional Transformers](https://arxiv.org/abs/1810.04805) टोकन-वर्गीकरण पैटर्न को पेश करता है जो मानक बन गया। /  introduced into becoming standard token 分类模式──
- [spaCy linguistic features — named entities](https://spacy.io/usage/linguistic-features#named-entities) प्रत्येक विशेषता के लिए व्यावहारिक संदर्भ `Doc.ents`और `Span`. / `Doc.ents`和 `Span`उपरोक्त प्रत्येक विशेषता का व्यावहारिक संदर्भ
- [seqeval](https://github.com/chakki-works/seqeval) सही मीट्रिक लाइब्रेरी. इसे हमेशा उपयोग करें. / 正确的指标库──始终使用它──
