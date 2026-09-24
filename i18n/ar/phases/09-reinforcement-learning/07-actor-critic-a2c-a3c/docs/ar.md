# الممثل-المنتقد  A2C و A3C 演员-معلق  A2C و A3C

> "إضافة نقدي يتعلم"`V̂(s)`، ويقلل من العودة، و تحصل على ميزة التي لديها نفس التوقعات ولكن أقل بكثير التباين. وهذا هو الممثل-النقدي. A2C يديرها بالتزامن؛ A3C يديرها عبر الأوتار. كلاهما هو النموذج العقلي لكل طريقة العميقة الحديثة RL.

> **【中文解读】**REINFORCE 方差太大──加入一个"评论家"(Critic)学习 V̂((s) ، استخدمها كمنشأ لتشكيل وظيفة ميزة A = G - V̂(s) ، والمتوقع لا يتغير ولكن الفرق يقل بشكل كبير── هذا هو Actor-CriticPPO、SAC 等 جميع النموذج الأساسي للطريقة الحديثة للعمق الـ RL──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 04 (TD Learning), Phase 9 · 06 (REINFORCE) | **前置知识:** Phase 9 · 04 (TD 学习), Phase 9 · 06 (REINFORCE)
**Time:** ~75 minutes | **时间:** ~75 分钟

## المشكلة المشكلة المشكلة

فانيلا رينفورس تعمل، ولكن تغيرها رهيب.`G_t`يمكن أن تتدفق على عامل 10 بين الحلقات.`∇ log π`و يُنتج متوسط تقدير التراجع الذي يستغرق آلاف الحلقات لنقل السياسة على نفس المسافة التي يمكنك نقلها بها مع تحديثات أقل بكثير من DQN.

> الموافقة المبدئية فعالة، ولكن الوضع سيء جدا.`G_t`في回合间可能波动 10 倍.`∇ log π`في المتوسط، يحتاج جهاز تقييم التدريج الذي ينشأ إلى آلاف المواجهات لتحريك استراتيجية مع أقل قدر من DQN  تحديث يمكن أن يصل إلى نفس النتائج 

التباين يأتي من استخدام العائدات الخام. إذا قمت بإسقاط خط أساسي `b(s_t)` أي وظيفة من الحالة، بما في ذلك القيمة المكتسبة  لا تتغير التوقعات وتقلص التباين.`V̂(s_t)`الآن الكمية مضاعفة`∇ log π`هو * الميزة*:

`A(s, a) = G - V̂(s)`

> 方差来自使用原始回报──如果减去基线 `b(s_t)` أي وظيفة حالة، بما في ذلك تعلم المتوقع لا يتغير ولكن الاختلاف يقلل.`V̂(s_t)`الآن يرتفع`∇ log π`≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ ≈ 

عمل جيد إذا كان ينتج عائد فوق المتوسط ؛ سيء إذا كان أقل. REINFORCE مع ناقد مدرب هو *منتقد الممثل. * يعطي النقاد الممثل معلمًا منخفضًا التباين. هذه هي كل طريقة سياسة عميقة بعد عام 2015 (A2C ، A3C ، PPO ، SAC ، IMPALA).

> 动作好如果产生高于平均的回报;差如果低于──带学习批评的 REINFORCE 就是 *الجهاز الممثل-النقاد*──النقد 给演员一个低方差的老师──这是2015年后每深度策略方法(A2C、A3C、PPO、SAC、IMPALA)──

## المفهوم الأساسي

![Actor-critic: policy net plus value net, TD residual as advantage](../assets/actor-critic.svg)

**Two networks, one shared loss:**

> **两个网络，一个共享损失：**

- **Actor** `π_θ(a | s)`: السياسة. عينات للتصرف. تدرب مع تراجع السياسة.
  **Actor** `π_θ(a | s)`: استراتيجية. اعتبارهم عمليات.
- **Critic** `V_φ(s)`: التقديرات المتوقعة العودة من الدولة. تدرب على الحد الأدنى `(V_φ(s) - target)²`. . .
  **Critic** `V_φ(s)`: التقديرات من حالة الإصدار المتوقع.`(V_φ(s) - target)²`.

**The advantage.**شكلين قياسيين:

> **优势函数。**两种标准形式:

- * ميزة المجلس المالي*:`A_t = G_t - V_φ(s_t)`غير متحيز، متباين أعلى
  *MC 优势:* 无偏,方差较高──
- *فائدة التكنولوجيا*:`A_t = r_{t+1} + γ V_φ(s_{t+1}) - V_φ(s_t)`. التحيز (استخدامات `V_φ`() ، المتغيرات أقل بكثير.`δ_t`. . .
  *TD 优势:* 有偏差(使用 `V_φ`),方差远低──也称为 *TD残差* `δ_t`.

**n-step advantage.**التقاط بين الاثنين:

`A_t^{(n)} = r_{t+1} + γ r_{t+2} + … + γ^{n-1} r_{t+n} + γ^n V_φ(s_{t+n}) - V_φ(s_t)`

`n = 1`هو طاهرة التد.`n = ∞`هو MC. معظم التنفيذات تستخدم `n = 5`لـ " أتاري "`n = 2048`لـ (بوبو) على (ميوجوكو)

> **n 步优势。**بينهما قيمة`n = 1`إنها مجرد إختبار`n = ∞`نعم MC. معظمها يطبق على Atari.`n = 5`, معظم الموظفين يستخدمون`n = 2048`.

**Generalized Advantage Estimation (GAE).**اقترح Schulman et al. (2016) متوسط معدل على نحو متكامل على جميع مزايا الخطوة n:

`A_t^{GAE} = Σ_{l=0}^{∞} (γλ)^l δ_{t+l}`

مع`λ ∈ [0, 1]`. .`λ = 0`هو TD (تباين منخفض، تحيز كبير). `λ = 1`هو MC (تباين عال، غير متحيز). `λ = 0.95`هو 2026 الوضع الافتراضي  حتى يكون الرقم المتحرك / التغير حيث تريد ذلك.

> **【中文解读】**GAE(التنقيديات الموسيقية) هو التحسن الرئيسي للجهات الفاعلة: من خلال مؤشر زيادة الوزن المتوسط في نـ 步优势، العثور على أفضل التوازن بين الاختلاف والاختلاف.

> **【拓展：GAE 在 RLHF 中的应用】**في مشهد الجامعة، "الوضع" هو سلسلة رمزية تم إنشاؤها، "التحرك" هو التوالي رمزية، "المكافأة" من نموذج مكافأة。

**A2C: synchronous advantage actor-critic.**جمع`T`خطوات عبر`N`بيئات متوازية، احسب مزايا لكل خطوة، قم بتحديث الممثل والنقيب على اللحظة المشتركة، أكرر، أسهل وأكثر قابلية للتوسع من A3C.

> **A2C：同步优势 Actor-Critic。**في`N`个并行 البيئة جمع `T`步──计算每步优势──在合并批次上更新 Actor 和 Critic──重复──A3C 的更简单、更可扩展的兄弟──

**A3C: asynchronous advantage actor-critic.**Mnih et al. (2016) ، Spawn `N`خيوط العمال، كل واحد يعمل على محيط. يحسب كل عامل تراجعات محليا على تنفيذها الخاص، ثم يطبقها بشكل غير متزامن على خادم معايير مشتركة. لا حاجة إلى مسدس إعادة التشغيل  يعملون على إزالة التنسيق عن طريق تشغيل مسارات مختلفة. أثبت A3C أنه يمكنك التدريب على وحدات المعالجة المركزية على نطاق واسع. في عام 2026، يهيمن A2C القائم على GPU (حوائط متوازية المجموعة) لأن GPUs تريد دفعات كبيرة.

> **A3C：异步优势 Actor-Critic。**(Mnih 等人 (2016) ‬`N`个工作线程,每个运行一个环境――每个工作线程在本地计算梯度,然后不同步应用到共享参数服务器――不需要回放缓冲区工作线程通过运行不同轨迹来相关――2026年,基于GPU的A2C占主导地位,因为GPU 需要大量的量――

**The combined loss.**

`L(θ, φ) = -E[ A_t · log π_θ(a_t | s_t) ]  +  c_v · E[(V_φ(s_t) - G_t)²]  -  c_e · E[H(π_θ(·|s_t))]`

ثلاثة شروط: خسارة مستوى السياسة، تراجع القيمة، مكافأة الإنتروبي. `c_v ~ 0.5`،`c_e ~ 0.01`هي نقاط بداية طائفية.

> **组合损失。**ثلاثة: استراتيجية التدريجية فقدان  قيمة العودة  مكافأة`c_v ~ 0.5`.`c_e ~ 0.01`هو القيمة الابتدائية النموذجية

> **【中文解读】**فقدان مجموعة من الممثلين-النقاد = 策略梯度损失 + 值函数归归 + 正则化── these three distinct对应: جعل احتمالات الحركة الجيدة أكبر 让批评更准确 防止策略过早缩为确定性策略──

> **【拓展：GAE→PPO→RLHF】**GAE (بيعي فائدة التقييم) هو الجسم الأساسي لـ PPO، و PPO هو الجهاز المعيارية للتدريب ChatGPT RLHF  . . = 0.95 هو القيمة المخصصة لعام 2026، لتحقيق التوازن بين الاختلافات والخلافات.

## بناء ذلك تحرك لتحقيق
```figure
actor-critic
```

## بناءها

### الخطوة الأولى: نقدي

النقاد الخطى`V_φ(s) = w · features(s)`تحديث مع MSE:

```python
def critic_update(w, x, target, lr):
    v_hat = dot(w, x)
    err = target - v_hat
    for j in range(len(w)):
        w[j] += lr * err * x[j]
    return v_hat
```

على البيانات الجدولية يتقارب النقاد في بضع مئات الحلقات. على Atari، استبدل النقاد الخطية مع صندوق CNN المشترك + رأس القيمة.

> النقاد`V_φ(s) = w · features(s)`استخدام MSE 更新──在表格环境中几百回合就收──在 Atari 上,替换为共享CNN 主干 + 值头──

### الخطوة الثانية: فائدة الخطوة

نظراً لعدد الطول`T`و نهائيّة محطّمة`V(s_T)`:

```python
def compute_advantages(rewards, values, gamma=0.99, lam=0.95, last_value=0.0):
    advantages = [0.0] * len(rewards)
    gae = 0.0
    for t in reversed(range(len(rewards))):
        next_v = values[t + 1] if t + 1 < len(values) else last_value
        delta = rewards[t] + gamma * next_v - values[t]
        gae = delta + gamma * lam * gae
        advantages[t] = gae
    returns = [a + v for a, v in zip(advantages, values)]
    return advantages, returns
```

`returns`هو الهدف النقدي.`advantages`هو ما يضاعف`∇ log π`. . .

> `returns`هو النقاد  هدف`advantages`هو ضرب `∇ log π`   

### الخطوة الثالثة: تحديث مشترك

```python
for step_i, (x, a, _r, probs) in enumerate(traj):
    adv = advantages[step_i]
    target_v = returns[step_i]

    # critic
    critic_update(w, x, target_v, lr_v)

    # actor
    for i in range(N_ACTIONS):
        grad_logpi = (1.0 if i == a else 0.0) - probs[i]
        for j in range(N_FEAT):
            theta[i][j] += lr_a * adv * grad_logpi * x[j]
```

في السياسة، تنفيذ واحد لكل تحديث، معدلات التعلم منفصلة للممثل والنقيب.

> استراتيجية على الإنترنت, كل مرة تحديث تنفيذ,الممثل و النقاد استخدام مختلف معدل التعلم.

### الخطوة الرابعة: التوازي (A3C مقابل A2C)

- **A3C:**ألتقط`N`كل واحد يدير محيطه الخاص والمرور الأمامي الخاص به. دفع تحديثات التراجع بشكل دوري إلى الماجستير المشترك. لا قفل على الماجستير  السباقات بخير، فإنها مجرد إضافة الضوضاء.
- **A2C:**أركض`N`في حالة عمل واحد، قم بتجميع الملاحظات إلى مجموعة`[N, obs_dim]`المجموعة، المجموعة المقدمة، المجموعة الخلفية المجموعة. استخدام أعلى من GPU، تحديد، أسهل للتفكير. الافتراض في عام 2026.

رمز ألعابنا هو واحد خيط لوضوح؛ إعادة كتابة إلى A2C المكتوب هو ثلاثة خطوط من numpy.

> كود ألعابنا هو خط واحد للحفاظ على وضوحه؛ إعادة كتابة الكمية A2C فقط تحتاج إلى ثلاث صفوف من النومب

## الفخاخ

- **Critic bias before actor gradient.**إذا كان النقاد عشوائيًا، فإن خط أساسه غير معلومي وأنت تتدرب على الضوضاء النقية. احترم النقاد لبضعة مئات الخطوات قبل تشغيل نسبة السياسة، أو استخدم معدل تعلم الممثلون البطيء.
  **Actor 梯度之前的 Critic 偏差。**إذا كان النقدي هو من العشوائية، لا يوجد كمية من المعلومات، أنت تدرب على الضجيج النقي.
- **Advantage normalization.**تعاديل المزايا إلى صفر المتوسط / وحدة-std لكل دفعة. يثبت التدريب بشكل كبير مقابل تكلفة قريبة من الصفر.
  **优势归一化。**كل حزمة من الميزات سوف تتم تكييفها إلى صفر متوسط القيمة / الوحدة المعيارية الفرق.
- **Shared trunk.**استخدم مخرج الميزات المشتركة للممثل والنقيب على مدخلات الصورة. رؤوس منفصلة. الميزات المشتركة مفتوحة على كل من الخسائر.
  **共享主干。**图像输入时使用共享特征提取器──分开的头──共享特征同时从两个损失中获益──
- **On-policy contract.**A2C يستخدم البيانات مرة أخرى لنحديث واحد بالضبط. أكثر و تدرجك متحيز (تصحيح العينات المهمة هو ما يضيف PPO).
  **在线策略约束。**A2C 恰好用数据做一次更新.
- **Entropy collapse.**بدون`c_e > 0`سياسة تصبح شبه تحديدية بعد بضع مئات من التحديثات وتتوقف عن الاستكشاف
  **熵坍缩。**لا يوجد`c_e > 0`، إستراتيجية بعد مئات المرات تحديثات تغيرت لتصبح قريبة من اليقين وتوقف عن البحث.
- **Reward scale.**تعتمد magnitudes الميزة على مقياس المكافآت. عادي مكافآت (مثل، تشغيل-std تقسيم) لعدد التراجع المتسقة عبر المهام.
  **奖励尺度。**درجة الفائدة تعتمد على درجة الجائزة 

## استخدمها في إطار التنفيذ

A2C / A3C نادرا ما تكون الخيار النهائي في عام 2026 ولكنها هي الهندسة المعمارية التي يضبطها كل شيء لاحقاً:

> A2C / A3C في عام 2026 نادرًا ما يكون الخيار النهائي ، ولكنها هي بعد ذلك جميع الطرق المحددة:

| Method | Relation to A2C |
|--------|----------------|
| Method / 方法 | Relation to A2C / 与 A2C 的关系 |
| PPO | A2C + clipped importance ratio for multi-epoch updates / A2C + 裁剪重要性比率用于多轮更新 |
| IMPALA | A3C + V-trace off-policy correction / A3C + V-trace 离策略修正 |
| SAC (Phase 9 · 07) | Off-policy A2C with a soft-value critic (next lesson) / 离策略 A2C + 软值 Critic |
| GRPO (Phase 9 · 12) | A2C without the critic — group-relative advantage / 无 Critic 的 A2C——组相对优势 |
| DPO | A2C collapsed into a preference-ranking loss, no sampling / 折叠为偏好排名损失的 A2C |
| AlphaStar / OpenAI Five | A2C with league training + imitation pre-training / A2C + 联盟训练 + 模仿预训练 |

إذا رأيت "ميزة" في ورقة عام 2026، فكر في ناقد الممثلين.

> إذا رأيت "ميزة" في مقال عام 2026 ففكر في الممثل والنقد

## أرسلها .

إبقوا`outputs/skill-actor-critic-trainer.md`:

```markdown
---
name: actor-critic-trainer
description: Produce an A2C / A3C / GAE configuration for a given environment, with advantage estimation and loss weights specified.
version: 1.0.0
phase: 9
lesson: 7
tags: [rl, actor-critic, gae]
---

Given an environment and compute budget, output:

1. Parallelism. A2C (GPU batched) vs A3C (CPU async) and the number of workers.
2. Rollout length T. Steps per env per update.
3. Advantage estimator. n-step or GAE(λ); specify λ.
4. Loss weights. `c_v` (value), `c_e` (entropy), gradient clip.
5. Learning rates. Actor and critic (separate if using).

Refuse single-worker A2C on environments with horizon > 1000 (too on-policy, too slow). Refuse to ship without advantage normalization. Flag any run with `c_e = 0` and observed entropy < 0.1 as entropy-collapsed.
```

## تمارين التدريب

1. **Easy.**تدريب الممثلين المنتقدين مع ميزة MC (`G_t - V(s_t)`) على 4×4 GridWorld. مقارنة كفاءة العينة مع REINFORCE-with-running-mean-baseline من الدروس 06.
2. **Medium.**الانتقال إلى ميزة TD-`r + γ V(s') - V(s)`) قياس التباين بين مجموعات الميزات. كم ينخفض؟
3. **Hard.**تنفيذ GAE ((λ).`λ ∈ {0, 0.5, 0.9, 0.95, 1.0}`. العائد النهائي للمخطط مقابل كفاءة العينة أين هو نقطة التحيز/الاختلاف المثالي لهذا المهمة؟

## شروط الرئيسية

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Actor | "The policy net" / 演员（策略网络） | `π_θ(a\|s)`, updated by policy gradient. |
| Critic | "The value net" / 评论家（值网络） | `V_φ(s)`, updated by MSE regression to returns / TD targets. |
| Advantage | "How much better than average" / 优势函数 | `A(s, a) = Q(s, a) - V(s)` or its estimators. Multiplier for `∇ log π`. |
| TD residual | "δ" / TD 残差 | `δ_t = r + γ V(s') - V(s)`; one-step advantage estimate. |
| GAE | "The interpolation knob" / 广义优势估计 | Exponentially weighted sum of n-step advantages, parameterized by `λ`. |
| A2C | "Synchronous actor-critic" / 同步演员-评论家 | Batched across envs; one gradient step per rollout. |
| A3C | "Async actor-critic" / 异步演员-评论家 | Worker threads push gradients to a shared param server. Original paper; less common in 2026. |
| Bootstrap | "Use V at the horizon" / 自举截断 | Truncate the rollout, add `γ^n V(s_{t+n})` to close the sum. |

## المزيد من القراءة

- [Mnih et al. (2016). Asynchronous Methods for Deep Reinforcement Learning](https://arxiv.org/abs/1602.01783) A3C، ورقة الممثلين المنتقدين الأصلية غير المزامن.
- [Schulman et al. (2016). High-Dimensional Continuous Control Using Generalized Advantage Estimation](https://arxiv.org/abs/1506.02438) GAE
- [Sutton & Barto (2018). Ch. 13 — Actor-Critic Methods](http://incompleteideas.net/book/RLbook2020.pdf)أساسيات؛ إزواج هذا مع فصل 9 على التقريب الوظيفي عندما يكون النقاد شبكة عصبية.
- [Espeholt et al. (2018). IMPALA](https://arxiv.org/abs/1802.01561) تحديداً متوزعاً للمحركين المنتقدين مع تصحيح خارج السياسة في البصمة.
- [OpenAI Baselines / Stable-Baselines3](https://stable-baselines3.readthedocs.io/) إنتاج عمليات A2C/PPO التي تستحق القراءة.
- [Konda & Tsitsiklis (2000). Actor-Critic Algorithms](https://papers.nips.cc/paper/1786-actor-critic-algorithms) النتيجة الأساسية للتقارب للفشل الممثل-النقدي على مقياسين.
