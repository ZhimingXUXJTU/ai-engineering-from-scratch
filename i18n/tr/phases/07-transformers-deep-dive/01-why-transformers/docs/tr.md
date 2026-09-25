# Neden Transformers  RNN'lerle Sorunlar
# Transformer  RNN'in sorunu nedir ?

> RNN'ler bir seferde birer tokeni işliyor. Transformerler tüm tokeni bir seferde işliyor. Bu tek mimari bahis 2017'den sonra derin öğrenimdeki her ölçekleme eğriğini değiştirdi.

> RNN 个别处理代币――Transformer 一次性处理所有代币―― Bu yapı 2017 yılından sonra derin öğrenimdeki her bir genişleme eğilimi değiştirdi.

> **【中文解读】**RNN'de üç ölümcül sorun var: yürüyemez, uzun süreli bir şekilde kaybolur, sabit bir şekilde kalır.

**Type:** Learn | **类型:** 学习
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 3 (Deep Learning Core), Phase 5 · 09 (Sequence-to-Sequence), Phase 5 · 10 (Attention Mechanism) | **前置知识:** 阶段 3（深度学习基础），阶段 5 · 09（序列到序列），阶段 5 · 10（注意力机制）
**Time:** ~45 minutes | **时间:** ~45 分钟

## Öğrenme hedefleri

- Tekrarlanan sinir ağlarının (RNN) üç ölümcül zayıflığını anlayın
  Çeviri Neural Networks'in üç ölümcül zayıf noktasını anlamak
- Seryal derinliğin neden GPU eğitim süresini belirlediğini açıklayın, işlem sayısını değil.
  解释为什么串行深度(而不是操作数) GPU 训练时间的决定
- RNN vs. Transformer karmaşıklığını sekans modelileme görevlerinde karşılaştırın
  RNN ile Transformer'ın dizaynı oluşturma görevindeki karmaşıklığı karşılaştır
- RNN'lerin veya devlet uzay modelleri hala tercih edilebileceği senaryoları tanımlamak
  识别 RNN 或状态空间模型仍然优越场景
- Yerelden küresel dikkatine indüktif önyargıyı fark et
  認識局部性'den tüm局注意の归纳偏好轉移

## Sorunlar. Sorunlar.

2017'den önce, gezegen üzerindeki her en son sekans modeli  dil, çeviri, konuşma  bir geri dönüştürücü sinir ağıydı. LSTM ve GRU'lar yarım on yıl boyunca ImageNet eşdeğer çeviri referansları kazandı.

> 2017 yılına kadar, dünya çapında her en gelişmiş dizi modeli  dil、翻译、语音 hepsi döngüsel sinir ağları。LSTM 和 GRU ise ImageNet'in 级ye eşdeğer olan 翻訳基准测试'da  5 yıl boyunca  adı verilen                                                                                                                                                                                                                              

Üç ölümcül zayıflıkları vardı.`t+1`Gizli bir durumun belirtileri için gerekli .`t`1.024 tokenlik bir dizi, bir GPU'da 1.024 seri adım anlamına gelir.

> Üç ölümcül zayıf noktası var.`t+1`Token ' den gelmek gerekiyor .`t`1.024 token'ın bir diziyi oluşturan bir işlemci, 1.024 adet bir dizi adım atmak için çalışır.

> **【中文解读】**İlk ölümcül zayıflık: 串行计算──RNN 序列处理每个代币, GPU'nun 串行计算能力──完全无法利用的序列计算能力──训练时间与序列长度线性增长, GPU 时代的巨大的浪费──

Kayıp gradientler, 50 token geriye gelen bilginin zaten 50 doğrusal olmayan birimle sıkıştırıldığını gösterir. Gated recurrent units (LSTM, GRU) kırıklığı yumuşatır ama asla ortadan kaldırmaz. Uzun mesafeli bağımlılıklar  "Geçen yaz Kyoto'ya giden bir uçakta okuduğum kitap..."  rutin olarak başarısız oldu.

> 梯度消失  50 token  önceki bilgiler 50 線性変化によって圧縮され, çoğu zaman ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒ ⇒  ⇒ ⇒    ⇒ ⇒   ⇒ ⇒ ⇒         ⇒      ⇒      ⇒      ⇒                                                                                               

> **【中文解读】**İkinci ölümcül zayıflık: Düzeni ortadan kaldırmak. 50 katlı olmayan değişimden sonra, uzak yerlerde bilgi neredeyse tamamen kayboldu.

