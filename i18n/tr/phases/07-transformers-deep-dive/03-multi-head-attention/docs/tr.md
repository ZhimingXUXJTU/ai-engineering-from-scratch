# Çok Başlı Dikkat
# Çok dikkatli olmak

> Bir dikkat başı bir arada bir ilişkiyi öğrenir. Sekiz baş sekiz öğrenir.

> Bir dikkat ilk kez bir ilişki öğrenmek için.

> **【中文解读】**Birçok dikkatli bir modelin aynı zamanda farklı tür ilişkilere odaklanmasına izin vermesi:语法、语义、位置等──GPT-3 96 dikkatli bir başlıktır──理解多头 =理解Transformer's expressive ability──

**Type:** Build | **类型:** 动手
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 7 · 02 (Self-Attention from Scratch) | **前置知识:** 阶段 7 · 02（从零实现自注意力）
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar. Sorunlar.

Tek bir kendi dikkat başı bir dikkat matrisi hesaplar. Bu matris bir tür ilişkiyi yakalar  genellikle eğitim sinyalleri ne olursa olsun kayıpları en aza indirgenir. Verilerinizde konu-ketim anlaşması, eş-referans, uzun mesafeli konuşma ve sentaksik parçalanma varsa, tek bir baş onları tek yumuşak maksimum dağılımına ayırır ve sinyalin yarısını kaybeder.

> 单个自注意头计算一个注意矩阵――这个矩阵捕获一种关系通常是最小化训练信号损失的那种――如果你的数据中的主题一致、共指消解、长程语篇和句法分块纠在一起,单个头会它们模糊成单软max 分布,丢失半信号――

2017 Vaswani makalesinden alınan düzeltme: her biri kendi Q, K, V projeksiyonlarıyla paralel olarak birkaç dikkat fonksiyonu çalıştırır ve çıkışları birleştirir. Her baş daha küçük boyut alt alanında çalışır.`d_model / n_heads`Toplam parametreler aynı kalır.

> 2017 Vaswani 论文的修复方案:并行运行多个注意函数,每个都有自己的Q、K、V 投影,然后拼接输出──每个头在维度为`d_model / n_heads`Genel konular değişmez, performans güçleri artıyor.

Çok başlı dikkat, 2026 gemilerindeki her transformatörün varsayılanıdır. Tek argüman * kaç* başlı ve anahtarların ve değerlerin projeksiyonları paylaşıp paylaşmadığı hakkında (Grouped-Query Attention, Multi-Query Attention, Multi-head Latent Attention).

> Çoğu başlıklı dikkat 2026 yılında her Transformer'ın öntanımlı konumudır. Tek tartışma * kaç* başlık ve anahtar ve değer hakkında olup olmadığını paylaşmakla ilgili.

> **【中文解读】**Tek dikkat başı sadece bir ilişki modeli öğrenebilir, ancak doğal dilde birçok ilişki vardır.

## Konsepten bir şey.

![Multi-head attention splits, attends, concatenates](../assets/multi-head-attention.svg)

**Split.**Al .`X`şekli ile`(N, d_model)`- Her biri şekilinde Q, K, V'ye kadar.`(N, d_model)`- Yeniden değiştir .`(N, n_heads, d_head)`nerede`d_head = d_model / n_heads`- Transposer `(n_heads, N, d_head)`- Evet .

> **拆分。**取形为 `(N, d_model)``X`◊ Projecteze `(N, d_model)`Bu, bir şey değil.`(N, n_heads, d_head)`, içinden `d_head = d_model / n_heads`                                                                                                                                                                                                                                                              `(n_heads, N, d_head)`- Evet.

**Attend in parallel.**Her başın içinde bir nokta üretici dikkatini çalıştır.`(N, d_head)`Başlar yerleşimlerin farklı alt alanlarında çalışır ve dikkat hesaplama sırasında hiç konuşmazlar.

> **并行计算注意力。**Her başta çalışmak için yoğunlaşın.`(N, d_head)`❖ Başlıca yerleşik farklı alanlarda işlem, dikkat hesaplama sırasında birbirleriyle iletişim

