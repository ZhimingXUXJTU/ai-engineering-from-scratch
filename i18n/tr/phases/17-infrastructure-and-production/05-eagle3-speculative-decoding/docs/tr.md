# Üretimdeki SPEKYULATFİK KADANMA EAGLE-3

> Tahmin edici çözme, hızlı bir taslak modeli hedefli modelle eşleştirir. Özet K tokenleri önerir; hedef tek bir ilerileme ile doğrulanır; kabul edilen tokenler ücretsizdir. 2026 yılında EAGLE-3 üretim derecesi varyasyonudur. Genel sohbette kabul oranı alfa'yı 0.6-0.8 bantına itip, ham toponlar yerine hedef modelin gizli durumlarında bir taslak başını eğitir. Doğru soru "Taplama ne kadar hızlı" değil "Trafikimde alfa nedir?" Eğer alfa ~ 0.55'in altına düşerse, spekülatör çözme yüksek eşzamanlılıkta net negatif olur çünkü reddedilen her taslama ikinci hedef ileri geçiş maliyetini öder. Bu ders önce alfa ölçmeyi ve ikinci olarak bayrağı çevirmeyi öğretir.

> **【中文解读】**Bu bölümde küçük modellerle tahmin yaparak büyük modellerin hızlandırılması için kullanılan teknikler hakkında bilgi edindiler.
**Type:** Learn
**Languages:** Python (stdlib, toy acceptance-rate simulator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 10 · 18 (Multi-Token Prediction)
**Time:** ~60 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy acceptance-rate simulator) | **语言:** Python（标准库，接受率模拟器）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 10 · 18 (Multi-Token Prediction) | **前置知识:** Phase 17 · 04（vLLM 服务内部）, Phase 10 · 18（多 Token 预测）

>  **【前置】**Öğrenci bölümünün ilk aşaması: 17·04(vLLM)、10·18(MTP 多 token 预测)、10·25(投机解码原理)。本节是生产版 EAGLE-3。
>  **【类比】**EAGLE-3 = "Üfadeci tarafından hazırlanmış bir taslak"──草稿模型(öntem) 速猜 K 个代币,目标模型一次验证──猜对=免费,猜错=多一次验证开销──EAGLE-3 创新:用目标模型隐藏状态训练草案(而非原始代币),接受率 α 提到 0.6-0.8──生产关键问题:α 在你的流量上多少?<0.55 时反而拖慢(拒绝的草案 浪费算力)必须先测α 再开旗──
**Time:** ~60 minutes | **时间:** ~60 分钟

## Öğrenme hedefleri

- Üç nesil spekülatör kodlama yöntemini anlatın ve EAGLE-3'ün EAGLE-2'den ve klasik bir taslak modelinden neyi değiştirdiğini açıklayın.
  Çinçe Çevirimiçi: 出推测解码的三代,并解释 EAGLE-3 相比EAGLE-2 和经典草案 模型改变了什么──
- Kabul oranı alfa'yı tanımlayın, alfa ve K'den beklenen hızlandırmayı hesaplayın (çeft uzunluğu) ve hedef eşzamanlılığınız için kırılma oranı alfa'yı belirleyin.
  Çinçe çevirisi: definise accept rate alpha, alpha 和 K(tası 长度) hesaplama beklenmiş hızlanma oranı,并确定目标并发下亏平衡 alpha。
- Spekülatör çözümü vLLM 2026'da neden seçme (devayla değil) olduğunu ve alfa ölçümsüz olarak açılmasının neden üretim karşıtı bir örneğe sahip olduğunu açıklayın.
  Çinçe çevirisi: Neden 2026 yılında vLLM içinde seçme (opt-in) ve neden alfa ölçümü açmaması için üretme karşı modeli olarak kullanılırsa açıklayın.
- Bir ölçüm planı yazın: hangi referans değerini, hangi dağıtımını uyarır, hangi eşzamanlılık noktasını, hangi metrikleri kapatacak.
  Çinçe çevirisi: write out measurement plan: hangi kılavuz testı, hangi hızlı, hangi gelişme noktası, hangi gösterge, hangi kontrol noktası.

## Sorunlar. Sorunlar.

