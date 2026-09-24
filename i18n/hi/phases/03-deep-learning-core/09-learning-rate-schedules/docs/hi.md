# सीखने की दर तालिका और वार्मअप

> सीखने की दर सबसे महत्वपूर्ण हाइपरपैरामीटर है. वास्तुकला नहीं. डेटा सेट का आकार नहीं. सक्रियण फ़ंक्शन नहीं. सीखने की दर. यदि आप कुछ और नहीं ट्यून करते हैं, तो इसे ट्यून करें.

> **【中文解读】**सीखने की दर सबसे महत्वपूर्ण सुपरपरमांक है  संरचना नहीं, डेटा मात्रा नहीं, सीखने की दर है  लामा 3 का उपयोग शिखर मूल्य lr=3e-4 + 2000 步 वार्मिंग + कॉसिन गिरावट  जीपीटी-3 का उपयोग lr=6e-4 + वार्मिंग  समझ सीखने की दर अनुक्रमण किसी भी मॉडल का प्रशिक्षण करने की कुंजी है

**Type:** Build
**Languages:** Python
**Prerequisites:** Lesson 03.06 (Optimizers), Lesson 03.08 (Weight Initialization)
**Time:** ~90 minutes

## सीखने के लक्ष्य

- निरंतर, चरण क्षय, कोसिन एनेलिंग, वार्मिंग + कोसिन, और 1 चक्र सीखने की दर के कार्यक्रमों को खरोंच से लागू करें
- सीखने की दर के चयन के तीन विफलता मोड प्रदर्शित करेंः विचलन (बहुत अधिक), स्थगित (बहुत कम) और घर्षण (कोई गिरावट नहीं)
- बताएँ कि आदम आधारित अनुकूलनकर्ताओं के लिए वार्मिंग क्यों आवश्यक है और यह प्रारंभिक प्रशिक्षण को कैसे स्थिर करता है
- एक ही कार्य पर सभी पांच कार्यक्रमों में अभिसरण गति की तुलना करें और एक दिए गए प्रशिक्षण बजट के लिए उपयुक्त एक चुनें

> **【中文解读】**इस अध्याय में पांच प्रकार के सीखने की दर का अनुक्रम किया गया है:恒定、阶梯衰减、余弦退火、 वार्मअप+余弦、1 चक्र 策略。 आधुनिक बड़े मॉडल का मानक विन्यास वार्मअप है(前 1-5% 步数线性升温) + कॉस्मीन गिरावट(余弦衰减到接近零)。 समझें वार्मअप क्यों आवश्यक है

## समस्या  समस्या परिचय

प्रशिक्षण की दर को 0.1 पर सेट करें। प्रशिक्षण विचलित होता है - नुकसान 3 चरणों में अनंत तक कूदता है। इसे 0.0001 पर सेट करें। प्रशिक्षण क्रॉल करता है - 100 युगों के बाद, मॉडल को यादृच्छिक से लगभग नहीं हटाया गया है। इसे 0.01 पर सेट करें। प्रशिक्षण 50 युगों के लिए काम करता है, फिर नुकसान न्यूनतम के आसपास टहलता है जो कभी नहीं पहुंच सकता क्योंकि चरण बहुत बड़े हैं।

>  प्रशिक्षण 0.1  प्रशिक्षण प्रसार  नुकसान 3 चरणों में कूदने के लिए अनंत  0.0001  प्रशिक्षण धीमी क्रैकिंग  100  युग  के बाद, मॉडल लगभग किसी भी समय से नहीं चला  0.01  प्रशिक्षण से पहले 50  युग प्रभावी, फिर नुकसान एक कभी नहीं प्राप्त करने योग्य चरम मूल्य के पास झोंका, क्योंकि चरण बहुत बड़ा 

प्रशिक्षण के दौरान सीखने की इष्टतम दर स्थिर नहीं होती है। यह प्रशिक्षण के दौरान बदलती है। शुरुआत में, आप जल्दी से जमीन को कवर करने के लिए बड़े कदम चाहते हैं। प्रशिक्षण के अंत में, आप छोटे कदम चाहते हैं कि एक तेज न्यूनतम में समायोजित हो जाएं। 90% सटीक मॉडल और 95% सटीक मॉडल के बीच अंतर अक्सर केवल कार्यक्रम होता है।

> प्रशिक्षण के दौरान यह बदलता है। प्रारंभिक चरण में, आप बड़े चरणों में तेजी से कवर करने की आवश्यकता होती है। प्रशिक्षण के बाद, आप छोटे चरणों में एक चरम सीमा पर स्थिर होना चाहते हैं।