Sıkı genişliğin gizli durumları, kodlayıcı, kaynakın 5 token veya 500 olması önemli değil; şişe boynuzunun aynı şekli vardır.

> Sıkı genişliğin gizli durumu, kodlayıcı çözücü herhangi bir içeriği görmeden önce tüm kaynak dizisini bir vektor olarak sıkıştırır.

> **【中文解读】**Üçüncü ölümcül zayıflık: sabit genişlik şişe. Kodlayıcı tüm kaynak dizisini sabit uzunlukta bir vektörde sıkıştırmalı. Transformatörün kendi kendine dikkat etmesi, her konumdaki diğer tüm konumlara doğrudan erişilebilmesini sağlayarak bu şişeyi tamamen ortadan kaldırıyor.

2017'de yayınlanan "Eğer İhtiyacınız varsa Dikkat" makalesinde radikal bir şey önerildi: Tekrarlanmayı tamamen bırakın. Her pozisyonun diğer pozisyonlara paralel olarak dikkat etmesine izin verin.

> 2017 yılında yayınlanan "Eğer İhtiyacınız varsa Dikkat" makalesinde, bir teşvikçi önerme önerildi: döngüyü tamamen bırakın.

Sonuç 2026 yılına kadar her modalite hakimdir. Dil (GPT-5, Claude 4, Llama 4), görme (ViT, DINOv2, SAM 3), ses (Sippeder), biyoloji (AlphaFold 3), robotik (RT-2). Aynı blok, farklı girişler.

> 2026 yılına kadar, onun sonuçları her türlü modemayı yönetiyor.

## Konsepten bir şey.

![RNN sequential compute vs Transformer parallel attention](../assets/rnn-vs-transformer.svg)

**Recurrence as a bottleneck.**RNN hesaplar `h_t = f(h_{t-1}, x_t)`Her adım önceki adımdan bağlı.`h_5`Daha önce`h_4`10.000'den fazla paralel çekirdekli modern GPU'larda bu, uzun bir dizide silikonun %99'unu atıyor.

> **循环即瓶颈。**RNN 计算 `h_t = f(h_{t-1}, x_t)`Her adım öncesine bağlı.`h_4`之前计算 `h_5`❖ 10.000+ ve daha fazla çekirdekli modern GPU'ya sahip olmak, bu uzun dizilerin %99'unu boşa harcadı.

> **【中文解读】**Çevre, şişenin özelliğidir: Her zaman aşamasının hesaplanması ön aşamasının sonuçlarına bağlıdır. GPU'nun binlerce paralel işlemden üstün olması, RNN'nin bir dizi bağımlılığı ise GPU'nun sadece çok küçük bir kısmına kalıcıdır.

**Attention as a broadcast.**Kendine dikkat hesaplamaları `output_i = sum_j(a_ij * v_j)`Her çift için .`(i, j)`Tüm N×N dikkat matrisi bir partili matmul'e doldurulur.

> **注意力即广播。**Kendine dikkat et.`(i, j)`计算 `output_i = sum_j(a_ij * v_j)`◊ Tüm N×N dikkat gücü matçları bir kez bir miktar matç çarpma içinde doludur.

**The speedup is not a constant.**Bu `O(N)`seri derinliği ve `O(1)`Serial derinliği. pratikte, transformatörler eşleşen donanımlarda N=512'de 510x daha hızlı çalıştırılır ve boşluk, `O(N²)`Akılda tutulan hafıza duvarı (Flash Attention'ın daha sonra düzelttiği  12. dersi gör).

> **加速不是常数。**- Evet .`O(N)`串行深度与 `O(1)`串行深度 arasındaki fark. Praktede, uyumlu bir donanım üzerinde N=512 时,Transformer Her dönem için eğitim hızı 5-10 kat hızlıdır, ve fark, dikkatle karşılaşana kadar dizilerin uzunluğu arttıkça genişler.`O(N²)`内存壁(Flash Attention 后来修复了它见第 12 课) ⋅

**What transformers cost.**Dikkat hafıza ölçekleri `O(N²)`128K bağlamı için kaydırıcı pencereler, RoPE ekstrapolasyonu, Flash dikkat kapakları veya doğrusal dikkat çeşitleri gerekir.`O(N)`Zaman ve hafıza her iki tarafta; transformatörler zamanla hafıza alışverişinde bulunur ve paralellik yoluyla zamanı geri kazanır.