> **【中文解读】**推理的解码阶段是内存带宽限的每解码一个代币 需要读取约140GB/s的权重,GPU 计算几乎空──推测解码利用这个空:K个候选代币的低价小模型生成K个候选代币,然后让目标模型在一次前向传播中验证所有K个个――接受率alpha,唯一重要的指标低于0.55 时推测解码在高并发下而反而有害──

> **【拓展：推测解码的产业应用】**Google 2025 yılında AI Deployment'e (Arama Motoru Özetleri) tarafından yayınlanacak.`speculative_config`作为官方接口──在生产中,推测解码特别适合实时对话(TTFT 敏感) 和代码补全(延迟敏感)场景──但需要注意:高并发(256+)

Dekode hafıza bağlıdır. Llama 3.3 70B FP8 çalışan bir H100'de, her dekode edilmiş token ~ 140 GB / s ağırlık okuyor ve bir token yayar. GPU hesaplama dekode sırasında neredeyse boştur.

> H100'de Llama 3.3 70B FP8'de, her çözümü token'ın 读取约140 GB/s'in ağırlığı ve bir token üretimi.

Speküel dekodlama boşluğu kullanır. K aday tokenlerini ucuz bir taslak modeli ile oluşturun, sonra hedef modelden tüm K'yi tek bir ileri geçitle doğrulamalarını isteyin. Her doğrulanmış token etkin olarak ücretsizdir (hedef her şekilde yapmalıydı).

> 推测解码利用这个差距――廉价的草案模型生成K个候选标记,然后让目标模型在一次前向传播中验证所有K个――每个验证通过的标记――实际上是免费的(分摊到目标模型应该做的K 批前向中) ――

Klasik taslak model yaklaşımı aynı ailenin daha küçük bir modelini kullanır (Llama 3.2 1B taslak Llama 3.3 70B için). Çalışır ama kabul oranı orta  daha küçük model dağıtım hedeften farklıdır. EAGLE, sonra EAGLE-2, sonra EAGLE-3 bir hafif çekim başını hedefin iç durumlarına doğrudan yönlendirir. Böylece çekim dağıtımı hedefi çok daha yakından takip eder. Bu yüzden alfa, 0.4'ten EAGLE-3'e 0.6-0.8'e gidiyor.

> 经典的草案 模型方法使用同系列的更小模型(Llama 3.2 1B 为 Llama 3.3 70B做草案)──它可行但接受率平更小模型的分布偏离目标──EAGLE、EAGLE-2、EAGLE-3 直接在目标模型的内部状态上训练轻量草案头,所以草案的分布更接近目标──这就是为什么从草案的0.4 升至EAGLE-3 的0.6-0.8──

Yaptığımız şey: EAGLE-3 2026'da vLLM'ye katılmayı seçti.`speculative_config`Alfa trafiğini ölçmeden onu açan takımlar, genellikle kuyruğun gecikmesini daha kötü, daha iyi görüyor.

> Önemli nokta: EAGLE-3 2026 yılında VLLM arasında seçme seçeneği vardır.`speculative_config`必須顯示設定──無標志,就沒有加速──不測真流量 alfa 就開啟的團隊常見尾部延遲變差而不是改善──

## Konsepten bir şey.

### Spekülatör çözme aslında ne satın alır

> **【中文解读】**推测解码的加速比公式为 `S = (1 + K*alpha) / (1 + verify_overhead)`❖ K=5, alfa=0.7 için teorik hızlanma 4.1x. Fakat gerçek üretim genellikle sadece 2-3x'e ulaşır, çünkü alfa gerçek akımda çok az 0.7'e ulaşır ve yüksek parti boyutlarında satışın arttığı doğrulanır.

Spec kodlaması olmadan, bir token maliyeti bir hedef ileri.`1 + K * alpha`Hızlandırma .`(1 + K * alpha) / (1 + epsilon)`Epsilon'un K=5, alfa=0.7 için,`(1 + 5*0.7) / (1 + 0.1) = 4.5 / 1.1 = 4.1x`Gerçek dünya rakamları 2-3 kat gruplanır çünkü alfa, üretim trafiğinde nadiren o kadar yüksek olur ve epsilon, yüksek seri büyüklüğünde büyür.

