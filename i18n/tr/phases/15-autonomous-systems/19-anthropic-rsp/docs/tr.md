# Antropik Sorumlu Ölçekleme Politikası v3.0

> RSP v3.0, 2023 politikasını değiştirerek 24 Şubat 2026 tarihinde yürürlüğe girdi. İki katlı azaltma: Anthropic'in tek taraflı olarak ne yapacağı vs. endüstri genelinde bir önerme olarak çerçeve edilen (RAND SL-4 güvenlik standartları dahil). Bir kez teslim edilen ürünlerin yerine, sınır güvenliği yol haritası ve risk raporları kalıcı belgeler olarak eklenir. 2023'te bir süreliğine bağlılık düşürüyor. AI R&D-4 eşiğini tanıttı: Bir kez geçtiğinde, Anthropic, yanlış uyum sağlama risklerini ve hafiflemelerini belirleyen bir onaylı vaka yayınlamalıdır. Claude Opus 4.6 bunu aşmaz. Antropic, v3.0 duyurmasında "bunu güvenle dışlamak zorlaşıyor" diyor. SaferAI 2023 RSP'yi 2.2 olarak değerlendirdi; v3.0'u 1.9'a düşürdüler. Bu sayede Antropic OpenAI ve DeepMind ile birlikte "zayıf" RSP kategorisine girdi. Kaliteli eşiğin 2023'teki miktarlı yükümlülükleri değiştirdiği için, durak sözcükünün kaldırılması en şiddetli gerilemedir.

> **【中文解读】**RSP v3.0 2026 yılında 2 月 24 日生效,替代 2023 政策。双层缓解:Anthropic 单边做什么 vs 行业范围建议(包括 RAND SL-4 安全标准) ・添加边界安全路线图和风险报告 作为常设文档而非一次性交付物品──删除 2023 暂停承诺──引入 AI R&D-4 齐值:一旦跨越,Anthropic 必须发布识别不对风险和缓解的肯定案──Claude Opus 4.6 未跨越它──Anthropic 在 v3.0 公告中声明"自信地排除这变得困难"──Safer 评价 2023 RSP 为 2.2;降级 v3.0 至 1.9,将将人类与 OpenMind                                                                                                                                                                      

> **【拓展：v3.0 的核心改动】**Üç önemli değişiklik: 1) 添加前沿安全路线图、风险报告、AI R&D-4 值; 2) 删除2023 暂停承诺; 3) 重构两层缓解时间表(Antropic 单边 vs 行业建议) ――SaferAI'nin indirim faktörü:定性值替代定量、暂停承诺删除、AI R&D-4 缓解描述为"肯定案例"而非具体措施、审查机制依赖于安тропо的安全咨询组缺乏独立监督──

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, RSP threshold decision engine) | **语言:** Python（标准库，RSP 阈值决策引擎）
**Prerequisites:** Phase 15 · 06 (AAR), Phase 15 · 07 (RSI) | **前置知识:** Phase 15 · 06（AAR），Phase 15 · 07（RSI）
**Time:** ~45 minutes | **时间:** ~45 分钟

>  **【前置】**Öte yandan, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bu süreçte, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, ve bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, ve bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, ve bir şekilde, bir şekilde, bir şekilde, bir şekilde, bir şekilde, ve, bir şekilde, bir şekilde, bir şekilde, ve, bir şekilde, bir şekilde, bir şekilde, bir şekilde, ve, bir şekilde, bir şekilde, bir şekilde, bir şekilde, ve, bir şekilde, bir şekilde, ve, bir şekilde, bir şekilde, bir şekilde, ve, bir şekilde, bir şekilde
>  **【类比】**RSP = "AI  şirketinin güvenlik anayasası"──2023 版 = 严格(定量值+暂停承诺);v3.0 = 灵活(定性值+删除暂停)──SaferAI 评分 2.2 降至 1.9("弱"类别)──新增 AI R&D-4 值 = Bir kez AI 自動化 AI 研发 研发 某水平に達したら, zorunlu açıklama yapılması gerekir
> 🤔 **【困惑】**S: Neden kaldırılmadı? 商业压力──暂停 = 竞争对手超越你──OpenAI、Google 都没暂停,Antropic 单方面暂停=自杀──修复:行业协调(RAND SL-4 标准) + 监管介入(EU AI Act) تاکہ囚犯困境──

