# Modelleşimi, maliyet azaltma için bir temel olarak.

> Dinamik bir broker her talebi değerlendirir (tüm görev türü, token uzunluğu, yerleştirme benzerliği, güven) ve basit sorguları ucuz bir modele gönderir, karmaşık sorguları sınır modeline yükselir. Model kaskadı olarak da adlandırılır. Üretim vaka çalışmaları, ABD/İngiltere/AB dağıtımları arasında iso-kalite'de maliyetlerin %20-60 oranında azalması göstermektedir; yüksek hacmi SaaS'de %30 yönlendirme verimliliğinin iyileştirilmesi, yıllık altı rakamlı tasarruf haline gelir. 2026 bağlamında LLM sonucu fiyatları yılda ~ 10 kat düştü  bir GPT-4 sınıfı token gitti $20/M to ~$2022'nin sonundan 2026'ya kadar 0.40/M. Çoğu düşüş, donanım değil, daha iyi servis halinde (Fase 17 · 04-09), Routing, fiyat düşüşünü ürün gerilemesi olmadan marj olarak dönüştürmenin yoludur. Başarısızlık modusu ucuz model sürüşüdür: rota %40'ı zayıf bir modele doğru itiyor, kalitesi akıl yürütme görevlerinde %3-5% düşüyor, kimse bir çeyrek bile fark etmez. Geçit yolları çevrimiçi kalite ölçümleri ile, sadece çevrimiçi değerleme setleri ile değil.

> **【中文解读】**Bu bölüm, farklı modellerin maliyet optimize stratejilerini görev karmaşıklığına göre seçmek için model yollarını tanımlıyor.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy cascading router simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 19 (AI Gateways) | **前置知识:** Phase 17 · 01 (Managed LLM Platforms), Phase 17 · 19 (AI Gateways)

>  **【前置】**学本节前 Lütfen önce bil:Fase 17·01(托管平台) 、Fase 17·19(AI Gateway) 』模型路由 = 动态 bróкери 按任务复杂度选便宜或贵模型──
>  **【类比】**模型路由 = "医院分诊"──简单感冒→社区医生(Haiku/Sonnet); şü难杂症→专家(Opus);急诊→主任(GPT-4)──20-60% 成本降,30% 路由效率改进=六位数年省──背景:LLM 价格 2022-2026 降10倍/年,多数降来自服务改进而非硬件路由把价转转成利──
> ️ **【易错点】**便宜模型漂移:40% 路由到弱模型→推理质量降低 3-5%→一个季度没人发现──修复:用在线质量监控(不仅离线评估)守住底线──
**Time:** ~60 minutes | **时间:** ~60 minutes

## Öğrenme hedefleri

- Modelin kaskadını açıklayın: güven kontrolü ile ucuz-birincisi, düşük güven üzerinde yükseliş.
  Çinçe Çevirimiçi: açıklama modelleri sınıfı: ucuz öncelikçe güvence, düşük güvence zaman yükseltme
- Dört yönlendirme sinyali (tüm görev sınıflandırması, hızlı uzunluk, bilinen sert set ile benzerliği yerleştirmek, ilk geçişten itibaren kendine güven)
  Çinçe Çevirimiçi:列举四种路由信号(任务分类、提示长度、嵌入相似度、首次通过自置信度)
- Hedef yönlendirme bölünmesi ve kalite kaybı toleransında beklenen karışık maliyetin hesaplanması.
  Çinçe Çevirisi: hesaplama hedef yolu分流和質損失耐性下预期混合成本。
- Ucuz model sürüklemeyi takip eden metrik (online kalite kapısı) isimlendirin.
  Çinçe Çevirisi: ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ 

## Sorunlar. Sorunlar.

> **【中文解读】**Model yolunun temel anlayışı:70% sorgu basit bir şeydir. Haiku sınıfı modelinin 3% maliyetle tam olarak işlenmesi mümkündür. Sadece 30%'ü GPT-5 sınıfı düşünme yeteneğine ihtiyaç duyar. 70%'i ucuz modelden, 30%'i ön cephede olan modelden, aynı ürün kalitesi yaklaşık %65'i düşürür.

> **【拓展：模型路由的产业案例】**2026 model yoluyla üretimdeki tipik sonuçlar:20-60% Kastük düştü(同质量下) ・LLM 推理价从2022年到2026年下降约10x/年(GPT-4 级从$20/M 降到 $0.40/M), büyük bir kısmının düşüşü, önerilen  optimizasyonlardan geliyor.

Servisiniz GPT'de ayda 80 bin dolar masraf ediyor.Analytikleriniz, soruların %70'inin basit olduğunu gösteriyor: "Paris'te saat kaç?" "Bu cümleyi yeniden ifade et". Haiku sınıfı modeli, maliyetin %3'ünde bunları mükemmel şekilde ele alır. %30'a GPT-5'in mantıklılığı gerek  kodlama, matematik, çok adımlı planlama.

