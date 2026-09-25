# Üretim Kvantı  AWQ, GPTQ, GGUF K-kvantları, FP8, MXFP4/NVFP4 量化 生产

> Kvantisalizasyon biçimi evrensel bir seçim değildir  donanım, hizmet motor ve iş yükü fonksiyonu. GGUF Q4_K_M veya Q5_K_M, llama.cpp ve Ollama üzerinden teslim edilen CPU ve kenarına sahiptir. GPTQ aynı tabanda çoklu LORA'ya ihtiyaç duyduğunda vLLM'de kazanır. Marlin-AWQ çekirdekleri ile AWQ, en iyi Pass@1 ile 7B sınıfı modelinde, 2026'da veri merkezi üretimi için varsayılan  INT4'de ~741 tok/s'i sağlar. FP8 Hopper, Ada ve Blackwell'de orta yerde kalır  neredeyse kayıpsız ve yaygın olarak desteklenir. NVFP4 ve MXFP4 (Blackwell mikroskalingi) agresif ve blok başına onaylama gerektirir. İki tuzak ısırma ekibi: Kalibrasyon verileri dağıtım alanına eşleşmelidir ve KV önbelleği ağırlık kvantizasyonundan ayrıdır  AWQ dersi "Modem şimdi 4 GB'dır" üretim seri boyutlarında 10-30 GB KV önbelleğini unutur.

> **【中文解读】**Bu bölüm, üretim çevre ölçümselliği bölümünün INT8/INT4/FP8  ölçümsellik teknolojisinin tahmin maliyetlerini azaltma içindeki uygulanmasını anlattı.
**Type:** Learn
**Languages:** Python (stdlib, toy memory and throughput comparison across formats)
**Prerequisites:** Phase 10 · 13 (Quantization foundations), Phase 17 · 04 (Serving Engine Internals)
**Time:** ~75 minutes


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, toy memory and throughput comparison across formats) | **语言:** Python
**Prerequisites:** Phase 10 · 13 (Quantization foundations), Phase 17 · 04 (vLLM Serving Internals) | **前置知识:** Phase 10 · 13 (Quantization foundations), Phase 17 · 04 (vLLM Serving Internals)

>  **【前置】**Öğrenci bölümünün ilk aşamasında:Dava 10·13(kısımlılık temel) Dava 17·04(vLLM) Kısımlılık biçimi Kardınç+Motor+Sadağ yükleme seçeneği 
>  **【类比】**量化格式 = "sıcaklama 行李"。GGUF Q4_K_M = 适合火车/edge(CPU 友好);GPTQ = vLLM 多 LoRA 场景;AWQ + Marlin 内核 = 数据中心默认(7B 模型 741 tok/s,INT4 最佳);FP8 = Hopper/Ada/Blackwell 中选择(近乎无损);NVFP4/MXFP4 = 激进,需块逐验证。
> ️ **【易错点】**两个陷:(1) 校准数据集必须匹配部署领域(医疗模型用通用文本校准会失真);(2) " Benim modeli sadece 4GB " KV cache unuttu ((生产批 下 10-30GB) ⋅
**Time:** ~75 minutes | **时间:** ~75 minutes

## Öğrenme hedefleri

- 2026'da altı üretim kuantitasyon biçimi ve tatlı noktalarını isimlendirin.
  Çinçe Çevirimi: ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ ︎ 
- Verilen donanım (CPU vs GPU, Hopper vs Blackwell), motor (vLLM, TRT-LLM, llama.cpp) ve iş yükünü seçin (rutinal sohbet, mantık, multi-LoRA).
  Çin dilinde:{\displaystyle \mathbb {\displaystyle \mathbb {\mathbb {\mathbb {\mathbb} }
- Kaydedilen ağırlık belleğini hesaplayın ve seçilen biçim için KV önbelleği dokunulmamış olarak bırakın.
  Çinçe çevirisi:计算选定格式节省的权重内存和未触及的 KV 缓存──
- Domen trafiğinde kuantistik modelleri düşüren kalibrasyon veri kümesi tuzağını isimlendirin.
  Çinçe Çevirisi: Say out led to quantization model in the field flow on degeneration

## Sorunlar. Sorunlar.

> **【中文解读】**量化減少内存和HBM 带宽消耗 正是解码最需要的阶段──FP16'ın 70B modeli ağırlığı 140GB,INT4 量化后仅35GB,一张H100 上运行可用(80GB HBM) ⋅ ancak 量化 ücretsiz değildir 激进量化量化降低质量 (özellikle yoğunlu görevleri düşünün), farklı biçimlerde farklı motorlar, farklı donanım destekleri farklı kesimlerde bulunmaktadır.

> **【拓展：量化技术演进】**量化技術 üç nesilden geçti: 1) 均量化(INT8/INT4)  简单但精度损失大; 2) 感知量化(AWQ/GPTQ)  保护重权重,INT4 下质量接近BF16; 3) 浮点量化(FP8/NVFP4) 硬件加速,动态范围更好──2024-2026 yılları 量化 araştırmasının temel başarısı "mikroskalaş"  微缩)  权分块 has independent shrinking factor, in 4-bit 下仍然保持良好──ARK Invest 估计化 估计化 贡献推 cost decrease 约30%──

