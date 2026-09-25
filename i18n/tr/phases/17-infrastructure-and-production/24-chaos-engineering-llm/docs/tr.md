# Kaos Mühendisliği Yüksek Lisans Üretimi için .

> LLM için kaos mühendisliği 2026 yılında kendi disiplinidir. Üretim deneylerini yürütmeden önce ön koşullar: tanımlanmış SLI/SLO, izleme+metrik+log gözlemliliği, otomatik geri dönüş, çalıştırma defterleri, çağrıda bulunma. Mimarlık dört düzlemde bulunur: kontrol (deney programcısı), hedef (hizmetler, alt, veri depoları), güvenlik (kuvarlar + iptal + trafik filtreleri), gözlemsellik (metrikler + izler + günlükler), geri bildirim (SLO ayarlarına). Koruma rayları zorunludur: yanma oranı uyarıları, günlük hata bütçesi yanma> 2 katı beklenirse deneyleri durdurur; bastırma pencereleri + izleme kimliği ilişkisi alarmı gürültüsü çıkarır. Cadence: haftalık küçük kanarya + SLO inceleme; aylık oyun günü + ölüm sonrası; çeyreklik takım arası dayanıklılık denetimi + bağımlılık haritası. LLM'ye özel deneyler: hafıza aşırı yükü, ağ arızası, sunucu kesintileri, yanlış biçimlendirilmiş istekler, KV önbelleği tahrip fırtınaları. Araçlama: Harness Chaos Engineering (LLM'den kaynaklanan öneriler, patlama radyüsünün azaltılması, MCP araç entegrasyonu); LitmusChaos (CNCF); Chaos Mesh (CNCF Kubernetes-native).

> **【中文解读】**Bu bölümde LLM 混沌工程 başlıca olarak sorunlara girdi ve LLM サービス性実践をテストしました。


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy chaos experiment runner) | **语言:** Python
**Prerequisites:** Phase 17 · 23 (SRE for AI), Phase 17 · 13 (Observability) | **前置知识:** Phase 17 · 23 (SRE for AI), Phase 17 · 13 (Observability)

>  **【前置】**Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli bir ders: Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli Önemli
>  **【类比】**LLM 混沌工程 = " yanğın hareketi"。前提:SLI/SLO 定義好、可观测、自动回滚、runbook、on-call。四平面:控制(实验调度) +目标(服务/数据/基础设施) +安全(守卫/中止/流量过) +可观测。必须护:错误预算燃烧率 > 2x 时暂停实验。节奏:每周小卡纳里度+月度游戏日+季度跨团队审计。LLM 专属实验:内存过载、网络故障、供应商 机、坏快点、KV缓存 驱逐风暴。
**Time:** ~60 minutes | **时间:** ~60 minutes

## Öğrenme hedefleri

- Beş kaos mühendisliği ön şartını (SLI/SLO, gözlemlenebilirlik, geri dönüş, çalışma defterleri, çağrıda bulunma) belirleyin ve herhangi bir atlamanın neden uygulamayı iptal ettiğini açıklayın.
  Çinçe Çevirimi Çevirisi: 五个混沌工程前置条件 SLI/SLO、可观测性、回滚、运行手册、待命文化)
- Dört düzeni (kontrol, hedef, güvenlik, gözlemlenebilirlik) ve geri bildirim döngüsünü SLO'ya çiz.
  Çinçe Çevirimiçi: Çerçeve düzlemleri çizmek (kontrol, hedef, güvenlik, gözlem) ve SLO 仪表板'a karşı döngü çizmek.
- Beş LLM özel deneyi (hüye hafızası aşırı yük, ağ başarısızlığı, sağlayıcı kesinti, yanlış işlenmiş istek, KV tahrip fırtınası) listeleyin.
  Çinçe Çevirimi:列举五个 LLM 特定的混沌实验(内存过载、网络故障、提供商机、形输入、缓存失效)
- Bir araç seçin  Harness, LitmusChaos, Chaos Mesh  verilen yığın.
  Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çizüm: Çizlem: Çizlem: Çizlem: Çizlem: Çizlem: Çizlem: Çizlem

## Sorunlar. Sorunlar.

> **【中文解读】**LLM 混沌工程 is 2026 yılının bağımsız学科──LLM  yeni故障 modeli ekledi:4K-token'in tokinizasyon karakterleri分词器卡卡住12 saniye;上游提供商 429 触发网关重试,重试大大并发导致OOM;突发负载下 KV Cache 淘汰风暴引发重预填级联,尽量计算资源── bunlar, kullanıcıların onları buluncaya kadar 混沌工程 araçlarının tek bir testi içinde ortaya çıkmayacaktır──

> **【拓展：LLM 混沌工程的五类实验】**2026 yılında LLM 特定的五类混沌实验:(1) 内存过载发送长上下文高并发请求引发 KV Cache 抢占风暴,观察服务是优雅降级还是崩;(2) 网络故障断断推理网关与供应商的连接,观察故障over 是否在SLA内生效;(3) 供应商中断模拟100% OpenAI 429,观察路由是否失败到人类;(4) 形提示注入器具死负载吗(分层嵌套 Unicode、 UTF-8 码点),观察单个请求锁定工作者淘汰;5) KV 淘汰巨大暴风和vLLM 块预算强制淘汰, L L L 恢复 恢复服务MCMC 降级观察.

