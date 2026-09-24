# समय का अंतर  Q-Learning & SARSA  समय का अंतर  Q learning और SARSA

> मोन्टे कार्लो एपिसोड समाप्त होने तक इंतजार करता है। टीडी अगले मूल्य अनुमान को बूटस्ट्राप करके हर कदम के बाद अपडेट करता है। क्यू-लर्निंग ऑफ-पॉलिसी और आशावादी है; SARSA नीति पर है और सावधान है। दोनों कोड की एक पंक्ति हैं। दोनों इस चरण में हर गहरे आरएल विधि का आधार हैं।

> **【中文解读】**MC को अपडेट करने के लिए चक्र समाप्त होने तक इंतजार करना होगा,TD(समय की भिन्नता) प्रत्येक चरण में सब कुछ अपडेट किया जा सकता है उपयोग `r + γ V(s')`️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️️`max`लेकिन यह सभी गहरे आरएल की आधारशिला है।

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 9 · 01 (MDPs), Phase 9 · 02 (Dynamic Programming), Phase 9 · 03 (Monte Carlo) | **前置知识:** Phase 9 · 01 (MDP), Phase 9 · 02 (动态规划), Phase 9 · 03 (蒙特卡洛)
**Time:** ~75 minutes | **时间:** ~75 分钟

## समस्या  समस्या परिचय

मोन्टे कार्लो काम करता है लेकिन इसकी दो महंगी मांगें हैं। इसे एपिसोड की आवश्यकता होती है जो समाप्त हो जाते हैं, और यह केवल अंतिम वापसी के बाद अपडेट होता है। यदि आपका एपिसोड 1,000 चरणों का है, तो एमसी कुछ भी अपडेट करने के लिए 1,000 चरणों का इंतजार करता है। यह उच्च-विभिन्नता, कम पूर्वाग्रह और अभ्यास में धीमा है।

> 蒙特卡洛 प्रभावी है लेकिन दो महंगे आवश्यकताएँ हैं। इसे समाप्त करने के लिए चक्र की आवश्यकता होती है, और केवल अंतिम प्रतिक्रिया के बाद ही अपडेट किया जाता है। यदि चक्र में 1,000 चरण होते हैं, तो एमसी को कुछ भी अपडेट करने के लिए 1,000 चरणों का इंतजार करना चाहिए।

गतिशील प्रोग्रामिंग का विपरीत प्रोफ़ाइल है  शून्य-विभेद बूटस्ट्रैप बैकअप  लेकिन एक ज्ञात मॉडल की आवश्यकता होती है।

> 动态规划有相反的特点零方差的自举备份但需要已知模型

समय अंतर (टीडी) सीखने से अंतर को विभाजित किया जाता है।`(s, a, r, s')`, एक कदम का लक्ष्य बनाओ`r + γ V(s')`और धक्का`V(s)`कोई मॉडल नहीं, कोई पूर्ण एपिसोड नहीं, अनुमानित उपयोग से पूर्वाग्रह`V`आरएचएस पर, लेकिन सीएम और ऑनलाइन अपडेट से नाटकीय रूप से कम भिन्नता चरण एक से.

> 时序差分(TD) सीखने का समय दो में से एक है।`(s, a, r, s')`构建单步目标 `r + γ V(s')`,将 `V(s)`                                                                                                                                                                                                                                                              `V`जबकि अंतर एमसी से बहुत कम है, यह पहले चरण से ही ऑनलाइन अपडेट हो सकता है।

यह वह पिव्वट है जिस पर आधुनिक आरएल  डीक्यूएन, ए 2 सी, पीपीओ, एसएसी  घूमता है। शेष चरण 9 कार्य अनुमान और ट्रिक्स की परतें हैं जो इस पाठ में आप लिखने वाले एक चरण के टीडी अपडेट के ऊपर निर्मित हैं।

> यह सभी आधुनिक आरएलडीक्यूएन、ए2सी、पीपीओ、एसएसी के केंद्रों में से है। चरण 9 के शेष भाग इस कक्षा में आप एक चरण में लिखे जाने वाले एक चरण में TD 更新 पर निर्मित कार्य की बारीकियों और कौशल परतों में है।

