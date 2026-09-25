# Uzun Video Anlayışları Milyon Token Kontextda

> 24 FPS'de 1 saatlik 4K video, çişilmiş ve gömülü 60 milyon token üretir. 2 saatlik podcast bölümünün transkripsi 30.000 token. Blu-ray'de tam bir film, agresif bir gruplama ile sıkıştırılmış bile olsa, yüz binlerce token. Google'ın Gemini 1.5 (Mart 2024) bu çağı 10 milyon token bağlamıyla açtı. Bir saatlik videolar boyunca güvenilir bir iğne-haystack hatırlatması yaptı. LWM (Liu et al., Şubat 2024) halka dikkatinin ölçeklenme yolunu gösterdi. LongVILA ve Video- XL alımını daha da arttırdı. VideoAgent, çürük bağlamı ajantik çekim için değiştirdi. Her yaklaşım, hesaplama, hatırlama ve mühendislik karmaşıklığı konusunda farklı bir ödeme. Bu ders onları yan yana okuyor.

> **【中文解读】**1 小时 4K 视频可产生约6000.000 代币,远超任何模型的上下文窗口──处理长视频有三条路径:(1) 暴力上下文(Gemini 1.5'in千万 代币 上下文);(2) Ring Attention 跨设备分布式注意力;(3) Token 压缩(Video-XL'in özetleri);(4) 代币 检索(VideoAgent 检索将视频当数据库查询)  Her 条路径在计算量,召回率和工程复杂度上有不同取取.

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, needle-in-haystack simulator + agentic-retrieval router) | **语言:** Python（标准库，大海捞针模拟器 + Agent 检索路由器）
**Prerequisites:** Phase 12 · 17 (video temporal tokens) | **前置知识:** Phase 12 · 17（视频时间 token）
**Time:** ~180 minutes | **时间:** ~180 分钟

>  **【前置】**Öğrenci bölümün önüne geçerek:Fase 12·17(video saat simgesi ile alıştırma);Fase 10·34(Anamak dikkat dağıtımlı dikkat);Fase 14(Agent 检索,VideoAgent 思路)。本节是长视频理解的极限挑战:百万代币上下文。
>  **【类比】**长视频理解 = "看完整部电影后能回答细节"──三种策略:(1) Gemini 1.5 路线 = Bütün filmi beynine sertleştirmek(10M token 上下文,硬件怪兽);(2) Video-XL 路线 = 看完写摘要+检索原始片段(token 压缩);(3) VideoAgent 路线 = 当数据库查,问题导向地拉取相关段段(Agent 检索) ~~

## Öğrenme Hedefleri

- Uzun format videoları için toplam görsel işaret sayısını değişen FPS ve birleştirme ile hesaplayın.
  Çinçe Çevirimiçi:计算不同 FPS 和池化配置 下长视频的视觉代币 总数──
- Ölçekleme yollarını açıklayın: kaba bağlam (Gemini 1.5), yüzük dikkat (LWM), simge sıkıştırma (LongVILA / Video-XL).
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Doğruluk ve gecikme konusunda çiğ bağlam video VLM'leri vs. ajantik-içtikleme video VLM'leri (VideoAgent) karşılaştırın.
  Çinçe Çevirimiçi:Comparison original sur le casse de VLM 和 Agent 检索视频 VLM(VideoAgent) on准确率和延迟的表现──
- 30 dakikalık bir video için bir iğne-hay asmak testi tasarlayın ve belirli bir dakikada hatırlama ölçün.
  Çin Çeviri: 30 dakika video tasarım büyük denizde bir ip test ve belirli bir dakika için çağrı oranını ölçmek

## Sorunlar. Sorunlar.

Qwen2.5 VL boyutlu bir çubuk, 384 yerel çözünürlükte ~729 token. 3x3 birleştirme ile bu, çerçeve başına 81 token. 1 FPS = 1800 çerçeve = 145.800 token. 2025 yılına kadar yapılabilir açık VLM'ler, sıkı. 2 FPS'de 291.600 token  sadece en büyük bağlamlar uygundur.

> Qwen2.5-VL Büyük boyutlu patch içinde 384 orijinal yaşam çözünürlüğü altında her 729 token──3x3 池化后每 81 token──30 分钟片段 1 FPS = 1800  = 145,800 token,2025 yıl açık VLM işleme edilebilir ama紧张──2 FPS 下 291,600 token只有最大上文下文才能容纳──

1 FPS'de 2 saatlik bir film 583k jeton tutar. 2026 açık modellerinin çoğundan öte; Gemini 2.5 Pro veya daha agresif birleştirme gerektirir.

