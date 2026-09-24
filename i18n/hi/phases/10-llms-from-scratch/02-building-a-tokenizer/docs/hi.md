# खरोंच से एक टोकन बनाने से शून्य से निर्माण分词器

> पाठ 1 आपको एक खिलौना देता है।

> **【中文解读】**प्रथम श्रेणी का बीपीई एक खिलौना है, इस श्रेणी का निर्माण उत्पादन श्रेणी分词器:处理 यूनिकोड、空白归归一化、特殊 टोकन、字节级回退(让任何输入都能编码,包括爱默契和中文) 👇

> **【拓展：tiktoken/HuggingFace】**जीपीटी-4 के टिकटोक और लामा के वाक्य का टुकड़ा उत्पादन श्रेणी के शब्दयंत्रों के कार्यान्वयन में शामिल है। इनकी आंतरिक सिद्धांतों को समझने से प्रम्प्ट 工程 और लागत नियंत्रण को अनुकूलित करने में मदद मिलती है।

>  **【前置】**学本节前 कृपया पहले समझेंः(1) चरण 10·01(Tokenizers: BPE/WordPiece/SentencePiece)  समझें BPE 合并循环和合并表的概念;(2) यूनिकोड और UTF-8 编码codepoint、字节、NFC/NFKC 归一化的区别;(3) 正则表达式特别是`\p{L}``\p{N}`、负向先行断言 `(?!\S)`;(4) पायथन `regex`库( मानक नहीं `re`, क्योंकि `re`(→ Unicode property)

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 10, Lesson 01 (Tokenizers: BPE, WordPiece, SentencePiece)
**Time:** ~90 minutes

## सीखने के लक्ष्य

- एक उत्पादन-ग्रेड बीपीई टोकनराइज़र बनाएं जो यूनिकोड, व्हाइटस्पेस नॉर्मलाइजेशन और विशेष टोकन को संभालता है
  构建处理 यूनिकोड、空白归归化和特殊代币的生产级 BPE 分词器
- बाइट-स्तर के बैकअप को लागू करें ताकि टोकनइज़र अज्ञात टोकन के बिना किसी भी इनपुट (इमोजी, सीजेके और कोड सहित) को कोड कर सके
  实现字节级回退,分词器能编码任何输入(包括 इमोजी、CJK、代码) बिना अज्ञात टोकन उत्पन्न
- BPE विलय लागू करने से पहले शब्द सीमाओं पर पाठ को विभाजित करने वाले पूर्व-टोकेनाइज़ेशन रेजेक्स पैटर्न जोड़ें
  添加预分词正则模式,在 BPE 合并前按词边界分文本
- एक कॉर्पस पर कस्टम टोकनराइज़र को प्रशिक्षित करें और बहुभाषी पाठ पर टिक्टोकन के खिलाफ इसके संपीड़न अनुपात का मूल्यांकन करें
  भाषा सामग्री पर स्वयं परिभाषित शब्द निकालने का अभ्यास करें, और बहुभाषी ग्रंथों पर इसका मूल्यांकन करें

> **【中文解读】**इस वर्ग का उद्देश्य है पहले वर्ग के खिलौने बीपीई को उत्पादन श्रेणी के लिए अपग्रेड करना। इसमें महत्वपूर्ण सुधार शामिल हैंः यूनिकोड 归一化(NFKC) 预分词正则(跨词边界的合并防止) 字节级回归(零未知 टोकन) 特殊 टोकन 管理(BOS/EOS/聊天模板标记器) ⋅ ये "पूरे इंटरनेट" के लिए आवश्यक तंत्र हैं।

## समस्या  समस्या परिचय

पाठ 01 से आपका BPE टोकन टाइगर अंग्रेजी पाठ पर काम करता है अब इसे जापानी या इमोजी या मिश्रित टैब और स्थानों के साथ पायथन कोड पर फेंक दें।

> अपने प्रथम श्रेणी के बीपीई 分词器能处理英文文本──现在给它日文──或是爱莫吉──或混合制表符和空格的 Python 代码──

यह टूट जाता है.

> यह टूट जाएगा.

यह इसलिए नहीं है क्योंकि बीपीई गलत है - क्योंकि कार्यान्वयन अधूरा है. एक उत्पादन टोकनराइज़र किसी भी एन्कोडिंग में कच्चे बाइट्स को संभालता है, विभाजन से पहले यूनिकोड को सामान्य बनाता है, विशेष टोकन को प्रबंधित करता है जो कभी विलय नहीं होते हैं, उपशब्द विभाजन के साथ श्रृंखला पूर्व टोकनकरण, और यह सब इतनी तेजी से करता है कि प्रशिक्षण पाइपलाइन को 15 ट्रिलियन टोकन को संसाधित करने में बाधा नहीं आती है।

> यह इसलिए नहीं है क्योंकि बीपीई में समस्याएं हैं, बल्कि इसलिए है क्योंकि यह पूरा नहीं है। उत्पादन श्रेणी में शब्दयंत्र किसी भी कोड के मूल तत्वों को संसाधित करता है, विभाजन से पहले Unicode को एकीकरण में शामिल करता है, विशेष टोकन को संसाधित करने में कभी भाग नहीं लेता है,串联预分词与子词分割, और सभी संचालन पर्याप्त रूप से तेजी से होते हैं, 15 बिलियन टोकन के प्रशिक्षण ट्यूबलाइन की बोतल को संसाधित नहीं करेगा।

GPT-2 के टोकन 50257 टोकन है। लामा 3 में 128,256 हैं। GPT-4 में लगभग 100,000 हैं। ये खिलौना संख्या नहीं हैं। उन शब्दावली के पीछे के मेज टेबल को सैकड़ों गीगाबाइट टेक्स्ट पर प्रशिक्षित किया गया था, और आसपास की मशीनें -- सामान्यीकरण, पूर्व-टोकनाइज़ेशन, विशेष टोकन इंजेक्शन, चैट टेम्पलेट स्वरूपण -- वह है जो एक टोकनराइज़र को अलग करती है जो "हैलो वर्ल्ड" को संभालने वाला है और एक जो पूरे इंटरनेट को संभालने वाला है।

> जीपीटी-2 के विभाजनकर्ता में 50,257 टोकन हैं। लामा 3 में 128,256 个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个

आप उस मशीन का निर्माण करने जा रहे हैं।

> तुम उस तंत्र का निर्माण करोगे

> **【中文解读】**生产级分词器不是单一算法,而是一个五阶段管线:归一化 → 预分词 → BPE 合并 → 特殊代币注入 → ID 映射──每个阶段解决不同的问题──例如 NFKC 归一化把 "fi" 连字(U+FB01) 变成 "fi" 两个字符,预分词防止 "猫" 被合并出 "e c" 这样代币──

>  **【类比】**उत्पादन श्रेणी分词器像"邮局的信件处理流水线":归一化是"统一邮编格式"(U+FB01 "fi" → "fi",全角字母 → 半角),预分词是"按目的地先分堆"(按词边界、数字、标点切,避免跨城市混装),BPE 合并是"高频包裹自动拼箱"(常见词直接整箱),特殊代币是"挂号信标签"(BOS/EOS/PAD 最后永远不参与拼箱),才是"贴条形码"(ID 映射) ⋅任何套漏掉,邮件就乱.

> **【拓展：Llama 3 的分词器升级】**Meta 在 Llama 3 中将词表从 32K (Llama 2 के वाक्य) से बढ़कर 128K (BPE) तक), विशेष रूप से गैर-अंग्रेजी अक्षरों के टोकन को बढ़ाया गया है 分配── यह परिवर्तन बहुभाषी संपीड़न दक्षता को लगभग 2 गुना बढ़ाता है, लेकिन एम्बेड किए गए矩阵 तत्वों की संख्या भी 4 गुना बढ़ी है।

