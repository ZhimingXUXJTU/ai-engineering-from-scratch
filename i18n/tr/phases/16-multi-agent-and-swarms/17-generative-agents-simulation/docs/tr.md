# Genereatif Ajanlar ve Yenilik Simülasyonu .

> Park et al. 2023 (UIST '23, arXiv:2304.03442) nüfuslu **Smallville**, 25 ajanlı bir kum kutusu, üç bölümlü bir mimari ile:**memory stream**(doğal dil kayıtları),**reflection**(Ajantin kendi akışında ürettiği yüksek düzeyde sentezler) ve**plan**(gündüz düzeyinde davranış, sonra alt planlar). Önemli sonuç Sevgililer Günü partisi ortaya çıktı: bir ajan daha fazla senaryo yazmadan "sevgililer Günü partisi vermek istiyor" ile tohumlandı, nüfus arasında yayılmış davetiye üretti, koordinasyon tarihleri ve parti 24 ajanın bilgisi olmadan başlattığı bir parti oldu. Ablationlar, inançlılık için üç bileşenin de gerekli olduğunu göstermektedir. Belgelemiş hatalar, yer norm hataları (kapalı mağazalara girmek, tek kişilik banyo paylaşmak) dir. Bu, 2026'da ajan simülasyonları ve çoklu ajan sosyal değerlendirme için referans mimarisi.

> **【中文解读】**Bu bölümde yaratılmış bir ajanı simgeleyen 25 AI ajanı, bir sanal toplulukta kendi kendine yaşamı için Stanford'un küçük kasaba deneyimi ile tanıştı.

> **【拓展：generative agents simulation→具体应用】**斯坦福'un üretimi  deney  Park et al., 2023) 25 AI ajanı oluşturdu. Bu deney LLM ajanının ortaya çıkmış sosyal davranışlar geliştirebileceğini kanıtladı.


**Type:** Learn + Build | **类型:** 学习 + 构建
**Languages:** Python (stdlib) | **语言:** Python（标准库）
**Prerequisites:** Phase 16 · 04 (Primitive Model), Phase 16 · 13 (Shared Memory) | **前置知识:** Phase 16 · 04（原语模型），Phase 16 · 13（共享内存）

>  **【前置】**Öğrenci bölümünün ilk aşaması: 16·04(şihni dil)、16·13(şebekârlık 內存)、11·04(Embeddings, memories流检索用)。Stanford Smallville = 多 Agent 涌现社会行为的里程碑实验。
>  **【类比】**Smallville = "AI 版模拟人生"──25 个 AI 居民各有生活、记忆、计划──情人节派对奇迹:一个代理 想办派对→邀请传开→其他人调整日程→派对真发生全是涌现,无脚本──三件套:memory stream(经历日志) + refleksiyon(自我总结) + plan(日计划)──三者缺一不可, 删除任一代理 行为变得不可信──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Sorunlar sorunun giriş

Çoğu çoklu ajan sistemi sıkı bir şekilde yazılmış ekiplerdir: planlama planları, kodlayıcı kodları, inceleyiciler incelemeleri. Bu iyi tanımlanmış görevler için çalışır. Ajanların hafızası, öncelikleri ve açık bir dünyası olduğunda ortaya çıkan ortaya çıkan, yazılmamış davranışları yakalamaz. Araştırma, toplumsal simülasyon ve giderek daha fazla oyun AI'nin bu ikinci türüne ihtiyacı vardır.

> Çoğu Agent  sistemi, sıkı bir yazı kitlesidir: planlayıcı planlama, kodlamacı kodlama, değerlendirmen değerlendirmesi. Bu, belirgin görevlerin tanımlanması için geçerlidir. Ama Agent olarak algılayamaz. Hatırlama, öncelik ve açık dünya zamanında ortaya çıkan ‒ yazı kitlesiz davranışlar. Araştırma, sosyal simülasyon ve gittikçe daha fazla oyun AI'nin ikinci türü gerekir.

Park 2023'e kadar en iyi ajan simülasyonları ufak senaryo takipçileriydi; bundan sonra, örnekteki açık dünyalarda üreticiler için varsayılandır. 2026'da bir ajan simülasyonu oluşturursanız, ya Smallville'in üç bileşenini kullanıyorsunuz ya da açıkça neden olmadığınızı haklı çıkarıyorsunuz.

> Smallville yapısı bu tür bir temel noktadır. Park 2023'e kadar en iyi Agent 模拟は浅層の脚本フォローヤー; sonra, bu model açık dünyada üretilen Agent'in öntanımlı haline geldi. Eğer 2026 yılında Agent 模拟 inşa ederseniz, Smallville'in üç bileşeni kullanmak istiyorsanız, neden kullanılmadığını açıkça açıklayın.

## Konsept merkezi konsept

### Üç bileşen

**Memory stream.**Her giriş bir zaman damgası, bir tür, bir açıklama (doğal dil) ve elde edilen metadata sahiptir:**recency**- Evet .**importance**(Agent tarafından 1-10 değerlendirilmiş) ve **relevance**(kurrent sorguya benzerlik gösterir).

> **记忆流。**Bir ek gözlem, eylem, düşünce ve plan günlüğü. Her bir yazı zamanlı, türlü ve açıklamalar içerir.**时效性**- Evet.**重要性**(Agent 自评 1-10)**相关性**(Bugün sorguların öyüstrü benzerliği)

```
[2026-02-14 09:12:03] observation: Isabella Rodriguez asked me if I like jazz
[2026-02-14 09:14:22] reflection:   I enjoy long conversations about music
[2026-02-14 10:05:00] plan:         Attend Isabella's Valentine's Day party tonight
```

Hatıra kurtarma üç puanı birleştirir:`score = w_recency * e^(-decay * age) + w_importance * importance + w_relevance * cos_sim`Top-k girişleri mevcut çağrıda girer.

**Reflection.**Periodik olarak (her N anısı veya önemli olaylarda), ajan son anılardan daha yüksek sıradaki sentezler üretir. Yansıma girişleri akıma geri döner ve diğer hafızayla aynı şekilde geri alınır. Bu şekilde ajanlar "anlamalar" oluşturur  mimarinin uzun vadeli inançlara eşdeğeri.

> **反思。**定期(每 N 条记忆或在重要事件时),Agent, yakın zamanda hatırlananlardan yüksek aşama bir bütün oluşturur.

**Plan.**Top-down parçalanma. Önce gün düzeyde planı geniş vuruşlarda ("işe git, Klaus ile akşam yemeği yiyin"). Sonra saat düzeyde planlar. Sonra eylem düzeyde planlar. Planlar gözden geçirilebilir: bir gözlem bir plana aykırı olduğunda, ajan etkilenen bölümü yeniden planlar.

> **计划。**Öncelikle, kaba bir gün seviyesinin planı, sonra da küçük bir saat seviyesinin planı, sonra da hareket seviyesinin planı, öncelikle, planın anlaşmazlıkları sırasında, yeni planların yeniden düzenlenmesinin etkilenen bir kısmı.

### Neden üçü de önemli (bırak)

Park et al. gözlem, düşünme ve planlama her birini düşüren ablationlar çalıştı.

> Park  et al. , bir giderme deneyi yaptı, ayrıca gözlem, düşünce ve planı yok etti.

- - Hayır .**observation**Ajan bağlamı kaçırıyor ve eski inançlara göre hareket ediyor.
  Çeviri: yok**观察**,Agent 缺失上下文, geçmiş inanç hareketine dayanarak.
- - Hayır .**reflection**ajan daha yüksek düzeyde inançlar oluşturabilir; etkileşimler yüzeysel kalır.
  Çeviri: yok**反思**,Agent                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
- - Hayır .**plan**Davranışlar reaktif gürültü haline gelir; hedefler dağılar.
  Çeviri: yok**计划**, davranışlar reaksiyon sesine dönüşür; hedef giderek yayılır.

İnsan değerlendiricilerinden alınan inanç puanları, üçüyle de en yüksek; herhangi birini düşürmek ölçülebilir bir gerileme üretir.

> İnsan değerlendiricilerinin güvenilirlik oranı en yüksek; ölçülebilir bir geri dönüşün herhangi birinden kurtulmak için.

### Sevgililer Günü'nün ortaya çıkması

Bir ajan, Isabella Rodriguez, "14 Şubat'ta saat 5'te Hobbs Cafe'de Sevgililer Günü partisi vermek istiyor" hedefiyle tohumlanmış.

> Bir ajan, Isabella Rodriguez, "İşime yerleştirildi" düşüncesi 2 14 gün öğleden sonra 5'te Hobbs Cafe'de bir aşk kutlaması düzenliyor. Diğer 24 ajan böyle bir tohum almadı.

1. Isabella'nın planı insanları davet etmektir.
   Çinçe Çevirimiçi:İsabella'nın planı insanları davet etmekti.
2. Her davet komşunun hafızasında bir gözlem haline gelir.
   Çinçe Çevirisi: Her davet komşu hatırası akımında bir gözlemci olmaya davet edilir.
3. Komşunun düşüncesi inançlara yol açar: "Isabella parti veriyor".
   Çinçe Çevirisi: Komşunun düşüncesi: "Isabella'nın bir parti yapması gerekiyor".
4. Komşunun planı "14 Şubat'ta partiye katılmak" içermektedir.
   Çinçe Çevirisi: Nezakörlerin planı纳入"2月14日参加派对"―
5. Komşular diğer komşulara haber verirler.
   Çinçe Çevirimiçi: komşu diğer komşularına anlatıyor.
6. 14 Şubat akşam 5'te birkaç ajan Hobbs Cafe'de toplanıyor.
   Çin Çeviri: 2月 14日下午 5 点, birkaç ajan 汇聚到霍布斯咖啡馆──

Bu teknik anlamda ortaya çıkış: sistem düzeyinde davranış (bir parti) merkezi bir orkestrasyoncu olmadan yerel etkileşimlerden (iki taraflı davetler + bireysel planlama) ortaya çıktı.

> Bu, teknik anlamda ortaya çıkan bir sistemlik davranışdır.

### Belgelemiş başarısızlık modları

Park et al. açıkça belge:

> Park  et al. net olarak kaydetti:

- **Spatial norm errors.**Ajanlar kapalı mağazalara giriyorlar. Ajanlar aynı tek kişilik tuvaletini kullanmaya çalışıyorlar. Ajanlar yemek için tasarlanmamış odalarda yemek yiyorlar.
  Çeviri:**空间规范错误。**Ajan 走进关闭的商店──Ajan 试图使用同一个人浴室──Ajan 在非用餐室用餐──模型不能仅从环境推断社会物理规范──
- **Memory overflow.**Derin simülasyon çalışmalar hafıza kurtarma maliyetinin artmasına neden olur. Pratik bir çözüm: periyodik hafıza sıkıştırılması (cümle ve kesme) ve düşük önemli girişlerde bozulma.
  Çeviri:**记忆溢出。**Derinlik modeli çalışması, hafıza araması maliyetinin artmasına neden olmuştur.
- **Reflection hallucination.**Refleksyonlar hafıza akımında bulunmayan ilişkileri icat edebilir. Yumuşaklaştırma: Refleksyon isteklerinde kaynak hafıza kimliklerini ekle ve kurtarma zamanında doğrulayın.
  Çeviri:**反思幻觉。**Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıtlama: Anıt: An An An An An An An An An Anıt

Bunlar üretim ile ilgili hata modlarıdır: 2026 ajan simülasyonu onları miras alır.

> Bunlar üretim ile ilgili başarısızlık modudur: 2026 yılının herhangi bir ajanı onları miras alacak.

### Üç bileşenli uygulama kuralları

1. **Memory is append-only.**Hiç bir hafıza girişini mutasyona sokmayın.
   Çeviri:**记忆只追加。**永遠不修改記憶条目──更正是新条目──
2. **Importance scores are cheap.**Yazma zamanı 1-10 değerini değerlendirmek için Yüksek Lisans Yüksek Lisansına arayın.
   Çeviri:**重要性分数是廉价的。**写入时调用 LLM 评分 1-10──缓存分数──
3. **Retrieval is ranked, not filtered.**Top-k kombinasyon puanı; sert filtreler kullanmayın (koneks kaybederler).
   Çeviri:**检索是排序的，不是过滤的。**按综合分数取 top-k; sert over                                                                                                                                                                                                                                                         
4. **Reflection runs periodically.**İşlenmemiş hafızaların öneminin toplamı bir eşiği (örneğin 150) aşırırken tetikleyici.
   Çeviri:**反思定期运行。**Bu, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden önce, bir anlama gelmeden, bir anlama gelmeden, bir anlama gelmeden, bir anlama gelmeden, bir anlama gelmeden, bir anlama gelmeden, bir anlama gelmeden, bir anlama gelmeden, bir anlama gelmeden, bir anlama gelmeden, bir anlama gelmeden, bir anlama gelmeden, bir anlama gelir.
5. **Plans are revisable.**Yeni bir gözlem bir plana aykırı olduğunda, sadece etkilenen bölümü, tüm planı değil, yeniden oluşturun.
   Çeviri:**计划可修订。**Yeni gözlem ile planın çelişkili olduğu zaman, sadece etkilenen kısım yeniden üretilir, tüm plan değil.

### Smallville'den öte üreticiler

2024-2026 takip literatürü mimarlığı genişletiyor:

> 2024-2026 yılları için sonraki yayınlar bu yapı genişletiyor:

- **Multi-agent social simulation for policy / market research.**Smallville gibi nüfuslar, kullanıcı davranışlarını özelliklere karşılık olarak simüle eder.
  Çeviri:**用于政策/市场研究的多 Agent 社会模拟。**类似Smalville 的人群模拟用户对功能的响应──比 A/B 测试更快;准确性有争议──
- **NPC AI for games.**Smallville ajanları ile oynanan rol oynayan oyunlar senaryoda görevlerin yerine yeni hikayeler üretir.
  Çeviri:**游戏 NPC AI。**Smallville Ajan'ın rolü, bir hikaye oyunu değil, bir film oyunu.
- **Generative-agent evaluation benchmarks.**Görev doğruluğu yerine, metrik uzun süreler boyunca davranışların güvenilirliği + tutarlılığı haline gelir.
  Çeviri:**生成式 Agent 评估基准。**Görev doğruluğu oranı, uzun süreli çalışmanın güvenilirliği ve davranışın devamlılığı için belirtilir.

Arsitektur referanstır. Genişlemeler değişken bileşenler (hüye için vektör depolama, geri alma artıran yansıma, nörosimbolik plan) ama üç bölümlü yapıyı korur.

> Bu yapı bir referansdır. Bu yapı, bir yapı olarak kullanılır.

### Bu neden çoklu ajan mühendisliği için önemli

Smallville, çoklu ajanların ortaya çıkmasının bileşenler doğru olduğunda ucuz olduğunu kavramın kanıtıdır. Mimarlık şimdi açık kaynaklı modellerde çoğaltıldı (küçük LLM'ler, keskin değil, şık bir şekilde güvenilirliğini kaybediyor).**emergent social behavior**Bu şekli kullanır.**tight task execution**Bu aşamada daha önceki yönetici / rol / ilkeler kalıplarını kullanıyor.

> Smallville, bir konsept testidir, bileşen doğru olduğunda, çoklu ajanın ortaya çıkması ucuz olduğunu gösterir. Bu yapı açık kaynaklı bir modelde ortaya çıkmıştır.**涌现社会行为**Bu tür bir biçim kullanılıyor.**紧密任务执行**Sistemler bu aşamada erken dönemlerde gözlemci/karakter/origin language model kullanılmıştır.

## Yapın.
```figure
a5-memory-reflection
```

## Yapın

`code/main.py`Stdlib Python'da üç bileşenini scripted agent politikaları ile uyguluyor (gerçek LLM yok).

- `MemoryStream` Yenilik/Önem/Alaylılık Kayıtları ile sadece ekleme kayıtları.
  Çeviri:`MemoryStream` 带时效性/重要性/相关性检索的仅额外日志──
- `reflect(stream)` Son zamanlarda önemli anılar üzerinde yazılı bir düşünce.
  Çeviri:`reflect` Yakın zamanda çok önemli olan hafızaların yazılılığı için düşünceler
- `plan(agent_state)` Günlük ve saatlik düzeyde güncel inançlara dayanan planlar.
  Çeviri:`plan`  Gün ve saat sınıfı planı temelinde mevcut inançlar
- Scenari: 5 ajan. 1 ajan saat 5'te "eğlenme partisi" ile başlar. Simülasyonda tikler, daveti yayılır ve ajanlar bir araya gelir.
  Çinçe Çevirisi: Çeviri: 5 个 代理 ・ 代理 1 以"下午5 点办派对"开始──在模拟的时间步中,邀请传播, 代理 汇聚──

Çık:

```
python3 code/main.py
```

Beklenen çıkış: tik-tik iz. Son tik'e kadar, 5 ajanın en az 3'ü partiyi planlarında gösterir ve parti konumunda bir araya gelirler. Tek tohum hiçbir orkestrasyoncu olmadan koordine edilmiş bir gelişi üretir.

> 预期输出:逐步跟踪──5 ajanın en az 3'ü, planda gösterilen partide toplandılar, parti yerlerinde toplandılar──

## Kullanın Kullanın

`outputs/skill-simulation-designer.md`Bir jeneratif ajan simülasyonu tasarlıyor: ajan sayısı, hafıza şeması, yansıma kadansı, plan ufku ve değerlendirme metrikleri.

> `outputs/skill-simulation-designer.md`设计一个生成式 Agent 模拟:Agent 数量、记忆模式、反思频率、计划范围和评估标志──

## Gönderin.

Üretim simülasyonları için kurallar:

- **Memory is the database.**Gerçek bir mağazayı (vector DB, Postgres) ölçekle seçin.
  Çeviri:**记忆是数据库。**Ölçüsünde gerçek depoyu seçmek için, DB ∼ Postgres ∼内存 içindeki standartlar sadece orijinal türde kullanılır.
- **Log the retrieval trace.**Her eylem için, onu yönlendiren en üst-k anıları kaydet.
  Çeviri:**记录检索轨迹。**Her hareket için, kayıt onu yönlendirir. Bu senin kontrol yeteneğin.
- **Budget per-agent tokens.**Her ajanın tik başına alın + refleks + planı O(k) LLM çağrılarıdır. N ajan × T tik × tik başına çağrılar bütçenizi küçültüyor.
  Çeviri:**预算每 Agent token。**Her Ajan Her Zaman Adımı Kontrol + Düşünce + Planı O(k) İkinci LLM 调用──N 个 Ajan × T 个时间步 ?? × 每时间步 ?? 调用数可能让你的预算相形见──
- **Compact memory periodically.**Düşük önemli yazıları özetleyip biç.
  Çeviri:**定期压缩记忆。**Özet ve inceleme öneminin az olması için ayrıntılar değil, tasarımı tasarımıdır.
- **Detect spatial / social norm violations**Mimarlık onları öğrenmez.
  Çeviri:**显式检测空间/社会规范违规。**Arşivler onları öğrenmeyecek.

## Egzersizler.

1. Çık .`code/main.py`3+ ajanın partide toplandığını onaylayın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ 3 +Agent 汇聚到派对───Agent 增至10 涌现还会发生吗?
2. Yönlendirme adımını kaldırın. Davranış nasıl görünüyor? Park 2023'te bulunan ablasyon bulgularına haritan.
   Çinçe Çevirimiçi:移除反思步骤──行为看起来如何?映射到公園 2023 的消融发现──
3. Rekabetçi bir hedef oluşturun ("Klaus akşam 5'te bir araştırma konuşması yapmak istiyor").
   Çinçe Çevirimi: Introduction to a competition's seed goal ((("Klaus 想在下午5 点做研究报告") ").
4. Yer kısıtlamaları ekleyin: Hobbs Cafe en fazla 4 ajanı tutabilir.
   Çin Çeviri: Add Space约束: Hobbs Cafe 最多容纳 4 代理──模拟能优雅地处理溢出,还是会碰到"单人浴室"失败模式吗?
5. Park et al. (arXiv:2304.03442) Bölüm 6 (Çok gelişmiş davranış deneyleri).
   Çine dilinde yapılan bir çeviri:Park 等人 (ArXiv:2304.03442) 6. bölüm: Çekimsel davranış deneyimi.

## Anahtar Terimler

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Memory stream / 记忆流 | "The agent's diary" / "Agent 的日记" | Append-only log of observations, actions, reflections, plans. / 观察、行动、反思、计划的只追加日志。 |
| Recency / 时效性 | "How new is the memory" / "记忆有多新" | Exponential-decay score by age. / 按年龄的指数衰减分数。 |
| Importance / 重要性 | "How much does the agent care" / "Agent 有多在意" | Self-rated 1-10 at write time. Cached. / 写入时自评 1-10。已缓存。 |
| Relevance / 相关性 | "How related to the current query" / "与当前查询有多相关" | Cosine similarity (embedding-based). / 余弦相似度（基于嵌入）。 |
| Reflection / 反思 | "Higher-order belief" / "高阶信念" | Synthesis generated from recent memories, re-ingested as a new memory. / 从最近记忆生成的综合，作为新记忆重新摄入。 |
| Plan / 计划 | "Day/hour/action decomposition" / "日/小时/动作分解" | Top-down plan tree. Revisable when observations contradict. / 自顶向下计划树。观察矛盾时可修订。 |
| Smallville / 小镇 | "Park 2023's sandbox" / "Park 2023 的沙盒" | 25-agent simulation that produced the Valentine's Day emergence. / 25 个 Agent 的模拟，产生了情人节涌现。 |
| Believability / 可信度 | "The quality metric" / "质量指标" | Human-rater score for whether behavior seems like a plausible agent. / 人类评分者对行为是否像合理 Agent 的评分。 |

## Daha fazla okumak

- [Park et al. — Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) Referans mimarisi
- [UIST '23 paper page](https://dl.acm.org/doi/10.1145/3586183.3606763) Yayınlama yeri
- [Smallville code release](https://github.com/joonspk-research/generative_agents) Referans Python uygulaması
- [Hayes-Roth 1985 — A Blackboard Architecture for Control](https://www.sciencedirect.com/science/article/abs/pii/0004370285900639) Yapılandırılmış hafıza ajanları için önceden kullanılan sanat
