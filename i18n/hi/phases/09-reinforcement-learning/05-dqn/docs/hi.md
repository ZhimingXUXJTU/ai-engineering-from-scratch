# डीप क्यू नेटवर्क (डीक्यूएन)

> 2013: एमएनआई ने कच्चे पिक्सेल पर एक क्यू-लर्निंग नेटवर्क को प्रशिक्षित किया, सात एटारी गेम पर हर क्लासिक आरएल एजेंट को हराया। 2015: 49 गेम तक बढ़ाया, नेचर में प्रकाशित, गहरे आरएल युग को जन्म दिया। डीक्यूएन क्यू-लर्निंग प्लस तीन ट्रिक्स है जो फ़ंक्शन अनुमान को स्थिर बनाते हैं।

> **【中文解读】**डीक्यूएन = क्यू-लर्निंग + न्यूरियल नेटवर्क + तीन स्थिरता तकनीकें (अनुभव पुनःप्रसारण, लक्ष्य नेटवर्क, पुरस्कार काटा) ◊2013-2015 के दौरान एटारी  गेम पर सभी क्लासिक आरएल  पद्धतियों को हराकर, गहन आरएल 时代 शुरू हुई। इन तीनों तकनीकों का उपयोग आज भी सभी गहन आरएल  पद्धतियों में किया जाता है।

**Type:** Build | **类型:** 动手
**Languages:** Python | **语言:** Python
**Prerequisites:** Phase 3 · 03 (Backpropagation), Phase 9 · 04 (Q-learning, SARSA) | **前置知识:** Phase 3 · 03 (反向传播), Phase 9 · 04 (Q-learning, SARSA)
**Time:** ~75 minutes | **时间:** ~75 分钟

## समस्या  समस्या परिचय

तालिकात्मक क्यू-लर्निंग को प्रत्येक (स्थिति, कार्रवाई) जोड़ी के लिए एक अलग क्यू-मूल्य की आवश्यकता होती है। एक शतरंज बोर्ड में ~1043 राज्य होते हैं। एक अटारी फ्रेम 210 × 160 × 3 = 100,800 विशेषताएं होती हैं। तालिकात्मक आरएल हजारों राज्यों में मर जाता है, अरबों को छोड़ दें।

> एक अटारी  में 210×160×3 = 100,800 个特征──表格 RL में हजारों राज्यों में पहले से ही विफल हो गया है, और अरबों को कहने की जरूरत नहीं है──

पीछे की ओर देखते हुए समाधान स्पष्ट हैः क्यू-टेबल को न्यूरल नेटवर्क से बदलें, `Q(s, a; θ)`. लेकिन स्पष्ट-इन-पछाड़ में दशकों लग गए। "मृत्यु त्रयी" के तहत साफ़-साफ़ फ़ंक्शन समीकरण और क्यू-लर्निंग के साथ अंतर  फ़ंक्शन समीकरण + बूटस्ट्रेपिंग + नीतिगत सीखने। Mnih et al. (2013, 2015) ने तीन इंजीनियरिंग ट्रिक्स की पहचान की जो सीखने को स्थिर करते हैंः

> समस्या का हल बहुत सरल हैः तंत्रिका नेटवर्क का उपयोग करें।`Q(s, a; θ)`√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√√

1. **Experience replay**परिवर्तनों को विकोरेल करता है।
   **经验回放**打破转移的时间相关性──
2. **Target network**बूटस्ट्रैप लक्ष्य को जमे हुए है।
   **目标网络**结自举目标──
3. **Reward clipping**ग्रेडिएंट मैग्निटी को सामान्य बनाता है।
   **奖励裁剪**归一化梯度量级――

अत्तारी पर डीक्यूएन पहली बार एक एकल आर्किटेक्चर था जिसमें एक ही हाइपरपैरामीटर सेट था जिसने कच्चे पिक्सल से दर्जनों नियंत्रण समस्याओं को हल किया।  DDQN, रेनबॉउ, डुअल, डिस्ट्रीब्यूशनल, R2D2, एजेंट57  के बाद से निर्मित सभी "दीप-आरएल" इस तीन-ट्रिक आधार के शीर्ष पर ढेर किए गए हैं।

> अत्तारी के ऊपर DQN पहली बार एकल संरचना और एकल सुपरपरमाइंडर सेट का उपयोग करके मूल चित्रण से दर्जनों नियंत्रण समस्याओं को हल करने के लिए किया गया था। इसके बाद सभी "गहनता RL" DDQN、 रेनबॉउ、ड्यूलिंग、 डिस्ट्रीब्यूशनल、R2D2、एजेंट57 सभी इन तीन तकनीकों पर आधारित हैं।

