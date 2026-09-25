# AI Gateways  LiteLLM, Portkey, Kong AI Gateway, Bifrost 网关 LLM

> Uygulamalarınız ve model sağlayıcılarınız arasında bir geçit yer alır. Temel özellikler sunucu yönlendirme, geri dönüş, tekrar deneme, hız sınırlaması, gizli referanslar, gözlemlenebilirlik, korumalar. 2026'da piyasa bölünmesi: **LiteLLM**OpenAI ile uyumlu olan 100'den fazla sağlayıcı ile MIT OSS'dir, ancak yaklaşık 2000 RPS (8 GB bellek, yayınlanan referans değerlerinde kaskadaki hatalar) arasında ayrılır; Python için en iyi, <500 RPS, dev/prototipleme. **Portkey**kontrol düzeni konumlandırılmış (güvenlikler, PII redaksiyonu, jailbreak algılama, denetim izleri), Apache 2.0 açık kaynak Mart 2026'da 20-40 ms gecikme overhead gitti, $49/mo production tier. **Kong AI Gateway** built on Kong Gateway — Kong's own benchmark on same 12 CPUs: 228% faster than Portkey, 859% faster than LiteLLM; $Model/ay fiyatı 100 (Plus seviyesinde maksimum 5); Kong'da zaten varsa işletme için uygun. **Bifrost**(Maxim AI)  Otomatik geri dönüş, OpenAI 429'da Anthropic'e geri dönmek. **Cloudflare / Vercel AI Gateways** yönetilen, sıfır operasyonlar, temel yeniden deneme. Veriler konumu kendi kendine konukseverlik kararını yönlendirir; Portkey ve Kong, OSS + seçmeli yönetilen ortada oturuyor.

> **【中文解读】**Bu bölümde AI 网关LLM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM LEM 


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy gateway-routing simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 16 (Model Routing) | **前置知识:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 16 (Model Routing)

>  **【前置】**Önemli bir şekilde, bu süreçte, yeni bir teknoloji geliştirmek için yeni bir teknoloji geliştirmek için daha fazla bilgi edinmek gerekir.
>  **【类比】**AI Gateway = "AI 流量交警"。LiteLLM = 开源 MIT 100+ sağlayıcı, ancak < 500 RPS 适合;Portkey = 控制面(PII 脱敏/越狱检测/审计) $49/月;Kong = 性能王(自家基准比 Portkey 快 228%、比 LiteLLM 快 859%), Kong'un işletmelerine uygun;Bifrost = 自动重试+按回退;Cloudflare/Vercel = 托管运维──是否零需自托管:
**Time:** ~60 minutes | **时间:** ~60 minutes

## Öğrenme hedefleri

- Altı temel geçit özelliklerini (routing, fallback, retry, hız limitleri, sırlar, gözlemlenebilirlik, koruma) listeleyin.
  Çinçe Çevirimiçi:列举六个核心网关功能 (路由,回退,重试,速率限制,密钥管理,可观测性)
- Çatılar ve kullanım durumları ölçeklendirilirken 2026'da dört geçit (LiteLLM, Portkey, Kong AI, Bifrost) haritasını yapın.
  Çin dilinde:将四个 2026年网关(LiteLLM、Portkey、Kong AI、Bifrost) 映射到规模上限和用例──
- Kong referans değerini alıntılayın (228% vs Portkey, 859% vs LiteLLM) ve neden >500 RPS için önemli olduğunu açıklayın.
  Çin dilinde:引用 Kong 基准测试(228% vs Portkey,859% vs LiteLLM)并解释为什么在 >500 RPS 时重要──
- Verilerin konut ve operasyon bütçesi verildiği için kendi kendine barındırılan vs yönetilen seçin.
  Çinçe çevirisi:给定数据驻留和运维预算,选择自托管 vs.托管──

## Sorunlar. Sorunlar.

