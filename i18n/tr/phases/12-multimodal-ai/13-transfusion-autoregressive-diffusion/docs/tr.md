# Transfüzyon: Autoregressive Text + Diffusion Image in One Transformer  Transfusion: a Transformer 兼做自归文本和扩散图像

> Chameleon ve Emu3 her şeyi ayrı tokenlere bahse girdiler. Çalışırlar, ancak kuantitasyon boğazı görünür  Sürekli uzay yayılma modelleri altında görüntü kalitesi platoları. Transfüzyon (Meta, Zhou ve diğerleri, Ağustos 2024) tam ters bahis yapar: görüntüleri sürekli tutun, VQ-VAE'yi tamamen düşürün ve iki kayıpla bir transformatörü eğitiniz. Metin tokenleri bir sonraki token tahminini alır. Görüntü patchleri akış eşleşimi / difüzyon kaybı elde eder. Her iki hedef de aynı ağırlıkları optimize eder. Stable Diffusion 3 (MMDiT) altında yatan mimarlık yakın bir kuzenidir. Bu ders Transfusion tezini okuyor, oyuncak iki kaybı eğitimi yapan bir oyuncak inşa ediyor ve bir transformatörün her iki işi de yapmasına izin veren dikkat maskesini izliyor.

> **【中文解读】**Transfusion(Meta,2024年8月) seçti Chameleon/Emu3 相反的路径:保持图像为连续表示,无需VQ-VAE,用一个变压器 同时跑两个损失文本代币 用下一个代币 预测,图像补丁用流匹配/扩散损失──Stable Diffusion 3 MMDiT 架构就是近亲──

> **【拓展：双损失训练的工程挑战】**Transfüzyonun temel zorluğu, iki sayısal ölçek farklı kayıp fonksiyonunun dengelenmesinde bulunmaktadır. NTP kayıp ve yayılma MSE kayıpları miktar sınıfı farkları bir kayıp yönetici eğitimiye yol açabilir.

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, two-loss trainer on MNIST-scale toy) | **语言:** Python（标准库，MNIST 规模玩具的双损失训练器）
**Prerequisites:** Phase 12 · 11 (Chameleon), Phase 8 (Generative AI) | **前置知识:** Phase 12 · 11（Chameleon），Phase 8（生成式 AI）
**Time:** ~180 minutes | **时间:** ~180 分钟

>  **【前置】**Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özetle: Özet
>  **【类比】**Transfusion = "双拼户型"──Chameleon = 一居室(bütün içerik aynı token ile);LLaVA = 联排别(视觉和文本完全分开,靠桥接连接);Transfusion = 双拼(一边文本 next-token loss,一边图像扩散 loss,共享承重墙 = 同一个变体器 骨干)──2 hasar ortak olarak optimization 组参数, kendi modelleri avantajlarını korumak.
> ️ **【易错点】**两个损失直接相加而不调权重 → 一个损失主导训练(通常扩散 MSE 数值大,文本 NTP被淹没) ・修复:使用损失权重(如 λ_text=1.0, λ_image=0.1) 或 GradNorm自适应平衡──

## Öğrenme hedefleri

- Tek omurgasına iki kayıp (metin jetonlarında NTP, görüntü yamalarında difüsiyon MSE) yapan bir transformatörü telleştirin.
  >  Aynı kemik üzerinde iki zararla çalışabilecek bir Transformer inşa et 
- Resim yamaları arasındaki iki yönlü dikkatin ve metin işaretleri üzerinde nedenlik dikkatin neden doğru maske seçeneği olduğunu açıklayın.
  > 解释为什么"图像补丁双向 + 文本代币因果"是正确的掩码选择──
