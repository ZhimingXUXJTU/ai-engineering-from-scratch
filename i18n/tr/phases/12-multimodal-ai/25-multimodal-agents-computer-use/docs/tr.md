# Multimodal ajanlar ve bilgisayar kullanımı (Capstone) ✓

> 2026 sınır ürünü ekran görüntüleri okuyan, düğmeler üzerinde tıklayan, web UI'lerini gezinen, formları dolduran ve iş akışlarını sonundan sonuna tamamlayan bir multimodal ajan. SeeClick ve CogAgent (2024) GUI-burunlama ilkelerini kanıtladı. Ferret-UI'ye mobil eklendi. ChartAgent, grafikler için görsel araç kullanımı tanıttı. VisualWebArena ve AgentVista (2026) sınır kovalamaları  ve hatta Gemini 3 Pro ve Claude Opus'un zor görevlerinde %30'luk puanı var. Bu kapı taşı 12 aşamasının her ipini bir araya getiriyor: algılama (yüksek çözünürlüklü VLM), mantıklama (cilt kullanımı ile LLM), yerleştirme (koordinat çıkışı), uzun ufukta hafıza ve değerlendirme.

> **【中文解读】**2026 yılının ön kenar ürünleri ise, iş akışının çoklu biçimlerini okuyabilmektedir. Bu ürünler, Gemini 3 Pro ve Claude Opus 4.7'nin bile geçiş oranının %30'unu oluşturmaktadır. Bu, 12. aşamada yapılan eğitim, bütünleşme, algılama, konumlandırma, uzun süreli bellek ve değerlendirme programıdır.

**Type:** Capstone
**Languages:** Python (stdlib, action schema + agent loop skeleton)
**Prerequisites:** Phase 12 · 05 (LLaVA), Phase 12 · 09 (Qwen-VL JSON), Phase 14 (Agent Engineering)
**Time:** ~240 minutes

>  **【前置】**学本节前 Lütfen önce bil:Fase 12 全部(VLM 演进) 、Fase 14·01-10(Agent 循环、工具调用) 、Fase 14·30+(工作台系列 Agent 实践) ⋅ 本节是Fase 12 的毕业课所有多模态 + Agent 技术整合成一个能操作电脑的产品──
>  **【类比】**Çoğu zaman, bir kişiye bir iş yaptırmak için bir yol bulması zor olabilir. Bu yolla, bir kişiye bir iş yaptırmak için bir yol bulması zor olabilir.
> ️ **【易错点】**让 Agent 直接执行动作不设人工审核 = 灾难(可能误转账、错删除) 修复:所有"破坏性动作" (bkz: 破坏性动作) 点击提交、确认、删除按) 必须人类审核或干运行 模式。Antropic Computer Use's design philosophy is "提案→人类批准→执行",对应阶段15·15 模式──

## Öğrenme hedefleri

- Multimodal bir ajan döngüsünü tasarlayın: algı → neden → eylem → gözlem → tekrar.
  设计多模态 Ajan 循环:感知 → 推理 → 行动 → 观察 → 重复。
- VLM'nin JSON olarak yayınlayabileceği bir GUI yerleştirme çıkış şeması oluşturun (klik koordinatları, metin yazma, kaydırma, çekme).
  构建 GUI 定位输出模式(点击坐标、输入文字、滚动、拖),VLM 以 JSON 格式输出──
- Sadece ekran görüntüsü ajanları vs erişilebilirlik ağacı ajanları vs hibrit ajanları karşılaştırın.
  Temiz bir kesim ajanı ‒ engelli ağaç ajanı ‒ karışık ajanı ‒
- Küçük bir VisualWebArena parçası üzerinde multimodal ajan referans değerlendirmeyi oluşturun.
  VisualWebArena'da küçük boyutlu bir grup üzerinde oluşturulmuştur.

## Sorun , sorun tanımlandı .

