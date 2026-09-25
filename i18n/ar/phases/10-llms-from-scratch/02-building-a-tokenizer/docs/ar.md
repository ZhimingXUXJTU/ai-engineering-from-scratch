# بناء Tokenizer من الصفر من الصفر بناء分词器

> الدروس رقم واحد أعطتك لعبة، هذه الدروس تعطيك سلاحاً

> **【中文解读】**أول صف BPE هو لعبة،本课构建生产级分词器:处理 یونیكود、空白归归一化、特殊代币、字节级回退(让任何输入都能编码,包括emoji 和中文) ⋅

> **【拓展：tiktoken/HuggingFace】**تمثل إطار GPT-4 من إشارات التكنولوجيا والإلاما تنفيذات درجة الإنتاج. فهم مبادئها الداخلية يساعد على تحسين الإعداد والتحكم في التكلفة.

>  **【前置】**学本节前请先掌握:(1) المرحلة 10·01(Tokenizers: BPE/WordPiece/SentencePiece)  فهم مفهوم BPE 合并循环和合并表的;(2) Unicode و UTF-8 编码codepoint、字节、NFC/NFKC 归一化的区别;(3) 正则表达式特别是`\p{L}`.`\p{N}`、负向先行断言 `(?!\S)`()) (4) (بايتون)`regex`库( ليست معيار `re`، لأن`re`غير تدعم خصائص يونيكود)。

**Type:** Build
**Languages:** Python
**Prerequisites:** Phase 10, Lesson 01 (Tokenizers: BPE, WordPiece, SentencePiece)
**Time:** ~90 minutes

## أهداف التعلم

- قم ببناء رمز BPE من مستوى الإنتاج الذي يتعامل مع Unicode ، وتطبيع الفضاء الأبيض ، والرموز الخاصة
  构建处理 يونيكود、空白归归一化和特殊代币的生产级 BPE 分词器
- تنفيذ التراجع على مستوى البايت حتى يتمكن الوهم من تشفير أي مدخل (بما في ذلك إيموجي ، CJK ، والرمز) دون رموز مجهولة
  实现字节级回退,使分词器能编码任何输入( بما في ذلك إموجي、CJK、代码) دون إنتاج رمز غير معروف
- إضافة أنماط regex قبل التوكينيزة التي تقسم النص في حدود الكلمات قبل تطبيق دمج BPE
  添加预分词正则模式,在 BPE 合并前按词边界 分分文本
- تدريب رمزية مخصصة على الجسم وتقييم نسبة ضغطها مقابل التكوكين على النص متعدد اللغات
  في اللغة تعليمه على تعريف الكلمات الخاصة بك، وتقييمها على مقالات متعددة اللغات مع تكتوكين

> **【中文解读】**هذا الدراسة هو الهدف من الدراسة الأولى من أدوات BPE  تحسين لدرجة الإنتاج 分词器.

## المشكلة المشكلة المشكلة

رمز البيانات البيانية من الدروس 01 يعمل على النص الإنجليزي الآن ارمي اليابانية عليه أو إيموجي أو رمز Python مع علامات التبويب المختلطة والمساحات

> تعليميات المعلومات المختلفة:

إنه يتحطم

> سوف تنهار

ليس لأن BPE خاطئ، لأن التنفيذ غير كامل. إشارة الإنتاج تتعامل مع البايتات الخام في أي تشفير، وتقوم بتطبيع يونيكود قبل الانقسام، وتتعامل مع الرموز الخاصة التي لا يتم دمجها، وتقوم بتطبيق الرموز قبل الانقسام مع الكلمات الفرعية، وتقوم بكل هذا بسرعة كافية لتجنب تعقيد خط أنابيب تعليمي معالجة 15 تريليون رمزا.

> ليس لأن BPE لديه مشاكل بل لأن التنفيذ غير كامل‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬

توكيينزير جي بي تي-2 لديه 50257 توكيين إلاما 3 لديها 128,256. (جبت 4) لديها حوالي 100 ألف هذه ليست أرقام ألعاب تم تدريب الجداول المدمجة وراء هذه المفردات على مئات الجيغابايت من النص، والآلة المحيطة بها -- التطبيع، التوكنات المسبقة، حقن رمز خاص، تنسيق قوالب الدردشة -- هي ما يفصل بين رمزية تتعامل مع "هلا العالم"

> يحتوي جهاز GPT-2 على 50،257 رمز. لاما 3 لديه 128،256 رمز. GPT-4 حوالي 100،000 رمز. هذه ليست أرقام اللعب. هذه الكلمات ليست أرقام اللعب.

ستقوم ببناء تلك الآلة