## अवधारणा का मूल अवधारणा

### पूरी पाइपलाइन

एक उत्पादन टोकन एक एल्गोरिथ्म नहीं है, यह पांच चरणों की पाइपलाइन है, प्रत्येक एक अलग समस्या को हल करता है।

> उत्पादन श्रेणी शब्दयंत्र एक एकल एल्गोरिथ्म नहीं है। यह एक पांच चरणों की पाइपलाइन है, प्रत्येक चरण में विभिन्न समस्याएं हल होती हैं।

```mermaid
graph LR
    A[Raw Text] --> B[Normalize]
    B --> C[Pre-Tokenize]
    C --> D[BPE Merge]
    D --> E[Special Tokens]
    E --> F[Token IDs]

    style A fill:#1a1a2e,stroke:#e94560,color:#fff
    style B fill:#1a1a2e,stroke:#e94560,color:#fff
    style C fill:#1a1a2e,stroke:#e94560,color:#fff
    style D fill:#1a1a2e,stroke:#e94560,color:#fff
    style E fill:#1a1a2e,stroke:#e94560,color:#fff
    style F fill:#1a1a2e,stroke:#e94560,color:#fff
```

प्रत्येक चरण का एक विशिष्ट कार्य होता हैः

> प्रत्येक चरण में विशिष्ट कार्य हैं:

| Stage | What It Does | Why It Matters |
|-------|-------------|----------------|
| Normalize | NFKC Unicode, lowercase optional, strip accents optional | "fi" ligature (U+FB01) becomes "fi" (two chars). Without this, same word gets different tokens. |
| Pre-Tokenize | Split text into chunks before BPE | Prevents BPE from merging across word boundaries. "the cat" should never produce a token "e c". |
| BPE Merge | Apply learned merge rules to byte sequences | The core compression. Turns raw bytes into subword tokens. |
| Special Tokens | Inject [BOS], [EOS], [PAD], chat template markers | These tokens have fixed IDs. They never participate in BPE merges. The model needs them for structure. |
| ID Mapping | Convert token strings to integer IDs | The model sees integers, not strings. |

### बाइट लेवल बीपीई

पाठ 01 के टोकनराइज़र UTF-8 बाइट्स पर काम किया। यह सही कॉल था। लेकिन हमने कुछ महत्वपूर्ण छोड़ दियाः क्या होता है जब वे बाइट्स UTF-8 वैध नहीं हैं?

> प्रथम श्रेणी का शब्दकोश UTF-8 字节 पर संचालित होता है। यह सही विकल्प है। लेकिन हमने कुछ महत्वपूर्ण चीजों को छोड़ दिया हैः जब ये वर्ण UTF-8 字节 प्रभावी नहीं होते हैं तो क्या होता है?

