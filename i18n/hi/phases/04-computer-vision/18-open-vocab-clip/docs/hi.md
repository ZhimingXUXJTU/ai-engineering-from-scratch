# ओपन-वोकैब्युलर विजन  CLIP  开放词汇视觉  CLIP

> एक छवि एन्कोडर और एक पाठ एन्कोडर को एक साथ प्रशिक्षित करें ताकि मिलान (छवि, कैप्शन) जोड़े साझा स्थान में एक ही बिंदु पर लैंड करें। यही पूरी चाल है।

> **【中文解读】**CLIP साथ ही प्रशिक्षण छवि संपादक और पाठ संपादक, जो एक ही बिंदु पर स्थित साझा अंतरिक्ष के लिए उपयुक्त हैं।

> **【拓展：CLIP 是多模态 AI 的基石】**CLIP DALL-E  स्थिर विसारण  ग्रंथ शर्त  LVA  GPT-4V आदि बहुआयामी मॉडल के बुनियादी घटक हैं। इसके विपरीत सीखने के लिए पूर्व प्रशिक्षण प्रारूप व्यापक रूप से अपनाया गया है, जिससे "खुले हुए शब्द"  विजन के नए युग के मॉडल को समझने में सक्षम बनाया गया है।

**Type:** Build + Use | **类型:** 动手 + 应用
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 4 Lesson 14 (ViT), Phase 4 Lesson 17 (Self-Supervised) | **前置知识:** Phase 4 Lesson 14（ViT），Phase 4 Lesson 17（自监督）
**Time:** ~45 minutes | **时间:** ~45 分钟

## सीखने के लक्ष्य

- CLIP के दो टावरों के वास्तुकला और विपरीत प्रशिक्षण के उद्देश्य को समझाएं
- बिना किसी कार्य-विशिष्ट प्रशिक्षण के शून्य शॉट वर्गीकरण के लिए पूर्व-प्रशिक्षित CLIP (या SigLIP) का उपयोग करें
- शून्य शॉट वर्गीकरण को खरोंच से लागू करेंः कोड वर्ग प्रम्प्ट, कॉसिन समानता की गणना करें, argmax लें
- CLIP, SigLIP, OpenCLIP और LLaVA/LLaMA-vision मॉडल में अंतर करें  2026 में प्रत्येक के लिए क्या है

> **【中文解读】**सीखने के लक्ष्य इस कक्षा को पूरा करने के बाद जो मूल क्षमताएं होनी चाहिए, उन्हें सूचीबद्ध करते हैं।


## समस्या  समस्या परिचय

पारंपरिक वर्गीकरण बंद-वाक्य संग्रह हैंः 1000 वर्गों के इमेजनेट मॉडल केवल 1000 लेबल की भविष्यवाणी कर सकते हैं। प्रत्येक नई श्रेणी के लिए लेबल वाले डेटा और एक पुनः प्रशिक्षित सिर की आवश्यकता होती है।

> 传统分类器是封闭词汇的:1000 类的 ImageNet 模型只能预测1000 标签── प्रत्येक नई श्रेणी को डेटा और पुनः प्रशिक्षित शीर्षक के लिए चिह्नित करने की आवश्यकता होती है──

CLIP (Radford et al., OpenAI 2021) ने दिखाया कि वेब से स्क्रैप किए गए 400M (छवि, कैप्शन) जोड़े पर प्रशिक्षण एक मॉडल का उत्पादन करता है जो निष्कर्ष पर किसी भी सेट की श्रेणियों में वर्गीकृत कर सकता है, जिसे शुद्ध रूप से प्राकृतिक भाषा में वर्णित किया गया है। आप इसे एक वाक्य लिखकर एक नया वर्ग देते हैं।

> CLIP(Radford等,OpenAI 2021) से पता चलता है कि 400 मिलियन से अधिक वेब से प्राप्त (चित्र, शीर्षक) मॉडल पर उत्पन्न प्रशिक्षण किसी भी श्रेणी के संग्रह में विचार में विभाजित किया जा सकता है, शुद्ध प्राकृतिक भाषा में वर्णन किया गया है।

