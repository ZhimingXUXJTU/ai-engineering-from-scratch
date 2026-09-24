# पूर्ण ट्रांसफार्मर  एन्कोडर + डिकोडर
# 完整 ट्रांसफार्मर  编码器 + 解码器

> ध्यान तारा है. बाकी सब कुछ  अवशिष्ट, सामान्यीकरण, फ़ीड-फॉरवर्ड, क्रॉस-अटेंशन  है जो आपको इसे गहराई से ढेर करने देता है।

> ध्यान मुख्य बिंदु है। अन्य सभी  शेष कनेक्शन, पुनर्मिलन, पूर्व नेटवर्क, पार ध्यान आपको इसे गहरे से अधिक ढेर करने में सक्षम बनाने के लिए हैं।

> **【中文解读】**इसे एक पूर्ण ट्रांसफार्मर में संरेखित करें।

**Type:** Build | **类型:** 动手
**Language:**पायथन**语言:**पायथन
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head Attention), Phase 7 · 04 (Positional Encoding) | **前置知识:** 阶段 7 · 02（自注意力），阶段 7 · 03（多头注意力），阶段 7 · 04（位置编码）
**Time:** ~75 minutes | **时间:** ~75 分钟

## समस्या  समस्या परिचय

एक एकल ध्यान परत एक विशेषता निकालने वाला है, न कि एक मॉडल। प्रति परत एक मटमूल भाषा के लिए पर्याप्त क्षमता नहीं है। आपको सही नल के बिना गहराई  और गहराई ब्रेक की आवश्यकता है।

> एक ध्यान स्तर विशेषता निकालने वाला है, न कि मॉडल  प्रत्येक स्तर पर एक बार में एक रैंक गुणा करने की क्षमता पर्याप्त नहीं है आपको गहराई की आवश्यकता है और गहराई में कोई सही पाइपलाइन नहीं है

2017 के वास्वनी पेपर में छह डिजाइन निर्णय पैक किए गए थे जिन्होंने एक ध्यान परत को एक स्टैक करने योग्य ब्लॉक में बदल दिया था।  एन्कोडर-केवल (BERT), डिकोडर-केवल (GPT), एन्कोडर-डिकोडर (T5)  से प्रत्येक ट्रांसफार्मर एक ही कंकाल का उत्तराधिकारी है। 2026 में ब्लॉक को परिष्कृत किया गया है (RMSNorm, SwiGLU, प्री-नॉर्म, RoPE) लेकिन कंकाल समान है।

> 2017 में Vaswani 论文打包了六个设计决策,将一个注意层变成堆叠的块──此后每个变压器纯编码器BERT) 纯解码器GPT) 编码器-解码器T5) 都继承了相同的骨架──2026 में, ये块已优化了(RMSNorm、SwiGLU、前归化、RoPE),但骨架完全相同──

यह पाठ कंकाल है। अगले पाठों में इसे  06 कोडर के लिए, 07 कोडर के लिए, 08 कोडर-डेकोडर के लिए विशेषज्ञता दी गई है।

> इस वर्ग में एक ढांचा है। अगला वर्ग इसे विशेष रूप से प्रस्तुत करता है।

> **【中文解读】**单个注意层只是一个特征提取器,不是完整模型――2017 के论文将六个设计决策包装成可堆积的块:嵌入+位置编码、自注意力、FFN、残差连接、层归化、交叉注意力――所有后续变体 变体BERT、GPT、T5都继承了相同的骨架――

## अवधारणा का मूल अवधारणा

![Encoder and decoder block internals, wired](../assets/full-transformer.svg)

### छह टुकड़े  छह घटक

1. **Embedding + positional signal.**टोकन → वेक्टर। RoPE (आधुनिक) या sinusidal (क्लासिक) के माध्यम से इंजेक्ट की गई स्थिति।
   **嵌入 + 位置信号。**टोकन → 向量──通过 RoPE(现代) या正弦编码(经典) 注入位置──