> **【中文解读】**टीडी सीखने का एक ही चरण में परिवर्तन होता है।`(s,a,r,s')`构造目标 `r + γV(s')`, मॉडल की आवश्यकता नहीं है, न ही पूर्ण चक्र की आवश्यकता है।

> **【拓展：游戏AI→LLM对齐】**Q-learning 2013 में Atari DQN का केंद्र था, जिसने गहन RL 时代 को शुरू किया।

## अवधारणा का मूल अवधारणा

![Q-learning vs SARSA: off-policy max vs on-policy Q(s', a')](../assets/td.svg)

**The TD(0) update for V:**

`V(s) ← V(s) + α [r + γ V(s') - V(s)]`

ब्रेस किए गए मात्रा टीडी त्रुटि है `δ = r + γ V(s') - V(s)`यह `G_t - V(s_t)`एमसी में अभिसरण की आवश्यकता होती है`α`रोबिन-मोंरो को संतुष्ट करने के लिए (`Σ α = ∞`,`Σ α² < ∞`) और सभी राज्यों का अनगिनत बार दौरा किया।

> **V 的 TD(0) 更新：**括号中量是 TD 误差 `δ = r + γ V(s') - V(s)` यह एमसी में है `G_t - V(s_t)`                                                                                                                                                                                                                                                              `α`满足 रॉबिन्स-मोंरो 条件且所有状态被无限次访问──

**Q-learning.**नियंत्रण के लिए नीतिगत TD विधिः

`Q(s, a) ← Q(s, a) + α [r + γ max_{a'} Q(s', a') - Q(s, a)]`

`max`यह मानता है कि * लोभी* नीति का पालन किया जाएगा`s'`आगे, चाहे एजेंट वास्तव में क्या कार्रवाई करता है. यह डिकूपलिंग Q-लर्निंग सीखने बनाता है`Q*`जबकि एजेंट ε-गामी के माध्यम से खोजता है। Mnih et al. (2015) ने इसे अटारी पर गहन Q-लर्निंग में परिवर्तित किया (लर्निंग 05).

> **Q-learning。**एक अलग रणनीति टीडी  नियंत्रण विधि`max`假设从 `s'`开始将遵循*贪心*策略,无论智能体实际上采取什么动作──这种解使 Q-learning在通过 ε-贪心探索的同时学习 `Q*`Mnih 等人 (2015) इसे अत्तारी 上的深度 Q-learning में बदल देगा

**SARSA.**नीतिगत टीडी विधिः

`Q(s, a) ← Q(s, a) + α [r + γ Q(s', a') - Q(s, a)]`

नाम है टूपल `(s, a, r, s', a')`SARSA कार्रवाई का उपयोग करता है `a'`एजेंट *वास्तव में* अगला लेता है, लालची नहीं `argmax`. `Q^π`जो भी ε-लाभकारी के लिए `π`चल रहा है, जो सीमा में है `ε → 0`बन जाता है`Q*`. .

> **SARSA。**एक प्रकार की ऑनलाइन रणनीति टीडी विधि---नाम है एक समूह`(s, a, r, s', a')`✿SARSA 使用智能体*实际*采取的下一个动作 ✿`a'`और न ही लालच से`argmax`收到当前 ε-贪心 `π``Q^π`, में `ε → 0`                                                                                                                                                                                                                                                              `Q*`

**The cliff-walking difference.**क्लासिक चट्टान-चढ़ाने के कार्य पर (fall-off-cliff = reward -100), Q-learning चट्टान के किनारे के साथ इष्टतम पथ सीखता है लेकिन कभी-कभी खोज के दौरान दंड लेता है। SARSA चट्टान से एक कदम दूर एक सुरक्षित पथ सीखता है क्योंकि यह खोज शोर को अपने Q-मूल्य में कारगर बनाता है। प्रशिक्षण के साथ, दोनों इष्टतम पर पहुंचते हैं।`ε → 0`. व्यवहार में यह मायने रखता हैः जब वास्तव में परिचालन पर अन्वेषण हो रहा है, तो SARSA का व्यवहार अधिक रूढ़िवादी है।