> 2 小时电影 1 FPS 583k tokenı ise, 2026 yılındaki çoğu açık model kapasitesini aşar.

Üç merdiven yolu ortaya çıktı.

> Çıkışlar:

## Konsepten bir şey.

> **【中文解读】**长视频理解(百万代币 级别) çok modoldaki AI'nin ön kenarında bir meydan okuma.

> **【拓展：Gemini 1.5 Pro 的百万 token 上下文**Gemini 1.5 Pro  destek 1M token  giriş, yaklaşık 1 saatlik video veya 1000+ sayfa dosyası ile işlenebilir.


### Yolu 1: Kırmızı bağlam (Gemini 1.5, Claude Opus)

Soruna donanım atın, bağlamı milyonlarca tokene kadar ölçeyin, her şeyi bir ileri geçişle işleyin.

> Bir kez daha tüm içeriği ele almak için, bir kez daha şiddetle mücadele etmek için bir kez daha daha daha daha daha fazla bilgi almak için bir kez daha daha kullanın.

Gemini 1.5 Pro 1M token ile piyasaya sürüldü; Gemini 1.5 Ultra 10M; Gemini 2.5 Pro 2026'da saatlerce video güvenilir bir şekilde yapar.

> Gemini 1.5 Pro, 1M token ile yayınlandı; Gemini 1.5 Ultra 10M'ye kadar genişledi; Gemini 2.5 Pro, 2026 yılında 9.5M token aralığında %99.7'lik büyük deniz çekimleri çekim oranını kaydetti.

Mühendislik: hafıza hiyerarşisi (yerel + küresel + nadir) ve uzun bağlamlı verimlilik için MoE uzman yönlendirme ile özel bir dikkat uygulaması. Tam ayrıntılı olarak yayınlanmamış. Açık kaynaklı değil.

> 工程实现:自定义注意力机制,带有内存层次(局部+全局+稀疏),加上 MoE 专家路由提升长上下文效率──未完整公开──非开源──

### Yolu 2: Yüzük dikkat (LWM, LongVILA)

Yüzük dikkat, her bir cihazın bir parça tutduğu bir "zeng"deki cihazlar arasında uzun diziler dağıtır.

> **【中文解读】**Ring Attention uzun dizilerinin bir çok cihazeye dağıtıldığını, her cihazeyi bir bloklu bir dizide bulduğunu, çapraz iletişim ile tüm dünyayı hesaplayan dikkatini, hesaplama miktarını, ikinci değil, aşağıdaki uzunluklılık ile birlikte büyütüyor.

LWM (Liu et al., 2024) 1M-token bağlam modeli bu şekilde eğitildi. Eğitim hesaplama ölçekleri bağlam ile doğrusal olarak, karadesel olarak değil  dikkat üzerinde karadesel vurma halka cihazları boyunca amortize edilir.

