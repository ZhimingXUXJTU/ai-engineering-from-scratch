# Rol Uzmanlığı  Planlayıcı, Eleştirmen, İcracı, Dayanıcı  Deneyici  Eleştirmen  Planı  Rol

> 2026'da en yaygın çok ajanlı parçalanma: bir ajan planlar, bir yönetir, bir eleştirir veya doğruluyor. MetaGPT (arXiv:2308.00352) bunu rol isteklerine kodlanmış SOP'ler olarak resmileştirir  Ürün Yöneticisi, Mimar, Proje Yöneticisi, Mühendis, Sorucu Mühendis  aşağıdaki `Code = SOP(Team)`- Evet . ChatDev (arXiv:2307.07924) dizayner, programcı, yorumcu, testçi dizaynını "çap zinciri" ile "kommunikatif halüsinasyon" ile zincirler (ajanlar açıkça eksik detayları talep eder). Verifiyeci yük taşıyıcıdır: Cemri et al. (MAST, arXiv:2503.13657) gösterir her multi-ajan başarısızlığı kayıp veya kırık doğrulama izlenebilir. PwC, CrewAI'de yapılandırılmış onay döngüslerinden 7× doğruluk artışı (% 10 → 70%) rapor etti.

> **【中文解读】**Bu bölüm, rol uzmanlaşımını tanıtır.

> **【拓展：role specialization→具体应用】**角色专业化是 CrewAI'nin temel psikolojik düşüncesi Her ajanın bir rolü vardırRole) 、目标 (目标) 及背景故事Back story)  Praktiki, belirgin rol tanımının çok sayıda ajanın işbirliği etkinliğini önemli ölçüde artırabileceğini göstermektedir


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib) | **语言:** Python (标准库)
**Prerequisites:** Phase 16 · 04 (Primitive Model), Phase 16 · 05 (Supervisor) | **前置知识:** Phase 16 · 04 (Primitive Model), Phase 16 · 05 (Supervisor)
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Öğrenci Bölüm:Düşünç:Pase 16·04-05
>  **【类比】**角色专业化 = "电影制作团队"──Planner = 编剧(定方向)、Executor = 演员(执行)、Critic = 内审、Verifier = 质检员──MetaGPT、ChatDev、CrewAI 都用这种角色分解──Cemri 等人 MAST 论文:所有多 Agent 失败都可追溯到"缺少或破损的验证人"验证是承重墙──PwC 案例:加验证人 让准确率从10% 到70% 7倍)──

## Sorunlar sorunun giriş

Genel çoklu ajanlı sistemler genel çıkış üretir. Grup sohbetinde üç kodlayıcı aynı ortalama kodun üç tadını yazar. Daha fazla ajan ekleyebilir, daha fazla yuvarlak ekleyebilir ve yine de kalite eşiğini geçemezsiniz.

> Genel olarak kullanılan çoklu ajanlar  sistemi genel olarak üretilen bir çıkış oluşturur. Grup konuşma içindeki üç kodlayıcı üç farklı ısılı aynı düzlemli kod yazıyor. Daha fazla ajan ekleyebilirsin. Daha fazla sıra, hala kalite kapısını geçemezsin.

Sorun miktar değil, tekerlilik. Aynı görevi verilen üç aynı ajan, üç benzer yanlış cevap verir. Aynı kıpırdakları paylaşırlar çünkü aynı kıpırdak ve model paylaşırlar. Aynı şeylerin daha fazlasını eklemek yardımcı olmaz; üretken yönlerden farklı ajanlara ihtiyacınız var.

>  sorun sayı değil aynı niteliktir.  Üç aynı ajan  aynı görev verilmiş üç benzer hata cevap üretir.  Bunlar aynı noktaları paylaşırlar çünkü aynı ipucu ve modelleri paylaşırlar.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    

Bu, bir sistemin temel düzeltme ile içsel anlaşmazlığa sahip olması anlamına gelir. Bu sistemin temel düzeltme ile içsel anlaşmazlıkları vardır.

> Düzeltme yöntemi daha fazla Agent değil, farklı Agent olarak farklı roller belirlemiştir. Eleştirmen planlayıcısına hiçbir araç verilmez.

Anahtar değişim: "bir daha fazla ajan aynı şeyi yapıyor"dan "farklı ajanlar farklı şeyler yapıyor". Uzmanlık olmadan paralellik sadece pahalı tahminler. Uzmanlık sistemin kendi hatalarını yakalamalarına izin veren asimetri yaratır.

