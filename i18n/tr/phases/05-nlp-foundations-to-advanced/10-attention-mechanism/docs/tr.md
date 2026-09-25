# Dikkat Mekanizması  Yürümüşlük  Dikkat Mekanizması  Transformer'ın çekirdek açısı

> Dekodör, sıkıştırılmış bir özetle göz kırpmayı bırakır ve tüm kaynağa bakmaya başlar.
> Çözümcü artık resmini görmeye başladı, tüm kaynağa bakmaya başladı.

> **【中文解读】**dikkat mekanizması, modelin giriş ile ilgili bölümlere odaklanmasını sağlar.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 09 (Sequence-to-Sequence Models) | **前置知识:** Phase 5 · 09（序列到序列模型）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Sorunlar. Sorunlar.

Ders 09 ölçülü bir başarısızlıkla sona erdi. Oyuncak kopya görevinde eğitilmiş bir GRU kodlayıcı-dekodör, uzunluk 5'de %89 doğruluktan neredeyse şans uzunluğuna 80'e kadar gidiyor. Sebep yapısal, eğitim hatası değil: kodlayıcı topladığı her bilgi, sabit boyutlu bir gizli durumda yer almalı ve dekodör başka hiçbir şey görmez.

> 9. Sınıf: Bir ölçülebilir başarısızlıkla sona erdi. Oyuncak kopyalama görevinde eğitim gören GRU kodlayıcı- çözücü, uzunlukta 5'de %89 doğruluk oranı, uzunlukta 80'de ise hızla yaklaştı.

Bahdanau, Cho ve Bengio 2014 yılında üç satırlı bir düzeltme yayınladı. Dekodere yalnızca son kodlayıcı durumunu vermek yerine, her kodlayıcı durumunu koruyun.`i`Bu ağırlıklı ortalama bağlamdır ve her dekodör adımını değiştirir.

> Bahdanau、Cho 和 Bengio 2014 yılında bir üçgen revivi yayınladı.`i`"Bu artış ortalaması yukarı aşağıda, her çözücü adımında değişir.

Bu fikir tümüyle aynı. Transformatörler onu genişletti. Kendine dikkatle tek bir dizine uyguladı. Çoklu başlı dikkat paralel olarak çalıştı. Ama 2014 versiyonu zaten şişek boynunu kırmıştı ve bir kez sahip olduktan sonra, transformatörlerin çekirdeği konsept değil mühendisliktir.

> Bu tüm fikirlerdir. Transformer'ın genişletilmesi için dikkat çekildi. Tek bir diziye uygulanması için dikkat çekildi.

## Konsepten bir şey.

> **【中文解读】**Bu bölümde temel kavramlar ve teoriler hakkında konuşuluyor. Bu kavramları öğrenmek, sonradan gerçekleştirilme önemi, aynı zamanda, görüşmeler ve mühendislik uygulamalarında yüksek sıklıkta yapılan incelemelerin bilgi noktasıdır.

![Bahdanau attention: decoder queries all encoder states](../assets/attention.svg)

Her dekoder adımında `t`- ...

> Her bir çözücü adımında.`t`- ...

1. Önceki dekodörün gizli durumunu kullan `s_{t-1}`bir **query**- Evet .
2. Her kodlayıcıya karşı puan verin .`h_1, ..., h_T`- Kodlayıcı pozisyonu başına bir skalar.
3. Dikkat ağırlıkları almak için puanları yumuşat `α_{t,1}, ..., α_{t,T}`Bu toplam 1'e kadar.
4. Bağlantı vektörü `c_t = Σ α_{t,i} * h_i`- Kodlayıcı durumlarının ağırlıklı ortalaması.
5. Dekodör alır `c_t`+ önceki çıkış token, bir sonraki token üretir.
   1. kullanın                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            `s_{t-1}` olarak**查询（Query）**- Evet.
   2. Her kodlayıcıyla gizli durumunu ayarlayın.`h_1, ..., h_T`打分── her kodlayıcı bir etiketleme yerleştirir.
   3. Parçalanmaya yumuşaklık göstermek için dikkat çekmek için .`α_{t,1}, ..., α_{t,T}`, toplamı 1
   4. Ün aşağıdaki `c_t = Σ α_{t,i} * h_i`❖ Kodlayıcı durumunun artış oranı
   5. Çekilme cihazı`c_t`Bir önceki çıkış simgesi, bir sonraki simgesi oluşturmak için.