> **【中文解读】**"मौतिक तीन तत्व": फ़ंक्शन नजदीक + स्वयं उठ + 离策略 → 训练不稳定甚至发散――DQN के तीन तकनीकें इस समस्या को हल करती हैंः

> **【拓展：经验回放→RLHF】**अनुभव पुनःप्रसार (अनुभव पुनःप्रसार) का विचार LLM प्रशिक्षण में अनुपस्थित हैःPPO प्रशिक्षण के दौरान बफर、RLHF में प्राथमिकता डेटा संग्रह、DPO के ऑफ़लाइन डेटामूलतः "बैक डेटा प्रासंगिकता、反复利用 अनुभव" हैं।

## अवधारणा का मूल अवधारणा

![DQN training loop: env, replay buffer, online net, target net, Bellman TD loss](../assets/dqn.svg)

**The objective.**डीक्यूएन न्यूरल क्यू-फंक्शन पर एक चरण में टीडी हानि को कम करता हैः

`L(θ) = E_{(s,a,r,s')~D} [ (r + γ max_{a'} Q(s', a'; θ^-) - Q(s, a; θ))² ]`

`θ`= ऑनलाइन नेटवर्क, gradient descending के प्रत्येक चरण में अद्यतन। `θ^-`= लक्ष्य नेटवर्क, से आवधिक रूप से कॉपी `θ`(हर ~ 10,000 कदम) ।`D`= पिछले संक्रमणों का पुनःपूर्ति बफर।

> **目标。**DQN 最小化神经 Q 函数 पर एक कदम TD 损失──`θ`= 在线网络, प्रत्येक चरण से नीचे नीचे अपडेट`θ^-`= 目标网络, नियमित रूप से `θ`复制(約每 10,000 步) `D`= 过去转移的回放缓冲区──

**The three tricks, in order of importance:**

> **三个技巧，按重要性排序：**

**Experience replay.**एक रिंग बफर के `~10⁶`प्रत्येक प्रशिक्षण चरण एक मिनी बैच को समान रूप से यादृच्छिक रूप से नमूना देता है। यह temporal correlation (लगातार फ्रेम लगभग समान होते हैं) को तोड़ता है, नेटवर्क को कई बार दुर्लभ फायदेमंद संक्रमणों से सीखने देता है, और लगातार ग्रेडिएंट अपडेट को decorrects करता है। इसके बिना, एक तंत्रिका नेटवर्क के साथ ऑन-पॉलिसी TD Atari पर भिन्न होता है।

> **经验回放。**एक लगभग 106 बार स्थानांतरण के चक्रवर्ती ढलान क्षेत्र। प्रत्येक प्रशिक्षण चरण के साथ-साथ एक छोटे से बैच के रूप में किया जाता है।

**Target network.**एक ही नेटवर्क का उपयोग `Q(·; θ)`बेलमैन समीकरण के दोनों पक्षों पर लक्ष्य हर अद्यतन को स्थानांतरित करता है  "अपने खुद के पूंछ का पीछा करना।" फिक्सः एक दूसरे नेटवर्क बनाए रखें `Q(·; θ^-)`जमे हुए वजन के साथ।`C`कदम, प्रतिलिपि `θ → θ^-`. यह एक बार में हजारों ग्रेडिएंट चरणों के लिए विघटन लक्ष्य को स्थिर करता है.`θ^- ← τ θ + (1-τ) θ^-`(डीडीपीजी, एसएसी में प्रयोग) एक सुचारू संस्करण है।

> **目标网络。**बेलमैन समीकरण के दोनों पक्षों पर एक ही नेटवर्क का उपयोग करना लक्ष्य को प्रत्येक अद्यतन में सभी को "अपने खुद के尾巴 का पीछा करना" करने के लिए बनाता है।`C`步复制 `θ → θ^-`◊ 软更新(DDPG、SAC 中使用) अधिक सुगम变体──

**Reward clipping.**अत्तारी पुरस्कार की मात्रा 1 से 1000+ तक होती है।`{-1, 0, +1}`जब पुरस्कार का आकार मायने रखता है तो गलत; अत्तारी के लिए ठीक है जहां केवल हस्ताक्षर मायने रखते हैं।

