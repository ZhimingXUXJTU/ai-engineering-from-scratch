# InternVL3: Yerli Multimodal Pretraining

> InternVL3'den önceki her açık VLM aynı üç adımlı tarifi izledi: trilyonlarca metin tokeni üzerinde eğitilmiş bir metin LLM alın, bir görme kodleyicisine bağlanın, sonra dikişleri ince ayarlayın. Bu işlevsel ama uyum borcudur  metin LLM tüm eğitim öncesi bütçesini saf metin için harcadı ve görsel tokenleri doğuştan anlamıyor. Görüş sonrası eklediğinizde, LLM'nin metni unutmadan görsel girişleri metin mantıklarına nasıl bağlayacağını yeniden öğrenmesi gerekir. InternVL3 (Zhu et al., Nisan 2025) post-hoc yaklaşımını reddediyor: bir antrenman öncesi koşusu, bir adımdan beri birbirine karışan metin ve multimodal. Sonuç, MMMU-Pro'da Gemini 2.5 Pro'yla 78B param açık. Bu ders, yerli önceden eğitim için olan durum ve bunu yaptığınızda neler değiştiğini anlatır.

> **【中文解读】**InternVL3'ün temel yeniliği: "Önce eğitimli metin programı reddetmek, ilk adımdan metin ve çok biçimli veri bağlantısı eğitimine dönüştürmek, "Önce eğitimli metin programı reddetmek" ve "Önce eğitimli metin becerilerini unutmak" gibi sorunları ortadan kaldırmak. InternVL3-78B MMMU-Pro'da Gemini 2.5 Pro'yu uyguladı.

> **【拓展：原生预训练 vs 后装的成本权衡】**Orijinal hazırlık, borçları ortadan kaldırdı, ancak maliyetler sonrakı hazırlık programından çok daha yüksek oldu. Bir milyon GPU'ya ihtiyaç duyuldu ve her zaman temel LLM'nin esnekliğini bıraktı. Çoğu proje için, sonrakı hazırlık programı daha ekonomik hale geldi.

**Type:** Learn  | **类型：学习**
**Languages:** Python (stdlib, training-corpus mixer)  | **语言：Python（标准库，训练语料混合器）**
**Prerequisites:** Phase 12 · 05, Phase 12 · 07 (recipes)  | **前置：阶段12第05课、阶段12第07课（配方）**
**Time:** ~120 minutes  | **时长：约120分钟**

>  **【前置】**Önemli bir ders: Önemli bir ders, önemli bir ders, önemli bir ders, önemli bir ders.
>  **【类比】**后装 VLM(LLaVA) = "成年后学外语"已经掌握母语(文本),再艰难学第二语言(视觉) ・・・原生 VLM(InternVL3) = "双语家庭长大"两种语言同时学,没有翻译损耗──后装方案便宜但有口音(对齐债务),原生方案昂贵但流利──
> 🤔 **【困惑】**S: 既然原生预训练如此好,为什么LLaVA 仍然主流?  成本!原生预训练需要数百万GPU 小时从头跑(一次 ~数百万美元),后装LLaVA 只需8×A100 跑一天──除非你是大厂从头训新模型,否则LLaVA 路线性价格比较高──

## Öğrenme hedefleri

- Post-hoc VLM eğitimi neden bir uyum borcu biriktirdiğini açıklayın, üç ölçülebilir semptomları (kazaflı unutma, cevap sürükleme, görsel-metin tutarlılığı) belirtin.
- InternVL3'ün yerel antrenman öncesi mixini ve neden metin oranının: birbirine karışmış olması: başlık önemli olduğunu açıklayın.
- V2PE ile Qwen2-VL'nin M-RoPE'si karşılaştırın.
- Görsel çözünürlük yönlendiricisi (ViR) ve kopyalanmış görsel dil (DvD) dağıtım optimizasyonlarını isimlendirin.

## Sorun  sorun arka planı

Post-hoc VLM eğitimleri varsayılan bir yöntemdir. LLaVA, BLIP-2, Qwen-VL, Idefics  hepsi önceden eğitilmiş bir LLM (Llama, Vicuna, Qwen, Mistral) alır ve görme ekler. Eğitim aşamaları tipik olarak şöyle görünür:

1. Dondurulmuş LLM + dondurulmuş görüntü kodlayıcı + eğitimli projektor, gömülmeleri düzeltmek için yazım çiftlerinde eğitilmiştir.
2. LLM'yi dondur, talimat verileri üzerine eğitim ver.
3. Seçenekli görevler için özel ince ayarlama.

Dönüşüm borçlarının üç semptomunu ortaya koyuyor:

