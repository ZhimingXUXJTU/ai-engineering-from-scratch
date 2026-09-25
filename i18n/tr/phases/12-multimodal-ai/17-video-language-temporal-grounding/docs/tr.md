# Video-Language Models: Zamanlı Token ve Yerleşim.

> Video bir sürü fotoğraf değil. 5 saniyelik bir klip, bir görüntü modeli temsil edemeyeceği sebepçi sırayla, eylem fiillerine ve olay zamanlamasına sahiptir. Video-LLaMA (Zhang et al., Haziran 2023) ilk açık video-LLM'yi ses-görsel yerleştirme ile gönderdi. VideoChat ve Video-LLaVA bu örneği genişletti. 2025 yılına kadar Qwen2.5 VL'nin TMRoPE, sınır özel modelleri ile olan boşluğu kapattı. Her sistem zamanlı tokenleri farklı olarak çözdü. Klip başına Q-former, çerçeve başına concat-pool, token başına TMRoPE. Bu ders, kalıpları okuyor, bir benzerlik karşı dinamik çerçeve örneği oluşturur ve zamanlı yerleştirme görevlerini değerlendirir.

> **【中文解读】**Videolar bir sürü fotoğrafın bir yığın değil. 5 saniyelik kısa videolar, sonuç sırası, hareket, hareket ve olay zamanını içerir. Bu görüntü modelinin ifade edemeyeceği bir görüntüdir. Video-LLaMA'dan 2023 yılına kadar, video VLM'nin temel başarısı "4.2 saniye" yerine "15 saniye" olarak görülebilmesi için TM RoPE'nin yapıldığı bir video.

**Type:** Build
**Languages:** Python (stdlib, frame sampler + temporal-grounding evaluator)
**Prerequisites:** Phase 12 · 08 (LLaVA-OneVision)
**Time:** ~180 minutes

>  **【前置】**Özetle:LLaVA-OneVision 统一视觉代币 预算) Phase 7·04(RoPE 旋转位置编码,本节升级为TMRoPE 三轴) ⋅视频 VLM'in核心挑战:token 爆炸(1 分钟视频 = 35万代币) + 时间维度建模──
>  **【类比】**Video VLM 处理时间维度 = "看足球比赛回放"──均采样 = 每 10 秒截一(错过进球瞬间);事件驱动采样 = 进球时密集采样+其他时间稀疏(捕捉关键时刻);动态 FPS = 根据画面变化自动调度──TMRoPE 让模型能理解"4.2 秒发生进球"而不是"第15 ", bu ürün seviyesindeki video anlama anahtarıdır──

## Öğrenme Hedefleri

- Zamanlı konum kodlaması neden görüntü kodlayıcıdan bağımsız olarak video VLM performansını değiştirdiğini açıklayın.
  Çinçe Çevirimiçi: Çözüm neden zaman konum kodlaması bağımsızdır
- Sekundu başına tokenler vs yerleştirme doğruluğunda benzer, dinamik-FPS ve olay yönlendirilmiş çerçeve örneklemesini karşılaştırın.
  Çinçe Çevirimiçi:                                                                                                                                                                                                                                                           
- Q-former-per-clip (Video-LLaMA) vs pooled-per-frame (Video-LLaVA) vs M-RoPE-per-token (Qwen2.5-VL) tasarımlarını açıklayın.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Çeviri: Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- VideoMME, TempCompass, EgoSchema, Video-MMMU gibi dört video referans değerini söyleyin.
  Çeviri:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze:Müze

## Sorunlar. Sorunlar.

30 FPS'de 1 dakikalık bir video 1800 çerçeveye eşittir. Bir çerçeveye 196 görsel token (ViT-B 224) ile, bu, 2024 dönemindeki herhangi bir LLM bağlamından daha büyük 352k token.

> 1 dakika 30 FPS video  1800 ──  196 视觉 符号以每 视觉 符号(ViT-B  224 分辨率下) hesaplama, 共 352k 符号  2024 herhangi bir LLM                                                                                                                                                                                                                               