> **【中文解读】** क्लासिक क्लिपशिप ट्रेकिंग प्रयोगों से क्यू-लर्निंग और SARSA के बीच महत्वपूर्ण अंतर पता चलता हैः क्यू-लर्निंग सीखें कि सबसे अच्छा मार्ग क्या है जो कि चट्टान पर है, लेकिन खोज के समय गिर जाता है, SARSA सीखें कि चट्टान से दूर सुरक्षित मार्ग क्या है क्योंकि यह खोज शोर पर विचार करता है।

**Expected SARSA.**प्रतिस्थापन`Q(s', a')``π`:

`Q(s, a) ← Q(s, a) + α [r + γ Σ_{a'} π(a'|s') Q(s', a') - Q(s, a)]`

SARSA से कम भिन्नता (कोई नमूना नहीं)`a'`), नीतिगत लक्ष्य पर एक ही। अक्सर आधुनिक पाठ्यपुस्तकों में डिफ़ॉल्ट।

> **期望 SARSA。**उपयोग `π`निम्न अपेक्षित मूल्य प्रतिस्थापन `Q(s', a')` SARSA 方差更低无需采样 `a'`), उसी में ऑनलाइन रणनीति लक्ष्य── हमेशा आधुनिक पाठ्यपुस्तकों के रूप में默认选择──

**n-step TD and TD(λ).**TD(0) और MC के बीच प्रतीक्षा करके अंतरण करें `n`बूटस्ट्रेपिंग से पहले कदम। `n=1`TD है, `n=∞`है MC. TD(λ) सभी पर औसत `n`ज्यामितीय भार के साथ `(1-λ)λ^{n-1}`. अधिकांश गहरे आरएल उपयोग `n`3 से 20 के बीच।

> **n 步 TD 和 TD(λ)。**TD(0) और MC  के बीच में प्रवेश मूल्य, प्रतीक्षा `n`步再自举──`n=1`TD,`n=∞`है MC---TD(λ) उपयोग几何权重对所有 `n`取平均──大多数深度 RL 使用 `n`3 से 20 के बीच में।

> **【拓展：TD 误差在 LLM RLHF 中的对应】**टीडी 误差 δ = r + γV(s') - V(s) LLM के RLHF 训练中直接对应:PPO का优势函数 A = r + γV(s') - V(s) 就是 TD 误差的变体──每生成一个代币,计算当前代币的奖励──来自RM)加上评论对未来价值的估计减减当前估计──理解 TD 误差是理解 PPO 优势函数的关键──

## इसे बनाओ, इसे पूरा करो।
```figure
qlearning-gridworld
```

## इसे बनाओ

### चरण 1: लालचपूर्ण नीति पर SARSA

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

Q-Learning से *केवल* अंतर लक्ष्य रेखा है।

> 八行代码── Q-learning के साथ *अकेला* अंतर है लक्ष्य行──

### चरण 2: Q-learning

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

`max`यह एक प्रतीक है नीतिगत और गैर-नीतिगत के बीच अंतर है।

> `max`लक्ष्य और व्यवहार को परिभाषित करना। यह एक प्रतीक है जो ऑनलाइन रणनीति और अप्लॉएज रणनीति में अंतर है।

### चरण 3: सीखने की वक्रता

100 एपिसोड पर ट्रैक औसत रिटर्न। सरल निर्धारात्मक ग्रिडवर्ल्ड पर क्यू-लर्निंग तेजी से अभिसरण करता है; चट्टान पर चलने पर SARSA अधिक रूढ़िवादी है।`code/main.py`, दोनों लगभग अनुकूल हैं ~ 2,000 एपिसोड के बाद के साथ `α=0.1, ε=0.1`. .

> प्रति 100 प्रतिशोधों का औसत प्रतिशोधों में Q-learning में सरल निश्चितता GridWorld ऊपर प्राप्त करने के लिए अधिक तेजी से; SARSA पर चट्टानों पर चलने पर अधिक संरक्षित में`code/main.py`की 4×4 ग्रिडवर्ल्ड ऊपर, दो में `α=0.1, ε=0.1`नीचे लगभग 2,000 पल बाद करीब सबसे अच्छा

### चरण 4: डीपी सत्य की तुलना करें

