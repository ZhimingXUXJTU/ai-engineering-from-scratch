# Satış API'leri % 50 indüstri standardı olarak indirim

> Her büyük sağlayıcı %50 indirim ve ~24 saatlik dönüşüm ile async parti API'si gönderir. OpenAI, Anthropic, Google ve çoğu sonuçlama platformu (Fireworks parti seviyesinde, Together parti) aynı kalıpı uyguluyor. Hızlı önbelleğe alınan ve gece geçici boru hattı olan yığın seri, sinkron-yüklenmemiş maliyetin %10'una düşer. Kural çok basit: Eğer etkileşimsizse, partiye ait. İçerik üretimi boruları, belge sınıflandırması, veri çıkarımı, rapor üretimi, toplu etiketleme, katalog etiketleme  24 saat gecikmeye toleranslı olan her şey, toplamaya geçene kadar masada kalan para. 2026 üretim tarzı, her yeni LLM çalışma yükünün üç dizine ayrılmasıdır: etkileşimli (memleketle eşzamanlı), yarı etkileşimli (sinkron olmayan sırada geri dönüş), seri (gece, önbelleğe girilen giriş yığılmış). İnteraktifmiş gibi davranan ama dakikalarca gecikme süreci geçiren iş yükleri en çok harcanır.

> **【中文解读】**Bu bölüm, büyük ölçekli farklı işlemler için kullanılan bir çok işlem API'yi tanımlıyor.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy batch-vs-sync cost simulator) | **语言:** Python
**Prerequisites:** Phase 17 · 14 (Prompt & Semantic Caching) | **前置知识:** Phase 17 · 14 (Prompt & Semantic Caching)
**Time:** ~45 minutes | **时间:** ~45 minutes

>  **【前置】**Öğrenci bölümün önüne geç: 17·14..
>  **【类比】**批处理 API = "物流拼车"──同步 = 急件快递(贵);批处理 = 整车发货(半价)──规则:非交互式任务必须上批──三层分流:交互式(同步+缓存)、半交互(异步队列+回退)、批处理(过夜+缓存叠加可降至10%)──伪装成交交交的"5 分钟可接受延迟"任务最浪费必须分类──

## Öğrenme hedefleri

- Üç tedarikçi parti API'si (OpenAI, Anthropic, Google) ve ortak %50 indirim + 24 saatlik dönüş garantilerini isimlendirin.
  Çinçe çevirisi: ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ 
- Gecelik sınıflandırma iş yükü üzerinde bir seriyi yığma + önbelleğe girilen giriş maliyetini hesaplayın ve senkronizasyon-önceltilmemiş başlangıç seviyesine karşılaştırın.
  Çinçe çevirisi: hesaplama üstü toplama işlem + 缓存输入在隔夜分类工作负载上的成本,并与同步未缓存基线相比──
- Bir iş yükünü etkileşimli / yarı etkileşimli / partiye ayırıp, şeridi haklı çıkarın.
  Çinçe Çevirisi:将工作负载分流到交互式/半交互式/批处理,并为每个车道说明理由──
- İki tuzağı isimlendirin: kısmi etkileşim (kullanıcı 24 saatten daha hızlı bekliyor) ve çıkış şeması süresi (batch dosya biçimi sağlayıcıya göre farklıdır).
  Çinçe Çevirimiçi: : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : : :   :   :                                                                                              

## Sorunlar. Sorunlar.

> **【中文解读】**Satış işlem API'si LLM'nin en ucuz araç kutusudur. Her ana tedarikçi %50 indirim + 24 saatlik değişik satış işlemleri sunuyor.

> **【拓展：三大提供商的批处理 API】**2026 yılında üç büyük LLM  tedarikçi tarafından toplu işlem bağlantısı:(1) OpenAI Batch APIJSONL 文件上传,/v1/batches 端点,50% 折,实际周转 2-8 小时;(2) Anthropic Message BatchesJSONL 上传,支持 cache_control,50% 折;(3) Google Vertex AI Batch PredictionBigQuery veya GCS 输入,Gemini 50% 折.

Ekibiniz her gece rapor üretimi hattı gönderir. 50.000 belge, her birini özetleyin, özetleri gruplandırın, bir yönetim kurulu raporu hazırlayın. Sinkron çalıştırmak, gece başına 2.000 dolar için 4 saat sürer.

Bu paketle %50 indirim elde ediyorsunuz. Sistem istekleri üzerinde de önbelleğe girme işlemini etkinleştirirsiniz (bütün 50k aramalarda paylaşılan).