> 关键转变: "Daha fazla ajan aynı şeyi yap"dan "farklı ajan farklı şeyler yap"a.

## Konsept merkezi konsept

### Dört kanonik rol

**Planner.**Hedef okuyor, adım listesi veya bir spesifikasyon oluşturur. Araçlar: bilgi alımı, belgeleri. Çıktı: yapılandırılmış plan.

> **规划者。**读取目标,产生步骤列表或规范──工具:知识检索、文档──输出: yapılandırma planı──

**Executor.**Bir planı bir adımdan bir okuyor, eser üretir. Araçlar: gerçek çalışma araçları (kod kompiliörü, kabuğu, API istemcisi). Çıktı: eser.

> **执行者。**Her zaman bir plan adımını, bir işlemi oluşturmak için bir program yapın.

**Critic.**Yönetici'nin niyetine karşı çıkışını okuyor. Araçlar: eserlere sadece okuyucu erişim, statik analiz. Çıktı: kabul/dönüş nedenlerle.

> **批评者。**Yapımcıların sadece çalışmalarına yönelik çalışma biçimleri, durumlar ve analizler, sonuçlar, kabul/ reddetme ve nedenler.

**Verifier.**Artifakti okuyor ve belirleyici bir kontrol yürütüyor. Araçlar: test koşucusu, tip kontrolcü, şema onaylayıcı. Çıktı: kanıt ile geç / başarısız.

> **验证者。**读取工件并运行确定性检查──工具:测试运行器、类型检查器、模式验证器──输出:通过/失败及证据──

Eleştirmen, öznel, görüşlü, genellikle LLM tabanlıdır.

> Eleştirmenler önyargılı, genellikle LLM'ye dayalıdır.

Bu nedenle, bu sistemler, sadece eleştirmenlere (LLM inceleyicileri) sahip bir sistem için doğru ancak yanlış bir çıkış elde eder.

> Bu sistemleri bir araya getirmek en yaygın çoklu bir tasarım hatasıdır. Sadece eleştirmenlerin (LLM) sistemleri doğru ancak kötü bir çıkış elde eder.

### MetaGPT'nin SOP örneği

MetaGPT (arXiv:2308.00352) yazılım mühendisliği SOP'lerini rol istekleri olarak kodlar:

> MetaGPT(arXiv:2308.00352)将软件工程 SOP 编码为角色提示:

"SOP" çerçevesini insan organizasyonlarından ödünç alınmıştır: Standart İşlem Prosedurları ad-hoc çalışmasını tekrarlanabilir bir sürece dönüştürür. MetaGPT bunu LLM'lere uyguluyor.

> "SOP" çerçevesinin insan örgütlerinden alınması: Standart Operasyon süreci geçici çalışmaları tekrarlanabilir süreci olarak dönüştürecek.

- **Product Manager**- PRD'nin yazdığı gibi.
  Çeviri:**产品经理**编写 PRD──
- **Architect**Sistem tasarımı üretir.
  Çeviri:**架构师**产生系统设计──
- **Project Manager**Görevleri bölüyor.
  Çeviri:**项目经理**- Çıkarım.
- **Engineer**araçlar.
  Çeviri:**工程师**实现──
- **QA Engineer**Testler yaptırıyor.
  Çeviri:**QA 工程师**运行测试──

Her rolün kapsamlı bir giriş/çıktı şeması vardır.`Code = SOP(Team)`formülasyon  Deterministik SOP'ler bir LLM ekibiyi öngörülebilir bir boru hattına dönüştürür.

> Her rolün sert bir giriş/çıktı modeli vardır. Rol gösterisi rolün* ne olduğunu ve* neyi üretmesi gerektiğini söyler.`Code = SOP(Team)`SOP'nin bir LLM  Ekibi bir öngörülebilir akış hattına dönüştüğü belirlenir.

Anahtar anlayış: takımın iş akışını sohbet olarak değil kod olarak kodlayın. LLM rollerinin her biri belirleyici bir grafikte bir düğümdür; grafik yapısı insan tarafından yazılmıştır. LLM'ler yerel işi yapar; insanlar küresel iş akışına sahip.

> 关键洞察:将团队工作流编码为代码,而不是对话――每个 LLM 角色是确定性图中的节点;图结构由人类编写――LLM 做局部工作;人类拥有全局工作流――

### ChatDev'in iletişimsel halüsinasyonu.