प्राप्त करने के लिए रन मूल्य पुनरावृत्ति (लक्ष्मी 02)`Q*`चेक करें`max_{s,a} |Q_learned(s,a) - Q*(s,a)|`. एक स्वस्थ तालिकाबद्ध टीडी एजेंट के भीतर लैंडिंग `~0.5`4×4 ग्रिडवर्ल्ड पर 10,000 एपिसोड के बाद।

> 运行值代(लक्ष 02) प्राप्त `Q*` जाँच `max_{s,a} |Q_learned(s,a) - Q*(s,a)|`एक स्वस्थ आकृति TD 智能体在10,000 回合后在4×4 GridWorld 上误差在 `~0.5`में

## फंदे

- **Initial Q values matter.**आशावादी आरंभ (`Q = 0`एक नकारात्मक-पुरस्कार कार्य के लिए) खोज को प्रोत्साहित करता है।
  **初始 Q 值很重要。**乐观初始化 负奖励任务中 `Q = 0`) को प्रोत्साहित करना अन्वेषण करना।
- **α schedule.**निरंतर`α`यह गैर-स्थिर समस्याओं के लिए ठीक है।`α_n = 1/n`सिद्धांत में अभिसरण देता है लेकिन व्यवहार में बहुत धीमा होता है  पिन `α`में `[0.05, 0.3]`और सीखने की वक्रता की निगरानी करें।
  **α 调度。**常数 `α`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             `α_n = 1/n` सिद्धांत रूप में प्राप्त करना, लेकिन अभ्यास में बहुत धीमा होना`α`固定在 `[0.05, 0.3]`और सीखने की दिशा की निगरानी करना।
- **ε schedule.**उच्च प्रारंभ (`ε=1.0`), क्षय करने के लिए `ε=0.05`. "GLIE" (असीम अन्वेषण के साथ सीमा में लालची) अभिसरण की स्थिति है।
  **ε 调度。**से高值开始`ε=1.0`), घटकर `ε=0.05` "GLIE"极极极贪心且无限探索)                                                                                                                                                                                                                                                       
- **Max bias in Q-learning.**`max`ऑपरेटर ऊपर की ओर पूर्वाग्रह है जब `Q` हेसल्ट के डबल क्यू-लर्निंग (जे कि डडीक्यूएन ने पाठ 05) में इस्तेमाल किया है) दो क्यू तालिकाओं के साथ इसे ठीक करता है।
  **Q-learning 的最大化偏差。** `max`算子在 `Q` हसेल्ट का द्विवार्षिक Q-लर्निंग (DQN) दो Q के साथ
- **Non-terminating episodes.**टीडी टर्मिनल के बिना सीख सकता है, लेकिन आपको या तो चरणों को कैप करना होगा या कैप पर बूटस्ट्रैप को सही ढंग से संभालना होगा। मानकः कैप को गैर-टर्मिनल के रूप में व्यवहार करें, बूटस्ट्रैप करना जारी रखें।
  **非终止回合。**टीडी को अनंत स्थिति में सीखना संभव है, लेकिन इसे चरणों की संख्या की सीमा पर या सही ढंग से सीमा पर काम करने के लिए सेट करने की आवश्यकता होती है।
- **State hashing.**यदि राज्य टूपल्स/टेंसर हैं, तो एक हैश करने योग्य कुंजी (टूपल, सूची नहीं; टूपल फ्लोट्स गोल, कच्चे नहीं) का उपयोग करें।
  **状态哈希。**यदि स्थिति है युनिट/张量, उपयोग कर सकते हैं की ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह ह

## इसे फ्रेमवर्क के साथ लागू करें

2026 में टीडी परिदृश्यः

> 2026 साल के टीडी 学习 के संस्करणः