Bu nedenle, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temelinde, bu programın temel olarak, bu programın temelinde, bu programın temel olarak, bu programın temelinde, bu programın temel olarak, bu programın temel olarak, bu programın temel olarak, bu programın temel olarak, bu programın temel olarak, bu programın temel olarak, bu programın temel olarak, bu programın temel olarak, bu programın temel olarak, bu programın temel olarak, bu programın temel olarak, bu programın temel olarak, bu programın temel olarak, bu programın temel olarak, bu programın temel olarak, bu programın temel olarak, bu programın temel olarak, bu programın, bu programın temel olarak, bu programın, bu programın, bu programın, bu programın, bu programın, bu programın, bu programın, bu programın, bu programın, bu programın, bu programın, bu programın, bu programın, bu programın, bu programın, bu programın, bu programın, bu programın, bu programın, bu programın, bu programın, bu programın, bu programın, bu programın, bu na bağlı olarak, bu programın, bu programın, bu programın, bu programın, bu na bağlı olarak, "İstanbul, "İstanbul, "İstanbul, "İstanbul, "İstanbul, "İstanbul, "İstanbul, "İstanbul, "İstanbul, "İstanbul, "İstanbul, a.

## Konsepten bir şey.

### Üç parti API'si

**OpenAI Batch API**JSONL dosyası yüklenmesi, talepler listesine sahip. 24 saatlik dönüşü söz verilir (genellikle pratikte ~ 2-8 saat). Girme ve çıkış tokenlerinde %50 indirim. `/v1/batches`Kaynaklı girişler de önbelleğe girme fiyatlandırmasını üstlenir.

**Anthropic Message Batches**JSONL yükleme, 24 saatlik dönüş, %50 indirim.`cache_control` önbelleğe yazılar açıkça, okumalar otomatik olarak seri içinde gerçekleşir.

**Google Vertex AI Batch Prediction**BigQuery veya GCS girişleri. Gemini için benzer %50 indirim. Vertex boru hattlarıyla entegre.

### Semantik: Asinkron, yavaş değil

Satış "24 saat içinde geri döneceğime söz veriyorum"  değil "Bu 24 saat sürecek". Tipik P50 2-6 saat.

### Önbelleği ile dolu

> **【拓展：批处理 + 缓存的叠加经济模型】**批处理 + 缓存叠加的具体经济模型:50K 文档摘要任务,共享 4K-token 系统提示──同步未缓存:50000 × ($input × 4000 + $Çıkış × 200) 全价;同步+缓存:系统提示首次写入后,后续 49999次享受约10x更便宜的输入;批处理+缓存:上述所有基础上再加50%折扣──最终结果:批处理 + 缓存 =同步未缓存成本的约10%──任何隔夜运行和共享系统提示的工作负载都应使用这个组合──

Aynı 4K token sistemi ile 50k belge özetleme:

- Sinkron kaydedilmemiş: 50000 × ($input × 4000 + $Çıktı × 200) tam hızlarda.
- Sinkron önbelleğe alınan: sistem tesisi ilk yazımdan sonra önbelleğe alınır; kalan 49999'ün 10 kat daha ucuz giriş elde edilir.
- Parça önbelleğe alınmış: yukarıdaki tümü artı okuma ve yazma için %50 indirim.

Satır: parti + önbelleğe = %10 eşzamanlı önbelleğe alınmamış faturanın. Gece boyunca çalışan ve paylaşılan bir sistem uyarısı olan herhangi bir iş yükü bunu kullanmalıdır.

### İş yükü sınıflandırması

> **【中文解读】**工作负载分诊是批处理 API'nin kullanımı önemi. 三条车道:(1) 交互式(user waiting response) TTFT 重要, must synergize调用+提示缓存;(2) 半交互式(user submit task,几分钟后回来查看) 异步队列+同步后备;(3) 批处理(user expectation"明早"或"一小时后") 内容流水线、大规模分类、离线分析, must批处理+叠加缓存;;

> **【拓展：批处理 API 的陷阱】**Satış İşleme API'si iki sıkı sıkıntısı vardır: 1) 部分交互性 user expectations比 24 小时更快(如带有"刷新"按的夜间报告),团队错误地使用同步调调用; 2) 输出方案 漂移不同供应商的批处理文件格式不同(OpenAI JSONL、Anthropic JSONL、Vertex BigQuery/TFRecord), "bir批处理客户端" yazmak için her sağlayıcı için bir adaption器 kodunu oluşturmak gerekir.

**Interactive** kullanıcı cevap bekliyor. TTFT önemli. Hızlı önbelleğe sahip eşzamanlı arama.

**Semi-interactive** kullanıcı bir görev gönderir, dakika içinde geri kontrol eder. Batch mevcut değilse senkronize etmek için fallback ile asynk kuyruk. Orta çaplı RAG indeksleme düşünün.

**Batch** kullanıcı sonuçları "sabah" veya "kötü saat"e kadar bekler. İçerik boruları, ölçekte sınıflandırma, çevrimdışı analiz. Her zaman seri, her zaman yığın önbelleği.

Genel hata: her şeyi etkileşimli olarak sınıflandırmak çünkü boru hattı üretimdir. Üretim bir gecikme speçikası değildir  SLA.

### Bölümsel etkileşim tuzağı

