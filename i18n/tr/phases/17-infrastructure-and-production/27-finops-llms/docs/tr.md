# LLM için FinOps  Birim Ekonomisi ve Çoklu Kiracı Atribuasyonu  LLM için FinOps  Birim Ekonomisi ve Çok Kiracılık

> Geleneksel FinOps LLM harcamalarında kesimler. Maliyetler kaynak zaman değil, token işlemler. Etiketler haritalamıyor  bir API çağrısı bir işlemdir, bir varlık değil. Mühendislik kararları (sürekli tasarım, bağlam penceresi, çıkış uzunluğu) finansal kararlardır. 2026 oyun kitabı bir gün önce enstrüman için üç atribut boyutuna sahiptir: kullanıcı başına (`user_id`) yer fiyatlandırması ve genişlemesi için görev başına (`task_id`+ `route`) ürün yüzey maliyetleri ve öncelikleri için, kiracılık (`tenant_id`) için birim ekonomisi ve yenilenme. Dört token katmanı  prompt, araç, bellek, cevap  bir kova saklar harcamak. Çoklu kiracı ürünler için uygulanma merdivi: kiracı başına oran sınırı (2-3x beklenen zirve, net 429 + tekrar deneme sonrası); günlük harcama limiti (1.5-3x sözleşmiş tavan; hız sıkıştırmayı tetikler + uyarı); harcama z puanı > 4'te (otomatik ara + çağrı açılan sayfa) kesintiler. Atribusiyon kalıpları: etiketleme ve toplamlama, telemetri-birleştirme (izleme-ID → faturalama; en yüksek doğruluk), örnekleme ve ekstrapolasyon, model tabanlı tahsis, olay kaynaklı, gerçek zamanlı akış. Birim metrik: çözülen sorgu başına maliyet, üretilen eser başına maliyet  $/M tokens değil. Geriye dönük etiketleme her zaman eksik; istek üzerine oluşturma aracı.

> **【中文解读】**传统 FinOps LLM 支出上失效成本是 Token 交易而非资源运行时间──工程决策──提示设计、上下文窗口、输出长度) 就是财务决策──2026 yılının Playbook 建议在第一天建立三个归因维度:用户按用户,任务按,租户按. 四个 Token 层──提示、工具、单位记忆、响应) 无法合并为一个桶──标标应为"解决的查询成本",而不是"百万个 Token 成本"──

> **【拓展：FinOps → LLM 成本优化】**LLM uygulamalarında, maliyet kontrolü çekirdeği zorluklardır. LLM + 量化部署可降低推理成本,模型路由, 简单任务用小模型、复杂任务用大模型) 可优化性价格,语义缓存可减少重调调. FinOps'un "在请求创建时就埋点" prensibi LLM'nin değerlendirilmesi için temel oluşturur.

**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cost-attribution simulator with kill switch) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 14 (Caching) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 14 (Caching)

>  **【前置】**学本节前 Lütfen önce bil:Fase 17·13(可观测性)、Fase 17·14(缓存)、云 FinOps 基础。LLM FinOps = 传统 FinOps 失效后的新方法。
>  **【类比】**LLM FinOps = "kullanım ücretlerine göre su elektrik ücretleri"。 geleneksel FinOps = 按服务器 uptime(标签=资产);LLM FinOps = 按代币交易(标签=交易)。三大归因维度(1 gün 必埋):user-per-user(席位定价)、per-task(产品成本)、per-tenant(单位经济)。四层代币(prompt/tool/memory/response)
> ️ **【易错点】**单位指标用$/M token is errõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõõ
**Time:** ~60 minutes | **时间:** ~60 minutes

## Öğrenme hedefleri

- Geleneksel FinOps'in (tag + seviyeler) LLM harcamaları neden kırıldığını ve üç yeni atribut boyutunu neden belirlediğini açıklayın.
  Çin dilinde: 訳:解释为什么传统FinOps (→ 层级) ⇒ LLM 支出上失效,并说出三个新归因维度──
- Dört token katmanını (sürekli, araç, bellek, yanıt) ve tek kutu faturalama neden maliyetleri gizlerse, listeleyin.
  Çinçe dilde: 列举四个标志层 (提示、工具、记忆、响应),以及为什么单桶计费产生误导――
- Çoklu kiracı bir ürün için bir uygulama merdiveni (sıfı → harcama limitı → öldürme anahtarı) tasarlayın.
  Çinçe Çevirimi: Design Execution阶梯(速率 -> 支出上限 -> 断开关) çok kiracı LLM 服务。
- $/M tokenleri yerine birim metrik ( çözülmüş sorgu / eser başına maliyet) seçin.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çev: Çeviri: Çev: Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Çev Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç

## Sorunlar. Sorunlar.