ChatDev bir anahtar hareket ekler: bir icracı planda olmayan belirli bir ayrıntıya ihtiyaç duyduğunda, devam etmeden önce tasarımcıya açıkça sorar. Bu, ayrıntıyı makul bir şekilde icat etmenin klasik LLM başarısızlığını önler.

> ChatDev bir anahtar girişim ekledi: Bir icracı bir planda bulunmayan belirli ayrıntılara ihtiyaç duyduğunda, tasarımcıya açıkça sorgu sorar ve bu da LLM klasiklerinin başarısızlığını önler.

Bu model, kaynakta halüsinasyonları yakalar. Gerçekten sonra uydurulmuş detayları tespit etmek yerine, uygulayıcının varsaymadan önce sormasını gerektirerek uydurmayı önler.

> Bu model, gerçekleri kontrol etmek için bir gerçektiren bir yöntem değildir.

Uygulama: rol sorgulaması "verilmediğiniz belirli bilgilere ihtiyacınız olduğunda, çıkış üretmeden önce ilgili rolün adını sorun".

> 实现:角色提示包括"When you need you not provided specific information, before generating output" ("Sana ihtiyaç duyduğunda sana verilmeyen belirli bilgilerle ilgili roller sorulduğunda, üretimden önce, başvurun" anlamına gelir.

### Neden doğrulayıcı en önemli

Cemri et al. (MAST) 1642 çoklu ajan uygulama başarısızlığını takip etti. 21.3% doğrulama boşluklarıydı  sistem kimse kontrol etmediği bir cevap gönderdi. Geri kalan 79% genellikle "sessiz bir şekilde başarısız olan bir kontrol vardı veya hiç çalıştırılmadı".

> Cemri 等人(MAST) 1642 多 代理 执行失败──21.3% 验证缺口──系统发布没有人检查过的答案──其余79% 通常追溯到"一个检查默默失败或从未运行"──验证是承担重角色──

21.3% rakamı, 2026'da çoklu ajan mühendisliği için en çok alıntılanan tek istatistiktir.

> 21.3% bu rakam 2026 yılındaki Agent 工程'da en çok alıntılanan statistiktir. Bu rakam şöyle diyor: Eğer sadece bir rol eklerseniz, sistemde bir onaylayıcı olmalısınız.

PwC (CrewAI dağıtımları, 2025) bir yapılandırılmış doğrulama döngüsünün eklenmesinin doğruluğunu %10'dan %70'e taşıdığını bildirdi.

> PwC  rapor(CrewAI 部署,2025) Ek yapılandırma test döngüsü doğruluk oranını %10'dan %70'e yükseltecek.

### Eleştirmen vs. doğrulayıcı

- Eleştirmen, bir eseryi kalitesi için değerlendiren bir Yüksek Lisans Derecesidir.
  Çinçe Çevirimi: eleştirmen bir eleştirmen.
- Bir doğrulayıcı, eser üzerinde çalışan bir belirleyici programdır.
  Çinçe Çevirimi:验证者 (验证者) işlemi üzerinde yürütülen kesinlik prosedürüdür.

İkisi de kullanın. Eleştirmen, verifikatörün ifade edemediği tad sorunlarını yakalar. Verifikatör, eleştirmenin göremediği hataları yakalar çünkü sadece çalıştırma sırasında ortaya çıkarlar.

> 两者都用──批评者捕获验证者无法表达的质量问题──验证者捕获批评者看不到的 bug,因为它们只在运行时出现──

Genel bir düzenleme: önce doğrulayıcı (hızlı, açıkça kırık çalışmayı öldürür), sonra eleştirmen (yavaş, kalitesini artar). Bazı ekipler, kırık kod üzerinde hesaplama harcamadan önce tad sorunlarını yakalamak için sırayı tersine çevirir.

> 常见序列:先验证者(快,杀死明显破损的工作), sonra eleştirmen(慢,精炼质量) ・・・ Bazı ekipler dönüşüm sırasıyla çiçek hesaplama kaynaklarını yeniden işlenmeden önce kalite sorunu yakalamak için hangi türleri görevinize uygun olarak test edebilirsiniz。

### Anti-önüm

Sisteminizde her rol bir LLM'dir ve her rolün çıkışı "Bana iyi görünüyor". Klasik MAST başarısızlık modudur.

> Sistemdeki her rol LLM'dir, her rolün çıkışı "görünmez"dir.

### Çerçeve haritalamaları

- **CrewAI** `Agent(role, goal, backstory)`ders kitabı uzmanlık yüzeyi.
  Çeviri:**CrewAI** `Agent(role, goal, backstory)`Bu, öğretim biçiminin uzmanlaşmış yüzeyi.
- **LangGraph** düğümler özel isteklere sahip olabilir; kenarlar boru hattını zorlar.
  Çeviri:**LangGraph** 节点可以有专门提示;边强制流水线──
- **AutoGen** Grup Çat'ta tek kelime isimleri ile rolü özel konuşma ajanları.
  Çeviri:**AutoGen** GroupChat'te belirtilen bir rolü olan KonversableAgent。
- **OpenAI Agents SDK** Rol uzmanı ajanlar arasında el ele alma araçları.
  Çeviri:**OpenAI Agents SDK** 角色专业化 Ajanlar arasındaki iletişim araçları。

## Yapın.
```figure
swarm-roles
```

## Yapın

`code/main.py`basit bir Python fonksiyonu oluşturan 4 rollü bir boru hattı uyguluyor:

> `code/main.py`实现一个构建简单 Python 函数的4 角色流水线:

- **Planner**bir spesifikasyon üretir.
  Çeviri:**规划者**产生规范──
- **Executor**bir kod dizini oluşturur.
  Çeviri:**执行者**Çıkışlı bir şey.
- **Critic**(LLM simülasyonu) açık sorunları işaretler.
  Çeviri:**批评者**(LLM 模拟) 标记明显问题──
- **Verifier**oluşturulan kodı kum kutuya (`exec`) bir test durumuna karşı.
  Çeviri:**验证者**"Şah kutusu"`exec`) test kullanımı örnekleri için çalıştırılan kodlar oluşturulur.