पिछले तीन वर्षों में प्रकाशित प्रत्येक प्रमुख मॉडल में सीखने की दर का एक कार्यक्रम होता है। Llama 3 ने 2000 वार्मिंग चरणों के साथ पीक lr = 3e-4 और 3e-5 तक कॉसिन गिरावट का उपयोग किया। GPT-3 ने 375 मिलियन टोकन से अधिक वार्मिंग के साथ lr = 6e-4 का उपयोग किया। ये मनमानी विकल्प नहीं हैं। वे व्यापक हाइपरपरमैटर स्वीप का परिणाम हैं जो लाखों डॉलर खर्च करते हैं।

> 过去三年发表的每个主要模型都使用学习率调度──Llama 3 使用峰值 lr=3e-4,2000 步升和余弦衰减到3e-5──GPT-3 使用 lr=6e-4,warmup 覆盖3.75 बिलियन टोकन──ये कोई पसंद नहीं हैं──ये बड़ी संख्या में सुपरपरंपेंट खोज करने के लिए लाखों डॉलर खर्च करते हैं──

आपको शेड्यूल को समझना होगा क्योंकि डिफ़ॉल्ट तरीके से आपके समस्या के लिए काम नहीं करेंगे। जब आप एक पूर्व-प्रशिक्षित मॉडल को ठीक से ट्यून करते हैं, तो सही शेड्यूल खरोंच से प्रशिक्षण से अलग है। जब आप बैच आकार बढ़ाते हैं, तो वार्मिंग अवधि को बदलने की आवश्यकता होती है। जब प्रशिक्षण 10,000 चरण पर टूट जाता है, तो आपको यह जानना होगा कि क्या यह एक शेड्यूल समस्या है या कुछ और।

> आपको अनुसूची योजना को समझने की आवश्यकता है, क्योंकि डिफ़ॉल्ट मान आपकी समस्या के लिए उपयुक्त नहीं है।

> **【中文解读】**सीखने की दर बहुत अधिक → प्रशिक्षण प्रसार(हानि तक अनंत); बहुत कम → प्रशिक्षण बहुत धीमा; उपयुक्त लेकिन घटता नहीं → 振荡 न्यूनतम मूल्य के पास है। प्रत्येक मुख्य मॉडल में सीखने की दर को समायोजित करने के लिए एक सुसंगत योजना है, जो लाखों डॉलर के स्तर पर सुपर पैरामीटर खोज द्वारा पाई जाती है।

> **【拓展：大模型的学习率配置】**Llama 3 405B:पिक lr=3e-4, वार्मअप=2000 步, कॉसिन गिरावट तक 3e-5, 训练 1.8T टोकन。GPT-3 175B:पिक lr=6e-4, वार्मअप=375M टोकन。BERT-base:पिक lr=1e-4, वार्मअप=10K 步, रैखिक गिरावट。规律:模型越大,学习率通常越小;预训练比微调的学习率高 10-100 倍。

## अवधारणा का मूल अवधारणा

### निरंतर सीखने की दर

सबसे सरल तरीका है, एक संख्या चुनें, हर कदम के लिए इसका इस्तेमाल करें।

> सबसे सरल तरीका है-- एक संख्या चुनें, हर कदम पर इसका उपयोग करें।

```
lr(t) = lr_0
```

यह शायद ही कभी इष्टतम है। यह या तो प्रशिक्षण के अंत के लिए बहुत अधिक है (कम से कम के आसपास गतिशीलता) या शुरुआत के लिए बहुत कम है (छोटे चरणों पर बर्बाद गणना) । यह छोटे मॉडल और डिबगिंग के लिए ठीक काम करता है। एक घंटे से अधिक समय तक प्रशिक्षण देने वाले किसी भी चीज़ के लिए एक भयानक विकल्प है।