बाइट-स्तर बीपीई हर संभव बाइट मान (0-255) को वैध टोकन के रूप में मानकर इसे हल करता है. आपकी आधार शब्दावली ठीक 256 प्रविष्टियां है. कोई भी फ़ाइल - पाठ, द्विआधारी, भ्रष्ट - एक अज्ञात टोकन उत्पन्न किए बिना टोकन किया जा सकता है।

> 字节级 BPE 通过将每个可能的字节值(0-255) को इस समस्या को हल करने के लिए एक वैध टोकन के रूप में देखा गया है।

GPT-2 ने एक चाल जोड़ीः प्रत्येक बाइट को प्रिंट करने योग्य यूनिकोड वर्ण में मैप करें ताकि शब्दावली मानव-पठनीय बनी रहे। बाइट 0x20 (अंतरिक्ष) उनके मैपिंग में वर्ण "जी" बन जाता है। यह शुद्ध रूप से सौंदर्य प्रसाधन है। एल्गोरिदम पर कोई फर्क नहीं पड़ता।

> GPT-2 एक फ़्लग जोड़ता हैः प्रत्येक वर्ण को एक मुद्रित यूनिकोड फ़ाइल में मैगज़ेट करना, शब्दों को पढ़ने योग्य बनाए रखना।

वास्तविक शक्तिः बाइट स्तर BPE पृथ्वी पर हर भाषा को संभालता है. चीनी वर्ण 3 UTF-8 बाइट्स प्रत्येक हैं. जापानी 3-4 बाइट्स हो सकता है. अरबी, देवनागरी, इमोजी - सभी बस बाइट अनुक्रम. BPE एल्गोरिदम इन बाइट अनुक्रमों में पैटर्न ठीक उसी तरह पाता है जैसे यह अंग्रेजी ASCII बाइट्स में पैटर्न पाता है.

> सच्ची शक्तिः字节 श्रेणी BPE 处理地球上每种语言──中文字符每占 3 个 UTF-8字节──日文占 3-4 个字节──阿拉伯文、天城文、emoji都只是字节序列──BPE 算法 इन字节序列 में मॉडल खोजने का तरीका अंग्रेजी में ASCII 字节 में बिल्कुल समान है──

> **【中文解读】**字节级 BPE के मूल लाभः आधार文字表恰好 256 字节值,任何输入都能编码;;GPT-2 ने एक "花招" भी बनाया है, जिसमें प्रत्येक字节 को एक मुद्रित यूनिकोड 字符 में मैप किया गया है, जिससे शब्द表 अधिक आसानी से पढ़ा जा सके।

### पूर्व टोकनकरण

इससे पहले कि BPE आपके पाठ को छू ले, आपको इसे टुकड़ों में विभाजित करना होगा। यह विलय एल्गोरिदम को शब्द सीमाओं को कवर करने वाले टोकन बनाने से रोकता है।

> BPE  अपने पाठ को संसाधित करने से पहले, आपको इसे ब्लॉक में विभाजित करने की आवश्यकता है।

GPT-2 पाठ को विभाजित करने के लिए एक रेजेक्स पैटर्न का उपयोग करता हैः

> जीपीटी-2 प्रयोग करने के लिए सामान्य अभिव्यक्ति को विभाजित करने के लिएः

```
'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+
```

यह पैटर्न संकुचन ("don't" बन जाता है "don" + "'t"), वैकल्पिक अग्रणी स्थानों, संख्याओं, विरामचिह्न और सफेद स्थानों वाले शब्दों पर विभाजित होता है। अग्रणी स्थान शब्द से जुड़ा रहता है - इसलिए "cat" ["the", "cat"] बन जाता है, न कि ["the", " ", "cat"] ।

> इस मोड को संक्षिप्त में विभाजित करके लिखें। "don't" 变成 "don" + "'t") 带可选前导空格的词、数字、标点和空格。前导空格保持在词上所以"the cat" 变成 ["the", "cat"],而不是 ["the", "", "cat"]。

Llama SentencePiece का उपयोग करता है, जो regex को पूरी तरह से छोड़ देता है। यह कच्चे बाइट स्ट्रीम को एक लंबे अनुक्रम के रूप में व्यवहार करता है और BPE एल्गोरिदम को सीमाओं का पता लगाने देता है। यह सरल है लेकिन BPE को क्रॉस-वर्ड टोकन बनाने के लिए अधिक स्वतंत्रता देता है।

> Llama उपयोग वाक्य टुकड़ा, पूरी तरह से सही अभिव्यक्ति से कूद गया। यह एक लंबी श्रृंखला के रूप में देखा जाएगा, BPE  एल्गोरिदम को खुद सीमा निर्धारित करने के लिए अनुमति देता है। यह सरल है, लेकिन BPE को अधिक बनाने के लिए अनुमति देता है।

विकल्प मायने रखता है। जीपीटी -2 का रेजेक्स टोकनराइज़र को यह सीखने से रोकता है कि एक शब्द के अंत में "the" और अगले की शुरुआत में "the" को मिलाया जाना चाहिए। SentencePiece इसे अनुमति देता है, जो कभी-कभी अधिक कुशल संपीड़न का उत्पादन करता है लेकिन कम व्याख्या योग्य टोकन।

