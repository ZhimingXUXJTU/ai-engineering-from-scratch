# ओसीआर और दस्तावेज़ समझ

> ओसीआर एक तीन चरणों वाला पाइपलाइन है  पाठ बक्से का पता लगाएं, वर्णों को पहचानें, फिर उन्हें बिछाएं। प्रत्येक आधुनिक ओसीआर प्रणाली इन चरणों को फिर से क्रमबद्ध करती है या उन्हें मिला देती है।

> **【中文解读】**ओसीआर (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (O) (OCR) (OCR) (OCR) (OCR) (OCR) (O) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (OCR) (O) (OCR) (O) (OCR) (OCR) (OCR) (O) (OCR) (O) (OCR) (OCR) (O) (OCR) (O) (OCR) (O) (OCR) (O) (OCR) (O) (OCR) (O) (OCR (O) (O) (O) (OCR (O) (OCR (O) (O) (OCR) (O) (O) (OCR (O) (O) (

> **【拓展：文档理解的金融应用】**OCR और दस्तावेज समझ का वित्तीय क्षेत्र में व्यापक उपयोग किया जाता हैः बैंकिंग प्रवाह पहचान, स्वचालित प्रसंस्करण, अनुबंध बुद्धिमान समीक्षा, वित्तीय रिपोर्टिंग विश्लेषण, लेआउटLM, डॉनट आदि मॉडल विजन और पाठ सूचना के एकीकरण को प्राप्त करते हैं, अंत से अंत तक दस्तावेज समझ।

**Type:** Learn + Use | **类型:** 学习 + 应用
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 4 Lesson 06 (Detection), Phase 7 Lesson 02 (Self-Attention) | **前置知识:** Phase 4 Lesson 06（目标检测），Phase 7 Lesson 02（自注意力）
**Time:** ~45 minutes | **时间:** ~45 分钟

## सीखने के लक्ष्य

- क्लासिक ओसीआर पाइपलाइन (डिटेक्ट -> पहचान -> लेआउट) और आधुनिक एंड-टू-एंड विकल्पों (डोनट, क्यूवेन-वीएल-ओसीआर) का पता लगाएं
- सीटीसी (कनेक्शनिस्ट टाइमओरियल क्लासिफिकेशन) को क्रमिक-से-क्रमिक ओसीआर प्रशिक्षण के लिए लागू करना
- बिना प्रशिक्षण के उत्पादन दस्तावेज पार्सिंग के लिए PaddleOCR या EasyOCR का उपयोग करें
- ओसीआर, लेआउट पार्सिंग और दस्तावेज़ समझ में अंतर करें  और प्रत्येक कार्य के लिए सही उपकरण चुनें

> **【中文解读】**सीखने के लक्ष्य इस कक्षा को पूरा करने के बाद जो मूल क्षमताएं होनी चाहिए, उन्हें सूचीबद्ध करते हैं।


## समस्या  समस्या परिचय

पाठ से भरे चित्र हर जगह हैंः रसीदें, चालान, आईडी, स्कैन की गई किताबें, फॉर्म, व्हाइटबोर्ड, साइन, स्क्रीनशॉट। उनमें से संरचित डेटा निकालना  न केवल वर्ण, बल्कि "यह कुल राशि है"  उच्चतम मूल्य वाली लागू दृष्टि समस्याओं में से एक है।

> ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒    ⇒ ⇒     ⇒      ⇒                                                                                          

क्षेत्र तीन कौशल परतों में विभाजित हैः

> इस क्षेत्र में तीन कौशल स्तरों में विभाजित हैः

1. **OCR proper**: पिक्सेल को पाठ में बदल दें।
2. **Layout parsing**: समूह ओसीआर आउटपुट क्षेत्रों (शीर्षक, शरीर, तालिका, हेडर) में।
3. **Document understanding**: लेआउट से संरचित फ़ील्ड ("इंवॉइस_टोटल = $42.50") निकालें।

प्रत्येक परत में शास्त्रीय और आधुनिक दृष्टिकोण होते हैं, और "मुझे एक छवि से पाठ चाहिए" और "मुझे इस रसीद से कुल राशि चाहिए" के बीच का अंतर अधिकांश टीमों की कल्पना से बड़ा है।

> प्रत्येक स्तर में क्लासिक और आधुनिक तरीके हैं, "मैं चित्र से शब्द प्राप्त करना चाहता हूँ" और "मुझे इस राशि की कुल राशि की आवश्यकता है" के बीच का अंतर अधिकांश टीमों की समझ से बड़ा है।

## अवधारणा का मूल अवधारणा

> **【中文解读】**इस भाग में मूल अवधारणाओं और सिद्धांतों की आधारभूत जानकारी दी गई है। इन अवधारणाओं को प्राप्त करना बाद में होने वाली प्रक्रियाओं के लिए एक शर्त है।


### शास्त्रीय पाइपलाइन

```mermaid
flowchart LR
    IMG["Image"] --> DET["Text detection<br/>(DB, EAST, CRAFT)"]
    DET --> BOX["Word/line<br/>bounding boxes"]
    BOX --> CROP["Crop each region"]
    CROP --> REC["Recognition<br/>(CRNN + CTC)"]
    REC --> TXT["Text strings"]
    TXT --> LAY["Layout<br/>ordering"]
    LAY --> OUT["Reading-order text"]

    style DET fill:#dbeafe,stroke:#2563eb
    style REC fill:#fef3c7,stroke:#d97706
    style OUT fill:#dcfce7,stroke:#16a34a
```

- **Text detection**प्रति पंक्ति या प्रति शब्द चतुर्भुज उत्पन्न करता है।
  中文翻译:**文本检测**प्रत्येक पंक्ति या प्रत्येक शब्द के चारो ओर के आकार के चौकोर
- **Recognition**प्रत्येक क्षेत्र को एक निश्चित ऊंचाई पर काटता है, एक चरित्र अनुक्रम उत्पन्न करने के लिए एक सीएनएन + BiLSTM + सीटीसी चलाता है।
  中文翻译:**识别**प्रत्येक क्षेत्र को तय ऊंचाई पर काटें, CNN + BiLSTM + CTC का संचालन करें
- **Layout**पढ़ने के क्रम को पुनर्निर्माण करता है (लैटिन के लिए शीर्ष से नीचे, बाएं से दाएं; अरबी, जापानी के लिए अलग) ।
  中文翻译:**布局**重建阅读顺序(拉丁文从上到下、从左到右;阿拉伯文和日文不同)

### एक पैराग्राफ में सीटीसी

OCR मान्यता एक निश्चित लंबाई के फीचर मानचित्र से एक चर-लंबाई अनुक्रम का उत्पादन करती है। CTC (Graves et al., 2006) आपको वर्ण-स्तर संरेखण के बिना इसे प्रशिक्षित करने देता है। मॉडल प्रत्येक समय चरण पर एक वितरण (शब्द + खाली) आउटपुट करता है; CTC हानि सभी संरेखणों पर हाशिए पर छोड़ता है जो पुनरावृत्ति और रिक्त स्थानों को हटाने के बाद लक्षित पाठ में कम हो जाते हैं।

> OCR  पहचान स्थिर लंबाई के लक्षण चित्र से परिवर्तनीय लंबाई अनुक्रम उत्पन्न करना──CTC(Graves आदि,2006) 让你无需字符级对齐就能训练──模型在每时间步输出(词表 +空白) पर वितरण;CTC 损失对所有合并重复和移除空白后归约为目标文本对齐方式进行边缘化──

```
raw output: "h h h _ _ e e l l _ l l o _ _"
after merge repeats and remove blanks: "hello"
```

सीटीसी इस कारण है कि सीआरएनएन ने 2015 में काम किया और अभी भी 2026 में अधिकांश उत्पादन ओसीआर मॉडल को प्रशिक्षित करता है।

> सीटीसी सीआरएनएन 2015 में प्रभावी है और 2026 में अभी भी प्रशिक्षण के अधिकांश उत्पादन OCR  मॉडल के कारणों से है।

### आधुनिक अंत-से-अंत मॉडल

- **Donut**(किम और अन्य, 2022)  एक ViT एन्कोडर + एक पाठ डिकोडर; एक छवि पढ़ता है और सीधे JSON उत्सर्जित करता है। कोई पाठ डिटेक्टर, कोई लेआउट मॉड्यूल नहीं।
  中文翻译:**Donut**(Kim 等,2022) ViT 编码器 + 文本解码器;读取图像直接输出 JSON──无需文本检测器或布局模块──
- **TrOCR** लाइन स्तर के ओसीआर के लिए वीटी + ट्रांसफार्मर डिकोडर।
  中文翻译:**TrOCR**ViT + ट्रांसफार्मर 解码器, उपयोग में आता है
- **Qwen-VL-OCR / InternVL** पूर्ण दृष्टि-भाषा मॉडल ओसीआर कार्यों के लिए ठीक से समायोजित; जटिल दस्तावेजों पर 2026 में सर्वोत्तम सटीकता।
  中文翻译:**Qwen-VL-OCR / InternVL** OCR 任务微调的完整视觉语言模型;2026 साल में जटिल दस्तावेजों पर उच्चतम सटीकता
- **PaddleOCR** परिपक्व उत्पादन पैकेज में क्लासिक डीबी + सीआरएनएन पाइपलाइन; अभी भी ओपन सोर्स वर्कहॉर्स।
  中文翻译:**PaddleOCR** परिपक्व उत्पादन के लिए क्लासिक DB + CRNN 流水线; अभी भी खुला स्रोत मुख्य शक्ति है。

अंत-से-अंत मॉडल को अधिक डेटा और गणना की आवश्यकता होती है लेकिन बहु-चरण पाइपलाइनों के त्रुटि संचय को छोड़ दें।

> 端到端模型 को अधिक डेटा और गणना की आवश्यकता होती है, लेकिन कई चरणों के प्रवाह लाइन के त्रुटि संचय से अधिक कूद जाता है।

### लेआउट पार्सिंग

संरचित दस्तावेजों के लिए, एक लेआउट डिटेक्टर (लेआउटLMv3, डॉकलेनेट) चलाएं जो प्रत्येक क्षेत्र को लेबल करता हैः शीर्षक, पैराग्राफ, आकृति, तालिका, फुटनोट। पढ़ने का क्रम फिर "लेआउट क्रम में क्षेत्रों के माध्यम से दोहराया जाता है, संगत" हो जाता है।

> 对于结构化文档,运行布局检测器(LayoutLMv3、DocLayNet) प्रत्येक क्षेत्र को चिह्नित करेंः शीर्षक,段落,图,表,脚注――阅读顺序变成"布局顺序遍历区域,拼接"――

प्रपत्रों के लिए प्रयोग करें **Key-Value extraction**मॉडल (दृश्य-समृद्ध दस्तावेजों के लिए डोनेट, सादे स्कैन के लिए लेआउटLMv3) । वे छवि + पता लगाया पाठ + स्थान लेते हैं और संरचित कुंजी-मूल्य जोड़े की भविष्यवाणी करते हैं।

> 对于表单,使用**键值提取**模型(视觉丰富文档用唐nut,普通扫描用 LayoutLMv3)──它们接收图像 + 检测到的文本 + 位置,预测结构化的键值对──

### मूल्यांकन मेट्रिक्स

- **Character Error Rate (CER)** लेवेंसस्टीन दूरी / संदर्भ लंबाई। निचला बेहतर है। उत्पादन लक्ष्यः < 2% स्वच्छ स्कैन पर।
  中文翻译:**字符错误率（CER）** 编辑距离 / 参考文本长度──越低越好──生产目标:清晰扫描上 < 2%──
- **Word Error Rate (WER)** शब्द स्तर पर भी यही।
  中文翻译:**词错误率（WER）**词级别的同样标标――
- **F1 on structured fields** प्रमुख मूल्य के कार्यों के लिए; यह मापें कि क्या `{invoice_total: 42.50}`सही दिखाई देता है।
  中文翻译:**结构化字段 F1**किट वैल्यू टास्क के सूचक; माप `{invoice_total: 42.50}`                                                                                                                                                                                                                                                              
- **Edit distance on JSON** अंत से अंत तक दस्तावेज़ विश्लेषण के लिए; डोनट पेपर ने रूख संपादन दूरी को सामान्य बनाया।
  中文翻译:**JSON 编辑距离**端到端文档解析的指标;Donut 论文引入归一化树编辑距离──

> **【中文解读】**इस भाग के माध्यम से कोड को शून्य से लागू किया जा सकता है कोर एल्गोरिदम। इस तरह के "शुरुआत से" तरीके से फ्रेमवर्क के पीछे के सिद्धांत को समझने में मदद मिलेगी, समस्याओं का सामना करते समय ब्लैक बॉक्स में फंस नहीं जाएगा।

> **【拓展：工业部署中的视觉系统】**वास्तविक औद्योगिक तैनाती में, विज़ुअल मॉडल को देरी, मॉडल आकार, किनारे उपकरण अनुकूलन आदि की समस्या पर विचार करने की आवश्यकता होती है। टेन्सरआरटी, ओएनएनएक्स रनटाइम, ओपनवीनो एक सामान्य उपयोग में आने वाला सुझाव त्वरण उपकरण है।

> **【拓展：数据标注与质量】**视觉任务的效果高度依赖标签数据质量──标签工作室、CVAT是主流标签工具──在工业场景中,主动学习(Active Learning) ले标签成本 को कम कर सकता हैः मॉडल अनिश्चित नमूना अनुरोधों के लिए कृत्रिम标签, अनिश्चितता के नमूने स्वचालित标签──




## इसे बनाओ, इसे पूरा करो।
```figure
cv3-ctc-collapse
```

## इसे बनाओ

### चरण 1: सीटीसी हानि + लोभी डिकोडर

```python
import torch
import torch.nn as nn
import torch.nn.functional as F


def ctc_loss(log_probs, targets, input_lengths, target_lengths, blank=0):
    """
    log_probs:      (T, N, C) log-softmax over vocab including blank at index 0
    targets:        (N, S) int targets (no blanks)
    input_lengths:  (N,) per-sample time steps used
    target_lengths: (N,) per-sample target length
    """
    return F.ctc_loss(log_probs, targets, input_lengths, target_lengths,
                      blank=blank, reduction="mean", zero_infinity=True)


def greedy_ctc_decode(log_probs, blank=0):
    """
    log_probs: (T, N, C) log-softmax
    returns: list of index sequences (blanks removed, repeats merged)
    """
    preds = log_probs.argmax(dim=-1).transpose(0, 1).cpu().tolist()
    out = []
    for seq in preds:
        decoded = []
        prev = None
        for idx in seq:
            if idx != prev and idx != blank:
                decoded.append(idx)
            prev = idx
        out.append(decoded)
    return out
```

`F.ctc_loss`जब उपलब्ध हो तो कुशल CuDNN कार्यान्वयन का उपयोग करता है। लालची डिकोडर एक बीम खोज से सरल है और आमतौर पर 1% सीईआर के भीतर है।

> `F.ctc_loss`उपयोग के समय उच्च कुशल CuDNN 实现 करते हैं।

### चरण 2: छोटा सीआरएनएन पहचानकर्ता

लाइन ओसीआर के लिए न्यूनतम सीएनएन + बीएलएसटीएम।

> ओसीआर के न्यूनतम सीएनएन + बीएलएसTM के लिए उपयोग किया जाता है।

```python
class TinyCRNN(nn.Module):
    def __init__(self, vocab_size=40, hidden=128, feat=32):
        super().__init__()
        self.cnn = nn.Sequential(
            nn.Conv2d(1, feat, 3, 1, 1), nn.BatchNorm2d(feat), nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(feat, feat * 2, 3, 1, 1), nn.BatchNorm2d(feat * 2), nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            nn.Conv2d(feat * 2, feat * 4, 3, 1, 1), nn.BatchNorm2d(feat * 4), nn.ReLU(inplace=True),
            nn.MaxPool2d((2, 1)),
            nn.Conv2d(feat * 4, feat * 4, 3, 1, 1), nn.BatchNorm2d(feat * 4), nn.ReLU(inplace=True),
            nn.MaxPool2d((2, 1)),
        )
        self.rnn = nn.LSTM(feat * 4, hidden, bidirectional=True, batch_first=True)
        self.head = nn.Linear(hidden * 2, vocab_size)

    def forward(self, x):
        # x: (N, 1, H, W)
        f = self.cnn(x)                # (N, C, H', W')
        f = f.mean(dim=2).transpose(1, 2)  # (N, W', C)
        h, _ = self.rnn(f)
        return F.log_softmax(self.head(h).transpose(0, 1), dim=-1)  # (W', N, vocab)
```

निश्चित ऊंचाई इनपुट (सीएनएन अधिकतम पूल ऊंचाई को 1 तक) चौड़ाई सीटीसी के लिए समय आयाम है।

> 固定高度输入(CNN 高度 अधिकतम इंकृत होगा 1)── चौड़ाई  CTC का समय आयाम──

### चरण 3: सिंथेटिक ओसीआर

अंत-से-अंत धुएं परीक्षण के लिए काले-से-सफेद अंक स्ट्रिंग उत्पन्न करें।

> 生成白底黑字符串, प्रयोग करने के लिए अंत तक धूम्रपान परीक्षण

```python
import numpy as np

def synthetic_line(text, height=32, char_width=16):
    W = char_width * len(text)
    img = np.ones((height, W), dtype=np.float32)
    for i, c in enumerate(text):
        x = i * char_width
        shade = 0.0 if c.isalnum() else 0.5
        img[6:height - 6, x + 2:x + char_width - 2] = shade
    return img


def build_batch(strings, vocab):
    H = 32
    W = 16 * max(len(s) for s in strings)
    imgs = np.ones((len(strings), 1, H, W), dtype=np.float32)
    target_lengths = []
    targets = []
    for i, s in enumerate(strings):
        imgs[i, 0, :, :16 * len(s)] = synthetic_line(s)
        ids = [vocab.index(c) for c in s]
        targets.extend(ids)
        target_lengths.append(len(ids))
    return torch.from_numpy(imgs), torch.tensor(targets), torch.tensor(target_lengths)


vocab = ["_"] + list("0123456789abcdefghijklmnopqrstuvwxyz")
imgs, targets, lengths = build_batch(["hello", "world"], vocab)
print(f"images: {imgs.shape}   targets: {targets.shape}   lengths: {lengths.tolist()}")
```

एक वास्तविक ओसीआर डेटासेट फ़ॉन्ट, शोर, घूर्णन, धुंधलापन और रंग जोड़ता है। ऊपर पाइपलाइन समान है।

> वास्तविक ओसीआर डेटा सभा में अक्षर, शोर, घूर्णन, अदृश्यता और रंगों में वृद्धि हो रही है।

### चरण 4: प्रशिक्षण स्केच

```python
model = TinyCRNN(vocab_size=len(vocab))
opt = torch.optim.Adam(model.parameters(), lr=1e-3)

for step in range(200):
    strings = ["abc" + str(step % 10)] * 4 + ["xyz" + str((step + 1) % 10)] * 4
    imgs, targets, target_lens = build_batch(strings, vocab)
    log_probs = model(imgs)  # (W', 8, vocab)
    input_lens = torch.full((8,), log_probs.size(0), dtype=torch.long)
    loss = ctc_loss(log_probs, targets, input_lens, target_lens, blank=0)
    opt.zero_grad(); loss.backward(); opt.step()
```

> **【中文解读】**इस भाग में दिखाया गया है कि इस तकनीक को कैसे तेजी से लागू किया जाए। इस प्रकार के एक परिपक्व ढांचे का उपयोग करके बग कम किए जा सकते हैं और विकास दक्षता में सुधार किया जा सकता है।


इस क्षुल्लक सिंथेटिक डेटा पर 200 चरणों पर नुकसान ~ 3 से ~ 0.2 तक गिरना चाहिए।

> इस सरल संश्लेषण डेटा में, 200 चरणों में नुकसान लगभग 3 से घटकर लगभग 0.2 हो सकता है।




> **【拓展：视觉模型的持续学习】**उत्पादन वातावरण में, दृश्य मॉडल को नए डेटा को लगातार अनुकूलित करने की आवश्यकता होती है। यह ऑटोमोटिव ड्राइविंग और औद्योगिक गुणवत्ता जांच में विशेष रूप से महत्वपूर्ण है।

## इसे फ्रेमवर्क के साथ लागू करें

तीन उत्पादन मार्गः

- **PaddleOCR** परिपक्व, तेज, बहुभाषी। एक पंक्ति का उपयोगः `paddleocr.PaddleOCR(lang="en").ocr(image_path)`. .
- **EasyOCR** पायथन-नेटिव, बहुभाषी, पायटॉर्च रीढ़ की हड्डी।
- **Tesseract** शास्त्रीय; अभी भी पुराने स्कैन किए गए दस्तावेजों के लिए उपयोगी है जब मॉडल संघर्ष करते हैं।

अंत-से-अंत दस्तावेज़ विश्लेषण के लिए, डोनट या वीएलएम का उपयोग करेंः

```python
from transformers import DonutProcessor, VisionEncoderDecoderModel

processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base-finetuned-cord-v2")
```

> **【中文解读】**इस खंड में इस बात पर ध्यान दिया गया है कि मॉडल को उपलब्ध उत्पादों के रूप में कैसे तैनात किया जाए। मूल से लेकर उत्पादन स्तर तक, प्रदर्शन अनुकूलन, त्रुटि प्रसंस्करण, निगरानी आदि के कई आयामों पर विचार करने की आवश्यकता है।


रिसीव, चालान और दोहराए जाने योग्य संरचना वाले फॉर्म के लिए, डोनट को ठीक से ट्यून करें। मनमाने दस्तावेजों या तर्क के साथ ओसीआर के लिए, क्यूवेन-वीएल-ओसीआर जैसे वीएलएम वर्तमान डिफ़ॉल्ट है।



## इसे भेजें उत्पाद

> **【中文解读】**练习题按照易/中级/难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;


इस पाठ से उत्पन्न होता हैः

- `outputs/prompt-ocr-stack-picker.md` एक संकेत जो टेसरैक्ट / पैडलओसीआर / डोनट / वीएलएम-ओसीआर को दस्तावेज़ प्रकार, भाषा और संरचना के अनुसार चुनता है।
- `outputs/skill-ctc-decoder.md` एक कौशल जो लालची और बीम-सर्च सीटीसी डिकोडर को खरोंच से लिखता है, जिसमें लंबाई सामान्यीकरण भी शामिल है।

## अभ्यास विषय

> **【中文解读】**术语表中的"क्या लोग कहते हैं" बनाम "क्या वास्तव में इसका मतलब है" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


1. **(Easy)**500 चरणों के लिए 5-अंकीय यादृच्छिक संख्यात्मक स्ट्रिंग पर TinyCRNN को प्रशिक्षित करें। एक लंबे समय तक आयोजित सेट पर सीईआर रिपोर्ट करें।
2. **(Medium)**लालची डिकोडिंग को बीम सर्च (beam_width=5) से बदलें। CER डेल्टा रिपोर्ट करें। किस इनपुट पर बीम सर्च जीतता है?
3. **(Hard)**20 रसीदों के सेट पर PaddleOCR का उपयोग करें, लाइन आइटम निकालें, और {item_name, price} जोड़े के लिए हाथ से लेबल किए गए ग्राउंड सत्य के खिलाफ F1 गणना करें।

## कीवर्ड्स  शब्द खोज तालिका

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| OCR | "Text from pixels" | Turning image regions into character sequences |
| CTC | "Alignment-free loss" | Loss that trains a sequence model without per-timestep labels; marginalises over alignments |
| CRNN | "Classic OCR model" | Conv feature extractor + BiLSTM + CTC; the 2015 baseline still used in production |
| Donut | "End-to-end OCR" | ViT encoder + text decoder; emits JSON directly from image |
| Layout parsing | "Find regions" | Detect and label Title/Table/Figure/Paragraph regions in a document |
| Reading order | "Text sequence" | Ordering of recognised regions into a sentence; trivial for Latin, non-trivial for mixed layouts |
| CER / WER | "Error rates" | Levenshtein distance / reference length at character or word granularity |
| VLM-OCR | "LLM that reads" | A vision-language model trained or prompted for OCR tasks; current SOTA on complex documents |

> **【中文解读】**延伸阅读 प्रदान करता है गहन सीखने के लिए उच्च गुणवत्ता वाले संसाधनों। ये लेख और पाठ्यक्रम इस क्षेत्र के लिए क्लासिक संदर्भ हैं, जो गहन समझ की आवश्यकता वाले पाठकों के लिए उपयुक्त हैं।


## आगे पढ़ना 延伸閱讀

- [CRNN (Shi et al., 2015)](https://arxiv.org/abs/1507.05717) मूल सीएनएन+आरएनएन+सीटीसी वास्तुकला
- [CTC (Graves et al., 2006)](https://www.cs.toronto.edu/~graves/icml_2006.pdf) मूल सीटीसी पेपर; एल्गोरिथम विचारों से घने पैक
- [Donut (Kim et al., 2022)](https://arxiv.org/abs/2111.15664) ओसीआर मुक्त दस्तावेज़ समझ ट्रांसफार्मर
- [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) ओपन सोर्स प्रोडक्शन ओसीआर स्टैक
