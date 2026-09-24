# شبكات "ديف ق"

> 2013: تدرب Mnih شبكة Q-تعلم على البيكسل الخام، هزمت كل وكيل RL كلاسيكي على سبعة ألعاب Atari. 2015: تمتد إلى 49 لعبة، نشرت في الطبيعة، أطلقت عصر العميقة RL. DQN هو Q-تعلم بالإضافة إلى ثلاث حيل تجعل التقريب الوظيفي مستقرة.

> **【中文解读】**DQN = Q-تعلم + شبكة العصبية + ثلاث مهارات استقرارية ((تجربة إعادة التأمين ‬الجهد ‬المنح الحصص المكافأة) ‬2013-2015 في Atari ‬العبة هزيمة جميع طرق RL الكلاسيكية ، فتح عصر RL العميقة‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 03 (Backpropagation), Phase 9 · 04 (Q-learning, SARSA) | **前置知识:** Phase 3 · 03 (反向传播), Phase 9 · 04 (Q-learning, SARSA)
**Time:** ~75 minutes | **时间:** ~75 分钟

## المشكلة المشكلة المشكلة

يتطلب تعلم Q الجدولي قيمة Q منفصلة لكل زوج (حالة ، عمل). لوح الشطرنج لديه ~ 1043 حالة. إطار Atari هو 210 × 160 × 3 = 100,800 ميزة. يموت RL الجدولي في آلاف الحالات ، ناهيك عن المليارات.

> 表格 Q-تعلم 需要为每一个状态,动作) على الاحتفاظ بمفرد 价值 Q. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .

والإصلاح واضح في الماضي: استبدال جدول Q بشبكة عصبية،`Q(s, a; θ)`لكن عملية التعرف على الوظائف الواضحة في الخلف استغرق عقود. يختلف التقريب المميز مع تعلم Q تحت "ثلاثة مميتة"  التقريب الوظائف + التشغيل + التعلم خارج السياسة. حدد Mnih et al. (2013, 2015) ثلاثة حيل هندسية تحافظ على التعلم:

> الحل بسيط جداً: باستخدام شبكة العصبية`Q(s, a; θ)`استغرق هذا "السهل" عدة عقود. تم تحديد ثلاثة مهارات هندسية للعلم الثابت:

1. **Experience replay**يُفصل بين الانتقالات.
   **经验回放**打破转移的时间相关性
2. **Target network**يجمد الهدف من إطلاق القيادة
   **目标网络**结自举目标──
3. **Reward clipping**يُعادِلُ الكبُرَاتِ المُتَحَدِّدَةِ.
   **奖励裁剪**归一化梯度量级──

كانت DQN على Atari هي المرة الأولى التي تحل فيها بنية واحدة مع مجموعة مفاتيح خارقة واحدة عشرات المشاكل التحكمية من البيكسلات الخام. كل شيء "عميق-RL" تم بناؤه منذ DDQN ، Rainbow ، Dueling ، Distribution ، R2D2 ، Agent57  يتم تجميعه فوق هذه القاعدة الثلاثية.

> كان DQN على Atari أول مرة تستخدمها مجموعة من المكونات الفريدة والعديد من المكونات الفريدة من الصور الأصلية لحل عشرات المشاكل التحكمية.

> **【中文解读】**"ثلاث عناصر قاتلة": وظيفة مقربة + أنفسها + 离策略 → 训练不稳定甚至发散── ثلاث حركات من DQN حل هذه المشكلة:

> **【拓展：经验回放→RLHF】**فكرة تجربة إعادة التعبير (Experience Replay) لا توجد في تدريبات الجامعة: البفر في تدريبات الـPPO RLHF  المجموعة المفضلة للبيانات  البيانات غير المتواصلة في DPO  هي في الأساس "القطع في المعلومات  التواصل  الاستخدام المكرر للتجارب".

## المفهوم الأساسي

![DQN training loop: env, replay buffer, online net, target net, Bellman TD loss](../assets/dqn.svg)

**The objective.**DQN يقلل من خسارة TD خطوة واحدة على وظيفة Q العصبية:

`L(θ) = E_{(s,a,r,s')~D} [ (r + γ max_{a'} Q(s', a'; θ^-) - Q(s, a; θ))² ]`

`θ`= شبكة الإنترنت، تحديث كل خطوة بالتراجع. `θ^-`= شبكة المستهدفة، يتم نسخها بشكل دوري من `θ`(كل 10000 خطوة)`D`= تعيد تعزيز الانتقالات الماضية.

