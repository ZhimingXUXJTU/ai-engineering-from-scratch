# LLaVA ve Görsel talimat ayarlama .

> LLaVA (April 2023) gezegenin en çok kopyalanan multimodal mimarisidir. BLIP-2'nin Q-Former'ini 2 katlı MLP ile değiştirdi, Flamingo'nun kapalı çapraz dikkatini naif bir simge zinciriyle değiştirdi ve GPT-4 tarafından yalnızca metin başlıklarından üretilen 158k görsel talimat dönüşlerinde eğitildi. 2023 ile 2026 yılları arasında bir VLM inşa eden herhangi bir uygulayıcı LLaVA'nın bir çeşitini inşa etti. LLaVA-1.5 AnyRes ekledi. LVA-NeXT çözünürlüğü yükseldi. LLaVA-OneVision tek bir tarifle birleşik görüntü, çoklu görüntü ve video. Bu ders, reçeti okuyor, projeksiyonu uyguluyor ve neden "simpler kazanmış" olduğunu açıklıyor.

> **【中文解读】**LLaVA, 2023-2026 yılları arasında en çok kopyalanan çok modoldaki yapıtıdır. Kök düşüncesi son derece basit: 2 katman MLP kullanarak, görsel kodlayıcıların çıkışlarını projeye bir dil modeliye yerleştirilmiş alanlara yerleştirerek, sonra görsel jetonu doğrudan metin dizisi arasında birleştirerek ortaya çıkarır.

> **【拓展：多模态大模型的起源】**LLaVA'ya kadar, çok modoldaki modeller çoğunlukla karmaşık跨模态 dikkat mekanizmalarına bağlıydı. Bu yöntemin doğrudan tüm ana VLM'leri etkiledi.

**Type:** Build  | **类型：构建**
**Languages:** Python (stdlib, projector + instruction-template builder)  | **语言：Python（标准库，投影器 + 指令模板构建器）**
**Prerequisites:** Phase 12 · 02 (CLIP), Phase 11 (LLM Engineering — instruction tuning)  | **前置：阶段12第02课（CLIP）、阶段11（LLM工程——指令微调）**
**Time:** ~180 minutes  | **时长：约180分钟**

>  **【前置】**Özetleme:LLAVA = BLIP-2'nin karşısında 刻意简化桥接,靠数据取胜──
>  **【类比】**LLaVA = "İşini doğrudan basıp dosyada yerleştir"―BLIP-2 Q-Former = " 256 sayfa çaplı kitap 32 sayfa özet yeniden LLM'ye teslim";LLaVA MLP = "576 sayfa orijinal tüm kitap yerleştir LLM'ye"―Öncü bölüm kağıt ama bilgi kaybediyor, sonuncusu kağıt ama LLM'yi görüyor tüm ayrıntıları LLM'ye yükseliyor aşağıdaki yazının değişiminden sonra, "kağıt" artık bir sorun değil,LLaVA doğal olarak kazanmıştır―

## Öğrenme hedefleri

- Bir MLP projecörünü inşa edin. Bu projecör, ViT patch embedde (dim 1024) ve LLM embedde (dim 4096) yerleştirir.
- LLaVA iki aşamalı tarifini izleyin: (1) 558k başlık çiftlerinde projektor düzeni, (2) 158k GPT-4 üretilen dönüşlerde görsel talimat ayarlaması.
- Resim jeton yer tutucu, sistem prompt ve kullanıcı/asistan dönüşleri ile LLaVA biçimindeki bir prompt oluşturun.
- Toplumun neden Q-Former'in token- bütçe kazanmasına rağmen Q-Former'den MLP'ye geçtiğini açıklayın.

## Sorun  sorun arka planı

BLIP-2'nin Q-Former'i (Denevi 12.03) bir görüntüyü 32 tokene sıkıştırır. Temiz, verimli, referans değerleri için iyi. Ama iki sorunu vardır.

İlk olarak, Q-Former eğitimlidir ancak kaybı son görev değildir. 1. aşama ITC+ITM+ITG'yi eğitir. 2. aşama LM kaybını eğitir. Sorgular LLM'nin sonra çözmesi gereken bazı ara temsilleri öğrenir. Bilgi boğazında kaybolur.

