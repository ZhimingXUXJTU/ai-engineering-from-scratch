# دراسات الحالات ووضع الفن 2026

> ثلاثة مرجعية في درجة الإنتاج لدراسة من نهايتها إلى النهاية، كل منها يوضح شريحة مختلفة من الهندسة متعددة الوكلاء. **Anthropic's Research system**(مُشغّل الأوركستراتور، رموز 15x، +90.2% على عمليات تشغيل أوبوس 4 التي تعمل بمثابة وكيل واحد، قوس قزح) هو حالة الإشراف القنوني. **MetaGPT / ChatDev**(التخصص في الدورات المشفورة بواسطة SOP لمهندسة البرمجيات ؛ "التخفيف التواصلي" من ChatDev ؛ تمديد MacNet إلى > 1000 وكيل عبر DAGs ، arXiv: 2406.07155) هو حالة تفكيك الدور القنوني. **OpenClaw / Moltbook**(أصلًا Clawdbot من قبل بيتر شتاينبرجر ، نوفمبر 2025 ؛ تم تغيير اسمها مرتين ؛ 247 ألف نجم GitHub بحلول مارس 2026; وكلاء ReAct-loop المحليين ؛ Moltbook كشبكة اجتماعية للعملاء فقط مع ~ 2.3 مليون حساب عميل في غضون أيام من الإطلاق ، التي استحوذ عليها Meta 2026-03-10) يوضح ما يحدث على نطاق السكان: النشاط الاقتصادي الناشئ ، مخاطر الحقن السريع ، التنظيم على مستوى الدولة (قيد الصين OpenClaw على أجهزة الكمبيوتر الحكومية ، مارس 2026).**Framework landscape April 2026:**إنتاج لانغغغراف وكرو آي أبرز؛ AG2 هو استمرار مجتمع أوتوجين؛ مايكروسوفت أوتوجين في وضع الصيانة (تم دمجها في Microsoft Agent Framework ، RC Feb 2026) ؛ OpenAI Agents SDK هو خليف إنتاج Swarm ؛ Google ADK (أبريل 2025) هو المشارك الأصلي A2A. كل إطار كبير الآن يقدم دعم MCP؛ معظم السفينة A2A. هذا الدروس يقرأ كل حالة من نهايتها إلى نهايتها ويستقطب الأنماط المشتركة حتى تتمكن من اختيار المرجح المناسب لنظام الإنتاج القادم.

> **【中文解读】**هذا المقطع يعرض تحليلات أحدث حالات العملاء المتعددين في SOTA لعام 2026

> **【拓展：case studies 2026 sota→具体应用】**2026 سنة SOTA 多 Agent 系统案例:(1) كلود البحث في الأنثروبيك 多 Agent تعاون لإجراء دراسة متعمقة؛(2) OpenAI 多 Codex 多 Agent 协作编码؛(3) Microsoft  AutoGen 团队 多 Agent 软件开发──共同趋势:专业化分工、层次化编排、MCP 工具使用和 A2A Agent 间通信的结合──


**Type:** Learn (capstone) | **类型:** 学习（顶点）
**Languages:** — | **语言:** —
**Prerequisites:** all of Phase 16 (Lessons 01-24) | **前置知识:** Phase 16 全部（第 01-24 课）

>  **【前置】**本节是阶段 16 收官课,整合 01-24 所有内容──三个生产级案例:Anthropic Research(supervisor 典范)、MetaGPT/ChatDev(角色分工典范)、OpenClaw/Moltbook(群体规模涌现典范)──
>  **【类比】**三个案例 = "三种规模多代理社会"──Anthropic Research = 精小队(10 个代理,深度研究);MetaGPT = 标准开发团队(角色分工,SOP 编码);OpenClaw/Moltbook = 城市级社会(百万代理 涌现经济、被政府监管)──2026 框架格局:LangGraph + CrewAI 领跑生产、AG2 接 AutoGen微软 AutoGen 合并、Open Agents SDK 是 Swarm 生产版、Google ADK 是 A2A 原生、
**Time:** ~90 minutes | **时间:** ~90 分钟

