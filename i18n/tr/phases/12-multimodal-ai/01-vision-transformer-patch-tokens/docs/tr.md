# Görüş Transformers ve Patch-Token Primitive

> Bir görüntü, bir transformatörün yiyebileceği bir simge sırası haline gelmeden önce multimodal bir şey olmalıdır. 2020 ViT makalesi 16x16 piksel yamaları, bir çizgi projeksiyonu ve bir pozisyon yerleştirme ile buna cevap verdi. Beş yıl sonra her 2026 sınır modeli (Claude Opus 4.7 2576px doğuştan, Gemini 3.1 Pro, Qwen3.5-Omni) hala bu şekilde başlar  kodlayıcı ViT'den DINOv2'ye SigLIP 2'ye değiştirildi, kayıt simgelerinin eklendiği, konumsal şema 2D-RoPE oldu, ancak ilkel tutuldu. Bu ders, patch-token borusunu sonuna kadar okuyor ve stdlib Python'da inşa ediyor. Böylece 12'nin geri kalanında "görsel tokenler" için bir zihinsel model var.

> **【中文解读】**Çok modülye girmeden önce, görüntü önce Transformer 能处理'in simge sırasına dönüşmelidir. ViT 16x16 görüntü blokları+linear proje + konum kodlaması ile bu dönüşümü gerçekleştirdi ve bugüne kadar tüm öncü modellerin temelini oluşturmaktadır.

> **【拓展：ViT Patch→多模态基础】**Patch-Token tüm görsel dil modelinin temelini oluşturur. CLIP'in görsel kodlayıcıları, LLaVA'nın görüntü girişleri veya dosya anlama modelleri olsun, hepsi Patch'ten 切分开始──

>  **【前置】**Özetle: 1) Fase 7·01-05(Transformer 基础)  Anlamak Self-Attention、Position Embedding; 2) Fase 4·03(CNNs)  Anlamak卷积特征提取,对比 ViT 补丁方法; 3) Fase 10·01(Tokenizers)  Anlamak文本代币,本节是其视觉对应; 4) numpy 矩阵运算──本节是 Fase 12 全部 25 节的基础,跳过会看不懂后续──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, patch tokenizer + geometry calculator) | **语言:** Python（标准库，patch tokenizer + 几何计算器）
**Prerequisites:** Phase 7 (Transformers), Phase 4 (Computer Vision) | **前置知识:** Phase 7（Transformer），Phase 4（计算机视觉）
**Time:** ~120 minutes | **时间:** ~120 分钟

## Öğrenme hedefleri

- HxWx3 resmini doğru konum kodlaması ile bir dizi yama tokeni haline getir.
  Çin Çeviri: HxWx3 图像转换为带有正确位置编码的补丁代码 序列
- Verilen bir ViT için dizinin uzunluğu, parametrelerin sayımı ve FLOP'ları hesaplayın (batç boyutu, çözünürlük, gizli soluk, derinlik).
  Çinçe çeviride: hesap verilmiş (patch)
- ViT'yi 2020 araştırmasından 2026 üretimine götüren üç yükseltmenin adını verin: kendi başına denetim altına alınmış önceden eğitim (DINO / MAE), kayıt simgelerinin ve yerel çözünürlüklü paketlemenin.
  Çinçe çevirisi:列举将 ViT 2020 yılından araştırma süresi 2026 yılına kadar üretim ortamının üç büyük yükseltilmesi:自监督预训练(DINO / MAE) 、register token 和原生分辨率打包──
- CLS birleştirme, ortalama birleştirme ve aşağı akıntılı bir görev için simgeler kaydetme arasında seçim yapın.
  Çinçe Çevirimiçi:为下游任务选择 CLS 池化、平均值池化或注册代币。

## Sorunlar. Sorunlar.