- Transfusion tarzı (daima görüntüler, difüzyon kaybı) ile Chameleon tarzı (diskret görüntüler, NTP) hesaplama, kalite ve kod karmaşıklığı ile karşılaştırın.
  > Transfusion 风格 (→连续图像、扩散损失) ile Chameleon 风格 (→ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎
- MMDiT'nin katkılarını belirtin: her blokta modalite spesifik ağırlıklar, kalan akımdaki ortak dikkat.
  > 列举 MMDiT'nin katkıları: Her blokun biçimi belirli bir ağırlık、残差流の共同注意──

## Sorun  sorun arka planı

Diskret vs. Sürekli görüntü belirtileri tartışması LLM'lerden daha eski. Sürekli temsiller (çık pikseller, VAE latenları) ayrıntıları korur. Diskret belirtiler (VQ indeksleri) transformatörün yerel sözlüklerine uyar ancak kuantitasyon aşamasında ayrıntıları kaybeder.

> 离散与连续图像代币的争论比 LLM 更早──连续表示(原始像素、VAE 潜变量)保留细节──离散代币(VQ 索引) Transformer'ın orijinal sözcük listesine uygun, ancak 量化步骤中损失细节──

Chameleon / Emu3 ayrılığa girdi: bir kayıp, bir mimarlık, ancak görüntü sadakati tokenizer kalitesi ile sınırlandı.

> Chameleon / Emu3 选择离散:一个损失,一个构架,但图像保真度受到分词器质量的限制──

Diffusion modelleri sürekli devam etti: olağanüstü görüntü kalitesi, ancak LLM'den ayrı bir model, karmaşık gürültü programı mühendisliği ve metin üretimi ile temiz bir entegrasyon yoktu.

> 扩散模型选择连续:卓越的图像质量, ancak LLM ile bağımsız bir modeldir, karmaşık bir gürültü düzenleme yapısı gerektirir, metin ile net birleştirme yapamaz.

Transfüzyon soruyor: İkisini de alabilir miyiz? Resimleri sürekli tut, bir model eğit, iki kayıpı bir gradient adımına dikişleyerek kullan.

> Transfusion 问:能否兼得两者? image连续,仍然训练一个模型,用两损拼拼接到一个梯度步骤中──

## Konsepten bir şey.

> **【中文解读】**TransFusion(Meta) kendi kendine dönüşecek metin oluşturma ve yayılma modelleri resim oluşturma birleşme içinde aynı Transformer: metin belirti Kullanım bir sonraki belirti tahmin kaybı, resim belirti Kullanım yayılma kaybı── iki biçim paylaşmak aynı model parametreleri ama farklı eğitim hedefleri kullanmak──

> **【拓展：多模态训练目标的融合】**TransFusion                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           


### İki kayıp mimarisi

Tek bir dekoderli transformatör, içeren bir dizini işliyor:

> 单一解码器 Transformer 处理 aşağıdaki içeriği içerir:

- Metin işaretleri (BPE sözcükten ayrıntılı).
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri: Çeviri Çeviri Çeviri: Çeviri Çeviri: Çeviri Çev Çev Çev Çev Çeviri Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Ç Çev Çev Çev Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Resim yamaları (doğru, 16x16 piksel blokları bir ViT kodlayıcı girişinin aynı  lineer yerleştirme yoluyla gizli sönük bir şekilde projelendi).
  Çinçe Çevirimiçi: resim yamacı(连续,16x16 像素块通过线性嵌入投影到隐藏维度与ViT 编码器输入相同) ⋅
- `<image>`ve `</image>`Sürekli yamaların yaşadığı yerleri işaretleyen etiketler.
  Çeviri:`<image>`和 `</image>`标签标记连续补丁的位置──

Ön geçiş bir kez geçer. Kayıp her token için iki baştan birini seçer:

> Önceki yazı:

- Metin işaretleri için: sözcük logit başındaki standart çapraz entropi.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Ç Çeviri Çeviri Ç Çeviri Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Çov Çov Ç Ç Ç Ç Çov Çov Ç Çov Çov
- Resim yamaları için: Sürekli yamalardaki difüzyon kaybı  her yamalara eklenen gürültüyü tahmin eder.
  Çinçe Çevirisi: İzleme yama:连续 yama 上的扩散损失预测每个补丁 添加的噪声──

Bu kayıplar, ortak ağırlıkları aynı anda iyileştirir.

> 梯度通过共享的变压器 体回流──两损同时改进共享权重──

### Dikkat maskası: sebepli metin + iki yönlü görüntü

Metin işaretleri nedensel olmalıdır. Bir metin işaretinin gelecekteki metine katılımını veya öğretmenlerin molaları zorlamasını yapmasına izin veremezsiniz.

> 文本符号 必須是因果的不能让文本符号 关注未来文本,否则教师强制会失败――但图像补丁代表一个快照;它们应该在同一图像块内双向关注彼此――

Maske:

> 掩码:

```
M[i, j] = 1 if:
  (i is text and j is text and j <= i)   # causal for text
  OR (i is image and j is image and same_image_block(i, j))   # bidirectional within image
  OR (i is text and j is image and j < i_image_end)   # text attends to previous images
  OR (i is image and j is text and j < i_image_start)   # image attends to preceding text
```

Eğitim ve sonuçlama için blok üçgenli bir maske olarak uygulanır.

> Eğitim ve düşünce sırasında blok üç köşesi için gerçekleştirmek.

### Transformatörün içinde difüzyon kaybı

Düzünlük kaybı standarttır: bir görüntü yamağına gürültü ekleyin, modelden gürültüyü (veya temiz yama, eşdeğer olarak) tahmin etmesini isteyin. Transfüzyon'un versiyonu akış eşleşmesini kullanır  gürültüden temizliğe hız alanını tahmin edin.

> 扩散损失是标准的:给图像补丁 添加噪音,让模型预测噪音(或等价地预测干净补丁) ――Transfusion 版本使用流匹配预测从噪音到干净的速度场──

Eğitim sırasında:
1. Her görüntü yama x0 için rastgele bir zaman adım t örneği.
   Çinçe Çevirimi: her resim yama x0, 采样随机时间步 t──
2. Örnek gürültü ε, hesap xt = (1-t) * x0 + t * ε (akış eşleşmesi için doğrusal interpolasyon).
   ÇXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
3. Transformatör v_theta(xt, t) tahmin eder; kaybı = MSE(v_theta(xt, t), ε - x0).
   Transformer 预测 v_theta(xt, t);损失 = MSE(v_theta(xt, t), ε - x0)。
4. Tekst ile birlikte arka tarafa NTP kayıpları aynı diziden.
   Çin Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri

Sonuç olarak, nesil:
- Metin işaretleri: standart autoregressive örnekleme.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Resim yamaları: önceki metin işaretlerine bağlı difüzyon örnekleme döngüsü (10-30 adım tipik).
  Çinçe Çevirisi: İzleme Çizgi: 以先前文本符号 为条件的扩散采样循环(通常10-30 步) ⋅

### MMDiT: Stable Diffusion 3'ün varianti

Stable Diffusion 3 (Esser et al., Mart 2024) MMDiT (Multimodal Diffusion Transformer) ile Transfusion'un yaklaşık aynı zamanda gönderildi.

> Stable Diffusion 3 (Esser 等人,2024 yıl 3 月) MMDiT (Multiform Transfusion) yayınladı,

MMDiT'nin temel farklılıkları:

> MMDiT'in anahtar farkları:

- Modallık-specifik ağırlıklar blok başına. Her transformatör bloku metin jetonları karşı görüntü yamaları için ayrı Q, K, V ve MLP ağırlıkları vardır. Dikkat ortak (çapraz modalik); diğer her şey modalik-specifiktir.
  Çinçe çevirisi: Her blokun modolu belirli bir ağırlıklılıktir. Her transformator blokunun bağımsız metin simgesi var.
- DDPM'den daha basit bir matematik ve örnekleme ile ilgili özel bir akış uyarlama varianti.
  Çinçe çevirisi:整流流训练──一种特定流匹配变体,采样已知,数学比DDPM更简单──
- Skala. MMDiT SD3'in omurgasıdır (2B ve 8B param varianları).
  Çinçe Çevirimiçi: 規模──MMDiT 是 SD3 的主干(20 億和 80 億参数变体)──Transfusion 论文扩展到70 亿──

Her ikisi de aynı temel fikir üzerinde birleşir: bir transformatör metinde NTP ve sürekli görüntü temsillerinde yayım yürütür.

> 两者收到同一核心理念: Transformer 在文本上运行NTP, 在连续图像表示上运行扩散──

### Neden bu, kameleon tarzını yendi?

Görüntü üretimi sırasında sürekli yayılma ve ayrı-ayrı NTP arasındaki kalite farkı ölçülebilir.

> 连续扩散和离散 NTP 图像生成上的质量差可量化──Transfusion 论文报告:

- 7B paramlarında, aynı boyutlu bir Cameleon tarzı modeli FID'de 3-5 puan geçiyor.
  Çin dilinde:70 milyar 参数下,FID 上击败同规模的马龙 风格模型 3-5 分──
- Tokenizer eğitimi gerekmez  görüntü kodlayıcı daha basit (Sınırlı projeksiyon gizli, bir ViT'nin giriş katmanı ile aynı).
  Çinçe Çevirimiçi:不需要分词器训练图像编码器更简单(线性投影到隐藏层,与ViT 输入层相同)
- Inferans, autoregressive görüntü belirtilerinin aksine, görüntü yama tanımlamasını paralelleştirebilir.
  Çinçe çevirisi: 推理可以并行化图像补丁 去噪,自归图像代号与不同──

Eksik taraf: Transfüzyon ikili kayblı bir modeldir, bu da eğitim dinamiklerini daha zorlaştırır. Kayıp ağırlıkların ayarlanması gerekir. NTP ve difüzyon arasındaki zamanlama eşleşmezliği bir başın baskısına neden olabilir.

> 缺点:Transfusion is a double loss model, training dynamics more complex。 weight loss needs to be adjusted。 NTP ve yayılma arasındaki düzenlilik uyumsuzluğu bir başlıca yönlendirmeye yol açabilir。

### Akıntıda oturanlar

Janus-Pro (Desin 12.15) Transfusion'un fikrini, Transfusion'un transforman vücudu paylaşırken bir tanesi için SigLIP, diğer tanesi için VQ'yi ayırarak ve anlayış ve jenerasyon için vizyon kodlayıcısını ayırarak geliştirir. Show-o (Desin 12.14) difüzyonu diskret difüzyon (maskeli tahmin) için değiştirir.

> Janus-Pro (第 12.15 课) Çözüm yoluyla 视觉编码器  Transfusion'ın düşüncesini geliştirdi SigLIP anlam için kullanıldı, VQ  Transformer 主体── Show-o (第 12.14 课) 扩散换为离散扩散──掩码预测──统一生成家族在 Transfusion 后迅速分化──

2026 üretiminde görüntü yayımlayan VLM'ler  Gemini 3 Pro, GPT-5, Claude Opus 4.7'in görüntü oluşturma yolu  neredeyse kesinlikle bu ailenin bazı soyundan gelmektedir.

> 2026 yılında VLMGemini 3 Pro、GPT-5、Claude Opus 4.7'ün görüntü üretimi yolu bu ailenin sonraki nesilleri tarafından kullanıldığından neredeyse emin olabilir.


> **【拓展：TransFusion 的推理过程】**TransFusion  Düşünme zamanı kilit adımlar: metin token kendi kendine geri dönüştürülür, görüntülere rastlanırken işaretlenmeye başlar ve genişleme modüsüne geçilir.


## Kullanın.
```figure
cfg-guidance-scale
```

## Kullan

`code/main.py`Küçük bir MNIST gibi bir soruya karşı oyuncak Transfusion inşa ediyor:

> `code/main.py`Küçük MNIST  sorun üzerinde yapılandırma oyuncak Transfüzyon:

- Metin başlıkları, bir rakamı (0-9) tanımlayan kısa tam sayı dizisidir.
  Çinçe Çevirim:文本描述是描述数字(0-9) 的短整数序列──
- Resimler 4x4 bayt ağları.
  Çinçe Çevirisi:图像是4x4 字节网格。
- Ortak ağırlıklı bir çift doğrusal projeksiyon, transformatörün yerine geçer; metinde NTP kaybı, gürültülü yamalarda MSE kaybı.
  Çinçe Çevirisi: 一对共享权重的线性投影作为变压器 替代;文本用NTP 损失,噪音补丁用MSE 损失──
- Eğitim döngüsü iki kayıpı değiştirir, dikkat maskası açıkça.
  Çin Çeviri: Çeviri değişimi iki kayıp, dikkatli örtüşme açıkça görülüyor.
- Genre bir ileri geçit içinde bir metin başlığı ve 4x4 resmi üretir.
  Çine Çeviri: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi: Çizgi:

İki kayıplı tesisat, dikkat maskası yapımı ve sonuç döngüsü gerçek eserlerdir.

> Transformer oyuncak sınıfıdır. İki kayıp boru hattı, dikkat saklama yapı ve düşünce döngüsü gerçek ürünlerdir.

## Gönderin.

Bu ders bize çok yararlı .`outputs/skill-two-loss-trainer-designer.md`Yeni bir multimodal eğitim görevi (metin + görüntü, metin + ses, metin + video) göz önüne alındığında, iki kayıp programını (kayıp ağırlıklar, maske şekli, paylaşılan vs. modalite özel bloklar) tasarlıyor ve uygulama risklerini işaretliyor.

> 本课产 出 `outputs/skill-two-loss-trainer-designer.md`◊ Yeni bir çok biçimli eğitim görevi belirledi: ((文本+图像、文本+音频、文本+视频), iki kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez daha bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez bir kez daha bir kez bir kez bir kez daha bir kez bir kez daha bir kez daha bir kez bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha bir kez daha daha bir kez daha daha bir kez daha daha daha daha bir kez bir kez daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha

## Egzersizler.

1. Transfusion tarzındaki bir model, %70 metin jetonu ve %30 görüntü yamalarını eğitir.
   Çinçe Çevirimi:Transfusion 风格模型训练 70% 文本代币 和 30% 图像补丁──图像扩散损失在量级上约为文本NTP 损失的10倍──什么损失权重能平衡它们?

2. Bir dizi için blok üçgenli maskeyi uygulayın: `[T, T, <image>, P, P, P, P, </image>, T]`Her giriş 0 veya 1 olarak işaretlenir.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Çeviri Çeviri Ç Ç Ç Ç Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç`[T, T, <image>, P, P, P, P, </image>, T]`实现块三角掩码──标记每个条目为0或1──

3. MMDiT'de modalite-specifik QKV ağırlıkları var. Bu hangi parametreler sayımı üstü ekliyor vs Transfusion'un tam paylaşılan transformatörü? 7B parametrelerinde, buna değer mi?
   Çinçe Çevirimi:MMDiT has a mode of specific QKV 权重──相比 Transfusion'ın 完全共享变压器 多少参数增加了?70亿参数下值值吗?

4. Üretim: bir metin istek verildiğinde, model 50 token için NTP çalıştırır, sonra vurur `<image>`...denoise adımları üzerinde 256 yama üzerinde yayılma çalışır.
   Çeviri: NTP 50 个 token, sonra karşılaştık `<image>`Sonra 256 patçta 20 adımla yayılmış bir gürültü var.

5. SD3 kağıdı bölüm 3. DDPM'den daha az sonuç aşamasında neden birleştiğini ve düzeltilmiş akışı açıkla.
   Çinçe çevirisi: SD3'yi okuyun.

## Anahtar Terimler

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Two-loss training | "NTP + diffusion" | A single transformer optimizes both cross-entropy on text tokens and MSE on continuous image patches in the same gradient step | 单一 Transformer 在同一梯度步中优化文本 token 交叉熵和连续图像 patch MSE |
| Flow matching | "Rectified flow" | Diffusion variant that predicts a velocity field from noise to clean data; simpler math than DDPM | 预测从噪声到干净数据速度场的扩散变体；数学比 DDPM 更简单 |
| MMDiT | "Multimodal DiT" | Stable Diffusion 3's architecture: joint attention, modality-specific MLPs and norms | SD3 架构：联合注意力、模态特定 MLP 和归一化 |
| Block-triangular mask | "Causal text + bidirectional image" | Attention mask that is causal across text but bidirectional within image regions | 文本因果、图像区域内双向的注意力掩码 |
| Continuous image representation | "No VQ" | Image patches as real-valued vectors, not integer codebook indices | 图像 patch 为实值向量，非整数码本索引 |
| Velocity prediction | "v-parameterization" | Network output is the velocity field between noise and data, not the noise itself | 网络输出为噪声和数据之间的速度场，非噪声本身 |

## Daha fazla okumak

- [Zhou et al. — Transfusion (arXiv:2408.11039)](https://arxiv.org/abs/2408.11039)
  Çeviri: Transfusion
- [Esser et al. — Stable Diffusion 3 / MMDiT (arXiv:2403.03206)](https://arxiv.org/abs/2403.03206)
  中文翻译:Stable Diffusion 3 / MMDiT 论文。
- [Peebles & Xie — DiT (arXiv:2212.09748)](https://arxiv.org/abs/2212.09748)
  Çeviri:DİT 扩散 Transformer 论文。
- [Zhao et al. — MonoFormer (arXiv:2409.16280)](https://arxiv.org/abs/2409.16280)
  Çeviri: MonoFormer
- [Xie et al. — Show-o (arXiv:2408.12528)](https://arxiv.org/abs/2408.12528)
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
