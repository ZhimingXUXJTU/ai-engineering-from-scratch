# Su işaretleme  SynthID, Stabil İmza, C2PA 稳定签名 水印 SynthID C2PA

> Üç teknoloji 2026 Yapay zeka tarafından üretilen içeriğin kaynağı olarak yapılandırılmıştır. SynthID (Google DeepMind)  görüntü su işaretleme Ağustos 2023'te başlatıldı, metin + video Mayıs 2024 (Gemini + Veo), metin açık kaynaklı Ekim 2024'te Responsible GenAI Toolkit aracılığıyla, Gemini 3 Pro ile birlikte Kasım 2025'te birleşik çok medya dedektörü. Metin su işaretleme, sonraki belirti örneği seçme olasılığını fark edilemez şekilde ayarlar; görüntü/video su işaretleri sıkıştırma, kesim, filtre, çerçeve hızında değişiklikler hayatta kalır. Stable Signature (Fernandez et al., ICCV 2023, arXiv:2303.15435)  gizli difüzyon dekodörünü ince ayarlar, böylece her çıkış sabit bir mesaj içerir; kesilmiş (içindeki %10) oluşturulan görüntülerin %90'ı FPR<1e-6'da tespit edilmiştir. Ardından "Stabil İmza Durgun" (arXiv:2405.07145, Mayıs 2024)  ince ayarlama, kaliteyi korurken su işaretini çıkarır. C2PA  Kriptografik olarak imzalanan, bozukluktan açık metadata standardı (C2PA 2.2 Açıklama 2025). Su işaretleri ve C2PA tamamlayıcıdır: metadatalar silinebilir ancak daha zengin bir kaynak taşır; su işaretleri transkodlama yoluyla kalır ancak daha az bilgi taşır.

> **【中文解读】**Bu bölümde AI su baskı teknolojisi SynthID、C2PA等 tanımlama AI oluşturma içeriği yöntemleri SynthID(Google DeepMind) düzenleme sonraki belirti 采样概率使生成包含更多"绿色"令牌不可知但可检测──Stable Signature 微调潜在扩散解码器使每个输出包含固定二进制消息──C2PA加密签名、防改的元数据标准──

> **【拓展：水印 → Deepfake 检测】**水印はDeepfake 检测的核心技术路径──SynthID'in跨模态检测器(2025 yıl 11 月) metin, resim, ses ve video içinden sinyal okuyabilir── ancak sınırlılık belirgin: modelleri belirtilmiştir.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, token-watermark embed + detect) | **语言:** Python（标准库，token 水印嵌入 + 检测）
**Prerequisites:** Phase 10 · 04 (sampling), Phase 01 · 09 (information theory) | **前置知识:** Phase 10 · 04 (采样), Phase 01 · 09 (信息论)
**Time:** ~75 minutes | **时间:** ~75 分钟

>  **【前置】**学本节前 Lütfen önce öğrenin:Dava 10·04(采样)、Dava 01·09(信息论)。三大水印技术 + 内容追溯标准。
>  **【类比】**水印 = "AI 内容の隐形身份证"。SynthID(Google) = 调整次要代码采样偏好"绿色"代码,不可知知可检测;Stable Signature = 微调解码器让每张图都含固定二进制消息(裁剪 10% 仍 >90% 检出);C2PA = 加密签名元数据──互补:元数据可剥取但信息丰富;水抗印转码但信息少──
> ️ "Stabil Signature 不稳定"2024.5:微调即可移除水印保质量──水印不是银弹──

## Öğrenme hedefleri

- Token seviyesindeki su işaretleme (SynthID-text tarzı) ve tespit edilebilme mekanizmasını açıklayın.
- Stable Signature'i ve 2024'te onu kıran kaldırma saldırısını açıkla.
- Devlet C2PA'nın rolü ve neden su işaretlemesine tamamlayıcıdır.
- Ana sınırlamaları açıklayın: model-sözlü sinyal, parafrase altında sağlamlık ve anlam koruyan saldırılar (arXiv:2508.20228).

