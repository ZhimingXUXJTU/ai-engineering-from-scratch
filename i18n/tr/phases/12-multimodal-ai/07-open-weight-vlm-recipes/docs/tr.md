# Açık Ağırlıklı VLM Reçepleri: Neyin Önemli Olduğu

> 2024-2026 açık ağırlıklı VLM literatürü, bir orman olarak kalır. Apple'ın MM1'i 13 görüntü kodlayıcı, bağlantı ve veri karışımı kombinasyonunu test etti. Allen AI'nin Molmo'su, detaylı insan başlıklarını GPT-4V destillasyonunu yendiğini kanıtladı. Cambrian-1 20+ kodlayıcı karşılaştırmasını yaptı. Idefics2 beş eksel tasarım alanını resmileştirdi. Prismatic VLM'ler kontrol edilen bir referans değerinde 27 eğitim tarifini karşılaştırdı. Tüm bu gürültüden, küçük bir dizi sonuç kağıt üzerinde geçerlidir: görüntü kodlayıcı bağlantı mimarisinden daha önemlidir, veri karışımı ikisinden de daha önemlidir ve ayrıntılı insan başlıkları destil edilmiş sentetik verileri yener. Bu ders bu tabloları okuyor, bu yüzden okumak zorunda değilsin.

> **【中文解读】**2024-2026 yılları açık kaynaklı VLM makalesinde çok sayıda tüketim deneyimi dolu. Bu ders Apple MM1  Allen AI Molmo  Cambrian  Idefics  Prismatic VLMs  gibi makalelerde çekirdeğe çıkarılmış: kodlayıcı, bağlantı makinesi yapısından daha önemli, veri karışımı, kodlayıcıdan daha önemli, ayrıntılı insanlık açıklaması, buhursuz veriden üstün.

> **【拓展：VLM 工程的实践指南】**Bu dersin sonucu doğrudan VLM 工程 uygulamasını yönlendirir. VLM  performansın belirsiz olduğunu fark ettiğinizde, aşağıdaki önceliklere göre sıralamalıdır: 1) görsel jeton sayısı yeterli mi? 2) kodlayıcı seçimi uygun mu? 2) %20), 3) veri kalitesi yeterli mi? 3) %10), 4) bağlantı aracının yapılandırması %5, neredeyse etkisi yoktur.

**Type:** Learn + lab  | **类型：学习 + 实验**
**Languages:** Python (stdlib, ablation table parser + recipe picker)  | **语言：Python（标准库，消融表解析器 + 配方选择器）**
**Prerequisites:** Phase 12 · 05 (LLaVA baseline)  | **前置：阶段12第05课（LLaVA基线）**
**Time:** ~180 minutes  | **时长：约180分钟**

>  **【前置】**Özetleme Yapımcılığı: Özetleme Yapımcılığı: Özetleme Yapımcılığı: Özetleme Yapımcılığı: Özetleme Yapımcılığı: Özetleme Yapımcılığı: Özetleme Yapımcılığı: Özetleme Yapımcılığı: Özetleme Yapımcılığı: Özetleme Yapımcılığı: Özetleme Yapımcılığı: Özetleme Yapımcılığı: Özetleme Yapımcılığı: Özetleme Yapımcılığı: Özetleme Yapımcılığı: Özetleme Yapımcılığı: Özetleme Yapımcılığı: Özetleme Yapımcılığı: Özetleme Yapımcılığı: Özetleme Yapımcılığı: Özetleme Yapımcılığı: Özetleme Yapımcılık: Özetleme Yapımcılık: Özetleme Yapımcılık: Özetleme Yapımcılık: Özetleme Yapımcılık: Özetleme Yapımcılık: Özetleme Yapımcılık: Özetleme Yapımcılık: Özetleme Yapımcılık: Özetleme Yapımcılık: Özetleme Yapımcılık: Özetleme Yapımcılık: Özetleme Yapımcılık: Özetleme Yapımcılık: Özetleme Yapımcılık: Özetleme Yapımcılık: Özetleme Yapımcılık: Özetleme Yapımcılık: Özetleme Yapımcılık: Özetleme Yapımcılık Özetleme Yapımcılık Özetleme Yapımcılık Özetleme Yapımcılık Özetleme Yapımcılık Özetleme Yapımcılık Özetleme Yapımcılık Özetleme Yapımcılık Özetleme Yapımcılık Özetleme Yapımcılık Özetleme Yapımcılık Özetleme Yapımcılık Özetleme Yapımcılık Özetleme Yapımcılık Özetleme Yapımcılık Özetleme Yapımcılık Özetleme Yapımcılık Özetleme Yapımcılık Özetleme Yapımcılık Özetleme Yapımcılık Özetleme Yapım Özetleme Yapımcılık Özetleme Yapımcılık Özetleme Yapım Özetleme Yap Yap Yap Yap Yap Yap Yap Yap Yap Yap Yap Yap Yap Yap Yap Yap Yap Yap Yap Yap Yap Yap Yap
>  **【类比】**开源 VLM 五轴选择 = "买车选配置"──编码器 = 发动机(性能差 5-7 分);连接器 = 中控台界面(几乎不影响驾驶);LLM = 车身大小;数据 = 油品(差油再好的发动机也跑不快);分辨率 = 轮胎(决定能跑什么地形)──纠结界面(连接器) 是新手陷,老司机优先看发动机和油。