Eğer %70'i ucuz ve %30'u pahalı bir şekilde yönlendirseniz, faturalarınız aynı ürün kalitesiyle %65 oranında düşer. Bu yönlendirme.

## Konsepten bir şey.

### Dört yönlendirme sinyali

> **【中文解读】**四种路由信号:(1) 任务分类简单/复杂/代码/数学/聊天,可用规则分类器或小 LLM($0.25/M);(2) 提示长度>4K token 通常需要前沿模型,<500通常不需要;(3) 嵌入相似度已知困难集的余弦相似度 >0.88 则直接升级;(4) 首次通过自信度发送到廉价模型,如果日志检查器 显示低信心或拒绝,重试到沿模型──

1. **Task classification**: basit/ karmaşık/ kodegen/ matematik/ sohbet. Kurallara dayalı bir sınıflandırıcı, küçük bir LLM (Haiku sınıfı $ 0.25 / M) veya etiketlenmiş kovalara benzerliği yerleştirmek olabilir.

2. **Prompt length**Bu nedenle, bu durumun bir diğer nedeni de, bu durumun da bir diğer nedeni de olabilir.

3. **Embedding similarity to known-hard set**: sorgu bilinen sert bir kova yakınsa (kosine > 0,88) doğrudan sınırlara tırmanın.

4. **Self-confidence from first-pass**: ucuz gönderin; modelin log-probleri düşük güven gösterirse YA da reddederse YA da koruma dilini çıkarırsa, sınırda yeniden deneyin. Trafikin %10'unda P95 gecikme oranını artırır, diğer %90'da ise %50+ tasarruf sağlar.

### Üç örneği

> **【拓展：模型路由的三种模式】**Model yolunun üç çeşit gerçekleştirme modeli karşılaştırması: 1) Ön yol  Ön yerleştirme  Ön sınıflandırma  kural veya küçük LLM), 5-10 ms artır                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        

**Pre-route**(telif önde): ~ 5-10 ms gecikme eklenmiştir; genel olarak en hızlı.

**Cascade**(incil olarak ucuz, düşük güvenle yükselir): ~1.2x ortalama gecikme ( ucuz çalıştırma artı doğrulama), ~2x yükselir. En iyi kalite zemin.

**Ensemble route**(çizgi ve sınır paralel olarak çalıştırılır, ödül model seçilir): en yüksek kalitede, en yüksek maliyette; yalnızca kritik A/B için kullanılır.

### Uygulama

AI geçitleri (Fase 17 · 19) yönlendirmeyi ortaya çıkarır. LiteLLM `router`Portkey'in gardiyanları + yönlendirme. Kong AI Gateway'in eklenti tabanlı yönlendirme. OpenRouter'ın model pazarı bir önerme API'si ortaya çıkarır.

Açık kaynaklı: RouteLLM (LMSYS), Diamond değil (ticari), Prompt Mule.

### 2026 fiyat eğri

| Model class | Late 2022 | 2026 | Change |
|-------------|-----------|------|--------|
| GPT-4-level quality | ~$20/M | ~$0.40/M | 50x cheaper |
| Frontier (GPT-5, Claude 4) | — | ~$3-10/M | new tier |

En büyük gelişme verimliliği hizmet vermektir. 17 · 04-09 Eğlence'deki temel dersler sağlayıcı tarafındaki maliyet düşüşüne dönüştü. Routing tüm kullanıcılarınızın ucuz seviyeye taşınmasını beklemek yerine uygulama katmanında bu kazançları yakalamanıza olanak sağlar.

### - Drift gerçek bir risk.

> **【中文解读】**漂移是模型路由的真正风险──路由将将40% 发送到廉价模型,6 个月后任务分布变化(用户更成熟、问题更长), ancak router'ın sınıflandırma makinesi hala Q1 数据训练基础上──质量下降没有投诉足够响亮,直到竞争对手基准测试中落才知道──必须通过在线质量指标门控制路由:用户反自动LLM 评审(5% 采样) 升级率、拒绝率──

> **【拓展：模型路由的实现方案】**2026 yıl model yolunun gerçekleştirilmesi seçeneği:(1) AI 网关(Fase 17·19) LiteLLM'in yönlendiricisi yapılandırması,Portkey'in koruyucuları+ruuting、Kong AI Gateway'ın ekleme biçimli yolunun OpenRouter'ın önerisi API;(2) 开源RouteLLM(LMSYS) tam bir yol kütlesini sunar;(3) 商业Not Diamond 提供 SaaS 模型路由产品──三种路由模式:Pre-route(前置分类,最快) Cascade(pre-廉价再升级,质量最稳) Ensemble(并行运行多模型+奖励模型选择,最高质量但最高成本) 