> यह विकल्प महत्वपूर्ण है। जीपीटी-2 का सही नियम एक शब्द के अंत में "the" और अगले में "the" के साथ एक शब्द का आरंभ करने से रोकता है।

### विशेष टोकन

प्रत्येक उत्पादन टोकनराइज़र संरचनात्मक मार्करों के लिए टोकन आईडी आरक्षित करता हैः

> प्रत्येक उत्पादन श्रेणी分词器都为结构标记保留 टोकन आईडी:

| Token | Purpose | Used By |
|-------|---------|---------|
| `[BOS]` / `<s>` | Beginning of sequence | Llama 3, GPT |
| `[EOS]` / `</s>` | End of sequence | All models |
| `[PAD]` | Padding for batch alignment | BERT, T5 |
| `[UNK]` | Unknown token (byte-level BPE eliminates this) | BERT, WordPiece |
| `<\|im_start\|>` | Chat message boundary start | ChatGPT, Qwen |
| `<\|im_end\|>` | Chat message boundary end | ChatGPT, Qwen |
| `<\|user\|>` | User turn marker | Llama 3 |
| `<\|assistant\|>` | Assistant turn marker | Llama 3 |

विशेष टोकन कभी भी बीपीई द्वारा विभाजित नहीं होते हैं। वे विलय एल्गोरिथ्म चलाने से ठीक पहले मेल खाते हैं, उनकी फिक्स्ड आईडी के साथ प्रतिस्थापित होते हैं, और आसपास के पाठ को सामान्य रूप से टोकन किया जाता है।

> 特殊 टोकन 永远不会被 BPE 拆分──它们在合并算法运行之前精确匹配,被替换为固定ID,周围文本正常分词──

> **【中文解读】**特殊 टोकन 分词器中"不可触碰" के लिए आरक्षित चिह्नः`[BOS]`(序列开始)`[EOS]`(序列结束)`[PAD]`(批次填充) 聊天模板标记等──它们有固定的ID,永远不参与BPE 合并,而在合并之前通过精确匹配被提取出来──Llama 3 使用 `<|start_header_id|>``<|end_header_id|>``<|eot_id|>`वार्तालाप संरचना, चैटजीपीटी प्रयोग `<|im_start|>`和 `<|im_end|>`

> **【拓展：聊天模板的工程陷阱】**聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天模板 聊天 聊天模板 聊天 聊天 聊天 聊天 聊天 聊天 聊天 聊天 聊天 聊天 聊天 聊天 聊天 聊天 聊天 聊天 聊天 聊天 聊天 聊 聊天 聊天 聊 聊 聊天 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊 聊`chat_template`जिनजा2 模板机制就是为了标准化这个过程――

> ️ **【易错点】**实现特殊 टोकन 的三个陷:(1) **特殊 token 内含正则元字符**如 `<|im_start|>`मध्य `|`, उपयोग करना होगा`re.escape()`转义,否则在 GPT-2 预分词的正则上会被解析成选择符;(2) **未从 BPE 词表中排除特殊 token**若 `<|im_end|>`                                                                                                                                                                                                                                                              **`add_special_tokens=False` 漏配**调用 `tokenizer.encode(text)`默认会自动加 BOS/EOS,做拼接时会出现 BOS BOS EOS EOS 序列,破坏注意力面具对齐──修复:编码时显式传 `add_special_tokens=False`, अंतिमतःआदर्शता से एकीकरण में प्रवेश किया गया।

### चैट टेम्पलेट्स

यह वह जगह है जहाँ अधिकांश लोग भ्रमित हो जाते हैं और अधिकांश कार्यान्वयन टूट जाते हैं।

> यह वह जगह है जहाँ अधिकांश लोग उलझन में हैं, और यह वह जगह है जहाँ अधिकांश लोग गलत काम करते हैं।

जब आप चैट मॉडल को संदेश भेजते हैं, तो एपीआई संदेशों की एक सूची स्वीकार करता हैः

> जब आप चैट मॉडल संदेश भेजते हैं, एपीआई एक संदेश सूची स्वीकार करता हैः

```
[
  {"role": "system", "content": "You are helpful."},
  {"role": "user", "content": "Hello"},
  {"role": "assistant", "content": "Hi there!"}
]
```

मॉडल JSON नहीं देखता है। यह एक फ्लैट टोकन अनुक्रम देखता है। चैट टेम्पलेट विशेष टोकन का उपयोग करके संदेशों को उस फ्लैट अनुक्रम में परिवर्तित करता है। प्रत्येक मॉडल यह अलग तरह से करता हैः

> 模型看不到 JSON── यह एक 平的符号序列 देखेगा── विशेष符号 का उपयोग करके संदेश को 平序列 में परिवर्तित करेगा── प्रत्येक मॉडल का अभ्यास अलग हैः

```
Llama 3:
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are helpful.<|eot_id|><|start_header_id|>user<|end_header_id|>

Hello<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Hi there!<|eot_id|>

ChatGPT:
<|im_start|>system
You are helpful.<|im_end|>
<|im_start|>user
Hello<|im_end|>
<|im_start|>assistant
Hi there!<|im_end|>
```

