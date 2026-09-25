# SRE AI için  Çoklu ajanlar olay tepkisi, Runbooks, Tahminci tespit 

> AI SRE, araştırma, belgeleme ve koordinasyon aşamalarını otomatikleştirmek için RAG üzerinden altyapı verilerine (loglar, çalıştırma kitapları, hizmet topolojisi) dayalı LLM'leri kullanır. 2026 mimarlık örneği, bir denetmen tarafından koordine edilen çoklu ajan orkestrasyonu  uzman ajanlar (loglar, metrikler, çalıştırma kitapları); AI hipotez ve sorular önerir, insanlar yargı çağrılarını onaylar. Datadog Bits AI ve Azure SRE Agent bunu yönetilen ürünler olarak gönderir. Çalışma kitapları gelişmektedir: NeuBird Hawkeye karşıt değerlendirmeyi kullanır (iki model aynı olayı analiz eder; anlaşma = güven, anlaşmazlık = belirsizlik); ekip değişiklikleri boyunca operasyonel hafızan kalır. Otomatik tedavi dikkatli kalır: Yapay zeka önerir, insanlar onaylar. Tamamen özerk eylem dar (başlangıç kapsülü, geri dönüş özel dağıtım) sıkı koruma rayları ile  "settin ve unut" satan herkes aşırı satış yapıyor. Yeni gelişen sınır: olay öncesi tahmin. MIT araştırmaları, tarihsel kayıtlar + GPU temp + API hata kalıpları üzerine eğitimli bir LLM'nin, %89'ın 10-15 dakika erken kesinti olacağını öngördüğünü bildirmektedir. Projection: İşletme LLM'lerinin %95'i 2026 sonuna kadar otomatik olarak başarısızlığa uğramış olacak.

> **【中文解读】**Bu bölümde AI'nin SRE  pratikLLM  servislerinin istasyonları güvenilirlik mühendislik yöntemleri hakkında bilgi edindiler.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy multi-agent incident triage simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 13 (Observability), Phase 17 · 24 (Chaos Engineering) | **前置知识:** Phase 17 · 13 (Observability), Phase 17 · 24 (Chaos Engineering)

>  **【前置】**Önemli bir ders: 17·13(可观测性)  17·24(混沌工程) SRE 基础(runbook/incident 响应) AI SRE = LLM 加持的故障响应──
>  **【类比】**AI SRE = "AI 急诊医生"。多 Agent 编排:日志 Agent+指标 Agent+runbook Agent 协调;AI 提假设+查日志,人类批准判断。Datadog Bits AI、Azure SRE Agent 是托管产品。NeuBird Hawkeye 用对抗评估(两模型同分析事件,一致=高置信)。自动修复保持谨慎:AI 建议+人批准。前沿:预故障预测(MIT 用历史日志+GPU 温度+API 错误提模式预测 89% 故障 10-15 分钟)。
**Time:** ~60 minutes | **时间:** ~60 minutes

## Öğrenme hedefleri

- Çoklu ajanlı AI SRE mimarisini çiz: denetçi + uzman ajanlar (loglar, metrikler, çalıştırma defterleri) + insan onay kapısı.
  Çine dilinde: 図制多 代理 AI SRE 架构: 主管 + 专业 Agent(日志、指标、运行手册)
- Otomatik düzeltmenin neden geniş değil (önce yapılandırma hizmeti) dar olduğunu açıklayın (baştan başlatma kapsülü, geri yükleme).
  Çinçe Çevirim: Neden otomatik olarak yeniden yapılandırmak geniş değilse, kısıtlı bir çerçeveye sahip olması gerektiğini açıklayın.
- Karşılıklı değerlendirme modelini (NeuBird Hawkeye) isimlendirin: iki model anlaşılır = güven; anlaşmazlık = yükseliş.
  Çinçe Çevirimi: ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎
- MIT'in %89 erken tespit sonucu ve operasyonel kısıtlamaları alın: Aksiyon olmadan tahminler sadece araç tablosudur.
  Çinçe çevirisi: MIT'in 89% 早期检测结果和运维约束:无历史基线的预测不可行──

## Sorunlar. Sorunlar.

> **【中文解读】**AI SRE'nin temel anlayışı:2026 yıl, olay araştırmasının ilk 20 dakikası otomatikleştirilmekle birlikte, son olarak dağıtılan uygulamalara ilişkin DATADOG'lar kullanımı için RAG +  araçları kullanılmıştır.

