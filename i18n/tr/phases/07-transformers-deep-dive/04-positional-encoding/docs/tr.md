# Konut kodlaması  Sinusoidal, RoPE, ALiBi
# 位置编码  正弦、RoPE、ALiBi

> Dikkat, permutasyon-invariant. "Kedi çarşaf üzerinde oturdu" ve "mat üzerinde sat kedi" pozisyon sinyalsiz aynı çıkış üretir.

> dikkat çekmek için bir dizi değişmez. Bu sorunun çözümü üç farklı algoritma ile çözülmüştür.

> **【中文解读】**Transformer 没有位置信息,需要手动注入──RoPE 是 Llama 使用的方法,ALiBi 支持外推到更长序列──

**Type:** Build | **类型:** 动手
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head Attention) | **前置知识:** 阶段 7 · 02（自注意力），阶段 7 · 03（多头注意力）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Sorunlar. Sorunlar.

Skalalı nokta ürün dikkat, sırayla kördür.`softmax(Q K^T / √d) V`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `X`Dikkatin içinde hiçbir şey pozisyonu önemsemedi.

> 缩放点积注意力是顺序无关的──注意力矩阵 `softmax(Q K^T / √d) V`Bu yüzden, bu da bir sorun değil.`X`Çıkış ve çıkış aynı şekilde bozulur.

Bu bir kelime çantası modelinde bir hata değil. dil, kod, ses, video için  emir anlamı taşıyan her şey  ölümcül.

> Bu bir hata değil. Ama dil, kod, ses, video için ölümcül bir şeydir.

Bu çözüm, yerleşimlere bir şekilde yerleştirmek.

> Düzeltme yönteminin yerleşim biçiminde yerleşmesi üç dönemde geçerlidir:

1. **Absolute sinusoidal**(Vaswani 2017) Ekle `sin/cos`Basit, öğrenilmez, eğitimli uzunluklardan kötü bir şekilde uzaklaştırılır.
   **绝对正弦编码**(Vaswani 2017) 将位置的`sin/cos`Yapılandırma yapısı: basit, öğrenme gerekliliği yok, eğitim uzunluğunun dışında, dışı bir kapasite farkı vardır.

2. **RoPE — Rotary Position Embeddings**(Su 2021). Q ve K vektörlerini pozisyonuna orantılı bir açıyla döndürün.
   **RoPE — 旋转位置嵌入**(Su 2021) ・ Yerine göre doğru oranlı açıdan dönmek Q 和 K 向量──直接在点积中编码*相对*位置──2026年占主地位──

3. **ALiBi — Attention with Linear Biases**(Press 2022). Tüm yerleşimleri atlayın; mesafeye göre dikkat puanlarına baş başına bir çizgi ceza ekleyin. Mükemmel uzunluk ekstrapolasyonu.
   **ALiBi — 带线性偏置的注意力**(Press 2022) ◊ tamamen içine atladı; dikkat çekme oranına göre her başın ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞

2026 itibariyle, esasen her sınır açık modeli RoPE kullanır: Llama 2/3/4, Qwen 2/3, Mistral, Mixtral, DeepSeek-V3, Kimi.

> 2026 yılına kadar, temel olarak her ön kenar açık kaynak modeli RoPE kullanıyor: Lama 2/3/4、Qwen 2/3、Mistral、Mixtral、DeepSeek-V3、Kimi。

> **【中文解读】**Öz dikkat kendisi sırada değişmez 乱乱输入序,输出只是对应打乱. Bu dil için ölümcül.

## Konsepten bir şey.

![Sinusoidal absolute vs RoPE rotations vs ALiBi distance bias](../assets/positional-encoding.svg)

### Kesin sinusoidal.

Bir sabit matris önceden hesaplayın `PE`şekli ile`(max_len, d_model)`- ...

> 预计算一个固定矩阵 `PE`, şekli `(max_len, d_model)`- ...

```
PE[pos, 2i]   = sin(pos / 10000^(2i / d_model))
PE[pos, 2i+1] = cos(pos / 10000^(2i / d_model))
```