2. **Self-attention.**प्रत्येक स्थिति एक दूसरे की देखभाल करती है.
   **自注意力。**प्रत्येक स्थान सभी अन्य स्थानों पर ध्यान केंद्रित करता है।

3. **Feed-forward network (FFN).**स्थिति के अनुसार दो-परत MLP: `W_2 · activation(W_1 · x)`. विस्तार अनुपात 4 × डिफ़ॉल्ट रूप से।
   **前馈网络 (FFN)。**位置级两层 एमएलपी:`W_2 · activation(W_1 · x)`◊默认扩展比 4×──

4. **Residual connection.** `x + sublayer(x)`इसके बिना, ग्रेडिएंट लगभग 6 परतों के बाद गायब हो जाते हैं।
   **残差连接。** `x + sublayer(x)`                                                                                                                                                                                                                                                              

5. **Layer normalization.** `LayerNorm`या `RMSNorm`(आधुनिक) शेष प्रवाह स्थिर करता है।
   **层归一化。** `LayerNorm`या `RMSNorm`(现代) 稳定残差流

6. **Cross-attention (decoder only).**क्वेरीएं डिकोडर से आती हैं, कुंजी और कोडर आउटपुट से मान।
   **交叉注意力（仅解码器）。**查询来自解码器,键和值来自编码器输出.

### एन्कोडर ब्लॉक (BERT द्वारा उपयोग किया, T5 एन्कोडर)
एक ब्लॉक के माध्यम से एक वेक्टर प्रवाह को देखेंः ध्यान स्थिति में मिश्रित होता है, शेष इसे आगे ले जाता है, FFN इसे बदल देता है, और सामान्य प्रवाह को स्थिर रखता है।

```figure
transformer-block
```

### एन्कोडर ब्लॉक (BERT, T5 एन्कोडर द्वारा उपयोग किया जाता है)

```
x → LN → MHA(self) → + → LN → FFN → + → out
                     ^              ^
                     |              |
                     └── residual ──┘
```

एन्कोडर दो दिशा है, कोई मास्किंग नहीं है, सभी स्थिति सभी स्थिति को देखते हैं।

> 编码器是双向的. 没有掩码. 任何位置都看所有位置.

### डिकोडर ब्लॉक (जीपीटी, टी 5 डिकोडर द्वारा इस्तेमाल किया)

```
x → LN → MHA(masked self) → + → LN → MHA(cross to encoder) → + → LN → FFN → + → out
```

डेकोडर में प्रति ब्लॉक तीन उप-परत होते हैं। मध्य में  क्रॉस-अटेंशन  एकमात्र स्थान है जहां जानकारी को एन्कोडर से डेकोडर तक प्रवाह होता है। शुद्ध डेकोडर-केवल वास्तुकला (जीपीटी) में, क्रॉस-अटेंशन को छोड़ दिया जाता है और आपके पास बस मास्क स्व-अटेंशन + एफएफएन है।

> 解码器 प्रत्येक ब्लॉक में तीन उप-स्तरीय हैं। मध्य में 交叉注意力 है 编码器 से 解码器 की एकमात्र जगह  है 编码器 से 解码器 की ओर प्रवाह                                                                                                                                                                                                                                      

### पूर्व-नियमित बनाम पोस्ट-नियमित

मूल कागज: `x + sublayer(LN(x))`vs `LN(x + sublayer(x))`. 2019 के आसपास पोस्ट-नॉर्म ने अपना पक्ष खो दिया  सावधानीपूर्वक वार्मिंग के बिना गहरे प्रशिक्षण करना कठिन है।`LN`*पूर्व* उपपरत) 2026 डिफ़ॉल्ट हैः Llama, Qwen, GPT-3+, Mistral सभी इसका उपयोग करते हैं।

> मूल निबंधः`x + sublayer(LN(x))`vs `LN(x + sublayer(x))`后归结在2019年左右失没有仔细预热就很难深度训练──前归结`LN`子层*之前*) 是2026年的默认:Llama、Qwen、GPT-3+、Mistral 都使用它──

### 2026 के आधुनिक ब्लॉक 2026 के आधुनिक ब्लॉक

