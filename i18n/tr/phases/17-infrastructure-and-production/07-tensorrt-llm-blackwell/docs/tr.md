# Blackwell'de TensorRT-LLM FP8 ve NVFP4 ile Blackwell TensorRT LLM
# Hardware-Specialized Inference Compilation  FP8 ve NVFP4 Blackwell'de

> Hardware uzmanlaştırılmış sonuçlama komisyonu, akışın taşınabilirliği için ticaret yapar ve Blackwell için ayarlanmış olan TensorRT-LLM  NVIDIA-sadece, ticaretin sonuç vermesinin en net örneğidir.$0.012 per million tokens on a 120B model in Q1-Q2 2026, against $H100 + vLLM  7 kat ekonomik fark. Bu yığın üç yüzer nokta rejimi ile birleşmiştir: FP8 KV önbelleği ve dikkat çekirdekleri için kritik kalır çünkü ihtiyaç duydukları dinamik aralığı vardır; NVFP4 (4 bit mikro ölçekleme) ağırlıkları ve etkinleştirmeleri ele alır; çoklu jeton öngörü (MTP) ve parçalanmış prefill / decode yukarıda bir daha 2-3x ekler. Day-0 model destek yükleri FP4 ağırlıkları doğrudan eğitim sonrası dönüşüm olmadan. 2026 mühendislik takımları için yakalama: TRT-LLM açık kaynaklı ancak NVIDIA-spesifik  CUDA- ve Blackwell-specialized  bu yüzden onu benimsemek geçiş için taşınabilirliği ticaret. Yapmadan önce model ve donanım karışımını matematikle çalıştır.

> **【中文解读】**Bu bölümde TensorRT-LLM ve Blackwell'in NVIDIA'nın LLM  optimizasyon çerçevesini ve en son GPU  yapılarını ele aldı.
**Type:** Learn
**Languages:** Python (stdlib, toy FP8/NVFP4 memory and cost calculator)
**Prerequisites:** Phase 17 · 04 (Serving Engine Internals), Phase 10 · 13 (Quantization)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy FP8/NVFP4 memory and cost calculator) | **语言:** Python（标准库，FP8/NVFP4 内存和成本计算器）
**Prerequisites:** Phase 17 · 04 (vLLM Serving Internals), Phase 10 · 13 (Quantization) | **前置知识:** Phase 17 · 04（vLLM 服务内部）, Phase 10 · 13（量化）

>  **【前置】**Önemli olan, Blackwell GPU'da en güçlü performanslı olan.
>  **【类比】**TensorRT-LLM = "NVIDIA 专属跑车"──GB200 NVL72 上 SemiAnalysis 测:120B 模型 $0.012/百万 token（H100+vLLM $0.09)  7 倍 经济性差距──三套浮点叠加:FP8(KV cache+attention 动态范围) + NVFP4(4-bit 权重激活) + MTP/解 prefill-decode 再加 2-3 倍──代价:闭源 NVIDIA ,可移植性换吞吐──选型前必须按你的模型/硬件组合算账──
**Time:** ~75 minutes | **时间:** ~75 分钟

## Öğrenme hedefleri

- FP8'nin neden NVFP4'te ağırlıklar olduğu halde KV kaydı ve dikkat için kritik olduğunu açıklayın.
  Çinçe Çevirimiçi: Neden, NVFP4'te, FP8'de KV'ye 缓存和注意力 neden hâlâ önemli olduğu açıklandı.
- BF16, FP8 ve NVFP4 çerçevesinde bir sınır modelinin HBM ayak izi hesaplayın ve tasarrufların nereden geldiğini açıklayın.
  Çin dilinde:计算前沿模型在 BF16、FP8 和 NVFP4 下的HBM 占用,分析节省来自哪里──
