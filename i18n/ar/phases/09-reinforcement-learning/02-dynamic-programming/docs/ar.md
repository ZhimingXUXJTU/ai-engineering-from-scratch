# التخطيط الديناميكي  التكرار السياسي وتكرار القيمة  التخطيط الحركي  الاستراتيجيات  التكرار والقيم  التكرار

> البرمجة الديناميكية هي RL مع الغش. أنت تعرف بالفعل وظائف الانتقال والمكافأة؛ أنت فقط تكرر معادلة بيلمان حتى `V`أو`π`إنه المعيار الذي تحاول كل طريقة تستند إلى العينات.

> **【中文解读】**动态规划是强化学习的"作弊版"你已知环境的转移概率和奖励函数,只需反复代贝尔曼方程直到收──它是所有采样方法的"金标准" Q-learning、PPO等) 参照──

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 01 (MDPs) | **前置知识:** Phase 9 · 01 (MDP)
**Time:** ~75 minutes | **时间:** ~75 分钟

## المشكلة المشكلة المشكلة

لديك MDP مع نموذج معروف: يمكنك استفسار `P(s' | s, a)`و`R(s, a, s')`لجميع أزواج الحالة. مدير المخزون يعرف توزيع الطلب. لعبة اللوحة لديها انتقالات تحديدية. عالم الشبكة هو أربعة خطوط من بيثون. لديك * نموذج *.

> لديك نموذج معروف من MDP: يمكنك استفسار أي حالة-تحركات على`P(s' | s, a)`和 `R(s, a, s')` مدير المخزون يعرف الاحتياجات الموزعة‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬

تم اختراع RL الخالية من النموذج (Q-learning ، PPO ، REINFORCE) للحالة التي لا يكون لديك نموذج  يمكنك فقط أخذ عينات من البيئة. ولكن عندما يكون لديك واحد ، هناك أساليب أسرع وأفضل: البرمجة الديناميكية. صممها بيلمان في عام 1957. لا يزالون يحددون الصواب: عندما يقول الناس "سياسة مثالية لهذا MDP ،" يعنيون أن السياسة DP ستعود.

> 无模型 RL(Q-learning、PPO、REINFORCE) هو وضع تم اختراعه من دون نموذج you can only sample from the environment‬ ولكن عندما يكون لديك نموذج، هناك طريقة أسرع وأفضل: التخطيط الحركي‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬

> **【中文解读】**عندما تعرف نموذج بيئي (((تحول احتمالية و وظيفة مكافأة) ، يمكن تحديد التخطيط الحركي للحصول على أفضل استراتيجية.

> **【拓展：AlphaZero/MCTS】**البحث عن الشجرة المتحركة (MCTS) في الأساس هو نسخة مختلفة من بيلمان الاحتياطيات في البحث عن الشجرةالعمل التغير في الشجرة.

تحتاج إليها في عام 2026 لثلاث أسباب. أولاً، يتم حل كل بيئة جدولية في أبحاث RL (GridWorld، FrozenLake، CliffWalking) مع DP لإنتاج سياسة معيار الذهب. ثانياً، القيم الدقيقة تسمح لك * إزالة * أساليب العينات: إذا كان تقدير Q-تعلم ل `V*(s_0)`يختلف مع إجابة DP بنسبة 30% ، فإن Q-learning لديك خطأ. ثالثًا ، فإن أساليب التخطيط والتنظيم الحديثة غير المتعلقة بالإنترنت (MCTS ، البحث في AlphaZero ، RL القائمة على النموذج في المرحلة 9 · 10) كلها تكرر نسخة احتياطية Bellman على النموذج المعلم أو المقدم.

> أنت في 2026 سنة تحتاج إليها، السبب هناك ثلاثة. أولا، ريل في كل جدول من البيئة البحثية ((GridWorld、FrozenLake、CliffWalking) كل استخدام دبي البحث لإنتاج استراتيجية المعيار الذهبية.`V*(s_0)`التقديرات مع DP 答案差 30%, Q-علمك على وجود حذاء.

## المفهوم الأساسي

![Policy iteration and value iteration, side by side](../assets/dp.svg)

**Two algorithms, both fixed-point iteration on Bellman.**

> **两种算法，都是对 Bellman 方程做不动点迭代。**

> **【中文解读】**两种算法都是对贝尔曼方程做不动点代――策略代:交替执行"策略评估"和"策略改进"直到策略不变;值代:将两者合并为一步,直接取 max――两者最终收到同一个最优值函数 V*。

**Policy iteration.**يتناوب خطوتين حتى تتوقف السياسة عن التغيير

> **策略迭代。**交替执行两个步骤直到策略不再改变──

1. *التقييم:* السياسة المقدمة `π`، الحساب`V^π`من خلال تطبيقها مراراً وتكراراً`V(s) ← Σ_a π(a|s) Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`حتى يتقارب
   * تقييم:* 给定策略 `π`، وكرر تطبيق بيلمان 方程 حتى `V^π`-أجل
2. *تحسين:* تم إعطائه `V^π`, جعل`π`الشريعون`V^π`: `π(s) ← argmax_a Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`. . .
   *改进:* 给定 `V^π`،让 `π`على`V^π`贪心──

يتم ضمان التقارب لأن (أ) كل خطوة تحسين إما تحافظ على`π`نفس أو زيادة صارمة `V^π`بالنسبة لبعض الدول، (ب) مساحة السياسات التحديدية محدودة. عادة ما تتقارب في ~ 520 التكرارات الخارجية حتى بالنسبة إلى مساحات الدولة الكبيرة.

> الإستجابة مؤكدة لأن كل تحسين يجب أن يتم`π`لا يتغير، أو يجب أن تزيد بشكل صارم من حالة`V^π`، ((ب) 确定性策略空间是有限的. حتى بالنسبة لمجال الحالة الكبيرة، عادة ما تحتاج فقط ~5-20 مرات للطبقة الخارجية.

**Value iteration.**ينهار التقييم والتحسين إلى صفعة واحدة. تطبيق معادلة بيلمان * الإيجابية *:

`V(s) ← max_a Σ_{s',r} P(s',r|s,a) [r + γ V(s')]`

كرر حتى`max_s |V_{new}(s) - V(s)| < ε`. استخراج السياسة في النهاية عن طريق اتخاذ الإجراء الطموح. أسرع بشكل صارم لكل إعادة التكرار  لا يوجد حلول تقييم داخلي  ولكن عادة ما تحتاج إلى المزيد من الإعادة التكرارية للتقارب.

> **值迭代。**سوف تقوم بتقييم وتحسين المجموعة لمراجعة واحدة. تطبيق بيلمان *أفضل نوعية* طريقة.

**Generalized policy iteration (GPI).**الإطار الموحد. يتم حبس وظيفة القيمة والسياسة في حلقة تحسين متجهين. أي طريقة تدفع كلا نحو التوافق المتبادل (تكرار القيمة غير المزامنة، وتكرار السياسة المعدلة، Q-التعلم، الممثل-النقاد، PPO) هي مثال على GPI.

> **【拓展：GPI→PPO/RLHF】**广义策略代 (GPI) هو الإطار الموحد: Q-learning、Actor-Critic、PPO في الأساس كلها مثال على GPI── فهمت GPI دبي، أنت على الفور فهمت فلسفة التصميم للدورة التدريبية RLHF ChatGPT 背后──

**Why `γ < 1` matters.**عامل بيلمان هو`γ`-التقلص في القاعدة السائدة:`||T V - T V'||_∞ ≤ γ ||V - V'||_∞`. التقلص يعني نقطة ثابتة و تقارب هندسي فريدة من نوعها.`γ < 1`و أنت تفقد الضمان تحتاج إلى أفق محدود أو حالة نهاية امتصاص

> **为什么 `γ < 1` 很重要。**بيلمان 算子 فى ظل النسبة`γ`- الضغط المخطوطة. الضغط يعني انقطاع واحد و كيفية الاستخدام.`γ < 1`لقد فقدت ضمانات أنك تحتاج إلى رؤية محدودة أو وضع إيقاف التدخين

## بناء ذلك تحرك لتحقيق
```figure
value-iteration-gamma
```

## بناءها

### الخطوة الأولى: بناء نموذج GridWorld MDP

استخدم نفس 4 × 4 GridWorld من الدروس 01. نضيف إختلاف استوكاستيك: مع احتمال `0.1`الوكيل ينزلق في اتجاه عمودي عشوائي

> استخدام دراسة 01 في نفس 4 × 4 شبكة العالم.`0.1`智能体会滑向随机垂直方向──

```python
SLIP = 0.1

def transitions(state, action):
    if state == TERMINAL:
        return [(state, 0.0, 1.0)]
    outcomes = []
    for direction, prob in action_probs(action):
        outcomes.append((apply_move(state, direction), -1.0, prob))
    return outcomes
```

`transitions(s, a)`يعود قائمة `(s', r, p)`هذا هو النموذج بأكمله

> `transitions(s, a)`عودتي`(s', r, p)`列表──هذا هو النموذج بأكمله──

### الخطوة الثانية: تقييم السياسات

نظراً لسياسة`π(s) = {action: prob}`، أعيد تعاديل معادلة بيلمان حتى `V`يتوقف عن التحرك:

> 给定策略 `π(s) = {action: prob}`, 代 بيلمان 方程 حتى `V`غير متغير:

```python
def policy_evaluation(policy, gamma=0.99, tol=1e-6):
    V = {s: 0.0 for s in states()}
    while True:
        delta = 0.0
        for s in states():
            v = sum(pi_a * sum(p * (r + gamma * V[s_prime])
                              for s_prime, r, p in transitions(s, a))
                   for a, pi_a in policy(s).items())
            delta = max(delta, abs(v - V[s]))
            V[s] = v
        if delta < tol:
            return V
```

### الخطوة الثالثة: تحسين السياسات

استبدل`π`مع السياسة الطموحة w.r.t.`V`إذا`π`لم يتغير، العودة نحن في المثالي.

> ستعمل`π`بدل لـ`V`贪心的策略──如果 `π`لا تغير، العودة إلى أفضل ما يمكن

```python
def policy_improvement(V, gamma=0.99):
    new_policy = {}
    for s in states():
        best_a = max(
            ACTIONS,
            key=lambda a: sum(p * (r + gamma * V[s_prime])
                              for s_prime, r, p in transitions(s, a)),
        )
        new_policy[s] = best_a
    return new_policy
```

### الخطوة الرابعة: خياطهما معاً

```python
def policy_iteration(gamma=0.99):
    policy = {s: "up" for s in states()}   # arbitrary start
    for _ in range(100):
        V = policy_evaluation(lambda s: {policy[s]: 1.0}, gamma)
        new_policy = policy_improvement(V, gamma)
        if new_policy == policy:
            return V, policy
        policy = new_policy
```

التقارب النموذجي على 4 × 4: 46 التكرارات الخارجية.`V*(0,0) ≈ -6`و سياسة تقلل صارمة من عدد الخطوات

> 4×4 上的典型收:4-6 次外层代──输出 `V*(0,0) ≈ -6`و استراتيجية تقليل عدد الخطوات

### الخطوة 5: التكرار القيم (إصدار حلقة واحدة)

```python
def value_iteration(gamma=0.99, tol=1e-6):
    V = {s: 0.0 for s in states()}
    while True:
        delta = 0.0
        for s in states():
            v = max(sum(p * (r + gamma * V[s_prime])
                       for s_prime, r, p in transitions(s, a))
                   for a in ACTIONS)
            delta = max(delta, abs(v - V[s]))
            V[s] = v
        if delta < tol:
            break
    policy = policy_improvement(V, gamma)
    return V, policy
```

نفس النقطة الثابتة، أقل خطات من الرمز.

> نفس النقطة غير متحركة، أقل عدد من أشكال الكود.

## الفخاخ

- **Forgetting to handle terminals.**إذا وضعت بيلمان في حالة امتصاص، فإنه لا يزال يلتقط "أفضل عمل" الذي لا يغير أي شيء.`if s == terminal: V[s] = 0`. . .
  **忘记处理终止状态。**إذا تطبق على حالة استيعاب بيلمان، فإنه سيظل يختار "أفضل تحرك" ولكن لا شيء يتغير.`if s == terminal: V[s] = 0`الحماية
- **Sup-norm vs L2 convergence.**استخدام`max |V_new - V|`الضمان النظري هو على القاعدة السائدة
  **Sup 范数 vs L2 收敛。**استخدام `max |V_new - V|`والتي لا تعتبر متوسطا.
- **In-place vs synchronous updates.**تحديث`V[s]`في مكان (غوس-سايدل) يتقارب أسرع من منفصل `V_new`(جاكوبي) رمز الإنتاج يستخدم في المكان
  **原地更新 vs 同步更新。**أحدث`V[s]`(غاوس-سايدل) مقارنة مع منفصلة`V_new`字典(Jacob)收更快──生产代码使用原地更新──
- **Policy ties.**إذا كانت اثنين من الأعمال لها قيمة Q متساوية،`argmax`قد يقطع الروابط بشكل مختلف في كل تكرار، مما يسبب تذبذب في عملية التحقق من "استقرار السياسة". استخدم وقف الربط المستقر (الفعال الأول في ترتيب ثابت).
  **策略平局。**إذا كانت قيمة Q من اثنين من الحركات`argmax`كل مرة يمكن أن تقطع المواصفات بطريقة مختلفة، مما يؤدي إلى "تكتيكات ثابتة" التزج.
- **State-space explosion.**دبي هو`O(|S| · |A|)`يعمل حتى ~ 107 حالة. وبالإضافة إلى ذلك، تحتاج إلى تقريب الوظيفة (المرحلة 9 · 05 وما بعدها).
  **状态空间爆炸。**كل مسح`O(|S| · |A|)`△ تطبق على حوالي 107 个状态──超出这个范围需要函数近似(Phase 9 · 05 起)

## استخدمها في إطار التنفيذ

في عام 2026، فإن DP هي خط الأساس للصواب والحلقة الداخلية للمخططين:

> 2026، دبي هو الدورة الداخلية للخطوط والمنظمين:

| Use case | Method |
|----------|--------|
| Use case / 用例 | Method / 方法 |
| Solve a small tabular MDP exactly / 精确求解小型表格 MDP | Value iteration (simpler) or policy iteration (fewer outer steps) / 值迭代（更简单）或策略迭代（更少外层步数） |
| Verify a Q-learning / PPO implementation / 验证 Q-learning/PPO 实现 | Compare to DP-optimal V* on a toy environment / 在玩具环境上与 DP 最优 V* 比较 |
| Model-based RL (Phase 9 · 10) / 基于模型的 RL | Bellman backup on a learned transition model / 在学习的转移模型上做 Bellman 备份 |
| Planning in AlphaZero / MuZero / AlphaZero/MuZero 中的规划 | Monte Carlo Tree Search = async Bellman backup / MCTS = 异步 Bellman 备份 |
| Offline RL (CQL, IQL) / 离线 RL | Conservative Q-iteration — DP with a penalty on OOD actions / 保守 Q 迭代——对 OOD 动作加惩罚的 DP |

كلما قال شخص ما "العمل القيمة المثلى" ، يعنى "نقطة DP ثابتة". عندما ترى `V*`أو`Q*`في ورقة، تخيل هذه الحلقة.

> كلما قال أحدهم "أفضل قيمة وظيفة" ، كانوا يشيرون إلى "DP غير متحرك"`V*`أو`Q*`فكر في هذه الدورة

## أرسلها .

إبقوا`outputs/skill-dp-solver.md`:

```markdown
---
name: dp-solver
description: Solve a small tabular MDP exactly via policy iteration or value iteration. Report convergence behavior.
version: 1.0.0
phase: 9
lesson: 2
tags: [rl, dynamic-programming, bellman]
---

Given an MDP with a known model, output:

1. Choice. Policy iteration vs value iteration. Reason tied to |S|, |A|, γ.
2. Initialization. V_0, starting policy. Convergence sensitivity.
3. Stopping. Sup-norm tolerance ε. Expected number of sweeps.
4. Verification. V*(s_0) computed exactly. Greedy policy extracted.
5. Use. How this baseline will be used to debug/evaluate sampling-based methods.

Refuse to run DP on state spaces > 10⁷. Refuse to claim convergence without a sup-norm check. Flag any γ ≥ 1 on an infinite-horizon task as a guarantee violation.
```

## تمارين التدريب

1. **Easy.**إدارة التكرار القيمة على شبكة 4 × 4 العالم مع `γ ∈ {0.9, 0.99}`كم عدد المراقبين حتى`max |ΔV| < 1e-6`طباعة`V*`كشبكة 4 × 4.
   > **练习1：**باستخدام عوامل مختلفة منخفضة  运行值代, observar 收速度 كيف  变化
2. **Medium.**مقارنة التكرار السياسة مقابل التكرار القيم على الشبكة التجاري * ستوكاستيك * (احتمال التزلج `0.1`العد: المصفحات، ساعة الحائط، النهائي `V*(0,0)`أيّها يتقارب أسرع في التكرار؟
   > **练习2：**مقارنة استراتيجية代和值代在随机网格世界中的收速度代次数和运行时间) 
3. **Hard.**إعداد تكرار سياسة معدلة: في خطوة التقييم، تشغيلها فقط `k`يُسحف بدلاً من التناغم`V*(0,0)`خطأ vs`k`لـ`k ∈ {1, 2, 5, 10, 50}`ماذا يخبرك المنحنى عن التداول بين التقييم والتحسين؟
   > **练习3：**                                                                                                                                                                                                                                                              

## شروط الرئيسية

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Policy iteration | "DP algorithm" / 策略迭代 | Alternating evaluation (`V^π`) and improvement (greedy `π` w.r.t. `V^π`) until the policy stops changing. |
| Value iteration | "Faster DP" / 值迭代 | Bellman optimality backup applied in one sweep; converges to `V*` geometrically. |
| Bellman operator | "The recursion" / Bellman 算子 | `(T V)(s) = max_a Σ P (r + γ V(s'))`; a `γ`-contraction in sup-norm. |
| Contraction | "Why DP converges" / 压缩映射 | Any operator `T` with `\|\|T x - T y\|\| ≤ γ \|\|x - y\|\|` has a unique fixed point. |
| GPI | "Everything is DP" / 广义策略迭代 | Generalized Policy Iteration: any method driving `V` and `π` to mutual consistency. |
| Synchronous update | "Jacobi-style" / 同步更新 | Use old `V` throughout a sweep; cleanly analyzable but slower. |
| In-place update | "Gauss-Seidel-style" / 原地更新 | Use `V` as it's being updated; converges faster in practice. |

## المزيد من القراءة

- [Sutton & Barto (2018). Ch. 4 — Dynamic Programming](http://incompleteideas.net/book/RLbook2020.pdf) العرض القنوني للتكرار السياسي وتكرار القيمة.
- [Bertsekas (2019). Reinforcement Learning and Optimal Control](http://www.athenasc.com/rlbook.html) التعامل الصارم مع حجج خريطة التقلص.
- [Puterman (2005). Markov Decision Processes](https://onlinelibrary.wiley.com/doi/book/10.1002/9780470316887) تكرار السياسة المعدل وتحليل التقارب.
- [Howard (1960). Dynamic Programming and Markov Processes](https://mitpress.mit.edu/9780262582300/dynamic-programming-and-markov-processes/)ورقة التكرار الأصلية للسياسة.
- [Bertsekas & Tsitsiklis (1996). Neuro-Dynamic Programming](http://www.athenasc.com/ndpbook.html)الجسر من دبي إلى تقريبي دبي / عميق RL المستخدم في كل درس لاحقا.
