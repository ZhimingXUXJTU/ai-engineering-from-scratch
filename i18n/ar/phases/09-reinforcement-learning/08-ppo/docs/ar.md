# تحسين السياسة القريبة (PPO)  تحسين استراتيجية النهاية

> يرمي A2C كل عملية تنفيذ بعد تحديث واحد. يلف PPO تراجع السياسة في نسبة أهمية خفضة حتى تتمكن من القيام بأكثر من 10 حقائق على نفس البيانات دون انفجار السياسة. Schulman et al. (2017). لا يزال الخوارزمية الافتراضية للسياسة-الترقي في عام 2026.

> **【中文解读】**استخدام PPO لقطع النسبة الأهمية لفئة الاستراتيجية، مما يجعل نفس البيانات يمكن القيام به 10 + دورات تحديث بينما الاستراتيجية لن تنفجر.

> **【拓展：PPO 与 ChatGPT】**PPO هو الخوارزمية الأساسية لتدريب ChatGPT RLHF.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic) | **前置知识:** Phase 9 · 06 (REINFORCE), Phase 9 · 07 (Actor-Critic)
**Time:** ~75 minutes | **时间:** ~75 分钟

## المشكلة المشكلة المشكلة

A2C (دروس 07) على السياسة: التراجع `E_{π_θ}[A · ∇ log π_θ]`يتطلب البيانات التي تم أخذها من *التيار* `π_θ`خذ تحديث واحد، و`π_θ`تغيرات، البيانات التي استخدمتها غير قانونية الآن إعادة استخدامها و تغير التحديد