> **【中文解读】**Bu nedenle, bir kullanıcıya bir web sitesi göndermek için bir web sitesine girmesi gerekir. Bu sitede bir web sitesi oluşturulmalıdır.

Bir rezervasyon sitesi iş akışı: "15 Nisan için Tokyo'ya bir uçak bul bana, 800 dolardan az bir koridor koltuğu, rezervasyon yap".

> Bir sipariş çalışma akışı:"Help me find 4 月 15 日飞东京的航班,靠走道,$800 以下,预订──"

Bir multimodal ajanın:

> 多模态 Ajan 需要:

1. Tarayıcı ekran görüntüsünü çek.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
2. Ekran çekimini + URL + hedefi bir plana ayırın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
3. Yapılandırılmış bir eylem yapın: tıklayın (x,y), "Tokyo" yazın (E elementinde), aşağıya kaydırın, seçin (radio düğmesi).
   Çine çevirisi:输出结构化动作:点击(x,y) 、输入"Tokyo"(element E) 、向下滚动、选择(单选按) ✿
4. Eylemleri tarayıcıya uygulayın.
   Çinçe Çevirisi:
5. Yeni durumu izleyin (sonraki ekran görüntüsü).
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
6. Görev bitene kadar tekrarlayın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri

Her adım bir multimodal VLM çağrısıdır. VLM çıkışı parse edilebilir JSON olmalıdır. Hatalar adımlar arasında karmaşık, bu yüzden kurtarma önemlidir.

> Her adım bir çok biçimli VLM 调用──VLM 输出必须是可解析的 JSON──错误在步骤间累积,因此恢复机制至关重要──

## Konsepten bir şey.

> **【中文解读】**Çok modolu bir ajan (örneğin Bilgisayar Kullanım Ajansı) AI'yi doğrudan bilgisayar arayüzünü yönetmesine izin verin: ekran içeriğini anlamak, fareler/kiy tableti işlemleri oluşturmak.

> **【拓展：Computer Use 的前沿**Antropik'in Bilgisayar Kullanımı 让Claude 直接操作桌面应用,完成网页浏览、表单填写等任务──OpenAI'nın Operator 使用类似方法──关键技术挑战:精确定位──准确点击按) 状态跟踪──理解界面变化──错误恢复──操作失败后重试──


### GUI yerleştirme  ilkel  GUI 定位 基础原语

GUI yerleştirme: bir ekran görüntüsü ve doğal dil talimatı verildiğinde, tıklamak için (x, y) koordinatını çıkartın (veya diğer eylem).

> GUI 定位是:给定一张截图和自然语言指令,输出需要点击的 (x, y) 坐标(或其他动作)

> **【中文解读】**GUI 定位是:给定一张截图和自然语言指令,输出需要点击的 (x, y) 坐标(或其他动作) ――SeeClick ilk büyük çapta açık bir başarıdır,CogAgent 增加了1120x1120高分辨率编码,Ferret-UI 聚焦移动端 UI──输出格式通常是JSON,`element_desc`字段帮助恢复当坐标在截图间漂移时,语义提示让系统重新定位──

SeeClick (arXiv:2401.10935) ölçekte ilk açık sonuç oldu: sentetik + gerçek GUI verilerine bir VLM'yi ince ayarlayın, çıkış koordinatları düz metin işaretleri olarak çalıştırın.

> SeeClick ilk büyük çapta açık bir başarıdır: Synthesis+ gerçek GUI verilerine göre VLM, saf metin token ile 输出坐标──有效──

CogAgent (arXiv:2312.08914) yoğun UI için 1120x1120 yüksek çözünürlüklü kodlama ekledi.

> CogAgent yoğun UI için 1120x1120 yüksek çözünürlüklü kodlama ekledi.

Ferret-UI (arXiv:2404.05719) mobil UI'lere odaklanır, iOS erişilebilirlik verileri ile entegre edilir.

> Ferret-UI 聚焦移动端 UI,集成 iOS 无障碍数据──