> 很少是最优的──要么对训练末期来说太高 ((在极小值附近振荡),要么对训练初步来说太低 ((微小步长浪费计算) ⋅适用小模型和调试──对训练超过一小时的任务来说是糟糕的选择──

### कदम गिरावट , कदम गिरावट

ResNet युग से पुराने स्कूल के दृष्टिकोण। निश्चित कालखंडों पर सीखने की दर को एक कारक (आमतौर पर 10 गुना) कम करें।

> ResNet 时代的老派方法── निश्चित काल में सीखने की दर एक कारक को कम करेगा (आमतौर पर 10 गुना)──

```
lr(t) = lr_0 * gamma^(floor(epoch / step_size))
```

जहां गामा = 0.1 और स्टेप_साइज = 30 का मतलब हैः lr हर 30 युगों में 10 गुना गिरता है. ResNet-50 ने इस का उपयोग किया -- lr = 0.1, 30, 60 और 90 युगों में 10 गुना गिरता है।

> gamma = 0.1 且 step_size = 30 अर्थ: प्रत्येक 30 年代 学习率 घटकर 10 गुना──ResNet-50 इस lr=0.1 का प्रयोग किया, 30、60 और 90 काल में 10 गुना घटकर 10 गुना──

समस्याः अनुकूलन गिरावट बिंदु डेटा सेट और वास्तुकला पर निर्भर करता है. एक अलग समस्या पर जाएं और आपको गिरने के समय को फिर से समायोजित करने की आवश्यकता है. संक्रमण अचानक हैं - नुकसान बढ़ सकता है जब दर अचानक बदल जाती है.

> 问题:最优衰减点取决于数据集和架构――另一个问题就需要重新调整何时降低――转过是突然学习率突然变化时损失可能升――

### कॉसीन एनेलिंग 余弦退火

एक कॉसिन वक्र के बाद अधिकतम सीखने की दर से न्यूनतम तक चिकनी गिरावटः

> अधिकतम सीखने की दर से न्यूनतम सीखने की दर के क्षीण घटने तक, शेष弦曲线 का अनुसरण करेंः

```
lr(t) = lr_min + 0.5 * (lr_max - lr_min) * (1 + cos(pi * t / T))
```

जहां t वर्तमान चरण है और T चरणों की कुल संख्या है।

> इनमें से t है वर्तमान चरण संख्या, T है सर्व चरण संख्या

t=0 पर, कॉसिन शब्द 1 है, इसलिए lr = lr_max। t=T पर, कॉसिन शब्द -1 है, इसलिए lr = lr_min। क्षय शुरू में हल्का होता है, मध्य में तेज होता है, और अंत के करीब फिर से हल्का हो जाता है।

> t=0 时,余弦项为1,所以 lr = lr_max──t=T 时,余弦项为 -1,所以 lr = lr_min──衰减开始平缓,中间加速,末期又变平缓──

यह अधिकांश आधुनिक प्रशिक्षण रन के लिए डिफ़ॉल्ट है. lr_max और lr_min से परे कोई हाइपरपैरामीटर नहीं है. कॉसिन आकार अनुभवजन्य अवलोकन से मेल खाता है कि अधिकांश सीखने प्रशिक्षण के बीच में होता है - आप उस महत्वपूर्ण अवधि के दौरान उचित चरण आकार चाहते हैं।

> यह अधिकांश आधुनिक प्रशिक्षण संचालन की डिफ़ॉल्ट पसंद है। lr_max और lr_min के अलावा, अतिरिक्त स्ट्रिंग आकार अनुभव के अनुसार है। अधिकांश सीखने का अनुभव प्रशिक्षण के मध्य अवधि में होता है।

### वार्मअप: क्यों आप छोटे से शुरू करें  वार्मअप: क्यों आप छोटे से सीखने की दर से शुरू करें 

एडम और अन्य अनुकूलन अनुकूलक ग्रेडिएंट औसत और भिन्नता के चल रहे अनुमान बनाए रखते हैं। चरण 0 पर, ये अनुमान शून्य पर आरंभिक रूप से किए जाते हैं। पहले कुछ ग्रेडिएंट अपडेट कचरे के आंकड़ों पर आधारित होते हैं। यदि इस अवधि के दौरान आपकी सीखने की दर बड़ी है, तो मॉडल बड़े पैमाने पर, खराब दिशा में कदम उठाता है।

> एडम और अन्य स्व-अनुकूलन अनुकूलक बनाए रखने के लिए औसत और अंतर के परिचालन अनुमानों में से एक है। 0 चरण में, ये अनुमान शून्य के रूप में शुरू किए गए हैं।

Warmup इस समस्या को ठीक करता है. एक छोटी सी सीखने की दर (अक्सर lr_max / warmup_steps या यहां तक कि शून्य) से शुरू करें और पहले N चरणों के दौरान रैखिक रूप से lr_max तक ramp up करें। जब आप पूर्ण सीखने की दर तक पहुंच जाते हैं, तो एडम के आंकड़े स्थिर हो जाते हैं।

> वार्मअप िस समस्या को ठीक कर दिया है ️ एक बहुत ही छोटी सीखने की दर से शुरू होते हैं ️ आम तौर पर lr_max / वार्मअप_steps भी शून्य होते हैं ️), फिर पहले N 步线性 में बढ़कर lr_max ️ होता है ️ जब आप पूर्ण सीखने की दर तक पहुंच जाते हैं, तो एडम की सांख्यिकी स्थिर हो जाती है ️

```
lr(t) = lr_max * (t / warmup_steps)     for t < warmup_steps
```

सामान्य वार्मिंगः कुल प्रशिक्षण चरणों का 1-5%। Llama 3 ने लगभग 1.8 ट्रिलियन टोकन के लिए प्रशिक्षण दिया और 2000 चरणों के लिए गर्म किया। GPT-3 ने 375 मिलियन टोकन से अधिक गर्म किया।

> **【拓展：Warmup 的数学解释】**एडम का विकृति सुधार (m_hat = m_t / (1-beta1^t)) में पहले कुछ चरणों में मुआवजा की कमी है। उदाहरण के लिए, बीटा 1=0.9 में, प्रथम चरण का m_1 = 0.1*ग्रेडिएंट, अलग से (1-0.9) =0.1 में सही स्तर का अनुमान मिलता है।

### रैखिक वार्मिंग + कॉसिन गिरावट .

आधुनिक डिफ़ॉल्ट. रैप ऊपर रैखिक, फिर कॉसिन के साथ गिरावटः

```
if t < warmup_steps:
    lr(t) = lr_max * (t / warmup_steps)
else:
    progress = (t - warmup_steps) / (total_steps - warmup_steps)
    lr(t) = lr_min + 0.5 * (lr_max - lr_min) * (1 + cos(pi * progress))
```

यह है कि Llama, GPT, PaLM, और अधिकांश आधुनिक ट्रांसफार्मर का उपयोग करते हैं। वार्मिंग प्रारंभिक अस्थिरता को रोकता है। कॉसिनस क्षय मॉडल को एक अच्छा न्यूनतम में समायोजित करता है।

> यह Llama、GPT、PaLM 和大多数现代Transformer 使用的方法── वार्मअप 早期不稳定──余弦衰减使模型稳定到一个好的极小值──

### एक चक्र नीति एक चक्र रणनीति

लेस्ली स्मिथ की खोज (2018): प्रशिक्षण के पहले छमाही में कम से उच्च मूल्य तक सीखने की दर को बढ़ाएं, फिर दूसरे छमाही में इसे वापस कम करें। विपरीत अंतर्ज्ञान - आप मध्यवर्ती के माध्यम से सीखने की दर को * क्यों बढ़ाएंगे?

> लेस्ली स्मिथ की खोज (2018): प्रशिक्षण के पहले भाग में सीखने की दर कम से उच्च तक बढ़ेगी, और दूसरे भाग में फिर से घटकर लौटेगी।

सिद्धांतः उच्च सीखने की दर अनुकूलन की प्रक्षेपवक्र में शोर जोड़कर नियमितता के रूप में कार्य करती है। मॉडल रैंप-अप चरण के दौरान नुकसान परिदृश्य का अधिक पता लगाता है, बेहतर बेसिन ढूंढता है। रैंप-डाउन चरण फिर सबसे अच्छा बेसिन पाया के भीतर परिष्कृत करता है।

> 理論: उच्च सीखने की दर अनुकूलित रस्सी के माध्यम से शोर को बढ़ाकर सही ढंग से अनुकूलित करने का कार्य करती है।

```
Phase 1 (0 to T/2):    lr ramps from lr_max/25 to lr_max
Phase 2 (T/2 to T):    lr ramps from lr_max to lr_max/10000
```

1cycle अक्सर एक निश्चित गणना बजट के लिए cosine annealing से तेज ट्रेनें।

> 1 चक्र में निश्चित गणना बजट में आमतौर पर शेष弦 वापसी प्रशिक्षण से तेज़ है।

> **【拓展：微调时的学习率策略】**微调预训练模型(如BERT、Llama) 时,学习率通常比预训小 10-100倍──LoRA 微调 Llama:lr=2e-5~1e-4,warmup=总步数的3%,cosine decay。关键技巧:对不同层使用不同学习率底层(接近输入) 较小的 lr(因为通用特征已经学好了),顶层(接近输出) 较大的 lr因为需要适应新任务) PyTorch 通过参数组实现──