Kvantizasyon, hafıza ve HBM bant genişliğini azaltır, bu da tam olarak dekodlamanın ihtiyacı olan şeydir. FP16 70B modeli 140 GB ağırlıklıdır. Kvantize ağırlıkları INT4 (AWQ veya GPTQ) olarak ölçün ve model 35 GB  bir H100'e KV kaş için yerleştirilir.

> 量化减少内存和HBM 带宽消耗,正是解码阶段最需要的──FP16'ın 70B modeli ağırlığı 140GB'yi oluşturuyor──后型 model sadece 35GB'ye kadar INT4(AWQ veya GPTQ'ye kadar ağırlıklı hale gelecektir.

Ancak kuantizasyon ücretsizdir. Agresif kuantizasyon kaliteyi, özellikle akıl yürütme ağır görevlerde bozar. Farklı biçimler farklı motorlarla çalışır. Farklı donanımlar farklı hassasiyetleri yerli olarak destekler. 2026 biçimi hayvanat bahçesi gerçek ve başkalarının seçimini kopyalayamazsınız.

> Ancak, ölçüm ücretsizdir. Yüksek ölçüm, kaliteyi azaltır. Özellikle yoğun bir görev düşüncesi.

## Konsepten bir şey.

### Altı format

| Format | Bits | Sweet spot | Engines |
|--------|------|-----------|---------|
| GGUF Q4_K_M / Q5_K_M | 4-5 | CPU, edge, laptops | llama.cpp, Ollama |
| GPTQ | 4-8 | Multi-LoRA on vLLM | vLLM, TGI |
| AWQ | 4 | Datacenter GPU production | vLLM (Marlin-AWQ), TGI |
| FP8 | 8 | Hopper/Ada/Blackwell datacenter | vLLM, TRT-LLM, SGLang |
| MXFP4 | 4 | Blackwell multi-user | TRT-LLM |
| NVFP4 | 4 | Blackwell multi-user | TRT-LLM |

### GGUF  CPU/geze varsayılan

> **【拓展：GGUF 在边缘推理中的地位】**GGUF, CPU/边缘 düşüncelerinde en büyük konumdaki llama.cpp 和 Ollama'nın öntanımlı biçimidir. Q4_K_M 和 Q5_K_M, 4-5 bitte öntanımlı üretim yapmaktadır. Aşağıda BF16'ın kalitesine yaklaşmaktadır.

GGUF, kendi başına bir kuantitasyon şeması değil, bir dosya biçimidir. K-quant varianlarını (Q2_K, Q3_K_M, Q4_K_M, Q5_K_M, Q6_K, Q8_0) bir konteynere birleştirir. Q4_K_M ve Q5_K_M, üretim öntanımlılarıdır.

