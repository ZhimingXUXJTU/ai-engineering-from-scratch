# Kendine Konutlanan Hizmet Seçimi  llama.cpp, Ollama, TGI, vLLM, SGLang
# Kendine Konutlanan Hizmet Seçimi  Hardware ve ölçekle Eşleşen Motor

> Motor seçimi, bir lider çizelgesi değil, bir donanım, ölçek ve ekosistem fonksiyonu. 2026 yılında dört motor kendi kendine konutlanmış sonuçlara hakim: llama.cpp, Ollama, vLLM, SGLang, TGI bakım modunda geride kalır.**llama.cpp**CPU'da en hızlı  en geniş model desteği, kuantitasyon ve ipleme üzerinde tam kontrol. **Ollama**dev-laptop tek komut yüklemesi, llama.cpp (Go + CGo + HTTP serileşmesi) ile karşılaştırıldığında ~15-30% daha yavaş, prod benzeri yük altında 3x geçiş boşluğu. **TGI entered maintenance mode December 11, 2025** sadece hata düzeltmeleri, ~ 10% daha yavaş ham üretimi, ancak tarihsel olarak en iyi gözlemlebilirlik ve HF ekosistem entegrasyonu. Bu bakım durumu, yeni projeler için riskli uzun vadeli bir bahis yapar  SGLang veya vLLM daha güvenli varsayımlardır. **vLLM**Genel amaçlı üretim öntanımlı  v0.15.1 (Şubat 2026) PyTorch 2.10, RTX Blackwell SM120, H200 optimizasyonu ekler. **SGLang**Bu, bir çok dönüş / önbellek ağırlıklı uzmanı  400.000+ GPU'ların üretimi (xAI, LinkedIn, Cursor, Oracle, GCP, Azure, AWS) için. Hardware kısıtlamaları: CPU-first → llama.cpp. AMD / non-NVIDIA → vLLM en güçlü desteklenen yol (TRT-LLM NVIDIA kilitlenmiştir). 2026 boru hattı modeli: dev = Ollama, staging = llama.cpp, prod = vLLM veya SGLang. Motorlar farklı ağırlık formatlarını alır  llama.cpp ailesi için GGUF, GPU motorları için HF safetensörleri  böylece bir format dönüşümü aşamalar arasında oturabilir.

> **【中文解读】**Bu bölümde kendiliğinden yönetim ve hizmet seçimi biçimleri, TGI, llama.cpp ve diğer çerçevelerin karşılaştırma ve seçimi hakkında bilgi edindiler.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, engine-decision tree walker) | **语言:** Python
**Prerequisites:** All Phase 17 lessons covering engines (04, 06, 07, 09, 18) | **前置知识:** All Phase 17 lessons covering engines (04, 06, 07, 09, 18)

>  **【前置】**Bu bölüm 17 EYİNİNİN ÖGÜRÜNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİNİ
>  **【类比】**Öz托管引擎 = "AI 服务器品牌"。llama.cpp = CPU 王者(最广模型支持、量化全控制);Ollama = 笔记本一键安装(比 llama.cpp 慢 15-30%);TGI 已进入维护模式(2025.12.11) Sadece bug,新项目别选;vLLM = 通用生产默认(v0.15.1+ PyTorch 2.10+Blackwell);SGLang = Agent 多轮+前万密集专家(40+ GPU 在 xAI/LinkedIn/Cursor) ⋅
> 🤔 **【困惑】**S: 我的场景该选哪个? CPU-only→llama.cpp;AMD/非 NVIDIA→vLLM(TRT-LLM 锁 NVIDIA);Agent 多轮→SGLang;通用→vLLM。2026 流水线:dev=Ollama、staging=llama.cpp、prod=vLLM/SGLang,全用 GGUF/HF 权重一致。
**Time:** ~45 minutes | **时间:** ~45 minutes

## Öğrenme hedefleri

- Verilen bir motor (CPU / AMD / NVIDIA Hopper / Blackwell), ölçek (1 kullanıcı / 100 / 10,000) ve iş yükünü seçin (genel sohbet / ajan / uzun bağlam).
  Çeviri: │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │ │
- 2026 TGI bakım modunun durumunu (11 Aralık 2025) ve yeni projeleri vLLM veya SGLang'a neden yönlendirdiğini belirtin.
  Çinçe Çevirimi:  维护模式状态 2026 yıl TGI 维护模式状态 (TGI 维护模式状态)
- Dev/staging/prod borusunu, tümünde aynı GGUF veya HF ağırlıklarını kullanarak tanımlayın.
  Çinçe Çevirimi: tüm yaşam döngüsü boyunca aynı GGUF veya HF 权重的开发/预发布/生产流水线的描述.
- "Sadece CPU" llama.cpp'i neden zorlar ve "AMD" TRT-LLM'i neden dışlıyor açıklayın.
  Çinçe Çevirimiçi: açıklama neden "sadece CPU" llama.cpp zorla kullanıyor ve "AMD" TRT-LLM'yi ortadan kaldırıyor.

## Sorunlar. Sorunlar.

> **【中文解读】**Öz托管推理引擎'ın seçimi üç boyuttan oluşmaktadır:硬件(CPU / AMD / NVIDIA Hopper / Blackwell)  Ölçü(1 kullanıcı / 100 / 10,000) 工作负载(通用聊天 / Agent / 长上下文)  2025 yıl 12 月 11 日 HuggingFace TGI 进入维护模式(仅 bug fix), bu yeni projenin TGI'den uzaklaşmayı, vLLM veya SGLang  2026 yılının 流水线 modeli: Ollama kullanımı geliştirmek, pre-release v.cpp, llama vLLM veya SGLang 全程相同 GGUF/HF 重权使用──
- GGUF'den güvenli sensörlere dönüşümünün aşamalar arasında yer aldığı yer de dahil olmak üzere dev/staging/prod borusunu açıklayın.
- "CPU-first" llama.cpp'e ve "AMD"'nin TRT-LLM'yi neden dışladığı açıklanmalı.

> **【拓展：2026 年推理引擎选择决策】**2026 yıl推理引擎的硬件优先决策树:(1) Yalnızca CPU-→ llama.cpp(唯一有竞争力的选项);(2) AMD GPU → vLLM(ROCm 支持),TRT-LLM 不支持 AMD;(3) NVIDIA Hopper → vLLM 或 SGLang 或 TRT-LLM(三选一);(4) NVIDIA Blackwell → TRT-LLM 吞吐最高;(5) Apple Silicon → llama.cpp(Metal 后端) △ ölçek决策:1 用户→Ollama,10-100→LLM 单,100-10K→LLM üretim-stack 或 SangGL,10K+→production-stack + 分离式 + LMC。

Ekibiniz yeni bir kendi kendine düzenlenen LLM projesine başlıyor. Bir mühendis Ollama, bir başkası vLLM, bir başkası "TGI sadece kutudan çıkmıyor mu?" diyor.

2026'da seçim ağacı önemlidir: donanım birinci, ölçek ikinci, iş yükü üçüncü. Ve 2025'te belirli bir olay  TGI 11 Aralık'ta bakım moduna girdi  yeni projeler için varsayılanı değiştirir.

## Konsepten bir şey.

### Beş motor

| Engine | Best for | Notes |
|--------|----------|-------|
| **llama.cpp** | CPU / edge / minimal deps / widest model support | Fastest on CPU, full control |
| **Ollama** | Dev laptops, single user, one-command install | 15-30% slower than llama.cpp; 3x prod throughput gap |
| **TGI** | HF ecosystem, regulated industries | **Maintenance mode Dec 11, 2025** |
| **vLLM** | General-purpose production, 100+ users | Broad production default; v0.15.1 Feb 2026 |
| **SGLang** | Agentic multi-turn, prefix-heavy workloads | 400,000+ GPUs in production |

### Hardware-first karar

**CPU-first**Ollama da çalışır ama daha yavaş. CPU'da diğer hiçbir motor rekabetçi değildir.

**AMD GPU**→ vLLM en güçlü desteklenen yol (AMD ROCm desteği). SGLang da çalışır. TRT-LLM NVIDIA kilitlenmiştir, bu yüzden dışarıdır.