İkinci olarak, Q-Former 188M param alır ve LLaVA'nın 2023 ölçeğinde hedefinize LLM ile birlikte tasarlamak zorunda kalırsınız. LLM'yi değiştirin, Q-Former'i yeniden eğitin. Görüş kodlayıcısını değiştirin, yeniden eğitin. Her kombinasyon ayrı bir araştırma ve geliştirme projesiydi.

> **【中文解读】**BLIP-2'nin Q-Former'i 32 token'e şekillendirdi, görünüşte yüksek verimliydi, ancak iki temel sorunu vardı: 1) eğitim hedefleri uyumsuzluk.

LLaVA cevabı basitliğiyle utanç vericiydi: ViT'nin 576 patch tokenini alın ve her biri iki katlı MLP üzerinden geçsin (`1024 → 4096 → 4096`Bu yüzden, bu programın ilk aşaması, bir sonraki aşaması, bir sonraki aşaması, bir sonraki aşaması, bir sonraki aşaması, bir sonraki aşaması, bir sonraki aşaması, bir sonraki aşaması, bir sonraki aşaması, bir sonraki aşaması, bir sonraki aşaması, bir sonraki aşaması, bir sonraki aşaması, bir sonraki aşaması, bir sonraki aşaması, bir sonraki aşaması, bir sonraki aşaması, bir sonraki aşaması, bir sonraki aşaması, bir sonraki aşaması, bir sonraki aşaması, bir sonraki aşaması, bir sonraki aşama, bir sonraki aşaması, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir sonraki aşama, bir LM kaybı, bir sonraki aşama, bir sonraki aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama, bir aşama

> **【中文解读】**LLaVA'nın programı basit ve utanç verici: doğrudan ViT'in 576 ekleme simgesiyle 2 katlı MLP'den geçiyor.`1024 → 4096 → 4096`Bu yüzden, tüm programları LLM'nin giriş sırasına atıyoruz.

> ️ **【易错点】**İlk aşama eğitilmeli! Birçok kişi aşama 1'den atlayabileceğini düşünüyor. Doğrudan talimat yaptırmak için adım atmıyor. Yetiştirilmemiş bir projector çıkartıyor. LLM  tamamen göremiyor.

Veriler nereden geliyor? LLaVA'nın ikinci anlayışı: talimat verileri oluşturmak için GPT-4'i (tekestli) kullanın. GPT-4'e bir görüntü için COCO başlığı ve sınırlama kutu verilerini besleyin, konuşmalar, açıklamalar ve karmaşık mantık soruları üretmesini isteyin. 158k talimat- yanıt ücretsiz döndürülür. İnsan notları yoktur.

> **【中文解读】**LLaVA'nın ikinci yeniliği: GPT-4'yi kullanarak talimat verileri üretmek. COCO'nun resimlerini tanımlamak için GPT-4'e talimat vererek, konuşma, açıklama ve düşünce sorularını oluşturmasını sağlayın.

Sonuç: bir gün boyunca 8 A100'de çalışan, MMMU'de Flamingo'yu yenen ve toplumun genişletebileceği açık bir kontrol noktası gönderdiği bir VLM. 2023'ün sonuna kadar 50+ çatal doğurdu.

> **【拓展：LLaVA 的产业影响】**LLaVA, VLM'nin büyük bir hesaplama gücüne ihtiyaç duymadığını kanıtladı. Bu, çok modolu araştırmanın kapısını büyük ölçüde düşürdü, açık kaynaklı VLM ortamının patlamasını tetikledi. Finansal sahnede, LLaVA yapısı, mali haber tabloları, aktlar görüntüleri vb. anlamak için kullanılır.

## Konsepten bir şey.

> **【中文解读】**LLaVA, CLIP  görsel kodlayıcı ile LLM  bağlantısı, görsel talimat yoluyla küçük düzenleme modelleri öğrencilik görsel konuşma.

> **【拓展：LLaVA 的开源生态】**LLaVA en başarılı açık kaynaklı çok model modelidir. LLaVA-NeXT                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           


### Mimarlık, mimarlık.