> **目标。**DQN 最小化神经 Q 函数 على خطوة واحدة TD 损失──`θ`= 在线网络,每步通过梯度下降更新──`θ^-`= 目标网络,定期从 `θ`复制(تقريباً في كل 10,000 步)`D`= 过去转移的回放缓冲区──

**The three tricks, in order of importance:**

> **三个技巧，按重要性排序：**

**Experience replay.**حلقة عازلة من`~10⁶`التحولات. كل خطوة تدريبية تعرض مجموعة صغيرة بشكل متساوي عشوائي. هذا يكسر التواصل الزمني (الإطارات المتتالية متطابقة تقريبًا) ، ويسمح للشبكة بالتعلم من التحولات النادرة المثمرة عدة مرات ، ويقوم بتحديثات التراجع المتتالية. بدون ذلك ، تختلف التد في السياسة مع شبكة عصبية على أتاري.

> **经验回放。**واحد حوالي 106 مرة تحويل حلقة كافة المنطقة. كل مرحلة التدريبية تتم بشكل متساوي باعتبارها مجموعة صغيرة من المرات. هذا يفسد الارتباط في الوقت.

**Target network.**باستخدام نفس الشبكة`Q(·; θ)`على جانبي معادلة بيلمان يجعل الهدف يتحرك كل تحديث  "المتابعة ذيلك".`Q(·; θ^-)`مع الأوزان المجمدة.`C`خطوات، نسخة `θ → θ^-`هذا يُثبت هدف التراجعة لآلاف الخطوات المرتفعة في وقت واحد`θ^- ← τ θ + (1-τ) θ^-`(مستخدم في DDPG، SAC) هي نوع أكثر سلاسة.

> **目标网络。**في معادلة بيلمان استخدام نفس الشبكة سوف يجعل الهدف كل تحديث في تحرك"المتابعة للشيء الخاص بك"‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬`C`步复制 `θ → θ^-`◊ soft update(DDPG、SAC 中使用) هو أكثر تغييرات سلمية

**Reward clipping.**مقياس مكافأة أتاري يختلف من 1 إلى 1000 +.`{-1, 0, +1}`يمنع أي لعبة واحدة من السيطرة على المرجع خطأ عندما تكون حجم الجائزة مهمة، جيد لـ Atari حيث فقط التوقيع مهمة.

> **奖励裁剪。**أطارى  الحصيلة من 1 إلى 1000+ غير وغيرها`{-1, 0, +1}`‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬‬

**Double DQN.**Hasselt (2016) تصحيح تحيز القياس القصوى: استخدام الشبكة على الإنترنت لـ * اختيار * الإجراء ، والشبكة المستهدفة لـ * تقييم * له.

`target = r + γ Q(s', argmax_{a'} Q(s', a'; θ); θ^-)`

استبدال التسجيل، أفضل بشكل ثابت، استخدميه بشكل افتراضي

> **双重 DQN。**Hasselt (2016) 修复最大化偏差:用在线网络*选择*动作,用目标网络*评估*它──直接替换,始终更好──默认使用──

**Other improvements (Rainbow, 2017):**إعادة التمثيل ذات الأولوية (مثل عدة عمليات انتقالية عالية التلفزيون) ، معمارة المواجهة (فصل `V(s)`و الرؤوس المفيدة) ، الشبكات الضوضاء (التنقيب المتعلم) ، عائدات خطوة n، Q التوزيعي (C51/QR-DQN) ، التشغيل متعدد الخطوات. كل واحد يضيف بضع في المئة؛ والمكاسب تقريبا إضافية.

> **其他改进（Rainbow, 2017）：**优先回放、决斗架构、噪声网络、n 步回报、分布式 Q、多步自举── كل نوع من التحسينات مساهمة بضع مئات النقاط؛收益大致可叠加──

> **【拓展：Rainbow DQN 与集成改进】**قوس قزح DQN(2017) سوف يتم دمج 6 أنواع من DQN  تحسين معا: التجربة الأولوية إعادة إرسال  دويل 架构、 الضجيج شبكة بحث、n 步回报、 تمتزيع Q تعلم、多步自举── كل نوع من التحسينات مساهمة بضع مئات من النقاط تحسين الأداء، وتجميع النتائج بشكل ملحوظ.

## بناء ذلك تحرك لتحقيق
```figure
f3-dqn-stability
```

## بناءها

