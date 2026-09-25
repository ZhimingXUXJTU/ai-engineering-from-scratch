# LLaVA-OneVision: Tek Resim, Çok Resim, Tek Modeldeki Video

> LLaVA-OneVision'dan önce (Li et al., Ağustos 2024) açık VLM dünyası ayrı soylara sahipti: Tek görüntüler için LLaVA-1.5, Mantis ve VILA gibi çok görüntü modeli, Video-LLaVA ve Video-LLaMA gibi video modeller. Her biri kendi referansını kazandı ve diğerlerinde başarısız oldu. LLaVA-OneVision, tek bir ders programının üç senaryoda da egemenlik gösterebilecek bir model yetiştirebileceğini ve ortaya çıkan görev transfer etkilerinin (tek görüntü becerileri videoya ihraç edilir, çok görüntü mantıklamaları tek görüntüye ihraç edilir) uzmanların toplamını yendiğini savundu. Reçet yanıltıcı bir şekilde basit: senaryolar boyunca sabit kalan görsel bir belirti bütçesi, ek olarak tek görüntüden OneVision (çok görüntü) videoya geçen açık bir ders programı. Bu ders bütçeyi, ders programını ve ortaya çıkan davranışları okur.

> **【中文解读】**LLaVA-OneVision'un temel katkıları: Birleştirilmiş bir görsel token ile  bütçe (yaklaşık 3000-4000 token) ve üç aşamalı bir ders çalışması (tek resim→多图→视频), aynı zamanda üç farklı durumun modelini geliştirmeyi eğitmek.

> **【拓展：统一多模态模型的产业价值】**Gerçek ürünler arasında, kullanıcı aynı anda tek bir resim, bir çok resim ve video taşıyabilir. Üç bağımsız modelin maliyetinin bir tek resim, bir çok resim ve bir video üzerinde işlem yapması için LVA-OneVision'un "sağlama token bütçesi" stratejisi maliyetlerin tahmin edilebilmesini sağlıyor.

**Type:** Build  | **类型：构建**
**Languages:** Python (stdlib, token budget solver + curriculum planner)  | **语言：Python（标准库，token预算求解器 + 课程规划器）**
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 12 · 06 (any-resolution)  | **前置：阶段12第05课（LLaVA）、阶段12第06课（任意分辨率）**
**Time:** ~180 minutes  | **时长：约180分钟**

>  **【前置】**Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemlik Önemli Önemlik Önemlik Önemlik Önemlik Önemlik Önemlik Önemlik Önemlik Önemlik Önemlik Önemlik Önemlik Önemlik Önemlik Önemlik Önemlik Önemlik Önemlik Önemlik Önemlik Önemlik Önemlik Önemlik Önemlik
>  **【类比】**LLaVA-OneVision = "全能瑞士军刀"。 diğer VLM = 专门的单功能刀(单图刀、多图刀、视频刀)。瑞士军刀的每个功能都不如专业刀精专,但能应对未知场景;维护一个统一代币 预算(3000-4000) = 子和刀片的总长度恒定,根据场景切换主功能──

## Öğrenme hedefleri

- Tek görüntü, çok görüntü ve video girişleri boyunca sabit olan görsel jeton bütçesini tasarlayın.
- Tek görüntüden videoya yetenekleri felaketsiz unutmadan aktaran bir eğitim programı sipariş edin.
- Bir tek model neden aynı parametreler sayısında uzmanlardan daha üstün olduğunu açıklayın.
- LLaVA-OneVision tarafından bildirilen üç yeni yetenek adı: çoklu kamera akıl yürütme, işaretleme uyarısı, iPhone ekran görüntüsü ajanı.

## Sorun  sorun arka planı

Resim, çoklu görüntü ve video her biri farklı bir model üzerinde durur.

Tek görüntü, OCR ve ince ayrıntıları yakalamak için yüksek çözünürlüklü jetonlar (AnyRes, ~ 2880 görsel jetonlar) ister.

Multi-image, orta çözünürlükte birkaç görüntü istiyor (her biri yaklaşık 576 token) bu nedenle görüntüler arasındaki mantık bağlamına uymaktadır.

Video, zamansal dinamikleri yakalamak için düşük çözünürlükte (bir çerçeveye bir araya getirildikten sonra yaklaşık 196 token) birçok çerçeve ister.

