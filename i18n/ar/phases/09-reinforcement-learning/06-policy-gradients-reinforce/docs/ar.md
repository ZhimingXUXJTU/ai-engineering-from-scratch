# سياسة تدريجية  تعزيز من الصفر ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬ ‬

> توقف عن تقدير القيمة. حدد السياسة مباشرة، وحسب تراجع العائد المتوقع، خطوة صعودا. كتب ويليامز (1992) ذلك في نظرية واحدة. هذا هو السبب في وجود PPO، GRPO، وكل حلقة LLM RL.

> **【中文解读】**غير تقييم قيمة العملات، مباشرة في استراتيجية تقييمات π_θ((a في المقابل) ، الحساب المتوقع للرداد من التدابير ومعدلات ارتفاع.`∇J(θ) = E[G · ∇log π_θ(a|s)]` هذا هو سبب وجود PPO ̊GRPO ̊ وكذلك جميع النماذج الكبيرة RL ̊ دورة تدريب ̊‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 03 (Backpropagation), Phase 9 · 03 (Monte Carlo), Phase 9 · 04 (TD Learning) | **前置知识:** Phase 3 · 03 (反向传播), Phase 9 · 03 (蒙特卡洛), Phase 9 · 04 (TD 学习)
**Time:** ~75 minutes | **时间:** ~75 分钟

## المشكلة المشكلة المشكلة

Q-التعلم و DQN تعريف وظيفة * القيمة *. انت تختار الإجراءات عن طريق `argmax Q`هذا جيد للأفعال المفصلة والحالات المفصلة. انهار عندما تكون الأفعال مستمرة (التي`argmax`أكثر من 10 أبعاد الدوران؟) أو عندما تريد سياسة استوكاستية (`argmax`هو تحديد من خلال البناء).

> Q-تعلم و DQN 参数化*值*函数──通过 `argmax Q`选择动作── هذا لا مشكلة فى الانفصال عن الحركة والحالة الانفصالية── ولكن عندما يتواصل الحركة`argmax`؟) أو تحتاج إلى استراتيجية`argmax`(تباً) ، (تباً)

تُعَدّل نسبة السياسة * السياسة* بدلاً من ذلك. `π_θ(a | s)`شبكة عصبية تنتج توزيع على الإجراءات.`θ`خطوة صعوداً`argmax`لا يوجد استرجاع بيلمان، فقط صعود التسلسل`J(θ) = E_{π_θ}[G]`. . .

> 策略梯度改为参数化*策略*`π_θ(a | s)`هو الإنتاج تحركات توزيع شبكة عصبية.`θ`梯度──往上走──不需要 `argmax`لا حاجة إلى بيلمان`J(θ) = E_{π_θ}[G]`أعلى مستوى صعود

نظرية REINFORCE (ويليامز 1992) تقول لك أن هذا التراجع يمكن حسابه:`∇J(θ) = E_π[ G · ∇_θ log π_θ(a | s) ]`أطلق حلقة، احسب العائد، مضاعفة بال`∇ log π_θ(a | s)`في كل خطوة، متوسط، صعود درجة، انتهى

> (ويليامز 1992) أخبرنا أن هذا التسلسل يمكن حسابه:`∇J(θ) = E_π[ G · ∇_θ log π_θ(a | s) ]`◊运行一个回合――计算回报――每步乘以 `∇ log π_θ(a | s)`◊取平均──梯度上升──完成──

كل خوارزمية LLM-RL في 2026  PPO، DPO، GRPO  هي تحسين من REINFORCE. فهمها في أصابعك هو شرط أساسي لبقية هذه المرحلة، وللمرحلة 10 · 07 (تنفيذ RLHF) والمرحلة 10 · 08 (DPO).

> 2026 كل سنة LLM-RL 算法PPO、DPO、GRPO هي تحسينات REINFORCE .

> **【中文解读】**الفكرة الأساسية لدرجة الاستراتيجية: تحسين مباشرة لعدد الاستراتيجية θ، جعل احتمالية حركة العائدات عالية تزيد`∇log π`"إنها" "إتجاهات الاستراتيجية" ، ضربة من "إتجاهات جيدة"