यह क्षमता  शून्य-शॉट स्थानांतरण  यह है कि हर आधुनिक दृष्टि प्रणाली एक CLIP-परिवार चेकपॉइंट के साथ क्यों शुरू होती है। पता लगाने (ग्राउंडिंग DINO, OWL-ViT), खंडन (CLIPSeg, SAM), पुनर्प्राप्ति, सामग्री मॉडरेशन, VLMs, और पाठ-से-छवि पीढ़ी सभी CLIP-शैली के संयुक्त एम्बेडमेंट पर आधारित हैं।

> उस क्षमता零样本迁移就是为什么每现代视觉系统都从CLIP家族的检查点开始――检测(Grounding DINO、OWL-ViT) 、 विभाजन(CLIPSeg、SAM) 、检索、内容审核、VLM 和文本到图像生成都建立在CLIP 风格的联合嵌入上──

## अवधारणा का मूल अवधारणा

> **【中文解读】**इस भाग में मूल अवधारणाओं और सिद्धांतों की आधारभूत जानकारी दी गई है। इन अवधारणाओं को प्राप्त करना बाद में होने वाली प्रक्रियाओं के लिए एक शर्त है।


### दो टावर

```mermaid
flowchart LR
    IMG["Image"] --> IENC["Image encoder<br/>(ViT-L/14)"] --> IEMB["Image embedding<br/>(1024,)"]
    TXT["Caption"] --> TENC["Text encoder<br/>(transformer)"] --> TEMB["Text embedding<br/>(1024,)"]
    IEMB --> SIM["Cosine similarity"]
    TEMB --> SIM

    style IENC fill:#dbeafe,stroke:#2563eb
    style TENC fill:#fef3c7,stroke:#d97706
    style SIM fill:#dcfce7,stroke:#16a34a
```

दोनों एन्कोडर एक ही एम्बेडिंग आयाम (512 के लिए CLIP-B/32, 1024 के लिए CLIP-L/14) के लिए एक रैखिक प्रोजेक्शन के साथ समाप्त होते हैं। L2-सामान्य और गणना कॉसिन समानता।

>  दो एडिटर                                                                                                                                                                                                                                                            

### उद्देश्य

N (छवि, कैप्शन) जोड़े के एक बैच को देखते हुए, एक NxN समानता मैट्रिक्स बनाएं। दोनों एन्कोडर को प्रशिक्षित करें ताकि विकर्ण (मिलते हुए जोड़े) में उच्च समानता हो और विकर्ण (गैर-मिलते) में कम समानता हो।

> 给定一批 N 个 (图像,标题) 对,构建 NxN相似度矩阵――训练两个编码器使对角线 (编码器) 匹配对) 相似度高,非对角线 (非对角线) 匹配对) 相似度低――

```
sim_matrix = image_embeddings @ text_embeddings.T / tau

loss_i2t = cross_entropy(sim_matrix,       targets=arange(N))
loss_t2i = cross_entropy(sim_matrix.T,     targets=arange(N))
loss = (loss_i2t + loss_t2i) / 2
```

सममित क्योंकि छवि-से-पाठ और पाठ-से-चित्र दोनों को काम करना चाहिए। `tau`(तापमान) आमतौर पर एक स्केलर पैरामीटर के रूप में सीखा जाता है, 0.07 पर शुरू किया जाता है।

> इसको इसलिए कहा जाता है क्योंकि छवि से पाठ और पाठ से छवि की जांच दोनों प्रभावी होनी चाहिए।`tau`(तापमान) सामान्यतः 0.07 के रूप में प्रारम्भिक है।

### सिगलिप: बेहतर हानि

सिगलिप (झाय एट अल., 2023) ने सॉफ्टमैक्स को प्रति जोड़ी सिग्मोइड से बदल दियाः