> **奖励裁剪。**अत्तारी  पुरस्कार राशि 1 से 1000+ तक `{-1, 0, +1}` किसी भी एकल खेल के प्रमुख स्तर को रोकने के लिए

**Double DQN.**Hasselt (2016) अधिकतम पूर्वाग्रह को ठीक करता हैः कार्रवाई का चयन करने के लिए ऑनलाइन नेट का उपयोग करें, लक्ष्य नेट का उपयोग करने के लिए * मूल्यांकन करें।

`target = r + γ Q(s', argmax_{a'} Q(s', a'; θ); θ^-)`

डिफ़ॉल्ट रूप से इसे उपयोग करें।

> **双重 DQN。**Hasselt (2016) 修复最大化偏差:用在线网络*选择*动作,用目标网络*评估*它──直接替换,始终更好──默认使用──

**Other improvements (Rainbow, 2017):**प्राथमिकता पुनरावृत्ति (उच्च टीडी-त्रुटि के लिए नमूना संक्रमण अधिक), द्वंद्व वास्तुकला (अलग `V(s)`और लाभ सिर), शोर नेटवर्क (लर्निंग एक्सप्लोरेशन), n-चरण रिटर्न, वितरण Q (C51/QR-DQN), बहु-चरण बूटस्ट्रेपिंग। प्रत्येक कुछ प्रतिशत जोड़ता है; लाभ लगभग योग हैं।

> **其他改进（Rainbow, 2017）：**优先回放、决斗架构、噪声网络、n 步回报、分布式 Q、多步自举── प्रत्येक सुधार में योगदान कुछ सौ अंक;收益大致可叠加──

> **【拓展：Rainbow DQN 与集成改进】**रेनबॉय डीक्यूएन(2017) में 6 प्रकार के डीक्यूएन सुधारों को एक साथ एकीकृत किया जाएगाः प्राथमिकता अनुभव पुनःप्रसारण, डुअल संरचना, शोर नेटवर्क खोज, वितरण Q सीखने, कई चरणों से कदम उठाने। प्रत्येक सुधार में कुछ प्रतिशत अंक का योगदान प्रदर्शन में सुधार, संयोजन प्रभाव उल्लेखनीय है।

## इसे बनाओ, इसे पूरा करो।
```figure
f3-dqn-stability
```

## इसे बनाओ

यहाँ कोड केवल stdlib-numpy-free है  हम एक छोटे से निरंतर ग्रिडवर्ल्ड पर एक हाथ से रोल किए गए एकल छिपे हुए परत MLP का उपयोग करते हैं, इसलिए प्रत्येक प्रशिक्षण चरण माइक्रोसेकंड में चलता है। एल्गोरिथ्म पैमाने पर Atari DQN के समान है।

> यहाँ कोड केवल मानक पुस्तकालय में एक माइक्रो प्रकार के连续 GridWorld ऊपर हाथ से उपयोग के लिए लिखा गया एकल छिपे हुए परत MLP  एल्गोरिथ्म बड़े पैमाने पर Atari DQN  पूरी तरह से समान 

### चरण 1: पुनःपूर्ति बफर

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

~ 50 हजार क्षमता एटारी के लिए; 5000 हमारे खिलौना पर्यावरण के लिए पर्याप्त है।

> अत्तारी को 50,000 की क्षमता चाहिए, हमारे खेल के लिए 5,000 पर्याप्त हैं।

### चरण 2: एक छोटा Q-नेटवर्क (मैनुअल MLP)

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

आगे की पारः रैखिक → ReLU → रैखिक। यह पूरे जाल है।

> 前向传播:线性 → ReLU → 线性── यह संपूर्ण नेटवर्क है──

### चरण 3: डीक्यूएन अद्यतन

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

आकार दो अंतर के साथ पाठ 04 से Q-लर्निंग हैः (क) हम एक अंतर के माध्यम से backprop `Q(·; θ)`तालिका को अनुक्रमित करने के बजाय, (ख) लक्ष्य उपयोग `Q(·; θ^-)`. .

> 形式 से पाठ 04 के Q-learning समान है, लेकिन दो अंतर हैंः`Q(·; θ)`विपरीत प्रसार तथा गैर सूचकांक表格,`Q(·; θ^-)`

### चरण 4: बाहरी लूप

प्रत्येक एपिसोड के लिए, काम ε-लाभकारी पर `Q(·; θ)`, बफर में संक्रमण धक्का, एक मिनी बैच का नमूना, एक ग्रेडिएंट कदम ले, आवधिक रूप से सिंक्रनाइज़ `θ^- ← θ`. . पैटर्नः

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

