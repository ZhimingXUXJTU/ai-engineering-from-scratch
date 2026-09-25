# Göster-o ve Diskret-Difusion Birleştirilmiş Modeller

> Transfüzyon sürekli ve ayrı temsilleri karıştırır. Show-o (Xie et al., Ağustos 2024) diğer tarafa gider: metin tokenleri sebepçi bir sonraki token tahminini kullanır, görüntü tokenleri MaskGIT ruhunda maskeli ayrı yayımı kullanır. İkisi de hibrit bir dikkat maskesine sahip bir transformatörün içinde oturuyor. Sonuç, bir omurgan, modalite başına bir tokenizer, bir kayıp formülasyonu (maskeli tahminlere uzanan bir sonraki token) üzerinde VQA, metin-resim, boyalama ve karışık modalite jenerasyonunu birleştirir. Bu ders, Show-o tasarımını  neden maskeli ayrı yayılma paralel, birkaç adımlı bir görüntü jeneratörü  ve Transfusion ve Emu3 ile karşıtlık gösterir.

> **【中文解读】**Show-o(2024年8月)走另一条路:文本代币 用因果下一代币 预测,图像代币 用掩码离散散散散散(MaskGIT 风格) ・・・ ikisi de ortak bir Transformer,混合注意力掩码── sonuç bir kontrol noktası 同时支持 VQA、文本生成图像和图像修复──

> **【拓展：并行解码的速度优势】**Show-o 生成图像只需约16步,而 Chameleon/Emu3 需要1024-4096步,而Emu3 需要1024-4096步,而Emu3 需要1024-4096步,而Emu3 需要1024-4096步,而Emu3 需要1024-4096步,而Emu3 需要1024-4096步,而Emu3 需要1024-4096步,而Emu3 需要1024-4096步.

**Type:** Learn  | **类型:** 学习
**Languages:** Python (stdlib, masked-discrete-diffusion sampler) | **语言:** Python（标准库，掩码离散扩散采样器）
**Prerequisites:** Phase 12 · 13 (Transfusion) | **前置知识:** Phase 12 · 13（Transfusion）
**Time:** ~120 minutes | **时间:** ~120 分钟

>  **【前置】**Öğrenci bölümün önüne geçerek:Fase 12·13(Transfusion 双损失)、Fase 12·11-12(Chameleon/Emu3 离散代币)、Fase 8(MaskGIT 离散扩散概念)。Show-o = 全离散 + 图像用 MaskGIT 风格并行解码,速度比 Emu3 快 60 倍。
>  **【类比】**Show-o = "并行开锁"──Emu3 = 一把钥匙开 1024 把锁(自归单个代币);Show-o = 16 步内同时尝试所有锁(掩码扩散并行解码)──代价:图像质量略差(VQ 量化损失),但推理快得多──

## Öğrenme hedefleri

- Maskeli ayrı yayımı açıklayın: simgelerinin bir şekilde maskelediği program, daha sonra transformatörden onları kurtarmasını ister.
  > 解释掩码离散扩散:均掩码 token sonra Transformer 恢复它们的调度──
- Hız ve kalite açısından paralel görüntü çözümü (Show-o, MaskGIT) ile autoregressive görüntü çözümü (Chameleon, Emu3) karşılaştırın.
  > Göster-o、MaskGIT) ile kendi kendine dönüşümlü görüntü çözümü için yapılan bir karşılaştırma.
- Show-o'nun tek kontrol noktasında yerine getirdiği üç görevi: T2I, VQA, görüntü boyaması.
  > Bir kontrol noktasında desteklenen üç görev: T2I、VQA、 görüntü onarım。
- Bir maskeleme programı seçin (kozin, doğrusal, kısaltılmış) ve örnek kalitesine etkisini düşünün.
  > 选择掩码调度 (余弦、线性、截断) ve 采样质量 üzerindeki etkisini analiz eder.

## Sorun  sorun arka planı

Transfusion'un iki kaybı eğitim çalışması ancak daha karmaşık dinamiklere sahiptir.  Sürekli difüzyon kaybı ayrı NTP kaybından farklı bir sayısal ölçekte yaşar.

> Transfüzyon ikili kaybı eğitimi uygulanabilir ama dinamik daha karmaşık                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            

Show-o'nun cevabı: her iki modaliteti de ayrı tutun (Chameleon gibi), ancak sıradan değil maskeli ayrı yayılım yoluyla paralel olarak görüntüler oluşturun. Eğitim amacı, doğal olarak bir sonraki token-böyleceyi genelleştiren tek maskeli-token-böyleceye dönüşür.

> Gösterme-o'nun cevabı: iki biçimi tutmak, birbiriyle dağılmak gibi bir şeydir, ama örtülü bir şekilde dağılmak ve görüntü üretmek için bir yol izler.