> GGUF, kendiliğinden bir dosya biçimidir, ölçümsel bir çözüm değildir. K-quant 变体打包在一个容器中──Q4_K_M 和 Q5_K_M, BF16 质量─CPU veya kenar hizmetinin en iyi seçeneği, çünkü llama.cpp şu anda en hızlı CPU 推理引擎──

VLLM'de geçiş cezası: ~93 tok/s 7B  format GPU çekirdekleri için optimize edilmemiştir. Ulaştırma hedefi CPU/gez olduğunda GGUF kullanın.

> VLLM'de toplama kaybı:7B  Model yaklaşık 93 tok/s Bu biçim GPU'ya yönelik değildir 内核优化。 sadece konuşlandırma amacı CPU/边缘时使用GGUF,否则不使用。

### GPTQ  vLLM'de çoklu LORA

GPTQ, kalibrasyon geçişine sahip bir eğitim sonrası kuantitasyon algoritmasıdır. Marlin çekirdekleri GPU'da (2.6x hızlandırma vs. Marlin olmayan GPTQ) hızlı hale getirir. ~712 tok/s 7B'de.

> GPTQ, bir eğitim sonrası ölçüm algoritmasıdır.

GPTQ-Int4 vLLM'de LoRA adaptörlerini destekler. Eğer bir temel model ve 10-50 ince ayarlanmış variantları (her biri bir LoRA olarak) sunuyorsanız, GPTQ yolunuzdur. NVFP4 henüz 2026'ın başından itibaren LoRA'yı desteklemiyor.

> Özel avantaj:GPTQ-Int4 vLLM içinde LoRA'yı destekler 适配器── eğer serviste bir temel modelde 10-50 个微调变体加 (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (karşılaştırma)  (tarımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımımım

### AWQ  veri merkezi GPU'sı varsayılan

> **【中文解读】**AWQ(Aktifleştirme Bilinci Ağırlık Kvantisiasyonu) 2026 yılın veri merkezi GPU 推理的默认选择──它保护量化过程中约1% 最显著的权重,配合Marlin-AWQ 内核实现 10.9x 加速── 7B 模型上达到 ~741 tok/s,是INT4 格式中 Pass@1最高的──除非需要多 LoRA(选择GPTQ) 或Blackwell FP4(选择 NVFP4),否应新 GPU 推理项目默认使用 AWQ──

Aktifleştirme-Aydın Ağırlık Kvantisalatı. Kvantisalat sırasında% 1 en iyi ağırlıkları korur. Marlin-AWQ çekirdekleri: 10.9x hızlandırma vs. naif. ~ 7B'de 741 tok/s, INT4 formatları arasında en iyi Pass@1.

> 激活感知权重量化──保护量化 sürecinde en önemli ağırlığın %1'i.

Yeni GPU servisini seçmek için AWQ seçin, ancak çoklu LoRA (GPTQ) veya agresif Blackwell FP4 (NVFP4) ihtiyacınız yoksa.

> Yeni GPU 推理项目选择 AWQ,除非需要多 LoRA(选 GPTQ) 或激进的Blackwell FP4(选 NVFP4)。

### FP8  güvenilir orta

> **【拓展：FP8 量化的生产应用】**FP8(8-bit 浮点) 2026 yılının kalitesi anlaşılmaz bir sahneye ait olduğu belirlenmiş bir doğrudur. Hopper Tensor Cores orijinal yaşamı hızlandırıcı FP8, Blackwell  mirasçı desteği. FP8 内存储省はINT4'in yarısıdır, ancak kalitesi riskleri çok düşüktür.

8 bit yüzen nokta. Neredeyse kayıpsız. Geniş desteklenir. Hopper Tensor Cores FP8'yi doğuştan hızlandırır. Blackwell miras alır. FP8 kalitesi pazarlanamayacak (düşünme, tıbbi, kod-gen) olduğunda güvenli 2026 varsayılan noktasıdır. Hatıra tasarrufu INT4'in yarısıdır ancak kalite riski çok daha düşüktür.

