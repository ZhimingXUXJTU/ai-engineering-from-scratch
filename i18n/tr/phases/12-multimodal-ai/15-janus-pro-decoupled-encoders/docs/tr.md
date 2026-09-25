# Janus-Pro: Birleştirilmiş Çok Modal Modeller için Çıkarılmış Kodlayıcılar

> Birleştirilmiş multimodal modeller kaçınılmaz bir gerginliğe sahiptir. Anlamak anlamlı özellikler ister  SigLIP veya DINOv2 konsept düzeyde bilgi zengin çıkış vektörleri. Genre yeniden inşa etmek için dostu kodlar istiyor. VQ tokenleri, tekrar net piksellere dönüştürülür. İki hedef tek bir kodlama ile uyumlu değil. Janus (DeepSeek, Ekim 2024) ve Janus-Pro (DeepSeek, Ocak 2025) çözümün denemeyi bırakmak olduğunu iddia ediyor: iki kodlayıcıyı kopartma. Transformer vücudu görevler arasında paylaşın, ancak SigLIP ile yol anlayışı ve VQ tokenizer aracılığıyla üretim. 7B'de, Janus-Pro, GenEval'de DALL-E 3'ü yenerken MMMU'da LLaVA'ya eşleşir. Bu ders, iki kodlamanın neden birinde başarısız olduğu konusunda açıklıyor.

> **【中文解读】**Janus-Pro(DeepSeek,2025年1月) bir temel çelişkiyi çözmek: anlamlı görevler gerekçe ifade özellikleri(SigLIP), oluşturma görevleri yeniden inşa etmek gerekçe dostlu kodlama(VQ token) ・・・ ikisi de tek bir kodlama makinesine uyumsuz olması gerekir。Janus-Pro'nun yanıtı şu: anlamlı  SigLIP 路径,生成走 VQ 路径,共享 Transformer 主体。7B 参数就在 GenEval 上击败了DALL-E 3。

> **【拓展：解耦编码器的产业影响】**解编码器思想 2026 yılında bir bütünleşmiş modelin öntanımlı yapı haline gelmiştir.

**Type:** Build  | **类型:** 构建
**Languages:** Python (stdlib, dual-encoder routing + shared-body signal) | **语言:** Python（标准库，双编码器路由 + 共享体信号）
**Prerequisites:** Phase 12 · 13 (Transfusion), Phase 12 · 14 (Show-o) | **前置知识:** Phase 12 · 13（Transfusion），Phase 12 · 14（Show-o）
**Time:** ~120 minutes | **时间:** ~120 分钟

>  **【前置】**学本节前 Lütfen önce bil:Fase 12·02(SigLIP 语义编码器)、Fase 12·13-14(Transfusion/Show-o 统一模型)、Fase 8(VQ-VAE 重建编码器)。Janus-Pro = "Bilmek vs 生成的编码器分离"是Fase 12 多模态生成模型的最终答案之一──
>  **【类比】**Janus-Pro = "Yok tarafı beyin分工"──左脑 = SigLIP(语义理解,认识"猫"的概念);右脑 = VQ-VAE(像素重建,能画出猫的细节)──其他统一模型 = 强迫一个脑区同时做两件事,两边都不极致;Janus-Pro = 强迫一个脑区同时做两件事,两边都不极致;Janus-Pro = 接受左右脑分工,共享脑干(Transformer 主体) 做高层推理──就像人类视觉皮层理解这个() 和运动皮层(绘画) 本来就在不同脑区──

## Öğrenme hedefleri

- Tek paylaşılmış kodlayıcı neden anlayışa veya üretim kalitesine zarar vereceğini açıklayın.
  > 解释为什么单一共享编码器会损害理解或生成质量──
- Janus-Pro'nun yönlendirmeyi açıklayın: Anlama için giriş tarafında SigLIP özellikleri, giriş ve çıkış için VQ jetonları.
  > 描述 Janus-Pro 的路由:理解路径输入侧使用SigLIP特征,生成路径输入和输出侧都使用VQ token──
- Janus Pro'nun başarısız olduğu yerlerde, Janus'un başarısını sağlayan veri karışımının ölçeklenmesini izleyin.
  > 追溯让Janus-Pro成功而Janus 失败的数据混合扩展──