## Konsepten bir şey.

> **【中文解读】**Gösterme 统一多模态理解和生成, 离散扩散的使用代替传统连续扩散──离散扩散的直接在代号级操作中,将遮盖预测(理解任务) 和去噪(生成任务)统一在同一框架下──

> **【拓展：离散扩散的统一优势】**离散扩散将文生成和图像生成统一到同一个数学框架 (BKT) 掩码代币 预测),多模态联合训练更简单―― 2025 yılının多模态 AI 趋势方向――


### Maskeli diskre difüzyona (MaskGIT)

Orijinal Chang et al. (2022) MaskGIT hilesi zarif. Tamamen maskeli bir görüntüden başlayın (her token özel bir simge)`<MASK>`id). Her adımda, tüm maskeli jetonları paralel olarak tahmin edin, sonra en güvenli tahminleri top-K'ye tutun ve geri kalanı yeniden maskelize edin. ~ 8-16 iterasyondan sonra, tüm jetonlar doldurulur.

> İlk kez, maskecilik teknikleri çok güzeldi.`<MASK>`ID) ・ her adım tüm gizleme simgelerini tahmin eder, sonra üst-K'yi korur, en güvenilir tahminler ve geri kalanı yeniden gizler.

Eğitim basit: maskeli oranı [0, 1'den] eşit bir şekilde örnekleyin, resmin VQ simgelerine uygulayın, transformatörü maskeli simgelerden kurtarmak için eğitin. BERT'in metin için yaptığı şey, görüntü üretimi için ölçeklendirilmiştir.

> 訓練很簡單: 來自 [0, 1] 均采样掩码比例, 應用到图像的VQ token, 訓練 變形器 恢复被掩码的 token──就是BERT对文本做,扩展到图像生成──

### Gösterme: bir transformatör, hibrit maske

Gösterme MaskGIT'i bir nedenci dil model transformatörüne koyar.

> Şov-o MaskGIT 放入因果语言模型 Transformer 中──注意力掩码是:

- Metin işaretleri: sebepli (standart LLM).
  Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çöntem: Çön: Çöntem: Çön: Çöntem: Çönçüm: Çöntem: Çöntem: Çönçüm: Çöntem: Çönçüm: Çöntem: Çönçüm: Çönçüm: Çöntem: Çönçüm: Çönçüm: Çönçüm: Çönçüm: Çönçüm: Çönçüm: Çönçüm:
- Resim jetonları: görüntü blokunun içinde tam iki yönlü (onlar maskeli jetonlar tahmin sırasında diğer tüm resim jetonlarını görebilir).
  Çinçe Çevirimiçi:图像代号:图像块内全双向(掩码代号:图像块内全双向(掩码代号:图像代号:图像块内全双向(掩码代号:图像代号:图像块内全双向(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((
- Metin-resim: metin önceki görüntülere, görüntü önceki metine hizmet eder.
  Çin Çeviri:文本到图像:文本关注之前的图像,图像关注之前的文本──

Eğitim değişimi:
1. Metin dizilerinde standart NTP.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri
2. T2I örnekleri: maskeli görüntü belirtileri olan metin → görüntü, maskeli belirtiler-böylece kaybı.
   Çeviri:T2I 样本:文本→带掩码图像代号的图像,掩码代号 预测损失──
3. VQA örnekleri: maskeli metin işaretleri ile görüntü → metin (gerçekten sadece NTP).
   Çeviri:VQA 样本:图像→带掩码文本代币 的文本(实际上就是 NTP) 』

Tek bir kayıp , çapraz entropi .`<MASK>`Tokens, hem metin NTP (sadece son token "maskelidir") hem de görüntü maskeli yayımı (hassasi alt kümesi maskelidir) kapsar.

> 统一损失是                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        `<MASK>`Son bir simge ise "asfalt" ve resim örtü genişletilmesi (asfalt)

### Dönüşteki örnekleme

Show-o, ~ 1000 (tekon başına otomatik gerileme) veya ~ 20 (haşlama) yerine ~ 16 adımla bir görüntü oluşturur. Her adımda, tüm maskeli jetonları paralel olarak tahmin edin; üst-K güvenini yükleyin; tekrarlayın.

> Gösterme, yaklaşık 16 adım içinde görüntü oluşturur, 1000 adım yerine (tık başına dönüştürülür) veya 20 adım yayılır.

Benzer şekilde:
- Chameleon / Emu3 (token üzerinde otomatik olarak geri dönük): N_tokens ileri geçişleri, tipik olarak 1024-4096 bir görüntü başına.
  Çinleme:Chameleon / Emu3(逐符号自归):N_tokens 次前向传播,通常每张图像 1024-4096。
- Transfüzyon (daima yayılma): ~ 20 adım, her biri tam bir transformatör geçişi.
  Çeviri:Transfusion (Transfusion) 连续扩散 (Transfusion)
- Show-o (maskeli ayrı yayılma): ~16 adım, her biri tam bir transformatör geçişi.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri: Çeviri Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri: Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç

Show-o benzer ölçekli modellerde Chameleon'dan daha hızlıdır ve Transfusion adım sayısına daha düşük adım maliyetleriyle (düşünçlü kelime logitleri vs sürekli MSE kaybı) yakışır.

> Show-o, aynı büyüklükte bir model üzerinde Camelyon daha hızlı, adım sayısı büyük ölçüde uyumlu Transfusion, ama her adım maliyeti daha düşük(razılaşmış sözcük listesi logits vs 连续 MSE 损失) 👇

### Tek kontrol noktasındaki görevler

Show-o, hızlı biçimle seçilen dört görevden söz eder:

> Göster-o, dört görevden destek gösterir.

- Metin oluşturma: standart autoregressive metin çıkışı.
  Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönüm: Çönönönönönönönönönönönönönönönönönönönönönönönönönönönönönönönönönönönönönönönönön
- VQA: görüntü içeri, mesaj çıkart.
  Çeviri:VQA:图像输入,文本输出.
- T2I: metin içeri, görüntü maskeli ayrı yayılım yoluyla dışarı.
  Çeviri:T2I:文本输入,通过掩码离散扩散输出图像──
- Boyanma: maskeli bir görüntü, doldur.
  Çinçe Çevirimiçi:图像修复:带部分掩码 符号 的图像,填充缺失部分──

VQ-token şebekesi bölgesini maske, geri kalanını besle ve bir metin istek, maske tokenlerini tahmin et.

> 图像修复能力 from掩码预测训练中免费获得──掩码 VQ token 网格的一个区域,进入其余部分加上文本提示,预测被掩码的 token──

### Maskeleme programı

Adım başına kaç tane simge açılması programı kaliteyi şekillendirir.

> Her adım çözülür.

```
mask_ratio(t) = cos(pi * t / (2 * T))   # t = 0..T
```

T'de hiçbir şey maskeli değildir. Cosine, kütleyi tahminlerin en bilgilendirici olduğu orta aralık oranlarında yoğunlaştırır. Düzsel programlar da çalışır ancak plato daha hızlıdır.

> İlk adım, tüm simgeler gizli kalır.

### Gösterme

Show-o2 (2025 takip, arXiv 2506.15564) ölçekleri Show-o: daha büyük LLM tabanı, daha iyi tokenizer, geliştirilmiş maske programı. Aynı mimari örneği.

### Show-o oturduğu yerde

2026 taksonomisi:

> 2026 yılının sınıfları arasında:

- Diskret tokenler + NTP: Kameleon, Emu3. Basit ama yavaş sonuç.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Çeviri Çeviri Ç Ç Ç Ç Çeviri Çeviri Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Çovi Çovi Çovi Çovi Ç Çovi Çovi Ç Ç Ç Ç Çovi Ç
- Diskret tokenler + maskeli yayılma: Show-o, MaskGIT, LlamaGen, Muse.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Ç Çeviri: Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Sürekli + difüzyon: Transfüzyon, MMDiT, DiT. En yüksek kalitede, daha karmaşık eğitim.
  Çeviri: 延续 + 扩散:Transfusion、MMDiT、DiT──最高质量,训练更复杂──
- Bir VLM'de sürekli + akış eşleşimi: JanusFlow, InternVL-U. En yeni.
  Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:VLM, Çeviri:

Görevler doğrultusunda seçin: T2I + boyamak + VQA'yı uygun bir hızla bir açık modelde istediğinizde gösterin; Kalite en önemli olduğunda ve iki kayıplı tesisat için para alabildiğinizde nakli.

> 按任务选择: needs an open model simultaneously do T2I + 修复 + VQA 且速度合理时选 Show-o;质量至上且能承担双损失复杂性时选 转血──


> **【拓展：Show-o 的离散扩散方法】**Gösterme-o'nun ayrıntılı yayılması örtüleme tahminleri kullanımı:随机遮盖部分 token,模型预测被遮盖的 token──理解任务遮盖答案部分,生成任务从全遮盖开始逐步到噪声──数学上等价于多项式扩散──


## Kullanın.
```figure
masked-diffusion-unmask
```

## Kullan

`code/main.py`gösterme örneklemesini simüle eder:

> `code/main.py`Şov-o 采样:

- 16 VQ tokeni olan bir oyuncak şebekesi.
  Çin Çeviri: 16 VQ tokenı
- Bir çağrı ve şu anda maskeli olmayan tokenlere dayanarak logitleri tahmin eden sahte bir "transformer".
  Bir de "Transformer" şeklinde bir işaret oluşturulmuştur.
- Paralel maskeli örnekleme 8 adım boyunca cosine programı ile.
  Çinçe Çevirim: 余弦调度下 8 步并行掩码采样──
- Orta durumları (mask örneği evrimi) ve son belirtileri yazdırır.
  Çinçe Çevirim: 打印中间状态 (BİRÇİN)

İndir, maskenin adım adım çözülmesini izle.

> - Yapma, gözlemle.

## Gönderin.

Bu ders bize çok yararlı .`outputs/skill-unified-gen-model-picker.md`. Açık ağırlık kısıtlaması ile hem anlayış (VQA, başlık) hem de nesil (T2I, boyanma) gerektiren bir ürün göz önüne alındığında, Show-o ailesi, Transfusion/MMDiT ailesi ve Emu3/Chameleon ailesi arasında kesin bir pazarlık yaparak seçim yapılır.

> 本课产 出 `outputs/skill-unified-gen-model-picker.md`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △                          

## Egzersizler.

1. 16 adımla maskeli ayrı difüzyon örnekleri. Neden 1 değil?
   Çinçe Çevirim: maskode ayrıştırma yayılması yaklaşık 16 adım içinde yayılmaktadır.

2. Show-o'nun boyası uzman bir modeli yendiği bir ürün kullanım durumunu (gerçek veya hipotetik) önerin.
   Çinçe çevirisi:掩码扩散的图像修复是免费的── önerdi bir Show-o 修复能力胜过专业模型的产品用例──

3. Kosine planı vs. doğrusal plan: T=8 için adım başına maskeli olmayan token sayısını izleyin. Hangisi daha dengeli?
   Çinçe çevirisi: 線性调度 vs.余弦调度: 線性调度: 追踪 T=8 时每步解掩码的符号 数――哪个更均衡?

4. 512x512 Gösterme görüntü 1024 simgeliktir. K=16384 sözcükte, model 1024 * log2(16384) = 14.336 bit (~1.75 KiB) veri yayar.
   ÇINCE TRÜBLİK:512x512 Gösterin 图像是1024 个标志──词汇表 K=16384 下,模型输出约1.75 KiB 数据──SD 输出约768 KiB 原始像素──压缩比是多少?换来什么质量?

5. LlamaGen'in sınıf koşullu autoregressive görüntü modeli Show-o'nun maskeli yaklaşımından nasıl farklıdır?
   LlamaGen'in sınıf koşulları, Show-o'nun gizleme yönteminden ne kadar farklıdır?

## Anahtar Terimler

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Masked discrete diffusion | "MaskGIT-style" | Training to predict masked tokens; at inference, iteratively unmask the most-confident predictions | 训练预测掩码 token；推理时迭代解掩码最有信心的预测 |
| Cosine schedule | "Unmask schedule" | Decay of mask ratio over inference steps; concentrates confidence growth at mid-range | 推理步骤中掩码比例的衰减；将信心增长集中在中程 |
| Parallel decoding | "All tokens at once" | Every step predicts the full sequence of masked tokens in one forward pass, then commits top-K | 每步在一次前向传播中预测所有掩码 token，然后提交 top-K |
| Hybrid attention | "Causal + bidirectional" | Mask that is causal over text tokens and bidirectional within image blocks | 文本 token 因果、图像块内双向的掩码 |
| Inpainting | "Fill-in generation" | Condition on an image with some tokens masked, predict the missing ones; free from the training objective | 以部分掩码图像为条件，预测缺失 token；从训练目标免费获得 |
| Commitment rate | "Top-K per step" | How many tokens are declared "done" per iteration; controls inference vs quality trade-off | 每次迭代声明"完成"的 token 数；控制推理与质量的权衡 |

## Daha fazla okumak

- [Xie et al. — Show-o (arXiv:2408.12528)](https://arxiv.org/abs/2408.12528)
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Show-o2 (arXiv:2506.15564)](https://arxiv.org/abs/2506.15564)
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çev Çeviri Çev Çeviri Çev Çev Çeviri Çeviri Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- [Chang et al. — MaskGIT (arXiv:2202.04200)](https://arxiv.org/abs/2202.04200)
  Çeviri:MaskGIT, mask码离散扩散的原始工作.
- [Sun et al. — LlamaGen (arXiv:2406.06525)](https://arxiv.org/abs/2406.06525)
  Çeviri:LlamaGen
- [Chang et al. — Muse (arXiv:2301.00704)](https://arxiv.org/abs/2301.00704)
  Çeviri:Muse 掩码图像生成──