## Sorunlar. Sorunlar.

Sınır laboratuvarları kısmen teknik belgeler, kısmen yönetim belgeleri ve kısmen düzenleyicilere sinyaller olan ölçekleme politikalarını yayınlar.

> Ön kenar laboratuvarın yayınladığı genişleme politikası, teknik dosyaların bir parçası, yönetim dosyalarının bir kısmı ve düzenleyicilere gönderilen sinyallerin bir kısmıdır.

RSP v3.0 şu anki Anthropic belgesi. Onu dikkatle okumak, ona uymak zorunlu olduğu için değil, çerçeve bir laboratuvarın felaket riskini nasıl algıladığını ve nasıl pazarlamaları halka iletiyorlarsa şekillendirdiği için önemlidir.

> RSP v3.0 is current Anthropic 文档──仔细阅读 önemli değil çünkü 合规具有约束力(不具), ama çünkü framework塑造实验室如何构想灾难性风险以及如何向公众传达权衡──

V3.0 vs. v2.0 farkı yararlı birimdir. Eklenenler: Sınır Güvenlik Yol Haritaları, Risk Raporları, AI R&D-4 eşiği. Alınanlar: 2023 duraklama taahhütü.

> v3.0 ve v2.0 arasındaki fark yararlı birimlerdir.

Yeni bir çerçeve oluşturuldu: Anthropic-bir taraflı ve endüstri önerisi arasında iki katlı bir azaltma programı bölündü. Dış inceleme  SaferAI  puanı 2.2 (v2) 'den 1.9 (v3.0) 'ye düşürdü.

> 重构: 分为人类 单边和行业建议的两层缓解时间表──外部审查SaferAI分数将从2.2(v2) 降至1.9(v3.0)──这是扩展政策如何在看上更精细的同时变得更不严谨的──

> **【中文解读】**Antropik'in sorumluluk genişleme politikası (RSP, Responsible Scaling Policy) AI  kapasite büyümekte güvenliğini korumak için bir çerçeve tanımladı.

## Konsepten bir şey.

### İki katlı hafifleme programı.

- **Anthropic unilateral actions**Diğer laboratuvarların yaptıklarından bağımsız olarak Anthropic'in yapacağı şey.
  Çeviri:**Anthropic 单边动作**Diğer laboratuvarlar ne yapsınlarsa yapsınlar.
- **Industry-wide recommendations**Bu, Anthropic'in tarafındaki yükümlülükler değil, politik destekler.
  Çeviri:**行业范围建议**Bu, Antropik 侧的承诺;是政策倡导──

İki katlı yapı v2'de değildi. Bu, bir okuyucu'nun her taahhüdün hangi sütunda yaşadığını görmesi gerektiği anlamına gelir. "endüstri genelinde önerme" sütunda bir güvenlik önlemi Anthropic'in vaadi değil; Anthropic'in umudu.

> Bu, okuyucuların her bir sözleşmeyi hangi sırada görmesi gerektiği anlamına gelir.

### AI R&D-4 eşiği.

Bu, RSP 3.0'ın önümüzdeki önemli eşiği olarak adlandırdığı yetenek seviyesi. Özellikle: AI araştırmalarının önemli bir kısmını rekabetçi maliyetle otomatikleştirebilecek bir model. Anthropic bir modelin bunu geçtiğine inandıktan sonra, ölçeklendirmeyi sürdürmeden önce yanlış uyum risklerini ve hafiflemeleri belirleyen bir onaylı durum yayınlamalıdır.