Transformatörler vektörlerin dizisinde çalışır. Metin zaten bir dizisidir (bayt veya jetonlar). Bir görüntü üç renk kanalı olan piksellerin 2 boyutlu bir şebekesi  bir dizis değildir. Her pikselini düzeltirseniz, 224x224 RGB görüntüsü 150.528 jeton olur ve bu uzunlukta kendine dikkat etmektir.

> Transformer 操作は向量序列である──文本本身就是序列である──字节或符号), ancak görüntü üç renkli bir yolla geçen bir像素 2D 网格 değildir── eğer her bir像素 için uzlaştırılırsa, bir 張 224x224'in RGB 像素 150,528 符号 haline gelir, bu uzunluk üzerinde dikkat çekmek ise yapılmaz.

2020'ye kadar yaklaşımlar CNN özellik çıkarıcısını ön tarafta boğulmuştur: ResNet, 2048 boyutlu vektörlerin 7x7 özellik haritasını üretir, bu 49 tokeni bir transformatöre besler. Bu çalışır ancak CNN'in önyargılarını miras alır (çevirim eşdeğerliği, yerel kabul alanları) ve transformatörün ölçek açlığını kaybeder.

> 2020 yılından önceki yöntem, CNN özellik çekicisi: ResNet'in 7x7'li 2048 维向量特征图'sını oluşturması, bu 49 tane tokeni Transformer'e vermesi mümkün oldu. Ancak CNN'in özelliği olan                                                                                                                                                                                                                                  

Dosovitskiy et al. (2020) net bir soru sordu: CNN'i atlasak ne olur? Resimi sabit boyutlu yamalara (örneğin 16x16 piksel) ayırın, her yamayı bir vektöre doğrusal olarak yansıtın, bir pozisyonal yerleştirme ekleyin ve dizini bir vanilya transformatörüne besleyin. O zamanlar bu, sarsılmaz bir görme biçimidir. Yeterince veriyle (JFT-300M, sonra LAION) ResNet'i ImageNet'te yendi ve gelişmeye devam etti.

> Dosovitskiy  et al.) bir doğrudan soru ortaya koydu: Eğer CNN'den atlasak, görüntü sabit büyüklükteki bir yama olarak bölünecek. Örneğin 16x16 像素 gibi), her yama için bir vektör, konum kodlaması ve ardından sıralamaları standart Transformer'e gönderir.

2026 yılına kadar ViT primitif sorgulanmayan bir temel haline geldi. Her açık ağırlıklı VLM'nin görme kulesi bir soylu (DINOv2, SigLIP 2, CLIP, EVA, InternViT) oldu.

> 2026 yılına kadar, ViT orijinal dili tartışmasız bir temel haline geldi. Her açık ağırlığın VLM'deki görme kulesi sonrakilerdir.

## Konsepten bir şey.

> **【中文解读】**Görüş Transformer (ViT) resimleri sabit büyüklükte bir yama olarak bölüyor, her yama 展平后通过线性投影变成一个代币,然后像NLP 中的变形机 一样处理──这是将变形机架构引入计算机视觉的奠基性工作,取代了CNN 成为视觉的脊柱──

> **【拓展：ViT 的影响】**Dosovitskiy  et al. 2020 yılında önerilen ViT kanıtı Transformer, görüntü sınıflandırma üzerinde CNN'i aşabilmektedir. ViT-L/14 ImageNet'te %88.5'e ulaştı.


> **【拓展：ViT 对 CNN 的优势】**ViT'in genel yoğunluğu, veri miktarında yeterince yoğunlaşmış olarak (JFT-300M veya LAION-5B gibi) CNN'in yerel duyusundan önemli ölçüde daha iyi olmuştur.


### Token olarak yamalar

Bir görüntü verildiğinde `x`şekli ile`(H, W, 3)`ve bir yama boyutu `P`, resmini bir şebekeye kazıyorsan`(H/P) x (W/P)`Dönüşmeyen yamalar.`P x P x 3`Bir küp piksel. Her küpeyi bir `3 P^2`Vectör. Paylaşılan bir çizgi projeksiyonu uygulayın `W_E`şekli ile`(3 P^2, D)`Her yama modelin gizli boyutuna yerleştirmek için.`D`- Evet .