टेम्पलेट गलत हो गया और मॉडल कचरा पैदा करता है. यह एक सटीक प्रारूप पर प्रशिक्षित किया गया था. किसी भी विचलन - एक गायब नई रेखा, एक swapped टोकन, एक अतिरिक्त स्थान - इनपुट को प्रशिक्षण वितरण के बाहर डालता है.

> 模板搞错了模型就会产生垃圾输出―― यह एक सटीक प्रारूप पर प्रशिक्षित है―― किसी भी विकृति अभाव परिवर्तन  विनिमय टोकन多一个空格都会使输入偏离训练分布──

> 🤔 **【困惑】**Q: Llama 3 क्यों त्यागें SentencePiece 改用TikToken?字节级 BPE比原版强在哪? A: 两点关键优势:(1) **SentencePiece 用 ⊗（U+2581）代替空格**, ASCII 字符和原始空格的混在聊天场景下导致 टोकन序列对快速 微小变化过于敏感;टिकटोकन 直接保留前导空格,"hello"和"hello"是不同 टोकन,更稳定;**字节级 BPE 词表恰好 256 个基础 token**, सैद्धांतिक रूप से किसी भी वर्ण क्रम को कोडित कर सकते हैं, जिसमें इमोजी शामिल हैं, विशेष क्षेत्र के वर्ण शामिल हैं, विशिष्ट भाषाओं पर निर्भर नहीं है; वाक्य टुकड़ा शब्द का उपयोग करना यदि किसी विशेष वर्ण से सीधे [UNK] तक प्रशिक्षित नहीं है।

### गति

उत्पादन टोकन के लिए पायथन बहुत धीमा है।

> पायथन 对于生产级分词太慢了──

tiktoken (OpenAI) रास्ट में पायथन बंधन के साथ लिखा गया है। HuggingFace टोकनाइज़र भी रास्ट है। SentencePiece C++ है। ये शुद्ध पायथन पर 10-100x स्पीडअप प्राप्त करते हैं।

> tiktoken(OpenAI) Rust के साथ 编写并提供 Python 绑定──HuggingFace टोकनाइज़र 也是 Rust──SentencePiece 是 C++──这些比纯 Python 快 10-100 倍──

परिप्रेक्ष्य के लिएः Llama 3 के लिए 15 ट्रिलियन टोकन को 1 मिलियन टोकन प्रति सेकंड (फास्ट पायथन) पर प्री-ट्रेनिंग करने में 174 दिन लगेंगे। 100 मिलियन टोकन प्रति सेकंड (रस्ट) पर, इसमें 1.7 दिन लगेंगे।

> उदाहरण: Llama 3 के लिए प्रति सेकंड 100 मिलियन टोकन की गति ️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️

आप पायथन में निर्माण कर रहे हैं एल्गोरिथ्म को समझने के लिए. उत्पादन में, आप एक संकलित कार्यान्वयन का उपयोग करेंगे और केवल पायथन रैपर को छूना होगा.

> आप पायथन का उपयोग करके निर्माण करते हैं ताकि एल्गोरिदम को समझ सकें 

## इसे बनाओ, इसे पूरा करो।
```figure
weight-tying
```

## इसे बनाओ

### चरण 1: बाइट-स्तर एन्कोडिंग

किसी भी स्ट्रिंग को बाइट्स के अनुक्रम में परिवर्तित करें, प्रत्येक बाइट को प्रदर्शित करने के लिए प्रिंट करने योग्य वर्ण में मैप करें, और प्रक्रिया को उलट दें।

> 基础── किसी भी字符串 को字节 क्रम में परिवर्तित करेगा, प्रत्येक字节 को प्रदर्शित करने के लिए मुद्रित करने योग्य अक्षरों में映射 करेगा,并反转该过程──

```python
def bytes_to_tokens(text):
    return list(text.encode("utf-8"))

def tokens_to_text(token_bytes):
    return bytes(token_bytes).decode("utf-8", errors="replace")
```

बाइट की गिनती देखने के लिए बहुभाषी पाठ पर परीक्षण करेंः

```python
texts = [
    ("English", "hello"),
    ("Chinese", "你好"),
    ("Emoji", "🔥"),
    ("Mixed", "hello你好🔥"),
]

for label, text in texts:
    b = bytes_to_tokens(text)
    print(f"{label}: {len(text)} chars -> {len(b)} bytes -> {b}")
```

"हैलो" 5 बाइट्स है. "你好" 6 बाइट्स है (3 प्रति वर्ण). फायर इमोजी 4 बाइट्स है. बाइट स्तर टोकनराइज़र को परवाह नहीं है कि यह किस भाषा है। बाइट्स बाइट्स हैं।

> "हैलो" 5 字节──"你好" 6 字节── प्रत्येक 字符 3 字节)──火焰 इमोजी 4 字节──字节级分词器不关心它是什么语言──字节就是字节──

### चरण 2: रेजेक्स के साथ प्री-टोकनाइज़र

GPT-2 रेजेक्स पैटर्न का उपयोग करके पाठ को टुकड़ों में विभाजित करें। प्रत्येक टुकड़ा BPE द्वारा स्वतंत्र रूप से टोकन किया जाता है।