> Bu RSP v3.0'dur. Bu önemli bir kapasite seviyesidir. Konkrete göre, AI çalışmalarının bir kısmı olan rekabet maliyetinin otomatikleşmesi ile mümkün.

Claude Opus 4.6 v3.0 duyurularına göre bunu aşmaz. Belge ekliyor: "Bu konuyu kesin olarak reddetmek zorlaşıyor". Bu ifade önemli; bu sınırın bir spekülasyon sınırı değil, canlı bir endişe için yeterince yakın olduğunu kabul ediyor.

> Claude Opus 4.6 根据 v3.0 公告未跨越它──文档添加:"自信地排除 this became困难──"Bu kelime önemli; 值足接近以致是现实关注,推测性限制不是──

6. Ders (Automatik Uyum Araştırması) ve 7. Ders (Kendici Öz-İyişim) doğrudan bu eşiğe girer.

> Bölüm 6 课(Automatisize Zı araştırma) ve 7. ders(Başlangıç öz geliştirme) doğrudan değer¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬¬

### Sınır Güvenliği Yol Haritaları ve Risk Raporları

v3.0 iki eser türünü kalıcı belgelere yükseltir:

> v3.0 iki sınıf ürünleri düzenli olarak arşivlenir:

- **Frontier Safety Roadmap**: planlanan güvenlik çalışmalarını, kapasite beklentilerini ve hafifleme araştırmalarını açıklayan ileriye bakışlı belge.
  Çeviri:**前沿安全路线图**Planı: Planı güvenliği çalışma, kapasiteler bekleme ve hafifleme çalışmalarının özetleme dosyası
- **Risk Report**: serbest bırakıldıktan sonra belirli modeller üzerinde gözlemlenen kapasite ve kalan riskleri açıklayan geriye dönük belge.
  Çeviri:**风险报告**: yayın sonrası belirli model olay sonrası dosyası, gözlem yeteneğini ve kalan riskleri anlatmak

Her ikisi de kamuoyundadır. Her ikisi de açıklanmış bir kadens üzerinde güncellenir. Faydalı olan: okuyucu, Anthropic'in bir Yol Haritasında yapacağını söylediği şeyin Risk Raporunda rapor ettikleriyle nasıl karşılaştırıldığını takip edebilir.

> 两者公开──两者按声明节奏更新──效果:读者可追踪 Antropic 在路线图中说会做与在风险报告中报告中的报告的如何对比──

### Durma maddesini kaldırıyorum.

2023 RSP açık bir durak taahhüdü içeriyordu: bir model belirli kapasite eşiğlerini geçirse, eğitim hafifletmeler yapılana kadar durakta kalır. v3.0 açık bir durakta daha yumuşak bir formülasyonla yerini alır (etkin bir durum yayınlayın, hafifletmeler yeterli ise devam edin). SaferAI ve diğer analistler bunu yeni belgedeki en güçlü gerilem olarak doğrudan çağırdılar.

> 2023 RSP 包含显式暂停承诺:如果模型跨越特定能力值,训练将暂停直到缓解就位──v3.0 用更软表述(发布肯定案,如缓解充分则继续)

Değişikliğin politik argümanı: 2023'te miktarlı eşiğler 2026 çağındaki kapasite referansları tarafından erişilemez hale geldi çünkü referanslar yeniden ölçeklendirilmiştir. Karşı argüman: ölçeklendirme politikasında bir duraklama klazuli bir taahhüt aracıdır; kaldırılması politikanın güvenilirliğini ortadan kaldırır.

> 变更的政策论文:2023'ün ölçümsel değerinin 2026'da 时代能力基准 tarafından elde edilemez olduğu kanıtlanmıştır, çünkü基准 kendisi yeniden küçültülmüştür.

### SaferAI'nin derecelendirilmesi.

SaferAI, RSP tarzındaki belgeleri değerlendiren bağımsız bir organizasyon. Halk tarafından yapılan değerlendirme: 2023 Anthropic RSP 2.2 puan aldı ( 4.0'ın en iyi mevcut RSP olduğu ve 1.0'ın nominal olduğu bir ölçekten). v3.0 1.9 puan aldı. Bu, Anthropic'i "orta" dan "zayıf"a taşıdı ve OpenAI ve DeepMind'e zayıf kategoride katıldı.