> ستقوم ببناء هذا الجهاز

> **【中文解读】**生产级分词器不是单一算法,而是一个五阶段管线:归一化 → 预分词 → BPE 合并 → 特殊代币注入 → ID 映射──每个阶段解决不同的问题──例如 NFKC 归一化把 "fi" 连字(U+FB01) تحول إلى "fi" 两个字符,预分词防止 "cat" 被合并出 "e c" 这样代币──

>  **【类比】**产产级分词器像"邮局的信件处理流水线":归一化是"统一邮编格式"(U+FB01 "fi" → "fi",全角字母 → 半角),预分词是"按目的先分堆"(按词边界、数字、标点切,避免跨城市混装),BPE 合并是"高频包裹自动拼箱"(常见词直接整箱),特殊代币是"挂号信标签"(BOS/EOS/PAD 最后永远不参与拼箱),才是"贴条形码"(ID 映射) ⋅ أي صيغة تفشل,邮件就乱.

> **【拓展：Llama 3 的分词器升级】**في Llama 3 中将词表从 32K(Llama 2 的句子Piece BPE) تحديث إلى 128K(tiktoken 风格字节级 BPE) ، خصيصاً زيادة رمزات الكتب غير الإنجليزية 分配── هذا التغيير جعل كفاءة الضغط في العديد من اللغات تزيد حوالي 2 مرات ، ولكن عدد عناصر المصفوفات المحددة قد زاد 4 مرات(32K→128K)──

## المفهوم الأساسي

### خط الأنابيب الكامل

إنّ رمز إنتاج ليس خوارزمية واحدة، بل خط أنابيب من خمس مراحل، تحلّ كلّ منها مشكلة مختلفة.

> إنتاج درجة الفصيلة ليست خوارزمية واحدة. إنها خطة من خمس مراحل، كل مرحلة تحل مشاكل مختلفة.

```mermaid
graph LR
    A[Raw Text] --> B[Normalize]
    B --> C[Pre-Tokenize]
    C --> D[BPE Merge]
    D --> E[Special Tokens]
    E --> F[Token IDs]

    style A fill:#1a1a2e,stroke:#e94560,color:#fff
    style B fill:#1a1a2e,stroke:#e94560,color:#fff
    style C fill:#1a1a2e,stroke:#e94560,color:#fff
    style D fill:#1a1a2e,stroke:#e94560,color:#fff
    style E fill:#1a1a2e,stroke:#e94560,color:#fff
    style F fill:#1a1a2e,stroke:#e94560,color:#fff
```

كل مرحلة لها وظيفة محددة:

> كل مرحلة لها وظيفة محددة:

| Stage | What It Does | Why It Matters |
|-------|-------------|----------------|
| Normalize | NFKC Unicode, lowercase optional, strip accents optional | "fi" ligature (U+FB01) becomes "fi" (two chars). Without this, same word gets different tokens. |
| Pre-Tokenize | Split text into chunks before BPE | Prevents BPE from merging across word boundaries. "the cat" should never produce a token "e c". |
| BPE Merge | Apply learned merge rules to byte sequences | The core compression. Turns raw bytes into subword tokens. |
| Special Tokens | Inject [BOS], [EOS], [PAD], chat template markers | These tokens have fixed IDs. They never participate in BPE merges. The model needs them for structure. |
| ID Mapping | Convert token strings to integer IDs | The model sees integers, not strings. |

### BPE مستوى البايت

كانت هذه الدعوة الصحيحة، لكننا نسرفنا شيئاً مهماً: ماذا يحدث عندما تكون تلك البايتات غير صالحة على UTF-8؟

> في أول صف تعريف الكلمات في UTF-8 字节 على التشغيل. هذا هو الخيار الصحيح. ولكننا قفزنا عن بعض الأشياء المهمة: ماذا يحدث عندما هذه العبارات ليست فعالة في UTF-8 ؟

يحل BPE على مستوى البايت هذا الأمر عن طريق التعامل مع كل قيمة البايت الممكنة (0-255) كرمز صالح. قاموسك الأساسي هو بالضبط 256 إدخال. أي ملف - نص، ثنائي، فاسد - يمكن أن يتم توكينه دون إنتاج رمز مجهول.

> 字节级 BPE 通过将每个可能的字节值(0-255)视为有效代币来解决这个问题――你的基础词表恰好 256条条点――任何文件文本、二进制、损坏的都可以被分词而无产生未知代币──

أضاف GPT-2 خدعة: خريطة كل بايت إلى حرف يونيكود قابل للطباعة حتى تظل المفردة قابلة للقراءة من قبل الإنسان. يصبح بايت 0x20 (المجال) حرف "G" في خريطهم. هذا تجميلي خالص. لا يهتم الخوارزمي.

