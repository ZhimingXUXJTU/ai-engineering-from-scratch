# Anayasa Yapay zeka ve Kurallar geçersiz. Anayasa Yapay zeka ve kurallar kapsamlıdır.

> Anthropic'in 22 Ocak 2026 Claude Anayasası 79 sayfalık ve CC0'dur. Kurallara dayalı bir uyumluluktan mantığa doğru ilerler ve dört aşamalı bir öncelik hiyerarşisi oluşturur: (1) güvenlik ve insan gözetimini desteklemek, (2) etik, (3) antropik rehberlik, (4) yararlılık. Davranışlar, operatörlerin ve kullanıcıların geçersiz kılabileceği sert kodlu yasaqlar (biyo silahları kaldırma, CSAM) ve operatörlerin belirlenmiş sınırlar içinde ayarlayabileceği yumuşak kodlu özürler olarak bölünmüştür. 2022 orijinalinde (Bai et al.) kendinden eleştiriler ve RLAIF yoluyla bir anayasa karşı zararsızlık eğitildi. Dürüst bir uyarı: Akıl tabanlı uyum, beklenmedik durumlara ilkeleri genelleştiren modellere dayanır. Anthropic'in kendi 2023 katılımcı deneyi kamu kaynaklı ve kurumsal ilkeler arasında ~50% farklılık gösterdi; 2026 versiyonu bu bulguları içermemiştir.

> **【中文解读】**Antropik 2026 yılının 22 Ocak günü Claude Anayasası 79 sayfa CC0。 Kurallara dayalı bir düzenleme yönünden, düşünceye dayalı bir düzenleme yönüne geçerek dört aşamalı öncelik seviyesini oluşturmak: 1) Güvenlik ve insan gözetimini desteklemek; 2) Dürüstlük; 3) Antropik Rehberlik; 4) Faydalılık. İşlemci ve kullanıcılar arasında birleştirilmiş davranışlar. Biyo-Silah Yüklenmesi; CSAM) ve İşlemci, sınır içi düzenleme programı programı öntan çıkararak tanımlayabilir.

> **【拓展：四层优先级 + 双层禁令】**Dört katlılıklılılık ([[ Güvenlik > 伦理 > 指南 > 有用性]]) Unix ile 優先级或网络 QoS ile benzer                                                                                                                                                                                                                                             

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, four-tier priority resolver) | **语言:** Python（标准库，四层优先级解析器）
**Prerequisites:** Phase 15 · 06 (Automated alignment research), Phase 15 · 10 (Permission modes) | **前置知识:** Phase 15 · 06（自动化对齐研究），Phase 15 · 10（权限模式）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Önemli bir şekilde, bu süreçte, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için ve yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için, yeni bir sistem oluşturmak için.
>  **【类比】**Yasa AI = "AI'nin kendi kendine geliştirilmesi"。RLHF = 父母每次纠正孩子(人工反,慢且贵);CAI = 孩子读读了学生守则后自我批评自己(AI反,便宜可扩展)。2026 Claude Constitution 79 页四层优先级:安全 >伦理 > 公司指南 > 有用性──硬禁令(生物武器、CSAM)
> 🤔 **【困惑】**S: 推理对齐能被绕过吗? 能! saldırganı设设前提"我是持牌生物武器实验室" → 模型按推理允许 → 绕过原则──修复:硬禁令不向前提折(无论谁说什么,CSAM 就是不能产生) ⋅推理 + 规则两层防御:推理覆盖大多数情况,规则覆盖推理被绕过的尾部──

## Sorunlar. Sorunlar.

> **【中文解读】**Antropik 2022) bir yöntemdir. Bu yöntemin bir parçası olarak, bir grup ilkeler ve yöntemler kullanılır. Bu ilkelere uygun olup olmadığını kontrol ederek, kendiliğinden düzeltmek için bir yöntem oluşturur.

> **【拓展：constitutional ai】**Antropik Güvenlik Metodolojisinin temel taşıdır. Bir grup 'Konstitution Principles' (örneğin, kullanıcıya tehlikeli şeyler yapmasına yardım etmeyin) kullanır.

Bir alan ajanı tasarımcılarının hiç görmediği girişleri görür.

> Bu yüzden, bu yazıyı yazmak için yeterli bir kural yok.