**Concatenate and project.**Yüklü başları geri dön .`(N, d_model)`ve öğrenilmiş bir çıkış matrisine çarpır `W_o`şekli ile`(d_model, d_model)`- Evet .`W_o`Başların karışması.

> **拼接并投影。**Başını yeniden toplayacağım.`(N, d_model)`Öğrenme çıkış matrajı`W_o`, şekli `(d_model, d_model)`- Evet.`W_o`Karışık bir yer.

**Why it works.**Her baş, temsil bütçesi için diğerleriyle rekabet etmeden uzmanlaşabilmektedir. 2019  2024'ten kalma araştırma çalışmaları farklı baş rollerini göstermektedir: pozisyonel başlar, önceki simgeye katılan başlar, kopya başları, isimli varlık başları, indüksiyon başları (konekst içi öğrenmenin temeli olan).

> **为什么有效。**Her başlık, diğer başlıklarla mücadele etmeden özel hale gelebilir. Bütçe. 2019-2024 yıllarındaki araştırma çalışmaları farklı başlık rollerini gösterdi: konum başlığı; önceki bir simgeye odaklanmak başlığı; kopya başlığı; isimlendirilmiş varlık başlığı; dönüş başlığı; bu, yukarı aşağı edebiyat eğitiminin temelidir.

> **【中文解读】**Üç adım adım: Bölünmüştür (özgürlüğü)→ Katılımcılık (özgürlüğü)→ Her başın dikkat çekmesi için dikkat çekmesi için dikkat çekmesi için dikkat çekmesi için dikkat çekmesi için dikkat çekmesi için dikkat çekmesi için dikkat çekmesi için dikkat çekmesi için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için dikkat çekmek için.

> **【拓展：GQA 在 Llama 3 中的实际应用】**Llama 3 70B 64 sorgu başlığı kullanırken sadece 8 KV başlığı kullanırken, KV 缓存 sızdırılması 8 katına kadar azalır. Bu, düşünce sırasında büyük miktarda kayıp tasarruf ederken, neredeyse model kalitesini kaybetmez. GQA, 2024-2026 yıllarında açık kaynaklı modellerin bir göstergesi haline gelmiştir.

**The 2026 lineage of variations:**

> **2026 年的变体谱系：**

| Variant | Q heads / Q 头数 | K/V heads / K/V 头数 | Used by / 使用者 |
|---------|---------|-----------|---------|
| Multi-head (MHA) / 多头 | N | N | GPT-2, BERT, T5 |
| Multi-query (MQA) / 多查询 | N | 1 | PaLM, Falcon |
| Grouped-query (GQA) / 分组查询 | N | G (e.g. N/8) | Llama 2 70B, Llama 3+, Qwen 2+, Mistral |
| Multi-head latent (MLA) / 多头潜在 | N | compressed to low-rank / 压缩为低秩 | DeepSeek-V2, V3 |

GQA, modern varsayılan bir yöntemdir çünkü KV-cache belleğini `N/G`MLA, K/V'yi gizli bir alanlara sıkıştırarak daha ileri gider, sonra hesaplama zamanında geri projeksine geçerek  FLOP'ler maliyetini artırır, çok daha fazla bellek tasarruf eder.

> GQA modern bir tercih, çünkü KV 缓存内存 azalır.`N/G`倍, aynı zamanda neredeyse tam kaliteyi korumakla birlikte MLA  K/V ı daha fazla gizli alanına sıkıştırarak, sonra hesaplama sırasında projektör geri dönerken  FLOP harcamakla daha fazla kayda tasarruf eder.

## Yapın.
```figure
multihead-split
```

## Yapın

### Adım 1: Tek başlı dikkatten ayrılan başlar.

Alın .`SelfAttention`2. dersten sonra bir çift bölünme/konkat ile sarın.`code/main.py`bir numpy uygulaması için; mantık:

> 取第 02 课的 `SelfAttention`, , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , , ,`code/main.py`中的 numpy 实现;逻辑如下:

```python
def split_heads(X, n_heads):
    n, d = X.shape
    d_head = d // n_heads
    return X.reshape(n, n_heads, d_head).transpose(1, 0, 2)  # (heads, n, d_head)

def combine_heads(H):
    h, n, d_head = H.shape
    return H.transpose(1, 0, 2).reshape(n, h * d_head)
```

Birini yeniden şekillendirip birini transpose et.`nn.MultiheadAttention`- Evet .

> Bir kez yeniden şekillendirilmiş ve bir kez dönüştürülmüş.`nn.MultiheadAttention`Alt katın yapması...

> **【中文解读】** `split_heads`和 `combine_heads`                                                                                                                                                                                                                                                              

### Adım 2: Başlık odaklı bir nokta- ürünü dikkatini çalıştırın.

Her baş kendi parçalarını alır. Dikkat bir matmul olur.

> Her baş kendi Q 、K 、V 切片ları elde eder.

```python
def mha_forward(X, W_q, W_k, W_v, W_o, n_heads):
    Q = X @ W_q
    K = X @ W_k
    V = X @ W_v
    Qh = split_heads(Q, n_heads)         # (heads, n, d_head)
    Kh = split_heads(K, n_heads)
    Vh = split_heads(V, n_heads)
    scores = Qh @ Kh.transpose(0, 2, 1) / np.sqrt(Qh.shape[-1])
    weights = softmax(scores, axis=-1)
    out = weights @ Vh                    # (heads, n, d_head)
    concat = combine_heads(out)
    return concat @ W_o, weights
```

Gerçek donanımlı .`Qh @ Kh.transpose(...)`Bir tane .`bmm`GPU ' nun görebileceği tek bir parça şekil .`(heads, N, d_head) × (heads, d_head, N) -> (heads, N, N)`Başları eklemek ücretsizdir.

> Gerçek bir cihazda,`Qh @ Kh.transpose(...)`Bir kere oldu.`bmm`◊GPU 看到的是形状为 `(heads, N, d_head) × (heads, d_head, N) -> (heads, N, N)`Tek seferlik birim oranı çarpı­tıcılık.

### Adım 3: Gruplandırılmış Sorgu Dikkat Variansı .

Sadece anahtar ve değer projeleri değişir.`n_heads`gruplar; K ve V get `n_kv_heads < n_heads`gruplar ve tekrar tekrarlar:

> Sadece anahtar ve değerlerin projeksiyonu değişir.`n_heads`个组;K 和 V 有 `n_kv_heads < n_heads`个组,并被重复以匹配:

```python
def gqa_project(X, W, n_kv_heads, n_heads):
    kv = split_heads(X @ W, n_kv_heads)       # (kv_heads, n, d_head)
    repeat = n_heads // n_kv_heads
    return np.repeat(kv, repeat, axis=0)      # (n_heads, n, d_head)
```

Bu hafıza tasarrufu yapar çünkü sadece`n_kv_heads`KV önbelleğinde kopyalar var, değil `n_heads`Llama 3 70B 64 sorgu başlığı ile 8 KV başlığı  8× önbelleği küçültücü kullanıyor.

> Bu, bir süreliğine kaydedildi çünkü sadece`n_kv_heads`份副本 KV 缓存中'da mevcuttur, değil `n_heads`份──Llama 3 70B 64 sorgu başlığı ve 8 KV başlığı 8 倍lik depo eksikliği kullanmak──

> **【拓展：MQA/GQA 在推理中的内存节约】**KV 缓存的大小与 KV 头数成正比──Llama 3 70B 64 sorgu başlığı kullanır, ancak sadece 8 KV 头, KV 缓存 压缩8倍──128K 上下文 için, bu, GB 显存数 tasarruf anlamına gelir──Bu büyük model uzun下文推理的关键优化GQA 几乎不损质,但显著降低推理成本──

### Adım 4: Her başın ne öğrendiklerini araştırın.