> **【中文解读】**Üç farklı durumlara karşı token  bütçe ihtiyacı: tek tablo yüksek çözünürlükle (((2880 token), çok tablo ortalama çözünürlükle (((576 token), video düşük çözünürlükle ama çok fazla (((196 token) 😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁😁

Ayrı modeller eğitirseniz, tek bir bütçe seçersiniz.

Pre-OneVision, varsayılan cevap "bir senaryoyu eğit, diğerlerini görmezden gelin". Video-LLaVA, videoyu ek eğitim aşamalarıyla birlikte bir görüntü modeline yeniden ayarladı. LLaVA-NeXT, kapaklama ile çoklu görüntü desteği ekledi.

## Konsepten bir şey.

### OneVision token bütçesi OneVision token bütçesi

LLaVA-OneVision, örnek başına yaklaşık 3000-4000 tane görsel jeton bütçesini seçer ve senaryo başına farklı olarak tahsis edilir:

- Tek görüntü / 单图: AnyRes-9 (3x3 bez + küçük resim), her bez 384'e 729 yama ile, saldırgan bilineer birleştirme 2x2 → 182 per bez. Toplam: 9 * 182 + 182 = 1820 jeton.
- Çoklu görüntü / 多图: her görüntü orta çözünürlükte (384, kapaklama yok), birleştirme olmadan 729 token.
- Video / 视频: 32 çubuk 384 çözünürlükte agresif 3x3 bilinear havuz → 81 token per frame.

Bu, bir programın entegre edilmesi için kullanılan bir programdır.

> **【中文解读】**核心思想:总代币 预算保持恒定(约3000-4000), fakat dağıtım biçimi olaylara göre farklıdır.

### Üç aşamalı ders programı.

LLaVA-OneVision trenleri üç aşamada:

1. Tek görüntü SFT (sare SI) / 单图指令微调. Tüm veriler tek görüntü artı metindir. Yüksek çözünürlüklü AnyRes girişleri üzerinde eğit. Bu algıyı, OCR'yi ve ince ince ince anlayışı öğretir. LLaVA-NeXT verilerini ek olarak OneVision spesifik tek görüntü verilerini kullanır.
2. OneVision SFT (sare OV) / 统一指令微调. Tek görüntü + çok görüntü + video (birbir şekilde örneklenmiş çerçeveler) karıştır. Tek bir token bütçesine göre eğitim verin. Bu, modelin heterogen parti şekilleri ile başa çıkmasını öğretir.
3. Görev transfer (stage TT) / 任务迁移. Genellikle ürünlere bağlı olarak çoklu görüntü veya video üzerinde daha ağır olan hedef görev karışımı ile devam edin.

Kritik: kurikulum düzeninin önemi. Video-birincisi veya çoklu görüntü-birincisi eğitim aynı verilerle bile tek görüntü-birincisi daha kötü görüntü performans üretir. Kağıt bunu açıkça ortadan kaldırır.

> ️ **【易错点】**Kendi kendini eğitmek birleştirmek VLM 时课程序列搞反了(先训视频再训单图)→ 单图性能大幅下降──原因:视频低分辨率输入让模型先学到"模糊是正常的",再训高分辨率单图时模型适应不过来──修复:必须单图 → 多图 → 视频的序列,先学精细再学粗──
> 🤔 **【困惑】**S: Neden sabit token  bütçe bu kadar önemli? Çünkü LLM'nin üst aşağıdaki penceresi sabit, tek tablo birden 5000 token 、 video 10000 token olacak batching yıkmak 和推理预算── sabit bütçe = tahmin edilebilir tahmin maliyeti, ürün dağıtımının anahtarıdır──

> **【中文解读】**课程顺序至关重要:先单图、再多图+视频、最后任务迁移── eğer önce video veya多图 eğitimi alırsa,单图性能会下降── çünkü单图 eğitimi duyusal temel oluşturur,多图和视频'nın zaman/spaces düşüncesinin temelinde olması gerekir──

### Neden kurikulum işe yarıyor ?

Tek görüntü eğitimi algılama tabanını oluşturur. Patch tokenleri ince ince ince görsel özelliklere sahiptir; LLM onları metinle entegre etmeyi öğrenir. Çoklu görüntü ve video güçlü algılama tabanı olmadan öğrenmek zor olan yapısal zorluklar (ne görüntü, hangisi ilk oldu) sunar.

Eğer tüm senaryoları sıfırdan birlikte eğitirseniz, model algılama (her parti için sınırlı tek görüntü verileri) ve aşırı yapı (çok fazla görüntü / video verileri) ile uyumludur. Sonuç: çapraz görüntü mantık kalıplarını izleyen ancak görsel olarak yüzeysel bir model.

Eğitim düzenlemesi, SI aşamasından algı gücünü, OV aşamasından dahi/zamansal akıl yürütmeyi verir, hiçbirini kaybetmeden.

> **【中文解读】**Eğer tüm olayları aynı anda eğitirsek, model, algılama kapasitesini eksiktirse, daha fazla yapı ile uyumlu olur. Bu da modelin resim üzerinde düşünmesine neden olur.

### Yeni gelişmiş senaryolar arası yetenekler

LLaVA-OneVision makalesinde üç yeni yetenek rapor edildi:

1. Çoklu kamera akıl yürütme / 多摄像头推理. Çoklu görüntü + video üzerinde ayrı olarak eğitilmiş; sonuç olarak, çoklu kamera sürüş sahnesi hakkında akıl yürütmek istenmiştir.
2. Seti işaret istekleri / 标记提示. Kullanıcı numaralı işaretlerle bir görüntüdeki nesneleri not eder; model "7 işaretine göre 3 işaret ne yapıyor" hakkında mantıklar verir.
3. iPhone ekran görüntüsü ajanı / 手机截图代理. Kullanıcı bir iPhone ekranının ekran görüntüsünü sağlar ve bir sonraki tıklama planlamasını ister. UI ekran görüntüleri, kullanıcı iş akışlarının videoları ve çiftlerden önce / sonra çoklu görüntü üzerinde eğitim almıştır.

Bunlar eğitimli görevler değil; onlar kurikulumun yapısı yapısından kaynaklanmaktadır.

> **【拓展：涌现能力的工程启示】**涌现能力, bir bütünliğin değerini farklı uzmanlardan öte ifade eder. 涌现能力, güvenlik denetimi, otomatik sürüş için kullanılabilir bir çok fotoğraf düşünme yeteneği, görüntü işaretleme aracı olarak kullanılabilir bir işaretleme ipucu, mobil kesim aracı olarak UI otomatikleştirme testleri için kullanılabilir. Bunlar açıkça eğitilmiş değil, ders öğrenilmesinin "karşı ürünleri"dir.

### Görsel-sıkıntılı birleştirme

Token bütçesi birleştirmeyi gerektirir. OneVision 2D yama şebekesinde çift çizgili interpolasyon kullanır: 24x24 = 576 yama 12x12 = 144 (2x faktörü) veya 8x8 = 64 (3x faktörü) olur. Birleştirme yerleşimi korumak için token boşluğu değil, yama şebekesi alanında yapılır.

Szenaryo başına birleştirme faktörünün seçimi kendiliğinden bir hiperparametre. Daha az birleştirme = daha fazla token = daha zengin bir temsil. Daha fazla birleştirme = daha az token = daha fazla çerçeve / görüntü uyumlu.

> **【中文解读】**池化在2D 补丁网格空间进行 (而非 token 空间),空间局部性保留为而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而而

### LLaVA-OneVision-1.5

2025 takip (LLaVA-OneVision-1.5, arXiv 2509.23661) eğitim verileri, model ağırlıkları ve kodlarında "tamamen açık"dır. Bazı referans değerlerinde sahiplik boşluğu karşılaştırır ve tarifi demokratikleştirir. Aynı ders planı, daha fazla veri, daha iyi bir LLM tabanı. mimarlık değişimi yoktur.

### Qwen2.5VL ile karşılaştırıldığında.

Qwen2.5-VL (Desin 12.09) farklı seçimler yapar. sabit birleştirme yerine M-RoPE ve dinamik FPS kullanır. Giriş ile bütçe ölçekleri  1 dakikalık bir video 5 saniyelik bir video ile karşılaştırıldığında daha fazla jeton kullanır. LLaVA-OneVision bütçeyi düzeltir ve birleştirmeyi ölçeklendirir. Her ikisi de çalışır; tahmin edilebilirlik için yapılandırmayı değiştirirler.

> **【中文解读】**M-RoPE ile hareketli 率,token  bütçe ile giriş ve kısaltma;LLaVA-OneVision  sabit bütçe 调整池化── iki strateji farklı avantajlara sahiptir:
```figure
l5-onevision-budget
```

## Kullan

## Kullanın.

`code/main.py`Bir OneVision tarzı VLM için bir ders planı ve bütçe planlayıcısıdır. Örnek başına bir token bütçesi ve hedef senaryo karışımı (örneğin 40% tek görüntü, 30% çok görüntü, 30% video) verildiğinde:

- Scenaryon başına çözünürlük, birleşim faktörü ve çerçeveleri ayırır.
- Her senaryoyu paylaşılan bütçeye uygun olup olmadığını kontrol eder.
- Rapor beklenen token sayısını, LLM FLOP'larını ve hangi senaryoların az tokenleşmiş olduğunu rapor ediyor.
- Eğitim programını aşama aşama basıyor.

## Gönderin.

Bu ders bize çok yararlı .`outputs/skill-onevision-budget-planner.md`. Hedef görev dağılımı ve örnek başına bütçe göz önüne alındığında, AnyRes faktörü, çerçeve birleştirme, video çerçeve sayısı ve kurikulum aşama ağırlıklarını yayar.

> **【中文解读】**Bu ders bir vizyon  bütçe planlama aracı olarak üretilmiştir.

## Egzersizler.

1. Ürününüz %80 tek görüntü, %10 çok görüntü (2-4 görüntü), %10 video (8-16 çerçeve) destekler.
   | 产品支持 80% 单图、10% 多图（2-4张）、10% 视频（8-16帧）。设计 token 预算。从轻量多图中省下的预算放在哪？

2. LLaVA-OneVision Bölümü 4.3 (Yarınma yetenekleri) okuyun.
   | 阅读 LLaVA-OneVision 第 4.3 节（涌现能力）。提出课程学习可能解锁但论文未报告的第四种涌现技能。

3. Eğitim programını değiştirin  önce çok resim, sonra tek resim, sonra video tren. Hangi referansların düşeceğini ve nedenini tahmin edin.
   | 交换课程顺序——先多图，再单图，最后视频。预测哪些基准会下降以及原因。

4. Gazete, örnek başına sadece 8 çerçeve üzerinde eğitilen video referanslarını rapor ediyor. Bu, sonuçta 30 saniyelik videolara genel mi?
   | 论文报告视频基准只用每样本8帧训练。这对推理时的30秒视频泛化吗？先崩溃的是 token 预算还是时序推理？

5. 24x24 patchlerin 12x12'e binaylı birleştirilmesi, dim başına 4x azaltma anlamına gelir. stdlib Python'da birleştirmeyi uygulayın ve her 2x2 blok üzerindeki ortalamanın binaylı çıkışla eşleşmediğini kontrol edin.
   | 将 24x24 补丁双线性池化为 12x12 是每维 4 倍缩减。用标准库 Python 实现池化，验证每个 2x2 块的均值与双线性输出一致。

## Anahtar Terimler

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| OneVision scenario | "Single-image, multi-image, or video" | One of three input shapes the unified VLM handles; the budget stays constant across | 统一 VLM 处理的三种输入形态之一，预算在场景间保持恒定 | |
| Token budget | "How many tokens per sample" | Total visual tokens the LLM sees per training / inference sample, typically 3000-4000 | LLM 每样本看到的总视觉 token 数，通常 3000-4000 | |
| Curriculum | "Training order" | Stage ordering (single-image → multi-image → video) chosen for emergent transfer | 课程学习：按单图→多图→视频顺序训练，促进技能迁移 | |
| Bilinear pooling | "Token shrink" | Applying bilinear interpolation to the patch grid (2D) to reduce token count while preserving locality | 在补丁网格上做双线性插值，减少 token 数并保留空间局部性 | |
| Emergent skill | "Not trained, still works" | Capability that appears at inference without matching training data, due to curriculum composition | 课程学习组合带来的未训练即涌现的能力 | |
| AnyRes-k | "k-tile setup" | k sub-tiles of fixed resolution plus one thumbnail, typical k ∈ {4, 9} | k 个固定分辨率子切片加一个缩略图 | |
| Task transfer | "Cross-scenario generalization" | Skills learned on single-image that apply to video (and vice versa) via shared backbone | 通过共享骨干网络，单图技能迁移到视频（反之亦然） | |

## Daha fazla okumak

- [Li et al. — LLaVA-OneVision (arXiv:2408.03326)](https://arxiv.org/abs/2408.03326)LLaVA-OneVision Önemli makale
- [LLaVA-OneVision-1.5: Fully Open Framework (arXiv:2509.23661)](https://arxiv.org/abs/2509.23661)Tamamıyla açık kaynaklı bir sürüm.
- [Lin et al. — Video-LLaVA (arXiv:2311.10122)](https://arxiv.org/abs/2311.10122)Video-LLaVA  Video çok modold
- [Lin et al. — VILA (arXiv:2312.07533)](https://arxiv.org/abs/2312.07533)# VILLA + resim modeli
- [Wang et al. — Qwen2-VL (arXiv:2409.12191)](https://arxiv.org/abs/2409.12191) Qwen2-VL Referans için