> 描述令牌级水印(SynthID-text 风格) ve onun kontrol edilebilir mekanizması──描述 Stable Signature 和 2024 yılını bozarak onun kaldırma saldırısı──说明 C2PA'nın rolü ve neden su ile birleştirilmesi──描述关键局限性:模型特定信号、释义下鲁棒性和意保持攻击──

## Sorun . Sorun .

2023-2024 yılları arasında derin sahtelik ve AI tarafından üretilen içerik politik ve tüketici bağlamlarına büyük ölçüde girmiştir. Su işaretleme önerilen teknik kaynak sinyalidır: yaratma sırasında nesilleri işaretleyin, onları daha sonra tespit edin. 2025 kanıtı: hiçbir su işaretinin koşulsuz sağlam olmadığı, ancak C2PA metadataları ile katlanmış olan kombinasyon kullanılabilir bir kaynak hikayesi sağlar.

> 2023-2024 yılları derin sahtelik ve AI üretimi içeriği büyük çapta siyasal ve tüketim sahnelerine girdi. Su baskıları önerilen teknik kaynak sinyalleri: yaratılışta işaret üretimi, sonra inceleme.

## Konsep kavramı.

> **【中文解读】**文本水印机(Kirchenbauer 等人 2023, by Google 产品化): her çözümü aşaması olacak Önceki K 个令牌哈希产生词汇表的伪随机"绿色"和"红色"分区,向绿色logits 添加 delta 偏置采样――生成包含比随机更多的绿色令牌――检测:重新哈希每个前,计数生成中的绿色令牌,计算 z 分数――水印文本 z > 0,人类文本 z ~ 0。

### Metin su işaretleme (SynthID-metin tarzı)

Google tarafından üretilen Kirchenbauer et al. 2023 mekanizması:

1. Her dekodlama aşamasında, sözcük kaynağının "yeşil" ve "kırmızı" setlerine pseudorandom bir bölünmesi oluşturmak için önceki K jetonlarını hash edin.
2. Yeşil logitlere δ ekleyerek yeşil kümelere doğru tarafsız örnekleme.
3. Neslin içi, rastlantının ürettiğinden daha fazla yeşil token içerir.

Deteksiyon: her önbellek yeniden yazılsın, nesillerdeki yeşil işaretleri sayılsın, bir z puanı hesaplansın.

Özellikleri:
- Okuyucular için fark edilemez (δ kalitesi kaybı hafif olması için yeterince küçüktür).
- Sözcük bölme fonksiyonuna erişilebilir.
- Parrafraze etmek için sağlam değil  metni yeniden yazmak sinyali yok eder.

SynthID-text, Google'ın Responsible GenAI Araç Kütüfi aracılığıyla Ekim 2024'te açık kaynaklı.

> **【中文解读】**Stable Signature(Fernandez 等人, ICCV 2023) mikro mod potansiyel yayılma çözücü her üretilen görüntüyi sabit bir ikili sistem içermektedir.

### Kalıcı İmza (resim)

Fernandez et al. ICCV 2023. Latent difüzyon dekodörünü ince ayarlayın, böylece üretilen her görüntü, latent temsiline gömülü sabit ikili bir mesaj içerir. Deteksiyon, nöral dekodörle latentten dekod edilir.

> Stable Signature 微调潜在扩散解码器 her üretilen görüntü sabit ikinci yapı mesajı içerir.

Mayıs 2024 "Stable Signature is Unstable" (arXiv:2405.07145): decoder'in ince ayarlaması, görüntü kalitesini korurken su işaretini çıkarır.

> 2024 yıl 5 月 "Stabil İmza Durgun" kanıtı, küçük bir modelleme kodlayıcıyı görüntü kalitesini aynı zamanda taşıyabilir.

### SynthID teker teker detektörü (Kasım 2025)