Demo iki kez çalışır: bir kez uygulayıcı doğru kod üretirken (kritik + doğrulayıcı her ikisi de geçer), bir kez uygulayıcı açık olmayan kod üretirken (kritik yanlışlığı kaçırır çünkü makul görünüyor, doğrulayıcı test başarısız olduğu için yakalar).

> 演示运行两次:一次执行者产生正确的代码(批评者 + 验证者都通过),一次执行者产生偏离规范的代码(批评者因为看起来合理而错过错误,验证者因为测试失败而捕获它) ]]

## Çerçeveyi kullanın.

`outputs/skill-role-designer.md`Bir görev alır ve rol listesi (3-5 rol), her rol için giriş/çıktı şeması ve doğrulayıcı kontrolü üretir.

> `outputs/skill-role-designer.md`接收任务并产生角色名册(3-5 个角色) 、 her rolün giriş/çıxış modeli ve验证人检查──在将代理 连接到框架之前使用──

## İndirin . Ürünler .

Kontrol listesini:

> 检查清单:

- **At least one deterministic verifier.**Hiç de tüm-LLM.
  Çeviri:**至少一个确定性验证者。**Hepimiz için bir LLM yok.
- **Explicit I/O schema per role.**Planlayıcı bir spesifikasyon gönderir, proza değil; uygulayıcı bu şemaları okuyor.
  Çeviri:**每个角色有明确的 I/O 模式。**规划者回归规范,散文 değil;执行者读取该模式──
- **Communicative dehallucination.**İnkârcı, bilgi eksik olduğunda planlayıcısına sormalıdır; asla icat etme.
  Çeviri:**交流去幻觉。**执行者在信息缺失时必须询问规划者;永远不要发明──
- **Critic/verifier ordering.**Önce eleştirmen çalıştır ( ucuz, tasarım sorunlarını yakalar), ikinci doğrulayıcı (yavaş, hataları yakalar).
  Çeviri:**批评者/验证者顺序。**Önceden eleştirmen, daha önce eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha sonra eleştirmen, daha daha fazla eleştirmen, daha daha daha fazla eleştirmen, daha daha daha daha fazla eleştirmen, daha daha daha daha daha iyi bir daha daha daha iyi bir daha daha daha daha daha daha daha iyi.
- **Loop budget.**Max 2 eleştirmen-işleyici gözden geçirme turları insan olarak yükselmeden önce.
  Çeviri:**循环预算。**En fazla 2 eleştirmen-işleyici modification轮

## Egzersizler.

