# Çok modoldaki RAG ve çapraz modoldaki kurtarma.

> Görüş-doğal belge RAG bir parça. Üretim multimodal RAG daha geniş bir alanı açar. Bu süreçte seyahat planlaması ("doğal ışıkla sakin bir vegan brunch bul") gibi iş akımları için metin, görüntü, ses ve video alınır. Üç 2025 anketleri  Abootorabi et al., Mei et al., Zhao et al.  alt sorunları kodlaştırdı: çapraz modal geri alım, geri alım birleşimi, üretim yerleştirme, multimodal değerlendirme. Bu ders, anketleri okur ve üretim borusunu tasarlar.

> **【中文解读】**Üretim seviyesinde çok modelli RAG  tek bir dosya kontrolü ötesinde  transtext, resim, ses, ses, video kontrolü, seyahat planlama, sağlık bölümü, e-ticaret önerisi, gerçek hizmet ve benzeri durumlar için ihtiyaç vardır.

**Type:** Build
**Languages:** Python (stdlib, cross-modal retriever with fusion + grounded generator)
**Prerequisites:** Phase 12 · 23 (ColPali), Phase 11 (RAG basics)
**Time:** ~180 minutes

>  **【前置】**学本节前 Lütfen önce öğrenin:Fase 12·23(ColPali 视觉文档 RAG) 、Fase 11·14-17(RAG 检索/融合/重排) 、Fase 12·02(CLIP 跨模态对齐) ⋅本节是ColPali'nin genişletilmesi多种模态一起检索+融合──
>  **【类比】**Çoğu zaman, hastalar "öğüt ağrısı" diyor. Hastalar "öğüt ağrısı" diyor.

## Öğrenme Hedefleri

- Modal çaplı çekim tasarımı: metin → resim, resim → metin, ses → video vb.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Üç füzyon stratejisini karşılaştırın: puan füzyonu, dikkat tabanlı füzyon, MoE füzyonu.
  Çinçe Çevirimiçi:Biyaraşmak Üç çeşit birleşim stratejisi:分数融合、注意力融合、MoE 融合。
- Nesil yerleştirmesini açıklayın: kaynaklar bir karışım modaliteler olduğunda "aykın kaynaklarınızı alıntılamak" nasıl görünüyor.
  Çine dilinde: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳: 訳
- 2025'te yapılan üç kanonik multimodal RAG anketinin ve alt sorun taksonomlarının adını verin.
  Çinçe Çevirim:列举 2025 年三篇经典多模态 RAG 综述及其子问题分类──

## Sorunlar. Sorunlar.

Tek modal RAG çözülmüş bir örnektir: göm sorgu, göm parçalar, geri almak, LLM'ye eşyalar.

> 单模态 RAG 是已解决的模式:嵌入查询、嵌入块、检索、塞入 LLM──多模态 RAG 需要:

1. Çoklu çekim başları (her modalite uyumlu bir alanda yerleştirilmelidir).
   Çinçe Çevirim: 多个检索头 (Büyük bir inceleme)
2. Arama sonuçlarının modaletler arasında birleşmesi.
   Çinçe Çevirisi:跨模态检索结果的融合──
3. Modeller arasında kaynakları belirleyen nesil yerleşimi.
   Çinçe Çevirisi:跨模态引用源的生成接地──
4. Modal çaplı sinyalleri kapsayacak değerlendirme ölçümleri.
   Çinçe Çevirisi:覆盖跨模态信号的评估指标──

2025 anketleri hepsi aynı taksonomide.

> 2025 yılındaki genel kayıtlar aynı sınıflandırma kurallarına sahipti.

## Konsepten bir şey.

> **【中文解读】**跨模态 RAG  genişletilmiş geleneksel metin RAG, multi-modal arama ve üretimi destekledi: metin arama görüntü, resim arama metin, veya karışık arama multi-modal dosyaları,

> **【拓展：多模态 RAG 的应用**Birçok model RAG, sağlık, elektronik, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret, ticaret


### Modal çaplı çekim

A. Modalite sorgulaması ile B modalite belgelerini alın. Üç örneği:

> 给定模态 A 的查询,检索模态 B 的文档──三种模式:

1. Paylaşılan yerleştirme alanı. CLIP ve CLAP paylaşılan bir alanda metin + görüntü / metin + ses yerleştirmeleri üretir. Modaliteler arasında kozine benzerliği doğrudan çalışır. CLIP eğitilmiş çiftlere sınırlıdır.
   Çinçe çevirisi: 共享嵌入空间──CLIP 和 CLAP 在共享空间中产生文本+图像/文本+音频嵌入──跨模态余弦相似度直接有效──限于CLIP 训过的配对──