> **【拓展：AI SRE 产品市场】**2026 yıl AI SRE  ürünleri:(1) Datadog Bits AIDatadog 内部托管 SRE copilot;(2) Azure SRE AgentAzure 原生;(3) NeuBird Hawkeye对抗性评估((2 model bağımsız analiz aynı olay,一致=高置信,不一致=升级) + 操作记忆(post-mortem 存入量 DB);(4) PagerDuty AIOps分类 + 去重;5)(Incident.io Autopilot事件指挥官 + 协调。MIT 2025 Araştırmaları gösterir, GPULLM 在历史志 + 温度 + API 错误模式上训练,可在 10-15 分钟 分前预测机 89% 的停滞──

Bir çağrı mühendisi sabahın 3'ünde "Kavda yüksek hata oranı" diye çağrılır. Datadog, Loki, üç çalıştırma defteri, dağıtım günlüğünü kontrol ederler. 30 dakika sonra temel nedeni KV önbelleği tırmanışından vLLM OOM olduğunu fark ederler. Kapsulunu yeniden başlatırlar; hata temizlenir.

2026'da bu soruşturmanın ilk 20 dakikası otomatik hale gelir. Son kullanımlara ilişkin, son yayımlara ilişkin, çalıştırma kitaplarına karşı eşleşen servis kayıtlarını gruplandırmak  hepsi RAG + araç kullanımıdır. Gözetim altındaki bir ajan, ilk geçiş triajını yapabilir ve insan Datadog'u açmadan önce bir hipotez sunabilir.

Tamamen otonom bir iyileştirme farklı bir problem. Kapsul: güvenli yeniden başlat. Skalalı GPU havuzu: güvenli eğer politika izin verir. Hizmet yeniden yapılandır: kesinlikle değil. Disiplin dar çizgi çizmektedir.

## Konsepten bir şey.

### Çoklu ajan mimarisi

> **【中文解读】**Çoğu Agent AI SRE 架构:Supravyör olayları bölmek için sorgu, uzmanlaştırma için göndermek için Sorgu Ajanı 日志 Ajanı 搜索日志、指标 Ajanı 查询 PromQL、Runbook Ajanı 检索文档) ❖Supravyör 综合,向人类呈现假设 + 证据──人类批准或重定向──安全自动修复范围:重启 Pod、回滚特定部署、预批准范围内扩展池──不安全范围:更改服务拓、更改资源限制、部署新代码、更改 IAM──

```
          Incident
             │
             ▼
        Supervisor
        /    |    \
       ▼     ▼     ▼
  Log agent  Metric agent  Runbook agent
       │     │     │
       └─────┴─────┘
             │
             ▼
        Hypothesis + evidence
             │
             ▼
        Human approval
             │
             ▼
        Action (narrow set)
```

Gözetmen olayı alt sorgulara ayırır. Uzman ajanlar araç erişimine sahiptir (log arama, PromQL, belge kurtarma). Gözetmen hipotezi + kanıt sunar, insanlara sunar. İnsan onaylar veya yönlendirir.

### Otomatik düzeltme kapsamı

> **【拓展：AI SRE 自动修复的安全边界】**AI SRE otomatik olarak değiştirilen güvenlik sınırı ayrımı: güvenlik(sıklık aralığı)  yeniden başlatma Pod、回滚特定部署、预批准范围内扩展池、启用预批准功能旗──不安全(广范围) 更改服务拓、修改资源限制、部署新代码、更改 IAM、修改数据库── herhangi bir iddia "saitin ardından unutulmuş" tedarikçi güvenliği aşırı bir vadede bulunmaktadır.

**Safe (narrow)**: başlatma modülü, belirli dağıtımları geri çevirme, önceden onaylanmış sınırlar içinde ölçekleme havuzu, önceden onaylanmış özellik bayrağını etkinleştirme.

**Not safe (broad)**: hizmet topolojisini değiştirmek, kaynak sınırlarını değiştirmek, yeni kodlar yerleştirmek, IAM'i değiştirmek, veritabanlarını değiştirmek.

"Sett it and forget it" satılan herkes aşırı satıyor.

### Karşılıklı değerlendirme (NeuBird Hawkeye)

İki model aynı olayı bağımsız olarak analiz eder. Eğer kök nedenleri konusunda anlaşırlarsa, güven yüksek olur. Eğer anlaşmazlıkları varsa, her iki hipotez de görünürken insana kadar yükselir.

### İşlem belleği

Ekip döngüsü, geleneksel SRE  kabile bilgisi yaprağının sessiz öldürülmesidir. AI SRE, bir vektör DB'de çalışma kitapları + post-mortemleri depolar; ajanlar her yeni olayda geri alırlar. Yeni mühendisler katıldığında, AI'nin tam tarihi vardır.

### Olay öncesi tahmin

MIT 2025 araştırması: Tarih kayıtları, GPU sıcaklıkları, API hata kalıpları üzerine eğitim alan LLM, test setinde gerçekleşmeden 10-15 dakika önce kesintilerin% 89'unu öngördü.

Gerçeklik kontrolü: etkinleştirilmemiş tahminler araç tablosudur. Operasyonel soru "Önümüze baktığımızda ne yapıyoruz?" önleyici boşaltma mı? Pager mi? Otomatik ölçeklendirme mi? Cevap politika özel.

### 2026 yılında ürünler

- **Datadog Bits AI**Datadog'un içinde SRE'nin yardımcı pilotunun yönetimi.
- **Azure SRE Agent** Azure doğası.
- **NeuBird Hawkeye** karşıt değerlendirme + işletim hafızası.
- **PagerDuty AIOps** triaj + deduplasyon.
- **Incident.io Autopilot** olay komutanı + koordinasyon.

### Kod olarak çalıştırma defterleri

