# विषय मॉडलिंग  LDA और BERTopic  विषय निर्माण  LDA और BERTopic

> LDA: दस्तावेज विषयों का मिश्रण हैं, विषय शब्दों पर वितरण हैं। BERTopic: दस्तावेज क्लस्टर एम्बेडिंग स्पेस में, क्लस्टर विषय हैं। एक ही लक्ष्य, अलग-अलग विघटन।
> LDA:文档是主题的混合,主题是词的分布──BERTopic:文档在嵌入空间中的聚类,聚类就是主题──相同的目标,不同分解──

> **【中文解读】**LDA उपयोग概率 मॉडल खोज विषय,BERTopic उपयोग BERT 嵌入

**Type:** Learn | **类型:** 学习
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word2Vec) | **前置知识:** Phase 5 · 02 (BoW + TF-IDF), Phase 5 · 03 (Word2Vec)
**Time:** ~45 minutes | **时间:** ~45 分钟


## समस्या  समस्या परिचय

आपके पास 10,000 ग्राहक सहायता टिकट, 50,000 समाचार लेख, या 200,000 ट्वीट हैं। आपको यह जानने की जरूरत है कि संग्रह क्या है, इसे पढ़ने के बिना। आपके पास श्रेणियां नहीं हैं। आप यह भी नहीं जानते कि कितनी श्रेणियां मौजूद हैं।
> आपके पास 10,000 张客户支持工单,50,000 篇新闻文章或200,000 条推文──आपको इस संग्रह के विषय को बिना पढ़े जानने की आवश्यकता है──आपको कोई चिह्नित श्रेणी नहीं है──आपको यह भी नहीं पता कि कितनी श्रेणीएं हैं──

> **【中文解读】**इस खंड में प्रश्न उठे हैं कि इस तकनीक को वास्तविक इंजीनियरिंग में सही ढंग से कैसे समझा जाए और लागू किया जाए।


विषय मॉडलिंग के बिना इसका जवाब देता है. इसे एक corpus दें, एक छोटे से सुसंगत विषयों का एक सेट वापस प्राप्त करें और, प्रत्येक दस्तावेज़ के लिए, उन विषयों पर एक वितरण।
> विषय निर्माण अनुगमन के बिना इस प्रश्न का उत्तर देना, इसे एक भाष्य संग्रह देना, एक समूह के लिए एक निरंतर विषय को वापस करना, साथ ही प्रत्येक दस्तावेज इन विषयों पर वितरण करना।

दो एल्गोरिथम परिवार हावी हैं। LDA (2003) प्रत्येक दस्तावेज़ को लटेंट विषयों के मिश्रण के रूप में और प्रत्येक विषय को शब्दों पर वितरण के रूप में व्यवहार करता है। इन्फेरेंस बेयसियन है। यह अभी भी उत्पादन में जहाज करता है जहां आपको मिश्रित सदस्यता विषय असाइनमेंट और स्पष्ट शब्द-स्तर की संभावना वितरण की आवश्यकता होती है।
> 两个算法族占主导地位――LDA(2003) प्रत्येक लेख को संभावित विषय के मिश्रण के रूप में देखा जाएगा, प्रत्येक विषय के रूप में शब्द के वितरण, 推断是贝叶斯的── यह अभी भी आपको मिश्रित सदस्य विषय के वितरण और व्याख्या योग्य शब्द श्रेणी संभावना वितरण के उत्पादन में प्रकाशित करने की आवश्यकता है──

BERTopic (2020) BERT के साथ दस्तावेजों को एन्कोड करता है, UMAP के साथ आयामता को कम करता है, HDBSCAN के साथ क्लस्टर करता है, और वर्ग-आधारित TF-IDF के माध्यम से विषय शब्दों को निकालता है। यह छोटे पाठ, सोशल मीडिया और किसी भी चीज़ पर जीतता है जहां शब्द ओवरलैप से अधिक अर्थिक समानता मायने रखती है। एक दस्तावेज़ एक विषय प्राप्त करता है, जो लंबे रूप की सामग्री के लिए एक सीमा है।
> BERTopic(2020) के साथ BERT 编码文档, UMAP 降维, HDBSCAN 聚类, के माध्यम से आधारित TF-IDF 提取主题词── यह लघु文本、社交媒体和语义相似性比词重叠比较重要内容 पर विजय प्राप्त करती है── एक文档 प्राप्त एक विषय, यह लंबे लेख की सामग्री के लिए एक प्रतिबंध है──