> **【中文解读】**AI 网关 uygulaması ve model sağlayıcıları arasında yer alır, çözülmesinin temel sorunu çok sayıda tedarikçi birliği yönetimidir. Ürünler aynı zamanda OpenAI 、Anthropic 和自托管 Llama'yı kullanır, her sağlayıcı farklı SDK 、 yanlış model 、 hız sınırlama ve onay programı vardır.

> **【拓展：2026 年 AI 网关市场】**2026 yılında AI 网关 pazarının dört ana oyuncusu:(1) LiteLLMMIT 开源,100+ 提供商, ancak ~2000 RPS 时崩(8GB 内存);(2) Portkey2026 yılının 3 月 开源 Apache 2.0,控制面定位(guardrails、PII 脱敏、越狱检测、审计追踪),20-40ms 延迟开销;(3) Kong AI Gateway 成熟 API 网关 ürünlerine dayalı, Kong 基准测试显示自己的Portkey 快 228%、比 LiteLLM 快 859%;(4) Cloudflare/Vercel AI Gateway 托管、零运维、边缘部署;;

Ürününüz OpenAI, Anthropic ve kendi kendine barındırılan Llama'yı çağırır. Her sağlayıcı farklı bir SDK, hata modeli, oran sınırı ve ot programına sahiptir. Başarısızlık yapmak istiyorsunuz (OpenAI 429'lar varsa, Anthropic'i deneyin), tek bir kredileme mağazası, tek bir gözlemsellik ve kiracı başına oran sınırı.

Bu uygulama katmanında yeniden icat etmek her hizmeti her sağlayıcıya eşleştirir. Bir geçit katmanı, hizmeti sağlayıcılara yayarak bir API ile (genellikle OpenAI uyumlu) bir süreçte birleştirir.

## Konsepten bir şey.

### Altı temel özellik

1. **Provider routing** OpenAI, Anthropic, Gemini, kendi kendine barındırılan, vb.
2. **Fallback**429, 5xx'te veya kalite başarısızlığı, başka bir yerde tekrar deneyin.
3. **Retries** Eksponansiyel geri dönüş, sınırlı girişimler.
4. **Rate limits** Kiracı başına, anahtar başına, model başına.
5. **Secret references** Kullanım zamanı (birde uygulamada) güvenirlik bilgileri kasadan çek.
6. **Observability** OTel + GenAI özellikleri (Fase 17 · 13) + maliyet atributları.
7. **Guardrails** PII düzenleme, jailbreak algılama, izin verilen konular filtreleri.

### LiteLLM  MIT OSS, Python

- 100+ sağlayıcı, OpenAI uyumlu, yönlendirme yapılandırması, geri dönüş, temel gözlemsellik.
- Kong'un referans değerinde 2000 RPS'nin kırılması; 8 GB hafıza ayak izleri, sürekli yük altında kaskadaki başarısızlıklar.
- En iyi uyum: Python uygulaması, <500 RPS, dev/staging geçitleri, deneysel yönlendirme.
- Fiyat: OSS için 0 dolar; bulutsuz bir kat var.

### Portkey  kontrol uçağının konumlandırılması

- Apache 2.0 OSS Mart 2026 tarihli olarak.
- 20-40 ms talep başına gecikme maliyeti.
- 49 $ / ay üretim seviyesine, tutma + SLA ile.
- En uygun: korumalara ihtiyaç duyan düzenlenmiş endüstriler + gözlemsellik birleştirilmiş.

### Kong AI Gateway  ölçek oyunu

- Kong Gateway üzerinde inşa edilmiş (olgun API geçit ürün, lua+OpenResty).
- Kong'un kendi 12 CPU eşdeğerindeki referans değerleri: Portkey'den 228% daha hızlı, LiteLLM'den 859% daha hızlı.
- Fiyat: 100 dolar / model / ay, maksimum 5 Plus seviyesinde.
- En iyi uygunluk: Kong'da zaten; > 1000 RPS; lisans almak için hazır.

### Bifrost (Maxim AI)