> प्रयोग GPT-2 正则模式将文本分分为块── प्रत्येक ब्लॉक BPE 独立分词── द्वारा विभाजित किया जाएगा।

```python
import re

try:
    import regex
    GPT2_PATTERN = regex.compile(
        r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
    )
except ImportError:
    GPT2_PATTERN = re.compile(
        r"""'(?:[sdmt]|ll|ve|re)| ?[a-zA-Z]+| ?[0-9]+| ?[^\s\w]+|\s+(?!\S)|\s+"""
    )

def pre_tokenize(text):
    return [match.group() for match in GPT2_PATTERN.finditer(text)]
```

`regex`मॉड्यूल Unicode गुणों को बचाने का समर्थन करता है (`\p{L}`पत्रों के लिए, `\p{N}`संख्याओं के लिए) मानक पुस्तकालय `re`मॉड्यूल नहीं है, तो हम ASCII वर्ण वर्गों पर वापस गिर जाते हैं. उत्पादन बहुभाषी टोकनाइज़र के लिए, स्थापित `regex`. .

> `regex`模块支持 यूनिकोड 属性转义(`\p{L}`表示字母,`\p{N}`表示数字) ・ मानक库 `re`模块不支持,所以我们回到ASCII 字符类──对于生产级多语言分词器,请安装 `regex`

कोशिश करो:

```python
print(pre_tokenize("Hello, world! Don't stop."))
# [' Hello', ',', ' world', '!', " Don", "'t", ' stop', '.']
```

मुख्य स्थान शब्द से जुड़ा रहता है। संकुचन अपोस्ट्रोफ पर विभाजित होता है। अंकन अपने स्वयं के टुकड़े बन जाता है। बीपीई इन सीमाओं के पार टोकन कभी भी विलय नहीं करेगा।

> पूर्व导空格保持在词上──缩写在撇号处分分──标点成为独立块──BPE 永远不会跨越这些边界合并代币──

### चरण 3: बाइट अनुक्रम पर बीपीई

पाठ 01, लेकिन अब स्वतंत्र रूप से पूर्व-टोकन टुकड़े पर काम कर रहे कोर एल्गोरिथ्म.

> प्रथम श्रेणी के मूल एल्गोरिथ्म, लेकिन अब स्वतंत्र रूप से पूर्ववर्ती शब्द के ब्लॉक पर संचालन किया जाता है।

```python
from collections import Counter

def get_byte_pairs(chunks):
    pairs = Counter()
    for chunk in chunks:
        byte_seq = list(chunk.encode("utf-8"))
        for i in range(len(byte_seq) - 1):
            pairs[(byte_seq[i], byte_seq[i + 1])] += 1
    return pairs

def apply_merge(byte_seq, pair, new_id):
    merged = []
    i = 0
    while i < len(byte_seq):
        if i < len(byte_seq) - 1 and byte_seq[i] == pair[0] and byte_seq[i + 1] == pair[1]:
            merged.append(new_id)
            i += 2
        else:
            merged.append(byte_seq[i])
            i += 1
    return merged
```

### चरण 4: विशेष टोकन हैंडलिंग

विशेष टोकन सटीक मिलान और निश्चित आईडी की आवश्यकता है। वे BPE पूरी तरह से बायपास.

> 特殊 टोकन 需要精确匹配和固定 ID──它们完全绕过BPE──

```python
class SpecialTokenHandler:
    def __init__(self):
        self.special_tokens = {}
        self.pattern = None

    def add_token(self, token_str, token_id):
        self.special_tokens[token_str] = token_id
        escaped = [re.escape(t) for t in sorted(self.special_tokens.keys(), key=len, reverse=True)]
        self.pattern = re.compile("|".join(escaped))

    def split_with_specials(self, text):
        if not self.pattern:
            return [(text, False)]
        parts = []
        last_end = 0
        for match in self.pattern.finditer(text):
            if match.start() > last_end:
                parts.append((text[last_end:match.start()], False))
            parts.append((match.group(), True))
            last_end = match.end()
        if last_end < len(text):
            parts.append((text[last_end:], False))
        return parts
```

### चरण 5: पूर्ण टोकनइज़र वर्ग

सब कुछ एक साथ चेन करें: सामान्यीकरण, विशेष टोकन पर विभाजित, पूर्व टोकन, बीपीई विलय, मानचित्र से आईडी तक।

> सभी चरणों को जोड़नाः归一化、按特殊代号 分割、预分词、BPE 合并、映射到ID──

