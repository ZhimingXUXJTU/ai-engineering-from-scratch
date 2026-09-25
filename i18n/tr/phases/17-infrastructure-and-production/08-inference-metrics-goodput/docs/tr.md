# İndirim Metrikleri  TTFT, TPOT, ITL, Goodput, P99  推理 指标 Goodput

> Dört metrik bir sonuç dağıtımının işe yaramayacağını belirler. TTFT, ön doldurma artı sıra artı ağ. TPOT (aynı şekilde ITL) bir token başına hafıza bağlı dekod maliyetidir. Son-son gecikme TTFT artı TPOT çarpı çıkış uzunluğu. Geçim, filonun her birinde toplanan saniyede tokenlerdir. Ama ürün için önemli olan şey, her SLO'yu aynı anda karşılayan isteklerin %2'si. Yüksek geçiş, düşük iyi çıkış demek oluyor ki kullanıcılara asla zamanında ulaşmayan tokenleri işletiyorsunuz. 2026 yılında Llama-3.1-8B-Instruct on TRT-LLM için referans numaraları: ortalama TTFT 162 ms, ortalama TPOT 7,33 ms, ortalama E2E 1,093 ms. Her zaman P50, P90, P99 'yi bildir. Ve ölçüm tuzağına dikkat edin: GenAI-Perf TTFT'yi ITL hesaplamasından çıkarır, LLMPerf onu içerir; aynı çalışmada TPOT hakkında iki araç anlaşmazlık yaşıyor.

> **【中文解读】**Bu bölümde, hizmet kalitesi için önemli bir gösterge sistemi ve Goodput ölçümünü tanıttık.
**Type:** Learn
**Languages:** Python (stdlib, toy percentile calculator and goodput reporter)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy percentile calculator and goodput reporter) | **语言:** Python（标准库，百分位计算器和 Goodput 报告器）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 17 · 04（vLLM 服务内部）

>  **【前置】**Öğrenci bölümün önüne geçerek: 17·04 aşama: vLLM) 统计基础: 百分位: 推理指标四件套:TTFT (Büyük) 时间: 首代币: 时间: 首代币: 首代币: 时间: 首代币: 首代币: 时间: 首代币: 首代币: 时间: 首代币: 首代币: 时间: 首代币: 首代币: 时间: 个代币: 时间: 个代币: 个代币: 个代币: 个代币: 个代币: 个代币: 个代币: 个代币: 个代币: 个代币: 个代币: 个代币: 个代币: 个代币: 个代币: 个代币: 个代币: 个代币: 个代币: 个代币: 个代币: 个个代币: 个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个个
>  **【类比】**推理指标 = "餐厅 KPI"。TTFT = 顾客 sitteth till第一道菜上桌(prefill+queue+network);TPOT = 后续每道菜间隔(解码成本);吞吐量 = 餐厅每小时出餐总数;Goodput = 满足所有SLO'nun talep oranı(关键!)。陷:高吞吐低 Goodput = çok fazla yemek yapmış ama müşteriler yemek vaktiyle karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı karşı
**Time:** ~60 minutes | **时间:** ~60 分钟

## Öğrenme hedefleri

- TTFT, TPOT, ITL, E2E, throughput ve goodput'u kesin olarak tanımlayın ve her bir ölçümün bileşeninin adını verin.
  Çinçe Çevirim: TTFT、TPOT、ITL、E2E、吞吐量和 Goodput,并说出每个指标测量的组件──
- LLM hizmetleri için neden ortalama yanlış istatistik olduğunu ve P50/P90/P99'u nasıl okuyacağını açıklayın.
  Çinçe Çevirimi: Neden ortalama değer LLM  servisin yanlış statistikası, ve nasıl okuyacağını açıklayın P50/P90/P99。
- SLO çok kısıtlama oluşturun (örneğin TTFT < 500 ms ve TPOT < 15 ms ve E2E < 2 s) ve buna göre iyi değer hesaplayın.
  Çin dilinde: yapı yapı SLO 多约束(如 TTFT<500ms 且 TPOT<15ms 且 E2E<2s)并据此计算 Goodput。