## Öğrenme hedefleri

- Beş eksel VLM tasarım alanını isimlendirin: görüntü kodlayıcı, bağlayıcı, LLM, veri karışımı, çözünürlük programı.
- MM1 / Idefics2 / Cambrian-1 ablation tablosunu okuyun ve hangi düğmenin belirli bir referans değerini hareket ettirdiğini tahmin edin.
- Yeni bir VLM için bir tarif seçin (kodlayıcı, bağlantı, veri, çözünürlük) hesaplama bütçesi ve görev karışımı verildiğinde.
- Neden detaylı insan başlıkları aynı token sayısında GPT-4V destillasyonunu yendiğini açıkla.

## Sorun  sorun arka planı

Yüzlerce açık ağırlıklı VLM var. "iyi" ve "yağnalı" arasındaki boşlukların çoğu mimarlık değil. Veriler, çözünürlük programı ve kodlama seçeneği.

2023 dalgası (LLaVA-1.5, InstructBLIP, MiniGPT-4) başlık çift öncesi eğitim + LLaVA-Instruct-150k üzerinde çalıştı. İyi başlangıç çizgisi. MMMU'nun% 35 civarında zirve aldı.

2024 dalgası (MM1, Idefics2, Molmo, Cambrian-1, Prismatic VLMs) son derece kapsamlı bir şekilde sonuçlandı.

> **【中文解读】**Yüzlerce açık kaynaklı VLM'de, "iyi" ve "en iyi" arasındaki fark temel olarak yapı değil, veri, çözünürlük düzenleme ve kodlayıcı seçimi. Bilin modelin belirlenmediğinde hangi parametreleri ayarlamak, 500 milyon GPU zaman kaybı önleyebilir. 2023 yılındaki LLaVA-1.5 ve diğer VLM'ler MMMU'da% 35 civarında durdu. 2024 yılındaki MM1 ‒ Molmo ve diğer sistemli bir şekilde giderme deneyleri önemli faktörleri ortaya koydu.

## Konsepten bir şey.

### Beş eksel tasarım alanı.

Idefics2 (Laurençon et al., 2024) ekselerin adını verdi:

1. Görüntü kodlayıcı / 图像编码器. CLIP ViT-L/14, SigLIP SO400m/14, DINOv2 ViT-g/14, InternViT-6B. Kodlayıcılar yama boyutunda, çözünürlükte ve eğitim öncesi hedefte farklıdır.
2. Bağlantı / 连接器. MLP (2-4 katman), Q-Former (32 sorgu + çapraz atn), Perceiver Resampler (64 sorgu), C-Abstraktor (konvolyüsyonal + bilinear birleştirme) / MLP(2-4 kat)、Q-Former(32 sorgu +交叉注意力)、Perceiver 重采样器(64 sorgu)、C-Abstraktor(卷积+双线性池化).
3. Dil modeli / 语言模型. Llama-3 8B / 70B, Mistral 7B, Phi-3, Gemma-2, Qwen2.5. LLM boyutu baskın param maliyet / LLM 大小是主要参数成本.
4. Eğitim verileri / 训练数据. Başlık çiftleri (CC3M, LAION), birbirine karışık (OBELICS, MMC4), talimat (LLaVA-Instruct, ShareGPT4V, PixMo, Cauldron) / 描述对、交错数据、指令数据.
5. Çözüm programı / çözünürlük düzenlemesi. sabit 224/336/448, AnyRes, yerli dinamik. eğitim sırasında hızlandırılmış veya sabit / 固定分辨率、AnyRes、原生動态分辨率── eğitim sırasında giderek veya sabit.