- Katastrofik unutma / 灾难性遗忘. Post-hoc VLM sadece metin becerilerini unutur. GSM8K puanları 5-10 puan düşer. Hellaswag puanları düşer. Temiz metin ajanları geri döner.
- Cevap sürükleme / 回答漂移. Aynı görsel sorunun küçük ifadeleri farklı cevaplar alır. Görüş kodlayıcı LLM'nin kendi tokenlerinden daha zayıf bağlarla LLM'ye bağlanır.
- Görsel-metin tutarlılığı / 视觉-文本不一致. VLM bir resmi doğru bir şekilde tanımlayabilir ve daha sonra kendi açıklamasına aykırı bir soruya cevap verebilir. Görsel jetonlar LLM'nin iç tutarlılık kontrollerine metin gibi katılmaz.

> **【中文解读】**后装 VLM'in üç çeşit karşılaşma borçları: 1) felaketli unutma GSM8K 掉 5-10 分; 2) 回答漂移 aynı görsel sorunun farklı ifadeleri farklı cevaplar almıştır; 3) 视觉文本不一致模型正确描述图像,却给出矛盾的答──这些症状是因为视觉代币不同于文本代币,那样深深参与了LLM's internal coherence check──

## Konsepten bir şey.

### Yerli çok modal öncesi eğitim

InternVL3 başlangıçtan itibaren bir corpus üzerinde çalışmaktadır.

- %40 tek metin verileri (FineWeb, Proof-Pile-2, vb.) / %40 纯文本数据
- % 35 birbirine karışmış görüntü-metin verileri (OBELICS, MMC4 tarzı) / % 35 交织图文数据
- % 20 çiftleştirilmiş resim başlık verileri / % 20 图文配对数据
- % 5 video metin verileri / % 5 视频文本数据

Görme simgelerinin, metin simgelerinin ve modal çapraz etkileşimlerin hepsi ilk gradient adımından itibaren aynı kayıpta yer alıyor.

Eğitim temel model için tek bir aşamadır. Eğitim ayarlaması takip eder, ancak temel model zaten görsel jetonları birinci sınıf vatandaşlar olarak anlar.

> **【中文解读】**InternVL3 ilk adımdan bir görsel jeton, metin jetonu, ve bir de bir kayıp işlevi içinde geçiyor.

### V2PE (değişken görsel pozisyon kodlaması)

Qwen2-VL, sabit eksel tahsisli M-RoPE kullanır. InternVL3 V2PE'yi tanıttı: pozisyon kodlaması, öğrenilebilir ölçeklendirme ile modalite türüne (metin, görüntü, video) göre değişir.

- Metin işaretleri 1 boyutlu konum elde eder.
- Resim yamaları 2 boyutlu konum elde eder.
- Video çerçeveleri 3D pozisyon alır (zaman, satır, kol).

Üçü aynı RoPE frekans tabanını paylaşır, ancak her bant için gizli-dim tahsis edilmesi sabit bir bölünme yerine öğrenilmiş bir parametredir.

V2PE'nin ablasyon iddiası: Aynı hesaplama sırasında M-RoPE'ye göre video referansları için 1-2 puan.

> **【中文解读】**V2PE ile M-RoPE arasındaki fark: Gizli boyutların her frekans aşamasında bölünmesi, sabit olmayan bir bölüm olarak öğrenilmektedir.

### Görsel Kararlılık Router (ViR)

Uygulama optimizasyonu. Tüm görüntülerin tam çözünürlüklü kodlama gerektirmemesi gerekir. Düşük detaylı bir nesne ile bir fotoğraf, 1280px yerli kodlandığında jetonları atır. ViR, soruyu cevaplamak için gerekli olan en az çözünürlüğü kodlamadan önce tahmin eden küçük bir sınıflandırıcıdır.

Routing üç katı: düşük çözünürlüklü (256 token), orta (576), yüksek (2048+). Üretim trafiğinde sorguların %60'ı için düşük veya orta yeterlidir. Net etki: eşit kalitede 2-3x geçiş.

> **【中文解读】**ViR is deployment optimization: Bir küçük sınıflandırma makinesi en düşük çözünürlükle kodlama öncesi tahmin sorguları gerektirir.

> **【拓展：ViR 与金融场景】**Finansal dosya işleme sırasında, sorguların büyük kısmı ("Bu张发票的总额是多少") sadece düşük çözünürlük gerektirir, ancak OCR yoğun görevleri ("提取所有行项目") yüksek çözünürlük gerektirir.

### Çıkarılmış Görüş Dil Deployment (DvD) 解视觉-语言部署