> **【中文解读】**1 dakika 30FPS video  1800 ,  196 视觉代币, toplam 352k 远超 2024 yıl LLM  上下文窗口──三种压缩策略各有取舍:采样损失时间细节,池化损失空间细节,Q-former 两者都损失一点但节省代币──

Üç azaltma stratejisi vardır:

> Üç çeşit basınç stratejisi:

1. Alt örnek çerçeveleri (1-8 FPS içeriğe bağlı olarak).
   中文翻译:子采样(根据内容 1-8 FPS)。
2. Her çerçevenin patch tokenlerini agresif bir şekilde (3x3 veya 4x4 binar havuz) birleştirin.
   Çinçe Çevirimi: için her   patch token                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
3. 16 kadro klipini alıp 64 token çıkaran bir Q-former ile sıkıştır.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç

Her bir değişim farklıdır. Alt örnekleme zamansal ayrıntıları kaybeder. Birleştirme uzaysal ayrıntıları kaybeder.

> Her türlü ağırlık farklıdır. Zaman ayrıntıları kaybolmuştur.

Zamanlı konum kodlaması diğer eksendir: model frame 5'in frame 6'dan önce geldiğini nasıl biliyor? Seçenekler arasında basit 1D temporal RoPE (Video-LLaMA), öğrenilmiş temporal embedments (Video-LLaVA) ve TMRoPE (Qwen2.5-VL, tam 3D) bulunur.

> 时间位置编码是另一个维度:模型怎么知道第5 在第6 之前?选项包括简单的 1D 时间 RoPE(Video-LLaMA)、可学习时间嵌入(Video-LLaVA) 和TMRoPE(Qwen2.5-VL,完整3D)。

## Konsepten bir şey.

> **【中文解读】**视频语言时序定位(Temporal Grounding) videoda doğru bulmak için doğal dil açıklaması ile karşı karşıya kalma zaman bölümü vardır. Örneğin, "O'nun teşekkür ettiği bir parça bulmak" için videoların zaman yapısını ve dilini anlama modeline ihtiyaç vardır.

> **【拓展：时序定位的应用场景】**时序定位在视频搜索、自动剪辑、体育分析、安防监控等场景s have wide application──技术上分为时刻检索(定位单个片段) 和亮点检测(定位高光时刻)──当前最佳模型在查拉德斯-STA数据集上达到约60%mIoU──


### Video-LLaMA: Klip başına Q-former + ses dalı

Video-LLaMA (2023) ilk açık video-LLM oldu.

> Video-LLaMA(2023) ilk açık video LLM:

- 16 kadro klipler 2 FPS'de (böylece 8 saniye).
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Ç Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Bir çerçeveye ViT özellikleri -> 16 çerçeveyi çapraz olarak takip eden Video Q-former -> 32 öğrenilmiş sorgu -> LLM.
  Çin dilinde: 每 ViT 特征 → Video Q-former对所有 16 做交叉注意力 → 32 个学习查询 → LLM。
- Paralel ses dalgası: dalga biçimi -> ImageBind ses kodlayıcı -> Audio Q-former -> 32 sorgu -> LLM.
  Çin dilinde:并行音频分支:波形 → ImageBind 音频编码器 → Audio Q-former → 32 个查询 → LLM。

Güç: sesli-görsel ortak düşünce. Zayıflık: sabit klip uzunluğu, keyfi zaman yerleştirme yok.

> 优势:音视频联合推理──劣势: sabit bir bölüm uzunluğu, herhangi bir zaman belirlenmesi mümkün değil──

### VideoChat ve Video-LLaVA

VideoChat, Video-LLaMA fikrini korudu ancak sesini düşürdü ve basitleştirdi. Video-LLaVA (Lin ve diğerleri, 2023) hem görüntüler hem de video çerçeveleri üzerinde tek bir görsel kodlayıcıyı ("projeksiyona kadar uyum") eğitmiştir.

> VideoChat, Video-LLaMA'nın düşüncelerini korudu ama ses sesini ortadan kaldırdı ve basitleştirdi.

İkisi de uzun videoları kullanmıyor.

> 两者都不能处理长视频──都是8-16 系统──