Decikleyici "Je" i "I"ye çevirmek zorunda kaldığında, kodlayıcı durumunu "Je" yüksek ve diğerlerini düşük ağırlıklandırır. "Hayır" gerektiğinde, "pas" yüksek ağırlıklandırır. Konekst vektörü her adımı yeniden şekillendirir.

> ∀============================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================================

> **【拓展：大语言模型的工程实践】**GPT'den ChatGPT'e kadar, NLP alanında "her görev bir model eğitimi" ile "her görevyi çözmek için bir model" biçiminin değişiminden geçti.

> **【拓展：RAG 与企业知识库】**检索增强生成(RAG) şu anki işletme AI 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用 应用  应用 应用 应用    应用     应用   应用        应用    应用       应用          应用        应用      应用          应用                                                                                                       

> **【拓展：NLP 的多语言挑战】**Küresel olarak 7000'den fazla dil vardır, ancak NLP çalışmaları çoğunlukla İngilizce ve az sayıda dil üzerinde yoğunlaşmaktadır.

## Şekiller (herkesi ısıran şey)

İlk kez dikkat uygulaması yanlış gittiği yer burası.

> Bu her dikkat ilk kez başarılan bir hata.

| Thing / 对象 | Shape / 形状 | Notes / 说明 |
|-------|-------|-------|
| Encoder hidden states `H` / 编码器隐藏状态 `H` | `(T_enc, d_h)` | If BiLSTM, `d_h = 2 * d_hidden` / 如果是 BiLSTM，`d_h = 2 * d_hidden` |
| Decoder hidden state `s_{t-1}` / 解码器隐藏状态 | `(d_s,)` | One vector / 一个向量 |
| Attention score `e_{t,i}` / 注意力分数 | scalar / 标量 | One per encoder position / 每个编码器位置一个 |
| Attention weight `α_{t,i}` / 注意力权重 | scalar / 标量 | After softmax over all `i` / 对所有 `i` 做 softmax 后 |
| Context vector `c_t` / 上下文向量 | `(d_h,)` | Same shape as an encoder state / 与编码器状态相同形状 |

**Bahdanau (additive) score.** `e_{t,i} = v_α^T * tanh(W_a * s_{t-1} + U_a * h_i)`- Evet .

> **Bahdanau（加性）分数。** `e_{t,i} = v_α^T * tanh(W_a * s_{t-1} + U_a * h_i)`- Evet.

- `s_{t-1}`şekli var .`(d_s,)`- Evet .`h_i`şekli var .`(d_h,)`- Evet .
- `W_a`şekli var .`(d_attn, d_s)`- Evet .`U_a`şekli var .`(d_attn, d_h)`- Evet .
- Tanh ' ın içinde olan toplamlarının şekli var .`(d_attn,)`- Evet .
- `v_α`şekli var .`(d_attn,)`İç ürün ile`v_α`Bir merdiven olarak çöküyor.**This is what `v_α` does.**Bu sihir değil, dikkat-dim vektörünü bir skalar skoruna dönüştüren bir projeksiyon.
  - `s_{t-1}`形状为 `(d_s,)`- Evet .`h_i`形状为 `(d_h,)`- Evet.
  - `W_a`形状为 `(d_attn, d_s)`- Evet.`U_a`形状为 `(d_attn, d_h)`- Evet.
  - içi ve şekli`(d_attn,)`- Evet.
  - `v_α`形状为 `(d_attn,)`❖ `v_α`İçin kısaltılmış.**这就是 `v_α` 的作用。**Bu sihirli bir şey değil. Bu dikkat ölçüsünün veektörünün bir proje olarak gösterilen bir proje.