- Otomatik bir şekilde yeniden çalıştırma.
- OpenAI 429'da Anthropic'e geri dönmek, kanonik bir tarif.
- Yeni giriş; ticari.

### Cloudflare AI Gateway / Vercel AI Gateway

- Başarılı, sıfır operasyon, temel yeniden deneme ve gözlemsellik.
- En iyi uyum: Cloudflare/Vercel'de Edge hizmet veren JavaScript uygulamaları.
- Kong/Portkey'e kıyasla koruma ve hız sınırları için sınırlı.

### Kendi kendine barındırılan vs yönetilen

> **【中文解读】**Kendiliğinden yönetim ve yönetim konusunda kararlılık etkisi vardır. Bu nedenle, TTFT'nin TTFT'yi doğrudan etkileyen bir süre vardır.

> **【拓展：网关 + 可观测性 + 路由的组合】**17·13(可观测性) + 16(模型路由) + 19(网关) ⇒生产中是同一层──选择一个覆盖所有三者的工具,或仔细连接它们:大多数 2026年部署将 Helicone(可观测性) 或 Portkey(guardrails) 与 Kong(规模) 组合分拆角色──Portkey's Apache 2.0 开源使"自托管 guardrails + Kong 规模"组合成为监管行业的标准模式──

Veri ikametciliği zorlayıcı işlevdir. Sağlık ve finans öntanımlı kendi-host (LiteLLM veya Portkey OSS veya Kong). İsteğe bağlı olarak yönetilen tüketici ürünleri (Cloudflare AI Gateway) veya orta seviye (Portkey yönetilen).

### Gecikme bütçesi

> **【拓展：AI 网关延迟预算分析】**AI 网关延迟直接影响TTFT,是选型的关键因素.2026年各网关的延迟开销:(1) LiteLLM 5-15msPython 实现,简单但高并发下不稳定;(2) Portkey 20-40ms功能最全面但延迟最高;(3) Kong 3-8msGo + OpenResty,延迟最低且高并发稳定;(4) Cloudflare/Vercel 1-3ms边缘部署优势;;;;

- LiteLLM: 5-15 ms genel yük tipik.
- Portkey: 20-40 ms üst.
- Kong: 3-8 ms üst.
- Cloudflare/Vercel: 1-3 ms genel maliyet (geçer avantajı).

Gateway gecikmesi doğrudan TTFT'ye eklenir. TTFT P99 < 100 ms SLA, Kong veya Cloudflare için. P99 < 500 ms için, herhangi bir.

### Sınır sınırı semantik meselesi

Basit token-bucket orta ölçekte çalışır. Çoklu kiracı sürükleyici pencere + patlama izin + kiracı başına bir katlama gerektirir. LiteLLM token-bucket gemileri; Kong gemileri sürükleyici pencere; Portkey gemileri katlandırılmış.

### Geçit + gözlemlenebilirlik + yönlendirme oluştur

17 · 13 aşaması (gözleyicilik) + 16 (modelleme yönlendirme) + 19 (kapı) aynı üretim katmanıdır. Üçünü de kaplayan bir araç seçin veya dikkatlice telleştirin: 2026'daki çoğu dağıtım Helicone (gözleyicilik) veya Portkey (kuzen) ile Kong (skala) bölünmüş roller için birleştirir.

### Hatırlamalısın numaralar

- LiteLLM: 2000 RPS'de kırılır, 8 GB bellek.
- Portkey: 20-40 ms üst düzey; Apache 2.0 Mart 2026'dan beri.
- Kong: Portkey'den 228% daha hızlı, LiteLLM'den 859% daha hızlı.
- Kong fiyatı: $ 100 / model / ay, 5 maksimum Plus seviyesinde.
- Cloudflare/Vercel: 1-3 ms uçta.

## Çerçeveyi kullanın.
```figure
mx-gateway-fallback
```

## Kullan

`code/main.py`429/5xx enjeksiyon altında 3 sunucu arasında geri dönüşle geçit yönlendirmeyi simüle eder. Gecikme, yeniden deneme oranı ve geri dönüş çarpma oranını rapor eder.