| Component / 组件 | 2017 | 2026 |
|-----------|------|------|
| Normalization / 归一化 | LayerNorm | RMSNorm |
| FFN activation / FFN 激活函数 | ReLU | SwiGLU |
| FFN expansion / FFN 扩展比 | 4× | 2.6×（SwiGLU 使用三个矩阵，总参数匹配） |
| Position / 位置编码 | Sinusoidal absolute / 绝对正弦 | RoPE |
| Attention / 注意力 | Full MHA | GQA (or MLA) |
| Bias terms / 偏置项 | Yes / 有 | No / 无 |

RMSNorm लेयरनॉर्म (एक कम घटाने) के औसत-केंद्रण को कम करता है, जो गणना को बचाता है और अनुभवजन्य रूप से कम से कम स्थिर है।`Swish(W1 x) ⊙ W3 x`) लगातार एलएएमए, पॉलम और क्यूवेन पेपर में रेलू/गेलू एफएफएन से लगभग 0.5 अंक अधिक प्रदर्शन करता है।

> RMSNorm ने LayerNorm के औसत मूल्य को हटाने के लिए कम से कम एक बार घटाया), गणना मात्रा को बचाया, अनुभव पर कम से कम समान रूप से स्थिर हो गया।`Swish(W1 x) ⊙ W3 x`) में Llama、PaLM 和 Qwen 论文中一致地比 ReLU/GELU FFN 好约0.5 个困惑度点──

> **【中文解读】**2026 के आधुनिक ट्रांसफार्मर 块 की तुलना में 2017 के मूल संस्करण के साथ:LayerNorm→RMSNorm,ReLU→SwiGLU,后归一化→前归一化,绝对位置编码→RoPE,全多头注意力→GQA── प्रत्येक सुधार क्रमिक है, लेकिन संयोजन से प्रशिक्षण स्थिरता और मॉडल की गुणवत्ता में काफी सुधार हुआ है──

> **【拓展：为什么 Decoder-only 成为主流】**यद्यपि अनुवाद जैसे कार्यों में कोडर-डिसीडर संरचना का प्राकृतिक लाभ है, लेकिन केवल डीकोडर मॉडल (GPT、Llama) विस्तार और सामान्यता में अधिक जीत हासिल करती है। यह उसी संरचना के साथ समझ और उत्पन्न करने के लिए काम कर सकती है।

### पैरामीटर गिनती।

एक ब्लॉक के लिए `d_model = d`और एफएफएन विस्तार `r`:

>  एक के लिए `d_model = d`且FFN 扩展比为 `r`                                                                                                                                                                                                                                                              

- एमएचए: `4 · d²`(Q, K, V, O प्रक्षेपण)
  एमएचए:`4 · d²`(Q、K、V、O 投影)
- FFN (SwiGLU): `3 · d · (r · d)`≈ ≈`3rd²`
  FFN(SwiGLU):`3 · d · (r · d)`≈ ≈`3rd²`
- मानदंडः नाटकीय
  归一化:可忽略

> **【拓展：参数计数与模型规模的实际意义】**ट्रांसफार्मर के तत्व मुख्य रूप से ध्यान में केंद्रित होते हैं ध्यान में投影(4d^2) और FFN(के बारे में 8d^2 के लिए SwiGLU) मध्य में。Llama 3 8B प्रत्येक परत के बारे में 1.5B 参数,32 परतों के बारे में 7B प्लस इनमेटेड परत और आउटपुट सिर。 समझने के लिए घटक वितरण अनुकूलन में मदद करता हैःMoE  प्रतिस्थापन FFN सकल तत्वों को बढ़ा सकते हैं और सक्रिय गणना में वृद्धि नहीं करते हैं; मात्रात्मककरण(जैसे GPTQ、AWQ) मुख्य संपीड़न FFN 权重──

## इसे बनाओ, इसे पूरा करो।

### चरण 1: निर्माण की सामग्री। चरण 1: निर्माण की संरचना।