- Blackwell'e özgü özelliklerin adı TRT-LLM (day-0 FP4, MTP, ayrıştırılmış servis, tümüne ilk gelenler) kullanılar.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Ç Ç Ç Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
- TRT-LLM'in NVIDIA kilitinin Hopper'daki 7 katlık maliyet farkına ne zaman değeceğini belirleyin.
  Çinçe Çevirimiçi: Decision TRT-LLM'nin NVIDIA 锁定何时值相比Hopper 上 vLLM'in 7x 成本差──

## Sorunlar. Sorunlar.

> **【中文解读】**2026 yılının öne çıkan ekonomik soruları ise "Her dolar ne kadar token"dır. Cevap dört katlı bir süsleme seçeneğine bağlıdır:硬件代际(Hopper H100/H200 vs Blackwell B200/GB200) 精度(BF16 → FP8 → NVFP4) 推理引擎(vLLM vs SGLang vs TRT-LLM)$0.09/M tokens；在 Blackwell + TRT-LLM + Dynamo 上仅 $0.012/M7x 差. Bu farkın fiyatı NVIDIA'nın diğer üreticilerin donanımında tekrarlanamayacağını belirledi.

> **【拓展：NVIDIA Blackwell 架构】**Blackwell(B200/GB200) NVIDIA 2024-2025 yıllarında tanıtılan Hopper (H100) ile karşılaştırıldığında LLM ı tahmininde 11-15x'in her GPU 吞吐提升ı vardır.

2026'da sonuç ekonomisinin sınırı "dolar başına kaç token" olacaktır. Cevap dört yığınlı seçeneğe bağlıdır: donanım üretimi (Hopper H100/H200 vs. Blackwell B200/GB200), hassaslık (BF16 → FP8 → NVFP4), servis motor (vLLM vs. SGLang vs. TRT-LLM), ve orkestrasyon (sırf vs. ayrıştırılmış vs. Dynamo).

> 2026 yılının öne geçmesi için yapılan ekonomik tahminler, "her dolarda ne kadar token" olarak belirlenmiştir.

