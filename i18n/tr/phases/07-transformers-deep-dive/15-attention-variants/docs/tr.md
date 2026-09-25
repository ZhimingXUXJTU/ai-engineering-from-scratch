# Dikkat Variantları  Çekilme Penceresi, Çekilme, Farklılık  Dikkat Değişimi  Çekilme Penceresi 稀疏、差分注意

> Tam dikkat bir döngüdür. Her simge her simgeyi görür ve hafıza bedelini öder. Dört varians döngünün şeklini eğer ve maliyetin yarısını geri alır.

> **【中文解读】**標準注意力 O(n^2) 複雜度太貴──滑動窗口注意力(Mistral) 稀疏注意力、差分注意力 is a method of reducing complexity──

**Type:** Hands-on | **类型:** 动手
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head), Phase 7 · 12 (KV Cache / Flash Attention) | **前置知识:** Phase 7 · 02 (Self-Attention), Phase 7 · 03 (Multi-Head), Phase 7 · 12 (KV Cache / Flash Attention)
**Time:** ~60 minutes | **时间:** ~60 分钟

## Sorunlar. Sorunlar.

Tam ilgi maliyetleri `O(N²)`hafıza ve `O(N²)`128K bağlamlı bir Llama 3 70B için, katman başına 16 milyar dikkat girişi çarpı 80 katman.`O(N²)`Aktifleştirme hafızası ama aritmetik maliyetini değiştirmez  her token hala diğer tokenlere katılır.

> Tüm dikkat, dizilerin uzunluğunda olan bellek ve hesaplama maliyetlerine odaklanır.`O(N²)`❖ 128K için ❖ Llama 3 70B, bu her kat 160 milyar dikkat ❖ 80 katı ❖ Flash dikkat ❖`O(N²)` her token                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          

Üç çeşit sınıfı dikkat matrisinin topolojisini değiştirir:

> Üç tür değişken dikkat matçının kendiliğinden genişletilmiş yapısını değiştirmiştir:

1. **Sliding window attention (SWA).**Her token komşuların sabit bir penceresine hizmet eder, tam öncü değil.`O(N · W)`nerede`W`Gemma 2/3, Mistral 7B'nin ilk katmanları, Phi-3-Long.
   Çeviri:**滑动窗口注意力 (SWA)。**Her token, tam önüne değil, sabit pencerenin komşu alanına odaklanır.`O(N · W)`, içinden `W`Bu da bir tane.
2. **Sparse / block attention.**Sadece seçilmiş çiftler `(i, j)`Longformer, BigBird, OpenAI nadir transformatör.
   Çeviri:**稀疏/块注意力。**Sadece seçilmiş .`(i, j)`Önemli değerlere; kalanı sıfır ağırlığa zorlanmaktadır.
3. **Differential attention.**İki dikkat haritasını ayrı Q / K projeksiyonlarıyla hesaplayın, birini diğerinden çıkarın. İlk birkaç tokene ağırlığı kanayan " dikkat sink" ı öldürür. Microsoft'un DIFF Transformer (2024).
   Çeviri:**差分注意力。**İzle bağımsız Q/K 投影计算两个注意力图,将一个从另一个减去――消除将权重汇聚到前几个代币的"注意力汇聚"现象――Microsoft's DIFF Transformer(2024)。

Bu özellikler birlikte var. 2026 sınır modeli genellikle onları karıştırır: çoğu katman SWA-1024, her beşde birisi küresel tam dikkat, ve bir avuç geri almayı temizleyen farklılık başlarıdır. Gemma 3'ün 5:1 SWA-global oranı mevcut derslik standartıdır.

> 2026 yılının ön kenar modelinde genellikle karışık kullanılır: Çoğu kat SWA-1024, her beş kat tüm düzeyde tüm dikkat, az sayıda temizleme kontrolünün farkı vardır.