**NVIDIA Hopper (H100 / H200)**→ VLLM veya SGLang veya TRT-LLM.

**NVIDIA Blackwell (B200 / GB200)**→ TRT-LLM, geçiş lideridir (Fase 17 · 07). vLLM ve SGLang yakından takip eder.

**Apple Silicon (M-series)**Ollama bunu sarıyor.

### İkinci ölçekli karar

**1 user / local dev**Bir komut, saniyeler içinde ilk işaret.

**10-100 users / small team**→ VLLM tek GPU.

**100-10k users / production**→ vLLM üretim aşaması (Fase 17 · 18) veya SGLang.

**10k+ users / enterprise**→ vLLM üretim aşaması + ayrıştırılmış (Fase 17 · 17) + LMCache (Fase 17 · 18).

### İş yükü üçüncü karar

**General chat / Q&A**→ vLLM geniş default kazanır.

**Agentic multi-turn (tools, planning, memory)**→ SGLang'ın RadixAttention (Fase 17 · 06) baskın.

**RAG with heavy prefix reuse**→ SGLang.

**Code generation**→ vLLM iyi; SGLang biraz daha iyi bir önbelleğe.

**Long context (128K+)**→ vLLM + parçalı ön doldurma; SGLang + katlı KV.

### TGI bakım tuzağı

