# Omni Modeller: Qwen2.5 Omni ve Düşünce Konuşması Bölünmüştür

> GPT-4o'nun Mayıs 2024'te yapılan ürün gösterisi altta yatan modelden dolayı değil, ürün şekli nedeniyle  konuştuklarınızda sesli bir arayüzün olması, modelin kamerada gördüğünü gördüğü ve 250 ms'den kısa bir süre içinde tekrar konuşması nedeniyle bozulmuştu. Açık ekosistem, 2024 ve 2025 yıllarının geri kalanını bu ürün yüzeyine ulaşmak için yarışarak geçirdi. Qwen2.5-Omni (Mart 2025) referans açık tasarımdır: bir Thinker (büyük metin üreten transformatör) ek olarak bir Talker (paralel konuşma üreten transformatör), akış konuşma jetonları ile bağlantılıdır. Mini-Omni basitleştirdi, Moshi gecikme süresine eşleşti, GLM-4-Voice Çin'e uzattı. Bu ders, akılcı-sözcü mimarisini ve akış gerçek zamanlı diyalogunu çalıştırmak için gecikme bütçesini okuyor.

> **【中文解读】**GPT-4o'nun aşamasında aşama model değil, ürün biçiminde 250ms'de sesli iletişim deneyimi vardır.

**Type:** Build
**Languages:** Python (stdlib, streaming pipeline latency simulator + VAD loop)
**Prerequisites:** Phase 12 · 19 (audio-LLMs), Phase 12 · 16 (any-to-any)
**Time:** ~180 minutes

>  **【前置】**学本节前 Lütfen önce bil:Fase 12·16(MIO 任意到任意流式)、Fase 12·19(音频 LLM)、Fase 6·04(VAD 语音活动检测)。Qwen2.5-Omni = "开源版 GPT-4o",核心是Thinker-Talker 双流架构,并行化降低延迟至250ms内。
>  **【类比】**Düşünceci-Söycü 架构 = "翻译员 + 同传播音员"。其他 omni 模型 = 一个人又要思考又要说话(串行,慢);Qwen2.5-Omni = Düşünceci(大脑,想"说什么")+ Konuşmacı(嘴巴,把文字变语音)并行工作。Thinker 流式吐出文本代币,Talker 一边接收一边合成语音,用户听到的是流水线输出,总延迟大幅降低。

## Öğrenme Hedefleri

- İfade borusunu düşünce (metin mantığı) ve konuşma (söz sentezi) olarak bölün ve paralel akış neden çalışır açıklayın.
  Çine dilinde:将推理管道分为 Thinker (Hinker) 文本推理) 和 Talker (语音合成),解释为什么并行流式可行──
- Bir konuşma etkileşimi için, bileşenler arasındaki Time-to-First-Audio-Byte (TTFAB) bütçesini hesaplayın.
  Çinçe Çevirimiçi:逐组件计算对话交互的首音频字节时间(TTFAB) bütçe。
- TMRoPE'nin düşünceci içinde görme, ses ve metin üzerinde zaman doğrultusunda konum kodlamasını açıklayın.
  Çinçe Çevirimiçi: Description Thinker 内 TMRoPE 跨视觉、音频和文本的时间对齐位置编码──
- Gerçek zamanlı üç konuşma örneğini isimlendirin: yarı duplex, dönüş, tam duplex.
  Çinçe Çevirimiçi:列举三种实时对话模式:半双工、轮流、全双工。

## Sorunlar. Sorunlar.

Gerçek zamanlı ses asistanı çok şey yapmalı, hızlı:

> Gerçek zamanlı bir ses asistanı çok şey hızlı bir şekilde halletmelidir.

1. Kullanıcıyı dinleyin. Gerçek zamanlı konuşma simgesi, ses etkinliği algılama (VAD) konuşma bittiklerini bilmek için.
   Çinçe Çevirimi: Слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать пользователям речи, слушать, слушать, слушать, слушать, слушать, слушать, слушать, слушать, слушать, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, речь, ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре ре
2. Kamera girişleri 2 ila 4 FPS'de, sesle birlikte düşünceciye akıştı.
   Çinçe Çevirimiçi:可选地看──摄像头输入 2-4 FPS,与音频一起流式传入 Thinker──
3. Düşün, konuşma geçmişine göre bir cevap yaz.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
4. Ses simgelerini sentezle, dalga şekline dekode et, kullanıcıların hoparlörlerine akışla.
   Çinçe Çevirimiçi: 话语, sintet音频 token,解码为波形,流式传输到用户扬声器,

Her adım gecikme ekler. Konuşma-hissesi toplam geri dönüş < 500ms  gerektirir, kullanıcı gecikmeyi fark etmeyi bırakır. GPT-4o ~250ms iddiasını ifade eder. Moshi ~160ms. Qwen2.5-Omni ~350-500ms.

> Her adım da gecikme artıyor. Sohbet gereksinimleri %s geri dönüşü < 500 ms 低于此,用户就不太注意延迟.

Her bileşen akışmalı. Hiçbir şey "her şeyi toplayıp sonra kodlamayı" olamaz.

> Her bileşen akışlı işleme gerektirir.

## Konsepten bir şey.

> **【中文解读】**Tüm Enerji Modelleri (Omni Models) aynı zamanda metin, ses, resim, video ve diğer tüm modellerle işlenir. Düşünceci-Sözcü yapı "düşünür" (düşünür) ve "sözcü" (düşünür) Çözüm: Düşünceci büyük dil modeli, konuşmacı da doğal dil çıkışı (düşünür) için sorumlu bir dil yapısı modülüdür.

> **【拓展：实时多模态交互**GPT-4o, gerçek zamanlı çoklu iletişim modelinin gerçekleştiği ilk modeldir: kullanıcılar sesli soruları sorabilir, model aynı zamanda fotoğraf resimlerini görebilir, doğal sesli gerçek zamanlı cevaplar verir.


### Düşünen ve Konuşan

Qwen2.5 Omni'nin parçalanması:

> Qwen2.5-Omni'nin ayrımı:

- Düşünceci: 7B-80B metin üreten bir transformatör. Çelişkili metin + görüntü + ses jetonlarını tüketir. Neyi söylemek istediğini temsil eden metin jetonlarını çıkarır.
  Çine çevirisi:Thinker:7B-80B 文本生成 Transformer。消费交错的文本+图像+音频符号。输出代表"说什么"的文本符号。
- Konuşmacı: daha küçük bir konuşma üreten transformatör (200M-1B). Düşüncenin metin çıkış işaretlerini ve son konuşma bağlamı işaretlerini tüketir. Diskret konuşma işaretlerini (kayıp-VQ indeksleri) çıkarır.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Konuşma dekodörü: Ses simgelerini gerçek zamanlı olarak ses örneklerine götüren akış dalga biçimleri dekodörü (SNAC, MoVQGAN ailesi).
  Çine dilinin anlamı: 流式波形解码器 (SNAC、MoVQGAN 系列),实时将语音代币 转为音频样本。

Ayrılma önemlidir. İyi bir mantık yürütmek için düşünen büyük olmalıdır. Konuşmacı küçük olabilir çünkü işinin yerel olması  metni konuşma işaretlerine dönüştürmek. Büyük Konuşmacı daha ifade edici değildir; daha yavaş.

> Bölünmek çok önemlidir. Düşünen  büyük yetenekle iyi düşünmelidir. Konuşmacı küçük olabilir çünkü onun görevi yerel  metin dönüşüm noktasıdır.

İkisini de paralel olarak çalıştırmak:

> Ve iki iş:

1. Düşünceci, metin simgesi t_i gönderir.
   Çeviri:Türkçe
2. Konuşmacı t_i (streaming yoluyla) tüketir ve konuşma işaretlerini s_i, s_{i+1}, ..., s_{i+k} gönderir.
   Çeviri:Sözcü 消费 t_i(通過流式)并输出语音符号 s_i, s_{i+1}, ..., s_{i+k}。
3. Konuşma dekodörü, konuşma işaretlerini geldiğinde tüketir ve ses örneklerini yayar.
   Çinçe Çevirimi:语音解码器在语音代码到达时消费并输出音频样本──
4. Düşünceci'nin metin simgesinde olduğu zaman, Konuşmacı t_0..t_{i+2} için ses akışı yapmış.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Çeviri: Ç Ç Ç Ç Ç Ç Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç

> **【中文解读】**Düşünceci  büyük olmalı  7B-80B) iyi düşünce yapabilmek için, Konuşmacı  küçük olabilir  200M-1B) çünkü onun görevi yerel 文本转语音符号── daha büyük Konuşmacı  没有更有表现力,只会更慢──并行运行时,当思想家在生成第一个+3 文本符号时, 讲者 已经播放第一个到第一个+2 文本对应的音频──

> **【拓展：Token 速率数学】**16kHz 语音 50Hz 基础语音符号, her saniye 50 语音符号 gerektiriyor demektir. Konuşmacı her saniye >= 50 语音符号 才能跟上── H100 上,200-300M'deki Konuşmacı her saniye yüz tane token çıkarabilir, ihtiyaç çok fazla; ama 7B Konuşmacı 会跟不上── işte bu yüzden özel küçük konuşmacı modeline ihtiyaç vardır, doğrudan kullanıcı model değil──

### TMRoPE  Zaman doğrultusunda çok modal pozisyonlar

Düşünceci, görüntü çerçevelerini (örneğin 4 FPS'ye ulaşmak), ses çerçevelerini (sekunde 50 çerçeveye ulaşmak) ve konuşma geçmişinden metinleri entegre etmelidir.

> Düşünceci  needs to integrate images((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((

TMRoPE, her token'e mutlak zaman damgaları verir. Görüş damgası t=2.3 saniye. Ses damgası t=2.32 saniye. Kullanıcıdan gelen metin damgası t=2.35 saniye. RoPE dikkatini zaman damgası ile döndürür; model onları geçici olarak eşzamanlı olarak görür.

> TMRoPE için her bir token ayrıştırılmaktadır ──视觉 token 在 t=2.3s──音频 token 在 t=2.32s── kullanıcıların "stop"文本 token 在 t=2.35s── RoPE 时间 旋转注意力;模型将它们视为时间同时发生──

Bu, "selamlarken el salladı" için altyapı çalışması için  model aynı kavramsal anlarda video çerçevesini ve sesini görür.

> Bu "O'nun elleri" diyor ki, "İyi" normal bir şekilde çalışabilecek altyapı.

### Akış konuşma sentezi

Konuşma jetonları akışmalı. Mini-Omni (Xie & Wu, 2024) "dilli modeller akışta düşünerek işitebilir, konuşabilir" tanıttı: Düşünceci çıkış jetonları ve Konuşmacı çıkış jetonları aynı sırada birbirine karışır. Konuşmacı bir sonraki metin jetonu yapıldığında ateş eder.

> 语音代币 必须流式传输──Mini-Omni 引入了"语言模型可以在流式思考的同时听和说":Thinker 输出代币 和 Talker 输出代币 在同一序列中交错──Thinker 一旦提交下一个文本代币,Talker 立即触发──没有批量边界──

Moshi (Défossez et al., Ekim 2024) en hızlı açık uygulamadır. 160 ms TTFAB tek bir A100'de. Mimarlık: Tek bir 7B transformatörü, değişen pozisyonlarda metin ve konuşma belirtilerini yayar, düşünce akışını konuşma akışından ayıran bir "içindeki monolog" ile. Bu etkili bir şekilde Düşünce + Konuşmacı'dır. Dikkatli eğitimle tek bir modelde birleştirildi.

> Moshi en hızlı açık kaynak gerçekleştirilmesidir. Tek A100'e 160 ms TTFAB'e yükseltilmiştir. Yapı: Tek 7B Transformer, metin ve ses jetonlarını çıkartarak, "内心独白" ile düşünce akışı ve konuşma akışını ayırarak bir model olarak birleşir.

### VAD ve dönüş

Ses etkinliği algılama giriş tarafında çalışır.

> 语音活动检测在输入端运行──两种模式:

- Yarım duplex: kullanıcı konuşur, model dinler. Model konuşur, kullanıcı dinler. VAD sessizlik algılama yoluyla açık el uzatma (~ 200 ms).
  Çinçe Çevirimi Çevirisi: yarım iş: kullanıcı konuşuyor, modelleri dinliyor, modelleri konuşuyor, kullanıcı dinliyor, VAD 静音检测 (Yüzdeyişle)
- Tam duplex: her ikisi de aynı anda konuşabilir. Model arka kanal ("uh-huh") veya kesilebilir.
  Çin dilinde tüm iki iş: her iki taraf da aynı anda konuşuyor olabilir.

Qwen2.5 Omni, sessizlik eşiği üzerinden dönüş yaparak varsayılan olarak yarım duplex destekler.

> Qwen2.5 Omni 默认支持半双工,通过静音值实现轮流──全双工需要应用层处理──

### Qwen3-Omni (Kasım 2025)

GPT-4o'nun 250 ms'ine yakın gecikme. Açık ağırlıklar. OmniBench'de Benchmarks.

> 继任者──Qwen3-80B Düşünücüsü, Daha Büyük Konuşucusu,改进的TMRoPE-v2──延迟接近 GPT-4o'nun 250ms──开放权重──OmniBench 基准与 Gemini 2.0 Live 竞争──

### Üretim gecikmesi bütçesi

Tipik bir akış etkileşimi için:

> Tipik bir iletişim:

- Mikrofon -> ses simgeler: 40-80 ms.
  Çeviri: 音频 token: 40-80ms
- Ön doldurma (sürekli + tarih): 7B'de 100-200 ms, 70B'de çok daha fazla.
  Çeviri:                                                                                                                                                                                                                                                             
- İlk düşünceci metin simgesi: 40 ms.
  Çönkemci: 文本代號:40ms。
- Konuşmacı ilk metin işlemi yapar: 20 ms.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- İlk konuşma simgesi: 40 ms.
  Çıktı. Çıktı.
- Geri kalan-VQ çözümü: 30 ms.
  Çıktı.
- Konuşma dalga şekli çözümü: 50-80 ms.
  Çeviri: 50-80ms

Toplam TTFAB: 7B'de 320-510 ms, 70B'de 600-900 ms. Sınır kalitesi genellikle 70B+ anlamına gelir; bu nedenle sınır gecikme boşluğu.

> 总 TTFAB:7B 约 320-510ms,70B 约 600-900ms──前沿质量通常意味着70B+; bu nedenle ön沿延迟差──

### Token oranı matematiği

16kHz konuşma ile 50 Hz temel konuşma işaretleri, çıkış saniyesinde 50 konuşma işaretine ihtiyacınız var. Konuşmacı takip etmek için ≥50 tok/s yaymalıdır. H100'de tipik bir LLM geçiş süresi 30-80 tok/s'de, küçük bir (200-300M) Konuşmacı yeterince hızlıdır; bir 7B Konuşmacı geride kalır.

> 16kHz 语音以 50 Hz 基础语音符号 计算,每秒输出需要50语音符号──讲者 必须以 ≥50 tok/s 的速度输出──H100 上典型 LLM 吞吐量为 30-80 tok/s,小型(200-300M) Konuşmacı 足够快;7B Konuşmacı 会跟不上──

Bu nedenle, "sadece ana modeli kullanmak" yerine küçük özel Talker modelleri var.

> Bu yüzden özel küçük konuşmacı modelleri ve "birbirle ilgili başlıklı modeller" değil.

## Çerçeveyi kullanın.
```figure
l5-thinker-talker
```

## Kullan

`code/main.py`- ...

- Sahte token emisyon oranları ile düşünce-sözcü boru hattını simüle eder.
  Çinçe Çevirim: Using模拟的代號 输出速率模拟 Düşünceci-Söyleyicisi 管道。
- Yapılandırılabilir model boyutları ve mikrofon örnek oranları için TTFAB hesaplar.
  Çinçe çevirisi:                                                                                                                                                                                                                                                            
- VAD sessizlik eşiği ile yarı duplex dönüş gösterir.
  Çinçe Çevirim: VAD 静音值演示半双工轮流。

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-omni-streaming-budget.md`. Gerçek zamanlı ses ürününün hedefi TTFAB ve özellik setini (görüş, iki dil, tam çift) göz önüne alarak, Qwen2.5-Omni, Qwen3-Omni, Moshi veya Mini-Omni'yi seçer ve Thinker/Talker'i boyutlandırır.

> 本课产 出 `outputs/skill-omni-streaming-budget.md`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △

## Egzersizler.

1. Hedefiniz TTFAB 300 ms. 7B Thinker ve 300M Talker'de, her bileşenin gecikmesini yazın.

2. Qwen2.5-Omni TMRoPE kullanır. Kullanıcı t=1s'de konuşmaya başladığı ve kamera t=1.2s'de bir hareket yakaladığı bir istek için modelin ne gördüğünü açıklayın. Qwen2.5-Omni TMRoPE kullanıyor.

3. Tam dubleks desteği, modelin dinlerken ses yaymasını gerektirir. Bunu öğreten bir eğitim veri biçimi önerin.

4. Moshi'nin makalesini okuyun Bölüm 4. "İçer monolog" ayrılığını ve neden Düşünce-Söycünün bölünmesini engellediğini açıklayın.

5. Geçim bütçesini hesaplayın: Konuşmacı 16kHz konuşmasını 50 temel katman tokeni/sekonda takip etmek için ne kadar hızlı token göndermelidir?

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Thinker | "Reasoning brain" 思考者 | Large text-generating transformer producing what to say 生成"说什么"的大型文本生成 Transformer | |
| Talker | "Speech-generating mouth" 说话者 | Small transformer producing discrete speech tokens from Thinker's text 将 Thinker 文本转为语音 token 的小型 Transformer | |
| TTFAB | "Latency budget" 首音频字节延迟 | Time-to-first-audio-byte: from user speech end to first audio sample out 从用户说话结束到首个音频样本输出的延迟 | |
| TMRoPE | "Time-aligned RoPE" 时间对齐旋转位置编码 | Position encoding using absolute timestamps across vision, audio, text 跨视觉、音频、文本使用绝对时间戳的位置编码 | |
| Half-duplex | "Turn-taking" 半双工 | User and model alternate; VAD silence detects user-done 用户和模型交替说话；VAD 静音检测用户说完 | |
| Full-duplex | "Simultaneous" 全双工 | Model can speak and listen at the same time; backchannel capable 模型可同时说话和监听；支持回话 | |
| Inner monologue | "Moshi separation" 内心独白 | Single-model design where thinking-stream and speaking-stream interleave 单模型设计，思考流和说话流交替出现 | |

## Daha fazla okumak

- [Xu et al. — Qwen2.5-Omni (arXiv:2503.20215)](https://arxiv.org/abs/2503.20215)
- [Qwen Team — Qwen3-Omni (arXiv:2509.17765)](https://arxiv.org/html/2509.17765v1)
- [Xie & Wu — Mini-Omni (arXiv:2408.16725)](https://arxiv.org/abs/2408.16725)
- [Défossez et al. — Moshi (arXiv:2410.00037)](https://arxiv.org/abs/2410.00037)
- [Zeng et al. — GLM-4-Voice (arXiv:2412.02612)](https://arxiv.org/abs/2412.02612)
