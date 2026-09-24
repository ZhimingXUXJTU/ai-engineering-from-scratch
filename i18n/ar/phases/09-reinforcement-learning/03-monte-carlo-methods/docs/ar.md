# أساليب مونت كارلو  تعلم من الحلقات الكاملة  أساليب مونت كارلو  تعلم من الحلقة الكاملة

> البرمجة الديناميكية تحتاج إلى نموذج. مونت كارلو لا تحتاج سوى الحلقات. تشغيل السياسة، مشاهدة العائدات، متوسطها. الأسهل فكرة في RL  والتي تفتح كل شيء أسفل التيار.

> **【中文解读】**动态规划需要已知环境模型,蒙特卡洛只需要完整回合数据:执行策略、观测回报、取平均──这是最简单的思想在RL中,也是所有后续算法的基石.

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 01 (MDPs), Phase 9 · 02 (Dynamic Programming) | **前置知识:** Phase 9 · 01 (MDP), Phase 9 · 02 (动态规划)
**Time:** ~75 minutes | **时间:** ~75 分钟

## المشكلة المشكلة المشكلة

البرمجة الديناميكية هي جميلة، ولكن يفترض أنه يمكنك استفسار`P(s' | s, a)`لا يمكن للروبوت تحليلًا لتوزيع بيكسلات الكاميرا بعد محركة مشتركة. لا يمكن ل خوارزمية التسعير أن تتكامل مع كل رد فعل محتمل للعميل. لا يمكن لشركة التسليم المختلف للاستمرار في جميع المواصلات الممكنة بعد رمز.

> التخطيط الحالي رائع، لكن افترض أنه يمكنك استفسار كل حالة و تحركات`P(s' | s, a)`◊ في الواقع لا يوجد تقريبا شيء يعمل هكذا ◊ الآلات لا يمكن تحديد حسابات التوزيع للقطاع بعد الصورة ◊ الجهاز التقييم لا يمكن أن تجاوب كل من الممكن العملاء ردود الفعل ◊ LLM لا يمكن أن يذكر الرمز ◊ بعد كل من الممكن الإتفاق ◊

تحتاج إلى طريقة لا تحتاج إلا إلى القدرة على * أخذ عينات * من البيئة. تنفيذ السياسة. الحصول على مسار`s_0, a_0, r_1, s_1, a_1, r_2, …, s_T`استخدمها لتقدير القيم هذا مونت كارلو

> تحتاج إلى طريقة فقط تحتاج إلى طريقة من البيئة`s_0, a_0, r_1, s_1, a_1, r_2, …, s_T`استخدمها لتقييم القيمة هذا ما هو مونت كارلو

التحول من DP إلى MC مهم فلسفيا: نقوم بالانتقال من * النموذج المعروف + النسخة الاحتياطية الدقيقة * إلى * التنفيذات المعدنية + العائد المتوسط *. يرتفع التباين ، ولكن التطبيق يتفجر. كل خوارزمية RL بعد هذه الدروس  TD ، Q-learning ، REINFORCE ، PPO ، GRPO  هي تقدير مونت كارلو في قلبها ، في بعض الأحيان مع إطلاق التطبيقات على الطوابق فوق.

> تحول من DP إلى MC مهم في الفلسفة: نحن من * نموذج معروف + احتياطات دقيقة * تحول * نموذج الاطلاق + متوسط العائدات * فوارس زادت ، ولكن نطاق التطبيق ارتفع بشكل متفجري.

> **【中文解读】**من DP إلى MC التحويل الأساسي: من "الموديل المعروف+حسابات الدقيقة" إلى "مجموعة المسارات+ متوسط العائدات"‬الفرق زاد، ولكن نطاق الاستخدام توسع بشكل متفجرات‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬

> **【拓展：LLM中的MC】**في تدريب ChatGPT RLHF ، يتم اختيار العديد من الإجابات على كل طلب  حساب متوسط المكافأة هذا هو التطبيق المباشر لـ MC 思想 في تدريب الموديل الكبير。

## المفهوم الأساسي

![Monte Carlo: rollout, compute returns, average; first-visit vs every-visit](../assets/monte-carlo.svg)

**The core idea, in one line:** `V^π(s) = E_π[G_t | s_t = s] ≈ (1/N) Σ_i G^{(i)}(s)`أين`G^{(i)}(s)`تُلاحظ العوائد بعد زيارات `s`في سياسة`π`. . .