छोटे का उपयोग करके `Matrix`कक्षा 03 से (स्वतंत्रता के लिए इस फ़ाइल में कॉपी किया गया):

> प्रयोग第 03 课中的微型 `Matrix`类(已复制到此文件以保持独立):

- `layer_norm(x, eps=1e-5)` औसत घटाएँ, std से विभाजित करें।
  `layer_norm(x, eps=1e-5)`                                                                                                                                                                                                                                                              
- `rms_norm(x, eps=1e-6)` RMS द्वारा विभाजित करें। कोई औसत घटाव नहीं।
  `rms_norm(x, eps=1e-6)` आरएमएस के अलावा 不减平均值
- `gelu(x)`और `silu(x) * W3 x`(स्विगलू) ।
  `gelu(x)`和 `silu(x) * W3 x`(स्विगल) ◊
- `ffn_swiglu(x, W1, W2, W3)`. .
- `encoder_block(x, params)`और `decoder_block(x, enc_out, params)`. .

### चरण 2: एक 2-परत एन्कोडर और एक 2-परत डेकोडर तार  चरण 2: कनेक्ट 2 स्तर कोडर और 2 स्तर कोडर

उन्हें ढेर करें. प्रत्येक डिकोडर क्रॉस-अटेंशन में एन्कोडर आउटपुट पारित करें. आउटपुट प्रोजेक्शन से पहले एक अंतिम LN जोड़ें.

> 堆叠它们──将编码器输出传入每个解码器交叉注意力──在输出投影前添加最终 LN──

```python
def encode(tokens, params):
    x = embed(tokens, params.emb) + sinusoidal(len(tokens), params.d)
    for block in params.encoder_blocks:
        x = encoder_block(x, block)
    return x

def decode(target_tokens, encoder_out, params):
    x = embed(target_tokens, params.emb) + sinusoidal(len(target_tokens), params.d)
    for block in params.decoder_blocks:
        x = decoder_block(x, encoder_out, block)
    return x
```

### चरण 3: खेल के उदाहरण पर आगे बढ़ें. चरण 3: खेल के उदाहरण पर चलें और प्रसारित करें.

एक 6-टोकन स्रोत और 5-टोकन लक्ष्य के माध्यम से फ़ीड करें. आउटपुट आकार सत्यापित करें है `(5, vocab)`कोई प्रशिक्षण नहीं है यह सबक वास्तुकला के बारे में है, नुकसान के बारे में नहीं है।

> 输入 6 个 टोकन के स्रोत और 5 个 टोकन के लक्ष्य──验证输出形状是 `(5, vocab)`不训练本课关注结构,不关注损失

### चरण 4: RMSNorm + SwiGLU में स्विच करें.

LayerNorm और ReLU-FFN को RMSNorm और SwiGLU के साथ बदलें। आकारों की पुष्टि अभी भी मेल खाती है। यह एक फ़ंक्शन प्रतिस्थापन के साथ 2026 आधुनिकीकरण है।

> RMSNorm और SwiGLU के साथ लेयरनॉर्म और ReLU-FFN को प्रतिस्थापित करें। यह एक बार में एक प्रकार का कार्य प्रतिस्थापन है जो 2026 में आधुनिक हो जाएगा।

## इसे फ्रेमवर्क के साथ लागू करें

PyTorch/TF संदर्भ कार्यान्वयनः `nn.TransformerEncoderLayer`,`nn.TransformerDecoderLayer`लेकिन 2026 उत्पादन कोड के अधिकांश अपने स्वयं के ब्लॉक रोल क्योंकिः

> PyTorch/TF 参考实现:`nn.TransformerEncoderLayer``nn.TransformerDecoderLayer` लेकिन 2026 के अधिकांश उत्पादन कोड स्वयं निर्मित होते हैं, क्योंकि:

- फ्लैश ध्यान ध्यान के अंदर बुलाया जाता है, ध्यान के माध्यम से नहीं `nn.MultiheadAttention`. .
  फ्लैश ध्यान ध्यान में ध्यान आंतरिक समायोजन, नहीं गुजर रहा है `nn.MultiheadAttention`