यह सबक दोनों के लिए अंतर्ज्ञान और नामों का निर्माण करता है कि किसी दिए गए कॉर्पस के लिए कौन सा चुनना है।
> इस विषय में दोनों के बीच सीधा-सादा विचार स्थापित करने और यह भी बताया गया है कि कौन सा विषय चुनना है।

> **【中文解读】**इस भाग में मूल अवधारणाओं और सिद्धांतों की आधारभूत जानकारी दी गई है। इन अवधारणाओं को प्राप्त करना बाद में होने वाली प्रक्रियाओं के लिए एक शर्त है।


## अवधारणा का मूल अवधारणा

![LDA mixture model vs BERTopic clustering](../assets/topic-modeling.svg)
> ![LDA 混合模型 vs BERTopic 聚类](../assets/topic-modeling.svg)

**LDA generative story.**प्रत्येक विषय शब्दों पर एक वितरण है। प्रत्येक दस्तावेज़ विषयों का मिश्रण है। एक दस्तावेज़ में एक शब्द उत्पन्न करने के लिए, दस्तावेज़ के मिश्रण से एक विषय का नमूना लें, फिर उस विषय के वितरण से एक शब्द का नमूना लें। इन्फेरेंस इसे उलट देता हैः दिए गए अवलोकन किए गए शब्दों को देखते हुए, प्रत्येक दस्तावेज़ पर विषय वितरण और विषय पर शब्द वितरण का अनुमान लगाएं। गिर गया गिब्स नमूना या वैरिएशनल बेयज़ गणित करता है।
> **LDA 生成故事。**प्रत्येक विषय शब्द का वितरण है। प्रत्येक दस्तावेज़ विषय का मिश्रण है। प्रत्येक विषय में एक शब्द उत्पन्न करना है, एक विषय को दस्तावेज के मिश्रण से अलग करना है, फिर उस विषय के वितरण से अलग करना है।

कुंजी एलडीए आउटपुटः
> 关键 LDA 输出:

- `doc_topic`: मैट्रिक्स `(n_docs, n_topics)`, प्रत्येक पंक्ति का योग 1 (दस्तावेज के विषय मिश्रण) है।
- `topic_word`: मैट्रिक्स `(n_topics, vocab_size)`, प्रत्येक पंक्ति का योग 1 (विषय के शब्द वितरण) है।
> - `doc_topic`:矩阵 `(n_docs, n_topics)`, प्रति行总和为 1(文档主题混合)
- `topic_word`:矩阵 `(n_topics, vocab_size)`, प्रति行总和为 1 ((主题的词分布)

**BERTopic pipeline.**
> **BERTopic 流水线。**

1. प्रत्येक दस्तावेज़ को वाक्य ट्रांसफार्मर से एन्कोड करें (जैसे, `all-MiniLM-L6-v2`) 384 आयामी वेक्टर।
2. UMAP के साथ आयाम को ~ 5 आयाम तक कम करें। BERT एम्बेडेड क्लस्टरिंग के लिए बहुत अधिक गहरे हैं।
3. HDBSCAN के साथ क्लस्टर। घनत्व आधारित, चर आकार के क्लस्टर और एक "बाह्य" लेबल का उत्पादन करता है।
4. प्रत्येक क्लस्टर के लिए, शीर्ष शब्दों को निकालने के लिए क्लस्टर के दस्तावेजों पर वर्ग आधारित TF-IDF की गणना करें।
> 1. 用句子 ट्रांसफार्मर(如 `all-MiniLM-L6-v2`)编码每篇文档──384 维向量──
2. यूएमएपी 降维到大约5维度.
3. HDBSCAN 聚类── घनत्व पर आधारित, उत्पन्न变大小聚类 तथा "离群值" 标签──
4. प्रत्येक वर्ग के लिए, वर्ग के दस्तावेजों पर गणना के आधार पर TF-IDF शीर्ष श्रेणी के शब्द निकालने के लिए।

आउटपुट प्रति दस्तावेज़ एक विषय है (और -1 आउटलियर लेबल) । वैकल्पिक रूप से, एचडीबीएससीएएन के संभावना वेक्टर के माध्यम से एक नरम सदस्यता।
> 输出是每篇文档一个主题 (加上 -1 离群值标签) ⋅可选地,通过HDBSCAN的概率向量获得软成员资格──

> **【中文解读】**इस भाग के माध्यम से कोड को शून्य से लागू किया जा सकता है कोर एल्गोरिदम। इस तरह के "शुरुआत से" तरीके से फ्रेमवर्क के पीछे के सिद्धांत को समझने में मदद मिलेगी, समस्याओं का सामना करते समय ब्लैक बॉक्स में फंस नहीं जाएगा।

> **【拓展：大语言模型的工程实践】**जीपीटी से चैटजीपीटी, एनएलपी के क्षेत्र में "प्रत्येक कार्य को प्रशिक्षित करने के लिए एक मॉडल" से "एक मॉडल सभी कार्य को हल करने के लिए" के लिए एक प्रकार के परिवर्तन का अनुभव किया गया है।

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) वर्तमान उद्यम एआई 应用 में सबसे लोकप्रिय संरचना हैः उपयोगकर्ता पूछताछ पहले संबंधित दस्तावेज टुकड़े को जांचें, फिर से जांच परिणाम के रूप में ऊपर नीचे दिए गए LLM  生成答案── इस तरह LLM ज्ञान过时和幻觉问题──向量数据库── जैसे कि Milvus、Pinecone、Weaviate) RAG 系统 का मूल घटक है──