الرمز هنا هو stdlib فقط خالية من النمبي  نستخدم MLP المتحركة اليدوية ذات الطبقة الواحدة المخفية على شبكة الإنترنت المستمرة الصغيرة، لذلك كل خطوة تدريبية تعمل في ميكروثانية. الخوارزمية هي نفس Atari DQN على النطاق.

> يستخدم هذا الكود فقط في المكتبة المعيارية في مجموعة صغيرة من النقاط التالية من شبكة الإنترنت.

### الخطوة 1: تعبئة إعادة

```python
class ReplayBuffer:
    def __init__(self, capacity):
        self.buf = []
        self.capacity = capacity
    def push(self, s, a, r, s_next, done):
        if len(self.buf) == self.capacity:
            self.buf.pop(0)
        self.buf.append((s, a, r, s_next, done))
    def sample(self, batch, rng):
        return rng.sample(self.buf, batch)
```

~ 50,000 قدرة ل Atari؛ 5000 يكفي لتجارة ألعابنا.

> أتاري تحتاج إلى 50 ألف حفرة، أما بيئة الألعاب لدينا فهي 5000

### الخطوة الثانية: شبكة Q الصغيرة (MLP اليدوية)

```python
class QNet:
    def __init__(self, n_in, n_hidden, n_actions, rng):
        self.W1 = [[rng.gauss(0, 0.3) for _ in range(n_in)] for _ in range(n_hidden)]
        self.b1 = [0.0] * n_hidden
        self.W2 = [[rng.gauss(0, 0.3) for _ in range(n_hidden)] for _ in range(n_actions)]
        self.b2 = [0.0] * n_actions
    def forward(self, x):
        h = [max(0.0, sum(w * xi for w, xi in zip(row, x)) + b) for row, b in zip(self.W1, self.b1)]
        q = [sum(w * hi for w, hi in zip(row, h)) + b for row, b in zip(self.W2, self.b2)]
        return q, h
```

الممر الأمامي: خطي → ريلو → خطي. هذا هو الشبكة بأكملها.

> 前向传播:线性 → ReLU → 线性──这就是整个网络──

### الخطوة الثالثة: تحديث DQN

```python
def train_step(online, target, batch, gamma, lr):
    grads = zeros_like(online)
    for s, a, r, s_next, done in batch:
        q, h = online.forward(s)
        if done:
            y = r
        else:
            q_next, _ = target.forward(s_next)
            y = r + gamma * max(q_next)
        td_error = q[a] - y
        accumulate_grads(grads, online, s, h, a, td_error)
    apply_sgd(online, grads, lr / len(batch))
```

الشكل هو Q-التعلم من الدروس 04 مع اختلافين: (أ) نحن نراجع من خلال التفريق `Q(·; θ)`بدلاً من تحديد جدول، (ب) استخدامات الهدف `Q(·; θ^-)`. . .

> 形式 مع دراسة 04 من Q-تعلم مشابهة، ولكن هناك فرقين:`Q(·; θ)`عكس التوزيع و غير المؤشر`Q(·; θ^-)`.

### الخطوة الرابعة: الحلقة الخارجية

لكل حلقة، تصرف بـ "الجشع"`Q(·; θ)`، دفع الانتقالات إلى العازلة، عينة مجموعة صغيرة، اتخاذ خطوة تراجعة، التزام المزامنة بشكل دوري `θ^- ← θ`النمط:

```python
for episode in range(N):
    s = env.reset()
    while not done:
        a = epsilon_greedy(online, s, epsilon)
        s_next, r, done = env.step(s, a)
        buffer.push(s, a, r, s_next, done)
        if len(buffer) >= batch:
            train_step(online, target, buffer.sample(batch), gamma, lr)
        if steps % sync_every == 0:
            target = copy(online)
        s = s_next
```

على شبكة الإنترنت الصغيرة لدينا مع حالة واحدة ساخنة 16 غطاء، العميل يتعلم سياسة مثالية تقريبا في حوالي 500 حلقة. على أتاري، نطيل هذا إلى 200 مليون إطار وإضافة إضافة CNN ميزة استخرج.

> في استخدامنا للـ 16 ̊ الـ 1 ̊ الـ GridWorld على الـ GridWorld، يتعلم الذكاء في حوالي 500 مرة إلى تقارب أفضل استراتيجيات.

## الفخاخ