> **【中文解读】**Üç çeşit dikkat karmaşıklığını azaltma yöntemleri: 1) 滑窗口(SWA)  sadece yerel komşu bölgeye odaklanmak, O(N*W) 复杂liği; 2) 稀疏/块注意力 yalnızca hesaplanmış belirlenmiş bir token için; 3) 差分注意力两组 Q/K dikkat çekimi azaltmak, "注意力汇聚" fenomeni ortadan kaldırmak.

## Konsepten bir şey.

### Çekilme Penceresi Dikkat (SWA)

Her sorgu pozisyonunda `i`Sadece pozisyonlara katılır `[i - W, i]`(kötü nedenlik SWA) veya `[i - W/2, i + W/2]`Pencerenin dışındaki simgeler çıkıyor .`-inf`Not matrisinde.

>  konum `i`Her sorunun bir sonucu var .`[i - W, i]`(因果 SWA) veya `[i - W/2, i + W/2]`(双向) 域内的位置──窗外的符号 在分数矩阵中获得`-inf`- Evet.

```
full causal:           sliding window (W=4):
positions 0-7          positions 0-7, W=4
    0 1 2 3 4 5 6 7        0 1 2 3 4 5 6 7
0 | x                0 |  x
1 | x x              1 |  x x
2 | x x x            2 |  x x x
3 | x x x x          3 |  x x x x
4 | x x x x x        4 |    x x x x
5 | x x x x x x      5 |      x x x x
6 | x x x x x x x    6 |        x x x x
7 | x x x x x x x x  7 |          x x x x
```

- Evet .`N = 8192`ve `W = 1024`, puan matrisi, 1024 × 8192 sıfır dışı sıralara sahiptir  8 × azaltma beklentisi.

> - Evet .`N = 8192`和 `W = 1024`% 1024 × 8192 ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′ ′     ′                                                                                                                             

**KV cache shrinks with SWA.**Sadece sonuncusu .`W`Gemma-3-ish yapılandırması (1024 penceresi, 128K bağlamı) için, KV önbelleği 128× düşer.

> **KV 缓存随 SWA 缩小。**Her kat K ve V'nin sonunu tutmak zorundadır.`W`个 token──对类 Gemma-3 的配置(1024 窗口,128K 上下文),KV 缓存减少 128 倍──

**Quality cost.**SWA-yalnızca transformatörler uzun mesafeli geri alım ile mücadele eder. Düzeltme: SWA katmanlarını tam dikkat katmanlarıyla aralaştırın. Gemma 3 5:1 SWA: global kullanır. Mistral 7B, bilgi'nin üst üste geçiş pencereleri üzerinden "geri akıyor" olduğu bir nedensel-SWA yığınını kullanır.`W`ve sonra`L`Modelin katılabileceği katmanlar `L × W`- Tokenleri geri ver.

> **质量代价。**SWA Transformer: SWA 層と全注意層交替使用──Gemma 3 使用 5:1 的 SWA:全局比例──Mistral 7B 使用因果 SWA 堆,信息通过重叠窗口"向前流动"每层将有效感受野扩展`W`- Evet .`L`层后模型 `L × W`- Bu bir işaret.

### İzleme / Blok Et

Bir seç .`N × N`Zaman öncesi bir kısıtlama modeli.

> 预先选择  Önceden Seçim`N × N`Bu tip bir yapı.

- **Local + strided (OpenAI sparse transformer).**Sonunculara kadar bak .`W`Tokenler artı her `stride`Yerel ve uzun mesafeli çekimleri yakalar.`O(N · sqrt(N))`Bilgisayar.
  Çeviri:**局部 + 步进（OpenAI 稀疏 Transformer）。**关注最后 `W`个标志加上之前每隔 `stride`- Evet.`O(N · sqrt(N))`Bu sayede, yerel ve uzun mesafe bilgileri elde ediliyor.
