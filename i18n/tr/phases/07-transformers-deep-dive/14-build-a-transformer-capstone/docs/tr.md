# Bir Transformer'ı sıfırdan inşa edin Capstone'dan inşa edin Transformer'ı inşa edin

> 13 ders, bir model, kısayol yok.

> **【中文解读】**Tüm bilgiyi bütünleştirmek, tam bir GPT yapısalı oluşturmak için. Bu aşamada, tüm Transformer kodlarını anlayabilmeniz için bu aşamada, bu aşamada, tüm bilgiyi bütünleştirmek için, tüm GPT yapısalılarını tamamlamak için, tüm bilgiyi tamamlamak için, tüm GPT yapısalılarını tamamlamak için.

**Type:** Hands-on | **类型:** 动手
**Language:**Python .**语言:**Python
**Prerequisites:** Phase 7 · 01 through 13. Don't skip. | **前置知识:** Phase 7 · 01 through 13. Don't skip.
**Time:** ~120 minutes | **时间:** ~120 分钟

## Sorunlar. Sorunlar.

Her makaleyi okudun. Dikkat, çok başlı bölünmeler, konum kodlamaları, kodlayıcı ve dekoder blokları, BERT ve GPT kaybı, MoE, KV önbelleği uyguladın. Şimdi gerçek bir görev üzerinde birlikte çalıştırın.

> Her makaleyi okudun. Şimdi onları gerçek bir görev üzerinde birlikte çalışmaya hazırlayın.

Baş taşı: karakter düzeyinde dil modelleme görevi için küçük bir decoder-tek transformatörü son-son eğit. Shakespeare'i okuyor. Yeni Shakespeare'i oluşturur. 10 dakikadan az bir süre içinde bir dizüstü bilgisayar üzerinde eğitilmek için yeterince küçük. Daha büyük bir veri kümesi ve daha uzun bir eğitimde değişmek size gerçek bir LM sağlar.

> 毕业项目: 在字符级语言建模任务上端到端训练一个小型解码器专用变压器──它读取莎士比亚,生成新的莎士比亚──它足够小,可以在笔记本上完成10分钟内训练──它足够正确,转换成更大的数据集和更长的训练时间就能得到真正的语言模型──

Bu ders "nanoGPT"i. Orijinal değil. Karpathy'nin 2023 nanoGPT öğretim kitabı her öğrencinin en az bir kez yazdığı referans uygulamasıdır. Şekilini kaldırıp kapadığımız şeyi yeniden düzenliyoruz.

> Bu, derslerin "nanoGPT"idir. Bu, başlangıçtaki değil. Karpati 2023 nanoGPT öğretimi, her öğrencinin en az bir kez yazması gereken bir referans uygulamasıdır.

> **【中文解读】**Bu eğitim projesi, 13 bölümden önce tüm bilgiyi birleştirir: karakter seviyesinde dil oluşturmak, işaretler yerleştirmek, konum kodlaması, RMSNorm, çok sayıda nedenle ilgili dikkat, SwiftGLU FFN, eksik bağlantı, bir Shakespeare üretici eğitimi.

> **【拓展：从 nanoGPT 到生产级 LLM】**Karpathy'nin nanoGPT'si Transformer'in öğrenme en iyi başlangıcı noktasıdır. NanoGPT'den üretim seviyesine LLM'nin önemli farkları: veri boyutu ((MB'den TB'ye kadar) ✓ eğitim altyapısı ((tek GPU'dan binlerce GPU'ya kadar) ✓ dağıtımlı eğitim ((data并行、模型并行、流水线并行) ✓) ✓ ve sonraki eğitim ((SFT + RLHF) ✓ ama çekirdek yapı aynıdır.

## Konsepten bir şey.

![Transformer-from-scratch block diagram](../assets/capstone.svg)

Mimarlık, şöyle açıklandı:

> 架构,带注释:

```
input tokens (B, N)
   │
   ▼
token embedding + positional embedding  ◀── Lesson 04 (RoPE option)
   │
   ▼
┌──── block × L ────────────────────┐
│  RMSNorm                          │  ◀── Lesson 05
│  MultiHeadAttention (causal)      │  ◀── Lesson 03 + 07 (causal mask)
│  residual                         │
│  RMSNorm                          │
│  SwiGLU FFN                       │  ◀── Lesson 05
│  residual                         │
└────────────────────────────────── ┘
   │
   ▼
final RMSNorm
   │
   ▼
lm_head (tied to token embedding)
   │
   ▼
logits (B, N, V)
   │
   ▼
shift-by-one cross-entropy            ◀── Lesson 07
```

### Neyi gönderiyoruz

> Biz teslimat içeriği:

- `GPTConfig` Tüm hiperparametreyi yapılandırmak için tek bir yer.
  Çeviri:`GPTConfig`                                                                                                                                                                                                                                                              
- `MultiHeadAttention` sebepçi, serili, seçeneği Flash tarzı yol (PyTorch's `scaled_dot_product_attention`)
  Çeviri:`MultiHeadAttention` 因果的、批量,可选闪风路径(PyTorch'ın `scaled_dot_product_attention`)。
- `SwiGLUFFN` Modern FFN.
  Çeviri:`SwiGLUFFN` 现代 FFN。
- `Block` Normalden önce, kalan sarılmış dikkat + FFN.
  Çeviri:`Block` 前归一化,残差包裹的注意力 + FFN。
- `GPT` yerleşim, yığılmış bloklar, LM başı, üretmek().
  Çeviri:`GPT` 嵌入、堆叠块、LM 头、生成()
- AdamW, cosine LR, gradient kesimi ile eğitim döngüsü.
  Çinçe Çevirim:带 AdamW、余弦学习率、梯度裁剪的训练循环──
- Shakespeare'in metinleri için bir işaretlemeci.
  Çeviri:Shakespeare

> **【中文解读】**完整的GPT 实现包含:配置类、多头因果注意力(可选 Flash Attention)、SwiGLU FFN、前归归化残差块、完整的GPT 模型类(嵌入 + 堆叠块 + LM 头 + 生成函数)、AdamW + 余弦学习率训练循环──简洁的说来,学习式位置嵌入 (学习式位置嵌入) 而不是 RoPE) 没有实现 KV 缓存,但练习要求你添加这些──

### - Neyi göndermiyoruz?

> Biz teslim etmiyoruz içerik:

- RoPE  Ders 04'te kavramsal olarak uygulanmıştır. Burada basitlik için öğrenilen pozisyonsal yerleşimleri kullanıyoruz.
  Çince Çevirimi:RoPE  第4 课有概念实现──这里为简洁起见使用学习式位置嵌入──练习要求你替换为RoPE──
- KV önbelleği, her nesil adımıyla tüm önbelleği yeniden hesaplar. Daha yavaş ama daha basit.
  Çinçe çevirisi:生成时的KV 缓存  Her bir üretim adımına dikkat etmelisin.
- Flash Dikkat  PyTorch 2.0+ otomatik gönderiler girdiler eşleşirse; biz kullanıyoruz `F.scaled_dot_product_attention`- Evet .
  Çeviri:PyTorch 2.0+`F.scaled_dot_product_attention`- Evet.
- MoE'yi blok başına tek FFN'den görüyorsunuz.
  Çin Çeviri: MoE  Her blok tek tek FFN。

### Hedef ölçümleri

Mac M2 dizüstü bilgisayarında, 4 katlı, 4 başlı, d_model=128 GPT 2000 adım için eğitilmiş.`tinyshakespeare.txt`- ...

> Mac M2'de 4 katı, 4 başı, 128 model = GPT'de`tinyshakespeare.txt`Üncelim 2000 步:

- Eğitim kaybı yaklaşık 6 dakika içinde ~4.2 (hassasi) ~1.5'e doğru ilerliyor.
  Çin Çince: eğitim kaybı yaklaşık 4.2                                                                                                                                                                                                                                                          
- Örnek alınan ürün Shakespeare şeklinde görünüyor: eski kelimeler, çizgi kesintiler, "ROMEO:" gibi özel isimler ortaya çıkıyor.
  Çine dilinde: 采样输出 looks like Shakespeare:古词、换行、"ROMEO:"等专名词出现──
- Val kaybı (teksten son 10%'i tutturulmuştur) eğitim kaybını yakından takip eder; bu boyutta/ bütçede fazla uygun değildir.
  Çinçe Çevirisi:验证损失 (Balanım)

> **【拓展：从字符级到子词级 Tokenizer】**Bu proje için kullanılan karakter sınıfı tokenizer(sadece ama düşük etkinlik)。 üretim sınıfı LLM BPE kullanmak(Byte Çift Kodlama) veya SentencePiece 等子词级 tokenizer。Llama BPE kullanmak, GPT-4 Cl100k_base BPE tokenizer。子词 tokenization 在词汇量、序列长度和语义粒度之间取得平衡,是现代 LLM 的标配──

## Yapın.
```figure
n5-block-stack
```

## Yapın

Bu ders PyTorch kullanıyor.`torch`(CPU yapı tamamdır).`code/main.py`Senaryo şu şekilde:

> 本课使用 PyTorch──安装 `torch`(CPU 版本即可)`code/main.py`❖ 該脚本处理:

- İndirmek`tinyshakespeare.txt`Eğer eksikse (veya yerel bir kopyayı okuyabilirse).
  Çeviri: if缺失则下载`tinyshakespeare.txt`(或读取本地副本)
- Byte seviyesindeki char tokenizer.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Tren/val bölümü 90/10'da.
  Çin Çeviri: 90/10 的训练/验证分割──
- Desteklenen donanım üzerinde bf16 otomatik olarak yayınlanan eğitim döngüsü.
  Çinçe Çevirisi: Support Hardware üzerinde bf16 自动混合精度训练循环──
- Eğitimden sonra örnekleme tamamlandı.
  Çinçe Çevirisi: eğitim tamamlanmasından sonra

### Adım 1: Veriler

```python
text = open("tinyshakespeare.txt").read()
chars = sorted(set(text))
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for c, i in stoi.items()}
encode = lambda s: [stoi[c] for c in s]
decode = lambda xs: "".join(itos[x] for x in xs)
```

65 eşsiz karakter, küçük kelime birikimi, 4 baytlık bir kelime boyutuna uygun, BPE, tokenizer dramı yok.

> 65 个唯一字符──微型词表──适配 4 字节词体_size──没有 BPE,没有分词器的麻烦──

### Adım 2: Model

Bakın .`code/main.py`.Blok, ders 05  pre-norm, RMSNorm, SwiGLU, nedenci MHA'dan ders kitabı. 4/4/128 için parametre sayısı: ~800K.

> 参见 `code/main.py`△ Bu blok 5. sınıfı ders kitabı 前归归化实现、RMSNorm、SwiGLU、因果多头注意力―4/4/128 参数:約800K―

### Adım 3: Eğitim döngüsü

- 256 uzunluklu simge pencerelerinin rastgele bir seriyi alın.

> 获取随机批量长度为 256 标志窗口──前向传播──偏移一位的交叉──反向传播──AdamW 步进──记录──重复──

```python
for step in range(max_steps):
    x, y = get_batch("train")
    logits = model(x)
    loss = F.cross_entropy(logits.view(-1, vocab_size), y.view(-1))
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    opt.step()
    opt.zero_grad()
```

### 4. adım: örnek

Bir istek verildiğinde, tekrar tekrar ileriye doğru, en üst p logitlerinden örnek, ekle ve devam et. 500 token sonrasında dur.

> 给定一个提示,反复前向传播, top-p logits 采样,追加,继续──500 个符号 后停止──

### Adım 5: çıkış oku

2000 adımdan sonra:

> 2000 步后:

```
ROMEO:
Away and mild will not thy friend, that thou shalt wit:
The chief that well shame and hath been his friends,
...
```

Shakespeare değil, Shakespeare şeklinde, 800 bin parameter ve 6 dakika bir dizüstü bilgisayarla kazanmış.

> Shakespeare değil ama Shakespeare gibi. 800 bin kişilik bir kazanç.

## Çerçeveyi kullanın.

Bu temel taş, bir referans mimarisi.

> Bu eğitim projesi bir referans yapı. Üç genişleme onu gerçekten kullanılabilir bir sisteme dönüştürmek için kullanılabilir:

1. **Swap the tokenizer.**BPE kullanın (örneğin `tiktoken.get_encoding("cl100k_base")`Sözcük boyutu 65'den ~ 50.000'e kadar atlıyor.
   Çeviri:**替换分词器。**BPE kullanın`tiktoken.get_encoding("cl100k_base")`)──词表大小 65 跳到约 50,000──模型容量需要相应扩展──
2. **Train on a bigger corpus.**Kullanım`OpenWebText`veya `fineweb-edu`Tek bir A100'de 10B token, 125M param GPT için yaklaşık 24 saat sürer.
   Çeviri:**在更大的语料上训练。**Kullanım`OpenWebText`Ya da`fineweb-edu`(HuggingFace) ・・・在单张 A100 上用10B token 训练 125M 参数 GPT 约需24小时──
3. **Add RoPE + KV cache + Flash Attention.**Aşağıdaki egzersizler her birinizi takip eder.
   Çeviri:**添加 RoPE + KV 缓存 + Flash Attention。**Aşağıdaki egzersizler her adımı tamamlamanıza yardımcı olacaktır.

Bu, akıcı İngilizce üreten 125M parametresi GPT olarak sona erer. Sınır modeli değil. Ama aynı kod yolu  sadece daha büyük  Karpathy, EleutherAI ve Allen Enstitüsü tarafından 2026'da araştırma kontrol noktalarını eğitmek için kullanılır.

> En sonunda akıcı İngilizce 125M parametr GPT üretebilen bir kod elde ettim. Önceki model değil. Ama aynı kod yolları sadece daha büyüktür. Karpathy, EleutherAI ve Allen Enstitüsü 2026 yılında kullanılan eğitim araştırma ve kontrol noktası olarak kullanılmıştır.

> **【拓展：Karpathy 的 nanoGPT 与教育意义】**Andrej Karpathy'nin nanoGPT'i (Yeni Üretim) 2023 yılında AI eğitim tarihindeki en etkili derslerden biri oldu. Bu, yaklaşık 300 adet PyTorch ile uygulanabilecek bir GPT'yi kanıtladı. Bu "seri yapılandırma" öğretim yöntemi, Transformer'i bir kara kutu olarak değil, her bileşenin rolünü gerçekten anlamana yardımcı oldu.

## İndirin . Ürünler .

Bakın .`outputs/skill-transformer-review.md`. Yetenek, önceki 13 dersin tümünde doğruluk için sıfırdan dönüştürücü uygulamasını gözden geçirir.

> 参见 `outputs/skill-transformer-review.md`Bu beceri, bir transformatörün sıfırdan inşa edilmesini kontrol ederek, tüm 13 derslerin doğruluğunu kontrol eder.

## Egzersizler.

1. **Easy.**Çık .`code/main.py`Eğitimli modelinizin son aşamada geçerlilik kaybının 2.0'den az olduğunu kontrol edin.`max_steps`2000'den 5000'e kadar olan val kaybı gelişmeye devam ediyor mu?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ Test Your Training Model'in son aşama test kaybı 2.0 ∼ olacak.`max_steps`2000'den 5000'e doğru verifi kaybı gelişmeye devam ediyor mu?
2. **Medium.**Öğrenilen pozisyonsal yerleşimleri RoPE ile değiştirin.`MultiHeadAttention`Tren ve kontrol val kaybı en az o kadar düşük.
   Çeviri: RoPE 替换学习式位置嵌入──在 `MultiHeadAttention`Ortalama Q ve K  uygulaması dönüşüm; eğitim ve test; test kaybı en az 差 değil.
3. **Medium.**Örnekleme döngüsünde bir KV önbelleği uygulayın. 500 token oluşturun.
   Çinçe Çevirisi: KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存── KV 缓存 缓存 缓存─ KV 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存 缓存
4. **Hard.**Bir sonraki bir ek bir token (MTP  DeepSeek-V3'den Multi-Token Tahmini) öngören ikinci bir baş ekleyin.
   Çin dilinde: Add Add a second head prediction under a second tokenMTP DeepSeek-V3'ün çoklu bir tokeninden geliyor.
5. **Hard.**Blok başına tek FFN'yi 4 uzman MoE ile değiştirin. Router + top-2 yönlendirme.
   Çinçe Çevirisi:将每块的单个FFN 替换为4 专家 MoE──路由器 + top-2 路由──观察在匹配活跃参数下验证损失的变化──

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| 术语 | 通俗说法 | 实际含义 |
| nanoGPT | "Karpathy's tutorial repo" | Minimal decoder-only transformer training code, ~300 LOC; the canonical reference. |
| nanoGPT | "Karpathy 的教程仓库" | 最小解码器专用 Transformer 训练代码，约 300 行；经典参考。 |
| tinyshakespeare | "The standard toy corpus" | ~1.1 MB of text; every character-LM tutorial since 2015 uses it. |
| tinyshakespeare | "标准玩具语料库" | 约 1.1 MB 文本；自 2015 年以来每个字符级语言模型教程都用它。 |
| Tied embeddings | "Share input/output matrix" | LM head weight = transpose of token embedding matrix; saves parameters, improves quality. |
| 绑定嵌入 | "共享输入/输出矩阵" | LM 头权重 = token 嵌入矩阵的转置；节省参数，提高质量。 |
| bf16 autocast | "Training precision trick" | Run forward/back in bf16, keep optimizer state in fp32; standard since 2021. |
| bf16 自动混合精度 | "训练精度技巧" | 前向/反向用 bf16，优化器状态用 fp32；2021 年以来的标准。 |
| Gradient clipping | "Stops spikes" | Cap global grad norm at 1.0; prevents training blowups. |
| 梯度裁剪 | "阻止尖峰" | 将全局梯度范数限制在 1.0；防止训练爆炸。 |
| Cosine LR schedule | "The 2020+ default" | LR ramps up linearly (warmup) then decays cosine-shaped to 10% of peak. |
| 余弦学习率调度 | "2020+ 默认" | 学习率线性升温（warmup）然后余弦衰减到峰值的 10%。 |
| MFU | "Model FLOP Utilization" | Achieved FLOPs / theoretical peak; 40% dense, 30% MoE is strong in 2026. |
| MFU | "模型 FLOP 利用率" | 实际 FLOPs / 理论峰值；2026 年稠密 40%、MoE 30% 是好的。 |
| Val loss | "Held-out loss" | Cross-entropy on data the model never saw; overfit detector. |
| 验证损失 | "留出损失" | 模型从未见过的数据上的交叉熵；过拟合检测器。 |

## Daha fazla okumak

- [The Annotated Transformer (Harvard NLP)](https://nlp.seas.harvard.edu/annotated-transformer/) klasik notlı uygulanma.
  Çeviri:Devamı, Çeviri:Devamı, Çeviri:Devamı, Çeviri:Devamı, Çeviri:Devamı, Çeviri:Devamı, Çeviri:Devamı, Çeviri:Devamı, Çeviri:Devamı, Çeviri:Devamı, Çeviri:Devamı, Çeviri:Devamı, Çeviri:Devamı, Çeviri:Devamı, Çeviri:Devamı, Çeviri:Devamı, Çeviri:Devamı, Çeviri:Deviri:Devamı, Çeviri:Devamı, Çeviri:Devamı, Çeviri:Deviri:Devamı, Çeviri:Deviri:Deviri:Devamı, Çeviri:Deviri:Deviri:Deviri:Deviri:Deviri:Deviri:Deviri:Deviri:Deviri:Deviri:Deviri:Deviri:Deviri:Deviri:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Devidi:Dev
