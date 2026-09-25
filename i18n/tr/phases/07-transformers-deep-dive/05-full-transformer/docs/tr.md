# Tam Transformer  Kodlayıcı + Dekodör
# 完整 Transformer  编码器 + 解码器

> Dikkat yıldızdır. Diğer her şey  kalıntılar, normallaşma, ileriye aktarma, çapraz dikkat  derinlere yığılmasına izin veren bir heykel.

> Dikkat, başlıca nokta. Diğer tüm                                                                                                                                                                                                                                                          

> **【中文解读】**Kendine Dikkat Etmek, Çok Başlılık, FFN, Kalıntılı, Katmanlık 组装成完整的变体器──这是注意是你需要的论文的实现──

**Type:** Build | **类型:** 动手
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head Attention), Phase 7 · 04 (Positional Encoding) | **前置知识:** 阶段 7 · 02（自注意力），阶段 7 · 03（多头注意力），阶段 7 · 04（位置编码）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar. Sorunlar.

Tek bir dikkat katmanı bir özellik çıkarıcıdır, bir model değildir. Bir katman için bir matmul dil için yeterli kapasite değildir. Doğru tesisat olmadan derinlik  ve derinlik kesintiler gerekir.

> 单个注意层是特征提取器,不是模型――每层一次矩阵乘法不够语言容量――你需要深度而深度没有正确管道会崩――

2017 Vaswani kağıdı, bir dikkat katmanını yığılabilir bir blok haline getiren altı tasarım kararını paketledi.  sadece kodlayıcı (BERT), sadece dekodör (GPT), sadece kodlayıcı-dekodör (T5) 'den bu yana her transformatör aynı iskeleti miras alır. 2026 yılında bloklar (RMSNorm, SwiGLU, pre-norm, RoPE) geliştirildi, ancak iskelet aynıdır.

> 2017 Vaswani 论文打包了六个设计决策,将一个注意层变成可堆叠的块――此后每个变压器纯编码器(BERT) 、纯解码器(GPT) 、编码器-解码器(T5) 都继承了相同的骨架――2026 yılında, bu bloklar 优化了(RMSNorm、SwiGLU、前归化、RoPE), ancak骨架 tamamen aynı――

Bu ders iskelet. Sonraki dersler onu  06 kodlayıcılar için, 07 dekodörler için, 08 kodlayıcı-dekodör için uzmanlaştırır.

> Bu ders bir yapıtıdır. Sonraki ders bunu özelleştirir.

> **【中文解读】**单个注意层只是一个特征提取器,不是完整模型――2017'deki makale altı tasarım kararını toplayabilir bir blok olarak örtecek:嵌入+位置编码、自注意力、FFN、残差连接、层归化、交叉注意力──所有后续变体 变体BERT、GPT、T5都继承相同的骨架──

## Konsepten bir şey.

![Encoder and decoder block internals, wired](../assets/full-transformer.svg)

### Altı parça. Altı parça.

1. **Embedding + positional signal.**Tokens → vectors. RoPE (modern) veya sinusoidal (klasik) yoluyla enjekte edilen pozisyon.
   **嵌入 + 位置信号。**Token → 向量──通過 RoPE(现代) 或正弦编码(经典) 注入位置──

2. **Self-attention.**Her pozisyon diğerine bakıyor, kodlayıcılarda maskeli.
   **自注意力。**Her yer diğer tüm yerleri takip ediyor.

3. **Feed-forward network (FFN).**Konum açısından iki katlı MLP: `W_2 · activation(W_1 · x)`- Default olarak 4× genişleme oranı.
   **前馈网络 (FFN)。**位置级两层 MLP:`W_2 · activation(W_1 · x)`◊默认扩展比4×──

4. **Residual connection.** `x + sublayer(x)`Bu olmadan, gradientler 6 katınlıktan sonra kaybolur.
   **残差连接。** `x + sublayer(x)`Bu yok, bu derece yaklaşık 6 kat sonra kayboldu.

5. **Layer normalization.** `LayerNorm`veya `RMSNorm`Geri kalan akışı istikrarlı hale getirir.
   **层归一化。** `LayerNorm`Ya da`RMSNorm`(现代) ❖稳定残差流──

6. **Cross-attention (decoder only).**Sorgular dekodörden, anahtarlardan ve kodlayıcı çıkış değerlerinden gelir.
   **交叉注意力（仅解码器）。**Çözücüden gelen sorgu, kodlayıcıdan gelen anahtar ve değer.

### Kodlayıcı blok (BERT tarafından kullanılır, T5 kodlayıcı)
Bir blok boyunca bir vektör akışını izleyin: dikkat pozisyonlar arasında karışır, kalanı ileriye taşıyor, FFN onu dönüştürüyor ve norm akışı istikrarlı tutar.

