# الفرق الزمني  Q-Learning & SARSA                                                                                                                                                                                                                                                        

> ينتظر مونت كارلو حتى تنتهي الحلقة. يقوم TD بتحديث كل خطوة من خلال إطلاق تقدير القيمة التالي. Q-تعلم غير سياسية ومثالي؛ SARSA على السياسة ومحذرة. كلاهما خط واحد من الشفرة. كلاهما يستند إلى كل طريقة عميقة RL في هذه المرحلة.

> **【中文解读】**يجب أن تنتظر حتى ينتهي المرحلة لتتجدد كل خطوة يمكن أن تتجدد`r + γ V(s')`作为目标来引导当前估计──Q-learning是离策略的(学习最优策略),SARSA是在线策略的(学习当前行为策略)──两者只差一点`max`لكن هذا هو أساس كل الـ "الـ"

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 01 (MDPs), Phase 9 · 02 (Dynamic Programming), Phase 9 · 03 (Monte Carlo) | **前置知识:** Phase 9 · 01 (MDP), Phase 9 · 02 (动态规划), Phase 9 · 03 (蒙特卡洛)
**Time:** ~75 minutes | **时间:** ~75 分钟

## المشكلة المشكلة المشكلة

يعمل مونت كارلو ولكن لديه طلبان مكلفان. يحتاج إلى حلقات تنتهي، ويُحديث فقط بعد العودة النهائية. إذا كانت حلقةك 1000 خطوة، ينتظر MC 1000 خطوة لتحديث أي شيء. إنها عالية التباين، منخفضة التحيز، وبطيئة في الممارسة.

> إنّه لا يزال يعمل، ولكن هناك طلبان مكلفان. إنه يحتاج إلى إيقاف دورة، ويجب أن يتمّ تحديثها فقط بعد إصدار المراجعة النهائية. إذا كان هناك 1000 خطوة في الحلقة، يجب أن ينتظر 1000 خطوة قبل تحديث أي شيء.

البرمجة الديناميكية لديها الملف المقابل  النسخ الاحتياطية المبدئية ذات التغير الصفر  ولكن تتطلب نموذجاً معروفًا.

> التخطيط الحراري لديه خصائص معاكسة 零方差  ولكن يحتاج إلى نموذج معروف‬

التعلم الفرق في الزمن (TD) يفرق الفرق. من انتقال واحد `(s, a, r, s')`، تشكيل هدف خطوة واحدة`r + γ V(s')`و الدفع`V(s)`لا نموذج، لا حلقات كاملة، تحيزات من استخدام تقريبي`V`على RHS، ولكن أقل بكثير من الاختلافات من MC والتحديثات على الانترنت من الخطوة الأولى.

> 时序差分(TD) تعلم折中了两者──从单次转移 `(s, a, r, s')`构建单步目标 `r + γ V(s')`،将 `V(s)`إلى مقربة منها.`V`هناك اختلافات، ولكن الاختلافات أقل بكثير من MC، ومن الخطوة الأولى على الإمكانية تحديثها على الإنترنت.

هذه هي المحور الذي يتحول عليه جميع RL  DQN الحديثة، A2C، PPO، SAC . الباقي من المرحلة 9 هي طبقات من التقريب الوظيفي والحيل التي بنيت على رأس تحديث TD خطوة واحدة ستكتب في هذا الدروس.

> هذا هو كل مركز RLDQN A2C、PPO、SAC الحديث. الجزء المتبقي من المرحلة 9 هو في هذا الدورة سوف تكتب خطوة واحدة TD 更新 على بناء وظيفة تقارب وتكنولوجيا طبقة.

> **【中文解读】**TD تعلم هو DP و MC: مع التحول بمرحلة واحدة`(s,a,r,s')`构建目标 `r + γV(s')`لا تحتاج إلى نموذج ، ولا تحتاج إلى دورة كاملة. هناك تناقضات (لأن استخدام تقارب V) ، ولكن التناقضات أقل بكثير من MC ، ويمكن تحديثها على الإنترنت.

> **【拓展：游戏AI→LLM对齐】**Q-التعلم هو جوهر Atari DQN في عام 2013 ، فتح عميقة RL 时代。PPO هو الخوارزمية الأساسية لتدريب ChatGPT RLHF  كلتا مبنية على فكرة TD 误差── فهم Q-تعلم ومع SARSA هو فهم نموذج كبير على أساس التدريب‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬

## المفهوم الأساسي

![Q-learning vs SARSA: off-policy max vs on-policy Q(s', a')](../assets/td.svg)

**The TD(0) update for V:**

`V(s) ← V(s) + α [r + γ V(s') - V(s)]`

الكمية المرتبطة هي خطأ TD `δ = r + γ V(s') - V(s)`إنه التناظر عبر الإنترنت لـ`G_t - V(s_t)`في المياه المختلفة .`α`(مُرضى (روبينز مونرو`Σ α = ∞`،`Σ α² < ∞`وكل الدول زارت كثيراً

> **V 的 TD(0) 更新：**括号中的量是 TD 误差 `δ = r + γ V(s') - V(s)`انها في مركز الموسيقى`G_t - V(s_t)` الإجراءات`α`满足 روبنز-مونرو 条件且所有状态被无限次访问。

**Q-learning.**طريقة TD خارج السياسة للسيطرة:

`Q(s, a) ← Q(s, a) + α [r + γ max_{a'} Q(s', a') - Q(s, a)]`

- نعم`max`يفترض أن سياسة * طمعية * سيتم اتباعها من`s'`وذلك التخلّص يجعل تعلم القيّة يتعلم`Q*`بينما يستكشف العميل عن طريق ε-greedy. Mnih et al. (2015) حول هذا إلى Deep Q-learning على Atari (دروس 05).

> **Q-learning。**طريقة تحكم التد`max`假设从 `s'`開始將遵循*贪心* استراتيجية، مهما كان المتحركات التي يتخذها المجهول الذكي فعليا.`Q*`Mnih 等人 (2015) سوف تحويل هذا إلى Atari 上的深度 Q-learning (تعلم القراءة)

**SARSA.**طريقة التنقل التجاري في السياسة:

`Q(s, a) ← Q(s, a) + α [r + γ Q(s', a') - Q(s, a)]`

الاسم هو الـ " توبل "`(s, a, r, s', a')`. سارسا تستخدم الإجراء`a'`العميل يأخذ التالي، وليس الجشع`argmax`. يتحرك إلى`Q^π`لأي شيءٍ طموح`π`يدير، الذي في الحد`ε → 0`يصبح`Q*`. . .

> **SARSA。**                                                                                                                                                                                                                                                              `(s, a, r, s', a')`✿SARSA استخدام الذكاء* فعليا* اتخاذ`a'`و ليس طمعًا`argmax`收到当前 ε-贪心 `π``Q^π`, في`ε → 0`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `Q*`.

**The cliff-walking difference.**في مهمة المشي على الصخره الكلاسيكية (سقطة-من-الصخره = مكافأة -100) ، يتعلم Q-التعلم المسار الأمثل على طول حافة الصخره ولكن في بعض الأحيان يأخذ العقوبة أثناء الاستكشاف. تعلم SARSA مسار أكثر أمانا خطوة واحدة بعيدا عن الصخره لأنه يعامل ضجيج الاستكشاف في قيمة Q. مع التدريب، كلتا الوصول إلى المثالي عند `ε → 0`في الممارسة المهمة: عندما يحدث الاستكشاف في الواقع عند النشر، سلوك SARSA أكثر تحفظًا.

> **【中文解读】**كشف تجربة التدريب على الصخره الكلاسيكية عن الفرق الرئيسي بين Q-learning و SARSA: تعلم Q-learning تعلم أفضل الطرق على الصخره ولكن التدريب سوف يقع ، SARSA تعلم طريق السلامة بعيدا عن الصخره لأنّه يدرس التدريب على الضوضاء.

**Expected SARSA.**استبدل`Q(s', a')`مع قيمته المتوقعة أقل من `π`:

`Q(s, a) ← Q(s, a) + α [r + γ Σ_{a'} π(a'|s') Q(s', a') - Q(s, a)]`

انخفاض التباين من SARSA (لا يوجد عينة من`a'`() نفس الهدف السياسي، غالباً ما يكون الاختلاف في الكتب المدرسية الحديثة.

> **期望 SARSA。**استخدام`π`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `Q(s', a')`◊ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √ √`a'`), نفس الهيكل الهيكلي ∞

**n-step TD and TD(λ).**التقاط بين TD(0) و MC عن طريق الانتظار `n`خطوات قبل إطلاقها. `n=1`هو TD، `n=∞`هو MC. TD(λ) المتوسطات على كل `n`مع الوزن الهندسي `(1-λ)λ^{n-1}`معظم استخدامات القوة العمقية`n`بين 3 و 20.

> **n 步 TD 和 TD(λ)。**في TD(0) و MC   بين القيمة، إنتظر `n`步再自举──`n=1`نعم ،`n=∞`نعم , ماكسي`n`取平均──大多数深度 RL 使用 `n`بين 3 إلى 20

> **【拓展：TD 误差在 LLM RLHF 中的对应】**TD 误差 δ = r + γV(s') - V(s) في دراسة RLHF في LLM 訓練ات من الصفات المباشرة:PPO 优势函数 A = r + γV(s') - V(s) هو TD 误差的变体──每生成一个代币,计算当前代币的奖励──来自 RM) 加上评论对未来价值的估算减减当前估算──理解 TD 误差是理解 PPO 优势函数的关键──

## بناء ذلك تحرك لتحقيق
```figure
qlearning-gridworld
```

## بناءها

### الخطوة الأولى: SARSA بشأن السياسة الـ "الحريصة"

```python
def sarsa(env, episodes, alpha=0.1, gamma=0.99, epsilon=0.1):
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})

    def choose(s):
        if random() < epsilon:
            return choice(ACTIONS)
        return max(Q[s], key=Q[s].get)

    for _ in range(episodes):
        s = env.reset()
        a = choose(s)
        while True:
            s_next, r, done = env.step(s, a)
            a_next = choose(s_next) if not done else None
            target = r + (gamma * Q[s_next][a_next] if not done else 0.0)
            Q[s][a] += alpha * (target - Q[s][a])
            if done:
                break
            s, a = s_next, a_next
    return Q
```

ثمانية خطوط، الفرق الوحيد بين Q-Learning هو خط الهدف.

> 八行代码── والفرق الوحيد بين Q- تعلم هو هدف行──

### الخطوة الثانية: تعلم القي

```python
def q_learning(env, episodes, alpha=0.1, gamma=0.99, epsilon=0.1):
    Q = defaultdict(lambda: {a: 0.0 for a in ACTIONS})
    for _ in range(episodes):
        s = env.reset()
        while True:
            a = choose(s, Q, epsilon)
            s_next, r, done = env.step(s, a)
            target = r + (gamma * max(Q[s_next].values()) if not done else 0.0)
            Q[s][a] += alpha * (target - Q[s][a])
            if done:
                break
            s = s_next
    return Q
```

- نعم`max`يفرق الهدف عن السلوك. هذا الرمز الواحد هو الفرق بين السياسة والسياسة الخارجي.

> `max`تحليل الهدف والسلوك. هذا الرمز هو الفرق بين الاستراتيجية على الإنترنت والإستراتيجية.

### الخطوة الثالثة: منحنى التعلم

متوسط العودة في 100 حلقة. يتقارب تعلم Q أسرع على شبكة التشبيه البسيطة ؛ SARSA أكثر تحفظا على المشي على الصخور. على شبكة 4 × 4 في `code/main.py`كلاهما مثالي تقريباً بعد 2000 حلقة`α=0.1, ε=0.1`. . .

> تتبع كل 100 مرة في المجموعة متوسط الانتخابات. Q-التعلم في البساطة التأكد شبكة العالم على الإستقبال أسرع. SARSA على المرفق على المشي أكثر الحفاظ.`code/main.py`4×4 GridWorld 上,两者在 `α=0.1, ε=0.1`تقريباً 2000 مرة بعد التجمع أقرب إلى أفضل

### الخطوة الرابعة: مقارنة الحقيقة

إعادة تشغيل القيمة (درس 02) للحصول على `Q*`- تفقد`max_{s,a} |Q_learned(s,a) - Q*(s,a)|`. وكيل TD صحي جداول الهبوط داخل `~0.5`على شبكة 4×4 العالم بعد 10,000 حلقة.

> 运行值代(درس 02) الحصول `Q*` التفتيش`max_{s,a} |Q_learned(s,a) - Q*(s,a)|`◊ صورة صحية TD  الذكاء في 10,000 مرة أخرى بعد في 4×4 شبكة العالم`~0.5`فى الداخل

## الفخاخ

- **Initial Q values matter.**بداية متفائلة (`Q = 0`يُشجع التنقيب. يمكن أن يقع بداية السوء في حُصّة سياسة طموحة إلى الأبد.
  **初始 Q 值很重要。**乐观初始化 负奖励任务中 `Q = 0`(شجع البحث.
- **α schedule.**مستمرة`α`لا بأس في مشاكل غير ثابتة.`α_n = 1/n`يعطي التقارب النظري ولكن بطيء جدا في الممارسة `α`في`[0.05, 0.3]`وراقب منحنى التعلم
  **α 调度。**常数 `α`تطبق على مشاكل غير مستقرة`α_n = 1/n`في النظرية، لكن في الممارسة، سيبطئ`α`ثبثت`[0.05, 0.3]`وراقب التعلم
- **ε schedule.**البدء مرتفع (`ε=1.0`، تدهور إلى`ε=0.05`"GLIE" (الحس في الحد مع استكشاف لا نهاية له) هو حالة التقارب.
  **ε 调度。**از高值开始`ε=1.0`), انخفاض إلى `ε=0.05`"الكنيسة" ((极限贪心且无限探索)
- **Max bias in Q-learning.**- نعم`max`المستخدم متحيز للأعلى عندما`Q`يؤدي إلى زيادة التقدير  تعلم هاسلت المزدوج Q (الذي استخدمه DDQN في الدروس 05) يصلح هذا مع جدولين Q.
  **Q-learning 的最大化偏差。** `max`-أجل`Q`هناك ضجيج عند التحيز الصوتي.
- **Non-terminating episodes.**يمكن لـ TD أن يتعلم دون محطات ، ولكن عليك إما أن تطبق الخطوات أو التعامل مع إطلاق الصوت بشكل صحيح في الحائط.
  **非终止回合。**يمكن التعلم في حالة لا نهاية لها، ولكن تحتاج إلى وضع عدد الخطوات فوق الحد أو إصلاح المقياسات.
- **State hashing.**إذا كانت الحالات هي أجزاء متجمدة/مضغوطات، استخدم مفتاحًا يمكن التشغيل به (أجزاء متجمدة، وليس قائمة؛ أجزاء متجمدة من العلو، وليس خامًا).
  **状态哈希。**إذا كان الحالة هي مجموعة من المكونات / حجم الـ张، استخدم مفتاحات القابل للاستعمال.

## استخدمها في إطار التنفيذ

المشهد التجاري لعام 2026:

> 2026 سنة TD 学习的版图:

| Task | Method | Reason |
|------|--------|--------|
| Task / 任务 | Method / 方法 | Reason / 原因 |
| Small tabular environments / 小型表格环境 | Q-learning | Learns optimal policy directly. / 直接学习最优策略。 |
| On-policy safety-critical / 在线策略安全关键 | SARSA / Expected SARSA | Conservative during exploration. / 探索期间保守。 |
| High-dimensional state / 高维状态 | DQN (Phase 9 · 05) | Neural-net Q-function with replay and target net. / 神经网络 Q 函数+回放+目标网络。 |
| Continuous actions / 连续动作 | SAC / TD3 (Phase 9 · 07) | TD update on a Q-network; policy net emits actions. / Q 网络上的 TD 更新；策略网络输出动作。 |
| LLM RL (reward-model-based) / LLM RL（基于奖励模型） | PPO / GRPO (Phase 9 · 08, 12) | Actor-critic with TD-style advantage via GAE. / Actor-Critic + GAE 的 TD 式优势。 |
| Offline RL / 离线 RL | CQL / IQL (Phase 9 · 08) | Q-learning with conservative regularization. / 带保守正则化的 Q-learning。 |

90% من "RL" التي تقرأ عنها في ورق 2026 هي بعض التطويرات من Q- تعلم أو SARSA. فهم تحديث الجدول المتحدي في أصابعك قبل قراءة أعمق.

> في مقال عام 2026، "RL" الذي قرأت، 90٪ هو نوع من التعلم القياسي أو SARSA. قبل قراءة عميقة، أولاً، تحديث المظهر إلى التعلم في الذاكرة الجسدية.

## أرسلها .

إبقوا`outputs/skill-td-agent.md`:

```markdown
---
name: td-agent
description: Pick between Q-learning, SARSA, Expected SARSA for a tabular or small-feature RL task.
version: 1.0.0
phase: 9
lesson: 4
tags: [rl, td-learning, q-learning, sarsa]
---

Given a tabular or small-feature environment, output:

1. Algorithm. Q-learning / SARSA / Expected SARSA / n-step variant. One-sentence reason tied to on-policy vs off-policy and variance.
2. Hyperparameters. α, γ, ε, decay schedule.
3. Initialization. Q_0 value (optimistic vs zero) and justification.
4. Convergence diagnostic. Target learning curve, `|Q - Q*|` check if DP is possible.
5. Deployment caveat. How will exploration behave at inference? Is SARSA's conservatism needed?

Refuse to apply tabular TD to state spaces > 10⁶. Refuse to ship a Q-learning agent without a max-bias caveat. Flag any agent trained with ε held at 1.0 throughout (no exploitation phase).
```

## تمارين التدريب

1. **Easy.**تنفيذ Q-تعلم و SARSA على 4 × 4 GridWorld. خطة منحنى التعلم (متوسط العائد لكل 100 حلقة) ل 2000 حلقة. من يتقارب أسرع؟
   > **练习1：**في GridWorld 上 مقارنة Q-تعلم و SARSA
2. **Medium.**قم ببناء بيئة المشي على الصخره (4 × 12 ، الصف الأخير هو الصخره مع مكافأة -100 وإعادة ضبطها للبدء). مقارنة سياسات Q-learning و SARSA النهائية. صور شاشة المسارات التي يتخذها كل واحد. أي من هذه السلالم أقرب إلى الصخره؟
   > **练习2：**实现悬崖行走环境,观察 Q-learning (تعلم القاعدة)  贴崖边) مقابل SARSA (远离崖边)  远离崖边)
3. **Hard.**تنفيذ تعلم Q مزدوج. في GridWorld (ضوضاء غوسيان σ=5 إضافة إلى مكافأة خطوة واحدة) ، أظهر تخفيف التعلم Q `V*(0,0)`وبالقدر المفيد بينما تعلم القي المزدوج لا يفعل
   > **练习3：**تحقيق التعلم الثنائي Q، تجربة أنه يمكن أن يزيل أقصى تعادل في تعلم Q.

## شروط الرئيسية

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| TD error | "The update signal" / TD 误差 | `δ = r + γ V(s') - V(s)`, the bootstrapped residual. |
| TD(0) | "One-step TD" / 单步 TD | Update after every transition using only the next state's estimate. |
| Q-learning | "Off-policy RL 101" / Q 学习 | TD update with `max` over next-state actions; learns `Q*` regardless of behavior policy. |
| SARSA | "On-policy Q-learning" / SARSA | TD update using the actual next action; learns `Q^π` for current ε-greedy π. |
| Expected SARSA | "The low-variance SARSA" / 期望 SARSA | Replace sampled `a'` with its expectation under π. |
| GLIE | "Correct exploration schedule" / 无限探索极限贪心 | Greedy in the Limit with Infinite Exploration; needed for Q-learning convergence. |
| Bootstrapping | "Using current estimate in the target" / 自举 | What distinguishes TD from MC. Source of bias but massive variance reduction. |
| Maximization bias | "Q-learning overestimates" / 最大化偏差 | `max` over noisy estimates is upward-biased; fixed by Double Q-learning. |

## المزيد من القراءة

- [Watkins & Dayan (1992). Q-learning](https://link.springer.com/article/10.1007/BF00992698) الورقة الأصلية و دليل التقارب.
- [Sutton & Barto (2018). Ch. 6 — Temporal-Difference Learning](http://incompleteideas.net/book/RLbook2020.pdf) TD(0) ، SARSA، Q-تعلم، المتوقع SARSA.
- [Hasselt (2010). Double Q-learning](https://papers.nips.cc/paper_files/paper/2010/hash/091d584fced301b442654dd8c23b3fc9-Abstract.html) إصلاح تحيز القياس
- [Seijen, Hasselt, Whiteson, Wiering (2009). A Theoretical and Empirical Analysis of Expected SARSA](https://ieeexplore.ieee.org/document/4927542) تحفيز سارسا المتوقع
- [Rummery & Niranjan (1994). On-line Q-learning using connectionist systems](https://www.researchgate.net/publication/2500611_On-Line_Q-Learning_Using_Connectionist_Systems) الورقة التي ابتكرت SARSA (التي كانت تسمى "التعلم Q-المرتبط المعدل) ".
- [Sutton & Barto (2018). Ch. 7 — n-step Bootstrapping](http://incompleteideas.net/book/RLbook2020.pdf) يجميع TD(0) إلى TD(n) ، المسار من Q-تعلم إلى آثار التأهل، ولاحقاً، GAE في PPO.
