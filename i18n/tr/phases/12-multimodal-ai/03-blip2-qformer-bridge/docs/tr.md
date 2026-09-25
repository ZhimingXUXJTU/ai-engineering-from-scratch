# CLIP'den BLIP-2'ye. Q-Former Modality Bridge olarak.

> CLIP, resim ve metni bir arada tutar, ancak başlıkları oluşturamaz, soruları cevaplayamaz veya bir sohbet yapamaz. BLIP-2 (Salesforce, 2023) bunu küçük bir eğitimli köprü ile çözdü: 32 öğrenilebilir sorgu vektörü, dondurulmuş bir ViT'nin özelliklerini çapraz dikkat yoluyla takip ederek, sonra dondurulmuş bir LLM'nin giriş akışına doğrudan yerleştirir. 188M köprü parametresi bir 11B LLM'yi bir ViT-g/14 ile bağladı. 2026 yılına kadar her adaptör tabanlı VLM  MiniGPT-4, InstructBLIP, LLaVA'nın kuzenleri  bir soylu. Bu ders, Q-Former'ın mimarisini okuyor, iki aşamalı eğitimini açıklıyor ve donmuş bir metin dekodere görsel jetonları besleyen bir oyuncak versiyonu oluşturur.

> **【中文解读】**CLIP sadece resimleri karşılayabilir ama üretemez. BLIP-2 32 öğrenilebilir sorgu yöntemi ile birleştirilmiş bir iletişim bağlantısı ile birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiş birleştirilmiştir.

> **【拓展：Q-Former→多模态架构演进】**Q-Eski "结视觉编码器+结LLM+轻量桥接" fanyomunun kurucusu, MiniGPT-4、InstructBLIP、LLaVA hepsi onun düşüncesinin son neslidir。

**Type:** Build | **类型:** 构建
**Languages:** Python (stdlib, cross-attention + learnable-query demo) | **语言:** Python（标准库，交叉注意力 + 可学习查询演示）
**Prerequisites:** Phase 12 · 02 (CLIP), Phase 7 (Transformers) | **前置知识:** Phase 12 · 02（CLIP），Phase 7（Transformer）
**Time:** ~180 minutes | **时间:** ~180 分钟

>  **【前置】**学本节前 Lütfen önce öğrenin:Fase 12·02(CLIP karşılaştırma öğrenmek için);Fase 7(Transformer 自注意力和交叉注意力);Fase 11·04(Embeddings)。
>  **【类比】**S-Eski = "Journalist interview"──32 个记者(query) Stand ViT 出来的 256 补丁 前面,每个人都提问自己的问题,听完回答后写下 32 条新闻摘要──这32 条摘要就是给LLM 的"新闻简报",LLM 不用看完整 256 张原始图片──

## Öğrenme hedefleri

- Dondurulmuş bir görme kodlayıcı ile dondurulmuş LLM arasındaki eğitimlenebilir bir boğazın maliyet ve istikrar konusunda son-son düzeltmeyi neden yendiğini açıklayın.
  Çinçe Çevirisi: Neden En Son Video Editing Değişimi ve LLM Arasındaki Eğitimli Boşluklar, maliyet ve sabitlik açısından en son seviyesine göre daha iyi olduğunu açıklayın.
- Dış görüntü özelliklerine göre öğrenilebilir sorguların sabit bir kümesi uygulanmış bir çapraz dikkat bloğu uygulanmalıdır.
  Çinçe Çevirisi: bir grup belirlenmiş öğrenilme sorusu oluşturan bir çaplı dikkat bloğu gerçekleştirmek.
- BLIP-2'nin iki aşamalı öncesi antrenmanını geçin: temsil (ITC + ITM + ITG) sonra üreticidir (dondurulmuş dekodör ile LM kaybı).
  Çinçe Çevirimi:理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理 BLIP-2 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B 理B
- Q-Former'ı LLaVA'da kullanılan basit MLP projeksiyonu ile karşılaştırın ve her seçim ne zaman kazanırsa tartışın.
  Çinçe Çevirimiçi: Q-Former 和 LLaVA kullanımı daha basit MLP 投影器,论证各自的优势场景──

## Sorunlar. Sorunlar.

Bir donmuş ViT'de, görüntü başına 256 parç tokeni üretilir. Dimin 4096'nın token yerleştirmelerini bekleyen donmuş 7B LLM'de bulunur. Açık bir köprü  1408'den 4096'a kadar bir doğrusal katman çalışır, ancak LLM'nin bağlamına tüm 256 parç tokeni eklemek, görüntü başına 256 ekstra tokeni maliyetindedir. 32 görüntüden oluşan bir partiye göre sadece görsel modalite tarafından tüketilen 8192 token.

> Bir sonucun bir ViT'i var, her görüntü 256 boyutlu bir patch token üretir. Bir sonucun bir 7B LLM'i var, 4096 token'ın bir boyutlu bir token olmasını bekler. Görünen o ki, 1408 ile 4096 arasındaki bir bağlantı mevcuttur.

BLIP-2 sorusu: 256 token resmi temsilini daha az token olarak (sayın 32) sıkıştırıp, LLM'nin resim hakkında başlık, soruları cevaplamak ve mantık yürütmek için yeterli bilgiyi koruyabilir mi? Ve bu köprüyü dondurulmuş omurganlara dokunmadan, eğitim maliyetini köprünün parametrelerine kadar tutabilir mi?

> BLIP-2 sorusu: 256 token görüntü göstergesini 32 tokenden daha azına sıkıştırarak, aynı zamanda LLM'nin resim tanımlamasını, soruları ve düşüncelerini yapmasını sağlayacak yeterli bilgiyi saklayabilir misiniz?

Cevap: Bir Q-Former. 32 öğrenilebilir "sorum" vektörleri, ViT'nin yama tokensine karşı karşıya giderek LLM'nin tükettiği 32 tokenli görsel bir özet üretir. 188M parametreler toplam. LLM'ye dokunmadan önce kontrast, eşleşme ve üretken hedeflerle eğitilmiştir.

> Cevap: Q-Former──32 个可学习的"查询"量通过交叉注意关注 ViT'in patch token,产生LLM 消费的32 token 视觉摘要──总共188M 参数──接触LLM 之前对比、匹配和生成目标进行训练──

## Konsepten bir şey.

> **【中文解读】**BLIP-2  Q-Former'i 结视觉编码器和结 LLM 之间轻量桥接层──Q-Former'ı kullanmak için bir grup öğrenilebilir sorgu simgesi kullanmak, video kodlayıcılardan metin ile en çok ilişkili görsel özellikler elde etmek, eğitim parametrelerini büyük ölçüde azaltmak, yüksek verimlilikli bir görsel-dilli birleştirme gerçekleştirmek.

> **【拓展：BLIP-2 的高效训练】**BLIP-2 tek Çang A100'de 12 saat içinde tamamlanabilir. Sadece Q-Former 参数), önceki yöntemlerden 10-100 kat daha hızlı. Q-Former'ın tasarımı sonrakilerdeki LLaVA、InternVL ve diğer modelleri etkiledi.


> **【拓展：Q-Former 的影响】**Q-Former'in tasarım düşüncesi (((Bilmek için kullanılabilir sorgulardan 结编码器提取任务相关特征) geniş çapta alınmıştır.


### Öğrenilme Sorular

Q-Former'ın temel hilesi: LLM'nin metin tokenlerinin görüntü yamalarına bakmasına izin vermek yerine, 32 öğrenilebilir sorgu vektörünün yeni bir seti sunulmalıdır `Q`*Tarifler modelin parametreleridir  eğitim sırasında öğrenildi ve her görüntü için aynı 32 sorgu kullanılır.

> Q-Former'in temel teknikleri: LLM'nin metin simgesi  resim yamacı üzerinde odaklanmak yerine yeni 32 öğrenilebilir soru yöntemi oluşturmak `Q`, let* them* focus on image patch── query is the parameter of the model in training, and each image uses the same 32 queries──

> ️ **【易错点】**"32 sorgu 32 farklı resim sorgu" 错!32 sorgu kesin  tüm resimlere aynıdır.
> 🤔 **【困惑】**S: 32 个查询 如何知道每个该看什么?A: 训练时三个损失(ITC/ITM/ITG) 会反向传播梯度告诉每个查询 该专精什么;;最终学到的 32 维编码是"损失下降最快的那个方向",不是人为指定的"颜色/物体/背景"――

Çelişkili dikkatten sonra, her sorgu resmin sıkıştırılmış bir özetini tutar  " ana nesneyi açıklayın", " arka planı açıklayın", " nesneleri sayın" vb. Sorgular kelimenin tam anlamıyla semantik etiketlere odaklanmaz; aşağıdaki kayıpları düşüren her kodlamayı öğrenirler.

> 交叉注意後, her sorguda resmin sıkıştırılmış özetleri var. "özel nesneyi tanımlamak""",töknemi anlatmak""",sayı hesaplama nesneyi hesaplamak" ve s. Sorgular kelimenin anlamı üzerinde yoğunlaşmıyor.

### Mimarlık

Q-Former, iki yollu küçük bir transformatördür (12 katman, ~ 100M param)

> Q-Former bir küçük Transformer (12 kat, yaklaşık 100M) vardır.

1. Sorgu yolu: 32 sorgu vektörü kendi kendine (kendileri arasında) akıyor, sonra dondurulmuş ViT'nin yama tokenleri üzerinde çapraz ilgi, sonra FFN.
   Çinçe Çevirimi: sorgu yolu: 32 个查询向量流过自注意力(彼此之间), sonra 结 ViT'in patch token yaparak交叉注意力,最后是FFN。
2. Metin yolu: BERT benzeri bir metin kodlayıcı sorgu yolu ile kendi dikkatini ve FFN ağırlıklarını paylaşır.
   Çinçe Çevirimiçi:文本路径:类 BERT'in文本编码器与查询路径共享自注意力和FFN 权重──文本路径禁用交叉注意力──

Eğitim sırasında her iki yol da çalışır. Sorgular ve metin ortak kendi dikkat yoluyla etkileşim kurar, bu da sorguların metine ihtiyaç duyan görevler için şartlanabileceği anlamına gelir. VLM teslimatı için sonuçlama zamanında, yalnızca sorgular akıyor ve 32 görsel jeton üretir.

> 訓練時兩条路線同時運行──查詢與文本通過共享的自注意交互, bu da sorguların metin gerektiren görevlerde kullanılabileceği anlamına gelir.

### İki aşamalı eğitim

BLIP-2 iki aşamada hazırlanır:

> BLIP-2 分两阶段预训练:

Eğitim aşaması 1: temsilcilik öğrenimi (LLM yok).
- ITC (image-text contrast): Toplanmış sorgu simgelerinin ve metin CLS simgelerinin arasındaki CLIP tarzı kontrast.
  Çinçe Çevirimiçi:ITC(图文对比):池化查询代币与文本 CLS代币 之间类 CLIP对比损失──
- ITM (resim-metin eşleşimi): ikili sınıflandırıcı  bu resim-metin çift eşleşebilir mi?
  Çinçe Çevirimiçi:ITM(图文匹配):
- ITG (resim tabanlı metin oluşturma): sorgulara bağlı olarak metin üzerine nedençi LM başlığı.
  Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilinde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine dilde: Çine di: Çine di: Çine di: Çine di: Çine di: Çine di: Çine Çine di: Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Çine Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç

>  **【类比】**Üç kaybı:ITC = "görüntü bulma yazısı" (粗粒度对齐);ITM = "görüntüyi doğru bir şekilde incelemek" (görüntüyi doğru şekilde incelemek);ITG = "görüntüyi doğru bir şekilde incelemek" (görüntüyi doğru şekilde incelemek)

Sadece Q-Former trenleri, ViT dondurulmuş, LLM dahil değil.

> 仅训练 Q-Former──ViT 结──不涉及 LLM──

2. aşama: üretken öğrenme. Dondurulmuş bir LLM (OPT-2.7B veya Flan-T5-XL, vb.) ekleyin. 32 sorgu çıkışlarını küçük bir doğrusal katman yoluyla LLM'nin gömülme zayıflığına projekte edin. Metin uyarısına hazırlayın. Sadece doğrusal projeksiyonu ve LM kayıpına LM üzerinde tren yapın.

> İkinci aşama: öğrenme oluşturmak. Bir LLM'nin sonucuna bağlanmak. Bir küçük linear katman üzerinden 32 sorgu çıkartmak ve projeyi LLM'nin yerleşim boyutuna çıkarmak.

2. aşamaldan sonra, Q-Former + projeksiyon tam görsel adaptördür.

> İkinci aşamada, Q-Former + 投影就是完整的视觉适配器──推理时:图像 → ViT → Q-Former → 线性投影 → 前置到文本 → 结 LLM 生成输出──

### Parametre ekonomisi

BLIP-2 ViT-g/14 (1.1B, dondurulmuş) + OPT-6.7B (6.7B, dondurulmuş) + Q-Former (188M, eğitilmiş) = 8B toplam, 188M eğitilmiş.

> BLIP-2 kullan ViT-g/14(11 milyar,结) + OPT-6.7B(67 milyar,结) + Q-Former(1.88 milyar, 结) = 共 80 milyar, 练 1.88 milyar, 练 1.88 milyar, Q-Former 仅占全参数约2.4%── 练费用反映这一点:少量 A100 上数天 vs 端到端数周──

Kalite: BLIP-2 sıfır vQA'da Flamingo-80B'ye eşleşir veya yenir.

> 质量:BLIP-2 在零样本 VQA 上匹配或超越 Flamingo-80B,同时小了50倍──桥接方案有效──

### InstructBLIP ve talimatları bilen Q-Former

InstructBLIP (2023) Q-Former'ı ek bir girişle genişletiyor: talimat metni kendisi. Çelişkili dikkat zamanında, sorgular artık hem görüntü yamalarına hem de talimata erişebilir. Sorgular tek sabit bir özet öğrenmek yerine talimat başına uzmanlaşabilen (" arabaları sayın", "ruhiyyeti açıklayın"). Benchmark, tutulan görevlerde kazanç sağlar.

> InstructBLIP(2023) ekstra giriş yoluyla genişletildi Q-Former: instruction text itself──.

### MiniGPT-4 ve sadece projektorla yaklaşım

MiniGPT-4 Q-Former'i korudu ancak diğer her şeyi dondururken sadece çıkış çizgisi projeksiyonunu eğitdi.

> MiniGPT-4'i Q-Former'e bırakmıştım, ama sadece tren çıkış linear projeksine, diğer tüm şeyleri bitirir.

### Neden LLaVA daha basit oldu ?

LLaVA (2023, Ders 12.05) Q-Former'ı, LLM alanına her ViT patch tokenini  576 token / görüntü için 24x24 şebekesi için projekt eden basit 2 katlı MLP ile değiştirdi. Daha kötü sıkıştırma ama LLM'nin incelemesini bırakır. O zamanlar bu tartışmalıydı; 2023'ün sonuna kadar baskınydı çünkü görsel talimat verileri (LLaVA-Instruct-150k) MLP'nin yeterli sinyal korumak için eğitilebileceğini kanıtladı. Tasarım: LLaVA'nın bağlamı daha hızlı dolduruyor, ancak doğal olarak çoklu görüntü ve videoya ölçeklendiriyor.

> LLaVA(2023, 12.05 课) basit 2 katlı MLP ile Q-Former'i değiştirdi, her ViT patch tokenini LLM 空间24x24 网格下 her resim 576 个 token'a, tüm LLM'e  压缩更差, ancak LLM'nin orijinal patch'e odaklanabilmesi için kullanıldı. O sırada bu tartışmalıydı; 2023 yılının sonuna kadar, görsel talimat verileri nedeniyle ana dayanan hale geldi.

> 🤔 **【困惑】**学完本节还会问:Q-Former vs LLaVA MLP 该选哪个? 短上下文 + 高质量 → Q-Former(压缩32 token 精心训练);长上下文 + 多图/视频 → LLaVA MLP(每 token 信息量大但灵活) ⋅ 2026 yılının çoğu VLM MLP kullanır, çünkü görsel talimat verileri yeterince fazla olduğunda, MLP öğrenilmesinin yeterince iyi ve daha kolay genişletilmesi için yeterli olacaktır―

2026 yılına kadar alan bölünmesi: Q-Former, token bütçesi önemli olan yerlerde hayatta kalır (uzun video, birçok görüntü); MLP projeksiyonu, token başına çiğ kalitenin öncelikli olduğu yerlerde baskınlık yapmaktadır.

> 2026 yılına kadar, alan ayrımı: Q-Former  token  bütçe önemli zaman 长视频、多图像) hayatta; MLP 投影器 每个 token 的原始质量优先时占主导;;

### Çapalı dikkat: Flamingo, ata

Flamingo (Denevi 12.04) BLIP-2'den önce aynı çapraz dikkat fikrini kullandı ancak her dondurulmuş LLM katmanında tek bir köprü olarak değil. BLIP-2 sadece giriş katmanına sıkıştırılabileceğini ve hala çalışabileceğini gösterdi. Gemini ve Idefics her ikisini birleştirdi: birbirine karışmış giriş jetonları ve bağlamda birkaç çekim için seçmeli kapalı çapraz dikkat.

> Flamingo (第 12.04 课) BLIP-2'den önce aynı anahtarlık dikkatini kullanmak ama her bir LLM katmanında, tek bir köprü değil bir tek bir köprüde kullanmakla birlikte BLIP-2'nin kanıtları sadece giriş katmanına kadar sıkıştırılabilir ve hala geçerlidir.

### 2026'daki soylular

- Q-Former: BLIP-2, InstructBLIP, MiniGPT-4, ve çoğu video dil modeli token bütçe nedenleri için.
  中文翻译:Q-Former:BLIP-2、InstructBLIP、MiniGPT-4,以及大多数视频语言模型 (BİLİP-2、InstructBLIP、MiniGPT-4,以及大多数视频语言模型)
- Algılayıcı resampler: Flamingo'nun varianti (Denevi 12.04); Idefics ailesi, Eagle, OmniMAE.
  Çeviri:Flamingo'nun değişimi (Flamingo'nun değişimi)
- MLP projekörü: LLaVA, LLaVA-NeXT, LLaVA-OneVision, Cambrian-1.
  Çeviri:LLaVA,LLaVA-NeXT,LLaVA-OneVision,Cambrian-1
- Dikkat havuzu: VILA, PaliGemma.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Ç Çeviri: Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç

Dörtü de geçerlidir. Önemli soru, simge bütçesi mi yoksa simge başına kalite mi kısıtlı?

> Dört farklı seçenek geçerlidir. Kararlılık sorusu, senin sınırların, senetlerin, bütçelerin veya her senetin kalitesi.

## Çerçeveyi kullanın.
```figure
modality-projection
```

## Kullan

`code/main.py`Stdlib Q-Former tarzı bir çapraz dikkat oluşturur:

> `code/main.py`构建一个标准库 Q-Former 风格的交叉注意:

1. 256 görüntü yama tokeni (dim 128) simüle edin.
   Çinçe Çevirim:模拟 256 个图像补丁符号(维度 128)。
2. 32 öğrenilme sorguyu (dim 128)
   Çinçe Çevirimi:实例化 32 个可学习查询(维度 128)。
3. Skalalı nokta- ürün çaplı dikkatini çalıştırın (Çeviri sorgularından, K/V'den yamalar).
   Çinçe Çevirimi: Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanakkale Çanak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Çak Ç Ç Ç Çak Çak Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
4. Proje ile LLM-dim (512) bir çizgi katman üzerinden.
   Çinçe Çevirim: 線性層投影到 LLM 维度 ((512) 』
5. 32 LLM hazır görsel tokeni çıkart.
   Çinçe Çevirisi:输出 32 LLM 就绪的视觉代号.

Tüm matematikler saf Python'da (vektorlar üzerinde yuva döngüleri). Oyuncak ama doğru şekil. Dikkat ağırlığı matrisi basılır, böylece her sorunun hangi yamalardan çekildiğini görebilirsiniz.

> Tüm matematik işlemleri saf Python ile yapılır.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-modality-bridge-picker.md`. Hedef bir VLM yapılandırmasını (görünüş kodlayıcı token sayımı, LLM bağlam bütçesi, dağıtım kısıtlamaları, kalite hedefi) göz önüne alındığında, her köprü için kısa bir tembih ve parametreler sayısının tahminini ile Q-Former vs. MLP vs. Perceiver resampler önerir.

> 本课产 出 `outputs/skill-modality-bridge-picker.md`△ 配置 (VLM 配置) △ 视觉编码器 token 数、LLM 上下文预算、部署约束、质量目标), Q-Former vs MLP vs Perceiver resampler,附简短理由和每个桥接层的参数估算──

## Egzersizler.

1. PyTorch'te çapraz dikkat blokunu uygulayın. 32 sorgu ve 256 anahtar/değer ile dikkat ağırlığı matrisinin 32 x 256 olduğunu ve her satırın softmax'den sonra 1'e kadar olduğunu kontrol edin.
   Çinçe Çevirim: PyTorch ile 实现交叉注意力块──验证 32 个查询和 256 个键/值,注意力权重矩阵为 32 x 256,每行软max 后和为 1──

2. BLIP-2 aşamasında Q-Former aynı anda üç kayıp yürütür: ITC, ITM, ITG. Her biri için ileriye imza yazın. Hangisi aktif olması için metin kodlayıcı yolunu gerektirir?
   Çin dilinde: BLIP-2 ilk aşamasında, Q-Former aynı zamanda üç kayıp işlevi: ITC, ITM, ITG.

3. Parametre sayısını karşılaştırın: Q-Former (12 katman, 768 gizli) vs. 2 katman MLP projeksiyonu (1408 → 4096, iki katman).
   Çin dilinde:Comparison参数:Q-Former(12 katlı, 768 隐藏维度) vs 2 katlı MLP 投影器(1408 → 4096,两层) ・・・

4. BLIP-2 makalesinin (arXiv:2301.12597) 3.2. bölümünü okuyun. Q-Former'in nasıl initialize edildiğini açıklayın.
   Çin dilinde:BLEIP-2 论文 ((arXiv:2301.12597) Bölüm 3.2 Q-Former başlangıç bölümü hakkında.

5. 60 kadroya kadar örneklenen 1 FPS'de 10 dakikalık bir video için, kadro başına token maliyetini (Q-Former → 32 token/frame) vs (MLP projeksiyonu → 576 token/frame) hesaplayın.
   Çine çevirisi: için 10 dakika video 1 FPS 样式为 60 ,计算每代币 成本:(Q-Former → 32 token/) vs(MLP 投影器 → 576 token/) ・・・ Hangi 128k token içine bırakabilir LLM 上下文窗口?

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| 术语 | 通俗说法 | 实际含义 | |
| Q-Former | "Querying transformer" | Small transformer with 32 learnable query vectors that cross-attend to frozen ViT features | 带有 32 个可学习查询向量的小型 Transformer，交叉关注冻结的 ViT 特征 |
| Learnable queries | "Soft prompt for vision" | A fixed set of parameters that serve as the query side of cross-attention; learned per model, shared across all inputs | 作为交叉注意力查询侧的固定参数集；按模型学习，所有输入共享 |
| Cross-attention | "Q from here, K/V from there" | Attention where query, key, and value come from different sources; how the queries pull from ViT patches | 查询、键和值来自不同来源的注意力；查询如何从 ViT patch 提取信息 |
| ITC | "Image-text contrastive" | CLIP-style loss applied to Q-Former pooled queries vs text CLS | 应用于 Q-Former 池化查询与文本 CLS 的类 CLIP 对比损失 |
| ITM | "Image-text matching" | Binary classifier on hard-negative-mined pairs; forces the queries to discriminate fine-grained mismatches | 难负例挖掘对上的二分类器；强制查询区分细粒度不匹配 |
| ITG | "Image-grounded text generation" | Causal LM loss where text is generated conditioned on queries; forces queries to encode text-decodable content | 以查询为条件生成文本的因果 LM 损失；强制查询编码可解码为文本的内容 |
| Two-stage pretraining | "Representation then generative" | Stage 1 trains Q-Former alone (ITC/ITM/ITG); Stage 2 attaches frozen LLM and trains only the projection + Q-Former | 第一阶段仅训练 Q-Former；第二阶段连接冻结 LLM，仅训练投影 + Q-Former |
| Frozen backbone | "Do not finetune" | The vision encoder and LLM weights are fixed; only the bridge trains | 视觉编码器和 LLM 权重固定；仅训练桥接层 |
| Projection head | "Linear to LLM dim" | Final linear layer mapping Q-Former output to the LLM's embedding dimension | 将 Q-Former 输出映射到 LLM 嵌入维度的最终线性层 |
| Perceiver resampler | "Flamingo's version" | Similar learnable-query cross-attention, used by Flamingo at every layer rather than as a single bridge | 类似的可学习查询交叉注意力，Flamingo 在每层使用而非单一桥接 |

## Daha fazla okumak

- [Li et al. — BLIP-2 (arXiv:2301.12597)](https://arxiv.org/abs/2301.12597) çekirdek kağıt.
  Çeviri:Blip-2
- [Li et al. — BLIP (arXiv:2201.12086)](https://arxiv.org/abs/2201.12086) ITC/ITM/ITG üçlü ile önceki.
  中文翻译:前作,包含 ITC/ITM/ITG 三联损失──
- [Li et al. — ALBEF (arXiv:2107.07651)](https://arxiv.org/abs/2107.07651) "Fusadan önce uyum"  1. aşamalı eğitimin kavramsal ataları.
  Çinçe Çevirisi: "Pere对齐再融合"
- [Dai et al. — InstructBLIP (arXiv:2305.06500)](https://arxiv.org/abs/2305.06500) talimatları bilen Q-Former.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Zhu et al. — MiniGPT-4 (arXiv:2304.10592)](https://arxiv.org/abs/2304.10592) Sadece projektorla yaklaşım.
  Çeviri: sadece projeci
- [Jaegle et al. — Perceiver IO (arXiv:2107.14795)](https://arxiv.org/abs/2107.14795) Öğrenilebilir-soru sorusu çapraz ilgi için genel mimarlık.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