**Luong (multiplicative) score.**Üç çeşit:

> **Luong（乘性）分数。**Üç değişim:

- `dot`- Evet .`e_{t,i} = s_t^T * h_i`- Gerekli .`d_s == d_h`- Kodlamanız iki yönlüse atlayın.
  `dot`- ...`e_{t,i} = s_t^T * h_i`❖ talep`d_s == d_h`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ 
- `general`- Evet .`e_{t,i} = s_t^T * W * h_i`- Evet .`W`şekli`(d_s, d_h)`- Aynı nükleerlik kısıtlamasını kaldırır.
  `general`- ...`e_{t,i} = s_t^T * W * h_i`- Evet .`W`形状为 `(d_s, d_h)`❖ Değiştirmek ❖
- `concat`Bahdanau şekli: ilk ikisi daha ucuz olduğundan nadiren kullanılır.
  `concat`:本质上是Bahdanau 形式──由于前两种更便宜,很少使用──

**One Bahdanau / Luong gotcha worth naming.**Bahdanau kullanıyor `s_{t-1}`(bu sözcük oluşturmadan önce * dekodör durumunda). Luong kullanır `s_t`Bir kağıt seçip, konvansiyonuna bağlı kalın.

> **一个值得注意的 Bahdanau / Luong 陷阱。**Bahdanau 使用 `s_{t-1}`(生成当前词*之前*的解码器状态) ――Long 使用 `s_t`Bu nedenle, bu konularda, bir makaleyi seçerek, bir makaleyi seçerek, bir makaleyi seçerek, bir makaleyi seçerek, bir makaleyi seçerek, bir makaleyi seçerek, bir makaleyi seçerek, bir makaleyi seçerek, bir makaleyi seçerek, bir makaleyi seçerek, bir makaleyi seçerek, bir makaleyi seçerek, bir makaleyi seçerek, bir makaleyi seçerek, bir makaleyi seçerek, bir makaleyi seçerek, bir makaleyi seçerek, bir makaleyi seçerek, bir makaleyi oluşturarak, bir makaleyi oluşturarak, bir makaleyi oluşturarak, bir makaleyi oluşturarak, bir makaleyi oluşturarak, bir makaleyi oluşturarak, bir makale oluşturarak, bir makale oluşturarak, bir makale oluşturarak, bir makale oluşturarak, bir makale oluşturarak, bir makale oluşturarak, bir makale oluşturarak, bir makale oluşturarak, bir makale oluşturur.

## Yapın.

> **【中文解读】**Bu bölüm kodla sıfırdan gerçekleştirilen çekirdek algoritmasıdır. Bu "sıfırdan" yöntem çerçevenin arkasındaki prensipleri anlama yardımcı olur.
```figure
attention-heatmap
```

## Yapın

### Adım 1: katkı (Bahdanau) dikkat

```python
import numpy as np


def additive_attention(decoder_state, encoder_states, W_a, U_a, v_a):
    projected_dec = W_a @ decoder_state
    projected_enc = encoder_states @ U_a.T
    combined = np.tanh(projected_enc + projected_dec)
    scores = combined @ v_a
    weights = softmax(scores)
    context = weights @ encoder_states
    return context, weights


def softmax(x):
    x = x - np.max(x)
    e = np.exp(x)
    return e / e.sum()
```

Şekillere bak.`encoder_states`şekli var .`(T_enc, d_h)`- Evet .`projected_enc`şekli var .`(T_enc, d_attn)`- Evet .`projected_dec`şekli var .`(d_attn,)`ve yayınlar. `combined`şekli var .`(T_enc, d_attn)`- Evet .`scores`şekli var .`(T_enc,)`- Evet .`weights`şekli var .`(T_enc,)`- Evet .`context`şekli var .`(d_h,)`- Gönder.

> Yukarıdaki tabloya bakıp şeklini kontrol et.`encoder_states`形状为 `(T_enc, d_h)`- Evet.`projected_enc`形状为 `(T_enc, d_attn)`- Evet.`projected_dec`形状为 `(d_attn,)`Ve yayıldı.`combined`形状为 `(T_enc, d_attn)`- Evet.`scores`形状为 `(T_enc,)`- Evet.`weights`形状为 `(T_enc,)`- Evet.`context`形状为 `(d_h,)`- Tamam, tamam.