हमारे छोटे ग्रिडवर्ल्ड में 16 आयाम के एक-गर्म राज्य के साथ, एजेंट लगभग 500 एपिसोड में एक आदर्श नीति सीखता है।

> 16 आयाम के एक-गर्म राज्य के माइक्रोटाइप ग्रिडवर्ल्ड पर, हमारे स्मार्ट बॉडीज लगभग 500 प्रतिभागियों में सबसे अच्छा रणनीति के करीब सीखने में सक्षम हुए।

## फंदे

- **Deadly triad.**फ़ंक्शन अनुमान + ऑफ-पॉलिसी + बूटस्ट्रेपिंग भिन्न हो सकते हैं। DQN लक्ष्य नेट + रिप्ले के साथ कम करता है; दोनों को न हटाएं।
  **致命三要素。**函数近似+离策略+自举可能发散──DQN 通过目标网络+回放缓解; किसी भी को न हटाएं──
- **Exploration.**प्रशिक्षण के पहले ~ 10% के दौरान सामान्य रूप से 1.0 से 0.01 तक घटना चाहिए। पर्याप्त प्रारंभिक खोज के बिना Q-नेट स्थानीय बेसिन में अभिसरण करता है।
  **探索。**                                                                                                                                                                                                                                                              
- **Overestimation.** `max`शोर-शोर Q के ऊपर पक्षपात है। उत्पादन में हमेशा डबल DQN का उपयोग करें।
  **过估计。**शोर के लिए प्रश्न`max`उत्तरी ओर निर्भरता
- **Reward scale.**पुरस्कारों को क्लिप या सामान्य करें; ग्रेडिएंट परिमाण पुरस्कार परिमाण के समानुपातिक है।
  **奖励尺度。** कटौती या एकीकरण पुरस्कार; डिग्री स्तर और पुरस्कार स्तर के समान अनुपात में
- **Replay buffer coldstart.**बफर कुछ हजार संक्रमण है जब तक प्रशिक्षण नहीं है. ~ 20 नमूने पर प्रारंभिक gradients overfit.
  **回放缓冲区冷启动。**缓冲区 में कुछ हजार बार स्थानांतरण के बाद पुनः प्रशिक्षण किया गया है।
- **Target sync frequency.**बहुत बार ≈ कोई लक्ष्य नेट; बहुत कम ≈ पुराने लक्ष्य। Atari DQN 10,000 एनवी चरणों का उपयोग करता है। अंगूठे का नियमः प्रशिक्षण क्षितिज के हर ~1/100 को सिंक्रनाइज़ करें।
  **目标同步频率。**太频繁≈没有目标网络;太不频繁≈过时目标――अनुभव विधि: प्रति 1/100 训练视野同步一次――
- **Observation preprocessing.**एटारी डीक्यूएन ने मार्कोव स्टेट बनाने के लिए 4 फ्रेम स्टैक किए हैं। गति जानकारी वाले किसी भी एनवी को फ्रेम स्टैकिंग या रिकर्सिव स्टेट की आवश्यकता होती है।
  **观测预处理。**अत्तारी डीक्यूएन 堆叠 4 使状态满足马尔可夫性── किसी भी गति से सूचना के वातावरण के सभी 堆叠 या परिपत्र राज्य── की आवश्यकता होती है।

## इसे फ्रेमवर्क के साथ लागू करें

2026 में, डीक्यूएन शायद ही कभी अत्याधुनिक होता है लेकिन संदर्भ नीतिगत एल्गोरिथ्म बना रहता हैः

> 2026 में, डीक्यूएन  बहुत कम उन्नत है, लेकिन अभी भी रणनीति एल्गोरिथ्म से दूर हैः

| Task | Method of choice | Why not DQN? |
|------|------------------|--------------|
| Task / 任务 | Method of choice / 首选方法 | Why not DQN? / 为什么不用 DQN？ |
| Discrete-action Atari-like / 离散动作类 Atari | Rainbow DQN or Muesli | Same framework, more tricks. / 相同框架，更多技巧。 |
| Continuous control / 连续控制 | SAC / TD3 (Phase 9 · 07) | DQN has no policy network. / DQN 没有策略网络。 |
| On-policy / high-throughput / 在线策略/高吞吐 | PPO (Phase 9 · 08) | No replay buffer; easier to scale. / 无回放缓冲区；更易扩展。 |
| Offline RL / 离线 RL | CQL / IQL / Decision Transformer | Conservative Q targets, no bootstrapping blowups. / 保守 Q 目标，无自举爆炸。 |
| Large discrete action spaces (recommender) / 大离散动作空间（推荐） | DQN with action embedding, or IMPALA | Fine; decoration matters. / 可行；细节很重要。 |
| LLM RL / LLM RL | PPO / GRPO | Sequence-level, not step-level; different loss. / 序列级而非步级；不同损失。 |