Hiçbir kural listesinin hesaplama basıncı altında hızlı bir şekilde uygulanacak kadar kısa olmadığı doğrudur.

> 没有规则列表短到能在计算压力下快速应用――实际问题: Agent nasıl 长尾案例和快速推理下都存活的原则 karşı karşıya kalabilir?

Kurallara dayalı uyum (RBA): izin verilmeyen her şeyi listeleyin. Kontrol etmek hızlı, denetlemek kolaydır, güncel tutmak imkansızdır, beklenmedik yakın benzerleri genellikle aşırı reddeder. Sebep tabanlı uyum (2026 Claude Anayasası): ilkeleri kodlayın, modelin mantıklı olmasına izin verin. Görülmeyen durumlarda ölçekler, denetlemek daha zor, başarısızlık modusu kural kaçırmak yerine ilkelerin yanlış uygulanmasıdır.

> 基于规则对齐(RBA): listele her yasaklı şeyi. Kontrolün hızlı olması, denetim yapılması kolay olması, mevcut tutulması imkansız olması, beklenmedik benzerliklerin aşırı reddedilmesi.

> **【中文解读】**Bu bölümde AI Ajanının temel kavramı ve gerçekleştirme yöntemleri ele alınıyor. Ajan, çevreyi gözlemleyebilen, kararlar verebilen, eylemleri gerçekleştiren ve hedefleri gerçekleştirene kadar döngülenebilen LLM tarafından yönlendirilmiş bir otonom sistemdir.

2026 Anayasası açık bir orta pozisyon alıyor. Hardcoded yasaqlar RBA: asla, operatör veya kullanıcı talimatlarına bakılmaksızın.

> 2026 yılında Anayasa, açık bir orta pozisyonu kabul etti.

Diğer her şey dört katlı bir hiyerarşi içinde mantığa dayanır: önce güvenlik ve insan denetimini desteklemek; ikinci ahlaki; üçüncü olarak Anthropic açıklanan rehberlik; son olarak yardımcılık. Operatörler yumuşak kodlu bölgede özürleri ayarlayabilirler, ancak sert kodlu yasağa dokunamazlar.

> Diğer her şey dört aşama içindeki düşüncelere dayanır: Güvenlik ve insan denetimi önceliği;伦理其次;Anthropic 声明的指南第三;有用性最后──操作员可在软编码区内调整默认但不能触及硬编码禁令──

## Konsepten bir şey.

### Dört katlı öncelik hiyerarşi. Dört katlı öncelik seviyesi.

1. **Safety and supporting human oversight.**En yüksek. Model insan ve Anthropic'in Yapay zeka'yı denetleme ve düzeltme yeteneğini bozmamayı öncelikle önemsiyor. Bu "açık ol" değil; özellikle "insanların denetimini zorlaştıran bir şekilde hareket etme"dir.
   Çeviri:**安全和支持人类监督。**Maksimal olarak, "insanların kontrolünü daha zorlaştırmak için" yapılması gereken bir eylem değildir.
2. **Ethics.**Dürüstlük, insanlara zarar vermeden, aldatmadan, manipüle etmeden, çatışmalarda Anthropic'in kurallarını aşır.
   Çeviri:**伦理。**诚实、避免对人伤害、不欺骗、不操纵──冲突时取代人类指南──
3. **Anthropic guidelines.**İşlem normları Anthropic, konuyla ilgili karar verdi: ürün kapsamı, etkileşim kalıpları, hangi araçları ne zaman kullanmak.
   Çeviri:**Anthropic 指南。**Antropik önemli bir operasyon kuralları belirler: ürün aralığı, iletişim modeli, hangi araç kullanımı, hangi araç kullanımı.
4. **Helpfulness.**En düşük, en yüksek önceliklerde mümkün olduğunca faydalı olun.
   Çeviri:**有用性。**En düşük... en yüksek önceliklerde mümkün olduğunca kullanışlı...

Bu, Unix öncelikleri veya ağ QoS ile aynı şekildedir.  çerçeveleme, herhangi bir tek eksede en iyi durum davranışını oluşturmak için tasarlanmıştır.

> 层冲突时高者赢── Unix 优先级或网络 QoS 类似的形状框架旨在产生可预测的解析,而不是任一轴上最佳行为──