> **【拓展：PPO→ChatGPT对齐】**ChatGPT RLHF  تدريب استخدام PPO  الخوارزمية، في الأساس هو REINFORCE + النقد 基线 + 信赖域剪剪──`loss = -advantage * log_prob`هذا الصف من الكود، يظهر الآن تقريبا كل 2026 عام نموذج RL  تدريب الكود في الكتب التدريبية.

## المفهوم الأساسي

![Policy gradient: softmax policy, log-π gradient, return-weighted update](../assets/policy-gradient.svg)

**The policy gradient theorem.**لأي سياسة`π_θ`المعلمات بواسطة `θ`:

`∇J(θ) = E_{τ ~ π_θ}[ Σ_{t=0}^{T} G_t · ∇_θ log π_θ(a_t | s_t) ]`

أين`G_t = Σ_{k=t}^{T} γ^{k-t} r_{k+1}`هو العائد المخصوم من الخطوة`t`التوقعات تجاوزت المسارات الكاملة`τ`تم أخذ عينات من`π_θ`. . .

> **策略梯度定理。**لأي شيء`θ`استراتيجيات التعددية`π_θ`، تتساوي درجة الرجوع المتوقع: تخفيضات العائد وارتفاع توقعات درجة الاستراتيجية العديدة.`π_θ`采样完整轨迹上取──

**The proof is short.**التفريق`J(θ) = Σ_τ P(τ; θ) G(τ)`تحت التوقعات.`∇P(τ; θ) = P(τ; θ) ∇ log P(τ; θ)`(حيلة المشتقات السجلية) عامل`log P(τ; θ) = Σ log π_θ(a_t | s_t) + environment terms that do not depend on θ`تعبيرات البيئة تختفي خطين من الجبر يعطيكما النظرية

> **证明很短。**فى انتظارك`J(θ)`求导──使用对数导数技巧──将 `log P(τ; θ)`تم تحديد العدد على النحوين.

**Variance reduction tricks.**"فانيلا رينفورس" لديها اختلافات قاتلة "الردود ضجة"`∇ log π`إنّهم صاخبان، إنّ منتجاتهم صاخبة جداً.

> **方差降低技巧。**هناك فرق كبير جداً في المعلومات`∇ log π`هناك ضجيج، ضجيجهم أكبر.

1. **Baseline subtraction.**استبدل`G_t`مع`G_t - b(s_t)`لأي خط أساسي `b(s_t)`لا تعتمد على`a_t`غير متحيز لأن`E[b(s_t) · ∇ log π(a_t | s_t)] = 0`اختيار نموذجي:`b(s_t) = V̂(s_t)`تعلم من قبل النقاد → الممثل-النقاد (درس 07).
   **基线减法。**استخدام`G_t - b(s_t)`بدل `G_t` اختيار نموذجي:`b(s_t) = V̂(s_t)`بواسطة النقاد 学习 → الممثل-النقاد
2. **Reward-to-go.**استبدل`Σ_t G_t · ∇ log π_θ(a_t | s_t)`مع`Σ_t G_t^{from t} · ∇ log π_θ(a_t | s_t)`. فقط العائدات المستقبلية مهمة لفعل معين  مكافآت سابقة تساهم في ضجيج صفر المتوسط.
   **未来回报。** فقط استرداد المستقبل على تحركات محددة له معنى إسهامات الماضي  صفر متوسط الضجيج

مجتمعة، تحصل على:

`∇J ≈ (1/N) Σ_{i=1}^{N} Σ_{t=0}^{T_i} [ G_t^{(i)} - V̂(s_t^{(i)}) ] · ∇_θ log π_θ(a_t^{(i)} | s_t^{(i)})`

وهو REINFORCE مع خط أساسي  الجدول المباشر لـ A2C (دراسة 07) و PPO (دراسة 08).

**Softmax policy parameterization.**بالنسبة للقيام بعمل منفصل، الخيار القياسي:

`π_θ(a | s) = exp(f_θ(s, a)) / Σ_{a'} exp(f_θ(s, a'))`

أين`f_θ`أي شبكة عصبية تنتج نتيجة لكل عمل.