### अनुसूची आकारों के लिए विन्यास आकार के लिए तुलना

```mermaid
graph LR
    subgraph "Constant"
        C1["lr"] --- C2["lr"] --- C3["lr"]
    end

    subgraph "Step Decay"
        S1["0.1"] --- S2["0.1"] --- S3["0.01"] --- S4["0.001"]
    end

    subgraph "Cosine Annealing"
        CS1["lr_max"] --> CS2["gradual"] --> CS3["steep"] --> CS4["lr_min"]
    end

    subgraph "Warmup + Cosine"
        WC1["0"] --> WC2["lr_max"] --> WC3["cosine"] --> WC4["lr_min"]
    end
```

### निर्णय प्रवाह चार्ट

```mermaid
flowchart TD
    Start["Choosing a LR schedule"] --> Know{"Know total<br/>training steps?"}

    Know -->|"Yes"| Budget{"Compute budget?"}
    Know -->|"No"| Constant["Use constant LR<br/>with manual decay"]

    Budget -->|"Large (days/weeks)"| WarmCos["Warmup + Cosine Decay<br/>(Llama/GPT default)"]
    Budget -->|"Small (hours)"| OneCycle["1cycle Policy<br/>(fastest convergence)"]
    Budget -->|"Moderate"| Cosine["Cosine Annealing<br/>(safe default)"]

    WarmCos --> Warmup["Warmup = 1-5% of steps"]
    OneCycle --> FindLR["Find lr_max with LR range test"]
    Cosine --> MinLR["Set lr_min = lr_max / 10"]
```