MHA'yı 4 başlı kısa cümle ile çalıştır.`(N, N)`Farklı başlar farklı yapıları seçerken rastgele başlangıç yaparak göreceksiniz. Bu kısmen sinyal, kısmen de alt uzaylarda dönüm simetrisidir.

> Kısa bir cümleyle 4 başı kullanın.`(N, N)`dikkatle çalıştırmak. Farklı başlıklar da farklı yapılara sahip olduğunu görürsün.

## Çerçeveyi kullanın.

PyTorch'de tek satırlı versiyon:

> PyTorch 中,一行版本:

```python
import torch.nn as nn

mha = nn.MultiheadAttention(embed_dim=512, num_heads=8, batch_first=True)
```

PyTorch 2.5+'den itibaren GQA:

> GQA(PyTorch 2.5+):

```python
from torch.nn.functional import scaled_dot_product_attention

# scaled_dot_product_attention auto-dispatches Flash Attention on CUDA.
# For GQA, pass Q of shape (B, n_heads, N, d_head) and K,V of shape
# (B, n_kv_heads, N, d_head). PyTorch handles the repeat.
out = scaled_dot_product_attention(q, k, v, is_causal=True, enable_gqa=True)
```

**How many heads?**2026'daki üretim modellerinden gelen basamak kuralları:

> **多少个头？**2026 yıl üretim modeli deneyimi kuralları:

| Model size / 模型大小 | d_model | n_heads | d_head |
|------------|---------|---------|--------|
| Small (~125M) / 小型 | 768 | 12 | 64 |
| Base (~350M) / 基础 | 1024 | 16 | 64 |
| Large (~1B) / 大型 | 2048 | 16 | 128 |
| Frontier (~70B) / 前沿 | 8192 | 64 | 128 |

`d_head`Bu, bir başın "görme" yeteneğinin birimidir. 32'nin altına düşer ve başlar ölçekleme faktörüne karşı savaşmaya başlar.`sqrt(d_head)`256'den fazla bir iş yaparsanız "çok küçük uzman" avantajını kaybedeceksiniz.

> `d_head`                                                                                                                                                                                                                                                              `sqrt(d_head)`冲突; 256 时, sen "niden çok küçük uzman" yararlarını kaybetti.

## İndirin . Ürünler .

Bakın .`outputs/skill-mha-configurator.md`. Bu beceri, yeni bir transformatör için baş sayısını, kv baş sayısını ve projeksiyon stratejisini, parametre bütçesi, dizi uzunluğu ve dağıtım hedefi vererek önerir.

> 参见 `outputs/skill-mha-configurator.md` Bu beceriler yeni Transformer                                                                                                                                                                                                                                                           

## Egzersizler.

1. **Easy / 简单。**MHA ' dan alın .`code/main.py`ve değişim .`n_heads`1 ila 16 arasında `d_model=64`Bir katmanlı modelin kaybını sentetik kopyalama işinde planlayın.
   Çekil`code/main.py`Orta MHA, içinde `d_model=64`Kesin koşullarda`n_heads`1'den 16'ya dönüştürülmüştür. Bir yapay kopyalanma görevi üzerinde küçük tek katmanlı modellerin kaybedilmesi.

2. **Medium / 中等。**MQA uygulaması (tüm sorgu başlıkları arasında paylaşılan bir KV başlığı). Parametre sayısının ne kadar düşeceğini ölçmek vs. tam MHA. N=2048 için sonuçta KV-cache boyutunun ne kadar azaldığını hesaplayın.
   实现 MQA(1 KV 头在所有查询头间共享) 测量与完整 MHA相比参数下降多少──计算在 N=2048 推理时 KV 缓存大小缩减多少──

3. **Hard / 困难。**Çok başlı Latent Dikkatin küçük bir versiyonunu uygulayın: K, V'yi bir sıralama ile sıkıştırın.`r`- KV'de saklanıp dikkat zamanı ile sıkıştır.`r`Kaş belleği tam MHA'nın 1/8'inden aşağı geçirken kalite doğrulama işleminin 1 bitinin içinde kalır mı?
   实现迷你版的多头潜伏注意:将 K,V 压缩为秩 `r`KV 缓存中存储隐向量,在注意计算时解压――在什么`r`值下缓存内存 MHA'nın tam 1/8'üne düşerken, aynı zamanda kalite de 1 bit içinde kalır.