`∇_θ log π_θ(a | s) = ∇_θ f_θ(s, a) - Σ_{a'} π_θ(a' | s) ∇_θ f_θ(s, a')`

أي، النتيجة من الإجراءات التي تم اتخاذها ناقصاً قيمتها المتوقعة في إطار السياسة.

> **Softmax 策略参数化。**للتحركات المفصلة، تدرجة فورما简洁: النسبة المطلوبة للتحركات التي تم اتخاذها خفضها تحت استراتيجية

**Gaussian policy for continuous actions.** `π_θ(a | s) = N(μ_θ(s), σ_θ(s))`. .`∇ log N(a; μ, σ)`هذا كل ما يحتاجه SAC في المرحلة 9 · 07

> **连续动作的高斯策略。** `∇ log N(a; μ, σ)`هناك حل مغلق. هذا كل ما يلزم من SAC في المرحلة 9 · 07

## بناء ذلك تحرك لتحقيق
```figure
policy-gradient-landscape
```

## بناءها

### الخطوة الأولى: شبكة سياسة softmax

```python
def policy_logits(theta, state_features):
    return [dot(theta[a], state_features) for a in range(N_ACTIONS)]

def softmax(logits):
    m = max(logits)
    exps = [exp(l - m) for l in logits]
    Z = sum(exps)
    return [e / Z for e in exps]
```

استخدم سياسة خطية (متجه وزن واحد لكل عمل) لتحويل جدول. بالنسبة لـ Atari ، قم بتبادل في CNN واحافظ على رأس softmax.

> 表格环境使用线性策略(每个动作一个权重向量) ・・・对 Atari,换进 CNN 并保留软max 头――

### الخطوة الثانية: أخذ العينات وإمكانية تسجيل السجلات

```python
def sample_action(probs, rng):
    x = rng.random()
    cum = 0
    for a, p in enumerate(probs):
        cum += p
        if x <= cum:
            return a
    return len(probs) - 1

def log_prob(probs, a):
    return log(probs[a] + 1e-12)
```

### الخطوة الثالثة: الإرسال مع التقاط المراقبة السجلية

```python
def rollout(theta, env, rng, gamma):
    trajectory = []
    s = env.reset()
    while not done:
        logits = policy_logits(theta, s)
        probs = softmax(logits)
        a = sample_action(probs, rng)
        s_next, r, done = env.step(s, a)
        trajectory.append((s, a, r, probs))
        s = s_next
    return trajectory
```

### الخطوة الرابعة: تحديث REINFORCE

```python
def reinforce_step(theta, trajectory, gamma, lr, baseline=0.0):
    returns = compute_returns(trajectory, gamma)
    for (s, a, _, probs), G in zip(trajectory, returns):
        advantage = G - baseline
        grad_log_pi_a = [-p for p in probs]
        grad_log_pi_a[a] += 1.0
        for i in range(N_ACTIONS):
            for j in range(len(s)):
                theta[i][j] += lr * advantage * grad_log_pi_a[i] * s[j]
```

التراجع`∇ log π(a|s) = e_a - π(·|s)`(بما في ذلك)`a`- احتمالات) هو قلب التدرج السياسية softmax. احرقها في الذاكرة العضلية.

