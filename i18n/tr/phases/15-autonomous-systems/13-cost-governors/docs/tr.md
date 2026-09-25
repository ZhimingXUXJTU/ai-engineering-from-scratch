# Hareket bütçeleri, İterasyon Kapıları ve Maliyet yöneticileri

> Orta büyüklükte bir e-ticaret ajansının aylık LLM maliyeti $1,200 to $Bu, fiyatlama hatası değil. Bu, yeni bir döngü bulmuş ve içindeki harcamaları sürdüren bir ajan. Microsoft'un Ajan Yönetimi Araç Kütleği (2 Nisan 2026) bu sınıfa karşı savunmayı kodlaştırır: talep başına`max_tokens`, görev başına token ve dolar bütçeleri, günlük / aylık limitler, iterasyon limitleri, katılımlı model yönlendirme, hızlı önbelleğe girme, bağlam pencereleri, pahalı eylemler için HITL kontrol noktaları, bütçe ihlalinde anahtarları öldürme. Anthropic'in Claude Code Agent SDK farklı isimlerle aynı primitifleri gönderir. Finansal hız limitleri  örneğin, erişimi 10 dakikada > $ 50'e kesin  aylık limitlerden daha hızlı yakalamak döngüler.

> **【中文解读】**Orta tipi E-Ticaret Ajanın Aylık LLM Ürünleri$1,200 跳到 $4.800── bu fiyat hata değil── bu Ajan yeni döngü bulup devamlı harcamalarıdır── Microsoft'un Ajan Yönetimi Araç Kütleği(2026 yılının 4 月 2 日) bu tür savunmaları: her istek için düzenledi`max_tokens`、 her görev belirti 和美元预算、每日/月上限、代上限、分层模型路由、提示缓存、上下文窗口、昂贵动作上 HITL 检查点、预算违反时的终止开关。Anthropic's Claude Code Agent SDK 以不同名称出货相同原语──金融速度限制例如10分内 >$50 切断访问比月度上限更快捕获循环──

> **【拓展：单一上限不够 → 分层栈】**失败模式与时间尺度需要应对:5 秒重试的失控循环 (Hızlılık sınırlaması) 工作的缓慢泄漏 (Hızlılık sınırlaması) 工作的缓慢泄漏 (Hızlılık sınırlaması) 工作的缓慢泄漏 (Hızlılık sınırlaması) 工作的缓慢泄漏 (Hızlı bilgi) 工作的缓慢泄漏 (Hızlı bilgi) 工作的缓慢泄漏 (Hızlı bilgi) 工作的缓慢泄漏 (Hızlı bilgi) 工作的缓慢泄漏 (Hızlı bilgi) 工作的缓慢泄漏 (Hızlı bilgi) 工作的缓慢泄漏 (Hızlı bilgi) 工作的缓慢泄漏 (Hızlı bilgi) 工作的缓慢泄漏 (Hızlı bilgi) 工作的缓慢泄漏 (Hızlı bilgi) 工作的缓慢泄漏 (Hızlı bilgi) 工作的缓慢泄漏 (Hızlı bilgi) 工作的缓慢泄漏 (Hazlı bilgi) 工作的缓慢泄漏 (Hazlı bilgi) 失败模式和时间的缓慢性) 缓慢性 (Hazlı) 缓慢性性) 缓慢泄漏 (Hazlı bilgi) 缓慢性) 缓慢性 (Hazli bilgi) 缓慢性 (Hazli bilgi) 缓慢性) 缓慢性 (Hazli bilgi) 缓慢性) 缓慢性 (Hazli bilgi) 缓慢性 (Hazli bilgi) 缓慢性) 缓慢性 (azide) 缓慢性 (azide)

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, layered cost-governor simulator) | **语言:** Python（标准库，分层成本治理器模拟器）
**Prerequisites:** Phase 15 · 10 (Permission modes), Phase 15 · 12 (Durable execution) | **前置知识:** Phase 15 · 10（权限模式），Phase 15 · 12（持久执行）
**Time:** ~60 minutes | **时间:** ~60 分钟