```python
import unicodedata

class ProductionTokenizer:
    def __init__(self):
        self.merges = {}
        self.vocab = {i: bytes([i]) for i in range(256)}
        self.special_handler = SpecialTokenHandler()
        self.next_id = 256

    def normalize(self, text):
        return unicodedata.normalize("NFKC", text)

    def train(self, text, num_merges):
        text = self.normalize(text)
        chunks = pre_tokenize(text)
        chunk_bytes = [list(chunk.encode("utf-8")) for chunk in chunks]

        for i in range(num_merges):
            pairs = Counter()
            for seq in chunk_bytes:
                for j in range(len(seq) - 1):
                    pairs[(seq[j], seq[j + 1])] += 1
            if not pairs:
                break
            best = max(pairs, key=pairs.get)
            new_id = self.next_id
            self.next_id += 1
            self.merges[best] = new_id
            self.vocab[new_id] = self.vocab[best[0]] + self.vocab[best[1]]
            chunk_bytes = [apply_merge(seq, best, new_id) for seq in chunk_bytes]

    def add_special_token(self, token_str):
        token_id = self.next_id
        self.next_id += 1
        self.special_handler.add_token(token_str, token_id)
        self.vocab[token_id] = token_str.encode("utf-8")
        return token_id

    def encode(self, text):
        text = self.normalize(text)
        parts = self.special_handler.split_with_specials(text)
        all_ids = []
        for part_text, is_special in parts:
            if is_special:
                all_ids.append(self.special_handler.special_tokens[part_text])
            else:
                for chunk in pre_tokenize(part_text):
                    byte_seq = list(chunk.encode("utf-8"))
                    for pair, new_id in self.merges.items():
                        byte_seq = apply_merge(byte_seq, pair, new_id)
                    all_ids.extend(byte_seq)
        return all_ids

    def decode(self, ids):
        byte_parts = []
        for token_id in ids:
            if token_id in self.vocab:
                byte_parts.append(self.vocab[token_id])
        return b"".join(byte_parts).decode("utf-8", errors="replace")

    def vocab_size(self):
        return len(self.vocab)
```

### चरण 6: बहुभाषी परीक्षा

असली परीक्षा. अंग्रेजी, चीनी, इमोजी, और कोड फेंक दो।

> ️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️

```python
corpus = (
    "The quick brown fox jumps over the lazy dog. "
    "The quick brown fox runs through the forest. "
    "Machine learning models process natural language. "
    "Deep learning transforms how we build software. "
    "def train(model, data): return model.fit(data) "
    "def predict(model, x): return model(x) "
)

tok = ProductionTokenizer()
tok.train(corpus, num_merges=50)

bos = tok.add_special_token("<|begin|>")
eos = tok.add_special_token("<|end|>")

test_texts = [
    "The quick brown fox.",
    "你好世界",
    "Hello 🌍 World",
    "def foo(x): return x + 1",
    f"<|begin|>Hello<|end|>",
]

for text in test_texts:
    ids = tok.encode(text)
    decoded = tok.decode(ids)
    print(f"Input:   {text}")
    print(f"Tokens:  {len(ids)} ids")
    print(f"Decoded: {decoded}")
    print()
```

चीनी वर्ण प्रत्येक 3 बाइट्स उत्पन्न करते हैं. इमोजी 4 बाइट्स उत्पन्न करता है. इनमें से कोई भी टोकनराइज़र को क्रैश नहीं करता है. कोई भी अज्ञात टोकन उत्पन्न नहीं करता है. यह बाइट स्तर BPE की शक्ति है।

> 中文字符每个产生 3 字节──emoji 产生 4 字节──这些都不会使分词器崩──都不会产生未知代币──这是字节级 BPE 的力量──

> **【中文解读】**ऊपर कोड सभी घटकों को संबद्ध करेगा:归一化 → 特殊代币 分割 → 预分词 → BPE 合并 → ID 映射――测试覆盖英文、中文、emoji、代码和特殊代币的混合场景──字节级 BPE保证任何输入都不会产生未知的代币

> **【拓展：分词速度的工程意义】**纯 Python 分词器每秒处理约1M टोकन,Llama 3 के पूर्व प्रशिक्षण语料有15亿亿 टोकन,Python 需要174 天──tiktoken(Rust 实现) प्रति सेकंड 100M टोकन, केवल 1.7 天──这就是为什么生产级分词器都用编译语言:tiktoken 用Rust,HuggingFace टोकनाइज़र用Rust,SentencePiece 用C++──

## इसे फ्रेमवर्क के साथ लागू करें

### वास्तविक टोकन बनाने वालों की तुलना

Llama 3, GPT-4 और Mistral के वास्तविक टोकन बनाने वाले को लोड करें। देखें कि प्रत्येक पैराग्राफ एक ही बहुभाषी पैराग्राफ को कैसे संभालता है।

> 加载 Llama 3、GPT-4 和 Mistral 的实际分词器──看看每个分词器如何处理同一段多语言文本──

```python
import tiktoken

gpt4_enc = tiktoken.get_encoding("cl100k_base")

test_paragraph = "Machine learning is powerful. 机器学习很强大。 L'apprentissage automatique est puissant. 🤖💪"

tokens = gpt4_enc.encode(test_paragraph)
pieces = [gpt4_enc.decode([t]) for t in tokens]
print(f"GPT-4 ({len(tokens)} tokens): {pieces}")
```

```python
from transformers import AutoTokenizer

llama_tok = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
mistral_tok = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")

for name, tok in [("Llama 3", llama_tok), ("Mistral", mistral_tok)]:
    tokens = tok.encode(test_paragraph)
    pieces = tok.convert_ids_to_tokens(tokens)
    print(f"{name} ({len(tokens)} tokens): {pieces[:20]}...")
```

आप एक ही पाठ के लिए अलग-अलग टोकन गिनती देखेंगे। 128K शब्दावली के साथ Llama 3 सामान्य पैटर्न को मिलाकर अधिक आक्रामक है। 100K के साथ GPT-4 बीच में बैठता है। 32K के साथ मिस्ट्रल अधिक टोकन उत्पन्न करता है लेकिन इसमें एक छोटा एम्बेडिंग परत है।