Çıktı biçimi genellikle JSON:

> 输出 biçimi genellikle JSON:

```json
{"action": "click", "x": 384, "y": 220, "element_desc": "Search button"}
```

- Evet .`element_desc`kurtarmaya yardımcı olur: Eğer koordinatlar ekran görüntüleri arasında hareket ederse, semantik ipucu sistemi yeniden yerleştirir.

> `element_desc`帮助恢复:如果坐标在截图间漂移,语义提示让系统重新定位──

### Hareket planları. Hareket modeli.

Tipik bir eylem şeması 6-10 eylem türüne sahiptir:

> Tipik hareket modüsü 6-10 türden hareket türü içerir:

> **【中文解读】**Tipik hareket modeli 6-10 种动作类型:click(点击)、type(输入)、scroll(滚动)、drag(拖)、select(选择)、hover(悬停)、navigate(导航)、wait(wait)、done)、完成 (Agent Her adım için bir hareket çıkarır,浏览器包装器执行后返回新状态──

- `click`(x, y)
  Çeviri:`click`:点击 (x, y) 』
- `type`(seks, x?, y?)
  Çeviri:`type`:输入文本,可选位置──
- `scroll`: (yön, miktar)
  Çeviri:`scroll`Çekilmek için bir yol var.
- `drag`(x0, y0, x1, y1)
  Çeviri:`drag`(x0, y0) 拖到 (x1, y1)
- `select`: (option_index)
  Çeviri:`select`Seçim Seçimleri:
- `hover`(x, y)
  Çeviri:`hover`:悬停 (x, y) 』
- `navigate`- Evet .
  Çeviri:`navigate`Uçuş adresine ulaşmak için.
- `wait`(ms)
  Çeviri:`wait`Millimeter saniye bekle.
- `done`: (Başarısı, açıklama)
  Çeviri:`done`:完成(成功/失败,解释)

Ajan her adımda bir eylem çıkarır. Tarayıcı sarısı yeni durumu yürütür ve gönderir.

> Ajan her adım bir hareket çıkarıyor.

### Ekran çekimi ve erişilebilirlik ağacı

> **【中文解读】**两种输入模式:纯截图模式最通用但精度较低;无障碍树 (BAN) 无障碍信息) 更多可靠但只在有结构数据时可用;混合模式同时使用两种,树用于原子动作定位,截图用于语义理解;;生产代理 尽可能使用混合模式;;

İki giriş modusu:

> 两种输入模式:

- Sadece ekran görüntüsü: tam görüntü, yapısal bilgi yok. En genel; herhangi bir uygulamada çalışır.
  Çinçe Çizgi: tam bir görüntü, yapısız bilgi, en genel kullanım, herhangi bir uygulamaya uygundur.
- Erişilebilirlik ağacı: yapılandırılmış DOM / iOS erişilebilirlik bilgileri. Yerleşim için çok daha güvenilir; ağaç mevcut olduğunda çalışır.
  Çinçe çevirisi: 无障碍树:结构化 DOM / iOS 无障碍信息──定位更可靠;在有树数据时可用──
- İkili de, atomik eylemler için güvenilir bir temel olarak ağaç ve semantik bağlam için ekran görüntüsü ile.
  Çeviri:                                                                                                                                                                                                                                                             

Üretim ajanları mümkün olduğunda hibrid kullanırlar. Tarayıcı otomasyonu (Selenium + erişilebilirlik) her zaman ağacı vardır; masaüstü uygulamaları bazen yapar.

> Üretim Ajanı 混合模式を尽可能使用します.

### Uzun vadede hafıza.

20 adımlı bir iş akışı 20 ekran görüntüsü oluşturur. VLM'nin bağlamı hızlı bir şekilde doldurulur.

> 20 步工作流产生 20 张截图──VLM 上下文快快填满──三种压缩策略:

> **【中文解读】**20 步工作流产生 20 张截图,VLM 上下文很快填满──三种缩写策略:摘要链(每5 步总结一次,丢弃旧截图) 跳(保留首尾和每第3 张) 、工具记录日志(仅保留文本日志不看旧截图)──Claude's computer use API 使用日志模式,更简单可靠──

- Özet zinciri: her 5 adımdan sonra, olanları özetleyin, eski ekran görüntüleri bırakın.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç
- Atlama çerçeve: ilk, son ve her 3. ekran görüntüsünü tutun.
  Çönüş: 保留首、尾和每第 3 张截图──
- Araç kayıtlı günlüğü: eylemleri gerçekleştirin, yapılanların metin günlüğünü tutun; eski ekran görüntüleri tekrar görmeyin.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç

Claude'un bilgisayar kullanımı API'si günlük örneğini kullanıyor.

> Claude'un bilgisayarları API kullanıyor 日志模式── daha basit, daha güvenilir──

### Görsel araç kullanmak. Görsel araç kullanmak.

> **【中文解读】**ChartAgent  giriş vizyuel araç调用:Agent "kesme bölgeyi (100,200,300,400) çıkartabilir, sonra OCR'yi araç调用 olarak kullanabilir.

ChartAgent (arXiv:2510.04514) grafik anlama için görsel araç kullanımı sunar: biçim, zoom, OCR, dış algılama çağrısı. Ajan "çeviri bölgeye (100, 200, 300, 400) çıkarabilir, sonra bir araç çağrısı olarak OCR çağrısı yapabilir. Alet metni iade eder; VLM mantıklamaya devam eder.

> ChartAgent  giriş vizyuel araçları调用用于图表理解:剪剪,缩放,OCR、调用外部检测──Agent "剪到区域 (100, 200, 300, 400) "ı dışarı çıkarıp OCR"ı araç olarak调用──工具返回文本;VLM 继续推理──

Bu örnekteki genelleştirmeler: işaret setini istekleme, bölge notasyonu ve dış algılama araçları hepsi aynı "bir araç çağrısı çıkart, yapılandırılmış bir yanıt al" şemasıyla uyumludur.

> Bu model de yayılabilir: toplama işaretleme göstergesi, bölge işaretleme ve dış denetim araçları aynı "çıktı, çıkış, araç kullanımı, alım yapılandırılmış yanıt" modüsüne uygun.

### 2026 yılındaki standartlar.

> **【拓展：多模态 Agent 基准全景】**ScreenSpot-Pro 测试 GUI 定位(open model ~85%,前沿 ~90%);VisualWebArena 测试端到端网页任务(open model ~20%,Gemini 3 Pro ~27%);AgentVista 2026 en zor基准, 12 个领域的真实工作流,前沿模型只有27-40%;WebArena/WebShop 已被前沿模型和──

- ScreenSpot-Pro. GUI'nin yerleştirilmesi 1k web ekran görüntüsüne. SOTA Qwen2.5-VL-72B ~85% Açık.
  Çeviri:Screenspot-Pro.                                                                                                                                                                                                                                                          
- VisualWebArena. Web görevleri (dükkan, forum, sınıflandırma reklamları). SOTA ~ 20% Açık. Gemini 3 Pro ~ 27%
  Çin dili:VisualWebArena。端到端网页任务(购物、论坛、分类广告)。开放 SOTA 约20%──Gemini 3 Pro 约27%──
- AgentVista (arXiv:2602.23166). 2026'da en zor standart. 12 alan arasında gerçekçi iş akışları. Sınır modelleri yüzde 27-40 puan alır; açık modeller yüzde 10-20 puan alır.
  Çin dilinde:AgentVista──2026 yılının en zor基准──跨 12 领域真实工作流──前沿模型 27-40%;开放模型 10-20%──
- WebArena / WebShop. Eski referanslar; sınır ile doymuş.
  Çeviri:WebArena / WebShop.

### Neden hala zor? Neden hala zor?

