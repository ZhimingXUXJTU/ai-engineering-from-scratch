# Yük Testleri LLM API'leri  Neden k6 ve çekirge yalan söylüyor  yük test API neden LLM  ABD

> Geleneksel yük denetleyicileri akış cevapları, değişken çıkış uzunlukları, token seviyesindeki ölçümler veya GPU doymuşluğu için tasarlanmamıştır. İki tuzak çoğu takımı ısırıyor. GIL tuzağı: Locust'in token seviyesindeki ölçümü Python GIL altında tokenizeyi yürütür, bu da ağır eşzamanlılık altında talep üretimi ile rekabet eder; tokenize geri kalanı daha sonra bildirilen tokenler arası gecikmeyi  müşteriniz şişek boynusu, sunucu değil. Çevre-birliği tuzağı: bir döngüde aynı çevreler, jeton dağılımında bir noktayı test eder; gerçek trafiğin değişken uzunluğu ve çeşitli ön işaret eşleşmeleri vardır. LLMPerf bunu düzeltiyor .`--mean-input-tokens`+ `--stddev-input-tokens`. 2026 yılında araç haritası: Token düzeyinde doğruluk için LLM uzmanlığı (GenAI-Perf, LLMPerf, LLM-Locust, guidellm);**k6 v2026.1.0**+ **k6 Operator 1.0 GA (Sept 2025)** Akıştan haberdar, TestRun/PrivateLoadZone CRD'ler üzerinden dağıtılan Kubernetes-native, CI/CD kapıları için en iyisi; Vegeta for Go sabit oranlı beslenme; Akış için sadece LLM-Locust uzantısı ile 2.43.3.

> **【中文解读】**Bu bölümde LLM API  yükleme testleri  değerlendirme önerisi hizmetlerinin yüksek yük altında performans gösterdiği test yöntemleri hakkında bilgi edindiler.


**Type:** Build | **类型:** 学习
**Languages:** Python (stdlib, toy realistic-prompt generator + latency collector) | **语言:** Python
**Prerequisites:** Phase 17 · 08 (Inference Metrics), Phase 17 · 03 (GPU Autoscaling) | **前置知识:** Phase 17 · 08 (Inference Metrics), Phase 17 · 03 (GPU Autoscaling)

>  **【前置】**学本节前 Lütfen önce bil:Fase 17·08(指标)、Fase 17·03(GPU 扩缩)。 geleneksel yükleme test cihazı 流式响应+变长输出设计。
>  **【类比】**LLM 负载测试 = "测自动驾驶 vs 测传统车"──两个陷:(1) GIL 陷:Locust 在 Python GIL 下做代币化,与请求生成抢锁→报告的代币 间延迟虚高(客户端是瓶不是服务端);(2) 快速 一致性陷:循环同步 快速只测分布一个点,真流量有多样化前匹配──LLMPerf 用`--mean-input-tokens+stddev`修复──2026 工具:GenAI-Perf/LLMPerf/LLM-Locust(LLM 专用) + k6 v2026.1(流式+K8s) + Vegeta(Go 常速率) + Locust(仅配 LLM-Locust 扩展)
**Time:** ~75 minutes | **时间:** ~75 minutes

## Öğrenme hedefleri

- Genel yük denetçilerinin LLM API'ler için yalan söylemesini sağlayan iki anti-önemli (GIL tuzağı, prompt-uniformity tuzağı) açıklayın.
  ÇINÇAMAN TRÜBLÜK: açıklama iki modüsün yanlış yönlendirmesini sağlar.
- Verilmiş bir amaç için bir araç seçin: LLMPerf (benchmark çalıştırma), k6 + akış uzatma (CI kapısı), guidellm (büyük ölçekli sentetik), GenAI-Perf (NVIDIA referansı).
  Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çözüm: Çizüm: Çizlem: Çizlem: Çizlem: Çizlem: Çizlem: Çizlem: Çizlem