O zaman ...`X' = X + PE[:N]`Her boyut farklı bir frekansta sinusoid.`max_len`: hiçbir şey modelin sadece pozisyon 02047'i gördüğünde 2048 pozisyonunda ne olduğunu söylemedi.

> Sonra dikkatli ol.`X' = X + PE[:N]`◊ her boyut farklı frekanslı doğru dalgalardır.`max_len`之外失效: Model sadece 0-2047 pozisyonunda görüldü, hiçbir şey 2048 pozisyonunda olacağını söylemiyor.

### RoPE, yerleşim için dönüştürülmüş.

Bir çift boyut için Q ve K vektörlerini (kaynak değil) döndürün `(2i, 2i+1)`- ...

> 旋转 Q 和 K 向量(not embedded) ⋅对对维度 `(2i, 2i+1)`- ...

```
[q'_2i    ]   [ cos(pos·θ_i)  -sin(pos·θ_i) ] [q_2i   ]
[q'_2i+1  ] = [ sin(pos·θ_i)   cos(pos·θ_i) ] [q_2i+1 ]

θ_i = base^(-2i / d_head),  base = 10000 by default
```

Aynı dönümsellik pozisyonlu anahtarlara uygulayın `pos_k`- Dots ürünü`q'_m · k'_n``(m - n)`- Yalnız.**the attention score depends only on the relative distance**- ...eğer de dönüşüm mutlak pozisyonlarda kilitlenmiş olsa.

> Ana uygulama konumlarına`pos_k`Aynı dönüm noktası.`q'_m · k'_n`Sadece dönüştü`(m - n)`Bu da bir ifade.**注意力分数只取决于相对距离**...eğer de dönüşüm kesin bir konuma dayanırsa... ...çok güzel bir tekniktir.

> **【中文解读】**RoPE'nin net yanı: Dönüş açısı mutlak konumlara dayanırken, Q·K'ın nokta sayısı yalnızca göreci mesafeye (m-n) bağlıdır. Bu da modelin göreci konum ilişkisini oluşturduğunu gösterir.

> **【拓展：RoPE 在 Llama 3 中的长上下文扩展】**Llama 3  YaRN                                                                                                                                                                                                                                                            

RoPE'yi uzatmak: `base`Llama 3'ün 8K'den 128K'ye kadar uzandığı bu şekilde.

> 扩展 RoPE:`base`Bu, 8K'den 128K'ye kadar genişlemenin bir yolu.

### ALiBi , dikkatini yönlendirerek

Dikkatin doğrudan puanlarını ayır.

> 跳过嵌入技巧──直接偏置注意分数:

```
attn_score[i, j] = (q_i · k_j) / √d  -  m_h · |i - j|
```

Nerede ?`m_h`başı için özel bir eğimdir (örneğin `1 / 2^(8·h/H)`) Yakınlıklı tokenler artırılır; uzak tokenler cezalandırılır. Eğitim zamanı maliyeti yoktur. Kağıt uzunluk ekstrapolasyonunun sinusoidal olduğunu ve RoPE'ye orijinal eğitim uzunluğunda eşleştiğini gösterir.

> İçlerinden `m_h`Bu, bir baş eğriden oluşur.`1 / 2^(8·h/H)`)。 Yakınlıklı bir simge yükseltildi; daha uzak bir simge cezalandırıldı。 hiç bir eğitim sırasında ek maliyetleri。

### 2026'da neyi seçmeliyiz?

| Variant / 变体 | Extrapolation / 外推能力 | Training cost / 训练成本 | Used by / 使用者 |
|---------|---------------|---------------|---------|
| Absolute sinusoidal / 绝对正弦编码 | poor / 差 | free / 免费 | original transformer, early BERT |
| Learned absolute / 学习式绝对编码 | none / 无 | tiny / 微小 | GPT-2, GPT-3 |
| RoPE | good with scaling / 良好（带缩放） | free / 免费 | Llama 2/3/4, Qwen 2/3, Mistral, DeepSeek-V3, Kimi |
| RoPE + YaRN | excellent / 优秀 | fine-tune stage / 微调阶段 | Qwen2-1M, Llama 3.1 128K |
| ALiBi | excellent / 优秀 | free / 免费 | BLOOM, MPT, Baichuan |