1. Çık .`code/main.py`ve doğrulayıcı eleştirmenin kaçırdığı hatayı nasıl yakaladığını gözlemleyin.`return`) bir ek doğrulayıcı olarak.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`Ve gözlemci nasıl eleştirmenlerin yanlışlarını yakalar.`return`Bu, bir diğer testici olarak neyi yakaladı?
2. 5. rolü ekleyin: "gereklilik analitiği" kullanıcı isteğini planlama hazır bir spesifikasyon olarak çevirir. Hangi iletişimsel halüsinasyon istekleri ona doğru akmalı?
   Çin dilinde: 添加第 5 个角色:"需求分析师",将用户愿望翻译为规划者可用规范──什么样的交流去幻觉请求应该流上方?
3. MetaGPT Bölümü 3'ü okuyun ("Agentler"). MetaGPT'nin 5 rolünün her birinin giriş/çıktı şeması listelenmelidir.
   Çine dilinde:{{lang-en_MetaGPT}} → "Agent") → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "Agent" → "A"
4. ChatDev'in sohbet zinciri şablonunu okuyun (arXiv:2307.07924 Şekil 3). İletişimsel halüsinasyonun sonsuz bir döngü kırıldığı yerleri belirleyin.
   Çinçe Çevirimi: ÇatDev'in Çat Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Çanak Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
5. PwC'nin 7 kat daha fazla doğruluk kazanımı doğrulama döngüslerinden geldi. Bir doğrulama cihazı eklemenin yardımcı olmayacağı üç görevi varsayın  doğruluğun belirleyici kontrolü imkansız veya yasaklı bir şekilde pahalı olduğu yerlerde.
   Çince Translation:PwC'nin 7 kat doğruluk oranı test döngüsünden yükseldi.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Role specialization / 角色专业化 | "Different agents, different jobs" / "不同 Agent，不同工作" | Distinct system prompts tuned for planner/executor/critic/verifier roles. / 为规划者/执行者/批评者/验证者角色调优的独特系统提示。 |
| SOP pattern / SOP 模式 | "Encoded standard operating procedure" / "编码标准操作流程" | MetaGPT's framing: strict I/O schemas per role turn a team into a pipeline. / MetaGPT 的框架：每个角色的严格 I/O 模式将团队变成流水线。 |
| Communicative dehallucination / 交流去幻觉 | "Ask before inventing" / "先问再发明" | ChatDev pattern: executor asks planner when a detail is missing rather than making one up. / ChatDev 模式：执行者在细节缺失时询问规划者而不是编造。 |
| Critic / 批评者 | "LLM reviewer" / "LLM 审阅者" | Subjective, opinionated reviewer. Catches taste issues. Can be fooled by plausible prose. / 主观的、有观点的审阅者。捕获质量问题。可以被似是而非的散文愚弄。 |
| Verifier / 验证者 | "Deterministic check" / "确定性检查" | Code-based pass/fail. Test runner, type checker, schema validator. Cannot be fooled. / 基于代码的通过/失败。测试运行器、类型检查器、模式验证器。不能被愚弄。 |
| Verification gap / 验证缺口 | "No one checked" / "没人检查" | 21.3% of MAST failures. Answer shipped without a check that would have caught the bug. / 21.3% 的 MAST 失败。发布答案时没有会捕获 bug 的检查。 |
| Revision loop / 修订循环 | "Critic sends it back" / "批评者打回" | Critic rejection triggers executor re-run with feedback. Needs a budget. / 批评者拒绝触发带反馈的执行者重新运行。需要预算。 |
| All-LLM anti-pattern / 全 LLM 反模式 | "Looks good to me" / "看起来不错" | Every role is an LLM, no deterministic check. Classic MAST failure. / 每个角色都是 LLM，没有确定性检查。经典的 MAST 失败。 |

## Daha fazla okumak

- [Hong et al. — MetaGPT: Meta Programming for Multi-Agent Collaboration](https://arxiv.org/abs/2308.00352) SOP-as-role-prompt referans kağıdı
  中文翻译:Hong 等人  MetaGPT:多 Agent 协作的元编程  SOP 作为角色提示的参考论文
- [Qian et al. — Communicative Agents for Software Development (ChatDev)](https://arxiv.org/abs/2307.07924) Çat zinciri + iletişimsel halüsinasyon
  Çinçe Çevirimi:Qian 等人  软件开发的通信代理(ChatDev) 聊天链 + 交流去幻觉
- [Cemri et al. — Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) MAST taksonomisi; doğrulama boşlukları başarısızlıkların % 21,3'ünü oluşturur
  Çinçe Çevirimi:Cemri  et al  Neden çok sayıda Ajan LLM 系统会失败? MAST 分类法;验证缺口占失的21.3%
- [CrewAI docs — Agent roles](https://docs.crewai.com/en/introduction) üretim rolü özellik yüzeyi
  Çeviri:CrewAI 文档  Ajan 角色  生产角色规范表面