> **【拓展：NLP 的多语言挑战】**विश्व में 7000 से अधिक भाषाएं हैं, लेकिन एनएलपी अध्ययन मुख्य रूप से अंग्रेजी जैसे कुछ भाषाओं पर केंद्रित है।


## इसे बनाओ, इसे पूरा करो।
```figure
topic-drift
```

## इसे बनाओ

### चरण 1: Sikit-learn के माध्यम से LDA
> ध्यान देंः हटा दिया गया रुक प्रयोग शब्द, min_df 和 max_df 过罕见和无处不在的词, CountVectorizer का उपयोग करें, TfidfVectorizer नहीं), क्योंकि LDA 期望原始计数──

```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np


def fit_lda(documents, n_topics=5, max_features=1000):
    cv = CountVectorizer(
        max_features=max_features,
        stop_words="english",
        min_df=2,
        max_df=0.9,
    )
    X = cv.fit_transform(documents)
    lda = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=42,
        max_iter=50,
        learning_method="online",
    )
    doc_topic = lda.fit_transform(X)
    feature_names = cv.get_feature_names_out()
    return lda, cv, doc_topic, feature_names


def print_top_words(lda, feature_names, n_top=10):
    for idx, topic in enumerate(lda.components_):
        top_idx = np.argsort(-topic)[:n_top]
        words = [feature_names[i] for i in top_idx]
        print(f"topic {idx}: {' '.join(words)}")
```

नोटः स्टॉपवर्ड हटाए गए, min_df और max_df दुर्लभ और सर्वव्यापी शब्दों को फ़िल्टर करते हैं, CountVectorizer (TfidfVectorizer नहीं) क्योंकि LDA कच्चे गिनती की उम्मीद करता है।
> `Topic != -1`                                                                                                                                                                                                                                                              `min_topic_size`控制 HDBSCAN का न्यूनतम聚类大小;BERTopic 库默认为 10──本例为课程规模显然设置为 15── 10,000 से अधिक 文档语料,增加到50或100──

### चरण 2: BERTopic (उत्पादन)
> 两种方法都输出主题词――问题是这些词是否连贯――

```python
from bertopic import BERTopic

topic_model = BERTopic(
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    min_topic_size=15,
    verbose=True,
)

topics, probs = topic_model.fit_transform(documents)
info = topic_model.get_topic_info()
print(info.head(20))
valid_topics = info[info["Topic"] != -1]["Topic"].tolist()
for topic_id in valid_topics[:5]:
    print(f"topic {topic_id}: {topic_model.get_topic(topic_id)[:10]}")
```