> LWM ((Liu 等人,2024) bu şekilde 1M token üzerinde aşağıdaki model üzerinde eğitim yaptı.

LongVILA (arXiv:2408.10188) örneği VLM'lere uyarladı. 1400-frame videoları çerçeve başına 192 token = 268k bağlamda, 8 yön paralellik boyunca halka dikkatle eğitilmiştir.

> LongVILA bu modayı VLM¬1400  video, her  192 token = 268k 上下文, geçiyor 8 路并行环形注意力训练──

### Yolu 3: Token sıkıştırma (Video-XL, LongVA)

Kötü bağlamdan daha ucuz: LLM'nin sırayı görmeden önce agresif bir şekilde sıkıştır.

> Bı şiddet üzerine aşağıdaki daha uygun: LLM                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

Video-XL (arXiv:2409.14485) görsel bir özetleme simgesi kullanır: N çerçevelerinin her bir klipi, N üzerinde bulunan tek bir "özetleme" simgesi üretir. Sonuç olarak, LLM, her bir klibe bir özetleme simgesi görür ve bağlamı önemli ölçüde küçültür.

> Video-XL Visual Extract Token: Her N 片段 generate a" abstract " token, on the N  make attention;;

LongVA, "uzun bağlam transfer" tekniği ile LLM bağlamını 200k'ten 2M'ye uzattı.

> LongVA "长上下文迁移" tekniğini kullanarak LLM 上下文 200k 扩展到2M──

Token sıkıştırması, ölçeklendirme için belirli zaman damlalarında hatırlama işlemlerini değiştirir.

> Token sırtılması belirli zaman sırtının geri dönüş oranı değişkenlik sırtıncılık sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sırtıncı sısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısısı

### Yolu 4: Ajantik geri alım (VideoAgent)

LLM'ye tam videoyu eklemeyin. Bunun yerine, videoyu bir veritabanı olarak ele alın ve sorgulamak için LLM kullanın.

> Tüm videoyu LLM'ye vermeyin.

VideoAgent (arXiv:2403.10517):

> VideoAgent ((arXiv:2403.10517):

1. LLM soruyu okuyor.
   > LLM 读取问题──
2. LLM ilgili klipler için bir geri alma aracı istiyor ("meşhengle segmentleri gösterin").
   > LLM 调用检索工具获取相关片段("给我看有猫的片段")
3. Araç, klip zaman damgalarına eşleşen bir görüntü verir.
   > 工具返回匹配的片段时间──
4. LLM, bu klipleri VLM üzerinden okuyor.
   > LLM 通過VLM 读取这些片段──
5. LLM cevapları oluşturur veya takip sorular sorar.
   > LLM Üretim Cevapları veya İlerleme Aramaları

Bu, uzun videolara uygulanan LLM-as-agent örneğidir. Daha ucuz sonuç (sadece ilgili klipler kodlanmış), daha zor mühendislik (içindeki kalitesini geri almak boğaz haline gelir).

> Bu, LLM-as-agent 模式应用到长视频──推理更便宜──工程更难──检索质量成为瓶──

### İğne-hay döşek referans değerleri

Standart uzun bağlam testi: Video'daki rastgele bir noktada benzersiz bir görsel veya metin işaretçisi ekle, sonra onu hatırlamanızı gerektiren bir soru sor.

> 标准长上下文测试: videoda her zamanki konumunda tek bir görüntü veya metin işaretini yerleştirin ve sonra bu işaretin hatırlanması gereken sorguları sorun.

Metrik: Video uzunluğu ve işaretçi pozisyonu boyunca Recall@k.

> 標籤:跨视频长度和标记位置的 Recall@k。

Gemini 2.5 Pro, 90 dakikalık videolarda %99'luk hatırlama puanı elde eder. Açık 72B modelleri (Qwen2.5-VL-72B, InternVL3-78B) 30 dakikada ~85-90% puan alır ve 60'dan aşağı düşürülür.

> Gemini 2.5 Pro 90 dakika videoya çekilme oranı %99'dur.

VideoAgent 2+ saatte çiğ bağlamlı modellerle eşleşebilir veya yenemez çünkü araç iyiyse geri alım iğneye çarpar.

> VideoAgent 2 saatten fazla videolarda orijinalde aşağıdaki modelle uyumlu veya üstesinden gelebilir, çünkü araç iyiyse, arama hedefleri elde edebilmektedir.

### Hangi yolu seçmeliyiz?

Sınır doğruluğunda 15 dakikalık bir klip için: açık 72B + yerel bağlam genellikle çalışır.

> 15 分片段追求前沿准确率:开放 72B + 原生上下文通常可行──选 Qwen2.5-VL-72B──

30 dakikalık 1 saatlik içerik için: LongVILA veya Video-XL açıktır; Gemini 2.5 Pro kapalıdır.

> 30 dakika 1 saat içerik: LongVILA veya Video-XL ile açık kaynak; Gemini 2.5 Pro ile kapalı kaynak.

2+ saatlik içerik için: VideoAgent veya benzer arama kalıpları. Alternatif olarak, daha küçük parçalara özetle ve hiyerarşik özetleri besleyin.

> 2 小时以上内容:VideoAgent veya benzer arama modeli.

### 2026 üretim modeli

Pratik olarak, üretim uzun video boru hattları hibriddir:

> 實踐中,生产级长视频管道是混合方案:

1. Tüm videoda dinamik FPS örnekleme + agresif birleştirme çalıştırın (100k token küresel bir temsil elde edin).
   Çinçe Çevirisi: tüm videoların tümü için FPS 采样 + 激进池化 (FPS)
2. Küresel bir özet için 72B VLM'ye geçin.
   Çeviri: 72B VLM 生成全局摘要.
3. Kullanıcı ayrıntılı sorular sorarsa, bir indeks olarak özet kullanarak ajantik geri alımı çalıştırın.
   Çinçe Çevirimi: Eğer kullanıcı detaylı sorular sorarsa, bir referans olarak bir özet kullanın.

Bu, küresel anlayış için kaba bağlamı ve yerel ayrıntıları bulmak için birleştirir.

> Bu, şiddet üzerine aşağıdaki genel anlayış ve araştırmanın yerel ayrıntıları yeteneğini birleştirir.

## Çerçeveyi kullanın.
```figure
mm-video-token-budget
```

## Kullan

`code/main.py`- ...

- Videolar için 1 dakikadan 3 saate kadar değişen FPS + birleştirme ile token bütçelerini hesaplar.
  Çin Çeviri:计算 1 分钟到 3 小时视频在不同 FPS + 池化下的代币 预算。
- İğneyi bir çiy yığını içinde çalıştırmayı simüle eder: rastgele bir zaman damgasına bir işaretçi enjekte eder, bir soru sorar, puan geri alır.
  Çinçe Çevirimiçi:模拟大海捞针测试:在随机时间注入标记,提问,评分召回率──
- Aşağı akıntılı bir VLM'ye beslemek için belirli klipleri seçen bir ajantik-içimi yönlendirme simülatörü içerir.
  Çeviri: İçeriyor bir Ajan 检索路由模拟器,选择特定片段给下游 VLM──

Bütçe masasını çalıştır ve ölçek boşluğunu hissedin.

> 运行预算表,感受规模差距──

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-long-video-strategy-planner.md`. Video süresi ve sorgu karmaşıklığı göz önüne alındığında, kaba bağlam, sıkıştırma ve ajantik geri alım arasında seçim yapar ve gecikme + kalite beklentilerini hesaplar.

> 本课产 出 `outputs/skill-long-video-strategy-planner.md`◊ video süresi ve sorgu karmaşıklığı, şiddet üzerindeki aşağıya ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞

## Egzersizler.

1. 45 dakikalık bir ders 1 FPS, çerçeve başına 81 token. Toplam token? Hangi model bağlamlarına uygun? 45 分钟讲座,1 FPS,每 81 token──总 token 数?能放入哪些模型的上下文?

2. İğne-hay-stack testi tasarlayın: Hangi dakikada işaretçiyi enjekte edersiniz ve tam sorgu biçimi nedir?

3. 1 saatlik bir videoda Kwen2.5-VL-72B (80k bağlam) ile VideoAgent (Claude 3.5 + kurtarma) arasında kaba bağlam karşılaştırın. Hangi çağrıda kazanır? Hangi gecikme üzerinde kazanır?

4. Ring dikkatinin hafıza maliyetleri, sırada uzunluk ve cihaz sayısında lineer olarak ölçeyor. Yüzük dönüşüm aşamasını düşürürseniz neden ve neyin başarısız olduğunu açıklayın. Ring dikkatinin内存开销随序列长度和设备数线性增长──解释原因,以及去掉环形轮转阶段会出什么问题──

5. Gemini 1.5 Bölüm 5'i okuyun Haystack'ta İğne. 1M vs 10M token sınırında hatırlama hakkında kağıt ne buldu?

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Brute context | "Just more tokens" 暴力上下文 | Scale LLM context to millions of tokens; process everything in one pass 将 LLM 上下文扩展到百万 token，一次前向传播处理全部内容 | |
| Ring attention | "LWM-style parallel" 环形注意力 | Distributed attention pattern where each device holds a chunk and rotates 分布式注意力模式，每个设备持有一块并在环中轮转 | |
| Token compression | "Summary tokens" 摘要 token | Reduce per-clip tokens via a learned compressor before the LLM LLM 前通过学习型压缩器减少每片段 token 数 | |
| Needle-in-haystack | "NIH test" 大海捞针测试 | Insert a unique marker at a random point, ask model to recall it at test time 在随机位置插入唯一标记，测试时要求模型回忆 | |
| Agentic retrieval | "LLM as query planner" Agent 检索 | LLM asks a retrieval tool for relevant clips, reads them via a VLM, composes answer LLM 调用检索工具获取相关片段，通过 VLM 阅读并生成回答 | |
| VideoAgent | "Retrieval pattern for video" 视频检索模式 | Canonical agentic-retrieval design: question -> tool -> clip -> answer 经典 Agent 检索设计：问题→工具→片段→回答 | |

## Daha fazla okumak

- [Gemini Team — Gemini 1.5 (arXiv:2403.05530)](https://arxiv.org/abs/2403.05530)
- [Liu et al. — LWM / RingAttention (arXiv:2402.08268)](https://arxiv.org/abs/2402.08268)
- [Xue et al. — LongVILA (arXiv:2408.10188)](https://arxiv.org/abs/2408.10188)
- [Shu et al. — Video-XL (arXiv:2409.14485)](https://arxiv.org/abs/2409.14485)
- [Wang et al. — VideoAgent (arXiv:2403.10517)](https://arxiv.org/abs/2403.10517)
