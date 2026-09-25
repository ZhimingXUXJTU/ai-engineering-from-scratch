# GPT  Sebep dili modeliştirme  GPT  因果语言模型

> BERT her iki tarafı da görüyor. GPT sadece geçmişi görüyor. Üçgen maskası modern AI'de en önemli tek bir kod satırıdır.

> **【中文解读】**GPT sadece Dekoder Transformer, kullanmak için neden bu tür bir şey var.

**Type:** Hands-on | **类型:** 动手
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 05 (Full Transformer), Phase 7 · 06 (BERT)
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar. Sorunlar.

Bir dil modeli bir soruya cevap verir: ilk soruya göre `t-1`Token, token üzerinde olasılık dağılımının ne olduğu`t`Bu sinyali çalıştır  bir sonraki belirti tahmin  ve bir seferde bir belirti gibi keyfi metin oluşturabilecek bir model elde edersiniz.

> 语言模型回答一个问题:给定前 `t-1`- Bir tane, bir tane.`t`个标志的概率分布是什么? Bu sinyalde 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预测 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 预 

Bu şekilde, her pozisyonun tahmininin sadece önceki pozisyonlara bağlı olması gerekir. aksi takdirde model cevaplara bakarak basitce aldatır.

> Tüm dizide bir son ve son olarak çalışmak için, her pozisyonun tahmin edilmesi sadece önceki konumdan bağlıdır. Yoksa model doğrudan cevapları görecek ve görevleri "çalıştıracak".

Sebep maskası bunu yapar.`-inf`Bu değerler, softmax'den önce dikkat puanlarına eklenir. softmax'den sonra, bu pozisyonlar 0 olur. Her pozisyon sadece kendisini ve önceki pozisyonları takip edebilir. ve onu tüm dizine bir kez uyguladığınız için, bir ileri geçişte N paralel bir sonraki belirti tahminlerini elde edersiniz.

> Çünkü bu bir üst üçgenlik.`-inf`值),  softmax                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

GPT-1 (2018), GPT-2 (2019), GPT-3 (2020), GPT-4 (2023), GPT-5 (2024), Claude, Llama, Qwen, Mistral, DeepSeek, Kimi  hepsi aynı çekirdek döngüsü olan sadece dekodörlü sebepçi transformatörlerdir. Sadece daha büyük, daha iyi veriler ve daha iyi RLHF.
GPT-1 (2018), GPT-2 (2019), GPT-3 (2020), GPT-4 (2023), GPT-5 (2025), Claude, Llama, Qwen, Mistral, DeepSeek, Kimi  hepsi aynı çekirdek döngüsü olan sadece dekodörlü sebepçi transformatörlerdir. Onları ayıran şey veri kalitesi, ölçek ve mimari gelişmeler ve eğitim sonrası (SFT, RLHF, DPO ve onların halefi).

> GPT-1(2018)、GPT-2(2019)、GPT-3(2020)、GPT-4(2023)、GPT-5(2024)、Claude、Llama、Qwen、Mistral、DeepSeek、Kimi Bunlar hepsi çözücü cihaz özel因果 Transformer, çekirdek döngü aynı¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬

> **【中文解读】**Çözümlü gizlenme, modern AI'de en önemli bir kod satırıdır. Bir üst üçgen matçının (inf  değeri), dikkat oranına ek olarak, softmax'ın ardından gizlenmiş konum 0'a değişir.

## Konsepten bir şey.

![Causal mask creates a triangular attention matrix](../assets/causal-attention.svg)

### Maske .

Uzunluk bir sırayla .`N`, bir inşaat`N × N`matris:

> 给定长度为 `N`Bir dizi oluşturun.`N × N`矩阵:

```
M[i, j] = 0       if j <= i
M[i, j] = -inf    if j > i
```

Ekle`M`softmax öncesinde yapılan incelemeler için. `exp(-inf) = 0`Dikkat matrisinin her satırı sadece önceki pozisyonlar üzerinde bir olasılık dağılımıdır.

> - Ben de .`M`Yumuşaklık maksimum'a kadar önce gelen ilk dikkat oranına kadar.`exp(-inf) = 0`Bu nedenle, gizlenmiş konumların ağırlığı sıfırdır. Dikkat etmek matçının her satırı sadece öncü konumdaki olasılık dağılımıdır.

Uygulama maliyeti: 1 `torch.tril()`Çağrı, hesaplama zamanı: nanoseconds, etkisi: her şey.

> 实现成本:一行 `torch.tril()`调用──计算时间:纳秒级── tüm alanın etkisi:改变了一切──
### Üçgenin nereden geldiği yer