Gemini 3 Pro ile birlikte: Tek bir API'de metin, görüntü, ses ve videolardan SynthID sinyallerini okuyabilen bir multimedya dedektörü. Google'ın kaynak yığınını birleştirir.

> Gemini 3 Pro ile birlikte: Bir çapraz modem denetleyicisi, metin, resim, ses ve videolardan SynthID  sinyallerini okuyabilir.

> **【拓展：C2PA + 水印互补 → EU AI Act Article 50】**C2PA 和水印互补:元数据可剥离但携带丰富来源链;水印通过转码持久但只携带少量比特──Google 在搜索、广告和"关于此图片"中集成两者──EU AI Act'ın 50. maddesinin şeffaflık kodları, AI'nin içeriği üretimi etiketiyi oluşturmasını gerektirir.

### C2PA

İçerik Kaynak ve Doğruluk Koalisyonu. Kriptografik olarak imzalanan sahtekarlık kanıtlı metadata standardı. C2PA 2.2 Açıklayıcı (2025). C2PA manifestı, kaynak iddialarını kaydeder (kimler, ne zaman, hangi dönüşümler) yaratıcının anahtarı tarafından imzalanmıştır.

> C2PA, bir anahtar imzalamacı tarafından yapılan bir imzalama.

Su işaretlemesine ek olarak:
- Metadatalar silinebilir; su işaretleri (sadece) silinebilir.
- Metadata zengin (tam kaynak zinciri); su işaretleri bit taşıyor.
- C2PA platformun kabul edilmesine bağlıdır; su işaretleri otomatik olarak yerleştirilmiştir.

> Su baskıları: Bilgi koparılabilir ama bilgi boldur; su baskıları geçici olarak kullanılır ama sadece küçük miktarda bit taşıyor.

Google hem Arama, Reklamlar hem de "Bu görüntü hakkında" ile birlikte.

> Google, arama, reklam ve "Bu resim hakkında" iki şeyi birleştirdi.

> **【拓展：水印局限性 → 模型特定信号问题】**关键局限性:SynthID 水印仅来自启用SynthID的模型──"无SynthID 信号"不等于真实性证明未启用SynthID的模型生成的任何内容都不会有水印──此外,arXiv:2508.20228(2025) saldırıyı sürdürmenin amacını gösterdi.

### Sınırlamalar

- **Model-specific.**SynthID'den kaynaklanan bir neslin nesiller. SynthID'den kaynaklanan bir neslin nesiller, SynthID'den kaynaklanan bir neslin nesilleridir.
- **Paraphrase.**Metin su işaretleri anlamı koruyan bir parafrasiyi sağlayamaz.
- **Transformation attacks.**arXiv:2508.20228 (2025) hem metin su işaretlerini hem de birçok görüntü su işaretlerini yok eden anlam koruma saldırıları gösterir.
- **Fine-tune removal.**"Stabil İmza Dursunmaz" için, nesneden sonraki ince ayarlama yerleştirilmiş su işaretlerini kaldırır.

### AB AI Yasası 50 Maddesi