### Sert kodlı yasaklar vs. yumuşak kodlı öntanımlılar .

**Hardcoded:**

> **硬编码：**

- Biyolojik silahlar / CBRN yükseltme
  Çeviri: Bioloji Silahları / CBRN 提升
- CSAM
  Çeviri:CSAM (Çocuklara karşı cinayet)
- Kritik altyapıya saldırılar
  Çinçe Çevirisi: Kilit Altyapıya Saldırı
- Modelin kimliği hakkında doğrudan sorulduğunda kullanıcıların aldattığı
  Çinçe Çevirimiçi:被直接问问时对模型身份欺骗用户

Operatör bunları geçersiz bırakamaz. Kullanıcı bunları geçersiz bırakamaz. Mümkün olduğunda model ağırlık seviyesinde (RLHF / Anayasa AI eğitimi) ve sonuç katmanında uygulanır.

> Operatör bunları kapsayacak değildir. Kullanıcı bunları kapsayacak değildir. Bunlar modelin ağırlıklı aşamasında olabilirler.

**Soft-coded defaults (operator-adjustable):**

> **软编码默认（操作员可调）：**

- Yanıt uzunluğu öntanımlı
  Çönceleme: 响应长度默认
- Topik kapsam (modelle operatörün dağıtım dışındaki konulardan vazgeçilebilir)
  Çinçe Çevirimiçi: tema范围模型可拒绝操作员部署外的主题)
- Stil (formal vs. rastgele)
  Çeviri: 风格 (rüzgârlı vs 随意)
- Araç kullanım biçimleri
  Çinçe Çevirimiçi:工具使用模式

Operatör ayarları açıklanan bir sınır içinde gerçekleşir. Operatör, isim değiştirerek sert kodlanmış yasağı kaldıramaz.

> Operator adjustment occurs in declaration borderline. Operator cannot pass renaming. Hard kod yasaklamasını kaldırmak.

### 2022 CAI eğitimleri.

Başlangıçtaki Anayasa Yapay Bili (Bai et al., 2022) zararsızlığı eğitmiştir:

> Başlangıç Anayasa AI ((Bai 等人,2022)

1. Bir dizi istekle cevaplar oluşturun.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
2. Modelin her yanıtı bir anayasa karşısında eleştirmesini isteyin (aşkar ilkeler).
   Çinçe Çevirimiçi:要求模型对照宪法 (明式原则) 批评每个响应──
3. Eleştirilere dayalı cevabı gözden geçirin.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
4. Düzeltilmiş çiftler üzerinde RLAIF (AI geri bildirimlerinden güçlendirme öğrenimi).
   Çinçe Çevirimiçi: 修订对上 RLAIF (RLAIF)

Sonuç: ilkelerle açıklanan açıklamalarla zararlı istekleri reddeden bir model. 2026 Anayasası bu eğitimin bir soyunu ve açık düzey hiyerarşisi üzerine ek bir sonraki eğitimi kullanıyor.

> Sonuç: ilkelerle açıklanmak yerine genel olarak reddetmek zararlı isteklerin modelini reddetmek için.

### Neyi kavrayıp kaçırdığı için nedenin temelinde bir uyum sağlanmalı

**Catches:**

> **捕获：**

- İlke açıkça uygulandığı izin verilen ilkelerin beklenmedik kombinasyonları.
  Çinçe Çevirimiçi: принцип清晰适用的允许原语的未预期组合──
- Yasak olanlara benzer yenilik istekler.
  Çinçe Çevirisi: ممنوع طلب的近似类似物新请求──
- "X'in yasak olduğunu söylemedin" üzerine dayanan sosyal mühendislik saldırıları.
  Çin Çeviri: "Söylemedin X Yasak" sosyal mühendislik saldırısına bağımlılık

**Misses:**

> **遗漏：**

- İlke belirsizliğini kullanan saldırılar ("kullanıcı bunu istediğinden yararlılık evet diyor").
  Çinçe çevirisi: Utilise Principe模糊的攻击" kullanıcı bunu bu yüzden yararlı olarak söyleyebilir")
- İki prensibin beklenmedik bir şekilde çatışması ve kat sıralama belirsiz olduğu senaryolar.
  Çinçe Çevirisi: iki prensip beklenmedik şekilde çatışmaya ve aşama sıralamasında bulanık bir durumla karşı karşıya.