> 8-bit 浮点──近乎无损──广泛支持──Hopper Tensor Cores 原生加速 FP8──Blackwell 继承──当质量不可妥协时(推理、医疗、代码生成),FP8 2026 yılının güvenli kabul edilmiş seçimi──内存节省 INT4'in yarısı, ancak质量风险 çok düşük──

### MXFP4 / NVFP4  Blackwell saldırgan

Mikroskala FP4. Ağırlıkların her bloku kendi ölçek faktörüne sahiptir. Blackwell Tensor Cores'te agresif ancak donanımsal hızlandırılmış. FP8 karşısında bir token için baytları yarıya düşürün  17 · 07 aşamasında ekonomik kazanç.

> 微缩放 FP4──每个权重块都有自己的缩放因子──激进但黑威尔 Tensor Cores 硬件加速──相比FP8 每字节减半Phase 17 · 07 中的经济优势──

Kafesler:
- LoRA desteği henüz yok (2026 başlarında).
  Çinçe Çevirimi:截至 2026年初尚不支持 LoRA。
- Kalit düşüşü, akıl yürütme ağır iş yüklerinde görülebilir.
  Çinçe Çevirisi: 推理密集型工作负载上可见质量下降──
- Model başına değerlendirme ayarını doğrulayın.
  Çinçe Çevirimiçi: her model değerlendirme koleksiyonunda test edilir.

### Kalibrasyon tuzakı

> **【中文解读】**校准数据集陷:AWQ 和 GPTQ 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据集 校准数据 校准数据集 校准数据 校准 校准数据 校准数据集 校准 校准数据 校准 校准 校准数据 校准数据 校准数据 校准 校准 校准 校准 校准数据 校准 校准 校准 校 校 校 校 校 校 校 校 校 校 校 校 校 校 校

> **【拓展：量化对 LLM 能力的影响】**量化对不同能力的影响程度不同:(1) 简单聊天/摘要INT4 几乎无影响;(2) 翻译/写作INT4 轻微退化;(3) 数学/推理INT4 损失 3-5 分(MATH referansı);(4) 长上下文理解INT4 在 128K+ bağlamında 上质量显著下降;(5) 代码生成INT4 在 HumanEval 上下降 2-3 分──核心原则:推理密集型任务应使用FP8 或 BF16,通用聊天可使用INT4──

AWQ ve GPTQ, tipik olarak C4 veya WikiText olarak bir kalibrasyon veri kümesi gerektirir. Domen modelleri (kod, tıbbi, yasal), genel web metnini kalibrlemek algoritmanın hangi ağırlıkları koruyacağı konusunda yanlış kararlar vermesine izin verir. HumanEval'de Pass@1 birkaç puan düşebilir.

> AWQ ve GPTQ 校准数据集 genellikle C4 veya WikiText── için alan modelleri(代码、医疗、法律), genel ağ metinlerinde 校准会让算法误决策保护哪些权重──HumanEval Pass@1可能下降几百分点──

Düzeltme: alan içindeki verileri kalibre edin. Yüzlerce alan örneği genellikle yeterli olur.

> 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修复方法: 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修 修    修 修    修 修 修   修       修      修                                                                                                                                                                    

### KV'nin önbellek tuzağı

> **【中文解读】**KV Cache 陷:AWQ, 4 bit'e kadar ağırlık sıkıştırmayı planlıyor, ancak KV Cache bağımsızdır, FP16/FP8。70B AWQ  modelinin tam内存 bütçesi şudur: 35GB + KV Cache(128 并发 × 2K bağlam) 20GB + 激活 5GB = 总计 60GB。

AWQ ağırlıkları 4 bit'e düşürür. KV önbelleği ayrıdır ve FP16/FP8'de kalır. AWQ ile 70B modeli için:

- Ağırlık: ~ 35 GB (INT4 140 GB'dan).
  Çeviri: Hakk: yaklaşık 35GB (Yeni Ülke: 140GB)
- KV önbelleği 128 eşzamanlı × 2k bağlamda: ~ 20 GB.
  Çinçe Çevirim: 128 并发 × 2K 上下文的 KV 缓存: yaklaşık 20GB──
- Aktifleştirmeler: ~ 5 GB.
  Çeviri: 5GB
- Toplam: ~ 60 GB  H100 80 GB'a uykuluyor.
  Çinçe Çevirim: toplam: yaklaşık 60GB  H100 80GB 

"Modemi 4 GB'ye kadar kvantize ettim" gibi safca, diğer 30-50 GB'ları unuttu.

> "Modem 4GB'ye kadar" dendiğinde, 30-50GB'yi unutmuştum.

Ayrıcası, KV cache kuantizasyonu (FP8 KV veya INT8 KV) kendi özelliği ile farklı bir seçimdir  dikkat doğruluğunu doğrudan etkiler ve ücretsiz bir kazanç değildir.

> Ayrıca, KV 缓存量化 (FP8 KV veya INT8 KV) farklı ağırlıklı bağımsız bir seçimdir.

### AWQ INT4 akıl yürütmek için tehlikelidir.

Düşünce zinciri, matematik, uzun bağlamlı kod-gen  bunlar agresif kuantizasyondan görülebilir şekilde zarar görür. AWQ INT4 MATH'de ~ 3-5 puan kaybeder. Düşünce ağır iş yükleri için, FP8 veya BF16'u gönderin; bellek maliyetini kabul edin.

> Düşünce zinciri, matematik, uzunlukta aşağıdaki kodların üretimi, bu gelişme miktarlarının belirgin etkisini göstermektedir.

### 2026 seçme rehberi

- CPU/gear servis: GGUF Q4_K_M. Tamamlandı.
  中文翻译:CPU/边缘服务:GGUF Q4_K_M。
- GPU servis, rutin sohbet, LoRA yok.
  Çeviri:GPU 服务,通用聊天,无 LoRA:AWQ。
- GPU servis, çoklu LoRA: Marlin ile GPTQ.
  中文翻译:GPU 服务,多 LoRA:GPTQ + Marlin。
- Dönüşümleme iş yükü: FP8.
  Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri
- Blackwell veri merkezi, onaylanmış kalite: NVFP4 + FP8 KV.
  Çeviri:Blackwell 数据中心,已验证质量:NVFP4 + FP8 KV。
- İkiyüzlü: her aday biçiminde 1000 örnek değerlendirme yapın.
  Çinçe Çevirimiçi:不确定: 在每个候选格式上运行 1,000 样本评估──

## Çerçeveyi kullanın.
```figure
gpu-memory-breakdown
```

## Kullan

`code/main.py`bir dizi model boyutu için hafıza ayak izi (koşum + KV + etkinleştirmeler) ve altı format boyunca nispeten geçiş hesaplar. KV önbelleğinin üstün olduğu, ağırlık sıkıştırmasının ödediği ve FP8'in güvenli seçimi olduğu yerleri gösterir.

> `code/main.py`計算一系列模型大小在六种格式下内存占用(权重 + KV + 激活) ve nispeten吞吐量──展示 KV 缓存在在哪里占主导、权重压缩在哪里划算、FP8 在哪里是安全选择──

## İndirin . Ürünler .

> **【拓展：量化选型决策树】**2026 yıl ölçüm biçimi seçim karar biçimi:(1) CPU/边缘部署 → GGUF Q4_K_M;(2) GPU 通用聊天、无 LoRA → AWQ;(3) GPU 多 LoRA → GPTQ + Marlin;(4) 推理密集型任务 → FP8;(5) Blackwell 数据中心、已验证质量 → NVFP4 + FP8 KV;(6) 不确定 → 在候选格式运行1000样本评估;;量化后验证步骤不可省略每个模型 × 量化格式 × 硬件组合都需要独立验;;

Bu ders bize çok yararlı .`outputs/skill-quantization-picker.md`. Hardver, model boyutu, iş yükü türü ve kalite toleransına göre bir format seçer ve kalibrasyon/validasyon planı oluşturur.

> 本课产 出 `outputs/skill-quantization-picker.md`❖ Hardware ❖ model ❖ çalışma yükü tipi ve kalite toleransı, seçim biçimi ve kurum/testleme programı ❖

## Egzersizler.

1. Çık .`code/main.py`Her format için toplam HBM'yi hesaplayın. Hangi format bir H100 80GB'ye sığmanıza izin verir?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`❖ 128 ve 2K'da bulunan 70B model için, her biçimdeki toplam HBM'yi hesaplayın. Hangi biçim bir H100 80GB'nin üzerine yerleştirilebilir?
2. Eğer kalite toleransı konusunda yanılıyorsanız, geri kazanma yolu nedir?
   Çin dilinde:You have a 7B 编码模型――选择一个格式并说明理由―― Eğer kalite toleransına karşı yanlış bir karar verirseniz, geri dönüş yolu nedir?
3. Bir tıbbi alan modeli için AWQ'yi kalibre etmek için gerekli kalibrasyon veri kümesi boyutunu hesaplayın.
   Çinçe çevirisi:计算医疗领域模型 AWQ 校准所需的数据集大小──为什么更多数据不总是好?
4. Marlin-AWQ çekirdek kağıdı veya yayın notlarını okuyun. AWQ'ın 7B'de neden 741 tok/s'e ulaştığını ve çiğ GPTQ'nin neden 712'e ulaştığını üç cümleyle açıklayın.
   Çin Çeviri: Marlin-AWQ 内核论文或发布说明──用三句话解释为什么AWQ 7B'de 741 tok/s'e ulaştığı ve orijinal GPTQ'da yaklaşık 712──
5. AWQ ağırlıklarını FP8 KV kaydıyla BF16'da tutmak ne zaman mantıklı olur?
   Çinçe Çevirimi:何時將 AWQ 权重与 FP8 KV 缓存组合有意,何時保持 BF16 KV?

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| GGUF | "llama.cpp format" | File format bundling K-quant variants; CPU/edge default |
| Q4_K_M | "Q4 K M" | 4-bit K-quant medium; the production GGUF default |
| GPTQ | "gee pee tee q" | Post-train INT4 with calibration; supports LoRA in vLLM |
| AWQ | "a w q" | Activation-aware INT4; Marlin kernels; best Pass@1 at INT4 |
| Marlin kernels | "fast INT4 kernels" | Custom CUDA kernels for INT4 on Hopper; 10x speedup |
| FP8 | "eight-bit float" | Safe precision default on Hopper/Ada/Blackwell |
| MXFP4 / NVFP4 | "microscaling four" | Blackwell 4-bit FP with per-block scale factors |
| Calibration dataset | "cal data" | Input text used to pick quantization parameters; must match domain |
| KV cache quantization | "KV INT8" | Separate choice from weights; affects attention accuracy |

## Daha fazla okumak

- [VRLA Tech — LLM Quantization 2026](https://vrlatech.com/llm-quantization-explained-int4-int8-fp8-awq-and-gptq-in-2026/) karşılaştırmalı referans değerleri.
- [Jarvis Labs — vLLM Quantization Complete Guide](https://jarvislabs.ai/blog/vllm-quantization-complete-guide-benchmarks) Formatlardaki geçiş sayısı.
- [PremAI — GGUF vs AWQ vs GPTQ vs bitsandbytes 2026](https://blog.premai.io/llm-quantization-guide-gguf-vs-awq-vs-gptq-vs-bitsandbytes-compared-2026/) Format-bu format seçimi.
- [vLLM docs — Quantization](https://docs.vllm.ai/en/latest/features/quantization/index.html) desteklenen formatlar ve bayraklar.
- [AWQ paper (arXiv:2306.00978)](https://arxiv.org/abs/2306.00978) orijinal AWQ formülasyonu.
- [GPTQ paper (arXiv:2210.17323)](https://arxiv.org/abs/2210.17323) orijinal GPTQ formülasyonu.