> **Transformer 的代价。**dikkat çekmek`O(N²)`增长──2K 上下文, sorun yok──128K 上下文,滑窗,RoPE 外推、Flash Attention 分块计算或线性注意力变体──循环在时间和内存上都是`O(N)`Transformer, zamanı kaydetir ve sonra zaman kazanır.

**The inductive bias shift.**RNN'ler yerellik ve yenilikçilik kabul eder. Transformatörler hiçbir şeyi kabul etmez.  her çift dikkat için bir adaydır. Bu nedenle transformatörler iyi eğitilmek için daha fazla veriye ihtiyaç duyarlar, ancak bir kez daha ölçeklendirirler. Chinchilla (2022) bunu resmileştirdi: yeterli token verildiğinde, bir transformatör her zaman eşit parametreler sayısının RNN'ini yener.

> **归纳偏好的转变。**RNN  hipotezi lokalite ve komşulık. Transformer hiçbir hipotezi yapmaz.  Her çift dikkat çekme adayıdır.  Bu yüzden Transformer    daha fazla veriye ihtiyaç duyar. İyi bir eğitim gerektirir, ancak yeterli veriyi elde ettikten sonra daha da genişleyebilir.

> **【中文解读】**归纳偏好转移是变压器成功的关键洞察──RNN 隐式假设"近处的符号更重要",而变压器不做任何假设任何两个位置之间可以建立直接联系──这种弱归纳偏好意味着需要更多的数据训练,但一旦数据充足,扩展性远远超 RNN──

> **【拓展：Chinchilla 缩放定律】**DeepMind'in Chinchilla makalesi ((2022)), modellerin sayısal ve eğitim verileri miktarı oranlarının artışını göstermektedir. Bu neden Llama, GPT-4 ve diğer modellerin milyonlarca seviyesli token eğitimi verilerine ihtiyaç duyduğunu açıklıyor.

## Yapın.
```figure
rnn-vs-parallel
```

## Yapın

Burada sinir ağı yok. Biz çekirdek boğazını sayısal olarak simüle ediyoruz. Böylece dizüstü bilgisayarınızda boşluğu hissedebilirsiniz.

> Burada sinir ağı yok. Numeroloji değerleri kullanarak çekirdekleri simgeledik.

> **【中文解读】**Bu bölüm, saf sayısal değerlerle simgelemekle, dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin dizilerin diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler diziler dizils " diziler diziler diziler diziler diziler diziler diziler dizils " diziler diziler diziler diziler diziler diziler dizils " diziler " diziler " diziler "hesheshesheshesheshesheshesheshesheshesheshesheshesheshesheshesheshesheshesheshesheshesheshesheshesheshesheshesheshesheshesheshesheshesheshesheshesheshesheshesheshesheshesheshesheshesheshes

### Adım 1: Seri derinliğini ölç.

Bakın .`code/main.py`Birini bir dizi ekleme zinciri olarak kodlarız (serial, RNN gibi). Birini paralel bir azaltma olarak kodlarız (ekleyici, dikkat gibi). Aynı matematik, farklı bağımlılık grafiği.

> 参见 `code/main.py`△ Biz iki işlevi oluştururuz. △ Birisi bir diziyi bir ek zincir için kodlayacaktır. △ RNN'ye benzer. △ Birisi de bir diziyi bir diziye benzer olarak kodlayacaktır.

```python
def rnn_style(xs):
    h = 0.0
    for x in xs:
        h = 0.9 * h + x   # can't parallelize: h depends on previous h
    return h

def attention_style(xs):
    return sum(xs) / len(xs)  # every x is independent
```

RNN sürümü O(N) ve tek bir CPU borusu. saf Python'da bile dikkat biçimindeki azaltma uzunluğu ≥ 1000'e geçiyor çünkü Python'un `sum()`C'de uygulanır ve adım başına tercümanlık ödemesi olmadan tekrarlanır.

> RNN ı                                                                                                                                                                                                                                                             `sum()`Bu, C 实现, 代时没有解释器的逐步开销.

### Adım 2: Teorik İşlemleri Sayın .

Her iki algoritma da N ekler. Fark * bağımlılık derinliği *: bir sonraki başlamadan önce kaç işlem sıradan gerçekleşmelidir. RNN derinliği = N. Dikkat derinliği = log(N) bir ağaç azaltma ile veya 1 paralel tarama ile.

