# Ses-Dil Modelleri: Sesli Flamingo 3 Arc 音频语言模型: Sesli Flamingo 3

> Whisper (Radford et al., Aralık 2022) konuşma tanıma  680k saat zayıf denetimli çok dilli konuşma, basit bir kodlayıcı-dekoder dönüştürücü, sonraki her ASR yayınını alıntı yapan bir referans değerini ayarladı. Ama tanınmak mantık değildir. "Bu kayıtta hangi aletler var?" ya da "sonucu ne duygu ifade ediyor?" ya da "üçüncü dakikada ne oldu?" sormak, ses anlayışını gerektirir, metinleri değil. Qwen-Audio, SALMONN, LTU ve NVIDIA'nın Audio Flamingo 3 (AF3, Temmuz 2025) bu yığınını aşamalı bir şekilde inşa etti: Whisper sınıfı kodlayıcıları tutun, Q-formörleri üzerine kurşun, ses metni talimat verileri üzerinde eğitim verin, düşünce zinciri mantıklılığı ekleyin. Bu ders, bir süreliğine ilerliyor.

> **【中文解读】**Sıfırlama 语音识别解决了,但识别不是推理──"Bu bölüm ses kayıtları ne alet kullanıyor"、" Konuşmacı ne duygu ifade ediyor"等 sorunlar, ses anlayışını gerektirir, basit bir dönüştürme değil. SALMONN'den Audio Flamingo 3(AF3), Audio LLM'nin gelişme yolu: Sıfırlama 级编码器 + 加 Q-Former 桥接 + 用音频-文本指令数据训练 + 加链式思考推理──

**Type:** Build
**Languages:** Python (stdlib, log-Mel spectrogram + audio Q-former skeleton)
**Prerequisites:** Phase 6 (Speech and Audio), Phase 12 · 03 (Q-Former)
**Time:** ~180 minutes

>  **【前置】**学本节前 Lütfen önce bil:Base 6·01-02(语音信号处理:FFT/Mel 频谱图/Whisper);Base 12·03(Q-Former 桥接,本节复用为音频 Q-Former);Base 7(Transformer 编码器-解码器)。音频 LLM = 视觉 LLM'nin "听觉版", sadece输入图像补丁 变成 Mel 频谱图补丁──
>  **【类比】**音频 LLM = "为 LLM 装耳朵"──Whisper = 助听器(只能转录不能思考);SALMONN = 聋学校的翻译员(Whisper 转录→LLM 思考);AF3 = 直接给 LLM 装耳(端到端听+想+答)──端到端的好处:能捕捉转录丢失的信息(语调、情绪、停顿), bunlar düşünce için önemlilerdir──

## Öğrenme Hedefleri

- Bir dalga şekli ile bir log-Mel spektrogramı hesaplayın: pencereler, FFT, filtre bankaları, log dönüşümü.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Şapışkan şapışkan, BEAT, AF-Şapışkın hibrid seçeneklerini karşılaştır.
  Çinçe Çevirim:Biraz 编码器选项:Hısır 编码器、BEATs、AF-Hısır 混合──各自何时胜出──
- Spektrogram yamalarına karşı çalışarak bir ses Q-former oluşturun: N öğrenilebilir sorular.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Kaskadel (Shisper-then-LLM) vs. sonundan sonuna kadar ses-LLM eğitimini açıklayın: neden sonundan sonuna kadar düzeyleri akıl yürütmek için daha iyi.
  Çinçe Çevirimi Çevirisi: açıklama seviyesinde

## Sorunlar. Sorunlar.

Konuşma tanıma, Whisper tarafından çözüldü. Ses OCR bir maldır. Ancak "mal" transkripsiyonda durur. Eğer model duyduğu şeyi akıl yürütemiyorsa  zamanlama, hoparlörler, duygu, müzik yapısı, çevresel sesler  tek başına transkripsiyon ürün özelliklerini yönlendirebilir.

> 语音识别已被语音识别已被语音识别已被语音识别已成为基础能力──但"基础能力"转录步骤止步──如果模型无法推理所听的内容时"",讲话人"",情绪"",音乐结构"",环境声仅靠转录无法驱动产品功能──

Üç açık yol:

> Üç条 Açık yolu:

1. Cascade: Whisper transkripte, LLM transkripte nedenler. saf konuşma senaryoları için çalışır. Müzik için başarısız, çevresel ses, çoklu hoparlör üst üstelik, duygu.
   Çinçe Çevirim: Sınıf: Sıfır 转录,LLM için 转录文本推理──适用纯语音场景──对音乐、环境音频、多人重叠、情绪不适用──

2. Sonundan sonuna kadar ses-LLM: bir ses kodlayıcı ses jetonlarını doğrudan bir LLM'ye ekler, transkripsiyonu atlar. Akustik bilgileri (duygu, hoparlör, ortam) korur. Yeni eğitim verilerine ihtiyaç duyar.
   Çinçe Çevirimi:端到端音频 LLM:音频编码器将音频代码器 直接输入 LLM,跳过转录──保留声学信息(情绪、说话人、环境) ・・・ yeni eğitim verisi gerekir。

3. Hibrit: ses kodlayıcı + hem yazıp hem de mantık edebilen metin dekodörü. Qwen-Audio ve Audio Flamingo bu yolu seçer.
   Çinçe Çevirimiçi:混合:音频编码器 + 文本解码器,既能转录又能推理──Qwen-Audio 和 Audio Flamingo 选择此路径──

## Konsepten bir şey.

> **【中文解读】**语音语言模型 Whisper (OpenAI'nin ses tanımlama modeli) ile AudioFlamingo'nun gelişimine kadar. Whisper 680.000 saatlik bir dil sesli yayın eğitimi sırasında ses tanımlama temel modelidir.

> **【拓展：语音 AI 的前沿**Whisper-large-v3  destek yaklaşık 100 种语言的语音识别──2024-2025 yıllarındaki eğilimler 语音大模型:GPT-4o 原生语音输入输出(延迟约 320ms),Gemini'in gerçek zamanlı语音对话,ElevenLabs'in语音克隆──AudioFlamingo, SOTA'ya ulaşmak için ses sıklığı anlama görevinde, müzik ve ses hakkında karmaşık soruları cevaplayabilir──


### Log-Mel spektrogramı: Giriş özelliği

Her ses kodlayıcı aynı özellikle başlar: bir log-Mel spektrogramı.

> Her ses sesleme kodlayıcı aynı özellikten başlıyor: log-Mel 频谱图──

1. 16 kHz'e yeniden örnekleme.
   Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre: Çevre Çevre: Çevre Çevre Çevre Çevre Çevre: Çevre Çevre Çevre Çevre Çevre
2. Kısa süreli Fourier dönüşümü 25 ms pencereleri ile, 10 ms atlama.
   Çinçe Çevirimi:短时里叶变换,25ms 窗口,10ms 步长。
3. FFT sonucu büyüklüğünü alın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç
4. Merak frekansına warp için Mel filtre bankalarını (genellikle 0-8000 Hz log-spaced 80 filtre) uygulayın.
   Çinçe Çevirimiçi: uygulama Mel 波器组 (normalde 80 个波器, 0-8000 Hz) 间隔对数映射到感知频率──
5. Dinamik aralığı için log kompres (log(1 + x))
   Çine dilinde:                                                                                                                                                                                                                                                             

Sonuç: T'nin zaman çerçeveleri sayısının olduğu şekil 2 boyutlu bir dizi (T, 80) .

> 结果:形状为 (T, 80) nın 2D 数组, T ∈ Time 数──30 秒片段在 100 Hz 率下:(3000, 80)。

### Şapışkan'ın kodlayıcı

Whisper'in kodlayıcı, 12 katlı ViT tarzı transformatördür ve log-Mel spektrogramını zaman çerçeveleri olarak işlemektedir.

> Whisper'in kodlayıcıları, 12 katlı bir ViT 风格的变压器, olarak zaman 序列处理――输出:每个时间一个隐藏状态向量――

ASR için, Whisper'in dekodörü, kodlayıcı çıkışına bağlı metin işaretlerini oluşturan çapraz bir dikkat transformörüdür.

> 对于 ASR,Whisper 的解码器是一个交叉注意力变压器,根据编码器输出生成文本代币──标准编码器-解码器──

ALM (audio-LLM) için, kodlayıcı çıkışını farklı bir LLM'ye giriş olarak istiyorsunuz. Şablon: Sisper kodlayıcı dondurulmuş, Q-eski eğitimli, LLM dondurulmuş veya ayarlanmış.

> 对于ALM(音频 LLM),需要将编码器输出作为另一个LLM的输入──模式:Whisper 编码器结,Q-former 可训练,LLM 结或微调──

### BEAT ve ses özel kodlayıcılar

Whisper konuşma baskın verileri üzerinde eğitilmiştir.

> Sessizlikle konuşma ve çevre sesleri üzerinde daha zayıflık gösterir.

BEATs (Chen et al., 2022) AudioSet üzerinde eğitilmiş bir kendiliğinden denetimli bir dönüştürücüdür.

> BEATs(Chen 等人,2022) AudioSet 上訓練的自监督 Transformer──在相同参数下比 Whisper 更好地捕捉音乐和环境声──

AF-Whisper (Audio Flamingo 3'ün hibrid): Whisper + BEAT'lar ses giriş olarak özellikler içerir. Whisper dil sinyali taşır, BEAT'ler akustik sinyali taşır.

> AF-Whisper(Audio Flamingo 3 的混合方案):拼音 Whisper + BEATs 特征作为音频输入──Whisper 携带语言信号,BEATs 携带声学信号──

### Sesli Q-former

BLIP-2'nin görsel Q-former ile aynı kalıp. Bir dizi öğrenilebilir sorgu (sık sık 32 veya 64) ses kodleyicisinin çıkış çerçeveleri üzerinde çapraz olarak katılır. Sorgular LLM tarafından tüketilen ses jetonları haline gelir.

> BLIP-2'nin görsel Q-eski benzer bir model── sabit sayıda öğrenilme sorusu(genellikle 32 veya 64 个) ses kodlayıcılarının çıkışına karşı karşılaştırmalı dikkat── sorular LLM 消费的音频代币──

Eğitim ayarlama aşaması: tek başına Q-former, audio-metin çiftlerinde kontrastlı + başlık kaybı (AudioCaps, Clotho).

> 訓練對齐阶段:仅 Q-former,音频-文本对上对比+描述损失(AudioCaps、Clotho) 』 指示阶段:端到端,解 LLM,在指示数据上训练──

### Ark  SALMONN, Qwen-Audio, AF3

SALMONN (Tang et al., 2023): Whisper + BEATs + Q-former + LLaMA. Ciddi bir akıl yürütme yeteneği olan ilk açık ses-LLM. MMAU'daki değerler ~0.55 bileşik gösterir.

> SALMONN(Tang 等人,2023):Susper + BEATs + Q-former + LLaMA。第一个具有严推理能力的开放音频 LLM。MMAU 基准综合约 0.55。

Qwen-Audio (Chu et al., 2023): benzer mimarlık, daha zengin bir veri kümesi üzerinde eğitilmiş, çok dönüşlü diyalog için ayarlanmıştır. MMAU ~ 0.60.

> Qwen-Audio(Chu 等人,2023): benzer yapı, daha zengin bir veri kitlesinde eğitim, çoklu sohbet optimize edilmesi için.

LTU  Dinle, Düşün, Anla (Gong et al., 2023): açık mantık verileri, ses klipleri üzerinde düşünce zinciri odaklan. Daha küçük ama daha odaklı.

> LTU听、想、理解(Gong 等人,2023):显式推理数据,专注于音频片段上的链式思考──更小但更专注──

Audio Flamingo 3 (Goel et al., Temmuz 2025): mevcut açık SOTA. 8B LLM omurgası (Qwen2 7B), Whisper-large encoder concat BEATs, 64 sorgu Q-former, 1M+ ses metni talimat çiftleri üzerinde eğitim. MMAU 0.72, bazı alt görevlerde özel sınırla eşleşir.

> Audio Flamingo 3(Goel 等人,2025 yıl 7 月):当前开放 SOTA──8B LLM 主干(Qwen2 7B),Whisper-large 编码器拼接 BEATs,64 查询 Q-former,在100万+音频-文本指令对上训练──MMAU 0.72,在某些子任务上匹配闭源前沿──

AF3 ayrıca ses için talep üzerine düşünce zinciri de sunar: model, son cevabın öncesinde düşünce belirtileri ("al önce aletleri tanımlayacağım: ...") seçeneği olarak yayılabilir. Karmaşık akıl yürütme görevlerinde doğruluk düşünce etkinleştirildiğinde 3-5 puan yükselmektedir.

> AF3 ayrıca, basınçlı sesli düşünce zinciri de dahil etti: model final cevap önce seçkin olarak düşünce belirtilerini çıkarabilir.

### Kaskadör vs. uçtan sonuna

Su içi boru hattı:

> Sınıf:

1. Whisper ses → metni transkripte eder.
   Çeviri:Susper 将音频转录为文本
2. - Yazıyı kullanmak için nedenler.
   Çeviri:L.M.

"Bu podcast'i özetle" için mükemmel bir şekilde çalışır.
- "Bu şarkının ruh halini ne?"  ruh halini ses, kelimeler değil.
- "Kim konuşuyor, Alice mi Bob mu?"  konuşmacı kimliğini belirleme gerektirir.
- "Plomba ne zaman gerçekleşir?"  Zamanlı yerleşim metinde kayboldu.
- "Bu gerçek mi yoksa üretilmiş mi?"  Deepfake algılama akustik özelliklere ihtiyaç duyar.

> Bu programı "Üstlediğim" için mükemmel uygulanıyor.
> - "Bu şarkının duygusu nedir?"
> - "Kim konuşuyor, Alice ya da Bob?"
> - "Bir kaç saniye içinde patlama?" yazısında zaman yerini kaybetti.
> - "Bu gerçek mi doğuştan?"

Sonundan sonuna kadar ses sinyali korunur. Qwen-Audio ve AF3 müzik, çevre ve duyguları doğal olarak ele alıyor.

> 端到端保留了声学信号──Qwen-Audio 和 AF3 原生处理音乐、环境和情绪──

> **【中文解读】**级联管道 (Whisper 转录→LLM 推理) sadece ses kayıtlarına uygun, ancak müzik duygularını, konuşmacıların tanımlanmasını, zaman belirlemesini, derin sahte incelemelerini ve diğerleri için ses özelliklerini işlemek için yeterli değildir.

> **【拓展：金融场景的音频理解】**Finansal alanda, ses anlayışı kullanılabilir: finansal haber telefon toplantısının duygusal analizi (((sadece metin kaydını değil, ayrıca语气和语调) ;; tüccarın ses talimatlarının tanınması, müşteri kalitesi denetimi duygusal inceleme, toplantı kayıtlarının konuşmalarının ayrılması;;

### 2026 üretim tarifi

Yeni bir ses anlama ürünü için:

> 对于新音频理解产品:

- Eğer: transkripsiyon amacımızsa, müzik yok, duygusal sonuç yok.
  Çin Çeviri: Ceyre Programı: Eğer hedefimiz kaydedilmekse, müzik yok, duygusal bir karar gerekmiyor.
- AF3 / Qwen-Audio-aile: müzik, duygu, çok konuşmacı veya karmaşık ses düşüncesi.
  Çinçe Çevirimi:AF3 / Qwen-Audio 系列: If there is music、情绪、多人说话或复杂音频推理──

Kaskadör daha ucuz ve daha basit.

> 级联更便宜更简单――端到端更强大――

### MMAU  sesli akıl yürütme referans değerini

MMAU (Massive Multimodal Audio Understanding) 2024-2025 ses akıl yürütme referansıdır:

> MMAU (大规模多模态音频理解) 2024-2025 yılları için bir sesli yayın planı olarak belirtilmiştir.

- 10.000 sesli metin, konuşma, müzik, çevresel sesler arasında birleştirilmiş.
  Çin Çeviri: 10,000 个跨语音、音乐、环境声的音频-文本 QA 对──
- Sınıflandırma, zamansal akıl yürütme, nedensel akıl yürütme, açık bir şekilde sorgulanma kapsamını kapsar.
  Çinçe Çevirimiçi:覆盖分类、时间推理、因果推理、开放式 QA。
- Kaskadör boru hattlarının sistematik olarak kaçırdığı şeyleri test eder.
  Çinçe çevirisi:测试级联管道系统性遗漏的内容──

Açık SOTA (AF3) 0,72; özel sınır ~ 0,78 (Gemini 2.5 Pro, Claude Opus 4.7).

> 开源 SOTA(AF3) 0.72;闭源前沿约0.78(Gemini 2.5 Pro、Claude Opus 4.7)。差距小于VideoMME 的开源-闭源差距,说明音频 LLM 正在成熟──

## Çerçeveyi kullanın.
```figure
audio-text-ctc
```

## Kullan

`code/main.py`- ...

- Stdlib'de log-Mel spektrogram hesaplamalarını uyguluyor: pencereler, saf DFT, Mel filtre bankası.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Ç Ç Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Audio Q- eski iskelet: verilen kodlayıcı çıkış çerçeveleri, hesap Q, K, V, dikkat ve N simgeler gönderir.
  Çine Çeviri:音频 Q-eski 骨架:给定编码器输出,计算 Q、K、V、注意力并输出 N 个代币。
- Oyuncak görevinde kaskadör karşı karşılaştırma.
  Çinçe Çevirisi: Oyuncak görevlerindeki uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç uç

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-audio-llm-pipeline-picker.md`. Sesli bir görev (transkripsiyon, müzik etiketleme, duygu çıkarımı, çoklu hoparlör günlükleştirme, ortam sınıflandırması) verildiğinde, kaskad, uçtan sonuna AF3 veya hibrid seçilir.

> 本课产 出 `outputs/skill-audio-llm-pipeline-picker.md`◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊ ◊                                                                                                                                                                                                                                            

## Egzersizler.

1. 16kHz, 25ms penceresi, 10ms hop, 80 Mel binleri için 30 saniyelik bir klip için log-Mel spektrogram boyutunu hesaplayın. 48kHz'de bu nasıl değişir?

2. Whisper neden müzikte düşük performans gösteriyor? BEAT'in Whisper'in yapmadığı hangi ses özelliklerini yakaladığı var? WHY Whisper 在音乐上表现不佳?

3. 64 sorgu ile 32 sorgu ile 64 sorgu ile 32 sorgu ile 64 ne kadar karmaşık bir görev yapar? 32 hesaplama ne için? 64 sorgu ile 32 sorgu ile 64 sorgu ile 64 daha değerli? 32 节省了什么计算?

4. AF3 Bölümü 4. On-demand düşünce üzerine okuyun. Düşünce zinciri en çok yardımcı olduğu üç ses görevini önerin.

5. AF3'ün çıkışını kullanarak minimal günlükleştirme borusunu uygulayın. Konuşmacı değişimlerini nasıl sinyallersiniz? AF3 输出实现一个最小的说话人分离管道.

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| Log-Mel spectrogram | "Mel features" Mel 频谱 | 2D (time, frequency) array of log-magnitude values after Mel filter banks 经 Mel 滤波器组后的对数幅度二维数组 | |
| Audio Q-former | "Audio Perceiver" 音频感知器 | Cross-attention bottleneck from audio encoder output to fixed-length queries feeding the LLM 音频编码器输出到固定长度查询的交叉注意力瓶颈 | |
| Cascaded | "ASR-then-LLM" 级联管道 | Pipeline where Whisper transcribes and a text LLM reasons; loses acoustic information Whisper 转录后文本 LLM 推理的管道；丢失声学信息 | |
| End-to-end | "Audio-LLM" 端到端音频 LLM | Audio features enter the LLM directly via Q-former; preserves acoustic signal 音频特征通过 Q-former 直接进入 LLM；保留声学信号 | |
| BEATs | "Audio AudioSet encoder" 音频自监督编码器 | SSL transformer trained on AudioSet; strong on music + environmental sounds 在 AudioSet 上训练的自监督 Transformer；擅长音乐和环境声 | |
| MMAU | "Audio reasoning bench" 音频推理基准 | 10k QA pairs across speech, music, environment; 2024 eval standard 跨语音、音乐、环境的 1 万条 QA；2024 年评估标准 | |
| On-demand thinking | "Audio CoT" 按需音频思考 | Model can optionally emit reasoning tokens before final answer, lifts accuracy 3-5 pts 模型可在最终回答前输出推理 token，提升准确率 3-5 个百分点 | |

## Daha fazla okumak

- [Radford et al. — Whisper (arXiv:2212.04356)](https://arxiv.org/abs/2212.04356)
- [Chu et al. — Qwen-Audio (arXiv:2311.07919)](https://arxiv.org/abs/2311.07919)
- [Goel et al. — Audio Flamingo 3 (arXiv:2507.08128)](https://arxiv.org/abs/2507.08128)
- [Tang et al. — SALMONN (arXiv:2310.13289)](https://arxiv.org/abs/2310.13289)
- [Gong et al. — LTU (arXiv:2305.10790)](https://arxiv.org/abs/2305.10790)