LLaVA-1.5 13B:  LLaVA-1.5 13B 参数版:
- Görüş kodlayıcı / 视觉编码器: CLIP ViT-L/14 @ 336 (Stage 1, seçenek olarak dondurulmuş 2 / 第一阶段结,第二阶段可选解).
- Projector / 投影器: GELU aktivasyonu ile 2 katlı MLP / 2 katlı MLP + GELU激活, `1024 → 4096 → 4096`- Evet .
- LLM / 语言模型: Vicuna-13B (sonradan Llama-3.1-8B / 后续使用 Llama-3.1-8B).

Önceden bir görüntü + metin istek: 图像+文本提示的前向传播:

```
img -> ViT -> 576 patches of dim 1024           # 图像 -> ViT -> 576个维度1024的补丁
patches -> MLP -> 576 tokens of dim 4096         # 补丁 -> MLP -> 576个维度4096的token
prompt: system + "<image>" placeholder + user question  # 提示词：系统提示 + <image>占位符 + 用户问题
replace <image> token with the 576 projected tokens      # 用576个投影token替换<image>
feed the full sequence to the LLM                       # 将完整序列送入LLM
decode response                                         # 解码响应
```

Resim LLM bağlamının 576 simgesini yer almaktadır. 2048 bağlamda, bu metin için 1472 simge bırakır. 32k bağlamda, yuvarlama hatasıdır.

> **【中文解读】**Bir resim, LLM'nin üst aşağıdaki penceresinin 576'sını oluşturuyor. 2048'de bu yüzde 28'i, sadece 1472'i kalıyor.

### Etap 1: Projector ayarlama.

Dondurma ViT. Dondurma LLM. Sadece iki katmanlı MLP'yi çalıştırın. Verim kümesi: 558k görüntü-başlık çiftleri (LAION-CC-SBU). Kayıp: başlık üzerinde dil modelleme, projelenen görüntü jetonları üzerinde şartlı.

Bu projektor, bir süre içinde, bir süre içinde, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre,

> **【中文解读】**İlk aşamada, sadece iki katmanlık MLP eğitimi aldı. 558k resimle, dil oluşturma ve kaybı eğitimi aldı.

### İkinci aşama: Görsel talimat ayarlama.

Projector'u (hâlâ eğitim edilebilir) dondur. LLM'yi (genellikle tamamen, bazen LoRA) dondur. 158k görsel talimat dönüşlerinde eğit.

Liu ve diğerleri bunu:
1. COCO resmini çek.
2. Metin açıklamasını çıkarın (5 insan başlıkları + sınırlama kutusu listesi).
3. GPT-4'e 3 şablon ile gönderin.
   - Konuşma / 对话: "Bir kullanıcı ve asistan arasında bu görüntü hakkında ileri geri bir diyalog oluşturun".
   - Detaylı açıklama / 详细描述: "Şekil hakkında zengin ve ayrıntılı bir açıklama verin".
   - Karmaşık düşünce / 复杂推理: "Bir soru sor ve resim hakkında düşünmeyi gerektiren bir soru sor ve sonra cevap ver".
4. GPT-4'ün çıkışını çiftlere ayır.

Bu hiçbir şey resme doğrudan dokunmaz  sadece metin açıklaması. GPT-4 inanılmaz görüntü içeriğini halüsinasyonlar. Biraz gürültü, ama işe yaradı: 158k dönüş diyalogun kilitlenmesi için yeterli oldu.

> **【中文解读】**关键创新: DATA生成完全不接触图像本身仅用文本描述──GPT-4 会"幻觉"出合理图像内容,虽然会有噪音,但158k条数据足以解锁对话能力──这种"强模型生成弱模型训练数据"的思路后来广泛采用了(如自教、阿尔帕卡等)

> 🤔 **【困惑】**S: GPT-4 没看图只看描述,那 LLaVA 训练时实际学学的"视觉"是什么?A: LLaVA 学习是两件事:(1) 投影机把 ViT 的视觉特征翻译成 LLM 能理解的语义;(2) LLM 学会"见图片 → 生成符合 GPT-4 风格的描述"──GPT-4 的"幻觉"实际上是合理的描述(基于字幕),因此最终 LLaVA 也能产生合理的描述──
> ️ **【易错点】**Self training LLaVA 时数据不清洗 → GPT-4'ün görsel kirlilik eğitim kümesi,模型可能描述图中没有的东西──修复: GPT-4V(多模态版本) GPT-4'in yerine, GPT-4'in gerçek görüntüsü oluşturulmasını sağlamak