```figure
transformer-block
```

### Kodlayıcı blok (BERT, T5 kodlayıcı tarafından kullanılır)

```
x → LN → MHA(self) → + → LN → FFN → + → out
                     ^              ^
                     |              |
                     └── residual ──┘
```

Kodlayıcı iki yönlü, maskeli değil.

> 编码器是双向的. 没有掩码. 任何位置都看所有位置.

### Çözücü blok (GPT, T5 Çözücü tarafından kullanılır)

```
x → LN → MHA(masked self) → + → LN → MHA(cross to encoder) → + → LN → FFN → + → out
```

Dekoder blok başına üç alt katman vardır. Orta bir  çapraz dikkat  sadece bilgi kodlayıcıdan dekodöre akıyor. Saf bir dekoder-tek mimaride (GPT) çapraz dikkat atılır ve sadece kendini dikkat + FFN maskeli vardır.

> Çözücüün her bir parçası üç katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir katmanlı bir bir katmanlı bir katmanlı bir bir katmanlılık katlı bir bir katmanlı bir bir katmanlılık katlı bir bir bir katmanlılık katlılılı bir bir bir bir katmanlılık katlılılı bir bir bir bir katmanlılık katlılılılı bir bir bir bir bir katmanlıktır.

### Ön norm vs. sonrası norm .

Orijinal kağıt: `x + sublayer(LN(x))`vs `LN(x + sublayer(x))`. Post-normal 2019 civarında favori kaybetti  dikkatli ısınma olmadan derin bir şekilde eğitmek daha zordur.`LN`* öncesinde* alt katman) 2026'da varsayılan: Llama, Qwen, GPT-3+, Mistral hepsi kullanıyor.

> Önemli bir yazı:`x + sublayer(LN(x))`vs `LN(x + sublayer(x))`◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊  ◊ ◊    ◊ ◊ ◊   ◊ ◊     ◊                ◊                                                                               `LN`Bu, 2026 yılının bir öntanımlı süresi.

### 2026'da modernleşmiş blok.

| Component / 组件 | 2017 | 2026 |
|-----------|------|------|
| Normalization / 归一化 | LayerNorm | RMSNorm |
| FFN activation / FFN 激活函数 | ReLU | SwiGLU |
| FFN expansion / FFN 扩展比 | 4× | 2.6×（SwiGLU 使用三个矩阵，总参数匹配） |
| Position / 位置编码 | Sinusoidal absolute / 绝对正弦 | RoPE |
| Attention / 注意力 | Full MHA | GQA (or MLA) |
| Bias terms / 偏置项 | Yes / 有 | No / 无 |

RMSNorm, hesaplama tasarrufu sağlayan ve en azından empirik olarak aynı derecede sabit olan LayerNorm'un ortalama merkezini düşürür.`Swish(W1 x) ⊙ W3 x`) Llama, PaLM ve Qwen makalelerinde ReLU/GELU FFN'i yaklaşık 0,5 puan daha iyi performans göstermektedir.

> RMSNorm LayerNorm'un ortalama değer merkezileşmesini bıraktı, hesaplama miktarını tasarruf etti, deneyime göre en az aynı şekilde sabit oldu.`Swish(W1 x) ⊙ W3 x`) Llama、PaLM 和 Qwen 论文中一致地比 ReLU/GELU FFN 好約 0.5 个困惑度点──

> **【中文解读】**2026 yılının modern Transformer 块 ile 2017 yılının orijinal sürümü arasında karşılaştırma:LayerNorm→RMSNorm,ReLU→SwiGLU,后归归一化→前归一化,绝对位置编码→RoPE,全多头注意力→GQA。 Her bir gelişme aşamalı, ancak birleşim eğitim kararlılığını ve model kalitesini önemli ölçüde yükseltti。

> **【拓展：为什么 Decoder-only 成为主流】**Kodlayıcı- çözücü yapı çevirme gibi görevlerde doğal avantajlara sahip olsa da, sadece Dekoder'in 模型 (GPT、Llama) genişleme ve genellik açısından daha üstün bir gerçektir. Aynı yapı ile anlama ve oluşturma görevlerini işleyebilir, eğitim hedeflerini birleştirir, ve genişleme Chinchilla 定律验证 tarafından onaylanmıştır. Bu, 2024-2026 yıllarındaki neredeyse tüm önde gelen büyük modellerin Dekoder-tek seçilmesinin nedeni budur.

### Parametre sayısı.

Bir blok için `d_model = d`ve FFN genişlemesi `r`- ...