> GPT-2 加一个花招:将每个字节映射到一个可打印的Unicode字符,使词表保持可读性──字节 0x20(空格) في خريطهم تصبح حرف "G"──这纯粹是装饰性的──算法不关心这个──

القوة الحقيقية: BPE على مستوى البايت يتعامل مع كل لغة على وجه الأرض. الحروف الصينية 3 UTF-8 بايت لكل. اليابانية يمكن أن تكون 3-4 بايت. العربية، ديواناجاري، إيموجي -- كل ذلك مجرد تسلسل البايت. خوارزمية BPE يجد أنماط في هذه تسلسلات البايت بالضبط بنفس الطريقة التي يجد فيها أنماط في البايتات ASCII الإنجليزية.

> الحقيقية للقوة: درجة الخطوط BPE  معالجة كل لغة على الأرض  الكلمات الوسطى كل 3  字节 UTF-8 字节。 اليابانية تشكل 3-4 字节。 العربية文、天城文、eMojis都只是字节序列。 الجيومات BPE  طريقة البحث عن النمط في هذه الجيومات 字节 هي تماما نفسها في الإنجليزية ASCII 字节。

> **【中文解读】**المزايا الأساسية لصفحة BPE: أساسية الكلمات تشكل 256 字节، أي إدخال يمكن ترقيتها. GPT-2 أيضاً عملت "فنية طريقا" لتقديم كل كلمة إلى خطة يونيكود قابلة للطباعة، لتجعل الكلمات تشكل أكثر سهولة القراءة.

### التوكنيزية السابقة

قبل أن يلمس BPE نصك، تحتاج إلى تقسيمه إلى قطع. هذا يمنع خوارزمية الاندماج من إنشاء رموز تتجاوز حدود الكلمات.

> قبل أن تقوم بـ BPE  معالجة نصك ، تحتاج إلى تقسيمها إلى كتب ‬ هذا يمنع الجهاز من إنشاء رموز عبر الحدود الكلمة ‬

يستخدم GPT-2 نمط regex لتمزيق النص:

> GPT-2 استخدام إعلانات رسمية لتحويل النص:

```
'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+
```

