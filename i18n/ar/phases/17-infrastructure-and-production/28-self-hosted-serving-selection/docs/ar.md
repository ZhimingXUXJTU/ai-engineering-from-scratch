# اختيار خدمة مضيفة ذاتية  llama.cpp, Ollama, TGI, vLLM, SGLang ‬ 自托管 选择 服务 SGLang vLLM
# اختيار الخدمات المضيفة الذاتية  تطابق المحرك مع الأجهزة والقياس

> اختيار المحرك هو وظيفة من الأجهزة والقياس والنظام البيئي  ليس قراءة لوحة الدرجة. أربعة محركات تهيمن على الاستنتاج المضيف الذاتي في عام 2026: llama.cpp، Ollama، vLLM، SGLang، مع TGI تتراجع في وضع الصيانة. **llama.cpp**هو أسرع على CPU  أوسع دعم النموذج، والسيطرة الكاملة على الكمية والخيوط. **Ollama**هو التثبيت من جهاز تحميل الكمبيوتر المحمول واحد القيادة، ~ 15-30٪ أبطأ من llama.cpp (Go + CGo + HTTP التسلسل) ، 3x فجوة التوصيل تحت مثل الحمل. **TGI entered maintenance mode December 11, 2025** فقط تحديات الحذاء، ~ 10% بطيئة التوصيل الخام من vLLM ولكن تاريخيا أعلى قابلية للملاحظة وتكامل HF-النظام البيئي. وهذا الوضع الصيانة تجعل من الرهان المخاطر على المدى الطويل  SGLang أو vLLM هي الافتراضات الأمانية للمشاريع الجديدة. **vLLM**هو افتراض الإنتاج العام  v0.15.1 (فبراير 2026) يضيف PyTorch 2.10, RTX Blackwell SM120, تحسين H200. **SGLang**هو المتخصص الوكلي متعدد التحولات / المواصلات الثقيلة  400,000+ GPU في الإنتاج (xAI ، LinkedIn ، Cursor ، Oracle ، GCP ، Azure ، AWS). القيود على الأجهزة: CPU-first → llama.cpp. AMD / غير NVIDIA → vLLM هو الطريق الأكثر دعماً (TRT-LLM مغلق من NVIDIA). نمط خط أنابيب 2026: dev = Ollama، staging = llama.cpp، prod = vLLM أو SGLang. المحركات تأخذ أشكال وزن مختلفة  GGUF لعائلة llama.cpp، HF safetensors لمحركات GPU  بحيث يمكن أن يكون تحويل النمط بين المراحل.

> **【中文解读】**هذا القسم يعرض على التفاوض والاختيار من إطار التمويل الذاتي.


**Type:** Learn | **类型:** 学习
**Languages:** Python (stdlib, engine-decision tree walker) | **语言:** Python
**Prerequisites:** All Phase 17 lessons covering engines (04, 06, 07, 09, 18) | **前置知识:** All Phase 17 lessons covering engines (04, 06, 07, 09, 18)

>  **【前置】**هذا الجزء هو المرحلة 17 收官课,整合 04/06/07/09/18 引擎知识 四大自托管引擎选择矩阵
>  **【类比】**خود托管引擎 = "AI 服务器品牌"。llama.cpp = CPU 王者(最广模型支持、量化全控制);Ollama = 笔记本一键安装(比 llama.cpp 慢 15-30%);TGI 已进入维护模式(2025.12.11) فقط صلاح البغ،新项目别选;vLLM = 通用生产默认(v0.15.1+ PyTorch 2.10+Blackwell);SGLang = وكيل 多轮+前万密集专家(40+ GPU 在 xAI/LinkedIn/Cursor) 
> 🤔 **【困惑】**س: 我的场景该选哪个? CPU-only→llama.cpp;AMD/非 NVIDIA→vLLM(TRT-LLM 锁 NVIDIA);Agent 多轮→SGLang;通用→vLLM。2026 流水线:dev=Ollama、staging=llama.cpp、prod=vLLM/SGLang,全用 GGUF/HF 权重一致。
**Time:** ~45 minutes | **时间:** ~45 minutes

## أهداف التعلم