फ़िल्टर चालू है `Topic != -1`BERTopic के आउटलीयर बाल्ट को छोड़ देता है (दस्तावेज़ HDBSCAN क्लस्टर नहीं कर सका) । `min_topic_size`HDBSCAN के न्यूनतम क्लस्टर आकार को नियंत्रित करता है; BERTopic के पुस्तकालय डिफ़ॉल्ट 10 है। इस उदाहरण में यह पाठ के पैमाने के लिए स्पष्ट रूप से 15 पर सेट किया गया है। 10,000 से अधिक दस्तावेजों के लिए, 50 या 100 तक बढ़ाएं।
> - **主题连贯度（c_v）。**结合滑动窗口上下文中顶级词对的 NPMI(归一化逐点互信息),分数聚合为主题向量,通过余弦相似度比较这些向量──越高越好──使用 `gensim.models.CoherenceModel`配 `coherence="c_v"`
- **主题多样性。**सभी विषयों में शीर्ष श्रेणी के शब्दों में एकमात्र शब्दों का अनुपात──越高越好── विषयों में कोई भार नहीं है──
- **定性检查。**阅读每题的顶级词――它们是否命名为一个真实的东西?

### चरण 3: मूल्यांकन

दोनों ही तरीकों से विषय के शब्द उत्पन्न होते हैं। प्रश्न यह है कि क्या ये शब्द एक दूसरे के साथ मेल खाते हैं।

- **Topic coherence (c_v).**स्लाइडिंग-विंडो संदर्भों पर शीर्ष शब्द जोड़े के NPMI (सामान्य बिंदु के अनुसार पारस्परिक जानकारी) को जोड़ता है, विषय वेक्टरों में स्कोर को एकत्र करता है, और कॉसिन समानता के माध्यम से उन वेक्टरों की तुलना करता है। उच्च बेहतर है। उपयोग `gensim.models.CoherenceModel`के साथ`coherence="c_v"`. .
- **Topic diversity.**सभी विषयों के शीर्ष शब्दों में अद्वितीय शब्दों का अंश। उच्च बेहतर है (विषय ओवरलैप नहीं करते हैं) ।
- **Qualitative inspection.**क्या वे किसी वास्तविक चीज़ का नाम देते हैं? मानव न्याय अभी भी रक्षा की आखिरी रेखा है।


> **【拓展：Prompt Engineering 与 LLM 应用】**शीघ्र इंजीनियरिंग  नेल्पी  इंजीनियरों के मूल कौशल बन गए हैं  शून्य-शॉट से लेकर कुछ-शॉट तक, सोच-विचार श्रृंखला से लेकर प्रतिक्रिया तक, विभिन्न सुझाव रणनीति विभिन्न परिदृश्यों के लिए लागू होती हैं                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

## कौन सी चुनना है

| Situation | Pick |
|-----------|------|
| Short text (tweets, reviews, headlines) | BERTopic |
| Long documents with topic mixtures | LDA |
| No GPU / limited compute | LDA or NMF |
| Need document-level multi-topic distributions | LDA |
| LLM integration for topic labeling | BERTopic (direct support) |
| Resource-constrained edge deployment | LDA |
| Max semantic coherence | BERTopic |

सबसे बड़ा व्यावहारिक विचार दस्तावेज़ लंबाई है। BERT एम्बेडेड ट्रिंकट; LDA किसी भी लंबाई पर काम करता है। एम्बेडेड मॉडल के संदर्भ से अधिक लंबे दस्तावेजों के लिए, या तो टुकड़ा + संकलित या LDA का उपयोग करें।

> **【中文解读】**इस भाग में दिखाया गया है कि इस तकनीक को कैसे तेजी से लागू किया जाए। इस प्रकार के एक परिपक्व ढांचे का उपयोग करके बग कम किए जा सकते हैं और विकास दक्षता में सुधार किया जा सकता है।


## इसे फ्रेमवर्क के साथ लागू करें

2026 स्टैकः
> 2026 साल तकनीकी:

- **BERTopic.**संक्षिप्त पाठ और अर्थशास्त्र के लिए कोई भी मायने रखता है।
- **`gensim.models.LdaModel`.**उत्पादन के लिए क्लासिक एलडीए, परिपक्व, युद्ध-परीक्षण.
- **`sklearn.decomposition.LatentDirichletAllocation`.**प्रयोगों के लिए आसान एलडीए।
- **NMF.**गैर-नकारात्मक मैट्रिक्स फैक्टरिज़ेशन. एलडीए के लिए त्वरित विकल्प, लघु पाठ पर तुलनात्मक गुणवत्ता।
- **Top2Vec.**BERTopic के समान डिजाइन। छोटा समुदाय लेकिन कुछ बेंचमार्क पर अच्छा।
- **FASTopic.**बहुत बड़े कॉर्पो पर BERTopic से अधिक नया, तेज़।
- **LLM-based labeling.**किसी भी क्लस्टरिंग चलाएं, फिर प्रत्येक क्लस्टर का नाम देने के लिए एक मॉडल को पूछें।
> - **BERTopic。**短文本和语义重要的场景的默认选择──
- **`gensim.models.LdaModel`。**生产级经典 LDA, परिपक्व,久经验──
- **`sklearn.decomposition.LatentDirichletAllocation`。** प्रयोग सरल LDA से
- **NMF。**गैर-ऋणात्मक矩阵分解──LDA का तीव्र प्रतिस्थापन,短文上质量相当──
- **Top2Vec。**类似BERTopic的设计──社区较小但在某些基准上表现良好──
- **FASTopic。**更新,在超大语料上比BERTopic 快──
- **基于 LLM 的标注。**运行任何聚类,然后提示模型命名每个聚类──

> **【中文解读】**इस खंड में इस बात पर ध्यान दिया गया है कि मॉडल को उपलब्ध उत्पादों के रूप में कैसे तैनात किया जाए। मूल से लेकर उत्पादन स्तर तक, प्रदर्शन अनुकूलन, त्रुटि प्रसंस्करण, निगरानी आदि के कई आयामों पर विचार करने की आवश्यकता है।


## इसे भेजें उत्पाद

`outputs/skill-topic-picker.md`:
> 保存为 `outputs/skill-topic-picker.md`:

```markdown
---
name: topic-picker
description: Pick LDA or BERTopic for a corpus. Specify library, knobs, evaluation.
version: 1.0.0
phase: 5
lesson: 15
tags: [nlp, topic-modeling]
---

Given a corpus description (document count, avg length, domain, language, compute budget), output:

1. Algorithm. LDA / NMF / BERTopic / Top2Vec / FASTopic. One-sentence reason.
2. Configuration. Number of topics: `recommended = max(5, round(sqrt(n_docs)))`, clamped to 200 for corpora under 40,000 docs; permit >200 only when the corpus is genuinely large (>40k) and note the increased compute cost. `min_df` / `max_df` filters and embedding model for neural approaches also belong here.
3. Evaluation. Topic coherence (c_v) via `gensim.models.CoherenceModel`, topic diversity, and a 20-sample human read.
4. Failure mode to probe. For LDA, "junk topics" absorbing stopwords and frequent terms. For BERTopic, the -1 outlier cluster swallowing ambiguous documents.

Refuse BERTopic on documents longer than the embedding model's context window without a chunking strategy. Refuse LDA on very short text (tweets, reviews under 10 tokens) as coherence collapses. Flag any n_topics choice below 5 as likely wrong; flag >200 on corpora under 40k docs as likely over-splitting.
```

> **【中文解读】**练习题按照易/中级/难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;


## अभ्यास विषय