> **【拓展：数据合成的范式意义】**LLaVA'nın veri sentezleme yöntemi (GPT-4 生成指令数据) VLM 数据工程の新范式を開設しました.

### Toplum bunu neden kopyaladı? Toplum neden bunu yaptı?

- 1. aşamada özel kayıplar yok. LM kayıpları tüm.
- Projector günler değil saatler içinde çalışacak.
- LLM sadece projeksiyoncuyu yeniden eğiterek değiştirilebilir.
- Görsel talimat veri boru hattı GPT-4 kullanıyor ve yeni bir alan için yenilenmek için ucuz.

### LLaVA-1.5 ve LLaVA-NeXT.

LLaVA-1.5 (Oktyabr 2023) eklendi:  LLaVA-1.5 ((2023年10月) 新增:
- Akademik görev verileri (VQA, OKVQA, RefCOCO) talimat ayarlamalarına karıştı.
- Daha iyi sistem önerisi.
- 2048 → 32k bağlamı.

LLaVA-NeXT (Ocak 2024) eklendi:
- AnyRes: yüksek çözünürlüklü görüntüleri 2x2 veya 1x3 şebekesine bölünerek 336x336 ürünlerden oluşan bir küresel düşük çözünürlüklü küçük resim ekleyerek. Her ürün 576 token oluşturuyor; toplamı her görüntü için yaklaşık 2880 görsel token. OCR ve tablo görevleri atladı.
- Daha iyi talimat verileri karışımı ShareGPT4V ile (yüksek kalitede GPT-4V başlıkları).
- Daha güçlü temel LLM (Mistral-7B, Yi-34B).

> **【拓展：AnyRes 与高分辨率理解】**AnyRes, LLaVA'nın yüksek çözünürlüklü görüntü işleme teknikleri için önemli bir tekniktir. Finansal sahnelerde raporlama, gönderme ve diğer dosya görüntüleri için, yüksek çözünürlük anlamak önemlidir.

### LLaVA-OneVision

12.08 dersi OneVision'ı derinlemesine kapsar. Kısa sürüm: aynı projektor, ancak tek görüntü, çok görüntü ve videoyu bir modelde paylaşılan görsel belirti bütçesi ile kapsayan bir ders planıyla eğitilmiştir.

> **【中文解读】**12.08  ders OneVision'ı derinlemesine anlatacak.

### Q-Former ile karşılaştırma.

| | Q-Former (BLIP-2) | MLP (LLaVA) |
|---|---|---|
| Visual tokens per image / 每张图视觉token数 | 32 | 576 (base/基础) or 2880 (AnyRes) |
| Trainable params / 可训练参数 | 188M + LM | 40M + LM |
| Stage 1 loss / 第一阶段损失 | ITC+ITM+ITG | LM only / 仅语言建模 |
| LLM drop-in / LLM替换 | Requires retrain / 需重新训练 | Swap with minimal retrain / 几乎无需重训 |
| Multi-image / 多图像 | Awkward / 不自然 | Natural (concat) / 自然拼接 |
| Video / 视频 | Awkward / 不自然 | Natural (per-frame concat) / 逐帧拼接 |
| Token budget / Token预算 | Small / 小 | Large / 大 |

MLP, basitlik ve token esnekliği ile kazanır. Q-Former, token bütçesinde kazanır. 2023'ün sonuna kadar token bütçesi artık bağlayıcı bir kısıtlama değildi (LLM bağlamları 32k-128k+'ye büyüdü) ve basitlik baskın oldu.

> **【中文解读】**MLP, Q-Former, token 预算 胜出, MLP 简洁性和代币 灵活性上胜出, Q-Former, token 预算 胜出. Ancak 2023 yılı sonuna kadar, LLM'nin üst üstelik penceresi 32k-128k'ye kadar büyüdüğü için, token  bütçesi artık bir şişe değil,简洁性 kararlı bir faktör haline geldi. Bu, AI 工程inde önemli bir prensibi ortaya koydu: Şartlar değişince, en iyi çözüm de değişecek.