> **核心思想，一行概括：** `V^π(s) = E_π[G_t | s_t = s] ≈ (1/N) Σ_i G^{(i)}(s)`، من بينهم`G^{(i)}(s)`هو في استراتيجية`π`下访问 `s`时观测到的回报──

> **【中文解读】**مركز MC  تقييم: قيمة الحالة = متوسط قيمة العودة التي تم رصدها خلال هذه الحالة.`V_new = V_old + α(target - V_old)`من MC إلى TD إلى جميع الحاليات الـ RL

**First-visit vs every-visit MC.**نظراً للفصل الذي يزور الولاية`s`في العديد من المرات، MC الزيارة الأولى تعتبر فقط العودة من الزيارة الأولى؛ كل زيارة MC تعتبر جميع الزيارات. كلاهما غير متحيز في الحد. الزيارة الأولى أسهل لتحليل (معاكرات iid). كل زيارة تستخدم المزيد من البيانات لكل حلقة وعادة ما تتقارب أسرع في الممارسة.

> **首次访问 vs 每次访问 MC。**عطى حالة زيارة أكثر`s`في المجموعة الأولى، العودة الأولى إلى المجموعة الأولى فقط حساب العودة الأولى إلى المجموعة الأولى؛ في المجموعة الأولى، العودة الأولى إلى المجموعة الأولى.

**Incremental mean.**بدلاً من تخزين جميع العائدات، قم بتحديث المتوسط التشغيلي:

`V_n(s) = V_{n-1}(s) + (1/n) [G_n - V_{n-1}(s)]`

إعادة تنظيم: `V_new = V_old + α · (target - V_old)`مع`α = 1/n`. تغيير`1/n`لـ (حجم خطوة ثابت)`α ∈ (0, 1)`و تحصل على مقياس MC غير ثابت الذي يتبع التغيرات في`π`هذه الخطوة هي قفزة كاملة من MC إلى TD إلى كل خوارزمية RL الحديثة.

> **增量均值。**لا تخزين كل العائدات، بل تحديث متوسط النشاط`1/n`替换为常数步长 `α ∈ (0, 1)`-حصل على متابعة`π`غيرات غير متساوية  MC  تقييمات ‬ هذا الخطوة هي قفزة كاملة من MC إلى TD إلى جميع الالتحديدات الحديثة ‬ الالتحديدات ‬

**Exploration is now a problem.**و"دي بي" لمست كل ولاية من خلال الإحصاءات، و"إم سي" ترى فقط الدول الزيارات السياسية.`π`إنّها تحديدية، لا يتمّ أخذ عينات على مناطق كاملة من مساحة الدولة، وتقديرات قيمتها تبقى عند الصفر إلى الأبد.

> **探索现在成了问题。**دبي 通过枚举触及每个状态──MC فقط يمكن أن ترى استراتيجية访问的状态──如果`π`هو مؤكد، أن منطقة كاملة من المجال الحالي لن يتم أخذها أبدا، وتقدير قيمتها إلى الأبد إلى صفر.

> **【中文解读】**探索问题:DP 能遍历所有状态,MC فقط يمكن أن ترى الاستراتيجية وزارت الحالة.

1. **Exploring starts.**تبدأ كل حلقة من زوج عشوائي (ات) يضمن تغطية؛ غير واقعي في الممارسة العملية (لا يمكنك "إعادة تعيين" الروبوت إلى حالة تعسفية).
   **探索起点。**كل إعادة من أي وقت مضى إلى أي حال
2. **ε-greedy.**تصرف طمعية في ق ق الحالي، ولكن مع احتمال`ε`اختر عمل عشوائي جميع أزواج الحالة يتم أخذ عينات بشكل غير متزامن
   **ε-贪心。**على حالية Q 贪心行动، ولكن على احتمالية `ε`随机选动作──所有状态动作对渐近地被采样──
3. **Off-policy MC.**جمع البيانات بموجب سياسة السلوك`μ`، تعلم عن السياسة المستهدفة`π`الاختلافات عالية، ولكنها هي الجسر إلى طرق التعبير مثل DQN
   **离策略 MC。**في استراتيجية السلوك`μ` جمع البيانات من خلال أهمية تلقاء الأهداف`π`الفرق العالي، ولكن هو طريق إلى DQN 等回放缓冲方法的桥梁。