2. Per-modality kodlayıcı + çevirim. Metin kodlayıcı + görüntü kodlayıcı + küçük bir çevirmen modülü boşluklar arasında haritası. Sen2Sen by Gupta et al. ve diğer 2024 tasarımları. Eğlenceli ancak karmaşıklığı artırır.
   Çinçe Çevirisi: 每模态独立编码器 + 翻译。文本编码器 + 图像编码器 + 在空间间映射的小翻译模块。Sen2Sen 等 2024 yıl tasarım。灵活但增加复杂度。

3. VLM'nin desteklediği her modalite işe yarıyor. Daha yüksek kalite, daha pahalı.
   Çin dili:VLM 编码器 olarak。VLM 隐藏状态作为检索表示──VLM 支持的任何模式都可用──质量更高,成本更高──

Seçim: Metin + Resim için CLIP / SigLIP 2; Metin + Ses için CLAP; Sınır kalitesi ile çapraz modal için VLM-gizli durumlar.

> 选择建议:文本+图像用 CLIP/SigLIP 2;文本+音频用 CLAP;前沿质量跨模态用 VLM 隐藏状态──

### Füzyon stratejileri

10 sonuç aldınız: 5 görüntü, 3 metin pasajı, 2 ses klipi. Nasıl birleştiriyorsunuz?

> 10 sonuç aradınız: 5 张图像、3 段文本、2 个音频片段──如何合并?

Skor füzyonu (en ucuz). Her modalitetin kendi retriever'i vardır, her biri puanlar verir.

> ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇ ̇

Dikkat tabanlı bir birleşim. Tüm alınan eşyaları birleştirin, küçük bir dikkat ağının ağırlığını almasına izin verin.

> dikkat çekmek için tüm araştırmaları yapın.

MoE birleşimi. Modalite-specifik uzmanlara ağ yollarını açmak. Farklı sorgu türleri farklı yönlendirir  görsel bir soru görüntülerin daha yüksek ağırlık taşıdığı bir sorgu.

> MoE 融合──门控网络路由到模态特定专家──不同查询类型路由不同视觉问题给图像更高权重──

Üretim standart: sorunun baskın modaliteye karşı hafif bir önyargı ile puan birleşimi. A / B alanınızda açık kazanç gösterirse MoE'ye yükseltin.

> 生产默认:分数融合 + sorgu yönlendirmesi modülünün hafif bir yönlendirme.

> **【中文解读】**Üç çeşit birleşim stratejisi:(1) Bölümsel birleşim farklı biçimli araştırma makineleri分別归归化分数后加权求和,最简单;(2) dikkat力融合小网络学习权重,训练需要;(3) MoE 融合门控网络按查询类型路由到不同专家──生产默认是分数融合 + 查询主导模态的微偏置──

> **【拓展：多模态 RAG 的跨模态检索基础】**跨模态检索有三种模式:(1) 共享嵌入空间(CLIP/SigLIP 2 用图文,CLAP 用文本-音频);(2) 每模态独立编码器 + 翻译模块;(3) 用 VLM 隐藏状态作为检索表示──选择建议:文本+图像用 CLIP/SigLIP 2,文本+音频用 CLAP,跨模态前沿质量用 VLM 隐藏状态──

### Nesil yerleştirme

LLM, her bir talebi hangi alınmış maddeyle yönlendirdiğini belirtmelidir.

> LLM 引用哪个检索项驱动了每个声明──对多模态:

- Metin kaynağı: standart alıntı `[1]`- Evet .
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`[1]`- Evet.
- Resim kaynağı: `[img 3]`Kısa bir başlıklı.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`[img 3]`附简短描述──
- Ses: `[audio 2 at 0:34]`- Evet .
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`[audio 2 at 0:34]`- Evet.

Yükleme bilgisi ile jeneratörü eğit: eğitim hedefinin her iddiası kaynak indeksle etiketlenir.

> Üzerinde algılama verileri eğitimi üreticisi: eğitimin hedefleri içindeki her açıklama işaretli kaynak kaynak kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynaklı kaynak

### 2025 anketleri

Abootorabi et al. (arXiv:2502.08826, "Herhangi bir Modalite'de Sorun"): multimodal RAG için taksonom. Geri alınma, füzyon, jenerasyon kapsamaktadır. En geniş kapsam.