> **【中文解读】**TGI 陷:HuggingFace TGI 2025 yılında 12月11日 olarak maintenance mode'a girdi, sadece hata düzeltmesi, artık hiçbir işlev yok. Tarihte TGI'nin en iyi gözlemselliği ve HF 生态集成 (HF) olması, orijinal 吞吐略低于 vLLM (ÜLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL

> **【拓展：工作负载驱动的引擎选择】**工作负载维度驱动引擎选择:(1) 通用聊天/问答 → vLLM(广泛默认);(2) Agent 多轮对话(工具、规划、记忆)→ SGLang RadixAttention 主导;(3) RAG 重前复用 → SGLang;(4) 代码生成 → vLLM 足够,SGLang 缓存略好;(5) 长上下文(128K+)→ vLLM + 分块预填充,SGLang + 分层 KV──Ollama 开发不适合但不是生产共享服务的理想选择Go HTTP 序列化增加开销并发管理比 vLLM 简单、Openmetry 支持滞后──

Hugging Face TGI bakım moduna girdi 11 Aralık 2025  sadece ileride hata düzeltmeleri. Tarihsel olarak: en üst düzey gözlemsellik, sınıfındaki en iyi HF ekosistem entegrasyonu (model kartlar, güvenlik araçları), ham üretimde vLLM'den biraz geride.

2026'da yeni projeler için: TGI'den default uzaklaştırılmalıdır. Mevcut TGI dağıtımları devam edebilir, ancak sonunda göç etmelidir. SGLang ve vLLM daha güvenli varsayımlardır.

### Boru hattı örneği

Dev (Ollama) → staging (llama.cpp) → prod (vLLM). Motorlar farklı ağırlık formatlarını alır  GGUF için llama.cpp ailesi, HF safetensorları için GPU motorları  böylece bir format dönüşümü aşamalar arasında oturabilir. Mühendisler dizüstü bilgisayarlarda hızlı bir şekilde tekrarlar; aşama aynaları üretim kuantitasyonu; prod hizmet hedefi.

### Ollama uyarısı

Ollama dev için harika. Paylaşılan üretim için iyi değildir: Git HTTP serializasyonu üst ücreti ekler, eşzamanlı yönetim vLLM'den daha basit, OpenTelemetry destek gecikmeleridir. Paylaşılan için  bir kullanıcı, bir komut  ve vLLM'ye geçiş için  parlayan Ollama kullanın.

### Kendi kendine konutlanan ve yönetilen bir karar.

17 · 01 (managed hyperscalers), · 02 (inference platforms) kapsamı yönetildi. Bu ders zaten kendi kendine barındırmaya karar verdiğinizi varsayır.

### Hatırlamalısın numaralar

- TGI bakım modusu: 11 Aralık 2025.
- vLLM v0.15.1: Şubat 2026; PyTorch 2.10; Blackwell SM120 desteği.
- SGLang üretim izleri: 400.000+ GPU.
- Ollama geçiş boşluğu vs llama.cpp: 15-30% daha yavaş; 3x daha düşük yük.

## Çerçeveyi kullanın.
```figure
data-parallel
```

## Kullan

`code/main.py`karar ağacı yürüyüşçüsüdür: donanım + ölçek + iş yükü verildiğinde, bir motor seçer ve nedenini açıklar.

> `code/main.py`karar ağacı yürüyüşçüsüdür: donanım + ölçek + iş yükü verildiğinde, bir motor seçer ve nedenini açıklar.

## İndirin . Ürünler .

> **【拓展：自托管 vs 托管的决策】**Öz托管 vs 托管 is independent decision. ――自托管的理由:(1) 数据驻留数据不能离开组织;(2) 自定义微调LoRA/QLoRA 适配器需要本地部署;(3) Büyük çaplı toplam sahip olmak 年推理支出超过$5M 时自托管通常更经济;(4) 领域模型不在托管平台上可用. ―Phase 17·01(托管超级) 和 ·02(推理平台) 覆盖托管选项.

Bu ders bize çok yararlı .`outputs/skill-engine-picker.md`- Zorluklar karşısında bir motor seçer ve göç planını yazar.

> 本课产 出 `outputs/skill-engine-picker.md`- Zorluklar karşısında bir motor seçer ve göç planını yazar.

## Egzersizler.

1. Çık .`code/main.py`Çıktı output içgüdülerine uyuyor mu?
   Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri: Çeviri`code/main.py`◊ Çıkış beklenmeye uygun mu?
2. İnfra 12 H100 ve 8 MI300X AMD'dir.
   Çinçe Çevirimi: Altyapınız 12 blok H100 ve 8 blok MI300X AMD.
3. Bir ekip 2026'da TGI'yi kullanmak istiyor çünkü "bildiklerimiz bu". Göçme davası hakkında tartışın.
   Bir ekip 2026 yılında TGI'yi kullanmayı düşünüyor çünkü "bu bizim bildiğimiz bir şey"
4. Ollama dev to vLLM prod: Kvantisaj, yapılandırma ve gözlemlenebilirlik hangi değişiklikler?
   Çinçe çevirisi: Ollama  geliştirilmeye vLLM 生产:量化、配置和可观测性 hangi değişiklikler var?
5. RAG ürünleri, P99 önleme uzunluğu 8K ve kiracılarda yüksek yeniden kullanımı ile.

## Anahtar Şartlar .

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| llama.cpp | "the CPU one" | Widest model support, fastest on CPU |
| Ollama | "the laptop one" | One-command install, dev-grade throughput |
| TGI | "HF's serving" | Maintenance mode since Dec 2025 |
| vLLM | "the default" | Broad production baseline 2026 |
| SGLang | "the agentic one" | Prefix-heavy, RadixAttention |
| TRT-LLM | "NVIDIA-locked" | Blackwell throughput leader, NVIDIA only |
| GGUF | "llama.cpp format" | Bundled K-quant variants |
| Production-stack | "vLLM K8s" | Phase 17 · 18 reference deployment |
| Pipeline pattern | "dev→stage→prod" | Ollama → llama.cpp → vLLM; weight formats differ per engine |

## Daha fazla okumak

- [AI Made Tools — vLLM vs Ollama vs llama.cpp vs TGI 2026](https://www.aimadetools.com/blog/vllm-vs-ollama-vs-llamacpp-vs-tgi/)
- [Morph — llama.cpp vs Ollama 2026](https://www.morphllm.com/comparisons/llama-cpp-vs-ollama)
- [n1n.ai — Comprehensive LLM Inference Engine Comparison](https://explore.n1n.ai/blog/llm-inference-engine-comparison-vllm-tgi-tensorrt-sglang-2026-03-13)
- [PremAI — 10 Best vLLM Alternatives 2026](https://blog.premai.io/10-best-vllm-alternatives-for-llm-inference-in-production-2026/)
- [TGI maintenance announcement](https://github.com/huggingface/text-generation-inference)- Bildirme notları.
- [vLLM v0.15.1 release notes](https://github.com/vllm-project/vllm/releases)