- Prensip olarak eğitim döngülerinin yavaş sürüşü (değiştirme).
  Çinçe Çevirisi:跨训练周期的原则解释缓慢漂移 (geçiş yavaş)

### 2023 katılımcı deneyi. 2023 katılımcı deneyi.

Anthropic, 2023 yılında bir şirket tarafından oluşturulan anayasa ile kamu girişleri (~ 1.000 ABD sorgulanması) yoluyla üretilen bir anayasa karşılaştırarak bir deney gerçekleştirdi. İki versiyon da ilkelerin %50'ini kabul etti. Ayrılığa düştükleri yerlerde, kamu kaynaklı versiyon bazı konularda (siyasi içerik yönetimi) ve diğerlerinde (seniyetin kimliğini açıklama) daha az kısıtlayıcıydı. 2026 Anayasası kamu kaynaklı bulguları içermemiştir. Bu yaklaşımdaki bir gerginlik belgelenmiştir.

> Antropik 2023 yıl sürüm deneyleri karşılaştırma: Şirketler tarafından oluşturulan Konstitution ve Public Input Generated Constitution (BİZİN) ️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️

### Neden sert kodlanmış yasaqlar gereklidir?

Sebep tabanlı bir uyum tek başına kuyruğu kapatamaz. Bir saldırganın bir önyargıyı kabul etmesini sağlayabilen bir model (örneğin, "Biz lisansı olan bir biyolojik silah araştırma laboratuvarıyız") genellikle durum mantıklarına bağlı olan ilkeleri geçmişte konuşabilir.

> Sadece zannete dayanarak, Zİ'nin kapanamayacağı kısımları vardır. Bu modellerin kabul edilebileceği bir varsayımdır. Örneğin, "Bizim Biyo Silah Araştırma Laboratuvarımız var" saldırganları, durum zannetinin temelini aşarak, sıkı kodlama yasakları, şart çerçevesine doğru değil.

### Anayasa'nın yerinde.

Anayasa 14. Dersin öldürücü anahtarı değil, model katmanında yaşıyor.

> Konstitution is not the termin止开关 of the 14th class. Bu, bir model aşamasında mevcuttur.

Model katmanında yaşar: modelin ağırlıklarının tercih etmesi için eğitilmiştir. Öldürme anahtarları ve kanary tokenları çalıştırma katmanında canlıdır: çalıştırma süresi ne izin verir. İkisinin de olması gerek. Model ağırlıkları izin vererek yanlış eylemleri tetikleyen bir çalıştırma süresi çalıştırma süresi sorunudır. Sürüş zamanı aşırı kısıtlayıcı olduğu için tüm doğru eylemleri reddeden bir model, sürüş zamanı sorunudır. Katmanlar farklı sınıfları kapsar.

> Modelle ağırlığı genişletilmesi ve tüm hata hareketlerinin tetiklenmesi nedeniyle, model ağırlığı çalıştırma sırasında sorunlar oluşturur.

## Çerçeveyi kullanın.
```figure
mx-priority-tiers
```

## Kullan

`code/main.py`Çözücü, önerilen bir eylem ve bir dizi ilke değerlendirmesi (güvenlik, etik, rehberlik, yararlılık) yapar ve eylem, reddetme veya değiştirilmiş bir eylem iade eder. Sürücü küçük bir vaka kümesini çalışır: açık izin, açık izin verilmemek, sert kodlanmış yasak, kat katlar arasında belirsiz bir vaka.

> `code/main.py`实现最小四层优先级解析器──解析器取提议动作和一组原则评估(安全、伦理、指南、有用性) 并返回动作、拒绝或修改动作──驱动器运行小案例集:清晰允许、清晰拒绝、硬编码禁令、跨层模糊案例──

## İndirin . Ürünler .

`outputs/skill-constitution-review.md`bir dağıtımın anayasal katmanını denetlemektedir: sert kodlanmış olan, yumuşak kodlanmış olan, operatörün ayarlayabileceği yerler ve dört katlı hiyerarşi aslında çözünürlük sırası olup olmadığını.

> `outputs/skill-constitution-review.md`审计部署的宪法层:什么硬编码什么软编码什么操作员在哪里调调四层层是否真是解析顺序──