> Bir kişi için.`d_model = d`且FFN 扩展比为 `r`Çekil:

- MHA:`4 · d²`(Q, K, V, O projeleri)
  MHA:`4 · d²`(Q、K、V、O 投影)
- FFN (SwiGLU): `3 · d · (r · d)`- Evet .`3rd²`
  FFN(SwiGLU):`3 · d · (r · d)`- Evet .`3rd²`
- Normalar: önemsiz
  归一化:可忽略

> **【拓展：参数计数与模型规模的实际意义】**Transformer'ın parametreleri esas olarak dikkatlemeyi çekmektedir. 4d^2) ve FFN(8d^2 için SwiGLU) 中。Llama 3 8B Her kat 1.5B 参数, 32 katlılık 共约 7B + gömülme katmanı ve çıkış başı。 Anlamak için parametreler dağılımı optimize etmektedir:MoE 替换FFN 增增总参数而不增加活计算;量化(如GPTQ、AWQ)

## Yapın.

### Adım 1: Bilt taşları. Adım 1: Bilt yapılandırması.

Küçük olanı kullanırdım .`Matrix`Ders 03'ten sınıflandırılmış (bağımsızlık için bu dosyaya kopyalandı):

> 3. sınıfın küçük biçimi`Matrix`类((Bu dosyaya bağımsız kalmak için kopyolular):

- `layer_norm(x, eps=1e-5)` ortalama çıkar, std ile böl.
  `layer_norm(x, eps=1e-5)`  减去平均值,除以标准差──
- `rms_norm(x, eps=1e-6)` RMS ile bölün.
  `rms_norm(x, eps=1e-6)` RMS dışında.
- `gelu(x)`ve `silu(x) * W3 x`- Evet.
  `gelu(x)`和 `silu(x) * W3 x`(Süylü)
- `ffn_swiglu(x, W1, W2, W3)`- Evet .
- `encoder_block(x, params)`ve `decoder_block(x, enc_out, params)`- Evet .

### Adım 2: İki katlı bir kodlayıcı ve iki katlı bir dekodör bağlayın.

Onları yığ. Kodlayıcı çıkışını her dekodere çapraz dikkatle aktar. Çıkış projesinden önce son bir LN ekle.

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

### Adım 3: Oyuncak örneği üzerinde ilerleyin.

6 simgelik bir kaynak ve 5 simgelik bir hedef gönderin.`(5, vocab)`Bu ders mimarlık hakkında, kayıp değil.

> 输入 6 个标记的源和 5 个标记的目标──验证输出形状是 输入 6 个标记的源和 5 个标记的目标──验证输出形状是 输出形状是 输出形状是 输出形状是 输入的目标是 输入的目标是 输入的来源是 输入的来源是 输入的来源是 输入的来源是 输入的目标是 输入的目的是 输入的目的是 输出的形是 输出的形是 输出的形是 输出的形是 输出的形是 输出的的形是 输入的的的的形是 输出的的形是 输出的的的形是 输入的的的的的形是 输入的的的的的的的的目的是 输入的的的的的目的是 输入的的的的的的目的是 输入的的的的的的的目的是`(5, vocab)`❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖

### Adım 4: RMSNorm + SwiGLU'yu değiştirin.

LayerNorm ve ReLU-FFN'i RMSNorm ve SwiGLU ile değiştirin. Şekillerin halen eşleşmesini onaylayın. Bu bir fonksiyon değiştirmesi ile 2026 modernizasyonu.

> RMSNorm 和 SwiGLU 替换 LayerNorm 和 ReLU-FFN──确认形状仍然匹配──这是通过一次函数替换实现的2026年现代化──

## Çerçeveyi kullanın.

PyTorch/TF referans uygulamalar: `nn.TransformerEncoderLayer`- Evet .`nn.TransformerDecoderLayer`Ama 2026 üretim kodunun çoğu kendi blokunu kullanıyor çünkü:

> PyTorch/TF 参考实现:`nn.TransformerEncoderLayer`- Evet.`nn.TransformerDecoderLayer` ama 2026 yılının çoğu üretim kodları kendiliğinden inşa edildi, çünkü:

- Flash Dikkat, dikkat içindeki dikkatle çağrılır, değil `nn.MultiheadAttention`- Evet .
  Akşam dikkat içinde dikkat düzenlenir, geçmez `nn.MultiheadAttention`- Evet.
- GQA / MLA'nın adı stdlib referansında bulunmuyor.
  GQA / MLA Not in Standard库参考中──
- RoPE, RMSNorm, SwiGLU PyTorch'ın öntanımlı özellikleri değil.
  RoPE、RMSNorm、SwiGLU değil PyTorch'un öntanımlı değeri.

**Encoder vs decoder vs encoder-decoder — when to pick:**

> **编码器 vs 解码器 vs 编码器-解码器——何时选择：**

| Need / 需求 | Pick / 选择 | Example / 示例 |
|------|------|---------|
| Classification, embeddings, QA over text / 分类、嵌入、文本 QA | Encoder-only / 纯编码器 | BERT, DeBERTa, ModernBERT |
| Text generation, chat, code, reasoning / 文本生成、聊天、代码、推理 | Decoder-only / 纯解码器 | GPT, Llama, Claude, Qwen |
| Structured input → structured output (translation, summarization) / 结构化转换 | Encoder-decoder / 编码器-解码器 | T5, BART, Whisper |

> **【中文解读】**Üç çeşit yapısal seçim:Encoder-tek(BERT) için uygun分类和嵌入;Decoder-tek(GPT/Llama) için uygun oluşturma ve genel görev;Encoder-Decoder(T5/BART) için uygun olan açık bir "çıkışlı kaynak sırası" için yapısal dönüşüm görevleri──2026 yılının的主流选择 is Decoder-only, because of its expansion性 best、 training most simple──

> **【拓展：SwiGLU 为何优于 ReLU】**SwiGLU(Swish-Gated Linear Unit) geçiş kontrol mekanizması FFN'in ifade yeteneğini daha güçlüleştirir. Llama, PaLM, Qwen ve diğer modellerin deneylerinin uyumlu olduğu göstermektedir. SwiGLU, ReLU/GELU'nun dil geliştirme karışıklığından yaklaşık 0.5 puan aşağıdır.

## İndirin . Ürünler .

Bakın .`outputs/skill-transformer-block-reviewer.md`. Yetenek, 2026'da varsayılan standartlara göre yeni bir transformatör blok uygulamasını gözden geçirir ve eksik parçaları (pre-norm, RoPE, RMSNorm, GQA, FFN genişleme oranı) işaretler.

> 参见 `outputs/skill-transformer-block-reviewer.md`◊ Bu beceri 2026 yılının standart ayarlarına göre yeni Transformer bloklarını incelemek, ve eksikliği belirlemek için bir bölüm oluşturmak.

## Egzersizler.

1. **Easy / 简单。**Encoder_block'daki parametreleri  olarak say`d_model=512, n_heads=8, ffn_expansion=4, swiglu=True`. Bloku uygulayarak ve `sum(p.numel() for p in block.parameters())`- Evet .
   计算 `d_model=512, n_heads=8, ffn_expansion=4, swiglu=True`时 encoder_block 的参数──通过实现块并使用 `sum(p.numel() for p in block.parameters())`验证。

2. **Medium / 中等。**Post-norm'dan pre-norm'a geçin. Her ikisini de başlatın ve 12 katmanlı bir şekilde rastgele giriş üzerine aktivasyon normunu ölçün. Post-norm'un aktivasyonları patlamalıdır; pre-norm'lar sınırlı kalmalıdır.
   İlk olarak iki yönü de 12 kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat kat

3. **Hard / 困难。**Oyuncak kopyası görevinde 4 katmanlı bir kodlayıcı-dekodör uygula (kopya `x`100 adım tren. Kayıp rapor. RMSNorm + SwiGLU + RoPE değişimi kayıp düşüyor mu?
   Bu oyuncak kopyasını yapma görevi`x`) üzerinde gerçekleştirilen 4 katlı kodlayıcı- çözücü cihazı--- eğitim 100 步── rapor kaybı--- RMSNorm + SwiGLU + RoPE 损失是否下降?

## Anahtar Şartlar .

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

## Daha fazla okumak

- [Vaswani et al. (2017). Attention Is All You Need](https://arxiv.org/abs/1706.03762) orijinal blok özellikleri.
  Vaswani 等人(2017)  原始块规范。

- [Xiong et al. (2020). On Layer Normalization in the Transformer Architecture](https://arxiv.org/abs/2002.04745) neden pre-norm, post-norm'u derinden yendi.
  Xiong 等人(2020)  Neden öne geri dönüşü derin seviyede birleştirmek için

- [Zhang, Sennrich (2019). Root Mean Square Layer Normalization](https://arxiv.org/abs/1910.07467) RMSNorm.

- [Shazeer (2020). GLU Variants Improve Transformer](https://arxiv.org/abs/2002.05202) SwiGLU kağıdı.
  Shazeer(2020)  SwiGLU 论文。

- [HuggingFace `modeling_llama.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/models/llama/modeling_llama.py) kanonik 2026 sadece dekodör blok.
  Yüzü sarma `modeling_llama.py` 2026 yılının kurallarının saf çözümü