> SaferAI RSP'nin bağımsız örgütleri tarafından değerlendirilir. Onun açık değerlendirmesi:2023 Antropik RSP 2.2(4.0 mevcut en iyi RSP, 1.0 isimli bir ölçekleme üzerinde)

SaferAI'ye göre derecelendirme faktörleri:

> SaferAI 列出的降级因素:

- Kaliteci eşiğin yerini miktarlı eşiğin aldı.
  Çine çevirisi:定性值替代定量──
- Durum yükümlülüğü kaldırıldı.
  Çıktı.
- AI R&D-4 eşiği azaltmaları, özel önlemlerden ziyade "etkin durum" olarak tanımlanır.
  Çin dilinde:AI R&D-4 值缓解描述为"肯定案例"而非具体措施──
- Tekrarlama mekanizmaları, sınırlı bağımsız denetim ile Anthropic'in Güvenlik Danışmanlık Grubu'na bağlıdır.
  Çinçe Çevirisi:审查机制依赖人类的安全咨询组,独立监督有限──

### Bu dersin ne olduğunu bilmiyorum.

Bu bir uyumluluk dersi değil. RSP 3.0 bir düzenlemedir; hiçbir şey Anthropic'i buna uymaya zorlamaz.

> Bu bir kural değil. RSP 3.0 kural değil.

Bu nedenle, bu konuda bir ders, belgelerin özelliği ve hak ettiği şüphecilik ile okunmasıdır. Ölçekleme politikaları, felaket riskli duruş hakkında yayınlanan ilk kamu sinyal sınır laboratuvarlarıdır. Onları iyi okuyan, çalışmaları sınır kapasitesine bağlı olan herkes için pratik bir beceri.

> Programın, ele alınan özellikleri ve şüpheciliklerini kullanmakla ilgili yayınlanmıştır.

## Çerçeveyi kullanın.
```figure
a5-rsp-ladder
```

## Kullan

`code/main.py`RSP eşiği değerlendirme şeklini yansıtan küçük bir karar motorunu uyguluyor: aday model ve bir dizi kapasite ölçümünü vererek, AI R&D-4 eşiği geçti mi, gerekli onaylı durum bölümleri ve dağıtım devam edebilir mi, geri dönün. Bu kasten basit; amacın belgenin mantığını açık bir şekilde yapmaktır.

> `code/main.py`RSP  değer değerlendirmesi biçiminin küçük karar motorunu gerçekleştirmek: given determinate candidate model and a set of capacity measurement, return AI R&D-4  value whether跨越、 需要肯定案节、部署是否可继续──它故意简单;点是让文档逻辑显式──

## İndirin . Ürünler .

`outputs/skill-scaling-policy-review.md`v3.0 referansına karşı bir ölçeklendirme politikasını (Anthropic, OpenAI, DeepMind veya iç) değerlendirir: iki katlı yapı, eşiği, duraklama yükümlülükleri, bağımsız değerlendirme.

> `outputs/skill-scaling-policy-review.md`"Antropik、OpenAI、DeepMind veya内部"): iki katlı yapı、 değer、暂停承诺、独立审查──

## Egzersizler.