Her üretim VLM'si her eksede bir seçim yapar. MMMU puanlarının çoğu farkı hangi bağlayıcıyı seçtiğiniz değil 1, 4 ve 5  ekselerle açıklanır.

> **【中文解读】**Her VLM beş aksel üzerinde seçilir. MMMU bölümünün büyük bölümü aksel1 (kodlayıcı) ⋅ aksel4 (date) ⋅ aksel5 ( çözünürlük) tarafından açıklanır. Bu, paranın daha iyi kodlayıcı ve daha iyi verilere harcanması anlamına gelir.

### Axis 1: Kodlayıcı > Bağlantı

MM1 Bölüm 3.2 gösterdi: CLIP ViT-L/14'den SigLIP SO400m/14'e değişmek 3+ MMMU puanı ekledi. MLP'den İhtiyaçlı Kaynaklayıcı Yeniden Örnekleyici'ye bağlantı değiştirmek 1 puandan az ekledi. Idefics2 aynı token sayısında tekrarlandı: SigLIP > CLIP, Q-Former ≈ MLP ≈ İhtiyaçlı Kaynaklayıcı.

Cambrian-1'in "Cambrian Vision Encoders Match-Up" (Tong et al., 2024) 20+ kodlayıcıyı görme merkezli bir referans (CV-Bench) üzerinde çalıştı. Lider tablosunun en üst kısmı DINOv2 ve SigLIP'in bir karışımıdır; CLIP paketin ortasındadır; ImageBind ve ViT-MAE daha düşüktür. CLIP ViT-L'den DINOv2 ViT-g/14'e arasındaki fark CV-Bench'de ~ 5-7 puandır.

Açık VLM'ler için 2026'da varsayılan kodlayıcı, semantik + yoğun özellikler için SigLIP 2 SO400m/14'dir, bazen DINOv2 ViT-g/14 özellikleriyle bağlanır (Cambrian'ın "Spatial Vision Aggregator" bunu yapar).

> **【中文解读】**换编码器(CLIP→SigLIP)加3+ 分 MMMU,换连接器(MLP→Perceiver)加不到1分──2026年开源 VLM'in默认编码器 is SigLIP 2 SO400m/14,有时与DINOv2 ViT-g/14 拼接(Cambrian'ın"空间视觉聚合器"就是这样做的)──

> ️ **【易错点】**Yeni insanlar "调连接器架构" tuzağına düştüler. Eski Q-O daha iyi olduğu için daha değerli araştırmaya değer.

### Axis 2: Bağlantı tasarımı bir yıkama. Bağlantı tasarımı neredeyse hiçbir etkisi yok.

MM1, Idefics2, Prismatic ve MM-Interleaved hepsi aynı sonuca vardı: sabit bir görsel-token sayısında, bağlayıcı mimarisi neredeyse önemli değildir. Ortalama birleştirilmiş yamalardaki iki katlı MLP, aynı token bütçesinde 32 sorgu Q-Former'ın 1 puan içinde çalışır.

Önemli olan, simgelerin sayısıdır. Daha fazla görsel simgeler = daha fazla LLM hesaplama = bir noktaya kadar daha iyi performans, sonra da azalır. Resim başına 64 simgeler OCR için çok azdır. 576-1024 simgeler çoğu açık VLM için tatlı noktadır. 2048+ yalnızca belgelere ve grafiklere yardımcı olur.

Q-Former vs. MLP, bir kalite sorusu değil, bir maliyet sorusu: Q-Former, görüntü çözünürlüğüne bakılmaksızın jetonları 32-64'e kapatır; MLP tüm patch jetonlarını yayar. Yüksek çözünürlüklü girişler için, Q-Former LLM bağlamını korur; düşük çözünürlükler için, fark gürültüdür.

> **【中文解读】**Sıkı görsel token sayısı altında, bağlantı makinesi yapısı neredeyse performansını etkilemez.2. kat MLP ve 32. sorgu Q-Former'ın farkı 1 dakika içinde.

### Axis 3: LLM boyutu tavanı belirler LLM

LLM'yi 7B'den 13B'ye iki katlamak, her VLM kağıdı boyunca MMMU'da güvenilir bir şekilde 2-4 puan ekler. 70B'de çoğu referans değerini doymuş olursunuz. VLM'nin multimodal akıl yürütme tavanı LLM'nin metin akıl yürütme tavanıdır.