1. **Easy.**20 न्यूजग्रुप डेटासेट पर 5 विषयों के साथ फिट एलडीए। प्रत्येक विषय पर शीर्ष 10 शब्द प्रिंट करें। प्रत्येक विषय को हाथ से लेबल करें। क्या एल्गोरिथम ने वास्तविक श्रेणियां पाई हैं?
2. **Medium.**BERTopic को एक ही 20 न्यूजग्रुप उपसमूह पर फिट करें। खोजे गए विषयों की संख्या, शीर्ष शब्दों और गुणात्मक सुसंगतता की तुलना LDA के साथ करें। वास्तविक श्रेणियों में कौन सा अधिक साफ रूप से सतह पर आता है?
3. **Hard.**अपने कॉर्पस पर LDA और BERTopic दोनों के लिए c_v सुसंगतता की गणना करें। 5, 10, 20, 50 विषयों के साथ प्रत्येक को चलाएं। प्लॉट सुसंगतता बनाम विषय संख्या। विषय संख्याओं के बीच कौन सी विधि अधिक स्थिर है, इसकी रिपोर्ट करें।
> 1. **简单。**20 न्यूजग्रुप में आँकड़ों के संग्रह पर 5 विषयों के साथ उपयुक्त LDAएँ छपाई करें। प्रत्येक विषय के शीर्ष 10 शब्दों को छापें।
2. **中等。**इसी तरह 20 न्यूजग्रुपों में एक साथ BERTopic को भी शामिल किया गया है।
3. **困难。**अपने भाषण पर गणना LDA तथा BERTopic के c_v 连贯度──分别用5、10、20、50 题运行──绘制连贯度 vs.题数──报告哪种方法在题数变化下更稳定──

> **【中文解读】**术语表中的"क्या लोग कहते हैं" बनाम "क्या वास्तव में इसका मतलब है" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## कीवर्ड्स  शब्द खोज तालिका

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Topic | A thing the corpus is about | A probability distribution over words (LDA) or a cluster of similar documents (BERTopic). |
| Mixed membership | Doc is multiple topics | LDA assigns each document a distribution over all topics. |
| UMAP | Dimensionality reduction | Manifold learning that preserves local structure; used in BERTopic. |
| HDBSCAN | Density clustering | Finds variable-size clusters; produces "noise" label (-1) for outliers. |
| c_v coherence | Topic quality metric | Average pointwise mutual information of top topic words within sliding windows. |
>  शब्द  लोग अक्सर कहते हैं  वास्तविक अर्थ 
|------|-----------|---------|
| 主题 | 语料关于的东西 | 词的概率分布（LDA）或相似文档的聚类（BERTopic）。 |
| 混合成员资格 | 文档是多个主题 | LDA 为每篇文档分配所有主题上的分布。 |
| UMAP | 降维 | 保留局部结构的流形学习；BERTopic 中使用。 |
| HDBSCAN | 密度聚类 | 找到变大小聚类；为离群值产生 "噪声" 标签（-1）。 |
| c_v 连贯度 | 主题质量指标 | 滑动窗口内顶级主题词的平均逐点互信息。 |

> **【中文解读】**延伸阅读 प्रदान करता है गहन सीखने के लिए उच्च गुणवत्ता वाले संसाधनों। ये लेख और पाठ्यक्रम इस क्षेत्र के लिए क्लासिक संदर्भ हैं, जो गहन समझ की आवश्यकता वाले पाठकों के लिए उपयुक्त हैं।


## आगे पढ़ना 延伸閱讀

- [Blei, Ng, Jordan (2003). Latent Dirichlet Allocation](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf) LDA पेपर।
- [Grootendorst (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure](https://arxiv.org/abs/2203.05794) BERTopic पेपर।
- [Röder, Both, Hinneburg (2015). Exploring the Space of Topic Coherence Measures](https://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf) कागज जो सी_वी और दोस्तों को पेश किया।
- [BERTopic documentation](https://maartengr.github.io/BERTopic/) उत्पादन संदर्भ। उत्कृष्ट उदाहरण।
> - [Blei, Ng, Jordan (2003). Latent Dirichlet Allocation](https://www.jmlr.org/papers/volume3/blei03a/blei03a.pdf) LDA 论文──
- [Grootendorst (2022). BERTopic: Neural topic modeling with a class-based TF-IDF procedure](https://arxiv.org/abs/2203.05794) BERTopic 论文──
- [Röder, Both, Hinneburg (2015). Exploring the Space of Topic Coherence Measures](https://svn.aksw.org/papers/2015/WSDM_Topic_Evaluation/public.pdf) 引入 c_v 及相关标标的论文──
- [BERTopic documentation](https://maartengr.github.io/BERTopic/) 生产参考──优秀示例──