> 🤔 **【困惑】**Öğrenmek için bir bölüm daha sorulur: 1) Neden LLaVA 上加 Q-Former? 加 加了复杂度变高、训练难度大、收益小(除非视频这样的标志 预算紧张场景) ⋅ 2) LLaVA-1.5 和 LLaVA-NeXT Hangi seçeneği seçilir? 默认 LLaVA-NeXT(支持高分辨率 AnyRes,OCR 和文档任务更强) ⋅

### İndirme biçimi.

```
A chat between a curious human and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the human's questions. USER: <image> Describe this image in detail. ASSISTANT: The image shows ...
```

`<image>`Tokenizer, eğitim aldığından biraz daha uzun bir dizini görür, ancak LLM yeni girişleri ele alır çünkü 1. aşamada öğretildi.

> **【中文解读】** `<image>`Bu yüzden hiç görülmemiş girişleri işleyebilmektedir, çünkü ilk aşamada yapılan eğitim, proje sonrası görüntü gösterilerini anlamalarını öğretmiştir.

### Parametre ekonomisi.

LLaVA-1.5-7B ayrıştırma:
- CLIP ViT-L/14 @ 336: 303M (dondurulmuş aşama 1, sıklıkla dondurulmuş aşama 2 / 第一阶段结,第二阶段通常解).
- Projector (2x linear) / 投影器: ~ 22M eğitimli / 可训练.
- Llama-7B: 7B.
- Toplam / 总计: 7.3B parametre. 2. aşamada antren edilebilir / 2. aşamada antren edilebilir: tam 7B + 22M projeksiyoncu / 全部7B + 22M投影器.

Etap 2: 8xA100'de 20 saatlik eğitim maliyeti. Bu anahtar sayı  bir gün, bir düğüm, yeniden üretilebilir.

> **【中文解读】**İkinci aşama eğitim maliyeti: 8 张 A100 跑约 20 小时──这是关键数字一天、一台机器、可复现──这是LLaVA 能够迅速传播的原因──
```figure
mm-llava-projector
```

## Kullan

## Kullanın.

`code/main.py`- Bu bir şey .`code/main.py`实现了:

1. İki katlı MLP projekörü (toy ölçeği için 16 → 32 → 32) saf Python.
2. Hızlı inşaat boru hattı: Sistem hızlılığı + `<image>`N projelenen token + kullanıcı dönüşü + asistan jenerasyon yer tutıcısı ile değiştirildi.`<image>`替换为N个投影代币 + 用户轮次 + 助手生成占位符──
3. LLM bağlamında 576 token görsel bloğunun neye benzediğini görselleştiren bir görüntüleme (% 2k / 32k / 128k bağlamı tüketildi).

## Gönderin.

Bu ders bize çok yararlı .`outputs/skill-llava-vibes-eval.md`LLaVA aile kontrol noktası olarak, 10 hızlı vibes-eval suite (3 başlık, 3 VQA, 2 akıl yürütme, 2 reddetme) çalıştırır ve insan okuyabilir bir puan kartı rapor eder.

> **【中文解读】**本课产 出 `outputs/skill-llava-vibes-eval.md`◊ LLaVA 系列 kontrol noktasını belirle, 10 个提示的"vibes-eval" test kitlerini çalıştır ◊ 3 açıklama ∙ 3 VQA ∙ 2 önerme ∙ 2 reddetme), yapay olarak okunur bir sonuç oluştur ◊ Bu resmi bir temel test değil, bir duman testidir, projector ve LLM  İyi bağlantılarını doğrulamak için ◊

## Egzersizler.

1. 2 katmanlı MLP projeksiyonu için tren edilebilir parametreler sayısını hesaplayın .`1024 → 4096 → 4096`GELU ve önyargıyla, LLaVA-13B'nin hangi kısmını temsil ediyor?
   | 计算维度为 `1024 → 4096 → 4096` 的 2 层 MLP 投影器的可训练参数量。含 GELU 和 bias，它占 LLaVA-13B 的多少比例？

2. "Refusal" vakaları için LLaVA uyarısı oluşturun  görüntüde bir özel kişi bulunur. Beklenen asistan cevabını yazın.
   | 为"拒绝"场景构建 LLaVA 提示词——图像包含私人个体。写出期望的助手回复。为什么 LLaVA 应该零样本拒绝？需要什么训练数据来强化拒绝行为？