Geleneksel yığınlarda kaos testi kuruldu. LLM yığınları yeni başarısızlık modlarını ekler. Zehir karakterli bir 4K-token istek, tokenizeciyi 12 saniye boyunca durdurur. Bir yukarı akım sağlayıcısı 429s; geçit girişiniz yeniden dener; servis OOM'larınız tekrar güçlendirilmiş eşzamanlı olarak. Bir KV önbelleği boşaltma fırtınası patlama yükü altında hesaplama doymuş kaskadları yeniden doldurmaya neden olur.

Bu testlerin hiçbiri birim testlerinde görünmüyor. Kaos mühendisliği, kullanıcıların yapmadan önce onları keşfetmenin bir yolu.

## Konsepten bir şey.

### Ön koşullar

> **【中文解读】**Üretim içinde çalışmakta olan kaos testi'nin beş şartı: 1) SLI/SLO 已定义; 2) 可观测性(trace + metric + log)已部署; 3) 自动回滚机制就绪; 4) 结构化 runbook 已编写; 5) 有值班人员响应──缺少任何一项, kaos就会变成真实事件──四个平面:控制面(实验调度机) 目标面、服务/基础设施) 安全、面杀开机 + 抑制窗口 + 爆射线 限制) 、观测面标志 + 痕迹 关关) 反循环将发现可回到 SLO 调整、运行 更新和代码簿修复──

Üretimdeki kaosı:

1. **SLI/SLO** hizmet düzeyin göstergelerinin ve hedeflerin belirlenmesi.
2. **Observability** izler, metrikler, kayıtlar, ara çubuğa kablo.
3. **Automated rollback** 17 · 20 aşama politika bayrağı geri dönüşü.
4. **Runbooks** yapılandırılmış, 17 · 23.
5. **On-call**- Cevap verecek biri.

Herhangi bir şekilde kayıp kaos gerçek bir olay haline gelir.

### Dört uçak + geri bildirim

**Control plane** deney programcısı (Litmus iş akışı, Kaos Mesh programı, Harness UI).

**Target plane**- Hizmetler, kapsüller, düğümler, yük dengeleyici, veri depoları.

**Safety plane** öldürme anahtarı, baskı pencereleri, patlama radyüsü sınırları, hata bütçesi kapıları.

**Observability plane** normal ölçümler + iz-İD korelasyonu doğal hatalardan oluşan kaosı ayırt etmek için.

**Feedback loop** Bulgular SLO ayarlamalarına, runbook güncellemelerine, kod düzeltmelerine geri döner.

### Koruma rayları zorunludur .

> **【拓展：混沌工程的安全护栏】**Çelişki mühendisliği'nin üç gerekli güvenlik koruması: 1) deney sırasında her gün yanlış bütçe tüketimi beklenenden 2 kat daha fazla olursa, otomatik olarak durdurma deneyi; 2) deney patlama yarısında sessizlik, sessizce hareket etmeyi engelleme penceresini; 3) arama ID'si bağlantısı tüm deneylerin ortaya çıkardığı hataları taşıma etiketlerini, arama üzerinde tekrar yapılabilmesi için kullanır.

- **Burn-rate alert**Günlük hata bütçesi yanma beklenenin iki katını aşarsa, durak deneyi.
- **Suppression windows**: deney sırasında patlama radyosunda deney dışı uyarıları sessizleştirmek.
- **Trace-ID correlation**: deneylerin neden olduğu tüm hatalar bir etiket taşır, böylece çağrıda bulunarak sonuçlanabilir.

### Beş LLM özel deneyi

1. **Memory overload** yüksek eşzamanlılık ile uzun bağlamlı istekleri göndererek KV önleme fırtınasını zorlamak.

2. **Network failure** İtkinlik geçidi ve sağlayıcı arasındaki bağlantıyı kesin.

3. **Provider outage simulation** OpenAI'den %100 429. Not: yönlendirme Antropic'e geçiş başarısız mı oluyor? (Fase 17 · 16, 19)

4. **Malformed prompt** Tokenizer-stalling payload enjekte (örneğin, derin bir yuva içindeki unicode, büyük UTF-8 kod noktası).

5. **KV eviction storm** vLLM blok bütçesini doymakla zorla çıkarma.

### Cadence

- **Weekly** küçük kanarya deneyleri, belki %5 projed.
- **Monthly** belirli bir senaryoda belirlenmiş oyun günü; takımlar arası katılım; ölüm sonrası.
- **Quarterly** Ekipler arası dayanıklılık denetimi; bağımlılık haritasının güncelleştirilmesi.

### Araçlama