Büyük bir VLM'ye hizmet verdiğinizde, görüntü kodlayıcı bir görüntü başına bir kez çalışır ancak LLM her çıkış jetonu için autoregressively çalışır. İki bileşen farklı şişlik boynuzları vardır (görüş = GPU bellek bant genişliği için conv + dikkat; LLM = KV önbelleği).

8B + 400M kodlayıcı modeli için, DvD, düğüm başına çıkış oranı ile birlikte yerleşik oranı yaklaşık olarak ikiye katlanır.

> **【中文解读】**DVD, video kodlayıcı ve LLM'nin farklı GPU'larda dağıtılması, akışlı nakliye bağlantıları yoluyla.

### Tek aşama vs. çok aşama kalitesi .

InternVL3'in ana referans iddiası: 78B paramlarda, Gemini 2.5 Pro'nun MMMU-Pro'yla eşleşir. 38B'de, GPT-4o ile eşleşir. 8B'de, açık-8B liderlik tabloyu liderlik et. Hepsi tek aşamalı bir tren öncesi + talimat-tune tarifi üzerine.

Düzeltme borcu hipotezi ölçülebilir: InternVL3-8B, görme-benchmark kazanç biriminden daha az metin değer puanı (MMLU, GSM8K) kaybeder.

> **【中文解读】**InternVL3-8B Her bir görsel basıncı oranının yükselmesi, kaybı için basıncı oranı Qwen2.5-VL-7B azı.

### InternVL3.5 ve InternVL-U

InternVL3.5 (Avgust 2025) tarihini ölçeklendirir. Aynı yerel önceden eğitim yaklaşımı, daha fazla veri, daha fazla param. MMMU geliştirmeleri artışsaldır.

InternVL-U (2026) aynı omurganın üzerine MMDiT başlıkları üzerinden birleşik nesil  görüntü çıkışı ekler. "U" Transfusion tarzı birleşik modelleri kovalayan "Anlama + nesil" anlamına gelir (Denevi 12.13). Aynı yerel önceden eğitilmiş omurgan hem anlayış hem de nesil başlıklarını destekler.

> **【中文解读】**InternVL-U(2026) aynı kemik üzerinde görüntü üretme yeteneğini katmıştır MMDiT 头 (MMDiT 头) yoluyla), Transfusion 风格的理解+生成统一模型──同一预训骨干同时支持理解和生成──

### Doğal eğitimden önce yapılan alışverişler.

Doğal öncesi eğitim ücretsizdir:

- Bilgisayar / 计算. Yeni bir VLM'yi sıfırdan eğitmek, metin bir LLM eğitimi ile aynı maliyeti taşır.  milyonlarca GPU saat. Post-hoc uyarlaması mevcut LLM ağırlıklarını yeniden kullanır, maliyetin çoğunu tasarruf eder.
- Veriler / 数据. Ölçüsünde birbirine karışan görüntü-metin korpusları nadirdir. OBELICS 141M belgeler; MMC4 571M. Tekest tek başına 15T jetonlarında gönderir. Multimodal önceden eğitim verileri kıtlığı zor bir zorluktur.
- Basis-LLM yeniden kullanımı / 基础LLM复用. Doğal öncesi eğitim daha sonra yeni bir LLM'yi bırakma seçeneğini bırakır. Post-hoc yalnızca adaptörü yeniden eğiterek Llama-3.1 ile Llama-4'e değişmenizi sağlar.

InternVL3'ün yaptığı bahis: Düzeltme borcu yeniden kullanım kaybından daha kötüdür. Benchmarks iddiayı destekler. Üretim maliyeti gelecek laboratuvarları ucuz kopyalamaktan engeller. Post-hoc VLM'ler mevcut olmaya devam edecek çünkü çoğu proje için daha ucuz kalırlar.

> **【中文解读】**InternVL3'ün 注:                                                                                                                                                                                                                                                          

## Kullanın.
```figure
l5-native-pretrain
```

## Kullan

`code/main.py`Eğitim-korpus karıştığı ve ViR yönlendirme simülatörüdür.

- Hedef korpus karışımı (% metin, %interleaved, %caption, %video) alır ve modalite başına beklenen adımları hesaplar.
- Bir dizi sorguda ViR yönlendirmeyi simüle eder (paylama: 50% düşük detaylı, 30% ortalama, 20% yüksek detaylı) ve ortalama token sayısını rapor eder.
- DvD'nin üretimi tahminlerini rapor ediyor.
- Post-hoc vs. yerli ön eğitiminin birbiriyle birbiriyle param, hesaplama, veri ve beklenen uyum-borç semptomlarını basıyor.