### प्रकाशित मॉडल से वास्तविक संख्याएँ 已发表模型的实际参数

```mermaid
graph TD
    subgraph "Published LR Configs"
        L3["Llama 3 (405B)<br/>Peak: 3e-4<br/>Warmup: 2000 steps<br/>Schedule: Cosine to 3e-5"]
        G3["GPT-3 (175B)<br/>Peak: 6e-4<br/>Warmup: 375M tokens<br/>Schedule: Cosine to 0"]
        R50["ResNet-50<br/>Peak: 0.1<br/>Warmup: none<br/>Schedule: Step decay x0.1 at 30,60,90"]
        B["BERT (340M)<br/>Peak: 1e-4<br/>Warmup: 10K steps<br/>Schedule: Linear decay"]
    end
```

## इसे बनाओ, इसे पूरा करो।
```figure
lr-schedule
```

## इसे बनाओ

> **【中文解读】**नीचे शून्य से पांच प्रकार की समायोजन रणनीति को लागू करने के बाद एक ही सर्कल के साथ डेटा सेट प्रशिक्षण नेटवर्क के परिणामों के मुकाबले प्रयोग दिखाएगाः उच्च सीखने की दर से प्रसार होता है, कम सीखने की दर से ठहराव होता है, उपयुक्त समायोजन प्रशिक्षण को फिर से तेज और स्थिर बनाता है।

### चरण 1: कार्य अनुसूची चरण 1: समायोजन समारोह

प्रत्येक फ़ंक्शन वर्तमान चरण को लेता है और उस चरण में सीखने की दर को लौटाता है।

> प्रत्येक फ़ंक्शन को प्राप्त करने के लिए वर्तमान चरण संख्या, उस चरण की सीखने की दर पर लौटें।

```python
import math


def constant_schedule(step, lr=0.01, **kwargs):
    return lr


def step_decay_schedule(step, lr=0.1, step_size=100, gamma=0.1, **kwargs):
    return lr * (gamma ** (step // step_size))


def cosine_schedule(step, lr=0.01, total_steps=1000, lr_min=1e-5, **kwargs):
    if step >= total_steps:
        return lr_min
    return lr_min + 0.5 * (lr - lr_min) * (1 + math.cos(math.pi * step / total_steps))


def warmup_cosine_schedule(step, lr=0.01, total_steps=1000, warmup_steps=100, lr_min=1e-5, **kwargs):
    if total_steps <= warmup_steps:
        return lr * (step / max(warmup_steps, 1))
    if step < warmup_steps:
        return lr * step / warmup_steps
    progress = (step - warmup_steps) / (total_steps - warmup_steps)
    return lr_min + 0.5 * (lr - lr_min) * (1 + math.cos(math.pi * progress))


def one_cycle_schedule(step, lr=0.01, total_steps=1000, **kwargs):
    mid = max(total_steps // 2, 1)
    if step < mid:
        return (lr / 25) + (lr - lr / 25) * step / mid
    else:
        progress = (step - mid) / max(total_steps - mid, 1)
        return lr * (1 - progress) + (lr / 10000) * progress
```

### चरण 2: सभी कार्यक्रमों को दृश्यमान करें।

प्रत्येक अनुसूची को प्रशिक्षण के दौरान कैसे विकसित होता है, यह दिखाने के लिए पाठ आधारित एक ग्राफ प्रिंट करें।

> 印文图表, प्रदर्शन प्रत्येक समायोजन प्रशिक्षण प्रक्रिया में विकास

```python
def visualize_schedule(name, schedule_fn, total_steps=500, **kwargs):
    steps = list(range(0, total_steps, total_steps // 20))
    if total_steps - 1 not in steps:
        steps.append(total_steps - 1)

    lrs = [schedule_fn(s, total_steps=total_steps, **kwargs) for s in steps]
    max_lr = max(lrs) if max(lrs) > 0 else 1.0

    print(f"\n{name}:")
    for s, lr_val in zip(steps, lrs):
        bar_len = int(lr_val / max_lr * 40)
        bar = "#" * bar_len
        print(f"  Step {s:4d}: lr={lr_val:.6f} {bar}")
```

### चरण 3: प्रशिक्षण नेटवर्क

सर्कल डेटासेट पर एक सरल दो-परत नेटवर्क, पिछले पाठों के समान, लेकिन अब हम कार्यक्रम को बदलते हैं।

> गोलाकार डेटाबेस पर सरल दो स्तरीय नेटवर्क, पिछले पाठ्यक्रम के समान, लेकिन अब हम बदल विन्यास योजना है।