> **【中文解读】**Agent  performans botları:1) 细粒度视觉定位("点击小 X"在移动分辨率下经常失败);2) 长期规划(10 步后 Agent 偏离目标);3) 错误恢复(点击失败时检测和恢复缺乏训练数据);4) 跨页面上下文(跳转标签页或长表单丢失状态) ――研究方向包括记忆架构、、式重规划多样式验证──

Ajanın performansındaki boğazlar:

> Ajan 性能瓶:

1. "Küçük X'e tıklayın" genellikle mobil çözünürlükte başarısız olur.
   Çinçe Çevirimiçi:细粒度视觉定位──"点击小 X"在移动分辨率下经常失败──
2. 10 eylemden sonra ajan hedefi terk eder.
   Çöntem: 10 个动作后 Agent 偏离目标──
3. Hata kurtarma. Bir tıklama başarısız olduğunda (hatalı düğme), tespit + kurtarma nadiren eğitimli veridir.
   Çinçe Çevirimi: error restore──点击失败时(按错按),检测+恢复缺乏训练数据──
4. Sayfalar arası bağlam. Sekmeler veya uzun formlar arasında atlamak durumunu kaybeder.
   Çin Çeviri:跨页面上下文──跳转标签页或长表单丢失状态──

Araştırma yönleri: hafıza mimarileri, açık bir yeniden planlama, multimodal doğrulama (eğer bir eylem başarısı için ekran görüntüsü eşleşir).

> Araştırma yönleri: anı yapı, açıkça yeniden planlama, çok modellik denetleme,

### Başta taş inşa-it-it.

> **【中文解读】**毕业项目任务:构建一个计算机使用代理,能够读取预订网站模拟页面的HTML+截图,规划多步序列(搜索→选择→填表→提交),输出匹配动作模式的JSON动作,并对10个固定任务进行评估──

Son görev: bilgisayar kullanımı ajanı oluşturmak:

> 毕业项目任务:构建一个计算机使用代理,要求:

1. Bir rezervasyon sitesi sahte sayfasının HTML + ekran görüntüsünü okuyor.
   Çinçe Çevirimiçi:读取预订网站模拟页面的HTML + 截图──
2. Çok adımlı bir dizi planlar: arama → seç → doldur formu → gönder.
   中文翻译:规划多步序列:搜索→选择→填表→提交──
3. Eylem şemasıyla eşleşen JSON eylemlerini gönderir.
   Çinçe Çevirim:输出匹配动作模式的 JSON 动作.
4. - 10 görevi olan sabit bir parça ile değerlendiriyor.
   Çin Çeviri: 固定 10 个任务上评估──

Ders, gerçek bir tarayıcıya kolayca yayılabilecek bir asfalt kodu sağlar.

> 课程提供脚手架代码, gerçek tarayıcılara kolayca genişletilebilir.

## Çerçeveyi kullanın.
```figure
mm-agent-loop
```

## Kullan

`code/main.py`- Taşlı bir asfalt:

- Eylem şeması JSON tanımlaması (10 eylem).
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- Sahte tarayıcı durumu dikt olarak.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Ajan kemiri: alış, hareket, uygula, kemir.
  Çeviri:Agent 循环骨架:接收状态、输出动作、执行、循环──
- 10 görevli mini-benchmark (sentezik sayfalar) son-son başarıyı ölçmek için.
  Çinçe Çevirim: 10 任务迷你基准 (synthesis page)