> 没有推测解码时,每次目标前向传播的成本.`1 + K * alpha`◊ hızlandırma`(1 + K * alpha) / (1 + epsilon)`, epsilon ise taslak + 验证开销── K=5, alfa=0.7:`(1 + 5*0.7) / (1 + 0.1) = 4.5 / 1.1 = 4.1x`◊ Gerçek veriler 2-3x'te yoğunlaşır çünkü alfa üretim hacmi çok az ve epsilon yüksek seri boyutlarında büyür.

### Neden alfa önemli olan tek metrik?

reddedilen tokenler kaybolmaz  ilk reddedilen token için ikinci bir hedef zorlar. Alfa'nın 0.4'e düştüğü bir iş yükünde, çekim ödemesi artı doğrulama artı yeniden çalıştırma ödenir. Yüksek eşzamanlılık (deyelim 256 eşzamanlı), dekodlama parti zaten "tek hedef" ve "target verify" arasındaki hafıza-bandwidth boşluğu küçülmeye yeterlidir. 2026 donanımlarının çoğunda alfa 0.55'in altında, spesifikasyon çözümü net negatif.

> Yabanlanmış token yok olmayacaklar. İlk reddedilen token'a ikinci hedef önüne doğru yayılmak zorunda kalırlar. Alfa  düşen 0.4 iş yükünde, bir taslak ödemenizi sağlar.

Alpha iş yüküne göre değişir. ShareGPT tarzındaki genel sohbette, ShareGPT'de eğitilmiş EAGLE-3 0.6-0.8'e ulaşır. Alan-özel trafiğe (kod, tıbbi, yasal) genel veri üzerine eğitilmiş taslak başı 0.4-0.6'a düşer.

> Alpha Because Workload and Difference. ShareGPT 风格的通用聊天天, ShareGPT 训练的EAGLE-3 达到0.6-0.8──在特定流量 (kode、医疗、法律) 领域上, 公共数据训练的草案头 (草案头) 降至0.4-0.6──训练领域的特定草案头可以恢复 alpha与目标微调相比,这是一个轻量、快速的训练任务──

### KİÇİN nesilleri bir bakışta

> **【中文解读】**推测解码经历了三代演进:(1) Klasik taslak modeli(同一系列的小模型,alpha 0.3-0.5)简单但接受率低;(2) EAGLE-1/2(目标模型隐藏状态上训练草案头,alpha 0.5-0.7)更高接受率;(3) EAGLE-3(多层隐藏状态上训练,alpha 0.6-0.8)2025-2026 yılları için üretim seviyesi方案──关键区别是 EAGLE 直接在目标模型内部表示上训练草案,而不是在原始代币上,因此分布更接近目标──

> **【拓展：推测解码 vs 其他加速技术】**LLM 推理加速技术对比:(1) 推测解码(EAGLE-3) 2-3x 加速, ekstra taslak başı gerektirir;(2) 量化(INT8/FP8) 推理加速 1.5-2x, hafif质量损失;(3) 分块预填降低ITL尾但不直接升吞;(4) 分离式预填/解码消除资源浪费,30-40% 成本节省;(5) 自研芯片(Groq/Cerebras) 5-10x 解码速度但单价更高──这些技术可叠加使用:EAGLE-3 + FP8 + 分离式部署的综合效果可达10x──

- **Classic draft model**Alfa 0.3-0.5. Altyapı basit  iki model yüklü, proje hedefe K ileri gidiyor.
  Çeviri:**经典 draft 模型**:同系列的小模型──Alpha 0.3-0.5──基础设施简单加载两个模型,草案 每次目标前向运行 K 次前向──
- **EAGLE-1 (2024)**Alfa ~ 0,5 - 0,6 . Hedeflerin üstündeki küçük parametre.
  Çeviri:**EAGLE-1 (2024)**: dans objectif hidden state (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en)  (en) )  (en)  (en)  (en) )  (en)  (en)  (en) )  (en)  (en)  (en) )  (en)  (en)  (en) )
- **EAGLE-2 (2025)**: adaptif taslak uzunluğu ve ağaç tabanlı taslaklar (bir hedef geçitinde birden fazla dalı doğrulayın). Alfa ~ 0.6-0.7. Daha karmaşık taslak programcı.
  Çeviri:**EAGLE-2 (2025)**Bu nedenle, bu projeyi yapabilmek için, bir süre önce, bir süre önce, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir sürece, bir sürececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececece
- **EAGLE-3 (2025-2026)**: Draft başı birden fazla hedef katman üzerinde eğitilmiştir (son değil), daha iyi bir uyum.
  Çeviri:**EAGLE-3 (2025-2026)**Bu yüzden, bu programın en iyi bir parçası olarak, daha iyi bir şekilde hazırlanmıştır.

### 2026 üretim tarifi

> **【中文解读】**Üretim ortamı EAGLE-3'ün beş adımlı süreçleri: 1) TTFT/ITL/吞吐量基线 oluşturmak için temel model oluşturmak; 2) EAGLE-3 taslakını etkinleştirmek; 3) kontrol kabul oranı alfavLLM V1 tarafından`spec_decode_metrics.accepted_tokens_per_request`暴露此指标;(4) Eğer alfa < 0.55,禁用推测解码或训练领域的特定草案头;(5) 在生产并发水平重新测试,确认 P99 ITL 没有恶化──

1. Görevli model açık. Temel TTFT, ITL, hedef eşzamanlılıktan geçiş ölçülür.
   Çinçe çevirisi:先以基础模型上线──在目标并发下测量基线 TTFT、ITL、吞吐量──
2. EAGLE-3 taslakını vLLM üzerinden etkinleştir `speculative_config`- Benchmark'ı tekrar çalıştır.
   Çeviri: VLLM`speculative_config`ATAGLE-3 taslakını başlatmak.
3. Günlük kabul oranı alfa. vLLM V1 bunu  olarak bildirir.`spec_decode_metrics.accepted_tokens_per_request`Alfa elde etmek için istenen çekim uzunluğuna bölün.
   Çeviri: kayıt kabul oranı alfa¬vLLM V1 通過 `spec_decode_metrics.accepted_tokens_per_request`Rapor: Arayanın taslakını çıkarıp, uzunluğu alfa ile elde edilir.
4. Eğer alfa < 0,55 üretim trafiği dağılımında ise, spesifikasyonları çözmeyi engelle veya alanı özel bir EAGLE-3 taslakını çalıştırın.
   Çinçe çevirisi: Eğer üretim akım dağılımının alfa < 0.55, kısıtlı olarak EAGLE-3 taslakını kullanmak zorunda kalmak veya eğitim alanında belirli bir EAGLE-3 taslakını kullanmak zorunda kalmak zorunda kalmak.
5. P99 ITL'nin daha da kötüleşmediğini doğrulayın.
   Çinçe Çevirimiçi: в производство并发下重新测试──确认 P99 ITL 没有恶化──

### Üretim sıkıntısı: P99 kuyruğu

P99'un ayarlanmaması durumunda daha da kötü olabilir. reddedilen taslaklar iki geçiş dizisini tetikler (taslak + doğrulama başarısızlığı + yeniden kaydırma). Tam parti altında, bu iki geçiş seriye edilir. P99 ITL'ye bak, P50 değil.

> 平均 ITL 随推测解码下降──如果不调优,P99可能恶化──被拒绝的草案 触发两次传递序列(草案 + 验证失败 + 重新生成)──在满批次下,这两次传递串行化──关注 P99 ITL,而不是 P50──

### EAGLE-3'ün zaten kullanıldığı yerler

Google 2025 yılında AI Özetlerinde spekülatör çözümü (aynı kalite, daha hızlı yanıt) yerleştirdi. vLLM V1 gemileri `speculative_config`V1'de N-gram GPU spekülatif çözümü, parçalanmış prefill ile uyumlu olan bir variandır. SGLang, prefix ağır iş yükleri için önerilirken EAGLE-3'yi önerilen taslak yolu olarak destekler.

> Google 2025 yılında AI'ye dağıtılacak.`speculative_config`V1 içindeki N-gram GPU 推测解码与分块预填兼容的变体──SGLang 支持 EAGLE-3 作为前密集工作负载的推草案路径──

### Bir satırdaki matematikleri düzeltmek

Beklenen hızlandırma: `S(alpha, K) = (1 + K*alpha) / (1 + verify_overhead)`- Yapılandırma`S = 1`alfa için çözünür: `alpha_breakeven = verify_overhead / K`. Tipik verify_overhead ~0.15 ve K=5: `alpha_breakeven = 0.03`Bu durum, çürük dekod matematikidir. Yüksek eşzamanlılıklarda doğrulama üstü maliyetleri artıyor ve dekod partiyası zaten hafıza okumalarını sekanslar boyunca amortize eder, bu yüzden etkili alfa_breakeven pratikte ~0.45-0.55'e tırmanır.