- जीसीए/एमएलए स्टडीलिब संदर्भ में नहीं हैं।
  जीक्यूए/एमएलए 不在标准库参考中──
- RoPE, RMSNorm, SwiGLU PyTorch डिफ़ॉल्ट नहीं हैं।
  RoPE、RMSNorm、SwiGLU नहीं है PyTorch के डिफ़ॉल्ट मूल्य──

**Encoder vs decoder vs encoder-decoder — when to pick:**

> **编码器 vs 解码器 vs 编码器-解码器——何时选择：**

| Need / 需求 | Pick / 选择 | Example / 示例 |
|------|------|---------|
| Classification, embeddings, QA over text / 分类、嵌入、文本 QA | Encoder-only / 纯编码器 | BERT, DeBERTa, ModernBERT |
| Text generation, chat, code, reasoning / 文本生成、聊天、代码、推理 | Decoder-only / 纯解码器 | GPT, Llama, Claude, Qwen |
| Structured input → structured output (translation, summarization) / 结构化转换 | Encoder-decoder / 编码器-解码器 | T5, BART, Whisper |

> **【中文解读】**三种架构的选择:Encoder-only(BERT)适合分类和嵌入;Decoder-only(GPT/Llama)适合生成和通用任务;Encoder-Decoder(T5/BART)适合有明确的"源序列"的结构化转换任务──2026年的主流选择是Decoder-only,因为它的扩展性最好,训练最简洁──

> **【拓展：SwiGLU 为何优于 ReLU】**SwiGLU(स्विस-गेटेड रैखिक इकाई) गेट कंट्रोल तंत्र के माध्यम से FFN की अभिव्यक्ति क्षमता को अधिक मजबूत बनाता है। लामा, पॉलम, क्यूवेन आदि मॉडल के प्रयोगों से पता चलता है कि SwiGLU ReLU/GELU की तुलना में भाषा निर्माण की उलझन में कम 0.5 个点 है। हालांकि इसे दो के बजाय तीन पावरवेट मैट्रिक्स की आवश्यकता होती है।

## इसे भेजें उत्पाद

देखो`outputs/skill-transformer-block-reviewer.md`. कौशल 2026 डिफ़ॉल्ट के खिलाफ एक नए ट्रांसफार्मर ब्लॉक कार्यान्वयन की समीक्षा करता है और गायब टुकड़ों (पूर्व-मानक, RoPE, RMSNorm, GQA, FFN विस्तार अनुपात) को चिह्नित करता है।

> 参见 `outputs/skill-transformer-block-reviewer.md` इस कौशल के आधार पर 2026 वर्ष की डिफ़ॉल्ट सेटिंग नए ट्रांसफार्मर ब्लॉक को अंजाम देने की समीक्षा करें, तथा इसमें कमी का हिस्सा को चिह्नित करें

## अभ्यास विषय

1. **Easy / 简单。**अपने encoder_block में पैरामीटर गिनें `d_model=512, n_heads=8, ffn_expansion=4, swiglu=True`. ब्लॉक को लागू करके और उपयोग करके सत्यापित करें `sum(p.numel() for p in block.parameters())`. .
   计算 `d_model=512, n_heads=8, ffn_expansion=4, swiglu=True`时 encoder_block 的参数──通过实现块并使用 `sum(p.numel() for p in block.parameters())`验证──

2. **Medium / 中等。**पोस्ट-नॉर्म से प्री-नॉर्म पर स्विच करें। दोनों को प्रारंभ करें और यादृच्छिक इनपुट पर 12 स्टैक किए गए परतों के बाद सक्रियण मानक को मापें। पोस्ट-नॉर्म के सक्रियण को विस्फोट करना चाहिए; प्री-नॉर्म को सीमित रहना चाहिए।
   बाद में एकीकरण के परिवर्तन से पूर्व एकीकरण तक। प्रारंभिककरण दोनों में 12 संचयी परतें हैं जो कि क्रमशः प्रविष्टि पर सक्रियण प्रकारों में हैं।