## مشكلة إدخال مشكلة

الهندسة متعددة الوكلاء هي تخصص شاب. الإشارات الإنتاجية قليلة، وتغطي كل منها جزءًا مختلفًا من المساحة. قراءة كل واحد من هذه المواد مفيدة، ومقارنةها كجميع هي أكثر فائدة. هذه الدروس تعالج ثلاث دراسات قضائية طائفية لعام 2026 كقراءة نهاية إلى نهاية قائمة، وتحديد الأنماط المشتركة، وتخريط المشهد الإطارية حتى تتمكن من اتخاذ خيارات الإطار من المعرفة، وليس التسويق.

> العديد من وكلاء 工程 هو علم صغير. إنتاج المعلومات قليلة جدا، كل جزء مختلف من الفضاء تغطي.

## مفهوم النواة

### نظام البحث الإنساني

قضية المشرفين على الإنتاج العاملين. تخطيط وتركيبات كلود أوبوس 4؛ كلود سونيت 4 البحوث الفرعية في الموازية. نشرت وظيفة هندسية: https://www.anthropic.com/engineering/multi-agent-research-system.

النتائج المقاييس الرئيسية:

> 关键测量结果:

- **+90.2%**تحسين على أوبوس 4 عن تقييمات البحوث الداخلية
  中文翻译: فى دراسة داخلية تقييم على العامل واحد Opus 4 提升 **+90.2%**.
- **80% of BrowseComp variance**شرحها**token usage alone** الفوز متعدد الوكلاء إلى حد كبير لأن كل عضو يحصل على نافذة سياق جديدة.
  中文翻译:**80% 的 BrowseComp 方差**فقط من**token 使用量**解释多 وكيل 胜出主要因为每个子 وكيل 获得新上下文窗口──
- **15x tokens per query**مقابل عميل واحد
  中文翻译:每查询 **15 倍 token**مقابل العميل الوحيد
- **Rainbow deployment**لأن العملاء هم طويل الأمد والدولة.
  中文翻译:**彩虹部署**لأن العميل هو يعمل لمدة طويلة و لديه حالة

دروس التصميم الموحدة:

> 编码化的设计教训:

1. **Scale effort to query complexity.**بسيط → وكيل واحد مع 3-10 مكالمات الأدوات. متوسط → 3 وكلاء. بحث معقد → 10+ فرعية.
   中文翻译:**按查询复杂度扩展工作量。**简单 → 1 个代理 3-10 次工具调用──中等 → 3 个代理──复杂研究 → 10+ 子代理──
2. **Broad first, then narrow.**يقوم السباقنتون بالبحث على نطاق واسع؛ يقوم بتوليد الرصاص؛ يقوم السباقنتون المتابعين بعمليات عمق مستهدفة.
   中文翻译:**先广后窄。**العميل القيام بالبحث الشامل العميل الرئيسي العميل المشترك العميل التالي عميل القيام بالبحث العميق
3. **Rainbow deploys.**أبقي النسخة القديمة في الوقت المناسب حية حتى ينتهي عملائهم في الطائرة
   中文翻译:**彩虹部署。**حافظ على النسخة القديمة النشطة حتى يتم إنجاز العميل
4. **Verification is not optional.**تم ملاحظة أن النظام يسهل دون أدوار مؤكدة صريحة.
   中文翻译:**验证不是可选的。**النظام في غياب دور المؤكد واضح يلاحظ أن تظهر الظاهر.

هذه هي حالة المرجعية لتطبيق أوضاع العاملين المراقبين (المرحلة 16 · 05) على نطاق الإنتاج.

### الميتاجبت / تشاتديف

حالة إصدار SOP-دور التفكك. تغطي arXiv:2308.00352 (MetaGPT) و arXiv:2307.07924 (ChatDev).