- Kopyalaşmamış (Janus-Pro), kopyalı-daima (Transfusion) ve kopyalı-diskre (Show-o) mimarlıkları karşılaştırın.
  > Bu yüzden, bu bir şey değil.

## Sorun  sorun arka planı

Birleştirilmiş modeller, anlayış ve nesne boyunca bir transformatör vücudu paylaşır. Önceki girişimler (Chameleon, Show-o, Transfusion) her ikisi de iki yön için bir görsel tokenizer kullanır. Tokenizer bir uzlaşma:

> 统一模型在理解和生成之间共享 Transformer 主体──之前的尝试(Chameleon、Show-o、Transfusion) 都使用一个视觉分词器处理两个方向──分词器是妥协:

- Yeniden inşa (genreasyon) için optimize edilmiş: VQ-VAE ince çekirdeği piksel ayrıntılarını yakalar, ancak zayıf semantik tutarlılıklı jetonlar üretir.
  Çine dilinde: 文文翻译:为重建优化 (生成):VQ-VAE 捕获细粒度像素细节,但产生的代号语义一致性弱──
- Semantik için optimize edilmiş (anlama): SigLIP yerleştirmeler "cat" simgelerinin yakınında "cat" resimlerini gruplandırır, ancak iyi bir yeniden yapılandırmaya izin vermez.
  Çinçe Çevirimiçi:为语义优化(理解):SigLIP 嵌将"猫"图像归归归"猫"的代号附近,但不允许好的重建──

Show-o ve Transfusion bunun için bir yönde görünür bir kalite vergisi ile ödeme yaparlar. Janus-Pro soruyor: görevlerin farklı ihtiyaçları olduğunda neden tek bir tokenizer gerektiren?

> Show-o 和 Transfusion bunun için görünür kalite vergisi ödüyor. Janus-Pro soru: Görev farklı ihtiyaçlar olduğunda neden bir sözcük cihazı kullanmak gerekir?

## Konsepten bir şey.

> **【中文解读】**Janus-Pro(DeepSeek) utilizando解的视觉编码器:一个用于理解任务(CLIP 编码器),一个用于生成任务(VQ 编码器);; iki编码器共享一个LLM 脊柱,各自专注优化不同的视觉表示;;

> **【拓展：解耦编码器的动机】**Bu nedenle, bu programın en önemli yönleri, yani, bir programın en önemli yönleri ve en önemli yönleri vardır.


### Çıkarılmış görsel kodlama

Janus-Pro'nun mimarisi iki kodlayıcıyı ayırır:

> Janus-Pro'nun yapı iki kodlayıcıdan ayrılır:

- Yolu anlamak. Giriş görüntüsü → SigLIP-SO400m → 2 katlı MLP → transformatör vücudu.
  中文翻译:理解路径──输入图像 → SigLIP-SO400m → 2 katlı MLP → Transformer 主体──
- Üretim yolu. Giriş görüntü (var olan bir görüntü üzerinde koşullandırma yapılırsa) → VQ tokenizer → token IDs → transformatör vücudu.
  中文翻译:生成路径──输入图像(如果以现有图像为条件)→ VQ 分词器 → token ID → Transformer 主体──
- Çıktı jenerasyonu. Transformatör → VQ dekoder → piksel tarafından öngörülen görüntü belirtileri.
  中文翻译:输出生成──Transformer 预测的图像代币 → VQ 解码器 → 像素──

Transformer vücudu paylaşılan. Vücudun akıntı ve aşağı akımındaki her şey görev-özel.

> Transformer 主体是共享的. 主体上下游. Tüm içeriği görevden oluşuyor.

Girdiler, hızlı biçimle belirsizleştirilmiştir: a `<understand>`SigLIP üzerinden rotaları işaretle .`<generate>`Ya da görevden dolayı yollama yapılır.

> 输入通过提示格式消歧:`<understand>`标签路由到 SigLIP;`<generate>`VQ'ye giden yol veya görevden gizlenmiş olarak belirlenmiş yol.

### Neden işe yarıyor?

Kayıp anlama, CLIP tarzı öncesi eğitiminin semantik benzerlik için ayarladığı SigLIP özelliklerini alır.