## Gönderin.

Bu ders bize çok yararlı .`outputs/skill-native-vs-posthoc-auditor.md`Önerilen VLM eğitim planı göz önünde bulundurularak, yerel veya post-hoc olup olmadığını denetlemektedir, uyumlulık- borç riskini belirler ve bir corpus karışımı önerir.

> **【中文解读】**Bu ders çıkıyor "Original vs 后装审计工具"──给定 VLM 训练计划,评估应走原生还是后装路线,标记对齐债务风险,推语料混合比例──

## Egzersizler.

1. InternVL3-8B (doğal tren öncesi) ve LLaVA-OneVision-7B (post-hoc) arasındaki hesaplama delta'sını tahmin edin.
   | 估算 InternVL3-8B（原生预训练）和 LLaVA-OneVision-7B（后装）的计算量差距。GPU 小时比率大约多少？什么解释了这个差距？

2. InternVL3 %40 metin / %35 birbirine karışık / %20 başlık / %5 video rapor ediyor. Eğer hedef göreviniz video ağırsa, yeni bir oran önerin ve temel modelin neden hala önemli metin ve başlık verilerine ihtiyacı olduğunu tartışın.
   | InternVL3 的语料比例是 40/35/20/5。如果目标任务是视频密集的，提出新比例，论证为什么基础模型仍需要大量文本和描述数据。

3. MM1.5 4. bölümünü okuyun unutma. Post-hoc eğitiminin en büyük gerileme gösterdiği tam referans değerini söyleyin. Gerileme maliyeti ne kadar?
   | 阅读 MM1.5 第 4 节关于遗忘的内容。指出后装训练在哪个基准上退化最大？退化了多少？

4. ViR trafiğin %60'ını düşük çözünürlüklü kodlama yönlendirir. Hangi sorguları yanlış yönlendirir (yüksek çözünürlük gerekirse düşük çözünürlüklere gönderir)?
   | ViR 将 60% 流量路由到低分辨率。哪些查询会被错误路由（需要高分辨率却发了低分辨率）？提出三种路由失败模式。

5. DvD görme ve LLM'yi ayrı GPU'lara ayırır. Hangi trafik kalıbı altında DvD, yardımı yerine geçiş hızını inceler?
   | DvD 将视觉和 LLM 分到不同 GPU。在什么流量模式下 DvD 反而降低吞吐量？

## Anahtar Terimler

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| Native multimodal pretraining | "From scratch together" | Text + image + video tokens participate in the loss from step 1, not bolted on later | 从第一步就将文本+图像+视频 token 纳入损失函数 | |
| Alignment debt | "Post-hoc penalty" | Measurable regression in text skills and answer consistency that comes from bolting vision onto a frozen LLM | 后装 VLM 带来的文本技能退化和回答一致性下降 | |
| V2PE | "Variable visual pos encoding" | Per-modality learnable position encoding allocation; InternVL3's M-RoPE successor | 按模态类型可学习的位置编码分配 | |
| ViR | "Resolution router" | Small classifier that picks minimum resolution needed per query before encoding, saving inference tokens | 编码前选择最低所需分辨率的小型分类器 | |
| DvD | "Decoupled deployment" | Vision encoder on one GPU, LLM on another, with stream handoff; doubles throughput for large VLMs | 视觉编码器和 LLM 分 GPU 部署，流式传输连接 | |
| InternVL-U | "Unified understanding + generation" | 2026 follow-up that adds image-generation heads to the native-pretrain backbone | 在原生预训练骨干上加入图像生成头的统一模型 | |
| Interleaved corpus | "OBELICS / MMC4" | Documents with text and images in natural reading order; the raw material for native pretraining | 文本和图像按自然阅读顺序交织的文档语料 | |

## Daha fazla okumak

- [Chen et al. — InternVL 1 (arXiv:2312.14238)](https://arxiv.org/abs/2312.14238)InternVL'nin ilk kuşağı.
- [Zhu et al. — InternVL3 (arXiv:2504.10479)](https://arxiv.org/abs/2504.10479)♬ InternVL3 İlk yaşam öncesi eğitim
- [InternVL3.5 (arXiv:2508.18265)](https://arxiv.org/abs/2508.18265)InternVL3.5 boyut genişleme
- [InternVL-U (arXiv:2603.09877)](https://arxiv.org/abs/2603.09877)# InternVL-U anlamak + birleştirme oluşturmak
- [Zhang et al. — MM1.5 (arXiv:2409.20566)](https://arxiv.org/abs/2409.20566)MM1.5 Borç ölçümleri