Yapay zeka ile üretilen içerik etiketlemesi için şeffaflık kodu (birinci taslak Aralık 2025, ikinci taslak Mart 2026, beklenen son Haziran 2026'da[European Commission status page](https://digital-strategy.ec.europa.eu/en/policies/code-practice-ai-generated-content)Kode Nisan 2026'dan itibaren taslakta kalır ve zaman çizelgesi değişebilir. Teknik katmanı gerektiren düzenleyici katman. Deepfakes etiketlenmelidir.

### Bu 18 fazaya uygun.

Dersler 22-23 modelin yaydığı (özel veriler, kaynak sinyali) hakkında. Ders 27 eğitim- veri yönetimi kapsamaktadır. Ders 24 bu teknik önlemleri gerektiren düzenleyici çerçeve.

> Ders 22-23  Model Ekiption  Private Data  Source Signal  Ders 27 DATA GERENMENT  Ders 24 bu teknik önlemlerin denetim çerçevesini gerektirir

## Kullanın Kullanın
```figure
an-watermark-greenlist
```

## Kullan

`code/main.py`Oyuncak metni bir su işaretini oluşturur. Tokenler tam sayı 0..N-1; su işaretli örnekleme taraftarları, hash tanımlı yeşil kümelere doğru. Bir detektör yeşil token z puanını hesaplar. 1000 token nesillerinde tespit gözlemleyebilir, sinyali yok etmeyi izleyebilir ve insan metni üzerinde yanlış pozitif oranı ölçebilirsiniz.

> `code/main.py`构建玩具文本水印──令牌是整数 0.N-1;水印采样偏向哈希定义的绿色集──检测器计算绿色令牌 z 分数── 1000 令牌生成的检测、释义破坏信号以及人类文本上的误报率──

## Gönderin.

Bu ders bize çok yararlı .`outputs/skill-provenance-audit.md`. Kaynak iddiası ile içerik dağıtımını göz önünde bulundurarak, su işaretleri mekanizmasını (varsa), C2PA imzalı zincirini (varsa), her birinin karşı karşılıksızlığını ve modalite kapsamını denetlemektedir.

> 本课产 出 `outputs/skill-provenance-audit.md` Sınırlama ve kontrol: Su İmza Mekanizması, C2PA imza zinciri, kendi içerikli kaynaklı açıklamalar ve her türlü kapsamlılık.

## Egzersizler.

1. Çık .`code/main.py`. Su işareti 1000 token üretimi karşılığı insan yazılı metin için z puanları bildirin. 95% güven eşiğinde yanlış pozitif oranı belirleyin.

2. Paraphrase saldırısını uygulayın ve 30%'i eşanımlarla değiştirin.

3. Kirchenbauer et al. 2023 Bölüm 6'da dayanıklılık hakkında okuyun.

4. SynthID-text + C2PA metadatalarını kullanan bir dağıtım tasarlayın. Bir tüketicinin gördüğü kaynak zincirini açıklayın. Her bileşenin bir başarısızlık modunu tanımlayın.

5. 2024 "Stabil İmza Durgun" sonucu, ince ayarlama görüntü su işaretini kaldırır. Bu saldırıyı sınırlayan bir dağıtım kontrolü tasarlayın.

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|-----------------|------------------------|
| SynthID | "Google's watermark" | Cross-modal provenance signal; text, image, audio, video |
| Token watermark | "Kirchenbauer-style" | Biased-sampling text watermark detectable via green-token z-score |
| Stable Signature | "image watermark" | Fine-tuned-decoder watermark; ICCV 2023 |
| C2PA | "the metadata standard" | Cryptographically signed tamper-evident provenance metadata |
| Paraphrase robustness | "does rewording break it" | Text watermark property; currently limited |
| Fine-tune removal | "adversarial unwatermark" | Attack that removes image watermark via decoder fine-tuning |
| Cross-modal detector | "unified SynthID" | November 2025 unified API across modalities |

## Daha fazla okumak

- [Kirchenbauer et al. — A Watermark for Large Language Models (ICML 2023, arXiv:2301.10226)](https://arxiv.org/abs/2301.10226) simge-su işaretleri mekanizması
- [Fernandez et al. — Stable Signature (ICCV 2023, arXiv:2303.15435)](https://arxiv.org/abs/2303.15435) resim su işaretleri kağıdı
- ["Stable Signature is Unstable" (arXiv:2405.07145)](https://arxiv.org/abs/2405.07145) Kaldırma saldırısı
- [Google DeepMind — SynthID](https://deepmind.google/models/synthid/) çapraz modal su işaretleri
- [C2PA 2.2 Explainer (2025)](https://c2pa.org/specifications/specifications/2.2/explainer/Explainer.html) Metadata Standartı