> Anlama kaybı elde SigLIP özellikleri, CLIP 风格的预训已经为语义相似性调优化了这些特征――模型的感知基准测试超过了Show-o / Transfusion,因为输入特征更适合任务――

Genre kaybı, bir tokenizer tarafından yeniden oluşturulmak için ayarlanmış VQ jetonları alır.

> Çözüm: VQ Token,分词器已为重建调优化这些 Token──图像质量超过Show-o,因为 VQ 码能干净地组合回像素──

Paylaşılan transformatör vücudu iki giriş dağıtımını görür (SigLIP ve VQ) ve her ikisiyle de çalışmayı öğrenir.

> 共享的变压器 主体看两种输入分布(SigLIP 和 VQ),学会与两者一起工作──声称:足够的数据 +足够的参数, 主体能吸收切换──

### Veri ölçeklendirme  Janus vs Janus-Pro

Janus (orjinal, arXiv 2410.13848) çözülmeyi başlattı ancak küçük ölçekte (1.3B parametreleri, sınırlı veri).

> Janus(原始版,arXiv 2410.13848) 了解引入但规模较小(13 亿参数,有限数据) ・Janus-Pro(arXiv 2501.17811) genişletildi:

- 7B paramları (1.3B karşılığı).
  Çin dilinde: 70 milyar参数 (13 milyar)
- Etap 1 (ağırış) için 90M görüntü-metin çiftleri 72M'den yukarı.
  Çinçe Çevirisi: 9000 milyonluk bir proje, 7.200 milyonluk bir proje.
- 72M'den 26M'ye kadar 2. aşama (birleştirilmiş) için.
  Çinli çeviriler: 72 milyonu ikinci aşamada kullanıldı
- 3. aşama için 200k görüntü-gen talimat örneği eklendi.
  Çin Çeviri: Üçüncü aşamada 200.000 resim oluşturma talimat örneği artırıldı.

Sonuç: Janus-Pro-7B MMMU'da LLaVA'ya (60.3 vs ~58) eşleşir ve GenEval'de DALL-E 3'yi (0.80 vs 0.67) yenir.

> 结果:Janus-Pro-7B MMMU 上匹配 LLaVA(60.3 vs ~58), GenEval 上 击败 DALL-E 3(0.80 vs 0.67);;

### JanusFlow  düzeltilmiş akış varianti

JanusFlow (arXiv 2411.07975) VQ üretim yolunu düzeltilmiş akış üretim yolu (daima) ile değiştirir. Bölüm anlama için SigLIP + düzeltilmiş akış için nesil olur. Kalite tavanları daha da yükselmektedir. Arsitekür kopyalanmış-kodlayıcı- paylaşılan vücut olarak kalır.

> JanusFlow(arXiv 2411.07975) VQ 生成路径を整流流生成路径に替える.

### Paylaşılan bir bedenin işi

Transformer vücudu, tek bir dizi işlemini yapar ancak iki giriş dağıtımıyla.

> Transformer 主体处理统一序列, fakat iki tür giriş dağılım vardır.

- Anlamak için: SigLIP özelliklerini tüket + metin işaretleri → metin autoregressively yayımlayın.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Üretim için: metin jetonlarını tüket + (ayrıca görüntü VQ jetonları) → otomatik olarak görüntü VQ jetonlarını yayın.
  中文翻译:生成:消费文本代币 +(可选图像 VQ代币)→ 自回归输出图像 VQ代币。

Blok başına belirli ağırlıklara sahip değil. Bu, Qwen veya Llama'nın içinde bulduğunuz metin tarzında bir transformatör ve iki giriş adaptörü.

> Önemli olan, Qwen veya Llama'da bulduğunuz bir metin biçimi transformörü ve iki giriş adaptörü vardır.

İlginçtir ki, bu Janus-Pro'nun vücudunun önceden eğitilmiş bir LLM'den initialize edilebileceği anlamına gelir. Janus-Pro DeepSeek-MoE-7B'den initialize eder. Bu seçim önemlidir: LLM, sıfırdan saf birleşik modellerin ulaşmak için mücadele ettiği mantık yeteneğine katkıda bulunur.

