# VLA'lar: RT-2, OpenVLA, π0, GR00T.

> Bir model ilk kez bir web sitesinden bir tarif okudu ve mutfak robotu ile uyguladı RT-2 (Google DeepMind, Temmuz 2023). RT-2, metin işaretleri olarak eylemleri ayırt etti, web verileri ve robot eylem verileri üzerine bir VLM'yi birlikte ayarladı ve web ölçeğinde görme dil bilgisinin robot kontrolüne aktarıldığını kanıtladı. OpenVLA (Haziran 2024) açık 7B referansını gönderdi. Fiziksel Zeka'nın π0 serisi (2024-2025) akış eşleşme eylem uzmanlarını ekledi. NVIDIA'nın GR00T N1 (Mart 2025) ikili sistemli (Sistem 1 / Sistem 2) kontrolü, insanüstü robotlar için ölçekte sağladı. VLA ilkel  görme dili-hareket, gören, okuyan ve hareket eden tek bir model  bu aşamada anlama modelleri ile 15. aşamada otonom sistemler arasındaki köprüdür.

> **【中文解读】**RT-2  İlk kanıt: 网络级视觉语言知识可迁移到机器人控制:将关节动作分离成文代币,与VLM 联合微调;; OpenVLA 是开源 7B 参考,π0 引入流匹配动作专家,GR00T N1 实现双系统(快思考/慢思考) 人形机器人控制──VLA(视觉语言动作) 连接多模态理解和自主系统的桥梁──

> **【拓展：Embodied VLA 到机器人产业】**VLA modeli laboratuvardan endüstriye doğru ilerliyor: Tesla Optimus, Şekil 01,1X Teknolojiler ve diğer biçimli makineler VLA'ya dayalı kontrol sistemleri geliştirmektedir. Endüstriyel ortamda, VLA'nın depose edilmesi, depolama makineleri, montaj hattı işletim makineleri ve diğerleri için kullanılabilir.

**Type:** Learn
**Languages:** Python (stdlib, action tokenizer + VLA inference skeleton)
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 15 (Autonomous Systems, referenced)
**Time:** ~180 minutes

>  **【前置】**Özetle: Önemli bir süreç, bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre sonra bir süre daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha daha
>  **【类比】**VLA = "e bir makineye beyin ve gözüyle donatacak"。 geleneksel makine = 程序员写死 if-else 规则(see红色就停下);VLA = 像人看图说话做事("把红杯放到桌上"→看杯→规划路径→控制关节执行)。RT-2 动作分散 टोकне = 动作当文字写进提示;π0 流匹配 = 输出连续动作而非分散 टोकне,更精确──

## Öğrenme Hedefleri

- Eylem simgesi tanımlayın: ayrı bin kodlaması (RT-2), FAST verimli eylem simgesi, sürekli akış eşleşme eylemleri (π0).
  ÇINCE TRIBULATION: description动作分词化:离散bin 编码(RT-2) 、FAST 高效动作符号、连续流匹配动作(π0)。
- Web + robot verilerindeki ortak ince ayarlamanın neden yeni görevlere genel bilgi aktarımını koruduğunu açıklayın.
  Çinçe çevirisi: Neden birleştirilen bir bilgiyi yeni görevlere aktarma yeteneğini koruyabilmesi için neden birleştirildiğini açıklayın.
- OpenVLA (open 7B Llama+VLM), π0 (akış eşleşimi) ve GR00T N1 (ikili sistem) ile aynı robot görevinde karşılaştırın.
  Çinçe çeviri: 在同一机器人任务上比较 OpenVLA(开放 7B Llama+VLM) 、π0(流匹配) 和 GR00T N1(双系统) ⋅
- Açık X-Embodiment veri kümesinin ve RT-X eğitim korpusu olarak rolünün adını verin.
  ÇX-Bodyme 数据集 ve onun rolü olarak RT-X 訓練语料の列举

## Sorunlar. Sorunlar.

Doğal dil talimatlarından iş yapan bir robot 1970'lerden beri bir araştırma hedefi olmuştur. 2020'lerin cevabı: bir görme dili-hareket (VLA) modeli. VQA için kullanılan aynı VLM mimarisi, ancak çıkış metin yerine eylemlerdir (birleştirilmiş torks, son efektör pozları, ayrı komutlar).

> VQA ile aynı VLM yapı kullanıyor, ancak çıkışı hareketli bir işlemdir.

VLA'lara özel zorluklar:

> VLA'nın Özel Çabası:

1. Hareket alanları sürekli (birleştirilmiş açılar, güçler) ve yüksek boyutlu (7 DOF kol + 3-DOF tutku = 30 Hz'de 10 dim).
   Çinçe çevirisi:动作空间是连续的 (→节角度、力) 且高维 (→) △7 自由度臂 + 3 自由度爪 = 30Hz 下 10 维) △
2. Robot özel eğitim verileri nadirdir. Açık X-Embodiment ~ 1M yoldur; web metin görüntüsü 5B +.
   Çinçe Çevirisi:机器人专专专训数据稀缺──Open X-Embodyment 约100万条轨迹;网页文本-图像有50亿+──
3. Kontrol frekansı önemli. 30 Hz kontrol döngüsü, her harekete 33 ms bütçedir.
   Çinçe Çevirimi: kontrol frekansı çok önemlidir. 30Hz  kontrol rotası her hareket için 33 ms  bütçe anlamına gelir.
4. Yanlış bir eylem donanım, insan veya malı zarar verir.
   Çinçe çevirisi: güvenlik.

## Konsepten bir şey.

> **【中文解读】**具身視觉-语言-动作模型(VLA) 机器人 understand语言指令和视觉场景后执行物理动作──OpenVLA ise açık kaynaklı VLA, pi0(Fiziksel Zeka) ve NVIDIA Groot ise具身智能的代表性模型──VLA = 视觉编码器 + LLM + 动作解码器──

> **【拓展：具身智能的进展**OpenVLA-7B, Google Robot'ta görev başarısının %80'ini gerçekleştirmektedir. Pi0 kullanımı 流匹配 (ağış eşleşimi)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          


### Eylem simgesi (RT-2)

RT-2'nin hilesi: her ortak hedefi kuantistik bir metin jetonu olarak temsil edin. Normalleştirilmiş [-1, 1] aralığını 256 kutuya ayırın, her kutuyu bir kelime birikimi kimliği ile harekete geçirin. 10 DOF eyleminin her kontrol adımında 10 jetonu olur.

> RT-2 teknikleri:将每个关节目标表示为量化文本代币――将归结化的 [-1, 1] 范围离散化为 256 个 bin,每个 bin 映射到一个词汇 ID──10 自由度动作在每个控制步骤变成10 个代币──

PaLM-X VLM'i karışım üzerinde birlikte ayarlayın:

> PaLM-X VLM'de karışık veriler üzerinde birleşik mikro düzenleme:

- Web görüntü-metin çiftleri (başlık, VQA).
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Ç Ç Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Robot gösterileri, simgeler olarak hareket.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri

Model "kırmızı küpü topla" (dilli) → görüntü (görünüş) → 10 jeton eylem dizisi (diskretleştirilmiş ortak hedefler) görür. Web öncesi eğitim genel bilgi aktarımını korur: RT-2 "hızlı hareket eden nesneye doğru hareket" yapabilmektedir.

> 模型看"拿起红色方块" ({{lang-en}}) 图像 ({{lang-en}}) 视觉 ({{lang-en}})   }}  }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }} }}    }} }} }}  }} }}     }}                                                   

RT-2 kağıtında 3-5 Hz'de bir ferans, VLM autoregressive decode ile sınırlandırılır.

> RT-2 论文中推理速度 3-5 Hz, VLM'ye sınırlı

### OpenVLA  açık 7B referansı

OpenVLA (Kim ve diğerleri, Haziran 2024) açık ağırlıklı RT-2 eşdeğeri. 7B Llama omurgası, DINOv2 + SigLIP çift görüş kodlayıcı, 256 kutu üzerinde eylem simgesellemesi.

> OpenVLA is open权重的RT-2等价物──7B Llama 主干,DINOv2 + SigLIP 双视觉编码器,256 bin 动作分词化──

Açık X-Embodiment'te eğitim görmüşler. 22 robot üzerinde 970 bin rota.

> Açık X-Bodiment Üstü eğitimde.

Aktarım: 4-5 Hz, bir A100'de kuantitasyonla.

> 推理:A100 上量化后 4-5 Hz──对慢速操作足够,不适合高频控制──

### Hızlı Tokenizer  daha hızlı eylem çözümü

Pertsch et al. (2024) diskre bin tokenizasyonunun verimsiz olduğunu gösterdi  bin alanının küçük bir bölgesinde çoğu eylem kümesi. FAST (Frequency-domain Action Sequence Tokenizer) DCT üzerinden eylem sekanslarını sıkıştırır ve koefisienleri kvantize eder.

> Pertsch 等人(2024) gösterdi ki bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge bölge böl

30 adımlı bir eylem tarzı 300 ayrı bin jetonu yerine ~ 10 FAST jetonu olur.

> 30 步动作轨迹 yaklaşık 10 快速令牌 haline geldi, 300 散散 bin token değil.

### π0 ve akış eşleşme eylemleri

Fiziksel Zekilik'in π0 (Black et al., Ekim 2024) ayrı eylem belirtilerini akış eşleşme eylem uzmanıyla değiştirir:

> Fiziksel Zeka'nın pi0 Ustream匹配动作专家替代离散动作令子:

- Küçük bir eylem transformatörü VLM'nin gizli durumlarını okuyor ve düzeltilmiş akış yoluyla sürekli 50 adımlı bir eylem dizisini çıkartıyor.
  Çinçe Çevirim: Küçük hareket Transformer 读取 VLM 隐藏状态,通过正流输出连续的50 步动作序列──
- Hareket başı akış eşleşme kaybı ile trenler; VLM antrenman öncesi değişmez kalır.
  Çinçe Çevirisi:动作头用流匹配损失训练; VLM 预训练不变──
- İndirim: ~ 5 denoizing adımlarda yayılan tam eylem dizisi, etkin olarak 50 Hz kontrolü.
  Çinçe Çevirimiçi: 推理:完整动作序列在约5 步去噪中输出,等效50Hz 控制──

π0'nun iddiası: OpenVLA ve Octo'yu geniş bir manipülasyon görevleri yelpazesi üzerinde yenir.

> π0 声称: geniş bir operasyon görevinde OpenVLA ve Octo ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅ ⋅                                                                                                                                                                                 

> **【中文解读】**π0 Uses Suat Matching Alternative Disparate Motion Token: A Small Motion Transformer 读取 VLM 隐藏状态,通过正流输出连续的50 步动序列──推理时只需要约5步去噪音,实现效率等效50Hz 控制频率──连续动作表达保留了离散会破坏的动作平滑性──

π0.5 ve π0-FAST, aşamalı yükseltmelerdir. π0-FAST, FAST tokenizasyonunu akış eşleşimi ile birleştirir.

> π0.5 和 π0-FAST, büyüme yükseltme biçimidir.

### GR00T N1  İnsanüstü hayvanlar için çift sistem

NVIDIA'nın GR00T N1 (Mart 2025) insanüstü robotlar için inşa edilmiştir (> 30 DOF, tam vücut):

> NVIDIA'nın GR00T N1 için insan şeklinde bir cihaz tasarımı:

- Sistem 2: Büyük bir VLM okuma sahnesini + talimatı, ~ 1 Hz'de yüksek düzeyde alt hedefler üretir.
  Çinçe Çevirimi: Sistem 2: Büyük VLM 读取场景+指示,以约1Hz 生成高层子目标──
- Sistem 1: alt hedeflere kondisyone edilen düşük seviye 50-100 Hz ortak komutları üreten küçük bir hareket başı transformatörü.
  Çine çevirisi: sistem 1: küçük hareket başı Transformer 根据子目标生成底层 50-100Hz 关节命令。

Kahneman'ın hızlı ve yavaş düşüncesine ayrılmış haritalar: Sistem 2 planları, Sistem 1 eylemleri. Avantajlar: yavaş VLM boyutlu planlama hızlı kontrolü engeller; Sistem 1 gecikme için küçük kalır.

> Bu tür ayrıntılar Karaman'ın hızlı düşüncesine doğru: sistem 2  planlama, sistem 1  yürütme  Avantajları: yavaş hızlı VLM  seviyesinin planlaması hızlı kontrolü engellemez; sistem 1  küçük ölçekli tutarak düşük gecikmeyi garanti eder.

GR00T N1.7 (yıl 2025 sonları) veri ölçeklemesini geliştirir. GR00T, Omniverse'den sim-real verilerle ince ayarlar yapar.

> GR00T N1.7 ((2025 yıl sonu) geliştirilmiştir:

### Açık X-Body

RT-X (Oktyabr 2023) 22 robot üzerinde 1M yörüngeleri kapsayan 22 veri kümesi topladı. Open X-Embodiment herkesin kullandığı korpus:

> 訓練資料──RT-X(2023 yıl 10 月) 22 資料集ı birleştirdi, 22 機器10万条軌跡を覆い──Open X-Embodiment is all-men use语料:

- ALOHA / Bridge V2 / Droid / RT-2 Mutfağı / Dil Masası.
  Çeviri:Aloha / Köprü V2 / Droid / RT-2 Mutfağı / Dil Masası。
- Her örnek: (robot durum, kamera görüntüleri, talimatlar, eylem sırası).
  Çinçe Çevirim: her örnek:(机器人状态、摄像头视图、指令、动作序列)
- Eğitim hijyen: eylem alanını tekelleştirmek, ortak alanları normalleştirmek, kameraların boyutlarını değiştirmek.
  Çinçe Çevirimi: eğitim kuralları:统一动作空间、归一化关节范围、统一摄像头分辨率──

OpenVLA ve π0 Open X-Embodiment'de trenler.

> OpenVLA 和 π0                                                                                                                                                                                                                                                            

### - Sadece robotla karşılaştırıldığında

Co-fine-tuning web VQA verilerini robot yolları ile karıştırır. oran önemlidir: çok fazla VQA ve model eylemleri unutuyor; çok fazla robot verisi ve model genel bilgiyi kaybediyor.

> 联合微调将网页 VQA 数据与机器人轨迹混合──比例很重要:VQA 太多模型忘记动作;机器人数据太多模型失去通用知识──

RT-2 oranı: ~1:1. OpenVLA: ~0.5:1 web-robot. π0: benzer.

> RT-2 oranı yaklaşık 1:1──OpenVLA ∼ 0.5:1──π0 类似──精确比例是按数据集大小调节的超参数──

Sadece robot eğitiminde dağıtım dışı talimatlarda başarısız olan görev-spesifik modeller üretilir. Ko-fin-tuning "kırmızı küpü (demodede) topla" ve "soldan üçüncü en büyük nesneyi topla" arasındaki farkdır.

>                                                                                                                                                                                                                                                               

### Güvenlik ve eylem sınırları

Her üretim VLA gemisi:

> Her üretim sınıfı VLA şehri:

- sert eklem sınırları (specifiğe geçebilir).
  Çinçe Çevirim: sert性关节限制 (Koruçluk)
- Hız sınırı (yumuşak kesim).
  Çeviri: hız sınırlaması
- Çalışma alanı sınırları (son efektör masayı terk edemez).
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Yeni görevler için insanlık olarak onay.
  Çinçe Çevirisi: Yeni görev的人工审批──

Bu VLA'nın kontrol katman kontrolleri olarak VLA'nın dışında oturuyor.

> VLA'nın çıkışı bir emir değil, bir tavsiye.

## Çerçeveyi kullanın.
```figure
mm-action-tokens
```

## Kullan

`code/main.py`- ...

- 256-bin eylem tokenizasyonu ve tokenizlemeyi uyguluyor.
  Çinçe Çevirimi:实现 256 bin 动作分词化和反分词化──
- DCT + kuantitasyon üzerine kurulmuş FAST tokenizer çizimleri.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Etkinlik adım başına simge sayısını karşılaştırır (diskret bin, FAST, sürekli akış).
  Çinçe Çevirim:BİN BARAT                                                                                                                                                                                                                                                        
- RT-2 → OpenVLA → π0 → GR00T'nin soy özetini basar.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-vla-action-format-picker.md`. Robot görevleri (manipülasyon, navigasyon, insanüstü tüm vücut) verildiğinde, diskre bin + RT-2, FAST + OpenVLA, akış eşleşimi + π0, veya çift sistem + GR00T arasında seçim yapılır.

> 本课产 出 `outputs/skill-vla-action-format-picker.md`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △                   

## Egzersizler.

1. 10 DOF kolu 30 Hz kontrol hızında. 256 kutuda diskret-bin tokenizasyonu saniyede kaç tane token yayar? 7B VLM bir takip edebilir mi? 10 Freedom Mechanical Arm, 30Hz  kontrol frekansı, 256 离散 bin── her saniye kaç tane token üretir? 7B VLM 能跟上?

2. Hızlı tokenizasyon 30 adımlı yolları ~ 10 tokene sıkıştırır. Yolu yüksek frekanslı hareketlere (örneğin davul) sahipse kullanıcı ne kaybeder? Hızlı 30 adımlı yollar yaklaşık 10 tokene sıkıştırılır.

3. π0'nun akış eşleşme başı ~ 5 adım ile denosiyon yapar.

4. GR00T'nin Sistem 1 / Sistem 2 Kahneman'ın haritalarını bölüyor. İki ayaklı yürümeye yardımcı olabilecek farklı bir bölünme (Sistem 3?) önerin. GR00T'nin sistemi1/ sistemi2 ayrılığı Karaman teorisine karşı bir farklı ayrılığı önerir.

5. Açık X-Embodiment Bölüm 4'ü okuyun. Alan sızmasını önleyen üç kurasyon kuralını isimlendirin.

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|---------|
| VLA | "Vision-language-action" 视觉-语言-动作模型 | Model that takes image + instruction and outputs action commands 接受图像+指令并输出动作命令的模型 | |
| Action tokenization | "Discrete bins" 离散 bin 编码 | Quantize continuous joint targets into 256 bins per dim, each a vocab ID 将连续关节目标量化为每维 256 个 bin，每个 bin 对应一个词表 ID | |
| FAST tokenizer | "Frequency action tokens" 频域动作 token | DCT + quantize to compress 30-step trajectories to ~10 tokens 用 DCT + 量化将 30 步轨迹压缩为约 10 个 token | |
| Co-fine-tune | "Mix web + robot" 混合微调 | Train on web VQA data alongside robot demos to preserve general knowledge 在网络 VQA 数据和机器人演示上联合训练以保留通用知识 | |
| Flow-matching action head | "pi0 continuous output" 流匹配动作头 | Small transformer that outputs a 50-step action sequence via rectified flow 通过矫正流输出 50 步连续动作序列的小型 Transformer | |
| System 1 / System 2 | "Dual-system control" 双系统控制 | Large VLM plans slowly, small action head acts quickly; GR00T pattern 大 VLM 慢规划，小动作头快执行；GR00T 模式 | |
| Open X-Embodiment | "RT-X dataset" 开放具身数据集 | 1M-trajectory cross-robot dataset; the training corpus 100 万轨迹跨机器人数据集；标准训练语料 | |

## Daha fazla okumak

- [Brohan et al. — RT-2 (arXiv:2307.15818)](https://arxiv.org/abs/2307.15818)
- [Kim et al. — OpenVLA (arXiv:2406.09246)](https://arxiv.org/abs/2406.09246)
- [Black et al. — π0 (arXiv:2410.24164)](https://arxiv.org/abs/2410.24164)
- [NVIDIA — GR00T N1 (arXiv:2503.14734)](https://arxiv.org/abs/2503.14734)
- [Open X-Embodiment Collab — RT-X (arXiv:2310.08864)](https://arxiv.org/abs/2310.08864)