Maske genellikle dikkat üzerine bir yama olarak sunulur. Delivasyonu diğer yönde çalıştırın ve gizemli olmaktan vazgeçirilir: dikkat bir önbellek ortalamasının üçüncü gelişmesidir ve üçgen bir matris olarak yazılan ortalamanın döngü sınırlarıdır.

**Stage 1 — prefix average.**Bir dizi için en aptalca nedenci özet: pozisyon .`i`pozisyonların ortalaması olur.`0…i`Bir döngü olarak, bu `out[i] = X[:i+1].mean(0)`Aynı hesaplama bir matris çarpmasıdır.

```python
import numpy as np

A = np.tril(np.ones((n, n)))
A = A / A.sum(axis=1, keepdims=True)
out = A @ X
```

Satır `i``A`- Evet .`[1/(i+1), …, 1/(i+1), 0, …, 0]`Diyagonalın üzerindeki sıfırlar sebepliliktir. Gelecek hakkında hiçbir şey gizlenmemiştir. Gelecek asla toplamda değildi.

**Stage 2 — learned weights.**Bir düz ortalama, geçmişteki her simgeyi eşit derecede değerlendirir.`S`Şimdi sıralar artık yapısal olarak birine toplamamaktadır, bu nedenle sayıya bölmek yerine her satırı softmax ile normalleştirin. Softmax asla tam bir sıfır çıkarmaz, bu da nedenlik ilişkisini kırır  eğer gelecekteki puanlar  gibi girmezse `-inf`Çünkü ...`exp(-inf) = 0`- ...

```python
def softmax(x, axis):
    e = np.exp(x - np.max(x, axis=axis, keepdims=True))
    return e / e.sum(axis=axis, keepdims=True)

S = S + np.triu(np.full((n, n), -np.inf), k=1)
A = softmax(S, axis=1)
out = A @ X
```

Aynı üçgen, aynı satır-stochastic matris, aynı bir matmul.`-inf`Maske yeni bir makine değil. 1. aşamada sıfır girişler, softmax'in giriş alanına çevrilmiştir.

**Stage 3 — content-dependent weights.**2. aşamada.`S`Eğitimden sonra sabitlenir: pozisyon 7 her zaman pozisyon 3'ün ağırlığını aynı şekilde taşır.`S = Q @ K.T / sqrt(d_k)`Maske, yumruk, matmul aynı.

Üç aşama, bir değişmez: aşağı üçgen sıra-stochastic matrisi katı sıra.

```figure
mask-derivation
```

### Paralel eğitim, seri sonucu

Eğitim: Tümünü ileriye geçin `(N, d_model)`Bir dizi bir kez, N çapraz entropy kaybı (her pozisyonda bir), toplam, backprop hesaplayın.

> 訓練: tüm için `(N, d_model)`序列做一次前向传播,计算 N 个交叉损失(每个位置一个),求和,反向传播──沿序列并行──这是GPT 训练可扩展的原因一次GPU 通行就能处理批量中的1M 个代币──

İfade: simgeyi simge olarak oluşturursunuz.`[t1, t2, t3]`- Tamam .`t4`- Yem .`[t1, t2, t3, t4]`- Tamam .`t5`- Yem .`[t1, t2, t3, t4, t5]`- Tamam .`t6`KV önbelleği (Denevi 12) gizli durumları kaydetir .`t1…tn`Bu yüzden her adımını yeniden hesaplamazsınız. Ama sonucu derinliği = çıkış uzunluğu. bu da autoregressive vergisidir ve neden çözme her LLM'nin gecikme boğazıdır.

> 推理: her bir simge 生成──输入 `[t1, t2, t3]`- Al .`t4`❖ 输入 `[t1, t2, t3, t4]`- Al .`t5`❖ 输入 `[t1, t2, t3, t4, t5]`- Al .`t6`KV 缓存 (第 12 课)保存 `t1…tn`Bu, her LLM'nin 延迟瓶                                                                                                                                                                                                                                                         

### Kayıp  birer birer değişim

Verilen tokens `[t1, t2, t3, t4]`- ...

> - Evet .`[t1, t2, t3, t4]`- ...

- Giriş: `[t1, t2, t3]`
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`[t1, t2, t3]`
- Hedefler: `[t2, t3, t4]`
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`[t2, t3, t4]`

Her pozisyon için .`i`, hesaplama`-log P(target_i | inputs[:i+1])`Bu, bütün dizinin çapraz entropisi.

