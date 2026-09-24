# KV कैश, फ्लैश ध्यान और तर्क अनुकूलन

> प्रशिक्षण समानांतर है और FLOP-bound है. इन्फरेंस सीरियल है और स्मृति-bound है. अलग-अलग बोतल गला, अलग-अलग ट्रिक्स.

> **【中文解读】**KV कैश  कैश स्टोरेज का हिसाब किया गया कुंजी/मूल्य 避免重复计算,是 LLM 推理加速的核心──Flash Attention 优化显存访问模式,减少显存使用──

**Type:** Hands-on | **类型:** 动手
**Language:**पायथन**语言:**पायथन
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 07 (GPT)
**Time:** ~75 minutes | **时间:** ~75 分钟

## समस्या  समस्या परिचय

एक भोले ऑटोरेग्रेसिव डिकोडर करता है `O(N²)`उत्पादन के लिए काम करना `N`टोकनः प्रत्येक चरण में यह पूर्ण पूर्वावलोकन पर ध्यान को पुनः गणना करता है। 4K-token प्रतिक्रिया के लिए जो 16M ध्यान संचालन है, उनमें से अधिकांश अधिशेष हैं। एक पूर्वावलोकन टोकन की हर छिपी हुई स्थिति निर्धारित है एक बार गणना की गई है। आपको केवल नए टोकन के क्वेरी को पहले की सभी कैश कुंजी और मूल्यों के खिलाफ चलाने की आवश्यकता है।

> एक साधारण स्व-घटनीय कूटनीतिक उपकरण उत्पन्न`N`个 टोकन 需要 `O(N²)`काम की मात्राः प्रत्येक चरण में पूर्ण पूर्वानुमान पर ध्यान दिया जाता है। 4K टोकन के लिए, यह 16M बार ध्यान दिया जाता है, जिनमें से अधिकांश अपर्याप्त हैं।

इसके अलावा, ध्यान स्वयं बहुत सारे डेटा को स्थानांतरित करता है। मानक ध्यान एक N×N स्कोर मैट्रिक्स, N×d सॉफ्टमैक्स आउटपुट, N×d अंतिम आउटपुट  को HBM पर बहुत अधिक पढ़ता और लिखता है। N≥2K के लिए, ध्यान FLOP-bound बनने से पहले स्मृति-बंधित हो जाता है। क्लासिक ध्यान कर्नेल 410× द्वारा आधुनिक GPU का उपयोग कम करते हैं।

> इसके अलावा, ध्यान स्वयं को बड़ी मात्रा में डेटा को स्थानांतरित करने के लिए है। मानक ध्यान N×N 分数矩阵、N×d softmax 输出、N×d अंतिम आउटपुट को HBM के लिए पढ़ने के लिए बहुत अधिक समय है।

दो अनुकूलन, दोनों दावो और अन्य से, सीमा पर निष्कर्ष को "धीमी" से "त्वरित" तक धकेल दियाः

> 两个优化 (都来自道人) 将前沿推理从"慢"推向"快"

1. **KV cache.**प्रत्येक उपसर्ग टोकन के K और V वेक्टरों को स्टोर करें. प्रत्येक नए टोकन का ध्यान कैश की कुंजी के खिलाफ एक क्वेरी है। इन्फेरेंस से कम होता है `O(N²)``O(N)`प्रति पीढ़ी कदम।
   中文翻译:**KV 缓存。**存储 प्रत्येक पूर्व टोकन के K 和 V 向量── प्रत्येक नए टोकन का ध्यान कैश कुंजी पर एक प्रश्न है──推理从每步 `O(N²)`降低到 `O(N)`
2. **Flash Attention.**ध्यान गणना टाइल ताकि पूर्ण N × N मैट्रिक्स कभी HBM को नहीं हिट करता है। सभी सॉफ्टमैक्स + मत्मूल SRAM में होता है। A100 पर 24× वॉल-क्लॉक स्पीडअप; FP8 के साथ H100 पर 510×।
   中文翻译:**Flash Attention。**ध्यान गणना खंडों में करना, पूर्ण N×N 矩阵 को हमेशा HBM में नहीं लिखना। सभी सॉफ्टमैक्स + 矩阵乘法 सभी SRAM में पूर्ण होते हैं।

2026 तक दोनों सार्वभौमिक हैं। प्रत्येक उत्पादन निष्कर्ष स्टैक (vLLM, TensorRT-LLM, SGLang, llama.cpp) उन्हें मानता है। फ्लैश ध्यान सक्षम प्रत्येक सीमा मॉडल जहाज।