RoPE, yapısını değiştirmeden dikkat çekerek, nispet konumunu kodlayarak ve `base`hiperparametre uzun bağlamlı ince ayarlama için temiz bir düğme verir.

> RoPE 胜出, yapı değiştirilmemesi nedeniyle dikkat çekebilir, kodlama görevi konumlandırılabilir ve`base`超参数长上下文微调 提供了清晰调节旋──

> **【中文解读】**2026 yılının konum kodlama seçimi çok net: Yeni proje öntanımlı RoPE── yapı değiştirmez, konumlara göre kodlama ‒ ve temel ‒parametrler tarafından ‒ uzun uzun aşağıdaki kısımları netleştirmek için açık bir yol sağlanmıştır.

> **【拓展：位置编码对长上下文 RAG 的影响】**RAG sisteminde, konum kodlama doğrudan uzun dosya işleme yeteneğini etkiler. RoPE + YaRN 让 Llama 3 能处理 128K token 的上下文, bu da yaklaşık 300 sayfalık dosyaları bir kez işleyebileceği anlamına gelir.
```figure
rope-explorer
```

## Yapın

## Yapın.

### Adım 1: Sinusoidal kodlama.

Bakın .`code/main.py`- 4 satırlık hesaplama:

> 参见 `code/main.py`△4 行计算:

```python
def sinusoidal(N, d):
    pe = [[0.0] * d for _ in range(N)]
    for pos in range(N):
        for i in range(d // 2):
            theta = pos / (10000 ** (2 * i / d))
            pe[pos][2 * i]     = math.sin(theta)
            pe[pos][2 * i + 1] = math.cos(theta)
    return pe
```

İlk dikkat katmanından önce bunu yerleştirme matrisine ekleyin.

> İlk dikkat katmanından önce bu da embedded matrix'e eklenecek.

### Adım 2: RoPE'yi Q, K'ye uygula.

RoPE, Q ve K'de yerinde çalışır. Her çift dimmer için:

> RoPE için Q 和 K orijinal toprak işlemleri için:

```python
def apply_rope(x, pos, base=10000):
    d = len(x)
    out = list(x)
    for i in range(d // 2):
        theta = pos / (base ** (2 * i / d))
        c, s = math.cos(theta), math.sin(theta)
        a, b = x[2 * i], x[2 * i + 1]
        out[2 * i]     = a * c - b * s
        out[2 * i + 1] = a * s + b * c
    return out
```

Önemli: aynı işlevi pozisyonda Q ' e uygulayın `m`Ve K pozisyonda `n`- Dots ürünü bir `cos((m-n)·θ_i)`Dikkat, nispet konumunu ücretsiz öğrenir.

> 关键: 位置`m`Bu da bir yer.`n`K                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `cos((m-n)·θ_i)`Çünkü... dikkat ücretsiz öğrenmek için göreceli konum...

> **【中文解读】**RoPE'nin gerçekleştirme merkezi: Q ve K'nin her bir boyutuna (2i, 2i+1) göre bir dönüm yaparak dönüm açısını konum oranına göre doğrulaştırır. Bu nedenle Q_m · K_n'un nokta birikimi ortaya çıkar cos(((m-n) *theta) 项, doğal olarak uzaklık karşısında kodlanır.

### Adım 3: ALiBi eğilimi ve tarafsızlığı

```python
def alibi_bias(n_heads, seq_len):
    # slope_h = 2 ** (-8 * h / n_heads) for h = 1..n_heads
    slopes = [2 ** (-8 * (h + 1) / n_heads) for h in range(n_heads)]
    bias = []
    for m in slopes:
        row = [[-m * abs(i - j) for j in range(seq_len)] for i in range(seq_len)]
        bias.append(row)
    return bias  # add to attention scores before softmax
```

Ekle`bias[h]`- ...`(seq_len, seq_len)`dikkat puanı matrisi başı `h`, sonra softmax.

> - Ben de .`bias[h]`Üstüne`h``(seq_len, seq_len)`Dikkat, sonra yumuşaklık.

### Adım 4: RoPE'nin nispet uzaklık özelliğini doğrulayın.