>  **【前置】**Önemli olan, bu, bir süre önce yapılan bir işlemin sonucunda yapılan bir işlemin sonucunda gerçekleşecek.
>  **【类比】**Ücret yöneticisi = "Agent'in kredi kartı oranı"──普通 LLM 调用 = 刷卡(每次小钱);Agent 进入死循环 = 盗刷(一夜烧光)──防御分层:(1) 速度限制10分钟 >$50 切断（防失控）；(2) 每日上限——$200/天(防慢泄漏);(3) 月度上限$3000/月（防坏发布）；(4) 单任务上限——$5/ görev (防单次任务爆炸)
> ️ **【易错点】**Sadece aylık sınırın üstünde hız sınırı yoktur → Bir gece yakıl bir aylık bütçeyi bulmuyor.

## Sorunlar. Sorunlar.

> **【中文解读】**Çekim kontrolcüleri) Kontrol ve kısıtlama Agent'in kaynak tüketimi Ana olarak API 调用费用和代币使用量──没有成本控制器的代理可能在循环或低效执行中产生巨额账单──三种控制策略:(1) 预算上限硬性代币/费用限制;(2) 速率限制每分/每小时调用上限;(3) 效率门控成本/收益比恶化时暂停──

> **【拓展：cost governors】**Çözümler arasında şunlar yer alır: 1) OpenAI'nin maksimum_output_tokens  limiti; 2) Anthropic'in kullanım takip API; 3) Üçüncü taraf araçlar Helicone ve Braintrust gibi maliyet izleme sistemi; best practice is for each task setting a clear cost up limit;;

Özerk ajanlar her dönüşte gerçek para harcıyor.

> Özgür ajan her turda gerçek para harcar.

Bir chatbot'un kötü çıkışı kötü bir cevapdır; bir ajansın kötü döngüsü bir fatura. Başarısızlık modunun endüstri belgelediği terimi "Cüzdanı reddetmek"  ajan mantık yürütmeye devam eder, araç çağrısını sürdürür, faturalama yapmayı sürdürür ve hiçbir şey onu durdurmaz çünkü hiçbir şey için tasarlanmamıştır.

> 聊天机器人错误输出是一条错误回复;Agent's errore cycle is a bill. 行业记录的失败模式术语是"Wallet'ı reddetmek"Agent 持续推理、持续调用工具、持续计费, hiçbir şey onu engellemiyor, çünkü hiçbir şey engellemek için tasarlanmıştır.

Bu, bir sayı değil, farklı zaman ölçeklerinde ve ayrıntılılıklarda bir dizi sınırdır: talep başına, görev başına, saat başına, gün başına, ay başına. İyi tasarlanmış bir yığın, birkaç dakika içinde kaçan bir döngü, saatler içinde yavaş bir sızıntı ve bir gün içinde kötü bir serbest bırakmayı yakalar. Aynı yığın, ajan uzun uzayda ve özerk olduğunda bütçeyi tutar.

> Düzeltme bir rakam değil. Zamanın farklı ölçüm ve ölçümlerinin sınırlamasıdır. Her istek, her görev, her saat, her gün, her ay. İyi tasarlanmıştır.

> **【中文解读】**Bu bölümde AI Ajanının temel kavramı ve gerçekleştirme yöntemleri ele alınıyor. Ajan, çevreyi gözlemleyebilen, kararlar verebilen, eylemleri gerçekleştiren ve hedefleri gerçekleştirene kadar döngülenebilen LLM tarafından yönlendirilmiş bir otonom sistemdir.

Bu bir mühendislik dersi: matematik önemsiz, disiplin takımların başarısız olduğu yerdir. Aşağıdaki sınırların listesi Microsoft Ajan Yönetim Araç Kütübesinde veya Anthropic Claude Code Agent SDK dosyalarında isimlendirilmiştir.

> Bu bir teknik ders: Matematik sıradan, Kurallar bir takım başarısızlığının bir parçasıdır. Aşağıdaki kısıtlamalar listesi tümü Microsoft Ajan yönetim araç kümesi veya Anthropic Claude Code Ajan SDK 文档中命名──

## Konsepten bir şey.

### Ücret yöneticisi yığın.

1. **`max_tokens` per request.**Basit.Bir çağrı sınırsız bir bitirme yayınlamasını engeller.
   Çeviri:**每请求 `max_tokens`。**简单――单次调用发发出无限补全――
2. **Per-task token budget.**Tüm koşuda N simgesini aşmayın.
   Çeviri:**每任务 token 预算。**Tüm işlemi N'den fazla değil.