> 2026 तक, दोनों लोकप्रिय हो चुके हैं। प्रत्येक उत्पादन सुझावों को लागू किया गया है।

> **【中文解读】**推理优化两大核心技术:KV Cache 存储已计算的钥匙/值向量,避免重复计算,将每步推理从O(N^2) 降至O(N);Flash Attention 通过分块计算避免 N×N矩阵写入HBM, SRAM में सभी गणनाएं पूरी करें, गति बढ़कर 2-10 गुना हो जाएगी।

## अवधारणा का मूल अवधारणा

![KV cache growth and Flash Attention tiling](../assets/kv-cache-flash-attn.svg)

### KV कैश गणित

प्रति डिकोडर परत, प्रति टोकन, प्रति सिरः

> प्रत्येक कोड लेयर, प्रत्येक टोकन, प्रत्येक सिरः

```
bytes_per_token_per_layer = 2 * d_head * dtype_size
                          ^
                          K and V
```

32 परतों, 32 सिरों, d_head=128, fp16 के साथ 7B मॉडल के लिएः

> 对于7B 模型(32 层、32 头、d_head=128、fp16):

```
per token per layer = 2 * 128 * 2 = 512 bytes
per token (32 layers) = 16 KB
per 32K context = 512 MB
```

> **【拓展：GQA 对 KV 缓存的影响】**GQA(Grouped-Query Attention) KV 头从 n_heads 减少到 n_kv_heads,直接等比例缩小 KV 缓存――उदाहरण के लिए Llama 3 70B के 64 查询头 / 8 KV 头配置, KV 缓存压缩了8倍――128K 上下文中, यह लगभग 4 GB 减少到 0.5 GB के KV 缓存,是长上下文推理的关键优化――

Llama 3 70B के लिए (80 परतें, d_head=128, GQA 8 KV heads के साथ):

> 对于Llama 3 70B(80 层、d_head=128、GQA 8 个 KV 头):

```
per token per layer = 2 * 8 * 128 * 2 = 4096 bytes (4 KB)
per 32K context = 10.4 GB
```

कि 10 GB है कि क्यों Llama 3 70B 128K संदर्भ में केवल केवी कैश के लिए 40 GB A100 के अधिकांश की जरूरत है बैच आकार 1 पर।

> यह 10 जीबी यही कारण है कि Llama 3 70B में 128K ऊपर नीचे केवल KV 缓存(बैच आकार 1) पर जरूरत है अधिकांश 40 जीबी A100 显存

**GQA is the KV-cache win.**64 हेड के साथ एमएचए 32 जीबी होगा। एमएलए और भी अधिक संपीड़ित करता है।

> **GQA 是 KV 缓存的胜利。**64 头的MHA 需要32GB──MLA 压缩得更进一步──
आयामों को खींचें और कैश आकार को आगे बढ़ते देखें। अनुक्रम की लंबाई या बैच को आगे बढ़ाएं और देखें कि यह एक एकल GPU से आगे कितनी तेजी से उड़ता हैः

```figure
kv-cache-sizer
```

### फ्लैश ध्यान  टाइलिंग ट्रिक

मानक ध्यानः

> 标准注意力:

```
S = Q @ K^T          (HBM read, N×N, HBM write)
P = softmax(S)       (HBM read, HBM write)
O = P @ V            (HBM read, HBM write)
```

तीन एचबीएम राउंड ट्रिप। एच 100 पर, एचबीएम बैंडविड्थ 3 टीबी / एस है; एसआरएएम 30 टीबी / एस है। हर एचबीएम यात्रा 10 का कारक है सब कुछ चिप पर रखने के मुकाबले धीमा।

> तीन बार एचबीएम 往返── H100 पर, एचबीएम 带宽 3 टीबी/s है; एसआरएएम 30 टीबी/s है── प्रति बार एचबीएम 访问比在片上保持所有数据慢10倍──

फ्लैश ध्यानः

```
for each block of Q (tile size ~128 × 128):
    load Q_tile into SRAM
    for each block of K, V:
        load K_tile, V_tile into SRAM
        compute S_tile = Q_tile @ K_tile^T     (SRAM)
        running softmax aggregation             (SRAM)
        accumulate into O_tile                  (SRAM)
    write O_tile to HBM
```