- **Deadly triad.**يمكن أن تختلف تقارب الوظيفة + خارج السياسة + إطلاق التشغيل. DQN تخفيف مع شبكة الهدف + إعادة تشغيل؛ لا تُزيل أي منها.
  **致命三要素。**函数近似+离策略+自举可能发散──DQN 通过目标网络+回放缓解; don't remove any one──
- **Exploration.**يجب أن يتحلل ε، عادةً من 1.0 إلى 0.01 خلال أول ~ 10% من التدريب. دون استكشاف مبكر كاف يتقارب شبكة Q إلى حوض محلي.
  **探索。**يُجب أن يقلل، عادةً من 1.0 إلى 0.01, يغطي حوالي 10% من التدريبات السابقة.
- **Overestimation.** `max`على Q الضوضاء هي التحيز الصعودي دائما استخدام DQN المزدوج في الإنتاج.
  **过估计。**لـ " صوتاً "`max`أعلى تعتمد.
- **Reward scale.**كليف أو تعاديل المكافآت؛ حجم التراجع متناسب مع حجم المكافأة.
  **奖励尺度。**剪裁或归归化奖励; 梯度量级与奖励量级成正比.
- **Replay buffer coldstart.**لا تتدرب حتى يكون لدى المضخّم بضعة آلاف من الانتقالات
  **回放缓冲区冷启动。**缓冲区有几千次转移后再训练――早期大约20样本上梯度过适应――
- **Target sync frequency.**متكرر جدا ≈ لا شبكة هدف ؛ نادر جدا ≈ أهداف قديمة. Atari DQN يستخدم 10,000 خطوات env. قاعدة عامة: مزامنة كل ~1/100 من آفاق التدريب.
  **目标同步频率。**太频繁≈没有目标网络;太不频繁≈过时目标── تجربة قانون: في كل حوالي 1/100 训练视野同步一次──
- **Observation preprocessing.**تقوم شركة Atari DQN بتجميع 4 إطارات لتكون حالة Markov. أي بيئة مع معلومات السرعة تحتاج إلى إطارات أو حالة متكررة.
  **观测预处理。**Atari DQN 堆叠 4 使状态满足马尔可夫性── أي بيئة لديها سرعة المعلومات تحتاج إلى 堆叠 أو الدورة الحالة──

## استخدمها في إطار التنفيذ

في عام 2026، نادرا ما تكون DQN حديثة، ولكنها تظل خوارزمية مرجعية خارج السياسة:

> عام 2026، DQN  قليل من المقدم، ولكن لا يزال بعيدا عن الخوارزمية الاستراتيجية:

| Task | Method of choice | Why not DQN? |
|------|------------------|--------------|
| Task / 任务 | Method of choice / 首选方法 | Why not DQN? / 为什么不用 DQN？ |
| Discrete-action Atari-like / 离散动作类 Atari | Rainbow DQN or Muesli | Same framework, more tricks. / 相同框架，更多技巧。 |
| Continuous control / 连续控制 | SAC / TD3 (Phase 9 · 07) | DQN has no policy network. / DQN 没有策略网络。 |
| On-policy / high-throughput / 在线策略/高吞吐 | PPO (Phase 9 · 08) | No replay buffer; easier to scale. / 无回放缓冲区；更易扩展。 |
| Offline RL / 离线 RL | CQL / IQL / Decision Transformer | Conservative Q targets, no bootstrapping blowups. / 保守 Q 目标，无自举爆炸。 |
| Large discrete action spaces (recommender) / 大离散动作空间（推荐） | DQN with action embedding, or IMPALA | Fine; decoration matters. / 可行；细节很重要。 |
| LLM RL / LLM RL | PPO / GRPO | Sequence-level, not step-level; different loss. / 序列级而非步级；不同损失。 |

لا تزال الدروس في السفر. تظهر إعادة التشغيل والشبكات المستهدفة في SAC ، TD3 ، DDPG ، SAC-X ، حافظة لعب الذاتية في AlphaZero ، وجميع أساليب RL غير متصلة بالإنترنت. تعيش قصف الجوائز كطبيعية فائدة في PPO. الهندسة المعمارية هي الخطوط المخططة.

> هذه التجارب لا تزال فعالة. وتعود وتظهر شبكة الهدف في SAC、TD3、DDPG、SAC-X、الفا زيرو في المنطقة التخفيفية الذاتية والطرق RL لكل إطلاق.

## أرسلها .

إبقوا`outputs/skill-dqn-trainer.md`:

```markdown
---
name: dqn-trainer
description: Produce a DQN training config (buffer, target sync, ε schedule, reward clipping) for a discrete-action RL task.
version: 1.0.0
phase: 9
lesson: 5
tags: [rl, dqn, deep-rl]
---

Given a discrete-action environment (observation shape, action count, horizon, reward scale), output:

1. Network. Architecture (MLP / CNN / Transformer), feature dim, depth.
2. Replay buffer. Capacity, minibatch size, warmup size.
3. Target network. Sync strategy (hard every C steps or soft τ).
4. Exploration. ε start / end / schedule length.
5. Loss. Huber vs MSE, gradient clip value, reward clipping rule.
6. Double DQN. On by default unless explicit reason to disable.

Refuse to ship a DQN with no target network, no replay buffer, or ε held at 1. Refuse continuous-action tasks (route to SAC / TD3). Flag any reward range > 10× per-step mean as needing clipping or scale normalization.
```

## تمارين التدريب

1. **Easy.**أركض`code/main.py`-سحب منحنى العودة لكل حلقة كم حلقة حتى تتجاوز المتوسط المتجاري -10؟
2. **Medium.**تعطيل شبكة الهدف (استخدم شبكة الإنترنت على جانبي هدف بيلمان). قياس عدم استقرار التدريب  هل تتذبذب العودة أو تختلف؟
3. **Hard.**إضافة DQN مزدوج: استخدم الشبكة على الانترنت لتحديد `argmax a'`، والهدف الشبكة لتقييم. مقارنة التحيز من`Q(s_0, best_a)`مقابل الحقيقة`V*(s_0)`بعد 1000 حلقة مع مقابل دون DQN المزدوج على جريد ورلد مكافأة ضوضاء.

## شروط الرئيسية

| Term | What people say | What it actually means |
|------|-----------------|-----------------------|
| DQN | "Deep Q-learning" / 深度Q网络 | Q-learning with a neural Q-function, replay buffer, and target network. |
| Experience replay | "Shuffled transitions" / 经验回放 | Ring buffer sampled uniformly each gradient step; decorrelates data. |
| Target network | "Frozen bootstrap" / 目标网络 | Periodic copy of Q used in the Bellman target; stabilizes training. |
| Deadly triad | "Why RL diverges" / 致命三要素 | Function approximation + bootstrapping + off-policy = no convergence guarantee. |
| Double DQN | "Fix for maximization bias" / 双重DQN | Online net selects action, target net evaluates it. |
| Dueling DQN | "V and A heads" / 决斗DQN | Decompose Q = V + A - mean(A); same output, better gradient flow. |
| Rainbow | "All the tricks" / Rainbow | DDQN + PER + dueling + n-step + noisy + distributional in one. |
| PER | "Prioritized Replay" / 优先经验回放 | Sample transitions proportional to TD-error magnitude. |

## المزيد من القراءة

- [Mnih et al. (2013). Playing Atari with Deep Reinforcement Learning](https://arxiv.org/abs/1312.5602)ورقة ورشة العمل في 2013 NeurIPS التي بدأت العميقة RL.
- [Mnih et al. (2015). Human-level control through deep reinforcement learning](https://www.nature.com/articles/nature14236)ورقة "نايچر" ، 49 لعبة DQN.
- [Hasselt, Guez, Silver (2016). Deep Reinforcement Learning with Double Q-learning](https://arxiv.org/abs/1509.06461) DDQN
- [Wang et al. (2016). Dueling Network Architectures](https://arxiv.org/abs/1511.06581)-تزاحم (دي.ك.ان)
- [Hessel et al. (2018). Rainbow: Combining Improvements in Deep RL](https://arxiv.org/abs/1710.02298)ورقة الحيل المكتظة
- [OpenAI Spinning Up — DQN](https://spinningup.openai.com/en/latest/algorithms/dqn.html) عرض حديث واضح
- [Sutton & Barto (2018). Ch. 9 — On-policy Prediction with Approximation](http://incompleteideas.net/book/RLbook2020.pdf) التعامل في الكتب الدراسية مع "التلاثة المميتة" (تقريب الوظيفة + إطلاق + خارج السياسة) التي تم تصميم شبكة DQN المستهدفة ومحافظة إعادة التشغيل لتدميرها.
- [CleanRL DQN implementation](https://docs.cleanrl.dev/rl-algorithms/dqn/) إشارة DQN ملف واحد المستخدم في دراسات التخلص؛ جيد للقراءة جنبا إلى جنب مع إصدار هذا الدروس من الصفر.