**Monte Carlo Control.**تقييم → تحسين → تقييم، تماما مثل التكرار السياسي، ولكن التقييم يعتمد على أخذ العينات:

1. أركض`π`، احصل على حلقة.
2. تحديث `Q(s, a)`من العائدات الملاحظة
3. - أفعلها`π`الـ طمع`Q`. . .
4. أكرر

يتحرك إلى`Q*`و`π*`مع احتمال 1 في ظروف خفيفة (كل زوج زيارة في كثير من الأحيان ،`α`يرضي (روبينز مونرو)

> **蒙特卡洛控制。**评估 → 改进 → 评估,就像策略代, ولكن التقييم على أساس الاختبار.`α`(تلبية (روبينز-مونرو) ، على الأرجح 1`Q*`和 `π*`.

## بناء ذلك تحرك لتحقيق
```figure
epsilon-greedy
```

## بناءها

### الخطوة الأولى: الإرسال → قائمة (s، a، r)

```python
def rollout(env, policy, max_steps=200):
    trajectory = []
    s = env.reset()
    for _ in range(max_steps):
        a = policy(s)
        s_next, r, done = env.step(s, a)
        trajectory.append((s, a, r))
        s = s_next
        if done:
            break
    return trajectory
```

لا نموذج، فقط`env.reset()`و`env.step(s, a)`نفس الواجهة مثل بيئة رياضية ولكن تم تجريدها

> لا تحتاج إلى نموذج، فقط تحتاج`env.reset()`和 `env.step(s, a)` مع صالة الرياضة  المواجهة البيئية نفسها ولكن أكثر تبسيطا

### الخطوة الثانية: إرجاع الحساب (التصفية العكسية)

```python
def returns_from(trajectory, gamma):
    returns = []
    G = 0.0
    for _, _, r in reversed(trajectory):
        G = r + gamma * G
        returns.append(G)
    return list(reversed(returns))
```

مرّة واحدة،`O(T)`التكرار الراجع`G_t = r_{t+1} + γ G_{t+1}`يتجنب إعادة جمع.

> مرة واحدة`O(T)` العكس`G_t = r_{t+1} + γ G_{t+1}`避免了重复求和──

### الخطوة الثالثة: تقييم المملكة العربية المتحدة في الزيارة الأولى

```python
def mc_policy_evaluation(env, policy, episodes, gamma=0.99):
    V = defaultdict(float)
    counts = defaultdict(int)
    for _ in range(episodes):
        trajectory = rollout(env, policy)
        returns = returns_from(trajectory, gamma)
        seen = set()
        for t, ((s, _, _), G) in enumerate(zip(trajectory, returns)):
            if s in seen:
                continue
            seen.add(s)
            counts[s] += 1
            V[s] += (G - V[s]) / counts[s]
    return V
```

ثلاث خطوط تقوم بالعمل: علامة حالة كما هو مرر على الزيارة الأولى، عدد الزيادة، تحديث متوسط التشغيل.

> 三行代码完成工作:标记首次访问的状态,增加计数,更新运行平均值──

### الخطوة الرابعة: إضفاء الضوابط على المجموعة المتحركة (على السياسة)

```python
def mc_control(env, episodes, gamma=0.99, epsilon=0.1):
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})
    counts = defaultdict(lambda: {a: 0 for a in ACTIONS})

    def policy(s):
        if random() < epsilon:
            return choice(ACTIONS)
        return max(Q[s], key=Q[s].get)

    for _ in range(episodes):
        trajectory = rollout(env, policy)
        returns = returns_from(trajectory, gamma)
        seen = set()
        for (s, a, _), G in zip(trajectory, returns):
            if (s, a) in seen:
                continue
            seen.add((s, a))
            counts[s][a] += 1
            Q[s][a] += (G - Q[s][a]) / counts[s][a]
    return Q, policy
```

### الخطوة 5: مقارنة مع معيار الذهب DP

تقديرات المجلس الوطني`V^π`يجب أن توافق مع نتيجة DP من الدروس 02 كحلقات → ∞. في الممارسة العملية: 50,000 حلقة على 4×4 GridWorld يجعلك في غضون `~0.1`من إجابة DP.

> أنت على`V^π`∞ 时应与课2的 DP 结果一致──实践中:4×4 GridWorld 上 50,000 回合可将误差控制在 ∞ 时应与课2的 DP 结果一致──实践中:4×4 GridWorld 上 50,000 回合可将误差控制在 ∞ ∞ 时应与课2的 DP 结果一致──实践中:4×4 GridWorld 上 50,000 回合可将误差控制在 ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ ∞ `~0.1`فى الداخل

## الفخاخ

- **Infinite episodes.**إن كان سياستك يمكن أن تكون دائمة للأبد، فليكن ذلك صحيحاً`max_steps`واعتبروا أنّه فشل ضمني، وذلك أمر طبيعي، فقط تأكد من احتسابها بشكل صحيح.
  **无限回合。**MC 要求回合*终止*。 إذا كانت الاستراتيجية قد تكون دائمة، تعيين `max_steps`العدالة والإفلاس
- **Variance.**الموسيقى تستخدم العائدات الكاملة في الحلقات الطويلة، الاختلاف هائل  مكافأة واحدة غير محظوظة في نهاية النقبات `V(s_0)`وذلك في نفس المبلغ. أساليب التد (دروس 04) خفض هذا عن طريق إطلاق.
  **方差。**MC استخدام كامل回报──长回合上方差很大 أخير الخطوة سوء حظ مكافأة`V(s_0)` تدي  طريقة  الدروس 04) من خلال التقدم الذاتي لخفض الاختلافات
- **State coverage.**الموسيقي الطمأنسي على ق جديد مع العلاقات سوف تجرب فقط عمل واحد يجب عليك استكشاف (ε-طمأنسي، استكشاف بدايات، UCB).
  **状态覆盖。**ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ ـ
- **Non-stationary policies.**إذا`π`تغيرات (كما هو الحال في مراقبة MC) ، العائدات القديمة هي من سياسة مختلفة.
  **非平稳策略。**إذا`π`变化(如 MC 控制中),旧回报来自不同策略──常数 α MC 处理此问题;样本平均 MC 不能──
- **Off-policy importance sampling.**الوزن`π(a|s)/μ(a|s)`يضاعف عبر مسار. ينفجر التباين مع الأفق. القيادة مع IS الموزن لكل قرار أو الانتقال إلى TD.
  **离策略重要性采样。**权重 `π(a|s)/μ(a|s)`في المسار المتراكم على المدى المتراكم.

## استخدمها في إطار التنفيذ

دور أساليب مونت كارلو لعام 2026:

> 2026 سنة مونتكارلو طريقة:

| Use case | Why MC |
|----------|--------|
| Use case / 用例 | Why MC / 为什么用 MC |
| Short-horizon games (blackjack, poker) / 短视野游戏（二十一点、扑克） | Episodes terminate naturally; returns are clean. / 回合自然终止；回报干净。 |
| Offline evaluation of a logged policy / 离线评估已记录的策略 | Average discounted returns over stored trajectories. / 对存储轨迹取折扣回报平均。 |
| Monte Carlo Tree Search (AlphaZero) / 蒙特卡洛树搜索 | MC rollouts from tree leaves guide selection. / 树叶的 MC rollout 指导选择。 |
| LLM RL evaluation / LLM RL 评估 | Compute average reward over sampled completions for a given policy. / 对给定策略的采样完成计算平均奖励。 |
| Baseline estimation in PPO / PPO 中的基线估计 | The advantage target `A_t = G_t - V(s_t)` uses an MC `G_t`. / 优势目标使用 MC 的 `G_t`。 |
| Teaching RL / 教学 RL | Simplest algorithm that actually works — strip bootstrapping to see the core. / 最简单且有效的算法——去掉自举看核心。 |

الخوارزميات الحديثة للخلفية العميقة (PPO، SAC) تتقاطع بين MC (العائد الكامل) و TD (الخطوة الواحدة من التشغيل)`n`-المستويات الخطوة أو GAE. كلا النقاط النهائية هي حالات من نفس المقدرة.

> 现代深度 RL 算法 ((PPO、SAC) من خلال `n`步回报或 GAE 在纯 MC(完整回报) و纯 TD(单步自举) بين القيمة المقطوعة.

## أرسلها .

إبقوا`outputs/skill-mc-evaluator.md`:

```markdown
---
name: mc-evaluator
description: Evaluate a policy via Monte Carlo rollouts and produce a convergence report with DP-comparison if available.
version: 1.0.0
phase: 9
lesson: 3
tags: [rl, monte-carlo, evaluation]
---

Given an environment (episodic, with reset+step API) and a policy, output:

1. Method. First-visit vs every-visit MC. Reason.
2. Episode budget. Target number, variance diagnostic, expected standard error.
3. Exploration plan. ε schedule (if needed) or exploring starts.
4. Gold-standard comparison. DP-optimal V* if tabular; otherwise a bound from a Q-learning / PPO baseline.
5. Termination check. Max-step cap, timeouts, handling of non-terminating trajectories.

Refuse to run MC on non-episodic tasks without a finite horizon cap. Refuse to report V^π estimates from fewer than 100 episodes per state for tabular tasks. Flag any policy with zero-variance actions as an exploration risk.
```

## تمارين التدريب

1. **Easy.**تنفيذ تقييم الممثلين في الزيارة الأولى لسياسة التعرض العشوائي الموحد على 4 × 4 GridWorld. تشغيل 10،000 حلقة.`V(0,0)`كعمل على عدد الحلقات مقابل إجابة DP.
   > **练习1：**实现 MC 评估,将 V(0,0) 随回合数的收曲线与 DP 基准对比──
2. **Medium.**تنفيذ التحكم في الـ " MC " الفطري مع`ε ∈ {0.01, 0.1, 0.3}`مقارنة معدل العودة بعد 20000 حلقة كيف يبدو منحنى؟ أين يعيش التداول بين التباينات والتحيزات؟
   > **练习2：**用不同 ε 值做 MC 控制,观察探索-利用权衡──
3. **Hard.**تنفيذ * خارج السياسة* MC مع أخذ العينات المهمة: جمع البيانات في إطار سياسة متساوية متساوية `μ`، تقدير `V^π`لسياسة التحديد المثلى`π`. مقارنة IS بسيطة مقابل IS لكل قرار مقابل IS الموزن
   > **练习3：**实现离策略 MC 重要性采样),比较不同 IS 方差的差异──

## شروط الرئيسية

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| Monte Carlo | "Random sampling" / 蒙特卡洛 | Estimate expectations by averaging over iid samples from the distribution. |
| Return `G_t` | "Future reward" / 回报 | Sum of discounted rewards from step `t` to episode end: `Σ_{k≥0} γ^k r_{t+k+1}`. |
| First-visit MC | "Count each state once" / 首次访问 MC | Only the first visit in an episode contributes to the value estimate. |
| Every-visit MC | "Use all visits" / 每次访问 MC | Every visit contributes; slightly biased but more sample-efficient. |
| ε-greedy | "Exploration noise" / ε-贪心 | Pick greedy action with prob `1-ε`; random action with prob `ε`. |
| Importance sampling | "Correcting for sampling from the wrong distribution" / 重要性采样 | Reweight returns by `π(a\|s)/μ(a\|s)` products to estimate `V^π` from `μ` data. |
| On-policy | "Learn from my own data" / 在线策略 | Target policy = behavior policy. Vanilla MC, PPO, SARSA. |
| Off-policy | "Learn from someone else's data" / 离线策略 | Target policy ≠ behavior policy. Importance-sampled MC, Q-learning, DQN. |

## المزيد من القراءة

- [Sutton & Barto (2018). Ch. 5 — Monte Carlo Methods](http://incompleteideas.net/book/RLbook2020.pdf) العلاج القنوني
- [Singh & Sutton (1996). Reinforcement Learning with Replacing Eligibility Traces](https://link.springer.com/article/10.1007/BF00114726) أول زيارة مقابل تحليل كل زيارة
- [Precup, Sutton, Singh (2000). Eligibility Traces for Off-Policy Policy Evaluation](http://incompleteideas.net/papers/PSS-00.pdf) خارج السياسة MC والتحكم في التباين.
- [Mahmood et al. (2014). Weighted Importance Sampling for Off-Policy Learning](https://arxiv.org/abs/1404.6362) مقياسات IS الحديثة ذات التغيرات المنخفضة.
- [Tesauro (1995). TD-Gammon, A Self-Teaching Backgammon Program](https://dl.acm.org/doi/10.1145/203330.203343) أول إثبات تجريبي واسع النطاق لعبة MC/TD الذاتية تتحول إلى لعبة فائقة الإنسانية؛ مقدمة مفهومية لكل درس في النصف الثاني من هذه المرحلة.