3. **Per-task dollar budget.**Tokenler gibi ama para biriminde.`max_budget_usd`Claude Code'da.
   Çeviri:**每任务美元预算。**Token ile aynı ama para birimi ile aynı.`max_budget_usd`- Evet.
4. **Per-tool call cap.**N' dan fazla değil`WebFetch`Çağrılar, N `shell_exec`Telefonlar vb.
   Çeviri:**每工具调用上限。**N                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `WebFetch`调用  个`shell_exec`调用等──
5. **Iteration cap (`max_turns`).**Toplam ajan döngü iterasyonları; sonsuz akıl döngüslerini önler.
   Çeviri:**迭代上限（`max_turns`）。**总 Agent 循环代数; sınırsız önerilerden kaçınmak
6. **Per-minute / per-hour / per-day / per-month cap.**Çevrimiş pencereler, farklı zaman ölçeklerinde sızıntılar algılar.
   Çeviri:**每分/时/日/月上限。**滚动窗口──在不同时间尺度捕获泄漏──
7. **Financial velocity limit.**Örneğin, "Eğer 10 dakika içinde 50 dolardan fazla harcadıyorsanız, erişiminizi kesin".
   Çeviri:**金融速度限制。**Örneğin, "Eğer 10 dakikada 50 dolardan fazla harcadıysa, ziyaretinizi kesin".
8. **Tiered model routing.**Küçük bir model için varsayılan; sınıflandırıcı görevi gerekli gördüğünde daha büyük bir model için yükselir.
   Çeviri:**分层模型路由。**默认小模型; yalnızca sınıflandırma biçimindeki değerli görevler daha büyük modellere yükseltilmelidir.
9. **Prompt caching.**Sistemi hızlı ve sabit bağlamı, sağlayıcı önbelleğinde depolanır; yeniden gönderme için token maliyeti sıfıra yakın.
   Çeviri:**提示缓存。**Sistem göstergesi ve sabitleme üzerine aşağıdaki yazılar tedarikçi depolama; yeniden yüklenmiş token
10. **Context windowing.**Etkin bağlamı bir eşiğin altında tutmak için kompaktleştirme / özetleme; doğrudan token maliyetleri azaltma.
    Çeviri:**上下文窗口。**压缩/摘要保持活跃上下文低于值;直接代号 成本降低──
11. **HITL checkpoints on expensive actions.**Pahalı olduğu bilinen bir eylemden önce (uzun araç çağrısı, büyük bir indirme, pahalı bir model yükseltmesi) insan dokunuşunu gerektirir.
    Çeviri:**昂贵动作上的 HITL 检查点。**Bu nedenle, bu tür bir uygulamaların kullanımı ve kullanımı için çok daha fazla ücret talep edilmektedir.
12. **Kill switch on budget breach.**Sessiyon herhangi bir kapalı ateşlerken sona erer. Kapalı kaydedilir; ayrı bir yeniden etkinleştirilmiş yol gerektirir.
    Çeviri:**预算违反时终止开关。**任一上限触发时会话停止──上限被记录;需要单独重新启动路径──

### Neden bir kapı değil, bir yığın?

Tek bir aylık kap, kaçan ajanı sadece cüzdanın kaybolmasından sonra yakalar. Tek bir istek kap, oturum düzeyinde hiçbir şey yakalamaz. Farklı başarısızlık modları farklı zaman ölçeklerini gerektirir:

> 单一月度上限只在钱包空后捕获失控代理. 单一每请求上限在会话级上没有捕获.

- **Runaway loop**(Agent 5 saniyelik bir tekrar deneme sırasında sıkıştı): Hız sınırı tarafından yakalanmış.
  Çeviri:**失控循环**(Agent 5 saniyelik çekim): Yakalanma hızı sınırlandırılması
- **Slow leak**(öğütçi görev başına beklenen işi 2 katına çıkarır): günlük sınırlama ile yakalanır.
  Çeviri:**缓慢泄漏**(Agent Her görev için 2x 预期工作):
- **Bad release**(yeni versiyon 5x token kullanıyor): haftalık / aylık sınırlama ile yakalanmış.
  Çeviri:**坏发布**(New Version with 5x token): 每周/月上限捕获──
- **Legitimate surge**(gerçek talep, bir hata değil): açık bir kayıt ile saat / gün kapalı tarafından yakalanmış.
  Çeviri:**合法激增**(真实需求,非 bug):小时/日上限带清晰日志捕获──