> सिग्लिप ((ज़ै आदि,2023) से सिग्मोइड के प्रतिस्थापन के लिए सॉफ्टमैक्सः

```
loss = mean over pairs of log(1 + exp(-y_ij * sim_ij))
y_ij = +1 if matching, -1 otherwise
```

प्रति जोड़ी हानि CLIP द्वारा आवश्यक बैच स्तर के सामान्यीकरण को समाप्त करती है। SigLIP छोटे बैच आकार पर बेहतर ट्रेन करता है और समान डेटा पर CLIP से मेल खाता है या उससे अधिक होता है।

>  प्रति हानि CLIP की आवश्यकता वाले बैच ग्रेड को एकीकरण को समाप्त कर दिया गया है

### शून्य शॉट वर्गीकरण

एक प्रशिक्षित CLIP के कारणः

> 给定训练好的 CLIP:

1. प्रत्येक वर्ग के लिए, एक प्रॉम्प्ट लिखेंः "एक {class} की तस्वीर"।
   中文翻译:为每个类别构造提示词:"एक {类别} की एक तस्वीर"。
2. पाठ एन्कोडर के साथ सभी वर्ग प्रमाणीकरण एन्कोड -> `T`आकार (सी, डी)
   中文翻译:用文本编码器编码所有类提示词 -> `T`形状 (C, d)
3. परीक्षण छवि को एन्कोड करें -> `I`आकार (1, डी)
   中文翻译:编码测试图像 -> `I`形状 (1, डी)
4. समानता = `I @ T.T`आकार (1, C)
   中文翻译:相似度 = `I @ T.T`形状 (1, C) ⋅
5. Argmax -> पूर्वानुमानित वर्ग।
   中文翻译:Argmax -> 预测类别。

त्वरित इंजीनियरिंग के मामले। ओपनएआई ने इमेजनेट के लिए 80 शीघ्र टेम्पलेट प्रकाशित किए ("एक {} की तस्वीर", "एक {} की एक धुंधली तस्वीर", "एक {} का एक स्केच", ...) । एक अतिरिक्त 1-3% शीर्ष-1 सटीकता के लिए प्रति वर्ग के सभी टेम्पलेट्स के एम्बेडमेंट का औसत करें।

> 提示词工程 बहुत महत्वपूर्ण है। ImageNet के लिए OpenAI ने 80 提示模板 जारी किए हैं। प्रत्येक श्रेणी के सभी मॉडलों में एम्बेड होने पर औसतन अतिरिक्त वृद्धि 1-3% की शीर्ष-1 准确率 प्राप्त होगी।

### जहां 2026 में CLIP शैली के मॉडल का उपयोग किया जाता है

- **Zero-shot classification** प्रत्यक्ष उपयोग।
  中文翻译:**零样本分类**直接使用──
- **Image retrieval** सभी छवियों को एक बार एन्कोड करें, निष्कर्ष पर क्वेरी एम्बेड करें।
  中文翻译:**图像检索** एक बार में सभी छवियों को कोडित करें, विचार करें
- **Text-conditioned detection** DINO को जमीन पर लटकाकर, OWL-ViT ने एक डिटेक्टर के चारों ओर एक CLIP पाठ टॉवर को लपेटा।
  中文翻译:**文本条件检测**Grounding DINO、OWL-ViT 在检测器外包装 CLIP 文本塔──
- **Text-conditioned segmentation** CLIPSeg; SAM CLIP के माध्यम से पाठ-प्रोम्प्ट इनपुट का उपयोग करता है।
  中文翻译:**文本条件分割**CLIPSeg;SAM 通过 CLIP 使用文本提示输入──
- **VLMs** LLaVA, Qwen-VL, InternVL एक CLIP-परिवार दृष्टि एन्कोडर LLM में तार।
  中文翻译:**VLM**LLaVA、Qwen-VL、InternVL CLIP परिवार के विडियो कोडर LLM में संलग्न होगा
- **Text-to-image gen** CLIP पाठ एम्बेडमेंट पर स्थिर विसारण, DALL-E 3 स्थिति।
  中文翻译:**文本到图像生成**स्थिर विसारण、DALL-E 3  CLIP आधारित 文本嵌入进行条件化──

एक बार जब आपके पास एक साझा एम्बेडिंग स्पेस हो जाता है, तो प्रत्येक दृष्टि + भाषा कार्य दूरी गणना बन जाता है।

> एक बार जब साझा स्थान में सम्मिलित होता है, तो प्रत्येक विजन+ भाषा कार्य दूरी गणना में बदल जाता है।

> **【中文解读】**इस भाग के माध्यम से कोड को शून्य से लागू किया जा सकता है कोर एल्गोरिदम। इस तरह के "शुरुआत से" तरीके से फ्रेमवर्क के पीछे के सिद्धांत को समझने में मदद मिलेगी, समस्याओं का सामना करते समय ब्लैक बॉक्स में फंस नहीं जाएगा।

> **【拓展：工业部署中的视觉系统】**वास्तविक औद्योगिक तैनाती में, विज़ुअल मॉडल को देरी, मॉडल आकार, किनारे उपकरण अनुकूलन आदि की समस्या पर विचार करने की आवश्यकता होती है। टेन्सरआरटी, ओएनएनएक्स रनटाइम, ओपनवीनो एक सामान्य उपयोग में आने वाला सुझाव त्वरण उपकरण है।

> **【拓展：数据标注与质量】**视觉任务的效果高度依赖标签数据质量──标签工作室、CVAT是主流标签工具──在工业场景中,主动学习(Active Learning) ले标签成本 को कम कर सकता हैः मॉडल अनिश्चित नमूना अनुरोधों के लिए कृत्रिम标签, अनिश्चितता के नमूने स्वचालित标签──




## इसे बनाओ, इसे पूरा करो।
```figure
clip-contrastive
```

## इसे बनाओ

### चरण 1: दो टावरों का छोटा मॉडल

वास्तविक CLIP ViT + ट्रांसफार्मर है। इस पाठ के लिए टावर पूर्व-उत्कर्षण सुविधाओं पर छोटे MLP हैं ताकि प्रशिक्षण संकेत सीपीयू पर दिखाई दे।

> वास्तविक CLIP ViT + Transformer है। इस कोर्स में छोटे MLP को प्री-डिटेक्शन फीचर पर रखा गया है ताकि सीपीयू पर प्रशिक्षण सिग्नल दिखाई दे सके।

```python
import torch
import torch.nn as nn
import torch.nn.functional as F


class TwoTower(nn.Module):
    def __init__(self, img_in=128, txt_in=64, emb=64):
        super().__init__()
        self.image_proj = nn.Sequential(nn.Linear(img_in, 128), nn.ReLU(), nn.Linear(128, emb))
        self.text_proj = nn.Sequential(nn.Linear(txt_in, 128), nn.ReLU(), nn.Linear(128, emb))
        self.logit_scale = nn.Parameter(torch.ones([]) * 2.6592)  # ln(1/0.07)

    def forward(self, img_feats, txt_feats):
        i = F.normalize(self.image_proj(img_feats), dim=-1)
        t = F.normalize(self.text_proj(txt_feats), dim=-1)
        return i, t, self.logit_scale.exp()
```

दो अनुमान, साझा-डिम आउटपुट, सीखा तापमान. असली CLIP एपीआई के रूप में एक ही आकार.

> दो प्रोजेक्शन ¦साझा आयाम आउटपुट ¦पढ़ने योग्य तापमान ∼ वास्तविक CLIP API  के समान आकार 

### चरण 2: विपरीत हानि

```python
def clip_loss(image_emb, text_emb, logit_scale):
    N = image_emb.size(0)
    sim = logit_scale * image_emb @ text_emb.T
    targets = torch.arange(N, device=sim.device)
    l_i = F.cross_entropy(sim, targets)
    l_t = F.cross_entropy(sim.T, targets)
    return (l_i + l_t) / 2
```

सममित। उच्च लॉजिट_स्केल = तेज सॉफ्टमैक्स = अधिक आत्मविश्वास लेकिन अस्थिरता का खतरा।

> ◊称的──更高的逻辑_尺度 = अधिक尖的软max = अधिक आत्मविश्वास लेकिन अनिश्चित风险──

### चरण 3: शून्य-शॉट वर्गीकरण

```python
@torch.no_grad()
def zero_shot_classify(model, image_feats, class_text_feats, class_names):
    """
    image_feats:      (N, img_in)
    class_text_feats: (C, txt_in)   one averaged embedding per class
    """
    i = F.normalize(model.image_proj(image_feats), dim=-1)
    t = F.normalize(model.text_proj(class_text_feats), dim=-1)
    sim = i @ t.T
    pred = sim.argmax(dim=-1)
    return [class_names[p] for p in pred.tolist()]
```

यह एक उत्पादन CLIP चेकपॉइंट के साथ उपयोग की जाने वाली सटीक शून्य शॉट प्रक्रिया है।

> प्रत्येक चरण में। यह उत्पादन स्तर क्लिप  जाँच बिंदु उपयोग की सटीक शून्य नमूना प्रक्रिया है।

### चरण 4: मानसिक स्वास्थ्य जांच

```python
torch.manual_seed(0)
model = TwoTower()

img = torch.randn(8, 128)
txt = torch.randn(8, 64)
i, t, scale = model(img, txt)
loss = clip_loss(i, t, scale)
print(f"batch size: {i.size(0)}   loss: {loss.item():.3f}")
```

हानि करीब होनी चाहिए`log(N) = log(8) = 2.08`एक यादृच्छिक रूप से शुरू मॉडल के लिए  सममित क्रॉस-एंट्रोपी लक्ष्य जब कोई संरचना अभी तक नहीं सीखा गया है।

>  जब प्रारम्भिक मॉडल का नुकसान निकट होना चाहिए `log(N) = log(8) = 2.08`अभी तक नहीं सीखा है संरचना के लिए  लक्ष्य

> **【中文解读】**इस भाग में दिखाया गया है कि इस तकनीक को कैसे तेजी से लागू किया जाए। इस प्रकार के एक परिपक्व ढांचे का उपयोग करके बग कम किए जा सकते हैं और विकास दक्षता में सुधार किया जा सकता है।





> **【拓展：视觉模型的持续学习】**उत्पादन वातावरण में, दृश्य मॉडल को नए डेटा को लगातार अनुकूलित करने की आवश्यकता होती है। यह ऑटोमोटिव ड्राइविंग और औद्योगिक गुणवत्ता जांच में विशेष रूप से महत्वपूर्ण है।

## इसे फ्रेमवर्क के साथ लागू करें

2026 में OpenCLIP समुदाय डिफ़ॉल्ट हैः

```python
import open_clip
import torch
from PIL import Image

model, _, preprocess = open_clip.create_model_and_transforms("ViT-B-32", pretrained="laion2b_s34b_b79k")
tokenizer = open_clip.get_tokenizer("ViT-B-32")

image = preprocess(Image.open("dog.jpg")).unsqueeze(0)
text = tokenizer(["a photo of a dog", "a photo of a cat", "a photo of a car"])

with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text)
    image_features = image_features / image_features.norm(dim=-1, keepdim=True)
    text_features = text_features / text_features.norm(dim=-1, keepdim=True)
    probs = (100.0 * image_features @ text_features.T).softmax(dim=-1)

> **【中文解读】** 本节关注如何将模型部署为可用的产品。从原型到生产级系统需要考虑性能优化、错误处理、监控等多个维度。


print(probs)
```

सिगलिप नया है, छोटे पैमाने पर बेहतर प्रशिक्षण देता है, और नए काम के लिए पसंद किया जाता हैः `google/siglip-base-patch16-224`. दोनों जहाजों को गले लगा रहा है.



## इसे भेजें उत्पाद

> **【中文解读】**练习题按照易/中级/难度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;


इस पाठ से उत्पन्न होता हैः

- `outputs/prompt-zero-shot-class-picker.md` एक प्रोंपट जो वर्गों की सूची और एक डोमेन दिए गए शून्य-शॉट CLIP के लिए वर्ग टेम्पलेट्स डिजाइन करता है।
- `outputs/skill-image-text-retriever.md` एक कौशल जो किसी भी CLIP चेकपॉइंट के साथ एक छवि एम्बेडिंग सूचकांक बनाता है, पाठ-दर-पाठ और छवि-दर-छवि क्वेरी का समर्थन करता है।

## अभ्यास विषय

1. **(Easy)**पूर्व प्रशिक्षित ओपनक्लिप ViT-B/32 का उपयोग करें और 80 टेम्पलेट प्रॉम्प्ट सेट के साथ CIFAR-10 पर शून्य शॉट वर्गीकरण करें। शीर्ष-1 सटीकता रिपोर्ट करें; यह लगभग 85-90% होना चाहिए।
2. **(Medium)**एक ही CIFAR-10 कार्य पर एकल टेम्पलेट ("एक {} की तस्वीर") बनाम 80-टेम्पलेट औसत एम्बेडमेंट की तुलना करें। अंतर को मात्रा दें और समझाएं कि टेम्पलेट्स क्यों मदद करते हैं।
3. **(Hard)**शून्य-शॉट छवि पुनर्प्राप्ति सूचकांक बनाएंः CLIP के साथ 1,000 छवियों को एम्बेड करें, FAISS सूचकांक बनाएं, प्राकृतिक भाषा विवरण के साथ क्वेरी करें। हाथ से लिखे गए 20 रखे गए क्वेरी के लिए रिकवरी रिकॉल@5 रिपोर्ट करें।

> **【中文解读】**术语表中的"क्या लोग कहते हैं" बनाम "क्या वास्तव में इसका मतलब है" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──


## कीवर्ड्स  शब्द खोज तालिका

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Two-tower | "Dual encoder" | Separate image and text encoders ending in a shared-dim projection head |
| Zero-shot | "No task-specific training" | Classify into classes described only by text at inference; no labels touched |
| Temperature / logit_scale | "tau" | Learned scalar that scales the similarity matrix before softmax |
| Prompt template | "A photo of a {}" | Natural-language wrapper around class names; averaging many templates boosts zero-shot accuracy |
| CLIP | "Image+text model" | The 2021 OpenAI model; vocabulary of the field in 2026 |
| SigLIP | "Sigmoid CLIP" | Swaps softmax for per-pair sigmoid; trains better at small batches |
| OpenCLIP | "Open reproduction" | Community-trained CLIP variants on LAION; production default for open-source pipelines |
| VLM | "Vision-language model" | A CLIP-family encoder plus an LLM, trained to answer questions about images |

> **【中文解读】**延伸阅读 प्रदान करता है गहन सीखने के लिए उच्च गुणवत्ता वाले संसाधनों। ये लेख और पाठ्यक्रम इस क्षेत्र के लिए क्लासिक संदर्भ हैं, जो गहन समझ की आवश्यकता वाले पाठकों के लिए उपयुक्त हैं।


## आगे पढ़ना 延伸閱讀

- [CLIP: Learning Transferable Visual Models from Natural Language Supervision (Radford et al., 2021)](https://arxiv.org/abs/2103.00020)
- [SigLIP: Sigmoid Loss for Language-Image Pre-Training (Zhai et al., 2023)](https://arxiv.org/abs/2303.15343)
- [OpenCLIP](https://github.com/mlfoundations/open_clip) सामुदायिक कोडबेस
- [DINOv2 vs CLIP vs MAE: a features comparison](https://huggingface.co/blog/dinov2) HF गाइड साथ-साथ उपयोग के मामले