Routeniz ucuz model için %40 gönderir. Altı ay içinde görev dağılımları değişir (kullanıcılar daha karmaşık hale gelir, daha uzun soru sorarlar). Router fark etmez çünkü sınıflandırıcısı Q1 verilerine eğitim almıştır. Kalite sessiz düşer. Kimse yeterince yüksek sesle şikayet etmez. Rakip benchmarkında kaybettiğini öğreniyorsun.

Online kalite ölçümleri ile geçit yolları:

- Kullanıcılar yol boyunca parmak parmaklarını yukarı / aşağıya kaldırır.
- Yol başına bir örnek (5%) üzerinde otomatik LLM yargıcı.
- Aşama oranı: Kaskadada %30'luk bir yükselme oranı varsa ucuz model aşırı yönlendiriliyor.
- Yol başına reddedilme oranı.

### Hatırlamalısın numaralar

- 2026 yönlendirme tasarrufu iso-kalitede: 20-60% vaka çalışmaları.
- LLM fiyatlarının düşüşü 2022-2026: ~ 10 kat yıllık toplam.
- GPT-4 seviyesinde 2022 vs. 2026: ~$20/M → ~$0.40/M.
- Kaskadalı gecikme etkisi: ~1.2x ortalama, ~2x yükseldi (trafikin ~ 10%).

## Çerçeveyi kullanın.
```figure
model-cascade-router
```

## Kullan

`code/main.py`-Küçük maliyet, kalite kaybı ve artış oranı raporları.

> `code/main.py`-Küçük maliyet, kalite kaybı ve artış oranı raporları.

> `code/main.py`-Küçük maliyet, kalite kaybı ve artış oranı raporları.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-router-plan.md`- İş yükü ve kalite bütçesi göz önüne alındığında, bir yönlendirme örneği ve sinyalleri seçer.

> 本课产 出 `outputs/skill-router-plan.md`- İş yükü ve kalite bütçesi göz önüne alındığında, bir yönlendirme örneği ve sinyalleri seçer.

## Egzersizler.

1. Çık .`code/main.py`Kaskadın önceden giden yolları hangi düzeyde geçer?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ Hangi seviye, ön yollardan daha iyi?
2. Kullanıcı tabanınız %30 işletme (mükemmel sorular), %70 ücretsiz seviyedir (sadece).
   Çinçe Çevirimi: Kullanıcı grupunuz %30'u işletme (sık sık sorgu) %70'ü ücretsiz (sık sık sorgu) %70'ü tasarlama (sık sık sorgu) %70'ü tasarlama (sık sık sorgu) %70'ü tasarlama (sık sık sorgu) %70'ü tasarlama (sık sık sorgu) %70'ü tasarlama (sık sık sorgu) %70'ü tasarlama (sık sık sorgu) %70'ü tasarlama (sık sık sorgu) %70'ü tasarlama (sık sık sorgu) %70'ü tasarlama (sık sorgu) %70'ü tasarlama (sık) %70'ü tasarlama (sık) %70'ü tasarlama (sık) %70'ü tasarlama (sık) %70'ü tasarlama (sık) %70'ü%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
3. Bir yol kalitesi %2 düşer ama %40 tasarruf eder.
   Çin Çeviri: bir yolla %2 oranında azaltma ama %40 tasarruf edilmesi.
4. OpenAI / Anthropic API'lerden logprobs kullanarak güven kontrolü uygulayın.
   Çevre dilinde: OpenAI/Anthropic API'nin logprobs'unu kullanmak 实现置信度检查──什么值触发升级?
5. Altı ay içinde, tırmanma oranı %8'den %22'e yükseldi.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Model routing | "cost broker" | Dynamic choice of model per request |
| Model cascade | "cheap-first escalate" | Run cheap, fall through to frontier on low confidence |
| Pre-route | "classify first" | Classifier up front; no re-run |
| Ensemble route | "parallel pick" | Run multiple, reward-model picks best |
| Escalation rate | "uprouted %" | Fraction of cascade requests that escalated |
| RouteLLM | "LMSYS router" | OSS router library |
| Not Diamond | "commercial router" | SaaS model-routing product |
| Drift | "cheap creep" | Distribution shift without router noticing |
| Online quality gate | "live check" | Automated LLM-judge sampling live traffic |

## Daha fazla okumak

- [AbhyashSuchi — Model Routing LLM 2026 Best Practices](https://abhyashsuchi.in/model-routing-llm-2026-best-practices/)
- [Lukas Brunner — Rise of Inference Optimization 2026](https://dev.to/lukas_brunner/the-rise-of-inference-optimization-the-real-llm-infra-trend-shaping-2026-4e4o)
- [RouteLLM paper / code](https://github.com/lm-sys/RouteLLM)
- [Not Diamond — model routing](https://www.notdiamond.ai/)
- [OpenRouter](https://openrouter.ai/) Routing primitipleri ile çoklu model geçit.