> A2C ((المدرس 07) في خط استراتيجيات:梯度 `E_{π_θ}[A · ∇ log π_θ]`要求从*当前* `π_θ`采样数据──一次更新后 `π_θ`تغيير؛ البيانات التي استخدمتها أصبحت خارج الاستراتيجية.

التشغيل مكلف. على Atari، التشغيل واحد عبر 8 envs × 128 خطوات = 1024 انتقالات وعشرة ثوان من الوقت البيئي. إلقاء ذلك بعيدا بعد خطوة تراجع واحدة هو مضيعة.

> التنفيذ مكلف جدا. في Atari، 8 بيئة × 128 خطوة = 1024 مرة تحويل و 10 ثواني من الوقت المحيطي.

كان تحسين سياسة منطقة الثقة (TRPO ، Schulman 2015) هو التحدي الأول: تقييد كل تحديث بحيث يبقى اختلاف KL بين السياسة القديمة والجديدة أقل `δ`نظرياً نظيفة، لكن تتطلب حلًا متضامنًا لكل تحديث. لا أحد يعمل على TRPO في عام 2026.

> اعتماد على استراتيجية النطاق المتميزة (TRPO,Schulman 2015) هو أول تعديل:`δ`وفي النظرية، هذا رائع، ولكن كل تحديث يحتاج إلى إجراءات متوافقة.

تمت إعادة تشكيل المعلومات في الموقع، حيث تمت إعادة تشكيل المعلومات في الموقع، حيث تمت إعادة تشكيل المعلومات في الموقع، حيث تمت إعادة تشكيل المعلومات في الموقع.

> PPO(Schulman 等人 2017) باستخدام هدف قصص بسيط لبدء الصعب اعتماد النطاق الحكم.多一行代码.

> **【中文解读】**الابتكار الأساسي لـ PPO: باستخدام قص قصة الهدف بديلًا لـ TRPO. النسبة الأهمية r_t(theta) = pi_theta / pi_old 被剪到 [1-epsilon, 1+epsilon] 范围内.

> **【拓展：PPO 之外的选择——DPO 与 GRPO】**على الرغم من أن PPO 仍然是 2026 عام الاختيار المخصص، ولكن البدائل تظهر.

## المفهوم الأساسي

![PPO clipped surrogate objective: ratio clipping at 1 ± ε](../assets/ppo.svg)

**The importance ratio.**

`r_t(θ) = π_θ(a_t | s_t) / π_{θ_old}(a_t | s_t)`

هذا هو نسبة احتمالية السياسة الجديدة مقابل السياسة التي جمعت البيانات. `r_t = 1`لا يعني أي تغيير`r_t = 2`يعني أن السياسة الجديدة أكثر عرضة للانتقال`a_t`مثل القديمة

> **重要性比率。**تشابه استراتيجية جديدة مع استراتيجية جمع البيانات`r_t = 1`لا تغير`r_t = 2`إظهار استراتيجية جديدة`a_t`احتمالية هذه الاستراتيجية القديمة مرتين

**The clipped surrogate.**

`L^{CLIP}(θ) = E_t [ min( r_t(θ) A_t, clip(r_t(θ), 1-ε, 1+ε) A_t ) ]`

شروطين:

- إذا كانت الميزة`A_t > 0`و يحاول النسبة أن تنمو`1 + ε`، المقطوعة تسطح التراجع  لا تدفع عمل جيد أبعد من `+ε`فوق الاحتمالات القديمة
- إذا كانت الميزة`A_t < 0`و يحاول النسبة أن تنمو`1 - ε`(ما يعني أننا سنجعل خطوة سيئة أكثر احتمالا مقارنة مع تقليصها المقطوعة) ، كليب كابس التراجع  لا يدفع خطوة سيئة أسفل `-ε`. . .

- نعم`min`يتعامل الاتجاه الآخر: إذا تحرك النسبة في الاتجاه * المفيد * ، فإنك لا تزال تحصل على التراجع (لا وجود قطع على الجانب الذي سيؤذيك).

نموذجي`ε = 0.2`. رسم الهدف كعمل من`r_t`: وظيفة خطية على شكل قطعة مع سقف مسطح على الجانب "الجيد" والطابق مسطح على الجانب "سيئ".

> **裁剪代理。**两项: إذا كانت الفوائد صائبة ومعدل أعلى من `1 + ε`، قطع تغير التسعير لا تجعل الحركة جيدة أكثر من احتمال القديم`+ε`更多── إذا كانت الفوائد سلبية ومعدل أقل من `1 - ε`لا تقلل من الحركة السيئة`-ε`更多──典型 `ε = 0.2`.

> **【中文解读】**إنما يعني أن الاستراتيجية تتغير أكثر من 20% في كل تحديث. إذا كان حركة جيدة، فإن الحالة ستزيد بنسبة 20%. إذا كان حركة سيئة، فإن الحالة ستقلل بنسبة 20%.

**The full PPO loss.**

`L(θ, φ) = L^{CLIP}(θ) - c_v · (V_φ(s_t) - V_t^{target})² + c_e · H(π_θ(·|s_t))`

نفس الهيكل الممثل-النقدي مثل A2C. ثلاثة معايير، عادة `c_v = 0.5`،`c_e = 0.01`،`ε = 0.2`. . .

> **完整的 PPO 损失。**مع A2C مشابهة للعملاء-النقاد 結構──三个系数, عادة `c_v = 0.5`.`c_e = 0.01`.`ε = 0.2`.

**The training loop.**

1. جمع`N × T`الانتقالات عبر `N`بيئات متوازية`T`كل خطوة
2. احسب المزايا (GAE) ، وتجمدها كمتواصلات.
3. تجميد`π_{θ_old}`كقطة من التيار`π_θ`. . .
4. لأجل`K`فترة، لكل مجموعة صغيرة من`(s, a, A, V_target, log π_old(a|s))`:
   - الحساب`r_t(θ) = exp(log π_θ(a|s) - log π_old(a|s))`. . .
   - التطبيق`L^{CLIP}`+ فقدان القيمة + إنتروبي
   - خطوة تدريجية
5. إرمي التنفيذ، عودي إلى الخطوة الأولى

`K = 10`وبالطائفة الصغيرة من 64 هو مجموعة متطابقة من المعايير.

> **训练循环。**جمع → 计算 GAE 优势 → 结旧策略 → K 轮更新 → 丢弃数据──`K = 10`و 64 من الجملة الصغيرة هي المعيارات العالية.

**KL-penalty variant.**اقترحت الورقة الأصلية بديلاً باستخدام عقوبة KL قابلة للتكيف: `L = L^{PG} - β · KL(π_θ || π_old)`مع`β`تم تعديلها بناءً على KL الملاحظ. أصبح نسخة القصص المهيمنة؛ والفرع KL يبقى في RLHF (حيث يكون KL إلى سياسة المرجعية قيودا منفصلة تريد دائما على أي حال).

> **KL 惩罚变体。**أظهرت النص الأصلي أن استخدام التكيف مع KL 惩罚 هو بديل للصيغة القصوى لتصبح رئيسية.

## بناء ذلك تحرك لتحقيق
```figure
ppo-clip
```

## بناءها

### الخطوة الأولى: التقاط`log π_old(a | s)`في وقت الإطلاق

```python
for step in range(T):
    probs = softmax(logits(theta, state_features(s)))
    a = sample(probs, rng)
    s_next, r, done = env.step(s, a)
    buffer.append({
        "s": s, "a": a, "r": r, "done": done,
        "v_old": value(w, state_features(s)),
        "log_pi_old": log(probs[a] + 1e-12),
    })
    s = s_next
```

يتم التقاط اللقطة مرة واحدة، في وقت الإطلاق. لا تتغير خلال فترات التحديث.

> 快照在推出时拍摄一次──在更新时代 期间不变──

### الخطوة الثانية: حساب ميزات GAE (المدرسة 07)

نفس A2C، تطبيع على جميع أنحاء اللحظة.

> مع A2C 相同──跨批次归归化──

### الخطوة الثالثة: تحديثات بديلة مقطوعة

```python
for _ in range(K_EPOCHS):
    for mb in minibatches(buffer, size=64):
        for rec in mb:
            x = state_features(rec["s"])
            probs = softmax(logits(theta, x))
            logp = log(probs[rec["a"]] + 1e-12)
            ratio = exp(logp - rec["log_pi_old"])
            adv = rec["advantage"]
            surrogate = min(
                ratio * adv,
                clamp(ratio, 1 - EPS, 1 + EPS) * adv,
            )
            # backprop -surrogate, add value loss, subtract entropy
            grad_logpi = onehot(rec["a"]) - probs
            if (adv > 0 and ratio >= 1 + EPS) or (adv < 0 and ratio <= 1 - EPS):
                pg_grad = 0.0  # clipped
            else:
                pg_grad = ratio * adv
            for i in range(N_ACTIONS):
                for j in range(N_FEAT):
                    theta[i][j] += LR * pg_grad * grad_logpi[i] * x[j]
```

نمط "التراجع إلى الصفر" هو قلب PPO. إذا تمت التحويل السياسة الجديدة بالفعل إلى اتجاه مفيد، فإن التحديث يتوقف.

> النموذج "قطع → 零梯度" هو جوهر PPO. إذا كانت الاستراتيجية الجديدة قد تحولت بعيداً جداً في اتجاه مواتٍ، فإن التحديث يتوقف.

### الخطوة الرابعة: القيمة والإنتروبي

إضافة MSE القياسية إلى الهدف النقدي ومكافأة الإنتروبي على الفاعل، نفس A2C.

> إلى النقاد  هدف إضافة المعايير MSE، إلى الممثل  إضافة  مكافأة، مع A2C

### الخطوة 5: التشخيص

ثلاثة أشياء يجب مشاهدتها في كل تحديث:

> كل تحديث يجب مراقبته ثلاثة أشياء:

- **Mean KL** `E[log π_old - log π_θ]`يجب أن تبقى في`[0, 0.02]`إذا تمرّ`0.1`، تقليل`K_EPOCHS`أو`LR`. . .
  **平均 KL。**يجب أن تبقى`[0, 0.02]`إذا تجاوزت `0.1`, تقليل`K_EPOCHS`أو`LR`.
- **Clip fraction** الجزء من العينات التي يقع نسبةها خارجها `[1-ε, 1+ε]`يجب أن يكون`~0.1-0.3`إذا`~0`، المقطع لا يطلق أبدا → رفع `LR`أو`K_EPOCHS`إذا`~0.5+`، أنت تتجاوز حدة التنفيذ → خفضهم.
  **裁剪比例。**%%`[1-ε, 1+ε]`نسبة نمط`~0.1-0.3`.
- **Explained variance** `1 - Var(V_target - V_pred) / Var(V_target)`. متريكه النقدي الجوده يجب أن يرتفع نحو 1 كما يتعلم النقدي
  **解释方差。**                                                                                                                                                                                                                                                              

## الفخاخ

- **Clip coefficient mistuned.** `ε = 0.2`هو المعيار الفعلي.`0.1`يجعل التحديثات خجولة جداً`0.3+`يدعو لعدم الاستقرار
  **裁剪系数调错。** `ε = 0.2`هو معيار حقيقة`0.1`太保守`0.3+`导致不稳定──
- **Too many epochs.** `K > 20`يزعج بشكل روتيني لأن السياسة تتحرك بعيداً عن`π_old`. فترات الحد الأقصى، خاصة للشبكات الكبيرة
  **太多 epoch。** `K > 20`لا يزال دائماً غير مستقرة، لأن الاستراتيجية متجاهلة`π_old`太远──限制时代,特别是大网络──
- **No reward normalization.**مقياس مكافأة كبيرة تستهلك نطاق المقاطع. عادي مكافآت (تشغيل std) قبل ميزات الحوسبة.
  **没有奖励归一化。**مقياس الجائزة الكبيرة تسبب في تغيير نطاق الحسابات.
- **Forgetting advantage normalization.**تعاديل المعدل الصفر لكل مجموعة وحدة ستد هو معيار. تخطي ذلك يدمّر PPO على معظم المعايير.
  **忘记优势归一化。**كل مجموعة من الصفوف / الوحدات المعيارية هي المعيارية.
- **Learning rate not decayed.**يُستفيد PPO من تدهور LR الخطي إلى الصفر. غالباً ما يكون LR الثابت أسوأ.
  **学习率未衰减。**PPO من LR 衰减到零中受益──常数 LR 通常更差──
- **Importance ratio math errors.**دائماً`exp(log_new - log_old)`للاستقرار الرقمي، لا `new / old`. . .
  **重要性比率数学错误。**始终用 `exp(log_new - log_old)`ضمان الثبات العدودي، وليس`new / old`.
- **Wrong gradient sign.**أقصى قدر من الاختيارات`-L^{CLIP}`علامة مُعكسة هي أخطاء (بي.بي.او) الأكثر شيوعاً
  **梯度符号错误。**أقصى حد للوكيل = * أقصى حد* `-L^{CLIP}`◊符号反转为 PPO 最常见 bug──

## استخدمها في إطار التنفيذ

إن PPO هو خوارزمية RL الافتراضية لعام 2026 عبر عدد مفاجئ من المجالات:

> PPO هو الارتجاع الروسي المتبقي في العديد من المجالات عام 2026:

| Use case | PPO variant |
|----------|-------------|
| Use case / 用例 | PPO variant / PPO 变体 |
| MuJoCo / robotics control / MuJoCo/机器人控制 | PPO with Gaussian policy, GAE(0.95) / 高斯策略的 PPO，GAE(0.95) |
| Atari / discrete games / Atari/离散游戏 | PPO with categorical policy, rolling 128-step rollouts / 分类策略的 PPO |
| RLHF for LLMs / LLM 的 RLHF | PPO with KL penalty to reference model, reward from RM at end of response / 带 KL 惩罚的 PPO |
| Large-scale game agents / 大规模游戏 Agent | IMPALA + PPO (AlphaStar, OpenAI Five) |
| Reasoning LLMs / 推理 LLM | GRPO (Lesson 12) — PPO variant without critic / 无 Critic 的 PPO 变体 |
| Preference-only data / 仅偏好数据 | DPO — closed-form collapsing of PPO+KL, no online sampling / 闭式 PPO+KL 折叠 |

تشكل PPO * الخسارة *  المقطع بديل + القيمة + الإنتروبي  هو الرفوف ل DPO ، GRPO ، وكل خط أنابيب RLHF تقريبًا.

> شكله* الخسارة* من PPO*قطع وكيل + 值 + 是 DPO、GRPO 和几乎所有RLHF 流水线的脚手架──

## أرسلها .

إبقوا`outputs/skill-ppo-trainer.md`:

```markdown
---
name: ppo-trainer
description: Produce a PPO training config and a diagnostic plan for a given environment.
version: 1.0.0
phase: 9
lesson: 8
tags: [rl, ppo, policy-gradient]
---

Given an environment and training budget, output:

1. Rollout size. `N` envs × `T` steps.
2. Update schedule. `K` epochs, minibatch size, LR schedule.
3. Surrogate params. `ε` (clip), `c_v`, `c_e`, advantage normalization on.
4. Advantage. GAE(`λ`) with explicit `γ` and `λ`.
5. Diagnostics plan. KL, clip fraction, explained variance thresholds with alerts.

Refuse `K > 30` or `ε > 0.3` (unsafe trust region). Refuse any PPO run without advantage normalization or KL/clip monitoring. Flag clip fraction sustained above 0.4 as drift.
```

## تمارين التدريب

1. **Easy.**إشغال PPO على 4 × 4 GridWorld مع `ε=0.2, K=4`- مقارنة كفاءة العينة مع A2C (حلقة واحدة لكل عملية التنفيذ) في مراحل البيئة المقابلة.
2. **Medium.**تفتيش`K ∈ {1, 4, 10, 30}`. عودة المسار مقابل خطوات البيئة وتتبع متوسط KL لكل تحديث.`K`هل ستنفجر (كيل) في هذه المهمة؟
3. **Hard.**استبدل الاختراق المستبدل مع عقوبة KL تكييفية (`β`مضاعفة إذا`KL > 2·target`، نصف إذا `KL < target/2`) مقارنة العائد النهائي، الاستقرار، وبدون كليب.

## شروط الرئيسية

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Importance ratio | "r_t(θ)" | `π_θ(a\|s) / π_old(a\|s)`; deviation from the policy that collected the data. |
| Clipped surrogate | "PPO's main trick" | `min(r·A, clip(r, 1-ε, 1+ε)·A)`; flat gradient past the clip on beneficial side. |
| Trust region | "TRPO / PPO intent" | Limit each update's KL to guarantee monotone improvement. |
| KL penalty | "Soft trust region" | Alternative PPO: `L - β · KL(π_θ \|\| π_old)`. Adaptive `β`. |
| Clip fraction | "How often clipping triggers" | Diagnostic — should be 0.1-0.3; outside means mistuned. |
| Multi-epoch training | "Data reuse" | K epochs on each rollout; variance cost traded for sample efficiency. |
| On-policy-ish | "Mostly on-policy" | PPO is nominally on-policy but K>1 epochs uses slightly-off-policy data safely. |
| PPO-KL | "The other PPO" | KL-penalty variant; used in RLHF where KL-to-reference is already a constraint. |

## المزيد من القراءة

- [Schulman et al. (2017). Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)-الورقة
- [Schulman et al. (2015). Trust Region Policy Optimization](https://arxiv.org/abs/1502.05477)(تريبو) ، سلف (بيبو)
- [Andrychowicz et al. (2021). What Matters In On-Policy RL? A Large-Scale Empirical Study](https://arxiv.org/abs/2006.05990) كل مفاتيح PPO متزايدة تم إزالة.
- [Ouyang et al. (2022). Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) InstructGPT: وصفة PPO-in-RLHF
- [OpenAI Spinning Up — PPO](https://spinningup.openai.com/en/latest/algorithms/ppo.html) نظيف المعرض الحديث مع PyTorch.
- [CleanRL PPO implementation](https://github.com/vwxyzjn/cleanrl) إشارة PPO ملف واحد يستخدم من قبل العديد من الأوراق.
- [Hugging Face TRL — PPOTrainer](https://huggingface.co/docs/trl/main/en/ppo_trainer) وصفة الإنتاج لـ PPO على نماذج اللغة؛ اقرأ جنبا إلى جنب مع الدروس 09 (RLHF).
- [Engstrom et al. (2020). Implementation Matters in Deep Policy Gradients](https://arxiv.org/abs/2005.12729) ورقة "37 تحسينات مستوى الرمز" ؛ أي خدوش PPO تحمل الحمل والتي هي شعبية.