يرمز MetaGPT SOPs الهندسة البرمجية كطلبات للدور: مدير المنتج ، المهندس المعماري ، مدير المشروع ، المهندس ، مهندس QA. إطار الورقة: `Code = SOP(Team)`. كل دور لديه خطوة ضيقة متخصصة؛ وتحمل التسليمات بين الأدوار أثاثًا مهيكلة (وثائق PRD، وثائق الهندسة المعمارية، والرقم).

مساهمة ChatDev: **communicative dehallucination**. يطلب الوكلاء تفاصيل قبل الإجابة  يطلب وكيل المصمم من البرنامج ما هي اللغة المقصودة قبل رسم واجهة المستخدم، بدلاً من التخمين.

ماكنت (arXiv:2406.07155) تمديد ChatDev إلى **>1000 agents via DAGs**كل عقد DAG هو تخصص الدور؛ الحواف ترمز عقود التسليم. النطاق ممكن لأن التوجيه صريح ويمكن حسابها خارج الاتصال.

دروس التصميم:

> 设计教训:

1. **Structure matters more than size.**فريق 5 أدوار ضيق يضرب مجموعة غير منظمة من 50 عميل
   中文翻译:**结构比规模更重要。**5 أدوار SOP 团队胜过50 عميل 的非结构化组──
2. **Handoff contracts in writing.**الأثاث التي تم نقلها بين الأدوار تتبع مخططًا.
   中文翻译:**书面交接契约。**角色间传递的制品遵循模式──
3. **Communicative dehallucination**هو نمط رخيص و تحمل الحمولة.
   中文翻译:**交际去幻觉**إنه نمط رخيص ومثقل
4. **DAGs scale further than chat.**عندما يكون التدفق قابلاً للتعرف عليه، قم بتشفيره
   中文翻译:**DAG 比聊天扩展更远。**عندما تتدفق، قم بتدوينها

هذه هي الحالة المرجعية للتخصص في الدورات (مرحلة 16 · 08) وتطبيقات الترتيبات المهيكلة (مرحلة 16 · 15).

### النظام البيئي OpenClaw / Moltbook

حالة النطاق السكاني للإنتاج