- اختر محرك معين الأجهزة (CPU / AMD / NVIDIA Hopper / Blackwell) ، والحجم (1 مستخدم / 100 / 10,000) ، والحمل العمل (التحدث العام / وكيل / السياق الطويل).
  中文翻译:给定硬件(CPU/AMD/NVIDIA Hopper/Blackwell) √规模和工作负载选择引擎──
- أسمي حالة وضع الصيانة TGI لعام 2026 (11 ديسمبر 2025) ولماذا تحيز المشاريع الجديدة نحو vLLM أو SGLang.
  中文翻译:说出 2026 年 TGI 维护模式状态(2025 年 12 月 11 日) و لماذا يؤثر على استخدام HuggingFace 默认设置的团队──
- وصف خط الأنابيب التطوير/التصميم/التصنيع باستخدام نفس الوزن GGUF أو HF في جميع أنحاء.
  中文翻译: وصف استخدام نفس GGUF أو HF 权重的开发/预发布/生产流水线在整个生命周期中──
- شرح لماذا "CPU فقط" يفرض llama.cpp و"AMD" يستبعد TRT-LLM.
  中文翻译:解释为什么"仅CPU"强制使用 llama.cpp而"AMD"排除TRT-LLM。

## المشكلة المشكلة المشكلة

> **【中文解读】**يعتمد اختيار محرك التفكير على ثلاثة أبعاد:hardware(CPU / AMD / NVIDIA Hopper / Blackwell) √ حجم(1 مستخدم / 100 / 10,000) √工作负载(通用聊天 / Agent / 长上下文)  2025 年 12 月 11 日 HuggingFace TGI 进入维护模式(صرف تصحيح البغ) ، مما يجعل المشروع الجديد يجب أن يكون默认远离 TGI ،转向 vLLM أو SGLang.
- وصف خط الأنابيب التطوير/التصميم/التصميم، بما في ذلك حيث يتم تحويل GGUF إلى أسلوب الجهازات الأمانية بين المراحل.
- شرح لماذا يشير "CPU-first" إلى llama.cpp و"AMD" يستبعد TRT-LLM.

> **【拓展：2026 年推理引擎选择决策】**2026 سنة推理引擎的硬件优先决策树:(1) خيارات التنافسية فقط → llama.cpp(唯一有竞争力的选项);(2) AMD GPU → vLLM(ROCm 支持),TRT-LLM 不支持 AMD;(3) NVIDIA Hopper → vLLM أو SGLang أو TRT-LLM(三选一);(4) NVIDIA Blackwell → TRT-LLM 吞吐最高;(5) Apple Silicon → llama.cpp(Metal 后端) △规模决策:1 用户→Ollama,10-100→LLvM 单,100-10K→LLM إنتاج-حجم أو SangGL,10K+→إنتاج-حجم + 分离式 + LMC。

فريقك يبدأ مشروع جديد للدرجة العليا المضيفة الذاتية. يقول مهندس واحد أولاما، يقول مهندس آخر vLLM، يقول ثالث "هل لا تعمل TGI فقط خارج الصندوق؟" كل ثلاثة مناسبة لاقياصات مختلفة. لا واحد مناسب للجميع.

في عام 2026 فإن شجرة الخيار مهمة: الأجهزة أولاً، والحجم الثاني، والحمية العمل الثالثة. وحدث محدد واحد في عام 2025  تدخل TGI وضع الصيانة 11 ديسمبر  تغير الافتراض للمشاريع الجديدة.

## المفهوم الأساسي

### المحركات الخمسة

| Engine | Best for | Notes |
|--------|----------|-------|
| **llama.cpp** | CPU / edge / minimal deps / widest model support | Fastest on CPU, full control |
| **Ollama** | Dev laptops, single user, one-command install | 15-30% slower than llama.cpp; 3x prod throughput gap |
| **TGI** | HF ecosystem, regulated industries | **Maintenance mode Dec 11, 2025** |
| **vLLM** | General-purpose production, 100+ users | Broad production default; v0.15.1 Feb 2026 |
| **SGLang** | Agentic multi-turn, prefix-heavy workloads | 400,000+ GPUs in production |

### القرار الأول عن الأجهزة

**CPU-first**لا يوجد محرك آخر قادر على المنافسة على المعالجة المركزية

**AMD GPU**→ vLLM هو أقوى مسار مدعوم (عملية AMD ROCm). يعمل SGLang أيضا. TRT-LLM مغلق من NVIDIA، لذلك هو خارج.