> 预期加速比:`S(alpha, K) = (1 + K*alpha) / (1 + verify_overhead)`▽设 `S = 1`求解 alpha:`alpha_breakeven = verify_overhead / K`❖ tipik verify_overhead 约0.15,K=5:`alpha_breakeven = 0.03`▽ ama o orijinal çözümü matematiği. ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ 

### Tahmin edici şifrelemeyi ne zaman kullanmamak gerekir

> **【拓展：推测解码的适用场景】**推测解码在以下场景有效:(1) 实时对话(TTFT < 200ms 要求) 2-3x 加速显著改善用户体验;(2) 代码补充(实时性要求高);(3) 低并发场景(< 50 concurrent) 内存带宽差距大,收益明显。在以下场景应避免:(1) 批量离线生成延迟不重要, plain target;(2) 短输出< 50 token) 草案 开销和验证成本主导;(3) 专业领域无领域训练的草案) alpha 太;(4) vLLM v0.18.0 +草案-model + 零点-pre-model + 组合 兼容

> **【拓展：vLLM 推测解码配置】**vLLM V1 支持三种推测解码模式:(1) Tasarım modeli传统小模型作为草案,与零碎预填不兼容;(2) EAGLE在隐状态上训练的草案头,用于通用场景;(3) N-gram GPU基于提示 中 N-gram 查找的 GPU 端草案,是唯一与零碎预填 兼容的模式──`speculative_config`必須顯示設定, vLLM 默认不開任何推测解码──

- Batch-1 offline jenerasyonu, gecikme önemi olmayan.
  Çinçe çevirisi:延迟无关紧要的批量为 1 的离线生成──使用普通目标模型──
- Çok kısa çıkışlar (50 token altında) Draft overhead ve verification cost baskın.
  Çinçe Çevirimi: çok kısa 输出(50 token 以下) ・ draft 开销和验证成本占主导──
- Özel alanlar, alan eğitimi olmayan bir başlık.
  Çinçe Çevirimiçi:没有领域训练草案负责的专业领域──Alpha 太低──
- vLLM v0.18.0 ve taslak model özellikleri çözme ve `--enable-chunked-prefill`Bu kombinasyon birleştirilmez. Belli bir istisna V1'deki N-gram GPU spesifikasyonunu çözme.
  中文翻译:vLLM v0.18.0 + taslak-model 推测解码 + `--enable-chunked-prefill`△ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △ △                                                      

## Çerçeveyi kullanın.
```figure
mx-speculative-tree
```

## Kullan

`code/main.py`K. bir dizi alfa değer ve taslak uzunlukları boyunca spekülasyonsal dekodlama ile ve olmadan bir dekodlama döngüsünü simüle eder. K. koparma alfa, ölçülen hızlanma ve kuyruğu davranışını yazdırırır.

> `code/main.py`模拟有/无推测解码的解码循环,覆盖一系列 alpha 值和草案 长度 K──它印打亏平衡 alpha、测量加速比和尾部行为──在多个 (alpha, K) 组合上运行,精确看推测解码在哪里停止收益──

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-eagle3-rollout.md`. Hedef model, trafik dağılımının açıklaması ve eşzamanlılık hedefi göz önüne alındığında, aşamalı bir EAGLE-3 dağıtım planı  referans tabanı üretir, yapılandırmayı, alfa ölçümünü, alfa >= 0.55, P99 ITL'yi etkinleştirir.

> 本课产 出 `outputs/skill-eagle3-rollout.md` belirlenmiş hedef modeli  akım dağılım açıklaması ve                                                                                                                                                                                                                                                                     

## Egzersizler.

1. Çık .`code/main.py`K=5'te 2x hızlandırmak için hangi alfa'ya ihtiyacınız var? 3x hızlandırmak için?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`K=5 时,2x 加快需要多少 alfa?3x 加快呢?
2. Üretim trafiğinin %70 genel sohbet, %30 kod bölüştüğünü düşünün. Genel sohbet, ShareGPT'de eğitilmiş EAGLE-3 ile alfa 0.7'e ulaşır; kod alfa 0.4'e ulaşır.
   Çin dilinde çevirme:假设生产流量 70% 通用聊天,30% 代码──通用聊天 alfa 0.7,代码 alfa 0.4──混合 alfa 是多少,推测解码是否净正向?