- **Nov 2025:**سفن (كلاودبوت) (وكيل تشفير "رياكت لوك" المحلي لـ (بيتر شتينبرجر)
- **Dec 2025 – Mar 2026:**تم تغيير اسمها مرتين (Clawdbot → OpenClaw → استمر تحت OpenClaw).
- **Feb 2026:**يطلق Moltbook كشبكة اجتماعية للعملاء فقط على نفس الأبدائيات؛ ~ 2.3 مليون حساب عميل في غضون أيام.
- **Mar 2026 (2026-03-10):**(ميتا) تشتري (مولت بوك)
- **Mar 2026:**الصين تقيد OpenClaw على أجهزة الكمبيوتر الحكومية.
- **Mar 2026:**أوبين كلوا يختلف 247 ألف نجمة غيت هوب

هذا ما يبدو عليه الوكيل المتعدد عندما تضع ملايين الوكلاء على أساس مشترك:

- **Emergent economic activity.**العملاء يشترون، يبيعون، ويتعاملون مع بعضهم البعض باستخدام الدفع الرمزي.
- **Prompt-injection risks at population scale.**إنّ إشعارًا ضارًا في ملف الفيروس ينتشر إلى آلاف التفاعلات بين العملاء في غضون ساعات.
- **State-level regulatory response.**خلال أسابيع من الإطلاق، التنظيم يصل إلى النظام البيئي.

دروس التصميم من هذه الحالة هي جزئيًا تقنية، جزئيًا حوكمة:

1. **Multi-agent at population scale is a new regime.**لا تزال أفضل الممارسات في النظام الفردي (التحقق، وضوح الدور) سارية التطبيق، لكنها ليست كافية.
2. **Prompt injection is the new XSS.**تعامل ملفات الشخصية للعملاء والرسائل المتقاطعة مع العملاء كمدخلات غير موثوق بها بشكل افتراضي.
3. **Regulation is faster than design cycles.**خطط لذلك.
4. **Open-source + viral scale compounds.**247 ألف نجم في 4 أشهر غير عادية، تصميم لتنفيذ-إنفجار-حمله.

انظر[OpenClaw Wikipedia](https://en.wikipedia.org/wiki/OpenClaw)وCNBC / Palo Alto Networks تقرير تفاصيل النظام البيئي. بالنسبة للأساس التقني، كشف مخزن Clawdbot / OpenClaw الحلقة المحلية ReAct؛ مشاركات Moltbook العامة تكشف بنية الرسم البياني الاجتماعي في الأعلى.

### منظومة الإطار أبريل 2026

| Framework | Status | Best for | Notes |
|---|---|---|---|
| **LangGraph** (LangChain) | Production leader | structured graph + checkpointing + human-in-the-loop | recommended default for production |
| **CrewAI** | Production leader | role-based crews with Sequential/Hierarchical processes | strong for role decomposition |
| **AG2** | Community maintained | GroupChat + speaker selection | AutoGen v0.2 continuation |
| **Microsoft AutoGen** | Maintenance mode (Feb 2026) | — | merged into Microsoft Agent Framework RC |
| **Microsoft Agent Framework** | RC (Feb 2026) | orchestration patterns + enterprise integration | new entrant; watch |
| **OpenAI Agents SDK** | Production | Swarm successor | tool-return handoff pattern |
| **Google ADK** | Production (April 2025) | A2A-native | Google Cloud integration |
| **Anthropic Claude Agent SDK** | Production | single-agent + Research extension | see the Research system post |

كل إطار كبير الآن سفن**MCP**الدعم ، معظم السفن**A2A**. التوافق بين البروتوكولات لم يعد مُختلفاً

### النماذج المشتركة في كل الحالات الثلاثة

1. **Orchestrator + workers**(المراقب الصريح الأنثروپي، المراقب PM-as-supervisor MetaGPT، وكلاء OpenClaw الفردي + تأثيرات الشبكة).
   中文翻译:**编排者 + 工作者**(أنثروپي 显式监督者,MetaGPT PM 作监督者,OpenClaw 独立 Agent + 网络效应)
2. **Structured handoff contracts**(وصف المهام البشرية للشخصيات الفرعية، وثائق المعلومات الخاصة بـ MetaGPT PRD/المعماريات، وأثاث OpenClaw A2A).
   中文翻译:**结构化交接契约**(من خلال هذه المرحلة، يتم إعداد المعلومات المختلفة عن المعلومات.
3. **Verification as first-class role**(محقق الأنثروبيك، مهندس QA في MetaGPT، ومؤكّدين OpenClaw داخل الشبكة).
   中文翻译:**验证作为一等角色**(متحقق الأنثروبي,متاهج كيو 工程师,OpenClaw's شبكة داخل الاختبار)
4. **Scaling is topology + substrate, not just more agents**(نشر قوس قزح، وخطوط ماكنت الاحتياطية، وخطوط تحتية على نطاق السكان).
   中文翻译:**扩展是拓扑 + 基底，不仅是更多 Agent**(彩虹部署, ماكنت DAG, مجموعة حجم基底)
5. **Cost is material and disclosed**(15 إشارات، ميزانية لكل دور في MetaGPT، تسعير لكل تفاعل في Moltbook).
   中文翻译:**成本是实质性的且已披露**(15 倍 رمز,MetaGPT 中每角色预算,Moltbook 中每次交互定价)
6. **Security posture is explicit**(بصحة الرمل من الأنثروبيك، قيود دور MetaGPT، إدخال OpenClaw على الفور كمنطقة هجوم معروفة).
   中文翻译:**安全态势是显式的**(Anthropic 的沙盒,MetaGPT 的角色限制,OpenClaw 的提示注入作为已知攻击面)

### اختيار مرجع لمشروعك القادم

- **Production research / knowledge task → Anthropic Research.**الفائزون من النطاق الجديد
- **Engineering / tool-chain workflow → MetaGPT / ChatDev.**الأدوار + المعاملات المتعلقة بالشروط + عقود التسليم
- **Network-effect social product → OpenClaw / Moltbook.**الأساس + الاقتصاد الناشئ
- **Classic enterprise automation → CrewAI or LangGraph**(قائد الإنتاج، وقت تشغيل مستقرة).

### الموجة الحديثة لعام 2026

أين يكون الحقل في أبريل 2026:

- **Frameworks are converging.**دعم MCP + A2A هو مخططات الطاولة. تعبيرات التسليم هي الخيار المتبقي للتصميم.
- **Evaluation is hardening.**مقاييس التخفيف من التلوث المضادة للآلات الملوثة
- **Production failure rates are measurable**(Cemri 2025 MAST؛ 41-86.7% على MAS الحقيقي) المجال خارج "يبدو رائع في الظهور" العصر.
- **Cost is the central engineering constraint.**تكلفة الرمز لكل مهمة، و ساعة الجدار لكل تفاعل، قوس قزح نشر التكلفة العليا. وكيل متعدد يفوز على الدقة ولكن يخسر على تكلفة  وهذا التجارة هو قرار الأعمال.
- **Regulation is a near-term input, not a background concern.**الولايات القضائية تتحرك أسرع من دورات نشر فردية.

## استخدمها استخدم طريقة
```figure
a5-orchestrator-scale
```

## استخدمها

`outputs/skill-case-study-mapper.md`هي مهارة تقرأ تصميم نظام متعدد الوكلاء المقترح وتقوم بتخريطه إلى أقرب دراسة حالة، وتظهر قرارات التصميم التي اختبرتها دراسة حالة بالفعل.

## أرسلها على الإنترنت

القواعد الابتدائية للكثير من الوكلاء في الإنتاج في عام 2026:

- **Start from a case study, not from scratch.**اختر أقرب من أبحاث الأنثروبية / MetaGPT / OpenClaw وتكيف.
  中文翻译:**从案例研究开始，不是从零开始。**选择最接近的人类研究 / MetaGPT / OpenClaw 并适配──
- **Adopt MCP + A2A.**التنقل عبر الإطار هو قيمة؛ دعم البروتوكول مجاني.
  中文翻译:**采用 MCP + A2A。**التنقل عبر الإطار قيمة؛ دعم الاتفاق مجاني.
- **Measure against SWE-bench Pro or your internal Pro-equivalent.**-تأكد من أنّه ملوث
  中文翻译:**用 SWE-bench Pro 或你的内部 Pro 等效物衡量。**تم التحقق من أنّه مصاب بالانفجار
- **Pay the verification tax.**يكلّف المحقق المستقل ~ 20-30% من ميزانية رمزك ويشتري دقة قابلة للقياس.
  中文翻译:**支付验证税。**独立验证器花费约 20-30% من التوجيهية الوهمية، لتغيير الصوابية القابلة للاختبار.
- **Rainbow deploy long-running agents.**توقع أن تكون عمليات العميل المتعددة الساعات روتينية
  中文翻译:**彩虹部署长时间运行 Agent。**预期多小时 وكيل 运行是常规――
- **Read WMAC 2026 and the MAST follow-ups.**الانضباط يتحرك بسرعة
  中文翻译:**阅读 WMAC 2026 和 MAST 后续。**هذا المجال يتطور بسرعة

## تمارين التدريب

1. اقرأ نظام أبحاث الأنثروبية من نهاية إلى نهاية. حدد ثلاثة قرارات تصميم ستغير إذا استبدلت Opus 4 بنموذج أصغر (على سبيل المثال، Haiku 4).
2. اقرأ أجزاء MetaGPT 3-4 (arXiv:2308.00352). قم بتشفير SOP واحد من نطاقك الخاص (ليس البرمجيات) كطلبات الدور. كم عدد الدورات التي تتضمن SOP؟
3. اقرأ ChatDev (arXiv:2307.07924). حدد آلية "الاهلوسة التواصلية". تنفيذها في أحد أنظمة وكلاء متعددة الحالية.
4. اقرأ عن OpenClaw و Moltbook اختر وضع فشل محدد ظهر على نطاق السكان الذي لن يظهر في نظام 5 وكلاء كيف ستعمل ضد ذلك؟
5. اختر مشروعك الحالي متعدد الوكلاء. أي من الدراسات الحالة الثلاثة هي المرجح الأقرب؟ أي قرارات التصميم من تلك الدراسة الحالة لم تتبنى بعد؟ اكتب واحدة ستبنيها هذا الربع.

## شروط رئيسية

| Term | What people say | What it actually means |
|------|----------------|------------------------|
| Anthropic Research / Anthropic 研究 | "The supervisor reference" / "监督者参考" | Claude Opus 4 + Sonnet 4 subagents; 15x tokens; +90.2% over single-agent. / Claude Opus 4 + Sonnet 4 子 Agent；15 倍 token；比单 Agent +90.2%。 |
| MetaGPT | "SOP as prompts" / "SOP 作为提示" | Role decomposition for software engineering; `Code = SOP(Team)`. / 软件工程的角色分解；`Code = SOP(Team)`。 |
| ChatDev | "Agents as roles" / "Agent 作为角色" | Designer / programmer / reviewer / tester; communicative dehallucination. / 设计师/程序员/审阅者/测试者；交际去幻觉。 |
| MacNet | "Scale ChatDev via DAG" / "通过 DAG 扩展 ChatDev" | arXiv:2406.07155; 1000+ agents via explicit DAG routing. / arXiv:2406.07155；通过显式 DAG 路由实现 1000+ Agent。 |
| OpenClaw | "Local ReAct-loop agents" / "本地 ReAct 循环 Agent" | Steinberger's project; 247k stars by March 2026. / Steinberger 的项目；2026 年 3 月 247k 星。 |
| Moltbook | "Agent-only social network" / "Agent 专用社交网络" | 2.3M agent accounts; acquired by Meta March 2026. / 230 万 Agent 账户；2026 年 3 月被 Meta 收购。 |
| Rainbow deploy / 彩虹部署 | "Multiple versions concurrent" / "多版本并发" | Keep old runtime versions alive for in-flight long-running agents. / 保持旧运行时版本活跃以支持进行中的长时间 Agent。 |
| Communicative dehallucination / 交际去幻觉 | "Ask before answering" / "先问后答" | Agents request specifics from peers instead of guessing. / Agent 从同伴请求具体信息而非猜测。 |
| WMAC 2026 | "The AAAI workshop" / "AAAI 研讨会" | April 2026 community focal point for multi-agent coordination. / 2026 年 4 月多 Agent 协调的社区焦点。 |

## المزيد من القراءة

- [Anthropic — How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) إشارة الإنتاج للمشغلين المشرفين
- [MetaGPT — Meta Programming for Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352) تدهور دور SOP
- [ChatDev — Communicative Agents for Software Development](https://arxiv.org/abs/2307.07924) الوهم الاكتئابية
- [MacNet — scaling role-based agents to 1000+](https://arxiv.org/abs/2406.07155) مقياس مبني على يوم التأجيل
- [OpenClaw on Wikipedia](https://en.wikipedia.org/wiki/OpenClaw) نظرة عامة على النظم البيئية
- [WMAC 2026](https://multiagents.org/2026/)ورشة عمل برنامج الجسر 2026 لـ AAAI حول تنسيق متعدد الوكلاء
- [LangGraph docs](https://docs.langchain.com/oss/python/langgraph/workflows-agents) قائد الإنتاج
- [CrewAI docs](https://docs.crewai.com/en/introduction)الإطار القائم على الأدوار