3. **Hard / 困难。**एक खिलौना कॉपी कार्य पर एक 4-परत एन्कोडर-डेकोडर लागू करें (कॉपी `x`100 कदम ट्रेन करें। हानि रिपोर्ट करें। RMSNorm + SwiGLU + RoPE में स्वैप करें  क्या हानि घटती है?
   में玩具复制任务(反转复制 `x`) पर 4 स्तरीय编码器-解码器--- प्रशिक्षण 100 步── रिपोर्ट हानि── RMSNorm + SwiGLU + RoPE हानि के लिए प्रतिस्थापन क्या घट गया?

## कीवर्ड्स  शब्द खोज तालिका

| Term | What people say / 人们怎么说 | What it actually means / 实际含义 |
|------|------------------------------|----------------------------------|
| Block / 块 | "One transformer layer" / "一个 Transformer 层" | Stack of norm + attention + norm + FFN, wrapped in residual connections. 归一化 + 注意力 + 归一化 + FFN 的堆叠，包裹在残差连接中。 |
| Residual / 残差连接 | "Skip connection" / "跳跃连接" | `x + f(x)` output; enables gradient flow through deep stacks. `x + f(x)` 输出；使梯度流能穿过深层堆叠。 |
| Pre-norm / 前归一化 | "Normalize before, not after" / "先归一化，不是后归一化" | Modern: `x + sublayer(LN(x))`. Trains deeper without warmup gymnastics. 现代：`x + sublayer(LN(x))`。无需预热技巧即可训练更深的网络。 |
| RMSNorm | "LayerNorm without the mean" / "没有均值的 LayerNorm" | Divide by RMS; one less op, same empirical stability. 除以 RMS；少一次操作，经验上同样稳定。 |
| SwiGLU | "The FFN everyone switched to" / "大家都换成的 FFN" | `Swish(W1 x) ⊙ W3 x → W2`. Beats ReLU/GELU on LM ppl. 在 LM 困惑度上击败 ReLU/GELU。 |
| Cross-attention / 交叉注意力 | "How the decoder sees the encoder" / "解码器如何看到编码器" | MHA with Q from decoder, K/V from encoder outputs. MHA 的 Q 来自解码器，K/V 来自编码器输出。 |
| FFN expansion / FFN 扩展比 | "How wide the middle MLP is" / "中间 MLP 有多宽" | Ratio of hidden-size to d_model, usually 4 or 2.6 (SwiGLU). 隐藏大小与 d_model 的比率，通常为 4 或 2.6（SwiGLU）。 |
| Bias-free / 无偏置 | "Drop the +b terms" / "去掉 +b 项" | Modern stacks omit biases in linear layers; slight ppl improvement, smaller model. 现代堆栈在线性层中省略偏置；轻微的困惑度改善，更小的模型。 |

## आगे पढ़ना 延伸閱讀

- [Vaswani et al. (2017). Attention Is All You Need](https://arxiv.org/abs/1706.03762) मूल ब्लॉक स्पेसिफिकेशन।
  Vaswani 等人(2017)  原始块规范──

- [Xiong et al. (2020). On Layer Normalization in the Transformer Architecture](https://arxiv.org/abs/2002.04745) क्यों पूर्व-नियमित पूर्व-नियमित से गहराई से आगे निकलता है।
  Xiong 等人(2020)  क्यों पूर्व पुनर्मिलन में गहरे स्तर पर विजय के बाद पुनर्मिलन में शामिल हो गया है。

- [Zhang, Sennrich (2019). Root Mean Square Layer Normalization](https://arxiv.org/abs/1910.07467) आरएमएसनॉर्म।

- [Shazeer (2020). GLU Variants Improve Transformer](https://arxiv.org/abs/2002.05202) SwiGLU पेपर।
  Shazeer(2020)  SwiGLU 论文──

- [HuggingFace `modeling_llama.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) कैनोनिक 2026 केवल डिकोडर ब्लॉक।
  गले लगाना`modeling_llama.py` 2026 वर्ष के विनियमन के शुद्धीकरण उपकरण ब्लॉक