Hopper'da 120B MoE'nin hızı ~$0.09 per million tokens. On Blackwell with TRT-LLM + Dynamo, the same model runs at ~$0.012  7x daha ucuz. Bu boşluktan bazıları donanımdır (Blackwell'in GPU LLM çıkışı karşı karşısına 11-15x). Bazıları yığın: FP4 ağırlıkları, MTP taslak, parçalanmış prefill / decode ve MoE uzman iletişim için NVLink 5 her şeye.

> Hopper + vLLM 上,120B MoE 运行约 $0.09/M tokens。在 Blackwell + TRT-LLM + Dynamo 上，同一模型运行约 $0.012便宜 7 倍──部分差来自硬件(Blackwell vs Hopper Her GPU LLM 吞吐 11-15 倍)──部分来自:FP4 权重、MTP draı、分离式预填/解码和 NVLink 5 all-to-all 用于MoE 专家通信──

Bu, NVIDIA'nın yığınının dışında tekrarlanamaz. Bu ekonomik için ödeme  taşınabilirlik. Hangi yığın seçimlerinin hangi boşluğu paylaştırdığını anlamak bu dersin amacıdır.

> Bu, NVIDIA'nın dışında bir şekilde yeniden üretilebilme gücünü ölçmek için kullanılabilir.

## Konsepten bir şey.

### Neden FP8 hala KV cache için zemin

> **【中文解读】**FP8 KV Cache'nin en düşük hassaslık gereksinimidir. KV Cache'nin dikkat anahtarı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı ısı

2026'da yaygın bir hata: NVFP4'in her yerde geçerli olduğunu varsaymak. Bu geçerli değildir. KV kasesi FP8'ye (8 bit yüzen nokta) ihtiyaç duyar. Çünkü geniş bir dinamik aralığı kapsadığı dikkat anahtarlarını ve değerleri depolar. KV'yi FP4'e kvantize etmek felaketli doğruluk kaybına neden olur.

> 2026 yılında bir yaygın hata: NVFP4'in tüm yerlere uygulanacağını varsaymak.

NVFP4 (2025-2026) ağırlıklara ve etkinleştirmeler için geçerlidir. Mikroskalalama: ağırlıkların her bloku kendi ölçek faktörüne sahiptir, bu nedenle küçük bloklar, per-tensor ölçek kaybı olmadan farklı dinamik aralıkları kaplayabilir.

> NVFP4 ((2025-2026) ağırlık ve aktivasyon için uygundur.

Tipik Blackwell'in yapılandırması:

- Ağırlıklar: NVFP4 (4 bit mikro ölçekleme).
  Çeviri: NVFP4
- Aktivasyon: NVFP4.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- KV önbelleği: FP8.
  Çeviri:KV 缓存:FP8。
- Dikkat akkumülatörü: FP32 (mükemmel maksimum istikrar).
  Çeviri: dikkat力累加器:FP32

### Blackwell'e özgü ilkeler TRT-LLM kullanır

- **Day-0 FP4 weights**Modelleme sahipler FP4 ağırlıklarını doğrudan gönderir; TRT-LLM yükleri eğitim sonrası dönüşüm olmadan.
  Çeviri:**Day-0 FP4 权重**Model Provider Directly Release FP4 权重;TRT-LLM 无需训练后转换即可载──FP4 不需要 AWQ/GPTQ 步骤──
- **Multi-token prediction (MTP)**: EAGLE'nin (Fase 17 · 05) aynı fikri ancak TRT-LLM yapısına entegre edildi.
  Çeviri:**多 token 预测 (MTP)**Bu nedenle, bu süreçte, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir sürececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececece
- **Disaggregated serving**Bu nedenle, bu işlemler, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir süre sonra, bir sürece, bir sürece, bir sürececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececececece
  Çeviri:**分离式服务**: Prefill and code on an independent GPU 池,KV 缓存 via NVLink or InfiniBand 传输──
- **All-to-all communication primitives**NVLink 5 MoE uzman iletişim gecikmesini 3x vs Hopper'a düşürüyor. TRT-LLM'in MoE çekirdekleri bunun için ayarlanmıştır.
  Çeviri:**All-to-all 通信原语**NVLink 5'in MoE 专家通信延迟降低 3倍――
- **NVFP4 + MXFP8 microscaling**Blackwell Tensor Cores'te donanımlı hızlandırılmış ölçek faktörleri ile işlenme.
  Çeviri:**NVFP4 + MXFP8 微缩放**Blackwell Tensor Core'ın üstündeki hardware hızlandırılması ve işlemini hızlandırmak için bir araçtır.

### Hatırlaman gereken rakamlar

- HGX B200, GPT-OSS-120B üzerinden TRT-LLM üzerinden 0.02 / M dolarlık tokenler.
  Çeviri:HGX B200 GPT-OSS-120B 上通过 TRT-LLM 为 $0.02/M tokens
- GB200 NVL72 $0.012/M tokenleri Dynamo (orkestreci TRT-LLM) üzerinden.
  Çeviri:GB200 NVL72 通过 Dynamo (TRT-LLM) = $0.012/M tokens
- H100 + vLLM ≈ $0.09 / M simgeler karşılaştırılabilir iş yükü.
  H100 + vLLM 在可比工作负载上 yaklaşık $0.09 / M jetonları。
- TRT-LLM güncellemelerinin üç ayında 2.8 katlık bir üretim artışı (2026).
  Çinçe Çevirimi:TRT-LLM 2026 yıl üç ay更新的 2.8 倍吞吐量提升──
- GPU LLM'de 11-15 katlık çıkış, Blackwell vs Hopper.
  Çeviri: Blackwell vs Hopper Her GPU LLM 吞吐量 11-15 倍。
- MLPerf Inference v6.0 (Epril 2026): Blackwell gönderilen her görevi egemenliği.
  Çeviri:MLPerf Inference v6.0(2026 yıl 4 月):Blackwell 在所有提交任务中领先──

### FP4'in kalitesiyle ilgili gerçekte ne kadar maliyetleri var

> **【中文解读】**NVFP4'de düşünce yoğunlu çalışma yükü (思维链、数学、长上下文代码生成) üzerinde görülür bir kalite bozgununa neden olur. Her bir kurulumun hafifletilebilir ama ortadan kaldırılamaz.2026 yılının pratik yöntemi: düşünce modeli FP8 权重 + FP4 激活作为折中,或继续使用H200 全 FP8── kural: NVFP4 权重提交之前, kendi değerlendirmesi kitinde görevlerin kalitesini doğrultmak gerekir.

> **【拓展：量化精度 vs 推理成本权衡】**量化精度的选择是质量和成本的权衡:(1) BF16质量损失,内存需求大,但内存需求大(70B 模型需要140GB);(2) FP8近乎无损,Hopper/Blackwell 硬件加速, yoğun tip görevleri tahmin etmek için önerilen;(3) INT4(AWQ/GPTQ) 4-bit 权重,MATH 分数下降 3-5 点,适合通用聊天;(4) NVFP4最激进,Blackwell 专用,必须在目标评估上精准.

NVFP4 agresifdir. Düşünce ağır iş yüklerinde (hüküm zinciri, matematik, uzun bağlamlı kod-gen), FP4 ağırlıkları görünür olarak düşer. Blok başına kalibrasyon hafifler ancak ortadan kaldırmaz. Takımlar nedencilik modellerini göndermek genellikle FP8 ağırlıklarını + FP4 etkinleştirmelerini bir uzlaşma olarak kullanır veya H200'e bağlıdır.

> NVFP4 激进的──在推理密集型工作负载 (思维链、数学、长上下文代码生成) 上,FP4 权重明显退化──每块校准缓解但不能消除──推理模型的团队通常使用FP8 权重 + FP4 激活作为折中,或在H200 上坚持全FP8──

Kural: NVFP4 ağırlıklarına katılmadan önce değerlendirme ayarınızda görev kalitesini her zaman doğrulayın.

> 規則: NVFP4 权重 before submitting,始终在您的评估集上验证任务质量──

### Neden bu bir NVIDIA kilitleme kararı

> **【中文解读】**TRT-LLM, C++ + CUDA + 闭源内核的组合──模型需要特定 GPU SKU 编译──不支持 AMD、Intel 或 ARM── Eğer altyapı stratejiniz çok sayıda tedarikçi ise, TRT-LLM 对于这个层是不可选项您仍然可以在混合硬件上使用vLLM──但是如果你只为NVIDIA,7x的经济差距值得此锁定──

> **【拓展：NVIDIA vs AMD 推理生态】**2026 yılında AI  Tahmin Çip Piyasasındaki Şekil:NVIDIA  CUDA  生态 ve TRT-LLM ile %80'lik veri merkezi tahmin payını oluşturuyor. AMD MI300X orijinal hesaplama gücünde rekabetçi, ancak yazılım (ROCm + vLLM) hala peşinden gidiyor. Intel Gaudi 3 başka bir seçenek ama benimsemiş oranı düşük.

TRT-LLM, C++ + CUDA + kapalı kaynak çekirdekleridir. Modeller belirli bir GPU SKU için oluşturulmalıdır. AMD, Intel veya ARM yoktur. İnfra stratejiniz çok satıcı ise, TRT-LLM hizmet verilen katman için başlangıçsızdır.

> TRT-LLM C++ + CUDA + 闭源内核的组合──模型需要特定 GPU SKU 编译──不支持 AMD、Intel 或 ARM── Eğer altyapı stratejiniz çok sayıda tedarikçi ise, TRT-LLM gitmemektedir

### 2026 pratik tarif

Hopper + vLLM'de çalışan yıllık bir 100 milyon dolarlık sonuç faturası için masada 7-10 kat daha fazla kalır. Maliyet baskın iş yüklerini Blackwell + TRT-LLM + Dynamo'ya aktarın. Modeldeki tekrarlama hızı için H100 + vLLM'de deney seviyesini koruyun. Her NVFP4 dönüştürülen modelde üretimden önce kaliteyi doğrulayın.

> $100M+ yıllık tahmin harcamaları için Hopper + vLLM'de çalışmak, 7-10 kat daha fazla tasarruf alanı bırakmak anlamına gelir. $100M+ vLLM'de çalışmanın aşamasını sürdürmek için çalışma kapasitesini sürdürmek için, %10'luk tasarruf alanı bırakmak anlamına gelir.

### Bölümleme bonusu

TRT-LLM'nin ayrıştırılmış servisi (ayrı önceden doldurma ve çözme havuzları) 17 · 20 aşamada derinliklere kaplıdır. Blackwell'de, katılımcılar: FP4 ağırlıkları × MTP hızlandırması × ayrıştırılmış yerleştirme × önbelleğe dikkat çeken yönlendirmeyi varsayır. 7x numarası bu tam yığını varsayır.

> TRT-LLM'nin ayrıntılı hizmetleri (( bağımsız önceden doldurulmuş ve anlaşma) 17 · 20 aşamasında derinlemesine tartışılmıştır.

## Çerçeveyi kullanın.

> **【拓展：Blackwell 迁移决策】**Hopper 迁移到Blackwell + TRT-LLM 决策框架:(1) Yıllık düşünce harcamaları 5 milyon dolardan fazla mı? is→ 迁移 değerlendirilmesi;(2) NVIDIA 锁定?否→ vLLM + Hopper kullanmaya devam etmek;(3) 工作负载是否包含 MoE 模型? is→Blackwell'in NVLink 5 all-to-all 额外 3x 加速;(4) 推理密集型任务占比是否超过30%? is→ 验证 NVFP4 质量──迁移 ROI genellikle 6-12 个月内回本──
```figure
pipeline-parallel
```

## Kullan

`code/main.py`HBM ayak izi, dekodlama geçişini (hüzdede bağlanmış rejim) ve üç yığın üzerinde bir model için $/M-tokenleri hesaplar: H100 + BF16 + vLLM, H100 + FP8 + vLLM, B200 + NVFP4/FP8 + TRT-LLM. Her değişikliğin katkıda bulunduğu karma etki ve boşluk payını görmek için çalıştırın.

> `code/main.py`計算模型在三上 HBM 占用、解码吞吐量(内存受限) ve $/M-tokens:H100 + BF16 + vLLM、H100 + FP8 + vLLM、B200 + NVFP4/FP8 + TRT-LLM──运行

## İndirin . Ürünler .

Bu ders bize çok yararlı .`outputs/skill-trtllm-blackwell-advisor.md`. İş yükü, model boyutu ve yıllık token hacmi göz önüne alındığında, Blackwell + TRT-LLM yığınının NVIDIA-kalka değer olup olmadığını belirler.

> 本课产 出 `outputs/skill-trtllm-blackwell-advisor.md`                                                                                                                                                                                                                                                                                                                                          

## Egzersizler.

1. Çık .`code/main.py`%30 aktif parametreleri olan 120B MoE'de, H100 BF16, H100 FP8 ve B200 NVFP4/FP8'de hafıza bant genişliği sınırlı dekod geçişini hesaplayın.
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`◊ % 30  aktif parametrinin 120B MoE üzerinde, H100 BF16、H100 FP8 ve B200 NVFP4/FP8 内存带宽限解码吞吐量── en büyük sıçrama nereden geliyor?
2. Bir müşteri H100 + vLLM için yılda 2 milyon dolar harcıyor. 7 kat ekonomik boşluğu göz önüne alarak 12 ay içinde TRT-LLM'ye göçü için amortize etmek için satın almaları gereken Blackwell GPU sayısı nedir?
   Çin dilinde: Client in H100 + vLLM 上每年花费2M $. 给定 7x 经济差距, they need to buy how much Blackwell GPU 才能在 12 个月内摊销迁移到TRT-LLM 的成本?
3. NVFP4 ağırlık dönüşümünden sonra MATH'de doğruluk 3 puan düşüşünü görürsünüz. İki kurtarma yolunun adını verin: bir kalite önce (FP8 ağırlıklarını koruyun), bir maliyet önce (domain verileri ile kalibre edin).
   Çin dilinde tercüme:NVFP4 权重转换后 MATH 精度下降 3 点──说出两条恢复路径:一条质量优先(保持 FP8 权重),一条成本优先(用领域内数据校准)
4. MLPerf v6.0 sonuçlarını okuyun. Hangi görevde Blackwell-over-Hopper farkı en az ve neden?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri: Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Çeviri Ç Çeviri Ç Ç Ç Ç Çeviri Çeviri Ç Çeviri Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Çeviri Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç Ç
5. 405B modeli için gereken HBM'yi NVFP4 ağırlıklarında + FP8 KV önbelleği 128k bağlamda hesaplayın.
   Çinçe Çevirimi:计算 405B 模型在 NVFP4 权重 + FP8 KV 缓存 + 128k 上下文下 HBM 需求──¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿

## Anahtar Şartlar .

| Term / 术语 | What people say / 通俗说法 | What it actually means / 实际含义 |
|------|----------------|------------------------|
| FP8 | "eight-bit float" / "8-bit 浮点" | 8-bit floating point; used for KV cache and attention due to dynamic range / 8-bit 浮点；因动态范围用于 KV 缓存和注意力 |
| NVFP4 | "four-bit micro" / "4-bit 微缩放" | NVIDIA's 4-bit microscaling FP format; weights and activations on Blackwell / NVIDIA 4-bit 微缩放浮点格式；Blackwell 上的权重和激活 |
| MXFP8 | "MX eight" / "MX 8-bit" | Microscaling FP8 variant; hardware-accelerated on Blackwell Tensor Cores / 微缩放 FP8 变体；Blackwell Tensor Core 硬件加速 |
| Day-0 FP4 | "ship FP4 weights" / "直接发布 FP4 权重" | Model providers release weights already in FP4; no post-train conversion step / 模型提供商直接发布 FP4 权重；无训练后转换步骤 |
| MTP | "multi-token prediction" / "多 token 预测" | TRT-LLM's integrated speculative-decoding draft (Phase 17 · 05) / TRT-LLM 集成的推测解码 draft |
| Disaggregated serving | "split prefill/decode" / "分离预填充/解码" | Prefill and decode on separate GPU pools; KV transferred over NVLink/IB / 独立 GPU 池的预填充和解码 |
| All-to-all | "MoE expert comm" / "MoE 专家通信" | Communication pattern routing tokens to expert GPUs; NVLink 5 cuts 3x / 将 token 路由到专家 GPU 的通信模式 |
| InferenceX | "SemiAnalysis inference bench" / "推理基准" | The 2026 industry-accepted cost-per-token benchmark / 2026 年行业接受的每 token 成本基准 |

## Daha fazla okumak

- [NVIDIA — Blackwell Ultra MLPerf Inference v6.0](https://developer.nvidia.com/blog/nvidia-blackwell-ultra-sets-new-inference-records-in-mlperf-debut/) Nisan 2026 MLPerf sonuçları.
- [NVIDIA — MoE Inference on Blackwell](https://developer.nvidia.com/blog/delivering-massive-performance-leaps-for-mixture-of-experts-inference-on-nvidia-blackwell/) NVLink 5 tüm ve MoE çekirdekleri.
- [TensorRT-LLM Overview](https://nvidia.github.io/TensorRT-LLM/overview.html) Resmi motor belgesi.
- [NVIDIA — Introducing Dynamo](https://developer.nvidia.com/blog/introducing-nvidia-dynamo-a-low-latency-distributed-inference-framework-for-scaling-reasoning-ai-models/) TRT-LLM'den yukarıdaki parçalanmış orkestrasyon.
- [MLPerf Inference](https://mlcommons.org/benchmarks/inference-datacenter/) Blackwell sayıları yayınlayan referans değerleri kümesi.