> İlginçtir ki, bu Janus-Pro  başlıca kişi ilk eğitimden başlayarak LLM başlangıcı yapabilir.

### InternVL-U ile karşılaştırıldığında

InternVL-U (Desin 12.10) 2026 takipidir.

> InternVL-U(第 12.10 课) 2026 yılının sonraki dönemidir.

- Doğal multimodal öncesi eğitim (InternVL3 omurgası).
  Çinçe Çevirimiçi:原生多模态预训练(InternVL3 主干)
- Çıkarılmış kodlayıcı yönlendirme (SigLIP içeri, VQ + yayılma çıkışları).
  ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇXM ÇX ÇXM ÇXM ÇXM ÇXM ÇX ÇXM ÇXM ÇX ÇXM ÇX ÇXM ÇXM ÇX ÇXM ÇX ÇXM ÇX ÇXM ÇX ÇXM ÇX ÇXM ÇX ÇX ÇXM ÇX ÇX ÇX ÇX ÇX ÇXM ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX ÇX Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Tek bir anlayış + jenerasyon + düzenleme.
  Çine çevirisi:统一理解 + 生成 + 编辑。

InternVL-U, Janus-Pro'nun mimari seçimini daha büyük bir çerçeveye dahil eder.

> InternVL-U, Janus-Pro'nun yapısal seçimlerini daha büyük çerçeveye dahil etti.

### Sınırlamalar

Çıkarılmış kodlayıcılar mimari karmaşıklığı artırır. Eğitmek için iki tokenizör, korumak için iki giriş yolu, iki set başarısızlık modu. Yürütme gerektirmeyen ürünler için Janus-Pro aşırı mühendislik yapılmıştır.

> Çözüm: Editör yapı karmaşıklığını arttırdı. İki sözcüğü eğitmek, iki giriş yolu sürdürmek, iki grup başarısızlık modeli.

Anlayış gerektirmeyen ürünler için Janus- Pro aşırı derecede nitelikli  Stable Diffusion 3 / Flux modeli seçin.

> 对于不需要理解的产品,Janus-Pro 大材小用选择 稳定扩散 3 /流动模型──

Her ikisine de ihtiyaç duyan ürünler için, Janus-Pro artık referans açık mimarlık.

> Her iki ürün için de Janus-Pro artık açık bir yapı olarak kullanılıyor.


> **【拓展：Janus-Pro 在基准上的表现】**Janus-Pro'nun çok modoldaki anlama tabanında, birleştirilmiş kodlayıcıların programının yaklaşık %3-5, görüntü üretimi tabanında yaklaşık %10-15'in üzerinde olması ortaya çıkıyor.


## Kullanın.
```figure
l5-janus-decouple
```

## Kullan

`code/main.py`Janus-Pro yönlendirmeyi simüle eder:

> `code/main.py`模拟 Janus-Pro 路由:

- İki sahte kodlayıcı: SigLIP benzeri (256-dimensiyonlu semantik vektörler üretir) ve VQ benzeri (tam sayı kodları üretir).
  Çinçe Çevirimi: iki模拟编码器:类 SigLIP (bkz: 256 维语义向量)
- Bir görev etiketine göre kodlayıcıyı seçen bir kılavuz.
  Çinçe Çevirimi: görev etiketlerine dayalı seçme kodlayıcıların ipucu yolcuları.
- Hangi kodlayıcı tarafından üretildiğine bakılmaksızın token dizilerini işleyen ortak bir vücut (stand-in).
  Çine dilinde:共享主体 (共享主体) 替代), hangi kodlayıcıya ait olursa olsun, 序列 işlemini yapar.
- 1. aşamalı (ağırlama) ve 3. aşamalı (özet sesi) ağırlıklı örnek programından geçiş.
  Çinçe Çevirim: Birinci aşamada, ikinci aşamada, ikinci aşamada, ikinci aşamada, ikinci aşamada, ikinci aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamada, üçüncü aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamalı aşamal

3 örneğe yönlendirilmiş yolları basın: görüntü QA, T2I, görüntü düzenleme.

> 印 3 図示の路由路径: 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図面 図

## Gönderin.