> **【中文解读】**传统 FinOps LLM 支出上失效的核心原因:LLM 成本是代币 交易而不是资源运行时间──标签(tags) Can't Directly Map API 调用是交易而非资产──工程决策(提示设计、上下文窗口、输出长度) 就是财务决策──账单显示40,000$,但你不知道:哪个租户花了多少,哪个产品功能驱动的是否有用的利用、是快速的膨胀还是工具调用还是记忆扩大导致的──

Hesabınızda 40.000 dolar yazıyor.
- Hangi kiracı harcadı?
- Hangi ürün özellikleri onu yönlendirdi.
- Kişisel bir kullanıcı kötüye kullanıyor mu?
- İster hızlı şişkinlik, ister alet çağrıları, isterse de hafıza güçlendirilmesi suçluydu.

Etiketler ve birleştirme, bulut kaynakları (EC2, S3) için hizmet sağlayıcı tarafında çalışır. Etiketler satır öğelerine yayılır. LLM API çağrıları otomatik olarak etiketlenmez.

## Konsepten bir şey.

### Üç atribut boyutu

**Per-user**(`user_id`): kim ne maliyet veriyor.Sit fiyatlarını belirler, genişleme konuşmaları yapar, elektrik kullanıcılarını tanımlar.

**Per-task**(`task_id`+ `route`): hangi ürün yüzeyi ne kadar maliyetlidir.

**Per-tenant**(`tenant_id`): hangi müşteri kârlı.

Üçü de ilk gün çağrı alanında.

### Dört simge katmanı

| Layer | Example | Typical % of total |
|-------|---------|---------------------|
| Prompt | system + user input | 40-60% |
| Tool | tool-call results fed back | 20-40% (agent workloads) |
| Memory | prior conversation / retrieved docs | 10-30% |
| Response | model output | 10-30% |

Dörtünü bir araya getirmek optimizasyonu kör eder.

### Yükleme merdiveni

> **【中文解读】**Çoğu kiracı ürünlerinin üç aşaması zorunlu aşama:(1) ırk sınırı kiracı başına 2-3x  beklenen zirve değer, geri dönüş 429 + Retry-After, kiracı 摩擦 ama hiç beklenmedik hesap hissetti;(2) 日支出上限 合同上限 1.5-3x 合同上限,触发时收紧率限制 + 告警客户成功团队;(3) Kill switch当支出 z-score > 4(相对租户基线) 时自动暂停租户,通知班,升级运维和客户成功;;

> **【拓展：LLM FinOps 的复合优化栈】**LLM FinOps'in karmaşık optimizasyonu(缓存 + 批处理 + 路由 + 网关) 叠加后的效果:(1) 缓存 L2(Phase 17·14) 约10x 更便宜的输入;(2) 批处理(Phase 17·15) 50% 折扣;(3) 路由到廉价模型(Phase 17·16) 60% 成本降低;(4) 网关效率(Phase 17·19) 冗余 + 重试──全叠加最优可降至朴素基线的约5-10%──大多数团队只启用了2-3杆,很少有团队叠加了四个.

1. **Rate limit**Kiracı başına. 2-3 kat beklenen zirve. 429'u geri getir.`Retry-After`Kiracı sürtüşmeyi görür, sürpriz hesabı yok.

2. **Daily spend cap**-Kartı: sıkılık oranı sınırı + müşteri başarısını uyarmak.

3. **Kill switch**İcatçı tabanına göre harcama z puanı > 4'e göre. Otomatik durak kiracı; çağrıda sayfa; operasyonlara tırman + CS.

### Atribu modelleri

- **Tag-and-aggregate**: metadata başlıkları; daha sonra toplayın.
- **Telemetry joiner**: izleri iz kimlikleri ile faturalama ile birleştirir. En yüksek doğruluk.
- **Sampling + extrapolation**%5-10% örnek, çarpma.
- **Model-based allocation**: geri dönüşü, maliyet sürücüsünü çıkarmak için.
- **Event-sourced**Bu nedenle, bu programın gerçek zamanlı olarak gerçekleşmesi için gerekli olan düzenlemeler de mevcuttur.
- **Real-time streaming**: tablo güncellemeleri alt saniye.

### X'e düşen maliyet birim metriktir

> **【中文解读】**$/M tokenleri ise tedarikçi dilidir. Ürün göstergesi olmalıdır: 1) Her çözümün destekleme çalışma tek maliyeti; 2) Her üretim yazı maliyeti; 3) Her başarılı ajan  görev maliyeti; 4) Her kullanıcı konuşması dakika maliyeti;

$/M tokenleri satıcı konuşuyor.

- Çözümlü destek biletinin fiyatı.
- Üretilen bir mal için maliyet.
- Başarılı bir ajan görevi için maliyet.
- Kullanıcı oturum dakikasındaki maliyet.