> **【拓展：混沌工程工具选择】**2026 yıl kaoslu bir mühendislik araç seçimi:(1) Harness Chaos Engineering商业,AI 驱动的实验推,blast radius 自动缩放,MCP 工具集成;(2) LitmusChaosCNCF 毕业,Kubernetes 工作流式;(3) Chaos MeshCNCF 沙箱,Kubernetes-native CRD风格;(4) Gremlin商业,广泛支持;(5) AWS FIS / Azure Chaos Studio托管云服务──节奏建议:每周小卡纳里 实验 + SLO 审查,每月游戏日 + 后期,每季度跨团队性审计 + 依赖映射更新──

- **Harness Chaos Engineering** Ticari; Yapay zeka kaynaklı deney önerileri; patlama radyüsünün azaltılması; MCP araçlarının entegrasyonu.
- **LitmusChaos** CNCF mezun; Kubernetes çalışma akışına dayalı.
- **Chaos Mesh** CNCF kum kutusu; Kubernetes-devli CRD tarzı.
- **Gremlin** Ticari; geniş destek.
- **AWS FIS**- Ne ?**Azure Chaos Studio** yönetilen bulut sunuşları.

### Küçük başlıyor.

İlk deney: sabit trafik altında bir kod kopyasını öldür. Yeniden yönlendirme ve kurtarma izleyin. Eğer bu işe yarıyorsa ve güvenli görünüyorsa, ağ kaosuna geçin.

İlk LLM özel deneyi: 5 dakika boyunca 429'u bir sunucuya enjekte edin.

### Hatırlamalısın numaralar

- Dört uçak: kontrol, hedef, güvenlik, gözlemlenebilirlik.
- Yanma oranı duraklama: Beklenen günlük bütçe yanma 2 katı.
- Cadence: haftalık kanarya, aylık oyun günü, çeyreklik denetim.
- Beş LLM deneyi: hafıza, ağ, sağlayıcı, yanlış düzenlenmiş istek, KV fırtınası.

## Çerçeveyi kullanın.
```figure
i4-chaos-guard
```

## Kullan

`code/main.py`Güvenlik uçak kapıları ile üç kaos deneyimi simülasyonu yaparak yanma oranı bozulmasını sağlayacak deneylerin raporlarını yapıyoruz.

> `code/main.py`Güvenlik uçak kapıları ile üç kaos deneyimi simülasyonu yaparak yanma oranı bozulmasını sağlayacak deneylerin raporlarını yapıyoruz.

> `code/main.py`Güvenlik uçak kapıları ile üç kaos deneyimi simülasyonu yaparak yanma oranı bozulmasını sağlayacak deneylerin raporlarını yapıyoruz.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-chaos-plan.md`- Dolu ve olgunluğu göz önüne alındığında ilk üç deneyi ve alet seçer.

> 本课产 出 `outputs/skill-chaos-plan.md`- Dolu ve olgunluğu göz önüne alındığında ilk üç deneyi ve alet seçer.

## Egzersizler.

1. Çık .`code/main.py`Hangi deney yakma oranı kapısını zorlar ve neden?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`Hangi deney yanma oranını kontrol etti?
2. VLLM tabanlı bir RAG hizmetinin ilk beş kaos deneyimi tasarlayın. Başarılılık kriterlerini dahil edin.
   Çinçe Çevirisi: VLLM'e dayalı RAG サービスデザイン前五个混沌实验──
3. Yanma oranı uyarısı bir deneyi durdurdu.
   Çinçe Çevirim: Senin yanma oranı polis bir deney durdurdu.
4. Yapım sırasında kaosun olması mı yoksa sadece sahnelenmesi mi gerektiğini tartışın.
   Çinçe çevirisi:论证混沌实验应在生产中还是仅在预发布环境运行中.
5. Genel ağ kaosu'nun yeniden üretemeyeceği üç LLM-sözlü başarısızlık modunu isimlendirin.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| SLI / SLO | "service targets" | Indicator + objective; required prerequisite |
| Blast radius | "scope" | Set of services / users affected by experiment |
| Burn-rate alert | "budget gate" | Fires when error-budget burn rate > 2x expected |
| Game day | "monthly drill" | Scheduled cross-team chaos exercise |
| LitmusChaos | "CNCF workflow" | Graduated CNCF Kubernetes chaos tool |
| Chaos Mesh | "CNCF CRD" | CNCF sandbox Kubernetes-native chaos |
| Harness CE | "commercial AI-assisted" | Harness chaos with AI recommendations |
| Malformed prompt | "tokenizer bomb" | Input that stalls tokenization |
| KV eviction storm | "preemption cascade" | Mass eviction triggering re-prefills |

## Daha fazla okumak

- [DevSecOps School — Chaos Engineering 2026 Guide](https://devsecopsschool.com/blog/chaos-engineering/)
- [Ankush Sharma — Observability for LLMs (book)](https://www.amazon.com/Observability-Large-Language-Models-Engineering-ebook/dp/B0DJSR65TR)
- [LitmusChaos (CNCF)](https://litmuschaos.io/)
- [Chaos Mesh (CNCF)](https://chaos-mesh.org/)
- [Harness Chaos Engineering](https://www.harness.io/products/chaos-engineering)
- [AWS FIS](https://aws.amazon.com/fis/)