- Bir eylem başarısız olduğunda hata kurtarma hokusu.
  Çinçe Çevirisi:动作失败时的错误恢复子──

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-multimodal-agent-designer.md`. Bilgisayar kullanım ürünü (domain, eylem seti, değerlendirme hedefi) göz önüne alındığında, tam ajan döngüsünü, hafıza stratejisini, yerleştirme modunu ve beklenen referans puanını tasarlar.

> 本课产 出 `outputs/skill-multimodal-agent-designer.md` Bilgisayar kullanım ürünleri (sektörler, hareketler, değerlendirmeler), tasarlanmış tam bir ajan döngüsü, hatıra stratejisi, konumlandırma modeli ve beklenen kılavuz oranı.

## Egzersizler.

1. Eylem şeması ile genişlet `screenshot_region`Hangi görevler yararlıdır?
   扩展动作模式,添加 `screenshot_region`工具(裁剪+缩放) ―― hangi görevler fayda sağlayacaktır?

2. AgentVista'yı okuyun (arXiv:2602.23166). En zor görev kategorisini ve neden sınır modelleri hala başarısız olduğunu açıklayın.
   阅读 AgentVista 论文──描述最困难的任务类别以及前沿模型仍然失败的原因──

3. Uzun uzayda hafıza sıkıştırması: ≤4 ekran görüntüsü canlı tutulan, herhangi bir sayı kaydedilen bir özet zinciri tasarlayın.
   长期记忆压缩:设计一个摘要链,保持 ≤4张截图活跃,任意数记录到日志──

4. Hata kurtarma hokunu oluşturun: eylem başarısız olduğunda (buton bulunamadı), ajan daha sonra ne yapar?
   构建错误恢复子:当动作失败 (按未找到) 当,Agent 下一步做什么?

5. Sadece ekran görüntüsü olan Claude 4.7 ile 10 web görevinde hibrit ekran görüntüsü + erişilebilirlik ağacı Qwen2.5 VL'yi karşılaştırın. Hangisi hangisiyle kazanır?
   Temiz bir şekilde kesilmiş Claude 4.7 ile karıştırılmış modunda Qwen2.5 VL'nin 10 web sayfasındaki görevlerde gösterdiği performans karşılaştırıldığında.

## Anahtar Terimler

| Term | What people say | What it actually means | 中文释义 |
|------|-----------------|------------------------|----------|
| GUI grounding | "Click coordinates" | Model outputs (x,y) for the target of an instruction on a screenshot | GUI 定位：模型输出截图上指令目标的 (x,y) 坐标 |
| Action schema | "Tool definitions" | JSON description of valid actions (click, type, scroll, drag) | 动作模式：有效动作的 JSON 描述 |
| Accessibility tree | "Structured DOM" | Machine-readable UI hierarchy from browser/iOS APIs | 无障碍树：来自浏览器/iOS API 的机器可读 UI 层级 |
| Hybrid agent | "Screenshot + tree" | Uses both image and structured info; more reliable than either alone | 混合 Agent：同时使用图像和结构化信息 |
| Visual tool use | "Zoom/crop/detect" | Agent calls external vision tools (OCR, detection) mid-plan | 视觉工具使用：Agent 在规划中调用外部视觉工具 |
| Summary-chain | "Memory compression" | Periodic text summaries replace long screenshot history | 摘要链：定期文本摘要替代长截图历史 |
| VisualWebArena | "E2E web bench" | 2024 benchmark for end-to-end web tasks | 端到端网页任务基准（2024） |
| AgentVista | "2026 hard bench" | 12-domain realistic workflows; even Gemini 3 Pro scores ~30% | 12 领域真实工作流基准，前沿模型仅约 30% |

## Daha fazla okumak

- [Cheng et al. — SeeClick (arXiv:2401.10935)](https://arxiv.org/abs/2401.10935)
- [Hong et al. — CogAgent (arXiv:2312.08914)](https://arxiv.org/abs/2312.08914)
- [You et al. — Ferret-UI (arXiv:2404.05719)](https://arxiv.org/abs/2404.05719)
- [ChartAgent (arXiv:2510.04514)](https://arxiv.org/abs/2510.04514)
- [Koh et al. — VisualWebArena (arXiv:2401.13649)](https://arxiv.org/abs/2401.13649)
- [AgentVista (arXiv:2602.23166)](https://arxiv.org/abs/2602.23166)