| Task | Method | Reason |
|------|--------|--------|
| Task / 任务 | Method / 方法 | Reason / 原因 |
| Small tabular environments / 小型表格环境 | Q-learning | Learns optimal policy directly. / 直接学习最优策略。 |
| On-policy safety-critical / 在线策略安全关键 | SARSA / Expected SARSA | Conservative during exploration. / 探索期间保守。 |
| High-dimensional state / 高维状态 | DQN (Phase 9 · 05) | Neural-net Q-function with replay and target net. / 神经网络 Q 函数+回放+目标网络。 |
| Continuous actions / 连续动作 | SAC / TD3 (Phase 9 · 07) | TD update on a Q-network; policy net emits actions. / Q 网络上的 TD 更新；策略网络输出动作。 |
| LLM RL (reward-model-based) / LLM RL（基于奖励模型） | PPO / GRPO (Phase 9 · 08, 12) | Actor-critic with TD-style advantage via GAE. / Actor-Critic + GAE 的 TD 式优势。 |
| Offline RL / 离线 RL | CQL / IQL (Phase 9 · 08) | Q-learning with conservative regularization. / 带保守正则化的 Q-learning。 |

2026 के पेपर में आप जो "RL" पढ़ते हैं उनमें से 90 प्रतिशत Q-learning या SARSA का कुछ विस्तार है। आगे पढ़ने से पहले अपनी उंगलियों में तालिका अद्यतन को समझें।

> 2026 साल के पेपर में आपने जो "RL" पढ़ा है, उसका 90% Q-learning या SARSA का एक प्रकार का है।

## इसे भेजें उत्पाद

`outputs/skill-td-agent.md`:

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

## अभ्यास विषय

1. **Easy.**4 × 4 ग्रिडवर्ल्ड पर क्यू-लर्निंग और SARSA लागू करें। 2,000 एपिसोड के लिए प्लॉट सीखने के वक्र (प्रति 100 एपिसोड औसत रिटर्न) बनाएं। कौन तेजी से अभिसरण करता है?
   > **练习1：**Q-Learning और SARSA के मुकाबले GridWorld में सीखने की वक्रता
2. **Medium.**एक चट्टान-चलने वाले वातावरण (4×12, अंतिम पंक्ति -100 के साथ चट्टान है और आरंभ करने के लिए रीसेट करें) । Q-learning और SARSA अंतिम नीतियों की तुलना करें। प्रत्येक पथ का स्क्रीनशॉट लें। चट्टान के करीब कौन सा है?
   > **练习2：**                                                                                                                                                                                                                                                              
3. **Hard.**दोहरे Q-लर्निंग को लागू करें। शोर-पुरस्कार ग्रिडवर्ल्ड (गॉसियन शोर σ=5 प्रति चरण पुरस्कार में जोड़ा गया) पर Q-लर्निंग की अतिशयोक्ति दिखाएं `V*(0,0)`जबकि डबल क्यू-लर्निंग नहीं करता है।
   > **练习3：** द्वि-वज़न Q-लर्निंग को प्राप्त करना, यह Q-लर्निंग के अधिकतम विकृति को समाप्त कर सकता है।

## कीवर्ड्स  शब्द खोज तालिका

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

## आगे पढ़ना 延伸閱讀

- [Watkins & Dayan (1992). Q-learning](https://link.springer.com/article/10.1007/BF00992698) मूल कागज और अभिसरण प्रमाण।
- [Sutton & Barto (2018). Ch. 6 — Temporal-Difference Learning](http://incompleteideas.net/book/RLbook2020.pdf) TD(0), SARSA, Q-learning, अपेक्षित SARSA।
- [Hasselt (2010). Double Q-learning](https://papers.nips.cc/paper_files/paper/2010/hash/091d584fced301b442654dd8c23b3fc9-Abstract.html) अधिकतम पूर्वाग्रह के लिए फिक्स।
- [Seijen, Hasselt, Whiteson, Wiering (2009). A Theoretical and Empirical Analysis of Expected SARSA](https://ieeexplore.ieee.org/document/4927542) अपेक्षित SARSA प्रेरणा।
- [Rummery & Niranjan (1994). On-line Q-learning using connectionist systems](https://www.researchgate.net/publication/2500611_On-Line_Q-Learning_Using_Connectionist_Systems) पेपर जो SARSA (तब "परिवर्तनवादी Q-learning" कहा जाता था) का निर्माण किया।
- [Sutton & Barto (2018). Ch. 7 — n-step Bootstrapping](http://incompleteideas.net/book/RLbook2020.pdf) TD(0) को TD(n) में सामान्यीकरण करता है, Q-learning से पात्रता के निशान तक और बाद में, PPO में GAE तक का रास्ता।