**NVIDIA Hopper (H100 / H200)**-إنهُم الثلاثة من الدرجة الأولى

**NVIDIA Blackwell (B200 / GB200)**→ TRT-LLM هو قائد التدفق (مرحلة 17 · 07). vLLM و SGLang تتبع قريبًا.

**Apple Silicon (M-series)**- لاما. سي بي (المعدنية) - أولاما يلف هذا

### قرار على المستوى الثاني

**1 user / local dev**أوليما، أوامر واحدة، أول رمز في ثواني.

**10-100 users / small team**-الـ"VLLM" بـ"GPU"

**100-10k users / production**→ مجموعة إنتاج vLLM (مرحلة 17 · 18) أو SGLang.

**10k+ users / enterprise**→ vLLM - مستوى الإنتاج + مقسم (مرحلة 17 · 17) + LMCache (مرحلة 17 · 18).

### ثالث قرار - عبء العمل

**General chat / Q&A**فوز vLLM على الاختلافات الواسعة

**Agentic multi-turn (tools, planning, memory)**تهيمن "RadixAttention" (المرحلة 17 · 06) من SGLang.

**RAG with heavy prefix reuse**-إلى (سجلانغ)

**Code generation**→ vLLM بخير؛ SGLang أفضل قليلا على التخزين.

**Long context (128K+)**→ vLLM + إعادة التعبئة المزروعة؛ SGLang + KV المرتبة.

### فخّ الصيانة TGI

> **【中文解读】**تجي 陷:HuggingFace تجي في 2025 12 مايو 11 日 دخول وضع الحفاظ على التجاوب فقط إصلاح الفحشات، لم يعد هناك إصلاحات وظيفية. في تاريخ تجي لديها أعلى مستويات قابلية للمشاهدة والإعداد الحي في HF.

> **【拓展：工作负载驱动的引擎选择】**工作负载维度驱动引擎选择:(1) 通用聊天/问答 → vLLM(广泛默认);(2) وكيل 多轮对话(工具、规划、记忆)→ SGLang RadixAttention 主导;(3) RAG 重前复用 → SGLang;(4) 代码生成 → vLLM 足够,SGLang 缓存略好;(5) 长上下文(128K+)→ vLLM + 分块预填充,SGLang + 分层 KV──Ollama 适合开发但不是生产共享服务的理想选择Go HTTP 序列化增加开销并发管理比 vLLM 简单、Openmetry 支持滞后.

دخلت Hugging Face TGI وضع الصيانة 11 ديسمبر 2025  فقط تصحيحات الأخطاء في المستقبل. تاريخيا: قابلية مراقبة على المستوى العالي ، أفضل في الفئة HF-التنمية التكامل (بطاقات النموذج ، أدوات السلامة) ، قليلاً خلف vLLM على الانتقال الخام.

بالنسبة للمشاريع الجديدة في عام 2026: الافتراض بعيدا عن TGI. يمكن استمرار نشر TGI الموجودة ولكن يجب أن تنتقل في نهاية المطاف. SGLang و vLLM هي الافتراضات الأكثر أمانا.

### نمط خط الأنابيب

Dev (Ollama) → staging (llama.cpp) → prod (vLLM). تأخذ المحركات تنسيقات وزن مختلفة  GGUF لعائلة llama.cpp ، HF safetensors لمحركات GPU  بحيث يمكن أن يكون تحويل النمط بين المراحل. يقوم المهندسون بالتكرار بسرعة على أجهزة الكمبيوتر المحمولة. تعكس المرايا المرحلة كمية الإنتاج.

### تحذير أولاما

أولاما عظيمة لـ dev. لا تناسب الإنتاج المشترك: إضافة التسلسلات HTTP إلى التكلفة العليا، وإدارة التزامن أبسط من vLLM، تأخيرات دعم OpenTelemetry. استخدم أولاما حيث يضيء  مستخدم واحد، أوامر واحدة  والتحول إلى vLLM للمشاركة.

### المضيف الذاتي مقابل المدير هو قرار منفصل