प्रति टाइल एक HBM यात्रा. कुल स्मृति पदचिह्न से गिरता है`O(N²)``O(N)`. बैकवर्ड पास आगे के पास से कुछ मानों को स्टोर करने के बजाय पुनः गणना करता है  एक और मेमोरी जीत।

> प्रत्येक टाइल एक बार एचबीएम का दौरा किया गया।`O(N²)`降到 `O(N)` विपरीत प्रवाहन से पूर्व प्रवाहन में पुनः गणना कुछ मूल्यों को भंडारण के बजाय  एक और内存 लाभ

**Numerical trick.**चल रही softmax बनाए रखता है `(max, sum)`फ्लैश ध्यान मानक ध्यान के लिए बिट-समान आउटपुट की गणना करता है (मॉड्यूल fp16 गैर-संबद्धता) ।

> **数值技巧。**运行时软max 跨 टाइल 维护 `(max, sum)`Flash Attention 计算与标准注意力逐位相同的输出 (Fp16 के अलावा) 

> **【中文解读】**फ्लैश ध्यान की मूल तकनीकः将注意力计算分块(tiling), GPU के रैपिड SRAM में सॉफ्टमैक्स और矩阵乘法 को पूरा करें, N×N के मध्य矩阵 को धीमी गति HBM में लिखने से बचें।

> **【拓展：vLLM 的 PagedAttention】**पेजड ध्यान(vLLM) KV 缓存 को स्थिर आकार के "पृष्ठ" के लिए व्यवस्थित करेगा, ऑपरेटिंग सिस्टम के समान वर्चुअल内存। यह नेमेज टुकड़े की समस्या को समाप्त कर दिया, जिससे कई并发请求 GPU 显存 को उच्च कुशलता से साझा कर सकें।

**Version evolution:**

| Version | Year | Key change | Speedup on reference hardware |
|---------|------|-----------|-------------------------------|
| 版本 | 年份 | 关键变化 | 参考硬件上的加速 |
| Flash 1 | 2022 | Tiled SRAM kernel | 2× on A100 |
| Flash 2 | 2023 | Better parallelism, causal-first ordering | 3× on A100 |
| Flash 3 | 2024 | Hopper asynchrony, FP8 | 1.5–2× on H100 (~740 TFLOPs FP16) |
| Flash 4 | 2026 | Blackwell 5-stage pipeline, software exp2 | Inference-first (forward only initially) |

फ्लैश 4 केवल लॉन्च के समय आगे-पास है। प्रशिक्षण अभी भी फ्लैश 3 का उपयोग करता है। GQA और varlen फ्लैश 4 के लिए समर्थन (मध्य 2026) इंतजार कर रहा है।

> फ्लैश 4 发布时仅支持前向传播──训练仍使用Flash 3──Flash 4 के GQA 和变长支持待定(2026年中)。

### अनुमानित डिकोडिंग  अन्य विलंबता जीत

सस्ते मॉडल N टोकन का प्रस्ताव करता है। बड़ा मॉडल सभी N को समानांतर में सत्यापित करता है। यदि सत्यापन k टोकन स्वीकार करता है, तो आपने k पीढ़ियों के लिए 1 बड़ा मॉडल फॉरवर्ड पास का भुगतान किया है। कोड और प्रोसेस पर विशिष्ट k = 35।

> 廉价模型提出 N 个代币――大模型并行验证所有 N 个―― यदि验证 ने k 个代币 स्वीकार किया है, तो आप एक बड़े मॉडल के साथ अग्रिम प्रसार प्राप्त करते हैं k 个生成――代码和散文的典型 k=3-5――

2026 चूकेंः
- **EAGLE 2 / Medusa.**एकीकृत ड्राफ्ट हेड जो सत्यापनकर्ता के छिपे हुए राज्यों को साझा करते हैं। 23x गुणवत्ता हानि के बिना गति।
  中文翻译:**EAGLE 2 / Medusa。**集成草案头,共享验证器的隐藏状态──2-3倍加速,质量损失──
- **Speculative decoding with draft model.**उपभोक्ता हार्डवेयर पर 24x गति।
  中文翻译:**带草案模型的推测解码。**消费级硬件上 2-4 倍加速──
- **Lookahead decoding.**जैकोबी पुनरावृत्ति; कोई ड्राफ्ट मॉडल की जरूरत नहीं. Niche लेकिन मुक्त.
  中文翻译:**前瞻解码。**जैकोबी 代;不需要草案模型──小众但免费──

### निरंतर बैचिंग

क्लासिक बैचड इन्फेरेंसः सबसे धीमी अनुक्रम के समाप्त होने की प्रतीक्षा करें, फिर एक नया बैच शुरू करें। जब लघु प्रतिक्रियाएं जल्दी समाप्त होती हैं तो जीपीयू बर्बाद होती है।

> 经典批量推理: सबसे धीमी क्रम के पूरा होने का इंतजार करें, फिर नई मात्रा शुरू करें.

निरंतर बैचिंग (पहले ऑर्का में शिप किया गया, अब vLLM, TensorRT-LLM, SGLang में): पुराने काम खत्म होने के तुरंत बाद नए अनुरोधों को बैच में स्विच करें। सामान्य चैट वर्कलोड के लिए 510x थ्रूपुट लाभ।

> 连续批处理(首次在Orca中发布,现在在vLLM、TensorRT-LLM、SGLang 中): पुराने अनुरोध पूरा होने के तुरंत बाद नए अनुरोध में बदलाव किया जाएगा।

### PagedAttention  KV कैश वर्चुअल मेमोरी के रूप में

vLLM की मुख्य विशेषता। KV कैश को 16 टोकन ब्लॉकों में आवंटित किया जाता है; एक पृष्ठ तालिका भौतिक ब्लॉकों के लिए तार्किक स्थानों का नक्शा बनाती है। यह आपको समानांतर नमूनों (बीम खोज, समानांतर नमूनाकरण), शीघ्र कैशिंग के लिए हॉट-स्वैप प्रीफिक्स और डिफ्रागमेंट मेमोरी के माध्यम से साझा करने की अनुमति देता है।

> vLLM की मूल विशेषताएं──KV 缓存 16 टोकन ब्लॉक वितरण; पृष्ठ सारिणी logical position mapping to physical block── अनुमति跨并行样本(束搜索、并行采样) साझा KV,热交换前用于提示缓存,以及内存碎片整理──比朴连续分配升高 4 倍吞吐量──

## इसे बनाओ, इसे पूरा करो।
```figure
flash-attention-memory
```

## इसे बनाओ

देखो`code/main.py`हम लागू करते हैंः

> 参见 `code/main.py` हम इसे पूरा करते हैंः

1. एक भोले आदमी`O(N²)`वृद्धिशील डिकोडर।
   中文翻译: एक सरल `O(N²)`增量解码器──
2. ए `O(N)`KV कैश किए गए डिकोडर।
   中文翻译: एक `O(N)`KV 缓存解码器──
3. एक टाइल सॉफ्टमैक्स जो फ्लैश ध्यान के चल-मैक्स एल्गोरिथ्म का अनुकरण करता है।
   中文翻译:一个模拟闪光注意 运行时最大值的分块软max──

### चरण 1: KV कैश

```python
class KVCache:
    def __init__(self, n_layers, n_heads, d_head):
        self.K = [[[] for _ in range(n_heads)] for _ in range(n_layers)]
        self.V = [[[] for _ in range(n_heads)] for _ in range(n_layers)]

    def append(self, layer, head, k, v):
        self.K[layer][head].append(k)
        self.V[layer][head].append(v)

    def read(self, layer, head):
        return self.K[layer][head], self.V[layer][head]
```

सरलः प्रति टोकन के, प्रति परत, प्रति सिर सूचियों में V वेक्टरों को बढ़ाते रहें।

> 简单: K、V 向量的每个代币的逐层、逐头的列表中持续增加

### चरण 2: टाइलें सॉफ्टमैक्स

```python
def tiled_softmax_dot(q, K, V, tile=4):
    """Flash-attention-style softmax(qK^T)V with running max/sum."""
    m = float("-inf")
    s = 0.0
    out = [0.0] * len(V[0])
    for start in range(0, len(K), tile):
        k_block = K[start:start + tile]
        v_block = V[start:start + tile]
        scores = [sum(qi * ki for qi, ki in zip(q, k)) for k in k_block]
        new_m = max(m, *scores)
        exp_old = math.exp(m - new_m) if m != float("-inf") else 0.0
        exp_new = [math.exp(sc - new_m) for sc in scores]
        s = s * exp_old + sum(exp_new)
        for j in range(len(out)):
            out[j] = out[j] * exp_old + sum(e * v[j] for e, v in zip(exp_new, v_block))
        m = new_m
    return [o / s for o in out]
```

 के लिए बिट-समान आउटपुट`softmax(qK) V`एक शॉट में, लेकिन किसी भी समय काम सेट एक है`tile × d_head`ब्लॉक, पूर्ण नहीं `N × d_head`. .