1. Çık .`code/main.py`. Farklı kapasite düzeyleri ile üç sentetik model ekleyin.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py` üç farklı yetenek seviyesinin yapılmış modeli                                                                                                                                                                                                                                                        

2. RSP v3.0'u tam olarak okuyun (32 sayfa). "endüstri genel önerisi" seviyesinde yaşayan her taahhüdü belirleyin.
   Çin dilinde Türkçe: Full text read RSP v3.0(32 sayfa) ◦ "Büyük sektör önerisi"

3. SaferAI'nin RSP derecelendirme metodolojisini okuyun. V3.0 için 1.9 puanlarını belgeye rubriklerini uygulayarak yeniden üretin. Hangi rubrik satırı en fazla indirmeyi tetikledi?
   Çinçe Çevirimiçi:PDF'nin RSP 评分方法论──通过将评分量表应用于文档复现 v3.0 的 1.9 分── hangi ölçü gösterisi en fazla indirme yapıyor?

4. 2023'te durdurma taahhüdü kaldırıldı. 2026'da referans değerlerini yeniden ölçeklendirme problemini kabul ederek politika güvenilirliğini koruyan bir değiştirme taahhüdünü önerin.
   Çinli dilde: "2023'te bir süreliğine geri çekilme sözleşmesi kaldırıldı.

5. RSP v3.0 ile OpenAI Hazırlık Çerçevi v2 (Denevi 20) karşılaştırın. v3.0'un daha güçlü olduğu bir alan seçin. Hazırlık Çerçevi daha güçlü olan bir alan seçin.
   中文翻译:RSP v3.0 ile OpenAI Preparedness Framework v2(第 20 课) ―― seçin bir v3.0 更强的领域── seçin bir Preparedness Framework 更强的领域──

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| RSP | "Anthropic's scaling policy" | Responsible Scaling Policy; v3.0 effective Feb 24, 2026 |
| RSP | "Anthropic 的扩展政策" | Responsible Scaling Policy；v3.0 2026 年 2 月 24 日生效 |
| AI R&D-4 | "Research-automation threshold" | Capability to automate substantial AI research at competitive cost |
| AI R&D-4 | "研究自动化阈值" | 以竞争成本自动化相当部分 AI 研究的能力 |
| Affirmative case | "Safety justification" | Published argument that risks are identified and mitigations adequate |
| 肯定案例 | "安全证明" | 风险已识别缓解充分的已发布论证 |
| Frontier Safety Roadmap | "Forward plan" | Standing document on planned safety work and expected capabilities |
| 前沿安全路线图 | "前瞻计划" | 计划安全工作和预期能力的常设文档 |
| Risk Report | "Retrospective on a model" | Standing document on observed capability and residual risk after release |
| 风险报告 | "模型事后" | 发布后观察能力和剩余风险的常设文档 |
| Two-tier mitigation | "Unilateral vs industry" | Anthropic commitments vs industry recommendations, separated |
| 两层缓解 | "单边 vs 行业" | Anthropic 承诺 vs 行业建议，分开 |
| Pause commitment | "2023 clause" | Explicit promise to pause training; removed in v3.0 |
| 暂停承诺 | "2023 条款" | 暂停训练的显式承诺；v3.0 中移除 |
| SaferAI rating | "Independent RSP grade" | Third-party rubric; v3.0 scored 1.9 (v2 was 2.2) |
| SaferAI 评分 | "独立 RSP 评分" | 第三方量表；v3.0 得 1.9（v2 是 2.2） |

## Daha fazla okumak

- [Anthropic — Responsible Scaling Policy v3.0](https://anthropic.com/responsible-scaling-policy/rsp-v3-0) 32 sayfalık politika.
  Çeviri: 完整 32 页政策。
- [Anthropic — RSP v3.0 announcement](https://www.anthropic.com/news/responsible-scaling-policy-v3) v2'den gelen değişikliklerin özetleri.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çev Çeviri Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Ç Ç Çev Ç
- [Anthropic — Frontier Safety Roadmap](https://www.anthropic.com/research/frontier-safety) RSP v3.0'dan bağlantılı kalıcı belge.
  Çine Çeviri:RSP v3.0 链接的常设文档。
- [Anthropic — Risk Report: Claude Opus 4.6](https://www.anthropic.com/research/risk-report-claude-opus-4-6) mevcut sınır modeli üzerinde geriye bakış.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Ç Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) AI R&D-4'i ölçülen özerklik ile bağlar.
  Çinçe Çevirimi:将 AI R&D-4 连接到测量的自主性──