```python
import random


def sigmoid(x):
    x = max(-500, min(500, x))
    return 1.0 / (1.0 + math.exp(-x))


def relu(x):
    return max(0.0, x)


def relu_deriv(x):
    return 1.0 if x > 0 else 0.0


def make_circle_data(n=200, seed=42):
    random.seed(seed)
    data = []
    for _ in range(n):
        x = random.uniform(-2, 2)
        y = random.uniform(-2, 2)
        label = 1.0 if x * x + y * y < 1.5 else 0.0
        data.append(([x, y], label))
    return data


def train_with_schedule(schedule_fn, schedule_name, data, epochs=300, base_lr=0.05, **kwargs):
    random.seed(0)
    hidden_size = 8
    total_steps = epochs * len(data)

    std = math.sqrt(2.0 / 2)
    w1 = [[random.gauss(0, std) for _ in range(2)] for _ in range(hidden_size)]
    b1 = [0.0] * hidden_size
    w2 = [random.gauss(0, std) for _ in range(hidden_size)]
    b2 = 0.0

    step = 0
    epoch_losses = []

    for epoch in range(epochs):
        total_loss = 0
        correct = 0

        for x, target in data:
            lr = schedule_fn(step, lr=base_lr, total_steps=total_steps, **kwargs)

            z1 = []
            h = []
            for i in range(hidden_size):
                z = w1[i][0] * x[0] + w1[i][1] * x[1] + b1[i]
                z1.append(z)
                h.append(relu(z))

            z2 = sum(w2[i] * h[i] for i in range(hidden_size)) + b2
            out = sigmoid(z2)

            error = out - target
            d_out = error * out * (1 - out)

            for i in range(hidden_size):
                d_h = d_out * w2[i] * relu_deriv(z1[i])
                w2[i] -= lr * d_out * h[i]
                for j in range(2):
                    w1[i][j] -= lr * d_h * x[j]
                b1[i] -= lr * d_h
            b2 -= lr * d_out

            total_loss += (out - target) ** 2
            if (out >= 0.5) == (target >= 0.5):
                correct += 1
            step += 1

        avg_loss = total_loss / len(data)
        accuracy = correct / len(data) * 100
        epoch_losses.append(avg_loss)

    return epoch_losses
```

### चरण 4: सभी शेड्यूल की तुलना करें

प्रत्येक कार्यक्रम के साथ एक ही नेटवर्क को प्रशिक्षित करें और अंतिम हानि और अभिसरण व्यवहार की तुलना करें।

> प्रत्येक अनुसूची प्रशिक्षण के साथ एक नेटवर्क, अंतिम हानि और प्राप्ति व्यवहार की तुलना करें।

```python
def compare_schedules(data):
    configs = [
        ("Constant", constant_schedule, {}),
        ("Step Decay", step_decay_schedule, {"step_size": 15000, "gamma": 0.1}),
        ("Cosine", cosine_schedule, {"lr_min": 1e-5}),
        ("Warmup+Cosine", warmup_cosine_schedule, {"warmup_steps": 3000, "lr_min": 1e-5}),
        ("1cycle", one_cycle_schedule, {}),
    ]

    print(f"\n{'Schedule':<20} {'Start Loss':>12} {'Mid Loss':>12} {'End Loss':>12} {'Best Loss':>12}")
    print("-" * 70)

    for name, schedule_fn, extra_kwargs in configs:
        losses = train_with_schedule(schedule_fn, name, data, epochs=300, base_lr=0.05, **extra_kwargs)
        mid_idx = len(losses) // 2
        best = min(losses)
        print(f"{name:<20} {losses[0]:>12.6f} {losses[mid_idx]:>12.6f} {losses[-1]:>12.6f} {best:>12.6f}")
```

### चरण 5: LR बहुत उच्च बनाम बहुत कम

तीन विफलता मोड दिखाएंः बहुत अधिक (विवर्जन), बहुत कम (क्रॉल) और सही।

> 展示三种失败模式: बहुत उच्च (बहुत कम)

```python
def lr_sensitivity(data):
    learning_rates = [1.0, 0.1, 0.01, 0.001, 0.0001]

    print("\nLR Sensitivity (constant schedule, 100 epochs):")
    print(f"  {'LR':>10} {'Start Loss':>12} {'End Loss':>12} {'Status':>15}")
    print("  " + "-" * 52)

    for lr in learning_rates:
        losses = train_with_schedule(constant_schedule, f"lr={lr}", data, epochs=100, base_lr=lr)
        start = losses[0]
        end = losses[-1]

        if end > start or math.isnan(end) or end > 1.0:
            status = "DIVERGED"
        elif end > start * 0.9:
            status = "BARELY MOVED"
        elif end < 0.15:
            status = "CONVERGED"
        else:
            status = "LEARNING"

        end_str = f"{end:.6f}" if not math.isnan(end) else "NaN"
        print(f"  {lr:>10.4f} {start:>12.6f} {end_str:>12} {status:>15}")
```

## इसे फ्रेमवर्क के साथ लागू करें

> **【中文解读】**PyTorch  15+ प्रकार के调度器 प्रदान करते हैं── सबसे आम उपयोग CosineAnnealingLR 和 HuggingFace के get_cosine_schedule_with_warmup──微调预训练模型时, उपयोग वार्मिंग = 总步数 के 3-5% + कॉसिन गिरावट सबसे सुरक्षित विकल्प है──

PyTorch  में समय निर्धारित करने वालों को प्रदान करता है`torch.optim.lr_scheduler`:

```python
import torch
import torch.optim as optim
from torch.optim.lr_scheduler import CosineAnnealingLR, OneCycleLR, StepLR

model = nn.Sequential(nn.Linear(10, 64), nn.ReLU(), nn.Linear(64, 1))
optimizer = optim.Adam(model.parameters(), lr=3e-4)

scheduler = CosineAnnealingLR(optimizer, T_max=1000, eta_min=1e-5)

for step in range(1000):
    loss = train_step(model, optimizer)
    scheduler.step()
```

वार्मअप + कॉसिन्स के लिए लैम्ब्डा शेड्यूलर या `get_cosine_schedule_with_warmup`HuggingFace सेः

> 对于热点 +余弦,使用 lambda 调度器或 HuggingFace 的 `get_cosine_schedule_with_warmup`:

```python
from transformers import get_cosine_schedule_with_warmup

scheduler = get_cosine_schedule_with_warmup(
    optimizer,
    num_warmup_steps=2000,
    num_training_steps=100000,
)
```

HuggingFace फ़ंक्शन सबसे Llama और GPT ठीक-ठीक करने स्क्रिप्ट का उपयोग करता है। जब संदेह हो, तो वार्मअप + कॉसिनस के साथ वार्मअप = कुल चरणों के 3-5% का उपयोग करें। यह लगभग हर चीज के लिए काम करता है।

> HuggingFace का कार्य अधिकांश Llama 和 GPT 微调脚本使用的──不确定时,使用热点 +余弦,热点为总步数的3-5%── यह लगभग सभी परिदृश्यों में लागू होता है──

## इसे भेजें उत्पाद

इस पाठ से उत्पन्न होता हैः
- `outputs/prompt-lr-schedule-advisor.md`-- एक संकेत जो आपके प्रशिक्षण सेटअप के लिए सही सीखने की दर कार्यक्रम और हाइपरपैरामीटर की सिफारिश करता है

> 本课产出:`outputs/prompt-lr-schedule-advisor.md`- एक सही सीखने की दर समायोजन और सुपर पैरामीटर के सुझाव शब्द

## अभ्यास विषय

1. एक्सपोनेंशियल गिरावट लागू करेंः lr(t) = lr_0 * गामा^t जहां गामा = 0.999. सर्कल डेटासेट पर कोसिन annealing की तुलना करें।

   1. 实现指数衰减:lr(t) = lr_0 * गामा^t, गामा = 0.999──在圆形数据集上和余弦退火对比──

2. सीखने की दर रेंज टेस्ट (लेस्ली स्मिथ) को लागू करेंः कुछ सौ चरणों के लिए प्रशिक्षित करें जबकि 1e-7 से 1 तक एलआर को तेजी से बढ़ाएं। प्लॉट हानि बनाम एलआर। अधिकतम एलआर नुकसान बढ़ने से ठीक पहले है।

   2. 实现学习率范围测试(Leslie Smith): प्रशिक्षण कुछ सौ कदम, साथ ही LR को 1e-7 से बढ़ाकर 1──चित्रण हानि बनाम LR 曲线──最优最大 LR 是 हानि 开始上升前的值──

3. वार्मअप + कोसिन के साथ प्रशिक्षण करें लेकिन वार्मअप की लंबाई को भिन्न करेंः 0%, 1%, 5%, 10%, कुल चरणों का 20%। सबसे अधिक स्थिर प्रशिक्षण के लिए एक मीठा स्थान खोजें।

   3. प्रयोग गरम + 余弦 प्रशिक्षण, लेकिन परिवर्तन गरम 长度:总步数的0%、1%、5%、10%、20%──

4. गर्म रिस्टार्ट (SGDR) के साथ कॉसीन एनीलिंग लागू करेंः प्रत्येक टी चरणों में सीखने की दर को lr_max पर रीसेट करें और फिर से गिरावट। लंबी प्रशिक्षण रन पर मानक कॉसीन की तुलना करें।

   4. 实现带热重启的余弦退火(SGDR): प्रति T 步把学习率重置为 lr_max 并再次衰退──在更长的训练上和标准余弦对比──