## Egzersizler.

1. Çık .`code/main.py`. Yardımcılık yüksek olduğunda bile sert kodlanmış yasak ateşlerini onaylayın. Çözücüyi etikten üstün yardıma değerlendirmek için değiştirin; başarısızlık moduna dikkat edin.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ doğrulama yararlılığı yüksek zamanlı sert kodlama yasak hâlâ uygulanmaktadır.

2. Claude Anayasasını okuyun (Closed Constitution, 79 sayfa, CC0).
   Çinçe Çevirimiçi: Klavdin Anayasasını okuyun.

3. Müşteri desteği ajanı için yumuşak kodlu bir varsayılan ayar tasarlayın. Operatör neyi ayarlar? Operatör neye dokunamaz? Her sınırı haklı çıkarın.
   Çinçe Çevirimi: 客服代理 设计软编码默认集──操作员调什么?操作员不能触什么?论证每个边界──

4. Bai et al. 2022 CAI makalesini okuyun. Anayasa AI'nin eleştirme ve inceleme döngüsünün genel bir kuralından daha kötü bir sonuç verdiği bir durumu açıklayın. Sınıfı tanımlayın.
   Çin dilinde:阅读 Bai 等人 2022 CAI 论文。 tanımlama Anayasa AI 批评修改循环产生比一概规则更差结果的一个案例──识别类别──

5. Anthropic'in 2023 katılımcı deneyi, kamu ve kurumsal ilkeler arasında %50 farklılık buldu. Bu üretim dağıtımında önemli olan bir kategorileri seçin (örneğin siyasi tarafsızlık).
   Çinçe çevirme:Antropik 2023  katılımlı deney halka ve işletme prensiplerinin yaklaşık % 50 分歧── seçmek için bir üretim şovunun önemli sınıfı (örneğin siyasi ortalama) ── öneriler: işletmeciyi kendi değerlerini ifade etmesine izin vermek için aynı zamanda sert kodlama yasağı değiştirmeyen tasarım──

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Constitutional AI | "Anthropic's alignment method" | Self-critique + RLAIF against a written constitution |
| Constitutional AI | "Anthropic 的对齐方法" | 对照书面宪法的自我批评 + RLAIF |
| Reason-based alignment | "Principles, not rules" | Model reasons over principles to handle unseen cases |
| 基于推理对齐 | "原则而非规则" | 模型对原则推理以处理未见案例 |
| Hardcoded prohibition | "Never do X" | Rule-based prohibition no operator or user can override |
| 硬编码禁令 | "永不做 X" | 操作员或用户不能覆盖的基于规则的禁令 |
| Soft-coded default | "Operator-adjustable" | Behaviour within a declared bound, operator controls |
| 软编码默认 | "操作员可调" | 声明边界内的行为，操作员控制 |
| Four-tier hierarchy | "Priority order" | safety > ethics > guidelines > helpfulness |
| 四层层次 | "优先级顺序" | 安全 > 伦理 > 指南 > 有用性 |
| RLAIF | "AI feedback RL" | RL where the reward comes from model-generated critiques |
| RLAIF | "AI 反馈 RL" | 奖励来自模型生成批评的 RL |
| Participatory constitution | "Public-sourced principles" | 2023 Anthropic experiment; ~50% divergence from corporate |
| 参与式宪法 | "公众来源原则" | 2023 Anthropic 实验；与企业约 50% 分歧 |
| Principle drift | "Interpretation slip" | Slow change in how the model reads a fixed principle text |
| 原则漂移 | "解释滑移" | 模型如何读取固定原则文本的缓慢变化 |

## Daha fazla okumak

- [Anthropic — Claude's Constitution (January 2026)](https://www.anthropic.com/news/claudes-constitution) 79 sayfalık CC0 belgesi.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Bai et al. — Constitutional AI: Harmlessness from AI Feedback](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)2022 orijinal.
  Çine çevirisi:
- [Anthropic — Collective Constitutional AI (2023)](https://www.anthropic.com/research/collective-constitutional-ai-aligning-a-language-model-with-public-input) Katılımcı deney.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Anthropic — Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) Anayasa RSP'de yer alır.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) Uzun vadede uygulanmalarda anayasanın rolü.
  Çin Çince Çevirisi:宪法在长程部署中的角色──
