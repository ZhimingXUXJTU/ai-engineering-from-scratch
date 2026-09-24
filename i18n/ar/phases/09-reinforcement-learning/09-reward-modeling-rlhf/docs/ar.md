# تمويل النموذجية & RLHF  تمويل تمويل النموذجية مع RLHF

> لا يمكن للبشر كتابة وظيفة مكافأة لـ "استجابة مساعد جيدة"، ولكن يمكنهم مقارنة ردود فعل اثنين واختيار أفضل. تناسب نموذج مكافأة لتلك المقارنات، ثم RL نموذج اللغة ضد ذلك. كريستيانو 2017.

> **【中文解读】**الناس لا يستطيعون كتابة وظيفة مكافأة "المساعد الجيد للردّ"، ولكن يمكن مقارنة اثنين من المكافآت بشكل أفضل.

> **【拓展：RLHF 是大模型对齐的关键】**RLHF(بناء على البشر反的强化学习) هو ChatGPT 成功的核心技术──三步流程:(1) 监督微调 SFT;(2) 训练奖励模型 RM;(3) 用PPO 优化 LM──DPO 简化第 2-3步,但本质相同──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 5 · 05 (Sentiment), Phase 9 · 08 (PPO) | **前置知识:** Phase 5 · 05 (情感分析), Phase 9 · 08 (PPO)
**Time:** ~45 minutes | **时间:** ~45 分钟

## المشكلة المشكلة المشكلة

لقد تدربت نموذج لغة على هدف التنبؤ التالي. يكتب اللغة الإنجليزية الجهامية. كما يكذب ويتجول ويرفض الرفض. لا يمكنك إصلاح هذا مع المزيد من التدريب.

> أنت في التوقيت التالي  التنبؤ الهدف تم تدريب نموذج اللغة ‬ . إنها تكتب لغة صحيحة من الانجليزية‬ . ولكن أيضا تكذب ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬

تريد مكافأة * مقياسية* تقول "الرد A أفضل من الرد B للتعليمات X". كتابة وظيفة مكافأة يدويا مستحيل. "المساعدة" ليست تعبيرًا مغلقًا على الرموز. ولكن البشر يمكنهم مقارنة نتائج اثنين وتحديد تفضيل. وهذا رخيص لجمعها على مقياس.

> أنت تريد مكافأة معينة، تعبر عن "للمواصفات X، رد A على B أفضل"...... كتابة هذه وظيفة مكافأة هي مستحيلة.

RLHF (Christiano et al. 2017; Ouyang et al. 2022) تحويل التفضيلات إلى نموذج مكافأة ، ثم تحسين LM عن طريق PPO ضد هذه المكافأة. في ثلاث خطوات: SFT → RM → PPO. إنها وصفة شحن ChatGPT ، كلود ، جيميني ، وجميع التوافقات الأخرى-LLM في 20232025.

> سيتم تحويل RLHF إلى نموذج مكافأة، ثم يتم تحسينها من خلال PPO على LM.

في عام 2026 يتم استبدال خطوة PPO معظمها ب DPO (المرحلة 10 · 08) لأنه أرخص وأكثر فائدة تقريباً للتحديد التوالي. ولكن قطعة * نموذج الجائزة * لا تزال تتمثل في كل عينة أفضل من N ، وكل خط أنبوب RL-من-المكافآت المتحققة ، وكل نموذج التفكير باستخدام نموذج مكافأة العملية. فهم RLHF وفهم كومة التوالي بأكملها.

> 2026 عام PPO 步骤大多被DPO 替换,因为更便宜且对齐效果几乎相同. ولكن * نموذج الجوائز* لا يزال أفضل من N 采样器、可验证奖励 RL 管道和过程奖励模型的基础── فهم RLHF على فهم كل التكنولوجيا ──

> **【中文解读】**RLHF 三阶段流程:(1) SFT على البيانات البشرية للإشراف على النموذج الأساسي؛(2) RM باستخدام التحيز البشري على التدريب برادلي-تيري 奖励模型؛(3) PPO باستخدام نموذج الحظوظ للإشارة تحسين لغة النموذج، في الوقت نفسه KL 惩罚 prevent deviation from SFT 太远── على الرغم من أن 2026 步骤多 PPO 已被 DPO 替代, ولكن نموذج الحظوظ لا يزال في أفضل من N 采样、可验证奖励 RL、 عملية ماڊل الحظوظ في مثل هذه المشهد.