Ürün sonuçlarına maliyet bağlayın.

### Ücret atributı iz şekli

```
trace_id: abc123
  user_id: u_42
  tenant_id: t_7
  task_id: task_classify_doc
  route: model_haiku
  layers:
    prompt_tokens: 1800
    tool_tokens: 600
    memory_tokens: 400
    response_tokens: 150
  cost_usd: 0.0135
  cached_input: true
  batch: false
```

Her çağrıda yayınlayın. Veriler gölünde saklayın. Boyut başına toplayın. 17 · 13 aşama gözlemlilik yığınında bu yerleşir.

### Toplu tasarruf yığınları

Stack: cache + batch + route + gateway.
- Kaş L2 (Fase 17 · 14): ~ 10 kat daha ucuz giriş.
- Satır (Fase 17 · 15): %50 indirim.
- Ucuz model için rota (Fase 17 · 16): %60 maliyet azaltımı.
- Geçit verimliliği (Fase 17 · 19): redundansi + tekrar deneme.

En iyi durum: saf başlangıç oranının %5-10'u. Çoğu takımda 2-3 kaldıraç kullanılır; birkaç kişi dörtünü de toplar.

### Hatırlamalısın numaralar

- Atribusiyon boyutları: kullanıcı başına, görev başına, kiracı başına.
- Dört token katmanı: prompt, araç, bellek, cevap.
- Öldürme düğmesi: z puanı> 4 kullan.
- Birim metrik: çözülen sorgu başına maliyet, $/M tokenleri değil.
- Yüklü optimizasyonlar: ~5-10% baseline mümkün.

## Çerçeveyi kullanın.
```figure
i4-spend-ladder
```

## Kullan

`code/main.py`Üç katlı uygulama merdivenle çoklu kiracı bir LLM hizmetini simüle eder.

> `code/main.py`Üç katlı uygulama merdivenle çoklu kiracı bir LLM hizmetini simüle eder.

> `code/main.py`Üç katlı uygulama merdivenle çoklu kiracı bir LLM hizmetini simüle eder.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-finops-plan.md`. Ürün ve ölçek göz önüne alındığında, atribut şeması ve uygulanma merdiveni tasarlar.

> 本课产 出 `outputs/skill-finops-plan.md`. Ürün ve ölçek göz önüne alındığında, atribut şeması ve uygulanma merdiveni tasarlar.

## Egzersizler.

1. Çık .`code/main.py`- Öldürücü ne zaman ateş eder?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`断开关在什么z-score下触发? nasıl yanlış haberleri önleyebilirim?
2. Bir kiracı başına, görev başına maliyetle bir tablo tasarlayın.
   Çinçe Çevirimiçi: Design per rent户, per task 費用儀表板.
3. En büyük kiracı ünite ekonomisi negatif.
   Çinçe Çevirisi: 你最大的租户单位经济学为负.
4. Destek ürünü için çözülmüş bir bilet başına maliyet hesaplama: 3M token/biletin, ~800 bilet/gün, GPT-5 önbelleğe alınan oran.
   Çinçe Çevirisi: hesaplama destek ürünlerinin her çözülme iş tek maliyeti: 3M token/工单, yaklaşık 2.5 defa tekrar deneyin.
5. Geriye dönük etiketlemeyi ne zaman kabul edilebilir?

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Per-user attribution | "user-level cost" | `user_id` stamped on every call |
| Per-task attribution | "feature cost" | `task_id` + `route` identify product surface |
| Per-tenant attribution | "customer cost" | `tenant_id`; drives unit economics |
| Four token layers | "cost layers" | prompt + tool + memory + response |
| Rate limit | "429 guard" | Per-tenant ceiling enforced at gateway |
| Daily spend cap | "daily ceiling" | Tenant-scoped budget with alert |
| Kill switch | "auto-pause" | Spend z-score > 4 triggers auto-suspension |
| Cost per resolved | "product unit metric" | Cost tied to product outcome, not tokens |
| Telemetry joiner | "trace-to-billing" | Highest-accuracy attribution pattern |
| Stacked optimization | "cache+batch+route+gateway" | Compounding savings to ~5-10% baseline |

## Daha fazla okumak

- [FinOps Foundation — FinOps for AI Overview](https://www.finops.org/wg/finops-for-ai-overview/)
- [FinOps School — Cost per Unit 2026 Guide](https://finopsschool.com/blog/cost-per-unit/)
- [Digital Applied — LLM Agent Cost Attribution 2026](https://www.digitalapplied.com/blog/llm-agent-cost-attribution-guide-production-2026)
- [PointFive — Managed LLMs in Azure OpenAI](https://www.pointfive.co/blog/finops-for-ai-economics-of-managed-llms-in-azure-open-ai)