पाठ अभी भी यात्रा करते हैं। रीप्ले और लक्ष्य नेटवर्क एसएसी, टीडी 3, डीडीपीजी, एसएसी-एक्स, अल्फाज़ेरो के स्वयं-प्ले बफर और हर ऑफ़लाइन आरएल विधि में दिखाई देते हैं। पुरस्कार क्लिपिंग पीपीओ में लाभ सामान्यीकरण के रूप में रहता है। वास्तुकला ब्लूप्रिंट है।

> ये अनुभव अभी भी प्रभावी हैं। पुनरावृत्ति और लक्ष्य नेटवर्क में SAC, TD3, DDPG, SAC-X, AlphaZero के स्वयं-प्रदर्शन और प्रत्येक अप-लाइन आरएल विधि में दिखाई देते हैं।

## इसे भेजें उत्पाद

`outputs/skill-dqn-trainer.md`:

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

## अभ्यास विषय

1. **Easy.**दौड़ें`code/main.py`. प्रति एपिसोड वापसी वक्र का पता लगाएं. कितने एपिसोड जब तक चल रही औसत -10 से अधिक नहीं हो जाता?
2. **Medium.**लक्ष्य नेटवर्क को अक्षम करें (बेलमैन लक्ष्य के दोनों पक्षों के लिए ऑनलाइन नेटवर्क का उपयोग करें) प्रशिक्षण अस्थिरता का माप करें  क्या रिटर्न ऑस्स्स्किलेट या डिवर्ज है?
3. **Hard.**डबल डीक्यूएन जोड़ेंः ऑनलाइन नेट का उपयोग करके चुनें `argmax a'`, लक्ष्य नेट का मूल्यांकन करने के लिए।`Q(s_0, best_a)`सत्य के विरुद्ध`V*(s_0)`एक शोर-पुरस्कार ग्रिडवर्ल्ड पर डबल डीक्यूएन के बिना बनाम के साथ 1,000 एपिसोड के बाद।

## कीवर्ड्स  शब्द खोज तालिका

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

## आगे पढ़ना 延伸閱讀

- [Mnih et al. (2013). Playing Atari with Deep Reinforcement Learning](https://arxiv.org/abs/1312.5602) 2013 न्यूरआईपीएस कार्यशाला पेपर जो गहरे आरएल की शुरुआत करता है।
- [Mnih et al. (2015). Human-level control through deep reinforcement learning](https://www.nature.com/articles/nature14236) प्रकृति पेपर, 49-गेम डीक्यूएन।
- [Hasselt, Guez, Silver (2016). Deep Reinforcement Learning with Double Q-learning](https://arxiv.org/abs/1509.06461) डीडीक्यूएन।
- [Wang et al. (2016). Dueling Network Architectures](https://arxiv.org/abs/1511.06581) ड्यूलिंग डीक्यूएन।
- [Hessel et al. (2018). Rainbow: Combining Improvements in Deep RL](https://arxiv.org/abs/1710.02298) ढेर-ट्रिक कागज।
- [OpenAI Spinning Up — DQN](https://spinningup.openai.com/en/latest/algorithms/dqn.html) स्पष्ट आधुनिक प्रदर्शनी।
- [Sutton & Barto (2018). Ch. 9 — On-policy Prediction with Approximation](http://incompleteideas.net/book/RLbook2020.pdf) "मृत्युलयी त्रयी" (फंक्शन अप्रोक्सिमेशन + बूटस्ट्रेपिंग + ऑफ पॉलिसी) के पाठ्यपुस्तक उपचार को DQN के लक्षित नेटवर्क और रिप्ले बफर को tame करने के लिए डिज़ाइन किया गया है।
- [CleanRL DQN implementation](https://docs.cleanrl.dev/rl-algorithms/dqn/) अपघटन अध्ययनों में इस्तेमाल किए जाने वाले संदर्भ एकल-फ़ाइल डीक्यूएन; इस पाठ के साथ-साथ पढ़ना अच्छा है।