> एक बार के साथ`softmax(qK) V`एक ही आउटपुट, लेकिन किसी भी समय काम समूह बस `tile × d_head`块, बजाय अपूर्ण `N × d_head`

### चरण 3: 100 टोकन पीढ़ी पर साफ़ बनाम कैश किए गए डिकोडिंग की तुलना करें

ध्यान के संचालन की गणना करें।`O(N²)`= 5050। कैशः `O(N)`= 100। कोड दोनों प्रिंट करता है।

> 計算注意力操作次数──朴素:`O(N²)`= 5050──缓存:`O(N)`= 100 ⋅代码会打印两者⋅

## इसे फ्रेमवर्क के साथ लागू करें

```python
# HuggingFace transformers auto-enables KV cache on decoder-only generate().
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-3B",
    attn_implementation="flash_attention_2",  # use FA3 if Hopper
    torch_dtype="bfloat16",
)
# generate() uses KV cache automatically
```

vLLM उत्पादनः

> वीएलएलएम 生产部署:

```bash
pip install vllm
vllm serve meta-llama/Llama-3.1-70B-Instruct \
    --tensor-parallel-size 4 \
    --max-model-len 32768 \
    --enable-prefix-caching \
    --kv-cache-dtype fp8
```

अनुरोधों के बीच पूर्वावलोकन कैशिंग एक बड़ी 2026 जीत है  एक ही सिस्टम प्रॉम्प्ट, कुछ शॉट उदाहरण, या लंबे संदर्भ दस्तावेज़ कॉल के बीच KV का पुनः उपयोग करता है। दोहराए गए टूल प्रॉम्प्ट के साथ एजेंट वर्कलोड के लिए, पूर्वावलोकन कैशिंग नियमित रूप से 5 × थ्रूपुट लाभ है।

> 跨请求的前缓存是2026 के प्रमुख लाभ समान प्रणाली提示、少样本示例或长上下文文档在调用间重复使用 KV── के लिए दोहराव उपकरण提示 के लिए代理工作负载,前缓存 आमतौर पर 5 गुना吞吐量提升带来

## इसे भेजें उत्पाद

देखो`outputs/skill-inference-optimizer.md`. कौशल एक नए निष्कर्ष तैनाती के लिए ध्यान कार्यान्वयन, KV कैश रणनीति, मात्रा और अनुमानात्मक डिकोडिंग चुनता है।

> 参见 `outputs/skill-inference-optimizer.md` यह कौशल नए सुझावों के लिए ध्यान केंद्रित करने के लिए चयनित है  KV 缓存 रणनीति  माप और अनुमानित समाधान योजना 

## अभ्यास विषय

1. **Easy.**दौड़ें`code/main.py`. निर्दोष और कैश किए गए डेकोडर एक ही आउटपुट का उत्पादन करते हैं; अप-कंट अंतर को ध्यान में रखें।
   中文翻译:运行 `code/main.py` पुष्टी करें कि सरल और कैशिंग क्वेरी एक ही आउटपुट उत्पन्न करते हैं; ध्यान दें ऑपरेशन की संख्या में अंतर
2. **Medium.**पूर्वावलोकन कैशिंग लागू करेंः एक प्रॉम्प्ट P और कई पूर्णताएं दी गई हैं, KV कैश भरने के लिए P पर एक आगे का पास चलाएं, फिर प्रति पूर्णता शाखाएं। प्रत्येक के लिए स्पीडअप बनाम पुनः एन्कोडिंग P मापें।
   中文翻译:实现前缓存:给定提示 P 和多个补充,对P 运行一次前向传播填充 KV 缓存,然后每个补充分支――测量与每次重编码 P 相比的速度提升――
3. **Hard.**एक खिलौना को लागू करें PagedAttention: एक मुक्त सूची के साथ 16 टोकन ब्लॉकों में KV कैश। जब एक अनुक्रम समाप्त हो जाता है, तो उसके ब्लॉकों को पूल में वापस लौटाएं। विभिन्न लंबाई के साथ 1,000 चैट पूर्णता का अनुकरण करें। स्मृति टुकड़े टुकड़े बनाम आसन्न आवंटन की तुलना करें।
   中文翻译:实现玩具版 PagedAttention:KV 缓存固定 16 टोकन 块加空列表──序列完成时归还块──模拟 1,000 个变长聊天补全──相比较连续分配的内存碎片化差异──