> 两种算法都做N 次加法。区别在*深度依赖*:在下一个操作开始之前,必须顺序执行多少操作。RNN深度 = N。注意力深度 = 用树形归约时为 log(N),并行扫描时为 1。决定 GPU 时间是深度,而不是操作数。

### Adım 3: Uzun Sequence'lerde Empirik Ölçekleme

O  N) boşluğu görülebilen bir zamanlama tablosunu yazdırırırız. 2026 Mac dizüstü bilgisayarında, 1000 element altındaki diziler ölçülmek için çok hızlıdır. 100,000'in dizileri temiz bir çizgi tarama gösterir. Bunu 16 384 token transformatörüne 12 katman LSTM eşdeğerle ölçeyin ve eğitim duvar saati neden 2016'da bir engelleyici olduğunu göreceksiniz.

> Biz bir tane O(N) fark görülebilir zaman çizelgesi yazdırıyoruz. 2026 Mac'in not defterinde, 1000'den az elementin dizisi çok hızlı ve ölçülmez. 100.000 elementin dizisi net bir çizgi tarama göstermektedir.

## Çerçeveyi kullanın.

2026'da RNN'i ne zaman seçmeliyiz?

> 2026 yıl何時 yine seçmeli RNN:

> **【中文解读】**Transformer çoğu durumda başarılı olsa da, fakat并非万能──流式推理((((((((((((超长序列(>1M token) ve kenar cihazlar sahnesinde,RNN veya Mamba gibi durum uzay modeli(((((((((2026 yılının eğilimleri karıştırılmış yapılardır(((((Jamba gibi), ikisinin de avantajları vardır.

> **【拓展：Mamba 与状态空间模型】**Mamba(2023) Seçimsel tarama mekanizması yoluyla O(N) karmaşıklıklı bir dizi oluşturmayı gerçekleştirdi, aynı zamanda eğitimini destekledi.

| Situation | Pick / 场景 | 选择 |
|-----------|-------------|------|
| Streaming inference, one token at a time, constant memory | RNN or state-space model (Mamba, RWKV) |
| Very long sequences (>1M tokens) where attention memory explodes | Linear attention, Mamba 2, Hyena |
| Edge device with no matmul accelerator | Depthwise-separable RNN still wins on FLOPs/watt |
| Anything else (training, batched inference, context up to 128K) | Transformer |

Mamba gibi devlet- uzay modelleri (SSM) esasen her ikisinin de en iyisini veren yapılandırılmış parametreleşme ile RNN'lerdir: `O(N)`Sıkıntılı bir şekilde, bir sürü farklı yöntemler kullanılır.

> 状态空间模型 (SSM) Mamba gibi aslında yapısal parametreye sahip RNN,兼具两者的优点:`O(N)`扫描内存,通过选择性扫描实现并行训练――它们恢复了变压器90%的质量,同时具有更好的长上下文扩展性――2026 yılının çoğu ön kenarında bulunan实验室训练混合 SSM+Transformer 模型(如Jamba、Samba) 循环没有灭亡,它是一个组件――

## İndirin . Ürünler .

Bakın .`outputs/skill-architecture-picker.md`. Yetenek, uzunluk, geçiş gücü ve eğitim bütçesi kısıtlamaları göz önünde bulundurularak yeni bir dizi sorunu için bir mimari seçer.

> 参见 `outputs/skill-architecture-picker.md`Bu beceri yeni bir dizi sorununun seçimi yapılandırması, uzunluğu, toplama ve eğitim bütçesi sınırlaması için kullanılmalıdır.

> **【拓展：架构选择决策树】**Gerçek tasarımda, yapı seçimi birçok boyut düşünmelidir: dizi uzunluğu, gecikme gereksinimleri, bellek bütçesi, eğitim veri miktarı, donanım yerleştirme. Çoğu NLP görevleri için, sadece Decoder'e dönüştürücü bir tercihdir. Süper uzun dizi için, Mamba veya karışık yapı düşünün. Kenar kenarında yerleştirilmek için, miktarlı RNN/SSM daha uygun olabilir.

## Egzersizler.

1. **Easy / 简单。**Al .`rnn_style`-`code/main.py`Ve saklı durumların uzunluğu 64 vektörü ile değiştirmek.
   Çekil`code/main.py`Orta `rnn_style`, ölçümün uzunluğu 64'ün gizli durum yönü ile değiştirilmesini sağlar.

2. **Medium / 中等。**Temiz Python'da paralel bir önbellek-sümayı (Hillis-Steele taraması) uygulayın.
   Temiz Python kullanılarak 实现并行前和(Hillis-Steele 扫描) 验证它在长度 1024 上产生与串行扫描相同的数值输出──计算深度──

3. **Hard / 困难。**Dikkat biçimindeki azaltmayı GPU'ya PyTorch'e aktarın.
   Dikkat tarzı 归约移植到 GPU 上的 PyTorch──在序列长度从64扫到65,536 时对两者计时──绘制并解释曲线形──

## Anahtar Şartlar .

| Term | What people say / 术语 | 人们怎么说 | What it actually means / 实际含义 |
|------|----------------------|-----------|----------------------------------|
| Recurrence | "RNNs are sequential" | 循环 (Recurrence) | Computation where step `t` depends on step `t-1`, forcing serial execution along the time axis. 步骤 `t` 依赖于步骤 `t-1` 的计算，强制沿时间轴串行执行。 |
| Serial depth | "How deep the graph is" | 串行深度 (Serial depth) | Longest chain of dependent ops; bounds wall-clock even on infinite hardware. 依赖操作的最长链；即使在无限硬件上也限制了时间开销。 |
| Attention | "Let tokens look at each other" | 注意力 (Attention) | Weighted sum `sum_j a_ij v_j` where `a_ij` comes from a similarity score between positions i and j. 加权求和 `sum_j a_ij v_j`，其中 `a_ij` 来自位置 i 和 j 之间的相似度得分。 |
| Context window | "How much the model sees" | 上下文窗口 (Context window) | Number of positions an attention layer can take as input; quadratic memory cost scales here. 注意力层可作为输入的位置数；二次内存开销在这里缩放。 |
| Inductive bias | "Assumptions baked into the architecture" | 归纳偏好 (Inductive bias) | Prior about what the data looks like; CNNs assume translation invariance, RNNs assume recency. 关于数据外观的先验；CNN 假设平移不变性，RNN 假设邻近性。 |
| State-space model | "RNN with algebra behind it" | 状态空间模型 (State-space model) | Recurrence parameterized for parallel training via structured state-space matrices. 通过结构化状态空间矩阵参数化以实现并行训练的循环。 |
| Quadratic bottleneck | "Why context costs so much" | 二次瓶颈 (Quadratic bottleneck) | Attention memory = `O(N²)` in sequence length; Flash Attention hides the constants, not the scaling. 注意力内存 = 序列长度的 `O(N²)`；Flash Attention 隐藏了常数，而非缩放。 |

## Daha fazla okumak

- [Vaswani et al. (2017). Attention Is All You Need](https://arxiv.org/abs/1706.03762) ana akım NLP'de tekrarlanmayı öldüren makale.
  Vaswani 等人(2017)  终结了主流NLP 中循环的论文──

- [Bahdanau, Cho, Bengio (2014). Neural MT by Jointly Learning to Align and Translate](https://arxiv.org/abs/1409.0473) dikkat doğduğu yer, RNN'ye bağlanmış.
  Bahdanau, Cho, Bengio(2014)  dikkat güç doğduğu yer, RNN 上に追加

- [Hochreiter, Schmidhuber (1997). Long Short-Term Memory](https://www.bioinf.jku.at/publications/older/2604.pdf) Kayıt için orijinal LSTM kağıdı.
  Hochreiter, Schmidhuber(1997)  原始 LSTM 论文,留作记录。

- [Gu, Dao (2023). Mamba: Linear-Time Sequence Modeling with Selective State Spaces](https://arxiv.org/abs/2312.00752) Transformatörlere modern tekrarlayıcı cevap.
  Gu, Dao(2023)  Transformer'ın modern döngü alternatif方案──

> **【拓展："Attention Is All You Need" 的历史影响】**Vaswani  et al. 2017'deki makaleler sadece RNN'in paralelleşme sorununu çözmekle kalmadı, bir model devrimi de başlatmıştır. BERT'den 2018'e kadar GPT-4'e kadar, ViT'den 2020'e kadar AlphaFold 2'e kadar, Transformer Architektur'ı modern AI'nin temel modülüne dönüşmüştür. Bu da " zayıf özsaygı tercihleri + büyük veri + büyük hesap gücü " 'in dikkatli tasarım alanındaki belirli yapıların aşılması " kanıtıdır.