> **【拓展：DPO 与 RLHF 的对比】**دبو ((التحسين المفضل المباشر) سوف RM+PPO RLHF 两步合并为一步 مباشرة من التحضيرية على استراتيجية التدريب، لا حاجة إلى نموذج مكافأة التدريب واضحة.

## المفهوم الأساسي

![Three-stage RLHF: SFT, RM training on pairwise prefs, PPO with KL penalty](../assets/rlhf.svg)

**Stage 1: Supervised Fine-Tuning (SFT).**البدء من نموذج أساسي مدرب مسبقًا. تحسين التوضيحات المكتوبة من قبل الإنسان لسلوك الهدف (ردود تتابع التعليمات، الردود المفيدة، إلخ). النتيجة: نموذج `π_SFT`التي * تحيز نحو السلوك الجيد * ولكن لا يزال لها مساحة عمل غير محدودة.

> **阶段 1：监督微调（SFT）。**من قبل التدريب الأساسي النموذج بدأ. في إظهار السلوك الهدف من كتابة البشر. النتيجة: نموذج * متجه نحو السلوك الجيد * ولكن لا يزال هناك حدوث غير محدود.`π_SFT`.

**Stage 2: Reward Model training.**

- جمع أزواج من الردود `(y_+, y_-)`إلى الإشارات`x`، يسميها البشر "y_+ تفضل على y_-. "
- تدريب نموذج مكافأة `R_φ(x, y)`لتحديد درجات أعلى ل`y_+`. . .
- الخسارة:**Bradley-Terry pairwise logistic**:

  `L(φ) = -E[ log σ(R_φ(x, y_+) - R_φ(x, y_-)) ]`

  σ هو sigmoid. الفرق في المكافأة يعني إيقاع الاختيارات التميزية. كانت BT هي القاعدة منذ عام 1952 (برادلي-تيري) وهي الخيار المهيمن في RLHF الحديث.

- `R_φ`عادة ما يتم تشغيلها من نموذج SFT مع رأس سكالي على الأعلى. نفس العمود الفقري للمتحول؛ طبقة خطية واحدة تنطلق الجائزة.

> **阶段 2：奖励模型训练。**جمع التأثيرات البشرية على التأثيرات البشرية`(y_+, y_-)`، تدريب مكافأة نموذج إعطاء`y_+`"أوّل شيء، فقدان" برادلي تيري "في العودة المنطقية"`R_φ`عادة من SFT 模型初始化، إضافة حجم نموذج الناتج.

**Stage 3: PPO against the RM with KL penalty.**

- إطلاق سياسة التدريب`π_θ`من`π_SFT`. إبقَ مرجعًا مُجمدًا`π_ref = π_SFT`. . .
- مكافأة في نهاية الإجابة`y`:

  `r_total(x, y) = R_φ(x, y) - β · KL(π_θ(·|x) || π_ref(·|x))`

  عقوبة ك.إل تمنع`π_θ`من التجول تعسفيًا من`π_SFT` هو * تنظيمي *، وليس منطقة ثقة صعبة. `β`عادةً`0.01`-أجل`0.05`. . .
- تشغيل PPO (دروس 08) مع هذه المكافأة. يتم حساب المزايا على مسار مستوى الرمز، ولكن RM تسجل فقط الاستجابة الكاملة.

> **阶段 3：对 RM 做 PPO + KL 惩罚。**من`π_SFT`ابتداريات تدريب استراتيجية. مكافأة = RM 分数 - β × KL إلى الاستشارة استراتيجية.

**Why the KL?**بدونها، سوف يجد PPO بكل سرور استراتيجيات اختراق المكافآت  تم تدريب RM فقط على الانتهاءات في التوزيع. قد يحصل استجابة خارج التوزيع على درجة أعلى من أي من كتب البشر.`π_θ`بالقرب من المجموعة حيث تم تدريب RM.

> **为什么需要 KL？**بدونها، ستجد البيانات المنتشرة في البيانات الموزعة.`π_θ`保持在RM 训练的流形附近──这是 RLHF أهم旋──

**2026 status:**

- **DPO**(رافائيلوف 2023): الهجرة المغلقة تسقط المرحلة 2 + 3 إلى خسارة واحدة تحت الإشراف على بيانات الاختيارات. لا RM، لا PPO. نفس الجودة على معايير التنظيم لجزء من الحساب. تغطية في المرحلة 10 · 08.
- **GRPO**(DeepSeek 20242025): PPO مع خط أساسي مرتبط بالجماعة بدلاً من النقاد، مكافأة من *verifier* (مشاركات الرمز / مطابقات الإجابات الرياضية) بدلاً من RM المدربة من قبل البشر. غالب على نماذج التفكير. تغطية في المرحلة 9 · 12.
- **Process reward models (PRMs):**حلول جزئية (كل خطوة من الحجج) تستخدم في كل من فترات RLHF و GRPO للتحقيق.
- **Constitutional AI / RLAIF:**استخدام القانون القانوني المتماشى لتوليد التفضيلات بدلا من البشر.

> **2026 年状态：**DPO 将阶段 2+3 折叠为单一监督损失──GRPO 用组相对基线替代评论,用验证器替代人类训练的 RM──PRM 评分部分解决方案──宪法 AI / RLAIF 用对齐的 LLM 生成偏好──

## بناء ذلك تحرك لتحقيق
```figure
reward-model
```

## بناءها

تستخدم هذه الدروس "التسجيلات" وال"ردود" الصناعية الصغيرة الممثلة على أنها سلسلة. RM هو مستحق رصيد خطي على تمثيل حقيبة من الرموز. لا يوجد LLM حقيقي  * شكل * من خط الأنابيب يهم ، وليس المقياس. انظر `code/main.py`. . .

> هذا المرحلة تستخدم صيغة صغيرة "تلميح" و"إعادة" مركبة.

### الخطوة الأولى: بيانات تفضيل صناعية

```python
PROMPTS = ["help me", "answer me", "explain this"]
GOOD_WORDS = {"clear", "specific", "kind", "thorough"}
BAD_WORDS = {"vague", "rude", "wrong", "short"}

def make_pair(rng):
    x = rng.choice(PROMPTS)
    y_good = rng.choice(list(GOOD_WORDS)) + " " + rng.choice(list(GOOD_WORDS))
    y_bad = rng.choice(list(BAD_WORDS)) + " " + rng.choice(list(BAD_WORDS))
    return (x, y_good, y_bad)
```

في RLHF الحقيقي يتم استبدال هذا بالعلامات البشرية.`(prompt, preferred_response, rejected_response)` هو نفس الشيء

> حقيقة RLHF 中由人类标注者替代──形状`(提示, 偏好回复, 拒绝回复)`تماماً نفسها

### الخطوة الثانية: نموذج مكافأة برادلي تيري

النتيجة الخطية: `R(x, y) = w · bag(y)`. التدريب لتقليل خسارة التسجيلات بالتزامن مع التسجيلات

```python
def rm_train_step(w, x, y_pos, y_neg, lr):
    r_pos = dot(w, bag(y_pos))
    r_neg = dot(w, bag(y_neg))
    p = sigmoid(r_pos - r_neg)
    for tok, cnt in bag(y_pos).items():
        w[tok] += lr * (1 - p) * cnt
    for tok, cnt in bag(y_neg).items():
        w[tok] -= lr * (1 - p) * cnt
```

بعد بضع مئات من التحديثات`w`يُعطي الوزن الإيجابي لرمز الكلمات الجيدة والسلبي للسيئ.

> بعد عدة مئات من التحديثات`w`أعطني رمز كلمة جيدة، ووزن كلمة سيئة، ووزن كلمة سيئة

### الخطوة الثالثة: سياسة تشبه PPO فوق RM

سياسة ألعابنا تنتج رمز واحد من المفردات`log π_θ(token | prompt)`، إضافة عقوبة KL إلى المرجع، وتطبيق قطع PPO بديل.

> استراتيجية ألعابنا هي أن تكون رمز واحد من خلال كلمة واحدة.`log π_θ(token | prompt)`إضافة KL إلى الإشارة إلى استراتيجية العقاب، وتطبيق قصة PPO 代理

```python
def rlhf_step(theta, ref, w, prompt, rng, eps=0.2, beta=0.1, lr=0.05):
    logits_theta = policy_logits(theta, prompt)
    probs = softmax(logits_theta)
    token = sample(probs, rng)
    logits_ref = policy_logits(ref, prompt)
    probs_ref = softmax(logits_ref)
    reward = dot(w, bag([token])) - beta * kl(probs, probs_ref)
    # ppo-style update on theta, treating reward as the return
    ...
```

> 关键:奖励 = RM 分数 - β × KL(π_θ 1920 π_ref) ――β هو التحكم في استراتيجية漂移程度的关键超参数太大策略几乎不变,太小则奖励黑客开始──

### الخطوة الرابعة: مراقبة الممر

متوسط المسار`KL(π_θ || π_ref)`كل تحديث، إذا كان يمر`~5-10`السياسة قد انحرفت بعيدا عن`π_SFT` أقل `β`هذا هو التشخيص الأعلى في RLHF الحقيقي.

> كل تحديث يتبع متوسط`KL(π_θ || π_ref)`إذا تجاوزت `~5-10`, الاستراتيجية قد ذهبت بعيدا`π_SFT`可能 β 正在降低或奖励黑客正在开始──这是真正的RLHF中最重要的诊断──

### الخطوة 5: وصفة الإنتاج مع TRL

بمجرد أن تفهم خط أنابيب الألعاب، هنا نفس الحلقة التي يكتبه مستخدم مكتبة حقيقية.[TRL](https://huggingface.co/docs/trl)هو تنفيذ المرجعية  `RewardTrainer`للمرحلة 2 و `PPOTrainer`(مع جهاز KL-to-reference مدمج) للمرحلة الثالثة.

> بمجرد فهمك لعبة تدفق الماء، هنا هو المستخدم الحقيقي كتابة نفس الدورة الطريقة.`RewardTrainer`, المرحلة 3`PPOTrainer`.

```python
# Stage 2: reward model from pairwise preferences
from trl import RewardTrainer, RewardConfig
from transformers import AutoModelForSequenceClassification, AutoTokenizer

tok = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
rm = AutoModelForSequenceClassification.from_pretrained(
    "meta-llama/Llama-3.1-8B-Instruct", num_labels=1
)

# dataset rows: {"prompt", "chosen", "rejected"} — Bradley-Terry format
trainer = RewardTrainer(
    model=rm,
    tokenizer=tok,
    train_dataset=preference_data,
    args=RewardConfig(output_dir="./rm", num_train_epochs=1, learning_rate=1e-5),
)
trainer.train()
```

```python
# Stage 3: PPO against the RM with KL penalty to the SFT reference
from trl import PPOTrainer, PPOConfig, AutoModelForCausalLMWithValueHead

policy = AutoModelForCausalLMWithValueHead.from_pretrained("./sft-checkpoint")
ref    = AutoModelForCausalLMWithValueHead.from_pretrained("./sft-checkpoint")  # frozen

ppo = PPOTrainer(
    config=PPOConfig(learning_rate=1.41e-5, batch_size=64, init_kl_coef=0.05,
                     target_kl=6.0, adap_kl_ctrl=True),
    model=policy, ref_model=ref, tokenizer=tok,
)

for batch in dataloader:
    responses = ppo.generate(batch["query_ids"], max_new_tokens=128)
    rewards   = rm(torch.cat([batch["query_ids"], responses], dim=-1)).logits[:, 0]
    stats     = ppo.step(batch["query_ids"], responses, rewards)
    # stats includes: mean_kl, clip_frac, value_loss — the three PPO diagnostics
```

ثلاثة أشياء تقوم بها المكتبة من أجلك`adap_kl_ctrl=True`تنفيذ جدول التكيف-β: إذا تجاوز KL الملاحظ `target_kl`النموذج المرجعي يتم تجميده بالاتفاقية  لا يجب أن تشارك المعلمات مع `policy`و رأس القيمة يعيش على نفس العمود الفقري`AutoModelForCausalLMWithValueHead`يرفق رأس MLP (MLP) ، ولهذا السبب تقرير TRL `policy/kl`و`value/loss`بشكل منفصل

> هناك ثلاثة أشياء يجب عليك القيام بها`adap_kl_ctrl=True`实现自适应 β 调度: إذا كان KL 超过 الهدف 则 β 翻倍, إذا كان أقل من نصف 则 β 减半.

## الفخاخ

- **Over-optimization / reward hacking.**الـ (مـ) غير كاملة`π_θ`العلامات: الافضل يرتفع إلى أجل غير مسمى بينما تقدم البشر تقييم مستطيلات أو انخفاض.`β`، وتوسيع بيانات تدريب RM.
  **过度优化/奖励黑客。**RM غير كاملة`π_θ`العلامات: الارتفاع المستمر في الارتفاع، ولكن معدلات التدريب البشري تتوقف أو تنخفض.
- **Length hacking.**غالباً ما يتم تكافؤ المعلمين المهنيين على الاستجابات المفيدة بشكل ضمني. تتعلم السياسة كيفية تعبئة الاستجابات. التعويض: مكافأة طبيعية على طول، أو RLAIF مع RM واعية على طول.
  **长度黑客。**في التدريب المفيد على التدريب RM 常隐式奖励长度──策略学会填充回复──缓解:长度归归化奖励或长度感知 RM──
- **Too-small RM.**يجب أن يكون الرقم الكبير على الأقل مثل السياسة، ولا يمكن لـ RM الصغير أن يحصل على نتائج سياسة
  **RM 太小。**RM على الأقل يجب أن تكون كبيرة مثل استراتيجية.
- **KL tuning.**انخفاض β → التجريد والكافأة القرصنة. انخفاض β → السياسة بالكاد يتغير. الخدعة القياسية هي * التكيف * β التي تهدف إلى KL ثابتة في كل خطوة.
  **KL 调优。**β 太低→漂移和奖励黑客──β 太高→ استراتيجية تقريبا لا تتغير──标准技巧是*自适应* β 目标为固定 KL──
- **Preference-data noise.**~ 30% من اللوحات البشرية ضوضاء أو غامضة. قم بتعليم RM على بيانات مرشحة بالاتفاق أو استخدم درجة حرارة على BT.
  **偏好数据噪声。**حوالي 30% من علامات الإنسان لديها ضجيج أو غامض.
- **Off-policy problems.**بيانات PPO غير سياسية قليلا بعد العصر الأول.
  **离策略问题。**بيانات PPO في العصر الأول 后略离策略──像课08 那样监控裁剪比例──

## استخدمها في إطار التنفيذ

RLHF في عام 2026 هو طبقات:

> فترة الـ 2026 من المرحلة الـ RLHF هي:

| Layer | Target | Method |
|-------|--------|--------|
| Layer / 层级 | Target / 目标 | Method / 方法 |
| Instruction following, helpfulness, harmlessness / 指令遵循、有用性、无害性 | Alignment / 对齐 | DPO (Phase 10 · 08) preferred over RLHF-PPO. |
| Reasoning correctness (math, code) / 推理正确性（数学、代码） | Capability / 能力 | GRPO with verifier reward (Phase 9 · 12). |
| Long-horizon multi-step tasks / 长视野多步任务 | Agentic / 代理 | PPO / GRPO with process reward models over steps. |
| Safety / refusal behavior / 安全/拒绝行为 | Safety / 安全 | RLHF-PPO with separate safety RM, or Constitutional AI. |
| Best-of-N at inference / 推理时 Best-of-N | Fast alignment / 快速对齐 | Use RM at decode time; no policy training needed. |
| Reward distillation / 奖励蒸馏 | Inference compute / 推理计算 | Train a small "reward head" on top of a frozen LM. |

كان RLHF * الطريقة * في 20222024. في عام 2026 ، يتم استخدام خطوط أنابيب التنظيم الإنتاج DPO- أولاً ، PPO- فقط للخطوات المكثفة في RM أو الحرجة في السلامة.

> في عام 2022-2024، فإن إنتاج خطوط المياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة بالمياه المزودة والمتعة بالمياه المزودة بالمياه المزودة بالمياه المتصورة.

## أرسلها .

إبقوا`outputs/skill-rlhf-architect.md`:

```markdown
---
name: rlhf-architect
description: Design an RLHF / DPO / GRPO alignment pipeline for a language model, including RM, KL, and data strategy.
version: 1.0.0
phase: 9
lesson: 9
tags: [rl, rlhf, alignment, llm]
---

Given a base LM, a target behavior (alignment / reasoning / refusal / agent), and a preference or verifier budget, output:

1. Stage. SFT? RM? DPO? GRPO? With justification.
2. Preference or verifier source. Humans, AI feedback, rule-based, unit-test-pass, or reward distillation.
3. KL strategy. Fixed β, adaptive β, or DPO (implicit KL).
4. Diagnostics. Mean KL, reward stability, over-optimization guard (holdout human eval).
5. Safety gate. Red-team set, refusal rate, safety RM separate from helpfulness RM.

Refuse to ship RLHF-PPO without a KL monitor. Refuse to use an RM smaller than the target policy. Refuse length-only rewards. Flag any pipeline that does not hold back a blind human-eval set as lacking over-optimization protection.
```

## تمارين التدريب

1. **Easy.**تدريب نموذج مكافأة برادلي تيري في`code/main.py`على 500 زوج من الأزواج المفضلة الاصطناعية. قياس دقة الأزواج على 100 زوج من الأزواج المحتملة. يجب أن يتجاوز 90%.
2. **Medium.**إشغال حلقة لعبة PPO-RLHF مع `β ∈ {0.0, 0.1, 1.0}`لكل منهما، قم بتحديد النتيجة المقدمة مقابل النتيجة المرجعية من خلال التحديثات
3. **Hard.**تنفيذ DPO (خسارة احتمالية تفضيل الشكل المغلق) على نفس البيانات المفضلة ومقارنة مع خط أنابيب RLHF-PPO في الحساب المستخدم والنتيجة النهائية RM التي تم تحقيقها.

## شروط الرئيسية

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| RLHF | "Alignment RL" | Three-stage SFT + RM + PPO pipeline (Christiano 2017, Ouyang 2022). |
| Reward Model (RM) | "The scoring net" | Learned scalar function fit to pairwise preferences via Bradley-Terry. |
| Bradley-Terry | "Pairwise logistic loss" | `P(y_+ ≻ y_-) = σ(R(y_+) - R(y_-))`; the standard RM objective. |
| KL penalty | "Stay near the reference" | `β · KL(π_θ \|\| π_ref)` in the reward; the anti-reward-hacking regularizer. |
| Reward hacking | "Goodhart's law" | Policy exploits RM flaws; symptoms: reward up, human eval flat. |
| RLAIF | "AI-labeled preferences" | RLHF where labels come from another LM instead of humans. |
| PRM | "Process Reward Model" | Scores partial reasoning steps; used in reasoning pipelines. |
| Constitutional AI | "Anthropic's method" | AI-generated preferences guided by explicit rules. |

## المزيد من القراءة

- [Christiano et al. (2017). Deep Reinforcement Learning from Human Preferences](https://arxiv.org/abs/1706.03741)- الصحيفة التي بدأت "الـ"ر"هـف
- [Ouyang et al. (2022). InstructGPT — Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) وصفة خلف ChatGPT.
- [Stiennon et al. (2020). Learning to summarize with human feedback](https://arxiv.org/abs/2009.01325) قبل الـ RLHF للاختصار.
- [Rafailov et al. (2023). Direct Preference Optimization](https://arxiv.org/abs/2305.18290) DPO؛ الاختلالات بعد RLHF في عام 2026.
- [Bai et al. (2022). Constitutional AI: Harmlessness from AI Feedback](https://arxiv.org/abs/2212.08073) RLAIF و حلقة النقد الذاتي.
- [Anthropic RLHF paper (Bai et al. 2022). Training a Helpful and Harmless Assistant](https://arxiv.org/abs/2204.05862)ورقة "إتش.إتش".
- [Hugging Face TRL library](https://huggingface.co/docs/trl) الإنتاج `RewardTrainer`و`PPOTrainer`. اقرأ مصدر المدرب لتفاصيل التكيفية-KL و القيمة رأس.
- [Hugging Face — Illustrating Reinforcement Learning from Human Feedback](https://huggingface.co/blog/rlhf)من قبل لامبرت، كاستريكاتو، فون وررا، هافريلا  المشي القنوني من خلال خط الأنابيب الثلاث المراحل مع الرسومات.
- [von Werra et al. (2020). TRL: Transformer Reinforcement Learning](https://github.com/huggingface/trl)المكتبة`examples/`لديه نصوص RLHF من نهاية إلى نهاية للاما، ميسرال، و Qwen.
- [Sutton & Barto (2018). Ch. 17.4 — Designing Reward Signals](http://incompleteideas.net/book/RLbook2020.pdf) وجهة نظر فرضية المكافأة؛ شرط أساسي للتفكير في اختراق المكافأة.