- **Longformer / BigBird.**Yerel pencere + küçük bir küresel token kümesi (örneğin `[CLS]`) herkesin katıldığı ve herkesin katıldığı + rastgele-sparse bağlantılar.
  Çeviri:**Longformer / BigBird。**局部窗口 + 少量全局 token(如 `[CLS]`) ile tüm simgeler 双向关注 + 随机稀疏连接―― deney aynı kalite altında aşağıdaki yazıyı 2 倍 genişletmeyi göstermiştir.
- **Native Sparse Attention (DeepSeek, 2025).**Hangi blokları öğrenin `(Q, K)`- Flaş Dikkatle uyumlu.
  Çeviri:**原生稀疏注意力（DeepSeek，2025）。**Öğrenmek ne?`(Q, K)`块重要;在内核级跳过零块──与FlashAttention 兼容──

Sparse dikkat çekirdek mühendisliği hikâyesidir. Matematik basit (score matrisi maskeli) ve kazanç SRAM'a asla sıfır girişleri yüklemeden gelir. FlashAttention-3 ve 2026 FlexAttention API PyTorch'de özel ilk sınıf kıt desenleri yapar.

> 稀疏注意力 (稀疏注意力) bir nüvehin hikayesi. Matematik çok basit. 稀疏注意力 (稀疏注意力) ise SRAM'a yüklenmiş olan 稀疏条目 (零条目) 'ten gelir.

> **【拓展：滑动窗口的信息传递机制】**滑窗注意力 görünüşe göre sadece yerel bilgileri yakalayabilir, ancak çok katlı bir toplama yoluyla, bilgi daha uzak bir yere "geçebilir". W 窗の L 層注意力, L×W olarak etkin olarak algılanır. Örneğin W=1024、L=32 modelinin 32K token olarak algılanması için geçerlidir. Mistral 7B, bu özelliği O(N*W) 計算 karmaşıklığını sürdürmekle birlikte gerçekleştirmek için kullanıyor.

### Farklı Dikkat (DIFF Transformer, 2024)