Bazı özellikler etkileşimli görünse de 5-10 dakika tolerantlık gösterir. Örnek: "Yenileştir" düğmesi ile gecelik bir müşteri sağlık raporu. Kullanıcı yenilgiye tıklıyor; 10 dakika beklemek iyidir. Takım onu eşzamanlı olarak gönderir. 50 eşzamanlı yenilgiye e-posta yoluyla toplanan ve teslim edilen maliyetin 10 katı maliyetini verir.

Eğer cevap "eğer fark etmezlerse"se, "24 saat bu kullanıcı için ne anlama gelir?" diye sormak için bir soru sor.

### Çıktı-sema tuzağı

Satış dosya biçimleri, sunucuya göre farklıdır:

- JSONL, her satırda bir talep.
- Antropik: JSONL, her satırda bir mesaj; cevap biçimi yerleştirilmiştir.
- Vertex: BigQuery tablo veya TFRecord ile GCS önlüğü.

"Bir seri istemcisi" yazmak, her bir sağlayıcı için adaptör kodunu ifade eder. Çoklu sağlayıcı seriyi reklamlayan geçitler (Portkey, LiteLLM bazı seviyeler) hala ham biçimi incelikle sarar.

### Hatırlamalısın numaralar

- Satış sağlayıcıları arasında parti indirme indirim + çıkış oranı %50 oranında sabit.
- Dönüşüm SLA: 24 saat garanti, 2-6 saat tipik P50.
- Yüklü seri + önbelleğe alınan giriş: Sinkronize edilmemiş önbelleğe alınan maliyetin %10'u.
- İş yükü sıralama kuralı: 24 saat gecikme kabul edilebilirse, her zaman seri.

## Çerçeveyi kullanın.
```figure
batch-lane-triage
```

## Kullan

`code/main.py`50k belge iş yükü için senkronize, senkronize + kas, parti ve parti + kas maliyetlerini hesaplar.

> `code/main.py`50k belge iş yükü için senkronize, senkronize + kas, parti ve parti + kas maliyetlerini hesaplar.

> `code/main.py`50k belge iş yükü için senkronize, senkronize + kas, parti ve parti + kas maliyetlerini hesaplar.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-batch-triager.md`. İş yükü özelliklerini göz önüne alarak, etkileşimli/yarı/batch'a ayırılır ve tasarruf tahmin edilir.

> 本课产 出 `outputs/skill-batch-triager.md`. İş yükü özelliklerini göz önüne alarak, etkileşimli/yarı/batch'a ayırılır ve tasarruf tahmin edilir.

## Egzersizler.

1. Çık .`code/main.py`. 3K-token sistem istekleri ve 500-token çıkışı ile 100k-doc boru hattı için, tam yığın (batch + cache) vs. senkronize tabanının tasarrufu hesaplanmalıdır.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ 100K için 文档管线(3K token 系统提示,共享缓存前),计算批处理 + 缓存 vs 同步成本。
2. Tanıdığınız gerçek bir ürünün üç özelliğini seçin.
   Çinçe Çevirimi: Sizde Bilen Gerçek Ürünler İçinde Seçilen Üç Fonksiyon.
3. Bir kullanıcı raporlarının 3 saat sürdüğünden şikayet ediyor.
   Çinçe Çevirimi: User complaint report has spent 3 hours. Bu birimcilik hatası mı yoksa beklenmiş bir davranış mı?
4. Bu durumun üstü, kapalı, kapalı ve kapalı sistemlerin üzerinde nasıl hareket ettiğini belirler.
   Çinçe Çevirimi: Senin toplama işlem API'nin SLA'yı geri göndermesi 24 saat ama P99'un 20 saat olması.
5. Hesaplama dengesi: Paylaşılan prefiks uzunluğunda, batch + cache, kendi rezerve GPU'da bir gecede çalışmaktan daha ucuz olur.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Batch API | "async discount" | 50% off with 24h turnaround |
| JSONL | "batch format" | One JSON request per line; OpenAI/Anthropic standard |
| Message Batches | "Anthropic batch" | Anthropic's batch API product name |
| Batch prediction | "Vertex batch" | Vertex AI's batch API product |
| Turnaround SLA | "24h promise" | Guarantee, not typical; typical is 2-6h |
| Workload triage | "interactivity decision" | Interactive / semi / batch routing decision |
| Output schema | "response format" | Per-provider JSONL layout; not portable |
| Stacked discount | "batch + cache" | ~10% of uncached sync bill when both apply |

## Daha fazla okumak

- [OpenAI Batch API](https://platform.openai.com/docs/guides/batch) JSONL biçimi ve `/v1/batches`- Semantik.
- [Anthropic Message Batches](https://docs.anthropic.com/en/docs/build-with-claude/batch-processing) parti biçimi ve `cache_control`etkileşim.
- [Vertex AI Batch Prediction](https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/batch-prediction-gemini)Gemini parti semantikası.
- [Finout — OpenAI vs Anthropic API Pricing 2026](https://www.finout.io/blog/openai-vs-anthropic-api-pricing-comparison)
- [Zen Van Riel — LLM API Cost Comparison 2026](https://zenvanriel.com/ai-engineer-blog/llm-api-cost-comparison-2026/)