- Aynı çalışmada TPOT konusunda anlaşmazlık çeken iki referans araçını isimlendirin ve nedenini açıklayın.
  Çinçe Çevirisi: Çıkarmak için iki farklı sonuç elde etmek için iki farklı test aracı bulunmaktadır.

## Sorunlar. Sorunlar.

> **【中文解读】**推理服务有多延迟轴,每个轴以不同方式失败──预先是计算有限的,随提示长度增长;Decode是内存有限的,随批量 增长;排队延迟是运维问题;网络是物理距离问题──需要不同的指标来衡量每个维度,需要百分数,还需要一个综合指标来说"用户是否获得预期的体验"这就是Goodput──

> **【拓展：LLM 推理指标体系】**2026 yılında LLM 推理的完整指标体系包括:(1) TTFT(首代币 延迟) 用户感知到的首次响应时间;(2) TPOT/ITL(每代币 延迟/inter-token 延迟) 流式输出平滑度;(3) E2E(端到端延迟) 请求到完成的总时间;(4) Throughput(吞吐量) 集群效率指标;((((((有效吞吐) 同时满足所有 SLA 请求比例;;ML已Perf Inference v6.0  Goodput 作为官方提交指标.

"Bizim geçiş kapasitemiz saniyede 15.000 token". Peki ne? Soruların %40'ı 2 saniyeden sonra uçtan uçuna uçtuysa kullanıcılar oturumu terk etti.

> "Bizim sıfırlama hacmi saniyede 15.000 token. " Peki ya? Eğer talebinin %40'ı sonuna kadar 2 saniye geçirse, kullanıcı konuşmayı terk eder.

İndirim, çok sayıda gecikme eksine sahiptir ve her biri farklı şekilde başarısız olur. Ön doldurma hesaplama ile bağlı ve uzunlukla ölçülür. Dekod, hafıza ile bağlanmış ve seri boyutları ile ölçeği. Çekilme gecikmesi operasyonel bir sorun. Ağ fiziksel mesafe sorunu. Her biri için farklı ölçümlere ve yüzdelilere ihtiyacınız var ve "kullanıcı beklediğini aldı mı" diyen tek bir bileşik gerekiyor.

> 推理有多延迟轴,每个轴以不同方式失败──预填是计算限制的,随提示长度增长──解码是内存限制的,随批次大小增长──排队延迟是运维问题──网络是物理距离问题──网络是物理距离问题──各维度需要不同的指标,需要百分数,还需要一个综合指标说"用户是否获得预期的体验"这是Goodput──

## Konsepten bir şey.

### TTFT  ilk token için zaman

> **【中文解读】**TTFT = sırada_zaman + ağ_davası + prefill_time。Prefill 在长提示时占主导32K prompt 在 Llama 3.3 70B FP8 H100 上需要约800ms 的纯预填──排队时间是调度器的行为,网络请求包括 TLS 的线缆时间──TTFT 是用户在流式返回任何内容之前感知到的延迟──

`TTFT = queue_time + network_request + prefill_time`

Ön doldurucu, istekler uzun olduğunda baskın olur. Llama-3.3-70B FP8'de H100'de, 32k istekler ~ 800 ms saf ön doldurucu süresi alır. Sır zamanı yük altında programcı davranışıdır. Ağ istekleri TLS dahil bir tel süresi. TTFT, herhangi bir şey geri akışmadan önce kullanıcı tarafından görülen gecikme süresi.

> 预充在长提示时占主导──Llama-3.3-70B FP8 在 H100 上,32K 提示需要约800ms的纯预充──排队时间是负载下调度器的行为──网络请求是包括TLS的线缆时间──TTFT, kullanıcıların herhangi bir içerik akışında geri dönüşü önceden algılanan gecikme­den oluşmaktadır──

### TPOT / ITL  tokenler arası gecikme

> **【中文解读】**TPOT(output token başına zaman) = ITL(inter-token latency) = token başına dekode latency。公式:TPOT = (decode_forward_time + scheduler_overhead) / tokens_produced。在 Llama 3.3 70B H100 + 分块预填充下,TPOT 均值约 7ms;无分块预填充时,在长预填 邻居序列期间 TPOT 可升至 50ms。永远监控 P99 而非均值。

Bir miktar için birçok isim.`TPOT`(output token başına zaman), `ITL`(tokenler arası gecikme),`decode latency per token` her şey aynı. İlkden sonra ardıcıl akışlı jetonlar arasındaki zaman.

> Bir miktarda çok isim.`TPOT`(Hem çıkış göstergesi 时间)`ITL`(inter-token 延迟)`每 token 解码延迟`都是同一个──它是第一个代币 之后连续流式代币 间时间──

`TPOT = (decode_forward_time + scheduler_overhead) / tokens_produced`

Aynı Llama-3.3-70B H100 yığınında parçalanmış ön doldurma ile TPOT ortalaması ~ 7 ms. parçalanmış ön doldurma olmadan, komşu bir dizide uzun bir ön doldurma sırasında TPOT 50 ms'e kadar artabilir. P99'u izleyin, ortalama değil.

> Aynı Llama-3.3-70B H100'de %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük ön doldurma, %2 bölük öndegelik değil %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2 %2

### E2E gecikmesi

`E2E = TTFT + TPOT * output_tokens + network_response`

Uzun çıkışlar (> 500 token) için E2E TPOT-dominated. Uzun isteklerle kısa çıkışlar için E2E TTFT-dominated.

> 对于长输出(>500 token),E2E by TPOT 主导──对长提示的短输出,E2E by TTFT 主导──报告按输出长度分条件的E2E──

### Çıktıranlık

`throughput = total_output_tokens / elapsed_time`

Toplam metrik, filo verimliliğini anlatır, bireysel talep sağlığını anlatmaz.

> 聚合指标――告诉你集群效率――不告诉你单个请求的健康状况――

### İyi performans  gerçekten önemsediğin metrik

> **【中文解读】**İyilik % 60'da başarısızlık; düşük üretim % 99'da başarısızlık. İyilik % 2026 yılı MLPerf Inference v6.0 ve AI platform sağlayıcılarının iç SLA takipleri iyilik merkezi gösterge olarak kullanılır.

`goodput = fraction of requests meeting (TTFT <= a) AND (TPOT <= b) AND (E2E <= c)`

SLO, çok kısıtlama. Bir istek sadece her kısıtlama yerine getirildiğinde "iyi" olur. Goodput payıdır. 60% goodput'ta yüksek throughput başarısızlık demektir. 99% goodput'ta düşük throughput hedeftir.

> SLO çok kısıtlı bir süreçtir. Sadece tüm kısıtlamalar yerine geldiğinde, talep "iyi"dir. İyilik bu payın %60'sını oluşturur. İyilik %99'sını oluşturur.

2026 yılında, goodput, MLPerf Inference v6.0 gönderilerinde ve AI platform sağlayıcılarında SLA iç takipinde kullanılan ölçümdür.

> 2026 yıl,Goodput is MLPerf Inference v6.0  SLA  takip kullanım göstergesi  SLA                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

### Neden yanlış bir istatistik kötüdür?

> **【中文解读】**LLM 延迟分布是右偏的──一个包含长预填 邻居的解码批可能发发出 500 个 TPOT ~7ms的代币 和 20 个 TPOT ~60ms的代币──平均值 TPOT ise 9ms, ancak P99 TPOT ise 65ms──用户经常遇到 P99这是他们离开的原因──永远报告三元组(P50, P90, P99),用户体验,P99 是需要优化的目标──

LLM gecikme dağıtımları sağ taraftan eğiliyor. Bir uzun önceden doldurulan komşu ile bir dekodlama partisi TPOT ~ 7 ms ile 500 token ve TPOT ~ 60 ms ile 20 token gönderebilir. Ortalama TPOT 9 ms. P99 TPOT 65 ms. Kullanıcılar düzenli olarak P99'a çarpıyor  bu yüzden ayrılıyorlar.

> LLM 延迟分布是右偏的──一个包含长预填充邻居的解码批次发发出500 个 TPOT 约7ms的代币和20 个 TPOT 约60ms的代币──平均值 TPOT 是9ms──P99 TPOT 是65ms──用户经常遇到P99这是他们离开的原因──

Her zaman üçlüyi bildirin (P50, P90, P99). Kullanıcı deneyimi için, P99 optimizasyon yapmanız gereken bir şeydir.

> 始终报告三元组(P50、P90、P99) ・・・ kullanıcı deneyimleri için,P99'ın optimize edilmesi gerekir。

### Referans numaraları  Llama-3.1-8B-TRT-LLM'ye Örgüt, 2026

- Ortalama TTFT: 162 ms
  中文翻译:均值 TTFT:162ms
- Ortalama TPOT: 7,33 ms
  中文翻译:均值 TPOT:7.33ms
- E2E ortalaması: 1,093 ms
  中文翻译:均值 E2E:1,093ms
- P99 TPOT: parçalanmış prefill yapılandırmasına bağlı olarak 10-25 ms değişir.
  Çeviri:P99 TPOT:10-25ms,取決分块预填配置──

Bunlar yayınlanan NVIDIA referans noktalarıdır. Model boyutu (70B 3-5x gösterir), donanım (H100 vs. B200 ~ 3x) ve yük ile değişir.

> Bunlar NVIDIA tarafından yayınlanan referans verileri.

### Ölçüm tuzağı

> **【中文解读】**2026 yılının en yaygın kullanılan iki temel test aracı TPOT'de farklı sonuçlar elde etti: NVIDIA GenAI-Perf TTFT'yi ITL'den  hesaplama sırasında çıkarır, tıknağı 2'den başlayın, LLMPerf TTFT'yi içerir, tıknağı 1'den başlayın.

> **【拓展：LLM 基准测试工具生态】**2026 yılında LLM 推理基准测试工具包括:(1) NVIDIA GenAI-PerfTriton 客户端,全面指标覆盖,ITL 不含TTFT;(2) LLMPerf(Anyscale)Rust-backed 分词,流式感知,含TTFT 的ITL;(3) LLM-Locust(TrueFoundry)Locust 扩展,修复 GIL 问题;4) guidelm大规模合成基准测试;5)((((k6 v2026.1.0流式感知,Kubernetes-native──选择工具时要了解其ITL 定义差异──

En çok kullanılan 2026 referans araçlarından ikisi aynı çalışmada TPOT konusunda anlaşmazlık yaşıyor:

- **NVIDIA GenAI-Perf**ITL'nin başlangıcı 2. simge ile başlar.
  Çeviri:**NVIDIA GenAI-Perf**ITL'den 计算中排除 TTFT──ITL 开始──
- **LLMPerf**ITL, token 1'den başlar.
  Çeviri:**LLMPerf**TTFT: ITL: 1 个代币: 开始:

TTFT 500 ms ve 100 çıkış tokeni ile 700 ms toplam dekodla yapılan bir talebe göre GenAI-Perf raporları `ITL = 700/99 = 7.07 ms`LLMPerf raporları `ITL = 1200/100 = 12.00 ms`- Araç seçimi numarayı değiştirir.

> TTFT 500ms  100   Output token  700ms  Total çözümü  GenAI-Perf  Rapor`ITL = 700/99 = 7.07ms`,LLMPerf  rapor `ITL = 1200/100 = 12.00ms`❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖ ❖

Her zaman hangi aracı belirleyin ve tanımını yayınlayın.

> 始终说明使用哪个工具──始终发布定义──

### SLO'nun oluşturulması

> **【拓展：LLM SLO 设定参考】**2026 yıl önerilen tüketim seviyesinin 70B 对话模型 SLO:TTFT P99 <= 800ms、TPOT P99 <= 25ms、E2E P99 <= 3s(<300 token 输出)、Goodput >= 99%。Enterprise seviyesinin SLO 收紧 TTFT(200-400ms) ama genişleten E2E── ölçüm yöntemi: kullanarak gerçek 流量 veya LLMPerf 合成流量(`--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`), hedef 2x 峰值并发,运行 30-50 次代取百分位数──

2026 yılında 70B sohbet modeli için tüketiciye yönelik makul bir SLO:

- TTFT P99 <= 800 ms.
  Çeviri:TTFT P99 <= 800 ms
- TPOT P99 <= 25 ms.
  Çeviri:TPOT P99 <= 25ms(
- E2E P99 <= 3 s <300 token çıkışları için.
  中文翻译:E2E P99 <= 3s(<300 token 输出) 』
- İyi üretim hedefi >= 99%.
  Çeviri:Düzgün 目標 >= 99%。

Enterprise SLOs TTFT (200-400 ms) sıkıştırır ve E2E'yi gevşetir.

> 企业级 SLO 收紧 TTFT(200-400ms)并放宽 E2E──关键是写下来、测量全部三、并将Goodput 作为单一综合指标追踪──

### Ölçüm nasıl

- Gerçek trafik veya gerçekçi sentetik (LLMPerf ile `--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`)
  Çinçe Çevirimiçi:运行真实流量或逼真合成流量`--mean-input-tokens 800 --stddev-input-tokens 300 --mean-output-tokens 150`)。
- Referans değerleri için 2x eşzamanlılık hedefi.
  Çinçe Çevirimi:基准测试运行目标为2倍峰值并发──
- 30-50 tekrar çalıştırın, birleşik numuneden yüzdelik alın.
  Çinçe Çevirimi:运行 30-50 次代,取合并样本的百分位数──
- Araç adı, araç sürümü, modeli, donanım, eşzamanlılık, hızlı dağıtım ile yayınlayın.
  Çinçe Çevirimi Çevirisi: yayınlama zaman etiketleme araç adı, versiyon, model, cihaz, 发发数,提示分布──

## Çerçeveyi kullanın.
```figure
throughput-latency
```

## Kullan

`code/main.py`Bu, bir oyuncak iyilik hesaplayıcıdır. Sintez bir gecikme dağılımını oluşturun, SLO uygulayın ve iyilik hesaplayın. Aynı iz üzerinde GenAI-Perf vs LLMPerf TPOT farkını da gösterir.

> `code/main.py`Bu, bir örnek olarak Goodput  hesaplama makinesi oluşturur, SLO uygulaması, Goodput hesaplaması. Aynı izleri gösterir.

## İndirin . Ürünler .

> **【拓展：SLO 设定与 Goodput 门控】**2026 yılının önerdiği 70B 对话模型 SLO:TTFT P99 <= 800ms、TPOT P99 <= 25ms、E2E P99 <= 3s(<300 token 输出)、Goodput 目标 >= 99%。Enterprise level SLO 收紧 TTFT(200-400ms) ama放宽 E2E──关键实践:(1) CI/CD merkez kapısı 部署决策于 Goodput值而非吞吐量;(2) 2x 峰并发行基准测试;(((((运行 30-50 次取百分位数;(4) 发布时标工具名、版本、模型、硬件、发发数、代提示分布;;

Bu ders bize çok yararlı .`outputs/skill-slo-goodput-gate.md`. İş yükü ve SLO'yu göz önüne alarak, kapıların geçiş yerine iyi verim üzerinde kullanıldığı bir CI/CD hazır bir referans tarifi üretir.

> 本课产 出 `outputs/skill-slo-goodput-gate.md`❖ Gösterilen iş yükü ve SLO, Goodput yerine throughput olarak deployment kontrolü olarak bir CI/CD 绪'un temel test programı oluşturur.

## Egzersizler.

1. Çık .`code/main.py`P99 TPOT'i 30 ms'den 15 ms'e sıkıştırdığınızda goodput nasıl değişir?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`△ % 1 尾部尖刺的分布── P99 TPOT'da 30ms 收紧到 15ms 时 Goodput 如何变化?
2. Bir satıcı "Llama 3.3 70B H100'de 15.000 tok/s" diye alıntı yapıyor.
   Çinçe Çevirimi: 供应商报价"Llama 3.3 70B H100 上 15,000 tok/s"
3. Parça dolgu neden P99 TPOT'i korur ama TPOT'i kastetmez?
   Çin Çeviri: neden %99 TPOT'yi koruyorsun?
4. Ses asistanı için bir tüketici SLO oluşturun (ilk token okunmaz, duyulur). Hangi metrik en çok kullanıcı tarafından görünür?
   Çinçe Çevirimi: Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çıktı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Ç. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Çı. Ç. Ç. Ç. Çı. Ç. Ç. Ç. Ç. Ç. Ç. Ç. Ç. Ç. Ç. Ç. Ç. Ç. Ç. Ç. Ç. Ç
5. LLMPerf README ve GenAI-Perf belgelerini okuyun.
   Çinçe Çevirimiçi:阅读 LLMPerf README 和 GenAI-Perf 文档──找出工具在另外三个标志上的分歧──

## Anahtar Şartlar .

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| TTFT | "time to first token" / "首 token 时间" | Queue + network + prefill; dominated by prefill at long prompts / 队列+网络+预填充；长提示时由预填充主导 |
| TPOT | "time per output token" / "每输出 token 时间" | Memory-bound decode cost per token after first / 首个 token 后每 token 的内存受限解码成本 |
| ITL | "inter-token latency" / "inter-token 延迟" | Same as TPOT in most tools (not all — see GenAI-Perf) / 大多数工具中同 TPOT（非所有——见 GenAI-Perf） |
| E2E | "end to end" / "端到端" | TTFT + TPOT * output_len; response-side network on top / TTFT + TPOT * 输出长度；加上响应端网络 |
| Throughput | "tok/s" / "token 每秒" | Fleet efficiency; useless without latency percentiles / 集群效率；无延迟百分位数则无意义 |
| Goodput | "SLO-met rate" / "SLO 达标率" | Fraction of requests meeting every SLO constraint simultaneously / 同时满足所有 SLO 约束的请求比例 |
| P99 | "tail" / "尾部" | 1-in-100 worst-case latency; the user experience metric / 百分之一最差延迟；用户体验指标 |
| SLO multi-constraint | "the joint" / "联合约束" | AND of all three latency bounds; a request fails if any one is violated / 三个延迟界限的 AND；任一违反即失败 |
| GenAI-Perf vs LLMPerf | "the tool trap" / "工具陷阱" | Tools disagree on whether ITL includes TTFT / 工具在 ITL 是否包含 TTFT 上不一致 |

## Daha fazla okumak

- [NVIDIA NIM — LLM Benchmarking Metrics](https://docs.nvidia.com/nim/benchmarking/llm/latest/metrics.html) TTFT, ITL, TPOT'nin kanonik tanımı.
- [Anyscale — LLM Serving Benchmarking Metrics](https://docs.anyscale.com/llm/serving/benchmarking/metrics) alternatif tanımlar ve ölçüm tarifi.
- [BentoML — LLM Inference Metrics](https://bentoml.com/llm/inference-optimization/llm-inference-metrics) Gerçek yerleşimlerde uygulanan ölçüm.
- [LLMPerf](https://github.com/ray-project/llmperf) Ray tabanlı açık kaynak referans.
- [GenAI-Perf](https://github.com/triton-inference-server/perf_analyzer/blob/main/genai-perf/README.md) NVIDIA'nın referans araçları.
- [MLPerf Inference](https://mlcommons.org/benchmarks/inference-datacenter/) endüstri tarafından kabul edilen, iyilik tabanlı bir referans değeridir.