- Dört yük örneğini (sağlam, ramp, spike, soak) tasarlayın ve her bir yakalama başarısızlık modunun adını verin.
  Çinçe Çevirimiçi: Design Four Sorunlu Modes (→ Çıkış, Çıkış, Çıkış, Çıkış)
- Yerleşik uzunluk yerine girme jetonlarının ortalama + stddev kullanılarak gerçekçi bir çabuk dağıtım oluşturun.
  Çinçe Çevirimiçi: %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 = %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2

## Sorunlar. Sorunlar.

> **【中文解读】**傳統負載測試工具不是LLM için tasarlanmış它们不支持流式响应、可变输出长度、token 级指标或 GPU 和度──两个常见陷:(1) GIL 陷Locust'ın token 级测量在Python GIL 下运行分词,高并发时代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代代

> **【拓展：LLM 负载测试的四种模式】**2026 yılında LLM  yükleme testinin dört farklı modeli: 1) 稳态(steady-state) 恒定 RPS 持续 30-60 dakika, kaptırma基线性能退化; 2) 渐增) ramp)  0 线性增加到目标 RPS, kaptırma kapasitesi断点和预热异常; 3) 突发(spike) 突然 3-10x RPS 持续 2 分钟然后回落,测试自动扩张响应、队列和和和冷启动影响; 4) 时间(浸水) 稳态持续 4-8 小时,捕获内存漏、连接池漂移和可观测性溢溢.

LLM son noktını 500 aynı anda kullanıcı ile test ettin. 500 aynı anda kullanıcı ile test ettin.

İki şey oldu. Birincisi, k6 500 aynı istek gönderdi.  istek toplama ve önbellek önbelleği önbelleğin aslında bir taneyle uğraşırken 500 eşzamanlı dekod kullanıyormuş gibi görünmesini sağladı. İkincisi, k6 akış tepkilerindeki tokenler arasındaki gecikmeyi izlemiyor. Gözün deneyimlediği şekilde; bir HTTP bağlantısını görür, değişik aralıklarla gelen 500 tokeni değil.

LLM'ler için yük testi kendi disiplinidir.

## Konsepten bir şey.

### GIL Tuzakı (Locust)

> **【拓展：Python GIL 对 LLM 负载测试的影响】**Python GIL(全局解释器锁) LLM 负载测试的影响:Locust Python 运行客户端分词,在高并发时代代代码化 队列排在请求生成后面。报告的间代码 延迟包含客户端代码化 积压你以为是服务器慢,其实是测试工具的瓶──解决方案:(1) LLM-Locust 扩展将代码化 移至独立进程;(2) 使用编译语言工具k6kk) rfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

Locust Python'u kullanır ve GIL altında tokenizasyon istemcisini çalıştırabilir. Yüksek eşzamanlılık altında, talepleri oluşturmak arkasındaki tokenizer kuyrukları. Raporlanan inter-token gecikmesi, istemci tarafındaki tokenizasyon arka planını içerir. Sunucu yavaş olduğunu düşünüyorsunuz; test harnesidir.

Düzeltme: LLM-Locust uzantısı, tokenizasyonu ayrı süreçlere taşıyor veya bir kompile dili harness kullanıyor (k6, tokenizers.rs kullanarak LLMPerf).

### Hızlı bir uyum tuzağı

Tüm bilinen yük denetleyicileri bir istek ayarı yapılandırmanıza izin verir. 10.000 tekrarlı bir döngü testinde her seferinde aynı istek gönderir. Sunucu her  ön ön önbellek kaş'ı vurduğunda aynı önbellek görür. %100'e yaklaşırken, geçiş mükemmel görünüyor.

Düzeltme: hızlı bir dağıtımdan alınan örnek.`--mean-input-tokens 500 --stddev-input-tokens 150` Çeşitli uzunluklar, çeşitli içerikler.