المرحلة 17 · 01 (مدارات المعدلات المضخمة) · 02 (مواقع الإضفاء) تغطية إدارة. هذا الدروس يفترض أنك قررت بالفعل استضافة الذات. أسباب الاستضافة الذاتية: إقامة البيانات، تحسينات مخصصة، امتلاك التكلفة الإجمالية على النطاق، نموذج النطاق غير متوفر على المضيف.

### أرقام يجب أن تتذكر

- وضع الصيانة TGI: 11 ديسمبر 2025.
- vLLM v0.15.1: فبراير 2026; PyTorch 2.10؛ دعم بلاكويل SM120.
- أثر إنتاج SGLang: 400،000+ GPU.
- فجوة التوصيل في Ollama مقابل llama.cpp: 15-30% أبطأ؛ 3x تحت الحمل الإضافي.

## استخدمها في إطار التنفيذ
```figure
data-parallel
```

## استخدمها

`code/main.py`هو المشي في شجرة القرار: مع إعطاء الأجهزة + الحجم + عبء العمل، يختار المحرك ويوضح السبب.

> `code/main.py`هو المشي في شجرة القرار: مع إعطاء الأجهزة + الحجم + عبء العمل، يختار المحرك ويوضح السبب.

## أرسلها .

> **【拓展：自托管 vs 托管的决策】**الذات المُتَوَفِّق ضدّ التّوَفّق هو قرار مستقل. أسباب التّوَفّق الذّاتية: 1) بيانات البقاء البيانات لا يمكن أن تغادر المنظمة؛ 2) تحديد الذّات  لورا/كلورا 适配器需要本地部署؛ 3) إجماليّة التّوَفّق المُتَوَفّق عن التّوَفّق السّنويّيّة أكثر من 5 مليون دولار  عندما يتّوَفّق الذّات عادةً أكثر اقتصادية. 4) النّموذج في مجال التّوَفّق لا يُمكن استخدامه على منصات التّوَفّق.

هذا الدرس يُنتج`outputs/skill-engine-picker.md`وبالنظر إلى القيود، يختار محركاً ويكتب خطة الهجرة

> 本课产出 `outputs/skill-engine-picker.md`وبالنظر إلى القيود، يختار محركاً ويكتب خطة الهجرة

## تمارين التدريب

1. أركض`code/main.py`مع أجهزة / حجم / عبء العمل الخاص بك. هل الخروج يطابق بديهيتك؟
   中文翻译: 用你的硬件/规模/工作负载运行 `code/main.py`هل الصادرات تتناسب مع توقعاتها؟
2. إنفرانتيك 12 H100s و 8 MI300X AMD أي محرك؟ لماذا ترت-LLM خارج الطاولة؟
   ترجمة: بنيتك التحتية هي 12 بلاك H100 و 8 بلاك MI300X AMD.
3. فريق يريد استخدام TGI في عام 2026 لأن "هذا ما نعرفه".
   ترجمة: فان فريق يفكر في استخدام TGI في عام 2026 لأن "هذا ما نعرفه"
4. أولاما ديف إلى vLLM prod: ما هي التغييرات في الكمية، التكوين، واللاحظية؟
   中文翻译:Ollama 开发到vLLM 生产: قياس، تكوين و可观测性 ما هي التغيرات؟
5. منتج RAG مع طول المرفق الأول P99 8K واستخدام عالي بين المستأجرين. اختيار محرك ووضعها مع المرحلة 17 · 11 + 18.

## شروط الرئيسية

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

## المزيد من القراءة

- [AI Made Tools — vLLM vs Ollama vs llama.cpp vs TGI 2026](https://www.aimadetools.com/blog/vllm-vs-ollama-vs-llamacpp-vs-tgi/)
- [Morph — llama.cpp vs Ollama 2026](https://www.morphllm.com/comparisons/llama-cpp-vs-ollama)
- [n1n.ai — Comprehensive LLM Inference Engine Comparison](https://explore.n1n.ai/blog/llm-inference-engine-comparison-vllm-tgi-tensorrt-sglang-2026-03-13)
- [PremAI — 10 Best vLLM Alternatives 2026](https://blog.premai.io/10-best-vllm-alternatives-for-llm-inference-in-production-2026/)
- [TGI maintenance announcement](https://github.com/huggingface/text-generation-inference) إطلاق الملاحظات.
- [vLLM v0.15.1 release notes](https://github.com/vllm-project/vllm/releases)