### Claude Code'un bütçe yüzeyi
### Harness bütçe yüzeyi

Claude Code Agent SDK (ağcı belgeleri) açıklıyor:

> Claude Code Agent SDK 暴露(公开文档):

- `max_turns` İterasyon kapısı.
  Çeviri:`max_turns`Üst sınır.
- `max_budget_usd` Dolarlık sınırlama; aşıklıkta kürtaj.
  Çeviri:`max_budget_usd`美元上限;违反时会话中止──
- `allowed_tools`- Ne ?`disallowed_tools` alet aletleri ve deniller.
  Çeviri:`allowed_tools`- Ne ?`disallowed_tools` tool allow list and reject list.
- Özel maliyet hesaplama için araç kullanmadan önce kaçağı noktaları.
  Çeviri: 子点用于自定义成本核算.

İzin modu merdivenine (Deneyim 10) birleştirin.`autoMode`Oturma olmadan`max_budget_usd`Antropic açıkça otomatik modun bütçe kontrollerini gerektiren çerçevesini oluşturur; sınıflandırıcı maliyetle ortogonaldır.

> Hakkın Örgütü (Hükümet)`max_budget_usd``autoMode`会话是未治理的自主──Antropic 明确将自动模式 框定为需要预算控制;分类器与成本正交──

### AB AI Yasası, OWASP Ajan Top 10

Microsoft'un Ajan Yönetimi Araç Kütleği, OWASP Ajan Top 10 ve AB AI Yasası'nın 14 (insan denetimi) maddesindeki gereksinimleri kapsar.

> Microsoft'un Ajan Yönetimi Araç Kütleği  OWASP Ajan Top 10 ve AB AI Fasalı 14 条  İnsan İzleme) Gereksinimleri  EU Üretim,日志 kayıt ve üst sınırlı uygulama için seçilebilir değildir

### Görülmüştür .$1,200 → $4800 dava gözlemlendi.$1,200 → $4.800 olay

Microsoft dosyalarında gerçek durum: yeni bir araç eklendiğinde aylık maliyetleri üç katına çıkmış bir e-ticaret ajansı.

> Microsoft'un dosyasındaki gerçek örnek: Bir e-ticaret ajanı yeni araç eklemenin maliyetinin üç katına çıkması

Bu araç, ajanın her oturum sırasında sipariş durumunu anketlemesine izin verdi. Çaplak algılama yok. Her araç başına bir kaplama yok. Haftadan haftaya artışla ilgili bir uyarı yok. Düzeltme bir araç başına bir kaplama ve günlük büyüme uyarısıydı. Bu bir şablon: her yeni araç yüzeyi yeni bir potansiyel döngüdür; her yeni araç kendi kaplamasına ve kendi uyarısına ihtiyaç duyar.

> Bu araç, Ajan'a her toplantı sırasında sırayla sipariş durumunu sormayı sağlar.

## Çerçeveyi kullanın.
```figure
cost-governor-stack
```

## Kullan

`code/main.py`simülasyonlu ajan birkaç dönüşten sonra bir oylama döngüsüne sürüklenir; katlı yığın, hız penceresinde yakalarken tek bir aylık kaplama birkaç gün sonra ateş etmez.

> `code/main.py`模拟有和无分层成本管理的代理 运行──模拟代理在某些轮次后漂移到轮询循环;分层在速度窗口内捕获它,而单一级上限直到几天后才触发──

## İndirin . Ürünler .

`outputs/skill-agent-budget-audit.md`Ödemelenen ajanların görevlendirilmesi için maliyet yöneticisi yığınını denetlemektedir ve eksik katmanları işaretler.

> `outputs/skill-agent-budget-audit.md`审计提议的代理部 部署的成本管理并标记缺层──

## Egzersizler.

1. Çık .`code/main.py`Seçim döngüsü trajektöründe iterasyon kapağından önce hız sınırı ateşlerini onaylayın. Şimdi hız sınırı etkisizleştirin ve iterasyon kapağı onu yakalamadan önce ajanın ne kadar "harcadığını" ölçün.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ Kontrol hızının, sorgu döngüsü yolunun 代上限前触发── ❖ şimdi kullanım hızının sınırlandırılması ve ölçümleri ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖

2. Bir tarayıcı ajansı için her araç için bir kap seti tasarlayın (Deneyim 11). Hangi araç en sıkı kap ihtiyacı vardır? Hangi araç risk olmadan sınırsız çalışabilir?
   Çinçe Çevirimi: Çevirici Ajan (第 11 课) Design Per Tool                                                                                                                                                                                                                                                    

3. Microsoft Ajan Yönetim Araç Kütü Dokümanlarını okuyun. Her kapak türü araç kit isimlerini listelenin. Her birini başarısızlık modlarından birine (kaynak döngüsü, yavaş sızıntı, kötü yayın, yükseliş) haritasına yerleştirin.
   Çinçe Çevirimi:阅读Microsoft Agent Governance Toolkit 文档。列出工具包命名的每个上限类型──将各映射到失败模式之一(失控循环、缓慢泄漏、坏发布、激增) 

4. Gerçekçi bir görev için bir gece boyunca gözden geçirilmemiş bir çalışmanın fiyatı (örneğin "repoda 50 işlem ele alın").`max_budget_usd`2x'i haklı çıkarın.
   Çinçe Çevirimiçi:为真实任务 (例如"分类 50 个仓库问题")`max_budget_usd`2x.. 2x.. 2x.. 2x..

5. Claude Code's'ın `max_budget_usd`Bu nedenle, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre sonra, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir süre, bir
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`max_budget_usd`Bu yüzden, bu konudaki tüm maliyetleri karşılamak için, bir tasarım yapın.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|---|---|---|
| 术语 | 通俗说法 | 实际含义 |
| Denial of Wallet | "Runaway bill" | Agent loop generating spend with no cap to stop it |
| Denial of Wallet | "失控账单" | 无上限阻止的 Agent 循环产生花费 |
| max_tokens | "Per-request cap" | Ceiling on a single completion's size |
| max_tokens | "每请求上限" | 单次补全大小上限 |
| max_turns | "Iteration cap" | Ceiling on agent loop iterations in a session |
| max_turns | "迭代上限" | 会话中 Agent 循环迭代数上限 |
| max_budget_usd | "Dollar kill switch" | Session cost cap; aborts on breach |
| max_budget_usd | "美元终止开关" | 会话成本上限；违反时中止 |
| Velocity limit | "Rate cap" | Limit on spend per short window (e.g., $50 / 10 min) |
| 速度限制 | "速率上限" | 短窗口花费限制（例如 $50/10 分钟） |
| Tiered routing | "Small model first" | Cheap model default; escalate only when classifier warrants |
| 分层路由 | "小模型优先" | 默认廉价模型；仅当分类器批准时升级 |
| Prompt caching | "Cached system prompt" | Provider-side cache reduces re-send token cost to near zero |
| 提示缓存 | "缓存系统提示" | 提供商侧缓存将重发 token 成本降至接近零 |
| HITL checkpoint | "Human approval gate" | Human tap required before expensive action |
| HITL 检查点 | "人类批准门" | 昂贵动作前需人类点击 |

## Daha fazla okumak

- [Anthropic Claude Code Agent SDK — agent loop and budgets](https://code.claude.com/docs/en/agent-sdk/agent-loop) `max_turns`- Evet .`max_budget_usd`, araçları kullananlar.
  Çeviri:`max_turns`- Evet.`max_budget_usd`、工具允许列表──
- [Microsoft Agent Framework — human-in-the-loop and governance](https://learn.microsoft.com/en-us/agent-framework/workflows/human-in-the-loop) maliyet yöneticisi kontrol noktaları.
  Çeviri: cost治理器检查点
- [Anthropic — Claude Managed Agents overview](https://platform.claude.com/docs/en/managed-agents/overview) tedarikçi tarafından maliyet kontrolü.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Anthropic — Prompt caching (Claude API docs)](https://platform.claude.com/docs/en/prompt-caching)- Önbelleğe alma mekanizması.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- [Anthropic — Prompt caching (Claude API docs)](https://platform.claude.com/docs/en/build-with-claude/prompt-caching)- Önbelleğe alma mekanizması.
- [Anthropic — Measuring agent autonomy in practice](https://www.anthropic.com/research/measuring-agent-autonomy) Uzun üfüre sahip ajanlar için maliyet profili.
  Çinçe Çevirisi:长程 Ajanın maliyet arşivleri