> Her bir pozisyon için .`i`,计算 `-log P(target_i | inputs[:i+1])`Bu, tüm dizilerin birincisi.

Bu kayıpta trenler hakkında duyduğunuz her transformatör LM.

> Dinlediğiniz her Transformer 言語模型はこの損失上訓練します.

> **【拓展：Teacher Forcing 与暴露偏差】**GPT trenings teacher forced每步输入真实前一个代币而非模型自己的预测──这导致"暴露偏差" (açıktırma önyargısı): training时模型从未见过自己的错输出,推理时却必须从自己的输出继续产生──

### Şifreleme stratejileri

Eğitimden sonra, örnek seçimi insanların düşündüklerinden daha önemli.

> Eğitim tamamlandıktan sonra, seçim stratejileri insanların hayalinden daha önemlidir.

| Method | What it does | When to use |
|--------|--------------|-------------|
| 方法 | 功能 | 适用场景 |
| Greedy | Argmax every step | Deterministic tasks, code completion |
| 贪心 | 每步取最大值 | 确定性任务、代码补全 |
| Temperature | Divide logits by T, sample | Creative tasks, higher T = more diversity |
| 温度 | 将 logits 除以 T 后采样 | 创意任务，T 越高多样性越大 |
| Top-k | Sample from top-k tokens only | Kills low-probability tails |
| Top-k | 只从概率最高的 k 个 token 采样 | 消除低概率尾部 |
| Top-p (nucleus) | Sample from smallest set with cumulative prob ≥ p | 2020+ default; adapts to distribution shape |
| Top-p（核采样） | 从累积概率 ≥ p 的最小集合中采样 | 2020+ 默认策略；自适应分布形状 |
| Min-p | Keep tokens with `p > min_p * max_p` | 2024+; better at rejecting long tails than top-p |
| Min-p | 保留 `p > min_p * max_p` 的 token | 2024+；比 top-p 更好地拒绝长尾 |
| Speculative decoding | Draft model proposes N tokens, big model verifies | 2–3× latency reduction at same quality |
| 推测解码 | 草案模型提出 N 个 token，大模型验证 | 相同质量下延迟降低 2-3 倍 |

2026'da, min-p + sıcaklık 0.7 açık ağırlıklı modeller için makul bir varsayımdır.

> 2026 yılında, min-p + sıcaklık 0.7 açık kaynak modelinin mantıklı bir şekilde belirlenmiş bir yapılandırmadır.

> **【中文解读】**解码策略的选择直接影响生成质量──贪心搜索(argmax) 确定性任务,温度采样增加多样性,top-p/min-p 截断低概率尾部──2026 yılının öneri:min-p + sıcaklık 0.7, geleneksel top-p 能更好地处理分布的度变化──

> **【拓展：从 GPT-2 到 GPT-4 的规模跳跃】**GPT-2(1.5B 参数)→ GPT-3(175B)→ GPT-4( tahmin 1.8T MoE) büyüklüğü sıçrayışta, yapı değişimleri çok küçük, ancak veri ve eğitim yönteminin gelişimi büyüktür.

### "GPT tarifi"nin işe yaramasına neden

1. **Decoder-only.**Bir katman için bir dikkat + FFN.
   Çeviri:**解码器专用。**没有编码器开销──每层一次注意力 + FFN 通行──
2. **Scaling.**124M → 1.5B → 175B → trilyonlar. Chinchilla ölçekleme yasaları (Denevi 13) size hesaplama nasıl harcanır, söyler.
   Çeviri:**规模扩展。**124M'den 1.5B'ye 175B'ye kadar, tekrar milyonlarca parametreye kadar.
3. **In-context learning.**6B13B civarında ortaya çıktı. Model ince ayarlama yapmadan birkaç atış örneğini takip edebilir.
   Çeviri:**上下文学习。**约在6B-13B 参数时涌现──模型无需微调就能遵循少样本示例──
4. **RLHF.**İnsan tercihleri üzerine eğitim sonrası, çiğ hazırlanmış metinleri sohbet asistanlarına dönüştürdü.
   Çeviri:**RLHF。**İnsan tercihleri üzerine yapılan antrenman sonrası, orijinal antrenman metni sohbet yardımcıları olarak çevrilmiştir.
5. **Pre-norm + RoPE + SwiGLU.**Stablı bir eğitim.
   Çeviri:**Pre-norm + RoPE + SwiGLU。**Büyük çaplı trenim.

GPT-2'den beri temel mimarlık çok fazla değişmedi. Veriler, ölçek ve eğitim sonrası ilkeler ile ilgili ilginç şeyler oldu.