5. एक "अनुसूची सर्जन" का निर्माण करें जो प्रशिक्षण हानि की निगरानी करता है और नुकसान स्थिर होने पर स्वचालित रूप से वार्मिंग से कोसिन पर स्विच करता है, और यदि नुकसान बहुत लंबे समय तक पठारों में है तो आईआर को कम करता है।

   5. 构建"调度医生": निगरानी प्रशिक्षण हानि, हानि 稳定时自动变暖 转换到余弦, हानि 停滞太久时降低 lr。

## कीवर्ड्स  शब्द खोज तालिका

| Term | What people say | What it actually means |
|------|----------------|----------------------|
| Learning rate | "How fast the model learns" | The scalar that multiplies the gradient to determine the parameter update size |
| Schedule | "Change the LR over time" | A function that maps training step to learning rate, designed to optimize convergence |
| Warmup | "Start with a small LR" | Linearly ramping the LR from near-zero to the target value over the first N steps to stabilize optimizer statistics |
| Cosine annealing | "Smooth LR decay" | Decreasing the LR following a cosine curve from lr_max to lr_min over training |
| Step decay | "Drop LR at milestones" | Multiplying the LR by a factor (usually 0.1) at fixed epoch intervals |
| 1cycle policy | "Up then down" | Leslie Smith's method of ramping LR up then down in a single cycle for faster convergence |
| LR range test | "Find the best learning rate" | Training briefly while increasing LR to find the value where loss starts diverging |
| Cosine with warm restarts | "Reset and repeat" | Periodically resetting the LR to lr_max and decaying again (SGDR) |
| Eta min | "The floor for the LR" | The minimum learning rate that the schedule decays to |
| Peak learning rate | "The maximum LR" | The highest LR reached during training, typically after warmup |

| 术语 | 俗称 | 实际含义 |
|------|------|---------|
| Learning rate / 学习率 | "模型学得多快" | 乘以梯度决定参数更新大小的标量 |
| Schedule / 调度 | "随时间变 LR" | 把训练步数映射到学习率的函数，旨在优化收敛 |
| Warmup / 预热 | "从小 LR 开始" | 在前 N 步把 LR 从近零线性升到目标值，稳定优化器统计 |
| Cosine annealing / 余弦退火 | "平滑 LR 衰减" | 训练中按余弦曲线从 lr_max 降到 lr_min |
| Step decay / 阶梯衰减 | "里程碑式降 LR" | 在固定 epoch 间隔把 LR 乘以一个因子（通常 0.1） |
| 1cycle policy / 1cycle 策略 | "先升后降" | Leslie Smith 的方法：单周期内先升 LR 后降，加速收敛 |
| LR range test / LR 范围测试 | "找最佳学习率" | 短训练中增加 LR，找到 loss 开始发散的点 |
| Cosine with warm restarts / 带热重启的余弦 | "重置并重复" | 周期性把 LR 重置为 lr_max 再次衰减（SGDR） |
| Eta min / 最小学习率 | "LR 的下限" | 调度衰减到的最小学习率 |
| Peak learning rate / 峰值学习率 | "最大 LR" | 训练期间达到的最高 LR，通常在 warmup 之后 |

## आगे पढ़ना 延伸閱讀

- लोश्चिलोव और हटर, "एसजीडीआरः वार्म रिस्टार्ट्स के साथ स्टोकास्टिक ग्रेडिएंट डाउनसेंट" (2017) -- कोसिन एनीलिंग और वार्म रिस्टार्ट्स पेश किया
  लोश्चिलोव और हट्टर,एसजीडीआर:带热重启的随机梯度下降(2017)引入余弦退火和热重启
- स्मिथ, "सुपर-कन्वर्जेंसः हाई लर्निंग रेट्स का उपयोग करके न्यूरल नेटवर्क का बहुत तेज़ प्रशिक्षण" (2018) -- 1 चक्र नीति पत्र
  स्मिथ,超收: उपयोग विश्वविद्यालय习率快速训练神经网络(2018)1 चक्र 策略论文
- Touvron et al., "Llama 2: ओपन फाउंडेशन और फाइन-ट्यून चैट मॉडल" (2023) -- वार्मअप + कॉसिन शेड्यूल को दस्तावेज करता है जो पैमाने पर उपयोग किया जाता है
  Touvron 等人,Llama 2: ओपन बेस और माइक्रो调聊天模型(2023) ने बड़े पैमाने पर उपयोग के रिकॉर्ड किए वार्मिंग + 余弦调度
- गोयल एट अल., "सटीक, बड़े मिनी बैच एसजीडीः 1 घंटे में प्रशिक्षण छविनेट" (2017) -- रैखिक स्केलिंग नियम और बड़े बैच प्रशिक्षण के लिए वार्मअप
  गोयल 等人,精确大批量 SGD:1 小时训练 ImageNet(2017) 线性缩放规则和大批量训练的热升