## Anahtar Şartlar .

| Term | What people say / 人们怎么说 | What it actually means / 实际含义 |
|------|------------------------------|----------------------------------|
| Head / 头 | "A single attention circuit" / "一个注意力电路" | One Q/K/V projection of dimension `d_head = d_model / n_heads` with its own attention matrix. 维度为 `d_head = d_model / n_heads` 的一个 Q/K/V 投影，有自己的注意力矩阵。 |
| d_head | "Head dimension" / "头维度" | Per-head hidden width; almost always 64 or 128 in production. 每个头的隐藏宽度；生产中几乎总是 64 或 128。 |
| Split / combine / 拆分/合并 | "Reshape tricks" / "reshape 技巧" | `(N, d_model) ↔ (n_heads, N, d_head)` reshape+transpose around attention. 围绕注意力的 `(N, d_model) ↔ (n_heads, N, d_head)` reshape+transpose。 |
| W_o | "Output projection" / "输出投影" | `(d_model, d_model)` matrix applied after concatenating heads; where heads mix. 拼接头后应用的 `(d_model, d_model)` 矩阵；头混合的地方。 |
| MQA | "One KV head" / "一个 KV 头" | Multi-Query Attention: single shared K/V projection. Smallest KV cache, some quality loss. 多查询注意力：单个共享的 K/V 投影。最小 KV 缓存，有一些质量损失。 |
| GQA | "The default since Llama 2" / "Llama 2 之后的默认" | Grouped-Query Attention with `n_kv_heads < n_heads`; repeats to match Q. 分组查询注意力，`n_kv_heads < n_heads`；重复以匹配 Q。 |
| MLA | "DeepSeek's trick" / "DeepSeek 的技巧" | Multi-head Latent Attention: K,V compressed to low-rank latent, decompressed at attend time. 多头潜在注意力：K,V 压缩为低秩隐向量，在注意力计算时解压。 |
| Induction head / 归纳头 | "The circuit behind in-context learning" / "上下文学习背后的电路" | A pair of heads that detect previous occurrences and copy what followed them. 一对检测先前出现模式并复制后续内容的头。 |

## Daha fazla okumak

- [Vaswani et al. (2017). Attention Is All You Need §3.2.2](https://arxiv.org/abs/1706.03762) orijinal çok başlı özellik.
  Vaswani 等人(2017)  原始多头规范──

- [Shazeer (2019). Fast Transformer Decoding: One Write-Head is All You Need](https://arxiv.org/abs/1911.02150) MQA kağıdı.
  Shazeer(2019)  MQA 论文。

- [Ainslie et al. (2023). GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](https://arxiv.org/abs/2305.13245) eğitimden sonra MHA'yı GQA'ya nasıl dönüştürülecek.
  Ainslie 等人(2023) 訓練後 MHA 转换为 GQA──

- [DeepSeek-AI (2024). DeepSeek-V2 Technical Report](https://arxiv.org/abs/2405.04434) MLA ve neden cache belleğinde MHA/GQA'yı yendi.
  DeepSeek-AI(2024)  MLA 及为何在缓存内存上击败 MHA/GQA──

- [Olsson et al. (2022). In-context Learning and Induction Heads](https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html) Başların ne yaptığını mekanizma olarak gör.
  Olsson 等人 (2022)  Başlıca gerçek fonksiyonların mekanizma analizi

> **【拓展：Induction Heads 与上下文学习】**Antropik bir araştırma, Transformer'ın üst aşağı edebi öğrenme yeteneğini (Transformer'ın üst aşağı edebi öğrenme yeteneği) esas olarak "indüksiyon başı" olarak adlandırılan bir dikkat başı tarafından gerçekleştirildi.