> 梯度 `∇ log π(a|s) = e_a - π(·|s)`(`a`يُعدّ محور التّسجيلات المُتَحَرّكَة في الذاكرة.

### الخطوة 5: خطوط أساسية

متوسط سريع من`G`على الرغم من أنّه لا يزال هناك الكثير من المعلومات عن المجموعة، فإنّه لا يزال من المفاجئ أنّه لا يزال من المفاجئ أنّه لا يزال من المفاجئ أنّه لا يزال من المفاجئ أنّه لا يزال من المفاجئ أنّه لا يزال من المفاجئ أنّه لا يزال من المفاجئ أنّه لا يزال من المفاجئ أنّه لا يزال من المفاجئ أنّه لا يزال من المفاجئ أنّه لا يزال من المفاجئ أنّه لا يزال من المفاجئ أنّه لا يزال من المفاجئ، ولكنّه لا يزال من المفاجئ أنّه لا يصل إلى المفاجئ.`V̂(s)`و تحصل على نقدي الممثل

> مؤخراً`G`متوسط النشاط كافٍ لتحقيق عمل 4 × 4 GridWorld  العمل؛ حوالي 500 回合收──将基线升级为学习的 `V̂(s)`لقد حصلت على نقدي الممثل

## الفخاخ

- **Exploding gradients.**العائدات يمكن أن تكون ضخمة دائماً التطبيع`G`إلى`~N(0, 1)`عبر اللحظة قبل أن تضاعف ب `∇ log π`. . .
  **梯度爆炸。**الإعلام قد يكون كبير جداً`∇ log π`قبل أن ينتهي`G`归一化到 `~N(0, 1)`.
- **Entropy collapse.**السياسة تتحرك نحو عمل تقريب القرار مبكراً جداً، وتوقف عن الاستكشاف، وتعلق.`β · H(π(·|s))`إلى الهدف
  **熵坍缩。**策略过早收到近确定性动作,停止探索,陷入困境──修复:向目标添加奖励 `β · H(π(·|s))`.
- **High variance.**تحتاج فانيلا رينفورس إلى آلاف الحلقات. خط أساسي للنقد (درس 07) أو منطقة الثقة في TRPO/PPO (درس 08) هو الإصلاح القياسي.
  **高方差。**المواجهة الأولى: التركيز على التنمية والتنمية
- **Sample inefficiency.**على السياسة يعني أنك ترمي كل انتقال بعد تحديث واحد. التصحيحات خارج السياسة عن طريق أخذ العينات الأهمية تجلب البيانات، على تكلفة التباين (نسبة الـPPO هي وزن IS المقلد).
  **样本效率低。**استراتيجية على الإنترنت تعني التخلص من كل تحويل بعد كل تحديث.
- **Non-stationary gradients.**نفس التراجع من 100 حلقة مضت يستخدم القديم`π`أساليب السياسة تحديث كل عدد قليل من التنفيذ لهذا السبب.
  **非平稳梯度。**100 回合前的梯度使用旧的 `π`                                                                                                                                                                                                                                                              
- **Credit assignment.**بدون مكافأة للذهاب، مكافآت سابقة تساهم في الضوضاء.
  **信用分配。**没有未来回报,过去的奖励贡献噪声──始终使用未来回报──

## استخدمها في إطار التنفيذ

في عام 2026، نادراً ما يتم تشغيل REINFORCE مباشرة ولكن صيغة تراجعها موجودة في كل مكان:

> 2026 سنة، رينفورس  قليل مباشرة للعمل، ولكن عدة عدة عدة عدة

| Use case | Derived method |
|----------|---------------|
| Use case / 用例 | Derived method / 派生方法 |
| Continuous control / 连续控制 | PPO / SAC with Gaussian policy / 高斯策略的 PPO/SAC |
| LLM RLHF / LLM RLHF | PPO with KL penalty, running on token-level policy / 带 KL 惩罚的 PPO，token 级策略 |
| LLM reasoning (DeepSeek) / LLM 推理 | GRPO — REINFORCE with group-relative baseline, no critic / 组相对基线的 REINFORCE，无 critic |
| Multi-agent / 多智能体 | Centralized-critic REINFORCE (MADDPG, COMA) / 集中 critic 的 REINFORCE |
| Discrete action robotics / 离散动作机器人 | A2C, A3C, PPO |
| Preference-only settings / 仅偏好设置 | DPO — REINFORCE rewritten as a preference-likelihood loss, no sampling / 重写为偏好似然损失的 REINFORCE |

عندما تقرأ`loss = -advantage * log_prob`في نص تدريب 2026، وهذا هو REINFORCE مع خط أساسي. الأوراق الكاملة (DPO، GRPO، RLOO) هي خدوش تقليل التباين فوق هذا الخط واحد.

> عندما تقرأ في كتاب التدريب لعام 2026`loss = -advantage * log_prob`,ذلك هو إعادة تعزيز خط الأساس.

## أرسلها .

إبقوا`outputs/skill-policy-gradient-trainer.md`:

```markdown
---
name: policy-gradient-trainer
description: Produce a REINFORCE / actor-critic / PPO training config for a given task and diagnose variance issues.
version: 1.0.0
phase: 9
lesson: 6
tags: [rl, policy-gradient, reinforce]
---

Given an environment (discrete / continuous actions, horizon, reward stats), output:

1. Policy head. Softmax (discrete) or Gaussian (continuous) with parameter counts.
2. Baseline. None (vanilla), running mean, learned `V̂(s)`, or A2C critic.
3. Variance controls. Reward-to-go on by default, return normalization, gradient clip value.
4. Entropy bonus. Coefficient β and decay schedule.
5. Batch size. Episodes per update; on-policy data freshness contract.

Refuse REINFORCE-no-baseline on horizons > 500 steps. Refuse continuous-action control with a softmax head. Flag any run with `β = 0` and observed policy entropy < 0.1 as entropy-collapsed.
```

## تمارين التدريب

1. **Easy.**تنفيذ REINFORCE على 4 × 4 GridWorld مع سياسة softmax خطية. تدريب لمدة 1000 حلقة دون خط أساسي. رسم منحنى التعلم؛ قياس التباين (std من العائدات).
2. **Medium.**إضافة خط أساسي متوسط التشغيل، تدريب مرة أخرى، مقارنة كفاءة العينة والتشابه مع الجري من الفانيليا. كم يقلل خط أساسي الخطوات إلى التقارب؟
3. **Hard.**إضافة إضافة إضافية للإنتروبيا `β · H(π)`- أُسحّر`β ∈ {0, 0.01, 0.1, 1.0}`الخطة النهائية العودة والسياسة الانتروبية أين هو نقطة اللطيفة في هذه المهمة؟

## شروط الرئيسية

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Policy gradient | "Train the policy directly" / 策略梯度 | `∇J(θ) = E[G · ∇ log π_θ(a\|s)]`; derived from the log-derivative trick. |
| REINFORCE | "The original PG algorithm" / REINFORCE算法 | Williams (1992); Monte Carlo returns multiplied by log-policy gradient. |
| Log-derivative trick | "Score function estimator" / 对数导数技巧 | `∇P(τ;θ) = P(τ;θ) · ∇ log P(τ;θ)`; makes gradients of expectations tractable. |
| Baseline | "Variance reduction" / 基线 | Any `b(s)` subtracted from `G`; unbiased because `E[b · ∇ log π] = 0`. |
| Reward-to-go | "Only future returns count" / 未来回报 | `G_t^{from t}` instead of the full `G_0`; correct and lower-variance. |
| Entropy bonus | "Encourage exploration" / 熵正则化 | `+β · H(π(·\|s))` term keeps the policy from collapsing. |
| On-policy | "Train on what you just saw" / 在线策略 | Gradient expectation is w.r.t. the current policy — cannot reuse old data directly. |
| Advantage | "How much better than average" / 优势函数 | `A(s, a) = G(s, a) - V(s)`; the signed quantity REINFORCE-with-baseline multiplies. |

## المزيد من القراءة

- [Williams (1992). Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning](https://link.springer.com/article/10.1007/BF00992696)ورقة REINFORCE الأصلية
- [Sutton et al. (2000). Policy Gradient Methods for Reinforcement Learning with Function Approximation](https://papers.nips.cc/paper_files/paper/1999/hash/464d828b85b0bed98e80ade0a5c43b0f-Abstract.html)النظريه الحديثة للسياسة-المركز مع التقريب الوظيفي.
- [Sutton & Barto (2018). Ch. 13 — Policy Gradient Methods](http://incompleteideas.net/book/RLbook2020.pdf) عرض الكتب المدرسية
- [OpenAI Spinning Up — VPG / REINFORCE](https://spinningup.openai.com/en/latest/algorithms/vpg.html) التعليم التربوي الواضح مع رمز PyTorch.
- [Peters & Schaal (2008). Reinforcement Learning of Motor Skills with Policy Gradients](https://homes.cs.washington.edu/~todorov/courses/amath579/reading/PolicyGradient.pdf) تقليل التباين والنظرية الطبيعية-المركزية التي تربط REINFORCE مع عائلة منطقة الثقة (TRPO، PPO).