> Abootorabi 等人:多模态 RAG 分类法──覆盖检索、融合、生成──覆盖最广──

Mei et al. (arXiv:2504.08748, "Multimodal RAG'nin Bir Anket"): alt görev referans değerlerine ve başarısızlık modlarına odaklanır.

> Mei 等人:聚焦子任务基准和失败模式――对评估设计有用――

Zhao et al. (arXiv:2503.18016): vizyon odaklı anket.

> Zhao 等人:聚焦视觉的综述──对 ColPali 系列工作覆盖深入──

Üçünü de okuduktan sonra 2025 baharına kadar en son gelişmeleri göreceksiniz.

> 阅读全部三篇 2025 yılının ilkbaharının en önde gelen durumunu elde edebilirsiniz. Çoğu çocuk sorusu hala açık.

### MuRAG  temel kağıt

MuRAG (Chen et al., 2022) ilk multimodal RAG'di. Bir multimodal KB'den görüntü + metin alınarak cevaplar üretildi. VLM dalgasından önce uygulanabilirliği gösterdi. Modern sistemler (REACT, VisRAG, M3DocRAG) buna dayanıyor.

> MuRAG ilk çok modoldaki RAG'dir. Bu temel üzerinde kurulan, VLM ırğasından önce kullanılabilirliği kanıtlayan bir çok modoldaki bilgi kütlesinden görüntüler ve metinler oluşturur.

### Üretim seyahat planlaması örneği

Sorum: "Bana doğal ışıkla sessiz bir vegan kahvaltı bul".

> Soru: "Bana bir sessiz, saf kahvaltı bul, doğal ışık var"...

Kök hattı:

> 管道:

1. Sorguyu parçala. "sessiz" → sesli / inceleme anahtar kelime; "veyan brunch" → menü öğesi; "doğal ışık" → görüntü özelliği.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
2. Modalite başına geri alın:
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
   - Yorumlar için metin alınması: "Vegan brunch, sakin ortam".
     Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çev Çev Çeviri Çev Çev Çeviri Çev Çeviri Çev Çev Ç Ç Ç Çev Çev Ç Ç Ç Ç Ç Ç Çev Çev Ç Ç Ç Ç Ç Çev Çev Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
   - Restoran fotoğraflarından görüntü alımı: "Doğal ışık, hava".
     Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
   - Çevre ses klipleri üzerinde ses çıkarma: "Uzun decibel, müzik yok".
     Çevre sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli sesli ses
3. Her restoranın bileşik puanları var.
   Çinçe Çevirisi:融合分数── her restoranın karmaşık bir sayı vardır──
4. Top-k restoranlar → VLM jeneratörü tüm kanıtlarla → cevap alıntılarla.
   Çeviri:VLM 生成器 (VLM)

Bu, metin-RAG'den çok daha fazlasıdır. Her modalitenin tek başına metin kaçırdığı bir sinyal eklenir.

> Bu çok fazla metin RAG. Her model sadece metin topluluğunun atık sinyallerine bağlı olarak eklenir.

### Ajantik multimodal RAG

Multi-hop: ilk arama yüksek güvenle cevap vermezse, LLM yeniden formüle eder ve tekrar alır.

> 多跳: Eğer ilk kez kontrol edilmemişse yüksek güvenle cevap verilmiştir,LLM 重新表述并再次检索──Fase 14'ün Ajan RAG 模式在此适用── örneği:

- İlk top-10'u geri alın → LLM "çok gürültülü, <40 dB'lik filtre" → yeniden alın.
  Çeviri: Çekşek ilk ilk 10 → LLM 提问"太杂,过 <40 分贝" → 重新检索──
- Resimleri geri alın → LLM bir menü var görüyor → menü metnini geri alın → cevap.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri

Karmaşıklık ekler ama tek çekimle geri alınamayan sorularla ilgilenir.

>  karmaşıklığı arttırmak ama tek bir sorguyu ele geçirmek mümkün değil.

### Değerlendirme

Modal çaplı değerlendirme henüz olgunlaşmamış.

> 跨模态评估 henüz olgunlaşmamıştır.

- Her modaliteye göre hatırlatma.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Top-k doğruluğu.
  Çinçe Çevirisi: 融合后的 top-k 准确率──
- İnsan tarafından değerlendirilmiş son-son tatmin edici.
  Çinçe Çevirisi: yapay değerlendirmenin sonu sonu sonu sonu tamamı.