Bu nedenle Qwen2.5VL-72B ve Claude Opus 4.7 MMMU-Pro ve ScreenSpot-Pro'yu ezdi: dil beyni büyüktür. 7B VLM akıllı bağlantı tasarımıyla 70B VLM'yi değiştiremez.

> **【中文解读】**LLM 翻倍(7B→13B)稳定增加 2-4 分 MMMU──70B 时大多数基准和──VLM'in多模态推理天花板就是LLM'in文本推理天花板视觉编码器只能""数据,不能取代推理──这就是为什么72B 参数的VLM 能压7B的语言大脑的规模不可替代的原因──

### Axis 4: Veri  Detaylı insan başlıkları destillasyonu yendi DATA: AI Description

Molmo + PixMo (Deitke et al., 2024) herkesin okuması gereken 2024 sonucu. Allen AI'nin insan notatörleri, görüntüleri 1-3 dakikalık yoğun konuşma metin geçişlerinde tanımladı ve 712K yoğun başlıklı görüntüler verdi. Eğitim verilerinde hiçbir yerde GPT-4V destilasyonu yoktu.

Molmo-72B, 11 değerden 11'ünde Llama-3.2-90B-Vision'ı yendi. Delta mimarlık değil  başlık kalitesi. Detaylı insan başlıkları kısa web başlıklarından 5-10 kat daha fazla bilgi içerir ve GPT-4V destillasyon halüsinasyonları olan gerçekleri yerleştirir.

ShareGPT4V (Chen et al., 2023) ve Cauldron (Idefics2) aynı oyun kitabı ile karışık insan + GPT-4V başlıkları ile takip etti.

> **【中文解读】**Molmo'nun temel bulguları: İnsan işaretleyicilerinin 1-3 dakikalık yoğun sesli bir tanımlama görüntü kullanmasını sağlamak, 712K 张高质量标注图像, tamamen GPT-4V 蒸──Molmo-72B 11/11 基准 üzerinde Llama-3.2-90B-Vision'i yendi. Aralık yapı değil  is tanımlama kalitesi── detaylı yapay tanımlama her bir resimdeki bilgi miktarı kısa ağ tanımlamasının 5-10 katı, ve gerçek doğru, GPT-4V  DATA会"ın ardından gerçekleşen bir görüntü──

> **【拓展：数据质量的投资回报】**Bu bulgu, dikey alanın inşaatında VLM için önemli bir ilham kaynağıdır: Yüksek kaliteli alan verileri elde etmek için çok fazla hesaplama gücü harcanan yapılandırma ile birlikte, kaynaklar harcanmak gibi değildir. Finansal sahada, profesyoneller tarafından işaretlenmiş raporlar, göndermeler, sözleşme resimleri ile tarif edilen, GPT-4V otomatik olarak üretilen verilerin etkisi daha iyi olacaktır.

### Axis 5: çözünürlük ve zamanlama, çözünürlük ve düzenleme.

Idefics2'in ablations: 384 -> 448 1-2 puan ekler. 448 -> 980 görüntü bölüşümü (AnyRes) ile OCR referans değerlerinde 3-5 daha ekler. Orta doğrulukta düz çözünürlüklü eğitim platoları; çözünürlük ramping (başlamak 224, bitirmek 448 veya yerli) trenleri daha hızlı ve daha yüksek sonuçlar.

Cambrian-1 çözünürlük karşı tokenler arasında bir ticaret gerçekleştirdi: sabit hesaplamalarda daha düşük çözünürlükte daha fazla token veya daha yüksek çözünürlükte daha az token olabilir.

2026 üretim tarifi: OCR ağır görevler için 1. aşama 384 sabit, 2. aşama 1280'e kadar dinamik çözünürlükle tren.

> **【中文解读】**Çözüm oranı 384'den 448'e yükseldi 1-2'e, 448'e, 980'e kadar (Anares artı) OCR'de yeniden 3-5'e katıldı. Çözüm oranı artış düzenlenmesi. 224'den başlayarak 448'e kadar veya orijinal çözünürlük sonuna kadar.

### Prismatic kontrol karşılaştırması Prismatic kontrol karşılaştırması deney

Prismatic VLMs (Karamcheti et al., 2024) tüm ekseleri kontrol eden makaledir. Aynı 13B LLM, aynı talimat verileri, aynı değerlendirme  bir seferde sadece bir eksel değişir. Sonuçlar:

- Resim başına görsel-tıkona sayısı %60'lık değişimi açıklıyor.
- - Bu bir kodlama seçeneği.
- Bağlantı mimarisi %5'i açıklıyor.
- Diğer her şey (veriler karışımı, programcı, LR) kalan %15'i açıklıyor.

Bu kaba bir parçalanma, ama edebiyatta "neyi öncelikle temizlemem gerekiyor" diye sorulan en temiz cevap.

> **【中文解读】**Prismatic VLM'ler en temiz kontrol deneyidir Aynı 13B LLM Aynı talimat verileri Aynı değerlendirme, her seferinde sadece bir çerçeve değişir Sonuç: Görüş simgesi sayı(60%)> 编码器(20%)> 其余(15%)> 连接器(5%)── bu " önce消融什么" için en iyi yanıt olacaktır。

### 2026 için bir seçmen. 2026 yıl önerisi.

Kanıtlara göre, 2026'da yeni bir proje için standart açık VLM tarifi:

- Kodlayıcı / 编码器: SigLIP 2 SO400m/14 NaFlex ile yerel çözünürlükte, bölünme / yerleştirme / 如需分割/定位则拼接 DINOv2 için yoğun özellikler için DINOv2 ViT-g/14 ile bağlanmıştır.
- Bağlantı / 连接器: Patch tokenlerinde iki katlı MLP. Token kısıtlı / 除非 token 受限否则跳过 Q-Former olmadıkça Q-Former'i atlayın.
- LLM / 语言模型: Qwen2.5 / Llama-3.1 / Gemma 2, 7B maliyet için / 成本优先选7B, 70B kalite için / 质量优先选70B, hedef gecikme / 按延迟目标选择 ile seçilir.
- Veriler / 数据: PixMo + ShareGPT4V + Kağız, görev-specifik talimat verileri / 補充任务特定指令数据 ile tamamlanmıştır.
- Çözüm / 分辨率: dinamik (min 256, uzun taraf başına maksimum 1280 piksel) / 动态(minimum256,最大1280像素每长边).
- Program / 调度: Etap 1 düzeltme (sadece projektor / 仅投影器), Etap 2 tam ince ayarlama / 全参数微调, Etap 3 görev-özel ince ayarlama / 任务特定微调.

Bu standartların her biri bu ders sonunda alıntılanan makalelerde ölçülen bir ablation'a kadar uzanır.

> **【中文解读】**Bu ders alıntılanan makalede geçen her bir defacıl seçim, yeni bir VLM projesinin 2026 yılındaki en iyi başlangıç noktası olarak görülebilir.

## Kullanın.
```figure
l5-vlm-recipe-knobs
```

## Kullan

`code/main.py`MM1 ve Idefics2 ablation tablolarını kodlar ve sorguya izin verir:

- "Büjet X ve görev Y'yi göz önüne alırsak, hangi tarif kazanır?"
- "7B Llama'da SigLIP'i CLIP'e değiştirirsem, beklenen MMMU delta nedir?"
- "% 80 güvenli bir cevap için önce hangi ekseni kapatmalıyım?"

Çıkış, beklenen referans değerleri ve "ablate first" tavsiyesi ile sıralanmış bir tarif listesidir.

## Gönderin.

Bu ders bize çok yararlı .`outputs/skill-vlm-recipe-picker.md`. Hedef görev karışımı, hesaplama bütçesi ve gecikme hedefi göz önüne alındığında, her seçimi haklı çıkaran ablasyonu alıntılayan bir tüm reçete (kodlayıcı, bağlayıcı, LLM, veri karışımı, çözünürlük programı) yayınlar. Mühendislerin yeni bir VLM projesi başladığında Idefics2 ablasyon tablosunu yeniden icat etmesini engeller.

> **【中文解读】**Bu ders çıktı VLM  biçim seçimi araçları。 verilen hedef görev kümesi、 hesaplama bütçesi ve gecikme hedefleri, çıkış tam biçimleri, her seçimi de birlikte birlikte birlikte makale giderim deneyimi alıntıları。 kaçınmak mühendisler her yeni başlayan VLM  projesi yeniden yapmak gerekir İdeyalar2  giderim tablo。

## Egzersizler.