3. LLaVA-NeXT blogunun AnyRes bölümünü okuyun. AnyRes'deki 1344x672 görüntü için görsel jeton sayısını hesaplayın. 336x336'daki 576 jetonun tabanına karşılaştırın.
   | 阅读 LLaVA-NeXT 博客的 AnyRes 部分。计算 1344x672 图像在 AnyRes 下的视觉 token 数量，并与 336x336 基础设置的 576 个 token 比较。

4. LLaVA aşama-1 projeksiyonu başlıklarda LM kaybı ile eğitilmiştir. 1. aşamayı atlayıp doğrudan 2. aşamaya (görsel talimat ayarlama) giderseniz ne olur?
   | LLaVA 第一阶段投影器用描述文本的语言建模损失训练。如果跳过第一阶段直接进入第二阶段会怎样？引用 Prismatic VLMs 消融实验（arXiv:2402.07865）回答。

5. LLaVA-Instruct-150k, talimatları oluşturmak için GPT-4 ile COCO başlıklarını kullanır. Yeni bir alan için (tıp X-ışını, uydu görüntüleri), her adımda yanlış giden ne olabilir?
   | LLaVA-Instruct-150k 用 GPT-4 从 COCO 描述生成指令。对于新领域（医疗X光、卫星图像），描述生成领域指令的四步数据管线。每步可能出什么问题？

## Anahtar Terimler

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|----------------|------------------------|----------|---------|
| Projector | "MLP bridge" | 2-layer MLP with GELU mapping ViT dim to LLM dim | 投影器：将ViT维度映射到LLM维度的2层MLP | |
| Image token | "<image> placeholder" | Prompt marker replaced by N projected visual tokens before inference | 图像token：推理前被替换为N个投影视觉token的提示标记 | |
| Visual instruction tuning | "LLaVA stage 2" | Training on GPT-4-generated (image, instruction, response) triplets | 视觉指令微调：在GPT-4生成的（图像,指令,回复）三元组上训练 | |
| Stage 1 alignment | "Projector pretraining" | Freeze ViT and LLM, train projector with LM loss on captions | 第一阶段对齐：冻结ViT和LLM，用描述文本的LM损失训练投影器 | |
| AnyRes | "Multi-crop tiling" | Split high-res image into a tile grid and concatenate each tile's visual tokens | AnyRes：将高分辨率图像切分为网格，拼接各切片的视觉token | |
| LLaVA-Instruct | "GPT-4-generated" | 158k instruction-response pairs synthesized from COCO captions + GPT-4 | LLaVA指令数据：用COCO描述+GPT-4合成的158k指令-回复对 | |
| Vision encoder freeze | "Backbone locked" | CLIP weights do not update in stage 1, sometimes not in stage 2 either | 视觉编码器冻结：CLIP权重在阶段1不更新，有时在阶段2也不更新 | |
| ShareGPT4V | "Better captions" | 1M dense captions generated by GPT-4V, used for higher-quality alignment | 100万条GPT-4V生成的密集描述，用于更高质量的对齐 | |
| VQA | "Visual question answering" | Task of answering a free-form question about an image | 视觉问答：回答关于图像的自由形式问题 | |
| Prismatic VLMs | "Design-space paper" | Karamcheti 2024 ablation systematically testing projector and data choices | 系统测试投影器和数据选择的设计空间消融实验论文 | |

## Daha fazla okumak

- [Liu et al. — Visual Instruction Tuning (arXiv:2304.08485)](https://arxiv.org/abs/2304.08485)LLaVA gazetesi.
- [Liu et al. — Improved Baselines with Visual Instruction Tuning (arXiv:2310.03744)](https://arxiv.org/abs/2310.03744)LLaVA-1.5.
- [Chen et al. — ShareGPT4V (arXiv:2311.12793)](https://arxiv.org/abs/2311.12793) yoğun başlıklı veri kümesi. 密集描述数据集
- [Karamcheti et al. — Prismatic VLMs (arXiv:2402.07865)](https://arxiv.org/abs/2402.07865) tasarım-uzay ablations.
- [Li et al. — LLaVA-OneVision (arXiv:2408.03326)](https://arxiv.org/abs/2408.03326) tek görüntü, çok görüntü, video.