### Adım 2: Luong nokta ve genel

```python
def dot_attention(decoder_state, encoder_states):
    scores = encoder_states @ decoder_state
    weights = softmax(scores)
    return weights @ encoder_states, weights


def general_attention(decoder_state, encoder_states, W):
    projected = W.T @ decoder_state
    scores = encoder_states @ projected
    weights = softmax(scores)
    return weights @ encoder_states, weights
```

Bu yüzden Luong'un kağıdı geldi.

> Bu Luong'un yazısının anlamı. Çoğu görevde aynı doğruluk oranı, kod daha azdır.

### Adım 3: İşlenen sayısal örnek

Üç kodlayıcı durum (kayın, uydu, mat) ve ilk ile en çok uyumlu bir dekoder durumu verildiğinde, dikkat dağılımı 0 pozisyonuna yoğunlaşır. Eğer dekoder durumu sonuncuyla uyumlu hale gelirse, dikkat 2. pozisyonu taşıyor.

> 给定三个编码器状态 ((大致是"cat"、"sat"、"mat") 和一个与第一个最齐齐的解码器状态,注意分布集中在位置0――如果解码器状态移动到最后的齐,注意力移动到位置2――下文向量随其追踪――

```python
H = np.array([
    [1.0, 0.0, 0.2],
    [0.5, 0.5, 0.1],
    [0.1, 0.9, 0.3],
])

s_close_to_cat = np.array([0.9, 0.1, 0.2])
ctx, w = dot_attention(s_close_to_cat, H)
print("weights:", w.round(3))
```

```
weights: [0.464 0.305 0.231]
```

İlk satır kazanır. Sonra dekodör durumunu üçüncü kodör durumuna yakınlaştır ve ağırlıkların kaymasını izle.

> İlk sırada bir başarı var. Sonra bir üçüncü kodlama durumuna yaklaşır.

### Dördüncü adım: Bu neden transformatörlere giden köprüdür ?

Yukarıdaki dili Q/K/V'ye çevirin:

> 将上的语言翻译为 Q/K/V:

- **Query**= dekodör durumu `s_{t-1}`
  **查询（Query）**= 解码器 durumu `s_{t-1}`
- **Key**= kodlayıcı durumları (neye karşı puan verdiğimiz)
  **键（Key）**= 编码器状态(我们用来打分的对象)
- **Value**= kodlayıcı durumları (koştukları ve toplamladığımızı)
  **值（Value）**= 编码器状态(我们用来加权和的对象)

Klasik dikkat, anahtarlar ve değerler aynı şeydir. Kendine dikkat onları ayırır: K ve V için farklı öğrenilen projeksiyonlarla bir diziyi kendine karşı soruyabilirsiniz. Çoklu başlı dikkat, farklı öğrenilen projeksiyonlarla paralel olarak çalışır. Transformatörler tüm aşamayı birçok kez yığar ve RNN'leri düşürür.

> Klasik dikkat içinde, anahtar ve değer aynı şeydir. Kendine dikkat ederek onları ayırır: farklı öğrenim projelerini kullanarak bir diziyi K ve V olarak sorarsın.

Matematik aynı. Şekiller aynı. Bahdanau dikkatinden ölçekli nokta ürün dikkatine pedagogik atlama çoğunlukla notasyondur.

> Matematik aynıdır. Şekili aynıdır. Bahdanau dikkat çekme noktasından küçültme noktasına dikkat çekme dersinde atlama, en çok simgelerden oluşur.

> **【中文解读】**Bu bölümde, PyTorch, HuggingFace gibi olgun çerçeveler nasıl kullanılacağını gösterir.

> **【拓展：Prompt Engineering 与 LLM 应用】**Hızlı Mühendislik NLP mühendislerinin temel beceri haline geldi. Zero-shot'tan birkaç-shot'a, Chain-of-Thought'tan ReAct'e kadar, farklı fikir stratejileri farklı durumlarda uygulanmaktadır.

## Çerçeveyi kullanın.

PyTorch ve TensorFlow dikkatini doğrudan gönderiyorlar.

> PyTorch ve TensorFlow  doğrudan dikkat sağlıyor

```python
import torch
import torch.nn as nn

mha = nn.MultiheadAttention(embed_dim=128, num_heads=8, batch_first=True)
query = torch.randn(2, 5, 128)
key = torch.randn(2, 10, 128)
value = torch.randn(2, 10, 128)

output, weights = mha(query, key, value)
print(output.shape, weights.shape)
```

```
torch.Size([2, 5, 128]) torch.Size([2, 5, 10]
```

Bu bir transformatör dikkat katmanı. 5 pozisyondan oluşan sorgu parti, 10 pozisyondan oluşan anahtar/değer parti, her biri 128 boyutlu, 8 baş.`output`Bu yeni bağlamlı sorulardır. `weights`Görüştürebileceğiniz 5x10 uyumlu matris.

> İşte bir Transformer dikkat seviyesi. 5 pozisyon, anahtar/değer bölümü, 10 pozisyon, her 128 维,8 头.`output`Yeni bir arama yapıyorum.`weights`5x10'un tam bir düzeni var.

### Klasik ilgi hala önemli olduğunda

- Tek başlı, tek katlı, RNN tabanlı versiyon her kavramı görünür kılar.
  Öğretim: Tek başlı, tek katlı, RNN'ye dayalı bir sürüm
- Transformatörlerin uyumsuz olduğu cihaz üzerindeki dizi görevleri.
  Transformer 放不下设备端序列任务。
- Bahdanau'nun toplantısını bilmeden yanlış okuyacaksınız.
  2014-2017 yıllarındaki herhangi bir makale.
- MT'de ince tanelerli uyum analizi. Çiğ dikkat ağırlıkları, transformatör modellerinde bile yorumlanabilirlik aracıdır ve bunları okumak ne olduklarını bilmeyi gerektirir.
  机器翻译中的细粒度对齐分析──原始注意权重甚至在变压器模型上也是可解释性工具,阅读它们需要知道它们是什么──

### Dikkat ağırlığı açıklama tuzağı

Dikkat ağırlıkları yorumlanabilir görünüyor. Bir pozisyonda bir kişiye toplamda bir ağırlıklardır; onları çizmek mümkündür; yüksek "bunu izle" anlamına gelir.

> dikkat çekimi, açıklanabilir görünüyor. Bunlar 1'in ve bir konum arasındaki bir çekimdir.

Bunlar göründüğü kadar yorumlanabilir değildir. Jain ve Wallace (2019) dikkat dağılımlarının bazı görevler için model tahminlerini değiştirmeden keyfi alternatiflerle değiştirilmesi ve değiştirilmesi gerektiğini gösterdi.

> Bunlar görünüşe göre açıklanamaz. Jane ve Wallace (2019) dikkat dağılımının belirli görevlerin model tahminini değiştirmeden, istedikleri yerine değiştirilebileceğini ve değiştirilebileceğini göstermektedir.

> **【中文解读】**Bu bölümde modellerin kullanılabilir ürünler için nasıl dağıtılacağı üzerinde yoğunlaşmaktadır.

## İndirin . Ürünler .

- Kaydet .`outputs/prompt-attention-shapes.md`- ...

> 保存为 `outputs/prompt-attention-shapes.md`- ...

```markdown
---
name: attention-shapes
description: Debug shape bugs in attention implementations.
phase: 5
lesson: 10
---

Given a broken attention implementation, you identify the shape mismatch. Output:

1. Which matrix has the wrong shape. Name the tensor.
2. What its shape should be, derived from (d_s, d_h, d_attn, T_enc, T_dec, batch_size).
3. One-line fix. Transpose, reshape, or project.
4. A test to catch regressions. Typically: assert `output.shape == (batch, T_dec, d_h)` and `weights.shape == (batch, T_dec, T_enc)` and `weights.sum(dim=-1) close to 1`.

Refuse to recommend fixes that silently broadcast. Broadcast-hiding bugs surface later as silent accuracy degradation, the worst kind of attention bug.

For Bahdanau confusion, insist the decoder input is `s_{t-1}` (pre-step state). For Luong, `s_t` (post-step state). For dot-product, flag dimension mismatch between query and key as the most common first-time error.
```

> **【中文解读】**练习题按照易/中级/难三度递进;;建议至少完成中级题,Hard级适合深入研究或面试准备;;

## Egzersizler.

1. **Easy.**Uygulama`softmax`Kodlayıcıdaki tokenleri kapatmak için dikkat ağırlığı sıfır.
   **简单。** gerçekleştirmek `softmax`掩码, kodlayıcıda doldurma simgesi dikkat çekimi 0 ⋅ üzerinde test
2. **Medium.**Luong ' a çok kişilik dikkat katın .`general`- Şekil.`d_h`- ...`n_heads`Tek başlı olayın daha önceki uygulamalarınızla uyumlu olduğunu kontrol edin.
   **中等。**Luong için`general`形式添加多头注意力──将 `d_h`Bölüm için`n_heads`组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组, 组
3. **Hard.**9. ders'ten bahdanau dikkatini oyuncak kopyası görevi için GRU kodlayıcı-dekodörünü eğit.
   **困难。**9. Sınıfın oyuncak kopyalama görevinde eğitim Bahdanau ile dikkatli GRU kodlayıcı- çözücü.

> **【中文解读】**术语表中的"İnsanların ne dediği" vs "Gerçekten ne anlama geldiği" 区分日常口语和精确技术含义──在团队协作中,统一术语定义可以避免大量沟通误解──

## Anahtar Şartlar .

| Term / 术语 | What people say / 人们常说的 | What it actually means / 实际含义 |
|------|-----------------|-----------------------|
| Attention（注意力） | Looking at things / 看东西 | Weighted average of a value sequence, weights computed from a query-key similarity. / 值序列的加权平均，权重从查询-键相似度计算。 |
| Query, Key, Value（查询、键、值） | QKV | Three projections: Q asks, K is what to match, V is what to return. / 三个投影：Q 询问，K 是要匹配的，V 是要返回的。 |
| Additive attention（加性注意力） | Bahdanau | Feed-forward score: `v^T tanh(W q + U k)`. / 前馈分数：`v^T tanh(W q + U k)`。 |
| Multiplicative attention（乘性注意力） | Luong dot / general | Score is `q^T k` or `q^T W k`. Cheaper, same accuracy on most tasks. / 分数是 `q^T k` 或 `q^T W k`。更便宜，大多数任务上相同准确率。 |
| Alignment matrix（对齐矩阵） | The pretty picture / 那张漂亮的图 | Attention weights as a `(T_dec, T_enc)` grid. Read it to see what the model attended to. / 注意力权重作为 `(T_dec, T_enc)` 网格。阅读它看模型关注了什么。 |

> **【中文解读】**延伸阅读, derinlemesine öğrenme için yüksek kaliteli kaynaklar sağladı. Bu makaleler ve dersler, derinlemesine anlama ihtiyacı olan okuyuculara uygun olarak bu alanın klasik referanslarıdır.

## Daha fazla okumak

- [Bahdanau, Cho, Bengio (2014). Neural Machine Translation by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473)- Gazete.
- [Luong, Pham, Manning (2015). Effective Approaches to Attention-based Neural Machine Translation](https://arxiv.org/abs/1508.04025) üç puan variansı ve karşılaştırmaları. / 三种分数变体及其比较──
- [Jain and Wallace (2019). Attention is not Explanation](https://arxiv.org/abs/1902.10186) yorumlanabilirlik uyarısı. / 可解释性警示──
- [Dive into Deep Learning — Bahdanau Attention](https://d2l.ai/chapter_attention-mechanisms-and-transformers/bahdanau-attention.html)PyTorch'la yürüyüşe geçebilir.