> GPT-2'den beri, çekirdek yapı büyük ölçüde değişmedi. Tüm ilginç şeyler veri, ölçek ve sonrası eğitim açısından gerçekleşmiştir.

> **【中文解读】**GPT'nin başarı unsurları:Only Decoder's 架构的简洁性,规模扩展 (Only Decoder's 架构的简洁性,规模扩展) 上下文学习能力 (~124M'den milyonlarca parametreye kadar) 上文学习能力 (~6B'lik parametre ortaya çıkmaya başladı) RLHF 后训练 (将预训文文转化为对话助手) 以及现代块设计 (Ön-norm + RoPE + SwiGLU)  GPT-2'den beri çekirdek yapı büyük ölçüde değişmedi, yenilikleri öncelikle veri 规模和后训练中.

> **【拓展：自回归生成的推理瓶颈】**GPT'nin temel çelişkisi: eğitim zaman并行计算整个序列 (高效),推理时必须逐代币 生成 (串行) ・KV 缓存 (缓存)  Lesson 12) 和推测解码 (推测解码)  Lesson 16) 推理延迟缓解 (推理延迟) 两个关键技术――

## Yapın.
```figure
causal-mask
```

## Yapın

### Adım 1: sebep maskası

Bakın .`code/main.py`Tek satırlı bir.

> 参见 `code/main.py`一行代码:

```python
def causal_mask(n):
    return [[0.0 if j <= i else float("-inf") for j in range(n)] for i in range(n)]
```

- Bu tüm mekanizma.

> Bu, tüm mekanizma.

### İkinci adım: İki katmanlı GPT-like model

İki dekoder blokunu yığ (maskeli kendi dikkat + FFN, çapraz dikkat yok). Bir token gömülmesi, bir pozisyon kodlaması ve bir unembedding ekleyin (GPT-2'den bu yana token gömülme matrisine bağlanmış  standart bir numara).

> 堆叠两个解码器块(掩码自注意力 + FFN,无交叉注意力) ・・・加点子 嵌入、位置编码和反嵌入(与代币 嵌入矩阵绑定GPT-2 以来的标准技巧) ・・・

### Adım 3: Sonraki belirti tahmin, sonundan sonuna

20 token oyuncak sözcük üzerinde, her pozisyonda logit üretin. Bir-bir değişim hedefi karşı çapraz entropik kayıp hesaplayın.

> 20 tane tokenin oyuncak kelimesi üzerinde, her konumda logitler üretilir.

### 4. adım: Örnekleme

Açgözlülük, sıcaklık, üst-k, üst-p, min-p uygulayın. Her birini sabit bir istekle çalıştırın ve çıkışları karşılaştırın.

> 实现贪心、温度、top-k、top-p、min-p 采样──在固定提示上分别运行并比较输出──一个采样函数只需要10 行代码──

## Çerçeveyi kullanın.

PyTorch, 2026 dilini:

> PyTorch,2026 yılının adet üzre yazılımı:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")
tok = AutoTokenizer.from_pretrained("meta-llama/Llama-3.2-3B-Instruct")

prompt = "Attention is all you need because"
inputs = tok(prompt, return_tensors="pt")
out = model.generate(
    **inputs,
    max_new_tokens=64,
    temperature=0.7,
    top_p=0.9,
    do_sample=True,
)
print(tok.decode(out[0]))
```

Kapusunun altında,`generate()`Önceki geçitini yürütür, son pozisyon logitlerini çekir, bir sonraki jetonu örnekler, ekler ve tekrarlar. Her üretim LLM sonuç kümesi (vLLM, TensorRT-LLM, llama.cpp, Ollama, MLX) aynı döngüyü ağır optimizasyonla uyguluyor  toplu önceden doldurma, sürekli serileme, KV önbelleği sayfalama, spekülasyonsal dekodlama.

> Alt katta,`generate()`运行前向传播,取出最后位置的logits,采样下一个代币,追加到序列中,重复──每个生产 LLM 推理(vLLM、TensorRT-LLM、llama.cpp、Ollama、MLX) 都用大量优化实现相同循环批量预填、连续批处理、KV 缓存分页、推测解码──

**GPT vs BERT, one line each:**GPT tahminleri `P(x_t | x_{<t})`BERT tahmin ediyor .`P(x_masked | x_unmasked)`Kayıp, modelin üretebildiğini belirler.

> **GPT 与 BERT 各一句话：**GPT 预测 `P(x_t | x_{<t})`│BERT 预测 │`P(x_masked | x_unmasked)`◊ Kayıp işlevi modelin üretilebilmesini belirler.

## İndirin . Ürünler .

Bakın .`outputs/skill-sampling-tuner.md`. Yetenek yeni nesil görev için örnekleme parametrelerini seçer ve deterministik dekodlama gerektiğinde işaretler.

> 参见 `outputs/skill-sampling-tuner.md`Bu beceride yeni oluşturma görevleri için parametre seçme, belirleme ve belirleme gereksinimleri belirlenir.

## Egzersizler.

1. **Easy.**Çık .`code/main.py`ve nedenci dikkat matrisinin softmax'den sonra alt üçgenli olduğunu kontrol edin.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`, test etkisi dikkat etkisi matçları softmax 后是下三角的──抽查:第3 行只有在第0-3 列有权──
2. **Medium.**Beam 4 ile açgözlülüğün karmaşıklığını 10 kısa sorguda karşılaştırın. Beam her zaman kazanıyor mu? (Tavsiye: genellikle çeviri için, açık uç sohbet için değil.)
   Çinçe Çevirisi: 实现宽度为 4 的束搜索──在 10 短提示上比较束搜索和贪心搜索的困惑──束搜索一定要好些吗?
3. **Hard.**Spekülatör çözümü uygulayın: taslak olarak küçük bir iki katlı model ve doğrulayıcı olarak 6 katlı model kullanın.
   Çinçe çevirisi: implement推测解码: 2 层小模型作为草案模型,6 层模型作为验证器── 100 个长度为 64 的补充上测量实际加速比──确认输出与验证器的贪心解码一致──

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Causal mask | "The triangle" | Upper-triangular `-inf` matrix added to attention scores so position `i` only sees positions `≤ i`. |
| 因果掩码 | "三角矩阵" | 加到注意力分数上的上三角 `-inf` 矩阵，使位置 `i` 只能看到位置 `≤ i`。 |
| Next-token prediction | "The loss" | Cross-entropy of the model's distribution against the true next token at every position. |
| 下一个 token 预测 | "损失函数" | 模型分布与每个位置真实下一个 token 之间的交叉熵。 |
| Autoregressive | "Generate one at a time" | Feed output back as input; parallelism only during training, not during generation. |
| 自回归 | "逐个生成" | 将输出反馈为输入；仅在训练时并行，生成时不并行。 |
| Logits | "Pre-softmax scores" | Raw output of the LM head before softmax; sampling happens on these. |
| Logits | "softmax 前的分数" | LM 头在 softmax 之前的原始输出；采样基于这些值。 |
| Temperature | "Creativity knob" | Divide logits by T; T→0 = greedy, T→∞ = uniform. |
| 温度 | "创造力旋钮" | 将 logits 除以 T；T→0 为贪心，T→∞ 为均匀分布。 |
| Top-p | "Nucleus sampling" | Truncate distribution to smallest set summing to ≥p; sample from what remains. |
| Top-p | "核采样" | 将分布截断为累积概率 ≥ p 的最小集合；从剩余部分采样。 |
| Min-p | "Better than top-p" | Keep tokens where `p ≥ min_p × max_p`; adapts cutoff to sharpness of distribution. |
| Min-p | "比 top-p 更好" | 保留 `p ≥ min_p × max_p` 的 token；根据分布锐度自适应调整截断。 |
| Speculative decoding | "Draft + verify" | Cheap model proposes N tokens; big model verifies in parallel. |
| 推测解码 | "草案+验证" | 廉价模型提出 N 个 token；大模型并行验证。 |
| Teacher forcing | "Training trick" | During training, feed the true previous token, not the model's prediction. Standard for every seq2seq LM. |
| Teacher forcing | "训练技巧" | 训练时输入真实的前一个 token，而非模型的预测。所有 seq2seq 语言模型的标准做法。 |

## Daha fazla okumak

- [Radford et al. (2018). Improving Language Understanding by Generative Pre-Training](https://cdn.openai.com/research-covers/language-unsupervised/language_understanding_paper.pdf) GPT-1.
  Çeviri:GPT-1
- [Radford et al. (2019). Language Models are Unsupervised Multitask Learners](https://cdn.openai.com/better-language-models/language_models_are_unsupervised_multitask_learners.pdf) GPT-2.
  Çeviri:GPT-2
- [Brown et al. (2020). Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) GPT-3 ve bağlam içi öğrenme.
  Çinçe Çevirimi:GPT-3 和上下文学习论文。
- [Leviathan, Kalman, Matias (2023). Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) Spec kodlama kağıdı.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [HuggingFace `modeling_llama.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) Kanonik nedensel-LM referans kodu.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç
