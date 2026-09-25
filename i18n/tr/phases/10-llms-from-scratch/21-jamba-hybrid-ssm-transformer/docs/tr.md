# Jamba  Hibrit SSM-Transformer  Jamba  Mixed SSM-Transformer

> Devlet uzay modelleri (SSM) ve transformatörler farklı şeyler istiyor. Transformatörler dikkatle kaliteyi kat kat maliyetle satın alırlar. SSM'ler, geri dönüş yoluyla, hatta zaman sonucu ve sabit hafıza satın alır. AI21'in Jamba (Mart 2024) ve Jamba 1.5 (Avgust 2024) modellerini aynı modelde koydu: her 7 Mamba katman için 1 Transformer katmanı, diğer her blokta MoE ve tek 80GB GPU'ya sığan 256k bağlam penceresi. Mamba-3 (ICLR 2026) SSM tarafını karmaşık değerli devlet alanları ve MIMO projeksiyonları ile sıkılaştırır. Bu ders, her iki mimarlığı da sonuna kadar okuyor ve melez tarifinin saf-SSM ve saf-Transformer uzun bağlamlı girişimlerinin yapmadığı zaman üç yıllık ölçeklendirmeyi neden hayatta bıraktığını açıklıyor.

> **【中文解读】**Transformer, SSM, Linear Time Teller ve Normal Bilgi Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı Kaynaklı

> **【拓展：SSM+Transformer→未来架构】**純 SSM 和純 Transformer 在长上下文任务上各有局限性──混合架构──Jamba、Mamba-3) iki avantajı birleştirdi, muhtemelen 2026-2027 yıl长上下文模型的主流方向──

>  **【前置】**学本节前请先掌握:Phase 07(Transformers);状态空间模型(SSM, Mamba) concept;MoE(Mix of Experts)。本节是SSM 和 Transformer 混合架构的代表作──
>  **【类比】**Jamba = "长短记忆组合"──Transformer = 短期记忆(精确但贵,每件事都需要注意力);Mamba = 长期记忆(粗略但便宜,用状态缩历史)──1:7 比例 = 偶尔做精确记忆,大多数时候用快速缩记忆──两者结合在 256K 上下文 下既精确又便宜──

**Type:** Learn
**Languages:** Python (stdlib, layer-mix calculator)
**Prerequisites:** Phase 10 · 14 (open-model architectures), Phase 10 · 17 (native sparse attention)
**Time:** ~60 minutes

## Öğrenme hedefleri

- Jamba blokundaki üç primitifleri açıklayın  Transformer katmanları, Mamba katmanları, MoE  ve 1:7:even birbirine karışan tarif.
  解释 Jamba 块中的三个基元Transformer 层、Mamba 层、MoE及 1:7:偶数层交织方案
- SSM'nin yüksek seviyede tekrarlanması nasıl göründüğünü ve neden sürekli hafıza çıkarımını sağladığını açıklayın.
  Açıklama: MSM'nin makroekonomik olarak dönüşümünün nasıl olduğunu ve neden sürekli sayısal kayıp düşüncesini gerçekleştirebildiğini açıklayın.
- Jamba modelinin KV önbelleği ayak izini 256k bağlamda hesaplayın ve saf Transformer modelinin ihtiyaç duyduğu ile karşılaştırın.
  计算 Jamba 模型在 256K 上下文中的 KV 缓存占用,并与纯变压器 模型对比
- Mamba-3'ün üç yeniliğini (eksponansiyel-trapezoidal diskretizasyon, karmaşık değerli durum güncelleştirmesi, MIMO) ve her birinin hedefi olan sorunu ne olarak adlandırın.
  Mamba-3'ün üç yeniliği, ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞           

## Sorunlar. Sorunlar.

Dikkat, dizilerin uzunluğunda karelidir. Devlet alan modelleri doğrusaldır. Bu fark bileşiklerdir: 256k jetonlarda, bir Transformer dikkat haritası baş başına 65B girişdir; bir SSM'nin tekrar eden durumu dizilerin uzunluğundan bağımsız olarak sabit boyutdadır.

> Sistem uzunluğunda dikkat ikinci bir şeydir. Devlet uzay modeli doğrusaldır. Bu fark toplanmadan sonra çok önemli: 256k token. Transformer dikkat çizgisinde her başta 650 milyar madde vardır.

Temiz SSM modelleri (Mamba, Mamba-2) küçük ölçeklerde Transformer karmaşıklığına eşleşir, ancak durum izleme görevlerinde geride kalır ve bağlam içi geri alım bazı kategorilerde başarısız olur.

> Mamba Mamba-2) küçük ölçekte uyumlu Transformer 困惑度, ama durum takip görevinde geride, bazı üst aşağıdaki arama sınıfında başarısızlık 直觉:SSM tarihini sabit duruma sıkıştırır, tarih uzun zaman, bilgi sızdırılır── dikkat her şeyi hatırlamak için dikkat ama ikinci bir ödeme yapmak──

Açık bir çözüm: İkisini de kullan. Transformer katmanlarını tam hatırlama önemli olduğu yere koy. SSM katmanlarını başka yerlerde kullan. Rasyon ayarlayın. Jamba, bu hibrit tarifini ölçekte gönderen ilk üretim derecesi modeli (52B toplam, 12B aktif, 256k bağlam, tek 80GB GPU). Jamba 1.5 ailesini toplam 398B / 94B aktif olarak genişletiyor. Mamba-3 (ICLR 2026) hibritlerin yeniden inşa edilebileceği mevcut en iyi saf SSM tabanıdır.

> 显而易见的修复:两者都用──在需要精确回忆的地方放 Transformer层──其他地方使用SSM层──调整比例──Jamba, bu karışımsal şevkinin ilk büyük çapta teslim edilen üretim sınıfı modeli olmuştur.52B 总参数,12B 活跃,256k 上下文,单张 80GB GPU)──Jamba 1.5 将家族扩展到398B 总参数 / 94B 活跃参数──Mamba-3ICLR 2026) mevcut en iyi saf SSM 基线, karışık yapı yeniden inşa edilebilir.

Bu ders, üç makaleyi de okuyor ve "doğru oranı seç" için zihinsel model oluşturur.

## Konsepten bir şey.

> **【中文解读】**Jamba, AI21 Laboratuvarları tarafından önerilen karmaşık SSM-Transformer yapı, Mamba'nın durum uzay modeli) katmanını ve Transformer dikkat katmanını birbiriyle birleştirir.

> **【拓展：SSM 与 Transformer 的融合趋势】**Mamba等 SSM'nin düşünce karmaşıklığı O(1)(Fixed State), Transformer ise O(n)(KV-cache 随序列增长) ・・・Jamba 将两者结合:SSM 处理长程依赖(高效),注意处理需要精确回溯的任务(准确) ・・・ Bu karışım yapı, uzun uzun aşağıdaki düşünce düşüncesinin gelecekteki yönü olabilir。


### Bir sayfada bir SSM

Bir devlet uzay modeli bir dizi işleme yapar `x_1, ..., x_N`sabit boyutlu bir durumla.`h`- ...

```
h_t = A h_{t-1} + B x_t
y_t = C h_t
```

Her aşamada , devlet bir çizgi dinamikle gelişir .`A`, giriş alır `B x_t`, ve çıkışı yayıyor `C h_t`- Evet .`A, B, C`Önemli bir özelliği dikkat edin: Bilgisayar`y_t`Sadece ihtiyaçları var.`h_{t-1}`ve `x_t`Daha önce hiç olmadı .`x`Hatırlama sabit.

Modelleme kalitesi için bir hile , `A`S4 (Gu 2021) eğitim sırasında uzun bir konvulsiyon olarak verimli bir şekilde değerlendirilebilecek yüksek yapılandırılmış bir matris kullandı.`A, B, C`Mamba-2 (2024) yapıyı daha da basitleştirdi. Mamba-3 (2026) belirli yerlerde karmaşıklığı yeniden ekledi.

Ana özellik: bir dekoder LLM için, bir SSM katmanı, büyüyen KV kasesi yerine sabit boyutlu katman durumuna sahip bir dikkat katmanı için bir düşüş değiştiricidir.

### Jamba blok

Jamba blokları iki sayıya göre katmanları birbirine bağlar:

- `l`Jamba kullanıyor `l = 8`, yani her 7 Mamba katmanı için 1 Transformer katmanı (7 Mamba + 1 Dikkat = grup başına 8 katman).
- `e`Jamba kullanıyor.`e = 2`Bu da diğer katmanların her birinde MoE geçerli olduğu anlamına geliyor.

Bir blok içindeki katman dizisi:

```
M  M  M  M  M  M  M  A    (7 Mamba + 1 Attention)
|  M  |  M  |  M  |  M    (where | marks MoE applied)
```

Her Jamba blok 8 katmandır. 4 blok derinlikte (toplam 32 kat), 28 Mamba ve 4 Dikkat katmanı elde ediyorsunuz.

### Neden 1:7 oranı

AI21 ablasiyonları çalıştı: Dikkat-Mamba oranı, uzun bağlam değerlendirmelerinde en iyi karmaşıklık per parametreler ve bağlam içi hatırlama sağlar?

- Çok fazla dikkat (1:1): kalite artıyor ama hafıza ve hız azalıyor.
- Çok az dikkat (1:15): hafızası büyük ama bağlamda geri almak başarısız.
- - Merhaba. 1: 7 veya 1: 8.

İçgüdü: Transformer katmanları tam hatırlama ve durum izlemeyi halleder. Mamba katmanları ucuz işlemlerin büyük kısmını haller.

### Konum kodlaması

Mamba katmanları kendileri konum farkındadır (tekrarlanma yoluyla). Mamba tabanlı orijinal hibridlerde dikkat katmanları RoPE  kullanmadı. SSM katmanları konum bilgileri sağladı. Jamba 1.5 daha uzun bağlam genellemesi için dikkat katmanlarına RoPE ekler.

### Hatırlama bütçesi

Jamba-1 şekli için (32 katman: 28 Mamba + 4 Dikkat, gizlenmiş 4096, 32 dikkat başlığı):

- KV önbelleği (yalnızca dikkat katmanları): `2 * 4 * 32 * 128 * 256k * 2 = 8.4 GB`Sadece 4 dikkat katmanı katkı sağlar.
- SSM durumu: `28 * hidden * state_size`Bu, bir katman için sabit bir boyut, dizilerin uzunluğu ile ölçeklenmemektedir.`28 * 4096 * 16 * 2 = 3.7 MB`- Toplam.

32 katlı saf bir Transformer ile karşılaştırın, aynı gizli, 32 başlı tam MHA:`2 * 32 * 32 * 128 * 256k * 2 = 128 GB`KV önbelleğinin 8 kat azalma.`2 * 32 * 8 * 128 * 256k * 2 = 32 GB`Jamba'nın 1:7 hibrid 16 GB'lı haliyle 2 kat daha küçük.

AI21'in "tek 80GB GPU'da 256k bağlam" olarak anlamı budur. "Tüm MHA saf bir Transformer'ın KV önbelleği uyum sağlamaz; hatta bir GQA temel hattı ağırlıklar ve etkinleştirmeler için yer bırakmaz; Jamba'nın yapması gerekir.

### Mamba-3: 2026'da saf SSM başlangıç çizgisi

Mamba-3 (ICLR 2026, arXiv:2603.15569) saf SSM tarafında üç yenilik sunar:

1. **Exponential-trapezoidal discretization.**Mamba-2'deki Euler yöntemi diskretleştirmesini daha ifade edici bir tekrarla değiştirir.`x_t`- Evet .

2. **Complex-valued state update.**Mamba-3'ün karmaşık değerleri 'e eşittir. Bu durum üzerinde veri bağımlı bir rotary gömülme eşittir. Bu, önceki gerçek değerli basitleştirmelerin maliyetinin bulunduğu devlet izleme yeteneklerini geri getirir.

3. **Multi-input multi-output (MIMO) projections.**Karakteristikleri açısından skalar projeksiyonlar yerine, matris değerli projeksiyonlar kullanın. Dekodlama gecikmesini arttırmadan modellerleme gücünü ve sonucu zaman donanım kullanımını geliştirir.

1.5B parametrelerinde, Mamba-3 Gated DeltaNet'e göre ortalama aşağı akıntı doğruluğunu 0.6 puan arttırır; MIMO varianti toplam 1.8 puan kazanç için 1.2 daha ekler. Aynı durum boyutunda, Mamba-3 Mamba-2 ile yarı durumla eşleşir.

Mamba-3 henüz ölçekli bir üretim hibridinde gönderilmiyor  ama bir sonraki Jamba sınıfı modelinin SSM tarafı için açık bir aday.

### Bir hibridin ne zaman bulunması gerekiyor

Hibritler kazanırsa:

- Koneks, saf Transformer KV önbelleğinin ağrılı hale gelmesi için yeterince uzun (64k+).
- Görevler kısa mesafe yapısını (SSM için iyi) uzun mesafe geri çağırma ile (Transformer ihtiyaçları) karıştırır.
- Tek GPU bellek bütçelerinde Transformer KV önbelleğinin kendi başına yerleşmeyeceği yerlerde dağıtmak istiyorsun.

Hibritler kaybederken:

- Kontext kısa (16k'dan daha düşük). SSM üstü harcanır; saf Transformer iyi.
- Görevler her yerde dikkat gerektirir ( derin düşünme, çok belgeli çapraz referans).
- Trisyonlarca parametrelik sınır modellerine kadar uzanıyorsunuz. Pure-Transformer + MLA + MoE (DeepSeek-V3 tarzı) şu anda kapasite yarışında kazandı.

### Rekabetçi manzarası

| Model | Family | Scale | Unique claim |
|-------|--------|------|-------------|
| Mamba-2 | pure SSM | 3B | linear time, constant memory |
| Jamba | hybrid | 52B/12B | 256k on 80GB |
| Jamba 1.5 Large | hybrid | 398B/94B | enterprise-grade long-context |
| Mamba-3 | pure SSM | 1.5B (paper) | state-tracking restored |
| DeepSeek-V3 | pure Transformer + MoE | 671B/37B | frontier capability |

2026 manzarası: saf Transformer MoE sınırda egemenlik gösterir, ancak hibritler 256k+ bağlamlı niş'e sahiptir. Mamba-3'ün devlet izleme kazanmaları, sonraki nesilde hibrit oranları daha düşük (daha fazla SSM, daha az dikkat) itebilir.


> **【拓展：Mamba/SSM 的优势与局限】**Mamba 推理复杂度 O(1),远优于 Transformer's O(n) ・・・ ancak SSM 在精确回溯任务上弱于注意力。Jamba 混合策略是折中方案。


## Çerçeveyi kullanın.
```figure
swiglu-ffn
```

## Kullan

`code/main.py`SSM-Transformer oranı ve gizli boyut / katman sayımı yapılandırmasını göz önüne alarak, hesaplar:

- KV önbelleği hedef bağlamda.
- SSM durum hafızası.
- Bir dizi model şekli için bağlam N'de toplam bellek.

Hesap makinesi:

- Pure-Transformer baseline (KV cache N ile büyüyor).
- Jamba tarzı 1:7 hibrid.
- Saf SSM (KV önbelleği yok).

Sayılar yayınlanmış şekiller için Jamba-1 ve Jamba-1.5 makalelerinden doğrudan alınmıştır ve hipotetik çeşitler için ekstrapolasyon yapılmıştır.

Gerçek bir yerleşim için entegrasyon düşünceleri:

- Çoğu üretim sonuç sunucuları (vLLM, SGLang) Jamba ve Mamba'yı destekler.
- 256k bağlamında, Jamba'nın bellek avantajı eşzamanlı talep çıkışında görünür. Aynı VRAM'da Transformer dizilerinden daha fazla Jamba dizisini yerleştiriyorsunuz.
- Mamba-3 bağımsız bir model olarak henüz üretimde gönderilmiyor  araştırma ön gösterisi 1.5B.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-hybrid-picker.md`. İş yükü özellikleri (koneks uzunluğu profil, görev karışımı, bellek bütçesi) göz önüne alındığında, hafıza ve kalite karşılığı konusunda açık bir mantıkla saf bir Transformer, Jamba tarzı hibrid ve saf bir SSM arasında tavsiye edilir.

> 本课产 出 `outputs/skill-hybrid-picker.md` Görev yükleme kuralları (→ 下文 长度配置、任务组合、内存预算), saf Transformer、Jamba 风格混合与纯 SSM arasında önerilmektedir ve 内存 ve kalite ağırlığı konusunda net bir önerme sunmaktadır.

## Egzersizler.

1. Çık .`code/main.py`KV önbelleğini 32 katlı saf Transformer için 256k bağlamda hesaplamak için (goymuş 4096, 32 baş) ve aynı şekildeki Jamba-1 hibrid için. AI21 kağıdı iddia ettiği ~ 8x hafıza azaltımı doğrulayın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`計算 32 層純變壓器 (Hidden 4096,32 头) 及相同形的Jamba-1 混合模型在 256K 上下文下 KV 缓存──验证 AI21 论文声称的约8倍内存减少──

2. Hesap makinesi 1:3 hibrid (4 Mamba: 1 Dikkat) ve 1:15 hibrid (14 Mamba: 1 Dikkat) modeline göre değiştirilsin.
   Çinçe Çevirimi Çevirisi: Modifié calculateur建模 1:3 混合(4 Mamba: 1 Dikkat) ve 1:15 混合(14 Mamba: 1 Dikkat) ・・・ KV 缓存与比率的关系──在什么比率下 KV 缓存等于 SSM 状态内存?

3. Jamba makalesinin 3. bölümünü okuyun (arXiv:2403.19887). AI21'in Mamba-2'nin daha hızlı olmasına rağmen Mamba-2'den ziyade Mamba-1'yi neden kullandığını açıklayın.
   Çinçe Çevirimi Çevirisi: Jamba'nın 3. bölümünü okuyun.

4. Jamba 1.5 Large'de MoE-her-diğer katmanın üstteki parametrelerini hesaplayın (398B toplam, 94B aktif).
   Çin dilinde:计算 Jamba 1.5 Large(398B 总计,94B 激活) 中每隔一层 MoE 的参数开销──将激活率与DeepSeek-V3(37B/671B)

5. Mamba-3 makalesinin 3. bölümünü okuyun (arXiv:2603.15569). Karmaşık değerli bir durum güncelleme neden veri bağımlı bir rotary embed ile eşdeğer olduğunu üç cümleyle açıklayın. Cevabı Fase 7 · Ders 04'ün RoPE türevine bağlayın.
   Çinçe çevirisi: Mamba-3'yi okuyun. 3. bölüm. Üç cümleyle açıklayın.

## Anahtar Şartlar .

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|------------------------|---------|
| State space model (SSM) | "Recurrence with a fixed state" | A layer with a learned recurrence `h_t = A h_{t-1} + B x_t`; constant memory per token | 状态空间模型，固定状态的递归层 |
| Selective SSM | "Mamba's trick" | Data-dependent A, B, C parameters that give the model gating-like selectivity at linear time | 选择性 SSM，数据依赖的参数实现门控 |
| Attention-to-Mamba ratio | "How many attention layers" | In Jamba, `l = 8` means 1 attention layer per 7 Mamba layers | 注意力与 Mamba 层比例，Jamba 用 1:7 |
| Jamba block | "The 8-layer group" | One attention + seven Mamba + MoE on alternate positions | Jamba 块，1 层注意力 + 7 层 Mamba + MoE |
| SSM state | "The hidden buffer" | Fixed-size per-layer state that replaces the KV cache for Mamba layers | SSM 状态，替代 Mamba 层 KV 缓存的固定大小状态 |
| 256k context | "Jamba's flagship number" | The sequence length Jamba-1 fits on a single 80GB GPU; pure Transformer cannot at that size | 256K 上下文，Jamba-1 在单张 80GB GPU 上的最大序列长度 |
| Mamba-3 | "2026 pure SSM" | Current-best pure-SSM architecture with complex state + MIMO; the baseline hybrids rebuild around | Mamba-3，2026 年最优纯 SSM 架构 |
| MIMO | "Multi-input multi-output" | Mamba-3 innovation using matrix-valued projections instead of scalar per-feature | MIMO，矩阵值投影替代标量投影 |
| Exponential-trapezoidal discretization | "Mamba-3's recurrence" | More expressive recurrence that subsumes Mamba-2's Euler-method discretization | 指数梯形离散化，更高效的递归表达 |
| Hybrid architecture | "Mix attention and SSM" | Any model that interleaves Transformer and SSM layers; Jamba is the production archetype | 混合架构，交替使用 Transformer 和 SSM 层 |

## Daha fazla okumak

- [Lieber et al. — Jamba: A Hybrid Transformer-Mamba Language Model (arXiv:2403.19887)](https://arxiv.org/abs/2403.19887) orijinal Jamba kağıdı, oran ablations, 256k bağlam iddiası
- [AI21 — Jamba 1.5: Hybrid Transformer-Mamba at Scale (arXiv:2408.12570)](https://arxiv.org/abs/2408.12570) genişletilmiş aile, 398B/94B ve 12B/52B açıklamalar
- [Gu, Dao — Mamba: Linear-Time Sequence Modeling with Selective State Spaces (arXiv:2312.00752)](https://arxiv.org/abs/2312.00752) Jamba'nın seçkin SSM kağıdı
- [Dao, Gu — Mamba-2 (arXiv:2405.21060)](https://arxiv.org/abs/2405.21060) basitleştirilmiş yapılandırılmış devlet- uzay varisi
- [Lahoti et al. — Mamba-3 (arXiv:2603.15569, ICLR 2026)](https://arxiv.org/abs/2603.15569) karmaşık değerli devlet, MIMO, 2026 saf SSM sınır
- [Gu et al. — Efficiently Modeling Long Sequences with Structured State Spaces (arXiv:2111.00396)](https://arxiv.org/abs/2111.00396) S4 makalesi, MSS soy hattının LLM için başlangıç noktası