> **【拓展：AI SRE 实施路径】**AI SRE'nin uygulanma önerileri: 1) önce yapılandırılmamış çalıştırma defteri yapılandırılmış bir işaretleme olarak dönüştürülür; 2) karşıdurma değerlendirmesini gerçekleştirir; 2) aynı olayı analiz eden iki bağımsız modelin karşıdurma değerlendirmesini gerçekleştirir; 3) operasyon hafızasını oluşturur; 4) "AI  insan onayını" başlatmakla doğrudan bağımsız eylemlere atlamayın; 5) ön olay tahminleri  MIT araştırmaları 10-15 dakika ön gösterir, ancak "ön tahmin sonrası ne yapılır" stratejisi tanımlaması  ön su?

Runbooks, Confluence sayfalarından yapılandırılmış bölümlerle (semptom, hipotez, doğrulama, eylem) versiyon markdown'a kadar evrimleşir. Struktürlü runbooks daha iyi RAG kurtarma sağlar.

### Hatırlamalısın numaralar

- MIT erken tespit: %89 kesinti, 10-15 dakika öncesi zaman.
- Çoklu ajan sınıflandırması: denetçi + (loglar, metrikler, çalışma kitapları) + insan.
- Güvenli otomatik düzeltme seti: Kapsul yeniden başlat, yeniden dağıt, sınırlar içinde ölçeklendirin.
- Karşılıklı değerlendirme: iki bağımsız model; anlaşma = güven.

## Çerçeveyi kullanın.
```figure
i4-incident-agents
```

## Kullan

`code/main.py`Bir çok ajanlı bir triaj simülasyonu: log ajanı hatayı bulur, metrik ajanı CPU spike bulur, runbook ajanı bilinen soruya eşleşir.

> `code/main.py`Bir çok ajanlı bir triaj simülasyonu: log ajanı hatayı bulur, metrik ajanı CPU spike bulur, runbook ajanı bilinen soruya eşleşir.

> `code/main.py`Bir çok ajanlı bir triaj simülasyonu: log ajanı hatayı bulur, metrik ajanı CPU spike bulur, runbook ajanı bilinen soruya eşleşir.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-ai-sre-plan.md`.Şimdilik çağrıda olan, olay hacmi, ekip olgunluğu göz önüne alındığında, bir AI SRE dağıtımını tasarlıyor.

> 本课产 出 `outputs/skill-ai-sre-plan.md`.Şimdilik çağrıda olan, olay hacmi, ekip olgunluğu göz önüne alındığında, bir AI SRE dağıtımını tasarlıyor.

## Egzersizler.

1. Çık .`code/main.py`Ya kayıt ve metrik ajanları anlaşmazlıklarda?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py` Eğer bir ajanın birbiriyle anlaşmazlığı varsa, yöneticisi nasıl yargıda bulunabilir?
2. Hizmetiniz için üç "güvenli" otomatik tedavi eylemini tanımlayın.
   Çinçe Çevirisi: Çevreyi tanımlamak için üç "güvenlik" otomatik olarak değiştirilmiştir.
3. Yapılandırılmış bir çalıştırma defteri şablonu yazın: bölümler, gerekli alanlar, doğrulama komutları.
   Çinçe Çevirimi:编写结构化运行手册模板:章节、必填字段、验证命令。
4. 12 dakika öncelik alarak ateş tespit edilebilir.
   Çinçe Çevirimi: 预测性检测在 12 分前量触发──你的策略是什么寻呼、预热还是等待?
5. 3 kişilik bir ekip 2026'da AI SRE'yi benimsemesi mi yoksa bekleme mi gerektiğini tartışın.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| AI SRE | "agent for on-call" | LLM-backed incident investigation + coordination |
| Supervisor agent | "the orchestrator" | Top-level agent breaking incidents into sub-queries |
| Specialized agent | "domain agent" | Sub-agent with tool access (logs, metrics, runbooks) |
| Auto-remediation | "AI fixes it" | Narrow pre-approved action; NOT broad re-architecture |
| Operational memory | "vector runbooks" | Post-mortems + runbooks in vector DB for RAG |
| Adversarial eval | "two-model check" | Independent analyses; agreement = confidence |
| NeuBird Hawkeye | "the adversarial one" | Product with adversarial-eval + memory pattern |
| Bits AI | "Datadog's SRE agent" | Datadog-managed AI SRE |
| Pre-incident prediction | "early detection" | 10-15 min lead time on outage prediction |

## Daha fazla okumak

- [incident.io — AI SRE Complete Guide 2026](https://incident.io/blog/what-is-ai-sre-complete-guide-2026)
- [InfoQ — Human-Centred AI for SRE](https://www.infoq.com/news/2026/01/opsworker-ai-sre/)
- [DZone — AI in SRE 2026](https://dzone.com/articles/ai-in-sre-whats-actually-coming-in-2026)
- [Datadog Bits AI](https://www.datadoghq.com/product/bits-ai/)
- [NeuBird Hawkeye](https://www.neubird.ai/)
- [awesome-ai-sre](https://github.com/agamm/awesome-ai-sre)