Düzenli dikkat "hatırlama" sorunu vardır: softmax her satırı 1'e toplamaya zorlar, bu nedenle belirli bir şeye katılmak istemeyen tokenler ilk token'da (veya ilk birkaç token'da) ağırlık atarlar. Bu gerçek içeriğe gitmesi gereken kapasiteyi çalır.

> 標準注意力有"注意力汇聚" sorunu:softmax 强制每行总和为1, bu yüzden belirli bir içeriğe odaklanmak istemediğimden, ağırlığı ilk token'a (or birkaç) 倾倒会) 权重倾倒会.

Farklı dikkat bunu hesaplama yoluyla düzeltir .**two**dikkat haritaları ve çıkarma:

> 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分注意力 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差分 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差 差  差 差 差 差 差 差 差 差 差 差 差 差 差  差 差 差 差 差 差 差 差 差 差   差 差 差   差 差      差 差 差    差 差 差 差 差   差 差    差**两个**Dikkat et, bu sorunu düzelt.

```
A1 = softmax(Q1 K1^T / √d)
A2 = softmax(Q2 K2^T / √d)
DiffAttn = (A1 - λ · A2) V
```

nerede`λ`A1 gerçek içerik ağırlıklarını yakalar; A2 sinkini yakalar. Kısıtlama sinkini iptal eder, ağırlığı ilgili simgeler için yeniden tahsis eder.

> İçlerinden `λ`A1 捕获真内容权重; A2 捕获汇聚――相减消除汇聚,权重再分配相关代币――

Raporlanan sonuçlar (Microsoft 2024): 510% daha düşük karmaşıklık, aynı eğitimli uzunlukta 1.52× daha uzun etkili bağlam, daha keskin iğne-haystack geri alımı.

> 報告結果(Microsoft 2024):困惑度降低 5-10%,同训长度下有效上下文长度增加1.5-2倍,针-in-haystack 检索更精确──

> **【中文解读】**差分注意力创新之处: standart dikkat çekmek 归归化导致"注意力汇聚" (acute attention gathering) 不相关的代币 焦重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重重

> **【拓展：Gemma 3 的混合注意力策略】**Google'ın Gemma 3 kullanımı 5:1'lik kaydırma penceresi ile genel dikkat oranı 5 katlı yerel dikkat oranı için 1 katlı genel dikkat oranı Bu hem uzun boyutlu bir uzaktan bağlantı sağlayan, hem de hesaplama maliyetini önemli ölçüde azaltan bir yapısal yapısal yapısal yapısal yapısal yapısal yapısal bir yapısal yapısal yapısal yapısal bir yapısal yapısal yapısal yapısal bir yapısal yapısal yapısal yapısal bir yapısal yapısal yapısal yapısal bir yapısal yapısal yapısal yapısal bir yapısal yapısal yapısal yapısal yapısal bir yapısal yapısal yapısal yapısal yapısal bir yapısal yapısal yapısal yapısal yapısal bir yapısal yapısal yapısal yapısal yapısal yapısal bir yapısal yapısal yapısal bir yapısal yapısal yapısal yapısal yapısal yapısal bir yapısal yapısal yapısal yapısal yapısal yapısal yapısal bir yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal bir yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal bir yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal yapısal

### Çeşitli karşılaştırmalar

| Variant | Compute | KV cache | Quality vs full | Production use |
|---------|---------|----------|-----------------|----------------|
| 变体 | 计算量 | KV 缓存 | 相对全注意力的质量 | 生产使用 |
| Full attention | O(N²) | O(N) per layer | baseline | every model's default layer |
| 全注意力 | O(N²) | 每层 O(N) | 基线 | 每个模型的默认层 |
| SWA (window 1024) | O(N·W) | O(W) per layer | -0.1 ppl, good with global layers | Gemma 2/3, Phi-3-Long |
| 滑动窗口 (窗口 1024) | O(N·W) | 每层 O(W) | -0.1 ppl，配合全局层效果好 | Gemma 2/3, Phi-3-Long |
| Local + strided sparse | O(N·√N) | mixed | similar to SWA | OpenAI sparse transformer, Longformer |
| 局部+步进稀疏 | O(N·√N) | 混合 | 类似 SWA | OpenAI 稀疏 Transformer, Longformer |
| BigBird (local + global + random) | O(N) approx | mixed | matches full at 2× context | early long-context BERT |
| BigBird (局部+全局+随机) | O(N) 近似 | 混合 | 2 倍上下文下匹配全注意力 | 早期长上下文 BERT |
| Native Sparse (DeepSeek-V3.2) | O(N · active fraction) | O(N) | within 0.05 ppl | DeepSeek-V3.2, 2025 |
| 原生稀疏 (DeepSeek-V3.2) | O(N · 活跃比例) | O(N) | 0.05 ppl 以内 | DeepSeek-V3.2, 2025 |
| Differential | O(2·N²) | O(2N) | -5 to -10% ppl | DIFF Transformer, early 2026 models |
| 差分 | O(2·N²) | O(2N) | 困惑度降低 5-10% | DIFF Transformer, 2026 早期模型 |

## Yapın.
```figure
gqa-kv-sharing
```

## Yapın

Bakın .`code/main.py`Oyuncak dizisinde tam, SWA, lokal+strided ve farklı dikkatini yan yana gösteren bir sebep maskası karşılaştırıcısı uyguluyoruz.

> 参见 `code/main.py`                                                                                                                                                                                                                                                              

### Adım 1: Tam sebep maskası (Başlamalı)

```python
def causal_mask(n):
    return [[0.0 if j <= i else float("-inf") for j in range(n)] for i in range(n)]
```

Ders 07'den baseline. Alt üçgen; diyagonalın üzerinde sıfır ağırlık.

> 第07 课的基线──下三角;对角线上权重为零──

### Adım 2: kaydırıcı pencerenin nedensel maskası

```python
def swa_mask(n, window):
    M = [[float("-inf")] * n for _ in range(n)]
    for i in range(n):
        lo = max(0, i - window + 1)
        for j in range(lo, i + 1):
            M[i][j] = 0.0
    return M
```

Bir parametreden  `window`- Evet .`window >= n`Bu yüzden, tüm nedensel dikkatini geri kazanırsın.`window = 1`, her simge sadece kendine hizmet eder.

> Bir parametre`window`- Evet.`window >= n`时,恢复为全因果注意力──当 `window = 1`Her bir şey kendi kendine odaklanmalı.

### Adım 3: Yerel + adımlı keskin maske

```python
def strided_mask(n, window, stride):
    M = [[float("-inf")] * n for _ in range(n)]
    for i in range(n):
        lo = max(0, i - window + 1)
        for j in range(lo, i + 1):
            M[i][j] = 0.0
        for j in range(0, i + 1, stride):
            M[i][j] = 0.0
    return M
```

Sıkı yerel pencere artı her `stride`-th simgesi dizinin başlangıcına geri döner.

> 密集局部窗加上序列开端每隔`stride`个标志──感受野随着层次数以对数步长的增长──

### Dördüncü adım: Farklı ilgi

```python
def diff_attention(Q1, K1, Q2, K2, V, lam):
    A1 = softmax_causal(Q1 @ K1.T / sqrt_d)
    A2 = softmax_causal(Q2 @ K2.T / sqrt_d)
    return (A1 - lam * A2) @ V
```

İki dikkat geçiyor, öğrenilmiş bir karıştırma katı ile çıkarıyoruz.

> 双重注意计算, öğrenilen karışık系数leri kullanarak çarpı azaltmak.

### Adım 5: KV önbelleği boyutları

Önbelleğin katman boyutunu `N = 131072`SWA ve nadir çeşitler 10 100 × düşer. Farklı çiftler.

> 打印 `N = 131072`时每种变体的缓存大小──SWA 和稀疏变体减少10-100倍──差分变体翻倍──要有意识地管理你的内存开销──

## Çerçeveyi kullanın.

2026 üretim modelleri:

> 2026 yıl üretim modeli:

```python
from transformers import AutoModelForCausalLM
# Gemma 3 mixes SWA (window=1024) and global layers at 5:1.
model = AutoModelForCausalLM.from_pretrained("google/gemma-3-27b-it")
# print(model.config.sliding_window, model.config.layer_types)
```

PyTorch 2.5+' deki FlexAttention, bir maske fonksiyonunu kabul eder:

> PyTorch 2.5+ 中的 FlexAttention  accept掩码函数:

```python
from torch.nn.attention.flex_attention import flex_attention, create_block_mask

def swa_pattern(b, h, q_idx, kv_idx):
    return (q_idx - kv_idx < 1024) & (q_idx >= kv_idx)

mask = create_block_mask(swa_pattern, B=batch, H=heads, Q_LEN=n, KV_LEN=n)
out = flex_attention(q, k, v, block_mask=mask)
```

Bu, özel bir Triton çekirdeğine birleştirir. Ortak kalıplar için FlashAttention-3 hızının %10'unun içinde ve maske işlevi Python çağrılabilir.

> Bu, Triton 内核 olarak tercüme edilir. Normal model için, hız FlashAttention-3'in %10'unda ve gizleme işlevi Python'un ayarlanabilir bir nesnesi olarak kullanılır.

**When to pick each:**

> **何时选择每种变体：**

- **Pure full attention** ~ 16K bağlamına kadar her katman veya geri alma kalitesi en önemli olduğunda.
  Çeviri:**纯全注意力** Her katman yaklaşık 16K yukarı aşağıya kadar kullanılır, veya kontrol kalitesi önemli bir sahne.
- **SWA + global mix** uzun bağlam (> 32K), eğitim ve sonucu hafıza bağlı.
  Çeviri:**SWA + 全局混合** 长上下文(>32K), eğitim ve düşünce 內存约束──32K 以上 2026 yıl默认配置──
- **Sparse block attention** özel çekirdek, özel bir desen. Uzman iş yükleri için rezerve (kaynaklama, ses).
  Çeviri:**稀疏块注意力** 自定义内核,自定义模式──专用于特殊工作负载(检索、音频)──
- **Differential attention** dikkat sink kontaminasyonunun zarar verdiği herhangi bir iş yükü (uzun bağlamlı RAG, çiy yığınındaki iğne).
  Çeviri:**差分注意力** dikkat力汇聚污染有害的任何工作负载(长上下文 RAG、針-in-haystack)

## İndirin . Ürünler .

Bakın .`outputs/skill-attention-variant-picker.md`. Bu beceri, hedef bağlam uzunluğu, geri alma talepleri ve eğitim/sürekli hesaplama profili göz önüne alındığında yeni bir model için bir dikkat topolojisini seçer.

> 参见 `outputs/skill-attention-variant-picker.md` Bu beceri  hedef üzerinde aşağıdaki yazının uzunluğuna göre  kontrol gereksinimleri ve eğitim/ önerme hesaplama konumu, yeni model için dikkatli seçim yapılması 

## Egzersizler.

1. **Easy.**Çık .`code/main.py`SWA ' yı kontrol edin .`window=4`Son 4 simge dışında her şeyi sıfırlıyor.`window=n`Tam sebepli dikkatini bit-ident olarak yeniden üretir.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ Test`window=4`SWA'nın her seferinde son 4 token dışında tüm içeriği verilecek .`window=n`能逐位复现全因果注意力──
2. **Medium.** ile nedensel SWA uygulamak`window=1024`Lesson 07'ün baş taşı üzerinde. Tinyshakespeare'da 1000 adımlar için eğitim.
   Çin Çince: 七 课毕业项目上实现`window=1024`SWA.Normally, the average rate of return is the average rate of return.
3. **Hard.**Gemma-3 tarzında 5:1 katman karışımı (5 SWA, 1 global) baş taşı modelinde uygulayın.
   Çinçe çevirme: Birim proje modelinde gerçekleştirilen Klas Gemma-3'ün 5:1 katlı karışımı ((5 katlı SWA、1 katlı tüm aşama) ⋅
4. **Hard.**Öğrenciyle farklı ilgi göstermek`λ`Bir sentetik geri alım görevinde çalışın (bir iğne, 2.000 dikkat dağıtıcı).
   Çinçe Çevirisi: gerçekleştirmek her başta öğrenme vardır`λ`Bu nedenle, bir inceleme işleminin yapılması için yapılan bir inceleme işleminin yapılması için yapılan bir inceleme işleminin yapılması için yapılan bir inceleme işleminin yapılması için yapılan bir inceleme işleminin yapılması için yapılan bir inceleme işleminin yapılması için yapılan bir inceleme işleminin yapılması için yapılan bir inceleme işleminin yapılması için yapılan bir inceleme işleminin yapılması için yapılan bir inceleme işleminin yapılması için yapılan bir inceleme işleminin yapılması için yapılan bir inceleme işleminin yapılması için yapılan bir inceleme işleminin yapılması için yapılan bir inceleme işleminin yapılması için yapılan bir inceleme yapılması için yapılan bir inceleme yapılması için yapılan bir inceleme yapılması için yapılan bir inceleme yapılması için yapılan bir inceleme yapılması için yapılan bir inceleme yapılması için yapılan bir inceleme yapılması için yapılan bir inceleme yapılması için yapılan bir inceleme yapılması için yapılan bir inceleme yapılması için yapılan bir inceleme yapılması için yapılan bir düzenleme yapılması için yapılan bir düzenleme yapıldı.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| Sliding window attention (SWA) | "Local attention" | Each query attends to its last `W` tokens; KV cache shrinks to `O(W)`. |
| 滑动窗口注意力 (SWA) | "局部注意力" | 每个查询关注其最后 `W` 个 token；KV 缓存缩小到 `O(W)`。 |
| Effective receptive field | "How far back the model sees" | In an `L`-layer SWA stack with window `W`, up to `L × W` tokens. |
| 有效感受野 | "模型能看多远" | 在 `L` 层 SWA 堆栈中，窗口 `W`，最多 `L × W` 个 token。 |
| Longformer / BigBird | "Local + global + random" | Sparse patterns with a few always-attending global tokens; early long-context approach. |
| Longformer / BigBird | "局部+全局+随机" | 带少量始终关注的全局 token 的稀疏模式；早期长上下文方案。 |
| Native Sparse Attention | "DeepSeek's kernel trick" | Learn block-level sparsity; skip zero blocks at the kernel level while keeping quality. |
| 原生稀疏注意力 | "DeepSeek 的内核技巧" | 学习块级稀疏性；在内核级别跳过零块同时保持质量。 |
| Differential attention | "Two maps, one subtracts" | DIFF Transformer: subtract a learned `λ` times a second attention map from the first to cancel attention sinks. |
| 差分注意力 | "两个图，一个相减" | DIFF Transformer：用第一个注意力图减去学习 `λ` 倍的第二个注意力图，消除注意力汇聚。 |
| Attention sink | "Weight bleeds to token 0" | Softmax normalization forces rows to sum to 1; uninformative queries dump weight on position 0. |
| 注意力汇聚 | "权重流向 token 0" | Softmax 归一化迫使每行总和为 1；无信息查询将权重倾倒到位置 0。 |
| FlexAttention | "Mask-as-Python" | PyTorch 2.5+ API that compiles arbitrary mask functions into FlashAttention-shape kernels. |
| FlexAttention | "掩码即 Python" | PyTorch 2.5+ API，将任意掩码函数编译为 FlashAttention 形式的内核。 |
| Layer type mix | "5:1 SWA-to-global" | Interleave sparse and full attention layers in a stack to keep quality at lower memory. |
| 层类型混合 | "5:1 SWA 与全局" | 在堆栈中交替使用稀疏和全注意力层，以较低内存保持质量。 |

## Daha fazla okumak

- [Beltagy, Peters, Cohan (2020). Longformer: The Long-Document Transformer](https://arxiv.org/abs/2004.05150) Kanonik kaydırma penceresi + global-token kağıdı.
  Çeviri:Düzenli, klasik 论文, klasik 滑动窗口 + 全局 方案
- [Zaheer et al. (2020). Big Bird: Transformers for Longer Sequences](https://arxiv.org/abs/2007.14062)Yerel + küresel + rastgele.
  Çeviri:Büyük Kuşlar,局部 + 全局 + 随机模式。
- [Child et al. (2019). Generating Long Sequences with Sparse Transformers](https://arxiv.org/abs/1904.10509) OpenAI'nin yerel + adımlı kalıbı.
  Çeviri:Düzgün Transformer,局部+步进模式──
- [Gemma Team (2024). Gemma 2: Improving Open Language Models at a Practical Size](https://arxiv.org/abs/2408.00118) 1:1 SWA:global mix.
  中文翻译:Gemma 2 论文,1:1 SWA 与全局混合──
- [Gemma Team (2025). Gemma 3 technical report](https://arxiv.org/abs/2503.19786) 5.1 karışımı ile penceresi=1024 bu şimdi ders kitabı varsayılan.
  Çeviri:Gemma 3 技术报告,5:1 混合,窗口=1024,现已成为教科书默认──
- [Ye et al. (2024). Differential Transformer](https://arxiv.org/abs/2410.05258) DIFF Transformer kağıdı.
  Çeviri:DIFF Transformer
- [Yuan et al. (2025). Native Sparse Attention](https://arxiv.org/abs/2502.11089)DeepSeek-V3.2'nin öğrendiği parsiplik dikkatini.
  Çeviri:DepSeek-V3.2
- [PyTorch — FlexAttention blog and docs](https://pytorch.org/blog/flexattention/) Use It'deki maske-as-call-able model için API referansı.
  Python FlexAttention 文档,掩码即可调用模式的 API 参考──