### Dört yük örneği

1. **Steady-state** 30-60 dakika boyunca sabit RPS. Yakalamalar: başlangıç performans gerilemeleri.
2. **Ramp** RPS'yi 15 dakikadan fazla sürede 0'dan hedefe linear olarak artırmak.
3. **Spike**2 dakika sonra 2-10 kat süren süren süren süren.
4. **Soak**4-8 saat boyunca sabit durum. Yakalamalar: hafıza sızıntıları, bağlantı havuzunun sürüşü, gözlemlenebilirlik aşırılığı.

### 2026 Araç haritası

> **【中文解读】**2026 yıl LLM 负载测试工具选择:(1) LLMPerf(Anyscale)Rust-backed 分词 + 流式感知,性能测试的默认选择;(2) NVIDIA GenAI-PerfNVIDIA 参考工具,注意其 ITL 不含 TTFT;(3) LLM-Locust(TrueFoundry)Locust 扩展,修复 GIL 问题;(4) k6 v2026.1.0 + k6 Operator 1.0 GA(2025 yıl 9 月) Go编译、无 GIL、流式、知感ernetes-native 分布测试,CI/CD gate 最佳选择──

> **【拓展：CI/CD 中的 SLA Gate】**CI'de k6'nın SLA kapısı kullanın 配置:每次 PR 运行 30-50 次代,gate 指标包括 P50/P95 TTFT、5xx < 5%、TPOT 在值以下──违规则构建失败──使用真实提示分布(mean + stddev of input tokens)而非固定长度LLMPerf 使用`--mean-input-tokens 500 --stddev-input-tokens 150`ÖZGÜNİNİN ÖZGÜNİNİN ÖZGÜNİNİN ÖZGÜNİN

**LLMPerf**(Anyscale) Python ama Rust desteklenen tokenizasyon. Ortalama / stddev istekleri. Akıştan haberdar. Performans çalışmalar için en iyi varsayılan.

**NVIDIA GenAI-Perf** NVIDIA'nın referansı. Triton istemcisini kullanır; kapsamlı metrik kapsam. Not ITL TTFT hariç; LLMPerf'in içerdiğini unutmayın.

**LLM-Locust**GIL tuzağını düzelten çekirgeler uzantısı.

**guidellm** Büyük ölçekli sentetik referans değerlendirme.

**k6 v2026.1.0**+ **k6 Operator 1.0 GA (Sept 2025)**- ...
- k6 kendisi (Go, oluşturulmuş, GIL yok) akıştan haberdar metrikler ekledi.
- k6 Operator, Kubernetes- doğuştan dağıtılmış testler için TestRun / PrivateLoadZone CRD'leri kullanır.
- CI/CD kapıları ve SLA testleri için en iyisi.

**Vegeta** Git, k6'dan daha basit. Sürekli HTTP doymuşluğu. LLM bilgili değil ama geçit / hız sınırı testleri için iyidir.

**Locust 2.43.3 stock** LLM için GIL tuzağı vardır. Sadece LLM-Locust uzantısı ile.

### SLA kapısı CI

İletişimde k6 çalıştır:

- Her biri 30-50 tekrarlar, başlangıç RPS'de.
- Kapı: P50/P95 TTFT, 5xx < 5%, TPOT eşiğinden aşağı.
- Çatışmayı boz.

### Gerçekçi bir hızlı dağıtım

Gerçek trafik örneklerinden (eğer varsa) veya yayınlanan dağıtımlardan (örneğin sohbet için ShareGPT istekleri, kod için HumanEval) oluşturun.

### Hatırlamalısın numaralar

- k6 Operatör 1.0 GA: Eylül 2025.
- K6 v2026.1.0: Akıştan haberdar olan ölçümler.
- Tipik LLMPerf çalışması: 100-1000 istek eşzamanlı X.
- Tipik CI kapısı: PR'ye 30-50 tekrarlama.
- Dört model: sabit, ramp, tırnak, ıslak.