> `code/main.py`429/5xx enjeksiyon altında 3 sunucu arasında geri dönüşle geçit yönlendirmeyi simüle eder. Gecikme, yeniden deneme oranı ve geri dönüş çarpma oranını rapor eder.

> `code/main.py`429/5xx enjeksiyon altında 3 sunucu arasında geri dönüşle geçit yönlendirmeyi simüle eder. Gecikme, yeniden deneme oranı ve geri dönüş çarpma oranını rapor eder.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-gateway-picker.md`Ölçek, operasyon pozisyonu, uyumluluk, gecikme bütçesi göz önüne alındığında, bir kapı seçer.

> 本课产 出 `outputs/skill-gateway-picker.md`Ölçek, operasyon pozisyonu, uyumluluk, gecikme bütçesi göz önüne alındığında, bir kapı seçer.

## Egzersizler.

1. Çık .`code/main.py`. OpenAI→Anthropic→self-hosted'den geri dönüş ayarlayın. % 5 servisçi hata oranında beklenen hit oranı nedir?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py` Configuration OpenAI -> Anthropic -> 自托管的回归── hangi koşullar en mantıklıdır?
2. SLA'nın TTFT P99 < 200 ms'dir. 300 ms'lik bir başlangıç çizgisinde. Hangi geçitler bütçenin içinde kalır?
   Çinçe Çevirimi: SLA'nın 300 ms 基线 üzerindeki TTFT P99 < 200 ms ⋅ hangi net关在预算内?
3. Sağlık hizmetleri için kendi kendine konutlama + kişisel bilgi düzenleme + denetim gerekir. Portkey OSS veya Kong'u seçin.
   Çin dili: bir sağlık hizmetinde müşteri kendi kendine bakım gerektirir + PII 脱敏 + 审计――选择 Portkey OSS 或 Kong。
4. LiteLLM vs Kong'u karşılaştırın: Bir takım hangi RPS tavanına göç etmeli?
   Çinçe Çevirimi: LiteLLM vs Kong: Ekip hangi RPS üst sınır altında taşınmalı?
5. Çok kiracı SaaS için ücret sınırlama politikası tasarlayın: ücretsiz, deneme, ücretli seviyeler. Token-bucket veya kaydırıcı pencere?

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Gateway | "API broker" | Process sitting between apps and providers |
| LiteLLM | "the MIT one" | Python OSS, 100+ providers, breaks at 2K RPS |
| Portkey | "guardrails gateway" | Control plane + observability, Apache 2.0 |
| Kong AI Gateway | "the scale one" | Built on Kong Gateway, benchmark leader |
| Bifrost | "Maxim's gateway" | Retries + Anthropic fallback recipe |
| Cloudflare AI Gateway | "edge managed" | Edge-deployed managed gateway, zero-ops |
| PII redaction | "data scrub" | Regex + NER mask before sending to model |
| Jailbreak detection | "prompt injection guard" | Classifier on user input |
| Audit trail | "regulated log" | Immutable record of every LLM call |
| Token-bucket | "simple rate limit" | Refill-based rate limiter |
| Sliding-window | "precise rate limit" | Time-windowed rate limiter; better fairness |

## Daha fazla okumak

- [Kong AI Gateway Benchmark](https://konghq.com/blog/engineering/ai-gateway-benchmark-kong-ai-gateway-portkey-litellm)
- [TrueFoundry — AI Gateways 2026 Comparison](https://www.truefoundry.com/blog/a-definitive-guide-to-ai-gateways-in-2026-competitive-landscape-comparison)
- [Techsy — Top LLM Gateway Tools 2026](https://techsy.io/en/blog/best-llm-gateway-tools)
- [LiteLLM GitHub](https://github.com/BerriAI/litellm)
- [Portkey GitHub](https://github.com/Portkey-AI/gateway)
- [Kong AI Gateway docs](https://docs.konghq.com/gateway/latest/ai-gateway/)