ينفصل هذا النمط على الانقباضات ("لا" يصبح "don" + "'t") ، الكلمات التي لديها مساحات رئيسية اختيارية ، والأرقام ، والخطوط ، والمساحة البيضاء. يتم الحفاظ على المساحة الرئيسية متصلة بالكلمة - لذلك "الكاتس" تصبح ["ال" " القط" "] ، وليس ["ال" " " " " القط" ".

> هذا النموذج حسب المختصرة تمزيقها("لا" حول إلى "don" + "'t")、带可选前导空格的词、数字、标点和空格。前导空格保持在词上所以" القط" 变成 ["the", "cat"],而不是 ["the", "", "cat"]。

يستخدم Llama SentencePiece ، الذي يخطى regex بالكامل. يعامل تيار البايت الخام كسلسلة طويلة واحدة ويسمح خوارزمية BPE معرفة الحدود. هذا أبسط ولكن يمنح BPE المزيد من الحرية لإنشاء رموز كلمة متقاطعة.

> لاستخدام جملة قطعة، تماما تجاوزت التعبير الاصلي. سوف يكون الافضل في الافضلات الاصلية لتكون سلسلة طويلة، دع الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخبار الاخاخاخاخاخاخاخاخاخاخاخاخاخاخاخاخاخاخاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخار الاخ

الاختيار مهم. يمنع regex GPT-2 من تعلم "ال" في نهاية كلمة واحدة و "ال" في بداية الكلمة التالية يجب أن تتضامن. يسمح SentencePiece بذلك ، مما ينتج أحيانًا ضغطًا أكثر كفاءة ولكن رموزًا أقل تفسيرًا.

> هذا الاختيار مهم للغاية. قاعدة GPT-2 هي الوقاية من تعبير الكلمات في نهاية كلمة واحدة "ال" و "ال" و "ال" في نهاية كلمة واحدة "ال" 合并.

### رموز خاصة

كل رمز إنتاج يحتفظ بطلائل رمزية للمعلامات الهيكلية:

> كل درجة الإنتاج分词器都为结构标记保留代币ID:

| Token | Purpose | Used By |
|-------|---------|---------|
| `[BOS]` / `<s>` | Beginning of sequence | Llama 3, GPT |
| `[EOS]` / `</s>` | End of sequence | All models |
| `[PAD]` | Padding for batch alignment | BERT, T5 |
| `[UNK]` | Unknown token (byte-level BPE eliminates this) | BERT, WordPiece |
| `<\|im_start\|>` | Chat message boundary start | ChatGPT, Qwen |
| `<\|im_end\|>` | Chat message boundary end | ChatGPT, Qwen |
| `<\|user\|>` | User turn marker | Llama 3 |
| `<\|assistant\|>` | Assistant turn marker | Llama 3 |

لا يتم تقسيم الرموز الخاصة من قبل BPE. يتم مطابقةها بالضبط قبل تشغيل خوارزمية الاندماج ، وتم استبدالها بطاقة الهوية الثابتة ، ويتم توكيين النص المحيط بشكل طبيعي.

> الـ "التكنولوجيا الخاصة" لن يتم تفكيكها أبداً. يتم تكييفها بشكل صحيح قبل أن يتم تنفيذ الخوارزمية المشتركة، وبدلًا في الهوية الثابتة.

> **【中文解读】**الـ "التعلامات الخاصة" هي علامة الاحتفاظ "لا يمكن لمسها" في الـ "分词器":`[BOS]`(序列开始)`[EOS]`(序列结束)`[PAD]`(批次填充) 聊天模板标记等──它们有固定的身份,永远不参与BPE 合并,而在合并之前通过精确匹配被提取出来──Llama 3 使用 `<|start_header_id|>`.`<|end_header_id|>`.`<|eot_id|>`لتعريف هيكل المحادثة،ChatGPT استخدام `<|im_start|>`和 `<|im_end|>`.

> **【拓展：聊天模板的工程陷阱】**聊天模板 هو أسهل مكان للخطاء في التنفيذ العملي. كل نموذج يستخدم رمز خاص في التدريب، أي خلاف  عدم وجود تبادل، 更多 空格、 टोकن  ترتيب الخطأ 都会让输入偏离训练分布,导致模型输出垃圾.`chat_template`نظام جينجا2 هو من أجل تقييم هذه العملية

> ️ **【易错点】**实现特殊 token 的三个陷:(1) **特殊 token 内含正则元字符**如 `<|im_start|>`وسط`|`يجب أن تستخدم`re.escape()`转义,否则在 GPT-2 预分词的正则上会被解析成选择符;(2) **未从 BPE 词表中排除特殊 token**若 `<|im_end|>`不在分割前被剥离, سيتم تفكيك سلسلة أوراقها إلى 8 رموز,模型永远看不到完整结构标记;(3) **`add_special_tokens=False` 漏配**调用 `tokenizer.encode(text)`默认会自动加 BOS/EOS,做拼接时会出现 BOS BOS EOS EOS 序列,破坏注意力面具对齐──修复:编码时显式传 `add_special_tokens=False`، أخيراً من قبل المعلم المنطقي

### نماذج الدردشة

هذا هو المكان الذي يخلط فيه معظم الناس ويتحطم معظم التنفيذات.

> هذا هو المكان الذي يقع فيه معظم الناس في حيرة، كما أن معظمهم ينجحون في الخطأ.

عندما ترسل رسائل إلى نموذج الدردشة، فإن API تقبل قائمة رسائل:

> عندما ترسل رسالة إلى المحادثة، تتلقى API قائمة رسائل:

```
[
  {"role": "system", "content": "You are helpful."},
  {"role": "user", "content": "Hello"},
  {"role": "assistant", "content": "Hi there!"}
]
```

النموذج لا يرى JSON. إنه يرى تسلسل رمز مسطح. قاعدة الدردشة تحويل الرسائل إلى هذا التسلسل المسطح باستخدام رموز خاصة. كل نموذج يفعل هذا بشكل مختلف:

> 模型看不到 JSON──它看到的是一个平的代币序列──聊天模板使用特殊代币将消息转换为平序列──每个模型的做法都不同:

```
Llama 3:
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are helpful.<|eot_id|><|start_header_id|>user<|end_header_id|>

Hello<|eot_id|><|start_header_id|>assistant<|end_header_id|>

Hi there!<|eot_id|>

ChatGPT:
<|im_start|>system
You are helpful.<|im_end|>
<|im_start|>user
Hello<|im_end|>
<|im_start|>assistant
Hi there!<|im_end|>
```

إذا أخطأت في القالب، فإن النموذج ينتج القمامة. تم تدريبها على شكل واحد بالضبط. أي انحراف -- خط جديد مفقود، رمز مبدل، مساحة إضافية -- يضع المدخل خارج توزيع التدريب.

> 模板搞错了模型就会产生垃圾输出──它是在一种精确的形式上训练的──任何偏差缺少换行、交换代币、多一个空格都会使输入偏离训练分布──

> 🤔 **【困惑】**س: لاما 3 لماذا ترك SentencePiece 改用TikToken؟字节级 BPE比原版强在哪? A: 两点关键优势:(1) **SentencePiece 用 ⊗（U+2581）代替空格**، على ASCII 字符和原始空格的混在聊天场景下导致代币序列对快速 微小变化过于敏感; 提克通 直接保留前导空格,"سلام" 和 "سلام" 是不同代币,更稳定;**字节级 BPE 词表恰好 256 个基础 token**، على النظرية يمكن ترميز أي حروف تسلسل ((( بما في ذلك الايموجي、 الحدود الخاصة) ، لا يعتمد على المواد المحددة؛SentencePiece 词表若未训练到某字符直接 [UNK]。Llama 3 词表从 32K 扩至 128K,多语言压缩比提升 ~2x,这是为推理成本买单的工程决策──

### السرعة

بايثون بطيئ جداً لتعريف الإنتاج

> Python 对于生产级分词太慢了──

تكتوكين (OpenAI) مكتوب في Rust مع روابط Python. تكتيكات HuggingFace هي أيضا Rust. SentencePiece هي C ++. هذه تحقق 10-100x سرعة أكثر من Python النقي.

> tiktoken(OpenAI) باستخدام Rust 编写并提供 Python 绑定──HuggingFace tokenizers 也是 Rust──SentencePiece 是 C++──这些比纯 Python 快 10-100 倍──

من وجهة نظر: إضافة 15 تريليون توكن إلى إضافة إضافات للاما 3 إلى 1 مليون توكن في الثانية (بايثون السريع) سيستغرق 174 يومًا. عند 100 مليون توكن في الثانية (رست) ، يستغرق 1.7 يومًا.

> 举例: 速度以每秒100万代币(快速Python) 速度为Llama 3 预训分词 15亿代币 需要174天──以每秒100亿代币(Rust) 速度,只需要1.7天──

أنت تقوم ببناء في Python لفهم الخوارزمية في الإنتاج، كنت تستخدم تنفيذ مرتب وتلمس فقط غلاف Python.

> أنت تستخدم Python لتكوينها لفهم الخوارزميات. في الإنتاج، سوف تستخدم编译实现، فقط تواصل Python 包装器.

## بناء ذلك تحرك لتحقيق
```figure
weight-tying
```

## بناءها

### الخطوة الأولى: تشفير مستوى البايت

أساس. حول أي سلسلة إلى تسلسل من البايت، خريطة كل بايت إلى حرف قابل للطباعة للعرض، وعكس العملية.

> 基础──将任何字符串转换为字节序列,将每个字节映射到可打印字符用于显示,并反转该过程──

```python
def bytes_to_tokens(text):
    return list(text.encode("utf-8"))

def tokens_to_text(token_bytes):
    return bytes(token_bytes).decode("utf-8", errors="replace")
```

اختبار على النص متعدد اللغات لمعرفة عدد البايت:

```python
texts = [
    ("English", "hello"),
    ("Chinese", "你好"),
    ("Emoji", "🔥"),
    ("Mixed", "hello你好🔥"),
]

for label, text in texts:
    b = bytes_to_tokens(text)
    print(f"{label}: {len(text)} chars -> {len(b)} bytes -> {b}")
```

"مرحبا" 5 بايت. "你好" 6 بايت (3 لكل حرف). إموجي النار 4 بايت. الوهم على مستوى البايت لا يهم ما هي اللغة. البايت هي بايت.

> "مرحبا" هو 5 字节──"你好" هو 6 字节── كل حرف 3 字节)──火焰 ايموجي هو 4 字节──字节级分词器不关心它是什么语言──字节就是字节──

### الخطوة الثانية: التوكنيزر المسبق مع Regex

تقسيم النص إلى قطع باستخدام نمط GPT-2 regex. يتم تعريف كل جزء بشكل مستقل من قبل BPE.

> استخدام GPT-2 رسمياً سوف ينفصل النص إلى كتب. كل كتب من قبل BPE 独立分词.

```python
import re

try:
    import regex
    GPT2_PATTERN = regex.compile(
        r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""
    )
except ImportError:
    GPT2_PATTERN = re.compile(
        r"""'(?:[sdmt]|ll|ve|re)| ?[a-zA-Z]+| ?[0-9]+| ?[^\s\w]+|\s+(?!\S)|\s+"""
    )

def pre_tokenize(text):
    return [match.group() for match in GPT2_PATTERN.finditer(text)]
```

- نعم`regex`الدليل يدعم إفلات خاصية Unicode (`\p{L}`للكتب`\p{N}`المكتبة القياسية`re`لم يكن لدينا ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما يصل إلى ما.`regex`. . .

> `regex`模块支持 يونيكود 属性转义(`\p{L}`تعبير حرفي`\p{N}`表示数字) ――                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          `re`模块不支持,所以我们回归 ASCII 字符类──对于生产级多语言分词器,请安装 `regex`.

جربها

```python
print(pre_tokenize("Hello, world! Don't stop."))
# [' Hello', ',', ' world', '!', " Don", "'t", ' stop', '.']
```

يبقى الفضاء الرئيسي مرتبطاً بالكلمة. تقسيم التقلصات عند المخطوطة. تصبح النقطة جزءاً من نفسها. لن يدمج BPE رموز عبر هذه الحدود أبدًا.

> قبل导空格保持在词上.缩写在撇号处分分.标点成为独立块.BPE 永远不会跨这些边界合并代币.

### الخطوة 3: BPE على تسلسلات البايت

الخوارزمية الأساسية من الدروس 01, ولكن الآن تعمل على قطع قبل الـ Tokenized بشكل مستقل.

> الجهاز الأساسي للصف الأول، ولكن الآن يتم التعامل مع الكلمات المحددة بشكل مستقل.

```python
from collections import Counter

def get_byte_pairs(chunks):
    pairs = Counter()
    for chunk in chunks:
        byte_seq = list(chunk.encode("utf-8"))
        for i in range(len(byte_seq) - 1):
            pairs[(byte_seq[i], byte_seq[i + 1])] += 1
    return pairs

def apply_merge(byte_seq, pair, new_id):
    merged = []
    i = 0
    while i < len(byte_seq):
        if i < len(byte_seq) - 1 and byte_seq[i] == pair[0] and byte_seq[i + 1] == pair[1]:
            merged.append(new_id)
            i += 2
        else:
            merged.append(byte_seq[i])
            i += 1
    return merged
```

### الخطوة الرابعة: التعامل مع رموز خاصة

الوهم الخاص يحتاج إلى مطابقة دقيقة وتعرف ثابتة.

> الـ "آي دي" الخاصة 需要精确匹配和固定 ID──它们完全绕过BPE──

```python
class SpecialTokenHandler:
    def __init__(self):
        self.special_tokens = {}
        self.pattern = None

    def add_token(self, token_str, token_id):
        self.special_tokens[token_str] = token_id
        escaped = [re.escape(t) for t in sorted(self.special_tokens.keys(), key=len, reverse=True)]
        self.pattern = re.compile("|".join(escaped))

    def split_with_specials(self, text):
        if not self.pattern:
            return [(text, False)]
        parts = []
        last_end = 0
        for match in self.pattern.finditer(text):
            if match.start() > last_end:
                parts.append((text[last_end:match.start()], False))
            parts.append((match.group(), True))
            last_end = match.end()
        if last_end < len(text):
            parts.append((text[last_end:], False))
        return parts
```

### الخطوة 5: فئة Tokenizer كاملة

قم بتجميع كل شيء: تعاديل، تقسيم على رموز خاصة، تحديد قبل، دمج BPE، خريطة إلى هويات.

> 将所有步骤串联:归一化、按特殊代币 分割、预分词、BPE 合并、映射到ID──

```python
import unicodedata

class ProductionTokenizer:
    def __init__(self):
        self.merges = {}
        self.vocab = {i: bytes([i]) for i in range(256)}
        self.special_handler = SpecialTokenHandler()
        self.next_id = 256

    def normalize(self, text):
        return unicodedata.normalize("NFKC", text)

    def train(self, text, num_merges):
        text = self.normalize(text)
        chunks = pre_tokenize(text)
        chunk_bytes = [list(chunk.encode("utf-8")) for chunk in chunks]

        for i in range(num_merges):
            pairs = Counter()
            for seq in chunk_bytes:
                for j in range(len(seq) - 1):
                    pairs[(seq[j], seq[j + 1])] += 1
            if not pairs:
                break
            best = max(pairs, key=pairs.get)
            new_id = self.next_id
            self.next_id += 1
            self.merges[best] = new_id
            self.vocab[new_id] = self.vocab[best[0]] + self.vocab[best[1]]
            chunk_bytes = [apply_merge(seq, best, new_id) for seq in chunk_bytes]

    def add_special_token(self, token_str):
        token_id = self.next_id
        self.next_id += 1
        self.special_handler.add_token(token_str, token_id)
        self.vocab[token_id] = token_str.encode("utf-8")
        return token_id

    def encode(self, text):
        text = self.normalize(text)
        parts = self.special_handler.split_with_specials(text)
        all_ids = []
        for part_text, is_special in parts:
            if is_special:
                all_ids.append(self.special_handler.special_tokens[part_text])
            else:
                for chunk in pre_tokenize(part_text):
                    byte_seq = list(chunk.encode("utf-8"))
                    for pair, new_id in self.merges.items():
                        byte_seq = apply_merge(byte_seq, pair, new_id)
                    all_ids.extend(byte_seq)
        return all_ids

    def decode(self, ids):
        byte_parts = []
        for token_id in ids:
            if token_id in self.vocab:
                byte_parts.append(self.vocab[token_id])
        return b"".join(byte_parts).decode("utf-8", errors="replace")

    def vocab_size(self):
        return len(self.vocab)
```

### الخطوة 6: اختبار متعددة اللغات

الاختبار الحقيقي، ألق الإنجليزية والصينية والإيموجي و الرمز عليه

> الاختبار الحقيقي.

```python
corpus = (
    "The quick brown fox jumps over the lazy dog. "
    "The quick brown fox runs through the forest. "
    "Machine learning models process natural language. "
    "Deep learning transforms how we build software. "
    "def train(model, data): return model.fit(data) "
    "def predict(model, x): return model(x) "
)

tok = ProductionTokenizer()
tok.train(corpus, num_merges=50)

bos = tok.add_special_token("<|begin|>")
eos = tok.add_special_token("<|end|>")

test_texts = [
    "The quick brown fox.",
    "你好世界",
    "Hello 🌍 World",
    "def foo(x): return x + 1",
    f"<|begin|>Hello<|end|>",
]

for text in test_texts:
    ids = tok.encode(text)
    decoded = tok.decode(ids)
    print(f"Input:   {text}")
    print(f"Tokens:  {len(ids)} ids")
    print(f"Decoded: {decoded}")
    print()
```

الكلمات الصينية تنتج 3 بايت لكل واحد. الايموجي ينتج 4 بايت. لا احد منهم يضرب الوهم. لا احد ينتج رموز مجهولة. هذا هو قوة BPE على مستوى البايت.

> 中文字符每个产生 3 字节──emoji 产生 4 字节──这些都不会使分词器崩──都不会产生未知代币──这是字节级BPE的力量──

> **【中文解读】**أعلاه الكود سوف يرتبط جميع المكونات:归一化 → 特殊代币 分割 → 预分词 → BPE 合并 → ID 映射──测试覆盖英文、中文、eMoji、代码和特殊代币的混合场景──字节级 BPE ضمان عدم وجود أي إدخال لإنتاج رمز غير معروف هذا هو السبب الأساسي لتصبح المعيار الصناعي‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬

> **【拓展：分词速度的工程意义】**純 Python 分词器每秒处理大约1M tokens,Llama 3 的预训语料有15亿亿代币, باستخدام Python 需要174天──tiktoken(Rust 实现) في كل ثانية 100M代币,只需要1.7天──这就是为什么生产级分词器都用编译语言:tiktoken 用Rust,HuggingFace Tokenizers 用Rust,SentencePiece 用C++──

## استخدمها في إطار التنفيذ

### مقارنة المشاركات الحقيقية

قم بتحميل الرموز الفعلية من Llama 3، GPT-4، و Mistral. انظر كيفية كل منهما التعامل مع نفس الفقرة متعددة اللغات.

> 加载 Llama 3、GPT-4 和 Mistral 的实际分词器──看看每个分词器如何处理同一段多语言文本──

```python
import tiktoken

gpt4_enc = tiktoken.get_encoding("cl100k_base")

test_paragraph = "Machine learning is powerful. 机器学习很强大。 L'apprentissage automatique est puissant. 🤖💪"

tokens = gpt4_enc.encode(test_paragraph)
pieces = [gpt4_enc.decode([t]) for t in tokens]
print(f"GPT-4 ({len(tokens)} tokens): {pieces}")
```

```python
from transformers import AutoTokenizer

llama_tok = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")
mistral_tok = AutoTokenizer.from_pretrained("mistralai/Mistral-7B-v0.1")

for name, tok in [("Llama 3", llama_tok), ("Mistral", mistral_tok)]:
    tokens = tok.encode(test_paragraph)
    pieces = tok.convert_ids_to_tokens(tokens)
    print(f"{name} ({len(tokens)} tokens): {pieces[:20]}...")
```

سترى حسابات رمزية مختلفة لنفس النص. Llama 3 مع ذخيرة 128K أكثر عدوانية في دمج الأنماط المشتركة. GPT-4 مع 100K يجلس في الوسط. Mistral مع 32K ينتج المزيد من الرموز ولكن لديها طبقة تضمين أصغر.

> سترى نفس النص مختلفة من الرمز عددها. سترى 128K من علامة 3                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         

التنازل هو دائما نفس الشيء: المفردات الكبيرة تعني تسلسلات أقصر ولكن معايير أكثر.

> الوزن هو دائما نفسها: الكلمات الأكبر تعني سلسلة أقصر ولكن المزيد من العناصر.

## أرسلها .

هذه الدروس تنتج طلب لبناء وتحريف أجهزة إضفاء الضبط الإنتاجية. انظر `outputs/prompt-tokenizer-builder.md`. . .

> هذا المنتج مصدر للتصميم والتحقيق في تصنيف وتربية الجهاز.`outputs/prompt-tokenizer-builder.md`.

## تمارين التدريب

1. **Easy:**إضافة`get_token_bytes(id)`طريقة تظهر البايتات الخام لأي رمز هويت. استخدمها للتحقق من ما تمثل أهم رموز دمجك في الواقع.
   中文翻译:添加 `get_token_bytes(id)`方法,显示任意 token ID 的原始字节──用它检查您最常用的合并代币 实际代表什么──
2. **Medium:**تنفيذ المُقبل للتوكينيزير على طراز Llama الذي ينقسم على الفضاء الأبيض والأرقام لكنه يحتفظ بالفراغات الرائدة. مقارنة ذخيره المفرد مع نهج GPT-2 regex على نفس الجسم.
   中文翻译:实现 Llama 风格的预分词器,按空格和数字分分但保留前导空格──在相同语料上比较其词表与GPT-2 正则方法──
3. **Hard:**إضافة طريقة نموذج دردشة تأخذ قائمة `{"role": ..., "content": ...}`رسائل وتنتج تسلسل رمزية صحيحة لنموذج دردشة Llama 3. اختبرها مع تنفيذ HuggingFace.
   中文翻译:添加聊天模板方法,接受 `{"role": ..., "content": ...}`消息列表并生成 Llama 3 聊天格式的正确代币序列──对照 HuggingFace 实现进行测试──

## شروط الرئيسية

| Term | What people say | What it actually means | 中文释义 |
|------|----------------|----------------------|---------|
| Byte-level BPE | "Tokenizer that works on bytes" | BPE with a base vocabulary of 256 byte values -- handles any input without unknown tokens | 字节级 BPE，基础词表 256 个字节值 |
| Pre-tokenization | "Splitting before BPE" | Regex or rule-based splitting that prevents BPE from merging across word boundaries | 预分词，防止跨词边界的 token 合并 |
| NFKC normalization | "Unicode cleanup" | Canonical decomposition followed by compatibility composition -- "fi" ligature becomes "fi", fullwidth "A" becomes "A" | NFKC 归一化，统一 Unicode 表示 |
| Chat template | "How messages become tokens" | The exact format for converting a list of role/content messages into a flat token sequence -- model-specific and must match training format | 聊天模板，消息转 token 的格式规则 |
| Special tokens | "Control tokens" | Reserved token IDs that bypass BPE -- [BOS], [EOS], [PAD], chat markers -- matched exactly before merge | 特殊 token，绕过 BPE 的控制标记 |
| Fertility | "Tokens per word" | Ratio of output tokens to input words -- 1.3 for English in GPT-4, 2-3 for Korean, higher means wasted context | 生育率，每词 token 数 |
| tiktoken | "OpenAI tokenizer" | Rust BPE implementation with Python bindings -- 10-100x faster than pure Python | OpenAI 的 Rust 分词器实现 |
| Merge table | "The vocabulary" | Ordered list of byte-pair merges learned during training -- this IS the tokenizer's learned knowledge | 合并表，分词器的核心知识 |

## المزيد من القراءة

- [OpenAI tiktoken source](https://github.com/openai/tiktoken)-- تنفيذ BPE الخرسانة المستخدمة من قبل GPT-3.5/4
- [HuggingFace tokenizers](https://github.com/huggingface/tokenizers)-- مكتبة الرست توكنيزر التي تدعم BPE، WordPiece، Unigram
- [Llama 3 paper (Meta, 2024)](https://arxiv.org/abs/2407.21783)-- تفاصيل حول 128K المفردات والتدريب على الوسائط
- [SentencePiece (Kudo & Richardson, 2018)](https://arxiv.org/abs/1808.06226)-- التوضيح اللغوي
- [GPT-2 tokenizer source](https://github.com/openai/gpt-2/blob/master/src/encoder.py)-- الخرائط الأصلية من البايت إلى اليونيكود