> 给定形为 `(H, W, 3)`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `x`和 patch büyük `P`,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `(H/P) x (W/P)`个不重叠的补丁网格──每个补丁是一个 `P x P x 3`Bu, bir çubuğun bir parçasıdır.`3 P^2`维向量──应用形为 `(3 P^2, D)`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `W_E`, her yama modelin gizli boyutlarına göre görüntülenir .`D`- Evet.

ViT-B/16 kanonik yapılandırması için:
- Resolüt 224, patch boyutu 16 → grid 14x14 → 196 patch tokenleri.
  中文翻译:分辨率 224, patch 大小 16 → 网格 14x14 → 196 个 patch token。
- Her yama `16 x 16 x 3 = 768`Piksel değerleri, `D = 768`- Evet .
  Çeviri: Her yama 包含 `16 x 16 x 3 = 768`个像素值,投影到 `D = 768`- Evet.
- Öğrenilenebilir bir ekle `[CLS]`token → dizinin uzunluğu 197.
  Çin Çeviri: 添加一个可学习的`[CLS]`işaret → 序列长度 197。

Patch projesi , matematik açısından çekirdek boyutlu 2 boyutlu bir konvulsyonla aynıdır .`P`, adım at `P`ve`D`Bu, üretim kodunun aslında bunu uyguladığı bir yöntem.`nn.Conv2d(3, D, kernel_size=P, stride=P)`"Linear proje" çerçevesinin kavramsal olması; çekirdeğin çerçevesinin verimli olması.

> Patch  projection matematikte nükleer büyüklükte `P`、步长为 `P`Çıkış yolu için`D`Bu şekilde gerçekleştirilen üretim kodudur.`nn.Conv2d(3, D, kernel_size=P, stride=P)` "Lineal projection" kavramsaldır; roll积核'un gerçekleşmesi yüksek verimlidir

### Konum yerleşimleri