> आप एक ही पाठ के अलग-अलग टोकन संख्या देखेंगे। लामा 3 के 128K शब्द का प्रदर्शन एक साथ और अधिक सक्रिय है। GPT-4 के 100K बीच में हैं।

समझौता हमेशा एक ही होता हैः बड़ी शब्दावली का अर्थ है छोटे अनुक्रम लेकिन अधिक मापदंड।

> 权衡始终相同: बड़ा शब्द表 का अर्थ होता है छोटा क्रम लेकिन अधिक पैरामीटर

## इसे भेजें उत्पाद

इस पाठ में उत्पादन टोकन बनाने और डिबग करने के लिए एक प्रॉम्प्ट उत्पन्न होता है।`outputs/prompt-tokenizer-builder.md`. .

> इस वर्ग का उत्पादन निर्माण एवं उत्पादन के लिए किया गया है।`outputs/prompt-tokenizer-builder.md`

## अभ्यास विषय

1. **Easy:**एक जोड़ें `get_token_bytes(id)`विधि जो किसी भी टोकन आईडी के लिए कच्चे बाइट्स दिखाता है. इसका उपयोग अपने सबसे आम विलय टोकन वास्तव में क्या प्रतिनिधित्व करते हैं की जांच करने के लिए.
   中文翻译:添加 `get_token_bytes(id)`方法,显示任意 टोकन ID的原始字节──用它检查您最常用的合并 टोकन 实际代表什么──
2. **Medium:**लामा शैली के प्री-टोकनीज़र को लागू करें जो सफेद स्थान और अंकों पर विभाजित होता है लेकिन अग्रणी स्थानों को बनाए रखता है। उसी कॉर्पस पर जीपीटी - 2 रेजेक्स दृष्टिकोण के साथ इसकी शब्दावली की तुलना करें।
   中文翻译:实现 Llama 风格的预分词器,按空格和数字分分但保留前导空格──在相同语料上比较其词表与GPT-2 正则方法──
3. **Hard:**एक चैट टेम्पलेट विधि जोड़े जो सूची लेता है `{"role": ..., "content": ...}`संदेश और Llama 3 चैट प्रारूप के लिए सही टोकन अनुक्रम उत्पन्न करता है. HuggingFace कार्यान्वयन के साथ परीक्षण करें.
   中文翻译:添加聊天模板方法,接受 `{"role": ..., "content": ...}`消息列表并生成 Llama 3 聊天格式的正确代币序列──对照 HuggingFace 实现进行测试──

## कीवर्ड्स  शब्द खोज तालिका

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Byte-level BPE | "Tokenizer that works on bytes" | BPE with a base vocabulary of 256 byte values -- handles any input without unknown tokens | 字节级 BPE，基础词表 256 个字节值 |
| Pre-tokenization | "Splitting before BPE" | Regex or rule-based splitting that prevents BPE from merging across word boundaries | 预分词，防止跨词边界的 token 合并 |
| NFKC normalization | "Unicode cleanup" | Canonical decomposition followed by compatibility composition -- "fi" ligature becomes "fi", fullwidth "A" becomes "A" | NFKC 归一化，统一 Unicode 表示 |
| Chat template | "How messages become tokens" | The exact format for converting a list of role/content messages into a flat token sequence -- model-specific and must match training format | 聊天模板，消息转 token 的格式规则 |
| Special tokens | "Control tokens" | Reserved token IDs that bypass BPE -- [BOS], [EOS], [PAD], chat markers -- matched exactly before merge | 特殊 token，绕过 BPE 的控制标记 |
| Fertility | "Tokens per word" | Ratio of output tokens to input words -- 1.3 for English in GPT-4, 2-3 for Korean, higher means wasted context | 生育率，每词 token 数 |
| tiktoken | "OpenAI tokenizer" | Rust BPE implementation with Python bindings -- 10-100x faster than pure Python | OpenAI 的 Rust 分词器实现 |
| Merge table | "The vocabulary" | Ordered list of byte-pair merges learned during training -- this IS the tokenizer's learned knowledge | 合并表，分词器的核心知识 |

## आगे पढ़ना 延伸閱讀

- [OpenAI tiktoken source](https://github.com/openai/tiktoken)-- GPT-3.5/4 द्वारा उपयोग किए जाने वाले जंग बीपीई कार्यान्वयन
- [HuggingFace tokenizers](https://github.com/huggingface/tokenizers)-- Rust Tokenizer लाइब्रेरी BPE, WordPiece, Unigram का समर्थन
- [Llama 3 paper (Meta, 2024)](https://arxiv.org/abs/2407.21783)-- 128K शब्दावली और टोकनराइज़र प्रशिक्षण के बारे में विवरण
- [SentencePiece (Kudo & Richardson, 2018)](https://arxiv.org/abs/1808.06226)-- भाषा-अज्ञानी टोकनकरण
- [GPT-2 tokenizer source](https://github.com/openai/gpt-2/blob/master/src/encoder.py)-- मूल बाइट-टू-यूनीकोड मानचित्रण