## Çerçeveyi kullanın.
```figure
load-pattern-waves
```

## Kullan

`code/main.py`gerçekçi bir hızlı dağıtım ile yük testi simülasyonu, etkili TPOT ölçümleri ve benzer bir hızlı tuzak gösterimi.

> `code/main.py`gerçekçi bir hızlı dağıtım ile yük testi simülasyonu, etkili TPOT ölçümleri ve benzer bir hızlı tuzak gösterimi.

> `code/main.py`gerçekçi bir hızlı dağıtım ile yük testi simülasyonu, etkili TPOT ölçümleri ve benzer bir hızlı tuzak gösterimi.

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-load-test-plan.md`İş yükü ve SLA'yı göz önünde bulundurarak, araç seçer ve dört yük örneğini tasarlar.

> 本课产 出 `outputs/skill-load-test-plan.md`İş yükü ve SLA'yı göz önünde bulundurarak, araç seçer ve dört yük örneğini tasarlar.

## Egzersizler.

1. Çık .`code/main.py`-Eskilik ve gerçekçilik arasındaki dağılımları karşılaştırın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`◊P99 TTFT 差异在哪里?
2. CI kapısı için k6 senaryosunu yaz: TTFT P95 < 800 ms 100 eşzamanlı, 5 dakika çalıştırma süresi.
   Çinçe Çevirimiçi: 编写 CI 门控的 k6 脚本:100 并发下 TTFT P95 < 800ms,运行 5 分钟──
3. Sıkıştırma testi 50 MB/saat hafızayı artırdığını gösteriyor.
   Çinçe Çevirimi: Your Bubble Test shows内存 per hour growth 50MB.
4. Spike test 10 RPS'den 100 RPS'e kadar. Karpenter + vLLM üretim-buçukları yerlerinde ise beklenen kurtarma süresi nedir (Fase 17 · 03 + 18)?
   Çinçe Çevirim: 10 RPS 尖峰测试~100 RPS ⋅ Eğer Karpenter  45 saniye bekliyorsa, geri dönüş süresi ne kadar?
5. GenAI-Perf TPOT=6ms rapor ediyor. LLMPerf aynı sunucuda TPOT=11ms rapor ediyor.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| LLMPerf | "the LLM harness" | Anyscale benchmark tool, streaming-aware |
| GenAI-Perf | "NVIDIA tool" | NVIDIA reference harness |
| LLM-Locust | "Locust for LLMs" | Locust extension fixing GIL trap |
| guidellm | "synthetic benchmark" | Large-scale synthetic tool |
| k6 Operator | "K8s k6" | CRD-based distributed k6 |
| GIL trap | "Python client overhead" | Tokenization backlog inflates reported latency |
| Prompt-uniformity trap | "single-prompt lie" | Loop with same prompt hits cache, inflates throughput |
| Steady-state | "constant load" | Flat RPS for N minutes |
| Ramp | "linear up" | 0 to target over duration |
| Spike | "burst test" | Sudden multiplier then revert |
| Soak | "long test" | Hours for leak detection |

## Daha fazla okumak

- [TianPan — Load Testing LLM Applications](https://tianpan.co/blog/2026-03-19-load-testing-llm-applications)
- [PremAI — Load Testing LLMs 2026](https://blog.premai.io/load-testing-llms-tools-metrics-realistic-traffic-simulation-2026/)
- [NVIDIA NIM — Introduction to LLM Inference Benchmarking](https://docs.nvidia.com/nim/large-language-models/1.0.0/benchmarking.html)
- [TrueFoundry — LLM-Locust](https://www.truefoundry.com/blog/llm-locust-a-tool-for-benchmarking-llm-performance)
- [LLMPerf](https://github.com/ray-project/llmperf)
- [k6 Operator](https://github.com/grafana/k6-operator)