Çizgilemeler iç içerikli bir sırayla değildir. Transformatör onları bir torba olarak görür. İlk ViTs, öğrenilebilir bir 1D pozisyonsal yerleşim ekledi (her pozisyonda bir 768-dim vektör, 197'si). Çalışır, ancak modeli eğitim çözünürlüğüne bağlar: sonuç olarak, şebekeni değiştirirseniz pozisyon tablosunu interpolasyonlamanız gerekir.

> Patch  sabit bir sırayla Transformer onları bir sırayla bir toplam olarak görüyor. Early ViT  öğrenilenebilir 1D konum kodunu ekledi.

Modern görme omurgası 2D-RoPE (Qwen2-VL'nin M-RoPE, SigLIP 2'nin varsayılan) veya faktörlü 2D konumları kullanır. 2D-RoPE, sorgu ve anahtar vektörlerini yama (sır, sütun) endeksine göre döndürür, bu nedenle model dönüm açısından nispeten 2D konumunu çıkarır.

> Modern görsel başlıca ağ 2D-RoPE(Qwen2-VL'nin M-RoPE、SigLIP 2'nin öntanımlı programı) veya parçalanmış 2D  konum kodlaması。2D-RoPE Patch'ın ↓ 列) indeksi dönüm sorguları 和 anahtar yönü, bu nedenle model dönüm açısından 2D  konumlara karşı tahmin eder.

### CLS tokenleri, toplu çıkış ve kayıt tokenleri

Resim seviyesinde temsil nedir? Üç seçenek bir arada var:

> 什么是图像级表示? 三种选择并存:

1. `[CLS]`Token. Patch dizisine bir öğrenilebilir vektör hazırlayın. Tüm transformatör bloklarından sonra, CLS token'in gizli durumu görüntü temsilidir. BERT'den miras alınmıştır.
   Çeviri:`[CLS]`token──在补丁序列前拼接一个可学习向量──所有 Transformer 块之后,CLS token'in gizli durumu ise görüntü göstergesi──继承自BERT──原始 ViT 和 CLIP 使用──
2. Ortalama bir havuz, patch tokenlerinin çıkışının ortalama gizli durumları SigLIP, DINOv2 ve çoğu modern VLM'de kullanılır.
   Çin dilinde çevirme:均值池化──对所有补丁代币的输出隐藏状态取平均──SigLIP、DINOv2 和大多数现代VLM使用──
3. Darcet ve diğerleri (2023) açık bir sink token olmadan eğitilmiş ViTs'lerin kendi dikkatini kaçırmak için yüksek normlu "artifak" yamalar geliştirdiklerini gözlemledi. 416 öğrenilebilir kayıt tokenlerini eklemek bu yükü absorbe eder ve yoğun tahmin kalitesini (seğimlendirme, derinlik) iyileştirir. DINOv2 ve SigLIP 2 her ikisi de kayıtlarla birlikte gemi.
   Çinçe çevirisi:Register token──Darcet 等人(2023) Noted, there is no apparent汇聚 token of ViT 会产生高范数"伪影"patch,劫持自注意力──添加4-16 个可学习的注册代号 可以吸收这种负载,提高密集预测质量──分割、深度──DINOv2 和 SigLIP 2 都带有注册──

Seçim aşağıdaki görevler için önemlidir. CLS sınıflandırma için iyidir. LLM'ye patch tokenlerini besleyen VLM'ler için, tümüyle birleştirmeyi atlatırsınız.

> Seçim için aşağı游 tâbi çok önemlidir. CLS 适合分类. LLM'nin VLM'sine 入 patch token için, her patch tamamen atladı.

### Ön eğitim: denetlenmiş, kontrastlı, maskeli, kendi kendine distillenmiş

2020 ViT, JFT-300M üzerinde denetimli sınıflandırma ile önceden eğitildi.

> 2020 yılının ViT'de JFT-300M 上用监督分类進行预训──很快被以下方法取代:

- CLIP (2021): 400M çiftler üzerinde kontrastlı görüntü-metin.
  Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Çince Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- MAE (2021, He et al.): %75 parşömen maske, piksel yeniden yapılandırma.
  Çinli dilde:MAE(2021,He 等人): %75'i koruyan bir yama, yeniden inşa edilmek, kendiliğinden izlemek, saf bir görüntü için uygulanmak.
- DINO (2021) / DINOv2 (2023): öğrenci-öğretmen ile kendi kendine destilasyon, etiketler, başlıklar yok. 2023 DINOv2 ViT-g/14 en güçlü tamamen görsel omurgan ve "sıkı özellikler" kullanım durumları için varsayılan.
  Çinli dilde:DINO(2021) / DINOv2(2023):师生自蒸,无需标签、无需描述──2023 yılının DINOv2 ViT-g/14 en güçlü saf görsel başkanlık ağıdır, aynı zamanda "密集特征" olarak da kullanılır.
- SigLIP / SigLIP 2 (2023, 2025): Sigmoid kaybı ile CLIP ve doğuştan görünüm oranı için NaFlex. 2026'da baskın görme kulesi açık VLM'ler (Qwen, Idefics2, LLaVA-OneVision).
  ÇXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Ön eğitim seçeneğiniz omurganın ne için iyi olduğunu belirler: semantik metin ile eşleşme için CLIP/SigLIP, yoğun görsel özellikler için DINOv2, aşağıdaki ince ayarlama için başlangıç noktası olarak MAE.

> 预训练方式决定主干网络擅长什么:CLIP/SigLIP, metin anlamına uygun kullanılır,DINOv2 yoğun görsel özellikler kullanılır,MAE,下游微调的起点──

### Ölçekleme yasaları

ViT ölçeklendirme (Zhai et al. 2022) bir ViT'nin kalitesi model boyutunda, veri boyutunda ve hesaplama konusunda öngörülebilir yasalara uyduğunu ortaya koydu.

> ViT 缩放定律(Zhai 等人,2022) ViT'nin kalitesini model büyüklüğü, veri büyüklüğü ve hesaplama miktarı hakkında öngörülebilir kurallar altında belirledi.

- Daha büyük model + daha fazla veri → daha iyi kalite.
  Çinçe Çevirimiçi: Daha büyük model + 更多数据 → 更好的质量──
- Patch boyutu, dizinin uzunluğuna karşı sadakatle ilgili bir kaldıraçtır. Patch 14 (DINOv2/SigLIP SO400m için tipik) bir görüntü başına 16 patch'tan daha fazla token verir; OCR ve yoğun görevler için daha iyi, hız için daha kötüdür.
  Patch 大小是序列长度与保真度之间的杆──Patch 14 ((DINOv2/SigLIP SO400m 的典型配置) Patch 16'dan daha fazla token üreten her görüntü; daha uygun OCR 和密集任务, ancak hız daha yavaş──
- Resolüt diğer büyük kaldıraç. 224'ten 384'e 512'e gitmek neredeyse her zaman yardımcı olur, FLOP'lerde kare maliyetinde.
  Çinçe Çevirisi: Çözüm oranı önemli bir diğer 杆── 224 提升至384 再至512 几乎总是有帮助,但FLOP 成本呈二次增长──

ViT-g/14 (1B param, patch 14, çözünürlük 224 → 256 token) ve SigLIP SO400m/14 (400M param, patch 14) 2026 açık VLM'ler için iki iş atı kodlayıcılarıdır.

> ViT-g/14(10 milyar parametre, patch 14,分辨率 224 → 256 个代币) ve SigLIP SO400m/14(4 milyar parametre, patch 14) 2026 yılında açık VLM'in iki büyük güç kodlayıcııdır.

### Bir ViT için parametre sayısı

Tam hesaplamalar `code/main.py`- ViT-B/16 için 224'te:

> 完整计算见 `code/main.py`❖ ViT-B/16 için 224 çözünürlük altında:

```
patch_embed = 3 * 16 * 16 * 768 + 768  =  591k
cls + pos    = 768 + 197 * 768          =  152k
block        = 4 * 768^2 (QKVO) + 2 * 4 * 768^2 (MLP) + 2 * 2*768 (LN)
             = 12 * 768^2 + 3k          =  7.1M
12 blocks    = 85M
final LN    = 1.5k
total       ≈ 86M
```

Kontrol noktasını yüklemeden önce her ViT'yi bu şekilde park et.

> Yükleme kontrol noktasından önce, bu yöntemle her bir VTyi tahmin ederek, ana ağın büyüklüğü VLM'nin belirgin kalınlığı sınırını belirler.

### 2026 üretim düzenlemesi

2026 yılında en açık VLM'lerin gemisi olan kodlayıcı, siglip 2 SO400m/14 olarak yerleşik çözünürlükte (naflex) kullanılmıştır.

> 2026 yılının çoğu açık VLM 搭载的编码器是原生分辨率 (NaFlex) 的SigLIP 2 SO400m/14──它具有:

- 400M parametreleri.
  Çeviri: 4 milyar
- Patch boyutu 14, varsayılan çözünürlük 384 → 729 patch token/resim.
  Çeviri:Pach                                                                                                                                                                                                                                                            
- Resim düzeyinde görevler için ortalama havuz; VQA için LLM'ye tüm 729 yama akıyor.
  Çinçe Çevirimi: resim sınıfı görev kullanımı ortalama değer; tüm 729 个补丁 流入 LLM 进行视觉问答。
- 4 kayıt simgesi, LLM tesliminden önce atıldı.
  ÇINÇIM TRÜBLİK: 4 个注册令牌,在交给 LLM 前丢弃
- 2D-RoPE, doğal boyut oranı için görüntü seviyesinde ölçeklendirme ile.
  Çinçe Çevirim: 2D-RoPE, orijinal yaşam genişliğine destek olmak için resim seviyesini küçültmüş.

Bu konfigürasyonda her karar okuyabileceğiniz bir kağıttan kaynaklanıyor.

> Bu konuyla ilgili her karar, okuyabileceğiniz makaleye dayanır.

## Çerçeveyi kullanın.
```figure
image-patch-tokens
```

## Kullan

`code/main.py`Bu bir patch tokenizer ve geometri hesaplayıcı.

> `code/main.py`Yapılan işlemler, bir patch tokenizer olarak belirtilmiştir.

- Çelişki şekli ve sekans uzunluğu, çitlenmeden sonra.
  Çinçe Çevirim:Pach 切分后的网格形和序列长度──
- Sintez 8x8 piksel oyuncak görüntüsü için simge dizisi (sırın + proje yolu boyunca yürüyün).
  Çinçe çevirisi: sintet 8x8 像素玩具图像的符号序列
- Parametre sayısı, yama gömülmesi, pozisyon gömülmesi, transformatör blokları ve başla ayrılmış.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Hedef çözünürlüğünde ileri geçiş başına FLOPs.
  Çinçe Çevirimiçi: hedef çözünürlük altında her seferinde yayılan FLOPlar
- ViT-B/16 @ 224, ViT-L/14 @ 336, DINOv2 ViT-g/14 @ 224, SigLIP SO400m/14 @ 384 arasındaki karşılaştırma tablosu.
  Çin dilinde:ViT-B/16 @ 224、ViT-L/14 @ 336、DINOv2 ViT-g/14 @ 224、SigLIP SO400m/14 @ 384 的对比表──

Parametre sayısını yayınlanan sayılarla eşleştirin.

> 运行它──将参数与发布数据对比──调整补丁大小和分辨率来感受代币数量成本──

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-patch-geometry-reader.md`. ViT yapılandırmasını (patch boyutu, çözünürlük, gizli soluk, derinlik) vererek, bir token sayısını, parametre sayısını ve VRAM tahminini haklı çıkarır.

> 本课产 出 `outputs/skill-patch-geometry-reader.md` belirlenmiş ViT 配置(patch 大小、分辨率、隐藏维度、深度), simge miktarı, parametre ve görünüş kaydedilen tahminleri ve buna dayananları oluşturur.

## Egzersizler.

1. Patch-token dizisi uzunluğunu, 14 patch boyutu ile yerel 1280x720 girişinde Qwen2.5 VL için hesaplayın. Bu sadece CLS temsiline nasıl karşılaştırılır?
   Çinçe çevirisi: hesap Qwen2.5 VL 在原生 1280x720 输入、patch 大小 14 下的 patch-token 序列长度──与仅使用 CLS 的表示相比怎么样?

2. Patch 14'te 1080p (1920x1080) bir çerçeve kaç tane token üretiyor? 5 dakikalık bir video üzerinde 30 FPS'de toplam kaç görsel token üretiyor? Hangi maliyet en çok tasarruf ediyor: birleştirme, çerçeve örneklemesi veya token birleşimi?
   Çinçe çevirisi: 图像1920x1080) Patch 14 下 ne kadar token üretti? 30 FPS 播放 5 分钟视频,总共多少视觉 token?

3. DINOv2 çıkışının 196'dan fazla tokenin ortalama toplamının modelin değerine uygun olduğunu kontrol edin.`forward`Birleştirilmiş yerleştirme istediğinizde geri gelir.
   Çinçe çevirisi: Pure Python ile patch tokenlerinin ortalama değerini gerçekleştirmek için.`forward`Geri dönüşü birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiştir.

4. "Vision Transformers Need Registers" (arXiv:2309.16588) kitabının 3. bölümünü okuyun.
   Çin dilinde: "Vision Transformers Need Registers" (Vision Transformers Need Registers) (ArXiv:2309.16588) 3. bölüm.

5. Değiştir `code/main.py`Parçalanma paketini desteklemek için: farklı çözünürlüklü görüntülerin bir listesini verdiğinizde, tek bir paketlenmiş dizini ve blok diyagonal dikkat maskesini oluşturun.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`E destekleme patch-n'-pack: farklı çözünürlüklü bir dizi görüntü, bir paketleme dizisi oluşturmak ve köşelere dikkat maskeyi oluşturmak.

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| Patch | "16x16 pixel square" | A fixed-size non-overlapping region of the input image; becomes one token | 固定大小的非重叠图像区域；成为一个 token |
| Patch embedding | "Linear projection" | A shared learned matrix (or Conv2d with stride=P) mapping flattened patch pixels to D-dim vectors | 共享的学习矩阵（或步长为 P 的 Conv2d），将展平的 patch 像素映射为 D 维向量 |
| CLS token | "Class token" | Prepended learnable vector whose final hidden state represents the whole image; optional in 2026 | 前置可学习向量，其最终隐藏状态代表整张图像；2026 年可选 |
| Register token | "Sink token" | Extra learnable tokens that absorb the high-norm attention artifacts ViTs develop during pretraining | 额外可学习 token，吸收 ViT 预训练中产生的高范数注意力伪影 |
| Position embedding | "Positional info" | Per-position vector or rotation making the sequence-order-aware; 2D-RoPE is the modern default | 每个位置的向量或旋转，使序列具有顺序感知；2D-RoPE 是现代默认方案 |
| Grid | "Patch grid" | The (H/P) x (W/P) 2D array of patches for a given resolution and patch size | 给定分辨率和 patch 大小下的 (H/P) x (W/P) 2D patch 数组 |
| NaFlex | "Native flexible resolution" | SigLIP 2 feature: single model serves multiple aspect ratios and resolutions without retraining | SigLIP 2 特性：单一模型服务多种宽高比和分辨率，无需重新训练 |
| Backbone | "Vision tower" | The pretrained image encoder whose patch-token outputs feed the LLM in a VLM | 预训练的图像编码器，其 patch-token 输出喂入 VLM 中的 LLM |
| Pooling | "Image-level summary" | Strategy to turn patch tokens into one vector: CLS, mean, attention pool, or register-based | 将 patch token 转为一个向量的策略：CLS、均值、注意力池化或基于 register |
| Patch 14 vs 16 | "Finer vs coarser grid" | Patch 14 produces more tokens per image, better fidelity for OCR, slower; patch 16 is the classic default | Patch 14 每张图产生更多 token，OCR 保真度更高但更慢；patch 16 是经典默认值 |

## Daha fazla okumak

- [Dosovitskiy et al. — An Image is Worth 16x16 Words (arXiv:2010.11929)](https://arxiv.org/abs/2010.11929) orijinal ViT.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [He et al. — Masked Autoencoders Are Scalable Vision Learners (arXiv:2111.06377)](https://arxiv.org/abs/2111.06377) MAE, kendi kendine denetimli bir eğitim öncesi eğitim.
  Çeviri:M.A.E.
- [Oquab et al. — DINOv2 (arXiv:2304.07193)](https://arxiv.org/abs/2304.07193) Ölçüsel kendiliğinden distillasyon, etiket yok.
  Çeviri: Büyük boyutlu, etiket gerektirmez.
- [Darcet et al. — Vision Transformers Need Registers (arXiv:2309.16588)](https://arxiv.org/abs/2309.16588) kayıt simgeler ve eser analizleri.
  Çin Çeviri: Kayıt simgesi
- [Tschannen et al. — SigLIP 2 (arXiv:2502.14786)](https://arxiv.org/abs/2502.14786) 2026'da standart görme kulesi.
  Çinçe Çevirisi:2026 Year默认的视觉塔──
- [Zhai et al. — Scaling Vision Transformers (arXiv:2106.04560)](https://arxiv.org/abs/2106.04560) Empirik ölçekleme yasaları.
  Çinçe Çevirisi: Experiência缩放定律