### Qwen2.5-VL ve TMRoPE

Qwen2.5-VL TMRoPE  Zamanlı-Modelli Rotary Position Embedding'i tanıttı. Her patch tokeninde t gerçek zaman damgası (cadra endeksi değil) olduğu (t, h, w) bir pozisyon vardır.

> Qwen2.5-VL  TMRoPE 时间-模态旋转位置编码──每个补丁代币 携带 (t, h, w) 位置,其中 t 是实际时间(非索引) ‖

Basit temporal yerleştirme ile ilgili temel farklar:

> Basit zamanlı yerleşimden önemli farklar:

- Model "4,2 saniye" olarak görüyor, "15 çerçeve" olarak görmüyor.
  Çine çevirisi:绝对时间而非索引.
- Her bir görüntü simgesi zaman damlasıyla bağımsız olarak döner.
  Çinçe Çevirim: her bir görüntü için zamanla bağımsız bir dönüm vardır.
- Eğer burada 2 FPS ve orada 4 FPS ile örnek alırsanız, TMRoPE eşitsiz mesafeyi doğal olarak ele alır.
  Çinçe Çevirimiçi:兼容动态 FPS──如果某处2 FPS采样、样另一处4 FPS采样,TMRoPE 原生处理不均间隔──

TMRoPE, "Kedi kaç saniye atlar?" sorularını etkinleştirir. Modelle "4,2 saniye" çıkarabilir. Video-LLaMA sadece "klipteki erken saatler" diyebilir.

> TMRoPE 支持"猫在几秒跳的?" bu tür soruları oluşturur.

> **【中文解读】**TMRoPE, Qwen2.5 - VL'nin anahtar yenilemidir: Her bir görsel token  taşı (t, h, w) konum bilgileri, t  real time  değil  indeksi                                                                                                                                                                                                                                        

> **【拓展：TMRoPE 在金融视频分析中的应用】**TMRoPE'nin kesin zaman konumlandırma yeteneği finansal sahneye çok önemlidir: analiz finansal haber yayınlama videolarında, "CEO ne zaman gelir artışını belirtir" belirlenebilir; analiz işlem izleme videolarında, sıra dışı olayların zaman noktasını belirleyebilir.

### Çerçeve örnekleme stratejileri

Bir yandan, N çerçeveleri eşdeğer olarak süresi boyunca.

> 均采样:在时长内均采样 N ──简单,但丢失运动峰值──

Dinamik FPS: Hareket yoğunluğuna göre örnekleme uyarlayıcı olarak. Optik akış veya çerçeve farklılığı yoğun örnekleme için yüksek hareketi segmentleri seçer. Qwen2.5-VL bu üzerinde trenler.

> 动态 FPS: Değişken güçlerine göre 采样自适应采样──光流或差分选择高运动段进行密集采样──Qwen2.5-VL 在此上训──

Olaylara dayalı: hafif bir detektör çalıştırın, eylemlerin olduğu yerlerde daha fazla örnek alın.

> 事件驱动:运行轻量级检测器,在动作发生处密集采样──VideoAgent 使用──

Anahtar çerçeve + bağlam: çekim sınırları + birkaç bitişik çerçeve örnek.

> 关键 + 上下文: 在镜头边界采样 + 少量相邻──用于电影内容──

> **【中文解读】**Çeviri  采样策略:均采样 (sadece kaybedilen hareket zirvesi) 动态 FPS (Hızlı ama kaybedilen hareket zirvesi) 事件驱动 (Hızlı fakat kaybedilen hareket yoğunluğu)  动作发生在密集采样)  关键+上下文 (Hızlı fakat kaybedilen hareket zirvesi)  2026 yılının en iyi uygulaması ise 动态 FPS + 3x3 双线性池化──

### Çerçeve başına birleştirme

1 FPS ve 576 token bir çerçeve, 5 dakikalık bir klip 172.800 token. Qwen2.5-VL-72B'nin 128k bağlamıyla yapılabilir ama pahalı.

> 1 FPS ∼ 576 token 下,5 分钟片段是172,800 个 token──Qwen2.5-VL-72B 的 128k 上下文可处理,但成本高──

3x3 binlineer havuzu, çerçeve başına 64 tokene kadar azalır -> 5 dakika boyunca 19.200 tokene.

> 3x3 双线性池化降至每 64 token → 5 分 19,200 token── çoğu görevin tatlısı──

Yerel ayrıntıların daha az önem verdiği ajan iş akışları için daha agresif bir şekilde (6x6 -> 16 token per frame) bir araya getirin.

> Daha fazla 激进地池化(6x6 → 每 16 token)

### Dört video referans göstergesi

- VideoMME: kapsamlı video anlayışı, kısa + orta + uzun.
  Çin dilinde:VideoMME:综合视频理解,短+中+长。
- TempCompass: ince tanelerli zamansal düşünce, "önce" / "sonra" sorular.
  Çine dilinde:TempCompass:细粒度时间推理, "之前" / "之后"问题──
- EgoSchema: Uzun boyutlu ilk kişilik video.
  Çin Çeviri:EgoSchema:长程第一人称视频──
- Video-MMMU: Multimodal multi-disiplin video soruları.
  Çinçe Çevirimi:Video-MMMU:多模态多学科视频问题──

Tam bir video-VLM değerlendirme dörtü de vurgulamaktadır. Farklı ekseller üzerinde vurgular  TempCompass sipariş etmekle ilgilidir, EgoSchema yaklaşık 3+ dakika akıl yürütme, VideoMME süreleri kapsamaktadır.

> 完整的视频 VLM 评估需要覆盖全部四基准──它们测试不同维度TempCompass 关注时序,EgoSchema 关注 3分以上的推理,VideoMME 跨越不同时长──

### Yerleştirme çıkış biçimleri

Zamanlı yerleştirme için çıkış biçimleri:

> 时序定位的输出格式:

- "Kedi 4 saniyelik çizginin etrafında atlar". Anlamak kolaydır ama net değil.
  Çeviri: "Kato 4 saniye sonra atlar.
- Yapılandırılmış JSON: `{"event": "jump", "start": 4.1, "end": 4.3}`- Qwen2.5 VL bu şekilde çalıştırıyor.
  Çeviri: JSON`{"event": "jump", "start": 4.1, "end": 4.3}`Qwen2.5VL                                                                                                                                                                                                                                                            
- Token tabanlı: özel `<time>4.1</time>`Bu, Qwen2.5VL'nin iç biçimi.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`<time>4.1</time>`Token ile cevap交错──Qwen2.5 VL'nin iç biçimi──

Token tabanlı, aşağı akıntılı kullanım için en doğru. Qwen2.5-VL'nin JSON çıkış biçimi doğrudan analiz edilir.

> 基于代币的格式在下游使用中最准确──Qwen2.5-VL 的 JSON 输出格式可直接解析──

### 2026 En iyi uygulamalar

2026'da video VLM'ler için:

> 2026 yıl video VLM'in en iyi uygulamaları:

- Kodlayıcı: SigLIP 2 M-RoPE veya TMRoPE (Qwen2.5-VL) ile.
  Çin Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Ç Ç Ç Ç Çeviri: Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Çerçeve örneği: dinamik FPS (1-4 hareketine bağlı olarak) maksimum çerçeve kapalı.
  Çeviri: 采样:动态 FPS (Hızım 1-4'e göre),
- Çerçeve başına birleştirme: 3x3 milyar.
  Çinçe Çevirim: 每池化:3x3 双线性──
- Çıktı: zaman + olay alanları ile yapılandırılmış JSON.
  Çinçe Çevirim:输出:带时间和事件字段的结构化 JSON。
- Benchmarks: VideoMME + TempCompass for general; EgoSchema for long horizon.
  Çin dilinde Türkçe:基准测试:通用用 VideoMME + TempCompass;长程用 EgoSchema。

## Çerçeveyi kullanın.
```figure
video-temporal-patches
```

## Kullan

`code/main.py`içerir:

> `code/main.py`包含:

- Teker teker ve dinamik FPS çerçeve örnekleri.
  Çinçe Çevirim:均和动态 FPS 采样器。
- Oyuncak zamansal yerleştirme değerlendiricisi: T zamanında "yerçek gerçek" olayı ve bir model çıkışı verildiğinde, doğruluğu tolerans ile puanlayın.
  Çinçe Çevirisi: bir oyun zamanı sıralama değerlendirici: given determination time T'in "real" events and model output, in capacity difference range评分。
- Video-LLaMA (16 çerçeve, eski Q), Video-LLaVA (8 çerçeve, MLP), Qwen2.5-VL (dinamik FPS + TMRoPE) arasındaki bir karşılaştırma.
  Çeviri: Video-LLaMA(16 ,Q-eski) 、Video-LLaVA(8 ,MLP) 、Qwen2.5-VL(动态 FPS + TMRoPE) 的对比──

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-video-vlm-frame-planner.md`. Bir video görevi (yakutma, eylem tanıma, zamanlı yerleştirme, özetleme) verildiğinde, çerçeve örneğini, birleştirme faktörünü, çıkış biçimini ve beklenen doğruluk seviyesini seçer.

> 本课产 出 `outputs/skill-video-vlm-frame-planner.md`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △                                                                            

## Egzersizler.

1. 3 dakikalık bir yemek demosu için, üniformal vs dinamik FPS seçin.

2. TMRoPE, basit bir zamanlı yerleştirme tablosunun yapamayacağı özel olarak neyi ekliyor? TMRoPE 具体添加了什么简单的时间嵌入表无法做到的功能?

3. VLM'nin yaymayı öğrenebileceği zamanlı yerleştirme için bir JSON şeması yazın. Hata durumları da dahil edin.

4. Video-LLaVA'nın "Projeksiyondan Önce Uyumlandırma" başlıklı 3. bölümünü okuyun. Bu neden ayrı görüntü ve video kodlayıcıları eğitmekten daha iyidir?

5. VideoMME liderlik çizelgesine göre, 2026 yılına kadar en üst açık model ve en üst özelliği model arasındaki fark nedir? Bu farkın ne kadarı zaman kodlama ile temel LLM ölçeğine bağlıdır? VideoMME 排行榜'a göre, 2026 yılındaki en üst düzey açık kaynak modeli ve en üst düzey kapalı kaynak modeli arasındaki fark ne kadar büyük?

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Temporal grounding | "Time-localized answers" 时序定位 | VLM outputs a specific timestamp range for when an event happens VLM 输出事件发生的具体时间戳范围 | |
| TMRoPE | "Time-Multimodal RoPE" 时间-多模态旋转位置编码 | 3D rotary position with absolute timestamps, used by Qwen2.5-VL 带绝对时间戳的 3D 旋转位置编码 | |
| Dynamic FPS | "Motion-aware sampling" 运动感知采样 | Sample more frames in high-motion segments, fewer in static ones 高运动段密集采样，静态段稀疏采样 | |
| Frame pooling | "Spatial compress per frame" 逐帧空间压缩 | Reduce patches per frame with bilinear interpolation before the LLM LLM 前用双线性插值减少每帧 patch 数 | |
| Video Q-former | "Clip compressor" 片段压缩器 | Cross-attention bottleneck mapping N frames to K learned queries 将 N 帧映射为 K 个学习查询的交叉注意力瓶颈 | |
| VideoMME | "Video bench" 视频基准 | Comprehensive short/medium/long video benchmark, 2500+ samples 覆盖短/中/长视频的综合基准测试 | |

## Daha fazla okumak

- [Zhang et al. — Video-LLaMA (arXiv:2306.02858)](https://arxiv.org/abs/2306.02858)
- [Li et al. — VideoChat (arXiv:2305.06355)](https://arxiv.org/abs/2305.06355)
- [Lin et al. — Video-LLaVA (arXiv:2311.10122)](https://arxiv.org/abs/2311.10122)
- [Qwen Team — Qwen2.5-VL (arXiv:2502.13923)](https://arxiv.org/abs/2502.13923)
- [Lin et al. — VILA-1.5 (arXiv:2312.07533)](https://arxiv.org/abs/2312.07533)