- Görev-özel (tüm rezervasyonlar tamamlandı, satın alınmıştır).
  Çinçe Çevirimi: görev belirli bir işaret

Standart bir referans değeri tüm yöntemleri kapsamamaktadır.

> 没有标准基准覆盖所有模态── çoğu makale alanın belirli görevleri üzerinde değerlendiriliyor──

## Çerçeveyi kullanın.
```figure
contrastive-matrix
```

## Kullan

`code/main.py`- ...

- Ortak restoranlar üzerinde çalışan üç sahte retriever (metin, görüntü, ses).
  Çinçe Çevirimiçi:三模拟检索器 (三模拟检索器)
- Modalite puanlarını yapılandırılabilir ağırlıklar ile birleştiren puan birleşimi.
  Çinçe Çevirimi: ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎
- Son cevabı alıntılarla yayınlayan bir jeneratör.
  Çine Çeviri: 输出带引用最终回答的生成器──
- Güven düşükse soruyu yeniden formüle eden basit bir ajanik döngü.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-multimodal-rag-designer.md`Multimodal sorgu akışı olan bir ürün özellikine göre, retriever, füzyon, jeneratör ve değerlendirme tasarımı.

> 本课产 出 `outputs/skill-multimodal-rag-designer.md` Çoklu modelli sorgu akışının ürün özellikleri, tasarım sorgu cihazları, birleşim stratejileri, üreticileri ve değerlendirme programları belirlenir.

## Egzersizler.

1. Bir tıbbi-trigörlü multimodal RAG önerin: sorgu = yaralanma fotoğrafı + metin semptomları. Hangi modaliteleri hangi KB'den elde edebilirsiniz?

2. Skor füzyonu basit bir ağırlıklı toplamdır. MoE füzyonu kaçınılması için hangi başarısızlık moduna sahiptir? 分数融合是简单的加权求和.

3. Abootorabi et al.'ın taksonomisi (Bölüm 3) okuyun. Üç kanonik alt sorununun ne olduğunu ve seçtiğiniz ürüne nasıl haritası yapıyorlar?

4. Bir seyahat planlayıcısı için bir eval spesifikasyonu tasarlayın. Hangi ölçütler görüntü hatırlaması, ses hatırlaması ve kompozisyon doğruluğunu kapsar?

5. Agent Multi-Hop RAG'nin geri dönüş yolculuğu başına gecikme vergisi vardır. Hangi sorgu zorluğu doğruluğunun kazancı gecikmeyi haklı çıkarır? Agent 多跳 RAG Her turda有延迟开销──在什么查询复杂度下,准确率提升值得延迟代价?

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Cross-modal retrieval | "Query one modality, retrieve another" 跨模态检索 | Text query retrieves images; image query retrieves text; requires a shared space or translator 文本查询检索图像；图像查询检索文本；需要共享空间或翻译器 | |
| Score fusion | "Combine scores" 分数融合 | Weighted sum of per-modality retrieval scores; simplest fusion 各模态检索分数的加权和；最简单的融合方式 | |
| MoE fusion | "Modality-routed experts" 混合专家融合 | Gating network picks which modality's scores to trust per query 门控网络按查询选择信任哪个模态的分数 | |
| Grounded generation | "Cite your sources" 接地生成 | Each claim in the answer tagged with the source index 回答中的每个声明都标注来源索引 | |
| MuRAG | "First multimodal RAG" 首个多模态 RAG | 2022 paper that established the multimodal RAG pattern 2022 年建立多模态 RAG 模式的论文 | |
| Agentic multi-hop | "Reformulate and retry" Agent 多跳 | LLM re-queries retrievers when first-pass confidence is low 首次检索置信度低时 LLM 重新查询检索器 | |

## Daha fazla okumak

- [Abootorabi et al. — Ask in Any Modality (arXiv:2502.08826)](https://arxiv.org/abs/2502.08826)
- [Mei et al. — A Survey of Multimodal RAG (arXiv:2504.08748)](https://arxiv.org/abs/2504.08748)
- [Zhao et al. — Vision RAG Survey (arXiv:2503.18016)](https://arxiv.org/abs/2503.18016)
- [Chen et al. — MuRAG (arXiv:2210.02928)](https://arxiv.org/abs/2210.02928)
- [Liu et al. — REACT (arXiv:2301.10382)](https://arxiv.org/abs/2301.10382)