## कीवर्ड्स  शब्द खोज तालिका

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| KV cache | "The trick that makes decoding fast" | Stored K and V from every prefix token; new queries attend to them instead of recomputing. |
| KV 缓存 | "让解码变快的技巧" | 存储每个前缀 token 的 K 和 V；新查询对它们做注意力而非重新计算。 |
| HBM | "GPU main memory" | High Bandwidth Memory; 80 GB on H100, 192 GB on B200. ~3 TB/s bandwidth. |
| HBM | "GPU 主内存" | 高带宽内存；H100 上 80 GB，B200 上 192 GB。约 3 TB/s 带宽。 |
| SRAM | "On-chip memory" | Per-SM fast memory, ~256 KB per SM on H100. ~30 TB/s bandwidth. |
| SRAM | "片上内存" | 每 SM 的快速内存，H100 上每 SM 约 256 KB。约 30 TB/s 带宽。 |
| Flash Attention | "Tiled attention kernel" | Computes attention without materializing N×N in HBM. |
| Flash Attention | "分块注意力内核" | 不在 HBM 中生成 N×N 矩阵即完成注意力计算。 |
| Continuous batching | "No-wait batching" | Swap finished sequences out, new ones in, without draining the batch. |
| 连续批处理 | "无等待批处理" | 完成的序列换出，新的换入，无需排空批次。 |
| PagedAttention | "vLLM's headline" | KV cache allocated in fixed blocks with a page table; eliminates fragmentation. |
| PagedAttention | "vLLM 的核心特性" | KV 缓存以固定块分配加页表；消除碎片化。 |
| Prefix caching | "Reuse long prompts" | Cache KV for a shared prefix across requests; major cost cut for agents. |
| 前缀缓存 | "复用长提示" | 跨请求缓存共享前缀的 KV；代理场景大幅降低成本。 |
| Speculative decoding | "Draft + verify" | Cheap draft model proposes tokens; big model verifies k in one pass. |
| 推测解码 | "草案 + 验证" | 廉价草案模型提出 token；大模型一次验证 k 个。 |

## आगे पढ़ना 延伸閱讀

- [Dao et al. (2022). FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135) फ्लैश 1
  中文翻译:फ्ल्याश ध्यान 1 论文。
- [Dao (2023). FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning](https://arxiv.org/abs/2307.08691) फ्लैश 2
  中文翻译:फ्ल्याश ध्यान 2 论文。
- [Shah et al. (2024). FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision](https://arxiv.org/abs/2407.08608) फ्लैश 3।
  中文翻译:फ्ल्याश ध्यान 3 论文。
- [FlashAttention-4 release notes (Dao-AILab, 2026)](https://github.com/Dao-AILab/flash-attention) ब्लैकवेल 5 चरण पाइपलाइन और सॉफ्टवेयर-exp2 ट्रिक; इस पाठ में उल्लेखित केवल आगे के लॉन्च चेतावनी के लिए रेपो README पढ़ें।
  中文翻译:Flash Attention 4 发布说明;ब्लैकवेल 5 阶段管道和软件 exp2 技巧。
- [Kwon et al. (2023). Efficient Memory Management for Large Language Model Serving with PagedAttention](https://arxiv.org/abs/2309.06180) VLLM पेपर।
  中文翻译:vLLM पेजडअटेंशन 论文。
- [Leviathan et al. (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) विनिर्देशों का डिकोडिंग।
  中文翻译:推测解码论文──
- [Li et al. (2024). EAGLE: Speculative Sampling Requires Rethinking Feature Uncertainty](https://arxiv.org/abs/2401.15077) समन्वित मसौदा दृष्टिकोण के लिए ईगल-1/2 पेपर जो पाठ में उद्धृत किया गया है।
  中文翻译:ईगल-1/2 论文,集成草案方法──
- [Cai et al. (2024). Medusa: Simple LLM Inference Acceleration Framework with Multiple Decoding Heads](https://arxiv.org/abs/2401.10774) ईगल के साथ मेडुसा दृष्टिकोण का संदर्भ।
  中文翻译:मेडुसा 论文,多解码头方法──
- [vLLM docs — PagedAttention](https://docs.vllm.ai/en/latest/design/kernel/paged_attention.html) 16 टोकन ब्लॉक और पृष्ठ-तालिका डिजाइन पर कैनोनिक गहरी गोता लगाना।
  中文翻译:vLLM PagedAttention 文档,16 टोकन 块和页表设计的深入解析──