3. VLLM oku `speculative_config`Dokümanlama. Üç modun (önerge modeli, EAGLE, N-gram) ve hangi bir mod parçalanmış prefill ile uyumlu olduğunu belirtin.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri: Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç`speculative_config`文档──说出三种模式(Müziketi modeli、EAGLE、N-gram)及哪个与分块预填兼容──
4. EAGLE-3'i etkinleştirdikten sonra ortalama ITL'de %25 düşüş görüyorsunuz ama P99 ITL'de %15 artış var.
   Çin dilinde: EAGLE-3'yi etkinleştirmek için ortalama ITL %25 düştü, fakat P99 ITL %15 yükseldi.
5. Llama 3.3 70B için EAGLE-3 çekim başlığının hafıza maliyetini hesaplayın.
   Çine dilinde:计算 Llama 3.3 70B'nin EAGLE-3 taslak başı 内存成本──与运行 Llama 3.2 1B 作为经典草案相比如何?

## Anahtar Şartlar .

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| Speculative decoding | "draft plus verify" / "draft 加验证" | Propose K tokens with a cheap model, verify all K in one target forward / 用廉价模型提议 K 个 token，一次目标前向验证所有 K 个 |
| Acceptance rate alpha | "spec accept rate" / "推测接受率" | Fraction of draft tokens accepted by the target; the only metric that matters / 被 target 接受的 draft token 比例；唯一重要的指标 |
| Draft length K | "spec k" / "推测 K" | How many tokens the draft proposes per target forward; typical 4-8 / 每次 target 前向 draft 提议多少 token；通常 4-8 |
| Verify overhead epsilon | "spec overhead" / "推测开销" | Extra cost to verify-and-reroll vs a plain target forward; grows with batch / 验证+重新生成 vs 普通 target 前向的额外成本；随 batch 增长 |
| EAGLE-3 | "latest EAGLE" / "最新 EAGLE" | 2025-2026 variant; trains draft head on multiple target layers; alpha 0.6-0.8 / 2025-2026 变体；在多个 target 层上训练 draft head |
| `speculative_config` | "vLLM spec config" / "vLLM 推测配置" | The explicit opt-in in vLLM V1; no default means no acceleration / vLLM V1 中的显式 opt-in；无默认即无加速 |
| N-gram spec decode | "N-gram draft" / "N-gram draft" | GPU-side draft using N-gram lookups in the prompt; chunked-prefill-compatible / GPU 端使用 prompt 中 N-gram 查找的 draft；与分块预填充兼容 |
| Break-even alpha | "no-op alpha" / "无效果 alpha" | Alpha at which spec decode gives zero speedup; watch this at production concurrency / 推测解码零加速的 alpha；在生产并发下关注 |
| Rejected-draft two-pass | "reroll cost" / "重新生成成本" | Two target forwards when drafts reject; drives P99 tail / draft 被拒绝时的两次 target 前向；驱动 P99 尾部 |

## Daha fazla okumak

- [vLLM — Speculative Decoding docs](https://docs.vllm.ai/en/latest/features/spec_decode/) yetkili kaynak `speculative_config`V1'de parçalanmış prefill uyumluluğu.
- [vLLM Speculative Config API](https://docs.vllm.ai/en/latest/api/vllm/config/speculative/) tam alan seti.
- [EAGLE paper (arXiv:2401.15077)](https://arxiv.org/abs/2401.15077) orijinal EAGLE çekim başlığı formülasyonu.
- [EAGLE-2 paper (arXiv:2406.16858)](https://arxiv.org/abs/2406.16858) Adaptif taslaklar ve ağaçlar.
- [UC Berkeley EECS-2025-224](https://www2.eecs.berkeley.edu/Pubs/TechRpts/2025/EECS-2025-224.html) Spekülatör çözme ile verimli LLM sistemi.
- [BentoML — Speculative Decoding](https://bentoml.com/llm/inference-optimization/speculative-decoding) Üretim başlatma kontrol listesi.