1. MM1 Bölüm 3.2. 50 milyon görüntü bütçesi ile sabit bir 2B LLM için hangi kodlayıcı kazanır?
   | 阅读 MM1 第 3.2 节。在固定 2B LLM 和 50M 图像预算下，哪个编码器最优？在 13B LLM 时答案会翻转吗？为什么？

2. Cambrian-1, DINOv2 + SigLIP'i birleştirmenin görme odaklı referans değerlerinde tek başına üstün olduğunu, ancak MMMU'da herhangi bir sinyal eklemediğini buldu.
   | Cambrian-1 发现 DINOv2+SigLIP 拼接在视觉中心基准上优于单独使用，但在 MMMU 上无增益。预测哪些基准提升、哪些持平。

3. Hedefiniz 2B LLM'de mobil bir UI ajanı. Kodlayıcı, bağlantı, çözünürlük ve veri karışımı seçin. Her seçeneği belirli bir ablation tablosu ile haklı çıkarın.
   | 目标是在 2B LLM 上构建移动端 UI 代理。选择编码器、连接器、分辨率和数据混合，用具体消融表论证每个选择。

4. Molmo 4B ve 72B modellerini üretir. 4B kapalı 7B VLM ile rekabetçi; 72B 11/11 referans değerlerinde Llama-3.2-90B-Vision'ı yenir.
   | Molmo 的 4B 模型与闭源 7B VLM 竞争力相当；72B 在 11/11 基准上击败 Llama-3.2-90B-Vision。这对 LLM 规模饱和假说意味着什么？

5. 7B VLM'deki veri karışımı kalitesini kodlayıcı kalitesinden ayırmak için bir ablation tablosu tasarlayın.
   | 设计消融实验表，在 7B VLM 上隔离数据混合质量和编码器质量。最少需要多少次训练？提出四组轴设置。

## Anahtar Terimler

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|----------|---------|
| Ablation | "Turning one knob" | Training multiple runs that differ in exactly one design-space axis, holding everything else constant | 消融实验：只改变一个设计轴、保持其他不变的多组训练 | |
| Connector | "Bridge" / "projector" | Trainable module that maps vision encoder output into the LLM's token space (MLP, Q-Former, Perceiver) | 连接器：将视觉编码器输出映射到 LLM token 空间的可训练模块 | |
| Detailed human caption | "Dense caption" | A multi-sentence human-written description (typically 80-300 tokens) richer than a web alt text | 详细人工描述：人类编写的多句描述（通常80-300 token） | |
| Distillation | "GPT-4V captions" | Training data generated by a stronger proprietary VLM; convenient but prone to inherited hallucination | 蒸馏：用更强的专有 VLM 生成训练数据；方便但会继承幻觉 | |
| AnyRes / dynamic res | "High-res path" | Strategy to feed images larger than the encoder's native resolution via tiling or M-RoPE | AnyRes/动态分辨率：通过切片或 M-RoPE 处理超过编码器原生分辨率的图像 | |
| Resolution ramp | "Curriculum" | Training schedule that starts low-resolution and increases, speeding alignment learning | 分辨率递增：从低分辨率开始逐步增加的训练调度 | |
| Vision-centric bench | "CV-Bench / BLINK" | Evaluation that stresses fine-grained visual perception rather than language-heavy reasoning | 视觉中心基准：测试精细视觉感知能力而非语言推理 | |
| PixMo | "Molmo's data" | Allen AI's 712K densely-captioned image dataset; human speech transcribed into dense captions | Allen AI 的 712K 密集标注图像数据集；人工语音转录为密集描述 | |

## Daha fazla okumak

- [McKinzie et al. — MM1 (arXiv:2403.09611)](https://arxiv.org/abs/2403.09611)Apple MM1 Multi Mode Model Düzeltme deneyimi
- [Laurençon et al. — Idefics2 / What matters building VLMs (arXiv:2405.02246)](https://arxiv.org/abs/2405.02246)VLM'i oluşturmanın anahtar faktörleri
- [Deitke et al. — Molmo and PixMo (arXiv:2409.17146)](https://arxiv.org/abs/2409.17146)# Molmo ve PixMo #
- [Tong et al. — Cambrian-1 (arXiv:2406.16860)](https://arxiv.org/abs/2406.16860)Cambrian-1 kodlayıcı ile karşılaştırma
- [Karamcheti et al. — Prismatic VLMs (arXiv:2402.07865)](https://arxiv.org/abs/2402.07865)Prismatik VLM'ler  Kontrolle Düzeltme Deneyimleri