Bu ders bize çok yararlı .`outputs/skill-decoupled-encoder-picker.md`. Ürününün sınırlı kaliteye sahip bir jenerasyon + anlayış isteyen bir ürün olduğu için, Janus-Pro, JanusFlow veya InternVL-U'yu, belirli bir veri ölçeği önerisi ile seçer.

> 本课产 出 `outputs/skill-decoupled-encoder-picker.md`◊ Önemli bir yaşam boyu bir ürün olarak anlamalı, Janus Pro、JanusFlow veya InternVL-U  arasında seçilir, belirli veri boyut önerileri ile birlikte.

## Egzersizler.

1. Janus-Pro-7B, GenEval'de DALL-E 3'ü yener. 7B açık modelinin neden nesil açısından sınırlı özel modelle eşleşebileceğini, ancak anlayış açısından neden eşleşebileceğini açıkla.
   Çinçe çeviri:Janus-Pro-7B, GenEval'de DALL-E 3'yi yendi.

2. Bir yönlendirme işlevi uygulayın: verilen tescil metni,  olarak sınıflandırın`understand`veya `generate`"Böylece anlat ve sonra çiz" gibi belirsiz istekleri nasıl ele alırsın?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`understand`Ya da`generate` nasıl işleyeceksin?

3. JanusFlow, VQ yolunun yerini düzeltilmiş akışla değiştirir. Transformatör vücudu şimdi ne çıkarır ve kayıpta ne değişiklikler olur?
   Çinçe Çevirim:JanusFlow VQ 路径── Transformer 主体现在输出什么?损失有什么变化?

4. Janus-Pro mimarisi bir daha kopyalanmış kodlayıcı ile halledebilecek dördüncü bir görevi önerin. Örnekler: görüntü segmentasyonu (DINO tarzı), derinlik (MiDaS tarzı).
   Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Ç Ç Ç Ç Ç Ç

5. Janus-Pro Bölümü 4.2'yi okuyun. Verilerin ölçeklenmesi. T2I kalitesi kazanımına en çok hangi verilerin katkı sağladığı Janus ile karşılaştırıldığında?
   Çin dilinde: Janus-Pro bölümünün 4.2 bölümünde veri genişletilmesi hakkında hangi veri aşaması T2I kalitesi yükseltmesine en büyük katkıda bulunur?

## Anahtar Terimler

| Term | What people say | What it actually means | 中文含义 | 中文释义 |
|------|-----------------|------------------------|---------|
| Decoupled encoding | "Two visual encoders" | Separate tokenizer or encoder per direction: semantic for understanding, reconstruction for generation | 每个方向使用独立的分词器或编码器：理解用语义，生成用重建 |
| Shared body | "One transformer" | Single transformer processes either encoder's output; no modality-specific weights | 单一 Transformer 处理任一编码器的输出；无模态特定权重 |
| SigLIP for understanding | "Semantic features" | CLIP-family vision tower providing rich conceptual features but poor reconstruction | CLIP 家族视觉塔，提供丰富的概念特征但重建能力差 |
| VQ for generation | "Reconstruction codes" | Vector-quantized tokens that decode cleanly back to pixels | 可干净解码回像素的向量量化 token |
| JanusFlow | "Rectified-flow variant" | Janus-Pro with a continuous flow-matching generation head instead of VQ | 使用连续流匹配生成头替代 VQ 的 Janus-Pro |
| Routing tag | "Task tag" | Prompt marker (`<understand>` / `<generate>`) that picks the input encoder | 选择输入编码器的提示标记 |

## Daha fazla okumak

- [Wu et al. — Janus (arXiv:2410.13848)](https://arxiv.org/abs/2410.13848)
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Chen et al. — Janus-Pro (arXiv:2501.17811)](https://arxiv.org/abs/2501.17811)
  Çeviri: Janus-Pro
- [Ma et al. — JanusFlow (arXiv:2411.07975)](https://arxiv.org/abs/2411.07975)
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [InternVL-U (arXiv:2603.09877)](https://arxiv.org/abs/2603.09877)
  Çeviri: InternVL-U 论文。
- [Dong et al. — DreamLLM (arXiv:2309.11499)](https://arxiv.org/abs/2309.11499)
  Çeviri:DreamLLM