İki rastgele vektör seçin .`a, b`- Dönüşüm .`(pos_a, pos_b)`- Sonra da .`(pos_a + k, pos_b + k)`Bu özellik RoPE'nin tüm noktasıdır  mutlak sıfırlama ile değişmez, sadece nispetik boşluk önemlidir.

> 选择两个随机向量 `a, b`- Kullanıyorum.`(pos_a, pos_b)`Sonra kullan.`(pos_a + k, pos_b + k)`旋转──2 nokta 积在浮点差范围内必须匹配── RoPE'nin tüm anlamı bu özelliktir.

> **【拓展：位置编码的历史演进】**Vaswani'nin 2017'de mutlak çentel kodlamasından GPT-2/3'nin öğrenme pozisyonu yerleşimine, tekrar RoPE'ye (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (Rope) (

## Çerçeveyi kullanın.

PyTorch 2.5+ gemileri RoPE hizmetleri `torch.nn.functional`Çoğu üretim kodu kullanıyor.`flash_attn`veya `xformers`RoPE dikkat çekirdeğinin içinde uygulanır.

> PyTorch 2.5+ `torch.nn.functional`中内置了 RoPE 工具── çoğu üretim kod kullanımı `flash_attn`Ya da`xformers`, RoPE                                                                                                                                                                                                                                                              

```python
from transformers import AutoModel
model = AutoModel.from_pretrained("meta-llama/Llama-3.2-3B")
# model.config.rope_scaling → {"type": "yarn", "factor": 32.0, "original_max_position_embeddings": 8192}
```

**Long-context tricks in 2026:**

> **2026 年的长上下文技巧：**

- **NTK-aware interpolation.**Yeniden ölçeklendirme`base`- ...`base * (scale_factor)^(d/(d-2))`4K'den 16K'ye kadar uzanırken.
  **NTK-aware 插值。**4K'den 16K'ye kadar genişletilince,`base`重新缩放为 `base * (scale_factor)^(d/(d-2))`- Evet.
- **YaRN.**Daha akıllı bir interpolasyon, uzun bağlamlarda dikkat entropiyi korur. Llama 3.1 128K kullanıyor.
  **YaRN。**Daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha akıllı, daha iyi.
- **LongRoPE.**Microsoft'un 2024 yöntemi, evrimsel arama kullanarak boyut boyutlarındaki faktörleri seçer.
  **LongRoPE。**Microsoft 2024 yılının yöntemi, gelişmiş arama seçimi kullanarak her boyutdaki kısaltma faktörünü seçmek.
- **Position interpolation + fine-tuning.**Sadece pozisyonları uzatma faktörü ile küçültüp 15B token için ince ayarlayın.
  **位置插值 + 微调。**Sadece genişleme faktörünün küçülmesi ve 1-5B tokeninin küçükleştirilmesi gerekir.

## İndirin . Ürünler .

Bakın .`outputs/skill-positional-encoding-picker.md`. Bu beceri, hedef bağlam uzunluğu, ekstrapolasyon ihtiyaçları ve eğitim bütçesi göz önüne alındığında yeni bir model için bir kodlama stratejisini seçer.

> 参见 `outputs/skill-positional-encoding-picker.md`◊ Bu beceri yeni modeller için kodlama stratejileri seçmek, aşağıdaki metin uzunluğu, dış ihtiyaç ve eğitim bütçesini belirlemek için kullanılır.

## Egzersizler.

1. **Easy / 简单。**Sinusoidal çizgiyi çiz .`PE` için bir ısı haritası olarak matris`max_len=512, d=128`"Dimension index büyüdükçe çizgiler daha genişleşiyor" şeklini onaylayın.
   Ben de öyleyim.`PE`矩阵绘制为`max_len=512, d=128`"Dimension index growth 条纹变宽" modelini onaylamak

2. **Medium / 中等。**NTK-a karşı duyarlı RoPE ölçeklendirme uygulayın. 256 uzunluklı sekanslarda küçük bir LM çalıştırın, sonra 1024 uzunlukta ölçeklendirme ile ve olmaksızın test edin. Kafasını karışıklık ölçün.
   实现 NTK-aware RoPE 缩放── uzunluk 256'nin bir dizi üzerinde küçük bir LM eğitmek, sonra uzunluk 1024 测量困惑度──

3. **Hard / 困难。**ALiBi ve RoPE'yi aynı dikkat modülüne uygulayın. 4 katlı bir transformatörü bir kopyalama görevi üzerinde uzunluğu 512 olan dizilerle çalıştırın. Test sırasında 2048'e ekstrapolasyon yapın.
   Aynı dikkat modülü içinde ALiBi ve RoPE gerçekleştirmek için 4 katlı Transformer eğitimi 512'nin kopya görevi üzerinde.

## Anahtar Şartlar .

| Term | What people say / 人们怎么说 | What it actually means / 实际含义 |
|------|------------------------------|----------------------------------|
| Positional encoding / 位置编码 | "Tells attention about order" / "告诉注意力顺序" | Any signal added to embeddings or attention that encodes position. 添加到嵌入或注意力中编码位置的任何信号。 |
| Sinusoidal / 正弦编码 | "The original one" / "原始的那种" | `sin/cos` at geometric frequencies added to embeddings; doesn't extrapolate. 以几何频率加到嵌入上的 `sin/cos`；不能外推。 |
| RoPE | "Rotary embeddings" / "旋转嵌入" | Rotate Q, K by position-dependent angle; dot product encodes relative distance. 按位置相关角度旋转 Q、K；点积编码相对距离。 |
| ALiBi | "Linear bias trick" / "线性偏置技巧" | Add `-m·|i-j|` to attention scores; no embedding needed, great extrapolation. 向注意力分数添加 `-m·|i-j|`；无需嵌入，出色的外推。 |
| base | "RoPE's knob" / "RoPE 的旋钮" | The frequency scaler in RoPE; increase to extend context at inference. RoPE 中的频率缩放器；增大以在推理时扩展上下文。 |
| NTK-aware | "A RoPE scaling trick" / "RoPE 缩放技巧" | Rescale `base` so high-frequency dims aren't squeezed when context expands. 重新缩放 `base` 使高频维度在上下文扩展时不被挤压。 |
| YaRN | "The fancy one" / "高级的那种" | Per-dimension interpolation+extrapolation that preserves attention entropy. 保留注意力熵的每维度插值+外推。 |
| Extrapolation / 外推 | "Works beyond trained length" / "超过训练长度还能用" | Can the position scheme serve correct output past `max_len` seen in training? 位置方案能否在训练中见过的 `max_len` 之后提供正确的输出？ |

## Daha fazla okumak

- [Vaswani et al. (2017). Attention Is All You Need §3.5](https://arxiv.org/abs/1706.03762) orijinal sinusoidal.
  Vaswani 等人(2017)  原始正弦编码──

- [Su et al. (2021). RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/abs/2104.09864) RoPE kağıdı.
  Su 等人(2021)  RoPE 论文。

- [Press, Smith, Lewis (2021). Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation](https://arxiv.org/abs/2108.12409) ALiBi.
  Basın, Smith, Lewis...

- [Peng et al. (2023). YaRN: Efficient Context Window Extension of Large Language Models](https://arxiv.org/abs/2309.00071) RoPE ölçeklendirme.
  Peng 等人(2023)  最先进的 RoPE 缩放──

- [Chen et al. (2023). Extending Context Window of Large Language Models via Positional Interpolation](https://arxiv.org/abs/2306.15595)Meta'nın Llama 2 uzun bağlamlı makalesi.
  Chen 等人(2023)  Meta'nın Llama 2 长上下文论文。

- [Ding et al. (2024). LongRoPE: Extending LLM Context Window Beyond 2 Million Tokens](https://arxiv.org/abs/2402.13753) Phi-3-Long tarafından kullanılan Microsoft yöntemi.
  Ding 等人(2024)  Microsoft'ın yöntemleri, Phi-3-Long tarafından kullanılmıştır.

- [HuggingFace Transformers — `modeling_rope_utils.py`](https://github.com/huggingface/transformers/blob/main/src/transformers/modeling_rope_utils.py) Her RoPE ölçekleme programının üretim derecesi uygulanması.
  HuggingFace Transformers  所有 RoPE 缩放方案的生产级实现──
